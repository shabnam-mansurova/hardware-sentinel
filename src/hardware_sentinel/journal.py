"""Bounded journal evidence collection for Hardware Sentinel."""

from __future__ import annotations

import json
import subprocess
from typing import Any


COMMAND_TIMEOUT_SECONDS = 5
DEFAULT_LINES = 20
MAX_LINES = 100

# Journal messages are external evidence. They may contain malformed,
# misleading, or attacker-controlled text and must never be treated as
# instructions to Hardware Sentinel or its LLM.
TRUST_CLASSIFICATION = "untrusted"


def _run_journalctl(args: list[str]) -> subprocess.CompletedProcess[str] | None:
    """Run journalctl with a bounded execution time and no privileges."""

    try:
        return subprocess.run(
            ["journalctl", *args],
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None


def _parse_entry(line: str) -> dict[str, Any] | None:
    """Convert one journalctl JSON record into minimal diagnostic evidence."""

    try:
        raw = json.loads(line)
    except (json.JSONDecodeError, TypeError):
        return None

    message = raw.get("MESSAGE")

    if not isinstance(message, str):
        message = str(message) if message is not None else ""

    return {
        "source": "systemd_journal",
        "trust": TRUST_CLASSIFICATION,
        "timestamp_us": raw.get("__REALTIME_TIMESTAMP"),
        "unit": raw.get("_SYSTEMD_UNIT") or raw.get("_SYSTEMD_USER_UNIT"),
        "identifier": raw.get("SYSLOG_IDENTIFIER"),
        "priority": raw.get("PRIORITY"),
        "message": message,
    }


def collect_journal_evidence(
    *,
    since: str = "10 minutes ago",
    priority: str | None = "warning",
    unit: str | None = None,
    user: bool = False,
    lines: int = DEFAULT_LINES,
) -> dict[str, Any]:
    """Collect a bounded set of recent journal entries."""

    lines = max(1, min(lines, MAX_LINES))

    args = [
        "--since",
        since,
        "--no-pager",
        "--output=json",
        f"--lines={lines}",
    ]

    if priority:
        args.extend(["--priority", priority])

    if user:
        args.append("--user")

    if unit:
        args.extend(["--unit", unit])

    result = _run_journalctl(args)

    if result is None:
        return {
            "available": False,
            "trust": TRUST_CLASSIFICATION,
            "entries": [],
            "reason": "journalctl_unavailable",
        }

    if result.returncode != 0:
        return {
            "available": False,
            "trust": TRUST_CLASSIFICATION,
            "entries": [],
            "reason": "journalctl_failed",
        }

    entries = []

    for line in result.stdout.splitlines():
        if entry := _parse_entry(line):
            entries.append(entry)

    return {
        "available": True,
        "trust": TRUST_CLASSIFICATION,
        "count": len(entries),
        "entries": entries,
    }
