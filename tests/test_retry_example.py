import pytest
from utils.retry_manager import retry
from utils.test_data import UserFactory


@retry(max_attempts=3, delay_seconds=1)
@pytest.mark.regression
def test_successful_login_with_retry(login_page, inventory_page):
    """Integration example: Login test with automatic retry.

    Demonstrates using @retry decorator on E2E tests to handle transient failures.
    If this test fails, it will automatically retry up to 3 times.
    """
    user = UserFactory.standard_user()

    login_page.navigate()
    login_page.login(user.username, user.password)

    page_title = inventory_page.get_page_title_text()
    assert page_title == "Products"


@retry(max_attempts=2, delay_seconds=0.5)
@pytest.mark.regression
def test_add_product_with_retry(login_page, inventory_page):
    """Integration example: Add product test with retry.

    Tests adding products to cart with automatic retry capability.
    Useful for tests that may occasionally timeout due to network delays.
    """
    user = UserFactory.standard_user()

    login_page.navigate()
    login_page.login(user.username, user.password)

    product = "Sauce Labs Backpack"
    inventory_page.add_product_to_cart(product)

    cart_count = inventory_page.get_cart_count()
    assert cart_count == 1


@retry(max_attempts=3, delay_seconds=1, backoff_multiplier=1.5)
@pytest.mark.regression
def test_sorting_products_with_backoff_retry(login_page, inventory_page):
    """Integration example: Product sorting with exponential backoff retry.

    Demonstrates using backoff_multiplier to increase delay between retries.
    Useful for rate-limited or heavily loaded environments.
    """
    user = UserFactory.standard_user()

    login_page.navigate()
    login_page.login(user.username, user.password)

    # Test Z-A sorting
    inventory_page.sort_products_by("za")
    sorted_names = inventory_page.get_all_product_names()

    # Verify correct sort order (just check first product)
    assert "Test.allTheThings()" in sorted_names[0]


@retry(max_attempts=3, delay_seconds=0.5)
@pytest.mark.regression
def test_complete_checkout_with_retry(login_page, inventory_page, cart_page):
    """Integration example: Complete checkout flow with automatic retry.

    Demonstrates retry on multi-step E2E flows that may have intermittent failures.
    """
    user = UserFactory.standard_user()
    backpack = "Sauce Labs Backpack"
    bike_light = "Sauce Labs Bike Light"

    login_page.navigate()
    login_page.login(user.username, user.password)

    inventory_page.add_product_to_cart(backpack)
    inventory_page.add_product_to_cart(bike_light)

    inventory_page.open_cart()

    cart_items = cart_page.get_cart_item_names()
    assert len(cart_items) == 2
    assert backpack in cart_items
    assert bike_light in cart_items

    cart_page.click_checkout()
    cart_page.fill_checkout_information("John", "Doe", "12345")

    cart_page.click_finish()
    completion_header = cart_page.get_complete_header_text()
    assert "Thank you" in completion_header


@retry(max_attempts=3)
@pytest.mark.regression
def test_error_path_with_locked_user_retry(login_page):
    """Integration example: Error path test with retry.

    Demonstrates retry on tests that validate error scenarios.
    Useful when error page rendering is occasionally slow.
    """
    user = UserFactory.locked_user()

    login_page.navigate()
    login_page.login(user.username, user.password)

    error_message = login_page.get_error_message()
    assert "locked out" in error_message.lower()


class TestRetryableE2EScenarios:
    """Collection of retryable E2E test scenarios."""

    @retry(max_attempts=2, delay_seconds=0.5)
    def test_inventory_page_load_with_retry(self, login_page, inventory_page):
        """Test that retries if inventory page loading is slow."""
        user = UserFactory.standard_user()

        login_page.navigate()
        login_page.login(user.username, user.password)

        # If page load is occasionally slow, retry will help
        products = inventory_page.get_all_product_names()
        assert len(products) == 6

    @retry(max_attempts=3, delay_seconds=1)
    def test_multiple_add_to_cart_with_retry(self, login_page, inventory_page):
        """Test adding multiple items with retry for transient failures."""
        user = UserFactory.standard_user()

        login_page.navigate()
        login_page.login(user.username, user.password)

        items = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]

        for item in items:
            inventory_page.add_product_to_cart(item)

        cart_count = inventory_page.get_cart_count()
        assert cart_count == 3


# Example: How to use retry with soft assertions (from Phase 1)
@retry(max_attempts=2, delay_seconds=1)
def test_inventory_validation_with_retry_and_soft_assertions(login_page, inventory_page):
    """Integration example: Retry + Soft Assertions together.

    Demonstrates combining retry mechanism with soft assertions from Phase 1.
    """
    from utils.soft_assertions import SoftAssert

    user = UserFactory.standard_user()

    login_page.navigate()
    login_page.login(user.username, user.password)

    products = inventory_page.get_all_product_names()

    # Use soft assertions to collect all validation failures
    with SoftAssert("test_inventory_validation") as soft:
        soft.equal(len(products), 6, "Should have 6 products")
        soft.contains("Sauce Labs Backpack", products, "Backpack should exist")
        soft.contains("Sauce Labs Bike Light", products, "Bike Light should exist")


# Example: Retry with custom exception handling
@retry(
    max_attempts=3,
    delay_seconds=1,
    retry_on_exceptions=(AssertionError, TimeoutError)
)
def test_element_visibility_with_timeout_retry(login_page, inventory_page):
    """Integration example: Retry on both AssertionError and TimeoutError.

    Useful when tests may timeout occasionally due to slow element loading.
    """
    user = UserFactory.standard_user()

    login_page.navigate()
    login_page.login(user.username, user.password)

    # This could occasionally timeout if element loading is slow
    page_title = inventory_page.get_page_title_text()
    assert page_title == "Products"
