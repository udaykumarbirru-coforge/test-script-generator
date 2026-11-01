from __future__ import annotations

from functools import wraps
from time import perf_counter
from typing import Any, Callable

from framework.reporting.context import get_reporter, is_framework_action_active, reporting_action_scope


class DriverManager:
    """Adds transparent reporting to direct Page-level navigation calls.

    Generated tests sometimes call page.goto(...) directly. Instrumenting the
    Playwright Page instance here keeps those scripts clean while still making
    navigation visible in the centralized execution report.
    """

    _PATCHED_FLAG = "_m2a_reporting_instrumented"

    @classmethod
    def instrument_page(cls, page: Any) -> Any:
        if getattr(page, cls._PATCHED_FLAG, False):
            return page
        mappings = {
            "goto": ("NAVIGATE", lambda args, kwargs: args[0] if args else kwargs.get("url")),
            "reload": ("REFRESH", lambda args, kwargs: None),
            "go_back": ("NAVIGATE_BACK", lambda args, kwargs: None),
            "go_forward": ("NAVIGATE_FORWARD", lambda args, kwargs: None),
        }
        for method_name, (action_name, value_extractor) in mappings.items():
            original = getattr(page, method_name, None)
            if not callable(original):
                continue
            setattr(page, method_name, cls._wrap_page_method(page, original, action_name, value_extractor))
        try:
            setattr(page, cls._PATCHED_FLAG, True)
        except Exception:
            pass
        reporter = get_reporter()
        if reporter is not None:
            reporter.bind_page(page)
        return page

    @staticmethod
    def _wrap_page_method(
        page: Any,
        original: Callable[..., Any],
        action_name: str,
        value_extractor: Callable[[tuple[Any, ...], dict[str, Any]], Any],
    ) -> Callable[..., Any]:
        @wraps(original)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            if is_framework_action_active():
                return original(*args, **kwargs)
            reporter = get_reporter()
            if reporter is None:
                return original(*args, **kwargs)
            started = perf_counter()
            value = value_extractor(args, kwargs)
            try:
                with reporting_action_scope():
                    result = original(*args, **kwargs)
                reporter.log_step(
                    action_name=action_name,
                    input_value=value,
                    expected_result="Browser action completes without error",
                    actual_result="Browser action completed successfully",
                    status="PASS",
                    started_at_monotonic=started,
                    page=page,
                )
                return result
            except Exception as exc:
                reporter.log_step(
                    action_name=action_name,
                    input_value=value,
                    expected_result="Browser action completes without error",
                    actual_result=str(exc),
                    status="FAIL",
                    started_at_monotonic=started,
                    page=page,
                    exception=exc,
                )
                raise
        return wrapped
