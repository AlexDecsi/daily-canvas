"""Daily artwork, 2026-10-25: María Corina Machado returns to Venezuela.

Verified scene (brief): Machado was seen at a church in Lara state, where
dozens of supporters greeted and hugged her, some recording on raised phones.
Not drawn because not verified: flags, signs, a stage, a mass rally, speeches.
Machado is identified by role and setting (and the caption), not by an
invented portrait.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import HAIR, SKIN, Look, Pose, figure  # noqa: E402

DATE = "2026-10-25"
R = rng(20261025)
SKY1, SKY2, SKY3 = "#7cc3d6", "#a9d8d8", "#f3dfa8"
CREAM, CREAM2, TERRA, WOOD, HILL, PLAZA, PLAZA2 = "#f6ead2", "#e6d3b0", "#c8613a", "#5a3524", "#8e7aa8", "#e2b97f", "#d4a568"
WHITE, INK = "#fbf8f1", "#2a2230"
CLOTHES = ["#d9472b", "#2f5d8a", "#e3a92f", "#3b7d5c", "#7a3f8f", "#c45c8a", "#1f2a44", "#e07a3a", "#4e8f9a"]


def backdrop():
    out = []
    for i, col in enumerate([SKY1, "#8ccbd8", SKY2, "#cfe3c9", SKY3]):  # banded poster sky
        out.append(rect(0, i * 100, WIDTH, 110, fill=col))
    out.append(circle(980, 150, 70, fill="#fff3c4"))
    out.append(path("M0 520 Q160 430 320 500 Q520 410 760 490 Q960 420 1200 500 L1200 560 L0 560 Z", fill=HILL))
    out += [path(f"M{x} 560 Q{x + 6} 470 {x + 2} 430", stroke="#5c4636", stroke_width=7, fill="none") for x in (90, 1110)]
    for x in (92, 1112):  # two palms flanking the plaza
        for k in range(6):
            a = -150 + k * 50
            out.append(path(f"M{x} 430 q{40 * (1 if a > -60 else -1)} {-30 + k * 6} {80 * (1 if a > -60 else -1)} {k * 14 - 10}",
                            stroke="#2f7a52", stroke_width=10, fill="none", stroke_linecap="round"))
    return out


def church():
    out = [
        rect(300, 230, 420, 420, fill=CREAM),                                              # facade
        path("M300 232 L300 200 Q510 90 720 200 L720 232 Z", fill=CREAM),                  # curved baroque gable
        path("M300 232 L300 200 Q510 90 720 200 L720 232", fill="none", stroke=CREAM2, stroke_width=10),
        rect(720, 120, 120, 530, fill=CREAM2), rect(712, 270, 136, 14, fill=CREAM),        # bell tower
        path("M720 120 Q780 50 840 120 Z", fill=TERRA),                                   # tower dome
        rect(777, 34, 6, 40, fill=INK), rect(766, 44, 28, 6, fill=INK),                    # cross atop
        path("M752 170 Q780 140 808 170 L808 230 L752 230 Z", fill="#3b2a2a"),             # belfry opening
        circle(780, 196, 13, fill="#c99a3a"),                                              # bell
        rect(290, 640, 560, 20, fill=CREAM2), rect(270, 658, 600, 22, fill="#ead9b8"),     # steps
    ]
    out += [rect(x, 260, 26, 380, fill=CREAM2) for x in (320, 674)]                        # pilasters
    out += [path("M440 640 L440 480 Q510 410 580 480 L580 640 Z", fill=WOOD),               # arched doorway
            path("M510 640 L510 450", stroke="#3e2318", stroke_width=4),
            circle(510, 300, 46, fill="#7fb6c9"), circle(510, 300, 46, fill="none", stroke=CREAM2, stroke_width=8)]
    out += [path(f"M{x} 420 L{x} 360 Q{x + 22} 334 {x + 44} 360 L{x + 44} 420 Z", fill="#5a7f8f") for x in (360, 616)]
    return out


def plaza():
    out = [rect(0, 560, WIDTH, 120, fill=PLAZA2), rect(0, 680, WIDTH, HEIGHT - 680, fill=PLAZA)]
    out += [path(f"M{600 + k * 30} 680 L{600 + k * 140} 900", stroke=PLAZA2, stroke_width=3) for k in range(-8, 9)]
    return out


def phone():
    return group([rect(-3.5, -11, 8, 13, fill="#1b1b22", rx=1.5), rect(-2.5, -10, 6, 10, fill="#bfe3ff")])


def crowd_back():
    """A modest crowd ('dozens', per AP): two loose rows, many holding phones up to record."""
    out = []
    for row_y, h, xs in [(735, 175, range(70, 1160, 62)), (790, 215, range(40, 1180, 88))]:
        for x in xs:
            x += R.uniform(-12, 12)
            if 430 < x < 800 and row_y == 790:  # keep the focal hug clear
                continue
            filming = R.random() < 0.55
            clap, wave = Pose(back_arm=(35, 85), front_arm=(40, 90)), Pose(back_arm=(-8, 10), front_arm=(165, -15))
            pose = Pose(back_arm=(-8, 10), front_arm=(150, -55)) if filming else (clap if R.random() < 0.6 else wave)
            look = Look(skin=R.choice(SKIN), hair=R.choice(HAIR), top=R.choice(CLOTHES), bottom=R.choice(["#2a2a3a", "#3a4a6a", "#5a4a3a"]),
                        hair_style=R.choice(["short", "long", "bun", "cap", "short"]))
            out.append(figure(round(x, 1), row_y + R.uniform(-6, 6), h + R.uniform(-12, 12), 1 if x < 600 else -1, pose, look,
                              hand_items={"front": phone() if filming else None}))
    return out


def focal_hug():
    out = []
    # supporter embracing her (facing left, toward Machado)
    out.append(figure(712, 905, 335, -1, Pose(back_arm=(70, 70), front_arm=(66, 80), back_leg=(-6, 0), front_leg=(10, 0), lean=12, head_tilt=12),
                      Look(skin=SKIN[3], top="#d9472b", bottom="#2a2a3a", hair="#8e8a86", hair_style="bun", face="smile")))
    # Machado: white top, long hair, arms around the supporter, smiling
    out.append(figure(565, 910, 370, 1, Pose(back_arm=(72, 62), front_arm=(80, 58), back_leg=(-8, 0), front_leg=(12, 0), lean=12, head_tilt=12),
                      Look(skin=SKIN[1], top=WHITE, top_shade="#e6e1d6", bottom="#3a4a6a", hair="#8a6a44", hair_style="long",
                           face="smile")))
    # two front-row supporters reaching in, one filming
    out.append(figure(330, 915, 330, 1, Pose(back_arm=(-10, 10), front_arm=(140, -60)),
                      Look(skin=SKIN[4], top="#2f5d8a", bottom="#2a2a3a", hair=HAIR[0], hair_style="short", face="smile"),
                      hand_items={"front": phone()}))
    out.append(figure(905, 915, 335, -1, Pose(back_arm=(-10, 10), front_arm=(145, -60)),
                      Look(skin=SKIN[2], top="#e3a92f", bottom="#3a4a6a", hair=HAIR[2], hair_style="long", face="smile"),
                      hand_items={"front": phone()}))
    return out


defs = [grain_filter(), radial("halo", [(0, "#fff6d8", 0.85), (1, "#fff6d8", 0)])]
body = backdrop() + church() + plaza() + [circle(605, 650, 240, fill="url(#halo)")] + crowd_back() + focal_hug() + [grain_overlay(opacity=0.35)]

save(document(defs, body,
              "María Corina Machado returns to Venezuela",
              "Graphic poster illustration: Venezuelan opposition leader María Corina Machado, in a white top, embraces "
              "a supporter outside a whitewashed colonial-style church, while a modest crowd of supporters around them "
              "smiles and holds up phones to record her return after about ten months abroad."),
     Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
