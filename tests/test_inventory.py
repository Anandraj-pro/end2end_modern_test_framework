import os
import pytest
from utils.assertions import Assert
from utils.logger import logger

@pytest.mark.cart
@pytest.mark.regression
def test_inventory_sorting(login_page, inventory_page):
    """Verifies that products can be sorted by Name (Z to A) and Price (Low to High)."""
    logger.info("--- Starting Test: test_inventory_sorting ---")
    
    # Setup - Standard login
    login_page.navigate()
    login_page.login(
        os.getenv("DEMO_USERNAME", "standard_user"),
        os.getenv("DEMO_PASSWORD", "secret_sauce")
    )
    
    # 1. Test Sorting by Name (Z to A)
    inventory_page.sort_products_by("za")
    product_names = inventory_page.get_all_product_names()
    
    # Create sorted copy to compare
    expected_sorted_names = sorted(product_names, reverse=True)
    Assert.equal(product_names, expected_sorted_names, "Verify products list is sorted alphabetically in Z-to-A order")
    
    # 2. Test Sorting by Price (Low to High)
    inventory_page.sort_products_by("lohi")
    product_prices = inventory_page.get_all_product_prices()
    
    # Create sorted copy to compare
    expected_sorted_prices = sorted(product_prices)
    Assert.equal(product_prices, expected_sorted_prices, "Verify products list is sorted numerically in Price Low-to-High order")
    
    logger.info("--- Completed Test: test_inventory_sorting (PASSED) ---")

@pytest.mark.cart
@pytest.mark.smoke
def test_e2e_shopping_cart_checkout(login_page, inventory_page, cart_page):
    """Executes a full E2E shopping experience from adding items to cart through checkout completion."""
    logger.info("--- Starting Test: test_e2e_shopping_cart_checkout ---")
    
    # Setup - Standard login
    login_page.navigate()
    login_page.login(
        os.getenv("DEMO_USERNAME", "standard_user"),
        os.getenv("DEMO_PASSWORD", "secret_sauce")
    )
    
    # 1. Add specific products to cart
    item_one = "Sauce Labs Backpack"
    item_two = "Sauce Labs Bike Light"
    
    inventory_page.add_product_to_cart(item_one)
    Assert.equal(inventory_page.get_cart_count(), 1, "Verify shopping cart badge increments to 1")
    
    inventory_page.add_product_to_cart(item_two)
    Assert.equal(inventory_page.get_cart_count(), 2, "Verify shopping cart badge increments to 2")
    
    # 2. Open cart and verify items are present
    inventory_page.open_cart()
    cart_items = cart_page.get_cart_item_names()
    
    Assert.contains(item_one, cart_items, "Verify item 'Sauce Labs Backpack' is listed inside the checkout cart")
    Assert.contains(item_two, cart_items, "Verify item 'Sauce Labs Bike Light' is listed inside the checkout cart")
    
    # 3. Proceed to Checkout and complete info form
    cart_page.click_checkout()
    cart_page.fill_checkout_information(
        first_name="John",
        last_name="Doe",
        zip_code="90210"
    )
    
    # 4. Assert checkout overview review state redirection
    Assert.contains("/checkout-step-two.html", cart_page.page.url, "Verify checkout page path URL redirects to checkout summary step two")
    
    # 5. Finalize the order and assert success confirmation banner
    cart_page.click_finish()
    Assert.contains("/checkout-complete.html", cart_page.page.url, "Verify checkout page path URL redirects to order complete screen")
    
    complete_header_text = cart_page.get_complete_header_text()
    Assert.equal(complete_header_text, "Thank you for your order!", "Assert order completion message reads 'Thank you for your order!'")
    
    logger.info("--- Completed Test: test_e2e_shopping_cart_checkout (PASSED) ---")
