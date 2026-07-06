#!/usr/bin/env python3
"""Build a narrated MP4 introduction with local synthesized English voice."""

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

C = {
    "ink": "#1C2430",
    "muted": "#5B6472",
    "paper": "#F7F5F0",
    "white": "#FFFFFF",
    "line": "#D8DEE6",
    "teal": "#2D6A6A",
    "blue": "#456990",
    "red": "#B23A48",
    "gold": "#D98E04",
}


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


def wrap(draw: ImageDraw.ImageDraw, text: str, font_obj, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        width = draw.textbbox((0, 0), trial, font=font_obj)[2]
        if width <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_text(draw, xy, text, font_obj, fill, max_width=None, line_gap=8):
    x, y = xy
    if max_width is None:
        draw.text((x, y), text, fill=fill, font=font_obj)
        return
    for line in wrap(draw, text, font_obj, max_width):
        draw.text((x, y), line, fill=fill, font=font_obj)
        y += font_obj.size + line_gap


def paste_contained(canvas: Image.Image, image_path: Path, box: tuple[int, int, int, int]) -> None:
    image = Image.open(image_path).convert("RGB")
    x1, y1, x2, y2 = box
    max_w, max_h = x2 - x1, y2 - y1
    ratio = min(max_w / image.width, max_h / image.height)
    resized = image.resize((int(image.width * ratio), int(image.height * ratio)))
    x = x1 + (max_w - resized.width) // 2
    y = y1 + (max_h - resized.height) // 2
    canvas.paste(resized, (x, y))


def frame_base(title: str, kicker: str = "Loneliness & Risk Decision Lab") -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (1920, 1080), C["paper"])
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1920, 16), fill=C["ink"])
    draw_text(draw, (110, 80), kicker.upper(), font(26, True), C["red"])
    draw_text(draw, (110, 142), title, font(76, True), C["ink"], max_width=1340, line_gap=12)
    draw_text(draw, (110, 1010), "Synthetic pilot data are disclosed; live submissions are stored separately.", font(24), C["muted"])
    return img, draw


def build_frames() -> list[Path]:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    frames: list[Path] = []
    specs = [
        (
            "Does loneliness change how people choose risk?",
            "The study focuses on late adolescents and emerging adults aged 16-24 in digitally mediated school and college communities.",
            None,
        ),
        (
            "The research pipeline connects psychology to statistics.",
            "Loneliness and connection signals enter choice tasks, then regression and ANOVA convert behavior into interpretable evidence.",
            ASSET_DIR / "method_flow.png",
        ),
        (
            "The pilot model shows a clear group gradient.",
            "Risk Decision Index rises from low to moderate to high loneliness groups in the synthetic demonstration data.",
            ASSET_DIR / "chart_anova_groups.png",
        ),
        (
            "Regression separates loneliness from connectedness and stress.",
            "Loneliness is positive, social connection is negative, and stress is positive in the OLS model.",
            ASSET_DIR / "chart_regression_coefficients.png",
        ),
        (
            "The website closes the data loop.",
            "Participants complete the questionnaire, receive a profile, and create live submissions that are separated from synthetic rows.",
            ASSET_DIR / "questionnaire_qr.png",
        ),
        (
            "The next scientific step is live sampling.",
            "Use the QR code, collect supervised responses, and rerun the included Stata-ready analysis before making empirical claims.",
            None,
        ),
    ]
    for i, (title, body, asset) in enumerate(specs, 1):
        img, draw = frame_base(title)
        if asset:
            draw.rectangle((1040, 250, 1780, 840), fill=C["white"], outline=C["line"], width=3)
            paste_contained(img, asset, (1080, 290, 1740, 800))
            text_width = 780
        else:
            draw.rectangle((1030, 250, 1740, 780), fill=C["ink"])
            draw_text(draw, (1090, 320), "Risk Decision Index", font(46, True), C["white"])
            draw_text(draw, (1090, 420), "64.2", font(132, True), C["gold"])
            draw_text(draw, (1090, 590), "Reward-sensitive accelerator", font(42, True), C["white"], max_width=520)
            text_width = 760
        draw_text(draw, (112, 610), body, font(44), C["muted"], max_width=text_width, line_gap=14)
        out = TMP_DIR / f"frame_{i:02d}.png"
        img.save(out)
        frames.append(out)
    return frames


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def audio_duration(path: Path) -> float:
    result = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    script_path = OUTPUT_DIR / "loneliness_risk_video_script.txt"
    audio_path = TMP_DIR / "narration.aiff"
    mp4_path = OUTPUT_DIR / "loneliness_risk_intro_video.mp4"
    frames = build_frames()

    run(["say", "-v", "Samantha", "-r", "168", "-f", str(script_path), "-o", str(audio_path)])
    duration = max(36.0, audio_duration(audio_path))
    sequence_dir = TMP_DIR / "sequence"
    if sequence_dir.exists():
        shutil.rmtree(sequence_dir)
    sequence_dir.mkdir()
    total_seconds = math.ceil(duration)
    for second in range(total_seconds):
        frame_index = min(len(frames) - 1, int(second / total_seconds * len(frames)))
        shutil.copyfile(frames[frame_index], sequence_dir / f"seq_{second + 1:04d}.png")

    run(
        [
            FFMPEG,
            "-y",
            "-framerate",
            "1",
            "-i",
            str(sequence_dir / "seq_%04d.png"),
            "-i",
            str(audio_path),
            "-r",
            "25",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            str(mp4_path),
        ]
    )
    print({"video": str(mp4_path), "audio": str(audio_path), "duration": round(duration, 2)})


if __name__ == "__main__":
    main()
