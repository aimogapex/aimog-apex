from dataclasses import dataclass
from typing import List


SCHEMA_VERSION = "1.0"


@dataclass
class InsightPayload:
    version: str
    summary: str
    risks: List[str]
    recommendations: List[str]
    confidence: str
    evaluation: str | None = None