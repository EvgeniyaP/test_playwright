import re
import allure
from playwright.sync_api import Page, expect


def test_has_title(page: Page):
    with allure.step("Check that Playwright page has title 'Playwright'"):
        page.goto("https://playwright.dev/")
        expect(page).to_have_title(re.compile("Playwright"))
        page.get_by_role("link", name="Get started").click()
