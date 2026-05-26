import pytest
import time
from utils.retry_manager import retry, RetryConfig, get_retry_config, has_retry_config


class TestRetryDecorator:
    """Test retry decorator functionality."""

    def test_passes_on_first_attempt(self):
        """Verify test passes on first attempt without retries."""
        attempt_count = 0

        @retry(max_attempts=3)
        def passing_test():
            nonlocal attempt_count
            attempt_count += 1
            assert True

        passing_test()
        assert attempt_count == 1

    def test_retries_on_assertion_failure(self):
        """Verify test retries when assertion fails."""
        attempt_count = 0

        @retry(max_attempts=3)
        def failing_test():
            nonlocal attempt_count
            attempt_count += 1
            assert False, "Always fails"

        with pytest.raises(AssertionError):
            failing_test()

        assert attempt_count == 3

    def test_stops_retrying_on_success(self):
        """Verify retries stop after successful attempt."""
        attempt_count = 0

        @retry(max_attempts=3)
        def eventually_passing_test():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise AssertionError("First attempt fails")
            assert True

        eventually_passing_test()
        assert attempt_count == 2

    def test_respects_max_attempts(self):
        """Verify decorator respects max_attempts limit."""
        attempt_count = 0

        @retry(max_attempts=5)
        def always_failing():
            nonlocal attempt_count
            attempt_count += 1
            assert False

        with pytest.raises(AssertionError):
            always_failing()

        assert attempt_count == 5

    def test_default_max_attempts_is_three(self):
        """Verify default max_attempts is 3."""
        attempt_count = 0

        @retry()
        def always_failing():
            nonlocal attempt_count
            attempt_count += 1
            assert False

        with pytest.raises(AssertionError):
            always_failing()

        assert attempt_count == 3

    def test_delay_between_retries(self):
        """Verify delay occurs between retries."""
        attempt_count = 0
        start_time = time.time()

        @retry(max_attempts=3, delay_seconds=0.1)
        def failing_test():
            nonlocal attempt_count
            attempt_count += 1
            assert False

        with pytest.raises(AssertionError):
            failing_test()

        elapsed = time.time() - start_time
        # Should have 2 delays of 0.1s each = 0.2s minimum
        assert elapsed >= 0.2

    def test_backoff_multiplier(self):
        """Verify backoff multiplier increases delay."""
        attempt_times = []

        @retry(max_attempts=3, delay_seconds=0.05, backoff_multiplier=2.0)
        def failing_test():
            attempt_times.append(time.time())
            assert False

        with pytest.raises(AssertionError):
            failing_test()

        # Should have 3 attempt times
        assert len(attempt_times) == 3

        # Gap between attempts should increase
        gap1 = attempt_times[1] - attempt_times[0]
        gap2 = attempt_times[2] - attempt_times[1]

        # gap2 should be approximately 2x gap1 (with tolerance for execution time)
        assert gap2 > gap1

    def test_retry_on_specific_exceptions(self):
        """Verify retry only on specified exceptions."""
        attempt_count = 0

        @retry(max_attempts=3, retry_on_exceptions=(ValueError,))
        def raises_type_error():
            nonlocal attempt_count
            attempt_count += 1
            raise TypeError("Wrong exception type")

        with pytest.raises(TypeError):
            raises_type_error()

        # Should not retry, only 1 attempt
        assert attempt_count == 1

    def test_retry_on_multiple_exception_types(self):
        """Verify retry on multiple exception types."""
        attempt_count = 0

        @retry(max_attempts=3, retry_on_exceptions=(ValueError, AssertionError))
        def sometimes_value_error():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise ValueError("First error")
            assert False

        with pytest.raises(AssertionError):
            sometimes_value_error()

        assert attempt_count == 3

    def test_preserves_function_name(self):
        """Verify decorator preserves function name."""
        @retry()
        def my_test_function():
            pass

        assert my_test_function.__name__ == "my_test_function"

    def test_passes_args_and_kwargs(self):
        """Verify decorator passes arguments to function."""
        @retry()
        def test_with_args(a, b, c=None):
            assert a == 1
            assert b == 2
            assert c == 3
            return True

        result = test_with_args(1, 2, c=3)
        assert result is True

    def test_returns_function_return_value(self):
        """Verify decorator returns function's return value."""
        @retry()
        def returns_value():
            return 42

        assert returns_value() == 42

    def test_raises_original_exception_on_final_failure(self):
        """Verify original exception is raised on final failure."""
        @retry(max_attempts=2)
        def always_fails():
            raise ValueError("Original error")

        with pytest.raises(ValueError, match="Original error"):
            always_fails()


