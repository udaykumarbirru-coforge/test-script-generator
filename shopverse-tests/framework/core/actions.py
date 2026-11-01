"""M2A reusable Playwright action library.

Cleaned from legacy browser/element/get/keyboard keyword implementations.
Framework-facing only: no M2A registry, executor, AppConfig, driver initializer,
or keyword_config dependencies.

Designed for Playwright sync API / pytest-playwright.
"""
from __future__ import annotations

import inspect
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional, Protocol, TypeVar

from playwright.sync_api import Locator, Page, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError, expect

from framework.core.runtime_healer import create_runtime_healer
from framework.reporting.context import get_reporter, reporting_action_scope

T = TypeVar("T")


@dataclass(frozen=True)
class ActionFailureContext:
    action: str
    logical_name: str | None
    locator: str | None
    error_type: str
    error_message: str


class RuntimeHealingHook(Protocol):
    def recover(
        self, *, page: Page, failed_locator: Locator, context: ActionFailureContext
    ) -> Locator | None: ...


class PlaywrightActionError(RuntimeError):
    """Raised when a reusable framework action cannot complete."""
    def __init__(self, context: ActionFailureContext | str) -> None:
        if isinstance(context, str):
            context = ActionFailureContext(
                action="framework_action", logical_name=None, locator=None,
                error_type="FrameworkActionError", error_message=context,
            )
        self.context = context
        super().__init__(
            f"Playwright action failed: action={context.action!r}, "
            f"object={context.logical_name!r}, locator={context.locator!r}, "
            f"cause={context.error_type}: {context.error_message}"
        )


