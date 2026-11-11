"""Daily artwork, 2026-11-10: House Republicans elect Jim Jordan as their leader for the next Congress.

Visual idea: the secret ballot takes flight. From a low angle, Jim Jordan, in his
signature shirtsleeves, speaks into a thicket of reporters' microphones; behind him
a long ribbon of blank folded ballot slips streams up out of the dusk and coils
around a towering, glowing Capitol dome, the slips shrinking as they climb.

Verified (brief): on Nov. 10, 2026, House Republicans chose Rep. Jim Jordan (Ohio)
over Majority Leader Steve Scalise, 106-73, in a secret ballot at the Capitol; Jordan
then gave brief remarks (CBS News, CNBC, AP via PBS).
Drawn: Jordan (lean build, short brown-grey hair, white shirt, rolled-down sleeves,
tie, no jacket) speaking; generic reporters and a camera operator holding microphones,
phones and a TV camera toward him. The dome is a poster backdrop for Congress, and the
ballot ribbon is illustrative (blank slips, no count, no text).
Not drawn: no Scalise or Thune figure, no applause, no signs, quotes or text.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure, SKIN, HAIR  # noqa: E402

DATE = "2026-11-10"
R = rng(20261110)

# palette: dusk teal, plum, coral glow, cream marble, mustard accent
TEAL, TEAL2, TEAL3 = "#2f7377", "#174a55", "#0b2a33"
PLUM, PLUM2 = "#5a2a5e", "#331638"
CORAL, CORAL2 = "#ff8a5c", "#e0563f"
CREAM, CREAM2, CREAM3 = "#fbefd9", "#e9d3ae", "#c7a982"
MUST = "#f2c14e"
PAPER = "#fffaf0"
INK = "#14161f"


def defs():
    return [
        linear("sky", [(0, TEAL3), (0.45, TEAL2), (0.78, PLUM), (1, CORAL2)]),
        radial("halo", [(0, "#ffe3b8", 0.95), (0.45, CORAL, 0.55), (1, CORAL, 0)]),
        radial("rim", [(0, "#ffd9a8", 0.55), (1, "#ffd9a8", 0)]),
        linear("domefill", [(0, CREAM), (0.7, CREAM2), (1, CREAM3)], x2=1, y2=0),
        linear("ground", [(0, PLUM2), (1, INK)]),
        blur("soft", 16),
        blur("softer", 5),
        halftone("dots", TEAL3, dot=1.7, spacing=7),
        halftone("dotsw", CREAM3, dot=1.3, spacing=6),
        grain_filter(),
    ]


# ---------------------------------------------------------------- background
def sky():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#sky)")]
    out.append(rect(0, 0, WIDTH, 420, fill="url(#dots)", opacity=0.35))
    # concentric light rings behind the dome (graphic, like a poster sun)
    out.append(circle(400, 330, 430, fill="url(#halo)"))
    for r_, op in ((300, 0.18), (360, 0.12), (420, 0.08)):
        out.append(circle(400, 330, r_, fill="none", stroke="#ffe3b8", stroke_width=3, opacity=op))
    return out


def dome():
    """Stylised US Capitol dome: colonnaded drum, ribbed cast-iron dome, peristyle lantern, statue."""
    cx = 400
    out = []
    # base / attic block
    out.append(rect(cx - 250, 640, 500, 120, fill=CREAM3))
    out.append(rect(cx - 250, 640, 500, 14, fill=CREAM2))
    # lower drum with columns
    out.append(rect(cx - 205, 470, 410, 175, fill="url(#domefill)"))
    out.append(rect(cx - 215, 458, 430, 18, fill=CREAM))
    out.append(rect(cx - 215, 640, 430, 12, fill=CREAM3))
    for k in range(15):
        x = cx - 196 + k * 28
        shade = 0.35 + 0.5 * abs(k - 7) / 7
        out.append(rect(x, 480, 12, 158, fill=CREAM3, opacity=shade))
        out.append(rect(x + 2, 480, 3, 158, fill=PAPER, opacity=0.5))
    # upper drum with windows
    out.append(rect(cx - 170, 395, 340, 66, fill=CREAM2))
    out.append(rect(cx - 178, 388, 356, 12, fill=CREAM))
    for k in range(11):
        x = cx - 155 + k * 29
        out.append(rect(x, 410, 13, 36, rx=6, fill=TEAL2, opacity=0.65))
    # the dome shell
    out.append(path(f"M{cx - 165} 392 Q{cx - 160} 250 {cx} 205 Q{cx + 160} 250 {cx + 165} 392 Z",
                    fill="url(#domefill)"))
    for k in range(-5, 6):
        t = k / 6
        out.append(path(f"M{cx + 165 * t:.1f} 392 Q{cx + 130 * t:.1f} 270 {cx + 22 * t:.1f} 208",
                        fill="none", stroke=CREAM3, stroke_width=3, opacity=0.7))
    # band of small windows on the dome
    for k in range(-4, 5):
        out.append(rect(cx + k * 30 - 4, 330 - 6 * abs(k) ** 1.2, 8, 14, rx=3, fill=TEAL2, opacity=0.5))
    out.append(path(f"M{cx - 165} 392 Q{cx - 160} 250 {cx} 205 Q{cx - 60} 250 {cx - 80} 392 Z",
                    fill=TEAL3, opacity=0.12))
    # lantern
    out.append(rect(cx - 34, 150, 68, 60, fill=CREAM))
    for k in range(5):
        out.append(rect(cx - 28 + k * 13, 158, 5, 44, fill=CREAM3))
    out.append(path(f"M{cx - 42} 152 Q{cx} 108 {cx + 42} 152 Z", fill=CREAM2))
    out.append(ellipse(cx, 178, 26, 22, fill="#fff2c2", opacity=0.55, filter="url(#softer)"))
    # Statue of Freedom (generic small silhouette)
    out.append(rect(cx - 5, 92, 10, 20, fill=CREAM3))
    out.append(path(f"M{cx - 7} 92 L{cx + 7} 92 L{cx + 4} 62 L{cx - 4} 62 Z", fill=CREAM3))
    out.append(circle(cx, 57, 6, fill=CREAM3))
    out.append(path(f"M{cx - 5} 54 L{cx} 44 L{cx + 5} 54 Z", fill=CREAM3))
    # wings of the building receding at the base
    out.append(rect(0, 690, WIDTH, 210, fill="url(#ground)"))
    out.append(rect(0, 690, WIDTH, 8, fill=CREAM3, opacity=0.5))
    for k in range(26):
        out.append(rect(k * 48 + 6, 705, 14, 70, fill=CREAM3, opacity=0.18))
    return out


# ---------------------------------------------------------------- the ballot ribbon
def slip(cx, cy, w, rot, color=PAPER):
    h = w * 0.62
    body = [rect(-w / 2 + 3, -h / 2 + 4, w, h, fill=TEAL3, opacity=0.22),
            rect(-w / 2, -h / 2, w, h, fill=color),
            rect(-w / 2, -h / 2, w * 0.5, h, fill=CREAM2, opacity=0.55),
            path(f"M0 {-h / 2:.1f} L0 {h / 2:.1f}", stroke=CREAM3, stroke_width=max(0.8, w * 0.04))]
    return group(body, transform=f"translate({cx:.1f} {cy:.1f}) rotate({rot:.1f})")


def ribbon_point(t):
    """Path of the ballot stream: from low behind Jordan, sweeping left, coiling up around the dome."""
    x0, y0 = 1080, 860
    if t < 0.35:
        u = t / 0.35
        x = x0 + (640 - x0) * u
        y = y0 + (560 - y0) * u - 120 * math.sin(math.pi * u)
        return x, y
    u = (t - 0.35) / 0.65
    ang = math.pi * 0.05 + u * 2.3 * math.pi
    rad = 260 * (1 - 0.7 * u)
    x = 400 + rad * math.cos(ang)
    y = 560 - 470 * u + rad * 0.28 * math.sin(ang)
    return x, y


def ballots():
    out = []
    n = 96
    for i in range(n):
        t = i / (n - 1)
        x, y = ribbon_point(t)
        x += R.uniform(-22, 22)
        y += R.uniform(-16, 16)
        w = 46 - 34 * t + R.uniform(-4, 4)
        u = (t - 0.35) / 0.65
        behind = t > 0.35 and math.sin(math.pi * 0.05 + u * 2.3 * math.pi) < -0.2
        out.append((behind, slip(x, y, w, R.uniform(-60, 60), color=PAPER if not behind else CREAM2)))
    pts = " L".join(f"{ribbon_point(s / 90)[0]:.1f} {ribbon_point(s / 90)[1]:.1f}" for s in range(91))
    trail = path("M" + pts, fill="none", stroke="#fff2d6", stroke_width=26, opacity=0.10, filter="url(#softer)",
                 stroke_linecap="round")
    back = [s for b, s in out if b]
    front = [s for b, s in out if not b]
    return back, [trail] + front


# ---------------------------------------------------------------- Jordan
def jordan():
    look = Look(skin="#eab894", top="#f7f4ee", top_shade="#d9d4ca", bottom="#232838", hair="#7a6650",
                hair_style="short", accent="#2b4a8a", long_tie=True, face="speak", build=0.95,
                extra=[
                    # shirt collar points and a shadow fold down the shirt front
                    path("M-3.5 -76 L0 -72.5 L-1 -76.8 Z", fill="#d9d4ca"),
                    path("M3.5 -76 L0 -72.5 L1 -76.8 Z", fill="#d9d4ca"),
                    path("M-7 -66 Q-8 -56 -7 -48", fill="none", stroke="#d9d4ca", stroke_width=1.2),
                    # grey at the temple
                    path("M-6.5 -89 Q-4 -92 -1 -91", fill="none", stroke="#b8ada0", stroke_width=1.3),
                ])
    pose = Pose(back_arm=(8, 18), front_arm=(62, 62), back_leg=(-4, 0), front_leg=(4, 0), lean=3, head_tilt=-4)
    fig = figure(820, 1030, 790, facing=-1, pose=pose, look=look)
    rim = [ellipse(860, 560, 170, 330, fill="url(#rim)", filter="url(#soft)")]
    return rim + [fig]


def mouth_xy():
    s = 7.9
    # local face front ~(+9, -84), mirrored (facing left)
    return 820 - 9 * s, 1030 - 84 * s


# ---------------------------------------------------------------- the press
def microphones():
    mx, my = mouth_xy()
    out = []
    specs = [(-40, -18, CORAL, 300), (-56, 14, MUST, 340), (-30, 40, "#3d7ea6", 360), (-62, 52, CREAM, 380),
             (-46, -48, "#b23a48", 280)]
    for i, (dx, dy, col, length) in enumerate(specs):
        tip = (mx + dx, my + dy)
        ang = math.radians(200 + i * 6)
        end = (tip[0] + length * math.cos(ang) * -1 * -1, tip[1] - length * math.sin(ang))
        end = (tip[0] - length * 0.92, tip[1] + length * (0.35 + i * 0.08))
        out.append(path(f"M{end[0]:.1f} {end[1]:.1f} L{tip[0]:.1f} {tip[1]:.1f}", stroke=INK, stroke_width=9,
                        stroke_linecap="round"))
        # flag box on the shaft
        fx = tip[0] + (end[0] - tip[0]) * 0.22
        fy = tip[1] + (end[1] - tip[1]) * 0.22
        out.append(rect(round(fx - 13, 1), round(fy - 11, 1), 26, 22, rx=3, fill=col,
                        transform=f"rotate({math.degrees(math.atan2(end[1] - tip[1], end[0] - tip[0])):.0f} "
                                  f"{fx:.0f} {fy:.0f})"))
        out.append(ellipse(round(tip[0], 1), round(tip[1], 1), 15, 13, fill="#2a2d38"))
        out.append(ellipse(round(tip[0] - 4, 1), round(tip[1] - 4, 1), 5, 4, fill="#5a5f70"))
    return out


def press():
    out = []
    people = [
        # x, feet y, height, facing, look kwargs, pose, item
        (90, 1060, 520, 1, dict(skin=SKIN[4], top=TEAL, hair=HAIR[0], hair_style="bun"),
         Pose(back_arm=(100, 30), front_arm=(95, 20), lean=6), "phone"),
        (250, 1110, 560, 1, dict(skin=SKIN[1], top=PLUM, hair=HAIR[3], hair_style="short"),
         Pose(back_arm=(20, 30), front_arm=(120, 10), lean=4), "phone"),
        (470, 1180, 600, 1, dict(skin=SKIN[2], top="#3a4a5e", hair=HAIR[1], hair_style="cap"),
         Pose(back_arm=(70, 110), front_arm=(85, 100), lean=2), None),
    ]
    for x, fy, h, facing, kw, pose, item in people:
        look = Look(bottom=INK, shoes=INK, **kw)
        if item is None:
            hi = {}
        elif item == "phone":
            hi = {"front": group([rect(-4, -12, 8, 14, rx=1.5, fill=INK), rect(-3, -11, 6, 11, fill="#9fd6e0")])}
        else:
            hi = {"front": group([rect(-6, -18, 30, 16, rx=2, fill="#22252e"), circle(26, -10, 7, fill="#333846"),
                                  circle(26, -10, 4, fill="#7fb4c9"), rect(0, -24, 10, 6, fill="#22252e")])}
        out.append(figure(x, fy, h, facing=facing, pose=pose, look=look, hand_items=hi))
    # shoulder-mounted TV camera on the operator, lens toward Jordan
    out.append(group([
        rect(440, 612, 150, 58, rx=8, fill="#22252e"),
        rect(452, 598, 70, 16, rx=4, fill="#2f333e"),
        rect(590, 618, 34, 46, rx=4, fill="#2f333e"),
        circle(624, 641, 20, fill="#3a3f4d"), circle(624, 641, 12, fill="#7fb4c9"),
        rect(470, 625, 60, 6, rx=3, fill=CORAL, opacity=0.9),
    ]))
    # foreground band of heads and shoulders hides the legs and frames the bottom edge
    out.append(rect(0, 640, 640, 260, fill=TEAL3, opacity=0.25))
    for x, y, rx_, ry_ in ((40, 905, 120, 70), (330, 925, 150, 75), (640, 915, 130, 60), (960, 930, 200, 70)):
        out.append(ellipse(x, y, rx_, ry_, fill=INK))
    for x, y, r_ in ((150, 846, 34), (560, 862, 30), (900, 870, 36)):
        out.append(circle(x, y, r_, fill=INK))
    return out


def boom_and_crowd():
    """Creativity pass: a boom mic reaching over Jordan, a warm key light, and press heads in the foreground."""
    out = []
    beam = poly([(1210, -20), (1270, 120), (900, 560), (700, 470)], fill="#ffe6c2", opacity=0.13, filter="url(#soft)")
    out.append(beam)
    out.append(path("M1230 930 L905 265", stroke=INK, stroke_width=10, stroke_linecap="round"))
    out.append(ellipse(890, 245, 58, 24, fill="#3a3a44", transform="rotate(-20 890 245)"))
    for k in range(14):
        a = k / 14 * 2 * math.pi
        out.append(ellipse(round(890 + 52 * math.cos(a), 1), round(245 + 20 * math.sin(a), 1), 9, 6, fill="#4a4a56",
                           transform="rotate(-20 890 245)"))
    # foreground heads and shoulders of more press, seen from behind
    for x, y, rx_, ry_ in ((830, 930, 210, 150), (1110, 950, 140, 120), (840, 830, 175, 125)):
        out.append(ellipse(x, y, rx_, ry_, fill=INK))
    for x, y, r_ in ((835, 722, 54), (1060, 805, 40)):
        out.append(circle(x, y, r_, fill=INK))
        out.append(path(f"M{x - r_ * 0.9:.0f} {y - r_ * 0.3:.0f} Q{x} {y - r_ * 1.25:.0f} {x + r_ * 0.9:.0f} "
                        f"{y - r_ * 0.3:.0f}", fill="none", stroke=CORAL, stroke_width=3, opacity=0.55))
    return out


def flashes():
    out = []
    for x, y, r_ in ((640, 520, 34), (180, 560, 22)):
        pts = []
        for k in range(16):
            a = k * math.pi / 8
            rr = r_ if k % 2 == 0 else r_ * 0.22
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        out.append(circle(x, y, r_ * 1.4, fill="#fff6e0", opacity=0.3, filter="url(#softer)"))
        out.append(poly(pts, fill=PAPER))
    return out


def build():
    d = defs()
    body = []
    body += sky()
    back, front = ballots()
    body += back
    body += dome()
    body += front
    body += jordan()
    body += press()
    body += microphones()
    body += boom_and_crowd()
    body += flashes()
    body.append(rect(0, 0, WIDTH, HEIGHT, fill="none", stroke=INK, stroke_width=60, opacity=0.35, filter="url(#soft)"))
    body.append(grain_overlay(opacity=0.32))
    title = "House Republicans elect Jim Jordan as their leader"
    desc = ("Editorial illustration. From a low angle, Rep. Jim Jordan, lean with short brown-grey hair, in a white "
            "shirt and tie with no jacket, speaks into a cluster of reporters' microphones while reporters hold up "
            "phones and a camera operator films. Behind him, against a teal and coral dusk, a ribbon of blank folded "
            "ballot slips streams up and coils around a glowing Capitol dome, symbolising the secret ballot in which "
            "House Republicans chose him as their leader on Nov. 10, 2026.")
    return document(d, body, title, desc)


if __name__ == "__main__":
    save(build(), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
