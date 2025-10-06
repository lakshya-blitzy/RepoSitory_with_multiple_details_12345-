"""
Login Page Module

Page object for user authentication providing element locators and login workflow methods.
This module migrates Java PageFactory pattern to Python property-based element access.

Migration Context:
    Converted from: src/main/java/com/testinium/pages/LoginP.java
    Original Pattern: PageFactory with @FindBy annotations and public WebElement fields
    Target Pattern: Property-based locators with explicit waits and encapsulation

Critical Changes:
    **DEDUPLICATION FIX**: The original Java file (LoginP.java) had duplicate password
    field locators at lines 16-17 (inputPassword) and lines 31-32 (bulletPass), both
    using @FindBy(name="password"). This Python implementation consolidates them into
    a single _INPUT_PASSWORD locator following the technical specification requirement
    for "deduplication of password field locator" (Section 0.4.3 and 0.5.1).

Key Features:
    - Email input element locator
    - Password input element locator (deduplicated from Java)
    - Login button element locator
    - Reset password link element locator
    - Dashboard verification element locator
    - Error message alert element locator
    - High-level login() method encapsulating authentication workflow

Design Pattern:
    Follows Page Object Model with property-based element access. Each property
    returns a fresh WebElement reference via BasePage wait methods, preventing
    stale element exceptions common in Java PageFactory pattern.

Example Usage:
    >>> from selenium import webdriver
    >>> from pages.login_page import LoginPage
    >>>
    >>> driver = webdriver.Chrome()
    >>> driver.get("https://testinium.example.com/login")
    >>> login_page = LoginPage(driver)
    >>>
    >>> # Access individual elements
    >>> login_page.input_email.send_keys("user@example.com")
    >>> login_page.input_password.send_keys("password123")
    >>> login_page.login_button.click()
    >>>
    >>> # Or use high-level login method
    >>> login_page.login("user@example.com", "password123")
    >>>
    >>> # Verify successful login
    >>> assert login_page.dashboard.is_displayed()
"""

