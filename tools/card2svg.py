#!/usr/bin/env python3
"""
card2svg.py — render ASCII art and a description as one .svg card, with the text
fitted row by row against the outline of the art instead of a rectangle.

Usage:
    python card2svg.py art/name.txt "Description text." -o art/name-card.svg
    python card2svg.py art/name.txt "Description text." -o art/name-card.svg --side right

Install once:  pip install pillow   (used only to measure text widths)
"""

import argparse
import sys
from xml.sax.saxutils import escape

from ascii2svg import CHAR_WIDTH, FILL, FILL_LIGHT, LINE_HEIGHT, NBSP

CARD_WIDTH = 800       # px; the README shows the card at this width
ART_WIDTH = 300        # px the art is drawn at inside the card
GAP = 18               # px between the art's edge and the text
FONT_SIZE = 16
TEXT_LINE = 24         # px between text baselines
TEXT_TOP = 12          # px from the top of the card to the first text line's top
# Browsers pick their own sans-serif, so measured widths get some slack.
SLACK = 1.08

# GitHub's body text colours for dark and light themes.
TEXT_DARK = "#e6edf3"
TEXT_LIGHT = "#1f2328"

FONTS = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/arial.ttf",
]


def text_measurer():
    from PIL import ImageFont

    for path in FONTS:
        try:
            font = ImageFont.truetype(path, FONT_SIZE)
            return lambda s: font.getlength(s) * SLACK
        except OSError:
            continue
    # No known font: assume an average glyph of 0.55em.
    return lambda s: len(s) * FONT_SIZE * 0.55 * SLACK


def art_edges(lines: list, scale: float):
    # For each art row, the x extent (left, right) of its glyphs in card px, or None if empty.
    edges = []
    for line in lines:
        if not line.strip():
            edges.append(None)
            continue
        left = len(line) - len(line.lstrip(" "))
        right = len(line.rstrip())
        edges.append((left * CHAR_WIDTH * scale, right * CHAR_WIDTH * scale))
    return edges


def free_span(edges, row_h, top, bottom, side, art_x):
    # The horizontal span left free for text between y=top and y=bottom.
    rows = range(max(0, int(top // row_h)), min(len(edges), int(bottom // row_h) + 1))
    spans = [edges[r] for r in rows if edges[r] is not None]
    if side == "left":
        reach = max((art_x + r for _, r in spans), default=None)
        x0 = reach + GAP if reach is not None else 0
        return x0, CARD_WIDTH
    reach = min((art_x + l for l, _ in spans), default=None)
    x1 = reach - GAP if reach is not None else CARD_WIDTH
    return 0, x1


def layout(words, edges, row_h, art_h, side, art_x, measure, top=TEXT_TOP):
    # Greedy word wrap where every line gets the width the art leaves free at its height.
    words = list(words)
    placed, y = [], top
    while words:
        x0, x1 = free_span(edges, row_h, y, y + TEXT_LINE, side, art_x)
        room = x1 - x0
        line = []
        while words and measure(" ".join(line + [words[0]])) <= room:
            line.append(words.pop(0))
        if not line:
            if room >= CARD_WIDTH * 0.9:  # a single word wider than the card
                line.append(words.pop(0))
            else:  # too tight here; move down a line
                y += TEXT_LINE
                continue
        placed.append((x0, x1, y, " ".join(line)))
        y += TEXT_LINE
    return placed, y


def to_card(lines: list, text: str, side: str) -> str:
    cols = max(len(line) for line in lines)
    scale = ART_WIDTH / (cols * CHAR_WIDTH)
    row_h = LINE_HEIGHT * scale
    art_h = len(lines) * row_h
    art_x = 0 if side == "left" else CARD_WIDTH - ART_WIDTH

    edges, measure, words = art_edges(lines, scale), text_measurer(), text.split()
    placed, text_bottom = layout(words, edges, row_h, art_h, side, art_x, measure)
    # Centre the text block against the art; the wrap shifts as it moves, so settle it twice.
    for _ in range(2):
        block = text_bottom - placed[0][2]
        top = max(TEXT_TOP, (art_h - block) / 2)
        placed, text_bottom = layout(words, edges, row_h, art_h, side, art_x, measure, top)
    height = int(round(max(art_h, text_bottom)))

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_WIDTH}" height="{height}" '
        f'viewBox="0 0 {CARD_WIDTH} {height}">',
        "<style>"
        f".art{{fill:{FILL}}}.txt{{fill:{TEXT_DARK}}}"
        f"@media (prefers-color-scheme: light) {{ .art{{fill:{FILL_LIGHT}}}.txt{{fill:{TEXT_LIGHT}}} }}"
        "</style>",
        f'<g class="art" transform="translate({art_x} 0) scale({scale:.5f})" font-family="monospace" '
        f'font-size="10" xml:space="preserve" style="white-space:pre">',
    ]
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        y = (i + 1) * LINE_HEIGHT - 2
        length = round(len(line) * CHAR_WIDTH, 2)
        out.append(
            f'<text x="0" y="{y}" textLength="{length}" lengthAdjust="spacingAndGlyphs">'
            f'{escape(line).replace(" ", NBSP)}</text>'
        )
    out.append("</g>")

    anchor = "start" if side == "left" else "end"
    out.append(
        f'<g class="txt" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" '
        f'font-size="{FONT_SIZE}" text-anchor="{anchor}">'
    )
    for x0, x1, y, words in placed:
        x = x0 if side == "left" else x1
        baseline = y + FONT_SIZE
        out.append(f'<text x="{x:.1f}" y="{baseline}">{escape(words)}</text>')
    out.append("</g>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="Render ASCII art and a description as one .svg card.")
    p.add_argument("art", help="path to a .txt file of ASCII art")
    p.add_argument("text", help="the description to fit beside the art")
    p.add_argument("-o", "--output", required=True, help="write the .svg to this path")
    p.add_argument("--side", choices=["left", "right"], default="left", help="which side the art sits on")
    args = p.parse_args()

    try:
        with open(args.art, encoding="utf-8") as f:
            lines = f.read().rstrip("\n").split("\n")
    except OSError as e:
        print(f"could not read {args.art}: {e}", file=sys.stderr)
        return 1

    svg = to_card(lines, args.text, args.side)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {args.output} (art on the {args.side})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
