#!/usr/bin/env python3
"""
ascii2svg.py — render a .txt file of ASCII art as an .svg with a transparent background.

Usage:
    python ascii2svg.py art/name.txt -o art/name.svg
    python ascii2svg.py art/name.txt -o art/name.svg --color art/name.png   # tint glyphs from the image

Install once for --color:  pip install pillow
"""

import argparse
import colorsys
import sys
from xml.sax.saxutils import escape

FONT_SIZE = 10
LINE_HEIGHT = 12
FILL = "#c9d1d9"
# GitHub's light-theme text colour, used when the viewer prefers a light scheme.
FILL_LIGHT = "#1f2328"

# Monospace glyphs advance about 0.6em, so each column is 6px at font-size 10.
CHAR_WIDTH = FONT_SIZE * 0.6

# Colours are rounded to this step so neighbouring glyphs share one <tspan>.
COLOR_STEP = 32

NBSP = " "


def colour_grid(path: str, cols: int, rows: int, sharp: bool = False):
    from PIL import Image, ImageFilter, ImageOps

    img = ImageOps.exif_transpose(Image.open(path)).convert("RGBA")
    # Blur first so thin ink lines pick up the colour of the area around them
    # (hair, skin, cloth) instead of their own near-black. Scenes skip this with
    # sharp=True so each glyph keeps the exact colour beneath it.
    if not sharp:
        img = img.filter(ImageFilter.GaussianBlur(img.width / 60))
    flat = Image.new("RGBA", img.size, (128, 128, 128, 255))
    flat.alpha_composite(img)
    return flat.convert("RGB").resize((cols, rows), Image.LANCZOS).load()


def tints(rgb):
    # Returns (dark-theme colour, light-theme colour): saturated and bright enough to
    # read on GitHub's dark background, and a darker twin for the light background.
    rgb = [min(255, round(c / COLOR_STEP) * COLOR_STEP) for c in rgb]
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    s = min(1.0, s * 1.8)
    dark = colorsys.hsv_to_rgb(h, s, 0.55 + 0.45 * v)
    light = colorsys.hsv_to_rgb(h, s, 0.25 + 0.25 * v)
    as_hex = lambda c: "#" + "".join(f"{round(x * 255):02x}" for x in c)  # noqa: E731
    return as_hex(dark), as_hex(light)


def coloured_runs(line: str, y: int, px, classes: dict) -> str:
    # Group neighbouring glyphs of the same colour; spaces join whatever run they sit in.
    runs, colour, buf = [], None, ""
    for x, ch in enumerate(line):
        if ch != " ":
            c = tints(px[x, y])
            if colour is not None and c != colour and buf:
                runs.append((colour, buf))
                buf = ""
            colour = c
        buf += ch
    if buf:
        runs.append((colour, buf))
    out = []
    for c, t in runs:
        t = escape(t).replace(" ", NBSP)
        if c is None:
            out.append(t)
        else:
            cls = classes.setdefault(c, f"c{len(classes)}")
            out.append(f'<tspan class="{cls}">{t}</tspan>')
    return "".join(out)


def to_svg(lines: list, px=None) -> str:
    cols = max((len(line) for line in lines), default=0)
    width = int(round(cols * CHAR_WIDTH))
    height = len(lines) * LINE_HEIGHT

    classes = {}
    body = []
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        # y is the text baseline; sit it near the bottom of each 12px row
        y = (i + 1) * LINE_HEIGHT - (LINE_HEIGHT - FONT_SIZE)
        # Browsers rendering an SVG as an <img> still collapse runs of spaces, so use
        # non-breaking spaces, and pin each line's width so the viewer's monospace font
        # can't drift the columns.
        length = round(len(line) * CHAR_WIDTH, 2)
        text = coloured_runs(line, i, px, classes) if px else escape(line).replace(" ", NBSP)
        body.append(
            f'<text x="0" y="{y}" textLength="{length}" lengthAdjust="spacingAndGlyphs">{text}</text>'
        )

    dark_rules = "".join(f".{cls}{{fill:{d}}}" for (d, _), cls in classes.items())
    light_rules = "".join(f".{cls}{{fill:{l}}}" for (_, l), cls in classes.items())
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        f"<style>{dark_rules}@media (prefers-color-scheme: light) {{ g {{ fill: {FILL_LIGHT}; }} {light_rules}}}</style>",
        f'<g font-family="monospace" font-size="{FONT_SIZE}" fill="{FILL}" xml:space="preserve" style="white-space:pre">',
    ]
    out.extend(body)
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="Render ASCII art from a .txt file as an .svg.")
    p.add_argument("text", help="path to a .txt file of ASCII art")
    p.add_argument("-o", "--output", required=True, help="write the .svg to this path")
    p.add_argument("--color", help="image the art was made from; colours each glyph to match it")
    p.add_argument("--sharp", action="store_true", help="with --color, skip the blur (for scenes, not ink portraits)")
    args = p.parse_args()

    try:
        with open(args.text, encoding="utf-8") as f:
            lines = f.read().rstrip("\n").split("\n")
    except OSError as e:
        print(f"could not read {args.text}: {e}", file=sys.stderr)
        return 1

    px = None
    if args.color:
        cols = max(len(line) for line in lines)
        try:
            px = colour_grid(args.color, cols, len(lines), args.sharp)
        except Exception as e:  # noqa: BLE001
            print(f"could not open {args.color}: {e}", file=sys.stderr)
            return 1

    svg = to_svg(lines, px)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {args.output} ({len(lines)} lines{', coloured' if px else ''})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
