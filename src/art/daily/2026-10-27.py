"""Daily artwork, 2026-10-27: Grand jury declines to indict Cassidy Hutchinson.

Visual idea: an over-the-shoulder view into a lamplit grand jury room where a
towering, unsigned indictment sits on the table, while a huge halftone "memory"
disc behind the jurors replays the 2022 Jan. 6 testimony that prompted the case.

Verified (brief): a federal grand jury in Washington declined the Justice
Department's request to indict Hutchinson, the House Jan. 6 committee's star
witness in 2022. The charges sought were not made public.
Drawn: anonymous, generic grand jurors (private individuals) seated around the
proposed indictment, its signature line left blank; Hutchinson only as her
public 2022 testimony at a witness table, set apart in a halftone panel.
Not drawn because not verified: Trump, any vote count, Hutchinson today, a
courtroom verdict, any readable text.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from svg import *  # noqa: E402,F403
from people import HAIR, SKIN, SIT, Look, Pose, figure  # noqa: E402

DATE = "2026-10-27"
R = rng(20261027)
AUBERGINE, PLUM, PLUM2, DEEP = "#24142c", "#3c2047", "#4e2b5a", "#160c1b"
CORAL, CORAL2, ROSE, CREAM, LAMP = "#ec6a55", "#c94a3c", "#f5b5a2", "#f7ecda", "#ffd27a"
WOOD, WOOD2 = "#5a2f3c", "#40202b"
TABLE_Y = 618


def room():
    out = [rect(0, 0, WIDTH, HEIGHT, fill=AUBERGINE)]
    out += [rect(x, 0, 6, TABLE_Y, fill=PLUM, opacity=0.6) for x in range(30, WIDTH, 120)]   # panelled wall seams
    out.append(rect(0, TABLE_Y - 150, WIDTH, 10, fill=PLUM2))                               # dado rail
    return out


def memory_disc():
    """Hutchinson testifying before the House Jan. 6 committee (2022), as a halftone memory."""
    cx, cy, r = 400, 300, 255
    inner = [rect(cx - r, cy - r, 2 * r, 2 * r, fill=CORAL),
             rect(cx - r, cy - r, 2 * r, 2 * r, fill="url(#dots)", opacity=0.55),
             # hearing-room backdrop: tall dais panel and a flag-free pleated curtain band
             rect(cx - r, cy - r, 2 * r, 150, fill=CORAL2, opacity=0.7)]
    inner += [rect(x, cy - r, 18, 150, fill=ROSE, opacity=0.25) for x in range(cx - r, cx + r, 46)]
    hutch = figure(cx - 40, cy + 230, 330, 1, Pose(back_arm=(55, 45), front_arm=(70, 30), back_leg=(80, -85),
                                                   front_leg=(85, -85), lean=6),
                   Look(skin=ROSE, top=DEEP, top_shade="#0f0812", bottom=DEEP, hair="#f3d58e", hair_style="long",
                        face="speak", build=0.95))
    inner.append(hutch)
    # witness table with microphone and a blank nameplate, in front of her lap
    inner += [rect(cx - 160, cy + 92, 420, 22, fill=PLUM),
              rect(cx - 150, cy + 114, 400, 200, fill=PLUM2),
              path(f"M{cx + 100} {cy + 92} L{cx + 72} {cy + 30}", stroke=DEEP, stroke_width=6, stroke_linecap="round"),
              ellipse(cx + 68, cy + 22, 10, 14, fill=DEEP, transform=f"rotate(-25 {cx + 68} {cy + 22})"),
              rect(cx + 140, cy + 70, 90, 22, fill=CREAM, opacity=0.8)]
    out = [el("clipPath", circle(cx, cy, r), id="disc")]
    out.append(group(inner, clip_path="url(#disc)"))
    out.append(circle(cx, cy, r, fill="none", stroke=ROSE, stroke_width=10))
    out.append(circle(cx, cy, r + 18, fill="none", stroke=CORAL, stroke_width=3, opacity=0.6))
    return out


def lamp():
    return [path("M760 0 L760 120", stroke=DEEP, stroke_width=4),
            path("M712 150 Q760 96 808 150 Z", fill=DEEP),
            poly([(722, 150), (798, 150), (1010, TABLE_Y + 40), (510, TABLE_Y + 40)], fill="url(#cone)"),
            ellipse(760, 152, 34, 6, fill=LAMP)]


JURORS = [  # (x, facing, skin, hair, style, top)
    (300, 1, 1, 2, "long", "#3f6a5a"),
    (420, 1, 5, 0, "short", "#8a5a6a"),
    (560, 1, 2, 1, "short", "#6a4c7a"),
    (650, 1, 4, 0, "bun", "#2f5d6a"),
    (880, -1, 0, 3, "long", "#8a4b3a"),
    (975, -1, 3, 5, "bald", "#41506b"),
    (1075, -1, 5, 0, "short", "#7a6a3a"),
]


def jurors():
    out = []
    for x, facing, s, h, style, top in JURORS:
        out.append(figure(x, TABLE_Y + 88, 250, facing,
                          Pose(back_arm=(30, 60), front_arm=(45, 70), back_leg=(0, 0), front_leg=(4, 0),
                               lean=6, head_tilt=10),
                          Look(skin=SKIN[s], top=top, bottom="#2a1d30", hair=HAIR[h], hair_style=style)))
    return out


def table():
    return [poly([(150, TABLE_Y), (1200, TABLE_Y), (1200, TABLE_Y + 70), (90, TABLE_Y + 70)], fill=WOOD),
            rect(90, TABLE_Y + 70, 1110, 24, fill=WOOD2),
            rect(90, TABLE_Y + 94, 1110, 300, fill=DEEP),
            ellipse(760, TABLE_Y + 36, 300, 30, fill="url(#pool)")]


def indictment():
    """The proposed indictment: a thick stack, top sheet's signature line left blank."""
    x, y = 760, TABLE_Y + 40
    out = [ellipse(x + 30, y + 8, 190, 20, fill=DEEP, opacity=0.5)]
    for i in range(9):  # thick stack of pages
        out.append(rect(x - 150 + (i % 2) * 3, y - 10 - i * 7, 300, 8, fill=CREAM if i % 2 else "#e6d6bd"))
    top = y - 72
    out.append(poly([(x - 150, top), (x + 150, top), (x + 170, top - 220), (x - 130, top - 220)], fill=CREAM))
    for j in range(8):  # unreadable text lines
        yy = top - 200 + j * 18
        out.append(rect(x - 118 + j * 0.0, yy, 210 - (j % 3) * 40, 6, fill="#b8a99a"))
    out.append(rect(x + 20, top - 40, 116, 4, fill=CORAL2))       # foreperson's signature line, left blank
    out.append(rect(x + 18, top - 66, 120, 22, fill=LAMP, opacity=0.18))
    out += [rect(x - 6, top - 232, 52, 26, fill=DEEP, rx=3),           # binder clip
            path(f"M{x + 2} {top - 232} Q{x + 20} {top - 262} {x + 38} {top - 232}", fill="none", stroke="#8a8090",
                 stroke_width=4)]
    out.append(group([rect(-70, -5, 140, 10, fill=CORAL, rx=5), poly([(70, -5), (88, 0), (70, 5)], fill=CREAM)],
                     transform=f"translate({x + 210} {y + 4}) rotate(-12)"))  # pen, laid down unused
    return out


