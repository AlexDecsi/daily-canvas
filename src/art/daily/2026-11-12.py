"""Daily artwork, 2026-11-12: Jensen Huang resigns as Nvidia CEO.

Visual idea: the empty keynote. Seen from low in a dark, empty auditorium, a single
spotlight falls on a bare stool with a black leather jacket left draped over it, while
behind it a colossal glowing graphics chip rises like a green sun on the stage screen,
its circuit traces radiating outward and a red share-price line slashing down across it
and climbing only part of the way back.

Verified (brief): on Nov. 12, 2026 Nvidia announced that Huang had stepped down as CEO
and from the board, effective immediately; CFO Colette Kress became interim CEO; the
shares fell as much as 14% and closed down about 4.3% (AP via NBC Boston, CBS, CNBC).
Drawn: an empty stage, stool and a generic black leather jacket (his widely documented
signature clothing) as illustrative symbolism; a generic chip; an unlabeled price line.
Not drawn: Huang himself, any other person, any allegation, logos, numbers or text.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403

DATE = "2026-11-12"
R = rng(20261112)

# palette: stage black, circuit green, spotlight cream, market red, steel
BLACK, BLACK2, BLACK3 = "#07090a", "#0e1412", "#161d1b"
GREEN, GREEN2, GREEN3, GREEN4 = "#b6f25a", "#76c42a", "#2f6a1c", "#12301a"
CREAM, CREAM2 = "#fff4d6", "#f3d9a0"
RED, RED2 = "#ff4a3d", "#b8231b"
STEEL, STEEL2, STEEL3 = "#4a5157", "#2c3237", "#1b1f23"
LEATHER, LEATHER2, SHEEN = "#141414", "#262626", "#9aa3a8"

CX, CY = 600, 290  # chip centre on the screen


def defs():
    return [
        linear("hall", [(0, BLACK2), (1, BLACK)]),
        linear("screen", [(0, "#0a1a10"), (0.6, GREEN4), (1, "#0b140e")]),
        radial("chipglow", [(0, GREEN, 0.9), (0.35, GREEN2, 0.45), (1, GREEN3, 0)]),
        radial("pool", [(0, CREAM, 0.85), (0.55, CREAM2, 0.35), (1, CREAM2, 0)]),
        linear("beam", [(0, CREAM, 0.0), (0.25, CREAM, 0.16), (1, CREAM2, 0.34)]),
        linear("stage", [(0, STEEL3), (1, BLACK)]),
        linear("die", [(0, "#d6ff8a"), (0.5, GREEN), (1, GREEN2)], x2=1, y2=1),
        linear("seat", [(0, STEEL2), (1, BLACK)]),
        blur("soft", 16),
        blur("softer", 5),
        halftone("dots", GREEN3, dot=1.5, spacing=7),
        halftone("dotsr", CREAM2, dot=1.1, spacing=6),
        el("clipPath", rect(70, 40, 1060, 520, rx=6), id="scr"),
        grain_filter(),
    ]


# ---------------------------------------------------------------- background
def hall():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#hall)")]
    # stage screen
    out.append(rect(70, 40, 1060, 520, rx=6, fill="url(#screen)"))
    out.append(rect(70, 40, 1060, 520, rx=6, fill="url(#dots)", opacity=0.45))
    return out


def traces():
    """Circuit traces radiating from the chip like sun rays: orthogonal runs with pads."""
    out = []
    r = R
    for i in range(46):
        ang = (i / 46) * 2 * math.pi + r.uniform(-0.05, 0.05)
        start = 150 + r.uniform(0, 10)
        x0, y0 = CX + math.cos(ang) * start, CY + math.sin(ang) * start
        length = r.uniform(170, 460)
        # first leg along the ray, then a 45-degree jog, then straight
        x1, y1 = CX + math.cos(ang) * (start + length * 0.45), CY + math.sin(ang) * (start + length * 0.45)
        jog = r.choice((-1, 1)) * 0.6
        a2 = ang + jog * 0.5
        x2, y2 = x1 + math.cos(a2) * length * 0.25, y1 + math.sin(a2) * length * 0.25
        x3, y3 = x2 + math.cos(ang) * length * 0.3, y2 + math.sin(ang) * length * 0.3
        # clip to screen
        x3 = max(80, min(1120, x3)); y3 = max(50, min(550, y3))
        col = GREEN if i % 3 == 0 else GREEN2
        w = 3.2 if i % 3 == 0 else 2
        out.append(path(f"M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f} L{x3:.0f} {y3:.0f}",
                        fill="none", stroke=col, stroke_width=w, opacity=0.75, stroke_linejoin="round"))
        out.append(circle(x3, y3, 5 if i % 3 == 0 else 3.5, fill="none", stroke=col, stroke_width=2, opacity=0.85))
    return out


def chip():
    out = [circle(CX, CY, 330, fill="url(#chipglow)")]
    s = 250
    x, y = CX - s / 2, CY - s / 2
    # pins
    for k in range(14):
        t = x + 18 + k * (s - 36) / 13
        for (px, py, w, h) in ((t - 4, y - 22, 8, 22), (t - 4, y + s, 8, 22)):
            out.append(rect(px, py, w, h, rx=2, fill=CREAM2, opacity=0.9))
        tt = y + 18 + k * (s - 36) / 13
        for (px, py, w, h) in ((x - 22, tt - 4, 22, 8), (x + s, tt - 4, 22, 8)):
            out.append(rect(px, py, w, h, rx=2, fill=CREAM2, opacity=0.9))
    # package and die
    out.append(rect(x, y, s, s, rx=14, fill=GREEN4, stroke=GREEN2, stroke_width=4))
    out.append(rect(x + 40, y + 40, s - 80, s - 80, rx=6, fill="url(#die)"))
    # die grid
    for k in range(1, 6):
        g = x + 40 + k * (s - 80) / 6
        out.append(path(f"M{g:.0f} {y + 44} L{g:.0f} {y + s - 44}", stroke=GREEN3, stroke_width=1.6, opacity=0.6))
        g = y + 40 + k * (s - 80) / 6
        out.append(path(f"M{x + 44} {g:.0f} L{x + s - 44} {g:.0f}", stroke=GREEN3, stroke_width=1.6, opacity=0.6))
    out.append(rect(x + 40, y + 40, s - 80, s - 80, rx=6, fill="none", stroke="#eaffc4", stroke_width=2, opacity=0.8))
    return out


def price_line():
    """Unlabeled share-price trace: steady, a steep plunge, a partial climb back."""
    pts = []
    x = 90
    y = 175
    r = R
    while x < 470:
        pts.append((x, y + r.uniform(-10, 10)))
        x += 22
    # plunge (as much as 14%)
    pts += [(488, 205), (500, 260), (512, 320), (524, 372), (538, 404), (552, 392)]
    # recovery, about two-thirds of the way back
    x, y = 574, 396
    while x < 1110:
        y -= r.uniform(4, 13)
        y = max(y, 262)
        pts.append((x, y + r.uniform(-8, 8)))
        x += 24
    d = "M" + " L".join(f"{px:.0f} {py:.0f}" for px, py in pts)
    return [
        path(d, fill="none", stroke=RED, stroke_width=22, opacity=0.35, filter="url(#softer)", stroke_linejoin="round"),
        path(d, fill="none", stroke=RED, stroke_width=8, stroke_linejoin="round", stroke_linecap="round"),
        path(d, fill="none", stroke="#ffd2c8", stroke_width=2, stroke_linejoin="round", opacity=0.8),
    ]


# ---------------------------------------------------------------- stage
def stage():
    out = []
    # stage floor (perspective trapezoid) and lip
    out.append(path("M0 600 L1200 600 L1200 790 L0 790 Z", fill="url(#stage)"))
    out.append(path("M0 560 L1200 560 L1200 600 L0 600 Z", fill=BLACK3))
    # floor boards in perspective
    for k in range(-12, 13):
        out.append(path(f"M{600 + k * 40} 600 L{600 + k * 110} 790", stroke=STEEL2, stroke_width=1.5, opacity=0.5))
    # reflection of the screen glow
    out.append(ellipse(600, 615, 520, 26, fill=GREEN2, opacity=0.18, filter="url(#soft)"))
    out.append(path("M0 790 L1200 790 L1200 812 L0 812 Z", fill=STEEL3))
    out.append(path("M0 790 L1200 790", stroke=STEEL, stroke_width=2))
    # side speaker stacks / truss towers
    for sx in (24, 1086):
        out.append(rect(sx, 120, 90, 470, fill=BLACK, stroke=STEEL2, stroke_width=3))
        for k in range(6):
            cy = 170 + k * 74
            out.append(circle(sx + 45, cy, 26, fill=BLACK3, stroke=STEEL2, stroke_width=3))
            out.append(circle(sx + 45, cy, 9, fill=STEEL2))
    return out


def spotlight():
    out = []
    # beam from a lamp above the frame
    beam = "M566 -10 L634 -10 L826 700 A226 40 0 0 1 374 700 Z"
    out.append(path(beam, fill="url(#beam)"))
    out.append(ellipse(600, 700, 250, 50, fill="url(#pool)"))
    out.append(path(beam, fill="url(#dotsr)", opacity=0.22))
    return out


def stool_and_jacket():
    out = []
    # long shadow thrown forward toward the empty seats
    out.append(path("M540 712 L660 712 L760 790 L440 790 Z", fill=BLACK, opacity=0.55, filter="url(#softer)"))
    # stool: four legs, foot ring, seat, two back uprights and a top rail
    for (x0, x1) in ((548, 516), (652, 684), (578, 570), (622, 630)):
        out.append(path(f"M{x0} 612 L{x1} 716", stroke=STEEL, stroke_width=8, stroke_linecap="round"))
    out.append(ellipse(600, 676, 60, 10, fill="none", stroke=STEEL, stroke_width=5))
    out.append(ellipse(600, 614, 82, 17, fill=STEEL2))
    out.append(ellipse(600, 609, 82, 16, fill=STEEL))
    out.append(ellipse(600, 607, 70, 11, fill="#6b747b"))
    for ux in (536, 664):
        out.append(path(f"M{ux} 606 L{ux} 452", stroke=STEEL, stroke_width=8, stroke_linecap="round"))
    out.append(path("M528 452 L672 452", stroke=STEEL, stroke_width=12, stroke_linecap="round"))

    # black leather jacket hung by its shoulders on the back rail, front open toward us
    j = []
    # sleeves (behind the body), hanging and slightly splayed
    j.append(path("M478 470 Q458 540 462 650 Q474 662 494 656 Q496 570 512 500 Z", fill=LEATHER))
    j.append(path("M722 470 Q742 540 738 650 Q726 662 706 656 Q704 570 688 500 Z", fill=LEATHER))
    j.append(path("M462 650 Q474 662 494 656 L494 640 Q476 646 463 636 Z", fill=LEATHER2))  # cuffs
    j.append(path("M738 650 Q726 662 706 656 L706 640 Q724 646 737 636 Z", fill=LEATHER2))
    # body: shoulders over the rail, hem at the seat
    j.append(path("M486 462 Q540 440 600 444 Q660 440 714 462 L708 620 Q600 636 492 620 Z", fill=LEATHER))
    # inner lining visible through the open front (dark, hanging over the seat)
    j.append(path("M566 452 L634 452 L628 624 Q600 630 572 624 Z", fill="#050505"))
    # left and right front panels with lapels and collar
    j.append(path("M520 452 L566 452 L582 508 L572 624 Q530 622 494 618 L496 480 Z", fill=LEATHER2))
    j.append(path("M680 452 L634 452 L618 508 L628 624 Q670 622 706 618 L704 480 Z", fill=LEATHER2))
    j.append(path("M548 446 L574 446 L592 500 L566 520 Z", fill=LEATHER))  # left lapel
    j.append(path("M652 446 L626 446 L608 500 L634 520 Z", fill=LEATHER))  # right lapel
    j.append(path("M540 440 Q600 424 660 440 L652 450 Q600 438 548 450 Z", fill="#1d1d1d"))  # collar
    # zips, pockets, waistband
    j.append(path("M572 520 L572 622 M628 520 L628 622", stroke=SHEEN, stroke_width=2.4, opacity=0.85))
    j.append(path("M514 560 L540 548 M686 560 L660 548", stroke=SHEEN, stroke_width=2.4, opacity=0.7,
                  stroke_linecap="round"))
    j.append(path("M494 606 Q530 612 572 612 M628 612 Q670 612 706 606", stroke="#000", stroke_width=6, fill="none"))
    # spotlight sheen on the leather (rim light from above)
    for d in ("M492 468 Q540 448 584 452", "M708 468 Q660 448 616 452", "M480 486 Q468 560 470 640",
              "M720 486 Q732 560 730 640", "M506 496 Q502 560 504 610", "M694 496 Q698 560 696 610",
              "M552 470 Q560 500 556 540"):
        j.append(path(d, stroke=SHEEN, stroke_width=3.4, fill="none", opacity=0.6, stroke_linecap="round"))
    for d in ("M498 470 Q540 452 576 456", "M702 470 Q660 452 624 456"):
        j.append(path(d, stroke=CREAM, stroke_width=1.6, fill="none", opacity=0.8, stroke_linecap="round"))
    out.append(group(j))
    # rail ends visible past the shoulders
    out.append(path("M526 452 L536 452 M664 452 L674 452", stroke="#6b747b", stroke_width=12, stroke_linecap="round"))
    return out


def extras():
    out = []
    # glossy floor: faint reflections of the red line's glow and the jacket
    out.append(ellipse(600, 742, 120, 10, fill=RED, opacity=0.18, filter="url(#softer)"))
    out.append(path("M496 722 Q600 734 704 722 L690 760 Q600 768 510 760 Z", fill=LEATHER2, opacity=0.35,
                    filter="url(#softer)"))
    # dust motes / haze in the beam
    for _ in range(70):
        t = R.uniform(0.05, 0.95)
        half = 34 + t * 190
        x = 600 + R.uniform(-half, half) * 0.9
        y = -10 + t * 700
        out.append(circle(x, y, R.uniform(0.8, 2.2), fill=CREAM, opacity=round(R.uniform(0.25, 0.7), 2)))
    # footlights along the stage lip, glowing up
    for k in range(9):
        fx = 150 + k * 112.5
        out.append(ellipse(fx, 790, 46, 16, fill=CREAM2, opacity=0.22, filter="url(#softer)"))
        out.append(rect(fx - 22, 786, 44, 10, rx=3, fill=STEEL2))
        out.append(rect(fx - 16, 786, 32, 4, rx=2, fill=CREAM, opacity=0.9))
    return out


def seat_lip():
    return [path("M518 612 Q600 634 682 612 L682 618 Q600 642 518 618 Z", fill="#6b747b"),
            path("M520 612 Q600 632 680 612", stroke=CREAM, stroke_width=1.5, fill="none", opacity=0.6)]


def audience():
    """Rows of empty seat backs in the foreground, rim-lit by the spotlight."""
    out = [rect(0, 812, WIDTH, 90, fill=BLACK)]
    for row, (y, w, h) in enumerate(((800, 78, 56), (842, 96, 70))):
        n = int(WIDTH / w) + 2
        off = (row % 2) * w / 2
        for k in range(n):
            x = -w + off + k * w
            out.append(path(f"M{x + 6} {y + h} L{x + 6} {y + 16} Q{x + 6} {y} {x + w / 2} {y} "
                            f"Q{x + w - 6} {y} {x + w - 6} {y + 16} L{x + w - 6} {y + h} Z",
                            fill="url(#seat)", stroke=BLACK, stroke_width=3))
            # rim light, stronger near the centre beam
            dist = abs(x + w / 2 - 600)
            op = max(0.08, 0.6 - dist / 900)
            out.append(path(f"M{x + 12} {y + 14} Q{x + 12} {y + 5} {x + w / 2} {y + 4} Q{x + w - 12} {y + 5} {x + w - 12} {y + 14}",
                            fill="none", stroke=CREAM2, stroke_width=2.5, opacity=round(op, 2)))
    return out


def build():
    d = defs()
    body = []
    body += hall()
    body.append(group(traces(), clip_path="url(#scr)"))
    body += chip()
    body += price_line()
    body += stage()
    body += spotlight()
    body += stool_and_jacket()
    body += seat_lip()
    body += extras()
    body += audience()
    body.append(rect(0, 0, WIDTH, HEIGHT, fill="none", stroke=BLACK, stroke_width=70, opacity=0.5, filter="url(#soft)"))
    body.append(grain_overlay(opacity=0.3))
    title = "Jensen Huang resigns as Nvidia CEO"
    desc = ("Editorial illustration. Seen from the empty seats of a dark auditorium, a single spotlight falls on a "
            "bare stool on an empty stage, with a black leather jacket left draped over it. Behind, a giant "
            "glowing green computer chip fills the stage screen, its circuit traces radiating outward, while a "
            "red share-price line plunges and climbs only part of the way back. It represents Jensen Huang's "
            "resignation as Nvidia's chief executive on Nov. 12, 2026, and the day's swing in the company's stock.")
    return document(d, body, title, desc)


if __name__ == "__main__":
    save(build(), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
