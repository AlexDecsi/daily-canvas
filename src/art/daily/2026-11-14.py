"""Daily artwork, 2026-11-14: SpaceX catches Starship's upper stage with the tower arms.

Visual idea: worm's-eye view of a giant's catch. From the Gulf dunes at Starbase we look
up at the towering lattice launch tower as its two "chopsticks" arms close around the
stainless-steel ship, which drops tail-first on short landing-burn flames, silhouetted
against a huge pale sun disc ringed by faint orbit arcs (an illustrative nod to its 14
orbits). Small silhouetted employees in the foreground throw up their arms and cheer.

Verified (brief): on Nov. 14, 2026, SpaceX caught the Starship upper stage (Ship 42) with
the launch tower's mechanical arms at Starbase, Texas, after Flight 15 launched Friday and
spent ~22 hours in space; employees cheered (CBS News, CNBC).
Drawn: a generic stainless ship with flaps and dark heat-shield tiles, a generic lattice
tower with two arms, dunes and Gulf water, generic cheering workers. Not drawn: the lost
booster, any named person, logos, text. The orbit rings and sun disc are illustrative.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-14"
R = rng(20261114)

# palette: cobalt Gulf sky, sea teal, sun cream, stainless silver, flame coral, dune sand
NAVY, COBALT, AZURE = "#0e1a3f", "#1f3f8f", "#3f7fd0"
SEA, SEA2 = "#1b8f9a", "#0f5b6e"
CREAM, BUTTER = "#fff4d8", "#ffd88a"
STEEL, STEEL2, STEEL3 = "#eef2f6", "#b9c3cf", "#7d8897"
TILE = "#1a1c26"
CORAL, FLAME, GOLD = "#ff5a3c", "#ff9a3c", "#ffe066"
SAND, SAND2 = "#e9b97a", "#c98a50"
INK = "#0a0f24"

HORIZON = 700
SUN = (470, 330, 250)
TX = 800            # tower centre x
TOP = 30            # tower top
ARM_Y = 300         # arms height
SHIP_X, SHIP_W = 500, 86
SHIP_TOP, SHIP_BOT = 120, 520


def defs():
    return [
        linear("sky", [(0, NAVY), (0.35, COBALT), (0.75, AZURE), (1, "#9fc6ec")]),
        radial("sun", [(0, CREAM, 1), (0.6, BUTTER, 0.95), (0.85, BUTTER, 0.5), (1, BUTTER, 0)]),
        radial("flameglow", [(0, GOLD, 0.9), (0.4, FLAME, 0.5), (1, CORAL, 0)]),
        linear("steel", [(0, STEEL3), (0.25, STEEL), (0.55, STEEL2), (0.8, STEEL3), (1, "#4c5563")], x2=1, y2=0),
        linear("flame", [(0, GOLD), (0.5, FLAME), (1, CORAL, 0)]),
        linear("sea", [(0, SEA), (1, SEA2)]),
        linear("dune", [(0, SAND), (1, SAND2)]),
        linear("towerfill", [(0, "#24366b"), (0.5, "#1a2a58"), (1, "#101a3c")], x2=1, y2=0),
        linear("trail", [(0, CREAM, 0), (1, BUTTER, 0.9)]),
        linear("near", [(0, "#2a1d3a"), (1, INK)]),
        blur("soft", 6), blur("softer", 16), blur("haze", 28),
        halftone("dots", CREAM, dot=1.3, spacing=7),
        halftone("sdots", BUTTER, dot=1.6, spacing=8, angle=30),
        grain_filter(strength=0.5),
    ]


def sky():
    sx, sy, sr = SUN
    out = [rect(0, 0, 1200, 900, fill="url(#sky)")]
    out.append(rect(0, 0, 1200, 300, fill="url(#dots)", opacity=0.08))
    # orbit rings: tilted ellipses around the sun (illustrative of 14 orbits)
    for k in range(14):
        rx = sr + 40 + k * 26
        out.append(ellipse(sx, sy, rx, rx * 0.32, fill="none", stroke=CREAM, stroke_width=1.6 if k % 3 else 2.6,
                           opacity=round(0.32 - k * 0.018, 3), transform=f"rotate(-14 {sx} {sy})",
                           stroke_dasharray=None if k % 2 else "3 9"))
    for k in range(24):
        a0 = math.radians(k * 15)
        a1 = math.radians(k * 15 + 6)
        L = 900
        out.append(poly([(sx, sy), (sx + math.cos(a0) * L, sy + math.sin(a0) * L),
                         (sx + math.cos(a1) * L, sy + math.sin(a1) * L)], fill=CREAM, opacity=0.06))
    out.append(circle(sx, sy, sr * 1.25, fill="url(#sun)", opacity=0.55, filter="url(#haze)"))
    out.append(circle(sx, sy, sr, fill="url(#sun)"))
    out.append(circle(sx, sy, sr, fill="url(#sdots)", opacity=0.25))
    # high streaks of thin cloud
    for y, x0, w in ((120, 40, 260), (165, 880, 300), (560, 40, 200), (600, 980, 220)):
        out.append(rect(x0, y, w, 6, rx=3, fill=CREAM, opacity=0.35))
        out.append(rect(x0 + 40, y + 12, w * 0.6, 4, rx=2, fill=CREAM, opacity=0.25))
    return out


def far_shore():
    out = [rect(0, HORIZON - 30, 1200, 60, fill="url(#sea)")]
    for k in range(18):
        y = HORIZON - 26 + k * 3
        x = R.uniform(0, 1100)
        out.append(rect(x, y, R.uniform(30, 120), 1.6, fill=CREAM, opacity=0.35))
    for k in range(10):
        w = 160 - k * 12
        out.append(rect(SUN[0] - w / 2 + R.uniform(-20, 20), HORIZON - 26 + k * 5, w, 2.4, fill=BUTTER,
                        opacity=0.7))
    # distant second tower and the tank farm at left
    out.append(group([
        rect(120, HORIZON - 250, 26, 220, fill="#2d4f86"),
        rect(110, HORIZON - 262, 46, 14, fill="#2d4f86"),
        *[rect(186 + k * 34, HORIZON - 110 + (k % 2) * 20, 24, 80 - (k % 2) * 20, rx=10, fill="#3a62a0")
          for k in range(5)],
    ], opacity=0.85))
    return out


def tower():
    """The launch tower: a square lattice, slightly converging upward (low camera)."""
    out = []
    base_w, top_w = 190, 120
    yb = 900

    def xl(y):
        t = (yb - y) / (yb - TOP)
        return TX - (base_w + (top_w - base_w) * t) / 2

    def xr(y):
        return 2 * TX - xl(y)

    out.append(poly([(xl(yb), yb), (xr(yb), yb), (xr(TOP), TOP), (xl(TOP), TOP)], fill="url(#towerfill)"))
    # rails
    for side in (xl, xr):
        out.append(path(f"M{side(yb):.1f} {yb} L{side(TOP):.1f} {TOP}", stroke=INK, stroke_width=14))
    # rim light on left rail from sun
    out.append(path(f"M{xl(yb) + 6:.1f} {yb} L{xl(TOP) + 6:.1f} {TOP}", stroke=BUTTER, stroke_width=3, opacity=0.7))
    # cross bracing
    y = yb
    step = 58
    while y - step > TOP:
        y2 = y - step
        out.append(path(f"M{xl(y):.1f} {y} L{xr(y2):.1f} {y2} M{xr(y):.1f} {y} L{xl(y2):.1f} {y2}",
                        stroke=INK, stroke_width=5))
        out.append(path(f"M{xl(y2):.1f} {y2} L{xr(y2):.1f} {y2}", stroke=INK, stroke_width=6))
        out.append(path(f"M{xl(y) + 8:.1f} {y} L{xr(y2) - 8:.1f} {y2}", stroke=BUTTER, stroke_width=1.2,
                        opacity=0.35))
        step = max(30, step * 0.94)
        y = y2
    # top crane/lightning mast
    out.append(rect(TX - 6, TOP - 26, 12, 30, fill=INK))
    out.append(circle(TX, TOP - 28, 4, fill=CORAL))
    out.append(circle(TX, TOP - 28, 12, fill=CORAL, opacity=0.4, filter="url(#soft)"))
    return out


def arm(near, y):
    """One chopstick arm: a long tapered truss from the tower carriage to past the ship."""
    x0 = TX - 70
    x1 = SHIP_X - SHIP_W / 2 - 60
    dy = 26 if near else -22          # perspective: near arm drops toward viewer
    col = "#202b4f" if near else "#121a35"
    h0, h1 = 46, 26
    top = [(x0, y - h0 / 2), (x1, y + dy - h1 / 2)]
    bot = [(x1, y + dy + h1 / 2), (x0, y + h0 / 2)]
    g = [poly(top + bot, fill=col)]
    n = 9
    for k in range(n + 1):
        t = k / n
        xa = x0 + (x1 - x0) * t
        ya = y + dy * t
        ha = h0 + (h1 - h0) * t
        g.append(path(f"M{xa:.1f} {ya - ha / 2:.1f} L{xa:.1f} {ya + ha / 2:.1f}", stroke=INK, stroke_width=3))
        if k < n:
            t2 = (k + 1) / n
            xb = x0 + (x1 - x0) * t2
            yb = y + dy * t2
            hb = h0 + (h1 - h0) * t2
            g.append(path(f"M{xa:.1f} {ya - ha / 2:.1f} L{xb:.1f} {yb + hb / 2:.1f}", stroke=INK, stroke_width=2))
    g.append(path(f"M{x0} {y - h0 / 2} L{x1} {y + dy - h1 / 2}", stroke=BUTTER if near else STEEL3,
                  stroke_width=3, opacity=0.8))
    # gripping jaw at the tip, wrapping the ship
    jx = x1
    jy = y + dy
    g.append(poly([(jx + 6, jy - h1 / 2 - 6), (jx - 18, jy - h1 / 2 - 2), (jx - 18, jy + h1 / 2 + 2),
                   (jx + 6, jy + h1 / 2 + 6)], fill=col))
    g.append(rect(jx - 22, jy - h1 / 2 - 8, 8, h1 + 16, fill=CORAL if near else "#7a2f2a"))
    # carriage block on tower
    g.append(rect(TX - 92, y - 40, 60, 80, fill=INK))
    return g


def ship():
    x, w = SHIP_X, SHIP_W
    l, r = x - w / 2, x + w / 2
    nose_h = 120
    out = []
    # glow behind (rim light from sun)
    out.append(rect(l - 8, SHIP_TOP + 40, w + 16, SHIP_BOT - SHIP_TOP - 40, rx=20, fill=CREAM, opacity=0.6,
                    filter="url(#soft)"))
    body = (f"M{l} {SHIP_BOT} L{l} {SHIP_TOP + nose_h} C{l} {SHIP_TOP + 40} {x - 14} {SHIP_TOP} {x} {SHIP_TOP} "
            f"C{x + 14} {SHIP_TOP} {r} {SHIP_TOP + 40} {r} {SHIP_TOP + nose_h} L{r} {SHIP_BOT} Z")
    out.append(path(body, fill="url(#steel)"))
    out.append(rect(l + 14, SHIP_TOP + 70, 7, SHIP_BOT - SHIP_TOP - 80, rx=3, fill="#ffffff", opacity=0.85))
    out.append(circle(l + 17, SHIP_TOP + 200, 14, fill="#ffffff", opacity=0.6, filter="url(#soft)"))
    # heat-shield tiles on the windward (right) half
    tiles = (f"M{x + 6} {SHIP_BOT} L{x + 6} {SHIP_TOP + 30} C{x + 20} {SHIP_TOP + 30} {r} {SHIP_TOP + 60} "
             f"{r} {SHIP_TOP + nose_h} L{r} {SHIP_BOT} Z")
    out.append(path(tiles, fill=TILE))
    for yy in range(SHIP_TOP + 60, SHIP_BOT, 12):
        out.append(path(f"M{x + 8} {yy} L{r - 2} {yy}", stroke="#2c3040", stroke_width=1))
    # ring welds
    for yy in range(SHIP_TOP + nose_h + 20, SHIP_BOT, 34):
        out.append(path(f"M{l} {yy} L{x + 6} {yy}", stroke=STEEL3, stroke_width=1.2, opacity=0.7))
    # forward flaps (small) and aft flaps (large)
    fy = SHIP_TOP + 70
    out.append(poly([(l + 2, fy), (l - 26, fy + 18), (l - 26, fy + 62), (l + 2, fy + 76)], fill=TILE))
    out.append(poly([(r - 2, fy), (r + 26, fy + 18), (r + 26, fy + 62), (r - 2, fy + 76)], fill=TILE))
    ay = SHIP_BOT - 120
    out.append(poly([(l + 2, ay), (l - 34, ay + 20), (l - 34, ay + 108), (l + 2, ay + 116)], fill=TILE))
    out.append(poly([(r - 2, ay), (r + 34, ay + 20), (r + 34, ay + 108), (r - 2, ay + 116)], fill=TILE))
    # catch pins under the forward flaps
    out.append(rect(l - 18, ARM_Y - 6, 18, 10, fill=STEEL3))
    out.append(rect(r, ARM_Y - 6, 18, 10, fill=STEEL3))
    # engine skirt and bells
    out.append(rect(l + 4, SHIP_BOT, w - 8, 10, fill="#3c4452"))
    for bx in (x - 24, x, x + 24):
        out.append(path(f"M{bx - 7} {SHIP_BOT + 10} L{bx - 11} {SHIP_BOT + 28} L{bx + 11} {SHIP_BOT + 28} "
                        f"L{bx + 7} {SHIP_BOT + 10} Z", fill="#2a2f3a"))
    return out


def descent():
    """Illustrative return path: a glowing dotted arc dropping out of the orbit rings onto the ship."""
    x = SHIP_X
    d = f"M60 40 C220 20 {x - 40} 10 {x} {SHIP_TOP - 14}"
    out = [path(d, fill="none", stroke=BUTTER, stroke_width=16, opacity=0.25, filter="url(#soft)"),
           path(d, fill="none", stroke=CREAM, stroke_width=4, stroke_dasharray="2 12", stroke_linecap="round",
                opacity=0.9)]
    # two small down-chevrons above the nose: it is coming down
    for k, yy in enumerate((SHIP_TOP - 70, SHIP_TOP - 44)):
        out.append(path(f"M{x - 14} {yy} L{x} {yy + 12} L{x + 14} {yy}", fill="none", stroke=CREAM,
                        stroke_width=4, stroke_linecap="round", opacity=0.55 + 0.3 * k))
    return out


def flames():
    x = SHIP_X
    y = SHIP_BOT + 28
    out = [ellipse(x, y + 40, 130, 80, fill="url(#flameglow)", filter="url(#softer)")]
    for bx, ln in ((x - 24, 62), (x, 80), (x + 24, 64)):
        out.append(path(f"M{bx - 11} {y} Q{bx} {y + ln * 1.1} {bx} {y + ln} Q{bx} {y + ln * 1.1} {bx + 11} {y} Z",
                        fill="url(#flame)"))
        out.append(path(f"M{bx - 5} {y} Q{bx} {y + ln * 0.6} {bx + 5} {y} Z", fill=CREAM))
    return out


def plume():
    """Steam and dust billowing off the pad below the tower."""
    out = []
    cx = (SHIP_X + TX) / 2
    for k in range(26):
        px = cx + R.uniform(-340, 300)
        py = HORIZON + 4 + R.uniform(-26, 26)
        rr = R.uniform(26, 58)
        out.append(circle(round(px, 1), round(py, 1), round(rr, 1), fill=STEEL if k % 3 else CREAM,
                          opacity=round(R.uniform(0.75, 0.95), 2)))
    for k in range(12):
        px = cx + R.uniform(-320, 280)
        py = HORIZON - 30 + R.uniform(-20, 20)
        out.append(circle(round(px, 1), round(py, 1), R.uniform(20, 44), fill=BUTTER, opacity=0.5))
    out.append(ellipse(SHIP_X, HORIZON - 10, 200, 50, fill=FLAME, opacity=0.35, filter="url(#softer)"))
    return out


def dunes():
    out = [path("M0 760 Q200 715 420 748 T860 740 T1200 735 L1200 900 L0 900 Z", fill="url(#dune)")]
    out.append(path("M0 760 Q200 715 420 748 T860 740 T1200 735", fill="none", stroke=CREAM, stroke_width=3,
                    opacity=0.5))
    fence = []
    for k in range(40):
        fx = k * 31
        fy = 742 + 12 * math.sin(fx / 170)
        fence.append(rect(fx, fy - 34, 3, 36, fill=INK))
    fence.append(path(" ".join(f"{'M' if k == 0 else 'L'}{k * 31} {742 + 12 * math.sin(k * 31 / 170) - 30:.1f}"
                                for k in range(40)), fill="none", stroke=INK, stroke_width=2))
    fence.append(path(" ".join(f"{'M' if k == 0 else 'L'}{k * 31} {742 + 12 * math.sin(k * 31 / 170) - 14:.1f}"
                                for k in range(40)), fill="none", stroke=INK, stroke_width=1.5))
    out.append(group(fence, opacity=0.55))
    # long cast shadows toward the viewer (sun behind)
    for sx in (160, 360, 650, 900, 1060):
        out.append(poly([(sx - 10, 830), (sx + 10, 830), (sx + 60, 900), (sx - 20, 900)], fill=SAND2, opacity=0.5))
    return out


def grass():
    out = []
    for k in range(70):
        x = R.uniform(-10, 1210)
        if 230 < x < 980 and R.random() < 0.6:
            continue
        h = R.uniform(40, 120)
        lean = R.uniform(-25, 25)
        out.append(path(f"M{x:.1f} 905 Q{x + lean * 0.3:.1f} {905 - h * 0.6:.1f} {x + lean:.1f} {905 - h:.1f}",
                        fill="none", stroke=INK, stroke_width=R.uniform(2, 4), stroke_linecap="round"))
    return out


def workers():
    """Generic SpaceX employees cheering at the edge of the site (silhouetted, backlit)."""
    dark = dict(skin="#1d1630", top="#1d1630", bottom="#130f22", shoes="#0a0814", hair="#0a0814")
    out = []
    spec = [
        (250, 900, 250, -1, Pose(back_arm=(165, 10), front_arm=(170, -10), back_leg=(-8, 0), front_leg=(8, 0),
                                 head_tilt=-18), "short"),
        (360, 905, 210, 1, Pose(back_arm=(150, 20), front_arm=(120, 40), back_leg=(-5, 0), front_leg=(6, 0),
                                head_tilt=-22), "cap"),
        (930, 902, 236, -1, Pose(back_arm=(100, 70), front_arm=(95, 75), back_leg=(-6, 0), front_leg=(6, 0),
                                 head_tilt=-20), "bun"),
        (1050, 908, 268, -1, Pose(back_arm=(-15, 15), front_arm=(170, 0), back_leg=(-6, 0), front_leg=(10, 0),
                                  head_tilt=-15), "short"),
        (1150, 900, 200, -1, Pose(back_arm=(160, 15), front_arm=(160, 15), back_leg=(-8, 0), front_leg=(8, 0),
                                  head_tilt=-25), "long"),
    ]
    for x, y, h, f, pose, hair in spec:
        out.append(ellipse(x + 30, y - 2, h * 0.22, 8, fill=INK, opacity=0.4))
        rim = Look(**{**dark, "skin": BUTTER, "top": BUTTER, "bottom": BUTTER, "shoes": BUTTER, "hair": BUTTER},
                   hair_style=hair)
        out.append(group([figure(x - 3, y, h, facing=f, pose=pose, look=rim)], opacity=0.8, filter="url(#soft)"))
        out.append(figure(x, y, h, facing=f, pose=pose, look=Look(**dark, hair_style=hair, vest=(x == 1050))))
    return out


def build():
    d = defs()
    body = []
    body += sky()
    body += far_shore()
    body += plume()
    body += [group(arm(False, ARM_Y))]
    body += tower()
    body += descent()
    body += flames()
    body += ship()
    body += [group(arm(True, ARM_Y))]
    body += dunes()
    body += grass()
    body += workers()
    body.append(rect(0, 0, WIDTH, HEIGHT, fill="none", stroke=INK, stroke_width=60, opacity=0.4, filter="url(#soft)"))
    body.append(grain_overlay(opacity=0.3))
    title = "SpaceX catches Starship's upper stage with the launch tower's arms"
    desc = ("Editorial illustration, seen from low on the dunes at SpaceX's Starbase site on the Texas Gulf Coast. "
            "A tall lattice launch tower rises on the right; its two long mechanical arms close around a "
            "stainless-steel Starship upper stage, dark heat-shield tiles on one side, as it descends tail-first on "
            "short landing-burn flames, its dotted return path arcing down from the sky, with steam billowing off the pad below. Behind it a huge pale sun is circled by "
            "faint orbit rings, an illustrative nod to its 14 orbits. In the foreground, silhouetted workers raise "
            "their arms and cheer. It represents SpaceX's first catch of the Starship upper stage on Nov. 14, 2026, "
            "after Flight 15.")
    return document(d, body, title, desc)


if __name__ == "__main__":
    save(build(), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
