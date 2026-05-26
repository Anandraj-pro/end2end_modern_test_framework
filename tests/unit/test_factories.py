import pytest
from utils.test_data import UserFactory, User, ProductFactory, Product


class TestUserFactory:
    """Test UserFactory and UserBuilder."""

    def test_builder_creates_user_with_custom_values(self):
        """Verify builder creates user with provided values."""
        user = (UserFactory.builder()
                .with_first_name("Jane")
                .with_last_name("Smith")
                .with_zip_code("90210")
                .build())

        assert user.first_name == "Jane"
        assert user.last_name == "Smith"
        assert user.zip_code == "90210"
        assert user.username == "standard_user"  # Default
        assert user.password == "secret_sauce"   # Default

    def test_builder_allows_custom_username_and_password(self):
        """Verify builder accepts custom credentials."""
        user = (UserFactory.builder()
                .with_first_name("Test")
                .with_last_name("User")
                .with_zip_code("12345")
                .with_username("custom_user")
                .with_password("custom_pass")
                .build())

        assert user.username == "custom_user"
        assert user.password == "custom_pass"

    def test_builder_requires_first_name(self):
        """Verify builder requires first_name."""
        with pytest.raises(ValueError, match="first_name"):
            UserFactory.builder().with_last_name("Smith").with_zip_code("12345").build()

    def test_builder_requires_last_name(self):
        """Verify builder requires last_name."""
        with pytest.raises(ValueError, match="last_name"):
            UserFactory.builder().with_first_name("Jane").with_zip_code("12345").build()

    def test_builder_requires_zip_code(self):
        """Verify builder requires zip_code."""
        with pytest.raises(ValueError, match="zip_code"):
            UserFactory.builder().with_first_name("Jane").with_last_name("Smith").build()

    def test_builder_fluent_chaining(self):
        """Verify fluent API allows method chaining."""
        user = (UserFactory.builder()
                .with_first_name("Alice")
                .with_last_name("Wonder")
                .with_zip_code("99999")
                .with_username("alice")
                .with_password("secret")
                .build())

        assert user.first_name == "Alice"
        assert user.username == "alice"

    def test_standard_user_preset(self):
        """Verify standard_user preset creates expected user."""
        user = UserFactory.standard_user()

        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.zip_code == "12345"
        assert user.username == "standard_user"
        assert user.password == "secret_sauce"
        assert isinstance(user, User)

    def test_locked_user_preset(self):
        """Verify locked_user preset creates locked user."""
        user = UserFactory.locked_user()

        assert user.first_name == "Locked"
        assert user.last_name == "User"
        assert user.username == "locked_out_user"
        assert user.password == "secret_sauce"

    def test_admin_user_preset(self):
        """Verify admin_user preset creates admin user."""
        user = UserFactory.admin_user()

        assert user.first_name == "Admin"
        assert user.username == "admin_user"
        assert user.password == "admin_pass"

    def test_test_user_convenience_method(self):
        """Verify test_user convenience method."""
        user = UserFactory.test_user("Bob", "Builder", "54321")

        assert user.first_name == "Bob"
        assert user.last_name == "Builder"
        assert user.zip_code == "54321"
        assert user.username == "standard_user"  # Default

    def test_user_repr(self):
        """Verify User string representation."""
        user = UserFactory.standard_user()
        repr_str = repr(user)

        assert "User" in repr_str
        assert "standard_user" in repr_str
        assert "John" in repr_str


