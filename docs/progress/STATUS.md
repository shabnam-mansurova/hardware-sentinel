# Hardware Sentinel — Project Status

Last updated: 2026-09-28

## Current Phase

**Phase 1 — Observability Foundation**

Status: **Complete**

Completion: **100%**

## Phase 1 Objective

Build a reliable, privacy-conscious foundation for observing Linux hardware and
software state and producing deterministic, structured evidence for later
diagnostic investigation.

## Completed

- [x] CPU telemetry
- [x] Per-core CPU telemetry
- [x] Memory telemetry
- [x] Swap telemetry
- [x] Disk-capacity telemetry
- [x] Disk I/O counters
- [x] Network I/O counters
- [x] Disk/network rate calculation
- [x] Human-readable I/O rates
- [x] Temperature monitoring
- [x] Battery monitoring
- [x] Process aggregation
- [x] Workload categorization
- [x] Intel GPU detection
- [x] Graceful GPU permission handling
- [x] Continuous local JSONL telemetry
- [x] Deterministic resource and thermal warnings
- [x] systemd system-state monitoring
- [x] Failed system-unit monitoring
- [x] Failed user-unit monitoring
- [x] Bounded systemd journal evidence collection
- [x] Machine metadata
- [x] Session identity and timestamps
- [x] Structured Incident model
- [x] Structured Evidence model
- [x] Deterministic anomaly-to-incident conversion
- [x] Incident-triggered bounded evidence collection
- [x] Explicit trusted/untrusted evidence classification
- [x] Instruction-like journal text preserved as untrusted data
- [x] Graceful journal and system-service failure handling
- [x] Integration and edge-case tests
- [x] End-to-end deterministic analysis CLI
- [x] Live Fedora validation
- [x] Phase 1 documentation
- [x] Phase 1 completion review

## Phase 1 Validation

Automated test suite:

    PYTHONPATH=src python -m unittest discover -v

Result at completion:

    Ran 45 tests
    OK

Live Fedora validation:

    PYTHONPATH=src python -m hardware_sentinel analyze

Validated end-to-end flow:

    telemetry snapshot
          ↓
    deterministic analysis
          ↓
    structured incident creation
          ↓
    bounded evidence collection
          ↓
    structured Incident / Evidence output

A normal live Fedora run produced a valid session, machine metadata,
deterministic metrics, and an empty incident list because no configured
threshold was crossed.

## Security Boundary

Hardware Sentinel distinguishes four layers.

**Facts**

Deterministic measurements and system state collected by software.

**Evidence**

Diagnostic material associated with an incident. External material such as
systemd journal messages is explicitly classified as untrusted.

**Reasoning**

Future diagnostic hypotheses and explanations. Reasoning must remain
distinguishable from facts and evidence.

**Actions**

Future remediation operations controlled by an explicit safety and
authorization policy.

Instruction-like text found in journal entries remains untrusted data. It does
not become an instruction to Hardware Sentinel, a future LLM investigator, or
the remediation layer.

The local LLM must not be treated as a source of telemetry facts or as direct
authority for system actions.

## Phase Roadmap

- [x] Phase 1 — Observability Foundation — 100%
- [ ] Phase 2 — History and Baselines
- [ ] Phase 3 — Diagnostic Engine
- [ ] Phase 4 — Local AI Investigator
- [ ] Phase 5 — Controlled Remediation
- [ ] Phase 6 — Reporting and UX
- [ ] Phase 7 — Testing and Portfolio Release

## Next Phase

**Phase 2 — History and Machine Baselines**

Planned work includes persistent local telemetry history, efficient history
queries, machine-specific and workload-aware baselines, trend analysis,
sustained-condition detection, deviation detection, and baseline tests.

Phase 2 should begin in a separate development session.

---

## Release Targets

### v1.0 — Sentinel Core

Target: **20 December 2026**

Complete, reproducible, open-source Linux diagnostic agent with CLI.

### v2.0 — Sentinel Desktop

Target: **30 April 2027**

Complete Linux desktop application with GTK interface and downloadable
installation package.

### Post-v2.0

Evaluate Flatpak and Flathub/software-store distribution.

See `docs/ROADMAP.md` for the complete roadmap.
