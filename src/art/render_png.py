"""Render an SVG to PNG previews so the artwork can be looked at before publishing.

Writes two previews to cache/previews/: full size (1200 px wide) and phone
size (360 px wide, the style guide's "readable on a phone" test). It tries
whichever renderer this machine has: cairosvg (pip), rsvg-convert (Linux),
headless Chrome, or macOS Quick Look.

    python3 src/art/render_png.py public/artwork/2026-10-25.svg
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "cache" / "previews"
CHROME = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "google-chrome", "chromium", "chromium-browser"]


def _cairosvg(svg, png, width):
    import cairosvg  # optional dependency
    cairosvg.svg2png(url=str(svg), write_to=str(png), output_width=width)


def _rsvg(svg, png, width):
    subprocess.run(["rsvg-convert", "-w", str(width), "-o", str(png), str(svg)], check=True, timeout=60)


def _chrome(svg, png, width):
    exe = next((c for c in CHROME if Path(c).exists() or shutil.which(c)), None)
    if not exe:
        raise FileNotFoundError("no Chrome")
    height = round(width * 0.75)
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "p.html"  # wrap so the SVG scales to the requested width
        page.write_text(f'<html><body style="margin:0"><img src="{svg.resolve().as_uri()}" '
                        f'style="width:{width}px;height:{height}px;display:block"></body></html>')
        subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                        f"--window-size={width},{height}", f"--screenshot={png}", page.as_uri()],
                       check=True, timeout=90, capture_output=True)


def _quicklook(svg, png, width):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["qlmanage", "-t", "-s", str(width), "-o", tmp, str(svg)], check=True, timeout=60, capture_output=True)
        shutil.move(str(Path(tmp) / (svg.name + ".png")), png)


def render(svg_path, widths=(1200, 360)):
    svg = Path(svg_path)
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = []
    for width in widths:
        png = OUT / f"{svg.stem}-{width}.png"
        for name, fn in (("cairosvg", _cairosvg), ("rsvg-convert", _rsvg), ("chrome", _chrome), ("quicklook", _quicklook)):
            try:
                fn(svg, png, width)
                if png.exists() and png.stat().st_size > 1000:
                    outputs.append((png, name))
                    break
            except Exception:
                continue
        else:
            raise RuntimeError("no SVG renderer available (install cairosvg or rsvg-convert)")
    return outputs


if __name__ == "__main__":
    for png, how in render(sys.argv[1]):
        print(f"wrote {png.relative_to(ROOT)} (via {how})")
