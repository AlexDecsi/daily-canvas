"""Daily artwork, 2026-11-09: Rep. Thomas Massie files articles of impeachment against Pete Hegseth.

Visual idea: eight pages take flight. From a low angle on the House floor, Massie
stands at a floor lectern in the foreground, mid-sentence, facing the Speaker's
rostrum; the eight pages of his resolution peel off his hand and spiral up through
a shaft of skylight toward the chamber's glass ceiling, shrinking as they rise:
a symbol of the articles going up to the House for a forced vote.

Verified (brief): on Nov. 9, 2026, Massie (R-Ky.) introduced and read on the House
floor a resolution with eight articles of impeachment against Defense Secretary
Pete Hegseth; House leaders must act within two legislative days (CBS News, CNBC).
Drawn: Massie (slim, glasses, short grey hair, dark suit) speaking at a floor
lectern; the rostrum tiers, the vertical US flag and clerks' desks; a few members
seated, neutral. The flying pages are illustrative, blank (no text).
Not drawn: no Hegseth figure, no vote, no signs or text, no crowd reaction.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure, SKIN, HAIR  # noqa: E402

DATE = "2026-11-09"
R = rng(20261109)

# palette: oxblood chamber, cream marble, slate navy, gold, paper white
OX, OX2, OX3 = "#6a1a2b", "#4a0f1d", "#2e0912"
CREAM, CREAM2, CREAM3 = "#efe2c8", "#d8c6a3", "#b9a47e"
SLATE, SLATE2, SLATE3 = "#2b3a5c", "#1d2843", "#121a2e"
GOLD, GOLD2 = "#e7b54a", "#a77b25"
PAPER, PAPER2 = "#fffaf0", "#d9d2c3"
WOOD, WOOD2 = "#5a3420", "#3b2214"
FLAG_R, FLAG_B = "#b3263a", "#1f2f66"


def defs():
    return [
        linear("wall", [(0, OX), (0.6, OX2), (1, OX3)]),
        linear("ceiling", [(0, "#fff4d8"), (0.5, CREAM), (1, CREAM2)]),
        linear("shaft", [(0, "#fff6dc"), (1, "#fff6dc")], x2=0, y2=1),
        linear("floor", [(0, SLATE), (1, SLATE3)]),
        linear("lectern", [(0, WOOD), (1, WOOD2)]),
        radial("glow", [(0, "#fffbe9"), (0.5, "#ffe9b0"), (1, "#ffe9b0")]),
        blur("soft", 14),
        blur("softer", 4),
        halftone("dots", OX3, dot=1.8, spacing=7),
        grain_filter(),
    ]


def opacity_stops(id_, color, a0, a1):
    return el("linearGradient", [el("stop", offset=0, stop_color=color, stop_opacity=a0),
                                 el("stop", offset=1, stop_color=color, stop_opacity=a1)],
              id=id_, x1=0, y1=0, x2=0, y2=1)


# ---------------------------------------------------------------- architecture
def ceiling():
    out = [rect(0, 0, WIDTH, 230, fill="url(#ceiling)")]
    # coffered side panels receding toward the skylight
    for i in range(9):
        x = i * 150 - 50
        out.append(poly([(x, 0), (x + 120, 0), (x + 105, 120), (x + 15, 120)], fill=CREAM2, opacity=0.55))
        out.append(poly([(x + 18, 8), (x + 102, 8), (x + 92, 100), (x + 28, 100)], fill=CREAM3, opacity=0.35))
    # skylight: a glowing glass oval with leading
    out.append(ellipse(560, 70, 330, 95, fill="url(#glow)"))
    for k in range(-6, 7):
        out.append(path(f"M560 70 L{560 + k * 60} {70 + 95 * (1 - abs(k) / 7):.0f}", stroke=GOLD2,
                        stroke_width=2, opacity=0.35))
    out.append(ellipse(560, 70, 330, 95, fill="none", stroke=GOLD2, stroke_width=5, opacity=0.6))
    out.append(ellipse(560, 70, 210, 60, fill="none", stroke=GOLD2, stroke_width=2, opacity=0.4))
    # cornice
    out.append(rect(0, 200, WIDTH, 30, fill=CREAM3))
    for x in range(0, WIDTH, 24):
        out.append(rect(x + 4, 206, 12, 16, fill=CREAM2))
    return out


def wall():
    out = [rect(0, 230, WIDTH, 420, fill="url(#wall)")]
    out.append(rect(0, 230, WIDTH, 420, fill="url(#dots)", opacity=0.25))
    # marble pilasters
    for x in (40, 230, 890, 1080):
        out.append(rect(x, 230, 56, 420, fill=CREAM2, opacity=0.9))
        out.append(rect(x + 8, 230, 6, 420, fill=CREAM, opacity=0.8))
        out.append(rect(x + 42, 230, 6, 420, fill=CREAM3, opacity=0.8))
    # gallery rail
    out.append(rect(0, 300, 380, 14, fill=GOLD2, opacity=0.8))
    out.append(rect(760, 300, 440, 14, fill=GOLD2, opacity=0.8))
    return out


def flag():
    """US flag hung vertically behind the rostrum: stripes run up-down, union at upper left."""
    x0, y0, w, h = 455, 245, 210, 270
    out = [rect(x0 - 6, y0 - 6, w + 12, h + 12, fill=OX3, opacity=0.6)]
    sw = w / 13
    for i in range(13):
        out.append(rect(round(x0 + i * sw, 1), y0, round(sw + 0.4, 1), h, fill=FLAG_R if i % 2 == 0 else PAPER))
    uw, uh = sw * 7, h * 0.47
    out.append(rect(x0, y0, round(uw, 1), round(uh, 1), fill=FLAG_B))
    for r_ in range(10):
        for c in range(5):
            cx = x0 + 10 + c * (uw - 20) / 4 + (5 if r_ % 2 else 0)
            cy = y0 + 9 + r_ * (uh - 18) / 9
            if cx < x0 + uw - 4:
                out.append(circle(round(cx, 1), round(cy, 1), 2.1, fill=PAPER))
    # gentle drape shading
    for i in range(0, 13, 3):
        out.append(rect(round(x0 + i * sw, 1), y0, round(sw * 1.2, 1), h, fill=OX3, opacity=0.12))
    # gold fasces flanking the flag
    for fx in (415, 705):
        out.append(rect(fx - 9, 250, 18, 250, rx=8, fill=GOLD))
        for k in range(5):
            out.append(rect(fx - 9, 262 + k * 52, 18, 5, fill=GOLD2))
        out.append(path(f"M{fx - 4} 250 L{fx + 16} 236 L{fx + 4} 262 Z", fill=GOLD2))
    return out


def rostrum():
    out = []
    # three marble tiers, widest at the bottom
    tiers = [(400, 515, 320, 60), (340, 575, 440, 62), (270, 637, 580, 70)]
    for x, y, w, h in tiers:
        out.append(rect(x, y, w, h, fill=CREAM))
        out.append(rect(x, y, w, 9, fill=CREAM3))
        for k in range(1, 6):
            px = x + k * w / 6
            out.append(rect(round(px - 28, 1), y + 18, 56, h - 28, fill=WOOD, opacity=0.85))
            out.append(rect(round(px - 24, 1), y + 22, 48, h - 36, fill="none", stroke=GOLD2, stroke_width=1.5,
                            opacity=0.7))
    # Speaker's chair back, empty presiding chair behind the top desk (presiding officer generic)
    out.append(rect(536, 470, 48, 50, rx=6, fill=SLATE2))
    # clerks seated at the two lower tiers: only shoulders and heads above the desks
    for cx, cy, i in [(400, 577, 0), (470, 577, 1), (650, 577, 2), (720, 577, 3), (520, 515, 4)]:
        skin = SKIN[(i * 2 + 1) % len(SKIN)]
        out.append(path(f"M{cx - 15} {cy} Q{cx - 14} {cy - 18} {cx} {cy - 19} Q{cx + 14} {cy - 18} {cx + 15} {cy} Z",
                        fill=[SLATE, "#3e4a6b", SLATE2, "#5a4a62", SLATE][i]))
        out.append(circle(cx, cy - 27, 8, fill=skin))
        out.append(path(f"M{cx - 8} {cy - 28} Q{cx} {cy - 40} {cx + 8} {cy - 28} Q{cx} {cy - 33} {cx - 8} {cy - 28} Z",
                        fill=HAIR[i % len(HAIR)]))
    return out


def seats():
    """Curved rows of members' benches sweeping across the lower floor."""
    out = [rect(0, 650, WIDTH, 250, fill="url(#floor)")]
    # well of the House: carpet in front of the rostrum
    out.append(path("M250 707 L870 707 L980 760 L140 760 Z", fill=SLATE2))
    for y in ROWS:  # bench seats and backs behind the members
        out.append(path(f"M-20 {y - 16} Q560 {y - 56} 1220 {y - 16}", stroke="#24304f", stroke_width=22, fill="none"))
    return out


