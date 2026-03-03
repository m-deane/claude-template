#!/usr/bin/env python3
"""Project Scanner — Discover and index all repositories in the projects directory.

Usage:
    python project-scanner.py                  # Scan and list all projects
    python project-scanner.py --register       # Register discovered projects in config.json
    python project-scanner.py --status         # Generate status report for all projects
    python project-scanner.py --status PROJECT # Status for a specific project
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.json"
DEFAULT_PROJECTS_ROOT = Path.home() / "projects"


def load_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {CONFIG_PATH} is malformed JSON, using defaults")
    return {"projects_root": str(DEFAULT_PROJECTS_ROOT), "managed_projects": [], "port_registry": {}}


def get_projects_root():
    """Read projects_root from config.json, fall back to ~/projects."""
    config = load_config()
    root = config.get("projects_root", str(DEFAULT_PROJECTS_ROOT))
    return Path(root).expanduser()


PROJECTS_ROOT = get_projects_root()


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def has_claude_md(path: Path) -> bool:
    return (path / "CLAUDE.md").exists()


def has_claude_config(path: Path) -> bool:
    return (path / ".claude").is_dir()


def get_git_info(path: Path) -> dict:
    """Get git status for a project."""
    info = {"branch": "unknown", "clean": False, "last_commit": "unknown", "uncommitted_files": 0}
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=path, timeout=5
        )
        info["branch"] = result.stdout.strip() or "detached"

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=path, timeout=5
        )
        changes = [l for l in result.stdout.strip().split("\n") if l.strip()]
        info["clean"] = len(changes) == 0
        info["uncommitted_files"] = len(changes)

        result = subprocess.run(
            ["git", "log", "-1", "--format=%h %s (%cr)"],
            capture_output=True, text=True, cwd=path, timeout=5
        )
        info["last_commit"] = result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return info


def get_project_info(path: Path) -> dict:
    """Extract project info from CLAUDE.md and package.json."""
    info = {
        "name": path.name,
        "path": str(path),
        "is_git_repo": is_git_repo(path),
        "has_claude_md": has_claude_md(path),
        "has_claude_config": has_claude_config(path),
        "stack": "unknown",
        "description": "",
    }

    # Read CLAUDE.md for project info
    claude_md = path / "CLAUDE.md"
    if claude_md.exists():
        content = claude_md.read_text()
        for line in content.split("\n"):
            if "**Stack**:" in line or "**Technology Stack**:" in line:
                info["stack"] = line.split(":", 1)[1].strip().strip("*")
            if line.startswith("**") and "—" in line:
                info["description"] = line.split("—", 1)[1].strip() if "—" in line else ""

    # Check for package.json (Node projects)
    pkg_json = path / "package.json"
    if pkg_json.exists():
        try:
            with open(pkg_json) as f:
                pkg = json.load(f)
            info["has_package_json"] = True
            info["scripts"] = list(pkg.get("scripts", {}).keys())
        except json.JSONDecodeError:
            info["has_package_json"] = False

    # Check for requirements.txt or pyproject.toml (Python projects)
    info["has_requirements"] = (path / "requirements.txt").exists()
    info["has_pyproject"] = (path / "pyproject.toml").exists()

    # Count skills, commands, agents
    claude_dir = path / ".claude"
    if claude_dir.is_dir():
        skills_dir = claude_dir / "skills"
        commands_dir = claude_dir / "commands"
        agents_dir = claude_dir / "agents"
        info["skills_count"] = len(list(skills_dir.glob("*/SKILL.md"))) if skills_dir.exists() else 0
        info["commands_count"] = len(list(commands_dir.glob("*.md"))) if commands_dir.exists() else 0
        info["agents_count"] = len(list(agents_dir.glob("*.md"))) if agents_dir.exists() else 0

    return info


def scan_projects():
    """Scan the projects directory for all repositories."""
    if not PROJECTS_ROOT.exists():
        print(f"Projects root not found: {PROJECTS_ROOT}")
        print("Set PROJECTS_ROOT environment variable or create ~/projects/")
        sys.exit(1)

    projects = []
    for item in sorted(PROJECTS_ROOT.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            info = get_project_info(item)
            projects.append(info)

    return projects


def display_projects(projects):
    """Display discovered projects in a table."""
    print(f"\n=== Projects in {PROJECTS_ROOT} ===")
    print(f"{'Name':<25} {'Git':<5} {'CLAUDE.md':<10} {'Config':<8} {'Stack'}")
    print("-" * 80)

    for p in projects:
        print(
            f"{p['name']:<25} "
            f"{'yes' if p['is_git_repo'] else 'no':<5} "
            f"{'yes' if p['has_claude_md'] else 'no':<10} "
            f"{'yes' if p['has_claude_config'] else 'no':<8} "
            f"{p['stack'][:30]}"
        )

    print(f"\nTotal: {len(projects)} projects")
    managed = sum(1 for p in projects if p["has_claude_md"])
    print(f"With CLAUDE.md: {managed}")


def register_projects(projects):
    """Register discovered projects in config.json."""
    config = load_config()
    config["managed_projects"] = [
        {"name": p["name"], "path": p["path"]}
        for p in projects
        if p["has_claude_md"]
    ]
    save_config(config)
    print(f"Registered {len(config['managed_projects'])} projects in config.json")


def generate_status(project_name=None):
    """Generate status report for projects."""
    projects = scan_projects()

    if project_name:
        projects = [p for p in projects if p["name"] == project_name]
        if not projects:
            print(f"Project not found: {project_name}")
            sys.exit(1)

    print(f"\n=== Project Status Report — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")

    for p in projects:
        if not p["is_git_repo"]:
            continue

        git = get_git_info(Path(p["path"]))

        print(f"## {p['name']}")
        print(f"  Branch: {git['branch']}")
        clean_status = "yes" if git["clean"] else f"NO ({git['uncommitted_files']} files)"
        print(f"  Clean: {clean_status}")
        print(f"  Last commit: {git['last_commit']}")
        print(f"  Stack: {p['stack']}")
        if p.get("skills_count", 0) > 0:
            print(f"  Skills: {p['skills_count']}, Commands: {p.get('commands_count', 0)}, Agents: {p.get('agents_count', 0)}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Project Scanner")
    parser.add_argument("--register", action="store_true", help="Register projects in config")
    parser.add_argument("--status", nargs="?", const="__all__", help="Generate status report")

    args = parser.parse_args()
    projects = scan_projects()

    if args.register:
        display_projects(projects)
        register_projects(projects)
    elif args.status:
        project_name = None if args.status == "__all__" else args.status
        generate_status(project_name)
    else:
        display_projects(projects)


if __name__ == "__main__":
    main()
