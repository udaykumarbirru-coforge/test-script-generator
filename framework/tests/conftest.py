import pytest
from playwright.sync_api import Page

pytest_plugins = ["framework.core.execution_hooks"]


@pytest.fixture
def app_page(page: Page) -> Page:
    page.set_default_timeout(10_000)
    return page
