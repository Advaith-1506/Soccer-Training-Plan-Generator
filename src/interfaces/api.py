from fastapi import FastAPI
from typing import Dict, List
from src.interfaces.dto import PlayerCreate, PlanResponse, CoachOverride
from src.domain.models import PlayerProfile, Drill
from src.planning.scheduler import assemble_session
from src.planning.team import assemble_team_sessions
from src.interfaces.state import _players, _registry, logger
from src.ai.storage import append_event
import os
import time


app = FastAPI(title="Soccer Training Automation")


@app.post("/players")
def create_player(p: PlayerCreate) -> PlayerProfile:
    player = PlayerProfile(**p.model_dump())
    _players[player.id] = player
    logger.info(f"player_created id={player.id} position={player.position} skill={player.skill_level}")
    return player


@app.get("/players")
def list_players() -> List[PlayerProfile]:
    return list(_players.values())


@app.get("/drills")
def list_drills() -> List[Drill]:
    return _registry.all()


@app.post("/plans/{player_id}")
def generate_plan(player_id: str) -> PlanResponse:
    player = _players[player_id]
    plan = assemble_session(player, _registry)
    logger.info(f"plan_generated player_id={player.id} duration={plan.total_duration_minutes} drills={len(plan.drills)}")
    try:
        append_event({"type": "plan_generated", "player_id": player.id, "duration": plan.total_duration_minutes, "drills": [d.id for d in plan.drills], "notes": plan.notes})
    except Exception:
        pass
    return PlanResponse(player_id=player.id, total_duration_minutes=plan.total_duration_minutes, drills=plan.drills, ai_notes=plan.notes)


@app.post("/plans/{player_id}/override")
def override_plan(player_id: str, override: CoachOverride) -> PlanResponse:
    player = _players[player_id]
    plan = assemble_session(player, _registry)
    drills = list(plan.drills)
    if override.remove_drill_ids:
        drills = [d for d in drills if d.id not in set(override.remove_drill_ids)]
    if override.add_drill_ids:
        add = [d for d in _registry.all() if d.id in set(override.add_drill_ids)]
        drills.extend(add)
    if override.intensity_cap is not None:
        drills = [d.model_copy(update={"intensity": min(d.intensity, override.intensity_cap)}) for d in drills]
    logger.info(f"plan_overridden player_id={player.id} drills={len(drills)}")
    try:
        append_event({"type": "plan_overridden", "player_id": player.id, "intensity_cap": override.intensity_cap, "drills": [d.id for d in drills]})
    except Exception:
        pass
    return PlanResponse(player_id=player.id, total_duration_minutes=sum(d.duration_minutes for d in drills), drills=drills, ai_notes=plan.notes)


@app.get("/api/ai/health")
def ai_health() -> Dict[str, str]:
    flag = os.environ.get("AI_SCHEDULER_ENABLED", "false").lower() in ("1", "true", "yes")
    status = "enabled" if flag else "disabled"
    return {"scheduler": status, "preview": "enabled", "last_error": "none", "avg_latency_ms": "n/a"}


@app.post("/team/plans")
def generate_team_plans() -> Dict[str, PlanResponse]:
    plans = assemble_team_sessions(list(_players.values()), _registry)
    result: Dict[str, PlanResponse] = {}
    for pid, plan in plans.items():
        result[pid] = PlanResponse(player_id=pid, total_duration_minutes=plan.total_duration_minutes, drills=plan.drills)
    logger.info(f"team_plans_generated count={len(result)}")
    return result
