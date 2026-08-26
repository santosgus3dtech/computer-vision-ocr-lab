from pathlib import Path

import cv2
import numpy as np


def load_image(path: str | Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    return image


def to_grayscale(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def denoise(gray: np.ndarray) -> np.ndarray:
    return cv2.medianBlur(gray, 3)


def threshold_otsu(gray: np.ndarray) -> np.ndarray:
    _, thresholded = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )
    return thresholded


def resize_for_ocr(image: np.ndarray, scale: float = 2.0) -> np.ndarray:
    if scale <= 0:
        raise ValueError("scale must be positive")
    return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)


def preprocess_for_ocr(image: np.ndarray, scale: float = 2.0) -> np.ndarray:
    gray = to_grayscale(image)
    resized = resize_for_ocr(gray, scale=scale)
    cleaned = denoise(resized)
    return threshold_otsu(cleaned)