ROWS = [770, 818, 868]


def arc_y(row_y, x):
    t = (x + 20) / 1240
    return row_y - 80 * t * (1 - t)


def members():
    """A handful of members seated on the benches, listening (neutral, generic)."""
    out = []
    spots = [(0, 60), (0, 200), (0, 360), (1, 120), (1, 290), (1, 470), (2, 40), (2, 380)]
    for i, (row, x) in enumerate(spots):
        hip_y = arc_y(ROWS[row], x) - 16
        h = 118 + row * 14
        look = Look(skin=SKIN[(i * 3 + 1) % len(SKIN)], top=["#3b4a6e", "#5b4766", "#3d5e5a", "#6e2b3b"][i % 4],
                    bottom=SLATE3, hair=HAIR[(i * 2) % len(HAIR)],
                    hair_style=["short", "long", "short", "bun", "short", "bald", "long", "short"][i],
                    accent=[GOLD, None, PAPER, None, FLAG_R, None, None, GOLD][i])
        pose = Pose(back_arm=(30, 50), front_arm=(35, 55), back_leg=(80, -85), front_leg=(85, -85), head_tilt=-6)
        out.append(figure(x, hip_y + h * 0.46, h, facing=1, pose=pose, look=look))
    # bench fronts drawn over the members' legs
    for y in ROWS:
        out.append(path(f"M-20 {y + 20} Q560 {y - 20} 1220 {y + 20}", stroke=SLATE3, stroke_width=42, fill="none"))
        out.append(path(f"M-20 {y} Q560 {y - 40} 1220 {y}", stroke="#4a5d88", stroke_width=3, fill="none"))
    return out


