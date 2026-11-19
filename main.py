#!/usr/bin/env python3
"""Copy the pre-rendered front page to the make.fun output directory."""

import os
import shutil


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "frontpage.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
