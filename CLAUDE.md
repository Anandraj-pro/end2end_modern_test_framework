# Claude Code Project Guide: End-to-End Modern Test Framework

**Project**: End-to-End Test Framework using Python + Playwright  
**Current Phase**: Phase 1: Stabilize (Test Suite Stabilization)  
**Date Started**: May 25, 2026  
**Duration**: 2 weeks (15-20 hours)

---

## Project Overview

A modern E2E testing framework built with:
- **Python 3** with pytest test runner
- **Playwright** for browser automation
- **Page Object Model (POM)** architecture with inheritance
- **Custom logging** (singleton with thread-safe logging)
- **Custom assertions** with built-in logging
- **HTML reports** with screenshots on failure

The framework has excellent architectural foundations but needs stability features before expanding.

---

## Current Architecture

### Layers

```
Tests Layer          → tests/test_login.py, tests/test_inventory.py
    ↓
Page Objects Layer   → LoginPage, InventoryPage, CartPage (inherit from BasePage)
    ↓
Base Layer          → BasePage (browser operations: click, fill, wait)
    ↓
Utils Layer         → Custom logger (singleton), assertions, data factories (new)
    ↓
Playwright Engine   → Browser automation
```

### Key Files

- **Tests**: `tests/test_login.py`, `tests/test_inventory.py`, `tests/conftest.py`
- **Pages**: `pages/base_page.py`, `pages/login_page.py`, `pages/inventory_page.py`, `pages/cart_page.py`
- **Utils**: `utils/logger.py` (singleton), `utils/assertions.py` (6 assertion methods)
- **Config**: `pytest.ini` (test markers: smoke, regression, login, cart), `.env` (environment vars)
- **Docs**: `docs/architecture.md` (excellent architecture documentation)

### Design Patterns Used

- **Page Object Model (POM)**: Encapsulate page elements and business logic
- **Inheritance**: BasePage parent, specific pages inherit
- **Singleton**: FrameworkLogger (thread-safe, single instance)
- **Facade/Wrapper**: Assert and BasePage wrap complex APIs
- **Dependency Injection**: Fixtures in conftest.py inject page objects into tests

---

## Phase 1: Stabilize - 4 Features

### Feature 1: Soft Assertions (2-3 hours)
**What**: Collect multiple failures instead of failing on first assertion  
**How**: Context manager pattern: `with SoftAssert("test") as soft:`  
**Where**: New file `utils/soft_assertions.py`  
**Why**: Developers see ALL issues in one test run, faster debugging  
**Status**: Opt-in, non-breaking

### Feature 2: Test Data Factories (3-4 hours)
**What**: Builder pattern for test data (UserFactory, ProductFactory)  
**How**: Fluent API: `UserFactory.builder().with_first_name("Jane").build()`  
**Where**: New package `utils/test_data/`  
**Why**: DRY principle, centralized test data, easier maintenance  
**Status**: Opt-in, non-breaking

### Feature 3: Retry Mechanism (4-5 hours)
**What**: Automatic retry for failed tests (whole test, not individual assertions)  
**How**: Decorator: `@retry(max_attempts=3, delay_seconds=2)`  
**Where**: New file `utils/retry_manager.py`, integration in `tests/conftest.py`  
**Why**: Handle transient failures without full debugging cycle  
**Status**: Opt-in per test, non-breaking

### Feature 4: Flaky Test Detection (3-4 hours)
**What**: Identify tests that fail randomly (20-80% failure rate)  
**How**: Singleton detector with JSON persistence (`.pytest_cache/flaky_tests.json`)  
**Where**: New file `utils/flaky_detector.py`, integration in `tests/conftest.py`  
**Why**: Build confidence in test suite, identify unstable tests  
**Status**: Passive monitoring (default enabled)

---

## Implementation Sequence

1. **Soft Assertions** → Lowest risk, isolated, foundation for others
2. **Test Data Factories** → Medium complexity, good learning step
3. **Retry Mechanism** → Higher complexity, pytest hook integration
4. **Flaky Test Detection** → Most complex, data persistence
5. **Integration & Documentation** → Verify all work together

