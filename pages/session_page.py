"""
Session Page Module

Page object for login session management providing element locators and interaction
methods for the Testinium application login form.

This module converts the Java SessionP.java PageFactory pattern to Python property-based
locators with explicit waits, ensuring fresh element references and preventing stale
element exceptions.

Migration Context:
    Converted from: src/main/java/com/testinium/pages/SessionP.java
    Java Pattern: PageFactory with @FindBy annotations and public WebElement fields
    Python Pattern: BasePage inheritance with private locator constants and @property
                   methods returning fresh WebElement references via explicit waits

Key Changes from Java Implementation:
    1. PageFactory.initElements() → __init__(self, driver) with BasePage inheritance
    2. @FindBy(id='login') → _INPUT_LOGIN = (By.ID, 'login') constant
    3. @FindBy(id='password') → _INPUT_PASSWORD = (By.ID, 'password') constant
    4. @FindBy(xpath="//button[.='Log in']") → _LOGIN_BUTTON constant with XPATH
    5. Public WebElement fields → Private @property methods with explicit waits
    6. Direct element access → wait_for_element() and wait_for_clickable() calls

Locator Preservation:
    All 3 original locators from SessionP.java are preserved exactly for behavioral
    equivalence with the Java test framework:
    - id='login' for username input field
    - id='password' for password input field
    - xpath="//button[.='Log in']" for login button (text-based locator)

Thread Safety:
    SessionPage instances are thread-safe when constructed with thread-local WebDriver
    instances from DriverManager.get_driver(). Each test thread has isolated page
    object instances supporting parallel test execution.

Example Usage:
    >>> from selenium import webdriver
    >>> from pages.session_page import SessionPage
    >>>
    >>> driver = webdriver.Chrome()
    >>> session_page = SessionPage(driver)
    >>>
    >>> # Property-based element access with automatic waits
    >>> session_page.input_login.send_keys("user@example.com")
    >>> session_page.input_password.send_keys("password123")
    >>> session_page.login_button.click()
    >>>
    >>> # All elements include explicit waits (no stale element exceptions)
    >>> assert session_page.input_login.is_displayed()
"""

