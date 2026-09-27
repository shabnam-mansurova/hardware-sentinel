# Hardware Sentinel Architecture

## Project Goal

Hardware Sentinel is a privacy-first local Linux system agent that observes
hardware and software state, detects abnormal conditions, investigates likely
causes using telemetry and system evidence, explains its findings with a local
LLM, recommends corrective actions, and can execute approved remediation steps
while verifying whether the issue was resolved.

The project is designed to operate locally. Raw telemetry, diagnostic evidence,
logs, and system history should not require transmission to a cloud service.

## Core Principle

Hardware Sentinel separates facts, reasoning, and actions.

### Facts

Facts come from deterministic collectors and analyzers:

- CPU utilization
- memory and swap utilization
- temperatures
- disk capacity and I/O
- GPU state
- battery and power state
- network activity
- processes
- workload categories
- service state
- relevant system logs

The LLM is not allowed to create measurements.

### Analysis

Deterministic analysis identifies measurable conditions such as:

- sustained CPU pressure
- memory pressure
- swap pressure
- low disk space
- thermal warnings
- failed services
- abnormal resource changes
- deviations from learned machine baselines

### Investigation

When an abnormal condition is detected, Hardware Sentinel collects additional
evidence relevant to that condition.

Examples include:

- process resource consumption
- systemd service state
- journal entries
- kernel messages
- historical telemetry
- workload context

### AI Reasoning

A local LLM receives structured evidence and may:

- explain observations
- correlate evidence
- propose hypotheses
- suggest additional diagnostic steps
- construct remediation plans
- generate human-readable reports

LLM hypotheses must remain distinguishable from deterministic facts.

### Remediation

Corrective actions pass through a controlled action layer.

Actions have explicit metadata such as:

- risk level
- whether confirmation is required
- whether root privileges are required
- reversibility
- verification procedure

Potentially disruptive actions require explicit user approval.

### Verification

After remediation, Hardware Sentinel collects telemetry again and determines
whether the observed condition improved, remained unchanged, or worsened.

## High-Level Pipeline

    Hardware / Linux
          |
          v
    Telemetry Collectors
          |
          v
    Local Structured Storage
          |
          v
    Deterministic Analysis
          |
          v
    Diagnostic Evidence Collection
          |
          v
    Local LLM Investigator
          |
          v
    Safety / Action Policy
          |
          v
    Remediation
          |
          v
    Verification
          |
          v
    Incident Report

## Privacy

Hardware Sentinel follows data minimization.

It should not collect application content unless explicitly required and
approved. In particular, normal telemetry collection should avoid storing:

- browser URLs
- document contents
- terminal command history
- LLM prompts
- clipboard contents
- keystrokes
- passwords, tokens, or secrets

Process and system metadata should be limited to information necessary for
resource analysis and diagnostics.

## Target CLI

    sentinel status
    sentinel monitor
    sentinel diagnose
    sentinel fix
    sentinel report
    sentinel history
    sentinel ask "<question>"

## Development Phases

### Phase 1 — Observability Foundation

Collect reliable local telemetry, process/workload information, system health,
logs, and structured incident evidence.

### Phase 2 — History and Baselines

Build local historical statistics, workload profiles, trends, and anomaly
detection.

### Phase 3 — Diagnostic Engine

Correlate abnormal conditions with processes, services, logs, and historical
context.

### Phase 4 — Local AI Investigator

Use a local LLM for evidence-grounded investigation, hypotheses, explanations,
and remediation planning.

### Phase 5 — Controlled Remediation

Implement an allowlisted action system with risk levels, confirmation,
execution, and post-action verification.

### Phase 6 — Reporting and UX

Provide useful incident reports, history, explanations, and a polished CLI.

### Phase 7 — Testing and Portfolio Release

Add comprehensive tests, installation packaging, documentation, examples,
architecture diagrams, and reproducible demonstrations.

---

## Internationalization Boundary

Hardware Sentinel Core is language-neutral.

Telemetry, incident identifiers, evidence structures, diagnostic rules, safety
policy, remediation permissions, action execution, and verification results
must not depend on the user's presentation language.

Localization is divided into two distinct mechanisms:

1. **Deterministic localization**
   - GUI strings
   - warnings and notifications
   - incident and severity names
   - action descriptions
   - approval dialogs
   - deterministic reports
   - verification results

2. **Local AI language generation**
   - diagnostic explanations
   - hypotheses
   - conversational investigation

Deterministic information is translated through local resources such as GNU
gettext catalogs. Measurements and other facts are inserted from structured
Sentinel data and must not be generated by the language model.

The local LLM receives structured facts and evidence but does not become the
source of those facts. Its multilingual output remains explanatory and must not
alter incident state, severity, safety policy, or action permissions.

GUI localization and AI-language support are therefore evaluated separately.

A locale may be fully supported by the interface while AI explanations for that
locale remain experimental or fall back to English.

Untrusted evidence remains untrusted regardless of language. Journal messages,
process-derived text, logs, and other external evidence must never become
instructions to the AI system or remediation layer merely because they appear
in a supported language.

Localization must not introduce a mandatory cloud dependency. Translation
resources and supported AI inference are intended to operate locally.
