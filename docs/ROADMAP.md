# Hardware Sentinel Roadmap

## Vision

Hardware Sentinel is a privacy-first local Linux diagnostic agent.

It observes hardware and software state, detects abnormal conditions, investigates
likely causes using deterministic telemetry and system evidence, uses a local LLM
for evidence-grounded reasoning, proposes controlled remediation, and verifies
whether corrective actions actually resolved the problem.

Hardware Sentinel is intended to be open source, reproducible, auditable, and
extensible by other developers.

---

# v1.0 — Sentinel Core

**Target release: 20 December 2026**

The objective of v1.0 is a complete, reproducible, well-tested Linux diagnostic
agent with a command-line interface.

## Phase 1 — Observability Foundation

**Target: early October 2026**

Status at 2026-09-28: complete.

Goals:

- CPU telemetry
- memory and swap telemetry
- disk capacity and I/O
- network I/O
- temperature sensors
- battery information
- process aggregation
- workload categorization
- optional Intel GPU telemetry
- systemd health
- failed service detection
- bounded journal evidence
- machine and session metadata
- structured Incident and Evidence models
- anomaly-to-evidence integration
- automated tests

## Phase 2 — History and Machine Baselines

**Target: October 2026**

Goals:

- persistent local telemetry history
- efficient history queries
- machine-specific baselines
- workload-aware baselines
- trend analysis
- sustained-condition detection
- deviation and anomaly detection
- baseline tests

The objective is to distinguish unusual behavior from behavior that is normal
for the specific machine and workload.

## Phase 3 — Diagnostic Engine

**Target: October–November 2026**

Goals:

- convert abnormal conditions into incidents
- correlate telemetry with processes
- correlate service state
- collect bounded journal evidence
- compare current state with historical context
- deterministic diagnostic checks
- structured evidence aggregation
- incident lifecycle tracking

The diagnostic engine must operate independently of the LLM.

## Phase 4 — Local AI Investigator

**Target: November 2026**

Initial model:

    llama3.2:1b via Ollama

Goals:

- structured diagnostic context
- explicit separation of facts, evidence, and hypotheses
- evidence-grounded explanations
- interactive investigation
- proposed diagnostic steps
- proposed remediation plans
- bounded context construction
- handling of untrusted log evidence
- hallucination-focused testing
- prompt-injection-boundary testing
- graceful operation when Ollama is unavailable

The LLM is a reasoning component, not a source of telemetry facts.

## Phase 5 — Controlled Remediation and Verification

**Target: November–December 2026**

Goals:

- action registry
- explicit action allowlist
- risk classifications
- confirmation requirements
- privilege requirements
- controlled execution
- action audit records
- before/after measurements
- post-remediation verification
- incident resolution tracking

Potentially disruptive actions must require explicit user authorization.

## Phase 6 — CLI, Reports and User Experience

**Target: December 2026**

Target commands:

    sentinel status
    sentinel monitor
    sentinel diagnose
    sentinel ask "<question>"
    sentinel fix
    sentinel history
    sentinel report

Goals:

- coherent CLI
- useful incident reports
- system-health reports
- human-readable diagnostic explanations
- useful failure messages
- predictable exit behavior
- clean installation and first-run experience

## Phase 7 — v1.0 Engineering Release

**Deadline: 20 December 2026**

Release requirements:

- comprehensive automated tests
- CI
- reproducible installation
- Python project packaging
- clean dependency management
- README
- architecture documentation
- privacy documentation
- security documentation
- CONTRIBUTING.md
- SECURITY.md
- open-source LICENSE
- CHANGELOG.md
- examples
- reproducible demonstrations
- release screenshots or terminal demonstrations
- tagged GitHub release

Release:

    Hardware Sentinel v1.0.0 — Sentinel Core

---

# v1.x — Stabilization

**December 2026–January 2027**

Goals:

- bug fixes
- compatibility improvements
- documentation corrections
- dependency updates
- feedback-driven improvements

Major new architecture should normally wait for v2.0.

---

# v2.0 — Sentinel Desktop

**Target release: 30 April 2027**

The objective of v2.0 is to transform the stable Sentinel Core into a complete
Linux desktop application.

Normal desktop use should not require the terminal.

## Desktop Phase A — Core/UI Separation

**Target: January 2027**

Goals:

- stable internal Sentinel Core API
- CLI and GUI consume the same core functionality
- separate presentation from diagnostic logic
- define GUI-facing state and events
- preserve CLI functionality

## Desktop Phase B — GTK Desktop Application

**Target: February–March 2027**

Planned interface:

