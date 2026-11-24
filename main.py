"""news-image-20261124 entry (Python 3.13, standard library only).

Copies the front-page image for Tuesday 24 November 2026, held in
``entry.png`` next to this file, to ``$MAKEFUN_OUTPUT_DIR/entry.png``
(``/output`` when the variable is unset, matching the grader container).

Run it from the repository root, for example:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

The copy is byte-for-byte and deterministic: the same input image always
produces the same output file. After copying, the program verifies the
destination's size and SHA-256 hash against the source and fails loudly
if either differs, so a truncated or corrupted write can never pass
silently.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip() or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / SOURCE_NAME
    if dest.resolve() == source.resolve():
        print("error: output directory is the repository itself", file=sys.stderr)
        return 1
    shutil.copyfile(source, dest)
    if dest.stat().st_size != source.stat().st_size:
        print("error: copied file size differs from source", file=sys.stderr)
        return 1
    if _sha256(dest) != _sha256(source):
        print("error: copied file hash differs from source", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({dest.stat().st_size} bytes, sha256 verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
