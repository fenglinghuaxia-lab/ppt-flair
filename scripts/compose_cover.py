# -*- coding: utf-8 -*-
"""ppt-flair Stage C+D tool: color-grade a background image and composite the
transparent calligraphy title. Defaults = validated recipe (2026-08, user-approved).

Usage:
  python -X utf8 compose_cover.py --bg bg.png --title title.png --out cover.png
  optional: --width-ratio 0.60 --v-center 0.26 --overlay 0.22 --brightness 0.97
            --saturation 0.92 --contrast 1.06 --size 1920x1080
"""
import argparse
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter


def crop_16x9(img, W, H):
    sw, sh = img.size
    scale = max(W / sw, H / sh)
    nw, nh = int(sw * scale + 0.5), int(sh * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - W) // 2
    y0 = (nh - H) // 2
    return img.crop((x0, y0, x0 + W, y0 + H))


def color_grade(img, sat, contrast, overlay_alpha, brightness):
    img = ImageEnhance.Color(img).enhance(sat)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    overlay = Image.new("RGB", img.size, (16, 30, 54))  # deep blue
    img = Image.blend(img, overlay, overlay_alpha)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    return img


def bottom_shadow(img, W, H, start=0.72, max_a=80):
    mask = Image.new("L", (1, H))
    for y in range(H):
        t = y / H
        v = 0 if t < start else int(max_a * ((t - start) / (1 - start)) ** 1.4)
        mask.putpixel((0, y), v)
    mask = mask.resize((W, H))
    dark = Image.new("RGB", (W, H), (8, 14, 26))
    return Image.composite(dark, img, mask)


def vignette(img, W, H):
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-W * 0.15, -H * 0.25, W * 1.15, H * 1.25), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(180))
    dark = Image.new("RGB", (W, H), (10, 16, 30))
    return Image.composite(img, dark, mask)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bg", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width-ratio", type=float, default=0.60)
    ap.add_argument("--v-center", type=float, default=0.26, help="title vertical center as ratio of height (upper area)")
    ap.add_argument("--saturation", type=float, default=0.92)
    ap.add_argument("--contrast", type=float, default=1.06)
    ap.add_argument("--overlay", type=float, default=0.22)
    ap.add_argument("--brightness", type=float, default=0.97)
    ap.add_argument("--size", default="1920x1080")
    a = ap.parse_args()

    W, H = (int(x) for x in a.size.lower().split("x"))

    bg = Image.open(a.bg).convert("RGB")
    bg = crop_16x9(bg, W, H)
    bg = color_grade(bg, a.saturation, a.contrast, a.overlay, a.brightness)
    bg = bottom_shadow(bg, W, H)
    bg = vignette(bg, W, H)

    title = Image.open(a.title).convert("RGBA")
    target_w = int(W * a.width_ratio)
    scale = target_w / title.width
    title = title.resize((target_w, int(title.height * scale)), Image.LANCZOS)

    canvas = bg.convert("RGBA")
    tx = (W - title.width) // 2
    ty = max(int(H * a.v_center) - title.height // 2, 40)
    canvas.alpha_composite(title, (tx, ty))
    canvas.convert("RGB").save(a.out)
    print("OK", a.out, f"{W}x{H}", f"title_w={a.width_ratio} v_center={a.v_center} "
          f"overlay={a.overlay} brightness={a.brightness}")


if __name__ == "__main__":
    main()
