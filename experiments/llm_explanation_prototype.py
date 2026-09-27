"""Local LLM explanation layer for Hardware Sentinel."""

from __future__ import annotations

from typing import Any

import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2:1b"


class LLMUnavailableError(RuntimeError):
    """Raised when the local Ollama service cannot be reached."""


def _build_findings(
    analysis: dict[str, Any],
    workloads: dict[str, Any] | None = None,
) -> list[str]:
    """Convert deterministic analysis into authoritative textual findings."""

    metrics = analysis["metrics"]
    warnings = analysis.get("warnings", [])

    findings = [
        f"Overall status: {analysis['status']}.",
    ]

    if warnings:
        findings.append(
            "Detected warning conditions: "
            + ", ".join(warnings)
            + "."
        )
    else:
        findings.append("No warning conditions were detected.")

    findings.extend(
        [
            f"CPU usage measured {metrics['cpu_percent']}%.",
            f"Memory usage measured {metrics['memory_percent']}%.",
            f"Swap usage measured {metrics['swap_percent']}%.",
            f"Disk usage measured {metrics['disk_percent']}%.",
        ]
    )

    thermal_warnings = analysis.get("thermal_warnings", [])

    for warning in thermal_warnings:
        findings.append(
            "Thermal warning: "
            f"{warning.get('sensor')} "
            f"{warning.get('label') or ''} "
            f"is {warning.get('state')} at "
            f"{warning.get('current_c')}°C with a reported threshold of "
            f"{warning.get('threshold_c')}°C."
        )

    if workloads:
        active = workloads.get("active_categories", [])

        if active:
            findings.append(
                "Detected active workload categories: "
                + ", ".join(active)
                + "."
            )

    return findings


def explain_analysis(
    analysis: dict[str, Any],
    workloads: dict[str, Any] | None = None,
) -> str:
    """Rewrite deterministic findings using a local LLM."""

    findings = _build_findings(analysis, workloads)

    findings_text = "\n".join(
        f"- {finding}" for finding in findings
    )

    prompt = f"""
You are the prose layer of Hardware Sentinel.

The statements below are authoritative findings produced by deterministic
software. Your only task is to rewrite them into concise, readable prose.

STRICT RULES:
- Preserve the meaning of the findings.
- Do not interpret or evaluate numeric values.
- Do not add adjectives such as high, low, elevated, excessive, safe,
  unsafe, healthy, unhealthy, hot, or cold unless they already appear
  in the findings.
- Do not invent causes, thresholds, warnings, diagnoses, or recommendations.
- Do not contradict the stated overall status.
- Do not infer anything from workload categories.
- Use only information explicitly contained in the findings.
- Write 2-4 sentences.

AUTHORITATIVE FINDINGS:
{findings_text}
""".strip()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0,
                },
            },
            timeout=60,
        )

        response.raise_for_status()

    except requests.RequestException as exc:
        raise LLMUnavailableError(
            "Local Ollama service is unavailable."
        ) from exc

    try:
        data = response.json()
    except (ValueError, requests.JSONDecodeError) as exc:
        raise LLMUnavailableError(
            "Ollama returned an invalid response."
        ) from exc

    explanation = data.get("response")

    if not isinstance(explanation, str) or not explanation.strip():
        raise LLMUnavailableError(
            "Ollama returned no usable explanation."
        )

    return explanation.strip()