class TestProductFactory:
    """Test ProductFactory and ProductBuilder."""

    def test_builder_creates_product_with_custom_values(self):
        """Verify builder creates product with provided values."""
        product = (ProductFactory.builder()
                   .with_name("Custom Product")
                   .with_price(19.99)
                   .with_description("A custom test product")
                   .build())

        assert product.name == "Custom Product"
        assert product.price == 19.99
        assert product.description == "A custom test product"

    def test_builder_requires_name(self):
        """Verify builder requires name."""
        with pytest.raises(ValueError, match="name"):
            ProductFactory.builder().with_price(10.0).build()

    def test_builder_requires_price(self):
        """Verify builder requires price."""
        with pytest.raises(ValueError, match="price"):
            ProductFactory.builder().with_name("Test").build()

    def test_builder_requires_positive_price(self):
        """Verify builder validates price is positive."""
        with pytest.raises(ValueError, match="positive"):
            ProductFactory.builder().with_name("Test").with_price(0).build()

        with pytest.raises(ValueError, match="positive"):
            ProductFactory.builder().with_name("Test").with_price(-5.0).build()

    def test_builder_allows_empty_description(self):
        """Verify builder allows empty description."""
        product = (ProductFactory.builder()
                   .with_name("Product")
                   .with_price(10.0)
                   .build())

        assert product.description == ""

    def test_backpack_preset(self):
        """Verify backpack preset."""
        product = ProductFactory.backpack()

        assert product.name == "Sauce Labs Backpack"
        assert product.price == 29.99
        assert isinstance(product, Product)

    def test_bike_light_preset(self):
        """Verify bike_light preset."""
        product = ProductFactory.bike_light()

        assert product.name == "Sauce Labs Bike Light"
        assert product.price == 9.99

    def test_shirt_preset(self):
        """Verify shirt preset."""
        product = ProductFactory.shirt()

        assert product.name == "Sauce Labs Bolt T-Shirt"
        assert product.price == 15.99

    def test_jacket_preset(self):
        """Verify jacket preset."""
        product = ProductFactory.jacket()

        assert product.name == "Sauce Labs Fleece Jacket"
        assert product.price == 49.99

    def test_onesie_preset(self):
        """Verify onesie preset."""
        product = ProductFactory.onesie()

        assert product.name == "Sauce Labs Onesie"
        assert product.price == 7.99

    def test_tshirt_preset(self):
        """Verify tshirt preset."""
        product = ProductFactory.tshirt()

        assert product.name == "Test.allTheThings() T-Shirt (Red)"
        assert product.price == 15.99

    def test_all_products(self):
        """Verify all_products returns all inventory items."""
        products = ProductFactory.all_products()

        assert len(products) == 6
        product_names = [p.name for p in products]
        assert "Sauce Labs Backpack" in product_names
        assert "Sauce Labs Bike Light" in product_names
        assert all(isinstance(p, Product) for p in products)

    def test_custom_product_convenience_method(self):
        """Verify custom_product convenience method."""
        product = ProductFactory.custom_product("Special Item", 39.99, "Special product")

        assert product.name == "Special Item"
        assert product.price == 39.99
        assert product.description == "Special product"

    def test_product_repr(self):
        """Verify Product string representation."""
        product = ProductFactory.backpack()
        repr_str = repr(product)

        assert "Product" in repr_str
        assert "Backpack" in repr_str
        assert "29.99" in repr_str


class TestFactoryIntegration:
    """Integration tests for factories working together."""

    def test_create_user_and_product_together(self):
        """Verify creating user and product in same test."""
        user = UserFactory.standard_user()
        product = ProductFactory.backpack()

        assert user.username == "standard_user"
        assert product.name == "Sauce Labs Backpack"

    def test_multiple_users_with_different_presets(self):
        """Verify creating multiple users with different presets."""
        standard = UserFactory.standard_user()
        locked = UserFactory.locked_user()
        admin = UserFactory.admin_user()

        assert standard.username == "standard_user"
        assert locked.username == "locked_out_user"
        assert admin.username == "admin_user"

    def test_multiple_products_from_inventory(self):
        """Verify creating multiple products."""
        backpack = ProductFactory.backpack()
        light = ProductFactory.bike_light()
        shirt = ProductFactory.shirt()

        products = [backpack, light, shirt]
        prices = [p.price for p in products]

        assert 29.99 in prices
        assert 9.99 in prices
        assert 15.99 in prices
