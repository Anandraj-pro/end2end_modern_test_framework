from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import logger

class CartPage(BasePage):
    """Page Object representing the SauceDemo Checkout, Info input, and completion screens."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # 1. Cart Page Locators
        self.checkout_button = self.page.get_by_role("button", name="Checkout")
        
        # 2. Checkout Information Form Locators
        self.first_name_input = self.page.get_by_placeholder("First Name")
        self.last_name_input = self.page.get_by_placeholder("Last Name")
        self.zip_code_input = self.page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = self.page.get_by_role("button", name="Continue")
        
        # 3. Checkout Overview Locators
        self.finish_button = self.page.get_by_role("button", name="Finish")
        
        # 4. Checkout Complete Locators
        self.complete_header = self.page.locator("h2.complete-header")
        
        # General selectors
        self._cart_item_name = ".inventory_item_name"

    def get_cart_item_names(self) -> list:
        """Retrieves and returns all product names currently listed in the cart."""
        item_elements = self.page.locator(self._cart_item_name).all()
        names = [el.inner_text().strip() for el in item_elements]
        logger.debug(f"Retrieved {len(names)} item names from checkout cart")
        return names

    def click_checkout(self):
        """Clicks the Checkout button in the cart screen."""
        logger.info("Proceeding to checkout")
        self.click_element(self.checkout_button)

    def fill_checkout_information(self, first_name: str, last_name: str, zip_code: str):
        """Fills the checkout profile details form and clicks Continue."""
        logger.info(f"Filling checkout info form. Profile: '{first_name} {last_name}, {zip_code}'")
        self.fill_input(self.first_name_input, first_name)
        self.fill_input(self.last_name_input, last_name)
        self.fill_input(self.zip_code_input, zip_code)
        self.click_element(self.continue_button)
        logger.debug("Checkout info form submitted successfully")

    def click_finish(self):
        """Clicks the Finish button to complete checkout overview."""
        logger.info("Finalizing order - clicking Finish")
        self.click_element(self.finish_button)

    def get_complete_header_text(self) -> str:
        """Retrieves order completion confirmation header text."""
        return self.get_element_text(self.complete_header)
