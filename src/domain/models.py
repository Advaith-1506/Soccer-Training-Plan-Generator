from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field, field_validator


class Position(str, Enum):
    defender = "defender"
    midfielder = "midfielder"
    forward = "forward"
    goalkeeper = "goalkeeper"


class SkillLevel(str, Enum):
    rookie = "rookie"
    intermediate = "intermediate"
    advanced = "advanced"


class Assessment(BaseModel):
    id: str
    player_id: str
    date: datetime
    metric_name: str
    value: float
    context: Optional[str] = None


class Drill(BaseModel):
    id: str
    name: str
    category: str
    position_tags: List[Position] = Field(default_factory=list)
    level: SkillLevel
    intensity: int = Field(ge=1, le=10)
    repetition_range: Tuple[int, int]
    duration_minutes: int = Field(ge=1, le=180)
    equipment: List[str] = Field(default_factory=list)
    space: Optional[str] = None
    prerequisites: List[str] = Field(default_factory=list)


class PlayerProfile(BaseModel):
    id: str
    name: str
    age: int = Field(ge=6, le=60)
    position: Position
    skill_level: SkillLevel
    performance_metrics: Dict[str, float] = Field(default_factory=dict)
    constraints: Dict[str, str] = Field(default_factory=dict)

    @field_validator("age")
    @classmethod
    def valid_age(cls, v: int) -> int:
        return v


class SessionPlan(BaseModel):
    id: str
    player_id: Optional[str] = None
    team_id: Optional[str] = None
    date: datetime
    drills: List[Drill] = Field(default_factory=list)
    total_duration_minutes: int = 0
    notes: Optional[str] = None
    safety_flags: List[str] = Field(default_factory=list)
