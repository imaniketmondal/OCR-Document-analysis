from __future__ import annotations

import csv
import os
from dataclasses import dataclass
from typing import List, Tuple

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


@dataclass
class ClassificationResult:
    label: str
    confidence: float


def train_classifier(data_path: str, model_path: str) -> None:
    texts: List[str] = []
    labels: List[str] = []

    with open(data_path, "r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            text = (row.get("text") or "").strip()
            label = (row.get("label") or "unknown").strip()
            if text:
                texts.append(text)
                labels.append(label)

    if not texts:
        raise ValueError("Training data is empty or missing 'text' column.")

    pipeline: Pipeline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(stop_words="english", max_features=5000)),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )

    pipeline.fit(texts, labels)

    model_dir = os.path.dirname(model_path)
    if model_dir:
        os.makedirs(model_dir, exist_ok=True)

    joblib.dump(pipeline, model_path)


def predict_label(text: str, model_path: str) -> ClassificationResult:
    model: Pipeline = joblib.load(model_path)

    if not text.strip():
        return ClassificationResult(label="unknown", confidence=0.0)

    probabilities = model.predict_proba([text])[0]
    classes = list(model.classes_)
    best_index = int(probabilities.argmax())

    return ClassificationResult(label=classes[best_index], confidence=float(probabilities[best_index]))
