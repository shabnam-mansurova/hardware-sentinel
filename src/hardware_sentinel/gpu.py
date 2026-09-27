"""Optional Intel GPU telemetry collection."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any


DRM_PATH = Path("/sys/class/drm")


@lru_cache(maxsize=1)
def _detect_intel_gpu() -> bool:
    """Detect whether an Intel i915 GPU is present."""

    if not DRM_PATH.exists():
        return False

    for card in DRM_PATH.glob("card[0-9]"):
        driver = card / "device" / "driver"

        try:
            if driver.resolve().name == "i915":
                return True
        except (FileNotFoundError, OSError):
            continue

    return False


@lru_cache(maxsize=1)
def _gpu_capability() -> dict[str, Any]:
    """Determine whether detailed Intel GPU metrics are accessible."""

    if not _detect_intel_gpu():
        return {
            "available": False,
            "vendor": None,
            "metrics_available": False,
            "reason": "no_supported_gpu",
        }

    base = {
        "available": True,
        "vendor": "intel",
        "driver": "i915",
        "metrics_available": False,
    }

    executable = shutil.which("intel_gpu_top")

    if executable is None:
        return {
            **base,
            "reason": "intel_gpu_top_not_installed",
        }

    try:
        process = subprocess.run(
            [executable, "-J"],
            capture_output=True,
            text=True,
            timeout=1.5,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""

        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")

        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")

        if stdout.strip():
            return {
                **base,
                "metrics_available": True,
                "reason": None,
            }

        if "Permission denied" in stderr or "CAP_PERFMON" in stderr:
            return {
                **base,
                "reason": "permission_denied",
            }

        return {
            **base,
            "reason": "metrics_unavailable",
        }

    stderr = process.stderr or ""

    if "Permission denied" in stderr or "CAP_PERFMON" in stderr:
        return {
            **base,
            "reason": "permission_denied",
        }

    if process.stdout.strip():
        return {
            **base,
            "metrics_available": True,
            "reason": None,
        }

    return {
        **base,
        "reason": "metrics_unavailable",
    }


def collect_gpu() -> dict[str, Any]:
    """Collect Intel GPU telemetry when available and permitted."""

    capability = dict(_gpu_capability())

    if not capability.get("metrics_available"):
        return capability

    executable = shutil.which("intel_gpu_top")

    if executable is None:
        return {
            **capability,
            "metrics_available": False,
            "reason": "intel_gpu_top_not_installed",
        }

    try:
        process = subprocess.run(
            [executable, "-J"],
            capture_output=True,
            text=True,
            timeout=1.5,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""

        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")

        if stdout.strip():
            return _parse_gpu_output(stdout, capability)

        return {
            **capability,
            "metrics_available": False,
            "reason": "metrics_unavailable",
        }

    if process.stdout.strip():
        return _parse_gpu_output(process.stdout, capability)

    return {
        **capability,
        "metrics_available": False,
        "reason": "metrics_unavailable",
    }


def _parse_gpu_output(
    output: str,
    base_result: dict[str, Any],
) -> dict[str, Any]:
    """Parse intel_gpu_top JSON output."""

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return {
            **base_result,
            "metrics_available": False,
            "reason": "invalid_gpu_output",
        }

    if isinstance(data, list):
        samples = [item for item in data if isinstance(item, dict)]

        if not samples:
            return {
                **base_result,
                "metrics_available": False,
                "reason": "no_gpu_samples",
            }

        sample = samples[-1]

    elif isinstance(data, dict):
        sample = data

    else:
        return {
            **base_result,
            "metrics_available": False,
            "reason": "invalid_gpu_output",
        }

    engines = sample.get("engines", {})

    return {
        **base_result,
        "metrics_available": True,
        "reason": None,
        "frequency_mhz": sample.get("frequency", {}).get("actual"),
        "rc6_percent": sample.get("rc6", {}).get("value"),
        "power_watts": sample.get("power", {}).get("GPU"),
        "engines": {
            name: values.get("busy")
            for name, values in engines.items()
            if isinstance(values, dict)
        },
    }
