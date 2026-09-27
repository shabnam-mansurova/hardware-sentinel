"""Linux system and systemd health collection."""

from __future__ import annotations

import subprocess
from typing import Any


COMMAND_TIMEOUT_SECONDS = 3


def _run_systemctl(args: list[str]) -> subprocess.CompletedProcess[str] | None:
    """Run a bounded systemctl command without requesting privileges."""

    try:
        return subprocess.run(
            ["systemctl", *args],
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None


def _failed_units(user: bool = False) -> dict[str, Any]:
    """Collect failed systemd units."""

    args = ["--failed", "--no-legend", "--plain"]

    if user:
        args.insert(0, "--user")

    result = _run_systemctl(args)

    if result is None:
        return {
            "available": False,
            "units": [],
        }

    if result.returncode != 0:
        return {
            "available": False,
            "units": [],
        }

    units = []

    for line in result.stdout.splitlines():
        line = line.strip()

        if not line:
            continue

        # systemctl output begins with the unit name.
        unit_name = line.split()[0]

        units.append(unit_name)

    return {
        "available": True,
        "count": len(units),
        "units": units,
    }


def collect_system_health() -> dict[str, Any]:
    """Collect deterministic systemd health information."""

    state_result = _run_systemctl(["is-system-running"])

    if state_result is None:
        system_state = {
            "available": False,
            "state": None,
            "healthy": None,
        }
    else:
        state = state_result.stdout.strip() or state_result.stderr.strip()

        system_state = {
            "available": bool(state),
            "state": state or None,
            "healthy": state == "running" if state else None,
        }

    return {
        "systemd": {
            "system_state": system_state,
            "failed_system_units": _failed_units(user=False),
            "failed_user_units": _failed_units(user=True),
        }
    }
