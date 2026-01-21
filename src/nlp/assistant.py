from typing import Dict


def parse_intent(text: str) -> Dict[str, str]:
    intent = {"age_group": "U14" if "U14" in text else "unknown", "focus": "technical" if "technical" in text else "mixed", "level": "intermediate"}
    return intent


def generate_suggestions(intent: Dict[str, str]) -> Dict[str, str]:
    return {"suggestion": f"High-intensity {intent.get('focus')} session for {intent.get('age_group')}.", "rationale": "Based on parsed intent; local-only stub."}

