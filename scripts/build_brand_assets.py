#!/usr/bin/env python3
"""Generate the LRDL-HHZ project logo assets."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
STATIC_DIR = ROOT / "static"

INK = "#071426"
NAVY = "#0B213A"
BLUE = "#2764FF"
TEAL = "#0FBAA7"
PINK = "#E63F66"
GOLD = "#F4A21A"
CYAN = "#2ABDF5"
PAPER = "#F7FBFF"
MUTED = "#607086"


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def hex_rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def mix(a: str, b: str, t: float) -> tuple[int, int, int, int]:
    ar, ag, ab, aa = hex_rgba(a)
    br, bg, bb, ba = hex_rgba(b)
    return (
        int(ar + (br - ar) * t),
        int(ag + (bg - ag) * t),
        int(ab + (bb - ab) * t),
        int(aa + (ba - aa) * t),
    )


def centered_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt, fill) -> None:
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1] - (box[3] - box[1]) / 2), text, font=fnt, fill=fill)


def rounded_gradient_box(size: int, radius: int) -> Image.Image:
    grad = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = grad.load()
    for y in range(size):
        y_t = y / max(1, size - 1)
        for x in range(size):
            x_t = x / max(1, size - 1)
            glow = max(0.0, 1.0 - math.hypot(x_t - 0.72, y_t - 0.2) * 1.8)
            base = mix(NAVY, "#122F4F", min(1, 0.65 * y_t + 0.35 * x_t))
            bright = mix(BLUE, TEAL, x_t)
            px[x, y] = tuple(int(base[i] * (1 - glow * 0.32) + bright[i] * glow * 0.32) for i in range(3)) + (255,)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)
    return out


def draw_mark(size: int = 1024) -> Image.Image:
    pad = int(size * 0.07)
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((pad, pad + int(size * 0.025), size - pad, size - pad + int(size * 0.025)), radius=int(size * 0.17), fill=(7, 20, 38, 58))
    shadow = shadow.filter(ImageFilter.GaussianBlur(int(size * 0.028)))
    im.alpha_composite(shadow)

    box = rounded_gradient_box(size - pad * 2, int(size * 0.16))
    im.alpha_composite(box, (pad, pad))
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle((pad, pad, size - pad, size - pad), radius=int(size * 0.16), outline=hex_rgba("#DDF7FF", 210), width=int(size * 0.014))
    d.rounded_rectangle((pad + int(size * 0.035), pad + int(size * 0.035), size - pad - int(size * 0.035), size - pad - int(size * 0.035)), radius=int(size * 0.11), outline=hex_rgba(CYAN, 74), width=max(2, int(size * 0.006)))

    nodes = {
        "C": (0.29, 0.30, TEAL),
        "L": (0.28, 0.72, PINK),
        "R": (0.73, 0.42, GOLD),
        "D": (0.72, 0.74, BLUE),
    }
    hub = (0.505, 0.535)
    for label in nodes:
        x, y, _ = nodes[label]
        d.line((hub[0] * size, hub[1] * size, x * size, y * size), fill=(221, 247, 255, 118), width=int(size * 0.015))
    for a, b in [("L", "C"), ("C", "R"), ("L", "D"), ("R", "D")]:
        ax, ay, _ = nodes[a]
        bx, by, _ = nodes[b]
        d.line((ax * size, ay * size, bx * size, by * size), fill=(221, 247, 255, 85), width=int(size * 0.010))

    curve = []
    for i in range(72):
        x = (0.19 + i / 71 * 0.64) * size
        y = (0.78 - 0.09 * math.sin(i / 71 * math.pi) - 0.17 * (i / 71)) * size
        curve.append((x, y))
    d.line(curve, fill=hex_rgba(GOLD, 235), width=int(size * 0.026), joint="curve")
    d.polygon(
        [
            (0.84 * size, 0.60 * size),
            (0.775 * size, 0.585 * size),
            (0.815 * size, 0.665 * size),
        ],
        fill=hex_rgba(GOLD, 235),
    )

    for label, (x, y, color) in nodes.items():
        r = int(size * (0.054 if label != "R" else 0.064))
        d.ellipse((x * size - r * 1.45, y * size - r * 1.45, x * size + r * 1.45, y * size + r * 1.45), fill=hex_rgba(color, 44))
        d.ellipse((x * size - r, y * size - r, x * size + r, y * size + r), fill=hex_rgba(color, 245), outline=hex_rgba("#FFFFFF", 230), width=max(2, int(size * 0.008)))
        centered_text(d, (int(x * size), int(y * size) - int(size * 0.003)), label, font(int(size * 0.058), True), "#FFFFFF")

    d.ellipse((0.385 * size, 0.390 * size, 0.625 * size, 0.630 * size), fill=(7, 20, 38, 150), outline=hex_rgba(CYAN, 170), width=int(size * 0.008))
    h_font = font(int(size * 0.225), True)
    centered_text(d, (int(size * 0.505), int(size * 0.522)), "H", h_font, (255, 255, 255, 242))
    centered_text(d, (int(size * 0.505), int(size * 0.845)), "LRDL-HHZ", font(int(size * 0.048), True), hex_rgba("#DDF7FF", 230))
    return im


def draw_lockup() -> Image.Image:
    w, h = 1800, 520
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle((28, 42, w - 28, h - 42), radius=48, fill=(255, 255, 255, 246), outline=hex_rgba("#BFD6EA", 190), width=4)
    mark = draw_mark(360)
    im.alpha_composite(mark, (54, 78))
    d.line((470, 120, 470, 400), fill=hex_rgba("#D5E4F2", 210), width=3)
    d.text((530, 116), "Loneliness Risk Decision Lab", font=font(78, True), fill=hex_rgba(INK))
    d.text((535, 220), "LRDL-HHZ Connection Lens", font=font(38, True), fill=hex_rgba(TEAL))
    d.text((535, 282), "Social connection, reward timing, conflict response, and risk decisions", font=font(34), fill=hex_rgba(MUTED))
    d.text((535, 354), "Developed by He Haoze", font=font(34, True), fill=hex_rgba(BLUE))
    d.line((1035, 370, 1515, 370), fill=hex_rgba(GOLD, 230), width=8)
    for x, color in [(1035, PINK), (1195, TEAL), (1355, BLUE), (1515, GOLD)]:
        d.ellipse((x - 18, 352, x + 18, 388), fill=hex_rgba(color, 245), outline=hex_rgba("#FFFFFF", 240), width=4)
    return im


def draw_stamp() -> Image.Image:
    w, h = 1300, 300
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle((18, 18, w - 18, h - 18), radius=38, fill=(255, 255, 255, 225), outline=hex_rgba(INK, 230), width=4)
    mark = draw_mark(190)
    im.alpha_composite(mark, (56, 55))
    d.text((285, 68), "LRDL-HHZ", font=font(66, True), fill=hex_rgba(INK))
    d.text((286, 148), "Intellectual property mark / Developed by He Haoze", font=font(32, True), fill=hex_rgba(TEAL))
    d.text((286, 201), "Loneliness Risk Decision Lab", font=font(28), fill=hex_rgba(MUTED))
    return im


MARK_SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" role="img" aria-labelledby="title desc">
  <title id="title">LRDL-HHZ Connection Lens logo</title>
  <desc id="desc">Logo for the Loneliness Risk Decision Lab by He Haoze, combining social connection nodes, risk curve, and H monogram.</desc>
  <defs>
    <linearGradient id="bg" x1="16" y1="112" x2="112" y2="16" gradientUnits="userSpaceOnUse">
      <stop stop-color="{NAVY}"/>
      <stop offset="0.52" stop-color="#123A62"/>
      <stop offset="1" stop-color="{BLUE}"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#071426" flood-opacity="0.28"/>
    </filter>
  </defs>
  <rect x="10" y="10" width="108" height="108" rx="22" fill="url(#bg)" filter="url(#softShadow)"/>
  <rect x="15" y="15" width="98" height="98" rx="17" fill="none" stroke="#DDF7FF" stroke-opacity="0.68" stroke-width="2"/>
  <path d="M35 83 L40 39 L76 67 L94 34 M35 83 L76 67 L69 91" fill="none" stroke="#DDF7FF" stroke-opacity="0.72" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M26 88 C43 66 72 77 101 56" fill="none" stroke="{GOLD}" stroke-width="4.5" stroke-linecap="round"/>
  <path d="M102 56 L95 55 L99 62 Z" fill="{GOLD}"/>
  <circle cx="35" cy="83" r="9" fill="{PINK}" stroke="#fff" stroke-width="2"/>
  <circle cx="40" cy="39" r="8" fill="{TEAL}" stroke="#fff" stroke-width="2"/>
  <circle cx="76" cy="67" r="10" fill="{GOLD}" stroke="#fff" stroke-width="2"/>
  <circle cx="94" cy="34" r="8" fill="{BLUE}" stroke="#fff" stroke-width="2"/>
  <circle cx="69" cy="91" r="8" fill="{CYAN}" stroke="#fff" stroke-width="2"/>
  <text x="64" y="73" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="800" fill="#fff">H</text>
  <text x="64" y="103" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="9" font-weight="800" fill="#DDF7FF">HHZ</text>
</svg>
'''


LOCKUP_SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 208" role="img" aria-labelledby="title desc">
  <title id="title">Loneliness Risk Decision Lab LRDL-HHZ logo lockup</title>
  <desc id="desc">Project lockup for Loneliness Risk Decision Lab, developed by He Haoze.</desc>
  <rect x="8" y="8" width="704" height="192" rx="24" fill="#FFFFFF" fill-opacity="0.92" stroke="#BFD6EA"/>
  <svg x="24" y="34" width="140" height="140" viewBox="0 0 128 128">{MARK_SVG.split('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" role="img" aria-labelledby="title desc">', 1)[1].rsplit('</svg>', 1)[0]}</svg>
  <line x1="190" y1="45" x2="190" y2="163" stroke="#D5E4F2"/>
  <text x="218" y="73" font-family="Arial, Helvetica, sans-serif" font-size="31" font-weight="800" fill="{INK}">Loneliness Risk Decision Lab</text>
  <text x="220" y="108" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="800" fill="{TEAL}">LRDL-HHZ Connection Lens</text>
  <text x="220" y="138" font-family="Arial, Helvetica, sans-serif" font-size="14" fill="{MUTED}">Social connection + risk decision research OS</text>
  <text x="220" y="166" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="800" fill="{BLUE}">Developed by He Haoze</text>
</svg>
'''


def main() -> None:
    ASSET_DIR.mkdir(exist_ok=True)
    STATIC_DIR.mkdir(exist_ok=True)
    mark = draw_mark()
    lockup = draw_lockup()
    stamp = draw_stamp()
    mark.save(ASSET_DIR / "lrdl_logo_mark.png")
    mark.resize((512, 512), Image.Resampling.LANCZOS).save(ASSET_DIR / "lrdl_logo_mark_512.png")
    lockup.save(ASSET_DIR / "lrdl_logo_lockup.png")
    stamp.save(ASSET_DIR / "lrdl_logo_stamp.png")
    (ASSET_DIR / "lrdl_logo_mark.svg").write_text(MARK_SVG, encoding="utf-8")
    (ASSET_DIR / "lrdl_logo_lockup.svg").write_text(LOCKUP_SVG, encoding="utf-8")
    (STATIC_DIR / "favicon.svg").write_text(MARK_SVG, encoding="utf-8")
    print(
        {
            "mark": str(ASSET_DIR / "lrdl_logo_mark.png"),
            "lockup": str(ASSET_DIR / "lrdl_logo_lockup.png"),
            "stamp": str(ASSET_DIR / "lrdl_logo_stamp.png"),
        }
    )


if __name__ == "__main__":
    main()