# ---------------------------------------------------------------- light and the pages
def light_shaft():
    return [poly([(450, 90), (680, 90), (1150, 900), (640, 900)], fill="url(#shaftfade)", filter="url(#soft)")]


def page(cx, cy, w, rot, curl):
    h = w * 1.3
    x0, y0 = -w / 2, -h / 2
    lines = []
    for k in range(7):
        ly = y0 + h * 0.16 + k * h * 0.1
        lw = w * (0.72 if k % 3 != 2 else 0.5)
        lines.append(rect(round(x0 + w * 0.14, 1), round(ly, 1), round(lw, 1), max(1.2, round(h * 0.022, 1)),
                          fill=PAPER2))
    body = [path(f"M{x0:.1f} {y0:.1f} L{x0 + w:.1f} {y0:.1f} L{x0 + w:.1f} {y0 + h - curl:.1f} "
                 f"L{x0 + w - curl:.1f} {y0 + h:.1f} L{x0:.1f} {y0 + h:.1f} Z", fill=PAPER),
            path(f"M{x0 + w:.1f} {y0 + h - curl:.1f} L{x0 + w - curl:.1f} {y0 + h - curl:.1f} "
                 f"L{x0 + w - curl:.1f} {y0 + h:.1f} Z", fill=PAPER2)] + lines
    shadow = rect(round(x0 + 6, 1), round(y0 + 8, 1), round(w, 1), round(h, 1), fill=OX3, opacity=0.25)
    return group([shadow] + body, transform=f"translate({cx:.1f} {cy:.1f}) rotate({rot:.1f})")


