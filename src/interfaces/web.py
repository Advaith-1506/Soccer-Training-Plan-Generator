from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, FileResponse
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from src.interfaces.state import _players, _registry, logger
from src.domain.models import PlayerProfile, Position, SkillLevel
from src.planning.scheduler import assemble_session
import os
from src.interfaces.ai_preview import router as ai_router
from dotenv import load_dotenv

app = FastAPI(title="Soccer Training Automation Web")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

load_dotenv()
if os.environ.get("AI_PREVIEW_ENABLED", "false").lower() in ("1", "true", "yes"):
    app.include_router(ai_router)

@app.get("/")
def index():
    return FileResponse("index.html")

@app.get("/style.css")
def style_css():
    return FileResponse("style.css", media_type="text/css")

@app.get("/players")
def players(request: Request):
    return templates.TemplateResponse("players.html", {"request": request, "players": list(_players.values()), "positions": list(Position), "levels": list(SkillLevel)})

@app.post("/players")
def create_player(name: str = Form(...), age: int = Form(...), position: str = Form(...), skill_level: str = Form(...)):
    pid = f"p-{len(_players)+1}"
    player = PlayerProfile(id=pid, name=name, age=age, position=Position(position), skill_level=SkillLevel(skill_level), performance_metrics={}, constraints={})
    _players[player.id] = player
    logger.info(f"player_created id={player.id} position={player.position} skill={player.skill_level}")
    return RedirectResponse(url="/players", status_code=303)

@app.get("/drills")
def drills(request: Request):
    return templates.TemplateResponse("drills.html", {"request": request, "drills": _registry.all()})

@app.get("/plans/{player_id}")
def plan(request: Request, player_id: str):
    player = _players[player_id]
    session = assemble_session(player, _registry)
    return templates.TemplateResponse("plan.html", {"request": request, "player": player, "plan": session})

@app.post("/plans/{player_id}/override")
def override(request: Request, player_id: str, intensity_cap: int = Form(None)):
    player = _players[player_id]
    session = assemble_session(player, _registry)
    drills = session.drills
    if intensity_cap is not None:
        drills = [d.model_copy(update={"intensity": min(d.intensity, intensity_cap)}) for d in drills]
    return templates.TemplateResponse("plan.html", {"request": request, "player": player, "plan": session.model_copy(update={"drills": drills, "total_duration_minutes": sum(d.duration_minutes for d in drills)})})
