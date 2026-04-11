# =========================================================
# Confidence‑Grounded RAG Agent
# ---------------------------------------------------------
# A public‑safe, conceptually advanced RAG example that
# demonstrates retrieval‑aware grounding behavior.
#
# This agent:
# - evaluates retrieval confidence heuristically
# - adjusts answer behavior based on context strength
# - emphasizes grounded, careful responses
# - mirrors modern reliability principles without exposing
#   any private AIMoG Apex Nexus architecture
#
# It remains intentionally minimal, readable, and aligned
# with the AIMoG Apex public identity.
# =========================================================

import os
import glob
from dataclasses import dataclass
from typing import List, Dict, Tuple

import numpy as np
import requests


# =========================
# Configuration
# =========================

@dataclass(frozen=True)
class Config:
    endpoint: str = os.getenv("APEX_LLM_ENDPOINT", "")
    api_key: str = os.getenv("APEX_LLM_KEY", "")
    model_chat: str = os.getenv("APEX_LLM_MODEL", "")
    model_embed: str = os.getenv("APEX_LLM_EMBED_MODEL", "") or os.getenv("APEX_LLM_MODEL", "")

    top_k: int = 4
    chunk_tokens: int = 300
    min_retrieval_score: float = 0.25
    temperature: float = 0.2

    def validate(self) -> None:
        if not self.endpoint or not self.api_key or not self.model_chat or not self.model_embed:
            raise ValueError(
                "Missing environment variables. "
                "Required: APEX_LLM_ENDPOINT, APEX_LLM_KEY, APEX_LLM_MODEL, "
                "APEX_LLM_EMBED_MODEL (optional fallback)."
            )


CONFIG = Config()
CONFIG.validate()


# =========================
# HTTP helper
# =========================

def _post_json(url: str, payload: Dict) -> Dict:
    headers = {"Content-Type": "application/json", "api-key": CONFIG.api_key}
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


# =========================
# Embeddings
# =========================

def embed_text(text: str) -> np.ndarray:
    url = f"{CONFIG.endpoint}/embeddings"
    payload = {"input": text, "model": CONFIG.model_embed}
    data = _post_json(url, payload)
    return np.array(data["data"][0]["embedding"], dtype=np.float32)


# =========================
# Document loading + chunking
# =========================

def load_documents(path: str = "data/*.txt") -> List[Dict]:
    docs = []
    for file_path in glob.glob(path):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            if text:
                docs.append({"id": file_path, "text": text})
    return docs


def chunk_text(text: str, max_tokens: int) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunk = " ".join(words[i:i + max_tokens])
        if chunk:
            chunks.append(chunk)
    return chunks


# =========================
# Vector store + retrieval
# =========================

@dataclass
class ChunkEntry:
    id: str
    source_id: str
    text: str
    vector: np.ndarray


def build_vector_store(documents: List[Dict]) -> List[ChunkEntry]:
    store = []
    for doc in documents:
        chunks = chunk_text(doc["text"], CONFIG.chunk_tokens)
        for idx, chunk in enumerate(chunks):
            vec = embed_text(chunk)
            store.append(
                ChunkEntry(
                    id=f"{doc['id']}#chunk{idx}",
                    source_id=doc["id"],
                    text=chunk,
                    vector=vec,
                )
            )
    return store


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def retrieve(query: str, store: List[ChunkEntry]) -> Tuple[List[ChunkEntry], float]:
    if not store:
        return [], 0.0

    q_vec = embed_text(query)
    scored = [(cosine_similarity(q_vec, entry.vector), entry) for entry in store]
    scored.sort(key=lambda x: x[0], reverse=True)

    top = scored[: CONFIG.top_k]
    if not top:
        return [], 0.0

    avg_score = float(sum(s for s, _ in top) / len(top))
    return [e for _, e in top], avg_score


# =========================
# Retrieval confidence heuristic
# =========================

@dataclass
class RetrievalAssessment:
    avg_score: float
    is_confident: bool
    label: str


def assess_retrieval(avg_score: float) -> RetrievalAssessment:
    if avg_score >= 0.55:
        return RetrievalAssessment(avg_score, True, "high")
    if avg_score >= CONFIG.min_retrieval_score:
        return RetrievalAssessment(avg_score, True, "medium")
    return RetrievalAssessment(avg_score, False, "low")


# =========================
# Prompting + generation
# =========================

def build_system_prompt(assessment: RetrievalAssessment) -> str:
    if not assessment.is_confident:
        guidance = (
            "The retrieved context may be incomplete. "
            "Be explicit about uncertainty and avoid fabricating details."
        )
    elif assessment.label == "medium":
        guidance = (
            "The retrieved context is somewhat relevant. "
            "Use it carefully and avoid overstating unsupported claims."
        )
    else:
        guidance = (
            "The retrieved context is strong. "
            "Ground your answer in it and avoid adding unsupported claims."
        )

    return (
        "You are a careful, grounded assistant. "
        "You must base your answers only on the provided context. "
        f"{guidance}"
    )


def generate_answer(query: str, chunks: List[ChunkEntry], assessment: RetrievalAssessment) -> str:
    if not chunks:
        return (
            "I could not retrieve any relevant context for your question. "
            "I prefer not to answer without grounded information."
        )

    context_blocks = [
        f"[Source: {c.source_id}]\n{c.text}"
        for c in chunks
    ]
    context_str = "\n\n---\n\n".join(context_blocks)

    system_prompt = build_system_prompt(assessment)

    user_prompt = f"""
Context:
{context_str}

User question:
{query}

Instructions:
- Answer using only the context above.
- If the context is insufficient, say so explicitly.
- Do not invent facts or speculate beyond the context.
"""

    url = f"{CONFIG.endpoint}/chat/completions"
    payload = {
        "model": CONFIG.model_chat,
        "temperature": CONFIG.temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    data = _post_json(url, payload)
    return data["choices"][0]["message"]["content"].strip()


# =========================
# Main loop
# =========================

def main() -> None:
    print("Loading documents...")
    docs = load_documents()
    store = build_vector_store(docs)
    print(f"Loaded {len(store)} chunks from {len(docs)} documents.\n")

    while True:
        query = input("Ask a question (or type 'exit'): ").strip()
        if query.lower() == "exit":
            break

        chunks, avg_score = retrieve(query, store)
        assessment = assess_retrieval(avg_score)

        print(f"\n[Retrieval score: {assessment.avg_score:.3f} | confidence: {assessment.label}]")

        answer = generate_answer(query, chunks, assessment)

        print("\n--- Answer ---")
        print(answer)
        print("--------------\n")


if __name__ == "__main__":
    main()