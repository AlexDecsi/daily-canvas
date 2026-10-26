"""Poster study 4 (breaking news / disaster): a passenger jet crash at an airport.

Shown respectfully: no victims. A generic airliner lies broken beside the
runway, its tail standing up; a black smoke column rises; airport fire trucks
arc foam onto the wreck while firefighters with a hose work in the foreground.
Fictional scenario; no airline livery or logos.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import HOSE, SKIN, Look, Pose, figure  # noqa: E402

R = rng(2009)
NIGHT, NAVY, SMOKE, SMOKE2, ORANGE, FIRE, YEL = "#141a3a", "#1f2a5c", "#2a2730", "#3d3844", "#f26b2a", "#ffc43d", "#f2d43a"
GRASS, RUNWAY, WHITE, TEAL, RED = "#21402f", "#3a3d4a", "#f4f1ea", "#2a9d8f", "#e0352b"
GROUND = 620


def sky():
    out = [rect(0, 0, WIDTH, GROUND, fill=NIGHT), rect(0, 0, WIDTH, GROUND, fill="url(#dots-navy)", opacity=0.6),
           ellipse(560, GROUND, 520, 200, fill="url(#fireglow)")]
    # airport skyline: control tower and terminal
    out += [rect(120, 390, 26, GROUND - 390, fill="#0d1129"), path("M100 392 L166 392 L156 350 L110 350 Z", fill="#0d1129"),
            rect(112, 356, 42, 14, fill="#6fd3c8", opacity=0.8), rect(0, 560, 420, 60, fill="#0d1129"),
            rect(900, 570, 300, 50, fill="#0d1129")]
    out += [rect(20 + k * 30, 576, 14, 6, fill="#ffd68a", opacity=0.6) for k in range(13)]
    return out


def smoke():
    out = []
    # column rises from the wreck and leans right with the wind
    for i in range(16):
        t = i / 15
        cx, cy = 600 + t * 380, 560 - t * 520
        r = 70 + t * 90
        col = SMOKE if i % 2 else SMOKE2
        out += cloud_puffs(R, cx, cy, r * 1.6, r, 7, r * 0.35, r * 0.6, fill=col)
    out.append(group(cloud_puffs(R, 600, 540, 260, 70, 14, 24, 48, fill=ORANGE, opacity=0.55)))
    out.append(rect(0, 0, WIDTH, GROUND, fill="url(#dots-dark)", opacity=0.35,
                    clip_path="url(#smokeclip)"))
    return [group(out)]


def ground():
    out = [rect(0, GROUND, WIDTH, HEIGHT - GROUND, fill=GRASS),
           poly([(0, 640), (1200, 600), (1200, 650), (0, 700)], fill=RUNWAY)]
    out += [poly([(x, 668 - x * 0.033), (x + 50, 666 - (x + 50) * 0.033), (x + 50, 670 - (x + 50) * 0.033),
                  (x, 672 - x * 0.033)], fill=WHITE) for x in range(20, 1200, 110)]
    out += [circle(x, 642 - x * 0.033, 3, fill="#ffd68a") for x in range(10, 1200, 45)]  # runway edge lights
    return out


def wreck():
    out = []
    # rear section with the tail fin standing up (no livery)
    out += [path("M640 600 L900 585 Q960 580 975 560 L985 600 L940 640 L650 650 Z", fill=WHITE),
            path("M900 586 L940 430 L985 430 L975 560 Z", fill=WHITE),
            path("M905 585 L942 440 L960 440 L930 586 Z", fill=TEAL),
            path("M950 560 L1020 545 L1025 556 L960 575 Z", fill="#d9d4c8")]  # horizontal stabiliser
    out += [rect(670 + k * 26, 604, 12, 10, fill="#2a3d5a", rx=3) for k in range(9)]
    out.append(path("M640 625 L980 610", stroke=TEAL, stroke_width=8))
    # broken wing lying behind
    out.append(path("M560 640 L760 600 L780 612 L600 660 Z", fill="#c9c4b8"))
    out.append(ellipse(700, 650, 34, 20, fill="#9a968c"))  # detached engine
    # front section nose-down
    out += [path("M300 640 Q300 600 340 592 L600 580 L612 640 L330 668 Q300 664 300 640 Z", fill=WHITE,
                 transform="translate(-40 14) rotate(11 450 620)"),
            path("M312 620 L340 604 L360 606 L330 626 Z", fill="#2a3d5a", transform="translate(-40 14) rotate(11 450 620)")]
    out += [rect(380 + k * 26, 598, 12, 10, fill="#2a3d5a", rx=3, transform="translate(-40 14) rotate(11 450 620)") for k in range(8)]
    out.append(path("M300 648 L612 618", stroke=TEAL, stroke_width=8, transform="translate(-40 14) rotate(11 450 620)"))
    # torn edges at the break, front and rear
    out.append(path("M600 588 L590 600 L604 610 L588 622 L602 632 L590 646 L612 650 L612 586 Z", fill="#3a3540",
                    transform="translate(-40 14) rotate(11 450 620)"))
    out.append(path("M640 600 L652 610 L638 620 L654 630 L640 642 L650 650 L630 652 L628 602 Z", fill="#3a3540"))
    # flames at the break
    for fx, fh in [(600, 120), (630, 160), (660, 100), (580, 80)]:
        out.append(path(f"M{fx - 26} 650 Q{fx - 30} {650 - fh * 0.5} {fx} {650 - fh} Q{fx + 30} {650 - fh * 0.5} {fx + 26} 650 Z",
                        fill=ORANGE))
        out.append(path(f"M{fx - 14} 650 Q{fx - 16} {650 - fh * 0.3} {fx} {650 - fh * 0.6} Q{fx + 16} {650 - fh * 0.3} {fx + 14} 650 Z",
                        fill=FIRE))
    # foam on the ground
    out += cloud_puffs(R, 560, 672, 520, 34, 40, 10, 22, fill=WHITE, opacity=0.9)
    return out


def fire_truck(x, y, facing, nozzle_to):
    """An airport crash tender with a roof turret spraying foam toward nozzle_to (absolute)."""
    out = []
    body = [rect(-150, -110, 300, 90, fill=YEL, rx=8), rect(70, -150, 80, 50, fill=YEL, rx=6),
            rect(80, -142, 60, 28, fill="#1d2a44"), rect(-150, -40, 300, 14, fill="#d4b72c"),
            rect(-140, -100, 200, 8, fill=RED)]
    body += [circle(wx, -18, 22, fill="#16161c") for wx in (-105, -30, 95)]
    body += [circle(wx, -18, 9, fill="#8a8a8a") for wx in (-105, -30, 95)]
    body += [rect(84, -160, 24, 10, fill=RED, rx=3), rect(112, -160, 24, 10, fill="#3a6fe0", rx=3)]
    out.append(group(body, transform=f"translate({x} {y}) scale({facing} 1)"))
    tx, ty = x - 20 * facing, y - 118
    out += [rect(tx - 10, ty - 10, 20, 12, fill="#555"), path(f"M{tx} {ty - 4} L{tx - 40 * facing} {ty - 26}", stroke="#555", stroke_width=8)]
    # foam arc
    sx, sy = tx - 40 * facing, ty - 26
    ex, ey = nozzle_to
    mx, my = (sx + ex) / 2, min(sy, ey) - 160
    out.append(path(f"M{sx} {sy} Q{mx} {my} {ex} {ey}", fill="none", stroke=WHITE, stroke_width=16, stroke_linecap="round", opacity=0.95))
    out.append(path(f"M{sx} {sy} Q{mx} {my} {ex} {ey}", fill="none", stroke="#cfe6f2", stroke_width=6, stroke_linecap="round"))
    out.append(circle(x + 100 * facing, y - 160, 60, fill="url(#redglow)"))
    out.append(circle(x + 128 * facing, y - 160, 60, fill="url(#blueglow)"))
    return out


def firefighters():
    out = []
    gear = dict(top="#c99a3a", top_shade="#a67c2c", bottom="#b8892f", shoes="#1d1b22", hair="#f2d43a",
                hair_style="firehat", vest=True)
    nozzle = rect(-2, -3, 26, 7, fill="#444", rx=2)
    crew = [(560, 880, 225), (440, 892, 238), (320, 904, 250)]
    for i, (x, y, h) in enumerate(crew):
        out.append(figure(x, y, h, 1, HOSE, Look(skin=SKIN[(i * 2 + 1) % 6], face="stern", **gear),
                          hand_items={"front": nozzle if i == 0 else None}))
    # the hose itself, snaking back to the left
    out.append(path("M300 845 Q400 815 470 818 Q560 820 600 798", fill="none", stroke="#8c2a1f", stroke_width=9))
    out.append(path("M605 795 Q615 740 600 680", fill="none", stroke=WHITE, stroke_width=10, opacity=0.9))  # water jet
    # an officer directing, arm pointed at the wreck
    out.append(figure(1050, 900, 245, -1, Pose(back_arm=(-10, 10), front_arm=(95, 0), back_leg=(-6, 0), front_leg=(8, 0)),
                      Look(skin=SKIN[4], face="shout", **gear)))
    return out


defs = [
    grain_filter(),
    halftone("dots-navy", "#2c3a7a", dot=1.6, spacing=7),
    halftone("dots-dark", "#000000", dot=2.4, spacing=9),
    radial("fireglow", [(0, ORANGE, 0.75), (1, ORANGE, 0)]),
    radial("redglow", [(0, "#ff3b30", 0.6), (1, "#ff3b30", 0)]),
    radial("blueglow", [(0, "#3a6fe0", 0.55), (1, "#3a6fe0", 0)]),
    el("clipPath", [rect(560, 0, 600, 600)], id="smokeclip"),
]
body = (sky() + smoke() + ground() + wreck() + fire_truck(1040, 800, -1, (720, 600)) +
        fire_truck(150, 790, 1, (420, 610)) + firefighters() + [grain_overlay(opacity=0.4), study_tag()])

save(document(defs, body,
              "Poster study: a passenger jet crash at an airport",
              "Graphic poster illustration at night: a white airliner lies broken in two beside the runway, its "
              "tail fin upright and flames at the break, a black smoke column rising into the sky; two yellow "
              "airport fire trucks spray arcs of foam onto it while firefighters in turnout gear work a hose in the "
              "foreground and an officer points toward the wreck. No victims shown. Fictional scenario for a style study."),
     Path(__file__).resolve().parents[3] / "prototypes" / "poster" / "04-crash.svg")
