"""Poster study 2 (science): astronauts walk out to their rocket.

Three suited astronauts stride along a causeway, one waving, carrying portable
suit-cooling cases; family and ground crew cheer behind a barrier, phones up;
the rocket and its tower stand against a giant setting sun in banded poster sky.
Fictional scenario, generic rocket with no national markings.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import CHEER, HAIR, SKIN, WALK, Look, Pose, figure  # noqa: E402

R = rng(1961)
COBALT, DEEP, ORANGE, SUN, CREAM, INK = "#1f3c88", "#13224d", "#e8622c", "#ffd36b", "#f6ecd8", "#121626"
GROUND = 800


def sky():
    bands = ["#13224d", "#1f3c88", "#4b4fa0", "#a6519a", "#e8622c", "#f39a4a"]
    out = []
    for i, col in enumerate(bands):  # stepped poster sky, no smooth gradients
        out.append(rect(0, i * 110, WIDTH, 120, fill=col))
    out.append(circle(930, 600, 230, fill=SUN))
    out.append(circle(930, 600, 230, fill="none", stroke="#ffe7a6", stroke_width=10))
    out.append(rect(0, 640, WIDTH, 160, fill="#2b2f5e"))  # far marsh
    out += [rect(0, 640 + k * 14, WIDTH, 3, fill="#3b3f74") for k in range(1, 11)]
    return out


def rocket_and_tower():
    x, w, top = 900, 92, 40
    out = [
        rect(x, top + 120, w, GROUND - top - 120, fill=CREAM),
        rect(x + w * 0.62, top + 120, w * 0.38, GROUND - top - 120, fill="#ddd1b8"),  # shading side
        path(f"M{x} {top + 120} L{x + w / 2} {top} L{x + w} {top + 120} Z", fill=CREAM),
        path(f"M{x + w * 0.5} {top} L{x + w} {top + 120} L{x + w * 0.62} {top + 120} Z", fill="#ddd1b8"),
        rect(x, top + 260, w, 16, fill=INK), rect(x, top + 520, w, 12, fill=INK),
        rect(x, top + 330, w, 6, fill=ORANGE),
    ]
    tx = x + w + 30
    out += [rect(tx, 120, 70, GROUND - 120, fill="none", stroke=ORANGE, stroke_width=6)]
    for y in range(120, GROUND, 40):
        out.append(path(f"M{tx} {y} L{tx + 70} {y + 40} M{tx + 70} {y} L{tx} {y + 40}", stroke=ORANGE, stroke_width=3))
        out.append(rect(tx, y, 70, 4, fill=ORANGE))
    out += [rect(x + w, 250, 30, 10, fill=ORANGE),  # crew access arm reaching the capsule
            rect(tx + 30, 60, 6, 60, fill=ORANGE), circle(tx + 33, 58, 6, fill="#ff4b3e")]
    return out


def causeway():
    out = [rect(0, GROUND, WIDTH, HEIGHT - GROUND, fill=INK),
           rect(0, GROUND, WIDTH, 8, fill=COBALT)]
    for k in range(-6, 14):  # perspective lines on the walkway
        out.append(path(f"M{600 + k * 40} {GROUND + 8} L{600 + k * 140} {HEIGHT}", stroke="#24305a", stroke_width=3))
    return out


def crowd():
    """Family and ground crew behind a barrier on the left: smaller, cheering, phones up."""
    out = []
    xs = [30, 72, 112, 155, 195, 238, 278]
    for i, x in enumerate(xs):
        look = Look(skin=R.choice(SKIN), hair=R.choice(HAIR), top=R.choice([ORANGE, "#e3a92f", "#3b7d5c", CREAM, "#a6519a"]),
                    bottom="#2a2a3a", hair_style=R.choice(["short", "long", "bun", "cap"]))
        if i % 3 == 0:
            pose = CHEER
        elif i % 3 == 1:
            pose = Pose(back_arm=(-10, 10), front_arm=(140, -60))  # holding a phone up
        else:
            pose = Pose(back_arm=(100, -20), front_arm=(120, -30))
        phone = rect(-3, -9, 7, 11, fill="#bfe3ff", rx=1.5) if i % 3 == 1 else None
        out.append(figure(x, GROUND - 4, 185 + R.uniform(-12, 12), 1, pose, look, hand_items={"front": phone}))
    # barrier in front of them
    out += [rect(0, GROUND - 84, 320, 12, fill=CREAM), rect(0, GROUND - 54, 320, 10, fill=CREAM)]
    out += [rect(x, GROUND - 84, 8, 84, fill=CREAM) for x in (10, 110, 210, 306)]
    return out


def astronauts():
    out = []
    case = rect(-7, -1, 14, 10, fill="#9aa3b5", rx=2)
    suit = dict(skin="#f4f1ea", top="#f4f1ea", top_shade="#d8d2c4", bottom="#ebe5d8", shoes="#2a2a33",
                hair_style="helmet")
    patch = [rect(-6, -70, 7, 6, fill=COBALT), rect(-8, -50, 16, 4, fill=COBALT)]  # shoulder patch and belt stripe
    walkers = [
        (580, 340, WALK),
        (760, 350, Pose(back_arm=(-20, 15), front_arm=(165, -25), back_leg=(-18, -14), front_leg=(20, -4))),  # waving
        (410, 330, Pose(back_arm=(-28, 15), front_arm=(28, 20), back_leg=(-22, -16), front_leg=(18, -4))),
    ]
    for x, h, pose in sorted(walkers, key=lambda w: w[0]):
        out.append(figure(x, GROUND + 70, h, 1, pose, Look(**suit, extra=patch), hand_items={"back": case}))
    return out


defs = [grain_filter()]
body = sky() + rocket_and_tower() + causeway() + crowd() + astronauts() + [grain_overlay(opacity=0.4), study_tag()]

save(document(defs, body,
              "Poster study: astronauts walk out to the rocket",
              "Graphic poster illustration: three astronauts in white suits and helmets stride along a causeway "
              "toward a tall rocket and its orange launch tower, one waving, each carrying a small suit-cooling case; "
              "family and crew behind a barrier cheer and hold up phones; a huge setting sun glows in a banded "
              "orange and violet sky. Fictional scenario for a style study."),
     Path(__file__).resolve().parents[3] / "prototypes" / "poster" / "02-walkout.svg")
