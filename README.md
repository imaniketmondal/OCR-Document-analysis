# Document Analysis (OCR + Classification)

This project extracts text from documents using EasyOCR and classifies the document type using a lightweight text classifier.

## Features
- OCR for images and PDFs (single file input)
- Document type classification (e.g., invoice, receipt, ID)
- CLI for training and analysis
- Docker support

## Requirements
- Python 3.10+
- For PDF OCR on Windows: Poppler in PATH (poppler-utils)

## Setup (Local)
1) Create and activate a virtual environment
2) Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

## Quick Start
Train a small model using the sample data:

```bash
python -m doc_analysis.cli train --data data/sample_train.csv --model models/model.joblib
```

Analyze a document:

```bash
python -m doc_analysis.cli analyze --file path/to/document.pdf --model models/model.joblib
```

OCR only:

```bash
python -m doc_analysis.cli ocr --file path/to/image.png
```

## Docker
Build:

```bash
docker build -t doc-analysis .
```

Run (image or PDF mounted into container):

```bash
docker run --rm -v "${PWD}:/work" doc-analysis analyze --file /work/path/to/document.pdf --model /work/models/model.joblib
```

## Notes
- If you only have images, Poppler is not required.
- The sample model is minimal and meant for testing. Replace with your own labeled data.
