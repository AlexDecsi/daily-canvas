"""A small kit for drawing stylized people in the graphic-poster style.

A figure is built like a jointed puppet: a torso, a head with hair, and arms
and legs drawn as thick rounded strokes. Poses are set with joint angles, so
the same kit can draw someone walking, waving, speaking, carrying or crouching.

Angles are in degrees, measured from "hanging straight down":
positive swings the limb forward (toward where the figure faces), negative backward.

    figure(x, y, height, facing=1, pose=Pose(...), look=Look(...))

(x, y) is the point between the feet. By default faces are blank (no eyes or
mouth). Key figures can get a simple profile face with an expression via
Look(face="smile" | "speak" | "shout" | "frown" | "stern" | "pout" | "neutral").
"""

import math
from dataclasses import dataclass, field

from svg import circle, ellipse, group, path, rect


@dataclass
class Pose:
    # (upper-arm angle, elbow bend) for the back and front arm
    back_arm: tuple = (-15, 10)
    front_arm: tuple = (15, 10)
    # (thigh angle, knee bend) for the back and front leg
    back_leg: tuple = (-6, 0)
    front_leg: tuple = (6, 0)
    lean: float = 0          # whole-body lean forward, degrees
    head_tilt: float = 0     # degrees, positive looks down


@dataclass
class Look:
    skin: str = "#c98e6b"
    top: str = "#2f5d8a"         # shirt / jacket
    top_shade: str = None        # back-arm colour; defaults to a darker top
    bottom: str = "#2b2b38"      # trousers or skirt
    shoes: str = "#1d1b22"
    hair: str = "#2a1d18"
    hair_style: str = "short"    # short, long, bun, bald, cap, helmet, hood, swept, firehat
    skirt: bool = False
    coat: bool = False           # long coat covering the thighs
    accent: str = None           # tie / scarf / stripe colour
    long_tie: bool = False       # accent drawn as a long tie reaching the belt
    vest: bool = False           # reflective safety stripes on the torso
    face: str = None             # None (blank) or an expression name, see _face()
    build: float = 1.0           # torso width: 1.0 average, 1.3 broad
    extra: list = field(default_factory=list)  # extra SVG drawn in the figure's local frame


def _shade(hex_color, factor=0.78):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#{:02x}{:02x}{:02x}".format(*(int(c * factor) for c in (r, g, b)))


def _limb(x0, y0, a1, l1, bend, l2):
    """Return the elbow/knee and the hand/foot positions for a two-segment limb."""
    r1 = math.radians(a1)
    x1, y1 = x0 + math.sin(r1) * l1, y0 + math.cos(r1) * l1
    r2 = math.radians(a1 + bend)
    return (x1, y1), (x1 + math.sin(r2) * l2, y1 + math.cos(r2) * l2)


def _stroke(points, width, color):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
    return path(d, fill="none", stroke=color, stroke_width=width, stroke_linecap="round",
                stroke_linejoin="round")


