from .schema import InsightPayload


def evaluate(insight: InsightPayload) -> InsightPayload:
    """
    Public-safe evaluation stub.

    In the full Nexus, evaluation would score or compare agents.
    Here we simply mark the insight as 'validated'.
    """
    insight.evaluation = "validated"
    return insight