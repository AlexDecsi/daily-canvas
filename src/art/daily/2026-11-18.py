"""Daily artwork, 2026-11-18: Xi greets Trump on the tarmac in Shenzhen.

Visual idea: a welcome under a giant sun. From a low tarmac angle, the towering nose of Air Force One
and its boarding stairs fill the left of the frame; at the foot of the stairs Trump and Xi embrace,
silhouetted against an enormous low sun whose rings frame them like a spotlight. Shenzhen's skyline,
led by the needle of the Ping An Finance Center, sits on the horizon; small dancers with flowers and
blank flags line the apron, and press photographers frame the foreground.

Verified (brief): on Nov. 18 Trump arrived in Shenzhen for APEC; Xi greeted him at the foot of Air
Force One's stairs and their handshake became a hug (AP, CBS); AP reported dancers waving flowers and
flags. A first Trump-Xi-Putin meeting is set for Thursday (AP, CBS, NBC).
Drawn: Trump (tall, swept blond hair, dark suit, long red tie) and Xi (dark side-parted hair, dark
suit) embracing; a simplified VC-25 in its blue-and-white livery with no lettering; generic dancers
and press. The sun and its rings are illustrative, not a claim about the time of day.
Not drawn: Putin (his handshake with Trump happened elsewhere), the trilateral (not yet held), any
text, flag designs, slogans or red carpet.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-11-18"
R = rng(20261118)
OUT = Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg"

# palette: plum-to-coral sky, molten sun, teal-slate tarmac, Air Force One blues, ink
SKY1, SKY2, SKY3 = "#2b1847", "#8a2f6b", "#f2735a"
SUN, SUN2 = "#ffd36b", "#ffb04a"
TARMAC1, TARMAC2 = "#24364a", "#122030"
AF_BLUE, AF_LIGHT, AF_WHITE = "#1f3f8a", "#9fd0ea", "#f5f3ee"
INK = "#120d1f"
CITY = "#3c2353"

defs = [
    grain_filter(),
    linear("sky", [(0, SKY1), (0.5, SKY2), (1, SKY3)]),
    radial("sunglow", [(0, "#fff1c2", 0.95), (0.35, SUN, 0.75), (0.7, SUN2, 0.25), (1, SUN2, 0)], r=0.5),
    linear("tarmac", [(0, TARMAC1), (1, TARMAC2)]),
    linear("fuselage", [(0, AF_WHITE), (0.55, AF_WHITE), (0.56, AF_BLUE), (0.62, AF_BLUE), (0.63, AF_LIGHT), (1, "#7bb6d6")]),
    linear("shine", [(0, "#ffffff", 0.0), (0.5, "#ffe2b0", 0.45), (1, "#ffffff", 0.0)], x2=1, y2=0),
    radial("pool", [(0, "#ffcf7a", 0.55), (1, "#ffcf7a", 0)], r=0.5),
    halftone("dots", "#ffffff", dot=1.3, spacing=7),
    halftone("sundots", "#ff8a4a", dot=2.0, spacing=9, angle=20),
    blur("soft", 8),
]

body = []
# --- sky -------------------------------------------------------------------
body.append(rect(0, 0, 1200, 900, fill="url(#sky)"))
body.append(rect(0, 0, 1200, 620, fill="url(#dots)", opacity=0.06))

# --- the giant sun with rings (focal halo behind the embrace) ----------------
SX, SY = 760, 470
body.append(circle(SX, SY, 520, fill="url(#sunglow)"))
for i, r in enumerate((430, 360, 300)):
    body.append(circle(SX, SY, r, fill="none", stroke="#ffd9a0", stroke_width=3, opacity=0.18 + 0.08 * i))
for k in range(24):
    a0 = math.radians(k * 15 - 3)
    a1 = math.radians(k * 15 + 3)
    body.append(poly([(SX, SY), (round(SX + 900 * math.cos(a0), 1), round(SY + 900 * math.sin(a0), 1)),
                      (round(SX + 900 * math.cos(a1), 1), round(SY + 900 * math.sin(a1), 1))],
                     fill="#ffb86b", opacity=0.10))
body.append(circle(SX, SY, 250, fill=SUN))
body.append(circle(SX, SY, 250, fill="url(#sundots)", opacity=0.35))
body.append(circle(SX, SY, 180, fill="#ffe08a", opacity=0.6))

# --- Shenzhen skyline on the horizon -----------------------------------------
HZ = 610
towers = [(380, 70, 120), (440, 40, 160), (480, 55, 110), (540, 45, 190), (900, 50, 170), (950, 70, 120),
          (1010, 40, 210), (1050, 60, 140), (1110, 50, 180), (1160, 60, 120), (330, 50, 90), (600, 60, 100),
          (840, 55, 130)]
for x, w, h in towers:
    body.append(rect(x, HZ - h, w, h, fill=CITY))
    for wy in range(HZ - h + 12, HZ - 8, 16):
        for wx in range(x + 8, x + w - 6, 12):
            if R.random() < 0.22:
                body.append(rect(wx, wy, 4, 6, fill="#ffcf7a", opacity=0.7))
# Ping An Finance Center: tall tapering tower with vertical ribs and a spire
PA = 1080
body.append(path(f"M{PA - 34} {HZ} L{PA - 26} {HZ - 300} Q{PA} {HZ - 345} {PA + 26} {HZ - 300} L{PA + 34} {HZ} Z",
                 fill="#2e1a44"))
for k in (-18, -6, 6, 18):
    body.append(path(f"M{PA + k * 1.6} {HZ} L{PA + k * 1.2} {HZ - 318}", stroke="#6a4a8a", stroke_width=2, opacity=0.8))
body.append(path(f"M{PA} {HZ - 335} L{PA} {HZ - 390}", stroke="#2e1a44", stroke_width=5))
body.append(rect(0, HZ - 6, 1200, 10, fill="#2a1840"))

# --- tarmac -----------------------------------------------------------------
body.append(rect(0, HZ, 1200, 900 - HZ, fill="url(#tarmac)"))
for i in range(-8, 16):
    body.append(path(f"M{SX + i * 40} {HZ} L{SX + i * 210} 900", stroke="#3a5068", stroke_width=2, opacity=0.35))
body.append(path(f"M{SX - 40} {HZ} L{SX - 330} 900", stroke="#ffd36b", stroke_width=6, opacity=0.85))  # taxi line
body.append(ellipse(SX, 700, 420, 70, fill="url(#pool)"))  # sun reflection on the apron
body.append(poly([(-40, 640), (540, 625), (470, 700), (-40, 760)], fill=INK, opacity=0.28, filter="url(#soft)"))

# --- Air Force One (simplified VC-25, nose toward the right, no lettering) -------
plane = []
# far wing and engines peeking under the fuselage
plane.append(poly([(-40, 470), (320, 430), (360, 455), (60, 520)], fill="#b9c8d6"))
for ex in (110, 230):
    plane.append(ellipse(ex, 520, 46, 24, fill="#cfd9e3"))
    plane.append(ellipse(ex + 38, 520, 10, 22, fill="#2a3442"))
# fuselage body (big, low angle)
plane.append(path("M-60 250 L470 250 Q560 250 600 300 Q622 330 600 360 Q560 410 470 412 L-60 412 Z",
                  fill="url(#fuselage)"))
# upper-deck hump
plane.append(path("M120 250 Q200 186 380 196 Q450 204 520 262 L470 252 L120 252 Z", fill=AF_WHITE))
# cockpit windows
plane.append(path("M528 272 Q556 280 574 300 L556 302 Q546 290 526 284 Z", fill="#1c2838"))
# window row along the blue cheatline
for wx in range(0, 460, 26):
    plane.append(rect(wx, 314, 11, 13, rx=4, fill="#1c2838"))
for wx in range(180, 430, 26):
    plane.append(rect(wx, 220, 9, 11, rx=3, fill="#1c2838"))
# forward door (open) where the stairs meet
plane.append(rect(430, 300, 38, 70, rx=4, fill="#ffe7b0"))
# warm rim light along the fuselage underside facing the sun
plane.append(path("M-60 408 L470 408 Q560 405 600 360", fill="none", stroke="#ffc46b", stroke_width=6, opacity=0.8))
plane.append(rect(-60, 270, 660, 30, fill="url(#shine)", opacity=0.5))
# near wing root and landing gear
plane.append(poly([(-60, 380), (260, 390), (300, 430), (-60, 450)], fill="#dfe6ee"))
plane.append(rect(380, 412, 16, 120, fill="#3a4452"))
plane.append(ellipse(388, 540, 22, 24, fill="#1a1f28"))
body.append(group(plane, transform="translate(-40 60) scale(1.0)"))

# boarding stairs from the door (≈ x 410-430, y 360-430 after transform) down to the apron
ST_TOP = (440, 430)
ST_BOT = (610, 730)
steps = []
n = 13
for i in range(n):
    t = i / n
    x = ST_TOP[0] + (ST_BOT[0] - ST_TOP[0]) * t
    y = ST_TOP[1] + (ST_BOT[1] - ST_TOP[1]) * t
    steps.append(rect(round(x, 1), round(y, 1), 70, 7, fill="#e9e4dc"))
body.append(poly([(ST_TOP[0] - 6, ST_TOP[1]), (ST_TOP[0] + 74, ST_TOP[1]), (ST_BOT[0] + 76, ST_BOT[1] + 10),
                  (ST_BOT[0] - 4, ST_BOT[1] + 10)], fill="#5a6577"))
body += steps
body.append(path(f"M{ST_TOP[0] + 72} {ST_TOP[1] - 40} L{ST_BOT[0] + 74} {ST_BOT[1] - 40}", stroke="#f0ebe2",
                 stroke_width=5))
body.append(path(f"M{ST_TOP[0]} {ST_TOP[1] - 40} L{ST_BOT[0]} {ST_BOT[1] - 40}", stroke="#c9c2b6", stroke_width=4))
# stair truck base
body.append(rect(560, 730, 150, 34, rx=6, fill="#3a4452"))
body.append(circle(585, 770, 14, fill="#151a22"))
body.append(circle(690, 770, 14, fill="#151a22"))

# --- dancers with flowers and blank flags (small, along the apron at right) -----
flower = group([circle(0, -4, 5, fill="#ff5a8a"), circle(4, 0, 4, fill="#ffd36b"), circle(-4, 1, 4, fill="#ff8ab0")])


def flag(col):
    return group([path("M0 0 L0 -26", stroke="#2a2a2a", stroke_width=1.4), rect(0, -26, 16, 11, fill=col)])


for i, x in enumerate(range(930, 1200, 46)):
    item = flower if i % 2 == 0 else flag("#e23b3b" if i % 4 == 1 else "#f6f1e6")
    body.append(figure(x, 690 + (i % 2) * 6, 92, facing=-1,
                       pose=Pose(back_arm=(-40, 20), front_arm=(150, 10) if i % 2 else (120, 20),
                                 back_leg=(-14, 0), front_leg=(16, -8), lean=-4 + 8 * (i % 2)),
                       look=Look(skin="#d9a27c", top="#e8445a" if i % 2 == 0 else "#f2b33d",
                                 bottom="#e8445a" if i % 2 == 0 else "#2f8f83", hair="#1a1210",
                                 hair_style="bun", skirt=i % 2 == 0),
                       hand_items={"front": item}))

# --- the embrace at the foot of the stairs ----------------------------------
# long shadows cast toward the viewer
body.append(poly([(660, 780), (760, 780), (700, 900), (520, 900)], fill=INK, opacity=0.35, filter="url(#soft)"))
TX, XX, GY = 672, 748, 780
trump = figure(TX, GY, 300, facing=1,
               pose=Pose(back_arm=(30, 40), front_arm=(40, 30), back_leg=(-6, 0), front_leg=(8, 0), lean=7,
                         head_tilt=4),
               look=Look(skin="#eab48c", top="#1a2036", bottom="#1a2036", hair="#f0c45a", hair_style="swept",
                         accent="#d3202f", long_tie=True, build=1.3, face="smile"))
xi = figure(XX, GY, 285, facing=-1,
            pose=Pose(back_arm=(35, 40), front_arm=(70, 25), back_leg=(-6, 0), front_leg=(8, 0), lean=7,
                      head_tilt=4),
            look=Look(skin="#e0b48c", top="#20232b", bottom="#20232b", hair="#141417", hair_style="short",
                      accent="#7a1f2b", build=1.3, face="smile"))
body.append(trump)
body.append(xi)
# Trump's arm reaching over Xi's shoulder to his back (drawn on top so the hug reads)
body.append(path(f"M{TX + 22} {GY - 196} Q{TX + 60} {GY - 212} {XX + 26} {GY - 186}", fill="none", stroke="#1a2036",
                 stroke_width=22, stroke_linecap="round"))
body.append(circle(XX + 30, GY - 182, 10, fill="#eab48c"))

# --- foreground press photographers (silhouettes framing the bottom corners) -----
cam = group([rect(-6, -6, 16, 11, rx=2, fill="#0a0812"), circle(10, -1, 5, fill="#0a0812"),
             circle(10, -1, 2.4, fill="#ffd36b", opacity=0.8)])
PRESS = "#0d0a18"
for x, h, f, arm in ((60, 340, 1, (100, 70)), (190, 300, 1, (110, 80)), (1165, 330, -1, (100, 70))):
    body.append(figure(x, 960, h, facing=f,
                       pose=Pose(back_arm=(80, 70), front_arm=arm, head_tilt=-4),
                       look=Look(skin=PRESS, top=PRESS, bottom=PRESS, shoes=PRESS, hair=PRESS, build=1.25),
                       hand_items={"front": cam}))

# two camera flashes popping toward the embrace
for fx, fy, sc in ((182, 646, 1.0), (1044, 656, 0.6)):
    pts = []
    for k in range(16):
        r = (34 if k % 2 == 0 else 9) * sc
        a = math.radians(k * 22.5)
        pts.append((round(fx + r * math.cos(a), 1), round(fy + r * math.sin(a), 1)))
    body.append(circle(fx, fy, round(44 * sc, 1), fill="#fff6d8", opacity=0.18))
    body.append(poly(pts, fill="#fffbe8", opacity=0.9))

body.append(grain_overlay(opacity=0.30))

title = "Xi greets Trump on the tarmac in Shenzhen"
desc = ("Editorial illustration. At the foot of Air Force One's boarding stairs, Donald Trump, with swept blond "
        "hair, a dark suit and a long red tie, embraces Xi Jinping, in a dark suit, against a huge low sun. The "
        "blue-and-white presidential jet towers on the left; Shenzhen's skyline, led by the Ping An Finance Center, "
        "lines the horizon; small dancers with flowers and blank flags stand on the apron at right, and silhouetted "
        "photographers frame the foreground. Represents Xi greeting Trump with a hug on his arrival in Shenzhen for "
        "the APEC summit on Nov. 18, 2026, ahead of a planned Trump-Xi-Putin meeting.")
save(document(defs, body, title, desc), OUT)
