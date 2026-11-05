"""Daily artwork, 2026-11-04: Democrats win control of the House and Senate.

Visual idea: dawn the morning after, seen from low on the Capitol's east plaza.
The rising sun behind us lights the marble east front a warm apricot while a
towering stylized blue wave swells up behind the building and curls above the
dome like a second sky, dwarfing it; at our feet a tiny TV crew and early
passers-by cast long shadows that stretch toward the steps: the day Congress
changed hands, before anyone has gone inside.

Verified (brief): on Nov. 4, the day after the midterms, CBS News projected
Democratic majorities in both the House and the Senate (also NBC News, WCVB, NYT);
Speaker Mike Johnson said he won't stay on as GOP leader (NBC; Axios, NPR).
Drawn: the US Capitol east front from known features: cast-iron dome with ribs,
peristyle drum, lantern and Statue of Freedom; central portico with pediment on
the steps; House wing (south, viewer's left) and Senate wing (north, viewer's
right) each with its own portico. The wave is a symbol of the widely used phrase
"blue wave", not a real event. The crew and passers-by are generic.
Not drawn: no real people or likenesses, no text, flags, signs, numbers or seat
counts, no damage to the building, no undecided races.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import HAIR, SKIN, WALK, Look, Pose, figure  # noqa: E402

DATE = "2026-11-04"
R = rng(20261104)

NAVY, NAVY2, COBALT, ULTRA, SKY, FOAM = "#0a1a45", "#132a6b", "#1f4fb8", "#3576e6", "#86bcff", "#eaf4ff"
DUSK = "#2a2560"
PEACH, APRICOT, SUN = "#ffc59b", "#ff9a66", "#ffe2b8"
MARBLE, MARBLE2, MARBLE3 = "#fff1e2", "#f1d3bb", "#d9a98c"
SHADOW = "#7a5a78"
PAVE, PAVE2 = "#c9876a", "#a86a58"
INK = "#1a1433"
BASE_Y = 640          # where the building meets the plaza


def sky():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#sky)")]
    out.append(rect(0, 0, WIDTH, 700, fill="url(#stars)", opacity=0.18))
    return out


def wave():
    """A great breaking swell rising behind the Capitol, its crest curling over the dome (symbolic)."""
    out = []
    # rear swell rising from the lower left and climbing to a crest at upper right
    body = ("M-60 600 C 40 420 140 300 300 230 C 470 156 640 110 800 80 "
            "C 930 58 1050 80 1110 150 C 1160 210 1150 300 1090 330 "
            "C 1040 354 990 320 1000 270 C 1010 230 1050 228 1070 250 "
            "C 1060 200 1000 170 940 176 C 1060 260 1230 380 1260 600 Z")
    out.append(path(body, fill="url(#wavebody)"))
    out.append(path(body, fill="url(#wavedots)", opacity=0.3))
    # the curling lip: a tongue of water folding forward and down, with a shadowed hollow inside
    out.append(path("M860 100 C 990 80 1110 120 1140 210 C 1160 280 1110 330 1060 316 "
                    "C 1020 304 1010 262 1040 246 C 1000 232 960 250 950 290 "
                    "C 940 220 900 160 860 140 Z", fill=COBALT))
    out.append(path("M1040 246 C 1010 262 1020 304 1060 316 C 1010 316 970 300 950 290 C 960 250 1000 232 1040 246 Z",
                    fill=NAVY))
    # pale inner face of the lip
    out.append(path("M800 80 C 930 58 1050 80 1110 150 C 1160 210 1150 300 1090 330 "
                    "C 1130 290 1130 220 1090 170 C 1040 112 940 96 860 104 Z", fill=SKY, opacity=0.75))
    # flowing water lines following the swell
    for i in range(8):
        k = i * 34
        out.append(path(f"M{-60 + i * 6} {640 - i * 8} C {120 + k * 0.3} {420 - k * 0.2} {420 + k * 0.4} {200 + k * 0.55} {760 + k * 0.4} {150 + k * 0.6}",
                        fill="none", stroke=SKY if i % 2 == 0 else ULTRA, stroke_width=5 if i % 2 == 0 else 3,
                        opacity=0.6 - i * 0.05, stroke_linecap="round"))
    # foam rim along the crest, breaking into claw-like fingers over the lip
    rim = [(300, 230), (380, 196), (460, 166), (540, 140), (620, 120), (700, 100), (780, 86), (860, 76),
           (940, 76), (1010, 90), (1070, 118), (1116, 160), (1140, 210), (1136, 262), (1100, 304), (1060, 316)]
    d = "M" + " L".join(f"{x} {y}" for x, y in rim)
    out.append(path(d, fill="none", stroke=FOAM, stroke_width=16, stroke_linecap="round", stroke_linejoin="round"))
    for i, (x, y) in enumerate(rim):
        r = 8 + min(i, 10) * 1.2
        out.append(circle(x, y - 4, r, fill=FOAM))
        out.append(circle(x + r * 0.8, y - r * 0.3, r * 0.65, fill=FOAM))
    for (x, y), a in zip(rim[6:], (-40, -25, -5, 15, 35, 55, 75, 95)):
        for j in range(3):
            ang = math.radians(a + j * 14 - 14)
            L = 34 + j * 6
            x2, y2 = x + math.cos(ang) * L, y - math.sin(ang) * L * -1 - 20
            out.append(path(f"M{x} {y} Q{x + (x2 - x) * 0.4} {y - 30} {x2:.1f} {y2:.1f}", fill="none", stroke=FOAM,
                            stroke_width=7 - j * 1.5, stroke_linecap="round"))
            out.append(circle(x2, y2, 4.5 - j, fill=FOAM))
    # spray flung up from the crest only
    for _ in range(40):
        x = R.uniform(760, 1150)
        y = R.uniform(20, 70) + (abs(x - 950) / 6)
        out.append(circle(x, y, R.uniform(2, 5), fill=FOAM, opacity=R.uniform(0.5, 0.95)))
    return out


def column_row(x0, x1, top, bottom, n, w):
    out = []
    step = (x1 - x0) / (n - 1)
    for i in range(n):
        x = x0 + i * step
        out.append(rect(x - w / 2, top, w, bottom - top, fill=MARBLE))
        out.append(rect(x + w * 0.15, top, w * 0.35, bottom - top, fill=MARBLE2))
        out.append(rect(x - w / 2 - 3, top - 6, w + 6, 6, fill=MARBLE2))   # capital
        out.append(rect(x - w / 2 - 3, bottom, w + 6, 5, fill=MARBLE2))    # base
    return out


def portico(cx, width, top, bottom, n, col_w, ped_h):
    """A temple-front portico: pediment, entablature, columns, dark recess behind."""
    x0, x1 = cx - width / 2, cx + width / 2
    out = [rect(x0 + 10, top + 24, width - 20, bottom - top - 24, fill=SHADOW, opacity=0.85)]
    out += column_row(x0 + 22, x1 - 22, top + 26, bottom, n, col_w)
    out.append(rect(x0, top, width, 26, fill=MARBLE))
    out.append(rect(x0, top + 18, width, 6, fill=MARBLE3))
    out.append(poly([(x0 - 6, top), (cx, top - ped_h), (x1 + 6, top)], fill=MARBLE))
    out.append(poly([(x0 + 22, top - 6), (cx, top - ped_h + 14), (x1 - 22, top - 6)], fill=MARBLE2))
    return out


def wing(x0, x1, cx_portico):
    """A legislative wing: long marble block with pilasters, windows and its own portico."""
    top = 470
    out = [rect(x0, top, x1 - x0, BASE_Y - top, fill=MARBLE)]
    out.append(rect(x0, top, x1 - x0, 14, fill=MARBLE2))
    out.append(rect(x0, top + 40, x1 - x0, 4, fill=MARBLE2))
    out.append(rect(x0 - 4, top - 10, x1 - x0 + 8, 12, fill=MARBLE))        # balustrade cap
    for x in range(int(x0) + 8, int(x1) - 4, 12):
        out.append(rect(x, top - 4, 5, 8, fill=MARBLE2))
    # windows in two storeys
    for x in range(int(x0) + 22, int(x1) - 20, 34):
        if abs(x - cx_portico) < 120:
            continue
        out.append(rect(x, top + 60, 14, 34, fill=SHADOW, opacity=0.7))
        out.append(rect(x, top + 120, 14, 28, fill=SHADOW, opacity=0.7))
    out += portico(cx_portico, 220, 452, BASE_Y - 20, 8, 12, 52)
    out.append(rect(cx_portico - 130, BASE_Y - 20, 260, 20, fill=MARBLE2))  # steps
    for i in range(3):
        out.append(rect(cx_portico - 130 + i * 6, BASE_Y - 20 + i * 7, 260 - i * 12, 2, fill=MARBLE3))
    # warm sunlight on the right side of each pilaster block
    out.append(rect(x0, top, x1 - x0, BASE_Y - top, fill="url(#facelight)", opacity=0.5))
    return out


def center_block():
    out = []
    x0, x1, top = 380, 820, 410
    out.append(rect(x0, top, x1 - x0, BASE_Y - top, fill=MARBLE))
    out.append(rect(x0 - 4, top - 10, x1 - x0 + 8, 12, fill=MARBLE))
    for x in range(x0 + 8, x1 - 4, 12):
        out.append(rect(x, top - 4, 5, 8, fill=MARBLE2))
    # central east portico, raised on its grand stair
    out += portico(600, 300, 400, 560, 10, 14, 70)
    # great stair
    for i in range(10):
        y = 560 + i * 8
        out.append(rect(440 - i * 8, y, 320 + i * 16, 8, fill=MARBLE if i % 2 else MARBLE2))
    # stair cheek blocks
    out.append(rect(400, 540, 40, 100, fill=MARBLE2))
    out.append(rect(760, 540, 40, 100, fill=MARBLE2))
    return out


def dome():
    out = []
    cx = 600
    # base attic and lower drum
    out.append(rect(cx - 170, 340, 340, 62, fill=MARBLE))
    out.append(rect(cx - 170, 340, 340, 8, fill=MARBLE2))
    out.append(rect(cx - 176, 332, 352, 10, fill=MARBLE))
    # peristyle: ring of columns around the drum
    out.append(rect(cx - 150, 262, 300, 74, fill=SHADOW, opacity=0.8))
    for i in range(15):
        t = (i - 7) / 7.0
        x = cx + math.sin(t * math.pi / 2) * 150
        w = 10 * math.cos(t * math.pi / 2.4) + 3
        out.append(rect(x - w / 2, 266, w, 68, fill=MARBLE))
    out.append(rect(cx - 160, 252, 320, 16, fill=MARBLE))
    out.append(rect(cx - 160, 262, 320, 4, fill=MARBLE3))
    # upper drum with tall windows
    out.append(rect(cx - 132, 200, 264, 54, fill=MARBLE))
    for i in range(11):
        x = cx - 110 + i * 22
        out.append(rect(x - 4, 212, 8, 32, rx=4, fill=SHADOW, opacity=0.75))
    out.append(rect(cx - 140, 194, 280, 10, fill=MARBLE2))
    # the dome shell with ribs
    out.append(path(f"M{cx - 128} 196 C {cx - 124} 120 {cx - 60} 84 {cx} 82 C {cx + 60} 84 {cx + 124} 120 {cx + 128} 196 Z",
                    fill=MARBLE))
    out.append(path(f"M{cx + 20} 84 C {cx + 70} 92 {cx + 124} 130 {cx + 128} 196 L{cx + 40} 196 Z", fill=MARBLE2, opacity=0.8))
    for k in range(-5, 6):
        x = cx + k * 23
        out.append(path(f"M{x} 196 Q{cx + k * 13} 120 {cx + k * 4} 86", fill="none", stroke=MARBLE3, stroke_width=2.5))
    for j, y in enumerate((170, 145, 122)):
        half = 128 - j * 18 - (8 if j else 0)
        for k in range(-4, 5):
            out.append(rect(cx + k * half / 4.6 - 2.5, y - 6, 5, 9, rx=2, fill=SHADOW, opacity=0.5))
    # lantern and Statue of Freedom silhouette
    out.append(rect(cx - 20, 50, 40, 36, fill=MARBLE))
    for k in range(-2, 3):
        out.append(rect(cx + k * 8 - 2, 56, 4, 22, fill=SHADOW, opacity=0.7))
    out.append(path(f"M{cx - 24} 52 Q{cx} 34 {cx + 24} 52 Z", fill=MARBLE2))
    out.append(rect(cx - 5, 26, 10, 12, fill=MARBLE2))
    out.append(path(f"M{cx - 6} 28 L{cx - 4} 6 Q{cx} 0 {cx + 4} 6 L{cx + 6} 28 Z", fill=INK))
    out.append(path(f"M{cx - 4} 6 Q{cx} -6 {cx + 5} 4", fill="none", stroke=INK, stroke_width=3))
    # sunlit rim on the dome (sun is low behind the viewer)
    out.append(path(f"M{cx - 128} 196 C {cx - 124} 120 {cx - 60} 84 {cx} 82", fill="none", stroke=SUN, stroke_width=4, opacity=0.8))
    return out


def plaza():
    out = [poly([(0, BASE_Y), (WIDTH, BASE_Y), (WIDTH, HEIGHT), (0, HEIGHT)], fill="url(#plaza)")]
    # perspective paving lines converging on the central stair
    for i in range(-8, 9):
        out.append(path(f"M{600 + i * 40} {BASE_Y} L{600 + i * 210} {HEIGHT}", stroke=PAVE2, stroke_width=2, opacity=0.6))
    for i in range(1, 7):
        y = BASE_Y + i * i * 7
        out.append(path(f"M0 {y} L{WIDTH} {y}", stroke=PAVE2, stroke_width=2, opacity=0.5))
    # long shadow of the building's foot
    out.append(rect(0, BASE_Y, WIDTH, 12, fill=SHADOW, opacity=0.5))
    # low sun behind the viewer: warm light fanning up the plaza
    for i in range(7):
        x = 80 + i * 180
        out.append(poly([(x - 60, HEIGHT), (x + 60, HEIGHT), (600 + (x - 600) * 0.35 + 12, BASE_Y + 14),
                         (600 + (x - 600) * 0.35 - 12, BASE_Y + 14)], fill=SUN, opacity=0.13))
    for i, h in enumerate((200, 150, 100, 50)):
        out.append(rect(0, HEIGHT - h, WIDTH, h, fill=SUN, opacity=0.07))
    # lamp standards
    for x, h in ((140, 150), (1060, 150), (300, 90), (900, 90)):
        y = BASE_Y + (60 if h > 100 else 18)
        out.append(rect(x - 3, y - h, 6, h, fill=INK))
        out.append(ellipse(x, y - h - 10, 10, 14, fill=SUN))
        out.append(rect(x - 8, y - h - 2, 16, 5, fill=INK))
    return out


def crew():
    """Generic TV crew and early passers-by in the foreground, long shadows toward the Capitol."""
    out = []
    # long cast shadows: sun low behind the viewer, so shadows run up the plaza toward the steps
    for x, w in ((300, 30), (350, 14), (470, 30), (760, 24), (850, 22), (940, 20)):
        tx = 600 + (x - 600) * 0.5
        out.append(poly([(x - w / 2, 884), (x + w / 2, 884), (tx + w * 0.2, 720), (tx - w * 0.2, 720)],
                        fill=SHADOW, opacity=0.42))
    # camera on a tripod
    out.append(path("M330 880 L350 790 L372 880 M350 790 L350 880", stroke=INK, stroke_width=5, fill="none"))
    out.append(rect(322, 754, 66, 40, rx=6, fill=INK))
    out.append(rect(386, 764, 26, 22, rx=4, fill="#2b2550"))
    out.append(circle(412, 775, 9, fill=ULTRA))
    out.append(rect(330, 746, 30, 10, rx=3, fill=INK))
    # camera operator behind the camera, facing the reporter
    out.append(figure(300, 882, 190, facing=1,
                      pose=Pose(back_arm=(60, 50), front_arm=(75, 40), lean=8),
                      look=Look(skin=SKIN[2], hair=HAIR[0], top="#3b3a6b", bottom="#22203d", hair_style="cap")))
    # reporter, back to the Capitol, speaking to camera with a microphone
    mic = {"front": rect(-2, -14, 5, 16, fill=INK) + circle(0.5, -16, 4.5, fill="#2b2550")}
    out.append(figure(470, 886, 200, facing=-1,
                      pose=Pose(back_arm=(-8, 10), front_arm=(35, 115)),
                      look=Look(skin=SKIN[4], hair=HAIR[2], top=APRICOT, bottom=INK, hair_style="long",
                                coat=True, face="speak"),
                      hand_items=mic))
    # passers-by walking toward the Capitol, seen from behind / side
    tops = [COBALT, "#6a4c93", "#2c7a7b"]
    for (x, h, top, style), facing in zip(((760, 150, tops[0], "short"), (850, 140, tops[1], "bun"), (940, 130, tops[2], "short")),
                                          (-1, -1, -1)):
        out.append(figure(x, 884, h, facing=facing, pose=WALK,
                          look=Look(skin=R.choice(SKIN), hair=R.choice(HAIR), top=top, bottom="#2b2738",
                                    hair_style=style, coat=True)))
    return out


def defs():
    return [
        linear("sky", [(0, NAVY), (0.45, DUSK), (0.8, "#6b4a8a"), (1, PEACH)]),
        linear("wavebody", [(0, ULTRA), (0.5, COBALT), (1, NAVY2)]),
        linear("plaza", [(0, PAVE), (1, "#e0a184")]),
        linear("facelight", [(0, SUN), (1, APRICOT)], x2=1, y2=0),
        halftone("wavedots", FOAM, dot=1.4, spacing=9),
        halftone("stars", FOAM, dot=1.0, spacing=23, angle=20),
        grain_filter(),
    ]


def main():
    building = group(dome() + wing(40, 400, 210) + wing(800, 1160, 990) + center_block(),
                     transform=f"translate(600 {BASE_Y}) scale(0.8) translate(-600 {-BASE_Y})")
    body = sky() + wave() + [building] + plaza() + crew() + [grain_overlay(opacity=0.3)]
    title = "The morning after: Democrats take the House and Senate"
    desc = ("Editorial illustration. At dawn, the white marble east front of the US Capitol, with its dome, central "
            "portico and House and Senate wings, glows apricot in low sun while a towering stylized blue wave swells "
            "behind it and curls over the dome. In the foreground a small TV crew films a reporter and passers-by walk "
            "toward the steps, casting long shadows. Represents Democrats winning control of both chambers of Congress "
            "in the 2026 midterms, reported Nov. 4, 2026; the wave is a symbol, not a real event.")
    save(document(defs(), body, title, desc), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")


if __name__ == "__main__":
    main()
