from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StepRecord:
    sequence: int
    timestamp: str
    action_name: str
    locator: str | None
    input_value: str | None
    expected_result: str | None
    actual_result: str | None
    status: str
    duration_ms: float
    screenshot: str | None = None
    exception_type: str | None = None
    exception_message: str | None = None
    stack_trace: str | None = None
    root_cause: str | None = None
    logical_name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TestRecord:
    nodeid: str
    name: str
    started_at: str = field(default_factory=utc_now_iso)
    completed_at: str | None = None
    duration_ms: float = 0.0
    status: str = "RUNNING"
    steps: list[StepRecord] = field(default_factory=list)
    failure: dict[str, Any] | None = None
    application_url: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "nodeid": self.nodeid,
            "name": self.name,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "steps": [step.as_dict() for step in self.steps],
            "failure": self.failure,
            "application_url": self.application_url,
        }
