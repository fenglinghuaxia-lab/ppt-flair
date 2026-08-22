# -*- coding: utf-8 -*-
"""ppt-flair delivery tool: embed candidate PNGs into a single dark HTML gallery
(base64 inline). Standard delivery format for multi-candidate previews.

Usage:
  python -X utf8 build_gallery.py output.html img1.png "Label 1" img2.png "Label 2" ...
  optional: --title "Gallery title" [--width 1400]
"""
import argparse
import base64
import io
import os
from PIL import Image


def to_b64(path, width):
    img = Image.open(path).convert("RGB")
    h = int(img.height * width / img.width)
    img = img.resize((width, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output")
    ap.add_argument("items", nargs="+", help="alternating: png_path label png_path label ...")
    ap.add_argument("--title", default="候选方案对比")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--width", type=int, default=1400)
    a = ap.parse_args()

    if len(a.items) % 2 != 0:
        raise SystemExit("items must be pairs: <png> <label> <png> <label> ...")

    pairs = [(a.items[i], a.items[i + 1]) for i in range(0, len(a.items), 2)]
    blocks = []
    for p, label in pairs:
        b64 = to_b64(p, a.width)
        blocks.append(
            '<div class="card"><div class="label">%s</div>'
            '<img src="data:image/jpeg;base64,%s" alt="%s"></div>' % (label, b64, label)
        )
    head = (
        '<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
        "body{background:#0d1524;color:#e8ecf4;font-family:'Microsoft YaHei',sans-serif;margin:0;padding:32px;}"
        "h1{font-size:20px;font-weight:600;letter-spacing:4px;}"
        "p{color:#8fa0b8;font-size:13px;}"
        ".card{margin-bottom:36px;}"
        ".label{font-size:14px;color:#c9a86a;margin-bottom:10px;letter-spacing:2px;}"
        "img{width:100%;border-radius:6px;display:block;box-shadow:0 8px 40px rgba(0,0,0,.5);}"
        "</style></head><body>"
        "<h1>" + a.title + "</h1><p>" + a.subtitle + "</p>"
    )
    html = head + "".join(blocks) + "</body></html>"
    with open(a.output, "w", encoding="utf-8") as f:
        f.write(html)
    print("GALLERY", a.output, round(os.path.getsize(a.output) / 1024), "KB,", len(pairs), "images")


if __name__ == "__main__":
    main()
