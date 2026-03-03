#!/usr/bin/env python3
"""Port Manager — Safe port allocation for multi-project environments.

Usage:
    python port-manager.py --check 3000-4000    # Check which ports are available
    python port-manager.py --scan               # Scan all ports and show status
    python port-manager.py --find [type]        # Find next available port for type
    python port-manager.py --register PORT PID PROJECT SERVICE  # Register a port
    python port-manager.py --release PORT       # Release a port
    python port-manager.py --cleanup            # Remove stale registry entries

Port ranges by convention:
    3000-3999: Development servers (Next.js, React, etc.)
    4000-4999: Documentation sites (Docusaurus, Storybook)
    5000-5999: Dashboards and monitoring UIs
    8000-8999: Backend API servers
    9000-9999: Database tools (Prisma Studio, pgAdmin)
"""

import argparse
import json
import os
import signal
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config.json"

PORT_RANGES = {
    "dev": (3000, 3999),
    "docs": (4000, 4999),
    "dashboard": (5000, 5999),
    "api": (8000, 8999),
    "db-tools": (9000, 9999),
}


def load_config():
    """Load the control library config."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {CONFIG_PATH} is malformed JSON, using defaults")
    return {"port_registry": {}}


def save_config(config):
    """Save the control library config."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def is_port_in_use(port: int) -> bool:
    """Check if a port is currently in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def is_pid_alive(pid: int) -> bool:
    """Check if a process is still running."""
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def get_port_process(port: int) -> str:
    """Get the process using a port."""
    try:
        result = subprocess.run(
            ["ss", "-tlnp", f"sport = :{port}"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return "unknown"


def check_range(start: int, end: int):
    """Check which ports in a range are available."""
    print(f"\nPort scan: {start}-{end}")
    print(f"{'Port':<8} {'Status':<12} {'Process'}")
    print("-" * 50)

    available = 0
    for port in range(start, end + 1):
        if is_port_in_use(port):
            proc = get_port_process(port)
            print(f"{port:<8} {'IN USE':<12} {proc[:40]}")
        else:
            available += 1

    print(f"\n{available}/{end - start + 1} ports available")


def find_available(port_type: str = "dev") -> int:
    """Find the next available port for a given type."""
    if port_type not in PORT_RANGES:
        print(f"Unknown type: {port_type}. Options: {', '.join(PORT_RANGES.keys())}")
        sys.exit(1)

    start, end = PORT_RANGES[port_type]
    for port in range(start, end + 1):
        if not is_port_in_use(port):
            print(f"Available: {port} (type: {port_type})")
            return port

    print(f"No available ports in range {start}-{end}")
    sys.exit(1)


def register_port(port: int, pid: int, project: str, service: str):
    """Register a port in the registry."""
    config = load_config()
    config["port_registry"][str(port)] = {
        "project": project,
        "service": service,
        "pid": pid,
        "started": datetime.now().isoformat(),
        "url": f"http://localhost:{port}",
    }
    save_config(config)
    print(f"Registered port {port} for {project}/{service} (PID {pid})")


def release_port(port: int):
    """Release a port from the registry."""
    config = load_config()
    key = str(port)
    if key in config["port_registry"]:
        entry = config["port_registry"].pop(key)
        save_config(config)
        print(f"Released port {port} (was {entry['project']}/{entry['service']})")
    else:
        print(f"Port {port} not in registry")


def cleanup_registry():
    """Remove stale entries where the process is no longer running."""
    config = load_config()
    stale = []

    for port, entry in config["port_registry"].items():
        pid = entry.get("pid", 0)
        if not is_pid_alive(pid):
            stale.append(port)
            print(f"Stale: port {port} — PID {pid} ({entry['project']}/{entry['service']}) no longer running")

    for port in stale:
        del config["port_registry"][port]

    if stale:
        save_config(config)
        print(f"\nCleaned {len(stale)} stale entries")
    else:
        print("No stale entries found")


def scan_all():
    """Show full registry status with live port checks."""
    config = load_config()
    registry = config.get("port_registry", {})

    print("\n=== Port Registry ===")
    print(f"{'Port':<8} {'Project':<20} {'Service':<15} {'PID':<8} {'Alive':<8} {'Port Open'}")
    print("-" * 75)

    for port, entry in sorted(registry.items(), key=lambda x: int(x[0])):
        pid = entry.get("pid", 0)
        alive = is_pid_alive(pid)
        port_open = is_port_in_use(int(port))
        print(
            f"{port:<8} {entry['project']:<20} {entry['service']:<15} "
            f"{pid:<8} {'yes' if alive else 'NO':<8} {'yes' if port_open else 'NO'}"
        )

    if not registry:
        print("(empty — no registered services)")


def main():
    parser = argparse.ArgumentParser(description="Port Manager for multi-project environments")
    parser.add_argument("--check", metavar="RANGE", help="Check port range (e.g., 3000-4000)")
    parser.add_argument("--scan", action="store_true", help="Scan registry and show status")
    parser.add_argument("--find", metavar="TYPE", nargs="?", const="dev", help="Find available port")
    parser.add_argument("--register", nargs=4, metavar=("PORT", "PID", "PROJECT", "SERVICE"))
    parser.add_argument("--release", type=int, metavar="PORT", help="Release a port")
    parser.add_argument("--cleanup", action="store_true", help="Remove stale registry entries")

    args = parser.parse_args()

    if args.check:
        start, end = map(int, args.check.split("-"))
        check_range(start, end)
    elif args.scan:
        scan_all()
    elif args.find:
        find_available(args.find)
    elif args.register:
        port, pid, project, service = args.register
        register_port(int(port), int(pid), project, service)
    elif args.release is not None:
        release_port(args.release)
    elif args.cleanup:
        cleanup_registry()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
