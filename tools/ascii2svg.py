#!/usr/bin/env python3
"""
ascii2svg.py — render a .txt file of ASCII art as an .svg with a transparent background.

Usage:
    python ascii2svg.py art/name.txt -o art/name.svg
"""

import argparse
import sys
from xml.sax.saxutils import escape

FONT_SIZE = 10
LINE_HEIGHT = 12
FILL = "#c9d1d9"

# Monospace glyphs advance about 0.6em, so each column is 6px at font-size 10.
CHAR_WIDTH = FONT_SIZE * 0.6


def to_svg(lines: list) -> str:
    cols = max((len(line) for line in lines), default=0)
    width = int(round(cols * CHAR_WIDTH))
    height = len(lines) * LINE_HEIGHT

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        f'<g font-family="monospace" font-size="{FONT_SIZE}" fill="{FILL}" xml:space="preserve" style="white-space:pre">',
    ]
    for i, line in enumerate(lines):
        # y is the text baseline; sit it near the bottom of each 12px row
        y = (i + 1) * LINE_HEIGHT - (LINE_HEIGHT - FONT_SIZE)
        out.append(f'<text x="0" y="{y}">{escape(line)}</text>')
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="Render ASCII art from a .txt file as an .svg.")
    p.add_argument("text", help="path to a .txt file of ASCII art")
    p.add_argument("-o", "--output", required=True, help="write the .svg to this path")
    args = p.parse_args()

    try:
        with open(args.text, encoding="utf-8") as f:
            lines = f.read().rstrip("\n").split("\n")
    except OSError as e:
        print(f"could not read {args.text}: {e}", file=sys.stderr)
        return 1

    svg = to_svg(lines)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {args.output} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
