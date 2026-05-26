import time
from functools import wraps
from dataclasses import dataclass
from typing import Callable, Tuple, Type, Optional
from utils.logger import logger


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    delay_seconds: float = 1.0
    backoff_multiplier: float = 1.0
    retry_on_exceptions: Tuple[Type[Exception], ...] = (AssertionError,)

    def __repr__(self) -> str:
        return (
            f"RetryConfig(max_attempts={self.max_attempts}, "
            f"delay_seconds={self.delay_seconds}, "
            f"backoff_multiplier={self.backoff_multiplier})"
        )


def retry(
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    backoff_multiplier: float = 1.0,
    retry_on_exceptions: Tuple[Type[Exception], ...] = (AssertionError,)
) -> Callable:
    """Decorator to retry a test function on failure.

    Retries the entire test function (not individual assertions) if it fails with
    one of the specified exceptions. Useful for handling transient failures like
    network timeouts or race conditions.

    Args:
        max_attempts: Maximum number of attempts (default 3)
        delay_seconds: Initial delay between retries in seconds (default 1.0)
        backoff_multiplier: Multiplier for delay after each retry (default 1.0, no backoff)
        retry_on_exceptions: Tuple of exception types to retry on (default (AssertionError,))

    Returns:
        Decorated function that retries on failure

    Example:
        @retry(max_attempts=3, delay_seconds=2)
        def test_flaky_element(page):
            assert element.is_visible()
    """

    def decorator(func: Callable) -> Callable:
        config = RetryConfig(
            max_attempts=max_attempts,
            delay_seconds=delay_seconds,
            backoff_multiplier=backoff_multiplier,
            retry_on_exceptions=retry_on_exceptions
        )
        func._retry_config = config

        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay_seconds
            last_exception: Optional[Exception] = None

            for attempt in range(1, max_attempts + 1):
                try:
                    if attempt > 1:
                        logger.warning(
                            f"RETRY {attempt}/{max_attempts} for '{func.__name__}' "
                            f"(waiting {current_delay}s)"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff_multiplier

                    return func(*args, **kwargs)

                except retry_on_exceptions as e:
                    last_exception = e

                    if attempt == max_attempts:
                        logger.error(
                            f"Test '{func.__name__}' failed after {max_attempts} attempts. "
                            f"Final error: {str(e)}"
                        )
                        raise

                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for '{func.__name__}': "
                        f"{type(e).__name__}: {str(e)}"
                    )

            # Should not reach here, but ensure we raise if somehow loop exits
            if last_exception:
                raise last_exception

        return wrapper

    return decorator


def get_retry_config(func: Callable) -> Optional[RetryConfig]:
    """Get retry configuration from a decorated function.

    Args:
        func: Function that may have been decorated with @retry

    Returns:
        RetryConfig if function has retry configuration, None otherwise
    """
    return getattr(func, "_retry_config", None)


def has_retry_config(func: Callable) -> bool:
    """Check if a function has retry configuration.

    Args:
        func: Function to check

    Returns:
        True if function has retry configuration, False otherwise
    """
    return hasattr(func, "_retry_config")
