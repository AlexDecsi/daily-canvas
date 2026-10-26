"""Poster study 6 (public figure): a president shows off a signed executive order.

Tests whether the kit can draw a recognizable public figure as an editorial
caricature: Donald Trump holding up a signed executive order in the Oval
Office, a recurring and widely photographed public act. Not a specific day's
news. Recognition comes from documented traits (hair, build, suit, long red tie,
pursed lips) and the setting, never from invented actions, quotes or text.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import SKIN, HAIR, Look, Pose, figure  # noqa: E402

R = rng(2025)
WALL, WALL2, GOLD, GOLD2, NAVY, RED, WOOD, WOOD2, CREAM = (
    "#efe2c0", "#e2d1a6", "#e3a92f", "#c88a1c", "#1b2a52", "#d22f2f", "#4a2c1d", "#3a2115", "#fbf5e6")


def room():
    out = [rect(0, 0, WIDTH, HEIGHT, fill=WALL)]
    out += [rect(x, 0, 40, 620, fill=WALL2) for x in range(0, WIDTH, 140)]  # curved-wall panelling
    # two tall windows with heavy gold drapes
    for wx in (120, 760):
        out += [rect(wx, 60, 220, 460, fill="#bcd7e6"), rect(wx + 104, 60, 12, 460, fill=CREAM),
                rect(wx, 280, 220, 10, fill=CREAM)]
        for side in (-1, 1):
            dx = wx - 50 if side < 0 else wx + 190
            out.append(path(f"M{dx} 30 L{dx + 80} 30 Q{dx + 60} 300 {dx + 70} 560 L{dx} 560 Z", fill=GOLD))
            out += [path(f"M{dx + 16 + k * 16} 40 Q{dx + 10 + k * 16} 300 {dx + 14 + k * 16} 555", fill="none",
                         stroke=GOLD2, stroke_width=4) for k in range(4)]
        out.append(rect(wx - 60, 20, 340, 26, fill=GOLD2, rx=6))
    # flags between the windows: stripes and a stars canton (simplified), and a dark blue flag
    out += [rect(486, 120, 6, 520, fill=GOLD2), circle(489, 116, 8, fill=GOLD)]
    for k in range(7):
        out.append(path(f"M492 {150 + k * 36} Q540 {160 + k * 36} 560 {150 + k * 36} L560 {168 + k * 36} "
                        f"Q540 {178 + k * 36} 492 {168 + k * 36} Z", fill=RED))
    out.append(rect(492, 140, 46, 70, fill=NAVY))
    out += [circle(500 + (k % 4) * 11, 152 + (k // 4) * 14, 2.2, fill=CREAM) for k in range(16)]
    out += [rect(646, 120, 6, 520, fill=GOLD2), circle(649, 116, 8, fill=GOLD),
            path("M652 140 Q700 150 720 140 L720 400 Q700 410 652 400 Z", fill=NAVY)]
    out.append(rect(0, 620, WIDTH, 280, fill="#2b3a6b"))  # deep blue carpet
    out.append(rect(0, 620, WIDTH, 280, fill="url(#dots-carpet)", opacity=0.5))
    return out


def aides():
    out = []
    looks = [Look(skin=SKIN[0], top="#2a2a33", bottom="#2a2a33", hair=HAIR[4], hair_style="long", face="smile"),
             Look(skin=SKIN[2], top="#3d4a5c", bottom="#3d4a5c", hair=HAIR[0], hair_style="short", face="smile", accent="#2f5d8a"),
             Look(skin=SKIN[1], top="#2a2a33", bottom="#2a2a33", hair=HAIR[5], hair_style="short", face="neutral", accent=RED)]
    clap = Pose(back_arm=(60, 70), front_arm=(65, 75))
    for (x, look) in zip((215, 300), looks[:2]):
        out.append(figure(x, 760, 330, 1, clap, look))
    return out


def president_and_desk():
    out = []
    folder = group([rect(-4, -66, 100, 70, fill="#121212", rx=3), rect(4, -60, 84, 58, fill=CREAM),
                    path("M14 -26 l8 -12 l6 14 l8 -18 l7 16 l9 -14 l6 12 l10 -16 l8 14", fill="none",
                         stroke="#111", stroke_width=3, stroke_linejoin="round")],
                   transform="translate(-6 4) scale(0.5)")
    out.append(figure(545, 960, 560, 1, Pose(back_arm=(118, -78), front_arm=(112, -72), lean=-3, head_tilt=-4),
                      Look(skin="#e9a46f", top=NAVY, bottom=NAVY, hair="#f0c75a", hair_style="swept", accent=RED,
                           long_tie=True, face="pout", build=1.35),
                      hand_items={"front": folder}))
    # the carved dark-wood desk in front
    out += [rect(330, 640, 470, 30, fill=WOOD, rx=4), rect(345, 668, 440, 200, fill=WOOD2),
            rect(500, 690, 130, 160, fill=WOOD, rx=6), circle(565, 770, 42, fill="none", stroke=GOLD2, stroke_width=5),
            rect(365, 690, 110, 160, fill=WOOD, rx=6), rect(655, 690, 110, 160, fill=WOOD, rx=6)]
    out += [rect(420, 630, 60, 10, fill="#111", rx=3), rect(700, 625, 14, 15, fill=GOLD)]  # pen box and lamp base
    return out


def press():
    out = []
    flash_at = [(905, 470), (1010, 500), (1120, 455)]
    for fx, fy in flash_at:  # camera flashes as starbursts
        pts = []
        for k in range(16):
            a = k * 3.14159 / 8
            r = 70 if k % 2 == 0 else 22
            pts.append((fx + r * __import__("math").cos(a), fy + r * __import__("math").sin(a)))
        out.append(poly(pts, fill="#ffffff", opacity=0.9))
    cam = group([rect(-10, -14, 30, 22, fill="#111", rx=3), circle(18, -3, 8, fill="#333"), rect(-2, -20, 10, 6, fill="#111")],
                transform="scale(0.5)")
    for i, (x, h) in enumerate([(1000, 320), (1090, 340), (1175, 330), (920, 290)]):
        look = Look(skin=SKIN[(i * 2 + 3) % 6], top=["#5b6b7a", "#2f5d8a", "#3b7d5c", "#7a3f8f"][i], bottom="#2a2a3a",
                    hair=HAIR[i % 6], hair_style=["cap", "short", "long", "short"][i])
        out.append(figure(x, 920, h, -1, Pose(back_arm=(110, -40), front_arm=(118, -50), lean=-4), look,
                          hand_items={"front": cam}))
    return out


defs = [grain_filter(), halftone("dots-carpet", "#16224a", dot=2.2, spacing=9)]
body = room() + aides() + president_and_desk() + press() + [grain_overlay(opacity=0.35), study_tag()]

save(document(defs, body,
              "Poster study: a president holds up a signed executive order",
              "Graphic poster caricature of Donald Trump in the Oval Office: with swept golden hair, a navy suit and "
              "a long red tie, he holds up a black folder showing a signed order from behind the dark carved desk, "
              "between gold drapes and flags, as aides applaud behind him and photographers' flashes burst in the "
              "foreground. Style test of a recurring, widely photographed act; not a specific day's news."),
     Path(__file__).resolve().parents[3] / "prototypes" / "poster" / "06-oval.svg")