def foreground():
    """Over-the-shoulder framing: two dark juror silhouettes (head and shoulders) cut by the frame."""
    def bust(x, y, sc, flip, bun=False):
        parts = [path("M-150 260 Q-150 40 -40 20 L40 20 Q150 40 150 260 Z", fill="#120a17"),
                 rect(-22, -30, 44, 60, fill="#120a17"),
                 ellipse(0, -70, 62, 74, fill="#120a17"),
                 path("M-62 -70 Q-60 -150 4 -146 Q64 -142 62 -60 Q30 -110 -10 -104 Q-50 -100 -62 -70 Z", fill="#0b060e")]
        if bun:
            parts.append(circle(-38, -136, 30, fill="#0b060e"))
        return group(parts, transform=f"translate({x} {y}) scale({sc * flip} {sc})")
    return [bust(110, 760, 1.25, 1), bust(1110, 790, 1.15, -1, bun=True)]


defs = [grain_filter(), halftone("dots", CORAL2, dot=2.6, spacing=9),
        linear("cone", [(0, LAMP, 0.55), (1, LAMP, 0.05)]),
        radial("pool", [(0, LAMP, 0.55), (1, LAMP, 0)])]
body = (room() + memory_disc() + lamp() + jurors() + table() + indictment() + foreground()
        + [grain_overlay(opacity=0.35)])

save(document(defs, body,
              "Grand jury declines to indict Cassidy Hutchinson",
              "Graphic poster illustration: under a single hanging lamp, anonymous grand jurors sit around a table on "
              "which lies a thick proposed indictment with its signature line left blank and a pen set aside. Behind "
              "them, a large coral halftone disc recalls Cassidy Hutchinson, shoulder-length blonde hair, testifying at "
              "a witness table before the House Jan. 6 committee in 2022."),
     Path(__file__).resolve().parents[3] / "public" / "artwork" / f"{DATE}.svg")
