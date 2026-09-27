"""Continuous telemetry recording for Hardware Sentinel."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from hardware_sentinel.telemetry import collect_snapshot


DATA_DIR = Path("data")


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

                file.write(json.dumps(snapshot) + "\n")
                file.flush()

                samples += 1

                cpu = snapshot["cpu"]["total_percent"]
                memory = snapshot["memory"]["percent"]
                workloads = snapshot["workloads"]["active_categories"]

                print(
                    f"[{samples:04d}] "
                    f"CPU {cpu:5.1f}% | "
                    f"RAM {memory:5.1f}% | "
                    f"workloads: {', '.join(workloads) or 'none'}"
                )

                next_sample += interval

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

    print(f"Samples collected: {samples}")
    print(f"Saved locally to: {output_path}")

    return output_path
