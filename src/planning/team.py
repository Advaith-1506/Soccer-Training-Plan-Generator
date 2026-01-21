from typing import Dict, List
from src.domain.models import PlayerProfile, SessionPlan
from src.catalog.registry import DrillRegistry
from src.planning.scheduler import assemble_session


def assemble_team_sessions(players: List[PlayerProfile], registry: DrillRegistry, target_duration: int = 60) -> Dict[str, SessionPlan]:
    plans: Dict[str, SessionPlan] = {}
    for p in players:
        plans[p.id] = assemble_session(p, registry, target_duration=target_duration)
    return plans
