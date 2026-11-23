# Computer Graphics Lab

Simple Python implementations of the four classic rasterization algorithms,
each with a matplotlib plot (red = ideal shape, green squares = computed pixels).

| File | Algorithm |
|------|-----------|
| `dda_line.py` | DDA Line |
| `bresenham_line.py` | Bresenham Line |
| `bresenham_circle.py` | Bresenham Circle |
| `midpoint_circle.py` | Midpoint Circle |

`cg_lab.ipynb` has the same four algorithms as a Jupyter notebook.

```bash
pip install matplotlib
python dda_line.py        # or: jupyter notebook cg_lab.ipynb
```

## The algorithms in simple words

**DDA Line** — "Divide, then Add."
Count how many steps the line needs (the longer of `dx` or `dy`), divide the
total distance into that many equal steps, then add a tiny x/y increment on
every step and round to the nearest pixel.

**Bresenham Line** — "Straight or diagonal?"
Only integers, no division. Step through `x` one pixel at a time and use a
decision value `p` to choose: if `p < 0` keep the same `y` (pixel to the East),
otherwise move `y` up too (pixel to the North-East).

**Bresenham Circle** — "Draw one slice, mirror it 8 times."
A circle is 8 symmetric octants, so you only compute a 45° slice. Decision
value `d` starts at `3 - 2r`: small `d` moves East, big `d` moves South-East.

**Midpoint Circle** — "Same trick, test the midpoint."
Identical 8-octant mirroring, but the decision value `p` starts at `1 - r`
and asks whether the midpoint between the E and SE candidates is inside the
circle.

## Tips & tricks to memorize the code

- **Every algorithm = init + loop + decision update.** Learn the skeleton,
  the details fill themselves in.
- **DDA**: `steps = max(|dx|, |dy|)`, `x_inc = dx/steps`, `y_inc = dy/steps`.
  The name IS the code: Digital Differential *Analyzer* — analyze the delta,
  then keep adding it.
- **Bresenham line**: `p = 2*dy - dx`. Each step *always* adds `2*dy`; when
  `y` also moves, subtract `2*dx`. Mnemonic: **"2dy always, 2dx when you climb."**
- **Circle updates come in pairs**: Bresenham uses `d += 4x + 6` or
  `d += 4(x - y) + 10`. Midpoint uses `p += 2x + 3` or `p += 2(x - y) + 5` —
  notice Midpoint is *half* of Bresenham (`4x→2x`, `6→3`, `10→5`, and
  `3 - 2r → 1 - r`). Learn one, halve it for the other.
- **The 8 octants**: write `(+x, +y)` with all four sign combos
  `(±x, ±y)`, then swap x and y for the other four `(±y, ±x)`. That's it —
  no need to memorize 8 formulas.
- **Loop conditions**: lines run `while x <= x2` (walk to the end);
  circles run `while x <= y` (stop at the 45° diagonal, which is exactly
  one octant).
- **Initial values**: Bresenham line `p = 2dy - dx`, Bresenham circle
  `d = 3 - 2r`, Midpoint circle `p = 1 - r`. Each one just asks
  "is the ideal shape above or below this pixel?"
