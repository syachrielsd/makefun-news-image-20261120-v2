#!/usr/bin/env python3
"""Copy-only entrypoint for the news-image-20261120 v2 entry.

The front page is rendered at build time by render.py and committed as
entry.png; this program only hands that file to the grader's output
directory. It resolves the image from its own directory (never the
working directory) and uses only the standard library, so both grader
runs write byte-identical output.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(HERE / "entry.png", dst)
    print(f"handed over entry.png -> {dst}")


if __name__ == "__main__":
    main()
