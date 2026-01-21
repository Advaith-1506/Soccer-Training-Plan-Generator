from datetime import datetime
from typing import List
from src.domain.models import SessionPlan, PlayerProfile, Drill
from src.adaptive.selectors import select_drills
from src.ai.recommender import rank
from src.ai.progression import readiness_score, adjust_intensity
from src.ai.explain import explanation
import os
from src.catalog.registry import DrillRegistry


def assemble_session(player: PlayerProfile, registry: DrillRegistry, target_duration: int = 60) -> SessionPlan:
    drills: List[Drill] = []
    use_ai = os.environ.get("AI_SCHEDULER_ENABLED", "false").lower() in ("1", "true", "yes")
    selected = select_drills(player, registry, count=6)
    explanations = {}
    if use_ai:
        try:
            candidates = registry.filter(position=player.position, level=player.skill_level)
            ranked = rank(player, candidates, top_n=6)
            ready = readiness_score(player)
            ordered = []
            for d, s, feats in ranked:
                adjusted = d.model_copy(update={"intensity": adjust_intensity(d.intensity, ready)})
                explanations[adjusted.id] = explanation(adjusted, feats, ready)
                ordered.append(adjusted)
            selected = ordered
        except Exception as e:
            selected = select_drills(player, registry, count=6)
    total = 0
    for d in selected:
        if total + d.duration_minutes <= target_duration:
            drills.append(d)
            total += d.duration_minutes
    plan = SessionPlan(
        id=f"plan-{player.id}-{int(datetime.now().timestamp())}",
        player_id=player.id,
        date=datetime.now(),
        drills=drills,
        total_duration_minutes=total,
        notes=None,
        safety_flags=[],
    )
    if use_ai and explanations:
        plan.notes = "AI scheduling active"
    return plan
