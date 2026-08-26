import argparse
import os

from .ocr import extract_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run OCR on an image with OpenCV preprocessing.")
    parser.add_argument("image", help="Path to the image to read.")
    parser.add_argument("--lang", default="eng", help="Tesseract language, for example eng or por.")
    parser.add_argument(
        "--tesseract-cmd",
        default=os.getenv("TESSERACT_CMD"),
        help="Optional path to the Tesseract executable.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    print(extract_text(args.image, lang=args.lang, tesseract_cmd=args.tesseract_cmd))


if __name__ == "__main__":
    main()
