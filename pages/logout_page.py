"""
Logout Page Module

Page Object Model implementation for user session termination functionality.
This module provides element locators and interaction methods for logout operations.

Key Features:
- Property-based element access with explicit waits
- User menu popup interaction
- Logout button access with clickable verification
- Warning message dialog detection
- Complete logout workflow encapsulation

Migration Context:
    Converted from LogOutP.java which used PageFactory with @FindBy annotations.
    Original Java implementation:
        - @FindBy(className = "o_user_menu") public WebElement popUpButton
        - @FindBy(xpath = "//a[.='Log out']") public WebElement logOutButton
        - @FindBy(xpath = "//div[@class= 'o_dialog_warning modal-body']") public WebElement warningMess
    
    Python implementation replaces public WebElement fields with property-based
    locators that return fresh element references on each access, preventing
    stale element exceptions.

Design Pattern:
    Inherits from BasePage for common WebDriver utilities including:
    - wait_for_element(): For element presence in DOM
    - wait_for_clickable(): For interactive button elements
    - wait_for_visibility(): For visible dialog messages
    - driver, wait, config: Inherited attributes

Element Locators:
    _POPUP_BUTTON: User menu dropdown trigger (className: 'o_user_menu')
    _LOGOUT_BUTTON: Logout link in dropdown menu (xpath: //a[.='Log out'])
    _WARNING_MESSAGE: Optional warning dialog (xpath: //div[@class='o_dialog_warning modal-body'])

Usage Example:
    >>> from pages.logout_page import LogoutPage
    >>> from utilities.driver_manager import DriverManager
    >>>
    >>> driver = DriverManager.get_driver()
    >>> logout_page = LogoutPage(driver)
    >>>
    >>> # Access individual elements
    >>> logout_page.popup_button.click()
    >>> logout_page.logout_button.click()
    >>>
    >>> # Use complete workflow
    >>> logout_page.logout()
"""