- system-health dashboard
- current incidents
- incident details
- investigation view
- evidence view
- history
- local AI investigator
- remediation approval dialogs
- verification results
- settings
- desktop notifications
- basic telemetry visualization

The GUI must not bypass the existing safety and action-policy layers.

## Desktop Phase C — Linux Integration and Distribution

**Target: March–April 2027**

Goals:

- application icon
- desktop launcher
- Linux package/installer
- clean installation
- clean uninstall
- update strategy
- permissions documentation
- distribution testing
- downloadable GitHub release

The application should appear and behave like a normal Linux desktop
application after installation.

## Desktop Phase D — v2.0 Release

**Deadline: 30 April 2027**

Release requirements:

- polished desktop UX
- desktop-specific tests
- installation documentation
- screenshots
- demonstration
- user documentation
- project website
- tagged GitHub release

Release:

    Hardware Sentinel v2.0.0 — Sentinel Desktop

---

# Post-v2.0

Possible future development includes:

- Flathub submission
- graphical Linux software-store distribution
- AMD GPU support
- NVIDIA GPU support
- additional Linux distributions
- additional local LLM backends
- plugin architecture
- community diagnostic rules
- community remediation actions
- translations
- accessibility improvements
- optional Windows backend
- optional macOS backend

Windows and macOS are not part of the v1.0 or v2.0 scope.

---

# Open-Source and Reproducibility Requirements

Hardware Sentinel should be designed so that another developer can:

1. clone the repository;
2. understand the architecture;
3. install the documented dependencies;
4. run the complete test suite;
5. run Hardware Sentinel on a supported Linux system;
6. reproduce documented demonstrations;
7. inspect security and privacy boundaries;
8. implement a new collector, diagnostic rule, or action;
9. submit improvements through normal GitHub workflows.

Private machine-specific data must not be required to reproduce the project.

Runtime telemetry and diagnostic evidence must not be committed to the public
repository.

---

# Product Boundary

Hardware Sentinel is not intended to compete with system monitors primarily by
providing more resource graphs.

Traditional system monitors primarily expose system state.

Hardware Sentinel focuses on the workflow:

    Observe
       ↓
    Detect
       ↓
    Investigate
       ↓
    Explain
       ↓
    Propose
       ↓
    Authorize
       ↓
    Remediate
       ↓
    Verify

The central product value is evidence-grounded diagnosis and controlled
resolution of Linux system problems.

---

# Distribution Strategy

## v1.0

GitHub source repository and reproducible CLI installation.

## v2.0

Installable Linux desktop application distributed through GitHub releases.

## Post-v2.0

Evaluate Flatpak and Flathub/software-store distribution after the desktop
security and permissions model is stable.

Software-store publication is not a requirement for v2.0.

---

# Internationalization and Localization

**Target: Hardware Sentinel v2.0**

Hardware Sentinel Desktop is designed as a multilingual, local-first application.

Localization belongs to the presentation layer. Sentinel Core remains
language-neutral. Changing the user-facing language must never change telemetry,
diagnostic rules, incident identifiers, evidence, safety policy, remediation
logic, or verification results.

## v2.0 Target Locales

The initial v2.0 localization target is:

- `en-US` — English (United States), canonical/reference locale
- `de-DE` — German
- `fr-FR` — French
- `es-ES` — Spanish (Spain)
- `pt-PT` — Portuguese (Portugal)
- `it-IT` — Italian
- `pl-PL` — Polish
- `zh-CN` — Simplified Chinese
- `ja-JP` — Japanese
- `ko-KR` — Korean

English (`en-US`) is the canonical source language.

The localization architecture must not impose a fixed language limit.
Additional locales may later be contributed without modifying Sentinel Core.

## Architecture

Internal data remains language-neutral.

For example:

    incident_type: memory_pressure
    severity: warning
    memory_percent: 93.1

The internal identifier remains `memory_pressure` regardless of whether the
user interface is displayed in English, German, French, Chinese, Japanese,
Korean, or another supported language.

Conceptually:

    Linux / Hardware
          |
          v
    Sentinel Core
          |
          | structured language-neutral data
          v
    Incident / Evidence Model
          |
          +-----------------------------+
          |                             |
          v                             v
    Deterministic i18n            Local AI Investigator
          |                             |
          | GUI                         | explanations
          | notifications               | hypotheses
          | reports                     | reasoning
          | action descriptions         |
          +---------------+-------------+
                          |
                          v
                         User

Safety, authorization, action execution, and verification remain independent
of presentation language.

## Deterministic Localization

User-facing deterministic information should use local translation resources
rather than LLM-generated translation wherever practical.

