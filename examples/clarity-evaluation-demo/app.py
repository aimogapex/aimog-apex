import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

MODEL = "gpt-4o-mini"  # Phase‑9 aligned lightweight model


def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_draft(user_request: str) -> str:
    prompt = load_prompt("prompt_templates/draft.txt").replace("{{user_request}}", user_request)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
        )
    return response.choices[0].message.content.strip()


def evaluate_draft(draft: str) -> str:
    prompt = load_prompt("prompt_templates/evaluation.txt").replace("{{draft}}", draft)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
        )
    return response.choices[0].message.content.strip().lower()


def refine_draft(user_request: str, previous_draft: str) -> str:
    refine_prompt = f"""
Refine the following draft response to better address the user request.

User request:
{user_request}

Previous draft:
{previous_draft}

Produce a clearer, more structured version.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": refine_prompt}],
        temperature=0.2
        )
    return response.choices[0].message.content.strip()


def clarity_evaluation_loop(user_request: str) -> str:
    draft = generate_draft(user_request)
    evaluation = evaluate_draft(draft)

    if evaluation == "strong":
        return draft

    refined = refine_draft(user_request, draft)
    second_eval = evaluate_draft(refined)

    return refined if second_eval == "strong" else refined


if __name__ == "__main__":
    user_request = input("Enter your request: ")
    final_output = clarity_evaluation_loop(user_request)
    print("\n--- AIMoG Apex Final Output ---\n")
    print(final_output)