class TestRetryConfig:
    """Test RetryConfig dataclass."""

    def test_config_defaults(self):
        """Verify RetryConfig has correct defaults."""
        config = RetryConfig()

        assert config.max_attempts == 3
        assert config.delay_seconds == 1.0
        assert config.backoff_multiplier == 1.0
        assert config.retry_on_exceptions == (AssertionError,)

    def test_config_custom_values(self):
        """Verify RetryConfig accepts custom values."""
        config = RetryConfig(
            max_attempts=5,
            delay_seconds=2.0,
            backoff_multiplier=1.5,
            retry_on_exceptions=(ValueError, TypeError)
        )

        assert config.max_attempts == 5
        assert config.delay_seconds == 2.0
        assert config.backoff_multiplier == 1.5
        assert config.retry_on_exceptions == (ValueError, TypeError)

    def test_config_repr(self):
        """Verify RetryConfig string representation."""
        config = RetryConfig(max_attempts=5, delay_seconds=2.0)
        repr_str = repr(config)

        assert "max_attempts=5" in repr_str
        assert "delay_seconds=2.0" in repr_str


class TestRetryHelper:
    """Test retry helper functions."""

    def test_get_retry_config_from_decorated_function(self):
        """Verify get_retry_config returns config from decorated function."""
        @retry(max_attempts=5, delay_seconds=2.0)
        def my_test():
            pass

        config = get_retry_config(my_test)

        assert config is not None
        assert config.max_attempts == 5
        assert config.delay_seconds == 2.0

    def test_get_retry_config_from_undecorated_function(self):
        """Verify get_retry_config returns None for undecorated function."""
        def my_test():
            pass

        config = get_retry_config(my_test)
        assert config is None

    def test_has_retry_config_true(self):
        """Verify has_retry_config returns True for decorated function."""
        @retry()
        def my_test():
            pass

        assert has_retry_config(my_test) is True

    def test_has_retry_config_false(self):
        """Verify has_retry_config returns False for undecorated function."""
        def my_test():
            pass

        assert has_retry_config(my_test) is False


class TestRetryEdgeCases:
    """Test edge cases and error conditions."""

    def test_zero_delay_between_retries(self):
        """Verify retry works with zero delay."""
        attempt_count = 0

        @retry(max_attempts=2, delay_seconds=0)
        def failing_test():
            nonlocal attempt_count
            attempt_count += 1
            assert False

        with pytest.raises(AssertionError):
            failing_test()

        assert attempt_count == 2

    def test_single_attempt(self):
        """Verify max_attempts=1 means no retries."""
        attempt_count = 0

        @retry(max_attempts=1)
        def failing_test():
            nonlocal attempt_count
            attempt_count += 1
            assert False

        with pytest.raises(AssertionError):
            failing_test()

        assert attempt_count == 1

    def test_retry_with_exception_in_finally_block(self):
        """Verify retry doesn't interfere with finally blocks."""
        executed_finally = False

        @retry(max_attempts=2)
        def test_with_finally():
            nonlocal executed_finally
            try:
                assert False
            finally:
                executed_finally = True

        with pytest.raises(AssertionError):
            test_with_finally()

        assert executed_finally is True
