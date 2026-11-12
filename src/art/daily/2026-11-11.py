"""Daily artwork, 2026-11-11: Democrat Scott Colom defeats Sen. Cindy Hyde-Smith in Mississippi.

Visual idea: the slow count blooms. A colossal magnolia blossom (Mississippi's state
flower) opens like a sunrise behind the lit Mississippi State Capitol, while in the
lamplit foreground county election workers check the last absentee and affidavit
envelopes, framed by glossy dark magnolia leaves.

Verified (brief): on Nov. 11, 2026 the AP, NBC News and CBS News projected Colom the
winner after local officials spent days processing absentee and affidavit ballots;
Hyde-Smith conceded by video that evening.
Drawn: generic, unidentifiable election workers handling blank envelopes; the
Mississippi State Capitol (central dome, lantern, gilded eagle, portico, wings) as a
poster backdrop for the state; the magnolia is illustrative symbolism.
Not drawn: no candidates, no vote count, no crowd or celebration, no text or signs.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure, SKIN, HAIR  # noqa: E402

DATE = "2026-11-11"
R = rng(20261111)

# palette: midnight indigo, magnolia cream and blush, leaf green, lamp gold
IND, IND2, IND3 = "#2b2f6b", "#1b1d4a", "#0f1030"
CREAM, CREAM2, CREAM3 = "#fff6e2", "#f4e0b9", "#d9bf8e"
BLUSH = "#f2b7a6"
LEAF, LEAF2, LEAF3 = "#2f6b4f", "#1e4a37", "#0f2a20"
GOLD, GOLD2 = "#f2b63c", "#c98a1e"
STONE, STONE2, STONE3 = "#efe3c8", "#cdbb97", "#9c8a6c"
PAPER = "#fffaf0"
INK = "#121226"


def defs():
    return [
        linear("sky", [(0, IND3), (0.5, IND2), (0.85, IND), (1, "#4a3a72")]),
        radial("bloomglow", [(0, "#fff3d6", 0.95), (0.4, "#ffd7a6", 0.5), (1, "#ffd7a6", 0)]),
        radial("lamp", [(0, "#ffe2a0", 0.85), (0.5, GOLD, 0.35), (1, GOLD, 0)]),
        linear("petal", [(0, PAPER), (0.75, CREAM2), (1, BLUSH)]),
        linear("petalback", [(0, CREAM2), (1, CREAM3)]),
        linear("stone", [(0, STONE), (1, STONE2)], x2=1, y2=0),
        linear("table", [(0, LEAF), (1, LEAF3)]),
        linear("floor", [(0, IND2), (1, INK)]),
        blur("soft", 18),
        blur("softer", 6),
        halftone("dots", IND, dot=1.6, spacing=7),
        halftone("dotsc", CREAM3, dot=1.2, spacing=6),
        grain_filter(),
    ]


# ---------------------------------------------------------------- background
def sky():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#sky)")]
    out.append(rect(0, 0, WIDTH, 560, fill="url(#dots)", opacity=0.5))
    # faint stars
    for _ in range(40):
        out.append(circle(R.uniform(0, WIDTH), R.uniform(0, 260), R.uniform(0.8, 1.8), fill=CREAM, opacity=R.uniform(0.3, 0.8)))
    return out


def magnolia(cx=600, cy=400):
    """A huge stylised magnolia blossom rising behind the Capitol like a sun."""
    out = []
    for k in range(18):
        a = math.radians(-90 + k * 10 + 5)
        a2 = a + math.radians(3.5)
        out.append(path(f"M{cx} {cy} L{cx + 900 * math.sin(a):.0f} {cy - 900 * math.cos(a):.0f} "
                        f"L{cx + 900 * math.sin(a2):.0f} {cy - 900 * math.cos(a2):.0f} Z", fill="#ffe9c4", opacity=0.07))
    out.append(circle(cx, cy, 470, fill="url(#bloomglow)"))
    # back ring of petals, then front ring, each a pointed oval rotated about the centre
    def petal(angle, length, width, fill, op=1.0):
        a = math.radians(angle)
        tipx, tipy = cx + length * math.sin(a), cy - length * math.cos(a)
        # control points either side of the axis
        px, py = math.cos(a), math.sin(a)
        mx, my = cx + 0.55 * length * math.sin(a), cy - 0.55 * length * math.cos(a)
        d = (f"M{cx:.1f} {cy:.1f} Q{mx + width * px:.1f} {my + width * py:.1f} {tipx:.1f} {tipy:.1f} "
             f"Q{mx - width * px:.1f} {my - width * py:.1f} {cx:.1f} {cy:.1f} Z")
        return path(d, fill=fill, opacity=op)

    for k in range(6):
        out.append(petal(-75 + k * 30 + 15, 300, 120, "url(#petalback)", 0.9))
    for k in range(5):
        out.append(petal(-60 + k * 30, 330, 115, "url(#petal)"))
    # petal centre veins
    for k in range(5):
        a = math.radians(-60 + k * 30)
        out.append(path(f"M{cx:.0f} {cy:.0f} L{cx + 250 * math.sin(a):.1f} {cy - 250 * math.cos(a):.1f}",
                        stroke=CREAM3, stroke_width=3, opacity=0.5, fill="none"))
    # stamen cone (hidden mostly by the dome, its tip peeks above)
    out.append(ellipse(cx, cy - 40, 46, 80, fill=BLUSH, opacity=0.9))
    for i in range(7):
        out.append(path(f"M{cx - 40} {cy - 90 + i * 14} Q{cx} {cy - 100 + i * 14} {cx + 40} {cy - 90 + i * 14}",
                        stroke="#d98a7a", stroke_width=3, fill="none", opacity=0.7))
    return out


def capitol(cx=600):
    """Mississippi State Capitol: central dome with lantern and gilded eagle, portico, two wings."""
    out = []
    base = 600
    # long main block and wings
    out.append(rect(cx - 520, base - 120, 1040, 140, fill=STONE2))
    out.append(rect(cx - 520, base - 128, 1040, 12, fill=STONE))
    for side in (-1, 1):
        wx = cx + side * 340
        # wing pavilions with low saucer domes (over the chambers)
        out.append(rect(wx - 110, base - 175, 220, 195, fill="url(#stone)"))
        out.append(rect(wx - 118, base - 185, 236, 14, fill=STONE))
        out.append(path(f"M{wx - 85} {base - 185} Q{wx} {base - 250} {wx + 85} {base - 185} Z", fill=STONE2))
        out.append(path(f"M{wx - 60} {base - 196} Q{wx} {base - 238} {wx + 60} {base - 196}", stroke=STONE3, stroke_width=3, fill="none"))
        for k in range(6):
            x = wx - 92 + k * 36
            out.append(rect(x, base - 165, 14, 175, fill=STONE3, opacity=0.55))
            out.append(rect(x + 3, base - 165, 3, 175, fill=PAPER, opacity=0.5))
        # lit windows on the main block between wing and centre
        for k in range(5):
            x = cx + side * (170 + k * 30) - 7
            out.append(rect(x, base - 95, 14, 30, fill=GOLD, opacity=0.85))
            out.append(rect(x, base - 50, 14, 30, fill=GOLD, opacity=0.7))
    # central drum and dome
    out.append(rect(cx - 150, base - 330, 300, 210, fill="url(#stone)"))
    out.append(rect(cx - 160, base - 340, 320, 16, fill=STONE))
    for k in range(11):
        x = cx - 140 + k * 27
        out.append(rect(x, base - 320, 11, 190, fill=STONE3, opacity=0.5))
        out.append(rect(x + 2, base - 320, 3, 190, fill=PAPER, opacity=0.55))
    # upper drum
    out.append(rect(cx - 118, base - 385, 236, 50, fill=STONE))
    for k in range(9):
        out.append(rect(cx - 104 + k * 25, base - 378, 8, 36, fill=GOLD, opacity=0.6))
    # dome shell with ribs
    out.append(path(f"M{cx - 125} {base - 383} Q{cx - 120} {base - 560} {cx} {base - 575} "
                    f"Q{cx + 120} {base - 560} {cx + 125} {base - 383} Z", fill="url(#stone)"))
    for k in range(-4, 5):
        x = cx + k * 26
        out.append(path(f"M{x} {base - 385} Q{x * 0.25 + cx * 0.75:.1f} {base - 540} {cx} {base - 572}",
                        stroke=STONE3, stroke_width=3, fill="none", opacity=0.6))
    # rim light on the dome's edge
    out.append(path(f"M{cx - 125} {base - 383} Q{cx - 120} {base - 560} {cx} {base - 575} "
                    f"Q{cx + 120} {base - 560} {cx + 125} {base - 383}", stroke="#fff3d6", stroke_width=5, fill="none", opacity=0.8))
    # lantern
    out.append(rect(cx - 26, base - 630, 52, 58, fill=STONE))
    for k in range(4):
        out.append(rect(cx - 20 + k * 12, base - 622, 5, 44, fill=GOLD, opacity=0.9))
    out.append(path(f"M{cx - 32} {base - 630} Q{cx} {base - 665} {cx + 32} {base - 630} Z", fill=STONE2))
    # gilded eagle, wings spread
    ey = base - 680
    out.append(path(f"M{cx} {ey + 14} L{cx - 34} {ey - 6} L{cx - 22} {ey + 2} L{cx - 30} {ey + 6} L{cx - 6} {ey + 12} Z", fill=GOLD))
    out.append(path(f"M{cx} {ey + 14} L{cx + 34} {ey - 6} L{cx + 22} {ey + 2} L{cx + 30} {ey + 6} L{cx + 6} {ey + 12} Z", fill=GOLD))
    out.append(ellipse(cx, ey + 12, 6, 10, fill=GOLD2))
    out.append(circle(cx + 1, ey + 1, 4, fill=GOLD2))
    out.append(circle(cx, ey + 8, 34, fill="#ffe2a0", opacity=0.25, filter="url(#softer)"))
    # central portico: 6 columns, pediment
    out.append(path(f"M{cx - 140} {base - 140} L{cx} {base - 200} L{cx + 140} {base - 140} Z", fill=STONE))
    out.append(path(f"M{cx - 110} {base - 148} L{cx} {base - 186} L{cx + 110} {base - 148} Z", fill=STONE2))
    out.append(rect(cx - 140, base - 140, 280, 16, fill=STONE))
    for k in range(6):
        x = cx - 125 + k * 48
        out.append(rect(x, base - 124, 18, 144, fill=STONE))
        out.append(rect(x + 13, base - 124, 5, 144, fill=STONE3, opacity=0.6))
    out.append(rect(cx - 120, base - 120, 240, 140, fill=GOLD2, opacity=0.25))
    # steps
    for i in range(4):
        out.append(rect(cx - 160 - i * 14, base + 20 + i * 8, 320 + i * 28, 8, fill=STONE if i % 2 else STONE2))
    # lawn and trees in silhouette
    out.append(rect(0, base + 20, WIDTH, 60, fill=LEAF3))
    for x in (40, 130, 1070, 1160):
        out += cloud_puffs(R, x, base - 20, 110, 90, 7, 25, 45, fill=LEAF2)
    return out


# ---------------------------------------------------------------- foreground count room
def envelope(w=30, h=20, rot=0, fill=PAPER):
    return group([rect(-w / 2, -h / 2, w, h, fill=fill, stroke=CREAM3, stroke_width=0.8),
                  path(f"M{-w / 2} {-h / 2} L0 {h * 0.1} L{w / 2} {-h / 2}", fill="none", stroke=CREAM3, stroke_width=0.8)],
                 transform=f"rotate({rot})")


def lamp_light():
    out = []
    for x in (330, 870):
        out.append(path(f"M{x - 30} 610 L{x - 230} 760 L{x + 230} 760 L{x + 30} 610 Z", fill="#ffe2a0", opacity=0.14))
        out.append(ellipse(x, 762, 260, 46, fill="url(#lamp)"))
    return out


def lamps():
    out = []
    for x in (330, 870):
        out.append(path(f"M{x - 34} 612 Q{x} 570 {x + 34} 612 Z", fill=LEAF2))
        out.append(rect(x - 3, 540, 6, 36, fill=LEAF3))
        out.append(ellipse(x, 612, 30, 5, fill="#ffe9b5"))
        out.append(circle(x, 616, 30, fill="#ffe2a0", opacity=0.35, filter="url(#softer)"))
    return out


def workers():
    out = []
    # seated workers behind the table (table hides their legs); feet below the table edge
    specs = [
        (290, 1, SKIN[4], HAIR[0], "short", "#8a3b4a", Pose(back_arm=(60, 70), front_arm=(115, 40), head_tilt=12)),
        (540, -1, SKIN[1], HAIR[3], "bun", "#3b5c8a", Pose(back_arm=(55, 60), front_arm=(70, 80), head_tilt=18)),
        (760, 1, SKIN[2], HAIR[5], "short", "#c26a2b", Pose(back_arm=(65, 55), front_arm=(105, 55), head_tilt=8)),
        (960, -1, SKIN[5], HAIR[0], "long", "#5b4a8a", Pose(back_arm=(60, 70), front_arm=(120, 35), head_tilt=6)),
    ]
    for x, facing, skin, hair, style, top, pose in specs:
        look = Look(skin=skin, top=top, bottom=INK, hair=hair, hair_style=style)
        env = envelope(16, 11, rot=-10)
        out.append(figure(x, 880, 360, facing=facing, pose=pose, look=look, hand_items={"front": env}))
    return out


def standing_worker():
    look = Look(skin=SKIN[3], top=GOLD2, bottom=IND2, hair=HAIR[1], hair_style="cap", vest=False)
    tray = group([rect(-4, -20, 34, 18, fill=CREAM3, stroke=STONE3, stroke_width=1)] +
                 [rect(-2 + i * 6, -30 + (i % 2) * 2, 5, 12, fill=PAPER, stroke=CREAM3, stroke_width=0.5) for i in range(5)])
    pose = Pose(back_arm=(40, 30), front_arm=(48, 28), back_leg=(-18, -6), front_leg=(20, -4), lean=6, head_tilt=6)
    return [figure(10, 1230, 640, facing=1, pose=pose, look=look, hand_items={"front": tray})]


def table():
    out = []
    far, near = 700, 900
    out.append(path(f"M150 {far} L1050 {far} L1260 {near} L-60 {near} Z", fill="url(#table)"))
    out.append(path(f"M150 {far} L1050 {far} L1260 {near} L-60 {near} Z", fill="url(#dots)", opacity=0.35))
    out.append(path(f"M150 {far} L1050 {far} L1056 {far + 8} L144 {far + 8} Z", fill=LEAF))
    # lamp pools on the cloth
    for x in (380, 830):
        out.append(ellipse(x, 770, 240, 70, fill="url(#lamp)"))
    # trays of envelopes receding along the table
    for x, y, sc in ((250, 712, 0.8), (480, 712, 0.8), (720, 712, 0.8), (950, 712, 0.8),
                     (120, 800, 1.25), (1080, 800, 1.25)):
        w, h = 80 * sc, 30 * sc
        out.append(rect(x - w / 2, y, w, h, fill=CREAM3, stroke=STONE3, stroke_width=1.5))
        for i in range(8):
            out.append(rect(x - w / 2 + 6 * sc + i * 8.5 * sc, y - 16 * sc + R.uniform(-3, 3) * sc, 7 * sc, 22 * sc,
                            fill=PAPER, stroke=CREAM3, stroke_width=0.6))
    # loose envelopes, bigger near the viewer
    for x, y, sz, rot in ((300, 760, 1.2, 8), (420, 790, 1.4, -14), (560, 745, 1.0, 5), (760, 775, 1.3, -6),
                          (880, 820, 1.7, 12), (640, 850, 1.9, -9), (230, 850, 1.8, 15)):
        out.append(group([envelope(40 * sz, 26 * sz, rot)], transform=f"translate({x} {y})"))
    # desk lamps
    for x in (420, 860):
        out.append(rect(x - 30, 742, 60, 8, fill=LEAF3))
        out.append(path(f"M{x} 746 L{x + 8} 690 L{x - 10} 660", stroke=LEAF3, stroke_width=6, fill="none"))
        out.append(path(f"M{x - 54} 680 Q{x - 14} 626 {x + 24} 664 Z", fill=GOLD2))
        out.append(path(f"M{x - 54} 680 L{x + 24} 664", stroke="#ffe9b5", stroke_width=4))
        out.append(circle(x - 14, 676, 26, fill="#ffe2a0", opacity=0.45, filter="url(#softer)"))
        out.append(path(f"M{x - 40} 672 L{x - 120} 770 L{x + 110} 770 L{x + 14} 664 Z", fill="#ffe2a0", opacity=0.12))
    return out


def leaves():
    """Glossy magnolia leaves framing the top corners (foreground layer)."""
    out = []
    def leaf(x, y, length, angle, fill):
        return group([path(f"M0 0 Q{length * 0.35} {-length * 0.22} {length} 0 Q{length * 0.35} {length * 0.22} 0 0 Z", fill=fill),
                      path(f"M0 0 L{length * 0.95} 0", stroke=LEAF, stroke_width=3, fill="none", opacity=0.7)],
                     transform=f"translate({x} {y}) rotate({angle})")
    for x, y, l, a in ((-30, 40, 260, 20), (-40, 150, 230, -5), (-20, -20, 220, 48)):
        out.append(leaf(x, y, l, a, LEAF3))
    for x, y, l, a in ((1230, 30, 270, 160), (1240, 140, 230, 185), (1220, -30, 220, 132)):
        out.append(leaf(x, y, l, a, LEAF3))
    return out


def build():
    d = defs()
    body = []
    body += sky()
    body += magnolia()
    body.append(group(capitol(), transform="translate(600 640) scale(0.8) translate(-600 -600)"))
    body += workers()
    body += table()
    body += standing_worker()
    body += leaves()
    body.append(rect(0, 0, WIDTH, HEIGHT, fill="none", stroke=INK, stroke_width=60, opacity=0.4, filter="url(#soft)"))
    body.append(grain_overlay(opacity=0.32))
    title = "Democrat Scott Colom wins Mississippi Senate race"
    desc = ("Editorial illustration. At night, election workers at a long lamplit table check stacks of absentee "
            "and affidavit ballot envelopes while a colleague carries in another tray. Behind them the Mississippi "
            "State Capitol, with its dome, lantern and gilded eagle, glows in front of a giant magnolia blossom "
            "opening like a sunrise. It represents the days-long count that ended on Nov. 11, 2026, when Democrat "
            "Scott Colom was projected to have defeated Sen. Cindy Hyde-Smith.")
    return document(d, body, title, desc)


if __name__ == "__main__":
    save(build(), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
