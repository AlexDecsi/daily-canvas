"""Daily artwork, 2026-11-13: the FAA halts departures nationwide; Logan's planes sit still.

Visual idea: the frozen sweep. From inside Logan's darkened terminal, stranded travelers
with their bags stand silhouetted at a vast window; outside, a line of parked jets waits
motionless at the gates, while behind the control tower a colossal radar scope rises
over the harbor like a setting sun, its sweep broken into interrupted, dashed arcs.
One far-off jet climbs out over the water (some transatlantic flights were let go).

Verified (brief): on Nov. 13, 2026 the FAA ordered a nationwide ground stop of departing
flights, citing communications and radar problems at air traffic control centers; it was
lifted that evening. At Logan departures were held, while some transatlantic flights left
case by case (NBC News, NBC10 Boston, AP via PBS and Boston.com).
Drawn: generic jets and terminal, a generic tower, a symbolic radar scope, generic
travelers. Not drawn: any cause, any named person, logos, text or departure boards.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-13"
R = rng(20261113)

# palette: twilight indigo and plum, tangerine horizon, radar teal, terminal ink
INK, INK2, INK3 = "#0c0a1c", "#15122d", "#211c42"
INDIGO, PLUM, ROSE = "#26235e", "#5a2f78", "#c0507a"
TANG, AMBER, CREAM = "#ff7a4d", "#ffb54a", "#fff1d6"
TEAL, TEAL2, TEAL3 = "#5ff0d6", "#2bb5a5", "#13645f"
JET, JET2 = "#e9e4f2", "#b9b2cf"

HORIZON = 590
RCX, RCY, RR = 790, 590, 330  # radar scope centre / radius


def defs():
    return [
        linear("sky", [(0, INK2), (0.35, INDIGO), (0.68, PLUM), (0.86, ROSE), (1, TANG)]),
        radial("scope", [(0, TEAL3, 0.95), (0.7, "#0f3c45", 0.85), (1, INDIGO, 0)]),
        radial("glow", [(0, AMBER, 0.75), (0.5, TANG, 0.25), (1, TANG, 0)]),
        linear("sweep", [(0, TEAL, 0), (1, TEAL, 0.55)], x2=1, y2=0),
        linear("floor", [(0, "#2a1f45"), (1, INK)]),
        linear("apron", [(0, "#3a2c5c"), (1, "#1c1636")]),
        linear("water", [(0, ROSE), (1, PLUM)]),
        blur("soft", 6), blur("rim", 2.5), blur("softer", 14), blur("haze", 30),
        halftone("dots", CREAM, dot=1.4, spacing=7),
        halftone("tdots", TEAL, dot=1.2, spacing=9, angle=30),
        el("clipPath", rect(0, 0, 1200, HORIZON), id="above"),
        grain_filter(strength=0.5),
    ]


def sky():
    out = [rect(0, 0, 1200, 900, fill="url(#sky)")]
    out.append(rect(0, 0, 1200, 360, fill="url(#dots)", opacity=0.07))
    for _ in range(40):  # first stars
        out.append(circle(R.uniform(0, 1200), R.uniform(0, 230), R.uniform(0.7, 1.8), fill=CREAM,
                          opacity=round(R.uniform(0.3, 0.8), 2)))
    out.append(ellipse(RCX, HORIZON, 560, 220, fill="url(#glow)"))
    return out


def radar():
    """A giant radar scope rising over the horizon, its sweep broken into stuttering arcs."""
    g = [circle(RCX, RCY, RR, fill="url(#scope)")]
    g.append(circle(RCX, RCY, RR, fill="url(#tdots)", opacity=0.35))
    for k in range(1, 5):
        g.append(circle(RCX, RCY, RR * k / 4, fill="none", stroke=TEAL, stroke_width=2, opacity=0.45))
    for a in range(0, 180, 30):
        ra = math.radians(a)
        g.append(path(f"M{RCX} {RCY} L{RCX + math.cos(ra) * RR:.1f} {RCY - math.sin(ra) * RR:.1f}",
                      stroke=TEAL, stroke_width=1.2, opacity=0.3))
    # the sweep wedge, frozen mid-turn
    a0, a1 = math.radians(118), math.radians(150)
    g.append(path(f"M{RCX} {RCY} L{RCX + math.cos(a0) * RR:.1f} {RCY - math.sin(a0) * RR:.1f} "
                  f"A{RR} {RR} 0 0 0 {RCX + math.cos(a1) * RR:.1f} {RCY - math.sin(a1) * RR:.1f} Z",
                  fill=TEAL, opacity=0.22))
    g.append(path(f"M{RCX} {RCY} L{RCX + math.cos(a1) * RR:.1f} {RCY - math.sin(a1) * RR:.1f}",
                  stroke=TEAL, stroke_width=4, opacity=0.9))
    # broken, interrupted echo arcs: the lost signal
    for k, rad in enumerate((RR * 0.97, RR * 0.82, RR * 0.64)):
        start = 18 + k * 9
        a = start
        while a < 165:
            seg = R.uniform(6, 16)
            b1, b2 = math.radians(a), math.radians(a + seg)
            jitter = R.choice((0, 0, 0, 7, -7))
            r2 = rad + jitter
            g.append(path(f"M{RCX + math.cos(b1) * r2:.1f} {RCY - math.sin(b1) * r2:.1f} "
                          f"A{r2:.1f} {r2:.1f} 0 0 0 {RCX + math.cos(b2) * r2:.1f} {RCY - math.sin(b2) * r2:.1f}",
                          fill="none", stroke=TEAL, stroke_width=5 - k, stroke_linecap="round",
                          opacity=round(R.uniform(0.45, 0.95), 2)))
            a += seg + R.uniform(5, 14)
    # frozen blips (aircraft still aloft)
    for _ in range(14):
        ang = math.radians(R.uniform(12, 170))
        d = R.uniform(0.25, 0.92) * RR
        x, y = RCX + math.cos(ang) * d, RCY - math.sin(ang) * d
        g.append(circle(round(x, 1), round(y, 1), 7, fill=TEAL, opacity=0.25, filter="url(#soft)"))
        g.append(circle(round(x, 1), round(y, 1), 3, fill=CREAM))
    g.append(circle(RCX, RCY, RR, fill="none", stroke=TEAL, stroke_width=5, opacity=0.8))
    return [group(g, clip_path="url(#above)")]


def skyline():
    """Boston's skyline across the harbor, low and hazy on the left."""
    out = []
    blds = [(40, 60, 70), (100, 40, 110), (140, 50, 85), (196, 34, 150), (232, 46, 120), (280, 26, 210),
            (310, 40, 140), (352, 30, 180), (386, 52, 100), (440, 36, 130), (480, 44, 80)]
    for x, w, h in blds:
        out.append(rect(x, HORIZON - h, w, h, fill="#3b2a66"))
        for wy in range(int(HORIZON - h + 12), HORIZON - 8, 14):
            if R.random() < 0.5:
                out.append(rect(x + 6, wy, w - 12, 3, fill=AMBER, opacity=0.35))
    # a tall glass slab and a tower with a mast
    out.append(poly([(280, HORIZON - 210), (306, HORIZON - 218), (306, HORIZON), (280, HORIZON)], fill="#47357a"))
    out.append(rect(199, HORIZON - 172, 28, 22, fill="#3b2a66"))
    out.append(rect(211, HORIZON - 200, 4, 30, fill="#3b2a66"))
    out.append(circle(213, HORIZON - 201, 2.5, fill=TANG))
    out.append(rect(0, HORIZON - 4, 520, 8, fill="#2e2152"))
    return [group(out, opacity=0.9)]


