def route(question: str) -> str:
    """
    Public-safe routing stub.

    In the full Nexus, routing would select among multiple agents.
    Here we always return the synthesis insight agent identifier.
    """
    return "synthesis-insight-agent"