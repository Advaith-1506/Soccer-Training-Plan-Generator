from typing import Dict
from src.domain.models import PlayerProfile
from src.catalog.registry import DrillRegistry
from src.config.logging import setup_logging

_players: Dict[str, PlayerProfile] = {}
_registry = DrillRegistry()
_registry.load()
logger = setup_logging()
