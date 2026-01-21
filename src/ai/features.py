from typing import Dict, List, Tuple
from src.domain.models import PlayerProfile, Drill, Position, SkillLevel


def player_features(player: PlayerProfile) -> Dict[str, float]:
    pm = player.performance_metrics or {}
    pass_accuracy = float(pm.get("pass_accuracy", 0.0))
    sprint_time = float(pm.get("sprint_time", 0.0))
    completion_consistency = float(pm.get("completion_consistency", 0.0))
    error_rate = float(pm.get("error_rate", 0.0))
    improvement_delta = float(pm.get("improvement_delta", 0.0))
    return {
        "pass_accuracy": pass_accuracy,
        "sprint_speed": max(0.0, 10.0 - sprint_time),
        "completion_consistency": completion_consistency,
        "error_rate_inv": max(0.0, 100.0 - error_rate),
        "improvement_delta": improvement_delta,
        "age": float(player.age),
        "position_defender": 1.0 if player.position == Position.defender else 0.0,
        "position_midfielder": 1.0 if player.position == Position.midfielder else 0.0,
        "position_forward": 1.0 if player.position == Position.forward else 0.0,
        "position_goalkeeper": 1.0 if player.position == Position.goalkeeper else 0.0,
        "level_rookie": 1.0 if player.skill_level == SkillLevel.rookie else 0.0,
        "level_intermediate": 1.0 if player.skill_level == SkillLevel.intermediate else 0.0,
        "level_advanced": 1.0 if player.skill_level == SkillLevel.advanced else 0.0,
    }


def drill_features(drill: Drill) -> Dict[str, float]:
    return {
        "drill_intensity": float(drill.intensity),
        "drill_duration": float(drill.duration_minutes),
        "drill_is_technical": 1.0 if drill.category == "technical" else 0.0,
        "drill_is_physical": 1.0 if drill.category == "physical" else 0.0,
        "drill_is_tactical": 1.0 if drill.category == "tactical" else 0.0,
        "drill_matches_position": 1.0 if drill.position_tags else 0.0,
    }


def combine(player: PlayerProfile, drill: Drill) -> Dict[str, float]:
    pf = player_features(player)
    df = drill_features(drill)
    x = {**pf, **df}
    return x

