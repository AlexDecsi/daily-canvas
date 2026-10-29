"""Daily artwork, 2026-10-28: Labor and civil rights leader Dolores Huerta dies at 96.

Visual idea: a farmworkers' picket line marches along a vineyard road in
silhouette against a huge setting sun, with a young Dolores Huerta at its head
raising her arm. The vine rows rush toward the sun, and the marchers cast long
shadows toward the viewer: a tribute at dusk to the Delano strike.

Verified (brief): Huerta died Oct. 28 at 96 in Bakersfield, California. In 1962
she co-founded the farmworkers' union that became the United Farm Workers, and
she marched with grape pickers on the Delano grape strike picket line.
Drawn: a historical scene only. Huerta is a young organizer with long dark hair
leading a small line of anonymous farmworkers past the vines. (A UFW flag was
tried in round 1 and removed: at poster scale it could be misread.)
Not drawn because not verified or not appropriate: her death or funeral,
mourners, Cesar Chavez's likeness, readable signs or slogans, a large crowd.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import HAIR, SKIN, Look, Pose, figure  # noqa: E402

DATE = "2026-10-28"
R = rng(20261028)
SKY = ["#f08a3c", "#f39b45", "#f5ae52", "#f7c263", "#f9d47a"]
SUN, SUN2 = "#fde6a4", "#ffd06a"
HILL, HILL2 = "#c0603a", "#9c4a34"
VINE, VINE2, VINE3, NIGHT = "#2f5a3a", "#24472f", "#1a3524", "#10241a"
DIRT, DIRT2 = "#d98a4a", "#b86d3a"
UFW_RED, INK, CREAM = "#c81e2b", "#141010", "#fbf3e2"
HORIZON, VX = 470, 600
ROAD_Y = 720


def sky():
    out = []
    band = HORIZON / len(SKY)
    for i, col in enumerate(SKY):
        out.append(rect(0, i * band, WIDTH, band + 1, fill=col))
    return out


def sun():
    cx, cy, r = VX, HORIZON, 330
    rays = []
    for k in range(14):
        a0 = math.radians(-180 + k * 180 / 14 + 2)
        a1 = a0 + math.radians(180 / 14 * 0.5)
        L = 1100
        rays.append(poly([(cx, cy), (cx + L * math.cos(a0), cy + L * math.sin(a0)),
                          (cx + L * math.cos(a1), cy + L * math.sin(a1))], fill="#ffe2a0", opacity=0.16))
    return rays + [circle(cx, cy, r + 60, fill=SUN2, opacity=0.35),
            circle(cx, cy, r, fill=SUN),
            circle(cx, cy, r, fill="url(#dots)", opacity=0.35),
            circle(cx, cy, r * 0.62, fill="#fff3cc", opacity=0.6)]


def hills():
    return [path(f"M0 {HORIZON - 30} Q160 {HORIZON - 70} 330 {HORIZON - 34} T700 {HORIZON - 24} "
                 f"T1200 {HORIZON - 52} L1200 {HORIZON} L0 {HORIZON} Z", fill=HILL, opacity=0.75),
            path(f"M0 {HORIZON - 8} Q300 {HORIZON - 26} 600 {HORIZON - 10} T1200 {HORIZON - 14} "
                 f"L1200 {HORIZON} L0 {HORIZON} Z", fill=HILL2)]


def vineyard():
    """Vine rows in one-point perspective, converging on the sun at the horizon."""
    out = [rect(0, HORIZON, WIDTH, ROAD_Y - 60 - HORIZON, fill=DIRT2)]
    n = 22
    for i in range(n + 1):
        xb = -900 + i * (3000 / n)
        xb2 = xb + 3000 / n * 0.55
        out.append(poly([(VX - 3, HORIZON), (VX + 3, HORIZON), (xb2, ROAD_Y - 40), (xb, ROAD_Y - 40)],
                        fill=VINE if i % 2 else VINE2))
    # trellis posts along each row near the road
    for i in range(n + 1):
        xb = -900 + i * (3000 / n) + 3000 / n * 0.27
        for t in (0.55, 0.75, 0.95):
            x = VX + (xb - VX) * t
            y = HORIZON + (ROAD_Y - 40 - HORIZON) * t
            out.append(rect(x - 2 * t, y - 30 * t, 4 * t, 30 * t, fill=NIGHT, opacity=0.7))
    out.append(rect(0, HORIZON, WIDTH, 40, fill=SUN2, opacity=0.18))  # haze at the horizon
    return out


def road():
    return [rect(0, ROAD_Y - 60, WIDTH, 200, fill=DIRT),
            rect(0, ROAD_Y - 60, WIDTH, 8, fill=SUN, opacity=0.5),          # rim of light along the road edge
            rect(0, ROAD_Y + 140, WIDTH, 60, fill=DIRT2)]


MARCHERS = [  # (x, height, skin, hair, style, top, bottom)
    (745, 300, 3, 0, "cap", "#3d5f7a", "#2a2a33"),
    (840, 290, 4, 1, "long", "#7a3f5a", "#33252a"),
    (925, 282, 2, 0, "short", "#5a6a3a", "#2b2b30"),
    (1010, 274, 5, 0, "cap", "#8a5a2a", "#2a2a33"),
    (1090, 266, 3, 5, "short", "#4a4f7a", "#2b2b30"),
    (1165, 258, 1, 1, "bun", "#6a3a2a", "#33252a"),
]


def shadow(x, y, h):
    """Long cast shadow falling toward the viewer (sun is behind the marchers)."""
    return poly([(x - 20, y), (x + 18, y), (x + 95, y + h * 0.62), (x + 30, y + h * 0.66)], fill="#8f4f2c", opacity=0.55)


def picket_line():
    out = []
    steps = [((-25, 15), (25, 20), (-20, -15), (22, -4)), ((20, 20), (-20, 15), (18, -6), (-18, -14))]
    for i, (x, h, s, hr, style, top, bottom) in enumerate(MARCHERS):
        out.append(shadow(x, ROAD_Y, h))
    for i, (x, h, s, hr, style, top, bottom) in reversed(list(enumerate(MARCHERS))):
        ba, fa, bl, fl = steps[i % 2]
        items = None
        pose = Pose(back_arm=ba, front_arm=fa, back_leg=bl, front_leg=fl, lean=4)
        out.append(group([figure(x + 3, ROAD_Y - 3, h, -1, pose, Look(skin=SUN, top=SUN, top_shade=SUN, bottom=SUN,
                                                                      shoes=SUN, hair=SUN, hair_style=style))],
                         filter="url(#rim)", opacity=0.8))
        out.append(figure(x, ROAD_Y, h, -1, pose,
                          Look(skin=SKIN[s], top=top, bottom=bottom, hair=HAIR[hr], hair_style=style)))
    return out


def huerta():
    x, h = 560, 400
    pose = Pose(back_arm=(-30, 20), front_arm=(165, -15), back_leg=(-24, -14), front_leg=(26, -4), lean=3)
    look = Look(skin=SKIN[2], top=UFW_RED, top_shade="#9a1520", bottom="#2a1f2a", hair=HAIR[0], hair_style="long",
                face="shout", build=0.92, skirt=True)
    glow = Look(skin="#fff6d8", top="#fff6d8", top_shade="#fff6d8", bottom="#fff6d8", shoes="#fff6d8",
                hair="#fff6d8", hair_style="long", skirt=True, build=0.92)
    return [shadow(x, ROAD_Y + 8, h),
            group([figure(x + 4, ROAD_Y + 4, h, -1, pose, glow)], filter="url(#rim)"),
            figure(x, ROAD_Y + 8, h, -1, pose, look)]


def foreground():
    """Dark vine leaves and grape clusters framing the bottom corners."""
    out = []
    def leaf(x, y, s, rot, col):
        return path("M0 0 Q-34 -6 -36 -30 Q-22 -30 -24 -44 Q-8 -40 0 -62 Q8 -40 24 -44 Q22 -30 36 -30 "
                    "Q34 -6 0 0 Z", fill=col,
                    transform=f"translate({x} {y}) rotate({rot}) scale({s})")
    def grapes(x, y, s):
        dots = []
        for row in range(5):
            for k in range(5 - row):
                dots.append(circle(x + (k - (4 - row) / 2) * 13 * s, y + row * 11 * s, 7.5 * s, fill="#3a1f3c"))
        return dots
    # a vine branch hanging into the top-left corner, with a heavy grape cluster
    out.append(path("M-10 40 Q120 70 190 30 Q240 0 300 -10", fill="none", stroke=NIGHT, stroke_width=14))
    out.append(path("M150 52 Q160 90 150 120", fill="none", stroke=NIGHT, stroke_width=6))
    for x, y, s_, rot in [(40, 60, 1.7, 160), (110, 40, 1.4, 200), (230, 30, 1.5, 170), (300, 0, 1.2, 210)]:
        out.append(leaf(x, y, s_, rot, VINE3))
    big = []
    for row in range(7):
        for k in range(6 - row // 2):
            big.append(circle(150 + (k - (5 - row // 2) / 2) * 17 + (row % 2) * 6, 130 + row * 15, 10,
                              fill="#4a2448" if (row + k) % 3 else "#5e2f5a"))
    out += big
    out.append(path("M0 900 L0 790 Q120 760 260 800 Q330 830 360 900 Z", fill=NIGHT))
    out.append(path("M1200 900 L1200 800 Q1080 770 960 820 Q900 850 880 900 Z", fill=NIGHT))
    for x, y, s, rot in [(60, 820, 1.6, -20), (170, 815, 1.3, 15), (270, 850, 1.1, 30), (20, 880, 1.4, -50)]:
        out.append(leaf(x, y, s, rot, VINE3))
    for x, y, s, rot in [(1140, 830, 1.5, 20), (1040, 830, 1.2, -15), (950, 860, 1.0, -30)]:
        out.append(leaf(x, y, s, rot, VINE3))
    out += grapes(205, 825, 1.6) + grapes(1010, 840, 1.4)
    return out


defs = [grain_filter(), halftone("dots", "#f7b84f", dot=3, spacing=10), blur("rim", 4)]
body = (sky() + sun() + hills() + vineyard() + road() + picket_line() + huerta() + foreground()
        + [grain_overlay(opacity=0.35)])

save(document(defs, body,
              "Dolores Huerta, labor and civil rights leader, dies at 96",
              "Graphic poster illustration of a 1960s farmworkers' picket line marching along a California vineyard "
              "road against a huge setting sun. A young Dolores Huerta, with long dark hair and a red top, leads the "
              "line with one arm raised in front of the sun, followed by farmworkers in work clothes and caps. Vine rows "
              "run to the horizon, grape clusters hang in the foreground, and long shadows stretch toward the viewer."),
     Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
