import argparse
import logging

from .config import Settings
from .client import AzureChatClient
from .routing import route
from .evaluation import evaluate
from .insight_agent import SynthesisInsightAgent


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AIMoG Apex - Phase-7 Synthesis Insight Agent demo"
    )
    parser.add_argument(
        "question",
        type=str,
        help="Question about AI/architecture to analyze",
    )
    args = parser.parse_args()

    settings = Settings.from_env()
    logging.basicConfig(
        level=settings.log_level,
        format="[synthesis-insight-agent] %(message)s",
    )

    logging.info("loading config")
    target = route(args.question)
    logging.info("routing → %s", target)

    client = AzureChatClient(settings)
    agent = SynthesisInsightAgent(client)

    logging.info("sending request → azure-openai")
    insight = agent.run(args.question)
    insight = evaluate(insight)
    logging.info("received structured insight")

    print()
    print("=== Synthesis Insight (v", insight.version, ") ===", sep="")
    print("Summary:")
    print(insight.summary)
    print()
    print("Risks:")
    for r in insight.risks:
        print(f"- {r}")
    print()
    print("Recommendations:")
    for rec in insight.recommendations:
        print(f"- {rec}")
    print()
    print("Confidence:", insight.confidence)
    print("Evaluation:", insight.evaluation)
    print()


if __name__ == "__main__":
    main()