**Time Budget**: 15-20 hours over 2 weeks  
**Priority if Short**: Complete 1-2 features thoroughly vs all 4 partially

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Retry scope | Entire test | Simpler, cleaner, works with fixtures |
| Testing approach | Unit + Integration | Comprehensive validation |
| Factory presets | Include presets | More readable tests (standard_user, locked_user, backpack) |
| Time priority | Depth > Breadth | 2 polished features > 4 half-baked |
| Backward compat | All non-breaking | Existing tests run unchanged |

---

## Working with Claude Code

### Before Starting a Task
1. Read this file (CLAUDE.md)
2. Check the plan: `C:\Users\sysadmin\.claude\plans\sunny-whistling-clover.md`
3. Review memory files in `C:\Users\sysadmin\.claude\projects\D--end2end-modern-test-framework\memory\`

### During Implementation
- Follow existing code patterns (static classes, singletons, dependency injection)
- Maintain logging integration (use `logger.info()`, `logger.error()` consistently)
- Write both unit AND integration tests
- Preserve backward compatibility (no breaking changes)

### Code Standards

**Existing Patterns to Follow**:
- Static utility classes: `Assert.equal()`, `Assert.contains()`
- Singleton pattern: `FrameworkLogger.get_logger()`
- Dependency injection: Page objects injected via conftest fixtures
- Semantic Playwright locators: `.get_by_role()`, `.get_by_placeholder()`, not CSS strings
- Comprehensive logging: Every major action logged

**New Code Should**:
- Use same patterns as existing code
- Include docstrings (one short line, no multi-paragraph blocks)
- Log key operations via `logger.info()` / `logger.error()`
- Support pytest fixtures (conftest.py)
- Be testable (write both unit and integration tests)

---

## File Structure

```
end2end_modern_test_framework/
├── tests/
│   ├── conftest.py              # Pytest configuration, fixtures, hooks
│   ├── test_login.py            # Login tests
│   └── test_inventory.py        # Inventory/cart tests
│
├── pages/
│   ├── base_page.py             # Parent class: browser operations
│   ├── login_page.py            # Login page object
│   ├── inventory_page.py        # Inventory/products page object
│   └── cart_page.py             # Cart/checkout page object
│
├── utils/
│   ├── logger.py                # Singleton logger (thread-safe)
│   ├── assertions.py            # Custom assertions (6 methods)
│   └── test_data/               # NEW: Test data factories
│       ├── __init__.py
│       ├── base_factory.py
│       ├── user_factory.py
│       └── product_factory.py
│
├── pytest.ini                    # Pytest configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── CLAUDE.md                    # This file
└── docs/
    ├── architecture.md          # Detailed architecture docs
    └── FEATURE_*.md             # Feature documentation (Phase 1)
```

---

## Testing the Implementation

### Run Existing Tests (Should Still Pass)
```bash
pytest tests/test_login.py tests/test_inventory.py -v
```

### Run Unit Tests for New Features
```bash
pytest tests/unit/test_soft_assertions.py -v
pytest tests/unit/test_factories.py -v
pytest tests/unit/test_retry_manager.py -v
pytest tests/unit/test_flaky_detector.py -v
```

### Run with New Features
```bash
pytest tests/test_with_new_features.py -v
```

---

## References

- **Plan**: `C:\Users\sysadmin\.claude\plans\sunny-whistling-clover.md`
- **Memory**: `C:\Users\sysadmin\.claude\projects\D--end2end-modern-test-framework\memory\`
- **Architecture Docs**: `docs/architecture.md`
- **Existing Code**: Follow patterns in `utils/logger.py` and `utils/assertions.py`

---

## Success Criteria for Phase 1

- ✅ Soft Assertions implemented with context manager pattern
- ✅ Test Data Factories with builder pattern and presets
- ✅ Retry Mechanism with decorator and pytest integration
- ✅ Flaky Test Detection with persistence
- ✅ All existing tests pass without modification
- ✅ Unit tests for each feature
- ✅ Integration tests showing features working together
- ✅ Documentation for each feature
- ✅ No new external dependencies
- ✅ Code follows existing patterns

---

**Last Updated**: May 25, 2026  
**Phase**: 1 (Stabilize)  
**Status**: Ready for implementation
