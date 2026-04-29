from __future__ import annotations

from dataclasses import asdict
from typing import Dict

from .classifier import ClassificationResult, predict_label
from .ocr import run_ocr


def analyze_document(file_path: str, model_path: str) -> Dict:
    text, page_results = run_ocr(file_path)
    prediction: ClassificationResult = predict_label(text, model_path)

    return {
        "file": file_path,
        "text": text,
        "pages": [
            [{"text": t, "confidence": c} for t, c in page]
            for page in page_results
        ],
        "prediction": asdict(prediction),
    }