def climbing_jet():
    """A distant jet climbing out over the harbor, lights on."""
    x, y = 150, 300
    g = [path(f"M{x - 40} {y + 14} Q{x} {y} {x + 44} {y - 16} L{x + 48} {y - 12} Q{x + 6} {y + 8} {x - 38} {y + 20} Z",
              fill=CREAM),
         path(f"M{x - 2} {y + 4} L{x - 22} {y + 22} L{x - 12} {y + 22} L{x + 10} {y + 2} Z", fill=JET2),
         path(f"M{x - 36} {y + 15} L{x - 44} {y - 2} L{x - 34} {y + 1} L{x - 28} {y + 12} Z", fill=CREAM),
         circle(x + 47, y - 14, 3, fill=AMBER),
         circle(x - 44, y - 2, 6, fill=TANG, opacity=0.5, filter="url(#soft)")]
    trail = path(f"M{x - 40} {y + 18} Q{x - 160} {y + 70} {x - 260} {y + 160}", fill="none", stroke=CREAM,
                 stroke_width=3, opacity=0.25, stroke_dasharray="2 10", stroke_linecap="round")
    return [trail, group(g)]


def tower():
    """A tall control tower, its cab lit, silhouetted against the scope."""
    x = RCX
    out = [path(f"M{x - 22} {HORIZON} L{x - 14} 330 L{x + 14} 330 L{x + 22} {HORIZON} Z", fill=INK2),
           path(f"M{x - 14} 330 L{x - 46} 300 L{x + 46} 300 L{x + 14} 330 Z", fill=INK2),
           poly([(x - 52, 300), (x + 52, 300), (x + 60, 262), (x - 60, 262)], fill="#2a4e5a"),
           poly([(x - 52, 298), (x + 52, 298), (x + 58, 266), (x - 58, 266)], fill=TEAL, opacity=0.75),
           path(f"M{x - 64} 262 L{x + 64} 262 L{x + 40} 244 L{x - 40} 244 Z", fill=INK2),
           rect(x - 2, 214, 4, 32, fill=INK2),
           circle(x, 212, 4, fill=TANG),
           circle(x, 212, 12, fill=TANG, opacity=0.4, filter="url(#soft)")]
    for k in range(-3, 4):
        out.append(rect(x + k * 15 - 1, 266, 2, 32, fill=INK2))
    return out


