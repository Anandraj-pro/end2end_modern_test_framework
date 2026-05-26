import pytest
from utils.test_data import UserFactory, ProductFactory


@pytest.mark.regression
def test_login_with_factory_user(login_page, inventory_page):
    """Integration example: Login using factory-generated user data.

    Demonstrates using UserFactory to create test users instead of hardcoded values.
    """
    # Create user with builder pattern
    user = (UserFactory.builder()
            .with_first_name("TestUser")
            .with_last_name("Demo")
            .with_zip_code("55555")
            .build())

    # Use factory-created user for login
    login_page.navigate()
    login_page.login(user.username, user.password)

    # Verify successful login
    page_title = inventory_page.get_page_title_text()
    assert page_title == "Products"


@pytest.mark.regression
def test_login_with_preset_user(login_page, inventory_page):
    """Integration example: Login using preset factory user.

    Demonstrates using factory preset builders for convenience.
    """
    # Use preset factory user
    user = UserFactory.standard_user()

    login_page.navigate()
    login_page.login(user.username, user.password)

    page_title = inventory_page.get_page_title_text()
    assert page_title == "Products"


@pytest.mark.regression
def test_login_with_locked_user_preset(login_page):
    """Integration example: Test locked user login with factory preset.

    Demonstrates using factory presets to test error scenarios.
    """
    # Use locked user preset for testing error handling
    user = UserFactory.locked_user()

    login_page.navigate()
    login_page.login(user.username, user.password)

    # Verify error message appears for locked user
    error_message = login_page.get_error_message()
    assert "locked out" in error_message.lower()


@pytest.mark.regression
def test_checkout_with_factory_data(login_page, inventory_page, cart_page):
    """Integration example: Complete checkout with factory-generated user data.

    Demonstrates using both user and product factories in an E2E flow.
    """
    # Create custom user with builder
    user = (UserFactory.builder()
            .with_first_name("Alice")
            .with_last_name("Wonder")
            .with_zip_code("90210")
            .build())

    # Get products using factory presets
    backpack = ProductFactory.backpack()
    bike_light = ProductFactory.bike_light()

    # Execute checkout flow
    login_page.navigate()
    login_page.login(user.username, user.password)

    inventory_page.add_product_to_cart(backpack.name)
    inventory_page.add_product_to_cart(bike_light.name)
    inventory_page.open_cart()

    cart_items = cart_page.get_cart_item_names()
    assert backpack.name in cart_items
    assert bike_light.name in cart_items

    cart_page.click_checkout()
    cart_page.fill_checkout_information(
        user.first_name,
        user.last_name,
        user.zip_code
    )

    cart_page.click_finish()
    completion_header = cart_page.get_complete_header_text()
    assert "Thank you" in completion_header


@pytest.mark.regression
def test_add_multiple_products_from_factory(login_page, inventory_page, cart_page):
    """Integration example: Add multiple products using factory to cart.

    Demonstrates using ProductFactory.all_products() for inventory validation.
    """
    user = UserFactory.standard_user()

    login_page.navigate()
    login_page.login(user.username, user.password)

    # Get all products from factory
    all_products = ProductFactory.all_products()

    # Add first 3 products to cart
    for product in all_products[:3]:
        inventory_page.add_product_to_cart(product.name)

    # Verify cart has 3 items
    cart_count = inventory_page.get_cart_count()
    assert cart_count == 3


@pytest.mark.regression
def test_fixture_injection_of_factory_data(
    login_page,
    inventory_page,
    standard_user_data,
    sample_products_data
):
    """Integration example: Use fixture injection of factory data.

    Demonstrates using @pytest.fixture injected factory data directly in tests.
    """
    # standard_user_data and sample_products_data come from conftest.py fixtures
    login_page.navigate()
    login_page.login(standard_user_data.username, standard_user_data.password)

    # Verify all 6 products are in inventory
    all_products = inventory_page.get_all_product_names()
    assert len(all_products) == len(sample_products_data)

    for product in sample_products_data:
        assert product.name in all_products


@pytest.mark.regression
def test_custom_product_factory(login_page, inventory_page):
    """Integration example: Create custom products with factory.

    Demonstrates using ProductFactory.custom_product() for ad-hoc creation.
    """
    # Create a custom product (not in standard inventory)
    custom = ProductFactory.custom_product(
        name="Sauce Labs Backpack",  # Using existing name for test
        price=29.99,
        description="Custom test product"
    )

    user = UserFactory.standard_user()

    login_page.navigate()
    login_page.login(user.username, user.password)

    # Verify custom product exists in inventory
    all_products = inventory_page.get_all_product_names()
    assert custom.name in all_products


@pytest.mark.regression
def test_multiple_users_in_sequence(login_page, inventory_page):
    """Integration example: Test login with multiple different users.

    Demonstrates creating and using multiple factory users in sequence.
    """
    user1 = UserFactory.standard_user()
    user2 = UserFactory.test_user("Jane", "Doe", "67890")

    # Test user 1 login
    login_page.navigate()
    login_page.login(user1.username, user1.password)
    assert inventory_page.get_page_title_text() == "Products"

    # Log out by refreshing (simple approach for this demo)
    login_page.navigate()

    # Note: In a real scenario, you'd have a logout action
    # For now, we're just re-navigating to login page
    # Test user 2 login
    login_page.login(user2.username, user2.password)
    assert inventory_page.get_page_title_text() == "Products"
