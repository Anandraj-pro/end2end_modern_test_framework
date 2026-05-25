from utils.logger import logger

class Assert:
    """Custom assertion wrapper that logs checks to standard output and log files.
    
    Provides highly readable assertion summaries during execution, allowing quick troubleshooting.
    """
    
    @staticmethod
    def true(condition: bool, message: str):
        """Asserts that a condition resolves to True."""
        logger.info(f"Asserting: {message}")
        if not condition:
            error_msg = f"Assertion FAILED: {message} (Expected: True, Actual: False)"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.info(f"Assertion PASSED: {message}")

    @staticmethod
    def false(condition: bool, message: str):
        """Asserts that a condition resolves to False."""
        logger.info(f"Asserting: {message}")
        if condition:
            error_msg = f"Assertion FAILED: {message} (Expected: False, Actual: True)"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.info(f"Assertion PASSED: {message}")

    @staticmethod
    def equal(actual, expected, message: str):
        """Asserts that two values are equal."""
        logger.info(f"Asserting: {message} | [Actual: '{actual}' | Expected: '{expected}']")
        if actual != expected:
            error_msg = f"Assertion FAILED: {message} (Actual: '{actual}' != Expected: '{expected}')"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.info(f"Assertion PASSED: {message}")

    @staticmethod
    def contains(substring: str, full_string: str, message: str):
        """Asserts that a substring is present within a full string."""
        logger.info(f"Asserting: {message} | [Checking if '{substring}' is in '{full_string}']")
        if substring not in full_string:
            error_msg = f"Assertion FAILED: {message} (Substring '{substring}' not found in '{full_string}')"
            logger.error(error_msg)
            raise AssertionError(error_msg)
        logger.info(f"Assertion PASSED: {message}")

    @staticmethod
    def element_visible(locator, message: str, timeout_ms: int = 5000):
        """Asserts that a Playwright Locator is visible within a timeout."""
        logger.info(f"Asserting Element Visibility: {message}")
        try:
            # Wait for visibility
            locator.wait_for(state="visible", timeout=timeout_ms)
            logger.info(f"Assertion PASSED: Element visible -> {message}")
        except Exception as e:
            error_msg = f"Assertion FAILED: Element not visible within {timeout_ms}ms -> {message}. Context: {str(e)}"
            logger.error(error_msg)
            raise AssertionError(error_msg)

    @staticmethod
    def element_hidden(locator, message: str, timeout_ms: int = 5000):
        """Asserts that a Playwright Locator is hidden within a timeout."""
        logger.info(f"Asserting Element Hidden/Absent: {message}")
        try:
            # Wait for element to become hidden
            locator.wait_for(state="hidden", timeout=timeout_ms)
            logger.info(f"Assertion PASSED: Element is hidden/absent -> {message}")
        except Exception as e:
            error_msg = f"Assertion FAILED: Element not hidden within {timeout_ms}ms -> {message}. Context: {str(e)}"
            logger.error(error_msg)
            raise AssertionError(error_msg)
