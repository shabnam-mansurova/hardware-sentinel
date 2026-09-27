# Hardware Sentinel — Project Status

Last updated: 2026-09-27

## Current Phase

**Phase 1 — Observability Foundation**

Estimated completion: **70–75%**

## Current Objective

Build a reliable, privacy-conscious foundation for observing Linux hardware and
software state and producing deterministic evidence for later diagnostic
investigation.

## Completed

- [x] CPU telemetry
- [x] Per-core CPU telemetry
- [x] Memory telemetry
- [x] Swap telemetry
- [x] Disk-capacity telemetry
- [x] Temperature monitoring
- [x] Battery monitoring
- [x] Process aggregation
- [x] Workload categorization
- [x] Intel GPU detection
- [x] Graceful GPU permission handling
- [x] Disk I/O counters
- [x] Network I/O counters
- [x] Disk/network rate calculation
- [x] Human-readable I/O rates
- [x] Continuous JSONL telemetry
- [x] Deterministic basic warnings
- [x] systemd system-state monitoring
- [x] Failed system-unit monitoring
- [x] Failed user-unit monitoring

## In Progress

- [ ] Bounded journal evidence collection
  - collector implemented
  - live Fedora test successful
  - automated tests pending
  - commit pending

## Remaining Phase 1 Work

- [ ] Complete journal collector tests
- [ ] Define Incident data model
- [ ] Define Evidence data model
- [ ] Add machine/session metadata
- [ ] Connect anomalies to incident creation
- [ ] Trigger bounded evidence collection for incidents
- [ ] Add integration and edge-case tests
- [ ] Update Phase 1 documentation
- [ ] Perform Phase 1 completion review

## Next Session

### Priority 1

Finish journal evidence collection.

Target:

- malicious-looking log text remains classified as untrusted data
- invalid JSON handled safely
- empty successful query distinguished from failure
- collection failure handled gracefully
- maximum line limit enforced
- complete suite reaches approximately 17 tests
- journal feature committed and pushed

### Priority 2

Design the structured Incident and Evidence model.

Target conceptual flow:

    deterministic anomaly
            ↓
         incident
            ↓
    evidence collection
            ↓
    structured evidence
            ↓
    later diagnostic reasoning

## Current Security Boundary

Hardware Sentinel distinguishes:

**Facts**
Deterministic measurements and system state.

**Evidence**
Externally generated diagnostic material such as journal messages. Evidence may
be untrusted.

**Reasoning**
Future diagnostic hypotheses and explanations.

**Actions**
Future remediation operations controlled by an explicit safety policy.

The local LLM must not be treated as a source of telemetry facts or direct
authority for system actions.

## Phase Roadmap

- [ ] Phase 1 — Observability Foundation — 70–75%
- [ ] Phase 2 — History and Baselines
- [ ] Phase 3 — Diagnostic Engine
- [ ] Phase 4 — Local AI Investigator
- [ ] Phase 5 — Controlled Remediation
- [ ] Phase 6 — Reporting and UX
- [ ] Phase 7 — Testing and Portfolio Release
