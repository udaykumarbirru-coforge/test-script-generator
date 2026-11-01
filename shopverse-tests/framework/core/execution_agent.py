from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from framework.reporting.context import set_reporter
from framework.reporting.extent_reporter import ExtentReportManager


class ExecutionAgentReportingBridge:
    """Execution-agent lifecycle bridge for centralized reporting."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.config = self._load_config()
        self.reporter: ExtentReportManager | None = None

    def _load_config(self) -> dict[str, Any]:
        config_path = self.project_root / "framework" / "config" / "reporting.json"
        defaults: dict[str, Any] = {
            "enabled": True,
            "report_root": "reports/executions",
            "screenshot_on_pass": True,
            "screenshot_on_fail": True,
            "full_page_screenshots": False,
            "mask_sensitive_inputs": True,
        }
        if config_path.is_file():
            try:
                loaded = json.loads(config_path.read_text(encoding="utf-8"))
                defaults.update(loaded)
            except (OSError, json.JSONDecodeError):
                pass
        env_enabled = os.getenv("M2A_REPORTING_ENABLED")
        if env_enabled is not None:
            defaults["enabled"] = env_enabled.strip().lower() not in {"0", "false", "no", "off"}
        if os.getenv("M2A_REPORT_ROOT"):
            defaults["report_root"] = os.environ["M2A_REPORT_ROOT"]
        return defaults

    def start_execution(self) -> ExtentReportManager | None:
        if not self.config.get("enabled", True):
            set_reporter(None)
            return None
        execution_id = os.getenv("M2A_EXECUTION_ID") or (
            datetime.now(timezone.utc).strftime("M2A_%Y%m%dT%H%M%SZ_") + uuid.uuid4().hex[:8]
        )
        report_root = Path(str(self.config.get("report_root", "reports/executions")))
        if not report_root.is_absolute():
            report_root = self.project_root / report_root
        execution_root = report_root / execution_id
        self.reporter = ExtentReportManager(execution_root, execution_id, self.config)
        self.reporter.set_environment("Project Root", str(self.project_root))
        self.reporter.set_environment("CI", os.getenv("CI", "false"))
        set_reporter(self.reporter)
        return self.reporter

    def finish_execution(self) -> Path | None:
        if self.reporter is None:
            return None
        self.reporter.finish_execution()
        report_path = self.reporter.report_path
        set_reporter(None)
        return report_path
