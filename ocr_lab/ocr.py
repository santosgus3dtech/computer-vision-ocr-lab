from pathlib import Path

import cv2
import pytesseract

from .preprocess import load_image, preprocess_for_ocr


def set_tesseract_cmd(path: str | None) -> None:
    if path:
        pytesseract.pytesseract.tesseract_cmd = path


def extract_text(path: str | Path, lang: str = "eng", tesseract_cmd: str | None = None) -> str:
    set_tesseract_cmd(tesseract_cmd)
    image = load_image(path)
    processed = preprocess_for_ocr(image)
    rgb = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
    return pytesseract.image_to_string(rgb, lang=lang).strip()
