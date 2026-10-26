"""Poster study 1 (politics): a leader addresses a packed assembly hall.

Graphic-poster style: limited palette, flat shapes, print grain, people as the
subject. The speaker stands at a rostrum on the left, mid-gesture; tiers of
delegates face them, some with translation headsets, some raising hands; a
giant screen behind repeats the speaker's silhouette. Fictional scenario.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import SKIN, HAIR, Look, Pose, figure  # noqa: E402

R = rng(1948)
TEAL, DEEP, GOLD, CREAM, RED, NAVY = "#17535c", "#0c3139", "#e8a93a", "#f4e9d0", "#d9472b", "#1d2a44"
SUITS = [NAVY, "#2a2a33", "#3d4a5c", "#5b2e36", "#2f4a3a", "#44365a"]


def backdrop():
    out = [rect(0, 0, WIDTH, HEIGHT, fill=GOLD)]
    # vertical wall panels
    out += [rect(x, 0, 6, 520, fill="#d6952b") for x in range(40, WIDTH, 80)]
    # a large abstract emblem: concentric arcs (not any real organisation's logo)
    for r, col in [(230, "#f0bf5a"), (190, GOLD), (150, "#f0bf5a"), (110, GOLD)]:
        out.append(circle(820, 230, r, fill=col))
    # giant screen with the speaker's silhouette
    out += [rect(330, 70, 300, 200, fill=DEEP, rx=6),
            rect(338, 78, 284, 184, fill=TEAL)]
    out.append(figure(470, 400, 330, 1, Pose(back_arm=(30, 60), front_arm=(75, -35), lean=3),
                      Look(skin=DEEP, top=DEEP, bottom=DEEP, shoes=DEEP, hair=DEEP)))
    out.append(rect(330, 262, 300, 260, fill=GOLD))  # wall below the screen hides the silhouette's legs
    out += [rect(x, 262, 6, 258, fill="#d6952b") for x in range(360, 640, 80)]
    out.append(path("M-40 0 L260 0 L420 900 L-40 900 Z", fill="url(#spot)"))  # spotlight on the rostrum
    return out


def delegate(x, y, s, facing=-1):
    """A seated delegate seen above a desk: shoulders, head, maybe headset or raised hand."""
    skin, hair, suit = R.choice(SKIN), R.choice(HAIR), R.choice(SUITS)
    out = []
    if R.random() < 0.12:  # raised hand asking to speak
        out.append(path(f"M{x + 6 * s * facing} {y - 10 * s} L{x + 9 * s * facing} {y - 44 * s}",
                        stroke=suit, stroke_width=6 * s, stroke_linecap="round", fill="none"))
        out.append(circle(x + 9 * s * facing, y - 46 * s, 3.4 * s, fill=skin))
    out.append(path(f"M{x - 13 * s} {y + 4 * s} Q{x - 13 * s} {y - 14 * s} {x} {y - 14 * s} "
                    f"Q{x + 13 * s} {y - 14 * s} {x + 13 * s} {y + 4 * s} Z", fill=suit))
    out.append(rect(x - 2 * s, y - 20 * s, 4 * s, 7 * s, fill=skin))
    out.append(ellipse(x, y - 25 * s, 7 * s, 8 * s, fill=skin))
    out.append(path(f"M{x - 7.5 * s} {y - 24 * s} Q{x - 8 * s} {y - 34 * s} {x} {y - 33.5 * s} "
                    f"Q{x + 8 * s} {y - 34 * s} {x + 7.5 * s} {y - 26 * s} Q{x} {y - 30 * s} {x - 7.5 * s} {y - 24 * s} Z",
                    fill=hair))
    out.append(path(f"M{x + 6.5 * s * facing} {y - 26 * s} L{x + 9.5 * s * facing} {y - 22.5 * s} "
                    f"L{x + 6.5 * s * facing} {y - 22 * s} Z", fill=skin))
    if R.random() < 0.4:  # interpretation headset
        out.append(path(f"M{x - 8 * s} {y - 25 * s} Q{x} {y - 39 * s} {x + 8 * s} {y - 25 * s}",
                        fill="none", stroke="#111", stroke_width=1.6 * s))
        out.append(circle(x - 7.5 * s * facing, y - 24 * s, 2.6 * s, fill="#111"))
    return out


def hall():
    out = []
    cx, cy = 900, 330  # centre of the curved tiers (off to the right, behind the viewer's eye line)
    rows = [(470, 0.95, 26), (545, 1.15, 22), (630, 1.4, 18), (725, 1.7, 15), (830, 2.05, 12)]
    for i, (y, s, n) in enumerate(rows):
        span = 720 + i * 140
        desk = []
        people = []
        for k in range(n):
            t = k / (n - 1)
            x = cx - span / 2 + t * span + R.uniform(-4, 4)
            if x < 330 + i * 10:  # keep the rostrum area clear
                continue
            dy = (t - 0.5) ** 2 * 60  # tiers curve upward at the ends
            people += delegate(x, y - dy, s)
            desk.append(rect(x - 16 * s, y - dy + 2 * s, 32 * s, 3 * s, fill=R.choice([CREAM, RED, "#8fb8b0"])))  # blank nameplates
        out += people
        # desk band follows the curve
        pts = [(cx - span / 2 - 40 + t * (span + 80), y + 4 * s - (t - 0.5) ** 2 * 60) for t in [j / 20 for j in range(21)]]
        top = " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
        bottom = " L".join(f"{px:.1f} {py + 22 * s:.1f}" for px, py in reversed(pts))
        out.append(path(f"M{top} L{bottom} Z", fill=TEAL if i % 2 else DEEP))
        out += desk
    return out


def rostrum():
    out = []
    out.append(figure(235, 900, 560, 1, Pose(back_arm=(25, 70), front_arm=(78, -38), lean=4, head_tilt=-4),
                      Look(skin="#a86f4c", top=NAVY, bottom=NAVY, hair="#1e1512", hair_style="short", accent=RED)))
    out += [path("M70 640 L380 640 L360 900 L90 900 Z", fill=DEEP),
            rect(60, 626, 330, 20, fill=TEAL),
            rect(150, 700, 150, 120, fill="none", stroke=GOLD, stroke_width=4),  # emblem plaque, blank
            circle(225, 760, 34, fill=GOLD)]
    for mx, a in [(330, -30), (345, -18)]:  # microphones
        out.append(path(f"M330 628 Q{mx + 10} 600 {mx + 26} {585 + a / 3}", fill="none", stroke="#111", stroke_width=3))
        out.append(ellipse(mx + 28, 583 + a / 3, 7, 5, fill="#111"))
    return out


defs = [grain_filter(), linear("spot", [(0, "#fff4d6", 0.0), (0.45, "#fff4d6", 0.45), (1, "#fff4d6", 0.2)])]
body = backdrop() + hall() + rostrum() + [grain_overlay(), study_tag()]

save(document(defs, body,
              "Poster study: a leader addresses the assembly",
              "Graphic poster illustration: a speaker in a dark suit and red tie gestures from a rostrum on the "
              "left, lit by a spotlight; curved tiers of delegates of many backgrounds face them, some wearing "
              "interpretation headsets and some raising hands; a gold wall and a giant screen repeat the "
              "speaker's silhouette. Fictional scenario for a style study."),
     Path(__file__).resolve().parents[3] / "prototypes" / "poster" / "01-assembly.svg")