import logging
from typing import Tuple, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LogoutPage(BasePage):
    """
    Page Object for logout functionality in Testinium application.

    This class provides access to logout-related UI elements and workflow methods
    for terminating user sessions. It implements the Page Object Model pattern
    with property-based element locators that use explicit waits.

    Attributes:
        driver (WebDriver): Selenium WebDriver instance (inherited from BasePage)
        config (ConfigReader): Configuration reader singleton (inherited from BasePage)
        default_timeout (int): Default explicit wait timeout (inherited from BasePage)
        wait (WebDriverWait): Pre-configured wait instance (inherited from BasePage)
        actions (ActionChains): ActionChains for complex interactions (inherited from BasePage)

    Element Properties:
        popup_button: User menu dropdown trigger button
        logout_button: Logout link within the dropdown menu
        warning_message: Optional warning dialog displayed during logout

    Methods:
        logout(): Complete logout workflow (click popup, click logout button)

    Thread Safety:
        LogoutPage instances are thread-safe when each thread has its own WebDriver
        instance (achieved via threading.local() in DriverManager). Each instance
        maintains its own driver reference for isolated parallel test execution.

    Example:
        >>> from selenium import webdriver
        >>> from pages.logout_page import LogoutPage
        >>>
        >>> driver = webdriver.Chrome()
        >>> driver.get("https://testinium.example.com/dashboard")
        >>> logout_page = LogoutPage(driver)
        >>>
        >>> # Perform complete logout
        >>> logout_page.logout()
        >>>
        >>> # Or access elements individually
        >>> logout_page.popup_button.click()
        >>> logout_page.logout_button.click()
        >>>
        >>> # Check for warning message
        >>> try:
        ...     message = logout_page.warning_message
        ...     print(f"Warning: {message.text}")
        ... except TimeoutException:
        ...     print("No warning message displayed")
    """

    # Private locator constants following Python naming convention
    # Tuple format: (By.STRATEGY, 'locator_value')
    # These replace Java's @FindBy annotations with runtime-evaluated tuples
    _POPUP_BUTTON: Tuple[str, str] = (By.CLASS_NAME, 'o_user_menu')
    _LOGOUT_BUTTON: Tuple[str, str] = (By.XPATH, "//a[.='Log out']")
    _WARNING_MESSAGE: Tuple[str, str] = (
        By.XPATH,
        "//div[@class='o_dialog_warning modal-body']"
    )

    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize LogoutPage with WebDriver instance.

        This constructor calls BasePage.__init__() to establish common utilities
        and then sets up a logger specific to LogoutPage for debugging and
        tracking logout operations.

        Args:
            driver: Selenium WebDriver instance for browser automation
                   Expected to be a thread-local instance from DriverManager

        Example:
            >>> from selenium import webdriver
            >>> from pages.logout_page import LogoutPage
            >>>
            >>> driver = webdriver.Chrome()
            >>> logout_page = LogoutPage(driver)
            >>> # logout_page ready for element interactions
        """
        super().__init__(driver)
        self._logger = logging.getLogger(__name__)
        self._logger.info("LogoutPage initialized")

    @property
    def popup_button(self) -> WebElement:
        """
        User menu dropdown trigger button property.

        Returns a fresh WebElement reference on each access using wait_for_clickable
        to ensure the button is visible and enabled before interaction. This prevents
        stale element exceptions and ensures reliable element access.

        Locator Strategy:
            By.CLASS_NAME: 'o_user_menu'
            Original Java: @FindBy(className = "o_user_menu")

        Wait Strategy:
            Uses wait_for_clickable() to ensure button is:
            - Present in DOM
            - Visible on screen
            - Enabled for interaction
            - Not obscured by other elements

        Returns:
            WebElement: The user menu popup button element ready for clicking

        Raises:
            TimeoutException: If button not clickable within default timeout
                            (usually indicates page not fully loaded or element hidden)

        Example:
            >>> logout_page = LogoutPage(driver)
            >>> popup = logout_page.popup_button
            >>> popup.click()  # Opens user menu dropdown
            >>>
            >>> # Verify button is displayed
            >>> assert logout_page.popup_button.is_displayed()
        """
        self._logger.debug("Accessing popup_button element")
        return self.wait_for_clickable(self._POPUP_BUTTON)

    @property
    def logout_button(self) -> WebElement:
        """
        Logout link within the user menu dropdown property.

        Returns a fresh WebElement reference on each access using wait_for_clickable
        to ensure the logout link is available for clicking. This button appears
        within the user menu dropdown after clicking the popup_button.

        Locator Strategy:
            By.XPATH: "//a[.='Log out']"
            Original Java: @FindBy(xpath = "//a[.='Log out']")
            Text-based XPath for resilience to DOM structure changes

        Wait Strategy:
            Uses wait_for_clickable() to ensure logout link is:
            - Present in DOM (menu dropdown expanded)
            - Visible in dropdown menu
            - Enabled for interaction
            - Ready to trigger logout action

        Returns:
            WebElement: The logout link element ready for clicking

        Raises:
            TimeoutException: If logout button not clickable within default timeout
                            (usually indicates dropdown not expanded or page navigation issue)

        Example:
            >>> logout_page = LogoutPage(driver)
            >>> logout_page.popup_button.click()  # First expand menu
            >>> logout_link = logout_page.logout_button
            >>> logout_link.click()  # Trigger logout action
            >>>
            >>> # Verify button text
            >>> assert logout_page.logout_button.text == "Log out"
        """
        self._logger.debug("Accessing logout_button element")
        return self.wait_for_clickable(self._LOGOUT_BUTTON)

    @property
    def warning_message(self) -> WebElement:
        """
        Optional warning dialog displayed during logout property.

        Returns a fresh WebElement reference on each access using wait_for_visibility
        to ensure any warning message dialog is visible before interaction. This element
        may not always appear depending on application state or unsaved changes.

        Locator Strategy:
            By.XPATH: "//div[@class='o_dialog_warning modal-body']"
            Original Java: @FindBy(xpath = "//div[@class= 'o_dialog_warning modal-body']")
            Class-based XPath for modal dialog body

        Wait Strategy:
            Uses wait_for_visibility() to ensure warning dialog is:
            - Present in DOM
            - Visible on screen (modal displayed)
            - Has dimensions (not hidden)
            - Ready for text extraction or interaction

        Returns:
            WebElement: The warning message dialog element

        Raises:
            TimeoutException: If warning message not visible within default timeout
                            This is expected behavior when no warning is displayed
                            Caller should handle TimeoutException for optional warnings

        Example:
            >>> logout_page = LogoutPage(driver)
            >>> logout_page.logout()
            >>>
            >>> # Check for optional warning
            >>> try:
            ...     warning = logout_page.warning_message
            ...     print(f"Warning displayed: {warning.text}")
            ... except TimeoutException:
            ...     print("No warning message - logout proceeding normally")
            >>>
            >>> # Assert specific warning text
            >>> from selenium.common.exceptions import TimeoutException
            >>> try:
            ...     warning = logout_page.warning_message
            ...     assert "unsaved changes" in warning.text.lower()
            ... except TimeoutException:
            ...     pass  # No warning is acceptable
        """
        self._logger.debug("Accessing warning_message element")
        return self.wait_for_visibility(self._WARNING_MESSAGE)

    def logout(self) -> None:
        """
        Perform complete logout workflow.

        This high-level method encapsulates the entire logout process:
        1. Click user menu popup button to expand dropdown
        2. Wait for logout button to become clickable in dropdown
        3. Click logout button to initiate session termination
        4. Log completion of logout action

        The method handles the two-step logout interaction pattern used in the
        Testinium application, ensuring each step completes before proceeding.

        Wait Strategy:
            Each element access uses property methods with explicit waits:
            - popup_button: Waits for user menu button clickability
            - logout_button: Waits for logout link clickability after dropdown expansion

        Error Handling:
            Raises TimeoutException if any element not found within timeout:
            - popup_button timeout: Page not loaded or user menu unavailable
            - logout_button timeout: Dropdown not expanded or navigation issue

        Returns:
            None

        Raises:
            TimeoutException: If popup_button or logout_button not clickable
            WebDriverException: If click operations fail due to browser issues

        Example:
            >>> from pages.logout_page import LogoutPage
            >>> from utilities.driver_manager import DriverManager
            >>>
            >>> driver = DriverManager.get_driver()
            >>> driver.get("https://testinium.example.com/dashboard")
            >>> logout_page = LogoutPage(driver)
            >>>
            >>> # Perform logout with single method call
            >>> logout_page.logout()
            >>>
            >>> # Verify user redirected to login page
            >>> from selenium.webdriver.support.ui import WebDriverWait
            >>> from selenium.webdriver.support import expected_conditions as EC
            >>> WebDriverWait(driver, 10).until(
            ...     EC.url_contains("login")
            ... )

        Usage in Step Definitions:
            >>> from behave import when
            >>> from pages.logout_page import LogoutPage
            >>>
            >>> @when('User logs out')
            >>> def user_logs_out(context):
            ...     logout_page = LogoutPage(context.driver)
            ...     logout_page.logout()
        """
        self._logger.info("Starting logout workflow")

        try:
            # Step 1: Click user menu popup button to expand dropdown
            self._logger.debug("Clicking user menu popup button")
            self.popup_button.click()
            self._logger.debug("User menu dropdown expanded")

            # Step 2: Click logout button in the expanded dropdown
            self._logger.debug("Clicking logout button")
            self.logout_button.click()
            self._logger.info("Logout workflow completed successfully")

        except Exception as exc:
            self._logger.error("Logout workflow failed: %s", exc)
            raise


# Module-level execution for documentation and verification
if __name__ == "__main__":
    """
    Module self-test demonstrating LogoutPage functionality.

    Note: This requires a running Selenium WebDriver instance and authenticated
    session. Primarily for documentation purposes. Actual usage should be in
    Behave step definitions or test scripts.
    """
    print("LogoutPage module loaded successfully")
    print("\nLogoutPage provides:")
    print("  - popup_button: User menu dropdown trigger")
    print("  - logout_button: Logout link in dropdown")
    print("  - warning_message: Optional warning dialog")
    print("  - logout(): Complete logout workflow method")
    print("\nExample usage in step definitions:")
    print("""
    from behave import when
    from pages.logout_page import LogoutPage

    @when('User clicks on logout button')
    def click_logout_button(context):
        logout_page = LogoutPage(context.driver)
        logout_page.popup_button.click()
        logout_page.logout_button.click()

    @when('User logs out')
    def user_logs_out(context):
        logout_page = LogoutPage(context.driver)
        logout_page.logout()  # Complete workflow in one call
    """)
