#!/usr/bin/env python3
"""ensemble_common.py — shared Python helpers for the Ensemble consultant skills.

The coherence anchor for every consultant skill script. Stdlib ONLY (no pyyaml, no
pip installs) so the skills run anywhere python3 runs. Every public function is
documented with its signature and behaviour; the companion README.md mirrors this.

Responsibilities owned here (do NOT duplicate in individual skills):
  * Resolve the engagement repo root and load its ``.ensemble/project.json``.
  * Parse a handoff packet's YAML-ish front-matter (scalars + simple lists) with no
    third-party YAML dependency.
  * Validate that front-matter against the engagement repo's
    ``schemas/packet.schema.json`` — a minimal JSON-Schema subset covering
    required / type / enum / pattern / minItems.
  * Read/write the per-user state files under ``~/.ensemble`` (tethers.json,
    collected.json, config.json + registry) with safe defaults.

Conventions (see SHARED CONTRACT):
  * State lives under ~/.ensemble (mode 0700).
  * A packet file is markdown: ``---`` front-matter ``---`` then a ``## Brief`` body.
  * The single source of truth for packet shape is the engagement repo's
    schemas/packet.schema.json — we re-use it, never re-spell the rules here.

All user-facing strings use Australian English.
"""
from __future__ import annotations

import json
import os
import re
import stat
from pathlib import Path
from typing import Any

__all__ = [
    "ENSEMBLE_HOME",
    "ensemble_home",
    "config_path",
    "registry_dir",
    "registry_path",
    "heartbeat_path",
    "tethers_path",
    "collected_path",
    "load_json",
    "save_json",
    "load_config",
    "config_get",
    "config_set",
    "DEFAULT_REGISTRY_REPO",
    "registry_repo",
    "load_registry",
    "find_repo_root",
    "load_project",
    "project_field",
    "require_tethered",
    "parse_front_matter",
    "split_packet",
    "validate_packet",
    "EnsembleError",
]


class EnsembleError(Exception):
    """Raised for any recoverable Ensemble error. Callers should print
    ``str(exc)`` to stderr and exit non-zero. Never carries secrets."""


# ---------------------------------------------------------------------------
# ~/.ensemble state locations
# ---------------------------------------------------------------------------

#: The per-user Ensemble state directory. Mirrors ens_home in the bash lib.
ENSEMBLE_HOME = Path(os.path.expanduser("~")) / ".ensemble"


def ensemble_home() -> Path:
    """Return the ~/.ensemble state directory, creating it with mode 0700 if absent.

    Returns:
        Path: the absolute path to ~/.ensemble (guaranteed to exist, mode 0700).
    """
    ENSEMBLE_HOME.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        os.chmod(ENSEMBLE_HOME, 0o700)
    except OSError:
        # Best effort — a pre-existing dir we cannot chmod should not be fatal.
        pass
    return ENSEMBLE_HOME


def config_path() -> Path:
    """Path to ~/.ensemble/config.json (may not exist)."""
    return ensemble_home() / "config.json"


def registry_dir() -> Path:
    """Path to ~/.ensemble/registry (the shallow clone of sasam-registry; may not exist)."""
    return ensemble_home() / "registry"


def registry_path() -> Path:
    """Path to ~/.ensemble/registry/registry.json (may not exist)."""
    return registry_dir() / "registry.json"


def heartbeat_path() -> Path:
    """Path to ~/.ensemble/registry/heartbeat.json (may not exist)."""
    return registry_dir() / "heartbeat.json"


def tethers_path() -> Path:
    """Path to ~/.ensemble/tethers.json (may not exist)."""
    return ensemble_home() / "tethers.json"


def collected_path() -> Path:
    """Path to ~/.ensemble/collected.json (may not exist)."""
    return ensemble_home() / "collected.json"


# ---------------------------------------------------------------------------
# JSON read/write with safe defaults
# ---------------------------------------------------------------------------


def load_json(path: str | os.PathLike[str], default: Any = None) -> Any:
    """Load JSON from ``path``, returning ``default`` if the file is absent.

    A present-but-corrupt file is an error (raises EnsembleError) rather than a
    silent reset — we never clobber the user's state on a parse glitch.

    Args:
        path: file to read.
        default: value returned when the file does not exist (default ``None``).

    Returns:
        The parsed JSON object, or ``default`` when the file is missing.

    Raises:
        EnsembleError: if the file exists but contains invalid JSON.
    """
    p = Path(path)
    if not p.exists():
        return default
    try:
        with p.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise EnsembleError(f"could not read JSON from {p}: {exc}") from exc


