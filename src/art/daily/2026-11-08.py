"""Daily artwork, 2026-11-08: Kyle Larson clinches his third NASCAR Cup Series championship.

Visual idea: the title is won before the finish line. From high above pit road at
Homestead-Miami, two crew leaders throw their arms up on top of a towering pit box
while, beyond them, the field circles slowly in single file behind a yellow pace
car under caution; radio waves arc from the pit-box antenna to Larson's No. 5
mid-pack: the championship was clinched by points at the end of Stage 1,
not by winning the race.

Verified (brief): on Nov. 8, 2026, Larson (Hendrick Motorsports, No. 5 Chevrolet)
clinched by finishing fourth in Stage 1, which ended under caution; he finished
12th and Ryan Blaney won the race. Crew chief Cliff Daniels and owner Rick Hendrick
celebrated atop the pit box and radioed Larson (NBC Sports, Heavy).
Drawn: the caution field behind a pace car, a generic white No. 5 car (not his
real livery), Daniels and Hendrick celebrating on the pit box, palms and stands.
Not drawn: no logos or other text, no trophy, no race winner, no invented crowd mood.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-08"
R = rng(20261108)

# South Florida afternoon: turquoise, coral, sand, palm green, asphalt, pace-car yellow
TURQ, TURQ2, SKY = "#2fb3bf", "#1d8c99", "#c9f3ee"
CORAL, CORAL2 = "#ff6f59", "#d94b3a"
SAND, SAND2 = "#f6dcae", "#e4bd7d"
PALM, PALM2, GRASS, GRASS2 = "#23885a", "#165c3c", "#4fb36a", "#3a9655"
ASPH, ASPH2 = "#4a4f5c", "#373b46"
YEL = "#ffd23f"
NAVY, NAVY2 = "#1e2a4a", "#141c33"
WHITE = "#fbfaf5"

# the oval's centreline across the middle of the frame (quadratic bezier)
P0, P1, P2 = (-80, 560), (560, 300), (1280, 520)


def bez(t):
    x = (1 - t) ** 2 * P0[0] + 2 * t * (1 - t) * P1[0] + t ** 2 * P2[0]
    y = (1 - t) ** 2 * P0[1] + 2 * t * (1 - t) * P1[1] + t ** 2 * P2[1]
    dx = 2 * (1 - t) * (P1[0] - P0[0]) + 2 * t * (P2[0] - P1[0])
    dy = 2 * (1 - t) * (P1[1] - P0[1]) + 2 * t * (P2[1] - P1[1])
    return x, y, math.degrees(math.atan2(dy, dx))


def defs():
    return [
        linear("sky", [(0, TURQ), (0.7, "#8fdfdc"), (1, SKY)]),
        linear("infield", [(0, GRASS), (1, GRASS2)]),
        radial("sun", [(0, "#fffbe0"), (0.4, "#fff1b8"), (1, "#fff1b8")]),
        el("radialGradient", [el("stop", offset=0, stop_color=YEL, stop_opacity=0.75),
                              el("stop", offset=1, stop_color=YEL, stop_opacity=0)], id="halo"),
        el("radialGradient", [el("stop", offset=0, stop_color="#ffb400", stop_opacity=0.9),
                              el("stop", offset=1, stop_color="#ffb400", stop_opacity=0)], id="beacon"),
        blur("soft", 10),
        halftone("crowd", NAVY, dot=1.7, spacing=6, angle=20),
        halftone("crowd2", CORAL2, dot=1.6, spacing=7, angle=-15),
        grain_filter(),
    ]


# ---------------------------------------------------------------- background
def sky():
    out = [rect(0, 0, WIDTH, 360, fill="url(#sky)")]
    out.append(circle(1010, 110, 120, fill="url(#sun)", opacity=0.45))
    out.append(circle(1010, 110, 42, fill="#fffbe6", opacity=0.9))
    out += cloud_puffs(R, 260, 120, 280, 50, 9, 22, 46, fill=WHITE, opacity=0.85)
    out += cloud_puffs(R, 680, 70, 200, 36, 7, 16, 34, fill=WHITE, opacity=0.7)
    return out


def palm(x, y, h, lean=0.0):
    out = []
    top = (x + lean * h, y - h)
    out.append(path(f"M{x - 5} {y} Q{x + lean * h * 0.4} {y - h * 0.5} {top[0] - 2:.1f} {top[1]:.1f} "
                    f"L{top[0] + 3:.1f} {top[1]:.1f} Q{x + 4 + lean * h * 0.4} {y - h * 0.5} {x + 5} {y} Z",
                    fill="#7a5a3a"))
    for k in range(7):
        a = math.radians(-170 + k * 27)
        ln = h * 0.42
        ex, ey = top[0] + ln * math.cos(a), top[1] + ln * math.sin(a) * 0.6 + ln * 0.25
        mx, my = top[0] + ln * 0.5 * math.cos(a), top[1] - ln * 0.18
        out.append(path(f"M{top[0]:.1f} {top[1]:.1f} Q{mx:.1f} {my:.1f} {ex:.1f} {ey:.1f} "
                        f"Q{mx:.1f} {my + 9:.1f} {top[0]:.1f} {top[1] + 4:.1f} Z",
                        fill=PALM if k % 2 else PALM2))
    return out


def grandstands():
    out = []
    # long stand along the far straight, tiers in sand and coral
    out.append(path("M-20 330 L1220 330 L1220 262 Q600 222 -20 262 Z", fill=SAND))
    out.append(path("M-20 330 L1220 330 L1220 262 Q600 222 -20 262 Z", fill="url(#crowd)", opacity=0.55))
    out.append(path("M-20 300 Q600 262 1220 300 L1220 308 Q600 270 -20 308 Z", fill=CORAL))
    out.append(path("M-20 280 Q600 242 1220 280 L1220 285 Q600 247 -20 285 Z", fill=CORAL2, opacity=0.8))
    # roof canopy
    out.append(path("M-20 262 Q600 222 1220 262 L1220 248 Q600 206 -20 248 Z", fill=WHITE))
    for x in range(20, 1220, 110):
        out.append(rect(x, 246, 4, 40, fill="#d8d3c4"))
    # palms between the stands and the track
    for x, h, lean in [(70, 120, 0.05), (150, 95, -0.08), (930, 130, 0.06), (1040, 105, -0.05), (1140, 140, 0.04)]:
        out += palm(x, 345, h, lean)
    return out


def track():
    d = f"M{P0[0]} {P0[1]} Q{P1[0]} {P1[1]} {P2[0]} {P2[1]}"
    out = [rect(0, 330, WIDTH, 570, fill="url(#infield)")]
    # outside wall and catch fence (above the racing surface)
    out.append(path(f"M{P0[0]} {P0[1] - 78} Q{P1[0]} {P1[1] - 78} {P2[0]} {P2[1] - 78}", stroke="#cfd4da",
                    stroke_width=14, fill="none"))
    out.append(path(f"M{P0[0]} {P0[1] - 92} Q{P1[0]} {P1[1] - 92} {P2[0]} {P2[1] - 92}", stroke="#9aa3ad",
                    stroke_width=10, fill="none", stroke_dasharray="2 6", opacity=0.7))
    # racing surface, banked: darker upper groove
    out.append(path(d, stroke=ASPH, stroke_width=150, fill="none"))
    out.append(path(f"M{P0[0]} {P0[1] - 40} Q{P1[0]} {P1[1] - 40} {P2[0]} {P2[1] - 40}", stroke=ASPH2,
                    stroke_width=50, fill="none", opacity=0.6))
    out.append(path(f"M{P0[0]} {P0[1] + 20} Q{P1[0]} {P1[1] + 20} {P2[0]} {P2[1] + 20}", stroke="#5a606d",
                    stroke_width=20, fill="none", opacity=0.6))
    # apron line and pit road
    out.append(path(f"M{P0[0]} {P0[1] + 76} Q{P1[0]} {P1[1] + 76} {P2[0]} {P2[1] + 76}", stroke=WHITE,
                    stroke_width=5, fill="none"))
    out.append(path(f"M{P0[0]} {P0[1] + 140} Q{P1[0]} {P1[1] + 140} {P2[0]} {P2[1] + 140}", stroke="#8b919b",
                    stroke_width=70, fill="none"))
    out.append(path(f"M{P0[0]} {P0[1] + 178} Q{P1[0]} {P1[1] + 178} {P2[0]} {P2[1] + 178}", stroke=WHITE,
                    stroke_width=4, fill="none", stroke_dasharray="30 18"))
    return out


# ---------------------------------------------------------------- the caution field
def car(color, trim, scale, number=None):
    body = [
        ellipse(0, 9, 34, 5, fill="#000", opacity=0.25),
        path("M-40 5 L-40 -4 L-43 -9 L-36 -9 L-34 -6 Q-22 -8 -12 -8 L-5 -15 Q4 -17 13 -15 L22 -7 Q36 -6 41 -1 "
             "L41 5 Z", fill=color),
        path("M-3 -13.5 Q4 -15.5 12 -13.5 L18 -8 L-8 -8 Z", fill="#1a2030"),
        rect(-40, -1, 81, 3, fill=trim),
        circle(-25, 5, 6, fill="#16181d"), circle(27, 5, 6, fill="#16181d"),
        circle(-25, 5, 2.4, fill="#9aa0a8"), circle(27, 5, 2.4, fill="#9aa0a8"),
    ]
    if number:
        body += [circle(2, -1, 7.5, fill=WHITE, stroke=CORAL, stroke_width=1.6),
                 el("text", number, x=2, y=3.2, text_anchor="middle", fill=CORAL2,
                    font_family="Helvetica, Arial, sans-serif", font_size=11, font_weight=700)]
    return body


def field():
    out = []
    lane = -18  # slightly above the centreline: the field runs single file in the groove
    liveries = [(CORAL, WHITE), ("#2c5fd6", YEL), ("#222", CORAL), ("#7a3fa0", WHITE), (None, None),
                ("#0f8a7e", WHITE), ("#e8e8e8", "#2c5fd6"), ("#d43a6b", NAVY), ("#3b4256", YEL)]
    # pace car leads at the right, the field trails back to the left
    t0 = 0.86
    gap = 0.072
    positions = []
    for i in range(len(liveries) + 1):
        t = t0 - i * gap
        x, y, ang = bez(t)
        sc = 0.9 + 0.5 * t
        positions.append((x, y + lane, ang, sc))
    # pace car
    x, y, ang, sc = positions[0]
    pace = car(YEL, "#e0a800", 1)
    pace += [rect(-6, -21, 16, 4, rx=1.5, fill=CORAL2), rect(-6, -21, 7, 4, rx=1.5, fill="#ffb400")]
    out.append(circle(round(x, 1), round(y - 18 * sc, 1), 40 * sc, fill="url(#beacon)"))
    out.append(group(pace, transform=f"translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale({sc:.2f})"))
    star = None
    for i, (color, trim) in enumerate(liveries):
        x, y, ang, sc = positions[i + 1]
        if color is None:
            star = (x, y, ang, sc)
            continue
        out.append(group(car(color, trim, 1), transform=f"translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale({sc:.2f})"))
    # Larson's No. 5 (generic white livery) with a warm halo around it
    x, y, ang, sc = star
    out.insert(0, ellipse(round(x, 1), round(y, 1), 80 * sc, 46 * sc, fill="url(#halo)"))
    out.append(group(car(WHITE, CORAL, 1, number="5"),
                     transform=f"translate({x:.1f} {y:.1f}) rotate({ang:.1f}) scale({sc * 1.08:.2f})"))
    return out, (x, y - 20 * sc)


# ---------------------------------------------------------------- foreground: the pit box
ANT = (400, 300)


def pit_box():
    out = []
    # scaffold legs and cross bracing
    for x in (150, 370):
        out.append(rect(x - 7, 520, 14, 400, fill=NAVY2))
    for k in range(5):
        y = 560 + k * 75
        out.append(path(f"M150 {y} L370 {y + 60}", stroke=NAVY, stroke_width=6))
        out.append(path(f"M370 {y} L150 {y + 60}", stroke=NAVY, stroke_width=6))
    # equipment cabinet body
    out.append(rect(130, 610, 260, 150, fill=CORAL))
    out.append(rect(130, 610, 260, 16, fill=CORAL2))
    for k in range(4):
        out.append(rect(146 + k * 60, 640, 44, 100, rx=4, fill=CORAL2, opacity=0.55))
    # top deck and railing
    out.append(rect(110, 512, 300, 18, fill=NAVY))
    for x in range(118, 410, 24):
        out.append(rect(x, 470, 4, 44, fill="#c9ced6"))
    out.append(rect(110, 466, 300, 6, fill="#c9ced6"))
    # antenna mast at the deck's corner
    out.append(rect(ANT[0] - 3, ANT[1], 6, 512 - ANT[1], fill="#9aa0a8"))
    out.append(rect(ANT[0] - 10, ANT[1] + 40, 20, 26, rx=3, fill=NAVY))
    out.append(circle(ANT[0], ANT[1], 6, fill=CORAL2))
    # shadow of the box on pit road
    out.insert(0, poly([(130, 900), (390, 900), (560, 760), (300, 760)], fill="#000", opacity=0.12))
    return out


def headset(dark):
    return [path("M-6 -95 Q1.5 -104 9 -95", fill="none", stroke=dark, stroke_width=2.2),
            ellipse(-3.8, -87, 1.8, 2.6, fill=dark), path("M-4 -84 Q2 -78 7 -80", fill="none", stroke=dark,
                                                           stroke_width=1.2)]


def celebrants():
    cheer_a = Pose(back_arm=(-150, -10), front_arm=(145, -15), back_leg=(-8, 0), front_leg=(10, -4), head_tilt=-10)
    cheer_b = Pose(back_arm=(-140, -5), front_arm=(150, -10), back_leg=(-10, 0), front_leg=(8, 0), lean=-3,
                   head_tilt=-12)
    daniels = Look(skin="#e3b08f", top=NAVY, bottom="#2a2f3a", hair="#3b2a20", hair_style="short", face="shout",
                   extra=headset("#111"))
    hendrick = Look(skin="#e8b896", top=NAVY, bottom="#2a2f3a", hair="#efece6", hair_style="short", face="smile",
                    build=1.1, extra=headset("#111"))
    rays = []
    cx, cy = 255, 380
    for k in range(14):
        a0 = math.radians(k * 360 / 14)
        a1 = a0 + math.radians(9)
        rays.append(poly([(cx, cy), (round(cx + 330 * math.cos(a0), 1), round(cy + 330 * math.sin(a0), 1)),
                          (round(cx + 330 * math.cos(a1), 1), round(cy + 330 * math.sin(a1), 1))],
                         fill="#fff6c8", opacity=0.14))
    return [group(rays), figure(195, 514, 200, facing=1, pose=cheer_b, look=hendrick),
            figure(310, 514, 212, facing=1, pose=cheer_a, look=daniels)]


def radio(target):
    tx, ty = target
    out = []
    # dotted link from antenna to the car
    mx, my = (ANT[0] + tx) / 2, min(ANT[1], ty) - 120
    out.append(path(f"M{ANT[0]} {ANT[1]} Q{mx:.0f} {my:.0f} {tx:.0f} {ty:.0f}", fill="none", stroke=YEL,
                    stroke_width=4, stroke_dasharray="3 12", stroke_linecap="round", opacity=0.95))
    # expanding arcs from the antenna, and arriving rings around the car
    for k in range(1, 4):
        r = 22 * k
        out.append(path(f"M{ANT[0] + r * 0.7:.0f} {ANT[1] - r * 0.7:.0f} A{r} {r} 0 0 1 {ANT[0] + r:.0f} {ANT[1]:.0f}",
                        fill="none", stroke=YEL, stroke_width=4, opacity=1 - k * 0.22, stroke_linecap="round"))
        out.append(path(f"M{ANT[0] - r * 0.7:.0f} {ANT[1] - r * 0.7:.0f} A{r} {r} 0 0 0 {ANT[0] - r:.0f} {ANT[1]:.0f}",
                        fill="none", stroke=YEL, stroke_width=4, opacity=1 - k * 0.22, stroke_linecap="round"))
    for k in range(1, 3):
        out.append(circle(round(tx, 1), round(ty + 14, 1), 30 + k * 16, fill="none", stroke=YEL, stroke_width=3,
                          opacity=0.7 - k * 0.2))
    return out


def foreground():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#turf)", opacity=0.0)]
    # pit wall along the near side of pit road, with tire stacks
    out.append(path("M-20 760 Q700 640 1220 720 L1220 748 Q700 668 -20 788 Z", fill=WHITE))
    out.append(path("M-20 788 Q700 668 1220 748 L1220 760 Q700 680 -20 800 Z", fill="#c9ced6"))
    for x, y in [(860, 700), (920, 706), (890, 668), (1080, 716), (1140, 722)]:
        for k in range(3):
            out.append(ellipse(x, y - k * 16 + 4, 26, 9, fill="#16181d"))
            out.append(ellipse(x, y - k * 16, 26, 9, fill="#2a2d33"))
            out.append(ellipse(x, y - k * 16, 12, 4, fill="#111"))
    # infield texture
    out.append(path("M-20 800 Q700 680 1220 760 L1220 900 L-20 900 Z", fill="url(#crowd2)", opacity=0.12))
    return out


def build():
    body = []
    body += sky()
    body += grandstands()
    body += track()
    cars, target = field()
    body += cars
    body += foreground()
    people = celebrants()
    body.append(people[0])
    body += pit_box()
    body += people[1:]
    body += radio(target)
    body.append(grain_overlay(opacity=0.3))
    title = "Larson clinches a third NASCAR Cup title"
    desc = ("Editorial illustration of Homestead-Miami Speedway on a bright afternoon. In the foreground, two crew "
            "leaders in headsets throw their arms up on top of a tall coral-and-navy pit box. Beyond them the field "
            "circles in single file behind a yellow pace car under caution, with a white No. 5 car mid-pack, glowing. "
            "Yellow radio waves arc from the pit-box antenna to that car, showing Kyle Larson's third Cup Series "
            "championship clinched at the end of Stage 1 on Nov. 8, 2026. Palm trees and grandstands line the far side.")
    return document(defs(), body, title, desc)


if __name__ == "__main__":
    save(build(), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
