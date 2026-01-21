from pydantic import BaseModel, Field
from typing import List
from src.domain.models import SessionPlan, Drill


class PlanValidationResult(BaseModel):
    valid: bool
    issues: List[str] = Field(default_factory=list)


def validate_plan(plan: SessionPlan) -> PlanValidationResult:
    issues: List[str] = []
    if plan.total_duration_minutes <= 0:
        issues.append("total_duration_minutes must be positive")
    seen = set()
    for d in plan.drills:
        if d.id in seen:
            issues.append("duplicate drill in plan")
        seen.add(d.id)
    return PlanValidationResult(valid=len(issues) == 0, issues=issues)
