from abc import ABC, abstractmethod
from utils.logger import logger


class Builder(ABC):
    """Abstract base builder pattern for test data factories.

    Provides common validation and building patterns for all builders.
    """

    def build(self):
        """Build and return the final object.

        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement build()")

    def _validate_required(self, **fields):
        """Validate that required fields are not None.

        Args:
            **fields: Field name (key) and value (value) pairs to validate

        Raises:
            ValueError: If any required field is None
        """
        missing = [name for name, value in fields.items() if value is None]
        if missing:
            raise ValueError(f"Required field(s) missing: {', '.join(missing)}")

    def _validate_type(self, field_name: str, value, expected_type):
        """Validate that a field has the expected type.

        Args:
            field_name: Name of the field
            value: Value to check
            expected_type: Expected type or tuple of types

        Raises:
            TypeError: If value is not of expected type
        """
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Field '{field_name}' expected {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )

    def _validate_positive(self, field_name: str, value: float):
        """Validate that a numeric field is positive.

        Args:
            field_name: Name of the field
            value: Value to check

        Raises:
            ValueError: If value is not positive
        """
        if value <= 0:
            raise ValueError(f"Field '{field_name}' must be positive, got {value}")


class Factory(ABC):
    """Abstract base factory pattern for test data.

    Provides a standard interface for creating test data with builder pattern.
    """

    @classmethod
    @abstractmethod
    def builder(cls):
        """Create and return a new builder instance.

        Must be implemented by subclasses.

        Returns:
            A new Builder instance for this factory
        """
        raise NotImplementedError("Subclasses must implement builder()")
