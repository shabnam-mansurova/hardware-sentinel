"""Deterministic hardware-state analysis."""

from __future__ import annotations

from typing import Any


def analyze_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Analyze a telemetry snapshot without using an LLM."""

    cpu_percent = float(snapshot["cpu"]["total_percent"])
    memory_percent = float(snapshot["memory"]["percent"])
    swap_percent = float(snapshot["swap"]["percent"])
    disk_percent = float(snapshot["disk"]["percent"])

    warnings: list[str] = []

    if cpu_percent >= 90:
        warnings.append("high_cpu_usage")

    if memory_percent >= 90:
        warnings.append("high_memory_usage")

    if swap_percent >= 50:
        warnings.append("high_swap_usage")

    if disk_percent >= 90:
        warnings.append("low_disk_space")

    thermal_warnings: list[dict[str, Any]] = []

    for sensor_name, entries in snapshot.get("temperatures", {}).items():
        for entry in entries:
            current = entry.get("current_c")
            high = entry.get("high_c")
            critical = entry.get("critical_c")

            if current is None:
                continue

            if critical is not None and current >= critical:
                thermal_warnings.append(
                    {
                        "sensor": sensor_name,
                        "label": entry.get("label"),
                        "state": "critical",
                        "current_c": current,
                        "threshold_c": critical,
                    }
                )
            elif high is not None and current >= high:
                thermal_warnings.append(
                    {
                        "sensor": sensor_name,
                        "label": entry.get("label"),
                        "state": "high",
                        "current_c": current,
                        "threshold_c": high,
                    }
                )

    if thermal_warnings:
        warnings.append("thermal_warning")

    return {
        "status": "warning" if warnings else "normal",
        "warnings": warnings,
        "thermal_warnings": thermal_warnings,
        "metrics": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent,
            "swap_percent": swap_percent,
            "disk_percent": disk_percent,
        },
    }
