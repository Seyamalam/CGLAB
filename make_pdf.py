"""Generate CG_Lab_Notes.pdf — a one-stop study note for the 4 algorithms."""
from fpdf import FPDF

pdf = FPDF(format="A4")
pdf.set_margins(12, 12, 12)
pdf.set_auto_page_break(True, margin=15)
pdf.add_page()

def h1(text):
    pdf.set_font("helvetica", "B", 20)
    pdf.cell(0, 12, text, new_x="LMARGIN", new_y="NEXT")

def h2(text):
    pdf.ln(4)
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)

def h3(text):
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")

def para(text):
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 5, text)
    pdf.ln(1)

def code_block(filename):
    with open(filename) as f:
        code = f.read().rstrip()
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("courier", "", 7)
    pdf.multi_cell(0, 3.4, code, fill=True)
    pdf.ln(2)

def step(text):
    pdf.set_font("helvetica", "", 10)
    pdf.multi_cell(0, 5, text, new_x="LMARGIN")

def table(headers, rows):
    pdf.set_font("helvetica", "", 8)
    with pdf.table(text_align="CENTER", line_height=5) as t:
        for data in [headers] + rows:
            row = t.row()
            for cell in data:
                row.cell(str(cell))
    pdf.ln(2)

# ---------------- Title ----------------
h1("Computer Graphics Lab Notes")
para("Rasterization = turning a smooth mathematical shape (a line, a circle) "
     "into real square pixels on the screen. The four algorithms below decide "
     "WHICH pixels to light up. DDA uses simple float maths; the Bresenham and "
     "Midpoint algorithms use only integers, so they are faster on real hardware.")
para("Each section gives you: the definition, the maths, the steps, a fully "
     "worked example with real numbers, and the actual code.")

# ---------------- 1. DDA ----------------
h2("1. DDA Line Algorithm")
h3("Definition")
para("DDA = Digital Differential Analyzer. Walk from the start point to the end "
     "point in equal-sized steps: the longer of dx or dy tells you how many "
     "steps to take, and you add a small increment to x and y each step, "
     "rounding to the nearest pixel.")
h3("The maths")
para("dx = x2 - x1        dy = y2 - y1\n"
     "steps = max(|dx|, |dy|)\n"
     "x_inc = dx / steps    y_inc = dy / steps\n"
     "repeat (steps + 1) times: plot (round(x), round(y));  x += x_inc;  y += y_inc")
h3("Steps")
for s in ["Step 1: Compute dx and dy.",
          "Step 2: steps = the longer of the two (so the line moves smoothly).",
          "Step 3: Divide: x_inc = dx/steps and y_inc = dy/steps.",
          "Step 4: Loop steps+1 times - plot round(x), round(y), then add the increments.",
          "Step 5: Done - every plotted point is a pixel of the line."]:
    step(s)
h3("Worked example: (2, 2) to (15, 8)")
para("dx = 13, dy = 6  ->  steps = 13,  x_inc = 1.0,  y_inc = 0.46")
table(["Step", "x (float)", "y (float)", "Pixel"],
      [[i, f"{2+i:.2f}", f"{2+6*i/13:.2f}", f"({2+i}, {round(2+6*i/13)})"] for i in range(14)])
h3("Code")
code_block("dda_line.py")

# ---------------- 2. Bresenham Line ----------------
h2("2. Bresenham Line Algorithm")
h3("Definition")
para("Same job as DDA but with INTEGER maths only (no division, no rounding). "
     "At every x step it uses a decision value p to pick between the pixel "
     "straight ahead (East) or the one diagonally up (North-East). This version "
     "works for slopes between 0 and 1.")
h3("The maths")
para("dx = x2 - x1        dy = y2 - y1\n"
     "p0 = 2*dy - dx\n"
     "if p < 0:  next pixel = E,   p = p + 2*dy\n"
     "if p >= 0: next pixel = NE,  p = p + 2*dy - 2*dx   (y goes up by 1)")
h3("Steps")
for s in ["Step 1: Compute dx, dy and the starting decision p = 2*dy - dx.",
          "Step 2: Plot the current pixel (x, y).",
          "Step 3: If p < 0, stay at same y and add 2*dy to p.",
          "Step 4: If p >= 0, move y up by 1 and add 2*dy - 2*dx to p.",
          "Step 5: x = x + 1; repeat while x <= x2."]:
    step(s)
h3("Worked example: (2, 2) to (15, 8)")
para("dx = 13, dy = 6  ->  p = 2*6 - 13 = -1")
table(["Pixel", "p before", "Decision", "p after"],
      [["(2, 2)", -1, "E", 11], ["(3, 2)", 11, "NE", -3], ["(4, 3)", -3, "E", 9],
       ["(5, 3)", 9, "NE", -5], ["(6, 4)", -5, "E", 7], ["(7, 4)", 7, "NE", -7],
       ["(8, 5)", -7, "E", 5], ["(9, 5)", 5, "NE", -9], ["(10, 6)", -9, "E", 3],
       ["(11, 6)", 3, "NE", -11], ["(12, 7)", -11, "E", 1], ["(13, 7)", 1, "NE", -13],
       ["(14, 8)", -13, "E", -1], ["(15, 8)", -1, "done", "-"]])
