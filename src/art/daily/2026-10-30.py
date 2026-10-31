"""Daily artwork, 2026-10-30: Pope Leo XIV votes by mail in the US midterms.

Visual idea: from a Vatican terrace beside St. Peter's dome, Leo sends a sealed
airmail envelope off along a huge dotted arc that sweeps over the curve of the
Atlantic to a tiny Chicago skyline on the far horizon: one vote crossing an ocean.

Verified (brief): the Holy See confirmed on Oct. 30 that Leo XIV, born in
Chicago, cast a mail-in ballot in Illinois ahead of the Nov. 3 midterms, the
first pope to vote in a U.S. general election (AP via PBS; CBS; NYT: "votes by
mail, from the Vatican").
Drawn: Leo in white cassock and skullcap releasing a plain, sealed envelope;
St. Peter's dome; a generic Chicago skyline (Willis Tower, Hancock Center).
Not drawn because not known: any ballot content, marks, candidates, parties or
results; no text at all; no crowds, guards or medical references.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-10-30"
R = rng(20261030)
ROSE, PEACH, LILAC, DUSK = "#f6b8a6", "#ffd9b0", "#b9a6d9", "#6c5aa6"
SEA, SEA2 = "#2f8f9d", "#1d6474"
STONE, STONE2, STONE3 = "#efe2cc", "#d9c3a2", "#b69c78"
TERRA, TERRA2 = "#c8613f", "#a24a30"
CREAM, CASSOCK_SH = "#fbf8f1", "#e3ddd2"
AIR_RED, AIR_BLUE = "#d6342c", "#24448f"
INK = "#2a2340"
FLOOR_Y = 800
HORIZON = 560


def sky():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#sky)"), rect(0, 0, WIDTH, HEIGHT, fill="url(#west)")]
    for k in range(14):  # soft sun rays fanning out from behind the dome
        a = math.radians(-100 + k * 13)
        a2 = a + math.radians(4)
        out.append(poly([(250, 300), (250 + 1600 * math.cos(a), 300 + 1600 * math.sin(a)),
                         (250 + 1600 * math.cos(a2), 300 + 1600 * math.sin(a2))], fill="#fff4dc", opacity=0.13))
    out += [rect(0, 0, WIDTH, 120 + k * 50, fill="url(#skydots)", opacity=0.09) for k in range(4)]  # dots fade downward
    out.append(circle(250, 300, 330, fill="url(#sunglow)"))        # low Roman sun behind the dome
    out.append(circle(250, 300, 120, fill=PEACH, opacity=0.9))
    for _ in range(40):  # first stars appearing over the cooler, western side
        x, y = R.uniform(760, WIDTH), R.uniform(10, 300)
        out.append(circle(x, y, R.choice([0.9, 1.3]), fill="#ffffff", opacity=R.uniform(0.3, 0.8)))
    return out


def ocean():
    """A curved Atlantic horizon: the Earth bulges up toward the middle."""
    top = f"M-40 {HORIZON + 90} Q600 {HORIZON - 120} 1240 {HORIZON + 90}"
    out = [path(top + f" L1240 {HEIGHT} L-40 {HEIGHT} Z", fill="url(#sea)")]
    for k in range(9):  # glinting wave lines
        y = HORIZON + 20 + k * 22
        x = R.uniform(480, 980)
        out.append(rect(x, y, R.uniform(40, 120), 2.2, fill="#bfeef0", opacity=0.45 - k * 0.03))
    out.append(path(top, fill="none", stroke="#fde7d0", stroke_width=3, opacity=0.7))  # rim of light on the horizon
    return out


def chicago():
    """A small, generic Chicago skyline on the far horizon: Willis Tower and the Hancock Center."""
    base = HORIZON + 4
    out = [rect(1000, base - 22, 170, 24, fill=DUSK)]
    for x, w, h in [(990, 18, 34), (1010, 16, 48), (1078, 14, 44), (1150, 18, 30), (1168, 14, 38)]:
        out.append(rect(x, base - h, w, h, fill=DUSK))
    # Willis Tower: stepped bundle of tubes, two antennas
    for dx, h in [(0, 96), (10, 122), (20, 108), (30, 84)]:
        out.append(rect(1030 + dx, base - h, 10, h, fill="#3b2f66"))
    out += [rect(1043, base - 140, 2, 18, fill="#3b2f66"), rect(1051, base - 136, 2, 14, fill="#3b2f66")]
    # Hancock Center: tapered tower with X-bracing and two antennas
    out.append(poly([(1100, base), (1124, base), (1120, base - 104), (1104, base - 104)], fill="#3b2f66"))
    for y in range(int(base - 100), int(base), 26):
        out.append(path(f"M1103 {y} L1121 {y + 24} M1121 {y} L1103 {y + 24}", stroke=LILAC, stroke_width=1, opacity=0.6))
    out += [rect(1107, base - 124, 2, 20, fill="#3b2f66"), rect(1115, base - 124, 2, 20, fill="#3b2f66")]
    for _ in range(26):  # lit windows
        out.append(rect(R.uniform(1000, 1165), R.uniform(base - 90, base - 4), 2, 2, fill="#ffe3a0", opacity=0.8))
    out.insert(0, ellipse(1080, base - 30, 130, 80, fill="url(#cityglow)"))
    return [group(out, transform=f"translate(-90 6) translate(1080 {base}) scale(1.1) translate(-1080 {-base})")]


def dome():
    """St. Peter's Basilica dome: drum with paired columns, ribbed dome, lantern, cross."""
    cx, by = 300, 520
    out = [rect(cx - 210, by, 420, 140, fill=STONE2)]                       # facade block below the drum
    for i in range(9):
        out.append(rect(cx - 195 + i * 47, by + 14, 12, 126, fill=STONE3, opacity=0.6))
    out.append(rect(cx - 150, by - 90, 300, 92, fill=STONE))                 # drum
    for i in range(8):
        x = cx - 140 + i * 40
        out += [rect(x, by - 86, 7, 84, fill=STONE2), rect(x + 10, by - 86, 7, 84, fill=STONE2)]
        if i < 7:
            out.append(path(f"M{x + 23} {by - 18} L{x + 23} {by - 52} Q{x + 30} {by - 62} {x + 37} {by - 52} "
                            f"L{x + 37} {by - 18} Z", fill=STONE3))
    out.append(rect(cx - 160, by - 98, 320, 12, fill=STONE2))
    shell = f"M{cx - 150} {by - 98} Q{cx - 150} {by - 300} {cx} {by - 318} Q{cx + 150} {by - 300} {cx + 150} {by - 98} Z"
    out.append(path(shell, fill="url(#domefill)"))
    for k in range(-3, 4):  # ribs
        x = cx + k * 44
        out.append(path(f"M{x} {by - 98} Q{cx + k * 30} {by - 250} {cx + k * 6} {by - 312}", fill="none",
                        stroke=STONE, stroke_width=5))
    out.append(path(shell, fill="url(#rimlight)"))
    # lantern and cross
    out += [rect(cx - 24, by - 372, 48, 56, fill=STONE),
            rect(cx - 20, by - 366, 7, 46, fill=STONE2), rect(cx + 13, by - 366, 7, 46, fill=STONE2),
            path(f"M{cx - 28} {by - 372} Q{cx} {by - 408} {cx + 28} {by - 372} Z", fill="#9a8a8c"),
            rect(cx - 3, by - 440, 6, 36, fill="#e8c46a"), rect(cx - 12, by - 430, 24, 5, fill="#e8c46a")]
    return out


