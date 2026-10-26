"""Tiny helpers for writing SVG illustrations in Python.

Every artwork script builds a list of SVG element strings and passes it to
`document()`. Randomness always comes from a seeded generator, so running a
script twice produces exactly the same picture.
"""

import math
import random
from pathlib import Path

WIDTH, HEIGHT = 1200, 900  # 4:3, matches the gallery frames


def rng(seed):
    return random.Random(seed)


def attrs(**kw):
    """Turn keyword arguments into SVG attributes (stroke_width -> stroke-width)."""
    parts = []
    for k, v in kw.items():
        if v is None:
            continue
        name = k.rstrip("_").replace("_", "-")
        if isinstance(v, float):
            v = f"{v:.1f}".rstrip("0").rstrip(".")
        parts.append(f'{name}="{v}"')
    return " ".join(parts)


def el(tag, children=None, **kw):
    a = attrs(**kw)
    if children is None:
        return f"<{tag} {a}/>"
    inner = "".join(children) if isinstance(children, list) else children
    return f"<{tag} {a}>{inner}</{tag}>"


def rect(x, y, w, h, **kw):
    return el("rect", x=x, y=y, width=w, height=h, **kw)


def circle(cx, cy, r, **kw):
    return el("circle", cx=cx, cy=cy, r=r, **kw)


def ellipse(cx, cy, rx, ry, **kw):
    return el("ellipse", cx=cx, cy=cy, rx=rx, ry=ry, **kw)


def path(d, **kw):
    return el("path", d=d, **kw)


def poly(points, **kw):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return el("polygon", points=pts, **kw)


def group(children, **kw):
    return el("g", children, **kw)


def linear(id_, stops, x2=0, y2=1):
    """Vertical gradient by default. stops: [(offset, color) or (offset, color, opacity)]."""
    s = [el("stop", offset=o, stop_color=c, stop_opacity=(rest[0] if rest else None))
         for o, c, *rest in stops]
    return el("linearGradient", s, id=id_, x1=0, y1=0, x2=x2, y2=y2)


def radial(id_, stops, cx=0.5, cy=0.5, r=0.5):
    s = [el("stop", offset=o, stop_color=c, stop_opacity=(rest[0] if rest else None))
         for o, c, *rest in stops]
    return el("radialGradient", s, id=id_, cx=cx, cy=cy, r=r)


def blur(id_, amount):
    return el("filter", el("feGaussianBlur", stdDeviation=amount), id=id_,
              x="-50%", y="-50%", width="200%", height="200%")


def cloud_puffs(r, cx, cy, w, h, n, rmin, rmax, **kw):
    """A billowing cloud made of overlapping circles inside an ellipse."""
    out = []
    for _ in range(n):
        a = r.uniform(0, 2 * math.pi)
        d = math.sqrt(r.random())
        out.append(circle(round(cx + math.cos(a) * d * w / 2, 1),
                          round(cy + math.sin(a) * d * h / 2, 1),
                          round(r.uniform(rmin, rmax), 1), **kw))
    return out


def document(defs, body, title, desc):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="t d">'
        f'<title id="t">{title}</title><desc id="d">{desc}</desc>'
        f'<defs>{"".join(defs)}</defs>{"".join(body)}</svg>\n'
    )


def study_tag():
    """Small corner tag so art studies can never be mistaken for real news."""
    return group([
        rect(24, 24, 150, 40, rx=4, fill="#ffffff", fill_opacity=0.85),
        el("text", "ART STUDY", x=99, y=51, text_anchor="middle", fill="#9a3b1f",
           font_family="Helvetica, Arial, sans-serif", font_size=20, font_weight=700, letter_spacing=2),
    ])


def save(svg, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(svg, encoding="utf-8")
    print(f"wrote {out_path} ({len(svg.encode()) // 1024} KB)")


def grain_filter(id_="grain", strength=0.55):
    """Fine paper/print grain. Apply with grain_overlay() as the last element."""
    return el("filter", [
        el("feTurbulence", type="fractalNoise", baseFrequency=0.85, numOctaves=2, seed=7, stitchTiles="stitch"),
        el("feColorMatrix", type="saturate", values=0),
        el("feComponentTransfer", el("feFuncA", type="linear", slope=strength)),
    ], id=id_, x=0, y=0, width="100%", height="100%")


def grain_overlay(id_="grain", opacity=0.35):
    return rect(0, 0, WIDTH, HEIGHT, filter=f"url(#{id_})", opacity=opacity, style="mix-blend-mode:multiply")


def halftone(id_, color, dot=2.2, spacing=8, angle=45):
    """A comic-style halftone dot pattern; use as fill="url(#id)" over a flat shape."""
    return el("pattern", circle(spacing / 2, spacing / 2, dot, fill=color), id=id_, width=spacing, height=spacing,
              patternUnits="userSpaceOnUse", patternTransform=f"rotate({angle})")
