"""Daily artwork, 2026-11-17: the U.S. loses its measles-elimination status.

Visual idea: the map breaks out in spots. Inside a pediatric clinic at dusk, a nurse leans in to
vaccinate a toddler held on a parent's lap, while the whole back wall is a giant glowing light-box
map of the lower 48 states, rashed with clusters of red dots that ripple outward like a spreading
outbreak (an openly symbolic, not data-accurate, map). Window light slants across the floor; a
second family waits in the doorway.

Verified (brief): on Nov. 17 PAHO announced the U.S. lost the measles-elimination status it held
since 2000; more than 5,400 cases in 2026 across 45 states and D.C. (CBS, CNBC); officials urged
MMR vaccination.
Drawn: generic nurse, parents and children; a stylized U.S. outline with illustrative dots.
Not drawn: officials, named people, sick or suffering people, any text or numbers.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-17"
R = rng(20261117)
OUT = Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg"

# palette: midnight-indigo wall, light-box cream, measles red, scrubs mint, warm mustard, lilac floor
WALL1, WALL2 = "#1c1d3a", "#2a2b55"
SCREEN, SCREEN2 = "#fbf1dc", "#f2dcb4"
RED, RED2 = "#e3342f", "#ff7a59"
MINT, MINT2 = "#5cc2a6", "#3c9a83"
MUSTARD = "#eaa83a"
FLOOR1, FLOOR2 = "#8c7fb3", "#6f6399"
INK = "#121226"

# --- simplified lower-48 outline (lon, lat) -----------------------------------
US = [(-124.7, 48.4), (-123.0, 49.0), (-95.2, 49.0), (-89.6, 48.0), (-84.8, 46.6), (-83.5, 46.0),
      (-82.4, 43.0), (-83.1, 42.0), (-79.0, 42.5), (-79.2, 43.4), (-76.4, 44.2), (-74.8, 45.0),
      (-71.5, 45.0), (-70.0, 46.7), (-69.2, 47.4), (-67.8, 47.1), (-67.0, 44.8), (-70.2, 43.7),
      (-70.7, 42.6), (-70.0, 41.8), (-71.4, 41.4), (-73.9, 40.6), (-74.0, 39.5), (-75.0, 38.8),
      (-76.0, 37.0), (-75.5, 35.3), (-77.9, 33.9), (-79.9, 32.7), (-81.4, 30.4), (-80.1, 26.9),
      (-80.4, 25.2), (-81.8, 26.0), (-82.8, 27.9), (-84.3, 30.0), (-86.5, 30.4), (-89.6, 30.2),
      (-89.4, 29.0), (-90.5, 29.1), (-93.8, 29.7), (-95.0, 29.2), (-97.2, 27.7), (-97.4, 25.9),
      (-99.5, 27.5), (-101.4, 29.8), (-103.0, 29.0), (-104.5, 29.6), (-106.5, 31.8), (-108.2, 31.3),
      (-111.0, 31.3), (-114.8, 32.5), (-117.1, 32.5), (-118.5, 34.0), (-120.6, 34.6), (-121.9, 36.6),
      (-122.5, 37.8), (-123.8, 39.8), (-124.2, 41.9), (-124.1, 43.7), (-124.0, 46.3)]
MX0, MY0, KX, KY = 150, 72, 15.3, 17.4


def proj(lon, lat):
    return MX0 + (lon + 125) * KX, MY0 + (49 - lat) * KY


MAP = [proj(*p) for p in US]


def inside(x, y, pts=MAP):
    c = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi:
            c = not c
        j = i
    return c


defs = [
    grain_filter(),
    linear("wall", [(0, WALL1), (1, WALL2)]),
    radial("glow", [(0, "#fff6e0", 0.55), (0.6, "#ffd9a0", 0.18), (1, "#ffd9a0", 0)], r=0.6),
    linear("screen", [(0, SCREEN), (1, SCREEN2)]),
    linear("beam", [(0, "#d6fff2", 0.42), (1, "#d6fff2", 0)], x2=1, y2=0.6),
    linear("dusk", [(0, "#4b4f8f"), (0.55, "#c98aa8"), (1, "#ffc98a")]),
    radial("rim", [(0, "#ffd9a0", 0.35), (1, "#ffd9a0", 0)], r=0.5),
    linear("floor", [(0, FLOOR2), (1, FLOOR1)]),
    halftone("dots", "#ffffff", dot=1.4, spacing=7),
    halftone("reddots", RED, dot=1.6, spacing=6, angle=30),
    blur("soft", 6),
]

body = []
# back wall
body.append(rect(0, 0, 1200, 900, fill="url(#wall)"))
body.append(rect(0, 0, 1200, 640, fill="url(#dots)", opacity=0.05))

# light-box frame + glow
body.append(ellipse(600, 300, 640, 380, fill="url(#glow)"))
body.append(rect(118, 40, 964, 520, rx=10, fill="#0e0f22"))
body.append(rect(130, 52, 940, 496, rx=6, fill="url(#screen)"))
# faint grid lines on the screen
for gx in range(130, 1070, 47):
    body.append(path(f"M{gx} 52 V548", stroke="#e6cfa3", stroke_width=1, opacity=0.6))
for gy in range(52, 548, 47):
    body.append(path(f"M130 {gy} H1070", stroke="#e6cfa3", stroke_width=1, opacity=0.6))

# the map
d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in MAP) + " Z"
body.append(path(d, fill="#fff9ee", stroke=INK, stroke_width=3.5, stroke_linejoin="round"))
body.append(path(d, fill="url(#reddots)", opacity=0.10))

# outbreak dots: hotspots with ripples, plus scattered spots
HOT = [(-102.2, 33.2, 1.0), (-77.2, 40.6, 1.1), (-112.6, 37.0, 0.8), (-82.0, 34.8, 0.8),
       (-89.5, 43.6, 0.6), (-75.5, 42.5, 0.5), (-96.5, 36.0, 0.5), (-117.5, 35.5, 0.45)]
dots = []
for lon, lat, w in HOT:
    cx, cy = proj(lon, lat)
    for k, rr in enumerate((70, 48, 28)):
        body.append(circle(round(cx, 1), round(cy, 1), round(rr * w + 6, 1), fill="none", stroke=RED2,
                           stroke_width=2, opacity=round(0.25 + 0.15 * k, 2)))
    n = int(26 * w) + 6
    for _ in range(n):
        a = R.uniform(0, 2 * math.pi)
        rad = abs(R.gauss(0, 26 * w))
        x, y = cx + math.cos(a) * rad, cy + math.sin(a) * rad * 0.8
        if inside(x, y):
            dots.append((x, y, R.uniform(3.2, 7.5)))
tries = 0
while tries < 900:
    tries += 1
    x, y = R.uniform(150, 1060), R.uniform(70, 500)
    if inside(x, y) and R.random() < 0.18:
        dots.append((x, y, R.uniform(2.5, 5.2)))
for x, y, r in dots:
    body.append(circle(round(x, 1), round(y, 1), round(r, 1), fill=RED))
    body.append(circle(round(x - r * 0.3, 1), round(y - r * 0.3, 1), round(r * 0.35, 1), fill="#ffb3a0", opacity=0.8))

# window on the left with a cool slanted beam
body.append(rect(0, 120, 96, 380, fill="url(#dusk)"))
for bx, bw, bh in ((0, 22, 120), (20, 18, 170), (36, 26, 95), (60, 14, 140), (72, 24, 110)):
    body.append(rect(bx, 500 - bh, bw, bh, fill="#2c3a5e"))
    for wy in range(510 - bh, 495, 14):
        if R.random() < 0.5:
            body.append(rect(bx + 5, wy, 4, 5, fill="#ffd98a", opacity=0.9))
body.append(rect(0, 120, 96, 380, fill="none", stroke="#0e0f22", stroke_width=10))
body.append(path("M48 120 V500 M0 310 H96", stroke="#0e0f22", stroke_width=6))
body.append(poly([(96, 130), (96, 500), (900, 900), (520, 900)], fill="url(#beam)"))

# floor
body.append(rect(0, 640, 1200, 260, fill="url(#floor)"))
for i in range(-10, 22):
    x0 = 600 + i * 70
    body.append(path(f"M{600 + i * 22} 640 L{x0 + i * 40} 900", stroke=FLOOR2, stroke_width=2, opacity=0.6))
for yy in (668, 705, 752, 812, 885):
    body.append(path(f"M0 {yy} H1200", stroke=FLOOR2, stroke_width=2, opacity=0.6))
body.append(rect(0, 628, 1200, 14, fill="#3b3a6a"))
body.append(poly([(96, 500), (96, 640), (900, 900), (520, 900)], fill="#d6fff2", opacity=0.12))

# doorway on the right with a waiting family
body.append(rect(1090, 230, 110, 410, fill="#f6d9a6"))
body.append(rect(1082, 222, 118, 418, fill="none", stroke="#0e0f22", stroke_width=12))
body.append(poly([(1090, 640), (1200, 640), (1200, 700), (1040, 700)], fill="#f6d9a6", opacity=0.25))
body.append(figure(1152, 636, 300, facing=-1,
                   pose=Pose(back_arm=(-8, 6), front_arm=(14, 8), head_tilt=8),
                   look=Look(skin="#8a5a3c", top="#c4547a", bottom="#2d2d4a", hair="#1a1210", hair_style="bun")))
body.append(figure(1112, 636, 150, facing=-1,
                   pose=Pose(back_arm=(-30, 30), front_arm=(-25, 10)),
                   look=Look(skin="#8a5a3c", top=MUSTARD, bottom="#3a6ea5", hair="#1a1210")))

# warm light pool spilling from the light-box onto the floor and the figures
body.append(ellipse(600, 650, 560, 90, fill="url(#rim)"))
# long shadows on the floor
body.append(ellipse(700, 860, 280, 26, fill=INK, opacity=0.35, filter="url(#soft)"))

# chair
CH = "#3b3a6a"
body.append(rect(700, 690, 210, 26, rx=8, fill=CH))
body.append(rect(860, 520, 30, 190, rx=8, fill=CH))
body.append(path("M715 716 L705 860 M890 716 L900 860", stroke=CH, stroke_width=12, stroke_linecap="round"))

# parent seated, facing left, holding the toddler
PS = 330
parent = figure(820, 690 + 46 * PS / 100 - 24 * PS / 100 * 0.0, PS, facing=-1,
                pose=Pose(back_arm=(55, 70), front_arm=(60, 60), back_leg=(85, -85), front_leg=(80, -80),
                          head_tilt=18),
                look=Look(skin="#e3b08a", top=MUSTARD, bottom="#2d3e6b", hair="#5a3a22", hair_style="short",
                          face="smile"))
body.append(parent)

# toddler on the lap
body.append(figure(772, 768, 175, facing=-1,
                   pose=Pose(back_arm=(20, 30), front_arm=(70, 10), back_leg=(85, -75), front_leg=(80, -70),
                             head_tilt=-6),
                   look=Look(skin="#e3b08a", top="#f2f2f2", bottom="#5cc2a6", hair="#7a4a26", face="neutral")))

# nurse leaning in from the left with a syringe
syringe = group([rect(0, -1.1, 7, 2.2, rx=0.5, fill="#f4f4f4", stroke="#7a7a8a", stroke_width=0.3),
                 rect(1.5, -0.7, 3, 1.4, fill="#ffb3a0"),
                 path("M7 0 L10.5 0", stroke="#9aa0a6", stroke_width=0.5), rect(-2, -1.6, 2, 3.2, fill="#7a7a8a")])
body.append(figure(540, 870, 390, facing=1,
                   pose=Pose(back_arm=(40, 50), front_arm=(68, 12), back_leg=(-10, 0), front_leg=(10, 0),
                             lean=10, head_tilt=14),
                   look=Look(skin="#b7794f", top=MINT, top_shade=MINT2, bottom=MINT2, shoes="#f4f4f4",
                             hair="#2a1d18", hair_style="bun", face="smile"),
                   hand_items={"front": syringe}))

# warm rim glow from the map over the group
body.append(ellipse(680, 560, 260, 120, fill="url(#rim)", style="mix-blend-mode:screen"))

# foreground: counter edge bottom-left with supply tray
body.append(rect(0, 800, 330, 100, fill="#141530"))
body.append(rect(0, 792, 340, 14, rx=4, fill="#2a2b55"))
body.append(rect(60, 760, 110, 34, rx=4, fill="#f4f4f4"))
body.append(rect(270, 742, 44, 52, rx=6, fill="#cfe9ff", opacity=0.55))
for cx_, cy_ in ((282, 780), (296, 772), (305, 784), (288, 762), (300, 758)):
    body.append(circle(cx_, cy_, 8, fill="#ffffff"))
body.append(rect(200, 740, 50, 54, rx=4, fill=RED))
body.append(rect(206, 732, 38, 10, rx=2, fill="#b02520"))

body.append(grain_overlay(opacity=0.32))

svg = document(
    defs, body,
    "The U.S. loses its measles-elimination status",
    "Editorial illustration. In a pediatric clinic a nurse in mint scrubs leans in with a syringe to vaccinate a "
    "toddler held on a parent's lap, while a second family waits in the doorway. Behind them the whole wall is a "
    "glowing map of the lower 48 states covered in clusters of red dots with rippling rings, an illustrative "
    "symbol of measles spreading. Represents the Pan American Health Organization's Nov. 17, 2026 announcement "
    "that the United States has lost its measles-elimination status.",
)
save(svg, OUT)
