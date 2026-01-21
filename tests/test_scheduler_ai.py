import os
from src.domain.models import PlayerProfile, Position, SkillLevel
from src.catalog.registry import DrillRegistry
from src.planning.scheduler import assemble_session


def test_assemble_session_flag_off():
    os.environ["AI_SCHEDULER_ENABLED"] = "false"
    registry = DrillRegistry()
    registry.load()
    player = PlayerProfile(id="t1", name="Test", age=14, position=Position.midfielder, skill_level=SkillLevel.intermediate, performance_metrics={}, constraints={})
    plan = assemble_session(player, registry, target_duration=60)
    assert plan.total_duration_minutes <= 60
    assert plan.notes is None


def test_assemble_session_flag_on():
    os.environ["AI_SCHEDULER_ENABLED"] = "true"
    registry = DrillRegistry()
    registry.load()
    player = PlayerProfile(id="t2", name="Test", age=14, position=Position.midfielder, skill_level=SkillLevel.intermediate, performance_metrics={"pass_accuracy": 70.0}, constraints={})
    plan = assemble_session(player, registry, target_duration=60)
    assert plan.total_duration_minutes <= 60
    assert plan.notes is not None
