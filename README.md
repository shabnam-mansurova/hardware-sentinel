# Hardware Sentinel

A privacy-first local Linux system agent for hardware monitoring, diagnostics, AI-assisted troubleshooting, and controlled remediation.

## Goal

Hardware Sentinel aims to act as an intelligent interface between the user, operating system, software workloads, and hardware.

It collects local system telemetry, detects abnormal conditions, investigates relevant processes and system evidence, and builds structured diagnostic context. A local LLM can then reason over that evidence to explain likely causes, propose troubleshooting steps, and generate reports.

The long-term goal is not only to detect problems, but also to safely resolve approved issues and verify whether the corrective action worked.

## Core Principles

- **Local-first:** telemetry and diagnostic evidence remain on the machine.
- **Privacy-conscious:** collect system metadata without unnecessarily capturing user content.
- **Deterministic facts:** measurements and warning conditions come from software collectors and analyzers, not from the LLM.
- **Evidence-grounded AI:** the local LLM reasons over collected evidence while hypotheses remain distinguishable from measured facts.
- **Controlled remediation:** potentially disruptive actions require explicit authorization.
- **Verification:** corrective actions are followed by new measurements to determine whether the problem improved.
- **Low overhead:** monitoring should not itself become a significant system workload.

## Architecture

Hardware Sentinel separates system observation, deterministic analysis, AI reasoning, and remediation.

See `docs/ARCHITECTURE.md` for the detailed architecture and development phases.

## Current Capabilities

- CPU utilization and per-core measurements
- Memory and swap monitoring
- Disk capacity monitoring
- Hardware temperature sensors
- Battery information
- Process aggregation
- Workload categorization
- Optional Intel GPU telemetry
- Graceful GPU permission handling
- Continuous local JSONL telemetry recording
- Deterministic resource and thermal warnings
- Automated unit tests

## Planned Capabilities

- Disk I/O and network telemetry
- systemd and service-health monitoring
- Privacy-conscious system-log evidence
- Historical machine baselines
- Anomaly detection
- Structured incident records
- Evidence-grounded local LLM investigation
- Interactive troubleshooting
- Controlled remediation
- Post-remediation verification
- Incident and system-health reports

## Target CLI

- `sentinel status`
- `sentinel monitor`
- `sentinel diagnose`
- `sentinel fix`
- `sentinel report`
- `sentinel history`
- `sentinel ask "<question>"`

## Local AI

The planned AI investigator runs locally through Ollama.

An early Llama 3.2 1B prototype demonstrated an important design constraint: even with deterministic input and temperature 0, a small LLM may introduce unsupported qualitative interpretations.

Hardware Sentinel therefore treats LLM output as reasoning rather than authoritative telemetry. Measurements and system state remain controlled by deterministic components.

The experimental prototype is preserved under `experiments/`.

## Privacy

Normal monitoring is designed to avoid collecting user content such as:

- browser URLs
- document contents
- terminal command history
- LLM prompts
- clipboard contents
- keystrokes
- passwords, tokens, and secrets

Only system metadata necessary for monitoring and diagnostics should be collected.

## Status

Active development.

The current focus is **Phase 1: Observability Foundation**.
