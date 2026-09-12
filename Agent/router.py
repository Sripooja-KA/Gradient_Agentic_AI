# Query routing logic will be implemented here.
# The router will decide: reddit, weather, both, or neither.
def route_intent(question: str) -> str:
    """Evaluates question intent for explicit tool routing."""
    q = question.lower()
    if any(w in q for w in ["weather", "temperature", "rain", "forecast", "climate"]):
        return "weather"
    elif any(w in q for w in ["reddit", "opinion", "think", "discussion", "people"]):
        return "reddit"
    return "none"