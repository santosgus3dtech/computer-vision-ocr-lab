from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ocr_lab.metrics import evaluate
from ocr_lab.ocr import extract_text
from ocr_lab.preprocess import load_image, preprocess_for_ocr
SOURCE = ROOT / "sample_images" / "portfolio-benchmark.png"
EXPECTED = "OPEN SOURCE OCR LAB Synthetic benchmark document Invoice ID 2026 1042"
OUTPUT = ROOT / "docs" / "screenshots" / "ocr-benchmark.png"
REPORT = ROOT / "docs" / "benchmark.json"


def generate_source() -> None:
    canvas = np.full((330, 1100, 3), 255, dtype=np.uint8)
    cv2.rectangle(canvas, (18, 18), (1082, 312), (38, 54, 62), 3)
    lines = (
        ("OPEN SOURCE OCR LAB", (64, 105), 1.9, 4),
        ("Synthetic benchmark document", (64, 190), 1.25, 3),
        ("Invoice ID 2026 1042", (64, 265), 1.25, 3),
    )
    for line, position, scale, thickness in lines:
        cv2.putText(
            canvas,
            line,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            scale,
            (22, 32, 38),
            thickness,
            cv2.LINE_AA,
        )
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(SOURCE), canvas)


def fit(image: Image.Image, width: int, height: int) -> Image.Image:
    copy = image.copy()
    copy.thumbnail((width, height), Image.Resampling.LANCZOS)
    return copy


def main() -> None:
    generate_source()
    actual = extract_text(SOURCE, lang="eng")
    metrics = evaluate(EXPECTED, actual)
    original = Image.open(SOURCE).convert("RGB")
    processed_array = preprocess_for_ocr(load_image(SOURCE))
    processed = Image.fromarray(cv2.cvtColor(processed_array, cv2.COLOR_GRAY2RGB))

    canvas = Image.new("RGB", (1300, 670), "#f3f5f6")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    draw.text((44, 36), "OCR benchmark", fill="#18232a", font=font)
    draw.text((44, 60), "Real Tesseract output from the repository's synthetic sample", fill="#64727a", font=font)
    panels = [(44, "Original image", original), (464, "OpenCV preprocessing", processed)]
    for x, title, image in panels:
        draw.rectangle((x, 110, x + 380, 510), fill="#ffffff", outline="#d5dde0")
        draw.text((x + 18, 130), title, fill="#2b3a41", font=font)
        preview = fit(image, 344, 320)
        canvas.paste(preview, (x + 18 + (344 - preview.width) // 2, 170 + (300 - preview.height) // 2))

    draw.rectangle((884, 110, 1256, 510), fill="#ffffff", outline="#d5dde0")
    draw.text((904, 130), "Recognition metrics", fill="#2b3a41", font=font)
    draw.text((904, 180), "CHARACTER ERROR RATE", fill="#68767d", font=font)
    draw.text((904, 210), f"{metrics['character_error_rate'] * 100:.2f}%", fill="#176a53", font=font)
    draw.text((904, 260), "EXACT NORMALIZED MATCH", fill="#68767d", font=font)
    draw.text((904, 290), "YES" if metrics["exact_match"] else "NO", fill="#176a53" if metrics["exact_match"] else "#a34b50", font=font)
    draw.text((904, 340), "OCR OUTPUT", fill="#68767d", font=font)
    y = 368
    for line in actual.splitlines() or ["(no text)"]:
        draw.text((904, y), line[:48], fill="#26363d", font=font)
        y += 20

    draw.rectangle((44, 548, 1256, 626), fill="#e8f2ee", outline="#bed8ce")
    draw.text((64, 568), "Pipeline: grayscale -> 2x resize -> median denoise -> Otsu threshold -> Tesseract", fill="#28584a", font=font)
    draw.text((64, 592), "The report records expected text, OCR output and edit-distance metrics for inspection.", fill="#52665f", font=font)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUTPUT, optimize=True)
    REPORT.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
