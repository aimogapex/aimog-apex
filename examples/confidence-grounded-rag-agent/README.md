# **Confidence‑Grounded RAG Agent**

This directory contains the **Confidence‑Grounded RAG Agent**, a minimal but intentionally structured retrieval‑augmented generation (RAG) example that demonstrates **retrieval‑aware grounding behavior**.

It is designed to be:

- **public‑safe**  
- **clean and readable**  
- **conceptually advanced without being enterprise‑grade**  
- **aligned with modern reliability and grounding principles**  
- **a teaser of the design philosophy behind AIMoG Apex**, without exposing any private architecture  

This example is *not* the AIMoG Apex Nexus agent.  
It is a **simplified, approachable demonstration** of careful, context‑aware reasoning.

---

## Purpose

The Confidence‑Grounded RAG Agent demonstrates how a retrieval‑augmented system can:

- load and chunk local documents  
- embed text using an Azure/OpenAI embedding model  
- retrieve relevant chunks using **cosine similarity**  
- compute a **retrieval confidence heuristic**  
- adjust answer behavior based on context strength  
- generate grounded responses that avoid speculation  

This mirrors modern reliability principles while remaining minimal and easy to understand.

---

## Why “Confidence‑Grounded”?

The agent incorporates a lightweight retrieval‑confidence assessment that influences how it answers:

- **High confidence** → grounded, direct answers  
- **Medium confidence** → careful, qualified answers  
- **Low confidence** → explicit uncertainty, no speculation  

This approach reflects a **careful, context‑aware reasoning style** without revealing any private evaluation or governance logic.

---

## Features

- **Document ingestion and chunking** (~300‑token segments)  
- **Embedding generation** via Azure/OpenAI embeddings API  
- **Cosine similarity retrieval**  
- **Top‑k retrieval** (default: 4 chunks)  
- **Retrieval confidence heuristic** (public‑safe)  
- **Confidence‑aware system prompting**  
- **Grounded, careful answer generation**  
- **Minimal, modular Python code**  
- **Simple configuration class** for environment variables  

This example is intentionally small but demonstrates a more thoughtful RAG pattern than a basic tutorial.

---

## Requirements

- Python 3.10+  
- Dependencies listed in `requirements.txt`  
- An LLM endpoint (Azure OpenAI recommended)  
- Environment variables for your model endpoint and key  

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your environment variables (Windows PowerShell):

```powershell
# Persistent (recommended)
setx APEX_LLM_ENDPOINT "your-endpoint-url"
setx APEX_LLM_KEY "your-api-key"
setx APEX_LLM_MODEL "your-chat-model"
setx APEX_LLM_EMBED_MODEL "your-embedding-model"

# Or session-only
$env:APEX_LLM_ENDPOINT = "your-endpoint-url"
$env:APEX_LLM_KEY = "your-api-key"
$env:APEX_LLM_MODEL = "your-chat-model"
$env:APEX_LLM_EMBED_MODEL = "your-embedding-model"
```

(If you're on macOS or Linux, use `export VAR="value"` instead.)

Run the agent:

```bash
python app.py
```

---

## How It Works

1. **Documents are loaded** from `/data`.  
2. Each document is **chunked** into ~300‑token segments.  
3. Each chunk is **embedded** and stored in memory.  
4. A user query is **embedded**.  
5. **Cosine similarity** is used to retrieve the top‑k relevant chunks.  
6. A **retrieval confidence score** is computed.  
7. The system prompt is adjusted based on confidence.  
8. The LLM generates a **grounded, careful answer**.  

This approach demonstrates reliability‑aware reasoning without exposing any private architecture.

---

## File Structure

```
confidence-grounded-rag-agent/
│
├── app.py                 # Main RAG workflow (confidence‑grounded version)
├── requirements.txt       # Dependencies
├── data/                  # Local documents for retrieval
└── README.md              # This file
```

---

## Notes

- This example is intentionally minimal and approachable.  
- It demonstrates **confidence‑aware grounding**, not enterprise‑grade evaluation.  
- It is **not** part of the AIMoG Apex Nexus architecture.  
- It reflects the **public identity** and **design philosophy** of AIMoG Apex.  
- It is suitable for learning, demonstration, and portfolio use.  

---

## Summary

The Confidence‑Grounded RAG Agent is a **clean, modern, reliability‑aware RAG example** that:

- retrieves context  
- evaluates retrieval confidence  
- adjusts answer behavior  
- avoids speculation  
- produces grounded responses  

It is a **public‑safe conceptual mirror** of the careful reasoning principles behind AIMoG Apex — without revealing any private architecture.