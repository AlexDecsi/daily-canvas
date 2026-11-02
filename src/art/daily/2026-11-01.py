"""Daily artwork, 2026-11-01: jet crashes on a Palm Beach County road, killing all nine aboard.

Visual idea: looking straight down rain-slicked Military Trail, the road itself
leads the eye to a burning crater in the pavement, and a black smoke column
climbs out of it into the storm clouds, splitting the picture in two: firefighters
pushing toward the fire on one side, residents walking away under umbrellas on
the other, with the untouched houses and palms pressing close on both.

Verified (brief): a Learjet 60 from Austin to the Bahamas crashed about 12:50 p.m.
on Nov. 1 on Military Trail in a residential part of Palm Beach County, nose-first,
leaving a burning crater in the road; all nine aboard died; no reported injuries
on the ground; it landed feet from homes and near passing vehicles; thick black
smoke; road closed both ways; about 600 mobile home residents evacuated; rain and
a flood watch (AP via PBS; NBC News).
Drawn: the crater, flames and smoke on the road; scattered pavement chunks;
untouched low houses, palms and a mobile home park; stopped ordinary cars; a red
fire engine and generic firefighters with a hose; a generic deputy's patrol car
blocking the road; generic residents leaving under umbrellas; rain.
Not drawn: no aircraft, wreckage close-ups, victims, names, logos, text, or cause.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import HOSE, SKIN, HAIR, WALK, Look, Pose, figure  # noqa: E402

DATE = "2026-11-01"
R = rng(20261101)
STORM, STORM2, STORM3, MIST = "#27353b", "#3f5359", "#6f8784", "#a9bcb4"
SMOKE, SMOKE2 = "#16171b", "#2b2c31"
FIRE, FIRE2, FIRE3 = "#ff7a1f", "#ffb43a", "#fff0a8"
ROAD, ROAD2, LINE = "#33393d", "#454c50", "#e9d77a"
LAWN, LAWN2 = "#4e6f4a", "#3c5a3d"
PALM, PALM2 = "#22382c", "#1a2b23"
STUCCO, STUCCO2, ROOF = "#e9d9bf", "#cdb99a", "#b5643f"
ENGINE, WHITE = "#c8312a", "#f2efe6"
HORIZON = 470
VX = 600  # vanishing point x


def road_half(y):
    """Half-width of Military Trail at screen height y (perspective)."""
    return 14 + (y - HORIZON) * 1.75


def sky():
    out = [rect(0, 0, WIDTH, HORIZON + 10, fill="url(#sky)"),
           rect(0, 0, WIDTH, HORIZON + 10, fill="url(#skydots)", opacity=0.25)]
    for cx, cy, w, h, col in [(180, 90, 520, 120, STORM), (980, 60, 560, 130, STORM),
                              (260, 250, 600, 90, STORM2), (950, 270, 520, 80, STORM2),
                              (600, 380, 900, 60, STORM3)]:
        out += cloud_puffs(R, cx, cy, w, h, 12, h * 0.3, h * 0.55, fill=col)
    out.append(ellipse(VX, HORIZON + 40, 520, 260, fill="url(#fireglow)"))
    return out


def smoke():
    out = []
    for i in range(18):
        t = i / 17
        cx = VX + 10 + t * t * 330 + (R.random() - 0.5) * 30
        cy = HORIZON + 105 - t * 560
        r = 34 + t * 120
        out += cloud_puffs(R, cx, cy, r * 1.5, r, 7, r * 0.35, r * 0.6, fill=SMOKE if i % 2 else SMOKE2)
    out += cloud_puffs(R, VX + 10, HORIZON + 95, 150, 34, 10, 14, 26, fill=FIRE, opacity=0.5)
    out.append(ellipse(VX + 20, HORIZON + 10, 110, 90, fill="url(#fireglow)", opacity=0.9))
    return [group(out)]


def homes_left():
    out = [rect(0, HORIZON - 2, VX - 30, 40, fill=LAWN2)]
    for x, w, h in [(30, 150, 46), (205, 120, 40), (345, 96, 32), (455, 60, 22)]:
        y = HORIZON + 8 + (VX - x) * 0.01
        out += [rect(x, y - h, w, h, fill=STUCCO), poly([(x - 8, y - h), (x + w / 2, y - h - h * 0.55), (x + w + 8, y - h)], fill=ROOF),
                rect(x + w * 0.15, y - h * 0.62, w * 0.18, h * 0.32, fill="#ffd27a", opacity=0.8),
                rect(x + w * 0.6, y - h * 0.62, w * 0.18, h * 0.32, fill="#3a4a4e")]
    return out


def near_homes():
    """Houses and a fence right at the roadside, close to where the jet came down (untouched)."""
    out = []
    for x, y, w, h in [(250, 600, 170, 70), (418, 566, 96, 44)]:
        out += [rect(x, y - h, w, h, fill=STUCCO), rect(x + w * 0.62, y - h, w * 0.38, h, fill=STUCCO2),
                poly([(x - 10, y - h), (x + w * 0.45, y - h - h * 0.5), (x + w + 10, y - h)], fill=ROOF),
                rect(x + w * 0.12, y - h * 0.6, w * 0.16, h * 0.34, fill="#ffd27a", opacity=0.85),
                rect(x + w * 0.38, y - h * 0.6, w * 0.16, h * 0.34, fill="#3a4a4e")]
    out += [path(f"M{x} {612 - (x - 230) * 0.14} L{x} {598 - (x - 230) * 0.14}", stroke="#e9e1cf", stroke_width=3)
            for x in range(230, 520, 14)]
    out.append(path("M230 604 L520 563", stroke="#e9e1cf", stroke_width=3))
    return out


def mobile_homes_right():
    out = [rect(VX + 30, HORIZON - 2, WIDTH, 50, fill=LAWN2)]
    for row, (y, h, n, x0, w) in enumerate([(HORIZON + 12, 16, 7, 700, 66), (HORIZON + 34, 22, 5, 760, 92)]):
        for k in range(n):
            x = x0 + k * (w + 14)
            col = [WHITE, "#d9e4e1", "#e8dcc8"][(k + row) % 3]
            out += [rect(x, y - h, w, h, fill=col, rx=2), rect(x, y - h - 3, w, 4, fill="#8c9692"),
                    rect(x + w * 0.2, y - h * 0.7, w * 0.16, h * 0.35, fill="#3a4a4e"),
                    rect(x + w * 0.6, y - h * 0.7, w * 0.16, h * 0.35, fill="#3a4a4e")]
    return out


def palm(x, y, h, lean=0, col=PALM):
    tx, ty = x + lean, y - h
    out = [path(f"M{x - 5} {y} Q{x + lean * 0.4} {y - h * 0.5} {tx - 2} {ty} L{tx + 2} {ty} Q{x + lean * 0.4 + 6} {y - h * 0.5} {x + 5} {y} Z", fill=col)]
    for a in range(9):
        dx = (-1 if a % 2 else 1) * (0.35 + a * 0.07) * h * 0.5
        dy = -h * 0.12 + a * h * 0.035
        out.append(path(f"M{tx} {ty} Q{tx + dx * 0.5} {ty + dy - h * 0.12} {tx + dx} {ty + dy + h * 0.1}",
                        fill="none", stroke=col, stroke_width=max(2, h * 0.035), stroke_linecap="round"))
    return out


def road():
    yb = HEIGHT
    out = [poly([(VX - road_half(HORIZON), HORIZON), (VX + road_half(HORIZON), HORIZON),
                 (VX + road_half(yb), yb), (VX - road_half(yb), yb)], fill="url(#asphalt)")]
    # verges between road and lawns
    out += [poly([(0, HORIZON + 30), (VX - road_half(HORIZON) - 6, HORIZON), (VX - road_half(yb) - 30, yb), (0, yb)], fill="url(#lawn)"),
            poly([(WIDTH, HORIZON + 40), (VX + road_half(HORIZON) + 6, HORIZON), (VX + road_half(yb) + 30, yb), (WIDTH, yb)], fill="url(#lawn)")]
    # median and lane lines
    y = HORIZON + 6
    while y < yb:
        y2 = y + (y - HORIZON) * 0.12 + 6
        for f in (-0.5, 0.5):
            out.append(poly([(VX + f * road_half(y) - 1, y), (VX + f * road_half(y) + 1, y),
                             (VX + f * road_half(y2) + 2, y2), (VX + f * road_half(y2) - 2, y2)], fill=WHITE, opacity=0.7))
        y = y2 + (y2 - HORIZON) * 0.14 + 6
    out.append(poly([(VX - 2, HORIZON), (VX + 2, HORIZON), (VX + 9, yb), (VX - 9, yb)], fill=LINE))
    # wet reflection of the fire running down the road
    out.append(poly([(VX - 40, HORIZON + 110), (VX + 60, HORIZON + 110), (VX + 160, yb), (VX - 120, yb)], fill="url(#reflect)"))
    return out


def crater():
    cy = HORIZON + 105
    out = [ellipse(VX + 10, cy + 4, 92, 18, fill="#151515"), ellipse(VX + 10, cy, 80, 13, fill="#2a1a12")]
    for k in range(22):
        side = 1 if k % 2 else -1
        px = VX + 10 + side * (85 + R.random() * 120)
        py = cy - 4 + R.random() * 34
        s = 5 + R.random() * 9
        out.append(poly([(px, py), (px + s, py - s * 0.4), (px + s * 1.3, py + s * 0.3), (px + s * 0.2, py + s * 0.4)], fill="#5d6468", stroke="#1b1d1f", stroke_width=1))
    for fx, fh in [(VX - 40, 70), (VX - 10, 120), (VX + 25, 150), (VX + 55, 90), (VX + 75, 55)]:
        out.append(path(f"M{fx - 22} {cy} Q{fx - 24} {cy - fh * 0.5} {fx} {cy - fh} Q{fx + 24} {cy - fh * 0.5} {fx + 22} {cy} Z", fill=FIRE))
        out.append(path(f"M{fx - 11} {cy} Q{fx - 12} {cy - fh * 0.3} {fx} {cy - fh * 0.6} Q{fx + 12} {cy - fh * 0.3} {fx + 11} {cy} Z", fill=FIRE2))
        out.append(path(f"M{fx - 5} {cy} Q{fx - 5} {cy - fh * 0.15} {fx} {cy - fh * 0.3} Q{fx + 5} {cy - fh * 0.15} {fx + 5} {cy} Z", fill=FIRE3))
    return out


def car(x, y, s, col, facing=1, lights=False):
    g = [path("M-60 -10 L-56 -30 L-30 -34 L-16 -52 L28 -52 L44 -34 L60 -30 L62 -10 Z", fill=col),
         path("M-12 -48 L-24 -34 L40 -34 L26 -48 Z", fill="#9fb6bb"),
         rect(-62, -14, 124, 6, fill=_dark(col)),
         circle(-36, -8, 11, fill="#141414"), circle(38, -8, 11, fill="#141414"),
         circle(-36, -8, 4, fill="#888"), circle(38, -8, 4, fill="#888"),
         rect(54, -28, 8, 6, fill="#ffe7a0")]
    if lights:
        g += [rect(-8, -60, 14, 8, fill="#e8352b", rx=2), rect(8, -60, 14, 8, fill="#3a6fe0", rx=2),
              path("M-60 -24 L62 -24", stroke="#2f6b46", stroke_width=6)]
    out = [group(g, transform=f"translate({x} {y}) scale({s * facing} {s})")]
    if lights:
        out += [circle(x, y - 56 * s, 70 * s, fill="url(#redglow)"), circle(x + 16 * s * facing, y - 56 * s, 70 * s, fill="url(#blueglow)")]
    return out


def _dark(c):
    h = c.lstrip("#")
    return "#{:02x}{:02x}{:02x}".format(*(int(int(h[i:i + 2], 16) * 0.7) for i in (0, 2, 4)))


def fire_engine():
    x, y, s = 330, 700, 0.9
    g = [rect(-170, -120, 250, 96, fill=ENGINE, rx=6), rect(80, -126, 92, 102, fill=ENGINE, rx=8),
         rect(96, -116, 64, 40, fill="#24343a"), rect(-170, -40, 342, 14, fill=WHITE),
         rect(-160, -110, 220, 10, fill="#e9e3d2"), path("M-170 -132 L60 -132", stroke="#bfbfbf", stroke_width=8),
         rect(110, -138, 22, 10, fill="#ff3b30", rx=3), rect(136, -138, 22, 10, fill="#ff3b30", rx=3)]
    g += [circle(wx, -20, 22, fill="#141414") for wx in (-120, -60, 120)]
    g += [circle(wx, -20, 8, fill="#8a8a8a") for wx in (-120, -60, 120)]
    g += [rect(-150 + k * 34, -96, 24, 40, fill=_dark(ENGINE), rx=3) for k in range(6)]
    out = [group(g, transform=f"translate({x} {y}) scale({s} {s})"),
           circle(x + 120 * s, y - 132 * s, 90, fill="url(#redglow)")]
    return out


def water():
    sx, sy, ex, ey = 455, 742, VX - 40, HORIZON + 80
    return [path(f"M{sx} {sy} Q{(sx + ex) / 2 - 20} {ey - 120} {ex} {ey}", fill="none", stroke=WHITE, stroke_width=11, stroke_linecap="round", opacity=0.9),
            path(f"M{sx} {sy} Q{(sx + ex) / 2 - 20} {ey - 120} {ex} {ey}", fill="none", stroke="#cfe8ee", stroke_width=4, stroke_linecap="round"),
            *cloud_puffs(R, ex, ey + 6, 70, 22, 8, 8, 16, fill=WHITE, opacity=0.7)]


def firefighters():
    gear = dict(top="#b8913a", top_shade="#97762c", bottom="#a8822f", shoes="#1d1b22", hair="#2a2a2a",
                hair_style="firehat", vest=True)
    nozzle = rect(-2, -3, 24, 7, fill="#444", rx=2)
    out = [path("M250 690 Q200 760 250 830 Q330 790 400 780 Q440 775 455 745", fill="none", stroke="#8c2a1f", stroke_width=8)]
    for i, (x, y, h) in enumerate([(430, 790, 150), (370, 806, 160), (300, 824, 170)]):
        out.append(figure(x, y, h, 1, HOSE, Look(skin=SKIN[(i * 2) % 6], face="stern" if i == 0 else None, **gear),
                          hand_items={"front": nozzle if i == 0 else None}))
    return out


def umbrella(col):
    return group([path("M0 0 L0 -56", stroke="#222", stroke_width=2.2),
                  path("M-38 -50 Q0 -88 38 -50 Q28 -56 19 -50 Q9 -56 0 -50 Q-9 -56 -19 -50 Q-28 -56 -38 -50 Z", fill=col)])


def evacuees():
    out = []
    lift = Pose(back_arm=(-20, 15), front_arm=(150, -150), back_leg=(-20, -15), front_leg=(22, -4))
    people = [(900, 760, 175, "#2a6f8f", "#e2b33c", 1), (990, 790, 190, "#7b3f6e", "#3d8f6a", 2),
              (1085, 770, 182, "#d9d2c0", "#d8382f", 4), (1150, 840, 215, "#3c5a7a", "#f29a3a", 5)]
    for i, (x, y, h, top, ucol, sk) in enumerate(people):
        out.append(figure(x, y, h, 1, lift, Look(skin=SKIN[sk], top=top, bottom="#2b2b38", hair=HAIR[i % 6],
                                                 hair_style=["long", "short", "bun", "short"][i]),
                          hand_items={"front": umbrella(ucol)}))
    # a child walking beside, and one resident turning back to look at the smoke
    out.append(figure(1035, 800, 105, 1, WALK, Look(skin=SKIN[2], top="#e2b33c", hair=HAIR[1])))
    out.append(figure(820, 740, 160, -1, Pose(back_arm=(-10, 10), front_arm=(20, 30)), Look(skin=SKIN[1], top="#4d7a5a", hair=HAIR[3], hair_style="long", face="frown")))
    return out


def deputy_block():
    out = car(720, 640, 0.95, WHITE, -1, lights=True)
    # striped barricade across the near lane, no lettering
    bx, by = 600, 860
    out += [rect(bx - 150, by - 60, 300, 22, fill="#f4efe6"), rect(bx - 150, by - 30, 300, 22, fill="#f4efe6"),
            rect(bx - 140, by - 64, 8, 64, fill="#5a5a5a"), rect(bx + 132, by - 64, 8, 64, fill="#5a5a5a")]
    for k in range(6):
        x = bx - 150 + k * 50
        out += [poly([(x, by - 60), (x + 22, by - 60), (x + 34, by - 38), (x + 12, by - 38)], fill="#e8762e"),
                poly([(x, by - 30), (x + 22, by - 30), (x + 34, by - 8), (x + 12, by - 8)], fill="#e8762e")]
    out.append(figure(680, 885, 215, 1, Pose(back_arm=(-10, 10), front_arm=(100, -15)),
                      Look(skin=SKIN[3], top="#2f4f3a", bottom="#2b3a30", hair_style="cap", hair="#1f2a22", face="stern",
                           accent="#d9b64a")))
    return out


def rain():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#rain)", opacity=0.6)]
    for k in range(40):
        y = 620 + R.random() * 270
        x = VX + (R.random() - 0.5) * 2 * road_half(y) * 0.9
        rx = 3 + (y - 600) * 0.04
        out.append(ellipse(x, y, rx, rx * 0.3, fill="none", stroke="#cfe0e0", stroke_width=1, opacity=0.6))
    return out


def vignette():
    return [rect(0, 0, WIDTH, HEIGHT, fill="url(#vignette)")]


def framing():
    return palm(60, 620, 420, 40, PALM2) + palm(1180, 560, 380, -30, PALM2) + palm(150, HORIZON + 30, 150, 10) + palm(1010, HORIZON + 40, 160, -12) + palm(480, HORIZON + 12, 90, 6)


defs = [grain_filter(),
        linear("sky", [(0, STORM), (0.5, STORM2), (0.9, STORM3), (1, MIST)]),
        linear("asphalt", [(0, ROAD2), (1, ROAD)]),
        linear("lawn", [(0, LAWN), (1, LAWN2)]),
        linear("reflect", [(0, FIRE, 0.55), (1, FIRE, 0)]),
        radial("fireglow", [(0, FIRE, 0.6), (1, FIRE, 0)]),
        radial("redglow", [(0, "#ff3b30", 0.55), (1, "#ff3b30", 0)]),
        radial("blueglow", [(0, "#3a6fe0", 0.5), (1, "#3a6fe0", 0)]),
        radial("vignette", [(0, "#000000", 0), (0.7, "#000000", 0), (1, "#000000", 0.45)], r=0.75),
        halftone("skydots", "#000000", dot=1.5, spacing=8),
        el("pattern", path("M0 0 L-8 26 M17 13 L9 39", stroke="#d8e6e6", stroke_width=1.3, opacity=0.6),
           id="rain", width=34, height=40, patternUnits="userSpaceOnUse")]
body = (sky() + homes_left() + mobile_homes_right() + road() + near_homes() + smoke() + crater()
        + car(470, 590, 0.55, "#5b7f9a", 1) + car(820, 600, 0.55, "#c9b27a", -1)
        + framing() + deputy_block() + fire_engine() + water() + firefighters() + evacuees()
        + rain() + vignette() + [grain_overlay(opacity=0.32)])

save(document(defs, body,
              "Jet crashes on a Palm Beach County road, killing all nine aboard",
              "Graphic poster illustration on a rainy afternoon: looking down a wide suburban Florida road, a burning "
              "crater in the pavement sends a black smoke column up into storm clouds, with chunks of pavement around "
              "it. Low houses, palm trees and a mobile home park stand close on either side, untouched, and two "
              "ordinary cars are stopped well back. Firefighters spray water from a red fire engine on the left; a "
              "patrol car with flashing lights and a striped barricade close the road; residents walk away under "
              "umbrellas on the right, one turning to look back. No aircraft, victims or text are shown."),
     Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
