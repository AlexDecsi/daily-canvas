"""Daily artwork, 2026-11-07: Trump offers UFC chief Dana White the White House press secretary job.

Visual idea: one man, two stages. A hard diagonal splits the canvas: on the left,
Dana White sits at a fight-night news conference in London, blasted by stage
lights, microphones bristling and ring ropes behind him; on the right, the
White House briefing-room podium waits EMPTY under a lone spotlight before rows
of empty seats. An overnight jet's contrail arcs from his side of the frame
across the divide toward the podium: he said he was flying to Washington for a
Monday meeting, and the offer is still unanswered.

Verified (brief): on Nov. 7, 2026, Trump said on Truth Social he had offered
White the press secretary job; at a London news conference White said he was
flying to Washington for a Monday meeting and did not say if he would accept
(CBS News, ESPN, NBC News). The post has been vacant since mid-October.
Drawn: White (bald, dark suit, open collar) at a press table in London; the
podium empty because nothing is decided. The jet is a symbol of his trip.
Not drawn: no Trump figure, no text or logos, White not shown at the podium.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-07"
R = rng(20261107)

# fight night: black, tangerine, hot white light
BLK, BLK2, SMOKE = "#0d0b10", "#1c1820", "#2c2630"
TANG, TANG2, AMBER = "#ff6a1f", "#c8431a", "#ffb347"
HOT = "#fff6e6"
# briefing room: ultramarine, navy, gold
ULTRA, ULTRA2, NAVY, NAVY2 = "#2a49c4", "#1d3592", "#101d55", "#0a1238"
GOLD, GOLD2 = "#f2c14e", "#b8862b"
WOOD, WOOD2 = "#8a5a33", "#5e3a20"
ICE = "#dfe8ff"

# the diagonal divide: top x, bottom x
DTOP, DBOT = 720, 560


def divide_x(y):
    return DTOP + (DBOT - DTOP) * y / HEIGHT


LEFT = [(0, 0), (DTOP, 0), (DBOT, HEIGHT), (0, HEIGHT)]
RIGHT = [(DTOP, 0), (WIDTH, 0), (WIDTH, HEIGHT), (DBOT, HEIGHT)]


# ---------------------------------------------------------------- left: London fight night
def london():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#arena)")]
    # crowd haze dots in the dark arena
    for _ in range(260):
        x, y = R.uniform(0, 760), R.uniform(250, 470)
        out.append(circle(round(x, 1), round(y, 1), round(R.uniform(1, 3), 1), fill=AMBER,
                          opacity=round(R.uniform(0.08, 0.35), 2)))
    # stage light cones from the rig
    for lx, tx, w in ((90, 300, 150), (330, 380, 170), (560, 470, 140)):
        out.append(poly([(lx - 10, 40), (lx + 10, 40), (tx + w, 700), (tx - w, 700)], fill="url(#beam)"))
    # lighting truss
    out.append(rect(0, 30, 760, 14, fill=SMOKE))
    for x in range(0, 760, 24):
        out.append(path(f"M{x} 30 L{x + 12} 44 L{x + 24} 30", stroke=BLK2, stroke_width=2, fill="none"))
    for lx in (90, 330, 560):
        out.append(rect(lx - 16, 40, 32, 22, rx=4, fill=BLK))
        out.append(ellipse(lx, 62, 14, 5, fill=HOT))
    # ring: corner post and three ropes behind the table
    out.append(rect(36, 330, 22, 330, fill=BLK2))
    out.append(rect(32, 326, 30, 18, rx=4, fill=TANG))
    for k, y in enumerate((370, 430, 490)):
        out.append(path(f"M58 {y} Q400 {y + 14} 760 {y - 26}", stroke=TANG if k != 1 else HOT, stroke_width=7,
                        fill="none", opacity=0.9))
    # ring apron / backdrop panel (blank, no logos)
    out.append(rect(0, 560, 760, 100, fill=BLK2))
    out.append(rect(0, 556, 760, 6, fill=TANG2))
    return out


def white():
    out = []
    # rim of hot light behind him
    out.append(circle(330, 500, 210, fill="url(#halo)"))
    suit = "#18161d"
    look = Look(skin="#e9b294", top=suit, bottom=suit, hair="#e9b294", hair_style="bald", accent=HOT,
                face="speak", build=1.3)
    # seated: feet hidden below the table edge
    out.append(figure(320, 900, 460, facing=1,
                      pose=Pose(back_arm=(40, 50), front_arm=(46, 44), lean=4, head_tilt=-3), look=look))
    # cool light from the briefing room falls across the divide onto his face
    out.append(poly([(DTOP - 40, 120), (DTOP, 120), (420, 600), (330, 520)], fill="url(#spill)"))
    # rim light on scalp and shoulder
    out.append(path("M300 474 q 22 -18 50 -4", stroke=HOT, stroke_width=5, fill="none", stroke_linecap="round"))
    out.append(path("M276 580 q 30 -16 66 -8", stroke=AMBER, stroke_width=3, fill="none", opacity=0.8))
    return out


def table():
    out = []
    # tabletop and drape
    out.append(rect(60, 652, 600, 16, fill="#3a3340"))
    out.append(rect(70, 668, 580, 160, fill="url(#drape)"))
    out.append(rect(70, 668, 580, 8, fill=TANG))
    # a water bottle and glass
    out.append(rect(520, 606, 18, 46, rx=6, fill=ICE, opacity=0.55))
    out.append(rect(524, 598, 10, 10, rx=2, fill="#5aa0ff", opacity=0.8))
    out.append(rect(552, 622, 20, 30, fill=ICE, opacity=0.35))
    # bristling microphones aimed at White, flags in plain colours (no text)
    mics = [(430, 652, 404, 566, TANG), (462, 652, 418, 584, HOT), (494, 652, 432, 572, AMBER),
            (410, 652, 398, 600, ULTRA), (520, 652, 444, 604, TANG2), (448, 652, 420, 616, HOT)]
    for x0, y0, x1, y1, col in mics:
        out.append(path(f"M{x0} {y0} L{x1} {y1}", stroke=BLK, stroke_width=5))
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        out.append(group([rect(-14, -9, 20, 18, rx=3, fill=col), ellipse(-20, 0, 9, 8, fill=BLK2)],
                         transform=f"translate({x1} {y1}) rotate({ang + 180:.0f})"))
    return out


def reporters():
    """Generic silhouetted reporters in the foreground, phones and cameras raised."""
    out = []
    sil = dict(skin=BLK, top=BLK, bottom=BLK, hair=BLK, shoes=BLK)
    phone = group([rect(-6, -12, 12, 22, rx=2, fill=BLK), rect(-4, -10, 8, 17, rx=1, fill="#9fc4ff")],
                  transform="scale(0.8)")
    cam = group([rect(-12, -16, 34, 24, fill=BLK, rx=3), circle(22, -4, 9, fill=SMOKE)], transform="scale(0.6)")
    for x, h, style, item in ((60, 330, "short", cam), (190, 300, "long", phone), (480, 320, "cap", cam),
                              (610, 290, "bun", phone)):
        out.append(figure(x, HEIGHT + 120, h, facing=1 if x < 330 else -1,
                          pose=Pose(back_arm=(-10, 10), front_arm=(130, -45), lean=-3),
                          look=Look(hair_style=style, **sil), hand_items={"front": item}))
    for x, h in ((60, 330), (190, 300), (480, 320), (610, 290)):
        hy = HEIGHT + 120 - 90 * h / 100
        out.append(path(f"M{x - 7 * h / 100:.0f} {hy - 2:.0f} q {8 * h / 100:.0f} {-9 * h / 100:.0f} {16 * h / 100:.0f} 0",
                        stroke=AMBER, stroke_width=3, fill="none", opacity=0.75, stroke_linecap="round"))
    # camera flashes
    for fx, fy, r in ((150, 610, 46), (560, 640, 34)):
        pts = []
        for k in range(16):
            a = k * math.pi / 8
            rr = r if k % 2 == 0 else r * 0.26
            pts.append((round(fx + rr * math.cos(a), 1), round(fy + rr * math.sin(a), 1)))
        out.append(poly(pts, fill=HOT, opacity=0.9))
    return out


# ---------------------------------------------------------------- right: the empty briefing room
def briefing_room():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#curtain)")]
    # curtain folds
    for x in range(560, 1200, 34):
        out.append(rect(x, 0, 14, 700, fill=NAVY, opacity=0.35))
        out.append(rect(x + 18, 0, 5, 700, fill=ICE, opacity=0.08))
    # valance
    out.append(rect(560, 0, 640, 46, fill=NAVY2))
    for x in range(560, 1200, 40):
        out.append(path(f"M{x} 46 Q{x + 20} 66 {x + 40} 46 Z", fill=NAVY2))
    # blank oval plaque on the curtain (no seal detail, no text)
    out.append(ellipse(960, 300, 104, 76, fill=GOLD2))
    out.append(ellipse(960, 300, 96, 69, fill=GOLD))
    out.append(ellipse(960, 300, 80, 56, fill=NAVY))
    out.append(ellipse(960, 300, 66, 44, fill="none", stroke=GOLD, stroke_width=2, opacity=0.7))
    # floor / stage riser
    out.append(rect(560, 700, 640, 200, fill=NAVY2))
    out.append(rect(560, 700, 640, 8, fill=ULTRA2))
    return out


def spotlight_and_podium():
    out = []
    # a single spotlight cone onto the podium
    out.append(poly([(1050, -10), (1110, -10), (1110, 760), (810, 760)], fill="url(#spot)"))
    out.append(ellipse(960, 744, 170, 26, fill=ICE, opacity=0.25))
    # long shadow of the podium cast to the left
    out.append(poly([(900, 742), (1000, 742), (850, 780), (730, 780)], fill=BLK, opacity=0.35))
    # podium: tapered wood lectern with a blank oval medallion
    out.append(poly([(890, 470), (1030, 470), (1012, 742), (908, 742)], fill="url(#wood)"))
    out.append(poly([(876, 452), (1044, 452), (1036, 476), (884, 476)], fill=WOOD))
    out.append(rect(884, 470, 152, 6, fill=GOLD, opacity=0.8))
    out.append(ellipse(960, 560, 34, 30, fill=GOLD))
    out.append(ellipse(960, 560, 26, 22, fill=NAVY))
    for x in (918, 1002):  # side trim
        out.append(path(f"M{x} 500 L{x + (6 if x > 960 else -6)} 720", stroke=GOLD2, stroke_width=3))
    # two microphone stems on the podium, angled at an empty spot
    out.append(path("M944 452 Q938 420 952 400", stroke=BLK2, stroke_width=4, fill="none"))
    out.append(path("M976 452 Q982 420 968 400", stroke=BLK2, stroke_width=4, fill="none"))
    out.append(ellipse(952, 398, 5, 7, fill=BLK2))
    out.append(ellipse(968, 398, 5, 7, fill=BLK2))
    return out


def empty_seats():
    out = []
    for row, (y, h, gap) in enumerate(((800, 70, 112), (858, 90, 134))):
        offset = 20 if row else 70
        for k in range(8):
            x = 560 + offset + k * gap
            if x - 40 < divide_x(y) - 10:
                continue
            out.append(rect(x - 44, y - h, 88, h + 40, rx=14, fill=ULTRA2 if row else ULTRA))
            out.append(rect(x - 44, y - h, 88, 10, rx=5, fill=ICE, opacity=0.18))
    return out


# ---------------------------------------------------------------- linking elements
def contrail():
    """An overnight flight arc from London toward Washington, crossing the divide."""
    out = []
    d = "M120 250 C 340 110, 640 70, 880 150"
    out.append(path(d, stroke=HOT, stroke_width=10, fill="none", opacity=0.18, stroke_linecap="round"))
    out.append(path(d, stroke=HOT, stroke_width=3.5, fill="none", stroke_dasharray="16 12", stroke_linecap="round"))
    # jet silhouette at the head of the arc, heading right and slightly down
    jet = group([path("M-34 0 L30 -3 Q40 0 30 3 Z", fill=HOT),
                 path("M-2 -2 L-18 -24 L-8 -24 L10 -2 Z", fill=HOT),
                 path("M-2 2 L-18 24 L-8 24 L10 2 Z", fill=HOT),
                 path("M-30 -1 L-38 -12 L-32 -12 L-24 -1 Z", fill=HOT)],
                transform="translate(905 164) rotate(18) scale(1.15)")
    out.append(jet)
    return out


def divide_line():
    return [path(f"M{DTOP} 0 L{DBOT} {HEIGHT}", stroke=BLK, stroke_width=16),
            path(f"M{DTOP + 7} 0 L{DBOT + 7} {HEIGHT}", stroke=GOLD, stroke_width=4)]


def defs():
    return [
        el("clipPath", [poly(LEFT)], id="cl"),
        el("clipPath", [poly(RIGHT)], id="cr"),
        linear("arena", [(0, BLK), (0.6, "#24151a"), (1, BLK)]),
        linear("beam", [(0, "rgba(255,246,230,0.55)"), (1, "rgba(255,246,230,0.04)")]),
        radial("halo", [(0, "rgba(255,179,71,0.55)"), (1, "rgba(255,106,31,0)")]),
        linear("drape", [(0, "#6a2e14"), (0.5, "#3c1d14"), (1, "#24151a")]),
        linear("curtain", [(0, ULTRA2), (0.6, ULTRA), (1, NAVY)]),
        linear("spot", [(0, "rgba(223,232,255,0.05)"), (1, "rgba(223,232,255,0.42)")]),
        linear("wood", [(0, WOOD), (0.5, "#a46d40"), (1, WOOD2)], x2=1, y2=0),
        linear("spill", [(0, "rgba(223,232,255,0.0)"), (1, "rgba(223,232,255,0.28)")]),
        grain_filter(),
    ]


def main():
    left = group(london() + white() + table() + reporters(), clip_path="url(#cl)")
    right = group(briefing_room() + spotlight_and_podium() + empty_seats(), clip_path="url(#cr)")
    body = [left, right] + divide_line() + contrail()
    body.append(grain_overlay(opacity=0.3))
    title = "One man, two stages: Trump offers UFC chief Dana White the press secretary job"
    desc = ("Editorial illustration split by a diagonal. On the left, in an orange-and-black fight-night setting in "
            "London, Dana White, bald and in a dark suit with an open collar, speaks at a news-conference table "
            "crowded with microphones under stage lights, with boxing-ring ropes behind him and silhouetted reporters "
            "raising cameras and phones. On the right, the White House briefing-room podium stands empty under a "
            "single spotlight in front of a blue curtain and empty seats. A dashed jet contrail arcs from his side "
            "toward the podium. Represents President Trump saying on Nov. 7, 2026, that he offered White the vacant "
            "press secretary job, and White saying in London he would fly to Washington for a Monday meeting; the "
            "empty podium shows the offer is unanswered, and the jet is a symbol, not a reported flight path.")
    save(document(defs(), body, title, desc), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")


if __name__ == "__main__":
    main()
