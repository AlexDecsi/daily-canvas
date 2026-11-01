"""Daily artwork, 2026-10-31: Virginia and D.C. sue to block Trump's planned arch.

Visual idea: the 250-foot arch that does not exist yet looms over Memorial Circle
as a giant glowing blueprint ghost, dwarfing the real Arlington Memorial Bridge
and Lincoln Memorial, while two small suited figures in the foreground hold up a
thick bound lawsuit against it: paper versus a phantom monument.

Verified (brief): on Oct. 31 Virginia AG Jay Jones and D.C. AG Brian Schwalb sued
in federal court to stop the arch, the third lawsuit against it (AP via PBS/CBS;
NBC). Plans: about 250 ft on a grassy site at Memorial Circle, off the bridge to
Arlington National Cemetery, topped by a winged bronze Lady Liberty with a torch.
The states cite traffic on the circle. Construction could start next week.
Drawn: the arch only as a dashed blueprint outline (it is unbuilt); the real
setting (Memorial Bridge's low granite arches, the Potomac, the Lincoln Memorial
and Washington Monument across the river); ordinary cars on the circle; two
generic suited figures holding a blank bound complaint, symbolizing the filing.
Not drawn: no likenesses, names, text, signs, protesters, crowds, construction
equipment, or any outcome of the case.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-10-31"
R = rng(20261031)
NAVY, COBALT, PERI, HAZE = "#16285c", "#2b4c9b", "#7f9fdc", "#c9d6f0"
GHOST, GHOST2 = "#dffaff", "#7fe3ff"
MARBLE, MARBLE2, MARBLE3 = "#f3ecdc", "#ddd1b8", "#b9ab8e"
RIVER, RIVER2 = "#3d5f8f", "#2a456f"
GRASS, GRASS2 = "#4f8a52", "#3a6b44"
LEAF, LEAF2, LEAF3 = "#e8762e", "#f2a33a", "#c4462a"
ASPHALT = "#2c2f3d"
RED = "#d8382f"
INK = "#14183a"

DECK_Y = 560           # bridge deck / far bank level
WATER_TOP, WATER_BOT = 575, 690
ARCH_CX, ARCH_BASE = 900, 668


def sky():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#sky)")]
    out.append(rect(0, 0, WIDTH, 560, fill="url(#skydots)", opacity=0.12))
    out.append(ellipse(ARCH_CX, 360, 470, 430, fill="url(#ghostglow)"))
    out.append(ellipse(-40, 560, 520, 260, fill="url(#sun)"))  # low late-afternoon sun to the west-left
    out.append(circle(40, 520, 46, fill="#ffd9a0", opacity=0.9))  # the blueprint's own glow
    return out


def far_bank():
    """Washington side across the Potomac: Lincoln Memorial and the Washington Monument."""
    out = [rect(0, DECK_Y - 30, 700, 50, fill="#5d7fb5")]
    # Washington Monument, far away, hazy
    out.append(poly([(588, DECK_Y - 30), (604, DECK_Y - 30), (601, 250), (591, 250)], fill=HAZE, opacity=0.85))
    out.append(poly([(591, 250), (601, 250), (596, 236)], fill=HAZE, opacity=0.85))
    out.append(rect(591, 250, 10, 70, fill="#ffffff", opacity=0.25))
    # Lincoln Memorial: stepped base, colonnade, attic
    lx, ly, lw = 420, DECK_Y - 30, 200
    out.append(rect(lx - 20, ly - 22, lw + 40, 22, fill=MARBLE2))
    out.append(rect(lx - 10, ly - 30, lw + 20, 8, fill=MARBLE))
    out.append(rect(lx, ly - 100, lw, 70, fill=MARBLE3))
    for i in range(12):
        out.append(rect(lx + 6 + i * 17.5, ly - 96, 8, 66, fill=MARBLE))
    out.append(rect(lx - 6, ly - 116, lw + 12, 16, fill=MARBLE))
    out.append(rect(lx + 8, ly - 132, lw - 16, 16, fill=MARBLE2))
    # autumn trees along the far bank
    for x in range(-10, 700, 34):
        if 390 < x < 640:
            continue
        out += cloud_puffs(R, x, DECK_Y - 40, 40, 16, 3, 10, 18, fill=R.choice([LEAF, LEAF2, LEAF3, "#8a9a52"]))
    return out


def bridge():
    """Arlington Memorial Bridge: a long, low granite bridge of shallow arches."""
    out = []
    deck_top = DECK_Y - 6
    out.append(rect(-10, deck_top, 760, 22, fill=MARBLE))
    out.append(rect(-10, deck_top + 22, 760, 6, fill=MARBLE3))
    for i in range(30):  # balustrade
        out.append(rect(4 + i * 25, deck_top - 12, 4, 12, fill=MARBLE2))
    out.append(rect(-10, deck_top - 15, 760, 4, fill=MARBLE))
    for i in range(6):  # low arches with piers
        x0 = -10 + i * 128
        out.append(path(f"M{x0} {deck_top + 28} L{x0 + 128} {deck_top + 28} L{x0 + 128} {WATER_TOP + 38} "
                        f"L{x0 + 114} {WATER_TOP + 38} Q{x0 + 64} {deck_top + 30} {x0 + 14} {WATER_TOP + 38} "
                        f"L{x0} {WATER_TOP + 38} Z", fill=MARBLE2))
        out.append(rect(x0 - 4, deck_top + 28, 22, WATER_TOP + 40 - deck_top - 28, fill=MARBLE))
    for i in range(7):  # lamp posts
        x = 30 + i * 110
        out += [rect(x, deck_top - 40, 2.5, 28, fill=INK), circle(x + 1.2, deck_top - 42, 3.5, fill="#ffe7a8")]
    return out


def river():
    out = [rect(0, WATER_TOP, WIDTH, WATER_BOT - WATER_TOP + 40, fill="url(#river)")]
    for k in range(14):
        y = WATER_TOP + 50 + k * 6
        out.append(rect(R.uniform(0, 1100), y, R.uniform(40, 140), 2, fill=HAZE, opacity=0.35))
    # reflection of the ghost arch in the water
    out.append(rect(ARCH_CX - 200, WATER_TOP + 40, 400, 70, fill=GHOST2, opacity=0.12))
    for k in range(6):
        out.append(rect(ARCH_CX - 180 + R.uniform(-10, 10), WATER_TOP + 48 + k * 10, 360 - k * 40, 2,
                        fill=GHOST, opacity=0.45 - k * 0.06))
    return out


def island():
    """Columbia Island / Memorial Circle on the Virginia side, with the traffic circle."""
    out = [path(f"M700 {DECK_Y + 10} Q900 {DECK_Y - 8} 1220 {DECK_Y + 6} L1220 {ARCH_BASE + 30} L640 {ARCH_BASE + 30} Z",
                fill=GRASS)]
    out.append(ellipse(ARCH_CX, ARCH_BASE + 4, 320, 30, fill=GRASS2))
    for x in range(1040, 1230, 30):
        out += cloud_puffs(R, x, DECK_Y - 6, 36, 20, 3, 10, 20, fill=R.choice([LEAF, LEAF2, LEAF3]))
    return out


def ghost_arch():
    """The proposed arch as a translucent blueprint: single great opening, attic, statue on top."""
    cx, by = ARCH_CX, ARCH_BASE
    w, top = 400, 215
    x0, x1 = cx - w / 2, cx + w / 2
    line = dict(fill="none", stroke=GHOST, stroke_width=3, stroke_dasharray="14 7")
    thin = dict(fill="none", stroke=GHOST2, stroke_width=1.4, stroke_dasharray="6 6", opacity=0.8)
    body = (f"M{x0} {by} L{x0} {top} L{x1} {top} L{x1} {by} L{cx + 85} {by} L{cx + 85} {by - 250} "
            f"A85 85 0 0 0 {cx - 85} {by - 250} L{cx - 85} {by} Z")
    out = [path(body, fill="url(#blueprint)", opacity=0.9), path(body, fill=GHOST2, opacity=0.12)]
    out.append(path(body, **line))
    # cornice and attic bands
    for y in (top + 60, top + 76):
        out.append(path(f"M{x0 - 14} {y} L{x1 + 14} {y}", **line))
    out.append(path(f"M{x0 - 14} {top} L{x1 + 14} {top} L{x1 + 14} {top + 14} L{x0 - 14} {top + 14} Z", **line))
    # paired columns on each pier
    for side in (-1, 1):
        for dx in (150, 120):
            x = cx + side * dx
            out.append(path(f"M{x - 7} {by} L{x - 7} {top + 90} M{x + 7} {by} L{x + 7} {top + 90}", **thin))
    # construction grid inside the opening and dimension line on the right
    out.append(path(f"M{cx - 10} {by - 335} L{cx} {by - 352} L{cx + 10} {by - 335} Z", **line))  # keystone
    for side in (-1, 1):  # relief panels in the attic and above the side piers
        out.append(rect(cx + side * 135 - 40, top + 22, 80, 30, **thin))
        out.append(rect(cx + side * 135 - 35, top + 100, 70, 120, **thin))
    out.append(path(f"M{x0 - 30} {by + 4} L{x1 + 30} {by + 4}", **line))
    out.append(path(f"M{x1 + 50} {by} L{x1 + 50} 48", fill="none", stroke=GHOST, stroke_width=2))
    for y in (by, 48):
        out.append(path(f"M{x1 + 38} {y} L{x1 + 62} {y}", stroke=GHOST, stroke_width=2))
    for k in range(1, 10):
        y = by - k * (by - 48) / 10
        out.append(path(f"M{x1 + 44} {y:.0f} L{x1 + 56} {y:.0f}", stroke=GHOST, stroke_width=1.2, opacity=0.8))
    out += statue(cx, top)

    return out


def statue(cx, top):
    """Winged Lady Liberty holding a torch, as a dashed blueprint outline."""
    line = dict(fill=GHOST2, fill_opacity=0.18, stroke=GHOST, stroke_width=2.5, stroke_dasharray="9 5")
    out = [path(f"M{cx - 40} {top} L{cx + 40} {top} L{cx + 32} {top - 18} L{cx - 32} {top - 18} Z", **line)]  # plinth
    out.append(path(f"M{cx - 16} {top - 18} Q{cx - 18} {top - 70} {cx - 8} {top - 100} L{cx + 8} {top - 100} "
                    f"Q{cx + 18} {top - 70} {cx + 16} {top - 18} Z", **line))  # robed body
    out.append(circle(cx, top - 110, 10, **line))  # head
    for side in (-1, 1):  # wings
        out.append(path(f"M{cx + side * 8} {top - 92} Q{cx + side * 70} {top - 140} {cx + side * 96} {top - 104} "
                        f"Q{cx + side * 64} {top - 98} {cx + side * 78} {top - 74} Q{cx + side * 44} {top - 78} "
                        f"{cx + side * 12} {top - 60} Z", **line))
    out.append(path(f"M{cx + 8} {top - 96} L{cx + 22} {top - 140}", stroke=GHOST, stroke_width=4))  # raised arm
    out.append(path(f"M{cx + 16} {top - 140} L{cx + 30} {top - 140} L{cx + 25} {top - 150} L{cx + 21} {top - 150} Z",
                    **line))
    out.append(circle(cx + 23, top - 160, 22, fill="url(#flame)"))  # flame glow
    out.append(path(f"M{cx + 23} {top - 150} Q{cx + 15} {top - 162} {cx + 23} {top - 176} Q{cx + 31} {top - 162} "
                    f"{cx + 23} {top - 150} Z", fill="#ffd36b", opacity=0.85))
    return out


def spill():
    """Cold blueprint light spilling down from the phantom arch onto the traffic circle."""
    x0, x1, by = ARCH_CX - 200, ARCH_CX + 200, ARCH_BASE
    return [poly([(x0 + 30, by - 6), (x1 - 30, by - 6), (x1 + 170, by + 150), (x0 - 170, by + 150)],
                 fill="url(#spill)", style="mix-blend-mode:screen")]


def road():
    """The traffic circle sweeping across the foreground, with ordinary cars."""
    out = [path(f"M-20 {ARCH_BASE + 20} Q600 {ARCH_BASE - 10} 1220 {ARCH_BASE + 30} L1220 {ARCH_BASE + 110} "
                f"Q600 {ARCH_BASE + 80} -20 {ARCH_BASE + 110} Z", fill=ASPHALT)]
    for k in range(16):
        x = 20 + k * 78
        out.append(rect(x, ARCH_BASE + 58 + 0.000004 * (x - 600) ** 2 * 6, 36, 3, fill="#f2e6b8", opacity=0.75))
    cars = [(140, "#e2c044", 1), (420, "#e9e4dc", -1), (700, RED, 1), (1010, "#6aa0c9", -1)]
    for x, col, d in cars:
        y = ARCH_BASE + (48 if d == 1 else 86)
        out += [path(f"M{x - 40} {y} L{x - 36} {y - 16} L{x - 18} {y - 18} L{x - 8} {y - 30} L{x + 22} {y - 30} "
                     f"L{x + 34} {y - 17} L{x + 42} {y - 14} L{x + 42} {y} Z", fill=col),
                path(f"M{x - 5} {y - 27} L{x + 8} {y - 27} L{x + 8} {y - 18} L{x - 14} {y - 18} Z", fill=HAZE),
                path(f"M{x + 11} {y - 27} L{x + 21} {y - 27} L{x + 30} {y - 18} L{x + 11} {y - 18} Z", fill=HAZE),
                circle(x - 22, y, 7, fill=INK), circle(x + 26, y, 7, fill=INK),
                rect(x - 42 if d == 1 else x + 38, y - 14, 5, 4, fill="#ff5a4a")]
    return out


def foreground():
    out = [path(f"M-20 {ARCH_BASE + 104} Q600 {ARCH_BASE + 74} 1220 {ARCH_BASE + 104} L1220 {HEIGHT} L-20 {HEIGHT} Z",
                fill="url(#lawn)")]
    for _ in range(40):  # fallen leaves
        x, y = R.uniform(0, WIDTH), R.uniform(ARCH_BASE + 110, HEIGHT)
        out.append(ellipse(x, y, 5, 2.5, fill=R.choice([LEAF, LEAF2, LEAF3]), opacity=0.9,
                           transform=f"rotate({R.uniform(0, 180):.0f} {x:.0f} {y:.0f})"))
    return out


def complaint():
    """A thick bound legal complaint, blank: red cover, cream page edges."""
    return group([rect(-14, -40, 34, 44, fill="#efe6d2", stroke=MARBLE3, stroke_width=0.6),
                  *[path(f"M-13 {-36 + k * 4} L19 {-36 + k * 4}", stroke=MARBLE3, stroke_width=0.4) for k in range(10)],
                  rect(-17, -44, 34, 44, fill=RED), rect(-17, -44, 5, 44, fill="#9e221c"),
                  rect(-9, -30, 20, 2, fill="#f6d9c8", opacity=0.6)], transform="rotate(-8)")


def officials():
    gy = HEIGHT - 36
    # long shadows stretch away from the low sun, toward the phantom arch
    out = [poly([(205, gy + 4), (300, gy + 4), (760, gy - 62), (700, gy - 74)], fill=INK, opacity=0.28),
           poly([(345, gy + 10), (445, gy + 10), (900, gy - 52), (850, gy - 64)], fill=INK, opacity=0.24),
           ellipse(250, gy - 170, 150, 220, fill="url(#sun)", opacity=0.35)]  # warm light wrapping the figures
    a = Look(skin="#a86f4c", top="#1e2a4a", bottom="#1e2a4a", hair="#1e1512", accent=RED, long_tie=True,
             coat=True, build=1.1, face="stern")
    out.append(figure(240, gy, 300, 1, Pose(back_arm=(-10, 10), front_arm=(150, -10), back_leg=(-10, 0),
                                              front_leg=(12, 0), lean=-4, head_tilt=-12),
                      a, hand_items={"front": complaint()}))
    b = Look(skin="#f1c7a5", top="#3a3f52", bottom="#2b2b38", hair="#6b4a2e", accent="#7fa6d9", long_tie=True,
             build=1.05, face="neutral")
    out.append(figure(395, gy + 10, 285, 1, Pose(back_arm=(-15, 15), front_arm=(95, 0), back_leg=(-14, -6),
                                                   front_leg=(16, -2), lean=2, head_tilt=-8), b))
    return out


def framing():
    """An autumn oak at the right edge frames the scene."""
    out = [path("M1180 900 Q1160 600 1200 300 L1240 300 L1240 900 Z", fill="#3b2a2a")]
    out += cloud_puffs(R, 1190, 170, 140, 160, 18, 30, 60, fill=LEAF3)
    out += cloud_puffs(R, 1170, 150, 110, 120, 12, 24, 44, fill=LEAF)
    return out


defs = [grain_filter(),
        linear("sky", [(0, NAVY), (0.45, COBALT), (0.85, PERI), (1, HAZE)]),
        radial("ghostglow", [(0, GHOST2, 0.5), (0.5, GHOST2, 0.18), (1, GHOST2, 0)]),
        radial("sun", [(0, "#ffb870", 0.75), (1, "#ffb870", 0)]),
        linear("spill", [(0, GHOST2, 0.3), (1, GHOST2, 0)]),
        radial("flame", [(0, "#ffe9a8", 0.9), (1, "#ffb84d", 0)]),
        linear("river", [(0, RIVER), (1, RIVER2)]),
        linear("lawn", [(0, GRASS), (1, GRASS2)]),
        halftone("skydots", "#ffffff", dot=1.3, spacing=9),
        el("pattern", path("M0 0 L24 0 M0 0 L0 24", stroke=GHOST2, stroke_width=1, opacity=0.75),
           id="blueprint", width=24, height=24, patternUnits="userSpaceOnUse")]
body = (sky() + far_bank() + river() + bridge() + island() + ghost_arch() + road() + foreground() + spill()
        + officials() + framing() + [grain_overlay(opacity=0.3)])

save(document(defs, body,
              "Virginia and D.C. sue to block Trump's planned arch",
              "Graphic poster illustration: the proposed 250-foot arch at Memorial Circle, which has not been built, "
              "is drawn as a glowing, dashed blueprint outline topped by a winged Lady Liberty holding a torch. It "
              "towers over the low granite arches of Arlington Memorial Bridge, the Potomac River, and the Lincoln "
              "Memorial and Washington Monument across the water, with ordinary cars on the traffic circle. In the "
              "foreground two generic figures in suits, standing for the Virginia and D.C. attorneys general, hold up "
              "a thick red-bound legal complaint toward it. No text."),
     Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
