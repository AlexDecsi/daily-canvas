"""Technical checks for a finished artwork SVG (style guide checklist item 6).

The visual and factual checks (focal point, people doing the reported action,
nothing invented) need eyes: Claude reviews the PNG preview from render_png.py.
This script checks what code can check:

- valid XML with an <svg> root, 1200×900 with viewBox "0 0 1200 900"
- <title> and <desc> present and non-empty
- nothing active or external: no <script>, <foreignObject>, <image>, on* event
  attributes, or links/urls that point outside the file
- file size within the limit

    python3 src/art/check_art.py public/artwork/2026-10-25.svg
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG = "{http://www.w3.org/2000/svg}"
FORBIDDEN_TAGS = {"script", "foreignObject", "image", "iframe", "embed", "object", "audio", "video"}
HREF_ATTRS = {"href", "{http://www.w3.org/1999/xlink}href"}


def check(path, max_kb=250):
    path = Path(path)
    if not path.is_file():
        return [f"file not found: {path}"]
    errors = []
    size_kb = path.stat().st_size / 1024
    if size_kb > max_kb:
        errors.append(f"file is {size_kb:.0f} KB (max {max_kb})")
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as err:
        return errors + [f"not valid XML: {err}"]
    if root.tag != f"{SVG}svg":
        errors.append("root element is not <svg> in the SVG namespace")
    if root.get("viewBox", "").split() != ["0", "0", "1200", "900"]:
        errors.append('viewBox must be "0 0 1200 900"')
    if root.get("width") != "1200" or root.get("height") != "900":
        errors.append("width/height must be 1200/900")
    for tag in ("title", "desc"):
        node = root.find(f"{SVG}{tag}")
        if node is None or not (node.text or "").strip():
            errors.append(f"missing <{tag}>")
    for node in root.iter():
        local = node.tag.split("}")[-1]
        if local in FORBIDDEN_TAGS:
            errors.append(f"forbidden element <{local}>")
        for attr, value in node.attrib.items():
            name = attr.split("}")[-1]
            if name.lower().startswith("on"):
                errors.append(f"event attribute {name} on <{local}>")
            if attr in HREF_ATTRS and not value.startswith("#"):
                errors.append(f"external link {value[:60]} on <{local}>")
            if re.search(r"url\(\s*['\"]?(?!#)", value):
                errors.append(f"external url() in {name} on <{local}>")
    return sorted(set(errors))


if __name__ == "__main__":
    problems = check(sys.argv[1])
    for p in problems:
        print(f"  ✗ {p}")
    print("OK: artwork passes technical checks" if not problems else "BLOCKED")
    sys.exit(1 if problems else 0)
