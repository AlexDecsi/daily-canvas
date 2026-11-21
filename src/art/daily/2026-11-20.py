"""Daily artwork, 2026-11-20: federal jury convicts a man of starting the fire that became the Palisades Fire.

Visual idea: the fire beneath the courtroom. A cross-section: the courtroom's tall back wall opens onto an
illustrative night view of the Pacific Palisades hills over the ocean, and under the hillside a thin glowing
thread of embers creeps through tangled roots from a small Jan. 1 spark (left) to a wall of flame on the
ridge (right), the prosecution's 'holdover fire' account drawn as an obvious diagram. Below, in a warm
spotlight, the jury of twelve sits in its box, the judge at the bench, and the generic defendant stands
between his two attorneys.

Verified (brief): on Nov. 20 a federal jury in Los Angeles convicted Jonathan Rinderknecht on both counts in a
retrial (AP, NBC); prosecutors said a Jan. 1, 2025 fire smoldered underground in roots and flared on Jan. 7
as the Palisades Fire (AP, NBC); 12 people died (AP, NBC); the jury was six men and six women (NBC);
he showed little reaction and hugged his attorneys (AP).
Drawn: generic, faceless defendant (private individual); generic attorneys, judge and jurors; the hillside,
houses and flames as illustration. Not drawn: any text, victims, bodies, faces of real people, courthouse
architecture, specific houses.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-20"
R = rng(20261120)
OUT = Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg"

# palette: smoky teal-charcoal night, ember orange/red, walnut courtroom, cream light
SKY1, SKY2 = "#0f1f26", "#24434a"
SEA = "#1c3a46"
RIDGE, RIDGE2 = "#0a1418", "#142328"
SOIL, SOIL2 = "#2a1a16", "#3a241c"
EMBER, EMBER2, FLAME, FLAME2 = "#ff5a1f", "#ff8a2a", "#ffc23d", "#fff0b0"
WOOD, WOOD2, WOOD3 = "#7a4527", "#5a311c", "#a2643a"
CREAM = "#f6e7c6"
INK = "#0b0e10"

defs = [
    grain_filter(),
    linear("sky", [(0, SKY1), (1, SKY2)]),
    linear("soil", [(0, SOIL2), (1, SOIL)]),
    linear("wall", [(0, WOOD2), (1, "#3f2214")]),
    linear("floor", [(0, "#4a2a18"), (1, "#24130b")]),
    linear("beam", [(0, "#ffe7b0", 0.55), (1, "#ffe7b0", 0)]),
    radial("fireglow", [(0, "#ffb347", 0.85), (0.45, EMBER, 0.35), (1, EMBER, 0)]),
    radial("spark", [(0, "#ffe3a0", 1), (0.4, EMBER2, 0.6), (1, EMBER, 0)]),
    halftone("dots", "#5f8f96", dot=1.5, spacing=9),
    halftone("wdots", "#c07a46", dot=1.2, spacing=7, angle=30),
    linear("spill", [(0, EMBER, 0.38), (1, EMBER, 0)]),
    blur("soft", 6),
    blur("glowb", 3),
]

body = []

# ======================= UPPER PANEL: the hillside view (inside the wall opening) =======================
WX0, WY0, WX1, WY1 = 60, 40, 1140, 470   # opening in the courtroom's back wall
GL = 300                                   # ground line of the hillside (approx)
view = []
view.append(rect(WX0, WY0, WX1 - WX0, WY1 - WY0, fill="url(#sky)"))
view.append(rect(WX0, WY0, WX1 - WX0, 260, fill="url(#dots)", opacity=0.25))
# moon-less night; distant ocean at left
view.append(poly([(WX0, 250), (430, 262), (430, 330), (WX0, 330)], fill=SEA))
for k in range(6):
    y = 268 + k * 9
    view.append(path(f"M{WX0 + 10 + k * 14} {y} L{380 - k * 20} {y + 1}", stroke="#4f8a95", stroke_width=1.4, opacity=0.5))
# fire glow behind the right ridge
view.append(ellipse(900, 230, 360, 220, fill="url(#fireglow)"))
# far ridge (Santa Monica Mountains)
view.append(path(f"M{WX0} 250 Q220 190 360 215 Q470 160 600 170 Q720 110 840 140 Q960 100 1060 150 L{WX1} 170 "
                 f"L{WX1} 330 L{WX0} 330 Z", fill=RIDGE2))
# smoke column off the burning ridge, leaning left with the wind
smoke = []
for i in range(14):
    t = i / 13
    cx, cy = 930 - t * 330, 210 - t * 150
    r = 40 + t * 70
    smoke += cloud_puffs(R, cx, cy, r * 1.7, r * 0.8, 6, r * 0.35, r * 0.6,
                         fill="#3b3a3f" if i % 2 else "#4a4448", opacity=0.85)
view.append(group(smoke))
view.append(group(cloud_puffs(R, 900, 200, 240, 40, 10, 20, 38, fill=EMBER, opacity=0.35)))
# near hillside surface with house silhouettes stepping up the slope
HILL = (f"M{WX0} 330 Q200 300 330 300 Q470 296 560 270 Q680 236 800 222 Q930 206 1020 216 Q1090 222 {WX1} 230")
view.append(path(HILL + f" L{WX1} {GL + 60} L{WX0} {GL + 60} Z", fill=RIDGE))
houses = []
for hx, hy, w, lit in ((170, 312, 34, True), (250, 302, 40, True), (330, 300, 30, False), (420, 294, 38, True),
                       (500, 282, 34, True), (590, 262, 40, False), (660, 246, 34, True)):
    houses.append(rect(hx, hy - 20, w, 22, fill="#081013"))
    houses.append(poly([(hx - 4, hy - 20), (hx + w / 2, hy - 34), (hx + w + 4, hy - 20)], fill="#081013"))
    if lit:
        houses.append(rect(hx + 6, hy - 14, 7, 7, fill="#ffd98a", opacity=0.85))
        houses.append(rect(hx + w - 13, hy - 14, 7, 7, fill="#ffd98a", opacity=0.6))
# palms on the slope
for px, py, h in ((210, 312, 46), (465, 290, 52), (625, 256, 44)):
    houses.append(path(f"M{px} {py} Q{px + 3} {py - h / 2} {px + 1} {py - h}", stroke="#081013", stroke_width=3, fill="none"))
    for a in range(-70, 90, 32):
        ra = math.radians(a - 90)
        houses.append(path(f"M{px + 1} {py - h} Q{px + 1 + 9 * math.cos(ra)} {py - h - 8} "
                           f"{px + 1 + 17 * math.cos(ra + 0.5)} {py - h + 6 + 6 * abs(math.sin(ra))}",
                           stroke="#081013", stroke_width=2.4, fill="none"))
view.append(group(houses))
# wall of flame along the upper right ridge
flames = []
for i in range(26):
    fx = 740 + i * 15 + R.uniform(-4, 4)
    base = 226 - (fx - 740) * 0.03 + (fx - 1000) ** 2 * 0.0002
    fh = R.uniform(70, 170) * (1 - abs(fx - 930) / 420)
    flames.append(path(f"M{fx - 13:.1f} {base:.1f} Q{fx - 6:.1f} {base - fh * 0.6:.1f} {fx + R.uniform(-6, 6):.1f} "
                       f"{base - fh:.1f} Q{fx + 8:.1f} {base - fh * 0.5:.1f} {fx + 13:.1f} {base:.1f} Z",
                       fill=EMBER if i % 3 == 0 else EMBER2))
for i in range(18):
    fx = 770 + i * 18 + R.uniform(-4, 4)
    base = 228 - (fx - 740) * 0.03 + (fx - 1000) ** 2 * 0.0002
    fh = R.uniform(30, 90) * (1 - abs(fx - 930) / 460)
    flames.append(path(f"M{fx - 7:.1f} {base:.1f} Q{fx:.1f} {base - fh:.1f} {fx + 7:.1f} {base:.1f} Z", fill=FLAME))
view.append(group(flames))
for i in range(40):
    sx, sy = R.uniform(640, 1130), R.uniform(60, 220)
    view.append(circle(round(sx, 1), round(sy, 1), round(R.uniform(1.2, 3.2), 1), fill=FLAME if i % 2 else EMBER2,
                       opacity=round(R.uniform(0.5, 0.95), 2)))
# cross-section: soil band under the hillside, with tangled roots
SOIL_TOP = HILL
view.append(path(f"M{WX0} 352 Q200 322 330 322 Q470 318 560 292 Q680 258 800 244 Q930 228 1020 238 Q1090 244 "
                 f"{WX1} 252 L{WX1} {WY1} L{WX0} {WY1} Z", fill="url(#soil)"))
view.append(path(f"M{WX0} 352 Q200 322 330 322 Q470 318 560 292 Q680 258 800 244 Q930 228 1020 238 Q1090 244 "
                 f"{WX1} 252 L{WX1} {WY1} L{WX0} {WY1} Z", fill="url(#wdots)", opacity=0.18))
roots = []
for i in range(30):
    x = 110 + i * 34 + R.uniform(-10, 10)
    top = 345 - (x - 60) * 0.1
    d = f"M{x:.1f} {top:.1f}"
    cx, cy = x, top
    for k in range(4):
        nx, ny = cx + R.uniform(-30, 30), cy + R.uniform(18, 34)
        d += f" Q{(cx + nx) / 2 + R.uniform(-12, 12):.1f} {(cy + ny) / 2:.1f} {nx:.1f} {ny:.1f}"
        cx, cy = nx, ny
    roots.append(path(d, fill="none", stroke="#5a3a28", stroke_width=round(R.uniform(2, 4.5), 1), stroke_linecap="round"))
view.append(group(roots))
# the ember thread: a small spark under the left slope, creeping right through the roots, up to the flames
thread = (f"M300 340 Q360 380 430 362 Q500 344 560 378 Q640 410 700 360 Q750 318 790 300 Q830 280 860 236")
view.append(path(thread, fill="none", stroke=EMBER, stroke_width=11, opacity=0.35, filter="url(#glowb)"))
view.append(path(thread, fill="none", stroke=EMBER2, stroke_width=4.5, stroke_linecap="round",
                 stroke_dasharray="2 9"))
view.append(path(thread, fill="none", stroke=FLAME2, stroke_width=1.6, stroke_linecap="round", opacity=0.8))
view.append(circle(300, 340, 26, fill="url(#spark)"))
view.append(circle(300, 340, 5, fill=FLAME2))
body.append(group(view))

# ======================= the courtroom: wall frame around the opening =======================
wall = [path(f"M0 0 L1200 0 L1200 900 L0 900 Z M{WX0} {WY0} L{WX0} {WY1} L{WX1} {WY1} L{WX1} {WY0} Z",
             fill="url(#wall)", fill_rule="evenodd")]
wall.append(rect(0, 0, 1200, 900, fill="url(#wdots)", opacity=0.08))
# moulding around the opening
wall.append(rect(WX0 - 10, WY0 - 10, WX1 - WX0 + 20, WY1 - WY0 + 20, fill="none", stroke=WOOD3, stroke_width=6))
wall.append(rect(WX0 - 2, WY0 - 2, WX1 - WX0 + 4, WY1 - WY0 + 4, fill="none", stroke="#2c170c", stroke_width=4))
for x in (WX0 - 40, WX1 + 40):
    wall.append(rect(x - 12, 0, 24, 900, fill=WOOD2, opacity=0.6))
body.append(group(wall))

# ======================= lower panel: courtroom interior =======================
FY = 700
# raised judge's bench, centre
BX0, BX1, BTOP = 470, 730, 572
body.append(rect(0, WY1 + 10, 1200, FY - WY1 - 10, fill="#4a2716"))
for x in range(0, 1200, 60):
    body.append(rect(x + 6, WY1 + 22, 48, FY - WY1 - 34, rx=3, fill="none", stroke="#331a0e", stroke_width=2))
# the fire's glow spilling from the opening down the courtroom wall (rim light)
body.append(rect(0, WY1 + 10, 1200, 120, fill="url(#spill)"))
body.append(figure(600, 712, 300, facing=-1, pose=Pose(back_arm=(10, 10), front_arm=(14, 14), head_tilt=6),
                   look=Look(skin="#d9a27c", top="#111214", bottom="#111214", hair="#9a9a9e", build=1.45, face="neutral")))
body.append(rect(BX0, BTOP, BX1 - BX0, FY - BTOP, fill=WOOD))
body.append(rect(BX0 - 12, BTOP - 12, BX1 - BX0 + 24, 16, fill=WOOD3))
for k in range(3):
    body.append(rect(BX0 + 22 + k * 80, BTOP + 30, 56, FY - BTOP - 50, rx=3, fill="none", stroke=WOOD2, stroke_width=3))

# jury box, left: two rows of six seated jurors (six men, six women; generic)
JX0, JX1 = 40, 430
skins = ["#f0c8a8", "#8d5a3c", "#d9a27c", "#5e3a26", "#e8b99a", "#b07a52"]
tops = ["#3d6f7a", "#a24a2e", "#d8c9a6", "#2f3d5a", "#7a5a8a", "#556b3a"]
hairs = ["#2a1d18", "#141417", "#b88a4a", "#5a3a24", "#9a9a9e", "#1d1410"]
for row, (ry, rh) in enumerate(((622, 128), (668, 132))):
    for i in range(6):
        k = (i + row * 3) % 6
        female = (i + row) % 2 == 0
        x = JX0 + 34 + i * 62 + row * 14
        body.append(figure(x, ry, rh, facing=1, pose=Pose(back_arm=(4, 4), front_arm=(8, 6), head_tilt=-3),
                           look=Look(skin=skins[k], top=tops[(k + row) % 6], bottom=INK,
                                     hair=hairs[(k + 2 * row) % 6], hair_style="long" if female else "short",
                                     build=0.95 if female else 1.15)))
    rail_y = ry - 50 if row == 0 else ry - 62
    body.append(rect(JX0, rail_y, JX1 - JX0, FY - rail_y, fill=WOOD if row else WOOD2))
    body.append(rect(JX0 - 6, rail_y - 8, JX1 - JX0 + 12, 10, fill=WOOD3))


# floor
body.append(rect(0, FY, 1200, 200, fill="url(#floor)"))
for x in range(-200, 1400, 90):
    body.append(path(f"M{x} {FY} L{(x - 600) * 1.6 + 600} 900", stroke="#160b05", stroke_width=2, opacity=0.4))

# spotlight cone from above onto the defense table
body.append(poly([(880, WY1 + 10), (960, WY1 + 10), (1150, 900), (700, 900)], fill="url(#beam)"))
body.append(ellipse(925, 830, 210, 40, fill="#ffe7b0", opacity=0.18))

# defense table and the three standing figures: attorney, defendant (generic), attorney
TY = 790
suit_a = Look(skin="#e3b08a", top="#23283a", bottom="#23283a", hair="#3a2a20", accent="#7a2a2a", build=1.2,
              face="neutral")
suit_b = Look(skin="#b98560", top="#2e2a2e", bottom="#2e2a2e", hair="#141417", hair_style="bun", skirt=True,
              build=1.0, face="neutral")
defendant = Look(skin="#e6bf9c", top="#6f7f8a", bottom="#2b2f38", hair="#6a4a30", build=1.05)
for x, look, h, pose in ((830, suit_a, 250, Pose(back_arm=(-8, 10), front_arm=(10, 20), head_tilt=8)),
                         (930, defendant, 252, Pose(back_arm=(-4, 4), front_arm=(4, 4), head_tilt=12)),
                         (1030, suit_b, 236, Pose(back_arm=(-6, 10), front_arm=(14, 30), head_tilt=6))):
    body.append(ellipse(x, TY + 4, 46, 9, fill="#000", opacity=0.35))
    body.append(figure(x, TY, h, facing=-1, pose=pose, look=look))
# table in front of them
body.append(rect(760, 742, 360, 22, fill=WOOD3))
body.append(rect(774, 764, 332, 136, fill=WOOD))
body.append(rect(774, 764, 332, 136, fill="url(#wdots)", opacity=0.2))
body.append(rect(800, 734, 70, 9, fill=CREAM, transform="rotate(-4 835 738)"))
body.append(rect(1000, 735, 56, 8, fill="#e9dcc0", transform="rotate(5 1028 739)"))

# foreground: gallery rail and a few silhouetted spectators from behind (framing)
body.append(rect(0, 846, 700, 14, fill="#1a0e07"))
for x in range(20, 700, 46):
    body.append(rect(x, 860, 10, 40, fill="#1a0e07"))
for x, h in ((120, 330), (300, 360)):
    body.append(figure(x, 1040, h, facing=1, pose=Pose(back_arm=(-4, 4), front_arm=(4, 4)),
                       look=Look(skin=INK, top=INK, bottom=INK, shoes=INK, hair=INK, build=1.25)))

body.append(grain_overlay(opacity=0.32))

title = "Jury convicts man of starting the fire that became the Palisades Fire"
desc = ("Editorial illustration. In a wood-panelled courtroom, a jury of twelve sits in its box at left, a judge "
        "in a black robe sits at the raised bench, and at right a man in a grey jacket stands under a spotlight "
        "between two attorneys at the defense table. The courtroom's back wall opens onto an illustrative night "
        "view of hillside homes above the ocean: beneath the slope, a thin glowing thread of embers creeps through "
        "tangled roots from a small spark to a wall of flame and smoke on the ridge, a diagram of the prosecution's "
        "account that a Jan. 1, 2025 fire smoldered underground before flaring into the Palisades Fire. Represents "
        "the Nov. 20, 2026 federal verdict convicting Jonathan Rinderknecht of starting the fire, which killed 12 people.")
save(document(defs, body, title, desc), OUT)
