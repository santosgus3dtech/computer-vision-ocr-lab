from ocr_lab.metrics import edit_distance, evaluate, normalize_text


def test_normalization_removes_case_and_punctuation_noise():
    assert normalize_text("Hello, OCR!\nLAB") == "hello ocr lab"


def test_edit_distance_handles_insertions_and_replacements():
    assert edit_distance("kitten", "sitting") == 3


def test_evaluation_reports_exact_normalized_match():
    result = evaluate("Open Source OCR", "OPEN source OCR!")
    assert result["exact_match"] is True
    assert result["character_error_rate"] == 0
