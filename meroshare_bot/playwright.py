import time

from playwright.sync_api import Browser
from playwright.sync_api import BrowserContext
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page
from playwright.sync_api import sync_playwright

from meroshare_bot import logger
from meroshare_bot.models import Account


class Playwright:
    def __init__(self, account: Account):
        self.start_time = time.time()
        self.account = Account(
            name=account.name,
            capital_id=account.capital_id,
            username=account.username,
            password=account.password,
            quantity=account.quantity,
            crn_number=account.crn_number,
        )

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

        return False

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
                        logger.info("Unable to login...")
                        return False

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
