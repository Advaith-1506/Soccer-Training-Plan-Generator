from pydantic import BaseModel
from typing import Dict, List, Optional
from src.domain.models import Position, SkillLevel, Drill


class PlayerCreate(BaseModel):
    id: str
    name: str
    age: int
    position: Position
    skill_level: SkillLevel
    performance_metrics: Dict[str, float] = {}
    constraints: Dict[str, str] = {}


class PlanResponse(BaseModel):
    player_id: str
    total_duration_minutes: int
    drills: List[Drill]
    ai_notes: Optional[str] = None


class CoachOverride(BaseModel):
    add_drill_ids: Optional[List[str]] = None
    remove_drill_ids: Optional[List[str]] = None
    intensity_cap: Optional[int] = None
