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

Status at 2026-09-27: approximately 75% complete.

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

Hardware Sentinel Desktop must be designed as a multilingual application.

The Sentinel Core remains language-neutral. Localization belongs to the
presentation layer and must not change telemetry, diagnostic rules, incident
identifiers, evidence structures, safety policies, or remediation logic.

## v2.0 Language Support

Hardware Sentinel v2.0 will provide complete support for:

- English
- German

The application should:

- automatically detect the Linux system locale;
- allow the user to manually select a language;
- externalize user-facing GUI strings;
- localize notifications and error messages;
- localize incident and diagnostic reports;
- request local AI explanations in the selected language;
- preserve deterministic measurements and identifiers independently of
  presentation language.

Conceptually:

    Sentinel Core
         |
         | structured language-neutral data
         v
    Localization Layer
         |
       +-+---------+
       |           |
       v           v
    English      Deutsch
       |           |
       v           v
    GUI          GUI
    Reports      Reports
    AI Output    AI Output

Internal identifiers remain stable regardless of language.

For example:

    memory_pressure

may be presented to the user as:

    English: Memory pressure
    German:  Speicherdruck

but the underlying incident type remains `memory_pressure`.

## Local AI Language

The language used by the local LLM is a presentation preference, not a source
of diagnostic truth.

For example, the same structured incident:

    incident_type: memory_pressure
    memory_percent: 93.1

may produce an English or German explanation while preserving exactly the same
underlying measurements and evidence.

## Community Translations

The localization architecture should allow additional languages to be added
without modifying Sentinel Core.

Potential future community-maintained translations include:

- French
- Spanish
- Italian
- Polish
- Turkish
- Azerbaijani
- other languages requested or contributed by users

Translation contributions should be possible through the normal open-source
workflow:

    fork
      |
    add/update translation
      |
    test
      |
    pull request
      |
    maintainer review

A future translation contribution guide should document this process.

## v2.0 Localization Completion Criteria

Before the v2.0 release:

- [ ] GUI strings are internationalized
- [ ] English localization is complete
- [ ] German localization is complete
- [ ] automatic locale detection works
- [ ] manual language selection works
- [ ] notifications are localized
- [ ] reports are localized
- [ ] AI response language follows the selected language
- [ ] changing language does not change diagnostic facts
- [ ] localization behavior has automated tests
- [ ] translation contribution documentation exists

## Global Localization Goal

Hardware Sentinel is intended to be usable internationally.

The localization system must not impose a fixed limit on supported languages.
New translations should be addable without modifications to Sentinel Core.

### v2.0 Maintained Languages

The initial target is:

- English
- German
- Azerbaijani
- Turkish

Additional translations may be provided and maintained by the community.

### Localization Architecture Requirements

- Unicode throughout the application
- gettext-based translatable resources
- automatic Linux locale detection
- manual language selection
- English fallback for missing translations
- locale-aware dates, times, numbers, and units
- pluralization support
- layouts capable of handling different text lengths
- architecture capable of future right-to-left language support
- localized notifications and reports
- translation tests
- documented translation contribution workflow

### Translation Quality

Machine- or AI-generated translations may be used as drafts, but a translation
must not be represented as verified solely because it was machine-generated.

Translation status should be distinguishable where appropriate:

- maintained/verified
- community-maintained
- incomplete/experimental

### AI Language Support

GUI localization and local-LLM language capability are separate features.

Hardware Sentinel may provide a translated interface even when the configured
local model has limited capability in that language.

AI language support must therefore be tested separately from GUI localization.

### Long-Term Goal

A contributor should be able to add a new Hardware Sentinel language by
contributing localization resources and tests without needing to understand or
modify telemetry, diagnostics, incident handling, AI safety boundaries, or
remediation logic.
