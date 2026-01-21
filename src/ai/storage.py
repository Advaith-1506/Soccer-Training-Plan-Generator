import json
from pathlib import Path
from typing import Any, Dict, List

LOG_PATH = Path("data/ai_logs.jsonl")


def append_event(event: Dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(event) + "\n")

