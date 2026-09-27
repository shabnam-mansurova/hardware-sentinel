"""Disk and network I/O telemetry for Hardware Sentinel."""

from __future__ import annotations

from typing import Any

import psutil


def collect_disk_io() -> dict[str, Any]:
    """Collect cumulative disk I/O counters."""

    try:
        counters = psutil.disk_io_counters()
    except (AttributeError, OSError):
        counters = None

    if counters is None:
        return {
            "available": False,
            "reason": "disk_io_unavailable",
        }

    return {
        "available": True,
        "read_bytes": counters.read_bytes,
        "write_bytes": counters.write_bytes,
        "read_count": counters.read_count,
        "write_count": counters.write_count,
        "read_time_ms": counters.read_time,
        "write_time_ms": counters.write_time,
    }


def collect_network_io() -> dict[str, Any]:
    """Collect cumulative network I/O counters."""

    try:
        counters = psutil.net_io_counters()
    except (AttributeError, OSError):
        counters = None

    if counters is None:
        return {
            "available": False,
            "reason": "network_io_unavailable",
        }

    return {
        "available": True,
        "bytes_sent": counters.bytes_sent,
        "bytes_received": counters.bytes_recv,
        "packets_sent": counters.packets_sent,
        "packets_received": counters.packets_recv,
        "errors_in": counters.errin,
        "errors_out": counters.errout,
        "dropped_in": counters.dropin,
        "dropped_out": counters.dropout,
    }


def collect_io() -> dict[str, Any]:
    """Collect disk and network I/O telemetry."""

    return {
        "disk": collect_disk_io(),
        "network": collect_network_io(),
    }


def calculate_io_rates(
    previous: dict[str, Any],
    current: dict[str, Any],
    elapsed_seconds: float,
) -> dict[str, Any]:
    """Calculate disk and network I/O rates between two snapshots."""

    if elapsed_seconds <= 0:
        raise ValueError("elapsed_seconds must be greater than zero")

    result: dict[str, Any] = {
        "disk": {"available": False},
        "network": {"available": False},
    }

    previous_disk = previous.get("disk", {})
    current_disk = current.get("disk", {})

    if (
        previous_disk.get("available")
        and current_disk.get("available")
    ):
        read_delta = max(
            0,
            current_disk["read_bytes"] - previous_disk["read_bytes"],
        )
        write_delta = max(
            0,
            current_disk["write_bytes"] - previous_disk["write_bytes"],
        )

        result["disk"] = {
            "available": True,
            "read_bytes_per_sec": round(
                read_delta / elapsed_seconds, 2
            ),
            "write_bytes_per_sec": round(
                write_delta / elapsed_seconds, 2
            ),
        }

    previous_network = previous.get("network", {})
    current_network = current.get("network", {})

    if (
        previous_network.get("available")
        and current_network.get("available")
    ):
        sent_delta = max(
            0,
            current_network["bytes_sent"]
            - previous_network["bytes_sent"],
        )
        received_delta = max(
            0,
            current_network["bytes_received"]
            - previous_network["bytes_received"],
        )

        result["network"] = {
            "available": True,
            "sent_bytes_per_sec": round(
                sent_delta / elapsed_seconds, 2
            ),
            "received_bytes_per_sec": round(
                received_delta / elapsed_seconds, 2
            ),
        }

    return result
