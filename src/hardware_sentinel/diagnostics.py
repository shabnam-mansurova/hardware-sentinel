"""Deterministic incident creation and evidence collection."""

from __future__ import annotations

from typing import Any

from hardware_sentinel.incidents import Evidence, Incident, UNTRUSTED
from hardware_sentinel.journal import collect_journal_evidence


WARNING_TYPES = {
    "high_cpu_usage": "cpu_pressure",
    "high_memory_usage": "memory_pressure",
    "high_swap_usage": "swap_pressure",
    "low_disk_space": "disk_space_pressure",
    "thermal_warning": "thermal_pressure",
}


def _facts_for_warning(
    warning: str,
    analysis: dict[str, Any],
) -> dict[str, Any]:
    """Extract deterministic facts relevant to one warning."""

    metrics = analysis.get("metrics", {})

    if warning == "high_cpu_usage":
        return {"cpu_percent": metrics.get("cpu_percent")}

    if warning == "high_memory_usage":
        return {"memory_percent": metrics.get("memory_percent")}

    if warning == "high_swap_usage":
        return {"swap_percent": metrics.get("swap_percent")}

    if warning == "low_disk_space":
        return {"disk_percent": metrics.get("disk_percent")}

    if warning == "thermal_warning":
        return {
            "thermal_warnings": analysis.get("thermal_warnings", []),
        }

    return {}


def _severity_for_warning(
    warning: str,
    analysis: dict[str, Any],
) -> str:
    """Determine severity from deterministic analyzer output."""

    if warning == "thermal_warning":
        thermal_warnings = analysis.get("thermal_warnings", [])

        if any(
            item.get("state") == "critical"
            for item in thermal_warnings
        ):
            return "critical"

    return "warning"


def _journal_evidence() -> Evidence:
    """Collect bounded journal evidence while preserving its trust boundary."""

    journal = collect_journal_evidence()

    return Evidence(
        source="systemd_journal",
        trust=UNTRUSTED,
        data=journal,
    )


def create_incidents(
    analysis: dict[str, Any],
    *,
    session_id: str,
    detected_at: str,
    collect_evidence: bool = True,
) -> list[Incident]:
    """Convert deterministic warnings into structured incidents."""

    incidents: list[Incident] = []

    for warning in analysis.get("warnings", []):
        incident_type = WARNING_TYPES.get(warning)

        if incident_type is None:
            continue

        incident = Incident(
            incident_type=incident_type,
            severity=_severity_for_warning(warning, analysis),
            facts=_facts_for_warning(warning, analysis),
            session_id=session_id,
            detected_at=detected_at,
        )

        if collect_evidence:
            incident.add_evidence(_journal_evidence())

        incidents.append(incident)

    return incidents
