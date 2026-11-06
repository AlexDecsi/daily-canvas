"""Daily artwork, 2026-11-05: Newsom commutes California's death sentences.

Visual idea: over the governor's shoulder at dusk. In the dark office he signs a
single letter in a pool of lamplight; beside him a tower of case folders rises
far above the desk (dramatic scale for 548 cases), and through a tall window the
long cell blocks of a distant prison sit under a rose-and-amber sky, their 548
tiny windows glowing like a field of small lights. Window light rakes across
the desk in long lattice shadows.

Verified (brief): on Nov. 5, 2026, Gov. Gavin Newsom reduced all 548 California
death sentences to life without parole, announced in an open letter to
Californians (NYT via Boston Globe; PBS NewsHour; NBC News). Some cases need
state Supreme Court review.
Drawn: Newsom from behind only (slicked-back dark hair greying at the temples,
navy suit), signing a blank-lined letter: an editorial staging of issuing the
letter, in an unspecified office. The California bear flag (bear, star, red
band; no lettering). The prison is generic, not a specific facility; the folder
tower is a symbol for the 548 cases.
Not drawn: no face, no readable text or signature, no inmates, no open cell
doors or releases, no execution imagery.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403

DATE = "2026-11-05"
R = rng(20261105)

WALL, WALL2 = "#0e2a2b", "#18403c"
VIOLET, ROSE, AMBER, GOLD, CREAM = "#3b1f4f", "#c4566a", "#f4a259", "#ffd77a", "#fbf0d8"
HILL, PRISON, PRISON2 = "#6a3358", "#2a1a36", "#3d2546"
WOOD, WOOD2, FRAME = "#5a2a1c", "#7d3f27", "#22140f"
NAVY, NAVY2 = "#16224a", "#0c1433"
HAIR, GREY, SKIN = "#3a2a22", "#a49a90", "#e0a888"
RED, BEAR = "#c8323a", "#6b4127"
MANILA, MANILA2 = "#e9c27a", "#c99a4f"
LAMPGREEN = "#1f7a55"

WX0, WX1, WY0, WY1 = 480, 1090, 40, 600     # window opening
HORIZON = 470


def window_scene():
    out = [rect(WX0, WY0, WX1 - WX0, WY1 - WY0, fill="url(#sky)")]
    out.append(circle(820, 455, 70, fill=GOLD, opacity=0.9))
    out.append(circle(820, 455, 130, fill="url(#sunglow)"))
    for a in range(-80, 81, 16):
        import math
        t = math.radians(a - 90)
        out.append(poly([(820, 455), (820 + 700 * math.cos(t - 0.04), 455 + 700 * math.sin(t - 0.04)),
                         (820 + 700 * math.cos(t + 0.04), 455 + 700 * math.sin(t + 0.04))], fill=GOLD, opacity=0.12))
    # distant hills
    out.append(path(f"M{WX0} 470 C 560 420 640 440 700 430 C 780 418 860 445 940 425 C 1010 410 1060 430 {WX1} 420 "
                     f"L{WX1} {WY1} L{WX0} {WY1} Z", fill=HILL))
    # back cell block (4 x 68 windows) and front block (4 x 69) = 548 lights
    blocks = [(520, 1060, 446, 498, PRISON2, 68), (500, 1075, 486, 548, PRISON, 69)]
    for x0, x1, y0, y1, col, cols in blocks:
        out.append(rect(x0, y0, x1 - x0, y1 - y0, fill=col))
        out.append(rect(x0, y0 - 6, x1 - x0, 6, fill=FRAME, opacity=0.6))
        sp = (x1 - x0 - 16) / cols
        rows = 4
        rh = (y1 - y0 - 14) / rows
        for r in range(rows):
            for c in range(cols):
                x = x0 + 8 + c * sp + sp * 0.25
                y = y0 + 7 + r * rh + rh * 0.25
                out.append(rect(round(x, 1), round(y, 1), round(sp * 0.5, 1), round(rh * 0.45, 1),
                                fill=GOLD if R.random() > 0.08 else AMBER))
    # guard tower
    out.append(rect(1012, 380, 22, 170, fill=PRISON))
    out.append(poly([(1000, 384), (1046, 384), (1040, 362), (1006, 362)], fill=PRISON))
    out.append(rect(1004, 366, 38, 10, fill=GOLD, opacity=0.8))
    # perimeter wall with fence and coiled wire
    out.append(rect(WX0, 548, WX1 - WX0, 52, fill="#1c1228"))
    for x in range(WX0 + 6, WX1, 34):
        out.append(rect(x, 520, 3, 30, fill="#1c1228"))
    out.append(rect(WX0, 524, WX1 - WX0, 2, fill="#1c1228"))
    for x in range(WX0 + 4, WX1, 12):
        out.append(circle(x, 519, 6, fill="none", stroke="#1c1228", stroke_width=1.6))
    return out


def window_frame():
    out = [group(window_scene(), clip_path="url(#win)")]
    # frame, mullions and transom
    out.append(rect(WX0 - 18, WY0 - 18, WX1 - WX0 + 36, WY1 - WY0 + 36, fill="none", stroke=FRAME, stroke_width=36))
    for x in (683, 887):
        out.append(rect(x - 7, WY0, 14, WY1 - WY0, fill=FRAME))
    out.append(rect(WX0, 300, WX1 - WX0, 14, fill=FRAME))
    out.append(rect(WX0 - 30, WY1 + 14, WX1 - WX0 + 60, 18, fill="#2e1a12"))  # sill
    return out


def flag():
    """California bear flag hanging from a pole, left of the window."""
    out = [rect(424, 40, 9, 560, fill="#b88a3e"), circle(428, 36, 10, fill=GOLD)]
    d = "M424 70 L250 74 C 244 160 256 250 246 330 L 300 360 L 352 326 L 424 352 Z"
    out.append(path(d, fill=CREAM))
    out.append(path("M246 300 L424 322 L424 352 L352 326 L300 360 L246 330 Z", fill=RED))
    out.append(poly([(286, 92), (291, 106), (306, 106), (294, 115), (298, 129), (286, 120), (274, 129), (278, 115),
                     (266, 106), (281, 106)], fill=RED))
    # walking bear (simple silhouette)
    out.append(path("M290 238 C 296 214 330 206 360 210 C 380 212 394 216 404 206 C 412 204 418 212 414 220 "
                    "C 410 228 404 232 404 244 L 406 272 L 394 272 L 390 252 L 360 254 L 356 274 L 344 274 "
                    "L 342 252 C 326 254 312 254 304 260 L 302 276 L 290 276 L 290 258 Z", fill=BEAR))
    out.append(circle(404, 207, 4, fill=BEAR))
    out.append(path("M300 248 L360 248 L404 220", fill="none", stroke="#8a5a36", stroke_width=2, opacity=0.6))
    # green ground strip under bear
    out.append(path("M262 280 L414 282", stroke="#4f7a3a", stroke_width=6, fill="none"))
    # folds
    for x in (290, 340, 390):
        out.append(path(f"M{x} 74 C {x - 6} 160 {x + 6} 250 {x - 4} 345", stroke="#000", stroke_opacity=0.12,
                        stroke_width=12, fill="none"))
    return out


def desk():
    out = [poly([(0, 640), (1200, 618), (1200, 900), (0, 900)], fill="url(#desk)")]
    out.append(poly([(0, 640), (1200, 618), (1200, 626), (0, 648)], fill=WOOD2))
    # window light raking toward the viewer, cut by mullion shadows
    beams = [(WX0, 683 - 7), (683 + 7, 887 - 7), (887 + 7, WX1)]
    for a, b in beams:
        out.append(poly([(a, 630), (b, 626), (b - 260, 900), (a - 360, 900)], fill=AMBER, opacity=0.16))
    out.append(poly([(560, 640), (1000, 634), (1040, 680), (520, 690)], fill=ROSE, opacity=0.18))
    # lamp glow pool
    out.append(ellipse(700, 760, 330, 120, fill="url(#pool)"))
    return out


def folders():
    """A tall, slightly leaning tower of case folders: a symbol for the 548 cases."""
    out = []
    y = 712
    x = 1040
    i = 0
    while y > -20:
        h = 7 + R.random() * 5
        w = 190 + R.random() * 22
        dx = R.uniform(-5, 5) - (712 - y) * 0.045
        col = MANILA if i % 3 else MANILA2
        out.append(rect(round(x - w / 2 + dx, 1), round(y - h, 1), round(w, 1), round(h, 1), fill=col))
        out.append(rect(round(x - w / 2 + dx, 1), round(y - h, 1), round(w, 1), 1.6, fill="#fff3d6", opacity=0.7))
        if i % 7 == 0:  # paper edge sticking out
            out.append(rect(round(x - w / 2 + dx + 14, 1), round(y - h + 2, 1), round(w - 30, 1), 2.4, fill=CREAM))
        y -= h
        i += 1
    # the tower's long shadow thrown across the desk by the window light
    shadow = poly([(940, 712), (1145, 712), (900, 900), (560, 900)], fill="#1a0c08", opacity=0.28)
    return [shadow] + out


def lamp():
    out = [ellipse(830, 700, 58, 14, fill="#8a6a2a"), rect(824, 610, 12, 90, fill="#c99a3e")]
    out.append(path("M735 612 C 760 572 900 572 925 612 Z", fill=LAMPGREEN))
    out.append(path("M735 612 C 760 600 900 600 925 612", fill="none", stroke="#0e3d2a", stroke_width=4))
    out.append(path("M748 600 C 780 584 880 584 912 600", fill="none", stroke="#6fd0a0", stroke_width=3, opacity=0.6))
    out.append(poly([(745, 614), (915, 614), (1010, 790), (650, 790)], fill="url(#cone)"))
    return out


def letter():
    pts = [(560, 700), (790, 690), (840, 840), (585, 856)]
    out = [poly([(p[0] + 8, p[1] + 10) for p in pts], fill="#000", opacity=0.25), poly(pts, fill=CREAM)]
    for k in range(9):
        t = 0.12 + k * 0.085
        x0 = 560 + (585 - 560) * t + 22
        y0 = 700 + (856 - 700) * t
        x1 = 790 + (840 - 790) * t - 26
        y1 = 690 + (840 - 690) * t
        out.append(path(f"M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}", stroke="#b9ad95", stroke_width=2.4, fill="none"))
    return out


def governor():
    out = []
    # body: navy suit back and shoulders, rising from the bottom-left
    out.append(path("M-20 900 L-10 700 C 10 630 90 600 170 592 L 330 592 C 400 600 440 630 470 680 "
                    "L 520 760 L 470 900 Z", fill=NAVY))
    out.append(path("M170 592 C 210 640 290 640 330 592", fill=NAVY2, opacity=0.6))  # center seam shading
    out.append(path("M-20 900 L-10 700 C 10 630 90 600 170 592 L 250 600 L 200 900 Z", fill="url(#suitdots)", opacity=0.5))
    # right arm reaching to the letter
    out.append(path("M400 620 C 470 640 540 700 610 735 L 640 770 C 600 790 560 790 520 770 C 470 740 420 720 380 700 Z",
                    fill=NAVY))
    out.append(path("M606 734 L 646 764 L 636 784 L 596 760 Z", fill=CREAM))  # cuff
    out.append(path("M640 762 C 664 760 690 772 694 790 C 680 802 652 800 634 786 Z", fill=SKIN))  # hand
    out.append(path("M650 826 C 664 812 672 830 684 818 C 694 808 700 828 718 824", stroke="#1d2a5a",
                    stroke_width=2.4, fill="none"))
    out.append(path("M676 794 L 714 820", stroke="#1a1a1a", stroke_width=7, stroke_linecap="round"))  # pen
    out.append(path("M714 820 L 722 826", stroke=GOLD, stroke_width=4, stroke_linecap="round"))
    # neck and collar
    out.append(rect(214, 520, 74, 80, fill=SKIN))
    out.append(path("M200 596 L 250 572 L 302 596 L 290 608 L 250 590 L 212 608 Z", fill=CREAM))
    # head from behind: ears, then slicked-back hair (rounder skull, tapered nape)
    out.append(ellipse(170, 468, 13, 22, fill=SKIN))
    out.append(ellipse(332, 468, 13, 22, fill=SKIN))
    out.append(path("M172 452 C 168 392 206 356 252 356 C 298 356 336 392 330 452 C 328 492 312 516 296 528 "
                    "L 290 540 C 266 548 238 548 214 540 L 208 528 C 190 516 174 492 172 452 Z", fill=HAIR))
    # combed-back strands sweeping from the crown to the nape
    for k, dx in enumerate((-40, -20, 0, 20, 40)):
        out.append(path(f"M{252 + dx * 0.5:.0f} 362 C {252 + dx * 1.15:.0f} 410 {252 + dx * 1.1:.0f} 470 {252 + dx * 0.75:.0f} 532",
                        stroke="#5e4a40", stroke_width=2, fill="none", opacity=0.4))
    out.append(path("M226 372 C 246 362 276 364 296 380 C 280 372 250 372 226 384 Z", fill="#6b5446", opacity=0.8))
    # greying temples and sides
    out.append(path("M178 420 C 178 456 186 488 204 516", stroke=GREY, stroke_width=9, fill="none", opacity=0.8))
    out.append(path("M324 420 C 324 456 316 488 298 516", stroke=GREY, stroke_width=9, fill="none", opacity=0.8))
    # rim light from the window
    out.append(path("M296 364 C 324 386 334 420 330 456", stroke=AMBER, stroke_width=5, fill="none", opacity=0.8))
    out.append(path("M330 594 C 400 602 440 630 470 680", stroke=AMBER, stroke_width=5, fill="none", opacity=0.7))
    return out


def defs():
    return [
        linear("sky", [(0, VIOLET), (0.5, ROSE), (0.85, AMBER), (1, GOLD)]),
        radial("sunglow", [(0, GOLD), (1, "rgba(255,215,122,0)")]),
        linear("wall", [(0, WALL), (1, WALL2)]),
        linear("desk", [(0, WOOD2), (1, WOOD)]),
        radial("pool", [(0, "rgba(255,215,122,0.55)"), (1, "rgba(255,215,122,0)")]),
        linear("cone", [(0, "rgba(255,226,150,0.45)"), (1, "rgba(255,226,150,0)")]),
        halftone("walldots", "#2a5a52", dot=1.6, spacing=10),
        halftone("suitdots", "#2a3a72", dot=1.8, spacing=9),
        el("clipPath", rect(WX0, WY0, WX1 - WX0, WY1 - WY0), id="win"),
        grain_filter(),
    ]


def main():
    body = [rect(0, 0, WIDTH, HEIGHT, fill="url(#wall)"), rect(0, 0, WIDTH, HEIGHT, fill="url(#walldots)", opacity=0.5)]
    body += window_frame() + flag() + desk() + folders() + letter() + lamp() + governor()
    body.append(grain_overlay(opacity=0.3))
    title = "Signing away death row: Newsom commutes California's death sentences"
    desc = ("Editorial illustration. Seen from behind, over his shoulder, Gov. Gavin Newsom, with slicked-back dark hair "
            "greying at the temples and a navy suit, signs a letter under a green desk lamp in a dark office at dusk. "
            "A tall tower of case folders rises beside him, a California bear flag hangs nearby, and through a tall "
            "window a distant generic prison's long cell blocks glow with rows of small lit windows under a rose and "
            "amber sky. Represents Newsom commuting all 548 California death sentences to life without parole on "
            "Nov. 5, 2026; the folder tower is a symbol, and the office and prison are not specific places.")
    save(document(defs(), body, title, desc), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")


if __name__ == "__main__":
    main()
