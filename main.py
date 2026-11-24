#!/usr/bin/env python3
"""Entry for make.fun news-image-20261124.

The finished front page is stored beside this file as entry.png
(it was drawn at build time from the 24 November 2026 headlines).
This program only copies those exact bytes to /output/entry.png,
so it needs no network, no extra packages and no randomness:
running it twice produces identical output.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    size = os.path.getsize(target)
    print(f"wrote {target} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
