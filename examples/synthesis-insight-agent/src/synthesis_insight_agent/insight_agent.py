import json
from dataclasses import asdict
from .client import AzureChatClient
from .schema import InsightPayload, SCHEMA_VERSION

SYSTEM_PROMPT = """
You are the AIMoG Apex Synthesis Insight Agent.

You take a single user question about AI systems, architecture, or strategy
and respond with a concise, strictly valid JSON object with this exact shape:

{
  "version": "1.0",
  "summary": "<2-3 sentence high-level answer>",
  "risks": ["<risk-1>", "<risk-2>"],
  "recommendations": ["<action-1>", "<action-2>"],
  "confidence": "<low|medium|high>"
}

Do not include any commentary, markdown, or text outside the JSON.
"""


class SynthesisInsightAgent:
    def __init__(self, client: AzureChatClient) -> None:
        self._client = client

    def run(self, question: str) -> InsightPayload:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]

        raw = self._client.chat(messages)
        data = json.loads(raw)

        return InsightPayload(
            version=data.get("version", SCHEMA_VERSION),
            summary=data.get("summary", ""),
            risks=data.get("risks", []),
            recommendations=data.get("recommendations", []),
            confidence=data.get("confidence", "medium"),
        )

    @staticmethod
    def to_pretty_dict(insight: InsightPayload) -> dict:
        return asdict(insight)