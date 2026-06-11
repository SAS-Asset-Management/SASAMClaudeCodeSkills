# `_lib` — shared library for the Ensemble consultant skills

Every consultant skill under `deploy/skills/ensemble/<skill>/` sources **one** of
these two files and reuses its helpers — no skill re-implements packet parsing,
schema validation, repo resolution, or `~/.ensemble` state I/O.

- **`ensemble_common.sh`** — bash functions for skill shell scripts.
- **`ensemble_common.py`** — Python helpers (the coherence anchor); stdlib only,
  no `pyyaml`, no pip installs.
- The bash lib shells out to the Python lib for anything non-trivial (state I/O,
  project.json reads), so the two halves can never disagree.

**Tooling:** bash + `python3` (stdlib) + `git` (+ `gh` / `git-lfs` where a skill
needs them). **No** pip installs, no other dependencies. All user-facing strings are
in Australian English. Helpers print errors to **stderr** and exit non-zero on
failure, and **never** print secrets/tokens.

## How a skill consumes the lib

```bash
#!/usr/bin/env bash
set -euo pipefail
_LIB="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../_lib" && pwd)"
# shellcheck source=/dev/null
. "$_LIB/ensemble_common.sh"

ens_have git
ROOT="$(ens_require_tethered)"          # die unless in a tethered engagement repo
SCOPE="$(ens_project_field scope_tag)"  # read a scalar from .ensemble/project.json
REG="$(ens_config_get registry_repo)" || exit 1   # prints a set-it hint if unset
```

Sourcing `ensemble_common.sh` prepends this `_lib` dir to `PYTHONPATH`, so any
`python3 -c 'import ensemble_common ...'` inside the skill resolves the module.

```python
# In a python script shipped beside a skill (PYTHONPATH set by the .sh, or add it
# yourself), or invoked via `python3 -c` from a sourced bash skill:
import ensemble_common as e
root = e.find_repo_root()
proj = e.require_tethered(root)
fm, brief = e.split_packet(open(packet_path).read())
errs = e.validate_packet(fm, f"{root}/schemas/packet.schema.json")
```

---

## `~/.ensemble` state layout (owned by this lib)

| Path | Purpose |
| --- | --- |
| `~/.ensemble/` | state root, **mode 0700**, created on first use |
| `~/.ensemble/config.json` | `{"registry_repo": "<git url or owner/sasam-registry>"}` |
| `~/.ensemble/registry/` | shallow clone/pull of `sasam-registry` |
| `~/.ensemble/registry/registry.json` | `{"projects":[{uuid,name,scope_tag,repo,status}]}` |
| `~/.ensemble/registry/heartbeat.json` | `{ts,repos_polled,claims,errors:[...]}` |
| `~/.ensemble/tethers.json` | `{"tethers":[{uuid,name,scope_tag,path,repo,tethered_at}]}` |
| `~/.ensemble/collected.json` | `{"collected":[{id,engagement,collected_at,paths:[...]}]}` |

State files written under `~/.ensemble` are saved atomically at **mode 0600**.

---

## `ensemble_common.sh` — bash functions

| Function | Signature | Behaviour |
| --- | --- | --- |
| `ens_die` | `ens_die <msg...>` | Print `ensemble: <msg>` to **stderr** and `exit 1`. The fatal-path primitive for every other function. |
| `ens_have` | `ens_have <cmd>` | Return 0 if `<cmd>` is on `PATH`; otherwise `ens_die` with a one-line install hint. Known hints: `git`, `gh`, `git-lfs`, `python3`. |
| `ens_home` | `ens_home` | **Echo** `~/.ensemble`, creating it at **mode 0700** if absent (idempotent). Delegates to the Python lib so bash and Python agree on the path/permissions. |
| `ens_repo_root` | `ens_repo_root` | **Echo** the engagement repo root. Prefers `git rev-parse --show-toplevel`; falls back to the Python walk-up (which also honours `.ensemble/project.json`). Dies if no repo is found. |
| `ens_require_tethered` | `ens_require_tethered` | Die unless `.ensemble/project.json` exists at the repo root. On success **echoes the repo root** (use `ROOT="$(ens_require_tethered)"`). Call at the top of any skill that mutates engagement state. |
| `ens_project_field` | `ens_project_field <key>` | **Echo** a scalar field from the engagement repo's `.ensemble/project.json` (via the Python lib). Dies if not in a tethered repo. A missing key echoes an **empty line**. e.g. `ens_project_field scope_tag`. |
| `ens_config_get` | `ens_config_get <key>` | **Echo** one key from `~/.ensemble/config.json`. If the file or key is absent/empty, print a one-line **set-it hint** to stderr and **exit non-zero** — so a skill needing e.g. `registry_repo` fails loudly and actionably. Use `val="$(ens_config_get registry_repo)" || exit 1`. |

**Side effect on source:** prepends this `_lib` dir to `PYTHONPATH` (idempotently)
so `import ensemble_common` resolves for the helpers above and for any ad-hoc
`python3 -c` in the consuming skill. Also exports `ENS_LIB_DIR` and `ENS_PY`.

