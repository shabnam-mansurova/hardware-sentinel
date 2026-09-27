"""Command-line interface for Hardware Sentinel."""

from __future__ import annotations

import argparse
import json

from hardware_sentinel.analyzer import analyze_snapshot
from hardware_sentinel.monitor import monitor
from hardware_sentinel.telemetry import collect_snapshot


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sentinel",
        description="Local hardware monitoring and workload analysis.",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "status",
        help="Show one hardware telemetry snapshot.",
    )

    subparsers.add_parser(
        "analyze",
        help="Analyze the current hardware state.",
    )

    monitor_parser = subparsers.add_parser(
        "monitor",
        help="Continuously record hardware telemetry.",
    )

    monitor_parser.add_argument(
        "--interval",
        type=float,
        default=5.0,
        help="Seconds between samples (default: 5).",
    )

    monitor_parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Optional monitoring duration in seconds.",
    )

    args = parser.parse_args()

    if args.command == "monitor":
        monitor(
            interval=args.interval,
            duration=args.duration,
        )

    elif args.command == "analyze":
        snapshot = collect_snapshot()
        analysis = analyze_snapshot(snapshot)
        print(json.dumps(analysis, indent=2))

    else:
        snapshot = collect_snapshot()
        print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()
