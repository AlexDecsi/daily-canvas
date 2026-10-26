"""Art study 3 (environment): a hurricane nearing a coastline, seen from orbit at night.

Earth's limb glows along the top; a moonlit hurricane with a clear eye spirals
over dark ocean (counter-clockwise, as Northern Hemisphere storms turn); its
outer bands reach a coast traced by city lights; lightning flickers in the
bands; the edge of a space-station solar array frames the view.
Fictional scenario, not a specific storm.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403

R = rng(2005)
CX, CY = 640, 540  # storm centre
SQUASH = 0.78      # oblique view flattens the storm vertically

LAND = [(0, 540), (90, 560), (170, 600), (240, 660), (300, 720), (330, 790), (390, 860), (430, 900), (0, 900)]


def inside(pt, poly_pts):
    x, y = pt
    inside_ = False
    j = len(poly_pts) - 1
    for i, (xi, yi) in enumerate(poly_pts):
        xj, yj = poly_pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside_ = not inside_
        j = i
    return inside_


def space_and_earth():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="#03040c")]
    for _ in range(120):
        out.append(circle(round(R.uniform(0, WIDTH), 1), round(R.uniform(0, 170), 1),
                          round(R.uniform(0.4, 1.3), 1), fill="#ffffff", opacity=round(R.uniform(0.3, 0.9), 2)))
    out += [
        circle(600, 2700, 2565, fill="url(#limb)"),  # atmosphere glow
        circle(600, 2700, 2540, fill="url(#ocean)"),
        circle(600, 2700, 2540, fill="none", stroke="#7fc4ff", stroke_width=2, opacity=0.8),
    ]
    return out


def land():
    out = [poly(LAND, fill="#0d1410"),
           path("M0 540 L90 560 L170 600 L240 660 L300 720 L330 790 L390 860 L430 900",
                fill="none", stroke="#2a3b4f", stroke_width=2)]
    lights = []
    cities = [(70, 575, 30), (190, 640, 26), (280, 730, 34), (360, 840, 26), (90, 720, 40), (180, 820, 30)]
    for cx, cy, spread in cities:
        for _ in range(120):
            p = (R.gauss(cx, spread / 2), R.gauss(cy, spread / 2.6))
            if inside(p, LAND):
                lights.append(circle(round(p[0], 1), round(p[1], 1), round(R.uniform(0.6, 1.8), 1),
                                     fill=R.choice(["#ffcf73", "#ffb547", "#ffe6a8"]),
                                     opacity=round(R.uniform(0.5, 1), 2)))
    for _ in range(260):  # thin highways and towns between cities
        p = (R.uniform(0, 430), R.uniform(540, 900))
        if inside(p, LAND):
            lights.append(circle(round(p[0], 1), round(p[1], 1), 0.8, fill="#ffcf73", opacity=0.45))
    for (x0, y0), (x1, y1) in zip(LAND[:-2], LAND[1:-1]):
        for t in range(18):
            f = t / 18
            p = (x0 + (x1 - x0) * f - R.uniform(2, 10), y0 + (y1 - y0) * f + R.uniform(2, 10))
            if inside(p, LAND):
                lights.append(circle(round(p[0], 1), round(p[1], 1), round(R.uniform(0.8, 1.6), 1),
                                     fill="#ffd98a", opacity=0.9))
    out.append(group(lights))
    out.append(group([circle(c[0], c[1], c[2] * 1.4, fill="url(#cityglow)") for c in cities]))
    return out


def storm():
    out = [ellipse(CX, CY, 330, 330 * SQUASH, fill="url(#overcast)")]  # thin outflow haze
    puffs = []
    # three ragged rain bands of different lengths and widths, breaking up outward
    for phase, turns, width, n in [(0.3, 1.35, 1.0, 230), (2.4, 1.05, 0.8, 180), (4.3, 0.8, 0.65, 140)]:
        for i in range(n):
            s = i / n
            if s > 0.35 and R.random() < s * 0.45:  # gaps open up in the outer band
                continue
            theta = phase + s * turns * 2 * math.pi  # outward = clockwise on screen = counter-clockwise rotation
            r = 110 + s * 300
            x = CX + r * math.cos(theta) + R.uniform(-14, 14)
            y = CY + r * math.sin(theta) * SQUASH + R.uniform(-10, 10)
            rx = (40 - s * 18) * width * R.uniform(0.7, 1.3)
            ry = rx * R.uniform(0.35, 0.6)
            tangent = math.degrees(theta) + 90
            op = round(max(0.15, 0.8 - s * 0.6), 2)
            puffs.append(ellipse(round(x, 1), round(y, 1), round(rx, 1), round(ry, 1),
                                 fill=R.choice(["#e6edf7", "#cfdaea", "#f4f7fc", "#b9c7dc"]), opacity=op,
                                 transform=f"rotate({tangent:.0f} {x:.1f} {y:.1f})"))
    out.append(group(puffs, filter="url(#soft)"))
    # the dense central overcast: a big, lumpy, bright disc around the eye
    core = cloud_puffs(R, CX, CY, 270, 270 * SQUASH, 140, 18, 36, fill="#eef3fa", opacity=0.55)
    out.append(group(core, filter="url(#soft)"))
    out.append(ellipse(CX, CY, 135, 135 * SQUASH, fill="url(#cdo)"))
    # curved texture streaks on the core so it reads as rotating
    for k in range(10):
        a0 = k * 0.63
        r0 = 40 + k * 9
        x0, y0 = CX + r0 * math.cos(a0), CY + r0 * math.sin(a0) * SQUASH
        x1, y1 = CX + (r0 + 30) * math.cos(a0 + 1.1), CY + (r0 + 30) * math.sin(a0 + 1.1) * SQUASH
        out.append(path(f"M{x0:.0f} {y0:.0f} Q{CX + (r0 + 25) * math.cos(a0 + 0.5):.0f} "
                        f"{CY + (r0 + 25) * math.sin(a0 + 0.5) * SQUASH:.0f} {x1:.0f} {y1:.0f}",
                        fill="none", stroke="#aebdd4", stroke_width=7, opacity=0.3, stroke_linecap="round", filter="url(#soft)"))
    out += [ellipse(CX, CY, 17, 17 * SQUASH, fill="url(#eye)"),
            ellipse(CX, CY, 19, 19 * SQUASH, fill="none", stroke="#ffffff", stroke_width=4, opacity=0.95)]
    # lightning in the bands
    for _ in range(9):
        a = R.uniform(0, 2 * math.pi)
        r = R.uniform(90, 300)
        x, y = CX + r * math.cos(a), CY + r * math.sin(a) * SQUASH
        out += [circle(round(x, 1), round(y, 1), round(R.uniform(16, 30), 1), fill="url(#flash)"),
                circle(round(x, 1), round(y, 1), 2, fill="#ffffff")]
    return out


def solar_array():
    """Edge of a space-station solar array in the top-right corner, framing the view."""
    out = []
    panel = []
    for row in range(5):
        for col in range(9):
            x, y = 860 + col * 44, 40 + row * 30
            panel.append(rect(x, y, 42, 28, fill="url(#cell)", stroke="#b08a3c", stroke_width=1))
    out.append(group(panel, transform="rotate(-14 1000 100) translate(30 -40)"))
    out.append(rect(790, 110, 420, 8, fill="#9a9aa6", transform="rotate(-14 1000 100)"))
    return out


defs = [
    radial("limb", [(0.96, "#3b8fe0", 0), (0.985, "#4aa8ff", 0.55), (1, "#4aa8ff", 0)], r=0.5),
    linear("ocean", [(0, "#10284a"), (0.08, "#0b1b33"), (0.2, "#050d1c")]),
    radial("overcast", [(0, "#c9d6e8", 0.55), (1, "#c9d6e8", 0)]),
    radial("cdo", [(0, "#ffffff", 0.95), (0.6, "#e6edf7", 0.8), (1, "#e6edf7", 0)]),
    radial("eye", [(0, "#0a1426"), (1, "#3a5272")]),
    radial("flash", [(0, "#d8e8ff", 0.95), (1, "#9cc2ff", 0)]),
    radial("cityglow", [(0, "#ffb547", 0.25), (1, "#ffb547", 0)]),
    linear("cell", [(0, "#2a3f7a"), (1, "#16224a")], x2=1, y2=1),
    blur("soft", 3),
]
body = space_and_earth() + land() + storm() + solar_array() + [study_tag()]

save(document(defs, body,
              "Art study: a hurricane nears the coast, seen from orbit",
              "A large hurricane with a clear eye spirals counter-clockwise over a dark ocean at night, lit by "
              "moonlight and flickering with lightning; its outer bands reach a coastline traced by golden city "
              "lights, under the glowing curve of Earth's atmosphere, framed by a space-station solar panel. "
              "Fictional scenario for an art study."),
     Path(__file__).resolve().parents[3] / "prototypes" / "art" / "03-hurricane.svg")
