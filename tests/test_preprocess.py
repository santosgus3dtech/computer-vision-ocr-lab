import numpy as np
import pytest

from ocr_lab.preprocess import (
    load_image,
    preprocess_for_ocr,
    resize_for_ocr,
    threshold_otsu,
    to_grayscale,
)


def test_sample_bitmap_loads_with_opencv():
    image = load_image("sample_images/sample-text.pbm")
    assert image.shape == (7, 17, 3)


def test_to_grayscale_converts_bgr_image():
    image = np.zeros((10, 10, 3), dtype=np.uint8)
    gray = to_grayscale(image)
    assert gray.shape == (10, 10)


def test_resize_for_ocr_scales_dimensions():
    image = np.zeros((8, 12), dtype=np.uint8)
    resized = resize_for_ocr(image, scale=2)
    assert resized.shape == (16, 24)


def test_resize_rejects_invalid_scale():
    with pytest.raises(ValueError):
        resize_for_ocr(np.zeros((8, 8), dtype=np.uint8), scale=0)


def test_threshold_output_is_binary():
    gradient = np.tile(np.arange(0, 255, dtype=np.uint8), (20, 1))
    thresholded = threshold_otsu(gradient)
    assert set(np.unique(thresholded)).issubset({0, 255})


def test_preprocess_for_ocr_returns_single_channel_binary_image():
    image = np.full((30, 80, 3), 255, dtype=np.uint8)
    image[10:20, 20:60] = 0
    processed = preprocess_for_ocr(image, scale=1)
    assert processed.shape == (30, 80)
    assert set(np.unique(processed)).issubset({0, 255})