def pages():
    """Eight blank pages spiralling up from the speaker's hand toward the skylight."""
    out = []
    hand = (800, 600)
    top = (565, 120)
    for i in range(8):
        t = (i + 1) / 8.6
        ang = t * 2.4 * math.pi + 0.6
        rad = 150 * (1 - t) + 30
        bx = hand[0] + (top[0] - hand[0]) * t
        by = hand[1] + (top[1] - hand[1]) * (t ** 0.9)
        x = bx + rad * math.cos(ang)
        y = by + rad * 0.35 * math.sin(ang)
        w = 74 - 46 * t
        out.append(page(x, y, w, rot=math.degrees(ang) * 0.35 - 25 + R.uniform(-10, 10), curl=w * 0.18))
    # a faint trail of motion linking the pages
    pts = []
    for s in range(60):
        t = s / 60 * 0.95
        ang = t * 2.4 * math.pi + 0.6
        rad = 150 * (1 - t) + 30
        bx = hand[0] + (top[0] - hand[0]) * t
        by = hand[1] + (top[1] - hand[1]) * (t ** 0.9)
        pts.append(f"{bx + rad * math.cos(ang):.1f} {by + rad * 0.35 * math.sin(ang):.1f}")
    trail = path("M" + " L".join(pts), fill="none", stroke=PAPER, stroke_width=3, opacity=0.35,
                 stroke_dasharray="2 12", stroke_linecap="round")
    halo = ellipse(600, 180, 150, 110, fill="#fff1c4", opacity=0.45, filter="url(#soft)")
    return [halo, trail] + out


# ---------------------------------------------------------------- foreground: Massie
def massie():
    look = Look(skin="#e8b896", top="#1c2233", bottom="#161a26", hair="#b9b4ad", hair_style="short",
                accent=FLAG_R, long_tie=True, face="speak", build=0.95,
                extra=[
                    # wire-rimmed glasses on the profile face (head centre is (1.5, -86) in local units)
                    circle(5.3, -87.3, 2.6, fill="none", stroke="#2a2a2a", stroke_width=0.8),
                    path("M2.7 -87.6 L-3 -88.4", stroke="#2a2a2a", stroke_width=0.6),
                ])
    pose = Pose(back_arm=(55, 45), front_arm=(78, -10), back_leg=(-4, 0), front_leg=(4, 0), lean=2, head_tilt=-6)
    held = group([rect(-4, -5, 8, 10, fill=PAPER2), rect(-2, -4, 8, 10, fill=PAPER)])
    fig = figure(930, 950, 600, facing=-1, pose=pose, look=look, hand_items={"back": held})
    # rim light along his back (light comes from the skylight, upper left)
    rim = ellipse(975, 520, 90, 220, fill="#ffe9b0", opacity=0.10, filter="url(#soft)")
    return [rim, fig]


def lectern():
    out = [poly([(700, 700), (920, 700), (950, 900), (670, 900)], fill="url(#lectern)")]
    out.append(poly([(680, 676), (940, 676), (928, 706), (692, 706)], fill=WOOD))
    out.append(rect(680, 670, 260, 8, fill=GOLD2))
    out.append(rect(735, 740, 150, 120, fill="none", stroke=GOLD2, stroke_width=3, opacity=0.7))
    # gooseneck microphone, tip short of his mouth
    out.append(path("M760 676 Q745 590 828 538", stroke="#1a1a1a", stroke_width=4, fill="none"))
    out.append(ellipse(832, 535, 7, 5, fill="#1a1a1a", transform="rotate(-30 832 535)"))
    return out


def build():
    d = defs() + [opacity_stops("shaftfade", "#fff3cf", 0.55, 0.0)]
    body = []
    body += ceiling()
    body += wall()
    body += flag()
    body += rostrum()
    body += seats()
    body += members()
    body += light_shaft()
    body += pages()
    body += massie()
    body += lectern()
    # vignette framing the foreground
    body.append(rect(0, 0, WIDTH, HEIGHT, fill="none", stroke=OX3, stroke_width=60, opacity=0.35, filter="url(#soft)"))
    body.append(grain_overlay(opacity=0.32))
    title = "Massie files articles of impeachment against Hegseth"
    desc = ("Editorial illustration. From a low angle on the House floor, Rep. Thomas Massie, slim with glasses and "
            "grey hair in a dark suit, speaks at a floor lectern toward the Speaker's rostrum, where clerks sit "
            "below a vertical US flag and a few members listen from the benches. Eight blank pages spiral up from "
            "his hand through a shaft of skylight, symbolising the eight articles of impeachment he introduced "
            "against Defense Secretary Pete Hegseth on Nov. 9, 2026.")
    return document(d, body, title, desc)


if __name__ == "__main__":
    save(build(), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
