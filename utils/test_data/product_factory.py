from dataclasses import dataclass
from typing import Optional, List
from utils.logger import logger
from utils.test_data.base_factory import Builder, Factory


@dataclass
class Product:
    """Represents test product data."""
    name: str
    price: float
    description: str = ""

    def __repr__(self) -> str:
        return f"Product(name='{self.name}', price=${self.price})"


class ProductBuilder(Builder):
    """Builder for creating Product objects with fluent API."""

    def __init__(self):
        """Initialize product builder."""
        self.name: Optional[str] = None
        self.price: Optional[float] = None
        self.description: str = ""
        logger.debug("ProductBuilder initialized")

    def with_name(self, name: str) -> "ProductBuilder":
        """Set product name.

        Args:
            name: Product name

        Returns:
            Self for chaining
        """
        self.name = name
        return self

    def with_price(self, price: float) -> "ProductBuilder":
        """Set product price.

        Args:
            price: Product price (must be positive)

        Returns:
            Self for chaining

        Raises:
            ValueError: If price is not positive
        """
        self._validate_positive("price", price)
        self.price = price
        return self

    def with_description(self, description: str) -> "ProductBuilder":
        """Set product description.

        Args:
            description: Product description

        Returns:
            Self for chaining
        """
        self.description = description
        return self

    def build(self) -> Product:
        """Build and return Product object.

        Validates required fields before building.

        Returns:
            Constructed Product object

        Raises:
            ValueError: If required fields are missing
        """
        self._validate_required(
            name=self.name,
            price=self.price
        )

        product = Product(
            name=self.name,
            price=self.price,
            description=self.description
        )
        logger.info(f"Created product: {product}")
        return product


class ProductFactory(Factory):
    """Factory for creating Product objects with preset configurations.

    Products are based on the Sauce Demo inventory.
    """

    # SauceDemo inventory data
    _INVENTORY = {
        "backpack": ("Sauce Labs Backpack", 29.99, "Carry your entire project in this sleek comfy backpack."),
        "bike_light": ("Sauce Labs Bike Light", 9.99, "A red light isn't the desired state in testing but it sure helps when riding your bike at night."),
        "shirt": ("Sauce Labs Bolt T-Shirt", 15.99, "Get your testing superhero on with the Sauce Labs bolt T-shirt."),
        "jacket": ("Sauce Labs Fleece Jacket", 49.99, "It's not just a fleece, it's a lifestyle upgrade."),
        "onesie": ("Sauce Labs Onesie", 7.99, "Onsies are one-pieces for the whole body."),
        "tshirt": ("Test.allTheThings() T-Shirt (Red)", 15.99, "This classic Sauce Labs t-shirt is perfect for any occasion."),
    }

    @classmethod
    def builder(cls) -> ProductBuilder:
        """Create a new ProductBuilder instance.

        Returns:
            ProductBuilder for fluent configuration
        """
        return ProductBuilder()

    @classmethod
    def backpack(cls) -> Product:
        """Create Sauce Labs Backpack product.

        Returns:
            Product configured as backpack
        """
        name, price, desc = cls._INVENTORY["backpack"]
        return (ProductBuilder()
                .with_name(name)
                .with_price(price)
                .with_description(desc)
                .build())

    @classmethod
    def bike_light(cls) -> Product:
        """Create Sauce Labs Bike Light product.

        Returns:
            Product configured as bike light
        """
        name, price, desc = cls._INVENTORY["bike_light"]
        return (ProductBuilder()
                .with_name(name)
                .with_price(price)
                .with_description(desc)
                .build())

    @classmethod
    def shirt(cls) -> Product:
        """Create Sauce Labs Bolt T-Shirt product.

        Returns:
            Product configured as bolt shirt
        """
        name, price, desc = cls._INVENTORY["shirt"]
        return (ProductBuilder()
                .with_name(name)
                .with_price(price)
                .with_description(desc)
                .build())

    @classmethod
    def jacket(cls) -> Product:
        """Create Sauce Labs Fleece Jacket product.

        Returns:
            Product configured as jacket
        """
        name, price, desc = cls._INVENTORY["jacket"]
        return (ProductBuilder()
                .with_name(name)
                .with_price(price)
                .with_description(desc)
                .build())

    @classmethod
    def onesie(cls) -> Product:
        """Create Sauce Labs Onesie product.

        Returns:
            Product configured as onesie
        """
        name, price, desc = cls._INVENTORY["onesie"]
        return (ProductBuilder()
                .with_name(name)
                .with_price(price)
                .with_description(desc)
                .build())

    @classmethod
    def tshirt(cls) -> Product:
        """Create Test.allTheThings() T-Shirt product.

        Returns:
            Product configured as test t-shirt
        """
        name, price, desc = cls._INVENTORY["tshirt"]
        return (ProductBuilder()
                .with_name(name)
                .with_price(price)
                .with_description(desc)
                .build())

    @classmethod
    def all_products(cls) -> List[Product]:
        """Get all SauceDemo inventory products.

        Returns:
            List of all 6 products in SauceDemo inventory
        """
        return [
            cls.backpack(),
            cls.bike_light(),
            cls.shirt(),
            cls.jacket(),
            cls.onesie(),
            cls.tshirt(),
        ]

    @classmethod
    def custom_product(cls, name: str, price: float, description: str = "") -> Product:
        """Create a custom product.

        Convenience method for quick custom product creation.

        Args:
            name: Product name
            price: Product price
            description: Optional product description

        Returns:
            Product object with provided values
        """
        return (ProductBuilder()
                .with_name(name)
                .with_price(price)
                .with_description(description)
                .build())
