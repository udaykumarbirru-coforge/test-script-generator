"""Centralized M2A execution reporting infrastructure."""

from framework.reporting.context import (
    get_reporter,
    is_framework_action_active,
    reporting_action_scope,
    set_reporter,
)
from framework.reporting.extent_reporter import ExtentReportManager

__all__ = [
    "ExtentReportManager",
    "get_reporter",
    "set_reporter",
    "reporting_action_scope",
    "is_framework_action_active",
]
