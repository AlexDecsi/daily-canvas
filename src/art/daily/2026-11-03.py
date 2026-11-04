"""Daily artwork, 2026-11-03: Pappas wins New Hampshire's Senate seat on midterm Election Day.

Visual idea: we stand behind the winner on election night. A huge dark silhouette
of the speaker at the podium, rim-lit coral by the stage lights, fills the right
foreground and looks out over a room of cheering supporters; behind them a giant
glowing blank ballot rises like a sunrise, its ovals the only "text" in the room.

Verified (brief): on Nov. 3 AP called New Hampshire's open Senate seat for Democrat
Chris Pappas at 8:22 p.m. (also CBS, NBC); John E. Sununu conceded; Democratic
partygoers cheered as word spread; Pappas addressed supporters after the win (ABC).
Drawn: a generic suited figure seen from behind at a podium with a microphone,
stage truss and lights, supporters with raised arms. The ballot is symbolic.
Not drawn: no face or likeness, no names, signs, slogans, numbers, confetti, flags
or crowd-size claim; no Senate-control outcome.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import CHEER, HAIR, SKIN, WAVE, Look, Pose, figure  # noqa: E402

DATE = "2026-11-03"
R = rng(20261103)
TEAL0, TEAL1, TEAL2, TEAL3 = "#06262a", "#0d3b3f", "#145a5c", "#2a8180"
CORAL, CORAL2, ROSE = "#ff6f61", "#ff9a85", "#ffc9b8"
GOLD, GOLD2 = "#ffcf5a", "#f4a83a"
CREAM, CREAM2 = "#fff4dc", "#f0dfbd"
INK = "#071618"
STAGE_Y = 770


def background():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#wall)")]
    # back-wall vertical drape panels
    for i in range(13):
        x = i * 96
        out.append(rect(x, 0, 48, 640, fill=TEAL2, opacity=0.18))
    out.append(rect(0, 0, WIDTH, HEIGHT, fill="url(#dots)", opacity=0.12))
    return out


def ballot():
    """Giant glowing generic ballot rising behind the crowd (symbolic, no text)."""
    cx, top, w = 450, 150, 360
    out = []
    # poster sunburst radiating from behind the ballot
    for i in range(18):
        a0, a1 = math.radians(i * 20), math.radians(i * 20 + 9)
        out.append(poly([(cx, 470), (cx + math.cos(a0) * 1100, 470 + math.sin(a0) * 1100),
                         (cx + math.cos(a1) * 1100, 470 + math.sin(a1) * 1100)], fill=GOLD, opacity=0.08))
    out.append(circle(cx, 470, 470, fill="url(#halo)"))
    inner = []
    inner.append(rect(cx - w / 2 + 14, top + 14, w, 520, rx=18, fill=TEAL0, opacity=0.45))
    inner.append(rect(cx - w / 2, top, w, 520, rx=18, fill=CREAM))
    inner.append(rect(cx - w / 2, top, w, 54, rx=18, fill=CREAM2))
    inner.append(rect(cx - w / 2, top + 36, w, 18, fill=CREAM2))
    for row in range(7):
        y = top + 100 + row * 62
        inner.append(ellipse(cx - w / 2 + 58, y, 20, 13, fill="none", stroke=TEAL1, stroke_width=4))
        # blank lines where candidate names would go (no text drawn)
        inner.append(rect(cx - w / 2 + 100, y - 6, 210 - (row % 3) * 40, 12, rx=6, fill=CREAM2))
        if row == 2:
            inner.append(ellipse(cx - w / 2 + 58, y, 17, 10.5, fill=TEAL1))
    out.append(group(inner, transform=f"rotate(-5 {cx} 470)"))
    return out


def truss():
    out = [rect(0, 38, WIDTH, 16, fill=INK), rect(0, 70, WIDTH, 8, fill=INK)]
    for i in range(26):
        x = i * 48
        out.append(path(f"M{x} 54 L{x + 24} 70 L{x + 48} 54", fill="none", stroke=INK, stroke_width=4))
    for x in (150, 420, 700, 980):
        out.append(rect(x - 16, 76, 32, 34, rx=6, fill=INK))
        out.append(ellipse(x, 112, 14, 6, fill=ROSE))
    return out


def beams():
    out = []
    for x, tx in ((150, 330), (420, 520), (700, 1020), (980, 1080)):
        out.append(poly([(x - 12, 112), (x + 12, 112), (tx + 190, STAGE_Y + 40), (tx - 190, STAGE_Y + 40)],
                        fill="url(#beam)", style="mix-blend-mode:screen"))
    return out


def crowd():
    """Supporters on the floor below the stage edge, cheering toward the speaker."""
    out = []
    tops = [CORAL, GOLD, TEAL3, "#e9e1cf", "#3e6fa8", "#b45a8a", GOLD2, "#7a9a5a"]
    rows = [(620, 150, 28, 0.55), (690, 190, 24, 0.8), (790, 240, 18, 1.0)]
    for ri, (base, h, n, alpha) in enumerate(rows):
        layer = []
        for k in range(n):
            x = -30 + k * (WIDTH + 40) / n + R.uniform(-14, 14) + (ri % 2) * 20
            pose = R.choice([CHEER, CHEER, WAVE, Pose(back_arm=(-10, 10), front_arm=(150, -20)),
                             Pose(back_arm=(30, 70), front_arm=(165, 0))])
            look = Look(skin=R.choice(SKIN), hair=R.choice(HAIR), top=R.choice(tops),
                        hair_style=R.choice(["short", "short", "long", "bun", "cap"]),
                        bottom=R.choice(["#1e2a33", "#2b2b38", "#3b3326"]),
                        face="smile" if ri == 2 and k % 3 == 0 else None)
            facing = 1 if x < 860 else -1
            layer.append(figure(x, base + h * 0.98, h, facing=facing, pose=pose, look=look))
        out.append(group(layer, opacity=f"{alpha:.2f}") if alpha < 1 else group(layer))
    return out


def stage():
    """We stand on the stage: its floor fills the bottom, its lit front edge cuts the crowd."""
    out = [poly([(0, STAGE_Y), (WIDTH, STAGE_Y), (WIDTH, HEIGHT), (0, HEIGHT)], fill="url(#stagefloor)")]
    out.append(rect(0, STAGE_Y, WIDTH, 10, fill=CORAL))
    out.append(rect(0, STAGE_Y + 10, WIDTH, 6, fill=TEAL0, opacity=0.6))
    # warm reflection of the ballot glow on the stage boards
    out.append(ellipse(470, STAGE_Y + 70, 380, 50, fill="url(#halo)", opacity=0.45))
    for i in range(1, 6):
        out.append(path(f"M0 {STAGE_Y + 16 + i * i * 7} L{WIDTH} {STAGE_Y + 16 + i * i * 7}", stroke=TEAL1, stroke_width=2, opacity=0.7))
    return out


def speaker():
    """Large back view of the winner at the podium; generic suit, no face."""
    out = []
    # long cast shadow on the stage toward the viewer
    out.append(ellipse(905, 880, 250, 30, fill=INK, opacity=0.6))
    # raised right arm waving to the room
    out.append(path("M1010 470 Q1060 380 1048 290", fill="none", stroke=INK, stroke_width=58, stroke_linecap="round"))
    out.append(path("M1032 470 Q1076 384 1066 296", fill="none", stroke=CORAL, stroke_width=7, stroke_linecap="round", opacity=0.9))
    out.append(rect(1024, 238, 46, 46, rx=16, fill="#8d5f45"))
    out.append(path("M1030 252 L1064 252 M1030 266 L1064 266", stroke="#6e4733", stroke_width=2.5))
    out.append(path("M1062 240 Q1074 258 1066 286", fill="none", stroke=CORAL2, stroke_width=5, stroke_linecap="round"))
    # torso / suit jacket
    out.append(path("M790 900 L800 560 Q808 470 880 448 L960 440 Q1030 448 1040 520 L1060 900 Z", fill=INK))
    out.append(path("M1040 520 L1060 900 L1048 900 L1028 530 Z", fill=CORAL, opacity=0.95))   # rim light
    out.append(path("M880 448 L920 470 L960 440", fill="none", stroke="#13292c", stroke_width=6))  # collar
    out.append(path("M922 470 L922 900", stroke="#13292c", stroke_width=3))  # back seam
    # left arm resting forward on podium
    out.append(path("M812 520 Q790 600 822 660", fill="none", stroke=INK, stroke_width=52, stroke_linecap="round"))
    # head (back of head, short dark hair) and neck
    out.append(rect(898, 400, 46, 58, fill="#8d5f45"))
    out.append(ellipse(921, 360, 58, 66, fill="#8d5f45"))
    out.append(path("M864 368 Q860 292 922 290 Q986 292 980 370 Q976 400 970 412 Q922 424 872 410 Q866 396 864 368 Z", fill="#1c1410"))
    out.append(path("M978 330 Q992 370 972 414", fill="none", stroke=CORAL2, stroke_width=6, stroke_linecap="round"))
    out.append(path("M890 306 Q922 296 956 308", fill="none", stroke="#3a2a20", stroke_width=5, stroke_linecap="round"))
    out.append(ellipse(864, 370, 8, 15, fill="#7a4f39"))
    out.append(ellipse(978, 370, 8, 15, fill="#a06a4c"))
    # podium (seen from behind) and microphone
    out.append(poly([(640, 640), (900, 640), (880, 900), (660, 900)], fill=TEAL1))
    out.append(poly([(620, 620), (920, 620), (900, 646), (640, 646)], fill=TEAL2))
    out.append(poly([(880, 646), (900, 646), (880, 900), (866, 900)], fill=CORAL, opacity=0.6))
    out.append(path("M760 620 Q752 560 712 520", fill="none", stroke="#2a2a2a", stroke_width=5))
    out.append(ellipse(706, 514, 11, 8, fill="#2a2a2a"))
    return out


def defs():
    return [
        linear("wall", [(0, TEAL0), (0.55, TEAL1), (1, TEAL2)]),
        linear("stagefloor", [(0, TEAL1), (1, TEAL0)]),
        radial("halo", [(0, GOLD), (0.35, GOLD2 + ""), (0.7, CORAL), (1, TEAL1)], r=0.5),
        linear("beam", [(0, ROSE), (1, CORAL)]),
        halftone("dots", CREAM, dot=1.6, spacing=9),
        grain_filter(),
    ]


def fix_defs(d):
    # soften gradients: halo fades out, beams fade with distance
    return [s.replace(f'stop-color="{TEAL1}"', f'stop-color="{TEAL1}" stop-opacity="0"', 1) if 'id="halo"' in s else
            s.replace('stop-color="#ff6f61"', 'stop-color="#ff6f61" stop-opacity="0"').replace(
                f'stop-color="{ROSE}"', f'stop-color="{ROSE}" stop-opacity="0.38"') if 'id="beam"' in s else s
            for s in d]


def main():
    body = background() + ballot() + truss() + beams() + crowd() + stage() + speaker() + [grain_overlay(opacity=0.3)]
    title = "Election night in New Hampshire: Pappas wins the Senate seat"
    desc = ("Editorial illustration. Seen from behind, a suited figure at a podium, rim-lit coral by stage lights, "
            "raises an arm to a room of cheering supporters. Behind them a giant glowing blank ballot rises like a sun. "
            "Represents Democrat Chris Pappas winning New Hampshire's open US Senate seat on Nov. 3, 2026.")
    svg_text = document(fix_defs(defs()), body, title, desc)
    save(svg_text, Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")


if __name__ == "__main__":
    main()
