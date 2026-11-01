from __future__ import annotations

import html
import json
import os
import platform
import re
import threading
import traceback
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any

from framework.reporting.models import StepRecord, TestRecord, utc_now_iso

_SENSITIVE_HINTS = (
    "password", "passwd", "pwd", "secret", "token", "authorization", "auth",
    "cvv", "cvc", "card number", "card_number", "credit card", "access key",
    "api key", "apikey", "private key",
)


def _safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
    return cleaned[:120] or "test"


def _escape(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


class ExtentReportManager:
    """Framework-native Extent-style report manager for Python/pytest/Playwright.

    The official AventStack ExtentReports implementation targets Java/.NET. This
    manager keeps the same centralized lifecycle semantics (single execution,
    tests, step events, media attachments, environment metadata, final flush)
    without introducing Java/.NET into a Python framework.
    """

    def __init__(self, execution_root: Path, execution_id: str, config: dict[str, Any] | None = None) -> None:
        self.execution_root = execution_root
        self.execution_id = execution_id
        self.config = config or {}
        self.screenshot_root = self.execution_root / "screenshots"
        self.report_path = self.execution_root / "extent-report.html"
        self.json_path = self.execution_root / "execution-report.json"
        self.result_path = self.execution_root / "execution-result.json"
        self.screenshot_root.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._tests: dict[str, TestRecord] = {}
        self._current_nodeid: str | None = None
        self._pages: dict[str, Any] = {}
        self._started_monotonic = perf_counter()
        self.started_at = utc_now_iso()
        self.completed_at: str | None = None
        self.environment: dict[str, str] = {
            "OS": platform.platform(),
            "Python": platform.python_version(),
            "Machine": platform.machine() or "unknown",
            "Execution ID": execution_id,
        }
        self.browser_info: dict[str, str] = {}
        self.application_info: dict[str, str] = {}

    @property
    def current_test(self) -> TestRecord | None:
        if not self._current_nodeid:
            return None
        return self._tests.get(self._current_nodeid)

    def set_environment(self, key: str, value: Any) -> None:
        if value is not None and str(value).strip():
            self.environment[str(key)] = str(value)

    def set_browser_info(self, **values: Any) -> None:
        for key, value in values.items():
            if value is not None and str(value).strip():
                self.browser_info[str(key)] = str(value)

    def set_application_info(self, **values: Any) -> None:
        for key, value in values.items():
            if value is not None and str(value).strip():
                self.application_info[str(key)] = str(value)

    def start_test(self, nodeid: str, name: str, page: Any | None = None) -> None:
        with self._lock:
            record = self._tests.get(nodeid)
            if record is None:
                record = TestRecord(nodeid=nodeid, name=name)
                self._tests[nodeid] = record
            self._current_nodeid = nodeid
            if page is not None:
                self._pages[nodeid] = page
                self._capture_application_url(record, page)

    def bind_page(self, page: Any) -> None:
        with self._lock:
            if self._current_nodeid:
                self._pages[self._current_nodeid] = page
                record = self._tests.get(self._current_nodeid)
                if record is not None:
                    self._capture_application_url(record, page)

    def _capture_application_url(self, record: TestRecord, page: Any) -> None:
        try:
            url = getattr(page, "url", None)
            if url and url != "about:blank":
                record.application_url = str(url)
                self.application_info.setdefault("Application URL", str(url))
                try:
                    title = page.title()
                    if title:
                        self.application_info.setdefault("Application Title", str(title))
                except Exception:
                    pass
        except Exception:
            pass

    def _mask_value(self, value: Any, *, locator: str | None, logical_name: str | None) -> str | None:
        if value is None:
            return None
        raw = str(value)
        if not self.config.get("mask_sensitive_inputs", True):
            return raw
        hints = " ".join(filter(None, [locator, logical_name])).lower()
        if any(hint in hints for hint in _SENSITIVE_HINTS):
            return "********"
        # Common payment-card shape: preserve only last four digits.
        digits = re.sub(r"\D", "", raw)
        if len(digits) in {15, 16, 19} and len(raw) >= 15:
            return f"**** **** **** {digits[-4:]}"
        return raw

    def _page_for_current_test(self, explicit_page: Any | None = None) -> Any | None:
        if explicit_page is not None:
            return explicit_page
        if self._current_nodeid:
            return self._pages.get(self._current_nodeid)
        return None

    def _screenshot(self, *, status: str, action_name: str, page: Any | None) -> str | None:
        if page is None:
            return None
        if status == "PASS" and not self.config.get("screenshot_on_pass", True):
            return None
        if status == "FAIL" and not self.config.get("screenshot_on_fail", True):
            return None
        test = self.current_test
        if test is None:
            return None
        sequence = len(test.steps) + 1
        test_dir = self.screenshot_root / _safe_name(test.name)
        test_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{sequence:04d}_{_safe_name(action_name.lower())}_{status.lower()}.png"
        target = test_dir / filename
        try:
            page.screenshot(
                path=str(target),
                full_page=bool(self.config.get("full_page_screenshots", False)),
            )
            return target.relative_to(self.execution_root).as_posix()
        except Exception as screenshot_error:
            return f"SCREENSHOT_CAPTURE_FAILED: {type(screenshot_error).__name__}: {screenshot_error}"

    @staticmethod
    def _root_cause(exc: BaseException) -> str:
        current: BaseException = exc
        while current.__cause__ is not None:
            current = current.__cause__
        return f"{type(current).__name__}: {current}"

    def log_step(
        self,
        *,
        action_name: str,
        locator: str | None = None,
        input_value: Any | None = None,
        expected_result: str | None = None,
        actual_result: str | None = None,
        status: str = "PASS",
        started_at_monotonic: float | None = None,
        page: Any | None = None,
        logical_name: str | None = None,
        exception: BaseException | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> StepRecord | None:
        with self._lock:
            test = self.current_test
            if test is None:
                return None
            page = self._page_for_current_test(page)
            if page is not None:
                self._capture_application_url(test, page)
            duration_ms = 0.0
            if started_at_monotonic is not None:
                duration_ms = round((perf_counter() - started_at_monotonic) * 1000, 2)
            normalized_status = str(status).upper()
            screenshot = self._screenshot(status=normalized_status, action_name=action_name, page=page)
            stack_trace = None
            exc_type = None
            exc_message = None
            root_cause = None
            if exception is not None:
                exc_type = type(exception).__name__
                exc_message = str(exception)
                stack_trace = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
                root_cause = self._root_cause(exception)
            record = StepRecord(
                sequence=len(test.steps) + 1,
                timestamp=utc_now_iso(),
                action_name=str(action_name).upper(),
                locator=locator,
                input_value=self._mask_value(input_value, locator=locator, logical_name=logical_name),
                expected_result=expected_result,
                actual_result=actual_result,
                status=normalized_status,
                duration_ms=duration_ms,
                screenshot=screenshot,
                exception_type=exc_type,
                exception_message=exc_message,
                stack_trace=stack_trace,
                root_cause=root_cause,
                logical_name=logical_name,
                metadata=metadata or {},
            )
            test.steps.append(record)
            return record

    def record_test_failure(self, exc: BaseException | None, longrepr: str | None = None, page: Any | None = None) -> None:
        with self._lock:
            test = self.current_test
            if test is None:
                return
            test.status = "FAIL"
            failure = {
                "exception_type": type(exc).__name__ if exc else "TestFailure",
                "message": str(exc) if exc else (longrepr or "Test failed"),
                "stack_trace": longrepr or (
                    "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)) if exc else None
                ),
                "root_cause": self._root_cause(exc) if exc else (longrepr or "Test failed"),
            }
            page = self._page_for_current_test(page)
            failure["screenshot"] = self._screenshot(status="FAIL", action_name="TEST_FAILURE", page=page)
            test.failure = failure

    def finish_test(self, nodeid: str, status: str, duration_seconds: float | None = None) -> None:
        with self._lock:
            test = self._tests.get(nodeid)
            if test is None:
                return
            if test.status != "FAIL":
                test.status = str(status).upper()
            test.completed_at = utc_now_iso()
            if duration_seconds is not None:
                test.duration_ms = round(duration_seconds * 1000, 2)
            if self._current_nodeid == nodeid:
                self._current_nodeid = None

    def finish_execution(self) -> None:
        self.completed_at = utc_now_iso()
        self.flush()

    def _summary(self) -> dict[str, Any]:
        tests = list(self._tests.values())
        passed = sum(1 for t in tests if t.status == "PASS")
        failed = sum(1 for t in tests if t.status == "FAIL")
        skipped = sum(1 for t in tests if t.status == "SKIP")
        total_steps = sum(len(t.steps) for t in tests)
        failed_steps = sum(1 for t in tests for s in t.steps if s.status == "FAIL")
        warning_steps = sum(1 for t in tests for s in t.steps if s.status == "WARNING")
        return {
            "tests": len(tests),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "steps": total_steps,
            "failed_steps": failed_steps,
            "warning_steps": warning_steps,
            "duration_ms": round((perf_counter() - self._started_monotonic) * 1000, 2),
        }

    def as_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "summary": self._summary(),
            "environment": self.environment,
            "browser": self.browser_info,
            "application": self.application_info,
            "tests": [test.as_dict() for test in self._tests.values()],
        }

    def flush(self) -> None:
        with self._lock:
            self.execution_root.mkdir(parents=True, exist_ok=True)
            payload = self.as_dict()
            self.json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            self.report_path.write_text(self._render_html(payload), encoding="utf-8")
            self.result_path.write_text(
                json.dumps(
                    {
                        "execution_id": self.execution_id,
                        "status": "FAIL" if payload["summary"]["failed"] else "PASS",
                        "report_location": str(self.report_path.resolve()),
                        "report_json": str(self.json_path.resolve()),
                        "screenshots_location": str(self.screenshot_root.resolve()),
                        "summary": payload["summary"],
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

    def _render_html(self, payload: dict[str, Any]) -> str:
        summary = payload["summary"]
        env_rows = "".join(
            f"<tr><td>{_escape(k)}</td><td>{_escape(v)}</td></tr>"
            for k, v in {**payload["environment"], **payload["browser"], **payload["application"]}.items()
        ) or "<tr><td colspan='2'>No environment metadata captured.</td></tr>"

        test_sections: list[str] = []
        for test in payload["tests"]:
            step_rows: list[str] = []
            for step in test["steps"]:
                screenshot = step.get("screenshot")
                if screenshot and not screenshot.startswith("SCREENSHOT_CAPTURE_FAILED"):
                    shot_html = f"<a href='{_escape(screenshot)}' target='_blank'><img class='thumb' src='{_escape(screenshot)}' alt='step screenshot'></a>"
                else:
                    shot_html = _escape(screenshot or "-")
                failure_html = ""
                if step.get("exception_message") or step.get("root_cause"):
                    failure_html = (
                        "<details><summary>Failure details</summary>"
                        f"<div><b>Root cause:</b> {_escape(step.get('root_cause'))}</div>"
                        f"<pre>{_escape(step.get('stack_trace'))}</pre></details>"
                    )
                step_rows.append(
                    "<tr>"
                    f"<td>{step['sequence']}</td>"
                    f"<td>{_escape(step['timestamp'])}</td>"
                    f"<td><b>{_escape(step['action_name'])}</b>{('<br><small>'+_escape(step.get('logical_name'))+'</small>') if step.get('logical_name') else ''}</td>"
                    f"<td><code>{_escape(step.get('locator') or '-')}</code></td>"
                    f"<td>{_escape(step.get('input_value') or '-')}</td>"
                    f"<td>{_escape(step.get('expected_result') or '-')}</td>"
                    f"<td>{_escape(step.get('actual_result') or '-')}{failure_html}</td>"
                    f"<td><span class='status {step['status'].lower()}'>{_escape(step['status'])}</span></td>"
                    f"<td>{step['duration_ms']:.2f}</td>"
                    f"<td>{shot_html}</td>"
                    "</tr>"
                )
            failure_block = ""
            if test.get("failure"):
                failure = test["failure"]
                shot = failure.get("screenshot")
                shot_link = ""
                if shot and not str(shot).startswith("SCREENSHOT_CAPTURE_FAILED"):
                    shot_link = f"<p><a href='{_escape(shot)}' target='_blank'>Open failure screenshot</a></p>"
                failure_block = (
                    "<div class='failure-box'><h4>Failure Analysis</h4>"
                    f"<p><b>Root cause:</b> {_escape(failure.get('root_cause'))}</p>"
                    f"{shot_link}<details><summary>Stack trace</summary><pre>{_escape(failure.get('stack_trace'))}</pre></details></div>"
                )
            test_sections.append(
                f"<section class='test-card'><div class='test-head'><div><h3>{_escape(test['name'])}</h3>"
                f"<small>{_escape(test['nodeid'])}</small></div><span class='status {test['status'].lower()}'>{_escape(test['status'])}</span></div>"
                f"<div class='test-meta'>Duration: {test['duration_ms']:.2f} ms &nbsp;|&nbsp; Steps: {len(test['steps'])}"
                f"{(' &nbsp;|&nbsp; URL: '+_escape(test.get('application_url'))) if test.get('application_url') else ''}</div>"
                f"{failure_block}<div class='table-wrap'><table><thead><tr>"
                "<th>#</th><th>Timestamp</th><th>Action</th><th>Locator</th><th>Input</th><th>Expected</th><th>Actual / Details</th><th>Status</th><th>ms</th><th>Evidence</th>"
                f"</tr></thead><tbody>{''.join(step_rows) or '<tr><td colspan=10>No framework actions captured.</td></tr>'}</tbody></table></div></section>"
            )

        generated = datetime.now(timezone.utc).isoformat()
        report_title = str(self.config.get("report_title", "M2A Extent Execution Report"))
        return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{_escape(report_title)} - {_escape(self.execution_id)}</title>
<style>
:root{{--bg:#f5f7fb;--card:#fff;--text:#172033;--muted:#68758a;--line:#dfe5ef;--pass:#0a7f46;--fail:#b42318;--warning:#b54708;--info:#175cd3}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);font:14px/1.45 Arial,sans-serif;color:var(--text)}}
header{{background:#111827;color:#fff;padding:24px 32px}}header h1{{margin:0 0 6px;font-size:24px}}header small{{color:#cbd5e1}}
main{{padding:24px;max-width:1800px;margin:auto}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:18px}}
.metric,.panel,.test-card{{background:var(--card);border:1px solid var(--line);border-radius:10px;box-shadow:0 1px 2px rgba(16,24,40,.04)}}
.metric{{padding:18px}}.metric b{{display:block;font-size:26px;margin-top:5px}}.panel{{padding:18px;margin-bottom:18px}}.panel h2{{margin-top:0}}
table{{width:100%;border-collapse:collapse}}th,td{{border-bottom:1px solid var(--line);padding:9px 10px;text-align:left;vertical-align:top}}th{{background:#f8fafc;position:sticky;top:0}}
.table-wrap{{overflow:auto;max-height:640px}}code,pre{{white-space:pre-wrap;word-break:break-word}}pre{{background:#101828;color:#f2f4f7;padding:12px;border-radius:6px;max-height:320px;overflow:auto}}
.status{{display:inline-block;border-radius:999px;padding:3px 9px;font-weight:700;font-size:12px}}.status.pass{{background:#dcfae6;color:var(--pass)}}.status.fail{{background:#fee4e2;color:var(--fail)}}.status.warning{{background:#fef0c7;color:var(--warning)}}.status.info,.status.running,.status.skip{{background:#dbeafe;color:var(--info)}}
.test-card{{margin:16px 0;overflow:hidden}}.test-head{{display:flex;justify-content:space-between;gap:10px;align-items:center;padding:16px 18px;border-bottom:1px solid var(--line)}}.test-head h3{{margin:0 0 3px}}.test-meta{{padding:10px 18px;color:var(--muted)}}
.failure-box{{margin:12px 18px;padding:12px;border-left:4px solid var(--fail);background:#fff1f0}}.thumb{{width:180px;max-height:110px;object-fit:cover;border:1px solid var(--line);border-radius:4px}}
footer{{padding:20px 32px;color:var(--muted)}}
</style></head>
<body><header><h1>{_escape(report_title)}</h1><div>Execution ID: {_escape(self.execution_id)}</div><small>Started: {_escape(self.started_at)} &nbsp;|&nbsp; Completed: {_escape(self.completed_at or '-')}</small></header>
<main><div class='grid'>
<div class='metric'>Tests<b>{summary['tests']}</b></div><div class='metric'>Passed<b>{summary['passed']}</b></div><div class='metric'>Failed<b>{summary['failed']}</b></div><div class='metric'>Skipped<b>{summary['skipped']}</b></div><div class='metric'>Steps<b>{summary['steps']}</b></div><div class='metric'>Warnings<b>{summary['warning_steps']}</b></div><div class='metric'>Duration<b>{summary['duration_ms']/1000:.2f}s</b></div>
</div>
<section class='panel'><h2>Environment / Browser / Application Information</h2><table><tbody>{env_rows}</tbody></table></section>
<section class='panel'><h2>Test Case Summary</h2><p>Step-level execution history, screenshot evidence, assertion results and failure analysis are shown below.</p></section>
{''.join(test_sections) or '<section class="panel">No test results were captured.</section>'}
</main><footer>Generated {_escape(generated)} by centralized M2A reporting infrastructure.</footer></body></html>"""
