"""Privacy-conscious process aggregation and workload detection."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import psutil


CATEGORIES = {
    "browser": {
        "brave", "chrome", "chromium", "firefox"
    },
    "gaming": {
        "steam", "steamwebhelper", "gamescope"
    },
    "local_llm": {
        "ollama", "alpaca"
    },
    "development": {
        "code", "code-insiders", "python", "python3",
        "java", "javac", "git"
    },
    "productivity": {
        "libreoffice", "soffice"
    },
}


def _category_for(name: str) -> str:
    normalized = name.lower()

    for category, process_names in CATEGORIES.items():
        if normalized in process_names:
            return category

    return "other"


def collect_process_summary(limit: int = 10) -> dict[str, Any]:
    """Aggregate running processes without recording arguments or content."""

    categories: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {
            "process_count": 0,
            "memory_percent": 0.0,
        }
    )

    processes: list[dict[str, Any]] = []

    for proc in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            info = proc.info
            name = info["name"] or "unknown"
            memory = float(info["memory_percent"] or 0.0)

            category = _category_for(name)

            categories[category]["process_count"] += 1
            categories[category]["memory_percent"] += memory

            processes.append(
                {
                    "name": name,
                    "category": category,
                    "memory_percent": round(memory, 2),
                }
            )

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    for values in categories.values():
        values["memory_percent"] = round(
            float(values["memory_percent"]), 2
        )

    top_processes = sorted(
        processes,
        key=lambda item: item["memory_percent"],
        reverse=True,
    )[:limit]

    active_categories = [
        category
        for category, values in categories.items()
        if category != "other" and values["process_count"] > 0
    ]

    return {
        "active_categories": sorted(active_categories),
        "categories": dict(categories),
        "top_processes": top_processes,
    }
