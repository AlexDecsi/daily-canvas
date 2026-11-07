"""Daily artwork, 2026-11-06: Stephen Miller replaces Susie Wiles as White House chief of staff.

Visual idea: a changing of the guard announced from a phone. At night, from low
on the North Lawn driveway, the West Wing's white portico glows; above its
pediment a colossal blank phone screen hangs in the crimson sky like a moon,
throwing cold light (the Truth Social post). Miller stands backlit in the
golden doorway as Wiles walks away down the drive, her long shadow stretching
toward the press corps silhouetted in the foreground.

Verified (brief): on Nov. 6, 2026, Trump announced on Truth Social that deputy
chief of staff Stephen Miller will replace Susie Wiles as chief of staff,
starting Monday; Wiles said Friday was her last day (CBS News; AP via PBS).
Drawn: Wiles (short pale-blonde hair, dark suit) walking away and Miller (bald,
slim dark suit, thin dark tie) in the doorway: an editorial staging of the
handover, not a reported moment. The phone is a symbol, with a blank screen.
The press are generic silhouettes. The portico is drawn from the West Wing's
known features (white pediment, columns, hanging lantern) but simplified.
Not drawn: no Trump figure, no readable text, no signs, no quotes.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-06"
R = rng(20261106)

OX0, OX1, OX2 = "#2a0710", "#5c0f1f", "#a3182c"       # oxblood night sky
SCARLET = "#d7263d"
MINT, MINT2, ICE = "#7ff5d8", "#3fc7ad", "#e6fff8"     # phone light
BONE, BONE2, BONE3 = "#f6efe2", "#ddd2bf", "#b9ab95"   # white facade
GOLD, GOLD2 = "#ffcc4d", "#f29b30"
CHAR, CHAR2, INK = "#24202a", "#3a3440", "#120e14"
HEDGE, HEDGE2 = "#14261f", "#1f3a2e"

GROUND = 762  # top of the driveway


def sky():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#sky)")]
    # cold rays from the phone
    cx, cy = 600, 250
    for a in range(0, 360, 12):
        t = math.radians(a)
        out.append(poly([(cx, cy), (cx + 900 * math.cos(t - 0.035), cy + 900 * math.sin(t - 0.035)),
                         (cx + 900 * math.cos(t + 0.035), cy + 900 * math.sin(t + 0.035))], fill=MINT, opacity=0.07))
    out.append(circle(cx, cy, 330, fill="url(#halo)"))
    # a few stars
    for _ in range(40):
        x, y = R.uniform(0, WIDTH), R.uniform(0, 380)
        if abs(x - cx) > 230:
            out.append(circle(round(x, 1), round(y, 1), round(R.uniform(0.8, 2), 1), fill=ICE, opacity=0.7))
    return out


def phone():
    """A huge blank phone screen hanging in the sky: a symbol for the social-media announcement."""
    x, y, w, h = 465, 40, 270, 470
    out = [rect(x - 16, y - 16, w + 32, h + 32, rx=46, fill=INK)]
    out.append(rect(x - 16, y - 16, w + 32, h + 32, rx=46, fill="none", stroke=MINT2, stroke_width=3, opacity=0.6))
    out.append(rect(x, y, w, h, rx=32, fill="url(#screen)"))
    out.append(rect(x + w / 2 - 34, y + 12, 68, 16, rx=8, fill=INK))  # camera notch
    # blank post shapes (no text): an avatar dot and a few soft bars
    out.append(circle(x + 46, y + 86, 22, fill=MINT2, opacity=0.55))
    for k, ww in enumerate((150, 190, 170, 120)):
        out.append(rect(x + 82 if k == 0 else x + 28, y + 76 + (k * 30 if k else 0) + (40 if k else 0), ww, 12, rx=6,
                        fill=MINT2, opacity=0.45))
    out.append(rect(x + 18, y + 18, 18, h - 40, rx=9, fill="#ffffff", opacity=0.10))  # glass sheen
    return out


def west_wing():
    out = []
    # long low facade behind the portico
    out.append(rect(60, 470, 1080, GROUND - 470, fill="url(#facade)"))
    out.append(rect(50, 452, 1100, 22, fill=BONE))
    for x in range(56, 1150, 22):  # roof balustrade
        out.append(rect(x, 432, 9, 20, fill=BONE2))
    out.append(rect(50, 428, 1100, 8, fill=BONE))
    out.append(rect(50, 426, 1100, 3, fill=MINT, opacity=0.7))
    # tall windows, warm light
    for x in list(range(100, 420, 80)) + list(range(800, 1120, 80)):
        out.append(rect(x, 520, 46, 150, fill=GOLD, opacity=0.9))
        out.append(rect(x + 21, 520, 4, 150, fill=BONE2))
        out.append(rect(x, 590, 46, 4, fill=BONE2))
        out.append(rect(x - 8, 506, 62, 12, fill=BONE))
        out.append(rect(x - 6, 670, 58, 8, fill=BONE))
    return out


def portico():
    out = []
    px0, px1 = 440, 760
    # pediment
    out.append(poly([(px0 - 20, 430), (600, 352), (px1 + 20, 430)], fill=BONE))
    out.append(poly([(px0 + 14, 424), (600, 368), (px1 - 14, 424)], fill=BONE2))
    out.append(path(f"M{px0 - 20} 430 L600 352 L{px1 + 20} 430", stroke=MINT, stroke_width=4, fill="none", opacity=0.8))
    out.append(rect(px0 - 24, 430, px1 - px0 + 48, 26, fill=BONE))
    out.append(rect(px0 - 24, 456, px1 - px0 + 48, 8, fill=BONE3))
    # door opening and golden light
    out.append(rect(548, 520, 104, GROUND - 520 - 30, fill="url(#door)"))
    out.append(path("M548 520 Q600 480 652 520 Z", fill=GOLD))  # fanlight
    # columns
    for cx in (462, 516, 684, 738):
        out.append(rect(cx - 14, 464, 28, GROUND - 464 - 30, fill="url(#col)"))
        out.append(rect(cx - 19, 464, 38, 10, fill=BONE))
        out.append(rect(cx - 19, GROUND - 42, 38, 12, fill=BONE))
    # hanging lantern
    out.append(rect(598, 464, 4, 12, fill=INK))
    out.append(poly([(588, 476), (612, 476), (609, 504), (591, 504)], fill=GOLD))
    out.append(path("M588 476 L612 476 L609 504 L591 504 Z M600 476 L600 504", fill="none", stroke=INK, stroke_width=2))
    # steps
    for k in range(3):
        out.append(rect(420 - k * 18, GROUND - 30 + k * 10, 360 + k * 36, 10, fill=BONE if k % 2 == 0 else BONE2))
    return out


def driveway():
    out = [rect(0, GROUND, WIDTH, HEIGHT - GROUND, fill="url(#drive)")]
    # light spilling from the door down the drive
    out.append(poly([(548, GROUND), (652, GROUND), (820, HEIGHT), (380, HEIGHT)], fill=GOLD, opacity=0.18))
    return out


def hedges():
    out = []
    for x0, x1 in ((0, 360), (840, 1200)):
        out.append(rect(x0, 712, x1 - x0, 52, fill=HEDGE))
        for x in range(x0, x1, 26):
            out.append(circle(x + 13, 714, 16, fill=HEDGE2))
    return out


def people():
    out = []
    suit = "#1b1a24"
    # Miller in the doorway, backlit; his long shadow runs down the steps and the drive toward the viewer
    out.append(poly([(588, GROUND - 30), (612, GROUND - 30), (690, HEIGHT), (560, HEIGHT)], fill=INK, opacity=0.55))
    miller = Look(skin="#e8b89a", top=suit, bottom=suit, hair="#e8b89a", hair_style="bald",
                  accent="#0b0b10", long_tie=True, build=0.95)
    out.append(figure(600, GROUND - 30, 205, facing=-1, pose=Pose(back_arm=(-4, 6), front_arm=(4, 6)), look=miller))
    out.append(path("M607 566 q 9 11 7 26", stroke=MINT, stroke_width=2.5, fill="none", opacity=0.8))  # rim on scalp
    # Wiles walking away down the drive, to the left, into the dark
    wiles = Look(skin="#efc3a6", top="#2c2a3a", bottom="#2c2a3a", hair="#efe3c4", hair_style="long", build=0.95)
    wx, wy = 300, 850
    out.append(poly([(wx - 14, wy), (wx + 14, wy), (wx - 30, HEIGHT), (wx - 130, HEIGHT)], fill=INK, opacity=0.45))
    out.append(figure(wx, wy, 210, facing=-1,
                      pose=Pose(back_arm=(-25, 15), front_arm=(22, 15), back_leg=(-20, -8), front_leg=(18, 0)),
                      look=wiles))
    # mint rim light on her hair from the phone
    s = 2.1
    out.append(path(f"M{wx + 6 * s:.0f} {wy - 95 * s:.0f} q {3 * s:.0f} {4 * s:.0f} {3 * s:.0f} {8 * s:.0f}",
                    stroke=MINT, stroke_width=2.5, fill="none", opacity=0.8))
    return out


def press():
    """Generic press silhouettes in the lower-right foreground, cameras raised toward the portico."""
    out = []
    for fx, fy, r in ((790, 712, 54), (1000, 640, 40)):  # two small camera flashes
        pts = []
        for k in range(16):
            a = k * math.pi / 8
            rr = r if k % 2 == 0 else r * 0.28
            pts.append((round(fx + rr * math.cos(a), 1), round(fy + rr * math.sin(a), 1)))
        out.append(poly(pts, fill=ICE, opacity=0.85))
    cam = group([rect(-12, -16, 34, 24, fill=INK, rx=3), circle(22, -4, 9, fill=CHAR2), rect(-2, -22, 12, 7, fill=INK)],
                transform="scale(0.55)")
    sil = dict(skin=INK, top=INK, bottom=INK, hair=INK, shoes=INK)
    for x, h, style in ((930, 270, "short"), (1050, 300, "long"), (1160, 280, "cap")):
        out.append(figure(x, HEIGHT + 30, h, facing=-1, pose=Pose(back_arm=(110, -40), front_arm=(118, -50), lean=-4),
                          look=Look(hair_style=style, **sil), hand_items={"front": cam}))
    # a boom mic reaching in from the right edge
    out.append(path("M1200 610 L960 520", stroke=INK, stroke_width=7))
    out.append(ellipse(948, 516, 26, 12, fill=INK))
    out.append(path("M926 512 Q948 500 972 510", stroke=MINT, stroke_width=2, fill="none", opacity=0.7))
    return out


def lamppost():
    """A dark lamppost and hedge corner framing the left edge."""
    out = [rect(40, 300, 16, HEIGHT - 300, fill=INK), rect(30, 860, 36, 40, fill=INK)]
    out.append(poly([(20, 300), (76, 300), (66, 250), (30, 250)], fill=INK))
    out.append(rect(32, 258, 32, 36, fill=GOLD, opacity=0.9))
    out.append(circle(48, 276, 60, fill="url(#lampglow)"))
    out.append(path("M48 250 L48 232", stroke=INK, stroke_width=6))
    return out


def defs():
    return [
        linear("sky", [(0, OX0), (0.55, OX1), (1, OX2)]),
        radial("halo", [(0, "rgba(127,245,216,0.45)"), (1, "rgba(127,245,216,0)")]),
        linear("screen", [(0, ICE), (1, MINT)]),
        linear("facade", [(0, BONE2), (1, BONE3)]),
        linear("col", [(0, BONE3), (0.4, BONE), (1, BONE2)], x2=1, y2=0),
        linear("door", [(0, GOLD), (1, GOLD2)]),
        linear("drive", [(0, CHAR2), (1, INK)]),
        radial("lampglow", [(0, "rgba(255,204,77,0.5)"), (1, "rgba(255,204,77,0)")]),
        grain_filter(),
    ]


def main():
    body = sky() + phone() + west_wing() + portico() + hedges() + driveway() + people() + press() + lamppost()
    body.append(grain_overlay(opacity=0.3))
    title = "Changing of the guard: Stephen Miller replaces Susie Wiles as White House chief of staff"
    desc = ("Editorial illustration. At night, the white columned portico of the White House West Wing glows, its "
            "doorway lit gold. Stephen Miller, bald, in a slim dark suit and tie, stands in the doorway while Susie "
            "Wiles, with short pale-blonde hair and a dark suit, walks away down the driveway. Above the pediment, a "
            "huge blank phone screen glows in a crimson sky like a moon, and silhouetted press with a TV camera and a "
            "boom microphone watch from the foreground. Represents President Trump announcing on Truth Social on "
            "Nov. 6, 2026, that Miller will replace Wiles as chief of staff; the handover scene and the phone are "
            "editorial symbols, not a reported moment.")
    save(document(defs(), body, title, desc), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")


if __name__ == "__main__":
    main()
