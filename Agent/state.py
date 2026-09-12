from typing import TypedDict, List

class AgentState(TypedDict):
    question: str
    route: str
    raw_evidence: str
    sources: List[str]
    answer: str
    is_grounded: bool
    errors: List[str]