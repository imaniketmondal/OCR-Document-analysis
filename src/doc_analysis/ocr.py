from __future__ import annotations

import os
from typing import List, Tuple

import numpy as np

from easyocr import Reader
from PIL import Image

_OCR_ENGINE: Reader | None = None


def _get_engine() -> Reader:
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        _OCR_ENGINE = Reader(["en"], gpu=False)
    return _OCR_ENGINE


def _load_images(file_path: str) -> List[np.ndarray]:
    ext = os.path.splitext(file_path.lower())[1]

    if ext == ".pdf":
        from pdf2image import convert_from_path

        pages: List[Image.Image] = convert_from_path(file_path)
        return [np.array(page.convert("RGB")) for page in pages]

    image = Image.open(file_path).convert("RGB")
    return [np.array(image)]


def run_ocr(file_path: str) -> Tuple[str, List[List[Tuple[str, float]]]]:
    engine = _get_engine()
    images = _load_images(file_path)

    all_text: List[str] = []
    page_results: List[List[Tuple[str, float]]] = []

    for image in images:
        result = engine.readtext(image)
        page_text: List[Tuple[str, float]] = []

        for line in result:
            if not isinstance(line, (list, tuple)) or len(line) < 3:
                continue

            text = str(line[1])
            confidence = float(line[2])

            if text:
                page_text.append((text, confidence))
                all_text.append(text)

        page_results.append(page_text)

    return "\n".join(all_text), page_results
