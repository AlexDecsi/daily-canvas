"""Daily artwork, 2026-10-26: James Comey charged a third time.

Verified (brief): prosecutors charged former FBI Director James Comey with
transmitting national defense information, in court papers unsealed Monday;
it is the third attempt to prosecute him in about a year. Comey said in a
video statement that he is innocent.
Scene: Comey (very tall, receding grey hair, dark suit) speaking to a camera,
beside three case files, the newest with its seal broken open.
Not drawn because not verified: a courtroom, arrest, handcuffs, Trump, any text.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import Look, Pose, figure  # noqa: E402

DATE = "2026-10-26"
R = rng(20261026)
TEAL, TEAL2, TEAL3 = "#14393f", "#1d4c53", "#0e2a2f"
MUSTARD, MUSTARD2, PAPER, MANILA, MANILA2 = "#e9b33c", "#f3cd6a", "#f7f1e3", "#d9a95b", "#c4914a"
SEAL, WOOD, WOOD2, INK, CHARCOAL = "#b0232e", "#6b3b26", "#542c1c", "#17171c", "#2c2f38"


def backdrop():
    out = [rect(0, 0, WIDTH, HEIGHT, fill=TEAL)]
    out += [rect(x, 0, 70, HEIGHT, fill=TEAL2) for x in range(40, WIDTH, 190)]           # panelled wall
    out.append(circle(560, 330, 290, fill=MUSTARD))                                     # spotlight disc
    out.append(circle(560, 330, 290, fill="none", stroke=MUSTARD2, stroke_width=14))
    out.append(path("M1200 0 L1200 900 L760 900 Z", fill=TEAL3, opacity=0.55))          # diagonal shadow
    return out


def desk():
    out = [rect(60, 690, 820, 30, fill=WOOD, rx=4), rect(80, 720, 780, 180, fill=WOOD2),
           rect(80, 720, 780, 10, fill="#3e1f13")]
    out += [rect(x, 760, 300, 110, fill="none", stroke="#6e3c27", stroke_width=6, rx=4) for x in (130, 510)]
    out += [rect(x + 130, 806, 40, 10, fill=MUSTARD, rx=5) for x in (130, 510)]          # drawer pulls
    return out


def folders():
    out = []
    tones = ["#a9773a", MANILA2, MANILA]
    for i, (dx, rot) in enumerate([(-8, -3), (16, 2), (0, -1)]):                         # three case files, oldest at the bottom
        y = 676 - i * 30
        out.append(group([rect(-140, -26, 280, 32, fill=tones[i], stroke="#8a5f2c", stroke_width=2, rx=3),
                          rect(-128, -34, 76, 12, fill=tones[i], rx=3)],
                         transform=f"translate({250 + dx} {y}) rotate({rot})"))
    # the newest file, opened: papers fanned out, cord loose, seal snapped in two
    for k, (x, y, r) in enumerate([(195, 560, -14), (250, 550, -4), (300, 556, 9)]):
        lines = [rect(-50, -58 + j * 15, 100 - (j % 3) * 18, 5, fill="#b9b2a2") for j in range(6)]
        out.append(group([rect(-62, -72, 124, 104, fill=PAPER, stroke="#d8d0bd", stroke_width=2)] + lines,
                         transform=f"translate({x} {y}) rotate({r})"))
    out.append(path("M130 612 Q180 632 232 618 Q280 604 320 622 Q350 636 396 628", fill="none",
                    stroke=SEAL, stroke_width=4, stroke_linecap="round"))
    out.append(path("M372 628 a30 30 0 0 1 0 -56 l10 14 -8 12 8 10 z", fill=SEAL))        # wax seal, snapped in two
    out.append(path("M394 632 a30 30 0 0 0 6 -58 l-8 16 8 12 -10 12 z", fill=SEAL, transform="rotate(16 394 604)"))
    out.append(circle(380, 600, 12, fill="#8c1a23", opacity=0.6))
    return out


def comey():
    hair = "#b7b3ad"
    receding = [path("M-6.5 -82 Q-8.2 -88 -5 -93 Q-7 -87 -3.5 -83 Z", fill=hair),       # grey hair at back and side
                path("M-5.8 -93 Q0 -97.5 5 -95 Q0 -95.6 -4.8 -92 Z", fill=hair)]
    return figure(570, 965, 770, 1,
                  Pose(back_arm=(-6, 4), front_arm=(32, 92), back_leg=(-4, 0), front_leg=(5, 0), lean=-1, head_tilt=-3),
                  Look(skin="#e8b896", top=CHARCOAL, top_shade="#23252c", bottom=CHARCOAL, hair=hair, hair_style="bald",
                       accent="#3b5f9a", long_tie=True, face="speak", build=1.05, extra=receding))


def camera():
    out = [path(f"M985 560 L{x} 900", stroke="#101215", stroke_width=9, stroke_linecap="round") for x in (900, 985, 1075)]
    out += [rect(960, 548, 50, 18, fill="#101215", rx=3),
            rect(920, 470, 150, 86, fill="#22252c", rx=10), rect(940, 452, 56, 22, fill="#22252c", rx=5),
            rect(862, 486, 62, 56, fill="#191b20", rx=6), circle(862, 514, 30, fill="#101215"),
            circle(862, 514, 20, fill="#2e5d77"), circle(856, 506, 6, fill="#9fd0e6", opacity=0.8),
            circle(1048, 488, 7, fill="#ff3b30"), circle(1048, 488, 12, fill="#ff3b30", opacity=0.3)]
    return out


defs = [grain_filter()]
body = backdrop() + [comey()] + desk() + folders() + camera() + [grain_overlay(opacity=0.35)]

save(document(defs, body,
              "James Comey charged a third time",
              "Graphic poster illustration: former FBI Director James Comey, tall in a dark suit and blue tie, speaks "
              "toward a video camera on a tripod against a golden spotlight. On the desk beside him lie three case files; "
              "the newest is open, its papers fanned out and its red seal broken, representing charges unsealed in court."),
     Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
