"""Art study 1 (international/political): United Nations Headquarters at dusk.

View from the East River looking west: the Secretariat tower's glass face,
the General Assembly building's swooping roof to the right (north), the low
Conference building along the river, and the Chrysler Building's spire in the
Midtown skyline behind. Fictional scenario: an evening General Assembly session.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403

R = rng(1945)
WATER = 660


def sky():
    out = [rect(0, 0, WIDTH, WATER, fill="url(#sky)"),
           ellipse(250, WATER - 20, 520, 120, fill="url(#sunglow)")]
    for _ in range(40):
        out.append(circle(round(R.uniform(0, WIDTH), 1), round(R.uniform(10, 200), 1),
                          round(R.uniform(0.6, 1.6), 1), fill="#fff", opacity=round(R.uniform(0.3, 0.9), 2)))
    out += [circle(1010, 110, 26, fill="#fff6dc"), circle(1021, 102, 24, fill="#262b58")]  # crescent moon
    for y, x, w in [(250, 40, 380), (285, 760, 420), (330, 120, 300), (210, 820, 260), (360, 900, 280)]:
        out.append(ellipse(x + w / 2, y, w / 2, 7, fill="#f39a86", opacity=0.45, filter="url(#soft)"))
    return out


def skyline():
    """Midtown silhouettes behind the UN, with the Chrysler Building's crown."""
    out = []
    for color, lo, hi, density, glow in [("#6d5a88", 300, 470, 0.08, 0.35), ("#3b3a5e", 380, 540, 0.16, 0.6)]:
        x = -10
        while x < WIDTH:
            w = R.randint(36, 95)
            top = R.randint(lo, hi)
            out.append(rect(x, top, w, WATER - top, fill=color))
            if R.random() < 0.35:  # setback crown
                out.append(rect(x + w * 0.2, top - 18, w * 0.6, 18, fill=color))
            if R.random() < 0.3:  # rooftop water tank or antenna
                out.append(rect(x + w * 0.6, top - 12, 10, 12, fill=color))
                out.append(rect(x + w * 0.3, top - 30, 2, 30, fill=color))
            for wy in range(top + 10, WATER - 40, 14):
                if R.random() < 0.5:
                    continue
                for wx in range(x + 6, x + w - 8, 12):
                    if R.random() < density * 2:
                        out.append(rect(wx, wy, 5, 7, fill="#f6c97a", opacity=glow))
            x += w + R.randint(-4, 6)
        out.append(rect(0, lo - 40, WIDTH, WATER - lo + 40, fill="url(#haze)"))

    # Chrysler Building (left of the Secretariat, as seen from the river)
    cx, base, top = 300, WATER, 330
    out += [
        rect(cx - 34, top, 68, base - top, fill="#454468"),
        rect(cx - 26, top - 40, 52, 40, fill="#4a4a6e"),
    ]
    crown = []
    for i, (hw, h) in enumerate([(26, 30), (21, 28), (16, 26), (11, 24)]):
        y = top - 40 - sum(hh for _, hh in [(26, 30), (21, 28), (16, 26), (11, 24)][:i + 1])
        crown.append(path(f"M{cx - hw} {y + h} Q{cx} {y - h * .6} {cx + hw} {y + h} Z",
                          fill="#c8cbd8", stroke="#7f84a0", stroke_width=1.5))
        for k in range(-2, 3):  # the famous triangular sunburst windows
            crown.append(poly([(cx + k * hw / 3 - 3, y + h - 2), (cx + k * hw / 3 + 3, y + h - 2),
                               (cx + k * hw / 3, y + h - 10)], fill="#ffe6a3"))
    out += crown
    out.append(path(f"M{cx - 3} {top - 152} L{cx} {top - 215} L{cx + 3} {top - 152} Z", fill="#c8cbd8"))
    return out


def secretariat():
    x0, x1, top, base = 420, 680, 150, 610
    out = [
        # thin shadowed marble end wall (south), seen at a slight angle
        poly([(x0 - 18, top + 8), (x0, top), (x0, base), (x0 - 18, base)], fill="#b9b4ae"),
        rect(x0, top, x1 - x0, base - top, fill="url(#glass)"),
    ]
    floors, cols = 39, 26
    fh = (base - top) / floors
    cw = (x1 - x0) / cols
    mechanical = {5, 15, 27, 38}  # dark louvred bands on the real facade
    for f in range(floors):
        y = top + f * fh
        if f in mechanical:
            out.append(rect(x0, y, x1 - x0, fh, fill="#1f3340"))
            for c in range(cols * 3):
                out.append(rect(x0 + c * cw / 3 + 1, y + 2, 1.2, fh - 4, fill="#3b5566"))
            continue
        c = 0
        while c < cols:
            run = R.randint(1, 7)
            if R.random() < 0.45:
                color = R.choice(["#ffe2a0", "#ffd27a", "#fff1c9", "#ffc66b"])
                out.append(rect(x0 + c * cw + 1.2, y + 1.5, min(run, cols - c) * cw - 2.4, fh - 3,
                                fill=color, opacity=round(R.uniform(0.8, 1), 2)))
            c += run
    # mullions and spandrels
    for c in range(cols + 1):
        out.append(rect(x0 + c * cw - 0.6, top, 1.2, base - top, fill="#20343f", opacity=0.6))
    for f in range(floors + 1):
        out.append(rect(x0, top + f * fh - 0.5, x1 - x0, 1, fill="#20343f", opacity=0.5))
    out.append(rect(x0, top, x1 - x0, base - top, fill="url(#sheen)"))
    out.append(rect(x0, top - 6, x1 - x0, 6, fill="#d9d3c9"))  # roof parapet
    out.append(ellipse((x0 + x1) / 2, (top + base) / 2, 220, 300, fill="url(#towerglow)"))
    return out


