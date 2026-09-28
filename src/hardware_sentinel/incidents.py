"""Structured incident and evidence models for Hardware Sentinel."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


TRUSTED = "trusted"
UNTRUSTED = "untrusted"

VALID_TRUST = {TRUSTED, UNTRUSTED}
VALID_SEVERITIES = {"warning", "critical"}


def _utc_now() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Evidence:
    """Diagnostic material associated with an incident.

    Evidence records preserve their trust classification. Externally generated
    material such as journal messages must remain untrusted.
    """

    source: str
    trust: str
    data: Any
    collected_at: str = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if not self.source:
            raise ValueError("evidence source must not be empty")

        if self.trust not in VALID_TRUST:
            raise ValueError(f"invalid evidence trust classification: {self.trust}")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)


@dataclass
class Incident:
    """A deterministic abnormal condition and its collected evidence."""

    incident_type: str
    severity: str
    facts: dict[str, Any]
    session_id: str
    detected_at: str
    incident_id: str = field(default_factory=lambda: str(uuid4()))
    evidence: list[Evidence] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.incident_type:
            raise ValueError("incident_type must not be empty")

        if self.severity not in VALID_SEVERITIES:
            raise ValueError(f"invalid incident severity: {self.severity}")

        if not self.session_id:
            raise ValueError("session_id must not be empty")

        if not self.detected_at:
            raise ValueError("detected_at must not be empty")

    def add_evidence(self, evidence: Evidence) -> None:
        """Attach evidence without changing its trust classification."""

        self.evidence.append(evidence)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return {
            "incident_id": self.incident_id,
            "incident_type": self.incident_type,
            "severity": self.severity,
            "detected_at": self.detected_at,
            "session_id": self.session_id,
            "facts": self.facts,
            "evidence": [item.to_dict() for item in self.evidence],
        }
