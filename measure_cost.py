#!/usr/bin/env python3
"""
Average the cost of the last N agent runs from logs/runs.jsonl.

    python measure_cost.py          last 10 successful /ask runs
    python measure_cost.py -n 5     last 5

How the numbers get there: serve.py's /ask reads generate.py's session
counters before and after run_agent() and logs the difference. Token counts
are the ones Gemini reports on every response (usage_metadata), not an
estimate. Seconds are wall-clock time around run_agent().

Start the server with the cache OFF before measuring, or repeated runs reuse
saved answers and report 0 tokens:

    $env:AI201_CACHE = '0'; python serve.py        (PowerShell)
    AI201_CACHE=0 python serve.py                  (macOS / Linux)
"""

import argparse
import json
import sys

import config  # noqa: F401 — UTF-8 console on Windows
from utils.run_log import LOG_FILE

METRICS = ["total_tokens", "prompt_tokens", "output_tokens", "model_calls", "seconds"]


def load_runs() -> list[dict]:
    if not LOG_FILE.exists():
        sys.exit(f"No log file yet at {LOG_FILE}. Run serve.py and send some /ask requests.")
    runs = []
    with LOG_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            # Successful /ask runs logged with cost fields. Skips add events,
            # rejected/crashed requests, and older lines from before counting.
            if entry.get("event") == "ask" and "status" not in entry and "total_tokens" in entry:
                runs.append(entry)
    return runs


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("-n", type=int, default=10, help="how many recent runs to average (default 10)")
    args = parser.parse_args()

    runs = load_runs()[-args.n:]
    if not runs:
        sys.exit("No successful /ask runs with cost fields in the log yet.")
    if len(runs) < args.n:
        print(f"Warning: only {len(runs)} runs found, wanted {args.n}.\n")

    cached = sum(1 for r in runs if r.get("cache_enabled"))
    if cached:
        print(f"Warning: {cached} of these runs had the cache ON — their token counts "
              f"may be 0 and the average will understate the cost.\n")

    queries = {r.get("query") for r in runs}
    print(f"Runs averaged: {len(runs)}  ({runs[0]['timestamp']} to {runs[-1]['timestamp']})")
    print(f"Queries: {', '.join(repr(q) for q in sorted(queries))}\n")

    print(f"{'metric':<15}{'average':>10}{'min':>10}{'max':>10}")
    print("-" * 45)
    for m in METRICS:
        values = [r[m] for r in runs]
        avg = sum(values) / len(values)
        print(f"{m:<15}{avg:>10.2f}{min(values):>10}{max(values):>10}")


if __name__ == "__main__":
    main()
