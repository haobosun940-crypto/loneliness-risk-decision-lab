#!/usr/bin/env python3
"""Build an animated narrated MP4 introduction with local voice synthesis."""

from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets"
OUTPUT_DIR = ROOT / "outputs"
TMP_DIR = ROOT / "tmp" / "video"
FFMPEG = "/Users/sunlele/.local/bin/ffmpeg"
FFPROBE = "/Users/sunlele/.local/bin/ffprobe"
W, H = 1920, 1080
FPS = 10

C = {
    "ink": "#071426",
    "navy": "#0B213A",
    "panel": "#102C46",
    "muted": "#607086",
    "paper": "#EFF8FF",
    "white": "#FFFFFF",
    "line": "#BFD6EA",
    "cyan": "#67E8F9",
    "blue": "#2764FF",
    "teal": "#0FBAA7",
    "pink": "#FB7185",
    "gold": "#F9D56E",
    "green": "#86EFAC",
}

SCRIPT = """Meet the Loneliness and Risk Decision Lab.

The question is simple: when connection feels low, do short-term rewards become louder?

In three minutes, a participant answers social-signal questions, completes choice scenarios, and receives a personal risk-decision profile.

Behind the screen, the system scores loneliness, connection, stress, delay preference, spending impulse, risky choice, and conflict response.

Then the statistics layer runs reliability checks, ANOVA, and OLS models, while keeping synthetic pilot rows separate from live submissions.

The first pattern is clear: higher loneliness maps onto a higher Risk Decision Index, while social connection buffers the effect.

This is a public research product: survey, database, dashboard, paper, workbook, slides, and video, ready to grow with real student data.
"""


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def font(size: int, bold: bool = False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def available_voices() -> str:
    try:
        result = subprocess.run(["say", "-v", "?"], check=True, capture_output=True, text=True)
        return result.stdout
    except Exception:
        return ""


def choose_voice() -> str:
    voices = available_voices()
    for candidate in ["Flo (英语（美国）)", "Sandy (英语（美国）)", "Shelley (英语（美国）)", "Samantha"]:
        if candidate in voices:
            return candidate
    return "Samantha"


def audio_duration(path: Path) -> float:
    result = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def blend(a: str, b: str, t: float) -> tuple[int, int, int]:
    ar, ag, ab = hex_to_rgb(a)
    br, bg, bb = hex_to_rgb(b)
    return (int(lerp(ar, br, t)), int(lerp(ag, bg, t)), int(lerp(ab, bb, t)))


def rounded(draw: ImageDraw.ImageDraw, box, radius=22, fill=None, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line: list[str] = []
    for word in words:
        trial = " ".join(line + [word])
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width or not line:
            line.append(word)
        else:
            lines.append(" ".join(line))
            line = [word]
    if line:
        lines.append(" ".join(line))
    return lines


def draw_text(draw, xy, text: str, fnt, fill, max_width: int | None = None, line_gap: int = 8):
    x, y = xy
    if not max_width:
        draw.text((x, y), text, font=fnt, fill=fill)
        return
    for line in wrap_text(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap


def gradient_bg(t: float) -> Image.Image:
    sw, sh = 240, 135
    img = Image.new("RGB", (sw, sh), C["paper"])
    px = img.load()
    for y in range(sh):
        row_t = y / sh
        base = blend("#F7FBFF", "#DDF4FF", row_t)
        for x in range(sw):
            col_t = (x / sw + 0.16 * math.sin(t * 0.7 + y / 20)) / 1.16
            glow = max(0, 1 - abs((x - sw * (0.72 + 0.08 * math.sin(t))) / 76))
            c1 = blend("#F7FBFF", "#DBF8FF", col_t)
            c2 = blend("#FFFFFF", "#D6FAF4", glow * 0.55)
            px[x, y] = tuple(min(255, int((c1[i] * 0.72 + c2[i] * 0.28))) for i in range(3))
    img = img.resize((W, H), Image.Resampling.BICUBIC)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for i in range(-3, 8):
        x = int((i * 310 + t * 80) % (W + 500) - 250)
        d.line((x, -80, x + 450, H + 80), fill=(39, 100, 255, 24), width=3)
    for x in range(0, W, 70):
        d.line((x, 0, x, H), fill=(39, 100, 255, 12), width=1)
    for y in range(0, H, 70):
        d.line((0, y, W, y), fill=(15, 186, 167, 10), width=1)
    for i in range(34):
        x = int((i * 137 + t * 48) % W)
        y = int((i * 83 + 80 * math.sin(t * 0.9 + i)) % H)
        color = [(39, 100, 255, 70), (15, 186, 167, 64), (251, 113, 133, 58), (249, 213, 110, 62)][i % 4]
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=color)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def panel(draw, box, title=None, dark=False):
    fill = "#0C233A" if dark else "#FFFFFF"
    outline = "#66D9EF" if dark else "#C4D9F0"
    rounded(draw, box, 18, fill=fill, outline=outline, width=2)
    if title:
        draw_text(draw, (box[0] + 28, box[1] + 24), title, font(26, True), C["cyan"] if dark else C["blue"])


def draw_header(draw, title: str, subtitle: str):
    draw_text(draw, (92, 74), "LONELINESS & RISK DECISION LAB", font(24, True), C["pink"])
    draw_text(draw, (92, 124), title, font(66, True), C["ink"], max_width=920, line_gap=8)
    draw_text(draw, (96, 292), subtitle, font(31), "#42566E", max_width=760, line_gap=10)


def scene_question(_img, draw, t, p):
    draw_header(draw, "Does loneliness change risk decisions?", "A three-minute behavioral test links loneliness, social connection, and reward preference to a decision-risk profile.")
    x = int(1040 + (1 - ease(p)) * 220)
    panel(draw, (x, 190, x + 700, 820), dark=True)
    labels = [("Loneliness", C["pink"], 0.78), ("Connection", C["cyan"], 0.38), ("Risk Index", C["gold"], 0.64)]
    for i, (label, color, value) in enumerate(labels):
        y = 300 + i * 150
        draw_text(draw, (x + 58, y), label, font(28, True), "#DDF5FF")
        rounded(draw, (x + 58, y + 56, x + 590, y + 88), 14, fill="#173A56")
        rounded(draw, (x + 58, y + 56, x + 58 + int(532 * value * ease(p)), y + 88), 14, fill=color)
    draw_text(draw, (x + 58, 720), "Personal profile: Reward-sensitive accelerator", font(30, True), C["white"], max_width=560)


def scene_pipeline(_img, draw, t, p):
    draw_header(draw, "From survey to research evidence", "The site is not just a page. It is a data collection, scoring, modeling, and reporting workflow.")
    steps = [
        ("Survey", "self-report + choices", C["blue"]),
        ("Scoring", "0-100 indicators", C["teal"]),
        ("Database", "synthetic vs live", C["gold"]),
        ("Models", "OLS + ANOVA", C["pink"]),
    ]
    for i, (title, body, color) in enumerate(steps):
        local = ease(min(1, max(0, p * 1.35 - i * 0.12)))
        x = int(150 + i * 425)
        y = int(560 - 60 * local)
        panel(draw, (x, y, x + 320, y + 260))
        draw.ellipse((x + 28, y + 26, x + 88, y + 86), fill=color)
        draw_text(draw, (x + 30, y + 122), title, font(34, True), C["ink"])
        draw_text(draw, (x + 30, y + 174), body, font(24), C["muted"], max_width=250)
        if i < len(steps) - 1:
            draw.line((x + 326, y + 130, x + 405, y + 130), fill=color, width=5)
            draw.polygon([(x + 405, y + 130), (x + 382, y + 116), (x + 382, y + 144)], fill=color)


def scene_network(_img, draw, t, p):
    draw_header(draw, "Psychology becomes measurable signals", "Loneliness, connection, stress, risk, and impulsivity move through the same animated model surface.")
    panel(draw, (930, 160, 1780, 890), "Quant cockpit", dark=True)
    nodes = {
        "L": (1120, 610, C["pink"]),
        "S": (1220, 360, "#93C5FD"),
        "R": (1400, 560, C["gold"]),
        "C": (1580, 360, C["cyan"]),
        "I": (1640, 650, C["green"]),
    }
    links = [("L", "S"), ("S", "R"), ("L", "R"), ("R", "C"), ("R", "I"), ("C", "I")]
    for a, b in links:
        ax, ay, _ = nodes[a]
        bx, by, _ = nodes[b]
        draw.line((ax, ay, bx, by), fill=(103, 232, 249), width=3)
        dot = ease((math.sin(t * 2.4 + ax) + 1) / 2)
        dx, dy = int(lerp(ax, bx, dot)), int(lerp(ay, by, dot))
        draw.ellipse((dx - 8, dy - 8, dx + 8, dy + 8), fill=C["pink"] if a == "L" else C["cyan"])
    for label, (x, y, color) in nodes.items():
        r = int(34 + 8 * math.sin(t * 2 + x))
        draw.ellipse((x - r - 18, y - r - 18, x + r + 18, y + r + 18), fill=color + "33")
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=C["white"], width=3)
        draw_text(draw, (x - 10, y - 16), label, font(32, True), C["white"])
    legend = [
        ("L", "Loneliness", 990, 800, C["pink"]),
        ("C", "Connection", 1215, 800, C["cyan"]),
        ("R", "Risk", 1460, 800, C["gold"]),
        ("I", "Impulsivity", 990, 845, C["green"]),
        ("S", "Stress", 1215, 845, "#93C5FD"),
    ]
    for k, v, x, y, color in legend:
        rounded(draw, (x - 12, y - 8, x + 185, y + 32), 14, fill="#173A56", outline=color, width=1)
        draw_text(draw, (x, y), f"{k} = {v}", font(19, True), "#DDF5FF")


def scene_charts(_img, draw, t, p):
    draw_header(draw, "The pilot pattern is visible", "Synthetic rows are labeled as demonstration data, while live submissions stay separate for future analysis.")
    panel(draw, (930, 170, 1780, 870))
    values = [29.4, 50.9, 66.4]
    labels = ["Low", "Moderate", "High"]
    colors = [C["teal"], C["gold"], C["pink"]]
    for i, value in enumerate(values):
        x = 1040 + i * 210
        h = int(value * 6.6 * ease(min(1, p * 1.2)))
        draw.rectangle((x, 760 - h, x + 120, 760), fill=colors[i])
        draw_text(draw, (x + 20, 786), labels[i], font(22, True), C["ink"])
        draw_text(draw, (x + 18, 720 - h), f"{value:.1f}", font(28, True), colors[i])
    draw_text(draw, (990, 240), "Risk Decision Index by loneliness group", font(34, True), C["ink"], max_width=700)
    draw_text(draw, (990, 330), "OLS: loneliness positive; social connection negative.", font(27), C["muted"], max_width=390, line_gap=6)


def scene_website(img, draw, t, p):
    draw_header(draw, "A public website closes the loop", "Participants can scan, complete the test, see a profile, and export live data for analysis.")
    panel(draw, (960, 170, 1740, 870), dark=True)
    qr = Image.open(ASSET_DIR / "questionnaire_qr.png").convert("RGB").resize((260, 260), Image.Resampling.NEAREST)
    draw.rounded_rectangle((1010, 250, 1320, 560), radius=18, fill=C["white"])
    img.paste(qr, (1035, 275))
    panel(draw, (1370, 250, 1680, 560))
    draw_text(draw, (1410, 292), "Your profile", font(32, True), C["ink"])
    for i, (label, color, value) in enumerate([("Loneliness", C["pink"], 0.62), ("Connection", C["cyan"], 0.47), ("Risk", C["gold"], 0.68)]):
        y = 360 + i * 54
        draw_text(draw, (1410, y), label, font(18, True), C["muted"])
        rounded(draw, (1535, y + 4, 1660, y + 22), 9, fill="#E8F2FC")
        rounded(draw, (1535, y + 4, 1535 + int(125 * value * ease(p)), y + 22), 9, fill=color)
    draw_text(draw, (1010, 650), "Live submissions are stored separately from synthetic pilot rows.", font(30, True), "#DDF5FF", max_width=620)


def scene_final(_img, draw, t, p):
    draw_header(draw, "A research-ready behavioral assessment platform", "Survey, scoring, database, models, dashboard, report, workbook, slides, and video in one workflow.")
    items = ["Start Decision Test", "View Dashboard", "Export CSV", "Download Research Package"]
    for i, item in enumerate(items):
        x = 1040
        y = 250 + i * 128
        local = ease(min(1, max(0, p * 1.4 - i * 0.16)))
        panel(draw, (int(x + (1 - local) * 220), y, 1740, y + 92))
        draw_text(draw, (int(x + (1 - local) * 220) + 36, y + 26), item, font(30, True), C["ink"])
    draw_text(draw, (96, 870), "Not a diagnosis. A transparent research prototype for learning, collecting, and explaining behavioral data.", font(30, True), C["blue"], max_width=820)


SCENES = [
    (0, 7.5, scene_question),
    (7.5, 15.0, scene_pipeline),
    (15.0, 23.5, scene_network),
    (23.5, 32.0, scene_charts),
    (32.0, 41.0, scene_website),
    (41.0, 52.0, scene_final),
]


def render_frame(t: float, duration: float) -> Image.Image:
    img = gradient_bg(t)
    draw = ImageDraw.Draw(img, "RGBA")
    for start, end, fn in SCENES:
        if start <= t < end or (t >= end and end == SCENES[-1][1]):
            p = (t - start) / (end - start)
            fn(img, draw, t, p)
            break
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    vdraw.rectangle((0, 0, W, H), outline=(39, 100, 255, 42), width=8)
    if t < 0.7:
        alpha = int((1 - t / 0.7) * 255)
        vdraw.rectangle((0, 0, W, H), fill=(255, 255, 255, alpha))
    if duration - t < 0.8:
        alpha = int((1 - (duration - t) / 0.8) * 255)
        vdraw.rectangle((0, 0, W, H), fill=(7, 20, 38, alpha))
    return Image.alpha_composite(img.convert("RGBA"), vignette).convert("RGB")


def render_sequence(duration: float) -> Path:
    sequence_dir = TMP_DIR / "sequence"
    if sequence_dir.exists():
        shutil.rmtree(sequence_dir)
    sequence_dir.mkdir(parents=True)
    total_frames = int(math.ceil(duration * FPS))
    for frame in range(total_frames):
        t = frame / FPS
        render_frame(t, duration).save(sequence_dir / f"seq_{frame + 1:05d}.jpg", quality=88)
    return sequence_dir


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    script_path = OUTPUT_DIR / "loneliness_risk_video_script.txt"
    audio_path = TMP_DIR / "narration.aiff"
    mp4_path = OUTPUT_DIR / "loneliness_risk_intro_video.mp4"
    script_path.write_text(SCRIPT, encoding="utf-8")
    voice = choose_voice()

    run(["say", "-v", voice, "-r", "152", "-f", str(script_path), "-o", str(audio_path)])
    duration = max(52.0, audio_duration(audio_path) + 0.8)
    sequence_dir = render_sequence(duration)
    fade_out_start = max(0.0, duration - 0.9)
    run(
        [
            FFMPEG,
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(sequence_dir / "seq_%05d.jpg"),
            "-i",
            str(audio_path),
            "-f",
            "lavfi",
            "-t",
            f"{duration:.3f}",
            "-i",
            "sine=frequency=196:sample_rate=44100",
            "-f",
            "lavfi",
            "-t",
            f"{duration:.3f}",
            "-i",
            "sine=frequency=392:sample_rate=44100",
            "-filter_complex",
            (
                f"[1:a]highpass=f=90,lowpass=f=9000,"
                f"acompressor=threshold=-18dB:ratio=2.2:attack=18:release=220,"
                f"volume=1.18,afade=t=in:st=0:d=0.35,afade=t=out:st={fade_out_start:.2f}:d=0.9[voice];"
                "[2:a]volume=0.018[bed1];[3:a]volume=0.010[bed2];"
                "[voice][bed1][bed2]amix=inputs=3:duration=first:dropout_transition=0[aout]"
            ),
            "-map",
            "0:v",
            "-map",
            "[aout]",
            "-r",
            "30",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-preset",
            "medium",
            "-crf",
            "22",
            "-c:a",
            "aac",
            "-b:a",
            "96k",
            "-shortest",
            str(mp4_path),
        ]
    )
    print({"video": str(mp4_path), "voice": voice, "duration": round(duration, 2), "fps": FPS})


if __name__ == "__main__":
    main()
