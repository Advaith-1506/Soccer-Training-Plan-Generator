from typing import Dict, List
from src.domain.models import Drill


def top_contributors(features: Dict[str, float]) -> List[str]:
    keys = [
        ("pass_accuracy", "Passing accuracy"),
        ("sprint_speed", "Sprint speed"),
        ("completion_consistency", "Completion consistency"),
        ("error_rate_inv", "Low error rate"),
        ("improvement_delta", "Recent improvement"),
        ("drill_is_technical", "Technical focus"),
        ("drill_is_physical", "Physical focus"),
        ("drill_is_tactical", "Tactical focus"),
        ("drill_matches_position", "Matches position"),
    ]
    items = []
    for k, label in keys:
        val = float(features.get(k, 0.0))
        items.append((abs(val), label))
    items.sort(key=lambda x: x[0], reverse=True)
    return [label for _, label in items[:3]]


def explanation(drill: Drill, features: Dict[str, float], readiness: float) -> str:
    contribs = top_contributors(features)
    return f"Ready: {round(readiness, 1)} • Because: " + ", ".join(contribs)

