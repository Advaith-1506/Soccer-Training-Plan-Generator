from typing import List, Tuple, Dict
from src.domain.models import PlayerProfile, Drill
from src.ai.features import combine

# Default weights for features (heuristic baseline)
DEFAULT_WEIGHTS: Dict[str, float] = {
    "pass_accuracy": 0.5,
    "sprint_speed": 0.4,
    "completion_consistency": 0.3,
    "error_rate_inv": 0.2,
    "improvement_delta": 0.3,
    "drill_intensity": 0.15,
    "drill_duration": -0.05,
    "drill_is_technical": 0.2,
    "drill_is_physical": 0.2,
    "drill_is_tactical": 0.1,
    "drill_matches_position": 0.3,
}


def score(features: Dict[str, float], weights: Dict[str, float]) -> float:
    s = 0.0
    for k, w in weights.items():
        s += w * float(features.get(k, 0.0))
    return s


def rank(player: PlayerProfile, drills: List[Drill], top_n: int = 5) -> List[Tuple[Drill, float, Dict[str, float]]]:
    results: List[Tuple[Drill, float, Dict[str, float]]] = []
    weights = DEFAULT_WEIGHTS
    for d in drills:
        feats = combine(player, d)
        s = score(feats, weights)
        results.append((d, s, feats))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]

