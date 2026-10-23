#!/usr/bin/env python3
"""
img2ascii.py — convert any image into real, pasteable ASCII art.

Usage:
    python img2ascii.py input.png                 # prints to terminal
    python img2ascii.py input.png -o art.txt      # saves as text (commit this)
    python img2ascii.py input.png -w 120 --invert # wider, inverted for light bg

Install once:  pip install pillow
"""

import argparse
import sys

from PIL import Image, ImageOps

# Dense ramp: darkest glyph first. Works for white text on a black background.
RAMP = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Monospace glyphs are roughly twice as tall as they are wide, so each
# character cell samples a 1:2 block of pixels to keep proportions right.
CHAR_ASPECT = 0.5


def to_ascii(img: Image.Image, width: int, invert: bool, ramp: str) -> str:
    gray = ImageOps.exif_transpose(img).convert("L")
    w, h = gray.size
    height = max(1, int(h / w * width * CHAR_ASPECT))
    gray = gray.resize((width, height), Image.LANCZOS)

    if invert:
        gray = ImageOps.invert(gray)

    px = gray.load()
    n = len(ramp) - 1
    lines = []
    for y in range(height):
        row = []
        for x in range(width):
            # 0 = black → last (lightest) glyph, 255 = white → first (densest) glyph
            idx = n - int(px[x, y] / 255 * n)
            row.append(ramp[idx])
        lines.append("".join(row).rstrip())
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    p.add_argument("image", help="path to a PNG/JPG/WEBP")
    p.add_argument("-w", "--width", type=int, default=100, help="characters per line (default 100)")
    p.add_argument("-o", "--output", help="write result to this .txt file instead of stdout")
    p.add_argument("--invert", action="store_true", help="invert tones (use for dark text on light bg)")
    p.add_argument("--ramp", default=RAMP, help="custom character ramp, densest first")
    args = p.parse_args()

    try:
        img = Image.open(args.image)
    except Exception as e:  # noqa: BLE001
        print(f"could not open {args.image}: {e}", file=sys.stderr)
        return 1

    art = to_ascii(img, args.width, args.invert, args.ramp)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(art + "\n")
        print(f"wrote {args.output} ({args.width} cols, {art.count(chr(10)) + 1} rows)")
    else:
        print(art)
    return 0


if __name__ == "__main__":
    sys.exit(main())