def rooftops():
    """Terracotta Roman rooftops below the terrace, between the dome and the sea."""
    out = []
    x = 470
    while x < 1220:
        w, h = R.uniform(50, 90), R.uniform(10, 50)
        top = FLOOR_Y - 150 - h
        out.append(rect(x, top, w, 300, fill=R.choice([TERRA, TERRA2, "#d98657"])))
        out.append(poly([(x - 6, top), (x + w / 2, top - 22), (x + w + 6, top)], fill=TERRA2))
        for wy in range(int(top) + 14, int(top) + 70, 24):
            out.append(rect(x + 10, wy, 8, 12, fill="#5b2e22", opacity=0.6))
        x += w + R.uniform(2, 10)
    return out


def terrace():
    """Stone terrace floor and a balustrade the pope stands behind."""
    rail_y = FLOOR_Y - 150
    out = [rect(0, rail_y + 10, WIDTH, HEIGHT, fill=STONE2)]
    for i in range(27):  # balusters
        x = 20 + i * 46
        out.append(path(f"M{x} {FLOOR_Y} L{x} {FLOOR_Y - 26} Q{x - 10} {FLOOR_Y - 70} {x + 6} {FLOOR_Y - 100} "
                        f"Q{x + 22} {FLOOR_Y - 70} {x + 12} {FLOOR_Y - 26} L{x + 12} {FLOOR_Y} Z", fill=STONE))
    out.append(rect(0, rail_y - 10, WIDTH, 22, fill=STONE))
    out.append(rect(0, rail_y + 10, WIDTH, 6, fill=STONE3))
    out.append(rect(0, FLOOR_Y, WIDTH, HEIGHT - FLOOR_Y, fill=STONE3))
    # long shadow of the balustrade toward the viewer
    out.append(rect(0, FLOOR_Y, WIDTH, 26, fill=INK, opacity=0.18))
    return out


