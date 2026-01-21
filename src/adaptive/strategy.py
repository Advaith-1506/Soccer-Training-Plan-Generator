from typing import List, Protocol
from src.domain.models import PlayerProfile, Drill
from src.catalog.registry import DrillRegistry


class AdaptiveStrategy(Protocol):
    def select(self, player: PlayerProfile, registry: DrillRegistry, count: int) -> List[Drill]:
        ...