from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class SessionPage(BasePage):
    """
    Session page object for Testinium application login session management.

    Provides access to login form elements (username input, password input, login button)
    using property-based locators with explicit waits. Inherits common WebDriver
    utilities from BasePage including wait_for_element, wait_for_clickable, and
    wait_for_visibility methods.

    This class replaces the Java SessionP.java implementation which used PageFactory
    with @FindBy annotations. The Python implementation uses private locator constants
    and @property decorators for fresh element references on each access.

    Attributes:
        driver (WebDriver): Selenium WebDriver instance (inherited from BasePage)
        wait (WebDriverWait): Pre-configured WebDriverWait instance (inherited)
        config (ConfigReader): Configuration reader singleton (inherited)
        default_timeout (int): Default explicit wait timeout in seconds (inherited)
        actions (ActionChains): ActionChains for complex interactions (inherited)

    Locators:
        _INPUT_LOGIN: Username/email input field locator (id='login')
        _INPUT_PASSWORD: Password input field locator (id='password')
        _LOGIN_BUTTON: Login submit button locator (xpath with text match)

    Properties:
        input_login: WebElement for username input field with automatic wait
        input_password: WebElement for password input field with automatic wait
        login_button: WebElement for login button with clickable wait

    Example:
        >>> from utilities.driver_manager import DriverManager
        >>> from pages.session_page import SessionPage
        >>>
        >>> # Initialize with thread-local driver from DriverManager
        >>> driver = DriverManager.get_driver()
        >>> session_page = SessionPage(driver)
        >>>
        >>> # Perform login using property-based element access
        >>> session_page.input_login.send_keys("salesmanager1@example.com")
        >>> session_page.input_password.send_keys("UserUser")
        >>> session_page.login_button.click()
        >>>
        >>> # Verify elements are displayed
        >>> assert session_page.input_login.is_displayed()
        >>> assert session_page.input_password.is_enabled()
    """

    # Private locator constants following Python naming conventions
    # Preserved from Java SessionP.java for behavioral equivalence
    _INPUT_LOGIN: Tuple[str, str] = (By.ID, "login")
    _INPUT_PASSWORD: Tuple[str, str] = (By.ID, "password")
    _LOGIN_BUTTON: Tuple[str, str] = (By.XPATH, "//button[.='Log in']")

    def __init__(self, driver) -> None:
        """
        Initialize SessionPage with WebDriver instance.

        Replaces Java's PageFactory.initElements(Driver.getDriver(), this) pattern
        with explicit constructor accepting WebDriver instance. Calls BasePage
        constructor to initialize driver, config, wait, and actions attributes.

        This constructor establishes the foundation for property-based element access
        by storing the driver reference and initializing common utilities through
        BasePage inheritance.

        Args:
            driver: Selenium WebDriver instance for browser automation
                   Expected to be thread-local instance from DriverManager.get_driver()
                   supporting parallel test execution with isolated sessions

        Example:
            >>> from selenium import webdriver
            >>> from pages.session_page import SessionPage
            >>>
            >>> driver = webdriver.Chrome()
            >>> session_page = SessionPage(driver)
            >>> # session_page.driver, session_page.wait, session_page.config available
        """
        super().__init__(driver)

    @property
    def input_login(self) -> WebElement:
        """
        Username/email input field element with automatic presence wait.

        Returns fresh WebElement reference on each access by calling BasePage.wait_for_element()
        with _INPUT_LOGIN locator. This prevents stale element exceptions and ensures
        element is present in DOM before interaction.

        Locator Strategy:
            By.ID = 'login' (preserved from Java @FindBy(id = "login"))
            ID-based locator provides fast, stable element identification

        Wait Strategy:
            Uses explicit wait for element presence (BasePage.wait_for_element)
            Default timeout from config.yaml 'timeouts.default_explicit_wait'
            Fallback timeout of 10 seconds if configuration missing

        Returns:
            WebElement: Username input field element when present in DOM
                       Element may be visible or hidden but exists in page structure

        Raises:
            TimeoutException: If username input field not found within timeout period
                            Indicates page not loaded or element locator changed

        Example:
            >>> session_page = SessionPage(driver)
            >>> # Property access automatically waits for element presence
            >>> username_field = session_page.input_login
            >>> username_field.send_keys("user@example.com")
            >>> username_field.clear()
            >>> username_field.send_keys("different@example.com")
            >>>
            >>> # Verify element attributes
            >>> assert session_page.input_login.get_attribute("id") == "login"
            >>> assert session_page.input_login.is_displayed()
        """
        return self.wait_for_element(self._INPUT_LOGIN)

    @property
    def input_password(self) -> WebElement:
        """
        Password input field element with automatic presence wait.

        Returns fresh WebElement reference on each access by calling BasePage.wait_for_element()
        with _INPUT_PASSWORD locator. This prevents stale element exceptions and ensures
        element is present in DOM before interaction.

        Locator Strategy:
            By.ID = 'password' (preserved from Java @FindBy(id = "password"))
            ID-based locator provides fast, stable element identification

        Wait Strategy:
            Uses explicit wait for element presence (BasePage.wait_for_element)
            Default timeout from config.yaml 'timeouts.default_explicit_wait'
            Fallback timeout of 10 seconds if configuration missing

        Returns:
            WebElement: Password input field element when present in DOM
                       Element may be visible or hidden but exists in page structure

        Raises:
            TimeoutException: If password input field not found within timeout period
                            Indicates page not loaded or element locator changed

        Example:
            >>> session_page = SessionPage(driver)
            >>> # Property access automatically waits for element presence
            >>> password_field = session_page.input_password
            >>> password_field.send_keys("SecurePassword123")
            >>> password_field.clear()
            >>> password_field.send_keys("UpdatedPassword456")
            >>>
            >>> # Verify element attributes
            >>> assert session_page.input_password.get_attribute("type") == "password"
            >>> assert session_page.input_password.is_enabled()
        """
        return self.wait_for_element(self._INPUT_PASSWORD)

    @property
    def login_button(self) -> WebElement:
        """
        Login submit button element with automatic clickable wait.

        Returns fresh WebElement reference on each access by calling BasePage.wait_for_clickable()
        with _LOGIN_BUTTON locator. This ensures button is both visible and enabled before
        interaction, preventing ElementNotInteractableException.

        Locator Strategy:
            By.XPATH = "//button[.='Log in']" (preserved from Java)
            Text-based XPath locator resilient to structural DOM changes
            Matches button element with exact text content 'Log in'

        Wait Strategy:
            Uses explicit wait for element clickability (BasePage.wait_for_clickable)
            Ensures button is visible, enabled, and not obscured
            Default timeout from config.yaml 'timeouts.default_explicit_wait'
            Fallback timeout of 10 seconds if configuration missing

        Returns:
            WebElement: Login button element when clickable (visible and enabled)
                       Ready for immediate click() operation

        Raises:
            TimeoutException: If login button not clickable within timeout period
                            Indicates page loading, button disabled, or element locator changed

        Example:
            >>> session_page = SessionPage(driver)
            >>> # Property access automatically waits for button to be clickable
            >>> login_btn = session_page.login_button
            >>> login_btn.click()
            >>>
            >>> # Verify button is clickable before click
            >>> assert session_page.login_button.is_displayed()
            >>> assert session_page.login_button.is_enabled()
            >>> session_page.login_button.click()
            >>>
            >>> # Button text verification
            >>> assert session_page.login_button.text == "Log in"
        """
        return self.wait_for_clickable(self._LOGIN_BUTTON)


# Module-level documentation for import validation
if __name__ == "__main__":
    """
    Module self-test demonstrating SessionPage functionality.

    This section provides usage examples and verifies the module can be imported
    successfully. Actual test execution requires running WebDriver instance and
    should be performed through Behave step definitions.
    """
    print("SessionPage module loaded successfully")
    print("\nSessionPage converted from Java SessionP.java")
    print("Locators preserved for behavioral equivalence:")
    print(f"  - input_login: {SessionPage._INPUT_LOGIN}")
    print(f"  - input_password: {SessionPage._INPUT_PASSWORD}")
    print(f"  - login_button: {SessionPage._LOGIN_BUTTON}")
    print("\nUsage example:")
    print("""
    from utilities.driver_manager import DriverManager
    from pages.session_page import SessionPage

    # Get thread-local WebDriver instance
    driver = DriverManager.get_driver()
    
    # Navigate to login page
    driver.get("https://app.testinium.com/login")
    
    # Initialize SessionPage
    session_page = SessionPage(driver)
    
    # Perform login with automatic waits
    session_page.input_login.send_keys("user@example.com")
    session_page.input_password.send_keys("password123")
    session_page.login_button.click()
    
    # Wait for navigation (handled by step definitions)
    """)
