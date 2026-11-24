#!/usr/bin/env python3
"""Refresh the generated token block in every example page.

Each example has a block `/* tokens:start <direction> */ ... /* tokens:end */` inside its <style>.
This script replaces the block's contents with the current output of tokens.py for that direction,
so examples never drift from the token generator. CI runs it and fails if anything changed.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import tokens  # noqa: E402

BLOCK = re.compile(r"(/\* tokens:start ([\w-]+) \*/\n)(.*?)(/\* tokens:end \*/)", re.S)


def refresh(text):
    return BLOCK.sub(lambda m: m.group(1) + tokens.to_css(tokens.build(m.group(2))) + m.group(4), text)


def main():
    changed = 0
    for page in sorted(HERE.glob("*.html")):
        old = page.read_text()
        new = refresh(old)
        if new != old:
            page.write_text(new)
            changed += 1
            print(f"updated {page.name}")
    print(f"{changed} example(s) updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
