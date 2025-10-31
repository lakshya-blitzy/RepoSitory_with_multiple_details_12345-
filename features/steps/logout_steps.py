"""
Logout Step Definitions Module

Behave step definitions for user session termination functionality in the Testinium
test automation framework. This module maps Gherkin scenario steps from Logout.feature
to Python implementation code using Behave decorators.

Key Features:
- Logout workflow with popup menu interaction
- Login page redirection verification after logout
- Back button navigation security testing
- Context-based driver and page object management

Migration Context:
    Converted from LogOutSD.java which used Cucumber @Then annotations.
    Original Java implementation:
        - Used WebDriverWait(Driver.getDriver(), 3) with hardcoded 3-second timeout
        - Used LogOutP page object with public WebElement fields
        - Used JUnit Assert.assertEquals and Assert.assertTrue
    
    Python implementation improvements:
        - Uses context.driver for thread-safe driver access
        - Uses LogoutPage with property-based element locators
        - Uses Python assert statements with descriptive error messages
        - Eliminates hardcoded waits (handled by page object properties)

Gherkin Steps Implemented:
    1. @then('User click Log out option')
       - Clicks user menu popup button
       - Clicks logout link in dropdown menu
       - Completes two-step logout workflow
    
    2. @then('User should see the login dashboard')
       - Verifies browser redirects to login page
       - Validates page title: "Login | Best solution for startups"
       - Confirms successful logout completion
    
    3. @then('User can not click the step back button to go the home page')
       - Navigates back using browser back button
       - Verifies warning message is displayed
       - Tests security against unauthorized access after logout

Step Text Preservation:
    All step texts MUST match exactly with Logout.feature Gherkin scenarios.
    Changes to step text will break test execution.

Thread Safety:
    Uses context.driver which is thread-safe in Behave when using parallel
    execution frameworks (behave-parallel or pytest-xdist). Each scenario
    gets its own context with isolated driver instance.

Usage Example:
    Feature file (Logout.feature):
        @Logout
        Scenario: Successful logout
            Given User is logged in
            When User click Log out option
            Then User should see the login dashboard
    
    This module provides the step implementation for all @then steps.

Dependencies:
    - behave: Python BDD framework providing @when, @then decorators
    - pages.logout_page: LogoutPage class with logout element locators
    - context.driver: WebDriver instance from Behave context

Author: Blitzy Platform - Java to Python Migration
Migration Date: 2024
Original Source: src/main/java/com/testinium/step_definitions/LogOutSD.java
"""

from behave import when, then
from pages.logout_page import LogoutPage


@when('User click Log out option')
def user_clicks_logout_option(context):
    """
    Step definition for clicking the logout option.
    
    This step performs the complete two-step logout workflow:
    1. Clicks the user menu popup button to expand the dropdown
    2. Clicks the "Log out" link within the expanded dropdown menu
    
    The method uses LogoutPage properties which include explicit waits,
    eliminating the need for the hardcoded 3-second WebDriverWait from
    the original Java implementation.
    
    Migration Notes:
        Java version:
            WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 3);
            wait.until(ExpectedConditions.visibilityOf(logOutP.popUpButton));
            logOutP.popUpButton.click();
            logOutP.logOutButton.click();
        
        Python version:
            logout_page = LogoutPage(context.driver)
            logout_page.popup_button.click()  # Includes wait_for_clickable
            logout_page.logout_button.click()  # Includes wait_for_clickable
    
    Args:
        context: Behave context object containing:
            - driver: WebDriver instance for browser automation
            - Other shared state between steps
    
    Raises:
        TimeoutException: If popup_button or logout_button not clickable
                         within the configured timeout period
        WebDriverException: If click operations fail due to browser issues
        AttributeError: If context.driver is not initialized
    
    Example:
        Gherkin:
            When User click Log out option
        
        Behave execution:
            >>> from behave.runner import Context
            >>> context = Context(runner=None)
            >>> context.driver = webdriver.Chrome()
            >>> user_clicks_logout_option(context)
    """
    # Initialize LogoutPage with context driver for thread-safe operation
    logout_page = LogoutPage(context.driver)
    
    # Step 1: Click user menu popup button to expand dropdown
    # The popup_button property uses wait_for_clickable internally,
    # eliminating the need for explicit WebDriverWait
    logout_page.popup_button.click()
    
    # Step 2: Click logout button in the expanded dropdown menu
    # The logout_button property ensures the element is clickable
    # after the dropdown expansion completes
    logout_page.logout_button.click()