def save_json(path: str | os.PathLike[str], obj: Any) -> Path:
    """Atomically write ``obj`` as pretty JSON to ``path``.

    Writes to a temp file in the same directory then renames, so a crash mid-write
    cannot truncate existing state. Creates parent directories as needed. When the
    target sits under ~/.ensemble the file is given mode 0600.

    Args:
        path: destination file.
        obj: any JSON-serialisable object.

    Returns:
        Path: the written file path.

    Raises:
        EnsembleError: if the object cannot be serialised or written.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    try:
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, p)
    except (OSError, TypeError, ValueError) as exc:
        try:
            tmp.unlink()
        except OSError:
            pass
        raise EnsembleError(f"could not write JSON to {p}: {exc}") from exc
    # Tighten perms for state under ~/.ensemble (it may hold a registry URL).
    try:
        if ENSEMBLE_HOME in p.parents:
            os.chmod(p, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass
    return p


# ---------------------------------------------------------------------------
# config.json + registry
# ---------------------------------------------------------------------------


def load_config() -> dict[str, Any]:
    """Load ~/.ensemble/config.json, or {} if it does not exist.

    Returns:
        dict: the config (e.g. {"registry_repo": "..."}), or {} when absent.
    """
    data = load_json(config_path(), default={})
    return data if isinstance(data, dict) else {}


def config_get(key: str, default: Any = None) -> Any:
    """Return a single key from ~/.ensemble/config.json.

    Args:
        key: the config key (e.g. "registry_repo").
        default: returned if the key (or the whole file) is absent.

    Returns:
        The config value, or ``default``.
    """
    return load_config().get(key, default)


def config_set(key: str, value: Any) -> None:
    """Set a single key in ~/.ensemble/config.json, preserving other keys.

    Best-effort: a write failure is swallowed (callers fall back to the in-memory
    value) so a read-only home never breaks a skill.
    """
    cfg = load_config()
    cfg[key] = value
    try:
        save_json(config_path(), cfg)
    except Exception:
        pass


#: The SAS-AM shared registry, used when ~/.ensemble/config.json does not pin one.
#: A bare ``owner/repo`` slug — the skills resolve it to an HTTPS URL, so a consultant
#: who has run ``gh auth login`` can clone it with no SSH key.
DEFAULT_REGISTRY_REPO = "SAS-Asset-Management/sasam-registry"


def registry_repo() -> str:
    """Resolve the registry repo, with a sensible SAS-AM default.

    Returns the ``registry_repo`` pinned in ~/.ensemble/config.json if present;
    otherwise returns (and persists) :data:`DEFAULT_REGISTRY_REPO` so a brand-new
    consultant never has to configure anything by hand. Persisting the default
    makes the choice explicit and keeps every skill (tether/sync/status) in step.
    """
    val = config_get("registry_repo")
    if val:
        return str(val)
    config_set("registry_repo", DEFAULT_REGISTRY_REPO)
    return DEFAULT_REGISTRY_REPO


def load_registry() -> dict[str, Any]:
    """Load the registry.json from ~/.ensemble/registry, or {"projects": []}.

    Returns:
        dict: the registry document; always has a "projects" list key.
    """
    data = load_json(registry_path(), default={"projects": []})
    if not isinstance(data, dict):
        return {"projects": []}
    data.setdefault("projects", [])
    return data


# ---------------------------------------------------------------------------
# engagement repo root + project.json
# ---------------------------------------------------------------------------


def find_repo_root(start: str | os.PathLike[str] | None = None) -> Path:
    """Locate the engagement repo root from ``start`` (default: cwd).

    Walks upward looking first for ``.ensemble/project.json`` (the authoritative
    marker of an engagement repo), then for ``.git`` as a fallback. Pure-stdlib so
    it works even when git is unavailable.

    Args:
        start: directory to begin the search from (default: current directory).

    Returns:
        Path: the repo root.

    Raises:
        EnsembleError: if no repo root can be found.
    """
    cur = Path(start or Path.cwd()).resolve()
    for d in (cur, *cur.parents):
        if (d / ".ensemble" / "project.json").is_file():
            return d
    for d in (cur, *cur.parents):
        if (d / ".git").exists():
            return d
    raise EnsembleError(
        "not inside a git repository (no .ensemble/project.json or .git found). "
        "cd into an engagement repo first."
    )


def load_project(root: str | os.PathLike[str]) -> dict[str, Any]:
    """Load ``.ensemble/project.json`` from an engagement repo root.

    Args:
        root: the engagement repo root directory.

    Returns:
        dict: the parsed project descriptor
            ({uuid, name, scope_tag, repo, bucket, consultants, review_defaults, ...}).

    Raises:
        EnsembleError: if the file is missing (not a tethered engagement repo) or
            is not a valid JSON object.
    """
    proj_path = Path(root) / ".ensemble" / "project.json"
    if not proj_path.is_file():
        raise EnsembleError(
            f"{proj_path} not found — this is not an Ensemble engagement repo. "
            "Tether it first (or cd into one)."
        )
    data = load_json(proj_path)
    if not isinstance(data, dict):
        raise EnsembleError(f"{proj_path} is not a JSON object")
    return data


def project_field(key: str, root: str | os.PathLike[str] | None = None) -> Any:
    """Return a single field from the engagement repo's project.json.

    Args:
        key: the project.json key (e.g. "scope_tag", "uuid", "repo", "bucket").
        root: engagement repo root; auto-discovered from cwd if omitted.

    Returns:
        The field value (None if the key is absent).
    """
    return load_project(root or find_repo_root()).get(key)


def require_tethered(root: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    """Assert we are inside a tethered engagement repo, returning its project.json.

    A skill that mutates engagement state must call this first.

    Args:
        root: engagement repo root; auto-discovered from cwd if omitted.

    Returns:
        dict: the project.json contents.

    Raises:
        EnsembleError: if not in a tethered engagement repo.
    """
    return load_project(root or find_repo_root())


# ---------------------------------------------------------------------------
# packet front-matter parsing + schema validation
# ---------------------------------------------------------------------------

# A scalar "key: value" line, e.g.  review_tier: full
_SCALAR_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$")
# A flow list, e.g.  inputs: [a.md, "b c.md"]
_FLOW_LIST_RE = re.compile(r"^\[(.*)\]$")
# A block list item, e.g.  "  - first criterion"
_LIST_ITEM_RE = re.compile(r"^\s*-\s+(.*?)\s*$")


def _coerce_scalar(raw: str) -> Any:
    """Best-effort YAML-ish scalar coercion: int, bool, null, else stripped string."""
    s = raw.strip()
    if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in "\"'"):
        return s[1:-1]
    low = s.lower()
    if low in ("null", "~", ""):
        return None if low in ("null", "~") else ""
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if re.fullmatch(r"-?\d+", s):
        try:
            return int(s)
        except ValueError:
            return s
    return s


def _split_flow_list(inner: str) -> list[Any]:
    """Split the inside of a ``[ ... ]`` flow list, honouring simple quoting."""
    items: list[Any] = []
    buf = ""
    quote: str | None = None
    for ch in inner:
        if quote:
            if ch == quote:
                quote = None
            else:
                buf += ch
        elif ch in "\"'":
            quote = ch
        elif ch == ",":
            if buf.strip():
                items.append(_coerce_scalar(buf))
            buf = ""
        else:
            buf += ch
    if buf.strip():
        items.append(_coerce_scalar(buf))
    return items


def parse_front_matter(text: str) -> dict[str, Any]:
    """Parse a packet's YAML-ish front-matter into a dict (stdlib only — no pyyaml).

    Supports the subset the packet schema needs:
      * scalar fields            ``key: value``  (str/int/bool/null coerced)
      * flow lists               ``key: [a, b]``
      * block lists              ``key:`` then ``  - item`` lines

    The front-matter is the leading ``---`` ... ``---`` fence; anything after it
    (the markdown ``## Brief`` body) is ignored here — use :func:`split_packet` to
    get the body.

    Args:
        text: the full packet file contents.

    Returns:
        dict: the parsed front-matter mapping.

    Raises:
        EnsembleError: if there is no opening fence or it is never closed.
    """
    stripped = text.lstrip()
    if not stripped.startswith("---"):
        raise EnsembleError("packet has no YAML front-matter (missing opening '---')")
    parts = stripped.split("---", 2)
    if len(parts) < 3:
        raise EnsembleError("packet front-matter is not closed (missing second '---')")
    block = parts[1]

    fm: dict[str, Any] = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = _SCALAR_RE.match(line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2)

        if val == "" or val is None:
            # Possible block list: gather following "  - item" lines.
            items: list[Any] = []
            j = i + 1
            while j < len(lines) and _LIST_ITEM_RE.match(lines[j]):
                items.append(_coerce_scalar(_LIST_ITEM_RE.match(lines[j]).group(1)))
                j += 1
            if items:
                fm[key] = items
                i = j
                continue
            fm[key] = None
            i += 1
            continue

        # Strip a trailing inline comment that is not inside quotes/brackets.
        flow = _FLOW_LIST_RE.match(val)
        if flow:
            fm[key] = _split_flow_list(flow.group(1))
        else:
            fm[key] = _coerce_scalar(val)
        i += 1
    return fm


def split_packet(text: str) -> tuple[dict[str, Any], str]:
    """Split a packet into (front_matter, brief_body).

    The body is everything after the ``## Brief`` heading; if that heading is
    absent the body is everything after the closing ``---`` fence.

    Args:
        text: the full packet file contents.

    Returns:
        tuple: (parsed front-matter dict, brief body string).
    """
    fm = parse_front_matter(text)
    stripped = text.lstrip()
    after_fence = stripped.split("---", 2)[2] if stripped.count("---") >= 2 else ""
    m = re.search(r"^##\s+Brief\s*$", after_fence, flags=re.MULTILINE)
    body = after_fence[m.end():] if m else after_fence
    return fm, body.strip()


# ---- minimal JSON-Schema validator (required / type / enum / pattern / minItems) ----

_JSON_TYPE_OK = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
    "null": lambda v: v is None,
}


def _check_value(name: str, value: Any, spec: dict[str, Any]) -> list[str]:
    """Validate one value against one property spec; return a list of error strings."""
    errs: list[str] = []

    jtype = spec.get("type")
    if jtype and jtype in _JSON_TYPE_OK and not _JSON_TYPE_OK[jtype](value):
        errs.append(f"{name}: expected {jtype}, got {type(value).__name__}")
        # Type is wrong — downstream checks would be noise.
        return errs

    if "enum" in spec and value not in spec["enum"]:
        errs.append(f"{name}: {value!r} is not one of {spec['enum']}")

    if "pattern" in spec and isinstance(value, str):
        if not re.search(spec["pattern"], value):
            errs.append(f"{name}: {value!r} does not match pattern {spec['pattern']}")

    if jtype == "string" and isinstance(value, str):
        if "minLength" in spec and len(value) < spec["minLength"]:
            errs.append(f"{name}: shorter than minLength {spec['minLength']}")

    if jtype == "integer" and isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in spec and value < spec["minimum"]:
            errs.append(f"{name}: {value} is below minimum {spec['minimum']}")

    if jtype == "array" and isinstance(value, list):
        if "minItems" in spec and len(value) < spec["minItems"]:
            errs.append(f"{name}: needs at least {spec['minItems']} item(s), got {len(value)}")
        item_spec = spec.get("items")
        if isinstance(item_spec, dict):
            for idx, item in enumerate(value):
                errs.extend(_check_value(f"{name}[{idx}]", item, item_spec))

    return errs


def validate_packet(fm: dict[str, Any], schema_path: str | os.PathLike[str]) -> list[str]:
    """Validate parsed packet front-matter against the engagement repo's packet schema.

    Re-uses the engagement repo's ``schemas/packet.schema.json`` as the single source
    of truth — this is a minimal JSON-Schema subset validator covering exactly the
    constraints that schema uses: ``required``, per-property ``type``, ``enum``,
    ``pattern``, ``minLength``, ``minimum``, ``minItems``, array ``items``, and
    ``additionalProperties: false``.

    Args:
        fm: the front-matter dict from :func:`parse_front_matter`.
        schema_path: path to the engagement repo's schemas/packet.schema.json.

    Returns:
        list[str]: human-readable error strings. An EMPTY list means the packet is
            valid. (Returning errors rather than raising lets a skill present all
            problems at once.)

    Raises:
        EnsembleError: only if the schema file itself cannot be read/parsed.
    """
    schema = load_json(schema_path)
    if schema is None:
        raise EnsembleError(f"packet schema not found at {schema_path}")
    if not isinstance(schema, dict):
        raise EnsembleError(f"packet schema at {schema_path} is not a JSON object")

    errors: list[str] = []
    props: dict[str, Any] = schema.get("properties", {})

    for req in schema.get("required", []):
        if req not in fm or fm[req] is None:
            errors.append(f"{req}: required field is missing")

    if schema.get("additionalProperties") is False:
        for key in fm:
            if key not in props:
                errors.append(f"{key}: unknown field (additionalProperties is false)")

    for key, value in fm.items():
        spec = props.get(key)
        if isinstance(spec, dict) and value is not None:
            errors.extend(_check_value(key, value, spec))

    return errors


if __name__ == "__main__":  # pragma: no cover - tiny self-check / CLI smoke test
    import sys

    if len(sys.argv) >= 2 and sys.argv[1] == "--self-check":
        sample = (
            "---\n"
            "id: HX-2026-0610-demo\n"
            "engagement: acme-water\n"
            "requested_by: scriv\n"
            "kind: project\n"
            "review_tier: full\n"
            "route_hint: api\n"
            "deadline: none\n"
            "inputs: [brief.md, \"two words.md\"]\n"
            "definition_of_done:\n"
            "  - first criterion\n"
            "  - second criterion\n"
            "retries: 0\n"
            "---\n"
            "## Brief\n"
            "Body text here.\n"
        )
        front, brief = split_packet(sample)
        print(json.dumps(front, indent=2))
        print("BRIEF:", brief)
        sys.exit(0)
    print("ensemble_common.py — import this module; run with --self-check to smoke-test.",
          file=sys.stderr)
    sys.exit(2)