def jet(x, y, s, flip=False, lit=True):
    """A parked jet seen side-on, nose at x. s = scale. Facing left unless flip."""
    d = -1 if flip else 1
    L = 300 * s
    H = 30 * s

    def X(v):
        return x + d * v

    body = path(f"M{X(0)} {y} Q{X(0)} {y - H * 0.55} {X(H * 0.9)} {y - H * 0.55} L{X(L * 0.82)} {y - H * 0.55} "
                f"L{X(L)} {y - H * 0.9} L{X(L)} {y - H * 0.2} L{X(L * 0.8)} {y + H * 0.45} "
                f"L{X(H * 0.6)} {y + H * 0.45} Q{X(0)} {y + H * 0.45} {X(0)} {y} Z", fill=JET)
    tail = path(f"M{X(L * 0.78)} {y - H * 0.5} L{X(L * 0.93)} {y - H * 2.7} L{X(L * 1.02)} {y - H * 2.7} "
                f"L{X(L * 0.98)} {y - H * 0.6} Z", fill=TANG)
    wing = path(f"M{X(L * 0.36)} {y + H * 0.2} L{X(L * 0.62)} {y + H * 0.35} L{X(L * 0.5)} {y + H * 0.42} "
                f"L{X(L * 0.34)} {y + H * 0.42} Z", fill=JET2)
    eng = ellipse(X(L * 0.42), y + H * 0.6, H * 0.75, H * 0.32, fill=JET2)
    belly = path(f"M{X(H * 0.6)} {y + H * 0.2} L{X(L * 0.8)} {y + H * 0.2} L{X(L * 0.8)} {y + H * 0.45} "
                 f"L{X(H * 0.6)} {y + H * 0.45} Z", fill=JET2, opacity=0.6)
    stripe = rect(min(X(H * 0.8), X(L * 0.8)), y + H * 0.02, abs(L * 0.8 - H * 0.8), H * 0.1, fill=ROSE)
    cock = path(f"M{X(H * 0.25)} {y - H * 0.2} L{X(H * 0.75)} {y - H * 0.42} L{X(H * 0.85)} {y - H * 0.2} Z", fill=INK2)
    wins = []
    for k in range(int((L * 0.68) / (9 * s + 3))):
        wx = X(H * 1.3 + k * (L * 0.68) / int((L * 0.68) / (9 * s + 3)))
        wins.append(rect(wx - 2 * s, y - H * 0.28, 4 * s, 5 * s, rx=1.5 * s, fill=AMBER if lit else INK3,
                         opacity=0.85 if lit else 1))
    gear = [rect(X(H * 0.7) - 2, y + H * 0.45, 4, H * 0.55, fill=INK2),
            circle(X(H * 0.7), y + H * 1.05, H * 0.18, fill=INK),
            rect(X(L * 0.5) - 3, y + H * 0.45, 6, H * 0.55, fill=INK2),
            circle(X(L * 0.5), y + H * 1.05, H * 0.2, fill=INK)]
    shadow = ellipse(X(L * 0.5), y + H * 1.25, L * 0.55, H * 0.18, fill=INK, opacity=0.45)
    beacon = [circle(X(L * 0.5), y - H * 0.6, 9 * s, fill="#ff3b3b", opacity=0.45, filter="url(#soft)"),
              circle(X(L * 0.5), y - H * 0.6, 3 * s, fill="#ff6b5b")]
    return [shadow, tail, eng, body, belly, stripe, wing, cock] + wins + gear + beacon


