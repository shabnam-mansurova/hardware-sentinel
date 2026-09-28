"""End-to-end deterministic diagnosis for Hardware Sentinel."""

from __future__ import annotations

from typing import Any

from hardware_sentinel.analyzer import analyze_snapshot
from hardware_sentinel.diagnostics import create_incidents
from hardware_sentinel.session import Session
from hardware_sentinel.telemetry import collect_snapshot


def diagnose_current_state() -> dict[str, Any]:
    """Collect, analyze, and structure the current machine state."""

    session = Session()
    snapshot = collect_snapshot()
    analysis = analyze_snapshot(snapshot)

    incidents = create_incidents(
        analysis,
        session_id=session.session_id,
        detected_at=snapshot["timestamp_utc"],
    )

    return {
        "session": session.to_dict(),
        "machine": snapshot["system"],
        "snapshot_timestamp_utc": snapshot["timestamp_utc"],
        "analysis": analysis,
        "incidents": [
            incident.to_dict()
            for incident in incidents
        ],
    }
