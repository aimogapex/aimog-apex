import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from app import generate_draft, evaluate_draft, refine_draft

load_dotenv()

def run_demo():
    print("\nAIMoG Apex — Clarity Evaluation Demo")
    print("====================================\n")

    user_request = input("Enter your request: ").strip()
    print("\nUnderstanding request…")
    print("Generating draft…")

    draft = generate_draft(user_request)
    print("\n--- Draft Response ---\n")
    print(draft)

    print("\nEvaluating draft…")
    evaluation = evaluate_draft(draft)

    if evaluation == "strong":
        print("\nDraft rated strong — no refinement needed.")
        final = draft
    else:
        print("\nDraft rated weak — refining…")
        refined = refine_draft(user_request, draft)

        print("\n--- Refined Response ---\n")
        print(refined)

        print("\nRe‑evaluating refined response…")
        second_eval = evaluate_draft(refined)

        if second_eval == "strong":
            print("\nRefined response rated strong.")
        else:
            print("\nRefined response still rated weak — returning refined version anyway.")

        final = refined

    print("\n=== AIMoG Apex Final Output ===\n")
    print(final)
    print("\n====================================\n")


if __name__ == "__main__":
    run_demo()