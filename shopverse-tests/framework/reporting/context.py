from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from framework.reporting.extent_reporter import ExtentReportManager

_reporter: ContextVar["ExtentReportManager | None"] = ContextVar("m2a_reporter", default=None)
_framework_action_depth: ContextVar[int] = ContextVar("m2a_framework_action_depth", default=0)


def set_reporter(reporter: "ExtentReportManager | None") -> None:
    _reporter.set(reporter)


def get_reporter() -> "ExtentReportManager | None":
    return _reporter.get()


def is_framework_action_active() -> bool:
    return _framework_action_depth.get() > 0


@contextmanager
def reporting_action_scope() -> Iterator[None]:
    current = _framework_action_depth.get()
    token = _framework_action_depth.set(current + 1)
    try:
        yield
    finally:
        _framework_action_depth.reset(token)
