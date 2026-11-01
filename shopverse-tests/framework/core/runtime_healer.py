from __future__ import annotations

import ast
import hashlib
import inspect
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from playwright.sync_api import Locator, Page


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _norm(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def _tokens(value: str | None) -> set[str]:
    return {x for x in _norm(value).split() if len(x) > 1}


class RuntimeHealerAdapter:
    def __init__(self, project_root: Path, report_root: Path) -> None:
        self.project_root = project_root
        self.report_root = report_root
        self.report_root.mkdir(parents=True, exist_ok=True)
        self._pending: dict[int, dict[str, Any]] = {}

    @staticmethod
    def _identity(failed_locator: Locator) -> tuple[str, str, Path] | None:
        for frame_info in inspect.stack()[2:18]:
            owner = frame_info.frame.f_locals.get("self")
            if owner is None or owner.__class__.__name__ in {"PlaywrightActions", "RuntimeHealerAdapter"}:
                continue
            for name, value in vars(owner).items():
                if value is failed_locator:
                    source = inspect.getsourcefile(owner.__class__)
                    if source:
                        return owner.__class__.__name__, name, Path(source).resolve()
        return None

    @staticmethod
    def _source_locator(path: Path, class_name: str, object_name: str) -> str | None:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            return None
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name):
            for node in ast.walk(cls):
                if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                    continue
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if not any(isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
                           and t.value.id == "self" and t.attr == object_name for t in targets):
                    continue
                value = node.value
                if (isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute)
                        and value.func.attr == "locator" and value.args):
                    arg = value.args[0]
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        return arg.value
        return None

    @staticmethod
    def _dom(page: Page) -> list[dict[str, str]]:
        return page.locator("body").evaluate("""body => Array.from(body.querySelectorAll('*')).map((e, i) => ({
          i: String(i), tag: (e.tagName || '').toLowerCase(), id: e.id || '', name: e.getAttribute('name') || '',
          testid: e.getAttribute('data-testid') || e.getAttribute('data-test') || '',
          aria: e.getAttribute('aria-label') || '', placeholder: e.getAttribute('placeholder') || '',
          role: e.getAttribute('role') || '', type: e.getAttribute('type') || '', value: e.getAttribute('value') || '',
          text: (e.innerText || e.textContent || '').trim().replace(/\s+/g,' ').slice(0,160)
        }))""")

    @staticmethod
    def _candidate(page: Page, row: dict[str, str]) -> tuple[Locator, str] | None:
        if row.get("id") and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", row["id"]):
            selector = "#" + row["id"]
            return page.locator(selector), selector
        if row.get("testid"):
            v = row["testid"]
            return page.locator(f'[data-test="{v}"]'), f'[data-test="{v}"]'
        if row.get("name") and '"' not in row["name"]:
            v = row["name"]
            return page.locator(f'[name="{v}"]'), f'[name="{v}"]'
        return None

    @staticmethod
    def _score(object_name: str, row: dict[str, str]) -> float:
        wanted = _tokens(object_name)
        if not wanted:
            return 0.0
        fields = " ".join(str(row.get(k, "")) for k in
                          ("id", "name", "testid", "aria", "placeholder", "role", "type", "value", "text"))
        actual = _tokens(fields)
        overlap = len(wanted & actual) / len(wanted)
        joined = _norm(object_name).replace(" ", "")
        compact = _norm(fields).replace(" ", "")
        contains = 1.0 if joined and joined in compact else 0.0
        return max(overlap, contains)

    def recover(self, *, page: Page, failed_locator: Locator, context: Any) -> Locator | None:
        if str(getattr(context, "action", "")).startswith("expect_"):
            return None
        identity = self._identity(failed_locator)
        if not identity:
            return None
        page_name, object_name, source = identity
        old_locator = self._source_locator(source, page_name, object_name)
        if not old_locator:
            return None
        ranked = []
        for row in self._dom(page):
            candidate = self._candidate(page, row)
            if not candidate:
                continue
            locator, selector = candidate
            score = self._score(object_name, row)
            if score < 0.75 or selector == old_locator:
                continue
            try:
                if locator.count() != 1 or not locator.is_visible() or not locator.is_enabled():
                    continue
            except Exception:
                continue
            ranked.append((score, selector, locator))
        ranked.sort(key=lambda x: (-x[0], x[1]))
        if not ranked:
            return None
        if len(ranked) > 1 and ranked[1][0] >= ranked[0][0] - 0.05:
            return None
        score, selector, locator = ranked[0]
        self._pending[id(failed_locator)] = {
            "page_name": page_name, "object_name": object_name,
            "action": str(getattr(context, "action", "")), "old_locator": old_locator,
            "new_locator": selector, "confidence": round(score, 4), "match_status": "CONFIRMED",
            "source_path": str(source),
        }
        return locator

    def record_success(self, *, page: Page, failed_locator: Locator, replacement: Locator, context: Any) -> None:
        evidence = self._pending.pop(id(failed_locator), None)
        if not evidence:
            return
        evidence.update({"runtime_validation": "PASSED", "review_status": "PENDING", "recorded_at": _now()})
        seed = f"{evidence['page_name']}|{evidence['object_name']}|{evidence['recorded_at']}"
        report_id = "HEAL_" + hashlib.sha256(seed.encode()).hexdigest()[:16]
        item_id = "ITEM_" + hashlib.sha256((report_id + evidence["object_name"]).encode()).hexdigest()[:16]
        evidence["item_id"] = item_id
        report = {"report_id": report_id, "mode": "runtime", "created_at": _now(),
                  "status": "REVIEW_REQUIRED", "items": [evidence]}
        target = self.report_root / f"{report_id}.json"
        temp = target.with_suffix(".tmp")
        temp.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        temp.replace(target)


def create_runtime_healer(page: Page) -> RuntimeHealerAdapter | None:
    framework_root = Path(__file__).resolve().parents[2]
    project_root = framework_root.parent
    config_path = project_root / "config.json"
    if not config_path.is_file():
        return None
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    healer = config.get("M2A_Healer") or {}
    if str(healer.get("mode", "runtime")).strip().lower() != "runtime":
        return None
    report_path = Path(str(healer.get("report_path", "reports/healer")))
    report_root = report_path if report_path.is_absolute() else project_root / report_path
    return RuntimeHealerAdapter(project_root, report_root)
