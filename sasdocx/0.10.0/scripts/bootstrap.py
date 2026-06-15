# SPDX-License-Identifier: MIT
"""First-use dependency bootstrap for SASdocX.

Stdlib-only by design: it must run BEFORE the engine's third-party
dependencies (python-docx, python-pptx, openpyxl, lxml, Pillow) are present,
so it cannot import the engine itself.

Behaviour:
  * ``python scripts/bootstrap.py``          -> install missing requirements (no-op if all present)
  * ``python scripts/bootstrap.py --check``  -> report only; exit 0 if ready, 3 if missing

On first use the SASdocX skills run this as their very first preflight step, so
the Python requirements install automatically. The install is performed by
``python -m pip install -r requirements.txt`` in THIS interpreter; because the
agent must run this command, the user authorises it through the normal
permission prompt. Once everything is installed it is an idempotent no-op.
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

# import-name -> the distribution that provides it (for human-readable output).
REQUIRED = {
    "docx": "python-docx",
    "pptx": "python-pptx",
    "openpyxl": "openpyxl",
    "lxml": "lxml",
    "PIL": "Pillow",
}

ROOT = Path(__file__).resolve().parent.parent  # scripts/ -> plugin root
REQUIREMENTS = ROOT / "requirements.txt"


def _missing() -> list[str]:
    """Return the import names of any required package that cannot be found."""
    return [name for name in REQUIRED if importlib.util.find_spec(name) is None]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sasdocx-bootstrap",
        description="Install SASdocX's Python requirements on first use.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="report readiness only; do not install (exit 3 if requirements are missing)",
    )
    args = parser.parse_args(argv)

    missing = _missing()
    if not missing:
        print("SASdocX dependencies: ok (all required Python packages present)")
        return 0

    pretty = ", ".join(sorted(REQUIRED[name] for name in missing))
    if args.check:
        print(f"SASdocX dependencies: MISSING ({pretty})")
        print(f"install with: python {Path(__file__).name} (run from {ROOT})")
        return 3

    if not REQUIREMENTS.is_file():
        print(f"SASdocX bootstrap: cannot find {REQUIREMENTS}", file=sys.stderr)
        return 1

    print(f"SASdocX: installing missing Python requirements ({pretty})...")
    print(f"  running: {sys.executable} -m pip install -r {REQUIREMENTS}")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)],
        check=False,
    )
    if result.returncode != 0:
        print(
            "SASdocX bootstrap: pip install failed. If your environment manages "
            "packages externally, install the contents of requirements.txt "
            "manually, then re-run.",
            file=sys.stderr,
        )
        return result.returncode

    still_missing = _missing()
    if still_missing:
        pretty2 = ", ".join(sorted(REQUIRED[name] for name in still_missing))
        print(
            f"SASdocX bootstrap: still missing after install ({pretty2}). "
            "Check that pip targeted this interpreter: " + sys.executable,
            file=sys.stderr,
        )
        return 1

    print("SASdocX dependencies: installed and ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
