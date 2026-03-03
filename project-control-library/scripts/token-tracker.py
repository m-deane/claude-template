#!/usr/bin/env python3
"""Token Tracker — Monitor and report token usage across Claude Code sessions.

Usage:
    python token-tracker.py --session           # Show current session usage
    python token-tracker.py --report            # Full usage report
    python token-tracker.py --log INPUT OUTPUT PROJECT TASK  # Log a usage entry
    python token-tracker.py --budget            # Show budget status
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "token-usage.json"
CONFIG_PATH = Path(__file__).parent.parent / "config.json"


def load_usage():
    if DATA_PATH.exists():
        with open(DATA_PATH) as f:
            return json.load(f)
    return {"sessions": [], "daily_totals": {}}


def save_usage(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"token_budget": {"daily_limit": 1000000, "alert_threshold": 0.8}}


def log_usage(input_tokens: int, output_tokens: int, project: str, task: str):
    """Log a token usage entry."""
    data = load_usage()

    entry = {
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "project": project,
        "task": task,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }

    data["sessions"].append(entry)

    # Update daily totals
    date = entry["date"]
    if date not in data["daily_totals"]:
        data["daily_totals"][date] = {"input": 0, "output": 0, "total": 0, "tasks": 0}
    data["daily_totals"][date]["input"] += input_tokens
    data["daily_totals"][date]["output"] += output_tokens
    data["daily_totals"][date]["total"] += input_tokens + output_tokens
    data["daily_totals"][date]["tasks"] += 1

    save_usage(data)
    print(f"Logged: {input_tokens:,} in + {output_tokens:,} out = {input_tokens + output_tokens:,} total")


def show_session():
    """Show current session (today's) usage."""
    data = load_usage()
    today = datetime.now().strftime("%Y-%m-%d")

    today_entries = [s for s in data["sessions"] if s["date"] == today]

    if not today_entries:
        print("No usage logged today.")
        return

    print(f"\n=== Today's Usage ({today}) ===\n")
    print(f"{'Time':<10} {'Project':<20} {'Task':<25} {'Input':>10} {'Output':>10} {'Total':>10}")
    print("-" * 90)

    total_in = 0
    total_out = 0
    for entry in today_entries:
        time = entry["timestamp"].split("T")[1][:8]
        print(
            f"{time:<10} {entry['project']:<20} {entry['task'][:24]:<25} "
            f"{entry['input_tokens']:>10,} {entry['output_tokens']:>10,} {entry['total_tokens']:>10,}"
        )
        total_in += entry["input_tokens"]
        total_out += entry["output_tokens"]

    print("-" * 90)
    print(f"{'TOTAL':<56} {total_in:>10,} {total_out:>10,} {total_in + total_out:>10,}")


def show_report():
    """Show full usage report with daily breakdowns."""
    data = load_usage()
    config = load_config()

    print("\n=== Token Usage Report ===\n")

    # Daily totals for last 7 days
    print("Daily Totals (last 7 days):")
    print(f"{'Date':<12} {'Tasks':>6} {'Input':>12} {'Output':>12} {'Total':>12}")
    print("-" * 60)

    for i in range(6, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        daily = data["daily_totals"].get(date, {"input": 0, "output": 0, "total": 0, "tasks": 0})
        if daily["total"] > 0:
            print(
                f"{date:<12} {daily['tasks']:>6} {daily['input']:>12,} "
                f"{daily['output']:>12,} {daily['total']:>12,}"
            )

    # Per-project breakdown
    project_totals = {}
    for entry in data["sessions"]:
        proj = entry["project"]
        if proj not in project_totals:
            project_totals[proj] = {"input": 0, "output": 0, "total": 0, "tasks": 0}
        project_totals[proj]["input"] += entry["input_tokens"]
        project_totals[proj]["output"] += entry["output_tokens"]
        project_totals[proj]["total"] += entry["total_tokens"]
        project_totals[proj]["tasks"] += 1

    if project_totals:
        print("\n\nPer-Project Totals (all time):")
        print(f"{'Project':<25} {'Tasks':>6} {'Input':>12} {'Output':>12} {'Total':>12}")
        print("-" * 70)
        for proj, totals in sorted(project_totals.items(), key=lambda x: x[1]["total"], reverse=True):
            print(
                f"{proj:<25} {totals['tasks']:>6} {totals['input']:>12,} "
                f"{totals['output']:>12,} {totals['total']:>12,}"
            )


def show_budget():
    """Show budget status."""
    data = load_usage()
    config = load_config()
    budget = config.get("token_budget", {"daily_limit": 1000000, "alert_threshold": 0.8})

    today = datetime.now().strftime("%Y-%m-%d")
    daily = data["daily_totals"].get(today, {"total": 0})

    limit = budget["daily_limit"]
    used = daily["total"]
    remaining = limit - used
    pct = (used / limit * 100) if limit > 0 else 0

    print(f"\n=== Token Budget Status ===\n")
    print(f"Daily limit:  {limit:>12,}")
    print(f"Used today:   {used:>12,} ({pct:.1f}%)")
    print(f"Remaining:    {remaining:>12,}")

    if pct >= budget["alert_threshold"] * 100:
        print(f"\n*** WARNING: Usage at {pct:.1f}% of daily budget ***")
    elif pct >= 50:
        print(f"\nNote: Over 50% of daily budget used")
    else:
        print(f"\nBudget healthy")


def main():
    parser = argparse.ArgumentParser(description="Token Usage Tracker")
    parser.add_argument("--session", action="store_true", help="Show today's usage")
    parser.add_argument("--report", action="store_true", help="Full usage report")
    parser.add_argument("--log", nargs=4, metavar=("INPUT", "OUTPUT", "PROJECT", "TASK"))
    parser.add_argument("--budget", action="store_true", help="Show budget status")

    args = parser.parse_args()

    if args.session:
        show_session()
    elif args.report:
        show_report()
    elif args.log:
        input_t, output_t, project, task = args.log
        log_usage(int(input_t), int(output_t), project, task)
    elif args.budget:
        show_budget()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
