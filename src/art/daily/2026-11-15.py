"""Daily artwork, 2026-11-15: NTSB says a tanker's steering failed before it hit a docked riverboat.

Visual idea: the runaway bow. From the New Orleans wharf at midday, a tanker's colossal dark
bow towers over a small white riverboat it has just struck, dwarfing it; behind the tanker a
long dashed wake bends hard to starboard across the brown Mississippi, tracing the stuck
rudder, while its anchor chain runs taut into the water. Crew and passengers in orange life
vests hurry down the gangway onto the dock, a harbor patrol boat and a tug close in, and the
steel cantilever trusses of the Crescent City Connection cross the pale sky behind.

Verified (brief): NTSB said Nov. 15 the Atlantic Asphalt's steering failed with the rudder to
starboard; it hit the docked riverboat American Heritage near the Crescent City Connection on
Nov. 13; the riverboat capsized 22 minutes later; more than 80 people were evacuated before it
overturned; all aboard survived; anchor orders were recorded (AP via PBS, Fox News, WCVB).
Drawn: generic tanker and riverboat (no names, liveries or logos), generic people evacuating,
generic responders' boats. Not drawn: anyone in the water, injuries, names, text.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-15"
R = rng(20261115)

# palette: hazy noon butter sky, Mississippi caramel, oxblood hull, riverboat white, slate steel, vest orange
SKY1, SKY2, SKY3 = "#f6efd2", "#f2dca0", "#e9c27a"
MUD, MUD2, MUD3 = "#8a7a48", "#6b5c34", "#3e3420"
OX, OX2, OX3 = "#6e1f24", "#4a1418", "#2a0b0e"
WHITE, WHITE2, WHITE3 = "#fbf8ef", "#dcd6c6", "#a9a294"
STEEL, STEEL2 = "#6f7d78", "#4b5753"
ORANGE, ORANGE2 = "#ff6a1f", "#d94e12"
NAVY, INK = "#22324a", "#1a1414"
WHARF, WHARF2 = "#8c8474", "#5f594e"

WATER = 520  # far bank / waterline


def defs():
    return [
        linear("sky", [(0, SKY1), (0.6, SKY2), (1, SKY3)]),
        linear("river", [(0, MUD), (0.5, MUD2), (1, MUD3)]),
        linear("hull", [(0, OX), (0.55, OX2), (1, OX3)], x2=1, y2=0.3),
        linear("bowlight", [(0, "#9a3a36", 0.9), (1, OX, 0)], x2=1, y2=0),
        radial("sun", [(0, "#fffbea", 1), (0.5, "#fff3c4", 0.7), (1, SKY2, 0)]),
        linear("wharf", [(0, WHARF), (1, WHARF2)]),
        blur("soft", 6), blur("softer", 14), blur("haze", 3),
        halftone("dots", SKY3, dot=1.6, spacing=8),
        halftone("mdots", MUD3, dot=1.4, spacing=7, angle=20),
        halftone("odots", OX3, dot=1.5, spacing=7, angle=60),
        grain_filter(strength=0.5),
    ]


def sky():
    out = [rect(0, 0, 1200, 900, fill="url(#sky)")]
    out.append(rect(0, 0, 1200, 420, fill="url(#dots)", opacity=0.18))
    out.append(circle(930, 120, 230, fill="url(#sun)"))
    out.append(circle(930, 120, 70, fill="#fffbea", opacity=0.9))
    return out


def truss_span(x0, x1, deck, top_at, depth=26):
    """A cantilever truss between x0 and x1; top chord follows a curve peaking at top_at points."""
    out = []
    n = int((x1 - x0) / 22)
    pts_top, pts_bot = [], []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        # top chord height: highest over the towers (top_at list of (x, height))
        h = depth
        for tx, th in top_at:
            h = max(h, th - abs(x - tx) * th / 230)
        pts_top.append((x, deck - h))
        pts_bot.append((x, deck))
    top = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts_top)
    out.append(path(top, fill="none", stroke=STEEL, stroke_width=5))
    out.append(rect(x0, deck - 3, x1 - x0, 9, fill=STEEL2))
    for i in range(n):
        (xa, ya), (xb, yb) = pts_top[i], pts_top[i + 1]
        out.append(path(f"M{xa:.1f} {deck} L{xb:.1f} {yb:.1f}", stroke=STEEL, stroke_width=2.2))
        out.append(path(f"M{xa:.1f} {ya:.1f} L{xa:.1f} {deck}", stroke=STEEL, stroke_width=2.2))
    return out


def bridge():
    """The Crescent City Connection: twin steel cantilever spans high over the river (background)."""
    out = []
    deck = 300
    # piers
    for px in (330, 760):
        out.append(rect(px - 14, deck, 28, WATER - deck, fill=STEEL2, opacity=0.85))
    out += truss_span(-40, 1240, deck, [(330, 150), (760, 150)])
    # second, parallel span peeking behind (twin bridges)
    back = truss_span(-40, 1240, deck - 14, [(345, 140), (775, 140)])
    out.insert(0, group(back, opacity=0.35))
    return [group(out, opacity=0.8)]


def far_bank():
    out = [rect(0, WATER - 22, 1200, 26, fill="#7d8a6a", opacity=0.8)]
    x = 0
    while x < 1200:
        w = R.uniform(30, 80)
        h = R.uniform(14, 60)
        out.append(rect(x, WATER - 20 - h, w, h + 4, fill="#9aa08a", opacity=0.75))
        x += w + R.uniform(4, 20)
    return out


def river():
    out = [rect(0, WATER, 1200, 380, fill="url(#river)")]
    out.append(rect(0, WATER, 1200, 380, fill="url(#mdots)", opacity=0.3))
    # reflection of the tanker's dark hull and of the sky
    out.append(poly([(650, 700), (980, 600), (1220, 560), (1220, 700), (700, 800)], fill=OX3, opacity=0.35,
                    filter="url(#softer)"))
    for _ in range(120):  # ripple dashes
        x = R.uniform(0, 1200)
        y = R.uniform(WATER + 6, 900)
        w = R.uniform(14, 50) * (0.5 + (y - WATER) / 380)
        out.append(rect(round(x, 1), round(y, 1), round(w, 1), 2, fill=SKY1,
                        opacity=round(R.uniform(0.15, 0.45), 2)))
    # glare path from the high sun across the river
    out.append(poly([(860, WATER), (1000, WATER), (1200, 640), (1200, 760)], fill="#fff3c4", opacity=0.18,
                    filter="url(#soft)"))
    for _ in range(50):  # sun glints under the sun
        x = R.uniform(760, 1200)
        y = R.uniform(WATER + 4, 560)
        w = R.uniform(10, 40)
        out.append(rect(round(x, 1), round(y, 1), round(w, 1), 2.2, fill="#fff3c4",
                        opacity=round(R.uniform(0.4, 0.9), 2)))
    return out


def wake():
    """Dashed wake hugging the tanker's waterline, then bending hard away: the swing to starboard."""
    out = []
    for k, (off, op) in enumerate(((0, 0.9), (26, 0.55), (52, 0.3))):
        d = f"M{700} {712 + off * 0.4} C{860} {690 + off} {1000} {720 + off * 1.4} {1240} {860 + off}"
        out.append(path(d, fill="none", stroke=WHITE, stroke_width=7 - 2 * k, stroke_linecap="round",
                        stroke_dasharray="28 18", opacity=op))
    return out


