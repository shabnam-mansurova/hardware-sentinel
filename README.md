# Hardware Sentinel

Privacy-first local hardware monitoring and workload analysis with lightweight LLM-assisted insights.

## Goal

Hardware Sentinel monitors local system resources, records workload telemetry, analyzes resource usage deterministically, and uses a lightweight local LLM to turn structured measurements into human-readable insights.

## Core principles

- Local-first and privacy-conscious
- Low monitoring overhead
- Deterministic hardware measurements
- LLM-assisted explanation, not LLM-generated measurements
- Useful across everyday workloads such as browsing, development, gaming, and local AI inference

## Local LLM

Hardware Sentinel uses Llama 3.2 1B through Ollama as its explanation layer.

The LLM does not determine hardware measurements, thresholds, or system state. Those are calculated by the monitoring and analysis components before structured results are passed to the model.

## Status

Early development.
