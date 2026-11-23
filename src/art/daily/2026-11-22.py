"""Daily artwork, 2026-11-22: Delta outage delays flights nationwide as Thanksgiving travel begins.

Visual idea: the scales tip at the gate. Seen over the shoulders of holiday travelers in a darkened terminal,
a tall window frames a parked airliner at sunset. A huge, obviously symbolic balance beam looms in the sky
behind it, tipped off-level (an airliner on one pan, suitcases on the other), standing for the failed
weight-and-balance system. Outside, ramp workers check a clipboard by the nose (manual workarounds). Inside,
a departures board glows with blank amber rows and travelers wait with rolling bags, backlit by the low sun.

Verified (brief): an outage in Delta's automated weight-and-balance system delayed more than 1,600 Delta
flights Sunday, mostly at Atlanta; Delta used manual workarounds and restored it in the afternoon; Logan
had 80+ delayed Delta flights (NBC News, ABC News, NBC Boston).
Drawn: a generic gate area and unbranded airliner; faceless generic travelers and ramp workers; the
balance as a clearly symbolic sky motif. Not drawn: airline logos, any text, named people, crowds or
confrontations, cancellations as a specific number.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-22"
R = rng(20261122)
OUT = Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg"

# palette: plum dusk, tangerine sun, warm cream, slate interior, one amber accent (the board)
SKY1, SKY2, SKY3 = "#2c1f4a", "#8a3f6b", "#f28a3c"
SUN, SUN2 = "#ffd27a", "#fff1c9"
CREAM, CREAM2 = "#f6ecd8", "#d9cbb0"
SLATE, SLATE2, INK = "#1c1a2b", "#2a2740", "#0f0d18"
AMBER, RED = "#ffb238", "#e2493a"
TARMAC, TARMAC2 = "#4a3a52", "#5d4a63"

WIN_T, WIN_B = 70, 610   # window glass top / bottom
HZ = 470                 # horizon on the airfield

defs = [
    grain_filter(),
    linear("sky", [(0, SKY1), (0.55, SKY2), (1, SKY3)]),
    linear("tarmac", [(0, TARMAC2), (1, TARMAC)]),
    linear("floor", [(0, SLATE2), (1, INK)]),
    linear("shaft", [(0, SUN2, 0.32), (1, SUN2, 0)]),
    radial("sunglow", [(0, SUN2, 0.95), (0.25, SUN, 0.6), (1, SUN, 0)]),
    radial("boardglow", [(0, AMBER, 0.35), (1, AMBER, 0)]),
    halftone("dots", "#b2557a", dot=1.5, spacing=9),
    halftone("fdots", "#3b3757", dot=1.3, spacing=8, angle=30),
]

body = []

# ================= outside: sky, sun, the symbolic balance =================
body.append(rect(0, 0, 1200, 640, fill="url(#sky)"))
body.append(rect(0, 0, 1200, 330, fill="url(#dots)", opacity=0.35))
SX, SY = 830, 440
body.append(ellipse(SX, SY, 420, 300, fill="url(#sunglow)"))
body.append(circle(SX, SY, 62, fill=SUN2))
# long thin clouds across the sun
for (cx, cy, w) in ((700, 380, 300), (980, 405, 240), (420, 300, 260), (1050, 250, 200)):
    body.append(rect(cx - w / 2, cy, w, 7, rx=3.5, fill="#f7b267", opacity=0.55))

# --- the giant balance beam (symbol, drawn as a pale outline in the sky) ---
PX, PY = 750, 195           # pivot
TILT = math.radians(-13)    # left end down
L = 320
lx, ly = PX - L * math.cos(TILT), PY - L * math.sin(TILT)
rx_, ry_ = PX + L * math.cos(TILT), PY + L * math.sin(TILT)
lx, ly, rx_, ry_ = round(lx, 1), round(ly, 1), round(rx_, 1), round(ry_, 1)
BAL = CREAM
bal = []
bal.append(path(f"M{PX} {PY} L{PX} {HZ}", stroke=BAL, stroke_width=10))           # post
bal.append(path(f"M{PX - 50} {HZ} L{PX + 50} {HZ}", stroke=BAL, stroke_width=8))
bal.append(path(f"M{lx} {ly} L{rx_} {ry_}", stroke=BAL, stroke_width=16, stroke_linecap="round"))
bal.append(circle(PX, PY, 16, fill=BAL))
bal.append(circle(PX, PY, 6, fill=SKY2))
bal.append(path(f"M{PX - 14} {PY - 14} L{PX} {PY - 52} L{PX + 14} {PY - 14} Z", fill=BAL))  # pointer
# pans with chains
def pan(ex, ey, drop, load):
    py = ey + drop
    out = [path(f"M{ex} {ey} L{ex - 70} {py}", stroke=BAL, stroke_width=2.5),
           path(f"M{ex} {ey} L{ex + 70} {py}", stroke=BAL, stroke_width=2.5),
           path(f"M{ex - 88} {py} Q{ex} {py + 46} {ex + 88} {py} Z", fill=BAL)]
    return out + load(ex, py)

def pan_jet(ex, py):
    s = 0.62
    return [group(jet_side(0, 0, 1.0, CREAM2, SKY2, windows=False), transform=f"translate({ex - 90 * s:.1f} {py - 26:.1f}) scale({s})")]

def pan_bags(ex, py):
    out = []
    for i, (dx, w, h, c) in enumerate(((-52, 34, 44, AMBER), (-14, 44, 30, RED), (32, 30, 40, CREAM2), (-8, 26, 22, "#7cc6b6"))):
        y0 = py - h - (30 if i == 3 else 0)
        out.append(rect(ex + dx, y0, w, h, rx=5, fill=c))
        out.append(rect(ex + dx + w / 2 - 6, y0 - 7, 12, 8, rx=3, fill="none", stroke=c, stroke_width=3))
    return out

def jet_side(x, y, s, body_c, accent, windows=True, shade="#b9ab95"):
    """Generic unbranded airliner, side view, nose to the left. (x, y) = top-left, length ~ 300*s."""
    def p(d):
        return d
    out = []
    # tail fin and stabiliser
    out.append(path("M232 26 L262 -34 L290 -34 L284 30 Z", fill=body_c))
    out.append(path("M244 22 L268 -28 L282 -28 L276 24 Z", fill=accent, opacity=0.9))
    out.append(path("M250 34 L300 26 L304 34 L258 42 Z", fill=shade))
    # fuselage
    out.append(path("M0 46 Q2 24 34 20 L276 20 Q296 22 300 34 L300 40 Q290 54 260 56 L30 58 Q4 58 0 46 Z", fill=body_c))
    out.append(path("M2 50 Q8 58 30 58 L260 56 Q290 54 300 40 L300 44 Q288 62 260 62 L30 64 Q6 62 2 50 Z", fill=shade))
    out.append(path("M14 30 L34 24 L38 31 L18 35 Z", fill=INK))  # cockpit window
    if windows:
        for k in range(18):
            out.append(rect(52 + k * 11.5, 30, 6, 7, rx=2.5, fill=INK, opacity=0.85))
    out.append(rect(44, 26, 10, 22, rx=2, fill="none", stroke=shade, stroke_width=1.5))  # door
    out.append(path("M24 50 L290 44", stroke=accent, stroke_width=3))
    # wing and engine
    out.append(path("M110 48 L180 48 L232 76 L214 78 Z", fill=shade))
    out.append(rect(118, 56, 46, 18, rx=9, fill=body_c))
    out.append(ellipse(120, 65, 4, 9, fill=INK))
    return [group(out, transform=f"translate({x} {y}) scale({s})")]

bal += pan(lx, ly, 70, pan_jet)
bal += pan(rx_, ry_, 70, pan_bags)
body.append(group(bal, opacity=0.85))

# ================= airfield =================
# distant terminal and control tower
far = [rect(0, HZ - 26, 360, 26, fill="#3a2a4c"), rect(960, HZ - 20, 240, 20, fill="#3a2a4c"),
       rect(1060, HZ - 120, 18, 100, fill="#3a2a4c"), path(f"M1046 {HZ - 118} L1092 {HZ - 118} L1084 {HZ - 146} L1054 {HZ - 146} Z", fill="#3a2a4c"),
       rect(1056, HZ - 142, 26, 10, fill=SUN, opacity=0.7)]
for k in range(12):
    far.append(rect(14 + k * 28, HZ - 18, 12, 5, fill=SUN, opacity=0.6))
body += far
body.append(rect(0, HZ, 1200, 640 - HZ, fill="url(#tarmac)"))
body.append(path(f"M0 {HZ + 40} L1200 {HZ + 22}", stroke=AMBER, stroke_width=3, opacity=0.6))  # taxi line
body.append(path(f"M300 640 Q560 540 1200 520", fill="none", stroke=AMBER, stroke_width=4, opacity=0.5, stroke_dasharray="18 14"))
# long sun reflection on tarmac
body.append(poly([(SX - 40, HZ), (SX + 40, HZ), (SX + 160, 640), (SX - 160, 640)], fill=SUN, opacity=0.18))

# a queue of airliners waiting on the far taxiway (delays)
for qx, qy, qs in ((1150, HZ - 6, 0.34), (1030, HZ - 2, 0.38), (985, HZ + 6, 0.44)):
    body += jet_side(qx, qy, qs, CREAM2, "#4c79b5")
# parked airliner at the gate (nose left, toward jet bridge)
JX, JY, JS = 300, 410, 2.3
body += jet_side(JX, JY, JS, CREAM, "#4c79b5")
# shadow under jet
body.append(ellipse(JX + 160 * JS, JY + 70 * JS + 4, 330, 10, fill=INK, opacity=0.35))
# jet bridge from the left
bridge = [poly([(0, 470), (300, 468), (340, 476), (340, 524), (300, 528), (0, 532)], fill="#6a5873"),
          rect(0, 470, 340, 8, fill="#7d6a86"),
          rect(120, 528, 16, 92, fill="#3a2a4c"), rect(104, 612, 48, 10, fill="#3a2a4c")]
for k in range(5):
    bridge.append(rect(20 + k * 58, 488, 34, 22, rx=3, fill=SUN, opacity=0.35))
body += bridge

# ramp workers by the nose with a clipboard, and a baggage cart
vest_orange = "#ff7a2f"
def ramp(x, y, h, facing, pose, item=None):
    return figure(x, y, h, facing=facing, pose=pose,
                  look=Look(top=vest_orange, bottom="#2c2c3e", hair_style="cap", hair="#1e2a44", vest=True,
                            skin="#a8714f"), hand_items={"front": item} if item else None)
clip = group([rect(-6, -10, 13, 17, fill=CREAM, rx=1.5), rect(-3, -12, 7, 4, fill="#555", rx=1),
              path("M-3 -4 L4 -4 M-3 -1 L4 -1 M-3 2 L2 2", stroke="#888", stroke_width=1)])
body.append(ramp(420, 600, 70, 1, Pose(front_arm=(70, -60), back_arm=(-10, 10), head_tilt=12), clip))
body.append(ramp(462, 602, 72, -1, Pose(front_arm=(35, -20), back_arm=(-8, 8), head_tilt=8)))
# baggage cart
cart = [rect(560, 576, 120, 26, rx=3, fill="#6a5873"), circle(578, 606, 7, fill=INK), circle(662, 606, 7, fill=INK)]
for i, (dx, w, h, c) in enumerate(((8, 26, 24, AMBER), (38, 30, 18, RED), (72, 22, 26, "#7cc6b6"), (98, 18, 16, CREAM2))):
    cart.append(rect(560 + dx, 576 - h, w, h, rx=3, fill=c))
body += cart

# sun flare and glass reflections (on the window panes)
for k, (x0, w) in enumerate(((330, 60), (420, 22), (640, 90), (960, 40), (1040, 16))):
    body.append(poly([(x0, WIN_B), (x0 + w, WIN_B), (x0 + w + 260, WIN_T), (x0 + 260, WIN_T)], fill=SUN2, opacity=0.07))
for a in range(0, 360, 30):
    r1, r2 = 80, 150 if a % 60 else 210
    ax, ay = math.cos(math.radians(a)), math.sin(math.radians(a))
    body.append(path(f"M{SX + ax * r1:.1f} {SY + ay * r1:.1f} L{SX + ax * r2:.1f} {SY + ay * r2:.1f}", stroke=SUN2,
                     stroke_width=2, opacity=0.35))
# ================= the terminal window frame =================
frame = []
frame.append(rect(0, 0, 1200, WIN_T, fill=SLATE))                       # ceiling
frame.append(rect(0, WIN_B, 1200, 900 - WIN_B, fill="url(#floor)"))       # floor
frame.append(rect(0, WIN_B, 1200, 900 - WIN_B, fill="url(#fdots)", opacity=0.4))
frame.append(rect(0, WIN_B - 6, 1200, 18, fill=INK))                       # sill
for x in (0, 300, 600, 900, 1188):
    frame.append(rect(x - 6 if x else 0, WIN_T, 14, WIN_B - WIN_T, fill=INK))
frame.append(rect(0, 330, 1200, 8, fill=INK))
# ceiling lights
for x in range(80, 1200, 200):
    frame.append(rect(x, 26, 80, 8, rx=4, fill=CREAM, opacity=0.5))
body += frame

# sunlight falling through the window onto the floor (long panes of light)
for x0 in (300, 600, 900):
    body.append(poly([(x0 + 10, WIN_B + 12), (x0 + 288, WIN_B + 12), (x0 + 120, 900), (x0 - 280, 900)], fill="url(#shaft)"))

# gate seats: a row of dark chairs in silhouette
seats = []
for k in range(7):
    x = 640 + k * 64
    seats += [rect(x, 662, 54, 12, rx=3, fill=INK), rect(x + 4, 622, 46, 42, rx=6, fill=SLATE2),
              rect(x + 24, 674, 6, 28, fill=INK)]
seats.append(rect(630, 700, 460, 6, fill=INK))
body += seats

# departures board hanging from the ceiling (blank rows, no text)
BX, BY, BW, BH = 70, 96, 300, 176
board = [ellipse(BX + BW / 2, BY + BH / 2, 260, 170, fill="url(#boardglow)"),
         rect(BX + 60, WIN_T, 6, BY - WIN_T, fill=INK), rect(BX + BW - 66, WIN_T, 6, BY - WIN_T, fill=INK),
         rect(BX - 8, BY - 8, BW + 16, BH + 16, rx=6, fill=INK), rect(BX, BY, BW, BH, rx=3, fill="#141223")]
rows = [AMBER, AMBER, RED, AMBER, AMBER, "#5fbf8f", AMBER, AMBER]
for i, c in enumerate(rows):
    y = BY + 12 + i * 20
    board.append(rect(BX + 12, y, 64, 11, rx=2, fill=CREAM, opacity=0.35))
    board.append(rect(BX + 86, y, 120, 11, rx=2, fill=CREAM, opacity=0.25))
    board.append(rect(BX + 216, y, 72, 11, rx=2, fill=c, opacity=0.95))
body += board

# ================= travelers (foreground, backlit) =================
def bag(color, tall=True):
    h = 30 if tall else 22
    return group([path(f"M0 0 L0 {44 - h}", stroke="#9a92a8", stroke_width=2.2),
                  rect(-9, 44 - h, 20, h, rx=4, fill=color),
                  path(f"M-6 {46 - h} L-6 42 M8 {46 - h} L8 42", stroke=_d(color), stroke_width=1.4),
                  circle(-5, 45, 2.4, fill=INK), circle(7, 45, 2.4, fill=INK)])

def _d(c):
    h = c.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#{:02x}{:02x}{:02x}".format(int(r * .7), int(g * .7), int(b * .7))

def traveler(x, y, h, facing, top, bottom, hair, style, pose, item=None, coat=False, skirt=False, skin="#8a5a44"):
    return figure(x, y, h, facing=facing, pose=pose,
                  look=Look(top=top, bottom=bottom, hair=hair, hair_style=style, coat=coat, skirt=skirt, skin=skin,
                            shoes=INK), hand_items={"front": item} if item else None)

phone = rect(-3, -6, 6, 9, rx=1.2, fill="#9fe1ff")
# rim light ellipses behind heads to suggest backlight
T = []
T.append(traveler(150, 860, 300, 1, "#3d2f5c", "#1d1a2c", "#2a1d18", "bun", Pose(front_arm=(18, 6), back_arm=(-12, 8), head_tilt=-6),
                  bag(RED), coat=True, skin="#b07a5a"))
T.append(traveler(300, 830, 250, 1, "#28405c", "#1b1b26", "#120e0c", "cap", Pose(front_arm=(14, 4), back_arm=(-10, 10), head_tilt=-4),
                  bag(AMBER), skin="#6b4432"))
T.append(traveler(232, 836, 170, 1, "#b8466a", "#2a2238", "#3a2418", "long", Pose(front_arm=(25, 10), back_arm=(-6, 6), head_tilt=-8),
                  skirt=True, skin="#d29b7a"))  # child beside the parents
T.append(traveler(1080, 880, 320, -1, "#2e3b30", "#191921", "#55463c", "short", Pose(front_arm=(60, -70), back_arm=(-8, 10), head_tilt=22),
                  phone, skin="#c48d6c"))  # checking a phone
T.append(traveler(930, 840, 220, -1, "#5a2e3e", "#1f1c2a", "#1a1414", "hood", Pose(front_arm=(10, 4), back_arm=(-14, 6), head_tilt=-2),
                  bag("#7cc6b6", tall=False), skin="#8d5c45"))
# low sun behind the travelers: long shadows stretch toward the viewer
for (fx, fy, w) in ((150, 860, 46), (300, 830, 40), (232, 836, 26), (1080, 880, 50), (930, 840, 34)):
    body.append(poly([(fx - w / 2, fy), (fx + w / 2, fy), (fx + w * 1.3 - (fx - SX) * 0.35, 900), (fx - w * 1.3 - (fx - SX) * 0.35, 900)],
                     fill=INK, opacity=0.45))
for t in T:
    body.append(t)
# warm rim light hint on floor near feet
body.append(rect(0, 862, 1200, 38, fill=INK, opacity=0.35))

body.append(grain_overlay(opacity=0.3))

title = "The scales tip at the gate"
desc = ("Editorial illustration for Nov. 22, 2026. From inside a darkened airport terminal at sunset, holiday travelers "
        "with rolling suitcases wait by a tall window and a departures board with blank amber rows. Outside, an unbranded "
        "airliner is parked at the jet bridge, and ramp workers in safety vests check a clipboard by its nose beside a "
        "loaded baggage cart. A huge, symbolic balance beam in the sky tips off-level, with an airliner on one pan and "
        "suitcases on the other. It stands for the failure of Delta's automated weight-and-balance system, which delayed "
        "more than 1,600 Delta flights nationwide as Thanksgiving travel began.")
save(document(defs, body, title, desc), OUT)