def bow_shadow():
    """The tanker's shadow thrown across the struck end of the riverboat (noon sun high, right)."""
    return [poly([(600, 420), (640, 690), (440, 700), (470, 430)], fill=OX3, opacity=0.3, filter="url(#haze)")]


def tanker():
    """A huge dark tanker bow, seen from low and ahead-left, pressed into the riverboat's end."""
    out = []
    stem_top, stem_bot = (600, 210), (650, 700)
    # port side receding to the right
    side = poly([stem_top, (1220, 360), (1220, 560), (980, 600), stem_bot], fill="url(#hull)")
    out.append(side)
    out.append(poly([stem_top, (1220, 360), (1220, 560), (980, 600), stem_bot], fill="url(#odots)", opacity=0.35))
    for k in range(1, 9):
        x = 600 + k * 70
        yt = 210 + (x - 600) * 150 / 620
        yb = 700 - (x - 650) * 140 / 570 if x < 980 else 600 - (x - 980) * 40 / 240
        out.append(path(f"M{x} {yt + 8:.1f} L{x + 6} {yb - 6:.1f}", stroke=OX3, stroke_width=2, opacity=0.5))
    # rim light along the bow's sunlit edge
    out.append(path("M600 210 L650 700", stroke="#e08a6a", stroke_width=4, opacity=0.8))
    # sunlit bow flare (front face)
    out.append(poly([stem_top, (548, 236), (590, 690), stem_bot], fill="#8e2f30"))
    out.append(poly([stem_top, (548, 236), (590, 690), stem_bot], fill="url(#bowlight)"))
    # red boot-topping band along the waterline and a deck edge rail
    out.append(poly([(640, 640), (1220, 515), (1220, 560), (980, 600), (650, 700)], fill="#b0302a", opacity=0.9))
    out.append(path("M548 236 L600 210 L1220 360", fill="none", stroke=WHITE2, stroke_width=4))
    for k in range(18):
        x = 610 + k * 34
        y = 213 + (x - 600) * 150 / 620
        out.append(rect(x, y - 14, 2.4, 14, fill=WHITE2))
    out.append(path("M600 196 L1220 346", fill="none", stroke=WHITE2, stroke_width=2))
    # hawsepipe and anchor chain running taut into the river
    out.append(ellipse(640, 300, 16, 10, fill=OX3))
    chain = []
    for k in range(16):
        t = k / 15
        cx, cy = 640 - t * 24, 300 + t * 400
        chain.append(ellipse(round(cx, 1), round(cy, 1), 5, 9, fill="none", stroke="#3a3433", stroke_width=3.5,
                             transform=f"rotate({10 if k % 2 else -20} {cx:.1f} {cy:.1f})"))
    out += chain
    out.append(ellipse(614, 706, 34, 7, fill="none", stroke=WHITE, stroke_width=3, opacity=0.8))
    # forward mast with whistle steam
    out.append(rect(700, 120, 6, 120, fill=WHITE3))
    out.append(rect(690, 150, 26, 4, fill=WHITE3))
    out += cloud_puffs(R, 742, 92, 70, 30, 7, 14, 26, fill=WHITE, opacity=0.85)
    # superstructure far aft (right edge)
    out.append(poly([(1090, 220), (1220, 230), (1220, 340), (1090, 330)], fill=WHITE))
    out.append(poly([(1090, 220), (1220, 230), (1220, 242), (1090, 232)], fill=WHITE3))
    for k in range(4):
        out.append(rect(1100 + k * 30, 250, 18, 10, fill=NAVY))
    out.append(rect(1150, 170, 34, 52, fill=OX2))
    # contact splash at the stem
    out += cloud_puffs(R, 618, 690, 90, 24, 9, 10, 22, fill=WHITE, opacity=0.75)
    return out


