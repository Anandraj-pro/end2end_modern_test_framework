from pages.base_page import BasePage
from playwright.sync_api import Page, Locator
from utils.logger import logger

class InventoryPage(BasePage):
    """Page Object representing the SauceDemo Products/Inventory Dashboard page."""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # 1. Semantic and Structural Locators
        self.page_title = self.page.locator("span.title")
        self.shopping_cart_link = self.page.locator("a.shopping_cart_link")
        self.shopping_cart_badge = self.page.locator("span.shopping_cart_badge")
        self.sort_select = self.page.locator("[data-test='product-sort-container']")
        
        # Base selector for products list
        self._product_item = ".inventory_item"

    def get_page_title_text(self) -> str:
        """Retrieves page title text (e.g., 'Products')."""
        return self.get_element_text(self.page_title)

    def get_product_container(self, product_name: str) -> Locator:
        """Locates the unique product card container containing a specific product name."""
        # Clean locator filter logic matching exact human-visible card content
        return self.page.locator(self._product_item).filter(has_text=product_name)

    def add_product_to_cart(self, product_name: str):
        """Locates and clicks the 'Add to cart' button for a specific product card."""
        logger.info(f"Adding product to cart: '{product_name}'")
        product_card = self.get_product_container(product_name)
        add_button = product_card.get_by_role("button", name="Add to cart")
        self.click_element(add_button)
        logger.debug(f"Added product '{product_name}' successfully")

    def remove_product_from_cart(self, product_name: str):
        """Locates and clicks the 'Remove' button for a specific product card."""
        logger.info(f"Removing product from cart: '{product_name}'")
        product_card = self.get_product_container(product_name)
        remove_button = product_card.get_by_role("button", name="Remove")
        self.click_element(remove_button)
        logger.debug(f"Removed product '{product_name}' successfully")

    def get_cart_count(self) -> int:
        """Returns the current number of items displayed in the shopping cart badge."""
        if self.is_element_visible(self.shopping_cart_badge, timeout_ms=500):
            count_text = self.get_element_text(self.shopping_cart_badge)
            logger.debug(f"Current cart count in badge: {count_text}")
            return int(count_text)
        logger.debug("Cart badge is absent (0 items)")
        return 0

    def open_cart(self):
        """Clicks the shopping cart link to navigate to the cart review page."""
        logger.info("Opening shopping cart")
        self.click_element(self.shopping_cart_link)

    def sort_products_by(self, option_value: str):
        """Sorts the product list by selecting a dropdown value.
        
        Supported options:
        - 'az' : Name (A to Z)
        - 'za' : Name (Z to A)
        - 'lohi': Price (low to high)
        - 'hilo': Price (high to low)
        """
        logger.info(f"Sorting products by select option value: '{option_value}'")
        self.sort_select.select_option(value=option_value)
        logger.debug("Products sorting option selected")

    def get_all_product_names(self) -> list:
        """Retrieves and returns list of all product names currently displayed on the page."""
        name_elements = self.page.locator(".inventory_item_name").all()
        names = [el.inner_text().strip() for el in name_elements]
        logger.debug(f"Retrieved {len(names)} product names from UI")
        return names

    def get_all_product_prices(self) -> list:
        """Retrieves and returns a list of float prices for all displayed products."""
        price_elements = self.page.locator(".inventory_item_price").all()
        prices = []
        for el in price_elements:
            price_text = el.inner_text().replace("$", "").strip()
            prices.append(float(price_text))
        logger.debug(f"Retrieved {len(prices)} product prices from UI")
        return prices
