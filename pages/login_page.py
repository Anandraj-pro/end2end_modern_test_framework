from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import logger

class LoginPage(BasePage):
    """Page Object representing the SauceDemo Login Page.
    
    Uses Playwright's modern semantic user-facing locators (by role, placeholder).
    """
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # 1. Semantic Locators
        self.username_input = self.page.get_by_placeholder("Username")
        self.password_input = self.page.get_by_placeholder("Password")
        self.login_button = self.page.get_by_role("button", name="Login")
        
        # Fallback locator for testing specific attributes
        self.error_message_container = self.page.locator("[data-test='error']")

    def navigate(self):
        """Navigates to SauceDemo site."""
        self.navigate_to("https://www.saucedemo.com/")

    def login(self, username: str, password: str):
        """Executes a standard user login flow."""
        logger.info(f"Attempting to login user: '{username}'")
        self.fill_input(self.username_input, username)
        self.fill_input(self.password_input, password)
        self.click_element(self.login_button)
        logger.info(f"Login action completed for user: '{username}'")

    def get_error_message(self) -> str:
        """Retrieves active validation error text on login screen."""
        if self.is_element_visible(self.error_message_container):
            return self.get_element_text(self.error_message_container)
        return ""