def riverboat():
    """A generic white multi-deck river cruise boat at the dock, beginning to list after the impact."""
    out = []
    x0, x1, wl = 40, 640, 690
    hull = path(f"M{x0} {wl - 60} L{x1} {wl - 60} L{x1 - 20} {wl} L{x0 + 30} {wl} Z", fill=WHITE)
    out.append(hull)
    out.append(rect(x0, wl - 30, x1 - x0 - 10, 8, fill=NAVY))
    decks = [(wl - 60, 70), (wl - 130, 62), (wl - 192, 56)]
    for i, (base, h) in enumerate(decks):
        inset = 20 + i * 30
        out.append(rect(x0 + inset, base - h, x1 - x0 - inset * 2, h, fill=WHITE if i % 2 == 0 else "#f3efe3"))
        out.append(rect(x0 + inset, base - h, x1 - x0 - inset * 2, 6, fill=WHITE3))
        # window row and balcony rail
        for wx in range(int(x0 + inset + 16), int(x1 - inset - 20), 34):
            out.append(rect(wx, base - h + 16, 22, 26, fill="#5d8fa8", opacity=0.85))
            out.append(rect(wx, base - h + 16, 22, 6, fill="#cfe3ea", opacity=0.7))
        out.append(rect(x0 + inset, base - 14, x1 - x0 - inset * 2, 3, fill=WHITE3))
    # pilot house and stack
    out.append(rect(300, wl - 300, 110, 50, fill=WHITE))
    out.append(rect(310, wl - 290, 90, 20, fill="#5d8fa8"))
    out.append(rect(360, wl - 340, 26, 42, fill=NAVY))
    # crumpled stern end where the bow struck (right end)
    out.append(poly([(x1 - 40, wl - 250), (x1 - 6, wl - 200), (x1 + 6, wl - 120), (x1 - 10, wl - 60),
                     (x1 - 50, wl - 110)], fill=WHITE2))
    out.append(path(f"M{x1 - 44} {wl - 230} L{x1 - 20} {wl - 170} L{x1 - 34} {wl - 120} L{x1 - 12} {wl - 80}",
                    fill="none", stroke=WHITE3, stroke_width=3))
    # list: tilt away from the dock around the waterline at the bow end
    return [group(out, transform=f"rotate(-3 {x0} {wl})")]


