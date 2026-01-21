from typing import Dict, Optional
from src.domain.models import PlayerProfile


class InMemoryPlayerRepo:
    def __init__(self):
        self._players: Dict[str, PlayerProfile] = {}

    def add(self, player: PlayerProfile) -> None:
        self._players[player.id] = player

    def get(self, player_id: str) -> Optional[PlayerProfile]:
        return self._players.get(player_id)

    def list(self):
        return list(self._players.values())
