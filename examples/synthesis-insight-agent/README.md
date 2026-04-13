# synthesis-insight-agent  
AIMoG Apex - **Synthesis Insight Agent** (Public Edition)

This example demonstrates a minimal, public‑safe Synthesis Insight Agent that:
- accepts a free‑form question about AI systems or architecture  
- calls Azure OpenAI  
- produces a deterministic, structured insight payload  
- passes through public‑safe routing + evaluation stubs  
- uses Apex‑style logging and schema discipline  

> This demo does **not** expose internal AIMoG Apex Nexus orchestration or private routing logic.

---

## Quickstart

```bash
cd examples/synthesis-insight-agent
cp .env.sample .env  # fill in your Azure values

python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install -e .

synthesis-insight-agent "How should I design a cost-aware multi-agent workflow?"
```

---

## Output Shape

The agent always returns JSON matching the public schema:

```json
{
  "version": "1.0",
  "summary": "...",
  "risks": ["..."],
  "recommendations": ["..."],
  "confidence": "low|medium|high"
}
```

The CLI prints a human‑friendly view and annotates it with a deterministic
`evaluation` field to reflect the Phase‑7 evaluation step.

---

## Phase‑7 Public Edition Architecture (Simplified)

```
question
   ↓
routing (public stub)
   ↓
synthesis insight agent
   ↓
azure openai
   ↓
evaluation (public stub)
   ↓
structured insight
```

---

## File Structure

```
synthesis-insight-agent/
  README.md
  pyproject.toml
  .env.sample
  .editorconfig
  .gitignore
  src/
    synthesis_insight_agent/
      __init__.py
      config.py
      client.py
      routing.py
      evaluation.py
      schema.py
      insight_agent.py
      cli.py
```

Each component is intentionally minimal and self‑contained to match the
AIMoG Apex public example style.

---

## Notes

- This example is designed for clarity and reproducibility.  
- It mirrors the structure of `confidence-grounded-rag-agent`.  
- It is safe for public consumption and does not reveal internal Nexus logic.  
- It demonstrates Phase‑7 synthesis behavior in a controlled, minimal form.

---

## License

MIT (same as the parent repository)