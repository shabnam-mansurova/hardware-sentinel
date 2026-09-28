"""Session metadata for Hardware Sentinel."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


def _utc_now() -> str:
    """Return the current UTC timestamp in ISO 8601 format."""

    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Session:
    """Identity and start time for one Hardware Sentinel session."""

    session_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: str = field(default_factory=_utc_now)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return asdict(self)
