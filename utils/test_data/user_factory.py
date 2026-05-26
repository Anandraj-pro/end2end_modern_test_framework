from dataclasses import dataclass
from typing import Optional
from utils.logger import logger
from utils.test_data.base_factory import Builder, Factory


@dataclass
class User:
    """Represents test user data."""
    first_name: str
    last_name: str
    zip_code: str
    username: str
    password: str

    def __repr__(self) -> str:
        return f"User(username='{self.username}', name='{self.first_name} {self.last_name}')"


class UserBuilder(Builder):
    """Builder for creating User objects with fluent API.

    Supports building custom users or using preset configurations.
    """

    def __init__(self):
        """Initialize user builder with sensible defaults."""
        self.first_name: Optional[str] = None
        self.last_name: Optional[str] = None
        self.zip_code: Optional[str] = None
        self.username: str = "standard_user"
        self.password: str = "secret_sauce"
        logger.debug("UserBuilder initialized with default username='standard_user'")

    def with_first_name(self, name: str) -> "UserBuilder":
        """Set user's first name.

        Args:
            name: First name

        Returns:
            Self for chaining
        """
        self.first_name = name
        return self

    def with_last_name(self, name: str) -> "UserBuilder":
        """Set user's last name.

        Args:
            name: Last name

        Returns:
            Self for chaining
        """
        self.last_name = name
        return self

    def with_zip_code(self, zip_code: str) -> "UserBuilder":
        """Set user's zip code.

        Args:
            zip_code: Zip code

        Returns:
            Self for chaining
        """
        self.zip_code = zip_code
        return self

    def with_username(self, username: str) -> "UserBuilder":
        """Set user's username.

        Args:
            username: Username for login

        Returns:
            Self for chaining
        """
        self.username = username
        return self

    def with_password(self, password: str) -> "UserBuilder":
        """Set user's password.

        Args:
            password: Password for login

        Returns:
            Self for chaining
        """
        self.password = password
        return self

    def build(self) -> User:
        """Build and return User object.

        Validates required fields before building.

        Returns:
            Constructed User object

        Raises:
            ValueError: If required fields are missing
        """
        self._validate_required(
            first_name=self.first_name,
            last_name=self.last_name,
            zip_code=self.zip_code
        )

        user = User(
            first_name=self.first_name,
            last_name=self.last_name,
            zip_code=self.zip_code,
            username=self.username,
            password=self.password
        )
        logger.info(f"Created user: {user}")
        return user


class UserFactory(Factory):
    """Factory for creating User objects with preset configurations."""

    @classmethod
    def builder(cls) -> UserBuilder:
        """Create a new UserBuilder instance.

        Returns:
            UserBuilder for fluent configuration
        """
        return UserBuilder()

    @classmethod
    def standard_user(cls) -> User:
        """Create a standard test user.

        Pre-configured with typical test values:
        - username: standard_user
        - password: secret_sauce
        - name: John Doe
        - zip: 12345

        Returns:
            User object configured as standard test user
        """
        return (UserBuilder()
                .with_first_name("John")
                .with_last_name("Doe")
                .with_zip_code("12345")
                .build())

    @classmethod
    def locked_user(cls) -> User:
        """Create a locked-out test user.

        Pre-configured for testing locked user scenarios:
        - username: locked_out_user
        - password: secret_sauce
        - name: Locked User
        - zip: 00000

        Returns:
            User object configured as locked user
        """
        return (UserBuilder()
                .with_username("locked_out_user")
                .with_password("secret_sauce")
                .with_first_name("Locked")
                .with_last_name("User")
                .with_zip_code("00000")
                .build())

    @classmethod
    def admin_user(cls) -> User:
        """Create an admin test user.

        Pre-configured for admin scenarios:
        - username: admin_user
        - password: admin_pass
        - name: Admin User
        - zip: 10000

        Returns:
            User object configured as admin
        """
        return (UserBuilder()
                .with_username("admin_user")
                .with_password("admin_pass")
                .with_first_name("Admin")
                .with_last_name("User")
                .with_zip_code("10000")
                .build())

    @classmethod
    def test_user(cls, first_name: str, last_name: str, zip_code: str) -> User:
        """Create a test user with custom values.

        Convenience method for quick custom user creation.

        Args:
            first_name: User's first name
            last_name: User's last name
            zip_code: User's zip code

        Returns:
            User object with provided values and default credentials
        """
        return (UserBuilder()
                .with_first_name(first_name)
                .with_last_name(last_name)
                .with_zip_code(zip_code)
                .build())
