"""Continuous telemetry recording for Hardware Sentinel."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from hardware_sentinel.io_metrics import calculate_io_rates
from hardware_sentinel.telemetry import collect_snapshot


DATA_DIR = Path("data")



def _format_rate(bytes_per_second: float) -> str:
    """Format a byte-per-second rate using a readable unit."""

    value = float(bytes_per_second)

    for unit in ("B/s", "KB/s", "MB/s"):
        if value < 1024.0:
            return f"{value:.1f} {unit}"
        value /= 1024.0

    return f"{value:.1f} GB/s"

def monitor(
    interval: float = 5.0,
    duration: float | None = None,
) -> Path:
    """Record telemetry snapshots as JSON Lines."""

    if interval <= 0:
        raise ValueError("interval must be greater than zero")

    if duration is not None and duration <= 0:
        raise ValueError("duration must be greater than zero")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_path = DATA_DIR / f"session_{timestamp}.jsonl"

    start = time.monotonic()
    next_sample = start
    samples = 0
    previous_io = None
    previous_io_time = None

    print("Hardware Sentinel monitoring started")
    print(f"Interval: {interval:.1f}s")
    print(f"Output:   {output_path}")
    print("Press Ctrl+C to stop.\n")

    try:
        with output_path.open("a", encoding="utf-8") as file:
            while True:
                now = time.monotonic()

                if duration is not None and now - start >= duration:
                    break

                if now < next_sample:
                    time.sleep(next_sample - now)

                snapshot = collect_snapshot()
                sample_time = time.monotonic()

                current_io = snapshot.get("io")

                if (
                    previous_io is not None
                    and previous_io_time is not None
                    and current_io is not None
                ):
                    elapsed = sample_time - previous_io_time
                    snapshot["io_rates"] = calculate_io_rates(
                        previous_io,
                        current_io,
                        elapsed,
                    )
                else:
                    snapshot["io_rates"] = {
                        "disk": {"available": False},
                        "network": {"available": False},
                    }

                previous_io = current_io
                previous_io_time = sample_time

                file.write(json.dumps(snapshot) + "\n")
                file.flush()

                samples += 1

                cpu = snapshot["cpu"]["total_percent"]
                memory = snapshot["memory"]["percent"]
                workloads = snapshot["workloads"]["active_categories"]
                io_rates = snapshot["io_rates"]

                disk_rates = io_rates["disk"]
                network_rates = io_rates["network"]

                if disk_rates.get("available"):
                    disk_write = _format_rate(
                        disk_rates["write_bytes_per_sec"]
                    )
                else:
                    disk_write = "n/a"

                if network_rates.get("available"):
                    net_down = _format_rate(
                        network_rates["received_bytes_per_sec"]
                    )
                    net_up = _format_rate(
                        network_rates["sent_bytes_per_sec"]
                    )
                else:
                    net_down = "n/a"
                    net_up = "n/a"

                print(
                    f"[{samples:04d}] "
                    f"CPU {cpu:5.1f}% | "
                    f"RAM {memory:5.1f}% | "
                    f"Disk W {disk_write} | "
                    f"Net ↓ {net_down} ↑ {net_up} | "
                    f"workloads: {', '.join(workloads) or 'none'}"
                )

                next_sample += interval

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

    print(f"Samples collected: {samples}")
    print(f"Saved locally to: {output_path}")

    return output_path
