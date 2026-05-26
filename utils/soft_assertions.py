from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional
from playwright.sync_api import Locator
from utils.logger import logger


@dataclass
class SoftAssertionFailure:
    """Represents a single failed soft assertion."""
    message: str
    expected: Any
    actual: Any
    assertion_type: str
    timestamp: str


class SoftAssert:
    """Context manager for collecting multiple assertion failures.

    Allows tests to collect all assertion failures instead of stopping at the first failure.
    All failures are reported at the end when exiting the context.

    Example:
        with SoftAssert("test_name") as soft:
            soft.equal(actual, expected, "Check 1")
            soft.equal(a, b, "Check 2")  # Continues even if check 1 fails
    """

    def __init__(self, test_name: str):
        """Initialize soft assertion context.

        Args:
            test_name: Name of the test for logging purposes
        """
        self.test_name = test_name
        self.failures: List[SoftAssertionFailure] = []
        self.passed_count = 0

    def __enter__(self):
        """Enter context manager."""
        logger.info(f"Starting soft assertions for '{self.test_name}'")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager and raise AssertionError if any failures occurred."""
        summary = f"Soft assertion summary: {self.passed_count} passed, {len(self.failures)} failed"
        logger.info(summary)

        if self.failures:
            formatted_failures = "\n".join(
                f"  [{i+1}] {f.message}\n"
                f"       Expected: {f.expected}\n"
                f"       Actual: {f.actual}"
                for i, f in enumerate(self.failures)
            )
            error_message = (
                f"Soft assertions failed for '{self.test_name}' ({len(self.failures)} failures):\n"
                f"{formatted_failures}"
            )
            logger.error(error_message)
            raise AssertionError(error_message)

        return False

    def equal(self, actual: Any, expected: Any, message: str) -> None:
        """Assert that actual equals expected (soft assertion).

        Args:
            actual: Actual value
            expected: Expected value
            message: Assertion description
        """
        if actual == expected:
            self.passed_count += 1
            logger.info(f"[SOFT PASS] {message} ✓")
        else:
            failure = SoftAssertionFailure(
                message=message,
                expected=expected,
                actual=actual,
                assertion_type="equal",
                timestamp=datetime.now().isoformat()
            )
            self.failures.append(failure)
            logger.error(f"[SOFT FAIL] {message}: Expected {expected}, got {actual}")

    def true(self, condition: bool, message: str) -> None:
        """Assert that condition is True (soft assertion).

        Args:
            condition: Condition to check
            message: Assertion description
        """
        if condition:
            self.passed_count += 1
            logger.info(f"[SOFT PASS] {message} ✓")
        else:
            failure = SoftAssertionFailure(
                message=message,
                expected=True,
                actual=False,
                assertion_type="true",
                timestamp=datetime.now().isoformat()
            )
            self.failures.append(failure)
            logger.error(f"[SOFT FAIL] {message}: Expected True, got False")

    def false(self, condition: bool, message: str) -> None:
        """Assert that condition is False (soft assertion).

        Args:
            condition: Condition to check
            message: Assertion description
        """
        if not condition:
            self.passed_count += 1
            logger.info(f"[SOFT PASS] {message} ✓")
        else:
            failure = SoftAssertionFailure(
                message=message,
                expected=False,
                actual=True,
                assertion_type="false",
                timestamp=datetime.now().isoformat()
            )
            self.failures.append(failure)
            logger.error(f"[SOFT FAIL] {message}: Expected False, got True")

    def contains(self, substring: str, full_string: str, message: str) -> None:
        """Assert that substring is contained in full_string (soft assertion).

        Args:
            substring: Substring to find
            full_string: String to search in
            message: Assertion description
        """
        if substring in full_string:
            self.passed_count += 1
            logger.info(f"[SOFT PASS] {message} ✓")
        else:
            failure = SoftAssertionFailure(
                message=message,
                expected=f"'{substring}' in string",
                actual=f"'{substring}' NOT found in: {full_string[:100]}",
                assertion_type="contains",
                timestamp=datetime.now().isoformat()
            )
            self.failures.append(failure)
            logger.error(f"[SOFT FAIL] {message}: '{substring}' not found in '{full_string}'")

    def element_visible(self, locator: Locator, message: str, timeout_ms: int = 5000) -> None:
        """Assert that a Playwright Locator element is visible (soft assertion).

        Args:
            locator: Playwright Locator object
            message: Assertion description
            timeout_ms: Timeout in milliseconds (default 5000)
        """
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
            self.passed_count += 1
            logger.info(f"[SOFT PASS] {message} ✓")
        except Exception as e:
            failure = SoftAssertionFailure(
                message=message,
                expected="Element visible",
                actual=f"Element not visible or timeout ({timeout_ms}ms): {str(e)[:100]}",
                assertion_type="element_visible",
                timestamp=datetime.now().isoformat()
            )
            self.failures.append(failure)
            logger.error(f"[SOFT FAIL] {message}: Element not visible. Error: {str(e)}")

    def element_hidden(self, locator: Locator, message: str, timeout_ms: int = 5000) -> None:
        """Assert that a Playwright Locator element is hidden (soft assertion).

        Args:
            locator: Playwright Locator object
            message: Assertion description
            timeout_ms: Timeout in milliseconds (default 5000)
        """
        try:
            locator.wait_for(state="hidden", timeout=timeout_ms)
            self.passed_count += 1
            logger.info(f"[SOFT PASS] {message} ✓")
        except Exception as e:
            failure = SoftAssertionFailure(
                message=message,
                expected="Element hidden",
                actual=f"Element visible or timeout ({timeout_ms}ms): {str(e)[:100]}",
                assertion_type="element_hidden",
                timestamp=datetime.now().isoformat()
            )
            self.failures.append(failure)
            logger.error(f"[SOFT FAIL] {message}: Element not hidden. Error: {str(e)}")

    def get_failures(self) -> List[SoftAssertionFailure]:
        """Return list of collected failures.

        Returns:
            List of SoftAssertionFailure objects
        """
        return self.failures

    def get_failure_count(self) -> int:
        """Return count of failures.

        Returns:
            Number of failures
        """
        return len(self.failures)

    def get_pass_count(self) -> int:
        """Return count of passes.

        Returns:
            Number of passed assertions
        """
        return self.passed_count