def figure(x, y, height, facing=1, pose=None, look=None, hand_items=None):
    """Draw one person. hand_items: {"front": svg, "back": svg} drawn at the hands (local, unscaled)."""
    pose = pose or Pose()
    look = look or Look()
    hand_items = hand_items or {}
    s = height / 100.0
    hip = (0, -46)
    neck_y = -46 - 30
    out_back, out_body, out_front = [], [], []

    # legs (knee bend is negative: shins swing backward)
    def leg(angles, color, shoe):
        a, bend = angles
        knee, foot = _limb(hip[0], hip[1], a, 23, bend, 24)
        return [_stroke([hip, knee, foot], 10, color),
                ellipse(foot[0] + 2.5, foot[1] + 1, 6, 3, fill=shoe)]

    out_back += leg(pose.back_leg, _shade(look.bottom, 0.8), look.shoes)
    out_front += leg(pose.front_leg, look.bottom, look.shoes)

    if look.skirt:
        out_front.append(path("M-8 -50 L8 -50 L13 -24 L-13 -24 Z", fill=look.bottom))
    if look.coat:
        out_front.append(path("M-9 -72 L9 -72 L12 -26 L-12 -26 Z", fill=look.top))

    # arms
    def arm(angles, color, side_x, item):
        a, bend = angles
        shoulder = (side_x, neck_y + 4)
        elbow, hand = _limb(shoulder[0], shoulder[1], a, 17, bend, 16)
        parts = [_stroke([shoulder, elbow, hand], 7.5, color), circle(hand[0], hand[1], 3.4, fill=look.skin)]
        if item:
            parts.append(group([item], transform=f"translate({hand[0]:.1f} {hand[1]:.1f})"))
        return parts

    back_color = look.top_shade or _shade(look.top)
    out_back += arm(pose.back_arm, back_color, -5 * look.build, hand_items.get("back"))

    # torso
    torso = [path(f"M-10.5 {neck_y + 4} Q-10 {neck_y - 1} 0 {neck_y - 1} Q10 {neck_y - 1} 10.5 {neck_y + 4} "
                  f"L9 {neck_y + 16} L8 -45 L-8 -45 L-9 {neck_y + 16} Z", fill=look.top)]
    if look.vest:
        torso += [path(f"M-9.5 {neck_y + 12} L9.5 {neck_y + 12} L9.2 {neck_y + 15} L-9.2 {neck_y + 15} Z", fill="#e6e8ea"),
                  path(f"M-8.5 {neck_y + 22} L8.5 {neck_y + 22} L8.3 {neck_y + 25} L-8.3 {neck_y + 25} Z", fill="#e6e8ea")]
    if look.accent and look.long_tie:
        torso += [path(f"M-3 {neck_y} L3 {neck_y} L1.5 {neck_y + 3} L-1.5 {neck_y + 3} Z", fill="#ffffff"),
                  path(f"M-1.6 {neck_y + 2.5} L1.6 {neck_y + 2.5} L3 {neck_y + 30} L0 {neck_y + 33} L-3 {neck_y + 30} Z",
                       fill=look.accent)]
    elif look.accent:
        torso.append(path(f"M0 {neck_y + 1} L2.5 {neck_y + 12} L0 {neck_y + 20} L-2.5 {neck_y + 12} Z", fill=look.accent))
    torso.append(path(f"M-7 -47 L7 -47 L7 -44 L-7 -44 Z", fill=_shade(look.bottom, 0.9)))  # belt line
    out_body.append(group(torso, transform=f"scale({look.build:.2f} 1)"))

    # head and hair
    head = []
    hx, hy = 1.5, neck_y - 10
    head.append(path(f"M-2 {neck_y + 1} L-2 {neck_y - 4} L3 {neck_y - 4} L3 {neck_y + 1} Z", fill=look.skin))  # neck
    style = look.hair_style
    if style == "long":
        head.append(path(f"M{hx - 9} {hy - 2} Q{hx - 10} {hy + 16} {hx - 4} {hy + 18} L{hx + 2} {hy + 4} Z", fill=look.hair))
    head.append(ellipse(hx, hy, 7.5, 8.5, fill=look.skin))
    head.append(path(f"M{hx + 6.5} {hy - 1} L{hx + 9.5} {hy + 2.5} L{hx + 6.8} {hy + 3} Z", fill=look.skin))  # nose
    if style in ("short", "long", "bun"):
        head.append(path(f"M{hx - 8} {hy + 1} Q{hx - 9} {hy - 10} {hx} {hy - 9.5} Q{hx + 8} {hy - 9} {hx + 7.8} {hy - 2} "
                         f"Q{hx + 2} {hy - 5} {hx - 2} {hy - 3} Q{hx - 4} {hy + 2} {hx - 8} {hy + 1} Z", fill=look.hair))
    if style == "bun":
        head.append(circle(hx - 6, hy - 7, 4.2, fill=look.hair))
    if style == "cap":
        head.append(path(f"M{hx - 8} {hy - 1} Q{hx} {hy - 13} {hx + 8} {hy - 1} Z", fill=look.hair))
        head.append(path(f"M{hx + 5} {hy - 2} L{hx + 13} {hy - 1} L{hx + 5} {hy + 0.5} Z", fill=look.hair))
    if style == "hood":
        head.append(path(f"M{hx - 10} {hy + 6} Q{hx - 11} {hy - 13} {hx + 1} {hy - 12} Q{hx + 11} {hy - 11} {hx + 9} {hy}"
                         f" L{hx + 6} {hy - 3} Q{hx} {hy - 9} {hx - 6} {hy - 2} L{hx - 6} {hy + 8} Z", fill=look.hair))
    if style == "helmet":
        head = [ellipse(hx, hy, 11, 11.5, fill="#f4f1ea", stroke="#c9c4ba", stroke_width=1),
                path(f"M{hx + 1} {hy - 6} Q{hx + 11} {hy - 6} {hx + 10} {hy + 3} Q{hx + 8} {hy + 6} {hx + 1} {hy + 5} Z",
                     fill="#26324a"),
                path(f"M{hx + 4} {hy - 4} Q{hx + 8} {hy - 4} {hx + 8} {hy}", fill="none", stroke="#9fd0ff",
                     stroke_width=1.2, opacity=0.8)]
    if style == "swept":  # voluminous hair swept back with a forward swoop
        head.append(path(f"M{hx - 8.5} {hy + 4} Q{hx - 11.5} {hy - 6} {hx - 6} {hy - 12.5} Q{hx + 1} {hy - 17} {hx + 8.5} {hy - 12} "
                         f"Q{hx + 12} {hy - 9} {hx + 10.5} {hy - 5} Q{hx + 6} {hy - 7.5} {hx + 1} {hy - 6} "
                         f"Q{hx - 3} {hy - 4} {hx - 3.5} {hy + 1} Q{hx - 5} {hy + 4} {hx - 8.5} {hy + 4} Z", fill=look.hair))
        head.append(path(f"M{hx - 4} {hy - 9} Q{hx + 3} {hy - 13} {hx + 9} {hy - 9}", fill="none",
                         stroke=_shade(look.hair, 0.82), stroke_width=1))
    if style == "firehat":
        head.append(path(f"M{hx - 13} {hy - 2} Q{hx} {hy - 4} {hx + 14} {hy - 1} L{hx + 14} {hy + 1} "
                         f"Q{hx} {hy - 1} {hx - 13} {hy} Z", fill=look.hair))
        head.append(path(f"M{hx - 8} {hy - 2} Q{hx - 8} {hy - 14} {hx} {hy - 14} Q{hx + 8} {hy - 14} {hx + 8} {hy - 2} Z",
                         fill=look.hair))
        head.append(rect(hx - 2, hy - 13, 4, 7, fill="#ffd34d"))
    if look.face and style != "helmet":
        head += _face(hx, hy, look.face, look.skin)
    head_group = group(head, transform=f"rotate({pose.head_tilt:.0f} {hx:.1f} {neck_y:.1f})")

    front_parts = out_front + arm(pose.front_arm, look.top, 5 * look.build, hand_items.get("front"))
    local = out_back + out_body + [head_group] + front_parts + list(look.extra)
    transform = f"translate({x:.1f} {y:.1f}) scale({s * facing:.3f} {s:.3f}) rotate({pose.lean:.1f} 0 -46)"
    return group(local, transform=transform)


