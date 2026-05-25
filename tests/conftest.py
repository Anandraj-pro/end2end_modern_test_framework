import os
import pytest
from dotenv import load_dotenv
from utils.logger import logger
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

# Load configurations from .env at runtime initialization
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

@pytest.fixture(scope="session", autouse=True)
def init_automation_suite():
    """Triggers at the start of E2E suite execution for environmental verification."""
    logger.info("======================================================================")
    logger.info("   Starting Modern Python Playwright E2E Test Suite Execution Session  ")
    logger.info("======================================================================")
    
    # Assert critical environment values are present
    base_url = os.getenv("BASE_URL")
    browser_type = os.getenv("BROWSER", "chromium")
    headless = os.getenv("HEADLESS", "True")
    
    logger.info(f"AUT Target URL: {base_url}")
    logger.info(f"Target Browser: {browser_type} (Headless={headless})")
    
    yield
    
    logger.info("======================================================================")
    logger.info("   E2E Test Suite Execution Session Finished - Cleaning up Resources  ")
    logger.info("======================================================================")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Overrides default Playwright browser context configuration.
    
    Configures consistent high-res viewports and configures tracing options.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 800},
        "ignore_https_errors": True
    }

# -----------------------------------------------------------------------------
# Dependency Injected POM Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def login_page(page):
    """Injects initialized LoginPage into tests."""
    return LoginPage(page)

@pytest.fixture
def inventory_page(page):
    """Injects initialized InventoryPage into tests."""
    return InventoryPage(page)

@pytest.fixture
def cart_page(page):
    """Injects initialized CartPage into tests."""
    return CartPage(page)

# -----------------------------------------------------------------------------
# Pytest Hooks for Advanced Reporting & Screen Capture
# -----------------------------------------------------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Listens to test status changes to intercept failures and attach screenshots.
    
    Tightly integrated with Pytest-HTML plugin.
    """
    # Excute downstream hooks to retrieve the final execution outcome
    outcome = yield
    report = outcome.get_result()
    
    # Check if failure occurs in the call stage (the actual test code execution)
    if report.when == "call" and report.failed:
        logger.error(f"TEST DETECTED FAIL: '{item.nodeid}'")
        
        # Grab active Playwright page fixture from function arguments if present
        page = item.funcargs.get("page") if "page" in item.funcargs else None
        
        if page:
            try:
                # Set absolute reports directory path
                reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
                os.makedirs(reports_dir, exist_ok=True)
                
                # Build unique file name based on test method
                screenshot_filename = f"fail_{item.name}.png"
                screenshot_abs_path = os.path.join(reports_dir, screenshot_filename)
                
                # Take full screenshot
                page.screenshot(path=screenshot_abs_path, full_page=True)
                logger.info(f"Captured error screen state and saved to relative: reports/{screenshot_filename}")
                
                # Embed the captured image as an interactive element inside the Pytest-HTML Report
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    extra = getattr(report, "extra", [])
                    # We link the screenshot relatively so the self-contained report is portable
                    html_embed = (
                        f'<div>'
                        f'<p style="font-weight:bold; color:#d9534f;">Failure State Screenshot:</p>'
                        f'<img src="{screenshot_filename}" alt="Failure Screenshot" '
                        f'style="width:500px; max-height:300px; border:2px solid #d9534f; border-radius:4px; cursor:pointer;" '
                        f'onclick="window.open(this.src)" />'
                        f'</div>'
                    )
                    extra.append(pytest_html.extras.html(html_embed))
                    report.extra = extra
            except Exception as e:
                logger.warning(f"Unable to capture failure screenshot. Error: {str(e)}")
