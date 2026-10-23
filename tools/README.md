# tools

## img2ascii.py

Turns an image into ASCII art I can paste above a member's heading in the main README.

Install Pillow once:

```
pip install pillow
```

Then convert an image and save the result into `art/`:

```
python tools/img2ascii.py <image> -w 90 --invert -o art/<name>.txt
```

`-w` sets the width in characters and `--invert` flips the tones for a light background. Leave out `-o` to print to the terminal instead.

## ascii2svg.py

Renders an ASCII art `.txt` file as a transparent `.svg` so it can float beside text in the README:

```
python tools/ascii2svg.py art/<name>.txt -o art/<name>.svg
```

Add `--color` with the cut-out image to tint each glyph with the colour of that part of the picture, with a darker set of the same colours for light mode:

```
python tools/ascii2svg.py art/<name>.txt -o art/<name>.svg --color art/<name>-color.png
```