@then('User should see the login dashboard')
def user_should_see_login_dashboard(context):
    """
    Step definition for verifying successful logout with login page redirection.
    
    This step validates that after logout, the user is redirected to the login
    page by checking the browser page title. The expected title is:
    "Login | Best solution for startups"
    
    This verification confirms:
    - Logout action completed successfully
    - Session was terminated on the server
    - Browser was redirected to the unauthenticated login page
    - Login page rendered correctly with expected title
    
    Migration Notes:
        Java version:
            String expectedDashboard = "Login | Best solution for startups";
            String actualDashboard = Driver.getDriver().getTitle();
            Assert.assertEquals("The title is not same as the expected! ",
                              expectedDashboard, actualDashboard);
        
        Python version:
            expected_title = "Login | Best solution for startups"
            actual_title = context.driver.title
            assert actual_title == expected_title, (
                f"Expected login page title '{expected_title}', "
                f"but got '{actual_title}'. Logout may have failed."
            )
    
    Args:
        context: Behave context object containing:
            - driver: WebDriver instance with current page loaded
    
    Raises:
        AssertionError: If actual page title does not match expected login page title
        AttributeError: If context.driver is not initialized
        WebDriverException: If unable to retrieve page title from browser
    
    Example:
        Gherkin:
            Then User should see the login dashboard
        
        Behave execution:
            >>> from behave.runner import Context
            >>> context = Context(runner=None)
            >>> context.driver = webdriver.Chrome()
            >>> context.driver.get("https://testinium.example.com/web/login")
            >>> user_should_see_login_dashboard(context)
    """
    # Define expected login page title (must match application login page)
    expected_title = "Login | Best solution for startups"
    
    # Get actual page title from browser
    actual_title = context.driver.title
    
    # Validate page title matches expected login page title
    # Descriptive error message aids in debugging logout failures
    assert actual_title == expected_title, (
        f"Expected login page title '{expected_title}', "
        f"but got '{actual_title}'. Logout may have failed or "
        f"redirected to incorrect page."
    )


@then('User can not click the step back button to go the home page')
def user_cannot_navigate_back_after_logout(context):
    """
    Step definition for testing back button navigation security after logout.
    
    This step verifies that after logging out, users cannot use the browser's
    back button to return to authenticated pages. It tests the security
    mechanism that prevents unauthorized access to protected resources after
    session termination.
    
    The test performs:
    1. Navigates back using browser.back()
    2. Verifies a warning message is displayed
    3. Confirms the warning prevents access to authenticated pages
    
    This security test is critical for:
    - Preventing session hijacking via browser history
    - Ensuring sessions are properly invalidated
    - Protecting sensitive data from unauthorized access
    - Meeting security compliance requirements
    
    Migration Notes:
        Java version:
            Driver.getDriver().navigate().back();
            Assert.assertTrue(logOutP.warningMess.isDisplayed());
        
        Python version:
            context.driver.back()
            logout_page = LogoutPage(context.driver)
            warning_element = logout_page.warning_message
            assert warning_element.is_displayed(), (
                "Expected warning message after back navigation post-logout, "
                "but no warning was displayed. Security vulnerability detected."
            )
    
    Security Implications:
        If this test fails (no warning message), it indicates a serious security
        vulnerability where users could access authenticated pages after logout
        by using the browser back button. This could expose sensitive data or
        allow unauthorized actions.
    
    Args:
        context: Behave context object containing:
            - driver: WebDriver instance currently on login page after logout
    
    Raises:
        AssertionError: If warning message is not displayed after back navigation
                       This indicates a security vulnerability
        TimeoutException: If warning_message element not found within timeout
                         This also indicates missing security mechanism
        AttributeError: If context.driver is not initialized
        WebDriverException: If browser navigation fails
    
    Example:
        Gherkin:
            Given User is logged in
            When User click Log out option
            And User should see the login dashboard
            Then User can not click the step back button to go the home page
        
        Behave execution:
            >>> from behave.runner import Context
            >>> from selenium import webdriver
            >>> context = Context(runner=None)
            >>> context.driver = webdriver.Chrome()
            >>> # After logout, user is on login page
            >>> user_cannot_navigate_back_after_logout(context)
            >>> # Verify warning message is displayed
    """
    # Attempt to navigate back to the previous page (authenticated page)
    # This simulates a user clicking the browser's back button after logout
    context.driver.back()
    
    # Initialize LogoutPage to access warning_message property
    logout_page = LogoutPage(context.driver)
    
    # Retrieve warning message element using property with explicit wait
    # The warning_message property uses wait_for_visibility to ensure
    # the warning dialog is present and visible
    warning_element = logout_page.warning_message
    
    # Verify warning message is displayed to user
    # This confirms the security mechanism is working correctly
    assert warning_element.is_displayed(), (
        "Expected warning message to be displayed after back navigation "
        "post-logout, but no warning was found. This indicates a security "
        "vulnerability where users can access authenticated pages after "
        "logout via browser back button."
    )


# Module-level execution for documentation and verification
if __name__ == "__main__":
    # Module self-test for documentation purposes.
    #
    # Note: This module requires Behave context and running WebDriver instance.
    # Actual usage is within Behave test execution framework.
    print("Logout Step Definitions module loaded successfully")
    print("\nStep definitions implemented:")
    print("  1. @when('User click Log out option')")
    print("     - Performs two-step logout workflow")
    print("     - Clicks user menu popup button")
    print("     - Clicks logout link in dropdown")
    print()
    print("  2. @then('User should see the login dashboard')")
    print("     - Verifies redirect to login page")
    print("     - Validates page title")
    print("     - Confirms logout success")
    print()
    print("  3. @then('User can not click the step back button to go the home page')")
    print("     - Tests back button security")
    print("     - Navigates back using browser.back()")
    print("     - Verifies warning message display")
    print()
    print("\nUsage: Run via Behave framework")
    print("Example: behave features/Logout.feature")