def general_assembly():
    # low building with the concave, swooping roofline and a shallow dome
    return [
        path("M700 615 L700 530 Q850 590 1000 515 L1000 615 Z", fill="#e8e1d4", stroke="#9d978c", stroke_width=2),
        path("M700 530 Q850 590 1000 515", fill="none", stroke="#fffaf0", stroke_width=3),
        path("M818 560 Q850 522 882 560 Z", fill="#c9c6bd", stroke="#9d978c", stroke_width=2),
        rect(706, 590, 290, 6, fill="#9d978c", opacity=0.6),
    ] + [rect(712 + i * 18, 597, 10, 14, fill="#ffd894", opacity=0.9) for i in range(16)]


def conference_and_riverbank():
    out = [rect(340, 605, 720, 34, fill="#cfc8bb"),
           rect(340, 612, 720, 12, fill="#2b3d4a")]
    out += [rect(346 + i * 14, 614, 9, 8, fill="#ffe0a1") for i in range(51) if R.random() < 0.8]
    out += [rect(0, 639, WIDTH, 21, fill="#2a2a3e"),  # FDR Drive / river wall
            rect(0, 639, WIDTH, 3, fill="#55556e")]
    for _ in range(24):  # car lights on the drive
        x = R.uniform(0, WIDTH)
        out.append(rect(x, 646, 7, 2.5, fill=R.choice(["#ff6b5a", "#fff4d2"])))
    return out


def river():
    out = [rect(0, WATER, WIDTH, HEIGHT - WATER, fill="url(#water)")]
    out.append(rect(410, WATER, 280, 240, fill="url(#towerrefl)", filter="url(#wide)"))
    for i in range(6):  # broken bands of sunset colour on the water
        out.append(rect(round(R.uniform(0, 500), 1), WATER + 8 + i * 9, round(R.uniform(80, 260), 1), 2.5,
                        fill="#f3a17e", opacity=round(0.5 - i * 0.07, 2)))
    # reflection of the lit tower: soft vertical streaks
    refl = []
    for _ in range(140):
        x = R.uniform(425, 675)
        y = R.uniform(WATER + 6, WATER + 220)
        refl.append(rect(round(x, 1), round(y, 1), round(R.uniform(2, 6), 1), round(R.uniform(2, 5), 1),
                         fill=R.choice(["#ffd27a", "#ffe8b0"]), opacity=round(R.uniform(0.25, 0.7), 2)))
    out.append(group(refl, filter="url(#soft)"))
    for _ in range(60):  # ripples
        x, y = R.uniform(0, WIDTH), R.uniform(WATER + 10, HEIGHT)
        w = R.uniform(20, 90) * (y - WATER) / 200
        out.append(rect(round(x, 1), round(y, 1), round(w, 1), 1.6, fill="#8fb4d6", opacity=0.25))
    # a small ferry crossing, for scale and life
    out += [path("M820 760 L1010 760 L990 785 L840 785 Z", fill="#f2efe8"),
            rect(860, 738, 110, 22, fill="#f2efe8"),
            rect(880, 724, 60, 14, fill="#d94f3a")]
    out += [rect(868 + i * 13, 744, 8, 8, fill="#ffd894") for i in range(8)]
    out.append(ellipse(915, 790, 120, 8, fill="#ffffff", opacity=0.25))
    return out


def railing():
    """Promenade railing across the river, in silhouette, for depth."""
    out = [rect(0, 846, WIDTH, 6, fill="#0a0d1f"), rect(0, 878, WIDTH, 22, fill="#0a0d1f")]
    out += [rect(x, 846, 5, 40, fill="#0a0d1f") for x in range(10, WIDTH, 60)]
    for x in (150, 1060):  # lamp posts with warm halos
        out += [rect(x, 700, 6, 180, fill="#0a0d1f"), circle(x + 3, 696, 9, fill="#ffe3a6"),
                circle(x + 3, 696, 40, fill="url(#lamp)")]
    return out


defs = [
    linear("sky", [(0, "#1d2350"), (0.45, "#5a3f78"), (0.78, "#e2766a"), (1, "#f8b979")]),
    radial("sunglow", [(0, "#ffd79a", 0.75), (1, "#ffd79a", 0)]),
    linear("glass", [(0, "#41707f"), (1, "#1f3b4a")], x2=1, y2=1),
    linear("water", [(0, "#283a63"), (1, "#0c1430")]),
    blur("soft", 2.5),
    blur("wide", 8),
    linear("towerrefl", [(0, "#3d6b7c", 0.55), (1, "#3d6b7c", 0)]),
    linear("haze", [(0, "#e2766a", 0), (1, "#f0a080", 0.35)]),
    linear("sheen", [(0, "#f2a08a", 0.28), (0.5, "#f2a08a", 0), (1, "#000000", 0.2)]),
    radial("towerglow", [(0, "#ffd99a", 0.12), (1, "#ffd99a", 0)]),
    radial("lamp", [(0, "#ffe3a6", 0.5), (1, "#ffe3a6", 0)]),
]
body = sky() + skyline() + secretariat() + general_assembly() + conference_and_riverbank() + river() + railing() + [study_tag()]

save(document(defs, body,
              "Art study: an evening session at the United Nations",
              "The United Nations Secretariat tower at dusk, many windows lit, beside the General Assembly "
              "building's curved roof, seen across the East River with the Chrysler Building in the skyline "
              "and a ferry passing. Fictional scenario for an art study, not a news event."),
     Path(__file__).resolve().parents[3] / "prototypes" / "art" / "01-un-dusk.svg")