This includes:

- GUI labels and controls
- incident names
- severity labels
- warnings
- notifications
- deterministic diagnostic statements
- action descriptions
- approval dialogs
- verification results
- structured reports

Measurements are inserted into translated templates from structured Sentinel
data. Translation must never generate or modify telemetry values.

GNU gettext is the planned localization mechanism.

## Localization Requirements

- Unicode throughout the application
- gettext-based translation catalogs
- automatic Linux locale detection
- manual language selection
- English fallback for missing translations
- locale-aware dates, times, numbers, and units
- pluralization support
- layouts capable of handling different text lengths
- correct rendering of Latin, Chinese, Japanese, and Korean text
- architecture capable of future right-to-left language support
- localized notifications and reports
- automated translation integrity tests
- documented translation contribution workflow

## Local AI Language Support

GUI localization and local-LLM language capability are separate features.

A translated Hardware Sentinel interface does not imply that the configured
local model has been validated for diagnostic reasoning in that language.

The AI Investigator receives structured facts and evidence from Sentinel Core.
Its output is treated as explanation or hypothesis, never as diagnostic truth.

Official AI support for a locale should only be claimed after that
language/model combination passes the multilingual diagnostic and safety
evaluation suite.

Where AI quality for the selected language has not been validated, Hardware
Sentinel should support a safe fallback such as English AI output while
retaining the selected GUI language.

## Multilingual AI Evaluation

The same canonical diagnostic cases should be evaluated across supported AI
languages.

Evaluation must check that the model:

- preserves measurements and numerical facts
- preserves incident severity
- distinguishes facts from hypotheses
- does not invent unsupported measurements or events
- does not omit safety-critical evidence
- does not reinterpret untrusted evidence as instructions
- cannot bypass the deterministic action policy
- does not change remediation permissions because of language
- communicates uncertainty when evidence is insufficient

The evaluation suite should include cases such as:

- CPU pressure
- memory and swap pressure
- thermal events
- disk pressure
- failed services
- unusual I/O activity
- insufficient evidence
- normal system state
- malicious or instruction-like journal content

A locale may have complete GUI localization while its AI support remains
experimental or falls back to English.

## Translation Quality

Machine- or AI-generated translations may be used as drafts, but they must not
be represented as verified solely because they were machine-generated.

Where appropriate, translation status should distinguish:

- maintained/verified
- community-maintained
- incomplete/experimental

Automated tests should verify:

- required translation keys exist
- placeholders are preserved
- translated templates remain valid
- Unicode content loads correctly
- locale fallback works
- changing language does not change underlying incident data
- deterministic measurements remain identical across locales

Human linguistic review remains desirable for determining whether translated
technical language is natural and precise.

## Privacy and Offline Operation

Localization must not introduce a mandatory cloud dependency.

Translation catalogs are stored locally.

Normal localization must not require:

- a translation API
- a cloud account
- an external translation service
- uploading telemetry or diagnostic evidence

Local AI explanations use a locally configured model.

Once Hardware Sentinel and its selected local model are installed, multilingual
operation should be capable of functioning without an Internet connection.

## Community Translation Model

A contributor should be able to add a new language by contributing translation
resources and tests without modifying telemetry, diagnostics, incident handling,
AI safety boundaries, remediation logic, or verification logic.

The intended contribution workflow is:

    fork
      |
    add/update translation
      |
    run localization tests
      |
    pull request
      |
    maintainer review

## v2.0 Localization Completion Criteria

Before the v2.0 release:

- [ ] localization architecture is separated from Sentinel Core
- [ ] GUI strings are internationalized
- [ ] `en-US` canonical localization is complete
- [ ] target locale catalogs are implemented
- [ ] automatic locale detection works
- [ ] manual language selection works
- [ ] English fallback works
- [ ] notifications are localized
- [ ] deterministic reports are localized
- [ ] deterministic action descriptions are localized
- [ ] locale-aware formatting works
- [ ] CJK text renders correctly
- [ ] changing language does not change diagnostic facts
- [ ] translation placeholders have automated integrity tests
- [ ] multilingual AI evaluation suite exists
- [ ] AI support is validated separately from GUI localization
- [ ] untrusted-evidence safety tests include multilingual cases
- [ ] offline multilingual operation is tested
- [ ] translation contribution documentation exists

## Long-Term Goal

Hardware Sentinel should be internationally usable without compromising its
local-first privacy model, deterministic diagnostic foundation, or security
boundaries.

Adding a language should change how Hardware Sentinel communicates with the
user, not how Hardware Sentinel determines what is true.
