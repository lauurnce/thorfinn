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
