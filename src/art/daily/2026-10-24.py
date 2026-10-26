"""Daily artwork, 2026-10-24: Trump votes early as Obama returns to the campaign trail.

Verified (brief): Trump voted early at the Palm Beach County elections office in
West Palm Beach, arriving with Melania Trump, wearing an "I Voted" sticker, and
spoke briefly to reporters. That evening Obama spoke at a rally in a Detroit
high-school gym. Split day/evening composition: the same day, two presidents.
Not drawn because not verified: signs, slogans, the sticker's text, other candidates' likenesses.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import HAIR, SKIN, Look, Pose, figure  # noqa: E402

DATE = "2026-10-24"
R = rng(20261024)
NAVY, RED, CREAM, INK = "#1b2a52", "#d22f2f", "#f6ecd8", "#16161c"
DIVIDE = [(650, 0), (1200, 0), (1200, 900), (570, 900)]


def mic():
    return group([rect(-1.5, -2, 3, 14, fill="#222"), circle(0, -4, 4.5, fill="#333")])


def florida_day():
    out = []
    for i, col in enumerate(["#ffd36b", "#ffe08f", "#bfe6ef", "#8fd0e0"][::-1]):  # bright banded sky
        out.append(rect(0, i * 110, 700, 120, fill=col))
    out.append(circle(130, 120, 60, fill="#fff3c4"))
    # low, flat-roofed government office building with glass doors
    out += [rect(-10, 330, 680, 300, fill="#e9dcc0"), rect(-10, 316, 680, 22, fill="#d6c6a4"),
            rect(150, 450, 240, 180, fill="#7fa8b8"), rect(266, 450, 8, 180, fill="#d6c6a4"),
            rect(150, 400, 240, 40, fill="#d6c6a4")]
    out += [rect(x, 380, 70, 50, fill="#7fa8b8") for x in (30, 460, 560)]
    for x in (60, 520):  # palms
        out.append(path(f"M{x} 640 Q{x + 10} 420 {x + 4} 300", stroke="#6b4f3a", stroke_width=10, fill="none"))
        for k in range(7):
            dx = (-1 if k % 2 else 1) * (50 + k * 6)
            out.append(path(f"M{x + 4} 300 q{dx * 0.5:.0f} -40 {dx:.0f} {10 + k * 6}", stroke="#2f7a52",
                            stroke_width=11, fill="none", stroke_linecap="round"))
    out += [rect(0, 630, 700, 270, fill="#cfc4ad"), rect(0, 630, 700, 10, fill="#b9ad95")]  # pavement
    # Melania Trump beside him
    out.append(figure(170, 905, 330, 1, Pose(back_arm=(-6, 10), front_arm=(8, 12)),
                      Look(skin=SKIN[1], top="#efe6d6", top_shade="#ddd2bf", bottom="#efe6d6", hair="#5a3a26",
                           hair_style="long", coat=True, face="neutral")))
    # Trump, "I Voted" sticker (a small blank badge) on his lapel, answering reporters
    sticker = [ellipse(-4.5, -64, 2.0, 1.4, fill="#ffffff"), ellipse(-4.5, -64, 1.3, 0.8, fill=RED)]
    out.append(figure(330, 915, 420, 1, Pose(back_arm=(-8, 12), front_arm=(55, -60), lean=-2),
                      Look(skin="#e9a46f", top=NAVY, bottom=NAVY, hair="#f0c75a", hair_style="swept", accent=RED,
                           long_tie=True, face="neutral", build=1.35, extra=sticker)))
    # reporters holding out microphones
    for x, h, look in [(505, 340, Look(skin=SKIN[3], top="#5b6b7a", bottom="#2a2a3a", hair=HAIR[0], hair_style="short")),
                       (580, 315, Look(skin=SKIN[0], top="#3b7d5c", bottom="#2a2a3a", hair=HAIR[4], hair_style="long"))]:
        out.append(figure(x, 915, h, -1, Pose(back_arm=(-6, 10), front_arm=(78, -2), lean=2), look,
                          hand_items={"front": mic()}))
    return out


def detroit_evening():
    out = [rect(560, 0, 640, 900, fill="#1f3c88"),                      # gym wall, evening
           rect(560, 560, 640, 340, fill="#c98a4a"),                    # wooden floor
           rect(560, 560, 640, 340, fill="url(#dots-floor)", opacity=0.5)]
    # bleachers with seated supporters
    for row in range(5):
        y = 300 + row * 52
        out.append(rect(560, y + 30, 640, 22, fill="#c7ccd8" if row % 2 else "#b4bacb"))
        for x in range(580 + (row % 2) * 18, 1200, 36):
            out += [circle(x, y + 12, 10, fill=R.choice(SKIN)),
                    path(f"M{x - 13} {y + 32} Q{x} {y + 16} {x + 13} {y + 32} Z", fill=R.choice(["#d9472b", "#2f5d8a", "#e3a92f", "#f4f1ea", "#3b7d5c"]))]
    # basketball hoop high on the wall
    out += [rect(980, 60, 150, 100, fill="#f4f1ea"), rect(1030, 100, 50, 36, fill="none", stroke=RED, stroke_width=4),
            ellipse(1055, 168, 30, 7, fill="none", stroke="#e8622c", stroke_width=5),
            path("M1028 168 L1036 210 M1055 175 L1055 214 M1082 168 L1074 210", stroke="#f4f1ea", stroke_width=2)]
    out += [circle(x, 30, 50, fill="url(#gymlight)") for x in (700, 900, 1100)]
    # lectern and Obama speaking, facing the crowd at the lower left
    out.append(figure(905, 820, 400, -1, Pose(back_arm=(30, 50), front_arm=(100, -45), lean=3),
                      Look(skin="#8a5a3c", top="#2a2a33", bottom="#2a2a33", hair="#6e6a66", hair_style="short",
                           face="speak", build=0.95, accent="#f4f1ea")))
    out += [path("M800 640 L960 640 L940 840 L820 840 Z", fill="#13224d"), rect(790, 626, 180, 18, fill="#2a3f7a"),
            circle(880, 730, 34, fill="#e3a92f")]  # blank round plaque, no text
    out.append(path("M842 628 Q830 600 818 588", stroke="#111", stroke_width=3, fill="none"))
    # foreground crowd seen from behind, some cheering
    for k, x in enumerate(range(600, 1220, 70)):
        skin = R.choice(SKIN)
        y = 900 + R.uniform(-10, 10)
        if k % 3 == 1:
            out.append(path(f"M{x + 10} {y - 90} L{x + 24} {y - 170}", stroke="#2a2a3a", stroke_width=14, stroke_linecap="round"))
            out.append(circle(x + 25, y - 175, 8, fill=skin))
        out += [path(f"M{x - 34} {y} Q{x - 32} {y - 80} {x} {y - 82} Q{x + 32} {y - 80} {x + 34} {y} Z", fill=R.choice(["#1d1b22", "#2a2a3a", "#3a2f4a"])),
                circle(x, y - 100, 22, fill=R.choice(HAIR))]
    return [group(out, clip_path="url(#right)")]


defs = [grain_filter(), halftone("dots-floor", "#a8702f", dot=1.8, spacing=8),
        radial("gymlight", [(0, "#fff3c4", 0.6), (1, "#fff3c4", 0)]),
        el("clipPath", [poly(DIVIDE)], id="right")]
body = florida_day() + detroit_evening() + [path("M650 0 L570 900", stroke=CREAM, stroke_width=10), grain_overlay(opacity=0.35)]

save(document(defs, body,
              "Trump votes early as Obama returns to the campaign trail",
              "Graphic poster illustration split diagonally between day and evening. Left: in Florida sunshine, Donald Trump, "
              "with swept blond hair, a navy suit, a red tie and a small voting sticker, stands with Melania Trump outside a "
              "low elections office while two reporters hold out microphones. Right: in a high-school gym with packed "
              "bleachers and a basketball hoop, Barack Obama speaks from a lectern to a cheering crowd."),
     Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
