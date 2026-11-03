"""Daily artwork, 2026-11-02: Supreme Court rejects bid to set aside 20,000 California ballots.

Visual idea: a split night scene on Election Eve. On the left the floodlit Supreme
Court towers from a low angle against a huge pale moon; a long ribbon of blank
white mail-ballot envelopes sweeps unbroken past its steps and across the split
into a warm amber California counting room, where election workers keep sorting:
the ballots were not pulled aside.

Verified (brief): on Nov. 2 the Supreme Court, in a brief unexplained order with no
public dissent, rejected the administration's emergency request that California
set aside up to ~20,000 mail ballots it says came from noncitizens (NBC; AP via
the Boston Globe; CBS). Hundreds of thousands of ballots had already been processed.
Drawn: the court's west front (wide steps, flanking seated statues on plinths,
eight-column portico, frieze band, pediment), lamp standards; generic county
election workers handling envelopes in trays; the envelope ribbon is symbolic.
Not drawn: no justices or likenesses, no text, names, numbers or markings on
envelopes, no protesters, no vote counts or outcomes.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-02"
R = rng(20261102)
PLUM, PLUM2, VIOLET, MAUVE = "#1f1238", "#3a1f5c", "#5d3a86", "#9a7bc0"
MOON = "#f6eed8"
MARBLE, MARBLE2, MARBLE3, MARBLE4 = "#f4ecf4", "#d9cde0", "#b3a3c4", "#7f6e98"
AMBER, AMBER2, AMBER3 = "#ffc65c", "#f39a3d", "#c8642a"
TEAL, TEAL2 = "#1f8a8a", "#156266"
PAPER, PAPER2 = "#fffdf6", "#e9e2d2"
INK = "#140b24"

SPLIT_TOP, SPLIT_BOT = 760, 600   # x of the diagonal split at the top and bottom of the frame


def split_x(y):
    return SPLIT_TOP + (SPLIT_BOT - SPLIT_TOP) * y / HEIGHT


def sky():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#sky)")]
    out.append(rect(0, 0, WIDTH, HEIGHT, fill="url(#dots)", opacity=0.10))
    out.append(circle(330, 250, 320, fill="url(#moonglow)"))
    out.append(circle(330, 250, 200, fill=MOON))
    out.append(circle(300, 200, 34, fill="#ebe0c4", opacity=0.6))
    out.append(circle(430, 300, 22, fill="#ebe0c4", opacity=0.5))
    for _ in range(40):
        x, y = R.uniform(0, 740), R.uniform(0, 420)
        if math.hypot(x - 360, y - 250) > 220:
            out.append(circle(x, y, R.uniform(0.8, 2.0), fill=MOON, opacity=R.uniform(0.4, 0.9)))
    return out


def court():
    """Supreme Court west front from a low angle: pediment, frieze, eight columns, steps."""
    cx, L, Rr = 360, 70, 650
    out = []
    # side wings in shadow behind the portico
    out.append(rect(0, 330, 90, 330, fill=MARBLE4))
    out.append(rect(630, 330, 120, 330, fill=MARBLE4))
    for k in range(4):
        out.append(rect(14 + k * 0, 360 + k * 70, 60, 34, fill=VIOLET, opacity=0.7))
        out.append(rect(655, 360 + k * 70, 60, 34, fill=VIOLET, opacity=0.7))
    # pediment
    out.append(poly([(L - 20, 236), (Rr + 20, 236), (cx, 120)], fill=MARBLE))
    out.append(poly([(L + 20, 228), (Rr - 20, 228), (cx, 138)], fill=MARBLE2))
    # sculpture group suggested as soft relief shapes
    for k in range(11):
        x = L + 70 + k * 44
        hgt = 76 - abs(x - cx) * 0.26
        out.append(ellipse(x, 226 - hgt / 2, 13, hgt / 2, fill=MARBLE3, opacity=0.8))
    out.append(rect(L - 26, 236, Rr - L + 52, 14, fill=MARBLE))
    # frieze / architrave band (inscription not drawn)
    out.append(rect(L - 14, 250, Rr - L + 28, 40, fill=MARBLE2))
    out.append(rect(L - 14, 286, Rr - L + 28, 8, fill=MARBLE3))
    # portico shadow behind columns
    out.append(rect(L, 294, Rr - L, 270, fill="url(#portico)"))
    # bronze doors glow faintly
    out.append(rect(cx - 34, 410, 68, 154, fill="#3b2a3e"))
    out.append(rect(cx - 30, 414, 60, 150, fill="#6b4a3a", opacity=0.8))
    # columns
    n = 8
    for i in range(n):
        x = L + 24 + i * (Rr - L - 48) / (n - 1)
        out.append(rect(x - 21, 294, 42, 12, fill=MARBLE))                  # capital
        out.append(path(f"M{x - 26} 294 Q{x} 282 {x + 26} 294 Z", fill=MARBLE2))
        out.append(path(f"M{x - 17} 306 L{x + 17} 306 L{x + 19} 556 L{x - 19} 556 Z", fill="url(#column)"))
        for f in (-9, 0, 9):
            out.append(path(f"M{x + f} 310 L{x + f * 1.1} 552", stroke=MARBLE3, stroke_width=1.4, opacity=0.6))
        out.append(rect(x - 24, 556, 48, 10, fill=MARBLE2))
    # stylobate and steps, widening toward the viewer
    out.append(rect(L - 30, 566, Rr - L + 60, 14, fill=MARBLE))
    for s in range(9):
        y = 580 + s * 22
        w = Rr - L + 60 + s * 70
        out.append(rect(cx - w / 2, y, w, 22, fill=MARBLE2 if s % 2 else MARBLE))
        out.append(rect(cx - w / 2, y, w, 4, fill=MARBLE3, opacity=0.7))
    # flanking plinths with seated statues (silhouettes)
    for sx in (L - 60, Rr + 10):
        out.append(rect(sx, 520, 110, 70, fill=MARBLE2))
        out.append(rect(sx - 4, 512, 118, 10, fill=MARBLE))
        out.append(path(f"M{sx + 30} 512 L{sx + 30} 470 Q{sx + 55} 430 {sx + 72} 470 L{sx + 82} 512 Z", fill=MARBLE3))
        out.append(circle(sx + 56, 440, 13, fill=MARBLE3))
    return out


def lamps():
    out = []
    for x in (20, 640):
        out.append(rect(x - 3, 640, 6, 140, fill=INK))
        out.append(circle(x, 632, 26, fill="url(#lampglow)"))
        out.append(circle(x, 634, 9, fill=AMBER))
    return out


def floodlight():
    """Cones of floodlight washing up the facade from the plaza."""
    return [poly([(120, 900), (230, 900), (330, 280), (80, 280)], fill="url(#flood)", style="mix-blend-mode:screen"),
            poly([(500, 900), (610, 900), (660, 280), (420, 280)], fill="url(#flood)", style="mix-blend-mode:screen")]


def counting_room():
    """California county ballot-processing room, seen through the diagonal split."""
    pts = [(split_x(0), 0), (WIDTH, 0), (WIDTH, HEIGHT), (split_x(HEIGHT), HEIGHT)]
    clip = el("clipPath", poly(pts), id="roomclip")
    room = [rect(0, 0, WIDTH, HEIGHT, fill="url(#roomwall)")]
    # ceiling light fixtures with downward cones
    for x in (800, 960, 1120):
        room.append(rect(x - 50, 70, 100, 12, fill=PAPER))
        room.append(poly([(x - 50, 82), (x + 50, 82), (x + 120, 560), (x - 120, 560)], fill="url(#cone)"))
    # back wall shelving with stacked trays
    room += window()
    for row in range(2):
        y = 320 + row * 70
        room.append(rect(700, y + 44, 520, 8, fill=AMBER3))
        for k in range(8):
            x = 712 + k * 62
            room.append(rect(x, y + 16, 54, 28, fill=TEAL2))
            for e in range(4):
                room.append(rect(x + 4 + e * 12, y + 8 + (e % 2) * 3, 9, 20, fill=PAPER2))
    room.append(rect(0, 640, WIDTH, 260, fill="url(#floor)"))
    # conveyor sorter: the envelope ribbon lands on its belt
    room.append(poly([(600, 640), (1200, 590), (1200, 612), (600, 662)], fill=INK, opacity=0.35))
    # workers stand behind the long table
    room += workers_behind()
    room.append(poly([(600, 600), (1200, 556), (1200, 606), (600, 652)], fill=TEAL))
    room.append(poly([(600, 652), (1200, 606), (1200, 628), (600, 672)], fill=TEAL2))
    room.append(poly([(600, 672), (1200, 628), (1200, 820), (600, 860)], fill="url(#counter)"))
    for k in range(6):
        x = 640 + k * 100
        top = 680 - (x - 600) * 0.073
        room.append(rect(x, top, 70, 150, fill=TEAL, opacity=0.35, rx=4))
    for x, y in ((960, 566), (1100, 555)):
        room.append(poly([(x - 50, y), (x + 50, y - 8), (x + 50, y + 14), (x - 50, y + 22)], fill=TEAL2))
        for e in range(6):
            room.append(rect(x - 42 + e * 15, y - 16 - e * 1.3, 12, 24, fill=PAPER, stroke=PAPER2, stroke_width=0.8))
    room += worker_front()
    group_ = group(room, clip_path="url(#roomclip)")
    spill = poly([(split_x(0) - 260, 0), (split_x(0), 0), (split_x(HEIGHT), HEIGHT), (split_x(HEIGHT) - 260, HEIGHT)],
                 fill="url(#spillwarm)", style="mix-blend-mode:screen")
    edge = path(f"M{split_x(0)} 0 L{split_x(HEIGHT)} {HEIGHT}", stroke=PAPER, stroke_width=10)
    return clip, [spill, group_, edge]


def window():
    """A night window on the back wall; palm silhouettes place the room in California."""
    x0, y0, w, h = 900, 130, 260, 160
    out = [rect(x0 - 8, y0 - 8, w + 16, h + 16, fill=AMBER3),
           rect(x0, y0, w, h, fill="url(#winsky)")]
    for px, ph in ((960, 130), (1050, 150), (1120, 110)):
        out.append(path(f"M{px} {y0 + h} Q{px + 6} {y0 + h - ph / 2} {px + 2} {y0 + h - ph}", fill="none",
                        stroke=INK, stroke_width=5))
        for a in range(0, 360, 45):
            r = math.radians(a)
            ex, ey = px + 2 + math.cos(r) * 34, y0 + h - ph + math.sin(r) * 14 + 8
            out.append(path(f"M{px + 2} {y0 + h - ph} Q{(px + ex) / 2} {y0 + h - ph - 14} {ex:.0f} {ey:.0f}",
                            fill="none", stroke=INK, stroke_width=4, stroke_linecap="round"))
    out.append(rect(x0 + w / 2 - 3, y0, 6, h, fill=AMBER3))
    out.append(rect(x0, y0 + h / 2 - 3, w, 6, fill=AMBER3))
    return out


def envelope(w=34, h=22):
    return group([rect(-w / 2, -h / 2, w, h, fill=PAPER, stroke=PAPER2, stroke_width=1),
                  path(f"M{-w / 2} {-h / 2} L0 {h * 0.12} L{w / 2} {-h / 2}", fill="none", stroke=PAPER2,
                       stroke_width=1.4)])


def held_envelope():
    return group([rect(-8, -12, 18, 12, fill=PAPER, stroke=PAPER2, stroke_width=0.8)])


def tray():
    return group([rect(-16, -6, 32, 10, fill=TEAL2),
                  *[rect(-13 + e * 6, -13, 5, 9, fill=PAPER) for e in range(5)]])


def workers_behind():
    out = []
    gy = 690
    a = Look(skin="#8d5a3c", top=AMBER2, bottom="#2d2440", hair="#1b1210", hair_style="bun", face="neutral")
    out.append(figure(790, gy, 250, 1, Pose(back_arm=(60, 30), front_arm=(70, 30), back_leg=(-4, 0),
                                             front_leg=(4, 0), lean=10, head_tilt=18), a,
                      hand_items={"front": held_envelope()}))
    b = Look(skin="#e6b998", top="#7b3e8c", bottom="#22223a", hair="#a0522d", hair_style="long", face="neutral")
    out.append(figure(960, gy - 14, 240, -1, Pose(back_arm=(50, 35), front_arm=(80, 25), back_leg=(-4, 0),
                                                   front_leg=(4, 0), lean=8, head_tilt=14), b,
                      hand_items={"front": held_envelope()}))
    d = Look(skin="#5e3b2a", top="#e7e1d3", bottom="#2b2b38", hair="#bdb6ad", hair_style="short", face="neutral",
             accent=TEAL)
    out.append(figure(1105, gy - 26, 230, -1, Pose(back_arm=(-10, 10), front_arm=(95, 40), back_leg=(-4, 0),
                                                    front_leg=(4, 0), lean=4, head_tilt=10), d,
                      hand_items={"front": held_envelope()}))
    return out


def worker_front():
    c = Look(skin="#c08a64", top="#8a2f55", bottom="#2b2b38", hair="#2a1d18", hair_style="cap")
    return [ellipse(1110, 892, 90, 12, fill=INK, opacity=0.25),
            figure(1110, 890, 300, -1, Pose(back_arm=(50, -10), front_arm=(55, -10), back_leg=(-16, -4),
                                             front_leg=(18, -2), lean=-2, head_tilt=8), c, hand_items={"front": tray()})]


def ribbon():
    """Symbolic stream of blank ballot envelopes sweeping past the steps into the trays."""
    out = []
    # bezier from bottom-left, across the steps, into the counting-room table
    p0, p1, p2, p3 = (-60, 790), (260, 930), (470, 640), (880, 610)
    n = 46
    out.append(path(f"M{p0[0]} {p0[1]} C{p1[0]} {p1[1]} {p2[0]} {p2[1]} {p3[0]} {p3[1]}", fill="none",
                    stroke=PAPER, stroke_width=70, stroke_linecap="round", opacity=0.10))
    out.append(path(f"M{p0[0]} {p0[1]} C{p1[0]} {p1[1]} {p2[0]} {p2[1]} {p3[0]} {p3[1]}", fill="none",
                    stroke=PAPER, stroke_width=26, stroke_linecap="round", opacity=0.14))
    for i in range(n):
        t = i / (n - 1)
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        s = 2.0 - 1.4 * t
        rot = R.uniform(-30, 30)
        jitter = R.uniform(-12, 12) * (1 - t)
        out.append(group([envelope()], transform=f"translate({x:.0f} {y + jitter:.0f}) rotate({rot:.0f}) scale({s:.2f})"))
    return out


defs = [grain_filter(),
        linear("sky", [(0, PLUM), (0.6, PLUM2), (1, VIOLET)]),
        radial("moonglow", [(0, MOON, 0.55), (0.6, MOON, 0.12), (1, MOON, 0)]),
        radial("lampglow", [(0, AMBER, 0.8), (1, AMBER, 0)]),
        linear("flood", [(0, "#fff4d8", 0.35), (1, "#fff4d8", 0)]),
        linear("portico", [(0, INK), (1, "#3a2552")]),
        linear("column", [(0, MARBLE), (1, MARBLE2)], x2=1, y2=0),
        linear("spillwarm", [(0, AMBER, 0), (1, AMBER, 0.32)], x2=1, y2=0),
        linear("counter", [(0, TEAL2), (1, "#0e3f42")]),
        linear("winsky", [(0, PLUM), (1, VIOLET)]),
        linear("floor", [(0, AMBER3), (1, "#8f4220")]),
        linear("roomwall", [(0, "#ffdf9a"), (1, AMBER)]),
        linear("cone", [(0, "#fffbe8", 0.55), (1, "#fffbe8", 0)]),
        halftone("dots", MOON, dot=1.2, spacing=9)]
clip, room = counting_room()
defs.append(clip)
body = (sky() + [group(court() + floodlight() + lamps(), transform="translate(6 40) scale(0.9)")] + room + ribbon() + [grain_overlay(opacity=0.3)])

save(document(defs, body,
              "Supreme Court rejects bid to set aside 20,000 California ballots",
              "Graphic poster illustration in a split composition at night. On the left, the floodlit marble west "
              "front of the U.S. Supreme Court, with its wide steps, columned portico and pediment, rises against a "
              "large pale moon. A ribbon of blank white mail-ballot envelopes sweeps past the steps and across a "
              "diagonal divide into a warmly lit California ballot-processing room, where generic election workers "
              "sort envelopes in trays at a long table. The envelope ribbon is symbolic. No justices, no text."),
     Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
