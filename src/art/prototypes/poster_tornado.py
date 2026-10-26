"""Poster study 5 (extreme weather): a tornado tears across farmland.

A huge funnel drops from a dark storm cloud under a green-tinged sky, throwing
debris over a wheat field toward a farm; in the foreground a family runs for
their storm cellar while a parent holds the door. Fictional scenario.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import RUN, Look, Pose, figure  # noqa: E402

R = rng(2011)
CLOUD, CLOUD2, FUNNEL, FUNNEL2 = "#2e2638", "#43384f", "#6b6470", "#857d88"
WHEAT, WHEAT2, BARN, DIRT, CREAM = "#e5b84a", "#c9952f", "#c4382b", "#7a5a3a", "#f4ead6"
HORIZON = 600


def sky():
    out = [rect(0, 0, WIDTH, HORIZON, fill="url(#greensky)")]
    # the storm's flat, heavy cloud base with striations
    out.append(path("M0 0 L1200 0 L1200 250 Q1000 300 760 290 Q500 300 300 260 Q120 240 0 270 Z", fill=CLOUD))
    for k in range(5):
        y = 60 + k * 45
        out.append(path(f"M0 {y + 20} Q600 {y + 70 + k * 6} 1200 {y + 10}", fill="none", stroke=CLOUD2, stroke_width=10))
    out.append(path("M0 0 L1200 0 L1200 250 Q1000 300 760 290 Q500 300 300 260 Q120 240 0 270 Z",
                    fill="url(#dots-cloud)", opacity=0.5))
    # lightning
    out.append(path("M210 250 L180 330 L210 330 L170 430 L250 310 L215 310 L245 250 Z", fill="#fff6c2"))
    out.append(circle(210, 340, 70, fill="url(#flash)"))
    return out


def far_land():
    out = [rect(0, HORIZON - 20, WIDTH, 40, fill="#4f6b3a")]
    # small town on the left horizon: water tower and grain elevator
    out += [ellipse(330, 520, 30, 18, fill="#3a4a3a"), rect(312, 536, 4, 50, fill="#3a4a3a"), rect(344, 536, 4, 50, fill="#3a4a3a"),
            rect(400, 500, 26, 86, fill="#3a4a3a"), rect(428, 520, 40, 66, fill="#3a4a3a")]
    # farm on the right: barn and silo, in the funnel's path
    out += [rect(940, 520, 120, 80, fill=BARN), poly([(930, 522), (1000, 470), (1070, 522)], fill="#8c2a20"),
            rect(985, 555, 30, 45, fill="#5a1d16"), rect(1080, 470, 40, 130, fill="#b9b4a8"),
            ellipse(1100, 470, 20, 12, fill="#9a968c")]
    return out


def tornado():
    out = []
    top_x, top_y, bot_x, bot_y = 780, 285, 700, 620
    # wall cloud lowering from the storm base
    out += cloud_puffs(R, top_x + 10, top_y - 5, 340, 50, 26, 26, 50, fill=CLOUD2)
    # funnel: a ragged, skewed cone of overlapping blurred swirls, darker on one side
    swirls = []
    for i in range(70):
        t = i / 69
        cx = top_x + (bot_x - top_x) * t + math.sin(t * 6.5) * 26 + R.uniform(-10, 10)
        cy = top_y + (bot_y - top_y) * t + R.uniform(-6, 6)
        rx = (140 * (1 - t) ** 1.6 + 16) * R.uniform(0.8, 1.15)
        swirls.append(ellipse(round(cx, 1), round(cy, 1), round(rx, 1), round(rx * 0.22 + 6, 1),
                              fill=R.choice([FUNNEL, FUNNEL2, "#5a5360"]), opacity=0.9,
                              transform=f"rotate({R.uniform(-8, 8):.0f} {cx:.0f} {cy:.0f})"))
    out.append(group(swirls, filter="url(#soften)"))
    for i in range(18):  # sharper streaks on top for a sense of spin
        t = i / 17
        cx = top_x + (bot_x - top_x) * t + math.sin(t * 6.5) * 26
        cy = top_y + (bot_y - top_y) * t
        rx = 140 * (1 - t) ** 1.6 + 16
        out.append(path(f"M{cx - rx * 0.8:.0f} {cy - 2:.0f} Q{cx:.0f} {cy + 9:.0f} {cx + rx * 0.6:.0f} {cy - 6:.0f}",
                        fill="none", stroke="#b0a8b2", stroke_width=2.5, opacity=0.7))
    # debris cloud at the base
    out += cloud_puffs(R, bot_x, bot_y - 10, 260, 70, 30, 18, 40, fill=DIRT, opacity=0.9)
    out += cloud_puffs(R, bot_x, bot_y - 30, 200, 60, 20, 12, 28, fill="#9c7a55", opacity=0.85)
    # flying debris orbiting the funnel: planks, shingles, a sheet of metal roofing
    for _ in range(26):
        a = R.uniform(0, 2 * math.pi)
        r = R.uniform(90, 260)
        x = bot_x + 40 + math.cos(a) * r
        y = bot_y - 120 - math.sin(a) * r * 0.55 - R.uniform(0, 120)
        kind = R.random()
        rot = R.uniform(0, 180)
        if kind < 0.5:
            out.append(rect(round(x, 1), round(y, 1), 26, 5, fill="#8a6440", transform=f"rotate({rot:.0f} {x:.0f} {y:.0f})"))
        elif kind < 0.8:
            out.append(rect(round(x, 1), round(y, 1), 10, 8, fill="#3b3540", transform=f"rotate({rot:.0f} {x:.0f} {y:.0f})"))
        else:
            out.append(rect(round(x, 1), round(y, 1), 30, 16, fill="#b9b4a8", transform=f"rotate({rot:.0f} {x:.0f} {y:.0f})"))
    return out


def field():
    out = [rect(0, HORIZON, WIDTH, HEIGHT - HORIZON, fill=WHEAT)]
    for k in range(-10, 22):  # crop rows converging on the horizon
        out.append(path(f"M{600 + k * 18} {HORIZON} L{600 + k * 120} {HEIGHT}", stroke=WHEAT2, stroke_width=4))
    out.append(rect(0, HORIZON, WIDTH, HEIGHT - HORIZON, fill="url(#dots-wheat)", opacity=0.5))
    # wind-bent wheat tufts in the foreground
    for _ in range(60):
        x, y = R.uniform(0, WIDTH), R.uniform(760, 900)
        out.append(path(f"M{x:.0f} {y:.0f} q12 -18 34 -26", fill="none", stroke="#a87a22", stroke_width=3))
    # wind streaks
    for _ in range(30):
        x, y = R.uniform(-100, WIDTH), R.uniform(320, 760)
        out.append(path(f"M{x:.0f} {y:.0f} l{R.uniform(60, 140):.0f} {R.uniform(-8, -2):.0f}", stroke=CREAM,
                        stroke_width=2, opacity=0.5))
    return out


def cellar_and_family():
    out = []
    # storm cellar: a concrete box in the ground, one door flung open
    out += [poly([(150, 800), (330, 800), (350, 830), (130, 830)], fill="#8f8a80"),
            poly([(165, 800), (315, 800), (325, 815), (155, 815)], fill="#1a1612"),
            poly([(240, 800), (320, 800), (292, 700), (230, 712)], fill="#7a5a3a")]  # door swung up
    out += [path(f"M{238 + k * 4} {796 - k * 22} L{316 - k * 6} {796 - k * 22}", stroke="#5c4229", stroke_width=3) for k in range(4)]
    # parent holding the door, shouting to hurry
    out.append(figure(345, 845, 250, 1, Pose(back_arm=(-10, 20), front_arm=(150, -60), back_leg=(-12, 0), front_leg=(16, -10), lean=-4),
                      Look(skin="#c98e6b", top="#2f5d8a", bottom="#3b3d4a", hair_style="short", hair="#3b2a20", face="shout")))
    # second parent running, holding the child's hand; child running ahead
    out.append(figure(620, 880, 255, -1, RUN, Look(skin="#7d4f35", top="#3b7d5c", bottom="#2a2a3a", hair_style="long",
                                                    hair="#1e1512", face="frown")))
    out.append(figure(500, 875, 160, -1, Pose(back_arm=(-60, 60), front_arm=(60, -70), back_leg=(-40, -55), front_leg=(42, -15), lean=12),
                      Look(skin="#7d4f35", top="#f2c230", bottom="#33405a", hair_style="short", hair="#1e1512", face="frown")))
    return out


defs = [
    grain_filter(),
    linear("greensky", [(0, "#4a4a52"), (0.55, "#7f9a64"), (1, "#c9d48a")]),
    radial("flash", [(0, "#fff6c2", 0.7), (1, "#fff6c2", 0)]),
    blur("soften", 3),
    halftone("dots-cloud", "#120e18", dot=2.2, spacing=8),
    halftone("dots-wheat", "#b07e1f", dot=1.8, spacing=8, angle=15),
]
body = sky() + far_land() + field() + tornado() + cellar_and_family() + [grain_overlay(opacity=0.4), study_tag()]

save(document(defs, body,
              "Poster study: a tornado tears across farmland",
              "Graphic poster illustration: under a green-tinged sky and a dark storm cloud lit by lightning, a huge "
              "grey tornado funnel throws dirt and debris over a golden wheat field toward a red barn and silo; in the "
              "foreground a parent holds open a storm cellar door and shouts as the other parent and a child run "
              "toward it. Fictional scenario for a style study."),
     Path(__file__).resolve().parents[3] / "prototypes" / "poster" / "05-tornado.svg")