para("DDA and Bresenham choose the SAME pixels - Bresenham is just the "
     "integer-only way to get them.")
h3("Code")
code_block("bresenham_line.py")

# ---------------- 3. Bresenham Circle ----------------
h2("3. Bresenham Circle Algorithm")
h3("Definition")
para("A circle looks the same in all 8 octants, so you only calculate one "
     "45-degree slice and mirror each pixel 8 times. A decision value d picks "
     "between stepping East or South-East while walking the octant.")
h3("The maths")
para("x = 0,  y = r,   d = 3 - 2r\n"
     "if d < 0:  move E,   d = d + 4x + 6\n"
     "if d >= 0: move SE,  d = d + 4(x - y) + 10,  y = y - 1\n"
     "each (x, y) becomes 8 pixels: (+-x, +-y) and (+-y, +-x)\n"
     "loop while x <= y")
h3("Steps")
for s in ["Step 1: Start at the top of the circle: x = 0, y = r.",
          "Step 2: d = 3 - 2r.",
          "Step 3: Mirror (x, y) into all 8 octants and plot them.",
          "Step 4: Update d (E move if d < 0, SE move + y down if d >= 0), x = x + 1.",
          "Step 5: Stop when x > y - one octant is done, the whole circle is drawn."]:
    step(s)
h3("Worked example: centre (0, 0), radius 10")
para("d = 3 - 20 = -17")
table(["Octant (x, y)", "d before", "Decision", "d after"],
      [["(0, 10)", -17, "E", -11], ["(1, 10)", -11, "E", -1], ["(2, 10)", -1, "E", 13],
       ["(3, 10)", 13, "SE, y=9", -5], ["(4, 9)", -5, "E", 17], ["(5, 9)", 17, "SE, y=8", 11],
       ["(6, 8)", 11, "SE, y=7", 13], ["(7, 7)", 13, "loop ends", "-"]])
para("Example mirroring: (4, 9) gives (4,9) (-4,9) (4,-9) (-4,-9) "
     "(9,4) (-9,4) (9,-4) (-9,-4).")
h3("Code")
code_block("bresenham_circle.py")

# ---------------- 4. Midpoint Circle ----------------
h2("4. Midpoint Circle Algorithm")
h3("Definition")
para("Same 8-octant trick as Bresenham's circle, but the decision value p "
     "tests the MIDPOINT between the East and South-East candidates: if the "
     "midpoint is inside the circle go E, otherwise go SE. The numbers look "
     "different but it draws the same pixels.")
h3("The maths")
para("x = 0,  y = r,   p = 1 - r\n"
     "if p < 0:  move E,   p = p + 2x + 3\n"
     "if p >= 0: move SE,  p = p + 2(x - y) + 5,  y = y - 1\n"
     "each (x, y) becomes 8 pixels: (+-x, +-y) and (+-y, +-x)\n"
     "loop while x <= y")
h3("Steps")
for s in ["Step 1: Start at the top: x = 0, y = r.",
          "Step 2: p = 1 - r.",
          "Step 3: Mirror (x, y) into all 8 octants and plot them.",
          "Step 4: Update p (E move if p < 0, SE move + y down if p >= 0), x = x + 1.",
          "Step 5: Stop when x > y."]:
    step(s)
h3("Worked example: centre (0, 0), radius 10")
para("p = 1 - 10 = -9")
table(["Octant (x, y)", "p before", "Decision", "p after"],
      [["(0, 10)", -9, "E", -6], ["(1, 10)", -6, "E", -1], ["(2, 10)", -1, "E", 6],
       ["(3, 10)", 6, "SE, y=9", -3], ["(4, 9)", -3, "E", 8], ["(5, 9)", 8, "SE, y=8", 5],
       ["(6, 8)", 5, "SE, y=7", 6], ["(7, 7)", 6, "loop ends", "-"]])
h3("Code")
code_block("midpoint_circle.py")

# ---------------- Memorize ----------------
h2("Quick Memorization Sheet")
table(["Algorithm", "Starts with", "Update if small", "Update if big", "Stop when"],
      [["DDA line", "steps = max(|dx|,|dy|)", "float + round", "-", "steps+1 times"],
       ["Bresenham line", "p = 2dy - dx", "+ 2dy (E)", "+ 2dy - 2dx (NE)", "x > x2"],
       ["Bresenham circle", "d = 3 - 2r", "+ 4x + 6 (E)", "+ 4(x-y) + 10 (SE)", "x > y"],
       ["Midpoint circle", "p = 1 - r", "+ 2x + 3 (E)", "+ 2(x-y) + 5 (SE)", "x > y"]])
para("Tricks:")
for s in ["- DDA: the name is the method - analyze the delta, then keep adding it.",
          "- Bresenham line: '2dy always, 2dx when you climb.'",
          "- Midpoint circle is HALF of Bresenham circle: 4x->2x, 6->3, 10->5, 3-2r->1-r.",
          "- 8 octants: write (+-x, +-y), then swap to (+-y, +-x). 8 formulas become 2.",
          "- All algorithms are: init -> loop { plot, update decision } -> stop."]:
    step(s)

pdf.output("CG_Lab_Notes.pdf")
print("CG_Lab_Notes.pdf written,", pdf.page_no(), "pages")
