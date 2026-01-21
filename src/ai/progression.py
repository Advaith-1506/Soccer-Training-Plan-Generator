from src.domain.models import PlayerProfile, SkillLevel


def readiness_score(player: PlayerProfile) -> float:
    pm = player.performance_metrics or {}
    consistency = float(pm.get("completion_consistency", 0.0))
    error_rate = float(pm.get("error_rate", 0.0))
    improvement = float(pm.get("improvement_delta", 0.0))
    base = consistency * 0.5 + max(0.0, 100.0 - error_rate) * 0.3 + improvement * 0.2
    level_boost = {
        SkillLevel.rookie: 0.8,
        SkillLevel.intermediate: 1.0,
        SkillLevel.advanced: 1.1,
    }[player.skill_level]
    return max(0.0, min(100.0, base * level_boost))


def adjust_intensity(intensity: int, readiness: float) -> int:
    if readiness > 75.0:
        return min(10, intensity + 1)
    if readiness < 35.0:
        return max(1, intensity - 1)
    return intensity