def responders():
    out = []
    # harbor patrol boat (generic, light bar)
    bx, by = 860, 760
    out.append(path(f"M{bx - 110} {by - 30} L{bx + 90} {by - 30} L{bx + 120} {by - 46} L{bx + 100} {by} L{bx - 100} {by} Z",
                    fill=WHITE))
    out.append(rect(bx - 100, by - 18, 196, 7, fill=NAVY))
    out.append(rect(bx - 60, by - 70, 80, 40, fill=NAVY))
    out.append(rect(bx - 52, by - 64, 64, 16, fill="#9fd0e4"))
    out.append(rect(bx - 40, by - 80, 40, 8, fill="#e8342c"))
    out.append(rect(bx - 20, by - 80, 20, 8, fill="#2c63e8"))
    out.append(circle(bx - 30, by - 76, 16, fill="#e8342c", opacity=0.35, filter="url(#soft)"))
    out.append(path(f"M{bx + 120} {by - 4} Q{bx + 200} {by + 8} {bx + 300} {by - 2}", fill="none", stroke=WHITE,
                    stroke_width=5, opacity=0.7, stroke_dasharray="20 12"))
    # two crew on deck reaching toward the riverboat
    out.append(figure(bx + 40, by - 30, 74, facing=-1, pose=Pose(front_arm=(110, 10), back_arm=(70, 20)),
                      look=Look(skin="#8d5a3f", top=ORANGE, bottom=NAVY, hair_style="cap", hair=NAVY)))
    out.append(figure(bx + 70, by - 30, 72, facing=-1, pose=Pose(front_arm=(60, 30)),
                      look=Look(skin="#e0b394", top=NAVY, bottom=NAVY, hair_style="cap", hair=NAVY, vest=True)))
    # tug nosing against the tanker (right, mid distance)
    tx, ty = 1060, 640
    out.append(path(f"M{tx - 70} {ty - 20} L{tx + 60} {ty - 20} L{tx + 70} {ty} L{tx - 80} {ty} Z", fill="#1f3b5a"))
    out.append(rect(tx - 30, ty - 52, 60, 32, fill=WHITE))
    out.append(rect(tx - 22, ty - 46, 44, 10, fill=NAVY))
    out.append(rect(tx + 6, ty - 80, 14, 28, fill=ORANGE2))
    out.append(rect(tx - 80, ty - 14, 10, 14, fill=INK))
    return out


def wharf():
    """The dock in the foreground, with the gangway down from the riverboat."""
    out = [poly([(0, 720), (700, 720), (760, 900), (0, 900)], fill="url(#wharf)")]
    out.append(rect(0, 712, 702, 12, fill=WHARF2))
    for bx in (90, 380, 620):
        out.append(rect(bx - 12, 690, 24, 26, rx=8, fill=INK))
        out.append(path(f"M{bx} 694 Q{bx - 60} 650 {bx - 100} 640", fill="none", stroke="#c7b48a", stroke_width=4))
    # gangway from the lower deck down to the wharf
    out.append(poly([(150, 610), (190, 610), (270, 730), (226, 730)], fill=WHITE3))
    out.append(path("M150 590 L226 712", stroke=WHITE2, stroke_width=3))
    out.append(path("M190 590 L270 712", stroke=WHITE2, stroke_width=3))
    # short noon shadows
    out.append(rect(0, 724, 700, 14, fill=INK, opacity=0.18))
    return out