def apron():
    out = [rect(0, HORIZON, 1200, 140, fill="url(#apron)")]
    out.append(rect(0, HORIZON, 520, 12, fill="url(#water)", opacity=0.7))
    # taxiway lights and lead-in lines
    for k in range(26):
        out.append(circle(10 + k * 47, HORIZON + 22, 2.4, fill=TEAL if k % 2 else AMBER, opacity=0.85))
    for gx in (170, 470, 770, 1070):
        out.append(path(f"M{gx} {HORIZON + 30} L{gx - 30} 730", stroke=AMBER, stroke_width=3, opacity=0.5))
    # far row of tails at a remote terminal
    for k in range(9):
        tx = 560 + k * 72
        out.append(path(f"M{tx} {HORIZON + 2} L{tx + 10} {HORIZON - 26} L{tx + 18} {HORIZON - 26} L{tx + 16} {HORIZON + 2} Z",
                        fill=TANG if k % 3 == 0 else JET2, opacity=0.6))
    # parked jets nosed in, all waiting (overlap slightly so they read as a held queue)
    out += jet(90, 655, 0.82, lit=True)
    out += jet(470, 662, 0.9, lit=True)
    out += jet(860, 650, 0.78, lit=False)
    # jet bridges reaching to the doors
    for bx, by in ((60, 650), (440, 656), (830, 645)):
        out.append(poly([(bx - 60, by - 22), (bx + 30, by - 18), (bx + 30, by + 4), (bx - 60, by + 2)], fill=INK3))
        out.append(rect(bx - 56, by - 16, 80, 5, fill=AMBER, opacity=0.4))
    return out


def window_frame():
    """Terminal glass: heavy mullions, a top beam and reflections of the hall lights."""
    out = [rect(0, 0, 1200, 46, fill=INK), rect(0, 46, 1200, 10, fill=INK3)]
    for mx in (0, 300, 600, 900, 1200):
        out.append(rect(mx - 14, 0, 28, 740, fill=INK))
        out.append(rect(mx + 8, 56, 3, 680, fill=TANG, opacity=0.35))
    out.append(rect(0, 410, 1200, 8, fill=INK, opacity=0.85))
    # faint reflections of ceiling lights on the glass
    for k in range(8):
        cx = 80 + k * 150
        out.append(ellipse(cx, 92, 40, 6, fill=CREAM, opacity=0.12))
    out.append(rect(0, 730, 1200, 14, fill=INK3))
    return out


def floor():
    out = [rect(0, 744, 1200, 156, fill="url(#floor)")]
    # sky reflected in the polished floor
    out.append(rect(0, 744, 1200, 60, fill=TANG, opacity=0.12))
    out.append(ellipse(RCX, 772, 320, 24, fill=TEAL, opacity=0.2, filter="url(#softer)"))
    for k in range(4):
        out.append(path(f"M{RCX - 300 + k * 40} {760 + k * 9} Q{RCX} {752 + k * 14} {RCX + 300 - k * 40} {760 + k * 9}",
                        fill="none", stroke=TEAL, stroke_width=2, opacity=0.18, stroke_dasharray="18 14"))
    for k in range(7):
        out.append(path(f"M{k * 200 - 100} 900 L{k * 200 + 40} 744", stroke=CREAM, stroke_width=1, opacity=0.06))
    return out


def suitcase(x, y, w=52, h=70, color=TEAL3):
    return [rect(x, y - h, w, h, rx=4, fill=color), rect(x + 3, y - h + 5, w - 6, 3, fill=INK, opacity=0.3),
            rect(x + 3, y - h + 22, w - 6, 3, fill=INK, opacity=0.2),
            rect(x + w / 2 - 2.5, y - h - 40, 5, 40, fill="#555066"),
            rect(x + w / 2 - 11, y - h - 44, 22, 7, rx=3, fill="#555066"),
            rect(x + 1, y - h, 3, h, fill=AMBER, opacity=0.35),
            circle(x + 8, y + 3, 5, fill=INK), circle(x + w - 8, y + 3, 5, fill=INK)]


def lit(x, y, h, facing=1, pose=None, look=None, hand_items=None):
    """A figure plus a soft warm halo behind it: rim light from the twilight window."""
    from dataclasses import replace
    halo_look = replace(look, skin=AMBER, top=AMBER, top_shade=AMBER, bottom=AMBER, shoes=AMBER, hair=AMBER,
                        accent=None, face=None)
    halo = group([figure(x, y, h, facing=facing, pose=pose, look=halo_look)], opacity=0.85, filter="url(#rim)")
    return group([halo, figure(x, y, h, facing=facing, pose=pose, look=look, hand_items=hand_items)])


