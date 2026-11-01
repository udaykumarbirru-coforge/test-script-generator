from __future__ import annotations

import os
from pathlib import Path
from time import perf_counter
from typing import Any

import pytest

from framework.core.driver_manager import DriverManager
from framework.core.execution_agent import ExecutionAgentReportingBridge
from framework.reporting.context import get_reporter

_BRIDGE: ExecutionAgentReportingBridge | None = None
_TEST_START: dict[str, float] = {}


def pytest_sessionstart(session: pytest.Session) -> None:
    global _BRIDGE
    project_root = Path(str(session.config.rootpath)).resolve()
    _BRIDGE = ExecutionAgentReportingBridge(project_root)
    reporter = _BRIDGE.start_execution()
    if reporter is not None:
        reporter.set_environment("Pytest", pytest.__version__)


def pytest_configure(config: pytest.Config) -> None:
    # Marker is registered here so users can filter or decorate tests later
    # without adding reporting code to generated scripts.
    config.addinivalue_line("markers", "m2a: test executed through M2A framework infrastructure")


@pytest.fixture(autouse=True)
def _m2a_reporting_test_context(request: pytest.FixtureRequest):
    reporter = get_reporter()
    nodeid = request.node.nodeid
    _TEST_START[nodeid] = perf_counter()
    page = None
    if reporter is not None:
        # Do not force a browser for API-only tests. Bind Page only when the test
        # already requests it through its normal fixture graph.
        if "page" in request.fixturenames:
            try:
                page = request.getfixturevalue("page")
                DriverManager.instrument_page(page)
            except Exception:
                page = None
        reporter.start_test(nodeid=nodeid, name=request.node.name, page=page)
        browser_name = None
        if "browser_name" in request.fixturenames:
            try:
                browser_name = request.getfixturevalue("browser_name")
            except Exception:
                pass
        if browser_name:
            reporter.set_browser_info(Browser=browser_name)
        if page is not None:
            try:
                viewport = getattr(page, "viewport_size", None)
                if viewport:
                    reporter.set_browser_info(Viewport=f"{viewport.get('width')}x{viewport.get('height')}")
                browser = getattr(getattr(page, "context", None), "browser", None)
                browser_version = getattr(browser, "version", None) if browser is not None else None
                if browser_version:
                    reporter.set_browser_info(Browser_Version=browser_version)
            except Exception:
                pass
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]):
    outcome = yield
    report = outcome.get_result()
    reporter = get_reporter()
    if reporter is None:
        return
    if report.when == "call" and report.failed:
        page = getattr(item, "_m2a_page", None)
        reporter.record_test_failure(call.excinfo.value if call.excinfo else None, str(report.longrepr), page=page)
    if report.when == "teardown":
        nodeid = item.nodeid
        started = _TEST_START.pop(nodeid, None)
        duration = (perf_counter() - started) if started is not None else report.duration
        # setup/call/teardown status is consolidated using rep_* properties set below.
        call_report = getattr(item, "rep_call", None)
        setup_report = getattr(item, "rep_setup", None)
        if (setup_report and setup_report.failed) or (call_report and call_report.failed) or report.failed:
            status = "FAIL"
        elif (setup_report and setup_report.skipped) or (call_report and call_report.skipped) or report.skipped:
            status = "SKIP"
        else:
            status = "PASS"
        reporter.finish_test(nodeid=nodeid, status=status, duration_seconds=duration)
        reporter.flush()
    setattr(item, f"rep_{report.when}", report)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    global _BRIDGE
    if _BRIDGE is None:
        return
    reporter = _BRIDGE.reporter
    if reporter is not None:
        reporter.set_environment("Pytest Exit Status", exitstatus)
    _BRIDGE.finish_execution()


def pytest_terminal_summary(terminalreporter: Any, exitstatus: int, config: pytest.Config) -> None:
    if _BRIDGE is not None and _BRIDGE.reporter is not None:
        terminalreporter.write_sep("=", f"M2A Extent Report: {_BRIDGE.reporter.report_path}")