def evacuees():
    out = []
    sh = lambda x, y, w=34: ellipse(x, y + 3, w, 6, fill=INK, opacity=0.35)
    vest_extra = lambda: []
    people = [
        # x, y, h, facing, pose, look
        (190, 640, 92, 1, Pose(back_arm=(-20, 10), front_arm=(30, 20), back_leg=(-18, 0), front_leg=(16, 0)),
         Look(skin="#e0b394", top=ORANGE, bottom="#3c4a6a", hair="#c7a46a", hair_style="short")),
        (228, 690, 100, 1, Pose(back_arm=(-25, 10), front_arm=(35, 15), back_leg=(-22, 0), front_leg=(18, 0)),
         Look(skin="#8d5a3f", top=ORANGE, bottom="#2b2b38", hair="#140f12", hair_style="bun")),
        # crew member at the foot of the gangway waving people on
        (300, 800, 150, -1, Pose(back_arm=(-10, 10), front_arm=(130, 40), back_leg=(-6, 0), front_leg=(8, 0),
                                 head_tilt=-6),
         Look(skin="#a86d4e", top=NAVY, bottom=NAVY, hair="#1d1514", hair_style="cap", vest=True, face="shout")),
        # passengers hurrying across the dock toward the viewer
        (400, 850, 170, -1, Pose(back_arm=(-30, 20), front_arm=(30, 30), back_leg=(-24, -12), front_leg=(22, 0),
                                 lean=8),
         Look(skin="#f0c8a8", top=ORANGE, bottom="#5a4a3a", hair="#ece6da", hair_style="short")),
        (470, 836, 156, -1, Pose(back_arm=(-20, 30), front_arm=(60, 70), back_leg=(-22, -10), front_leg=(20, 0),
                                 lean=6),
         Look(skin="#c48c68", top=ORANGE, bottom="#2f2a40", hair="#5a3420", hair_style="long")),
        (120, 860, 176, 1, Pose(back_arm=(-15, 10), front_arm=(95, 10), back_leg=(-6, 0), front_leg=(8, 0),
                                head_tilt=-14),
         Look(skin="#d9a27e", top=ORANGE, bottom="#24304a", hair="#8a8a8a", hair_style="short")),
    ]
    # passengers on the lower deck, moving along the rail toward the gangway
    for x, top, hair in ((330, "#3a5f8a", "#2a1d18"), (390, ORANGE, "#c7a46a"), (450, ORANGE, "#140f12")):
        people.append((x, 618, 70, -1, Pose(back_arm=(-25, 10), front_arm=(30, 20), back_leg=(-18, 0),
                                            front_leg=(16, 0)),
                       Look(skin="#c48c68", top=top, bottom="#2b2b38", hair=hair)))
    for x, y, h, f, p, lk in people:
        out.append(sh(x, y))
        out.append(figure(x, y, h, facing=f, pose=p, look=lk))
    return out


def build():
    d = defs()
    body = []
    body += sky()
    body += bridge()
    body += far_bank()
    body += river()
    body += wake()
    body += tanker()
    body += riverboat()
    body += bow_shadow()
    body += responders()
    body += wharf()
    body += evacuees()
    body.append(rect(0, 0, WIDTH, HEIGHT, fill="none", stroke=MUD3, stroke_width=50, opacity=0.35, filter="url(#soft)"))
    body.append(grain_overlay(opacity=0.3))
    title = "NTSB: a tanker's steering failed before it struck a docked riverboat in New Orleans"
    desc = ("Editorial illustration. At midday on the Mississippi River in New Orleans, the towering dark bow of a "
            "tanker has struck the end of a small white multi-deck riverboat moored at a wharf; the riverboat is "
            "beginning to list. Behind the tanker a dashed wake curves sharply across the brown river, an "
            "illustrative trace of the steering failure that held its rudder to starboard, and its anchor chain runs "
            "down into the water. People in orange life vests hurry down the gangway and across the dock as a crew "
            "member waves them on; a harbor patrol boat and a tug approach. Steel cantilever bridge trusses cross the "
            "pale sky. It represents the NTSB's Nov. 15, 2026 preliminary finding about the Nov. 13 collision of "
            "the tanker Atlantic Asphalt with the riverboat American Heritage, in which everyone aboard survived.")
    return document(d, body, title, desc)


if __name__ == "__main__":
    save(build(), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