def travelers():
    out = []
    shadow = lambda x, y, w=40: ellipse(x, y + 3, w, 7, fill=INK, opacity=0.55)
    # 1. pointing at the planes that aren't moving, on the left
    out += [shadow(150, 860)]
    out += suitcase(56, 862, color="#8a3a5c")
    out.append(lit(150, 860, 230, facing=1,
                      pose=Pose(back_arm=(-20, 20), front_arm=(115, -5), back_leg=(-6, 0), front_leg=(8, 0),
                                head_tilt=-12),
                      look=Look(skin="#8d5a3f", top="#3a3470", bottom="#1b1838", hair="#140f12",
                                hair_style="short", coat=True)))
    # 2. companion looking up, hand at brow
    out += [shadow(285, 866)]
    out.append(lit(285, 866, 214, facing=1,
                      pose=Pose(back_arm=(-10, 10), front_arm=(150, 95), back_leg=(-4, 0), front_leg=(6, 0),
                                head_tilt=-20),
                      look=Look(skin="#e0b394", top="#b8456a", bottom="#22203f", hair="#5a3420",
                                hair_style="long", skirt=False)))
    # 3. seated on a suitcase, phone in hand (centre-right)
    out += [shadow(700, 872, 50)]
    out += suitcase(668, 872, w=96, h=84, color="#2b5d68")
    out.append(lit(700, 870, 200, facing=-1,
                      pose=Pose(back_arm=(30, 40), front_arm=(40, 90), back_leg=(80, -80), front_leg=(70, -75),
                                head_tilt=18),
                      look=Look(skin="#c48c68", top="#4c6b3a", bottom="#26243a", hair="#1d1514",
                                hair_style="cap"),
                      hand_items={"front": rect(-3, -6, 6, 10, rx=1.5, fill=TEAL, opacity=0.9)}))
    out.append(ellipse(708, 690, 22, 22, fill=TEAL, opacity=0.18, filter="url(#soft)"))
    # 4. parent and child at the glass, right side
    out += [shadow(940, 864)]
    out += suitcase(990, 866, color="#c76b2c")
    out.append(lit(940, 864, 226, facing=-1,
                      pose=Pose(back_arm=(-15, 15), front_arm=(-10, 20), back_leg=(-4, 0), front_leg=(5, 0),
                                head_tilt=-8),
                      look=Look(skin="#a86d4e", top="#2a2a58", bottom="#3a2d50", hair="#120e10",
                                hair_style="bun", coat=True)))
    out += [shadow(880, 868, 26)]
    out.append(lit(880, 868, 120, facing=-1,
                      pose=Pose(back_arm=(-5, 10), front_arm=(160, 10), back_leg=(-5, 0), front_leg=(6, 0),
                                head_tilt=-25),
                      look=Look(skin="#a86d4e", top=AMBER, bottom="#2b2b48", hair="#120e10", hair_style="short")))
    # 5. a traveler walking in with a bag, far right edge
    out += [shadow(1130, 876)]
    out.append(lit(1130, 876, 236, facing=-1,
                      pose=Pose(back_arm=(-30, 10), front_arm=(25, 10), back_leg=(-22, -10), front_leg=(20, 0)),
                      look=Look(skin="#f0c8a8", top="#5c2f6e", bottom="#1d1a34", hair="#c7a46a",
                                hair_style="short")))
    out += suitcase(1040, 878, color="#3a3470")
    return out


def build():
    d = defs()
    body = []
    body += sky()
    body += radar()
    body += skyline()
    body += climbing_jet()
    body += tower()
    body += apron()
    body += window_frame()
    body += floor()
    body += travelers()
    body.append(rect(0, 0, WIDTH, HEIGHT, fill="none", stroke=INK, stroke_width=60, opacity=0.45, filter="url(#soft)"))
    body.append(grain_overlay(opacity=0.3))
    title = "The FAA halts departures nationwide; planes wait at Boston Logan"
    desc = ("Editorial illustration. From inside a darkened airport terminal at twilight, travelers with suitcases "
            "stand at a tall window: one points at the planes, others look up or wait on their bags. Outside, three "
            "parked jets sit still at their gates. Behind a lit control tower, a giant radar scope rises over the "
            "horizon like a setting sun, its sweep broken into interrupted arcs, an illustrative symbol of the air "
            "traffic control communications problem. Far off, one jet climbs out over the harbor past the Boston "
            "skyline. It represents the FAA's nationwide ground stop of departing flights on Nov. 13, 2026, which "
            "held departures at Logan until it was lifted that evening.")
    return document(d, body, title, desc)


if __name__ == "__main__":
    save(build(), Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
