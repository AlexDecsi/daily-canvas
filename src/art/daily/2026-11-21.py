"""Daily artwork, 2026-11-21: Trump orders federal contractors to check with the White House before answering Congress.

Visual idea: the detour on Pennsylvania Avenue. At night, the floodlit Capitol dome glows at the far end of
the avenue, but a towering blank sheet with a red seal (the executive order, drawn as an obvious symbol with
no text) stands across the road in front of it. A long line of generic contractors (hard-hat workers, office
staff with folders and document boxes) that was heading for the Capitol bends aside at the sheet and queues
back toward the floodlit north portico of the White House. Street lamps throw long shadows.

Verified (brief): an order issued late Friday, Nov. 20 directs federal contractors and subcontractors to
consult the administration about congressional inquiries, coordinate responses with the White House and
withhold communications it considers privileged, or risk losing contracts (AP, CNBC).
Drawn: Capitol dome and White House north portico from their known features; generic, faceless contractors;
the order as a blank symbolic sheet. Not drawn: Trump (no signing ceremony reported), any text, signs,
protesters, named officials or company logos.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-21"
R = rng(20261121)
OUT = Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg"

# palette: bottle-green night, floodlit marble cream, lamp gold, one crimson accent (the seal)
SKY1, SKY2 = "#0b211c", "#1d4638"
MARBLE, MARBLE2, MARBLE3 = "#f3ead3", "#d6c7a3", "#a8977a"
GOLD, GOLD2 = "#f4c45a", "#ffe6a3"
CRIMSON = "#c8323a"
ROAD, ROAD2 = "#26302b", "#323d37"
TREE, TREE2 = "#0a1a15", "#12291f"
INK = "#07110d"

defs = [
    grain_filter(),
    linear("sky", [(0, SKY1), (1, SKY2)]),
    linear("road", [(0, ROAD2), (1, ROAD)]),
    linear("paper", [(0, "#fffaf0"), (1, "#e9dfc4")]),
    linear("cone", [(0, GOLD2, 0.5), (1, GOLD2, 0)]),
    linear("flood", [(0, GOLD2, 0), (1, GOLD2, 0.35)]),
    radial("domeglow", [(0, "#fff3cf", 0.75), (0.5, "#f4d58a", 0.22), (1, "#f4d58a", 0)]),
    radial("paperglow", [(0, "#fff6da", 0.55), (1, "#fff6da", 0)]),
    radial("lampglow", [(0, GOLD2, 0.9), (0.4, GOLD, 0.35), (1, GOLD, 0)]),
    halftone("dots", "#3f7a62", dot=1.4, spacing=9),
    halftone("rdots", "#4a5a52", dot=1.2, spacing=7, angle=30),
    blur("soft", 8),
]

body = []
HZ = 470  # horizon / Capitol ground line

# ---------------- sky ----------------
body.append(rect(0, 0, 1200, 900, fill="url(#sky)"))
body.append(rect(0, 0, 1200, 420, fill="url(#dots)", opacity=0.35))
for i in range(40):
    body.append(circle(round(R.uniform(10, 1190), 1), round(R.uniform(10, 300), 1), round(R.uniform(0.6, 1.6), 1),
                       fill="#e8f1da", opacity=round(R.uniform(0.3, 0.8), 2)))

# ---------------- Capitol (far end of the avenue) ----------------
CX = 935
cap = [ellipse(CX, 330, 300, 230, fill="url(#domeglow)")]
# wings (Senate left, House right) with column bands
cap.append(rect(700, 412, 470, 58, fill=MARBLE2))
cap.append(rect(700, 406, 470, 8, fill=MARBLE))
for x in range(708, 1166, 11):
    cap.append(rect(x, 418, 3, 44, fill=MARBLE3, opacity=0.7))
# central block with pediment
cap.append(rect(860, 392, 150, 78, fill=MARBLE))
cap.append(poly([(866, 392), (CX, 366), (1004, 392)], fill=MARBLE))
for x in range(870, 1004, 12):
    cap.append(rect(x, 398, 4, 66, fill=MARBLE2))
# drum, peristyle, dome, lantern, statue
cap.append(rect(872, 318, 126, 50, fill=MARBLE))
for x in range(876, 996, 8):
    cap.append(rect(x, 322, 3, 42, fill=MARBLE2))
cap.append(rect(866, 314, 138, 6, fill=MARBLE))
cap.append(rect(884, 292, 102, 24, fill=MARBLE2))
for x in range(888, 984, 9):
    cap.append(rect(x, 296, 3, 16, fill=MARBLE3))
cap.append(path(f"M884 293 Q884 214 {CX} 206 Q986 214 986 293 Z", fill=MARBLE))
for k in range(-4, 5):
    cap.append(path(f"M{CX + k * 11} 292 Q{CX + k * 8} 240 {CX} 207", fill="none", stroke=MARBLE2, stroke_width=1.6))
cap.append(path(f"M886 268 Q{CX} 258 984 268", fill="none", stroke=MARBLE2, stroke_width=2))
cap.append(rect(CX - 9, 182, 18, 26, fill=MARBLE))
cap.append(path(f"M{CX - 11} 184 Q{CX} 170 {CX + 11} 184 Z", fill=MARBLE2))
cap.append(rect(CX - 2, 158, 4, 16, fill=MARBLE3))
cap.append(circle(CX, 157, 3, fill=MARBLE3))
# lit windows on the wings
for x in range(712, 1160, 22):
    if not 855 < x < 1015:
        cap.append(rect(x, 440, 6, 9, fill=GOLD2, opacity=0.7))
body.append(group(cap))

# avenue trees and distant buildings on both sides of the vista
trees = []
for x, y, r in ((560, 470, 44), (620, 478, 40), (680, 474, 36), (1150, 476, 40), (1100, 482, 30)):
    trees += cloud_puffs(R, x, y - r * 0.6, r * 1.6, r, 6, r * 0.45, r * 0.75, fill=TREE2)
body.append(group(trees))

# ---------------- ground and avenue ----------------
body.append(rect(0, HZ, 1200, 430, fill="#13281f"))
body.append(rect(0, HZ, 1200, 430, fill="url(#rdots)", opacity=0.25))
AVE = [(250, 900), (1200, 900), (1200, 760), (985, HZ), (880, HZ)]
body.append(poly(AVE, fill="url(#road)"))
# sidewalk edges and dashed centre line converging on the Capitol
body.append(path("M250 900 L880 470", stroke=MARBLE3, stroke_width=4, opacity=0.6))
body.append(path("M1200 760 L985 470", stroke=MARBLE3, stroke_width=4, opacity=0.6))
for i in range(12):
    t0, t1 = i / 12, (i + 0.5) / 12
    x0, y0 = 760 + (932 - 760) * t0 ** 0.6, 900 - (900 - HZ) * t0 ** 0.6
    x1, y1 = 760 + (932 - 760) * t1 ** 0.6, 900 - (900 - HZ) * t1 ** 0.6
    body.append(path(f"M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}", stroke=GOLD, stroke_width=max(1.5, 7 * (1 - t0)),
                     opacity=0.55))

# ---------------- White House north portico (left middle ground) ----------------
WX, WY = 40, 600  # left edge, ground line
wh = [ellipse(270, 520, 330, 170, fill="url(#domeglow)", opacity=0.6)]
wh.append(rect(WX, 448, 460, 152, fill=MARBLE))
wh.append(rect(WX, 440, 460, 10, fill=MARBLE2))
for x in range(WX + 6, WX + 460, 14):  # roof balustrade
    wh.append(rect(x, 428, 5, 12, fill=MARBLE2))
wh.append(rect(WX, 425, 460, 5, fill=MARBLE2))
# windows: two rows, with alternating pediments
for row, y in enumerate((474, 540)):
    for x in list(range(WX + 18, WX + 150, 40)) + list(range(WX + 330, WX + 450, 40)):
        wh.append(rect(x, y, 18, 32, fill=GOLD, opacity=0.9))
        wh.append(rect(x + 8, y, 2, 32, fill=MARBLE2))
        if row == 0:
            wh.append(poly([(x - 3, y - 2), (x + 9, y - 10), (x + 21, y - 2)], fill=MARBLE2))
        else:
            wh.append(rect(x - 3, y - 5, 24, 4, fill=MARBLE2))
# portico: pediment and columns
PX = WX + 240
wh.append(poly([(PX - 108, 440), (PX, 386), (PX + 108, 440)], fill=MARBLE))
wh.append(poly([(PX - 92, 434), (PX, 395), (PX + 92, 434)], fill=MARBLE2))
wh.append(circle(PX, 420, 8, fill=MARBLE))
wh.append(rect(PX - 110, 438, 220, 10, fill=MARBLE))
wh.append(rect(PX - 100, 448, 200, 152, fill=MARBLE3, opacity=0.6))
wh.append(rect(PX - 22, 520, 44, 80, fill="#3b2c1c"))
wh.append(path(f"M{PX - 22} 520 Q{PX} 500 {PX + 22} 520 Z", fill=GOLD, opacity=0.9))
wh.append(circle(PX, 486, 13, fill=GOLD2, opacity=0.9))  # lantern under the portico
for i in range(8):
    x = PX - 98 + i * 28
    wh.append(rect(x, 450, 12, 150, fill=MARBLE))
    wh.append(rect(x - 2, 448, 16, 5, fill=MARBLE2))
    wh.append(rect(x + 8, 452, 3, 146, fill=MARBLE2, opacity=0.7))
# floodlight wash from the lawn
wh.append(rect(WX, 448, 460, 152, fill="url(#flood)"))
body.append(group(wh))
# lawn and the iron fence with the gate
body.append(rect(0, 600, 560, 40, fill="#16301f"))
fence = [rect(0, 640, 520, 4, fill=INK)]
for x in range(4, 520, 9):
    if not 418 < x < 480:
        fence.append(rect(x, 606, 3, 38, fill=INK))
        fence.append(poly([(x - 1, 606), (x + 1.5, 600), (x + 4, 606)], fill=INK))
for gx in (412, 482):
    fence.append(rect(gx, 590, 10, 56, fill=INK))
    fence.append(circle(gx + 5, 586, 7, fill=GOLD2))
    fence.append(circle(gx + 5, 586, 22, fill="url(#lampglow)"))
body.append(group(fence))
body.append(ellipse(450, 650, 150, 26, fill=GOLD2, opacity=0.18))

# ---------------- the order: a towering blank sheet across the avenue ----------------
DOC = group([
    ellipse(130, 470, 230, 260, fill="url(#paperglow)"),
    path("M0 0 L240 0 L260 20 L260 470 L0 470 Z", fill="url(#paper)"),
    path("M240 0 L240 20 L260 20 Z", fill=MARBLE2),
    rect(28, 34, 150, 10, fill="#b9ad90"),
    *[rect(28, 76 + k * 30, 204 - (k % 3) * 26, 6, fill="#cfc4a6") for k in range(9)],
    rect(28, 360, 110, 6, fill="#cfc4a6"),
    path("M172 392 L160 452 L176 440 L186 456 L190 394 Z", fill=CRIMSON),
    path("M196 392 L214 448 L222 432 L236 444 L214 390 Z", fill="#9e232b"),
    circle(190, 392, 30, fill=CRIMSON),
    circle(190, 392, 22, fill="none", stroke="#e0646a", stroke_width=2.5),
    circle(190, 392, 12, fill="#9e232b"),
    path("M260 20 L260 470", stroke=GOLD2, stroke_width=4, opacity=0.85),          # rim light from the Capitol side
    path("M0 0 Q-26 -6 -30 22 Q-14 12 0 18 Z", fill=MARBLE2),                      # top-left corner curling forward
    rect(0, 0, 260, 470, fill="url(#rdots)", opacity=0.12),
], transform="translate(560 252) rotate(-3)")
# the sheet's long shadow, thrown toward the viewer by the Capitol's floodlight glow behind it
body.append(poly([(566, 718), (818, 706), (700, 900), (300, 900)], fill=INK, opacity=0.42))
body.append(DOC)

# ---------------- street lamps with light cones ----------------
for lx, ly, h in ((1182, 880, 330), (1050, 690, 170), (995, 590, 90)):
    s = h / 330
    body.append(poly([(lx - 6 * s, ly - h + 30 * s), (lx + 6 * s, ly - h + 30 * s), (lx + 120 * s, ly),
                      (lx - 120 * s, ly)], fill="url(#cone)", opacity=0.55))
    body.append(rect(lx - 4 * s, ly - h, 8 * s, h, fill=INK))
    body.append(rect(lx - 14 * s, ly - h - 34 * s, 28 * s, 36 * s, rx=4 * s, fill=GOLD2))
    body.append(circle(lx, ly - h - 16 * s, 70 * s, fill="url(#lampglow)"))

# ---------------- the queue of contractors ----------------
FOLDER = rect(-7, -5, 14, 10, fill="#d9a441")
FOLDER2 = rect(-7, -5, 14, 10, fill="#e8e1cf")
BOX = group([rect(-9, -10, 20, 13, fill="#b98a55"), rect(-9, -10, 20, 3, fill="#9a6f40")])
SKIN = ["#8a5a3b", "#c98e6b", "#e2b48f", "#6b4228", "#b07a55", "#f0c8a4"]


def walker(x, y, h, kind, i, facing=-1, look_up=False):
    step = 1 if i % 2 else -1
    look = Look(skin=SKIN[i % len(SKIN)], hair=["#2a1d18", "#5a3a22", "#9a9a9a", "#16110e"][i % 4])
    item = None
    pose = Pose(back_arm=(-20 * step, 12), front_arm=(20 * step, 14), back_leg=(-16 * step, -8),
                front_leg=(16 * step, -2), head_tilt=-12 if look_up else 0)
    if kind == "hardhat":
        look.top, look.bottom, look.vest = "#d9862f", "#2f3e52", True
        look.hair_style, look.hair = "cap", "#f2c230"
        pose.front_arm, item = (40, 40), {"front": FOLDER}
    elif kind == "suit":
        look.top, look.bottom, look.accent, look.long_tie = "#2b3548", "#1f2533", CRIMSON if i % 5 == 0 else "#7d93a8", True
        item = {"front": FOLDER2} if i % 2 else {"back": FOLDER}
    elif kind == "box":
        look.top, look.bottom = "#5d7f6e", "#3a2f2a"
        look.hair_style = "bun"
        pose.front_arm, pose.back_arm, item = (55, 45), (50, 50), {"front": BOX}
    elif kind == "coat":
        look.top, look.bottom, look.coat = "#8c5a46", "#2b2b38", True
        look.hair_style = "long"
        item = {"front": FOLDER2}
    # long cast shadow away from the lamps (toward the lower left)
    body.append(ellipse(x - h * 0.28, y + 2, h * 0.32, h * 0.04, fill=INK, opacity=0.4))
    body.append(figure(x, y, h, facing=facing, pose=pose, look=look, hand_items=item))


KINDS = ["hardhat", "suit", "box", "suit", "coat", "hardhat", "suit", "box"]
# path of the queue: from the right foreground up the avenue to the sheet, then left to the White House gate
queue = [
    (1080, 892, 210, False), (930, 848, 186, False), (800, 800, 160, False),   # foreground, walking toward the sheet
    (700, 760, 140, True), (620, 742, 128, True),                              # at the sheet, looking up
    (548, 720, 116, False), (480, 700, 104, False), (418, 684, 94, False),     # turned aside toward the gate
    (362, 670, 86, False), (312, 660, 80, False), (268, 652, 74, False),
]
# path on the lawn where the line bends to the gate (illustrative dashed track)
body.append(path("M760 790 Q640 740 450 672", fill="none", stroke=GOLD, stroke_width=3, stroke_dasharray="4 12",
                 opacity=0.7))
for i, (x, y, h, up) in enumerate(reversed(queue)):
    walker(x, y, h, KINDS[i % len(KINDS)], i, look_up=up)

# ---------------- foreground framing: dark elm branches ----------------
leaves = []
leaves += cloud_puffs(R, 80, 60, 260, 120, 12, 40, 80, fill=TREE)
leaves += cloud_puffs(R, 0, 200, 120, 220, 8, 40, 70, fill=TREE)
body.append(group(leaves))
body.append(path("M0 300 Q60 220 140 140 Q200 90 280 60", fill="none", stroke=TREE, stroke_width=14))

body.append(grain_overlay(opacity=0.3))

title = "The detour on Pennsylvania Avenue"
desc = ("Editorial illustration for Nov. 21, 2026. At night on Pennsylvania Avenue, the floodlit Capitol dome glows "
        "at the far end of the road, but a towering blank sheet with a red seal, a symbol of President Trump's new "
        "executive order, stands across the avenue. A line of generic federal contractors, hard-hat workers and office "
        "staff with folders and boxes, turns aside at the sheet and queues toward the White House's north portico "
        "and gate. The order directs contractors to check with the White House before answering Congress.")
save(document(defs, body, title, desc), OUT)
