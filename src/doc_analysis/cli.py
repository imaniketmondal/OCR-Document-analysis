from __future__ import annotations

import argparse
import json
import sys

from .classifier import predict_label, train_classifier


def _print_json(payload) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=True))


def _prompt_file_path() -> str:
    while True:
        path = input("Enter file path (PDF or image): ").strip()
        if path:
            return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Document OCR + classification")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ocr_parser = subparsers.add_parser("ocr", help="Run OCR on a file")
    ocr_parser.add_argument("--file", required=False, help="Path to image or PDF")

    train_parser = subparsers.add_parser("train", help="Train classifier model")
    train_parser.add_argument("--data", required=True, help="CSV with text,label columns")
    train_parser.add_argument("--model", required=True, help="Output model path")

    predict_parser = subparsers.add_parser("predict", help="Predict label from raw text")
    predict_parser.add_argument("--text", required=True, help="Raw text to classify")
    predict_parser.add_argument("--model", required=True, help="Model path")

    analyze_parser = subparsers.add_parser("analyze", help="OCR + classification")
    analyze_parser.add_argument("--file", required=False, help="Path to image or PDF")
    analyze_parser.add_argument("--model", required=True, help="Model path")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "ocr":
        from .ocr import run_ocr

        if not args.file:
            args.file = _prompt_file_path()

        text, pages = run_ocr(args.file)
        _print_json({
            "file": args.file,
            "text": text,
            "pages": [
                [{"text": t, "confidence": c} for t, c in page]
                for page in pages
            ],
        })
        return

    if args.command == "train":
        train_classifier(args.data, args.model)
        print(f"Model saved to {args.model}")
        return

    if args.command == "predict":
        result = predict_label(args.text, args.model)
        _print_json({"label": result.label, "confidence": result.confidence})
        return

    if args.command == "analyze":
        from .pipeline import analyze_document

        if not args.file:
            args.file = _prompt_file_path()

        payload = analyze_document(args.file, args.model)
        _print_json(payload)
        return

    print("Unknown command", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
