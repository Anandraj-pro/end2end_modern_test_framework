from playwright.sync_api import Page, Locator
from utils.logger import logger

class BasePage:
    """Parent Base Page object containing generic element interactions and custom waits.
    
    Provides abstract wrappers for standard browser operations with integrated logging.
    """
    
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        """Navigates to a specific URL."""
        logger.info(f"Navigating to URL: '{url}'")
        try:
            self.page.goto(url)
            logger.debug(f"Navigation successful to '{url}'")
        except Exception as e:
            logger.error(f"Failed to navigate to '{url}'. Error: {str(e)}")
            raise e

    def click_element(self, locator: Locator):
        """Waits for and clicks a Playwright Locator element."""
        logger.info(f"Clicking element: {locator}")
        try:
            # Playwright handles auto-waiting internally, we trigger click
            locator.click()
            logger.debug(f"Successfully clicked element: {locator}")
        except Exception as e:
            logger.error(f"Failed to click element: {locator}. Error: {str(e)}")
            raise e

    def fill_input(self, locator: Locator, text: str, clear: bool = True):
        """Fills an input field. Clears existing text by default."""
        logger.info(f"Filling input element: {locator} with text")
        try:
            if clear:
                locator.clear()
            locator.fill(text)
            logger.debug(f"Successfully filled element: {locator}")
        except Exception as e:
            logger.error(f"Failed to fill input element: {locator}. Error: {str(e)}")
            raise e

    def get_element_text(self, locator: Locator) -> str:
        """Retrieves and returns the text content of a Locator element."""
        logger.info(f"Retrieving text content for element: {locator}")
        try:
            text = locator.inner_text().strip()
            logger.debug(f"Text retrieved: '{text}'")
            return text
        except Exception as e:
            logger.error(f"Failed to get text content for element: {locator}. Error: {str(e)}")
            raise e

    def is_element_visible(self, locator: Locator, timeout_ms: int = 2000) -> bool:
        """Checks if an element is visible on the page, returning a boolean."""
        logger.debug(f"Checking visibility of element: {locator}")
        try:
            # Use custom short timeout to prevent long hangs on non-present items
            return locator.is_visible(timeout=timeout_ms)
        except Exception:
            return False

    def is_element_enabled(self, locator: Locator) -> bool:
        """Checks if an element is enabled on the page, returning a boolean."""
        logger.debug(f"Checking if element is enabled: {locator}")
        try:
            return locator.is_enabled()
        except Exception:
            return False