class PlaywrightActions:
    def __init__(self, page: Page, healer: RuntimeHealingHook | None = None, timeout: int = 10_000):
        self.page = page
        self.healer = healer if healer is not None else create_runtime_healer(page)
        self.timeout = timeout

    @staticmethod
    def _describe(target: Locator) -> str:
        return repr(target)

    @staticmethod
    def _infer_logical_name(target: Locator) -> str | None:
        """Infer the Page Object field name without changing business methods."""
        try:
            for frame_info in inspect.stack()[2:14]:
                owner = frame_info.frame.f_locals.get("self")
                if owner is None or owner.__class__.__name__ == "PlaywrightActions":
                    continue
                try:
                    for name, value in vars(owner).items():
                        if value is target:
                            return name
                except Exception:
                    continue
        except Exception:
            return None
        return None

    def _execute(
        self,
        action: str,
        locator: Locator | None,
        operation: Callable[[Locator | None], T],
        *,
        logical_name: str | None = None,
        heal: bool = True,
        input_value: Any | None = None,
        expected_result: str | None = None,
        actual_result: str | Callable[[T], str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> T:
        """Execute one framework action and publish a centralized step event.

        All screenshots, PASS/FAIL/WARNING status, locator evidence, timing and
        exceptions are handled here. Page objects and generated tests remain
        reporting-free.
        """
        started = time.perf_counter()
        reporter = get_reporter()
        if logical_name is None and locator is not None:
            logical_name = self._infer_logical_name(locator)
        locator_description = self._describe(locator) if locator is not None else None
        healed = False
        effective_locator = locator_description
        try:
            with reporting_action_scope():
                try:
                    result = operation(locator)
                except (PlaywrightTimeoutError, PlaywrightError) as original:
                    if locator is None:
                        raise
                    context = ActionFailureContext(
                        action, logical_name, locator_description, type(original).__name__, str(original)
                    )
                    replacement: Locator | None = None
                    if heal and self.healer is not None:
                        replacement = self.healer.recover(
                            page=self.page, failed_locator=locator, context=context
                        )
                    if replacement is not None:
                        try:
                            result = operation(replacement)
                            healed = True
                            effective_locator = self._describe(replacement)
                            recorder = getattr(self.healer, "record_success", None)
                            if callable(recorder):
                                recorder(
                                    page=self.page,
                                    failed_locator=locator,
                                    replacement=replacement,
                                    context=context,
                                )
                        except (PlaywrightTimeoutError, PlaywrightError) as retry_error:
                            retry_context = ActionFailureContext(
                                action, logical_name, self._describe(replacement),
                                type(retry_error).__name__, str(retry_error)
                            )
                            raise PlaywrightActionError(retry_context) from retry_error
                    else:
                        raise PlaywrightActionError(context) from original

            if callable(actual_result):
                resolved_actual = actual_result(result)
            elif actual_result is not None:
                resolved_actual = actual_result
            else:
                resolved_actual = "Action completed successfully"
            if reporter is not None:
                step_metadata = dict(metadata or {})
                if healed:
                    step_metadata["runtime_healed"] = True
                    step_metadata["original_locator"] = locator_description
                    step_metadata["healed_locator"] = effective_locator
                reporter.log_step(
                    action_name=action,
                    locator=effective_locator,
                    input_value=input_value,
                    expected_result=expected_result or "Action completes without error",
                    actual_result=resolved_actual,
                    status="WARNING" if healed else "PASS",
                    started_at_monotonic=started,
                    page=self.page,
                    logical_name=logical_name,
                    metadata=step_metadata,
                )
            return result
        except Exception as exc:
            if reporter is not None:
                reporter.log_step(
                    action_name=action,
                    locator=effective_locator,
                    input_value=input_value,
                    expected_result=expected_result or "Action completes without error",
                    actual_result=str(exc),
                    status="FAIL",
                    started_at_monotonic=started,
                    page=self.page,
                    logical_name=logical_name,
                    exception=exc,
                    metadata=metadata,
                )
            raise

    def _execute_page(
        self,
        action: str,
        operation: Callable[[], T],
        *,
        input_value: Any | None = None,
        expected_result: str | None = None,
        actual_result: str | Callable[[T], str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> T:
        return self._execute(
            action,
            None,
            lambda _: operation(),
            heal=False,
            input_value=input_value,
            expected_result=expected_result,
            actual_result=actual_result,
            metadata=metadata,
        )

    # Framework contract aliases used by generated Page Objects.
    def goto(self, url: str) -> None:
        self.open_url(url)

    def fill(self, locator: Locator, value: str, *, logical_name: str | None = None) -> None:
        self.input_text(locator, value, logical_name=logical_name)

    def clear(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self.clear_text(locator, logical_name=logical_name)

    def hover(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self.mouse_hover(locator, logical_name=logical_name)

    def check(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self._execute("CHECKBOX", locator, lambda el: el.check(timeout=self.timeout), logical_name=logical_name, expected_result="Checkbox is checked")

    def uncheck(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self._execute("CHECKBOX", locator, lambda el: el.uncheck(timeout=self.timeout), logical_name=logical_name, expected_result="Checkbox is unchecked")

    def press(self, locator: Locator, key: str, *, logical_name: str | None = None) -> None:
        self.send_keys(locator, key, logical_name=logical_name)

    # Assertion methods intentionally bypass locator healing so expected behavior is never changed.
    def expect_visible(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self._execute("ASSERTION", locator, lambda el: expect(el).to_be_visible(timeout=self.timeout), logical_name=logical_name, heal=False, expected_result="Element is visible", actual_result="Element is visible")

    def expect_hidden(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self._execute("ASSERTION", locator, lambda el: expect(el).to_be_hidden(timeout=self.timeout), logical_name=logical_name, heal=False, expected_result="Element is hidden", actual_result="Element is hidden")

    def expect_text(self, locator: Locator, value: str, *, logical_name: str | None = None) -> None:
        self._execute("ASSERTION", locator, lambda el: expect(el).to_have_text(value, timeout=self.timeout), logical_name=logical_name, heal=False, input_value=value, expected_result=f"Element text equals {value!r}", actual_result="Expected text matched")

    def expect_value(self, locator: Locator, value: str, *, logical_name: str | None = None) -> None:
        self._execute("ASSERTION", locator, lambda el: expect(el).to_have_value(value, timeout=self.timeout), logical_name=logical_name, heal=False, input_value=value, expected_result=f"Element value equals {value!r}", actual_result="Expected value matched")

    # ---------------- Browser keywords ----------------
    def open_url(self, url: str) -> None:
        self._execute_page("NAVIGATE", lambda: self.page.goto(url, wait_until="domcontentloaded", timeout=self.timeout), input_value=url, expected_result="Application URL loads successfully")

    def refresh(self) -> None:
        self._execute_page("NAVIGATE", lambda: self.page.reload(wait_until="domcontentloaded", timeout=self.timeout), expected_result="Current page reloads successfully", metadata={"navigation": "refresh"})

    def navigate_back(self) -> None:
        self._execute_page("NAVIGATE", lambda: self.page.go_back(wait_until="domcontentloaded", timeout=self.timeout), expected_result="Browser navigates to previous history entry", metadata={"navigation": "back"})

    def navigate_forward(self) -> None:
        self._execute_page("NAVIGATE", lambda: self.page.go_forward(wait_until="domcontentloaded", timeout=self.timeout), expected_result="Browser navigates to next history entry", metadata={"navigation": "forward"})

    def switch_tab(self, tab_index: int) -> Page:
        def op() -> Page:
            pages = self.page.context.pages
            if tab_index < 0 or tab_index >= len(pages):
                raise IndexError(f"Tab index {tab_index} unavailable; open tabs={len(pages)}")
            self.page = pages[tab_index]
            self.page.bring_to_front()
            self.page.wait_for_load_state("domcontentloaded", timeout=self.timeout)
            return self.page
        return self._execute_page("NAVIGATE", op, input_value=tab_index, expected_result="Requested browser tab becomes active", actual_result="Requested browser tab is active", metadata={"navigation": "switch_tab"})

    def close_tab(self) -> Page | None:
        def op() -> Page | None:
            context = self.page.context
            self.page.close()
            pages = context.pages
            if not pages:
                return None
            self.page = pages[-1]
            self.page.bring_to_front()
            return self.page
        return self._execute_page("NAVIGATE", op, expected_result="Current browser tab closes successfully", metadata={"navigation": "close_tab"})

    def maximize(self) -> None:
        # Browser-window resize is environment dependent; this preserves the legacy JS behavior.
        self._execute_page("CUSTOM_ACTION", lambda: self.page.evaluate("""() => { if (window.moveTo && window.resizeTo) { window.moveTo(0,0); window.resizeTo(screen.availWidth, screen.availHeight); } }"""), expected_result="Browser window maximize request completes", metadata={"action_type": "maximize"})

    # ---------------- Element keywords ----------------
    def click(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self._execute("CLICK", locator, lambda el: el.click(timeout=self.timeout), logical_name=logical_name, expected_result="Element is clicked successfully")

    def input_text(self, locator: Locator, text: str, *, logical_name: str | None = None, clear: bool = True) -> None:
        def op(el: Locator) -> None:
            el.scroll_into_view_if_needed(timeout=self.timeout)
            if clear:
                el.fill("", timeout=self.timeout)
            el.fill(str(text), timeout=self.timeout)
        self._execute("FILL", locator, op, logical_name=logical_name, input_value=text, expected_result="Input value is entered successfully")

    def select_date(self, locator: Locator, date_value: str, *, logical_name: str | None = None) -> None:
        def op(el: Locator) -> None:
            el.click(timeout=self.timeout)
            el.fill(str(date_value), timeout=self.timeout)
            el.press("Tab", timeout=self.timeout)
        self._execute("FILL", locator, op, logical_name=logical_name, input_value=date_value, expected_result="Date value is entered successfully", metadata={"action_type": "select_date"})

    def double_click(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self._execute("CLICK", locator, lambda el: el.dblclick(timeout=self.timeout), logical_name=logical_name, expected_result="Element is double-clicked successfully", metadata={"click_type": "double"})

    def right_click(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self._execute("CLICK", locator, lambda el: el.click(button="right", timeout=self.timeout), logical_name=logical_name, expected_result="Element is right-clicked successfully", metadata={"click_type": "right"})

    def mouse_hover(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self._execute("HOVER", locator, lambda el: el.hover(timeout=self.timeout), logical_name=logical_name, expected_result="Pointer hovers over the element")

    def scroll_to_element(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self._execute("SCROLL", locator, lambda el: el.scroll_into_view_if_needed(timeout=self.timeout), logical_name=logical_name, expected_result="Element is scrolled into view")

    def clear_text(self, locator: Locator, *, logical_name: str | None = None) -> None:
        self._execute("FILL", locator, lambda el: el.fill("", timeout=self.timeout), logical_name=logical_name, input_value="", expected_result="Input value is cleared", metadata={"action_type": "clear"})

    def append_text(self, locator: Locator, text: str, *, logical_name: str | None = None) -> None:
        self._execute("FILL", locator, lambda el: el.press_sequentially(str(text)), logical_name=logical_name, input_value=text, expected_result="Text is appended successfully", metadata={"action_type": "append"})

    def send_keys(self, locator: Locator, keys: str, *, logical_name: str | None = None) -> None:
        self._execute("KEYBOARD_ACTION", locator, lambda el: el.press(keys, timeout=self.timeout), logical_name=logical_name, input_value=keys, expected_result="Keyboard action completes successfully")

    def select_option(self, locator: Locator, value: str, *, logical_name: str | None = None) -> None:
        def op(el: Locator) -> None:
            tag = el.evaluate("el => el.tagName.toLowerCase()")
            input_type = (el.get_attribute("type") or "").lower()
            role = (el.get_attribute("role") or "").lower()
            if input_type in {"checkbox", "radio"}:
                el.check(timeout=self.timeout)
                return
            if tag == "select":
                el.select_option(label=str(value), timeout=self.timeout)
                return
            el.click(timeout=self.timeout)
            if role == "combobox" or tag == "input":
                try:
                    el.fill(str(value), timeout=self.timeout)
                except PlaywrightError:
                    pass
            option = self.page.get_by_role("option", name=str(value), exact=True)
            if option.count() == 0:
                option = self.page.get_by_role("option", name=str(value), exact=False)
            if option.count() == 0:
                raise PlaywrightActionError(f"Option not found: {value}")
            option.first.click(timeout=self.timeout)
        self._execute("SELECT", locator, op, logical_name=logical_name, input_value=value, expected_result="Requested option/state is selected")

    def unselect_option(self, locator: Locator, value: str | None = None, *, logical_name: str | None = None) -> None:
        def op(el: Locator) -> None:
            tag = el.evaluate("el => el.tagName.toLowerCase()")
            input_type = (el.get_attribute("type") or "").lower()
            if input_type == "checkbox":
                el.uncheck(timeout=self.timeout)
            elif tag == "select" and value is not None:
                el.evaluate("(el, val) => { for (const o of el.options) if (o.value === val || o.label === val) o.selected=false; el.dispatchEvent(new Event('change',{bubbles:true})); }", value)
            else:
                raise PlaywrightActionError("unselect_option supports checkbox or select elements")
        self._execute("SELECT", locator, op, logical_name=logical_name, input_value=value, expected_result="Requested option/state is unselected", metadata={"action_type": "unselect"})

    def toggle_switch(self, locator: Locator, expected_state: str, *, logical_name: str | None = None) -> None:
        expected = expected_state.strip().lower()
        if expected not in {"on", "off", "true", "false"}:
            raise ValueError("expected_state must be on/off/true/false")
        expected_on = expected in {"on", "true"}
        def op(el: Locator) -> None:
            input_type = (el.get_attribute("type") or "").lower()
            if input_type == "checkbox":
                if el.is_checked() != expected_on:
                    el.click(timeout=self.timeout)
                return
            aria = el.get_attribute("aria-checked")
            if aria is not None:
                current = aria.lower() == "true"
                if current != expected_on:
                    el.click(timeout=self.timeout)
                return
            el.click(timeout=self.timeout)
        self._execute("CHECKBOX", locator, op, logical_name=logical_name, input_value=expected_state, expected_result=f"Control state becomes {expected_state}")

    def search_and_select_autocomplete(self, locator: Locator, value: str, *, logical_name: str | None = None) -> None:
        def op(el: Locator) -> None:
            el.scroll_into_view_if_needed(timeout=self.timeout)
            el.click(timeout=self.timeout)
            el.fill(str(value), timeout=self.timeout)
            el.press("ArrowDown", timeout=self.timeout)
            el.press("Enter", timeout=self.timeout)
        self._execute("SELECT", locator, op, logical_name=logical_name, input_value=value, expected_result="Autocomplete value is selected", metadata={"action_type": "autocomplete"})

    def close_dialog(self, locator: Locator | None = None, *, logical_name: str | None = None) -> None:
        if locator is not None:
            self._execute("CLICK", locator, lambda el: el.click(timeout=self.timeout), logical_name=logical_name or "dialog_close", expected_result="Dialog closes successfully", metadata={"action_type": "close_dialog"})
            return
        def op() -> None:
            # Generic semantic fallback only; no application-specific selectors.
            for role, name in (("button", "Close"), ("button", "OK"), ("button", "Cancel")):
                candidate = self.page.get_by_role(role, name=name, exact=True)
                if candidate.count() > 0:
                    candidate.first.click(timeout=self.timeout)
                    return
            self.page.keyboard.press("Escape")
        self._execute_page("CUSTOM_ACTION", op, expected_result="Dialog closes successfully", metadata={"action_type": "close_dialog"})

    def upload_file(self, locator: Locator, file_path: str | Path, *, logical_name: str | None = None) -> None:
        path = str(file_path)
        def op(el: Locator) -> None:
            try:
                el.set_input_files(path, timeout=self.timeout)
            except PlaywrightError:
                with self.page.expect_file_chooser(timeout=self.timeout) as chooser_info:
                    el.click(timeout=self.timeout)
                chooser_info.value.set_files(path)
        self._execute("CUSTOM_ACTION", locator, op, logical_name=logical_name, input_value=path, expected_result="File is uploaded successfully", metadata={"action_type": "upload_file"})

    def drag_start(self, locator: Locator, *, logical_name: str | None = None) -> None:
        def op(el: Locator) -> None:
            box = el.bounding_box(timeout=self.timeout)
            if not box:
                raise PlaywrightActionError("Element has no bounding box")
            self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            self.page.mouse.down()
        self._execute("DRAG_DROP", locator, op, logical_name=logical_name, expected_result="Drag operation starts successfully", metadata={"drag_phase": "start"})

    def drag_move_to(self, locator: Locator, *, logical_name: str | None = None) -> None:
        def op(el: Locator) -> None:
            box = el.bounding_box(timeout=self.timeout)
            if not box:
                raise PlaywrightActionError("Element has no bounding box")
            self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        self._execute("DRAG_DROP", locator, op, logical_name=logical_name, expected_result="Dragged item moves to target", metadata={"drag_phase": "move"})

    def drag_end(self) -> None:
        self._execute_page("DRAG_DROP", lambda: self.page.mouse.up(), expected_result="Drag operation completes successfully", metadata={"drag_phase": "end"})

    def wait_time(self, seconds: float) -> None:
        self._execute_page("WAIT", lambda: time.sleep(float(seconds)), input_value=seconds, expected_result=f"Wait completes after {seconds} seconds")

    def api_call(self, operation: Callable[[], T], *, request_summary: str | None = None, expected_result: str | None = None) -> T:
        """Execute a framework-managed API operation with automatic reporting."""
        return self._execute_page(
            "API_CALL", operation, input_value=request_summary,
            expected_result=expected_result or "API call completes without error",
            actual_result=lambda result: f"API call completed: {result!r}",
        )

    def custom_action(self, action_name: str, operation: Callable[[], T], *, input_value: Any | None = None, expected_result: str | None = None) -> T:
        """Execute a custom framework action while preserving centralized evidence capture."""
        return self._execute_page(
            "CUSTOM_ACTION", operation, input_value=input_value,
            expected_result=expected_result or f"{action_name} completes without error",
            metadata={"custom_action": action_name},
        )

    # ---------------- Get keywords ----------------
    def get_text(self, locator: Locator, *, logical_name: str | None = None) -> str:
        value = self._execute("CUSTOM_ACTION", locator, lambda el: el.text_content(timeout=self.timeout), logical_name=logical_name, expected_result="Element text is retrieved", actual_result=lambda result: str(result or ""), metadata={"action_type": "get_text"})
        return value or ""

    # ---------------- Keyboard keywords ----------------
    def press_key(self, key: str) -> None:
        self._execute_page("KEYBOARD_ACTION", lambda: self.page.keyboard.press(key), input_value=key, expected_result="Keyboard action completes successfully")

    def type_text(self, text: str) -> None:
        self._execute_page("KEYBOARD_ACTION", lambda: self.page.keyboard.type(str(text)), input_value=text, expected_result="Keyboard text entry completes successfully", metadata={"action_type": "type_text"})

    def key_enter(self) -> None: self.press_key("Enter")
    def key_escape(self) -> None: self.press_key("Escape")
    def key_tab(self) -> None: self.press_key("Tab")
    def key_backspace(self) -> None: self.press_key("Backspace")
    def key_delete(self) -> None: self.press_key("Delete")
    def key_space(self) -> None: self.press_key("Space")
    def key_arrow_up(self) -> None: self.press_key("ArrowUp")
    def key_arrow_down(self) -> None: self.press_key("ArrowDown")
    def key_arrow_left(self) -> None: self.press_key("ArrowLeft")
    def key_arrow_right(self) -> None: self.press_key("ArrowRight")
    def key_home(self) -> None: self.press_key("Home")
    def key_end(self) -> None: self.press_key("End")
    def key_page_up(self) -> None: self.press_key("PageUp")
    def key_page_down(self) -> None: self.press_key("PageDown")
    def key_f1(self) -> None: self.press_key("F1")
    def key_f5(self) -> None: self.press_key("F5")
    def key_f12(self) -> None: self.press_key("F12")
    def key_ctrl_c(self) -> None: self.press_key("Control+C")
    def key_ctrl_v(self) -> None: self.press_key("Control+V")
    def key_ctrl_x(self) -> None: self.press_key("Control+X")
    def key_ctrl_a(self) -> None: self.press_key("Control+A")
    def key_ctrl_z(self) -> None: self.press_key("Control+Z")
    def key_ctrl_y(self) -> None: self.press_key("Control+Y")
    def key_ctrl_s(self) -> None: self.press_key("Control+S")
    def key_ctrl_p(self) -> None: self.press_key("Control+P")
    def key_alt_tab(self) -> None: self.press_key("Alt+Tab")
    def key_shift_tab(self) -> None: self.press_key("Shift+Tab")
    def key_ctrl_shift_tab(self) -> None: self.press_key("Control+Shift+Tab")
