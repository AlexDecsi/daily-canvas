"""Daily artwork, 2026-11-19: Trump, Xi and Putin hold their first three-way meeting in Shenzhen.

Visual idea: three men and one big page. The three leaders stride in step, side by side like a frieze,
toward the meeting, dwarfed by a towering, nearly blank sheet of paper behind them (four short ruled
blocks, an obviously symbolic nod to the four-point 'peace' declaration and how little it pinned down).
A low, hard side light throws their three long shadows across the floor, where they run together;
they walk toward a bright open doorway; silhouetted photographers fire flashes from the right.

Verified (brief): on Nov. 19 the three met in Shenzhen on the APEC sidelines and arrived together
(ABC photo captions); they issued a joint 'peace' declaration criticizing the ICC (AP, ABC); AP called
the results more symbolic than substantive.
Drawn: Trump (tall, swept blond hair, dark suit, long red tie), Xi (dark hair, dark suit, broad build,
centre as host; order illustrative), Putin (shorter, slim, thinning light hair, dark suit); generic press.
The giant page and its blank ruled blocks are illustration, not a depiction of the document.
Not drawn: any text, flags, venue features, handshake or quotes.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-19"
R = rng(20261119)
OUT = Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg"

# palette: ultramarine night, saffron light, ivory paper, ink, one red accent (Trump's tie)
BG1, BG2 = "#141c4f", "#2a3c9c"
SAFF, SAFF2 = "#ffb534", "#ff8f2a"
PAPER, PAPER2 = "#f4ecd9", "#ddd0b2"
INK = "#0b0d26"
FLOOR1, FLOOR2 = "#e6a440", "#9b5a2a"
SUIT = "#161a33"

defs = [
    grain_filter(),
    linear("bg", [(0, BG1), (1, BG2)]),
    linear("floor", [(0, FLOOR1), (1, FLOOR2)]),
    linear("paper", [(0, PAPER), (1, PAPER2)], x2=1, y2=0),
    linear("beam", [(0, "#ffd27a", 0.55), (1, "#ffd27a", 0)], x2=1, y2=0),
    radial("glow", [(0, "#ffd890", 0.75), (0.5, SAFF, 0.25), (1, SAFF, 0)], r=0.5),
    halftone("dots", "#8fa4ff", dot=1.6, spacing=9),
    halftone("pdots", "#b59a68", dot=1.2, spacing=7, angle=30),
    blur("soft", 7),
]

body = []
body.append(rect(0, 0, 1200, 900, fill="url(#bg)"))
body.append(rect(0, 0, 1200, 640, fill="url(#dots)", opacity=0.18))

# --- the giant page (symbolic declaration), slightly tilted, curling at the top ---
page = []
PX, PY, PW, PH = 330, 40, 560, 720
page.append(rect(PX + 18, PY + 18, PW, PH, fill=INK, opacity=0.35, filter="url(#soft)"))
page.append(path(f"M{PX} {PY + 30} Q{PX + PW / 2} {PY - 10} {PX + PW} {PY + 30} L{PX + PW} {PY + PH} L{PX} {PY + PH} Z",
                 fill="url(#paper)"))
page.append(rect(PX, PY, PW, PH, fill="url(#pdots)", opacity=0.25))
# four short ruled blocks, no text
for i in range(4):
    y = PY + 120 + i * 110
    page.append(circle(PX + 70, y + 10, 14, fill="none", stroke="#9b8a64", stroke_width=4))
    for k in range(3):
        w = [380, 330, 200][k] if i % 2 == 0 else [360, 250, 120][k]
        page.append(rect(PX + 110, y + k * 20, w, 8, rx=4, fill="#b9a983"))
# a seal-like circle at the foot of the page (blank)
page.append(path(f"M{PX} {PY + PH - 70} Q{PX + 40} {PY + PH - 60} {PX + 70} {PY + PH} L{PX} {PY + PH} Z", fill="#bfae86"))
body.append(group(page, transform=f"rotate(-3 {PX + PW / 2} {PY + PH})"))

# --- floor ------------------------------------------------------------------
FY = 640
body.append(rect(0, FY, 1200, 260, fill="url(#floor)"))
for i in range(0, 1300, 80):
    body.append(path(f"M{i} {FY} L{i - 160} 900", stroke="#7a4220", stroke_width=2, opacity=0.25))

# --- open doorway of light at left: the leaders walk toward it ---------------
DX, DW = 40, 170
body.append(circle(DX + DW / 2, 420, 380, fill="url(#glow)"))
body.append(rect(DX - 14, 150, DW + 28, FY - 150 + 4, fill="#2b2160"))
body.append(rect(DX, 166, DW, FY - 166, fill="#fff0c8"))
body.append(rect(DX + 20, 186, DW - 40, FY - 186, fill="#ffe29a", opacity=0.6))
# broad shafts of light leaving the doorway across the wall (behind the page)
for k, (t0, t1, spread) in enumerate(((166, 260, -0.55), (300, 380, -0.25), (420, 500, 0.02))):
    body.append(poly([(DX + DW, t0), (DX + DW, t1), (1200, round(t1 + spread * 1030, 1)),
                      (1200, round(t0 + spread * 1030 - 60, 1))], fill="#ffe3a0", opacity=0.12))
# light spilling across the floor from the doorway (a wedge widening to the right)
body.append(poly([(DX, FY), (DX + DW, FY), (1200, 860), (1200, 900), (DX - 120, 900)], fill="#ffe7a8", opacity=0.45))

# --- three long, crisp shadows trailing right, running together ----------------
GY = 760
for x, h in ((880, 360), (700, 355), (520, 330)):
    body.append(poly([(x - 26, GY + 4), (x + 26, GY + 4), (x + 26 + h * 1.15, GY + 92), (x - 10 + h * 1.15, GY + 104)],
                     fill=INK, opacity=0.42))

# --- the three leaders, walking left toward the light -------------------------
def walker(x, h, look, phase):
    if phase == 0:
        pose = Pose(back_arm=(-25, 10), front_arm=(25, 15), back_leg=(-18, 0), front_leg=(20, -6), lean=3)
    else:
        pose = Pose(back_arm=(20, 15), front_arm=(-20, 10), back_leg=(18, -6), front_leg=(-16, 0), lean=3)
    return figure(x, GY, h, facing=-1, pose=pose, look=look)


putin = Look(skin="#e8b99a", top=SUIT, bottom=SUIT, hair="#c9b08a", hair_style="short", accent="#3c5a9a",
             build=1.05, face="neutral")
xi = Look(skin="#e0b48c", top="#1b1e2a", bottom="#1b1e2a", hair="#141417", hair_style="short", accent="#7a1f2b",
          build=1.3, face="neutral")
trump = Look(skin="#eab48c", top="#1a2036", bottom="#1a2036", hair="#f0c45a", hair_style="swept",
             accent="#d3202f", long_tie=True, build=1.3, face="smile")
for x, h, b in ((880, 360, 1.3), (700, 355, 1.3), (520, 330, 1.05)):
    sc = h / 100
    body.append(rect(round(x - 9 * b * sc, 1), round(GY - 74 * sc, 1), round(18 * b * sc, 1), round(28 * sc, 1), fill=SUIT))
body.append(walker(880, 360, trump, 1))
body.append(walker(700, 355, xi, 0))
body.append(walker(520, 330, putin, 1))

# --- photographers silhouetted in the right foreground, turned toward the leaders ---
cam = group([rect(-6, -6, 16, 11, rx=2, fill="#05061a"), circle(10, -1, 5, fill="#05061a"),
             circle(10, -1, 2.4, fill="#ffd36b", opacity=0.8)])
for x, h in ((1175, 400), (1030, 300)):
    body.append(figure(x, 960, h, facing=-1, pose=Pose(back_arm=(80, 70), front_arm=(105, 75), head_tilt=-4),
                       look=Look(skin=INK, top=INK, bottom=INK, shoes=INK, hair=INK, build=1.25),
                       hand_items={"front": cam}))

for fx, fy, sc in ((958, 690, 0.8), (1092, 612, 1.0)):
    pts = []
    for k in range(16):
        r = (34 if k % 2 == 0 else 9) * sc
        a = math.radians(k * 22.5)
        pts.append((round(fx + r * math.cos(a), 1), round(fy + r * math.sin(a), 1)))
    body.append(circle(fx, fy, round(46 * sc, 1), fill="#fff6d8", opacity=0.2))
    body.append(poly(pts, fill="#fffbe8", opacity=0.9))

body.append(grain_overlay(opacity=0.30))

title = "Trump, Xi and Putin hold their first three-way meeting"
desc = ("Editorial illustration. Three leaders in dark suits stride side by side across a warm floor toward a bright open doorway: "
        "Donald Trump with swept blond hair and a long red tie, Xi Jinping at the centre, and Vladimir Putin, shorter "
        "with thinning light hair. Behind them rises a towering, nearly blank sheet of paper with four short ruled "
        "blocks, a symbolic stand-in for their joint declaration; their long shadows trail behind them, "
        "and silhouetted photographers in the foreground fire flashes. Represents the first three-way "
        "meeting of Trump, Xi and Putin in Shenzhen on Nov. 19, 2026, which produced a four-point 'peace' declaration.")
save(document(defs, body, title, desc), OUT)
