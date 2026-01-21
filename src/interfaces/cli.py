import json
import typer
from pathlib import Path
from src.catalog.registry import DrillRegistry
from src.domain.models import PlayerProfile
from src.planning.scheduler import assemble_session
from src.ai.storage import LOG_PATH


app = typer.Typer()


@app.command()
def generate(player_file: Path, out: Path, duration: int = 60):
    data = json.loads(player_file.read_text())
    player = PlayerProfile(**data)
    registry = DrillRegistry()
    registry.load()
    plan = assemble_session(player, registry, target_duration=duration)
    out.write_text(json.dumps({"player_id": player.id, "total_duration_minutes": plan.total_duration_minutes, "drills": [d.model_dump() for d in plan.drills]}, indent=2))

@app.command()
def train_ai(log_path: Path = LOG_PATH):
    """
    Stub: In future, read JSONL logs and fit local models.
    Currently verifies log file exists and prints line count.
    """
    if not log_path.exists():
        typer.echo(f"No logs found at {log_path}")
        raise typer.Exit(code=0)
    count = sum(1 for _ in log_path.open())
    typer.echo(f"AI logs entries: {count}. Training stub complete.")


if __name__ == "__main__":
    app()
