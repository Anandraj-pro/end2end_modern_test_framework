import os
import pytest
from utils.assertions import Assert
from utils.logger import logger

@pytest.mark.login
@pytest.mark.smoke
def test_successful_login(login_page, inventory_page):
    """Verifies that a standard user can successfully log in and access the inventory dashboard."""
    logger.info("--- Starting Test: test_successful_login ---")
    
    # Retrieve credentials from environment
    username = os.getenv("DEMO_USERNAME", "standard_user")
    password = os.getenv("DEMO_PASSWORD", "secret_sauce")
    
    # Step 1: Navigate to LoginPage
    login_page.navigate()
    
    # Step 2: Login
    login_page.login(username, password)
    
    # Step 3: Assert Redirection and Title
    # Verify inventory page title is visible and reads 'Products'
    Assert.element_visible(inventory_page.page_title, "Inventory page title indicator should be visible")
    Assert.equal(inventory_page.get_page_title_text(), "Products", "Verify page title text equals 'Products'")
    
    # Verify rediection url
    Assert.contains("/inventory.html", inventory_page.page.url, "Verify redirection URL contains '/inventory.html'")
    
    logger.info("--- Completed Test: test_successful_login (PASSED) ---")

@pytest.mark.login
@pytest.mark.regression
def test_failed_login_invalid_credentials(login_page):
    """Verifies that an error message is displayed when attempting to log in with invalid credentials."""
    logger.info("--- Starting Test: test_failed_login_invalid_credentials ---")
    
    # Step 1: Navigate to LoginPage
    login_page.navigate()
    
    # Step 2: Attempt Login with invalid credentials
    login_page.login("invalid_user", "wrong_password")
    
    # Step 3: Assert error message visibility and text content
    error_msg = login_page.get_error_message()
    Assert.element_visible(login_page.error_message_container, "Error banner container should be visible")
    Assert.contains("Username and password do not match any user in this service", error_msg, 
                    "Verify invalid credentials error message banner content")
    
    logger.info("--- Completed Test: test_failed_login_invalid_credentials (PASSED) ---")

@pytest.mark.login
@pytest.mark.regression
def test_failed_login_locked_out_user(login_page):
    """Verifies that a descriptive lockout error message is displayed when attempting login with a locked user profile."""
    logger.info("--- Starting Test: test_failed_login_locked_out_user ---")
    
    # Retrieve credentials from environment
    locked_username = os.getenv("LOCKED_OUT_USERNAME", "locked_out_user")
    password = os.getenv("DEMO_PASSWORD", "secret_sauce")
    
    # Step 1: Navigate to LoginPage
    login_page.navigate()
    
    # Step 2: Attempt Login with locked credentials
    login_page.login(locked_username, password)
    
    # Step 3: Assert descriptive lock-out banner is displayed
    error_msg = login_page.get_error_message()
    Assert.element_visible(login_page.error_message_container, "Error banner container should be visible")
    Assert.contains("Sorry, this user has been locked out", error_msg, 
                    "Verify lock-out warning error message banner content")
    
    logger.info("--- Completed Test: test_failed_login_locked_out_user (PASSED) ---")
