"""Hardware telemetry collection for Hardware Sentinel."""

from __future__ import annotations

import os
import platform
import socket
from datetime import datetime, timezone
from typing import Any

import psutil

from hardware_sentinel.workloads import collect_process_summary


def _temperatures() -> dict[str, list[dict[str, Any]]]:
    """Return available temperature sensors."""
    try:
        sensors = psutil.sensors_temperatures()
    except (AttributeError, OSError):
        return {}

    result: dict[str, list[dict[str, Any]]] = {}

    for sensor_name, entries in sensors.items():
        result[sensor_name] = [
            {
                "label": entry.label or None,
                "current_c": entry.current,
                "high_c": entry.high,
                "critical_c": entry.critical,
            }
            for entry in entries
        ]

    return result


def _battery() -> dict[str, Any] | None:
    """Return battery information when available."""
    try:
        battery = psutil.sensors_battery()
    except (AttributeError, OSError):
        return None

    if battery is None:
        return None

    return {
        "percent": battery.percent,
        "plugged_in": battery.power_plugged,
        "seconds_left": battery.secsleft,
    }


def collect_snapshot() -> dict[str, Any]:
    """Collect one deterministic hardware telemetry snapshot."""

    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage("/")
    cpu_per_core = psutil.cpu_percent(interval=1.0, percpu=True)

    try:
        load_1, load_5, load_15 = os.getloadavg()
    except OSError:
        load_1 = load_5 = load_15 = None

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "system": {
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "kernel": platform.release(),
            "architecture": platform.machine(),
            "cpu_logical_count": psutil.cpu_count(logical=True),
            "cpu_physical_count": psutil.cpu_count(logical=False),
        },
        "cpu": {
            "total_percent": round(sum(cpu_per_core) / len(cpu_per_core), 2)
            if cpu_per_core
            else 0.0,
            "per_core_percent": cpu_per_core,
            "load_average": {
                "1_min": load_1,
                "5_min": load_5,
                "15_min": load_15,
            },
        },
        "memory": {
            "total_gb": round(memory.total / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "percent": memory.percent,
        },
        "swap": {
            "total_gb": round(swap.total / (1024**3), 2),
            "used_gb": round(swap.used / (1024**3), 2),
            "percent": swap.percent,
        },
        "disk": {
            "total_gb": round(disk.total / (1024**3), 2),
            "used_gb": round(disk.used / (1024**3), 2),
            "free_gb": round(disk.free / (1024**3), 2),
            "percent": disk.percent,
        },
        "temperatures": _temperatures(),
        "battery": _battery(),
        "workloads": collect_process_summary(),
    }
