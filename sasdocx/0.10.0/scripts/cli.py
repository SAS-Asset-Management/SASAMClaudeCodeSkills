# SPDX-License-Identifier: MIT
"""Engine launcher (repo/plugin ROOT copy).

The same launcher each skill ships at ``skills/<skill>/scripts/cli.py``: it
resolves the engine root wherever the caller's working directory is (the skill
folder, the repo root, or the plugin cache), so ``python scripts/cli.py ...``
is the ONE invocation every doc can teach. ``SASDOCX_ROOT`` overrides the
detection.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _root(start: Path) -> Path:
    env_root = os.environ.get("SASDOCX_ROOT")
    if env_root:
        root = Path(env_root).expanduser().resolve()
        if (root / "scripts" / "sasdockit").is_dir():
            return root

    for parent in [start] + list(start.parents):
        if (parent / ".claude-plugin").is_dir():
            return parent
    return start.parents[1]


ROOT = _root(Path(__file__).resolve())
sys.path.insert(0, str(ROOT / "scripts"))

_THIRD_PARTY = {"docx", "pptx", "openpyxl", "lxml", "PIL"}
try:
    from sasdockit.cli import main  # noqa: E402
except ModuleNotFoundError as exc:  # missing runtime dependency on first use
    if (exc.name or "").split(".")[0] in _THIRD_PARTY:
        sys.stderr.write(
            "SASdocX: required Python dependency '%s' is not installed.\n"
            "Run the one-time bootstrap to install requirements (you will be "
            "asked to authorize):\n    python %s\n"
            % (exc.name, ROOT / "scripts" / "bootstrap.py")
        )
        raise SystemExit(3) from None
    raise

if __name__ == "__main__":
    raise SystemExit(main())
