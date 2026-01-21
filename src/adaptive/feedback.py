from src.domain.models import PlayerProfile, Assessment, SkillLevel


def apply_feedback(player: PlayerProfile, assessment: Assessment) -> PlayerProfile:
    metrics = dict(player.performance_metrics)
    metrics[assessment.metric_name] = assessment.value
    level = player.skill_level
    if assessment.metric_name == "pass_accuracy" and assessment.value > 85.0:
        level = SkillLevel.intermediate if level == SkillLevel.rookie else level
    return player.model_copy(update={"performance_metrics": metrics, "skill_level": level})
