"""
The structured run log, shared by serve.py and app.py.

Every entry is one JSON line appended to logs/runs.jsonl and echoed to the
terminal, so a session leaves a record you can commit.
"""

import json
from datetime import datetime, timezone

import config

LOG_FILE = config.ROOT / "logs" / "runs.jsonl"


def log_run(**fields):
    """Append one JSON line to logs/runs.jsonl and echo it to the terminal."""
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"), **fields}
    line = json.dumps(entry, ensure_ascii=False)
    LOG_FILE.parent.mkdir(exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)