import logging
from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Login page object for Testinium application user authentication.

    This class provides element locators and interaction methods for the login page,
    replacing Java's PageFactory annotation-based approach with Python property-based
    locators that use explicit waits for improved reliability.

    Attributes:
        _INPUT_EMAIL: Locator tuple for email/username input field
        _INPUT_PASSWORD: Locator tuple for password input field (DEDUPLICATED from Java)
        _LOGIN_BUTTON: Locator tuple for login submit button
        _RESET_PASSWORD_LINK: Locator tuple for password reset link
        _DASHBOARD: Locator tuple for dashboard element (login success verification)
        _ALERT_ERROR_MESSAGE: Locator tuple for error message alert

    Inherited Attributes (from BasePage):
        driver: Selenium WebDriver instance
        config: ConfigReader for accessing configuration
        wait: WebDriverWait instance with default timeout
        actions: ActionChains for complex interactions
        default_timeout: Default explicit wait timeout in seconds

    Element Access Pattern:
        All element properties use @property decorator and call BasePage wait methods
        (wait_for_element, wait_for_clickable, wait_for_visibility) to return fresh
        WebElement references, preventing stale element exceptions.

    Java Migration Notes:
        Original Java implementation (LoginP.java):
        - Line 13-14: @FindBy(name = "login") public WebElement inputEmail
        - Line 16-17: @FindBy(name="password") public WebElement inputPassword
        - Line 19-20: @FindBy(xpath = "//button[.='Log in']") public WebElement button
        - Line 22-23: @FindBy(xpath = "//a[.='Reset Password']") public WebElement resetPass
        - Line 25-26: @FindBy(id = "oe_main_menu_navbar") public WebElement dashboard
        - Line 28-29: @FindBy(className = "alert") public WebElement alertErrorMessage
        - Line 31-32: @FindBy(name="password") public WebElement bulletPass [DUPLICATE - REMOVED]

        Python implementation consolidates the duplicate password locators and uses
        property-based access with explicit waits instead of PageFactory.

    Thread Safety:
        LoginPage instances are thread-safe when each thread uses its own WebDriver
        instance (achieved via threading.local() in DriverManager). Parallel test
        execution with separate drivers maintains proper isolation.

    Example:
        >>> from selenium import webdriver
        >>> from pages.login_page import LoginPage
        >>>
        >>> driver = webdriver.Chrome()
        >>> driver.get("https://testinium.example.com/login")
        >>> login_page = LoginPage(driver)
        >>>
        >>> # Perform login
        >>> login_page.login("admin@example.com", "secure_password")
        >>>
        >>> # Verify login success
        >>> if login_page.dashboard.is_displayed():
        ...     print("Login successful!")
        >>>
        >>> # Handle login failure
        >>> if login_page.alert_error_message.is_displayed():
        ...     error_text = login_page.alert_error_message.text
        ...     print(f"Login failed: {error_text}")
    """

    # Private locator constants (replacing Java @FindBy annotations)
    # These tuples are used by property methods to locate elements with explicit waits

    # Email/username input field locator
    # Java: @FindBy(name = "login") public WebElement inputEmail
    _INPUT_EMAIL: Tuple[str, str] = (By.NAME, "login")

    # Password input field locator
    # **DEDUPLICATION**: Consolidated from two Java fields:
    #   - Line 16-17: @FindBy(name="password") public WebElement inputPassword
    #   - Line 31-32: @FindBy(name="password") public WebElement bulletPass
    # Both used identical locator (name="password"), creating unnecessary duplication
    _INPUT_PASSWORD: Tuple[str, str] = (By.NAME, "password")

    # Login submit button locator
    # Java: @FindBy(xpath = "//button[.='Log in']") public WebElement button
    _LOGIN_BUTTON: Tuple[str, str] = (By.XPATH, "//button[.='Log in']")

    # Reset password link locator
    # Java: @FindBy(xpath = "//a[.='Reset Password']") public WebElement resetPass
    _RESET_PASSWORD_LINK: Tuple[str, str] = (By.XPATH, "//a[.='Reset Password']")

    # Dashboard element locator for login success verification
    # Java: @FindBy(id = "oe_main_menu_navbar") public WebElement dashboard
    _DASHBOARD: Tuple[str, str] = (By.ID, "oe_main_menu_navbar")

    # Error message alert locator for login failure detection
    # Java: @FindBy(className = "alert") public WebElement alertErrorMessage
    _ALERT_ERROR_MESSAGE: Tuple[str, str] = (By.CLASS_NAME, "alert")

    def __init__(self, driver) -> None:
        """
        Initialize LoginPage with WebDriver instance.

        Calls BasePage.__init__ to set up driver, configuration, wait utilities,
        and logging infrastructure. No PageFactory.initElements() call needed as
        Python uses property-based lazy element location.

        Args:
            driver: Selenium WebDriver instance for browser automation
                   Expected to be thread-local instance from DriverManager

        Example:
            >>> from selenium import webdriver
            >>> from pages.login_page import LoginPage
            >>>
            >>> driver = webdriver.Chrome()
            >>> login_page = LoginPage(driver)
            >>> # login_page.driver, login_page.wait, login_page.config available
        """
        super().__init__(driver)
        self._logger = logging.getLogger(__name__)
        self._logger.info("LoginPage initialized")

    # Property-based element accessors (replacing Java public WebElement fields)
    # Each property calls BasePage wait methods to return fresh element references

    @property
    def input_email(self) -> WebElement:
        """
        Email/username input field element.

        Returns fresh WebElement reference via explicit wait for element presence.
        Replaces Java's public WebElement inputEmail field with encapsulated property.

        Java equivalent:
            @FindBy(name = "login")
            public WebElement inputEmail;

        Returns:
            WebElement: Email input element when present in DOM

        Raises:
            TimeoutException: If element not found within default timeout

        Example:
            >>> login_page.input_email.clear()
            >>> login_page.input_email.send_keys("user@example.com")
        """
        self._logger.debug("Accessing input_email element")
        return self.wait_for_element(self._INPUT_EMAIL)

    @property
    def input_password(self) -> WebElement:
        """
        Password input field element.

        Returns fresh WebElement reference via explicit wait for element presence.
        **DEDUPLICATED**: Consolidates Java's inputPassword (line 16) and bulletPass
        (line 31) fields which both used identical @FindBy(name="password") locator.

        Java equivalent (DUPLICATE removed):
            @FindBy(name="password")
            public WebElement inputPassword;  // Line 16-17

            @FindBy(name="password")
            public WebElement bulletPass;  // Line 31-32 [DUPLICATE - CONSOLIDATED]

        Returns:
            WebElement: Password input element when present in DOM

        Raises:
            TimeoutException: If element not found within default timeout

        Example:
            >>> login_page.input_password.clear()
            >>> login_page.input_password.send_keys("SecurePassword123")
        """
        self._logger.debug("Accessing input_password element (deduplicated locator)")
        return self.wait_for_element(self._INPUT_PASSWORD)

    @property
    def login_button(self) -> WebElement:
        """
        Login submit button element.

        Returns fresh WebElement reference via explicit wait for element clickability.
        Uses wait_for_clickable to ensure button is visible, enabled, and interactable
        before returning, preventing click failures.

        Java equivalent:
            @FindBy(xpath = "//button[.='Log in']")
            public WebElement button;

        Returns:
            WebElement: Login button when clickable

        Raises:
            TimeoutException: If button not clickable within default timeout

        Example:
            >>> login_page.login_button.click()
        """
        self._logger.debug("Accessing login_button element")
        return self.wait_for_clickable(self._LOGIN_BUTTON)

    @property
    def reset_password_link(self) -> WebElement:
        """
        Reset password link element.

        Returns fresh WebElement reference via explicit wait for element clickability.
        Used for navigating to password reset flow when user forgets credentials.

        Java equivalent:
            @FindBy(xpath = "//a[.='Reset Password']")
            public WebElement resetPass;

        Returns:
            WebElement: Reset password link when clickable

        Raises:
            TimeoutException: If link not clickable within default timeout

        Example:
            >>> login_page.reset_password_link.click()
            >>> # User redirected to password reset page
        """
        self._logger.debug("Accessing reset_password_link element")
        return self.wait_for_clickable(self._RESET_PASSWORD_LINK)

    @property
    def dashboard(self) -> WebElement:
        """
        Dashboard element for login success verification.

        Returns fresh WebElement reference via explicit wait for element visibility.
        Used to verify successful login by confirming dashboard navbar appears after
        authentication completes.

        Java equivalent:
            @FindBy(id = "oe_main_menu_navbar")
            public WebElement dashboard;

        Returns:
            WebElement: Dashboard navbar when visible

        Raises:
            TimeoutException: If dashboard not visible within default timeout
                            (indicates login failure or redirection issue)

        Example:
            >>> login_page.login("user@example.com", "password")
            >>> # Verify login succeeded
            >>> assert login_page.dashboard.is_displayed()
            >>> assert "Dashboard" in driver.title
        """
        self._logger.debug("Accessing dashboard element for login verification")
        return self.wait_for_visibility(self._DASHBOARD)

    @property
    def alert_error_message(self) -> WebElement:
        """
        Error message alert element for login failure detection.

        Returns fresh WebElement reference via explicit wait for element visibility.
        Used to capture and verify error messages when login fails due to invalid
        credentials, account issues, or server errors.

        Java equivalent:
            @FindBy(className = "alert")
            public WebElement alertErrorMessage;

        Returns:
            WebElement: Alert element when visible

        Raises:
            TimeoutException: If alert not visible within default timeout
                            (indicates no error occurred - successful login)

        Example:
            >>> login_page.login("invalid@example.com", "wrongpassword")
            >>> # Capture error message
            >>> if login_page.alert_error_message.is_displayed():
            ...     error_text = login_page.alert_error_message.text
            ...     assert "Invalid credentials" in error_text
        """
        self._logger.debug("Accessing alert_error_message element")
        return self.wait_for_visibility(self._ALERT_ERROR_MESSAGE)

    # High-level action methods (business logic)

    def login(self, username: str, password: str) -> None:
        """
        Perform complete login workflow with provided credentials.

        High-level method encapsulating the full authentication process:
        1. Clear and enter username in email field
        2. Clear and enter password in password field
        3. Click login button
        4. Wait for page to process login attempt

        This method provides a single entry point for authentication, improving
        test readability and maintainability compared to individual element
        interactions in step definitions.

        Args:
            username: User's email address or username
                     Example: "admin@example.com", "sales_manager"
            password: User's password (handled securely, not logged)

        Raises:
            TimeoutException: If email input, password input, or login button
                            not found/clickable within timeout
            Exception: If element interaction fails (e.g., element not interactable)

        Security Note:
            Password parameter is not logged to prevent credential exposure in logs.
            Only username (non-sensitive) is logged for debugging purposes.

        Example:
            >>> from pages.login_page import LoginPage
            >>>
            >>> # Successful login
            >>> login_page.login("admin@example.com", "SecurePass123")
            >>> assert login_page.dashboard.is_displayed()
            >>>
            >>> # Failed login
            >>> login_page.login("invalid@example.com", "wrongpass")
            >>> assert login_page.alert_error_message.is_displayed()
            >>>
            >>> # Usage in Behave step definition
            >>> @when('User logs in with "{username}" and "{password}"')
            >>> def step_login(context, username, password):
            ...     login_page = LoginPage(context.driver)
            ...     login_page.login(username, password)
        """
        self._logger.info("Performing login for user: %s", username)

        try:
            # Clear and enter username
            self._logger.debug("Entering username")
            email_field = self.input_email
            email_field.clear()
            email_field.send_keys(username)

            # Clear and enter password (not logged for security)
            self._logger.debug("Entering password (not logged for security)")
            password_field = self.input_password
            password_field.clear()
            password_field.send_keys(password)

            # Click login button
            self._logger.debug("Clicking login button")
            self.login_button.click()

            self._logger.info("Login workflow completed for user: %s", username)

        except TimeoutException as timeout_err:
            self._logger.error(
                "Login failed - timeout waiting for element: %s",
                timeout_err
            )
            raise

        except Exception as exc:
            self._logger.exception(
                "Login failed for user %s with unexpected error: %s",
                username,
                exc
            )
            raise


# Module-level example demonstrating LoginPage usage
if __name__ == "__main__":
    """
    Module self-test demonstrating LoginPage functionality.

    Note: This requires a running Selenium WebDriver instance and active Testinium
    application. Primarily for documentation purposes - actual usage should be in
    Behave step definitions or test scripts.
    """
    print("LoginPage module loaded successfully")
    print("This module provides login page object for Testinium application")
    print("\nKey features:")
    print("  - Deduplicated password field locator (consolidated from Java lines 16 and 31)")
    print("  - Property-based element access with explicit waits")
    print("  - High-level login() method for authentication workflow")
    print("  - Inherits wait utilities from BasePage")
    print("\nExample usage:")
    print("""
    from selenium import webdriver
    from pages.login_page import LoginPage

    driver = webdriver.Chrome()
    driver.get("https://testinium.example.com/login")
    
    login_page = LoginPage(driver)
    login_page.login("user@example.com", "password123")
    
    # Verify successful login
    assert login_page.dashboard.is_displayed()
    
    driver.quit()
    """)
