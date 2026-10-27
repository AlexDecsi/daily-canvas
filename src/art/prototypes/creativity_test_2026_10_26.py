"""Creativity-bar TEST (not published): 2026-10-26, James Comey charged a third time.

Visual idea: a low angle makes the very tall Comey loom as he records his video
statement under a ring light; behind him rise three towering stacks of case
files (one per prosecution attempt), the third with its red seal broken and its
papers, plus a folded newspaper for the 2016 story, swirling up into the night.
The camera's own screen in the foreground shows him small: a frame within a frame.

Facts from the brief only: charged over a 2016 NYT story; papers unsealed Monday;
third attempt in about a year; video statement saying he is innocent.
Not drawn because not verified: a courtroom, an arrest, handcuffs, Trump, any readable text.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

R = rng(1026)
INDIGO, INDIGO2, PLUM, AMBER, AMBER2 = "#1c1b3f", "#2a2860", "#4a2a5e", "#ffb347", "#ffd98a"
PAPER, PAPER2, SEAL, INK, STEEL = "#f6efe0", "#e3d7bd", "#d1302f", "#121219", "#3a3d4c"


def sky():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#night)"),
           rect(0, 0, WIDTH, HEIGHT, fill="url(#dots)", opacity=0.45)]
    return out


def stack(x, base, w, h, lean):
    """A tower of case files narrowing upward (low-angle perspective)."""
    out, y, k = [], base, 0
    while y > base - h:
        t = (base - y) / h
        sw = w * (1 - 0.35 * t)
        cx = x + lean * t
        th = R.uniform(14, 22)
        col = PAPER if k % 3 else PAPER2
        out.append(rect(round(cx - sw / 2 + R.uniform(-6, 6), 1), round(y - th, 1), round(sw, 1), round(th - 2, 1),
                        fill=col, rx=2))
        if k % 4 == 0:  # manila folder edge
            out.append(rect(round(cx - sw / 2, 1), round(y - 4, 1), round(sw * 0.6, 1), 4, fill="#d9a95b"))
        y -= th
        k += 1
    return out, (x + lean, base - h)


def towers():
    out = []
    s1, _ = stack(170, 900, 220, 300, 10)
    s2, _ = stack(380, 900, 240, 470, 18)
    s3, top = stack(860, 900, 300, 640, -30)
    out += s1 + s2 + s3
    # broken red seal on the third stack
    sx, sy = top[0], top[1] + 40
    out += [circle(sx, sy, 34, fill=SEAL), path(f"M{sx - 8} {sy - 34} L{sx + 4} {sy - 6} L{sx - 6} {sy + 8} L{sx + 6} {sy + 34}",
                                                stroke=INDIGO, stroke_width=5, fill="none"),
            circle(sx, sy, 22, fill="none", stroke="#9e1f22", stroke_width=4)]
    return out, top


def swirl(top):
    """Unsealed papers spiralling up out of the third stack, with a folded newspaper among them."""
    out = []
    cx, cy = top[0] - 20, top[1] - 40
    for i in range(46):
        t = i / 45
        a = t * 3.2 * math.pi
        r = 25 + t * 250
        x, y = cx + r * math.cos(a) * 1.25, cy - t * 150 + r * math.sin(a) * 0.4
        rot = R.uniform(-60, 60)
        w, h = R.uniform(30, 52), R.uniform(38, 64)
        out.append(group([rect(-w / 2, -h / 2, w, h, fill=PAPER, rx=2),
                          *[rect(-w / 2 + 5, -h / 2 + 7 + j * 7, w - 12, 2, fill="#b9ae96") for j in range(int(h // 9))]],
                         transform=f"translate({x:.0f} {y:.0f}) rotate({rot:.0f})", opacity=round(0.95 - t * 0.35, 2)))
    # the newspaper: wide sheet with a masthead bar and columns (no readable text)
    out.append(group([rect(-80, -55, 160, 110, fill="#efe9da", rx=2), rect(-70, -46, 140, 12, fill="#2b2b33"),
                      *[rect(-70 + c * 48, -26, 40, 70, fill="none", stroke="#9d9584", stroke_width=2) for c in range(3)],
                      path("M0 -55 L0 55", stroke="#c9c0ab", stroke_width=2)],
                     transform=f"translate({cx - 260} {cy - 70}) rotate(-18)"))
    return out


def ring_light_and_camera():
    out = [circle(1100, 330, 120, fill="url(#glow)"),
           circle(1100, 330, 70, fill="none", stroke="#fff4d6", stroke_width=16),
           circle(1100, 330, 70, fill="none", stroke=AMBER2, stroke_width=5, opacity=0.8),
           rect(1096, 400, 8, 500, fill=STEEL)]
    # camera on a tripod, close to the viewer (foreground right)
    out += [path("M1010 900 L1040 740 L1070 900 M1040 740 L1130 900", stroke=INK, stroke_width=10, fill="none"),
            rect(950, 640, 210, 110, fill=INK, rx=14), rect(890, 662, 80, 66, fill=INK, rx=8),
            circle(890, 695, 38, fill="#26324a"), circle(890, 695, 26, fill="#3f6fa8"), circle(880, 686, 8, fill="#bcd8f5"),
            circle(1140, 662, 8, fill=SEAL)]                                            # red recording light
    # flip-out screen showing Comey small: a frame within a frame
    out += [rect(1015, 560, 150, 100, fill=STEEL, rx=6), rect(1023, 568, 134, 84, fill="#3a3363"),
            group([figure(1090, 660, 95, -1, Pose(back_arm=(-6, 10), front_arm=(25, 120)),
                          Look(skin="#e8b391", top=INK, bottom=INK, hair="#b9b9bf", hair_style="short"))],
                  clip_path="url(#screen)")]
    return out


def comey():
    pose = Pose(back_arm=(-6, 12), front_arm=(62, -38), lean=-2, head_tilt=-6)  # open, speaking gesture toward the camera
    shadow_look = Look(skin=INK, top=INK, top_shade=INK, bottom=INK, shoes=INK, hair=INK, hair_style="short")
    out = [circle(600, 360, 260, fill="url(#halo)"),                                   # warm light behind him
           group([figure(560, 1010, 780, 1, pose, shadow_look)], opacity=0.2,
                 transform="translate(-260 40) skewX(28)")]                            # shadow thrown onto the files
    out.append(figure(560, 1010, 780, 1, pose,
                      Look(skin="#e8b391", top="#23232e", top_shade="#1a1a22", bottom="#23232e", hair="#b9b9bf",
                           hair_style="short", accent="#3f5f9a", long_tie=True, face="speak", build=1.05)))
    return out


defs = [grain_filter(), halftone("dots", "#3b3880", dot=1.6, spacing=8),
        linear("night", [(0, INDIGO), (0.6, INDIGO2), (1, PLUM)]),
        radial("halo", [(0, AMBER2, 0.55), (0.6, AMBER, 0.18), (1, AMBER, 0)]),
        radial("glow", [(0, "#fff4d6", 0.85), (0.5, AMBER, 0.35), (1, AMBER, 0)]),
        el("clipPath", [rect(1023, 568, 134, 84)], id="screen")]
tw, top = towers()
body = sky() + tw + swirl(top) + comey() + ring_light_and_camera() + [grain_overlay(opacity=0.35), study_tag()]

save(document(defs, body,
              "Creativity test: Comey charged a third time",
              "Test illustration: seen from a low angle, a very tall James Comey in a dark suit records a video statement "
              "under a glowing ring light, one hand raised. Behind him rise three towering stacks of case files, the third "
              "with a broken red seal, its papers and a folded newspaper swirling up into an indigo night; in the foreground "
              "a video camera's screen shows him small."),
     Path(__file__).resolve().parents[3] / "prototypes" / "creativity-test" / "2026-10-26-v2.svg")
