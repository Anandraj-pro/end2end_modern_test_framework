import pytest
from utils.soft_assertions import SoftAssert, SoftAssertionFailure


class TestSoftAssertEqual:
    """Test SoftAssert.equal() method."""

    def test_equal_passes_when_values_match(self):
        """Verify soft assertion passes when values are equal."""
        with SoftAssert("test") as soft:
            soft.equal(5, 5, "Numbers should match")

        assert soft.get_pass_count() == 1
        assert soft.get_failure_count() == 0

    def test_equal_fails_when_values_dont_match(self):
        """Verify soft assertion fails when values are not equal."""
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssert("test") as soft:
                soft.equal(5, 10, "Numbers should match")

        error_msg = str(exc_info.value)
        assert "Numbers should match" in error_msg
        assert "Expected: 10" in error_msg

    def test_equal_collects_multiple_failures(self):
        """Verify multiple equal failures are collected."""
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssert("test") as soft:
                soft.equal(1, 2, "First check")
                soft.equal(3, 4, "Second check")
                soft.equal(5, 6, "Third check")

        error_msg = str(exc_info.value)
        assert "First check" in error_msg
        assert "Second check" in error_msg
        assert "Third check" in error_msg
        assert "3 failures" in error_msg


class TestSoftAssertTrue:
    """Test SoftAssert.true() method."""

    def test_true_passes_for_true_condition(self):
        """Verify true assertion passes for true condition."""
        with SoftAssert("test") as soft:
            soft.true(True, "Should be true")

        assert soft.get_pass_count() == 1
        assert soft.get_failure_count() == 0

    def test_true_fails_for_false_condition(self):
        """Verify true assertion fails for false condition."""
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssert("test") as soft:
                soft.true(False, "Should be true")

        assert "Should be true" in str(exc_info.value)


class TestSoftAssertFalse:
    """Test SoftAssert.false() method."""

    def test_false_passes_for_false_condition(self):
        """Verify false assertion passes for false condition."""
        with SoftAssert("test") as soft:
            soft.false(False, "Should be false")

        assert soft.get_pass_count() == 1
        assert soft.get_failure_count() == 0

    def test_false_fails_for_true_condition(self):
        """Verify false assertion fails for true condition."""
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssert("test") as soft:
                soft.false(True, "Should be false")

        assert "Should be false" in str(exc_info.value)


class TestSoftAssertContains:
    """Test SoftAssert.contains() method."""

    def test_contains_passes_when_substring_exists(self):
        """Verify contains assertion passes when substring is found."""
        with SoftAssert("test") as soft:
            soft.contains("world", "hello world", "World should be in string")

        assert soft.get_pass_count() == 1
        assert soft.get_failure_count() == 0

    def test_contains_fails_when_substring_missing(self):
        """Verify contains assertion fails when substring not found."""
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssert("test") as soft:
                soft.contains("xyz", "hello world", "xyz should be in string")

        assert "xyz should be in string" in str(exc_info.value)

    def test_contains_is_case_sensitive(self):
        """Verify contains assertion is case sensitive."""
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssert("test") as soft:
                soft.contains("HELLO", "hello world", "HELLO should be in string")

        assert "HELLO should be in string" in str(exc_info.value)


class TestSoftAssertMixed:
    """Test mixing different assertion types."""

    def test_mixed_assertions_collect_all_failures(self):
        """Verify different assertion types are collected together."""
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssert("test") as soft:
                soft.equal(1, 2, "Check 1: Numbers")
                soft.true(False, "Check 2: Boolean")
                soft.contains("xyz", "abc", "Check 3: String")

        error_msg = str(exc_info.value)
        assert "Check 1: Numbers" in error_msg
        assert "Check 2: Boolean" in error_msg
        assert "Check 3: String" in error_msg
        assert "3 failures" in error_msg

    def test_mixed_assertions_with_passes_and_failures(self):
        """Verify both passes and failures are tracked together."""
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssert("test") as soft:
                soft.equal(1, 1, "Check 1: Pass")
                soft.equal(2, 3, "Check 2: Fail")
                soft.true(True, "Check 3: Pass")
                soft.contains("xyz", "abc", "Check 4: Fail")

        # After context exit, check counts
        # Note: Can't access soft.get_pass_count() after exception,
        # so verify from error message
        error_msg = str(exc_info.value)
        assert "2 failures" in error_msg
        assert "Check 2: Fail" in error_msg
        assert "Check 4: Fail" in error_msg


class TestSoftAssertFailureDataclass:
    """Test SoftAssertionFailure dataclass."""

    def test_failure_has_required_fields(self):
        """Verify SoftAssertionFailure has required fields."""
        failure = SoftAssertionFailure(
            message="Test message",
            expected="expected value",
            actual="actual value",
            assertion_type="equal",
            timestamp="2026-05-26T10:30:00"
        )

        assert failure.message == "Test message"
        assert failure.expected == "expected value"
        assert failure.actual == "actual value"
        assert failure.assertion_type == "equal"


class TestSoftAssertContextManager:
    """Test SoftAssert context manager behavior."""

    def test_context_manager_returns_self(self):
        """Verify context manager returns self for method chaining."""
        with SoftAssert("test") as soft:
            assert isinstance(soft, SoftAssert)

    def test_no_exception_when_all_pass(self):
        """Verify no exception is raised when all assertions pass."""
        # This should not raise
        with SoftAssert("test") as soft:
            soft.equal(1, 1, "Check 1")
            soft.equal(2, 2, "Check 2")
            soft.true(True, "Check 3")

        assert soft.get_pass_count() == 3
        assert soft.get_failure_count() == 0

    def test_exception_message_includes_test_name(self):
        """Verify exception message includes test name."""
        with pytest.raises(AssertionError) as exc_info:
            with SoftAssert("my_test_name") as soft:
                soft.equal(1, 2, "Check")

        assert "my_test_name" in str(exc_info.value)

    def test_get_failures_returns_failure_objects(self):
        """Verify get_failures returns SoftAssertionFailure objects."""
        try:
            with SoftAssert("test") as soft:
                soft.equal(1, 2, "Check 1")
                soft.equal(3, 4, "Check 2")
        except AssertionError:
            pass

        failures = soft.get_failures()
        assert len(failures) == 2
        assert all(isinstance(f, SoftAssertionFailure) for f in failures)
        assert failures[0].message == "Check 1"
        assert failures[1].message == "Check 2"