def envelope(x, y, w, angle):
    """A plain sealed airmail envelope with red/blue border dashes; no writing."""
    h = w * 0.62
    edge = []
    step = w / 10
    for i in range(10):
        c = AIR_RED if i % 2 == 0 else AIR_BLUE
        edge += [poly([(i * step, 0), ((i + 0.5) * step, 0), ((i + 1) * step - step * 0.2, h * 0.09), (i * step + step * 0.3, h * 0.09)], fill=c),
                 poly([(i * step, h), ((i + 0.5) * step, h), ((i + 1) * step - step * 0.2, h * 0.91), (i * step + step * 0.3, h * 0.91)], fill=c)]
    parts = [rect(0, 0, w, h, fill=CREAM), *edge,
             path(f"M0 0 L{w / 2} {h * 0.55} L{w} 0", fill="none", stroke=STONE3, stroke_width=w * 0.02),
             circle(w / 2, h * 0.55, w * 0.06, fill=AIR_RED)]
    return group([ellipse(w / 2, h / 2, w * 0.9, h * 0.9, fill="url(#envglow)"), *parts],
                 transform=f"translate({x} {y}) rotate({angle}) translate({-w / 2} {-h / 2})")


def flight():
    """The envelope's dotted flight path from the pope's hand to Chicago."""
    p0, c, p1 = (445, 350), (720, -60), (975, 440)
    pts = []
    for i in range(46):
        t = i / 45
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t ** 2 * p1[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t ** 2 * p1[1]
        pts.append((x, y))
    out = [circle(x, y, 3.4 - 1.6 * (i / 45), fill=CREAM, opacity=0.95 - 0.4 * (i / 45))
           for i, (x, y) in enumerate(pts) if i > 1]
    return out, pts


def pope():
    """Leo XIV in white cassock, short cape and white zucchetto, arm raised to send the envelope."""
    s = 4.6
    cape = path("M-12 -73 Q0 -80 12 -73 L14 -58 Q0 -54 -14 -58 Z", fill=CREAM)
    robe = path("M-10.5 -73 L10.5 -73 L15.5 2 Q0 4.5 -15.5 2 Z", fill=CREAM)
    fold = path("M-2 -44 L-4 -2 M5 -44 L8 -2", fill="none", stroke=CASSOCK_SH, stroke_width=1.2)
    sash = rect(-9.5, -49, 19, 4, fill=CASSOCK_SH)
    zucchetto = path("M-3 -96 Q3.5 -101 9.5 -95 Q3.5 -97 -3 -96 Z", fill=CREAM)
    look = Look(skin="#e9b9a0", top=CREAM, top_shade=CASSOCK_SH, bottom="#7a4a3a", shoes="#7a4a3a", hair="#9c9a9e",
                hair_style="short", coat=True, face="smile", extra=[robe, fold, sash, cape, zucchetto])
    pose = Pose(back_arm=(20, 15), front_arm=(140, -12), back_leg=(-5, 0), front_leg=(7, 0), lean=-3, head_tilt=-14)
    shadow = poly([(290, FLOOR_Y + 4), (372, FLOOR_Y + 4), (760, HEIGHT), (520, HEIGHT)], fill=INK, opacity=0.2)
    rim = path("M262 470 L250 800", stroke="#ffe3b0", stroke_width=6, stroke_linecap="round", opacity=0.8)
    return [shadow, ellipse(330, FLOOR_Y + 8, 90, 10, fill=INK, opacity=0.2),
            # warm rim light halo behind the figure
            ellipse(320, FLOOR_Y - 230, 120, 250, fill="url(#figglow)"),
            figure(320, FLOOR_Y + 6, 100 * s, 1, pose, look), rim]


def gulls():
    out = []
    for x, y, w in [(820, 610, 18), (870, 590, 13), (640, 520, 15)]:
        out.append(path(f"M{x - w} {y} Q{x - w / 2} {y - w * 0.5} {x} {y} Q{x + w / 2} {y - w * 0.5} {x + w} {y}",
                        fill="none", stroke=CREAM, stroke_width=2.4, stroke_linecap="round"))
    return out


def stone_pine():
    """A Roman umbrella pine framing the left edge of the terrace (foreground)."""
    out = [path("M-30 900 Q20 600 40 150 L62 150 Q48 600 10 900 Z", fill="#3a2a34")]
    out += cloud_puffs(R, 30, 110, 300, 90, 16, 30, 60, fill="#2f4a3e")
    out += cloud_puffs(R, 20, 90, 240, 60, 10, 24, 44, fill="#3e6150")
    return out


defs = [grain_filter(), blur("soft", 8),
        linear("sky", [(0, ROSE), (0.6, PEACH), (1, "#fbe8d4")]),
        radial("sunglow", [(0, "#fff3d6", 0.9), (1, PEACH, 0)]),
        linear("sea", [(0, SEA), (1, SEA2)]),
        linear("west", [(0, LILAC, 0), (0.55, LILAC, 0), (1, DUSK, 0.55)], x2=1, y2=0.4),
        halftone("skydots", "#ffffff", dot=1.4, spacing=9),
        radial("cityglow", [(0, "#ffd68a", 0.45), (1, "#ffd68a", 0)]),
        linear("domefill", [(0, "#c9bfd8"), (1, "#a596bb")]),
        linear("rimlight", [(0, "#fff1c9", 0.55), (1, "#fff1c9", 0)], x2=1, y2=0),
        radial("envglow", [(0, "#fff6dc", 0.85), (1, "#fff6dc", 0)]),
        radial("figglow", [(0, "#fff1c9", 0.55), (1, "#fff1c9", 0)])]
trail, pts = flight()
env_x, env_y = pts[11]
body = (sky() + ocean() + chicago() + gulls() + rooftops() + dome() + trail + terrace() + pope()
        + [envelope(env_x, env_y, 120, -24)] + stone_pine() + [grain_overlay(opacity=0.3)])

save(document(defs, body,
              "Pope Leo XIV votes by mail in the US midterms",
              "Graphic poster illustration: at sunset on a stone terrace beside the dome of St. Peter's Basilica, "
              "Pope Leo XIV in a white cassock and skullcap raises his arm to send off a sealed airmail envelope. A "
              "dotted flight path arcs from his hand over the curve of the Atlantic Ocean to a small Chicago skyline, "
              "with the Willis Tower and Hancock Center, on the far horizon. The envelope is blank and closed."),
     Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
