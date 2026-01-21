from typing import List
from src.domain.models import PlayerProfile, Drill, SkillLevel
from src.catalog.registry import DrillRegistry
from src.adaptive.strategy import AdaptiveStrategy


def _level_up(level: SkillLevel) -> SkillLevel:
    order = [SkillLevel.rookie, SkillLevel.intermediate, SkillLevel.advanced]
    idx = order.index(level)
    return order[min(idx + 1, len(order) - 1)]


def select_drills(player: PlayerProfile, registry: DrillRegistry, count: int = 5) -> List[Drill]:
    candidates = registry.filter(position=player.position, level=player.skill_level)
    ranked = []
    pass_acc = player.performance_metrics.get("pass_accuracy", 0.0)
    sprint = player.performance_metrics.get("sprint_time", 0.0)
    for d in candidates:
        score = 0.0
        if d.category == "technical":
            score += pass_acc
        if d.category == "physical":
            score += max(0.0, 10.0 - sprint)
        score += d.intensity * 0.2
        ranked.append((score, d))
    ranked.sort(key=lambda x: x[0], reverse=True)
    drills = [d for _, d in ranked[:count]]
    if pass_acc > 80.0:
        drills = [d.model_copy(update={"level": _level_up(d.level), "intensity": min(10, d.intensity + 1)}) for d in drills]
    return drills


class RuleBasedStrategy:
    def select(self, player: PlayerProfile, registry: DrillRegistry, count: int) -> List[Drill]:
        return select_drills(player, registry, count)
