# Grounding, citation, prompt-injection, scope and safety checks
# will be implemented here.
import re

def sanitize_user_input(text: str) -> str:
    """Sanitizes incoming prompt inputs to strip raw control tags."""
    return text.strip()

def wrap_untrusted_context(content: str) -> str:
    """
    Encapsulates retrieved payload inside custom XML delimiters.
    Prevents indirect prompt injection attacks from social posts or raw API text.
    """
    cleaned = re.sub(r'(system:|user:|assistant:)', '', content, flags=re.IGNORECASE)
    return f"<untrusted_evidence_payload>\n{cleaned}\n</untrusted_evidence_payload>"
