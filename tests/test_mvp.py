from src.catalog.registry import DrillRegistry
from src.domain.models import PlayerProfile, Position, SkillLevel
from src.planning.scheduler import assemble_session


def test_plan_generation_basic():
    registry = DrillRegistry()
    registry.load()
    player = PlayerProfile(
        id="p1",
        name="Alex",
        age=14,
        position=Position.midfielder,
        skill_level=SkillLevel.rookie,
        performance_metrics={"pass_accuracy": 70.0},
        constraints={},
    )
    plan = assemble_session(player, registry, target_duration=45)
    assert plan.total_duration_minutes > 0
    assert len(plan.drills) > 0
