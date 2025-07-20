import time
from typing import Any

from playwright.sync_api import Browser
from playwright.sync_api import BrowserContext
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page
from playwright.sync_api import sync_playwright

from meroshare_bot import logger
from meroshare_bot.models import Account


class Playwright:
    def __init__(self, account: Account, apply_all: bool):
        self.start_time = time.time()
        self.account = Account(
            name=account.name,
            capital_id=account.capital_id,
            username=account.username,
            password=account.password,
            quantity=account.quantity,
            crn_number=account.crn_number,
            bank=account.bank,
            transcation_pin=account.transcation_pin,
        )
        self.filter_ordinary_share = not apply_all

    def login_meroshare(self, page: Page):
        if page.url == "about:blank":
            logger.info("Opening meroshare page...")
            page.goto(
                "https://meroshare.cdsc.com.np",
                wait_until="networkidle",
            )
            cdsc_copyright_text = page.locator(".copyright").all_inner_texts()
            if cdsc_copyright_text:
                if any(
                    "CDS and Clearing Limited" in text
                    for text in cdsc_copyright_text
                ):
                    logger.info("Successfully reached login page...")
                    logger.info("Logging in...")
                    time.sleep(1)

                    logger.info("Selecting branch...")
                    page.click("#selectBranch")
                    time.sleep(1)

                    logger.info("Entering branch id...")
                    page.fill(
                        ".select2-search__field", self.account.capital_id
                    )
                    page.wait_for_selector("li.select2-results__option")
                    page.click("li.select2-results__option")

                    logger.info("Entering Username...")
                    page.get_by_label("Username").fill(self.account.username)
                    time.sleep(1)

                    logger.info("Entering Password...")
                    page.get_by_label("Password").fill(self.account.password)
                    time.sleep(1)

                    logger.info("Loggin in...")
                    page.click(".sign-in")
                    time.sleep(3)
                    return True

        return False

    def goto_asba(self, page: Page):
        asba = page.locator("#sideBar nav ul li:nth-child(8) a")
        if not any(" My ASBA" in text for text in asba.all_inner_texts()):
            logger.error(f"Login failed for {self.account.name}")
            return False

        logger.info(f"Successfully logged in {self.account.name}")
        logger.info("Clicking on My ASBA...")
        asba.click()
        time.sleep(2)
        return True

    def get_issues_list(self, page: Page):
        apply_for_issue = page.query_selector_all(".company-list")
        issue_list = [
            issue.inner_text().split("\n") for issue in apply_for_issue
        ]
        filtered_list = [
            (index, issue)
            for index, issue in enumerate(issue_list)
            if (
                not self.filter_ordinary_share or issue[4] == "Ordinary Shares"
            )
            and len(issue) > 5
            and issue[5] == "Apply"
        ]
        return filtered_list, len(issue_list)

    def select_issue(
        self, page: Page, issues_list: list[Any], total_issues: int
    ):
        issue_selector_index = (
            "" if total_issues == 1 else "[{}]".format(issues_list[0][0] + 1)
        )

        xpath_string = (
            '//*[@id="main"]/div/app-asba/div/div[2]/app-applicable-issue/div/div/div/div/div'
            + issue_selector_index
            + "/div/div[2]/div/div[4]/button"
        )

        apply_btn = page.query_selector(f"xpath ={xpath_string}")
        time.sleep(1)
        if apply_btn:
            apply_btn.click()
        logger.info(f"Successfully selected {issues_list[0][1][0]} to apply")
        time.sleep(1)
        return True

    def apply_share(self, page: Page):
        logger.info("Selecting Bank ...")
        page.locator("#selectBank").select_option(self.account.bank)
        time.sleep(1)

        logger.info("Selecting account number...")
        page.locator("#accountNumber").select_option(index=1)
        time.sleep(1)

        logger.info("Selecting applied kitta...")
        page.locator("#appliedKitta").fill(self.account.quantity)
        time.sleep(1)

        logger.info("Selecting crn number...")
        page.locator("#crnNumber").fill(self.account.crn_number)
        time.sleep(1)

        logger.info("Selecting disclaimer...")
        page.locator("#disclaimer").click()
        time.sleep(1)

        logger.info("Selecting proceed...")
        page.get_by_role("button", name="Proceed").click()

        logger.info("Selecting transaction pin...")
        page.locator("#transactionPIN").fill(self.account.transcation_pin)

        time.sleep(1)
        logger.info("Selecting apply button...")
        page.get_by_role("button", name="Apply").click()
        time.sleep(1)
        return True

    def launch_playwright(
        self,
    ) -> bool:
        browser: Browser | None = None
        context: BrowserContext | None = None
        page: Page | None = None
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=False,
                    slow_mo=1,
                    args=["--window-position=0,0"],
                )
                context = browser.new_context(
                    viewport={"width": 1040, "height": 720},
                    device_scale_factor=1.0,
                )
                page = context.new_page()
                if browser and page:
                    login = self.login_meroshare(page)
                    if not login:
                        logger.error(f"Unable to login {self.account.name}")
                        return False
                    asba = self.goto_asba(page)
                    if not asba:
                        return False
                    issues_list, total_issues = self.get_issues_list(page)
                    if not len(issues_list) > 0:
                        logger.error(
                            f"No ipo found to apply for user: {self.account.name}"
                        )
                        logger.info("Exiting...")
                        return False
                    select_issue = self.select_issue(
                        page, issues_list, total_issues
                    )
                    if not select_issue:
                        return False
                    if self.apply_share(page):
                        logger.info(
                            f"Successfully applied share of {issues_list[0][1][0]} for {self.account.name}"
                        )
                        return True

        except PlaywrightError as e:
            logger.exception(f"Playwright error: {e}")
        except Exception as e:
            logger.exception(f"Error: during account creation {e}")
        finally:
            try:
                if page and not page.is_closed():
                    page.close()
                if context:
                    context.close()
                if browser:
                    browser.close()
            except Exception as e:
                if "Is Playwright already stopped?" in str(e):
                    pass
                else:
                    logger.info(
                        f"\033[31mError\033[0m during cleanup: May be event loop was already closed {e}"
                    )
        return False