---

## `ensemble_common.py` — Python functions

Stdlib only. Public API is listed in `__all__`. Recoverable failures raise
`EnsembleError`; callers print `str(exc)` to stderr and exit non-zero.

### Errors

| Name | Signature | Behaviour |
| --- | --- | --- |
| `EnsembleError` | `class EnsembleError(Exception)` | Raised for any recoverable error. Carries a human-readable, **secret-free** message. |

### `~/.ensemble` paths and state I/O

| Function | Signature | Behaviour |
| --- | --- | --- |
| `ensemble_home` | `ensemble_home() -> Path` | Return `~/.ensemble`, creating it at mode 0700 if absent (idempotent). |
| `config_path` | `config_path() -> Path` | Path to `~/.ensemble/config.json` (may not exist). |
| `registry_dir` | `registry_dir() -> Path` | Path to `~/.ensemble/registry/`. |
| `registry_path` | `registry_path() -> Path` | Path to `~/.ensemble/registry/registry.json`. |
| `heartbeat_path` | `heartbeat_path() -> Path` | Path to `~/.ensemble/registry/heartbeat.json`. |
| `tethers_path` | `tethers_path() -> Path` | Path to `~/.ensemble/tethers.json`. |
| `collected_path` | `collected_path() -> Path` | Path to `~/.ensemble/collected.json`. |
| `load_json` | `load_json(path, default=None) -> Any` | Load JSON from `path`; return `default` when the file is **absent**. A present-but-corrupt file raises `EnsembleError` (never silently reset). |
| `save_json` | `save_json(path, obj) -> Path` | **Atomically** write `obj` as pretty JSON (temp file + `os.replace`). Creates parent dirs. Files under `~/.ensemble` are chmod 0600. Returns the written path; raises `EnsembleError` on failure. |
| `load_config` | `load_config() -> dict` | Load `~/.ensemble/config.json`, or `{}` if absent / not an object. |
| `config_get` | `config_get(key, default=None) -> Any` | One key from `config.json`, or `default`. |
| `load_registry` | `load_registry() -> dict` | Load `registry.json`, or `{"projects": []}`. Always has a `"projects"` list. |

### Engagement repo + `project.json`

| Function | Signature | Behaviour |
| --- | --- | --- |
| `find_repo_root` | `find_repo_root(start=None) -> Path` | Walk upward from `start` (default cwd) for `.ensemble/project.json`, then `.git`. Pure stdlib (works without git). Raises `EnsembleError` if none found. |
| `load_project` | `load_project(root) -> dict` | Load `.ensemble/project.json` from an engagement repo root → `{uuid,name,scope_tag,repo,bucket,consultants,review_defaults,...}`. Raises `EnsembleError` if missing (not tethered) or not an object. |
| `project_field` | `project_field(key, root=None) -> Any` | One field from `project.json`; auto-discovers `root` from cwd. `None` if the key is absent. |
| `require_tethered` | `require_tethered(root=None) -> dict` | Assert we are in a tethered engagement repo; return its `project.json`. Raises `EnsembleError` otherwise. Call first in any state-mutating skill. |

### Packet front-matter + schema validation

| Function | Signature | Behaviour |
| --- | --- | --- |
| `parse_front_matter` | `parse_front_matter(text) -> dict` | Parse a packet's leading `---`…`---` front-matter (stdlib, no pyyaml). Supports **scalars** (`key: value`, with str/int/bool/null coercion), **flow lists** (`key: [a, b]`), and **block lists** (`key:` then `  - item`). Ignores comment/blank lines and the body. Raises `EnsembleError` if the fence is missing/unclosed. |
| `split_packet` | `split_packet(text) -> tuple[dict, str]` | Return `(front_matter, brief_body)`. Body = everything after the `## Brief` heading (or after the closing fence if absent). |
| `validate_packet` | `validate_packet(fm, schema_path) -> list[str]` | Validate parsed front-matter against the **engagement repo's** `schemas/packet.schema.json` (the single source of truth). Minimal JSON-Schema subset: `required`, per-property `type`, `enum`, `pattern`, `minLength`, `minimum`, `minItems`, array `items`, and `additionalProperties: false`. Returns a list of error strings — **empty means valid** (so a skill can show all problems at once). Raises `EnsembleError` only if the schema file itself can't be read/parsed. |

#### Validator scope (deliberate)

The validator covers exactly the constraints used by the live packet schema
(`schemas/packet.schema.json`): `required`, `type`, `enum`, `pattern`, `minLength`,
`minimum`, `minItems`, array `items`, `additionalProperties: false`. It is **not** a
general JSON-Schema engine (no `$ref`, `allOf`, `oneOf`, `dependentRequired`, etc.).
The engagement repo's CI (`tier-gate.yml`) remains the authoritative gate; this
client-side check exists so a consultant catches a malformed packet **before**
pushing it to the `queue` branch.

---

## Self-check

```bash
python3 ensemble_common.py --self-check    # parses a sample packet, prints front-matter + brief
bash -n ensemble_common.sh                 # syntax-only check of the bash lib
```
