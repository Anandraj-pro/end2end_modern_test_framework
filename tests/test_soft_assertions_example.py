import pytest
from utils.soft_assertions import SoftAssert


@pytest.mark.regression
def test_inventory_with_soft_assertions(login_page, inventory_page):
    """Integration example: Inventory validation with soft assertions.

    Demonstrates how soft assertions collect multiple failures instead of
    failing on the first error. This allows seeing all issues in one test run.
    """
    # Setup: Login
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    # Use soft assertions to validate multiple aspects of the inventory page
    with SoftAssert("test_inventory_with_soft_assertions") as soft:
        # Check page title
        page_title = inventory_page.get_page_title_text()
        soft.equal(page_title, "Products", "Page title should be 'Products'")

        # Check that specific products exist
        product_names = inventory_page.get_all_product_names()
        soft.equal(len(product_names), 6, "Should have exactly 6 products")
        soft.contains("Sauce Labs Backpack", product_names, "Backpack should be in inventory")
        soft.contains("Sauce Labs Bike Light", product_names, "Bike Light should be in inventory")

        # Check that impossible conditions also get collected
        soft.contains("Non-existent Product", product_names, "Fake product check (will fail)")

        # Check product prices
        product_prices = inventory_page.get_all_product_prices()
        soft.equal(len(product_prices), 6, "Should have 6 product prices")
        soft.true(all(price > 0 for price in product_prices), "All prices should be positive")


@pytest.mark.regression
def test_checkout_flow_with_soft_assertions(login_page, inventory_page, cart_page):
    """Integration example: Complete checkout with soft assertions.

    Demonstrates soft assertions across multiple page objects in an E2E flow.
    """
    # Setup: Login and add products
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    inventory_page.add_product_to_cart("Sauce Labs Bike Light")

    # Open cart
    inventory_page.open_cart()

    # Verify cart contents with soft assertions
    with SoftAssert("test_checkout_flow_with_soft_assertions") as soft:
        cart_items = cart_page.get_cart_item_names()

        soft.equal(len(cart_items), 2, "Cart should contain exactly 2 items")
        soft.contains("Sauce Labs Backpack", cart_items, "Backpack should be in cart")
        soft.contains("Sauce Labs Bike Light", cart_items, "Bike Light should be in cart")
        soft.contains("Invalid Item", cart_items, "Invalid item check (will fail)")

        # Proceed through checkout
        cart_page.click_checkout()
        cart_page.fill_checkout_information("John", "Doe", "90210")

        # Final validation
        cart_page.click_finish()
        completion_header = cart_page.get_complete_header_text()
        soft.equal(
            completion_header,
            "Thank you for your order!",
            "Order completion message should appear"
        )
        soft.contains("Thank you", completion_header, "Thank you message present")


def test_soft_assertions_with_multiple_failures_demo():
    """Demonstration: Soft assertions collect multiple failures.

    This test intentionally has multiple failures to show how soft assertions
    collect them all and report them together.
    """
    with pytest.raises(AssertionError) as exc_info:
        with SoftAssert("demo_test") as soft:
            # These will all execute and be collected
            soft.equal("hello", "world", "Check 1: String comparison")
            soft.true(False, "Check 2: Boolean condition")
            soft.false(True, "Check 3: Negation")
            soft.contains("xyz", "abc", "Check 4: Substring search")

    # Verify all failures are in the error message
    error_msg = str(exc_info.value)
    assert "Check 1: String comparison" in error_msg
    assert "Check 2: Boolean condition" in error_msg
    assert "Check 3: Negation" in error_msg
    assert "Check 4: Substring search" in error_msg
    assert "4 failures" in error_msg