def _face(hx, hy, expression, skin):
    """A simple profile face (looking toward +x): one eye, one brow, a mouth."""
    ink = "#1a1414"
    brow_tilt = {"shout": 1.8, "frown": 1.6, "stern": 1.3, "pout": 0.8}.get(expression, -0.4)
    out = [ellipse(hx + 3.4, hy - 1.3, 1.05, 1.4, fill=ink),
           path(f"M{hx + 1.4} {hy - 4.4 - brow_tilt * 0.5} L{hx + 5.6} {hy - 4.2 + brow_tilt}",
                stroke=ink, stroke_width=1.1, stroke_linecap="round")]
    mx, my = hx + 4.6, hy + 4.6
    if expression == "smile":
        out.append(path(f"M{mx - 1.5} {my - 0.6} Q{mx + 0.5} {my + 1.6} {mx + 2.2} {my - 0.8}", fill="none",
                        stroke=ink, stroke_width=1, stroke_linecap="round"))
    elif expression == "shout":
        out.append(ellipse(mx + 0.9, my + 0.4, 1.5, 2.1, fill=ink))
    elif expression == "speak":  # mid-sentence: mouth open, brow relaxed (neutral tone, not angry)
        out.append(ellipse(mx + 0.9, my + 0.3, 1.2, 1.3, fill=ink))
    elif expression == "frown":
        out.append(path(f"M{mx - 1.4} {my + 0.8} Q{mx + 0.5} {my - 1} {mx + 2.2} {my + 0.6}", fill="none",
                        stroke=ink, stroke_width=1, stroke_linecap="round"))
    elif expression == "pout":  # pushed-forward pursed lips
        out.append(ellipse(mx + 2.2, my - 0.2, 1.6, 1.2, fill=_shade(skin, 0.72)))
    else:  # neutral / stern
        out.append(path(f"M{mx - 1} {my} L{mx + 2.2} {my}", stroke=ink, stroke_width=1, stroke_linecap="round"))
    return out


# A few ready-made poses
STAND = Pose()
WALK = Pose(back_arm=(-25, 15), front_arm=(25, 20), back_leg=(-20, -15), front_leg=(22, -4))
WAVE = Pose(back_arm=(-12, 10), front_arm=(160, -40), back_leg=(-14, -10), front_leg=(16, -4))
SPEAK = Pose(back_arm=(30, 60), front_arm=(70, -30), lean=4)
REACH_UP = Pose(back_arm=(140, 10), front_arm=(150, 0), back_leg=(-8, 0), front_leg=(8, 0), lean=-3)
CARRY = Pose(back_arm=(55, 50), front_arm=(60, 55), back_leg=(-16, -12), front_leg=(18, -4), lean=6)
CHEER = Pose(back_arm=(165, 0), front_arm=(170, 10), back_leg=(-8, 0), front_leg=(10, 0))
RUN = Pose(back_arm=(-50, 70), front_arm=(55, -80), back_leg=(-40, -60), front_leg=(45, -20), lean=14)
SIT = Pose(back_arm=(40, 40), front_arm=(45, 40), back_leg=(80, -85), front_leg=(85, -85))
HOSE = Pose(back_arm=(60, 10), front_arm=(75, -5), back_leg=(-22, -6), front_leg=(26, -4), lean=8)


# Palettes of skin tones so crowds are varied
SKIN = ["#f1c7a5", "#e0a982", "#c98e6b", "#a86f4c", "#7d4f35", "#5a3825"]
HAIR = ["#1e1512", "#3b2a20", "#6b4a2e", "#a3753f", "#d9c08a", "#8e8a86"]
