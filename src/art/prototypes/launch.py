"""Art study 2 (science/technology): a crewed rocket launch at twilight.

A generic two-stage rocket climbs from a coastal pad beside its lattice
service tower and lightning masts; the exhaust cloud billows across the pad,
the flame lights the lagoon, and spectators watch from a beach in the
foreground, some holding up phones. Fictional scenario, not a specific mission.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403

R = rng(1969)
HORIZON = 560
ROCKET_X = 620  # centre line of the rocket


def sky():
    out = [rect(0, 0, WIDTH, HORIZON + 5, fill="url(#sky)"),
           circle(ROCKET_X, 470, 420, fill="url(#flameglow)")]
    for _ in range(70):
        y = R.uniform(0, 260)
        out.append(circle(round(R.uniform(0, WIDTH), 1), round(y, 1), round(R.uniform(0.5, 1.5), 1),
                          fill="#ffffff", opacity=round(R.uniform(0.2, 0.8) * (1 - y / 300), 2)))
    return out


def far_shore():
    out = [path(f"M0 {HORIZON} L0 548 Q200 540 380 546 L900 544 Q1050 538 1200 548 L1200 {HORIZON} Z",
                fill="#1b2140")]
    # distant water tower and a low building on the horizon for a sense of place
    out += [ellipse(190, 500, 16, 12, fill="#1b2140"), rect(188, 510, 4, 38, fill="#1b2140"),
            rect(178, 528, 24, 2, fill="#1b2140"), rect(960, 528, 90, 18, fill="#1b2140")]
    return out


def tower():
    x0, x1, top, base = 690, 736, 250, 548
    out = [rect(x0, top, x1 - x0, base - top, fill="none", stroke="#c9563a", stroke_width=3)]
    y = top
    while y < base:  # lattice cross-bracing
        out.append(path(f"M{x0} {y} L{x1} {y + 20} M{x1} {y} L{x0} {y + 20}", stroke="#b04a33", stroke_width=1.5))
        out.append(rect(x0, y, x1 - x0, 2, fill="#c9563a"))
        y += 20
    out += [rect(x0 - 64, 352, 64, 6, fill="#c9563a"),  # crew access arm, swung away
            rect(x0 - 10, top - 50, 4, 50, fill="#c9563a"),
            circle(x0 - 8, top - 52, 3, fill="#ff5a4a")]
    for mx in (520, 790):  # lightning masts with catenary wires
        out += [rect(mx, 330, 5, 218, fill="#8a8fa8"), circle(mx + 2, 328, 3, fill="#ff5a4a")]
    out.append(path("M522 332 Q620 400 792 332", fill="none", stroke="#8a8fa8", stroke_width=1))
    out.append(rect(440, 544, 380, 6, fill="#3a3550"))  # pad deck
    return out


def plume():
    """The exhaust cloud: layers of puffs, darker at the top and lit orange from below."""
    out = []
    for cy, color, op, n in [(500, "#6d6380", 0.95, 70), (520, "#b58a86", 0.95, 80), (535, "#f3b37a", 0.9, 60)]:
        out += cloud_puffs(R, ROCKET_X, cy, 620, 90, n, 18, 46, fill=color, opacity=op)
    out += cloud_puffs(R, ROCKET_X - 260, 525, 200, 50, 26, 14, 30, fill="#8c7c8f", opacity=0.9)
    out += cloud_puffs(R, ROCKET_X + 270, 528, 200, 50, 26, 14, 30, fill="#8c7c8f", opacity=0.9)
    out += cloud_puffs(R, ROCKET_X - 130, 470, 150, 90, 30, 20, 40, fill="#7b6f8a", opacity=0.95)
    out += cloud_puffs(R, ROCKET_X + 140, 478, 150, 80, 30, 20, 40, fill="#7b6f8a", opacity=0.95)
    out += cloud_puffs(R, ROCKET_X - 120, 492, 140, 60, 24, 16, 30, fill="#d39a80", opacity=0.9)
    out += cloud_puffs(R, ROCKET_X + 130, 498, 140, 60, 24, 16, 30, fill="#d39a80", opacity=0.9)
    out += cloud_puffs(R, ROCKET_X, 505, 160, 50, 30, 12, 26, fill="#ffd9a0", opacity=0.9)
    out.append(ellipse(ROCKET_X, 505, 70, 26, fill="#fff3d0", opacity=0.9, filter="url(#soft)"))
    return [group(out)]


def flame_and_rocket():
    top, base = 70, 350
    w = 42
    out = [
        # exhaust column from nozzle to the cloud
        path(f"M{ROCKET_X - 12} {base + 10} Q{ROCKET_X - 30} 470 {ROCKET_X - 50} 515 "
             f"L{ROCKET_X + 50} 515 Q{ROCKET_X + 30} 470 {ROCKET_X + 12} {base + 10} Z",
             fill="#fff3c8", opacity=0.9, filter="url(#soft)"),
        ellipse(ROCKET_X, base + 60, 30, 70, fill="url(#flame)"),
        ellipse(ROCKET_X, base + 34, 11, 34, fill="#ffffff"),
        # body
        rect(ROCKET_X - w / 2, top + 60, w, base - top - 60, fill="url(#hull)"),
        rect(ROCKET_X - w / 2, top + 150, w, 10, fill="#2a2a33"),  # interstage band
        rect(ROCKET_X - w / 2, base - 18, w, 18, fill="#2a2a33"),  # engine section
        # crew capsule and launch-abort tower
        path(f"M{ROCKET_X - w / 2} {top + 60} L{ROCKET_X - 10} {top + 26} L{ROCKET_X + 10} {top + 26} "
             f"L{ROCKET_X + w / 2} {top + 60} Z", fill="#e9ebf2", stroke="#9aa0b4", stroke_width=1),
        rect(ROCKET_X - 2, top - 8, 4, 34, fill="#c5c9d6"),
        poly([(ROCKET_X - 4, top - 8), (ROCKET_X + 4, top - 8), (ROCKET_X, top - 22)], fill="#c5c9d6"),
        # warm light on the rocket's lower half from the flame
        rect(ROCKET_X - w / 2, base - 90, w, 72, fill="url(#underlight)"),
        # small fins
        poly([(ROCKET_X - w / 2, base - 30), (ROCKET_X - w / 2 - 12, base), (ROCKET_X - w / 2, base)], fill="#2a2a33"),
        poly([(ROCKET_X + w / 2, base - 30), (ROCKET_X + w / 2 + 12, base), (ROCKET_X + w / 2, base)], fill="#2a2a33"),
    ]
    # a US-style flag would assert a specific nation; keep the hull unmarked except a stripe
    out.append(rect(ROCKET_X - w / 2, top + 100, w, 4, fill="#c9563a"))
    return out


def lagoon():
    out = [rect(0, HORIZON, WIDTH, 170, fill="url(#water)")]
    # flame reflection: a broken column of warm ripples
    for i in range(46):
        y = HORIZON + 4 + i * 3.6
        spread = 20 + i * 2.6
        out.append(rect(round(ROCKET_X - spread / 2 + R.uniform(-14, 14), 1), round(y, 1),
                        round(spread * R.uniform(0.4, 1), 1), 2,
                        fill=R.choice(["#ffd27a", "#ffb35c", "#fff0c0"]), opacity=round(0.85 - i * 0.016, 2)))
    for _ in range(50):
        x, y = R.uniform(0, WIDTH), R.uniform(HORIZON + 6, HORIZON + 165)
        out.append(rect(round(x, 1), round(y, 1), round(R.uniform(15, 70), 1), 1.4, fill="#8aa0d0", opacity=0.25))
    return out


def person(x, base, h, phone=False, arms_up=False):
    """A simple standing silhouette, h pixels tall."""
    hw = h * 0.13
    head = h * 0.085
    sh = hw * 1.35  # shoulder half-width
    out = [circle(x, base - h + head, head * 1.05, fill="#0b0d18"),
           rect(round(x - head * 0.45, 1), round(base - h + head * 1.8, 1), round(head * 0.9, 1), round(head * 0.8, 1), fill="#0b0d18"),
           path(f"M{x - hw} {base} L{x - sh} {base - h * 0.62} Q{x - sh} {base - h * 0.78} {x - head} {base - h * 0.79} "
                f"L{x + head} {base - h * 0.79} Q{x + sh} {base - h * 0.78} {x + sh} {base - h * 0.62} L{x + hw} {base} Z",
                fill="#0b0d18")]
    if arms_up:
        out.append(path(f"M{x - hw} {base - h * 0.72} L{x - hw * 1.9} {base - h * 1.05} M{x + hw} {base - h * 0.72} "
                        f"L{x + hw * 1.9} {base - h * 1.05}", stroke="#0b0d18", stroke_width=h * 0.06, stroke_linecap="round"))
    if phone:
        out += [path(f"M{x + hw} {base - h * 0.7} L{x + hw * 1.6} {base - h * 0.95}", stroke="#0b0d18",
                     stroke_width=h * 0.06, stroke_linecap="round"),
                rect(round(x + hw * 1.4, 1), round(base - h * 1.04, 1), round(h * 0.07, 1), round(h * 0.1, 1),
                     fill="#bfe3ff", rx=1.5),
                circle(round(x + hw * 1.45, 1), round(base - h * 0.99, 1), round(h * 0.18, 1), fill="url(#screenglow)")]
    return out


def beach():
    out = [path("M0 730 Q300 712 600 724 Q900 736 1200 718 L1200 900 L0 900 Z", fill="#2b2333"),
           path("M0 730 Q300 712 600 724 Q900 736 1200 718", fill="none", stroke="#f0b27a", stroke_width=2, opacity=0.6)]
    # dune grass tufts on the right
    for _ in range(40):
        gx, gy = R.uniform(940, 1200), R.uniform(760, 900)
        for _ in range(5):
            out.append(path(f"M{gx:.0f} {gy:.0f} q{R.uniform(-8, 8):.0f} {-R.uniform(14, 34):.0f} {R.uniform(-16, 16):.0f} {-R.uniform(30, 50):.0f}",
                            fill="none", stroke="#14111c", stroke_width=2))
    # spectators: a back row (small) and a front row (larger), leaving the rocket's column clear
    for row_base, hmin, hmax, xs in [(760, 46, 60, range(60, 940, 34)), (930, 190, 220, [70, 250, 880])]:
        for x in xs:
            x = x + R.uniform(-8, 8)
            if row_base == 760 and abs(x - ROCKET_X) < 70:
                continue
            out += person(round(x, 1), row_base + R.uniform(-4, 4), R.uniform(hmin, hmax),
                          phone=R.random() < 0.35, arms_up=R.random() < 0.12)
    return out


defs = [
    linear("sky", [(0, "#0d1233"), (0.55, "#2c2d63"), (0.85, "#7a4a74"), (1, "#e98d6b")]),
    radial("flameglow", [(0, "#ffcc80", 0.55), (0.4, "#ff9a5c", 0.18), (1, "#ff9a5c", 0)]),
    radial("flame", [(0, "#ffffff"), (0.45, "#ffe08a"), (0.8, "#ff9a3c"), (1, "#ff6a2c", 0)], cy=0.3),
    linear("hull", [(0, "#c8ccd8"), (0.35, "#ffffff"), (1, "#9aa0b4")], x2=1, y2=0),
    linear("underlight", [(0, "#ffb070", 0), (1, "#ffb070", 0.6)]),
    linear("water", [(0, "#3a3466"), (1, "#141632")]),
    radial("screenglow", [(0, "#bfe3ff", 0.35), (1, "#bfe3ff", 0)]),
    blur("soft", 4),
]
body = sky() + far_shore() + tower() + flame_and_rocket() + plume() + lagoon() + beach() + [study_tag()]

save(document(defs, body,
              "Art study: a crewed rocket launch at twilight",
              "A white rocket rises on a bright flame from a coastal launch pad beside a red lattice tower, "
              "its exhaust cloud glowing orange; the flame reflects in a lagoon while silhouetted spectators "
              "on a beach watch, some holding up phones. Fictional scenario for an art study."),
     Path(__file__).resolve().parents[3] / "prototypes" / "art" / "02-launch.svg")
