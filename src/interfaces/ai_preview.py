from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from src.interfaces.state import _players, _registry
from src.ai.recommender import rank
from src.ai.progression import readiness_score, adjust_intensity
from src.ai.explain import explanation

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/ai/preview")
def ai_preview_page(request: Request):
    players = list(_players.values())
    return templates.TemplateResponse("ai_preview.html", {"request": request, "players": players})


@router.get("/api/ai/preview/recommendations")
def ai_preview_data(player_id: str = None, top_n: int = 5):
    players = list(_players.values())
    player = None
    if player_id:
        player = next((p for p in players if p.id == player_id), None)
    if player is None and players:
        player = players[0]
    if player is None:
        # fallback demo
        from src.domain.models import PlayerProfile, Position, SkillLevel
        player = PlayerProfile(
            id="demo",
            name="Demo Player",
            age=14,
            position=Position.midfielder,
            skill_level=SkillLevel.intermediate,
            performance_metrics={"pass_accuracy": 68.0, "sprint_time": 6.5, "completion_consistency": 70.0, "error_rate": 18.0, "improvement_delta": 5.0},
            constraints={},
        )
    _registry.load()
    drills = _registry.filter(position=player.position, level=player.skill_level)
    ranked = rank(player, drills, top_n=top_n)
    readiness = readiness_score(player)
    payload = []
    for d, s, feats in ranked:
        payload.append({
            "id": d.id,
            "name": d.name,
            "category": d.category,
            "intensity": adjust_intensity(d.intensity, readiness),
            "duration_minutes": d.duration_minutes,
            "score": round(s, 2),
            "explanation": explanation(d, feats, readiness),
        })
    return JSONResponse({"player_id": player.id, "readiness": round(readiness, 1), "recommendations": payload})

