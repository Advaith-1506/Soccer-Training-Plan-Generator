import json
from pathlib import Path
from typing import List, Optional
from src.domain.models import Drill, Position, SkillLevel


def _default_drills() -> List[Drill]:
    return [
        Drill(
            id="pass-accuracy-1",
            name="Passing Grid",
            category="technical",
            position_tags=[Position.midfielder, Position.defender],
            level=SkillLevel.rookie,
            intensity=4,
            repetition_range=(20, 40),
            duration_minutes=20,
            equipment=["cones", "balls"],
            space="half",
            prerequisites=[],
        ),
        Drill(
            id="shooting-1",
            name="Shooting Ladders",
            category="technical",
            position_tags=[Position.forward],
            level=SkillLevel.intermediate,
            intensity=6,
            repetition_range=(15, 30),
            duration_minutes=25,
            equipment=["balls"],
            space="box",
            prerequisites=[],
        ),
        Drill(
            id="goalkeeper-react-1",
            name="Reaction Saves",
            category="technical",
            position_tags=[Position.goalkeeper],
            level=SkillLevel.rookie,
            intensity=5,
            repetition_range=(20, 30),
            duration_minutes=20,
            equipment=["balls"],
            space="box",
            prerequisites=[],
        ),
        Drill(
            id="defensive-press-1",
            name="Defensive Pressing",
            category="tactical",
            position_tags=[Position.defender, Position.midfielder],
            level=SkillLevel.intermediate,
            intensity=7,
            repetition_range=(10, 20),
            duration_minutes=20,
            equipment=["cones", "vests"],
            space="half",
            prerequisites=[],
        ),
    ]


class DrillRegistry:
    def __init__(self, catalog_path: Optional[Path] = None):
        self.catalog_path = catalog_path
        self._drills: List[Drill] = []
        self._cache: dict = {}

    def load(self) -> None:
        if self.catalog_path and self.catalog_path.exists():
            data = json.loads(self.catalog_path.read_text())
            self._drills = [Drill(**d) for d in data]
        else:
            self._drills = _default_drills()

    def all(self) -> List[Drill]:
        return list(self._drills)

    def filter(
        self,
        position: Optional[Position] = None,
        level: Optional[SkillLevel] = None,
        category: Optional[str] = None,
    ) -> List[Drill]:
        key = (position.value if position else None, level.value if level else None, category)
        if key in self._cache:
            return list(self._cache[key])
        drills = self._drills
        if position:
            drills = [d for d in drills if position in d.position_tags]
        if level:
            order = {"rookie": 0, "intermediate": 1, "advanced": 2}
            drills = [d for d in drills if order[d.level.value] <= order[level.value]]
        if category:
            drills = [d for d in drills if d.category == category]
        self._cache[key] = list(drills)
        return list(drills)
