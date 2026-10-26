"""Poster study 3 (environment): neighbours prepare as a hurricane approaches.

A coastal street under a sky filled by a bold graphic hurricane spiral: one
neighbour on a ladder holds plywood over a window, another carries a box to a
packed car, a child in a yellow raincoat holds a dog's leash and looks up;
palms bend in the wind and rain streaks across. Fictional scenario.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import CARRY, Look, Pose, figure  # noqa: E402

R = rng(2017)
SKY, STORM, INK, SLATE = "#7fa3a6", "#24525a", "#13262b", "#4b6f75"
YELLOW, CORAL, MINT, CREAM, PLY = "#f2c230", "#e98a6b", "#9fd1bf", "#f4ead6", "#d8a866"
STREET = 730


def sky():
    out = [rect(0, 0, WIDTH, STREET, fill=SKY)]
    # hurricane: a thick spiral band, counter-clockwise inflow, with a pale eye
    cx, cy = 760, 210
    for width, col, turns, a0 in [(46, STORM, 2.4, 0.0), (30, SLATE, 2.2, math.pi)]:
        pts = []
        for i in range(260):
            t = i / 259
            theta = a0 + t * turns * 2 * math.pi
            r = 28 + t * 330
            pts.append((cx + r * math.cos(theta), cy + r * math.sin(theta) * 0.62))
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        out.append(path(d, fill="none", stroke=col, stroke_width=width, stroke_linecap="round", stroke_linejoin="round"))
    out += [ellipse(cx, cy, 30, 20, fill=CREAM), ellipse(cx, cy, 30, 20, fill="none", stroke=INK, stroke_width=6)]
    # low flat cloud lobes along the horizon
    for x in range(-40, WIDTH + 80, 110):
        out.append(ellipse(x, 470 + R.uniform(-12, 12), 90, 44, fill=SLATE))
    out.append(rect(0, 470, WIDTH, 60, fill=SLATE))
    return out


def palm(x, base, h, lean):
    tip = (x + lean, base - h)
    out = [path(f"M{x - 9} {base} Q{x + lean * 0.2} {base - h * 0.6} {tip[0] - 4} {tip[1]} L{tip[0] + 4} {tip[1]} "
                f"Q{x + lean * 0.2 + 12} {base - h * 0.6} {x + 9} {base} Z", fill="#6b4f3a")]
    for k in range(7):  # fronds streaming downwind (to the right)
        a = math.radians(-50 + k * 22)
        length = 110 + R.uniform(-15, 15)
        ex, ey = tip[0] + math.cos(a) * length + 40, tip[1] + math.sin(a) * length * 0.7 + 20
        out.append(path(f"M{tip[0]:.0f} {tip[1]:.0f} Q{(tip[0] + ex) / 2 + 10:.0f} {min(tip[1], ey) - 30:.0f} {ex:.0f} {ey:.0f} "
                        f"Q{(tip[0] + ex) / 2:.0f} {min(tip[1], ey) - 5:.0f} {tip[0]:.0f} {tip[1] + 6:.0f} Z", fill="#2f6b4f"))
    return out


def house(x0, x1, top, color, roof):
    out = [rect(x0, top, x1 - x0, STREET - top, fill=color),
           poly([(x0 - 20, top + 4), ((x0 + x1) / 2, top - 110), (x1 + 20, top + 4)], fill=roof)]
    return out


def street_scene():
    out = []
    out += palm(990, STREET, 380, 90)
    out += house(40, 470, 430, CORAL, INK)
    out += house(820, 1180, 470, MINT, STORM)
    # windows: left one already boarded, right one being boarded
    out += [rect(90, 500, 120, 110, fill=PLY), path("M90 500 L210 610 M210 500 L90 610", stroke="#b98a4c", stroke_width=5)]
    out += [rect(300, 500, 120, 110, fill="#1d3a40"), rect(306, 506, 108, 98, fill="#2d5a63")]
    out += [rect(880, 540, 100, 90, fill=PLY), rect(1040, 540, 100, 90, fill="#1d3a40")]
    out += [rect(230, 600, 50, 130, fill=INK)]  # door
    out += palm(140, STREET, 300, 70)
    # pavement and road
    out += [rect(0, STREET, WIDTH, 40, fill=CREAM), rect(0, STREET + 40, WIDTH, HEIGHT - STREET - 40, fill=INK)]
    out += [rect(x, 840, 70, 8, fill=YELLOW) for x in range(30, WIDTH, 140)]
    return out


def ladder_and_worker():
    out = []
    # ladder leaning on the wall beside the window
    out += [path("M440 735 L400 470", stroke="#c7c1b3", stroke_width=8),
            path("M490 735 L452 470", stroke="#c7c1b3", stroke_width=8)]
    out += [path(f"M{440 - k * 4.6:.0f} {735 - k * 30} L{490 - k * 4.4:.0f} {735 - k * 30}", stroke="#c7c1b3", stroke_width=6)
            for k in range(1, 9)]
    # the plywood sheet being held over the window, slightly tilted
    out.append(rect(292, 490, 136, 128, fill=PLY, transform="rotate(-4 360 554)"))
    out.append(figure(458, 676, 230, -1, Pose(back_arm=(100, 20), front_arm=(118, 8), back_leg=(-2, 0), front_leg=(28, -40), lean=-6),
                      Look(skin="#7d4f35", top="#c9452c", bottom="#33405a", hair_style="cap", hair="#1d2a44")))
    return out


def car_and_carrier():
    out = []
    cx, cy = 560, 780
    out += [path(f"M{cx} {cy} L{cx} {cy - 60} Q{cx + 10} {cy - 110} {cx + 70} {cy - 115} L{cx + 210} {cy - 115} "
                 f"Q{cx + 250} {cy - 110} {cx + 260} {cy - 60} L{cx + 280} {cy - 50} L{cx + 280} {cy} Z", fill=CREAM),
            rect(cx + 80, cy - 105, 70, 40, fill="#2d5a63"), rect(cx + 160, cy - 105, 60, 40, fill="#2d5a63"),
            circle(cx + 60, cy, 30, fill=INK), circle(cx + 220, cy, 30, fill=INK),
            circle(cx + 60, cy, 12, fill="#8a8a8a"), circle(cx + 220, cy, 12, fill="#8a8a8a")]
    # luggage strapped on the roof
    out += [rect(cx + 70, cy - 150, 90, 35, fill=YELLOW, rx=4), rect(cx + 165, cy - 142, 60, 27, fill=CORAL, rx=4),
            path(f"M{cx + 65} {cy - 132} L{cx + 230} {cy - 132}", stroke=INK, stroke_width=3)]
    # open hatch at the back (left), boxes inside
    out += [path(f"M{cx} {cy - 60} L{cx - 40} {cy - 130} L{cx - 30} {cy - 136} L{cx + 8} {cy - 68} Z", fill="#e3d8c0"),
            rect(cx + 8, cy - 70, 40, 34, fill=PLY)]
    box = rect(-16, -14, 32, 26, fill=PLY, stroke="#b98a4c", stroke_width=2)
    out.append(figure(500, 900, 250, 1, CARRY, Look(skin="#e0a982", top="#3b7d5c", bottom="#2a2a3a", hair_style="long",
                                                   hair="#6b4a2e"), hand_items={"front": box}))
    return out


def child_and_dog():
    out = []
    dog = [ellipse(0, -14, 20, 10, fill="#8b5a3c"), circle(-18, -24, 9, fill="#8b5a3c"),
           path("M-24 -30 L-20 -40 L-14 -30 Z", fill="#6a412a"), path("M18 -16 L30 -28", stroke="#8b5a3c", stroke_width=5),
           path("M-12 -6 L-12 4 M10 -6 L10 4", stroke="#8b5a3c", stroke_width=5)]
    out.append(group(dog, transform="translate(985 905) scale(1.7)"))
    out.append(figure(1085, 905, 215, -1, Pose(back_arm=(-10, 10), front_arm=(45, 20), head_tilt=-22),
                      Look(skin="#a86f4c", top=YELLOW, bottom="#33405a", hair_style="hood", hair=YELLOW, shoes=YELLOW)))
    out.append(path("M1062 800 Q1020 860 955 862", fill="none", stroke=INK, stroke_width=2.5))  # leash
    return out


def rain():
    out = []
    for _ in range(170):
        x, y = R.uniform(-60, WIDTH), R.uniform(0, HEIGHT)
        out.append(path(f"M{x:.0f} {y:.0f} l28 -50", stroke="#e8f1f2", stroke_width=2, opacity=0.55))
    return [group(out)]


defs = [grain_filter()]
body = sky() + street_scene() + ladder_and_worker() + car_and_carrier() + child_and_dog() + rain() + \
    [grain_overlay(opacity=0.4), study_tag()]

save(document(defs, body,
              "Poster study: neighbours prepare for the hurricane",
              "Graphic poster illustration: a hurricane's spiral fills a teal sky over a coastal street; one neighbour "
              "on a ladder holds a sheet of plywood over a window, another carries a box to a car loaded with luggage, "
              "and a child in a yellow raincoat holding a dog on a leash looks up at the storm as palms bend and rain "
              "streaks across. Fictional scenario for a style study."),
     Path(__file__).resolve().parents[3] / "prototypes" / "poster" / "03-storm.svg")
