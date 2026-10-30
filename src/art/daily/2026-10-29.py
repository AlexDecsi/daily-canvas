"""Daily artwork, 2026-10-29: Probes into Alaska's two-Dan-Sullivan Senate ballot.

Visual idea: a ballot towers like a snow peak in the Alaskan night, under the
aurora and the Big Dipper, and small investigators' flashlight beams cross on
the two "Sullivan" lines while a news camera films from the snow.

Verified (brief): the Senate ballot lists "Sullivan, Dan S." (the Republican
incumbent) and "Sullivan, Daniel J. Jr."; Gov. Dunleavy ordered a state
Department of Public Safety investigation on Oct. 28; the Justice Department
issued new subpoenas on Oct. 29 (CBS, citing sources). No one has been charged.
Drawn: an illustrative ballot whose only readable text is those two verified
names; anonymous, generic investigators and a camera operator.
Not drawn because not verified or only alleged: Peltola, Trump, Dunleavy or
either Sullivan as people, any party label, other names, vote marks, results,
arrests or the word "fraud".
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import HAIR, SKIN, Look, Pose, figure  # noqa: E402

DATE = "2026-10-29"
R = rng(20261029)
NIGHT, NIGHT2, DEEP = "#0b1630", "#14254a", "#060c1c"
AURORA, AURORA2, VIOLET = "#46e3a6", "#22b5a4", "#7a5bd6"
SNOW, SNOW2, SNOWSH = "#eef4f8", "#c9d8e6", "#8fa6c4"
PAPER, PAPER2, INK = "#f6efdf", "#e2d6bd", "#1b2238"
BEAM, BEAM2 = "#ffd86a", "#ffb43c"
GROUND_Y = 760


def sky():
    out = [rect(0, 0, WIDTH, HEIGHT, fill="url(#sky)")]
    for _ in range(140):  # stars
        x, y = R.uniform(0, WIDTH), R.uniform(0, 520)
        out.append(circle(x, y, R.choice([0.8, 1.1, 1.5]), fill="#ffffff", opacity=R.uniform(0.35, 0.9)))
    # Big Dipper and Polaris (the stars on Alaska's flag), upper right
    dipper = [(905, 70), (965, 92), (1012, 128), (1062, 150), (1076, 210), (1150, 214), (1146, 158)]
    out += [circle(x, y, 3.2, fill="#fff6d0") for x, y in dipper]
    out.append(circle(1120, 40, 4.4, fill="#fff6d0"))
    return out


def aurora():
    """Aurora curtains: a wavy lower edge with vertical rays rising from it."""
    out = []
    bands = [(AURORA, 0.6, 250, 150), (AURORA2, 0.45, 300, 120), (VIOLET, 0.35, 205, 100)]
    for k, (color, op, base, tall) in enumerate(bands):
        edge = lambda x: base + 45 * __import__("math").sin(x / 170 + k * 1.7) + 20 * __import__("math").sin(x / 61 + k)
        d = f"M-20 {edge(-20):.0f} " + " ".join(f"L{x} {edge(x):.0f}" for x in range(0, 1240, 20))
        out.append(path(d + f" L1220 {edge(1220) - tall:.0f} L-20 {edge(-20) - tall:.0f} Z", fill=f"url(#curtain{k})",
                        opacity=op, filter="url(#soft)"))
        rays = []
        for x in range(-10, 1220, 23):  # soft rays fading upward
            h = tall * R.uniform(0.6, 1.5)
            rays.append(rect(x, edge(x) - h, R.choice([5, 8, 12]), h, fill=f"url(#curtain{k})",
                             opacity=R.uniform(0.25, 0.6)))
        out.append(group(rays, filter="url(#soft)"))
        out.append(path(d, fill="none", stroke=color, stroke_width=10, opacity=op, filter="url(#soft)"))
        out.append(path(d, fill="none", stroke=color, stroke_width=2.5, opacity=op))
    return out


def mountains():
    far = [(0, 560), (90, 470), (160, 520), (250, 400), (330, 470), (420, 380), (520, 470), (640, 420),
           (760, 360), (860, 450), (960, 390), (1060, 470), (1140, 410), (1200, 450), (1200, 640), (0, 640)]
    near = [(0, 640), (120, 560), (210, 610), (300, 545), (410, 625), (800, 625), (900, 540), (990, 600),
            (1090, 520), (1200, 590), (1200, 700), (0, 700)]
    out = [poly(far, fill="#2b3f6e"), poly(near, fill="#1d2d55")]
    # snow caps on the far range
    for (x0, y0), (x1, y1), (x2, y2) in zip(far, far[1:], far[2:]):
        if y1 < y0 and y1 < y2 and x1 < 1200:
            out.append(poly([(x1, y1), (x1 - 34, y1 + 40), (x1 - 12, y1 + 32), (x1, y1 + 46), (x1 + 16, y1 + 30),
                             (x1 + 38, y1 + 44)], fill=SNOW2, opacity=0.85))
    # spruce line
    for x in range(-10, 1220, 26):
        if 330 < x < 870:
            continue
        h = R.uniform(50, 95)
        base = 690 + R.uniform(-6, 8)
        out.append(poly([(x, base - h), (x - 13, base), (x + 13, base)], fill="#0d1a38"))
    return out


def ballot():
    """An illustrative ballot standing in the snow; the only readable text is the two verified names."""
    x0, y0, w, h = 345, 70, 510, 700
    out = [ellipse(x0 + w / 2, y0 + 120, 420, 260, fill="url(#halo)")]  # aurora glow behind the sheet
    sheet = [rect(x0, y0, w, h, fill=PAPER),
             rect(x0, y0, w, h, fill="url(#paperdots)", opacity=0.35),
             rect(x0 + w - 26, y0, 26, h, fill=PAPER2),                 # right edge in shade
             rect(x0 + 36, y0 + 40, w - 72, 46, fill=INK),              # header band (no text)
             rect(x0 + 36, y0 + 104, 260, 14, fill="#9aa0b3"),          # office line (unreadable)
             rect(x0 + 36, y0 + 128, 180, 10, fill="#b9bccb")]
    rows = [None, None, "SULLIVAN, DAN S.", "SULLIVAN, DANIEL J. JR.", None]
    ry = y0 + 175
    for i, name in enumerate(rows):
        y = ry + i * 96
        sheet.append(rect(x0 + 36, y - 6, w - 72, 2, fill="#c9c0aa"))
        sheet.append(ellipse(x0 + 72, y + 40, 20, 13, fill="none", stroke=INK, stroke_width=3))
        if name:
            sheet.append(rect(x0 + 30, y + 6, w - 60, 70, fill=BEAM, opacity=0.55))
            sheet.append(el("text", name, x=x0 + 108, y=y + 52, fill=INK, font_family="Helvetica, Arial, sans-serif",
                            font_size=31, font_weight=700, letter_spacing=0.5))
        else:
            sheet.append(rect(x0 + 108, y + 30, 200 + (i % 2) * 60, 16, fill="#9aa0b3"))
    sheet.append(rect(x0 + 36, ry + 5 * 96 - 6, w - 72, 2, fill="#c9c0aa"))
    sheet.append(rect(x0, y0, 7, h, fill=AURORA, opacity=0.8))          # aurora rim light on the left edge
    sheet.append(rect(x0, y0, w, 6, fill=AURORA, opacity=0.5))
    out.append(group(sheet, transform=f"rotate(-2.5 {x0 + w / 2} {y0 + h})"))
    # long shadow of the ballot stretching toward the viewer
    out.append(poly([(x0 + 10, GROUND_Y + 10), (x0 + w, GROUND_Y + 10), (x0 + w + 60, HEIGHT), (x0 + 60, HEIGHT)],
                    fill="url(#shadowfade)"))
    # snow drift banked against the foot of the ballot
    out.insert(-1, path(f"M{x0 - 140} {GROUND_Y + 30} Q{x0 + 40} {GROUND_Y - 70} {x0 + w / 2} {GROUND_Y - 45} "
                        f"Q{x0 + w - 30} {GROUND_Y - 85} {x0 + w + 150} {GROUND_Y + 30} Z", fill=SNOW))
    return out


def ground():
    return [rect(0, GROUND_Y - 70, WIDTH, HEIGHT, fill=SNOW2),
            path(f"M0 {GROUND_Y - 40} Q300 {GROUND_Y - 80} 600 {GROUND_Y - 50} Q900 {GROUND_Y - 20} 1200 {GROUND_Y - 60} "
                 f"L1200 {HEIGHT} L0 {HEIGHT} Z", fill=SNOW),
            path(f"M0 {GROUND_Y + 60} Q400 {GROUND_Y + 30} 800 {GROUND_Y + 70} Q1000 {GROUND_Y + 90} 1200 {GROUND_Y + 60} "
                 f"L1200 {HEIGHT} L0 {HEIGHT} Z", fill=SNOWSH, opacity=0.35)]


def footprints():
    out = []
    for (xa, ya), (xb, yb) in [((-10, 860), (180, GROUND_Y + 45)), ((870, HEIGHT + 10), (945, GROUND_Y + 40))]:
        for i in range(9):
            t = i / 9
            x, y = xa + (xb - xa) * t + (6 if i % 2 else -6), ya + (yb - ya) * t
            out.append(ellipse(x, y, 7 - 3 * t, 3.2 - 1.2 * t, fill=SNOWSH, opacity=0.7))
    return out


def flashlight():
    return group([rect(-3, -4, 22, 8, fill="#2a2f3a", rx=2), rect(17, -5.5, 6, 11, fill=BEAM)])


def investigators():
    """Two generic investigators in parkas, shining flashlights up at the two Sullivan lines."""
    out = []
    # beams first (behind the people), from each hand to a Sullivan row
    out.append(poly([(205, 655), (838, 395), (858, 470)], fill="url(#beam)", opacity=0.75))
    out.append(poly([(925, 652), (400, 490), (412, 565)], fill="url(#beam2)", opacity=0.75))
    out.append(poly([(170, GROUND_Y + 40), (200, GROUND_Y + 40), (120, HEIGHT), (40, HEIGHT)], fill=DEEP, opacity=0.15))
    out.append(poly([(938, GROUND_Y + 34), (962, GROUND_Y + 34), (1000, HEIGHT), (930, HEIGHT)], fill=DEEP, opacity=0.15))
    up = Pose(back_arm=(25, 20), front_arm=(128, -10), back_leg=(-12, -6), front_leg=(14, -2), lean=-4, head_tilt=-18)
    out.append(figure(185, GROUND_Y + 40, 175, 1, up,
                      Look(skin=SKIN[1], top="#c4392f", bottom="#22283a", hair="#1d2a44", hair_style="hood",
                           coat=True, face="stern"), {"front": flashlight()}))
    out.append(figure(950, GROUND_Y + 34, 168, -1, up,
                      Look(skin=SKIN[4], top="#2f5aa8", bottom="#1b2033", hair="#22304f", hair_style="hood",
                           coat=True, face="neutral"), {"front": flashlight()}))
    return out


def camera_operator():
    """A generic TV camera operator in the foreground, filming the ballot."""
    cam = group([rect(-10, -12, 30, 17, fill="#2a2f3a", rx=3), rect(19, -9, 9, 12, fill="#11151f"),
                 circle(28, -3, 4.5, fill="#3b6fb6", opacity=0.8), rect(-4, -17, 14, 5, fill="#11151f"),
                 circle(-12, -16, 1.6, fill="#ff4a3a")])
    pose = Pose(back_arm=(70, 60), front_arm=(95, 40), back_leg=(-30, -40), front_leg=(60, -90), lean=10,
                head_tilt=-10)
    return [ellipse(1120, 868, 90, 10, fill=DEEP, opacity=0.25),
            figure(1140, 872, 215, -1, pose,
                   Look(skin=SKIN[2], top="#3d4a5c", bottom="#1a1f2b", hair=HAIR[0], hair_style="cap",
                        coat=True), {"front": cam})]


def spruce(x, y, h, color):
    """A layered spruce silhouette, tip at (x, y - h)."""
    pts, tiers = [(x, y - h)], 7
    for i in range(1, tiers + 1):
        ty = y - h + h * i / tiers
        wdt = h * 0.06 + h * 0.3 * i / tiers
        pts = [(x - wdt, ty), *pts, (x + wdt, ty)]
        pts.insert(1, (x - wdt * 0.45, ty - h / tiers * 0.25))
        pts.insert(-1, (x + wdt * 0.45, ty - h / tiers * 0.25))
    return poly(pts, fill=color)


def foreground():
    """Dark spruces framing the left edge, cropped by the frame."""
    return [spruce(-20, HEIGHT + 30, 560, "#08132c"), spruce(70, HEIGHT + 60, 330, "#0b1834")]


defs = [grain_filter(), blur("soft", 6), halftone("paperdots", "#d8ccb0", dot=1.6, spacing=7),
        linear("shadowfade", [(0, SNOWSH, 0.55), (1, SNOWSH, 0)]),
        radial("halo", [(0, AURORA, 0.35), (1, AURORA, 0)]),
        linear("sky", [(0, DEEP), (0.55, NIGHT), (1, NIGHT2)]),
        *[linear(f"curtain{k}", [(0, c, 0.8), (1, c, 0)]) for k, c in enumerate((AURORA, AURORA2, VIOLET))],
        linear("beam", [(0, BEAM, 0.85), (1, BEAM, 0.15)], x2=1, y2=0),
        linear("beam2", [(0, BEAM, 0.15), (1, BEAM, 0.85)], x2=1, y2=0)]
body = (sky() + aurora() + mountains() + ground() + ballot() + footprints() + investigators() + camera_operator() + foreground()
        + [grain_overlay(opacity=0.3)])

save(document(defs, body,
              "Probes into Alaska's two-Dan-Sullivan Senate ballot",
              "Graphic poster illustration: under green aurora and the Big Dipper, a giant paper ballot stands like a "
              "mountain in the snow of Alaska. Its only readable lines, two names lit in yellow, read 'SULLIVAN, DAN "
              "S.' and 'SULLIVAN, DANIEL J. JR.'. Two small investigators in parkas shine flashlights up at those "
              "lines while a news camera operator films from the snow."),
     Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
