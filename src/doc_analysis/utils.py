from __future__ import annotations

import json
from typing import List


def load_labels(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)
