# -*- coding: utf-8 -*-
"""ppt-flair Stage A tool: AI calligraphy (black bg + white ink) -> transparent PNG.
Usage: python -X utf8 keyout_title.py <input.png> <output.png> [--threshold 32] [--gamma 1.0]
Brightness-based keying: white strokes keep alpha, black background removed."""
import argparse
from PIL import Image


def keyout(src, dst, threshold=32, gamma=1.0):
    img = Image.open(src).convert("L")
    # alpha = scaled brightness; strokes (bright) opaque, bg (dark) transparent
    lut = []
    for i in range(256):
        v = i / 255.0
        if gamma != 1.0:
            v = v ** gamma
        a = int(v * 255)
        lut.append(0 if i < threshold else a)
    alpha = img.point(lut)
    out = Image.open(src).convert("RGB").convert("RGBA")
    out.putalpha(alpha)
    out.save(dst)
    # stats
    bbox = alpha.point(lambda p: 255 if p > 128 else 0).getbbox()
    print("OK", dst, "size", out.size, "content bbox", bbox)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--threshold", type=int, default=32, help="brightness below this = background")
    ap.add_argument("--gamma", type=float, default=1.0, help="<1 softens faint strokes, >1 hardens")
    a = ap.parse_args()
    keyout(a.input, a.output, a.threshold, a.gamma)
