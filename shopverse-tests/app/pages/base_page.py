from playwright.sync_api import Page

from framework.core.actions import PlaywrightActions, RuntimeHealingHook

class BasePage:
    def __init__(self, page: Page, healer: RuntimeHealingHook | None = None) -> None:
        self.page = page
        self.actions = PlaywrightActions(page, healer=healer)

    def open(self, url: str) -> None:
        self.actions.goto(url)

    def title(self) -> str:
        return self.page.title()
