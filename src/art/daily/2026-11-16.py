"""Daily artwork, 2026-11-16: the Supreme Court declines Trump's appeal over cancelled UC research grants.

Visual idea: light from the marble. A worm's-eye view up the Supreme Court's west steps puts its
towering Corinthian columns and pediment against a deep evening-green sky; from the central bay a
broad shaft of gold light falls diagonally across the picture into a lit cutaway research lab in
the lower right, where researchers are at work (microscope, flasks, notes) beneath a window that
shows a campus clock tower. Blank sheets of paper drift down the beam toward the lab, an openly
symbolic nod to grants the order leaves in place.

Verified (brief): on Nov. 16 the Court declined to hear the administration's appeal; lower courts
had found the NSF/NEH grant terminations to UC researchers likely violated the First Amendment;
no justice publicly dissented (NBC, CBS, AP via ABC).
Drawn: the Supreme Court's west facade (generic sculpture shapes, no inscription), generic
researchers, a generic campus clock tower. Not drawn: justices, officials, named people, any text.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-16"
R = rng(20261116)

# palette: evening emerald sky, marble cream, shadow teal-green, gold light, coral accent
SKY1, SKY2, SKY3 = "#0d3b36", "#14564c", "#2a7a64"
MARBLE, MARBLE2, MARBLE3 = "#f1ead8", "#d8ccb0", "#a99a7a"
SHADOW, SHADOW2 = "#0a2a27", "#123d38"
GOLD, GOLD2, GOLD3 = "#ffd36b", "#f7b23b", "#fff1c4"
CORAL, CORAL2 = "#ff6f59", "#d84e3c"
INK = "#10201e"
LABWALL, LABWALL2 = "#fbe9c6", "#f2d39a"

defs = [
    linear("sky", [(0, SKY1), (0.6, SKY2), (1, SKY3)]),
    linear("beam", [(0, GOLD3), (1, GOLD)], x2=1, y2=1),
    linear("bay", [(0, GOLD3), (1, GOLD2)]),
    linear("col", [(0, MARBLE2), (0.35, MARBLE), (1, MARBLE3)], x2=1, y2=0),
    linear("labwall", [(0, LABWALL), (1, LABWALL2)]),
    linear("win", [(0, "#1d5e55"), (1, "#f2a85a")]),
    blur("soft", 14),
    halftone("dots", MARBLE3, dot=1.6, spacing=7),
    grain_filter(),
]

body = []

# --- sky -----------------------------------------------------------------------------------
body.append(rect(0, 0, WIDTH, HEIGHT, fill="url(#sky)"))
for i, rr in enumerate((560, 430, 300)):  # faint concentric glow behind the court
    body.append(circle(430, 330, rr, fill=GOLD, opacity=0.05 + i * 0.03))
for k in range(14):  # radiating rays from the court's central bay
    a0 = math.radians(-180 + k * 13 + 3)
    a1 = a0 + math.radians(5)
    body.append(poly([(430, 360), (430 + 900 * math.cos(a0), 360 + 900 * math.sin(a0)),
                      (430 + 900 * math.cos(a1), 360 + 900 * math.sin(a1))], fill=GOLD, opacity=0.06))
for _ in range(40):
    body.append(circle(R.uniform(0, 1200), R.uniform(0, 260), R.uniform(0.8, 1.8), fill=GOLD3, opacity=0.5))

# --- Supreme Court west facade (low angle: columns lean in slightly toward the top) ----------
L, Rt = 20, 840            # facade extents at the column bases
TOPL, TOPR = 50, 810       # extents at the capitals (perspective taper)
BASE_Y, CAP_Y = 640, 270
ENT_Y = 205                # entablature top
PED_TOP = 70

# deep shadowed portico behind the columns
body.append(poly([(TOPL, CAP_Y), (TOPR, CAP_Y), (Rt, BASE_Y), (L, BASE_Y)], fill=SHADOW))
# bronze doors area in the central bay, glowing
body.append(poly([(385, 330), (475, 330), (482, BASE_Y), (378, BASE_Y)], fill="url(#bay)"))
body.append(ellipse(430, 470, 120, 220, fill=GOLD, opacity=0.35, filter="url(#soft)"))

# entablature + pediment
body.append(poly([(TOPL - 20, CAP_Y), (TOPR + 20, CAP_Y), (TOPR + 30, ENT_Y), (TOPL - 30, ENT_Y)], fill=MARBLE2))
body.append(rect(TOPL - 30, ENT_Y + 18, (TOPR - TOPL) + 60, 10, fill=MARBLE3, opacity=0.6))
body.append(poly([(TOPL - 50, ENT_Y), (TOPR + 50, ENT_Y), (TOPR + 40, ENT_Y - 16), (TOPL - 40, ENT_Y - 16)], fill=MARBLE))
ped = [(TOPL - 40, ENT_Y - 16), (TOPR + 40, ENT_Y - 16), (430, PED_TOP)]
body.append(poly(ped, fill=MARBLE))
body.append(poly([(TOPL + 10, ENT_Y - 24), (TOPR - 10, ENT_Y - 24), (430, PED_TOP + 22)], fill=MARBLE2))
# generic sculpture group in the tympanum: a row of seated/standing shapes, no detail
for i in range(9):
    x = 205 + i * 56 + R.uniform(-6, 6)
    h = max(14, 74 - abs(i - 4) * 15 + R.uniform(-8, 8))
    body.append(path(f"M{x - 12} {ENT_Y - 24} Q{x - 14} {ENT_Y - 24 - h} {x} {ENT_Y - 30 - h} "
                     f"Q{x + 14} {ENT_Y - 24 - h} {x + 12} {ENT_Y - 24} Z", fill=MARBLE3, opacity=0.85))
    body.append(circle(x, ENT_Y - 36 - h, 7, fill=MARBLE3, opacity=0.85))
body.append(poly(ped, fill="url(#dots)", opacity=0.35))

# columns
N = 8
for i in range(N):
    t = i / (N - 1)
    bx = L + 45 + t * (Rt - L - 90)
    tx = TOPL + 38 + t * (TOPR - TOPL - 76)
    wb, wt = 34, 28
    body.append(poly([(tx - wt, CAP_Y + 22), (tx + wt, CAP_Y + 22), (bx + wb, BASE_Y - 16), (bx - wb, BASE_Y - 16)],
                     fill="url(#col)"))
    for f in (-0.55, -0.2, 0.2, 0.55):  # fluting
        body.append(path(f"M{tx + f * wt:.1f} {CAP_Y + 26} L{bx + f * wb:.1f} {BASE_Y - 20}",
                         stroke=MARBLE3, stroke_width=2, opacity=0.55))
    # Corinthian capital: flared leafy block
    body.append(path(f"M{tx - wt} {CAP_Y + 24} Q{tx - wt - 14} {CAP_Y + 8} {tx - wt - 10} {CAP_Y} L{tx + wt + 10} {CAP_Y} "
                     f"Q{tx + wt + 14} {CAP_Y + 8} {tx + wt} {CAP_Y + 24} Z", fill=MARBLE))
    for k in (-1, 0, 1):
        body.append(ellipse(tx + k * 16, CAP_Y + 14, 7, 9, fill=MARBLE2))
    body.append(rect(bx - wb - 8, BASE_Y - 18, 2 * wb + 16, 18, fill=MARBLE2))
    # warm rim light on the side facing the bay
    side = 1 if bx < 430 else -1
    body.append(path(f"M{tx + side * (wt - 4):.1f} {CAP_Y + 26} L{bx + side * (wb - 4):.1f} {BASE_Y - 20}",
                     stroke=GOLD, stroke_width=5, opacity=0.55))

# steps: widen as they fall toward the viewer
for k in range(9):
    y0 = BASE_Y + k * 30
    grow = k * 34
    body.append(rect(L - 40 - grow, y0, (Rt - L) + 80 + 2 * grow, 30, fill=MARBLE if k % 2 == 0 else MARBLE2))
    body.append(rect(L - 40 - grow, y0, (Rt - L) + 80 + 2 * grow, 4, fill=MARBLE3, opacity=0.7))

# long cast shadows of the columns falling down the steps toward the viewer
for i in range(N):
    t = i / (N - 1)
    bx = L + 45 + t * (Rt - L - 90)
    dx = (bx - 430) * 0.9
    body.append(poly([(bx - 30, BASE_Y), (bx + 30, BASE_Y), (bx + 30 + dx + 50, 900), (bx - 30 + dx - 50, 900)],
                     fill=SHADOW2, opacity=0.14))
# a single pool of light spilling down the central steps
body.append(poly([(385, BASE_Y), (478, BASE_Y), (620, 900), (250, 900)], fill=GOLD3, opacity=0.45))

# --- the beam of light -----------------------------------------------------------------------
body.append(poly([(392, 340), (470, 340), (1200, 700), (1200, 900), (760, 900)], fill="url(#beam)", opacity=0.42))
body.append(poly([(410, 360), (455, 360), (1200, 780), (1200, 860), (880, 900)], fill=GOLD3, opacity=0.25))

# --- cutaway research lab, lower right -------------------------------------------------------
LX, LY = 660, 440
body.append(rect(LX - 14, LY - 14, 1200 - LX + 14, 900 - LY + 14, fill=INK))
body.append(rect(LX, LY, 1200 - LX, 900 - LY, fill="url(#labwall)"))
# window with campus clock tower at dusk
WX, WY, WW, WH = 900, 470, 250, 220
body.append(rect(WX, WY, WW, WH, fill="url(#win)"))
tx0 = WX + 165
body.append(rect(tx0 - 13, WY + 58, 26, WH - 58, fill="#2a3b3a"))
body.append(rect(tx0 - 15, WY + 52, 30, 30, fill="#22302f"))
for k in (-1, 1):
    body.append(rect(tx0 + k * 6 - 3, WY + 58, 6, 18, rx=3, fill="#f6c27a"))
body.append(poly([(tx0 - 15, WY + 52), (tx0 + 15, WY + 52), (tx0, WY + 8)], fill="#22302f"))
body.append(circle(tx0, WY + 98, 6, fill=GOLD3))
for bx in range(WX, WX + WW, 40):
    body.append(rect(bx, WY + WH - 30 - (bx % 3) * 8, 34, 30 + (bx % 3) * 8, fill="#24403c"))
body.append(rect(WX + WW / 2 - 3, WY, 6, WH, fill=INK))
body.append(rect(WX, WY + WH / 2 - 3, WW, 6, fill=INK))
body.append(rect(WX - 8, WY - 8, WW + 16, WH + 16, fill="none", stroke=INK, stroke_width=8))
# shelf with bottles
body.append(rect(690, 520, 180, 8, fill="#7a5a3a"))
for i, c in enumerate((CORAL, "#3d9a86", GOLD2, "#5a7fc0", CORAL2)):
    x = 700 + i * 34
    body.append(rect(x, 490, 20, 30, rx=4, fill=c, opacity=0.9))
    body.append(rect(x + 6, 482, 8, 10, fill=INK))
# lamp cone
body.append(poly([(800, 580), (770, 600), (640, 900), (980, 900), (830, 600)], fill=GOLD3, opacity=0.18))
# lab bench
BENCH = 760
body.append(rect(LX, BENCH, 1200 - LX, 18, fill="#2c4a46"))
body.append(rect(LX, BENCH + 18, 1200 - LX, 140, fill="#1d3633"))
body.append(ellipse(900, BENCH + 4, 260, 14, fill=GOLD3, opacity=0.45))
# flasks + rack on bench
body.append(path(f"M975 {BENCH} L985 {BENCH - 40} L985 {BENCH - 66} L997 {BENCH - 66} L997 {BENCH - 40} L1012 {BENCH} Z",
                 fill="#bfe6dc", opacity=0.9))
body.append(path(f"M979 {BENCH - 2} L987 {BENCH - 26} L995 {BENCH - 26} L1008 {BENCH - 2} Z", fill=CORAL, opacity=0.85))
for i in range(4):
    body.append(rect(1060 + i * 16, BENCH - 48, 10, 48, rx=4, fill=["#3d9a86", GOLD2, CORAL, "#5a7fc0"][i]))
body.append(rect(1052, BENCH - 20, 72, 8, fill="#6b6f70"))
# microscope (eyepiece at the leaning researcher's eye level)
mx = 800
body.append(rect(mx - 26, BENCH - 8, 52, 8, fill=INK))
body.append(path(f"M{mx + 10} {BENCH - 8} Q{mx + 22} {BENCH - 36} {mx + 4} {BENCH - 58}", fill="none",
                 stroke=INK, stroke_width=9, stroke_linecap="round"))
body.append(rect(mx - 20, BENCH - 30, 30, 5, fill="#5a6263"))
body.append(poly([(mx - 2, BENCH - 50), (mx + 8, BENCH - 56), (mx - 12, BENCH - 84), (mx - 21, BENCH - 79)], fill="#3b4445"))
body.append(circle(mx - 4, BENCH - 30, 5, fill=GOLD3, opacity=0.9))

# researchers
coat = dict(top="#f8f6f0", top_shade="#d9d4c6", coat=True)
# seated at microscope (facing right toward it? microscope is right of her: face +1)
body.append(figure(745, BENCH + 140, 240, facing=1,
                   pose=Pose(back_arm=(55, -10), front_arm=(62, -18), back_leg=(-4, 0), front_leg=(4, 0),
                             lean=10, head_tilt=28),
                   look=Look(skin="#8a5a3c", hair="#1c1412", hair_style="bun", bottom="#2b3a5a", face="neutral",
                             **coat)))
# standing, holding a flask up to the light
flask = path("M-3 0 L3 0 L3 -6 L6 -14 L-6 -14 L-3 -6 Z", fill="#bfe6dc",
             stroke="#7fb6aa", stroke_width=1)
body.append(figure(905, BENCH + 140, 260, facing=-1,
                   pose=Pose(back_arm=(30, 20), front_arm=(150, 10), head_tilt=-12),
                   look=Look(skin="#e2b48f", hair="#b8742c", hair_style="short", bottom="#3a2f2a",
                             face="smile", accent=CORAL, **coat),
                   hand_items={"front": flask}))
# standing at right, reading a blank sheet
sheet = rect(-1, -12, 12, 16, fill="#ffffff", stroke=MARBLE3, stroke_width=0.6)
body.append(figure(1130, BENCH + 140, 250, facing=-1,
                   pose=Pose(back_arm=(40, 60), front_arm=(55, 75), head_tilt=14),
                   look=Look(skin="#c98e6b", hair="#2a1d18", hair_style="long", bottom="#28324a",
                             face="neutral", **coat),
                   hand_items={"front": sheet}))

# --- papers drifting down the beam toward the lab ---------------------------------------------
for i in range(11):
    t = (i + 0.5) / 11
    x = 470 + t * 560 + R.uniform(-30, 30)
    y = 360 + t * 300 + R.uniform(-60, 40)
    a = R.uniform(-35, 35)
    w, h = 34 - t * 8, 44 - t * 10
    body.append(group([
        rect(-w / 2 + 3, -h / 2 + 4, w, h, fill=INK, opacity=0.18),
        rect(-w / 2, -h / 2, w, h, fill="#fffdf4"),
        path(f"M{-w / 2} {h / 2 - 8} L{-w / 2 + 8} {h / 2} L{-w / 2} {h / 2} Z", fill=MARBLE2),
    ], transform=f"translate({x:.0f} {y:.0f}) rotate({a:.0f})"))

# frame vignette at top for depth
body.append(rect(0, 0, WIDTH, 30, fill=SKY1, opacity=0.5))
body.append(grain_overlay())

TITLE = "The Supreme Court leaves UC research grant rulings in place"
DESC = ("Editorial illustration: a low-angle view up the marble steps and Corinthian columns of the U.S. Supreme Court "
        "against a deep green evening sky. Gold light streams from the central bay down across the picture into a "
        "university research lab, where researchers in lab coats work at a microscope and hold up a flask beneath a "
        "window showing a campus clock tower, while blank sheets of paper drift along the beam. It represents the "
        "Court declining, on Nov. 16, 2026, the Trump administration's appeal over cancelled University of California "
        "research grants.")

save(document(defs, body, TITLE, DESC), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
