"""
Base Page Module

Abstract base class providing common WebDriver utilities for all page objects.
This module replaces Java's PageFactory pattern with property-based element access.

Key Features:
- Explicit wait helpers (wait_for_element, wait_for_clickable, wait_for_visibility, wait_for_text)
- Element interaction methods with built-in waiting
- ActionChains integration for complex interactions (drag-and-drop)
- Configuration access via ConfigReader
- Logging capabilities for page object interactions
- Foundation for property-based locators in child page classes

Migration Context:
    This class has no direct Java equivalent. The Java implementation used
    PageFactory with @FindBy annotations for element location. This Python
    implementation provides a more flexible foundation using property-based
    locators that call wait methods, preventing stale element references.

Design Pattern:
    All 10 page object classes (LoginPage, CalendarPage, ContactsPage, CrmPage,
    EmployeePage, InventoryPage, LogoutPage, NotesPage, SalesPage, SessionPage)
    inherit from BasePage to eliminate code duplication and ensure consistent
    wait strategies across the test framework.

Wait Strategy:
    Following technical specification requirements (Section 0.8.1):
    - Uses ONLY explicit waits (no implicit waits)
    - Configurable timeout from config.yaml 'timeouts.default_explicit_wait'
    - Fallback default of 10 seconds if configuration missing
    - Eliminates Thread.sleep() anti-pattern from Java implementation

Example Usage:
    >>> from pages.base_page import BasePage
    >>> from selenium.webdriver.common.by import By
    >>>
    >>> class LoginPage(BasePage):
    ...     _INPUT_EMAIL = (By.NAME, "login")
    ...
    ...     @property
    ...     def input_email(self):
    ...         return self.wait_for_element(self._INPUT_EMAIL)
    ...
    ...     def login(self, username, password):
    ...         self.input_email.send_keys(username)
"""

import logging
from typing import Tuple, List, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from utilities.config_reader import ConfigReader


class BasePage:
    """
    Abstract base class for all page objects providing common WebDriver utilities.

    This class establishes the foundation for the Page Object Model pattern in the
    Python/Behave test framework, replacing Java's PageFactory annotation-based
    approach with property-based element access.

    Attributes:
        driver (WebDriver): Selenium WebDriver instance for browser interaction
        config (ConfigReader): Configuration reader singleton for accessing settings
        default_timeout (int): Default explicit wait timeout in seconds
        wait (WebDriverWait): Pre-configured WebDriverWait instance
        actions (ActionChains): ActionChains instance for complex interactions
        _logger (Logger): Logger instance for page object operations

    Thread Safety:
        BasePage instances are thread-safe when each thread has its own WebDriver
        instance (achieved via threading.local() in DriverManager). Each BasePage
        instance is tied to a specific WebDriver, so parallel test execution with
        separate drivers maintains isolation.

    Design Decisions:
        1. Instance-based (not static): Each page instance has its own driver reference
        2. Explicit waits only: No implicit waits to avoid unpredictable behavior
        3. Property-based locators: Child classes define locators as tuples and use
           properties that call wait methods for fresh element references
        4. Configurable timeouts: Default timeout from config.yaml, overridable per-method
        5. Comprehensive logging: All wait operations logged for debugging

    Example:
        >>> from selenium import webdriver
        >>> from pages.login_page import LoginPage
        >>>
        >>> driver = webdriver.Chrome()
        >>> login_page = LoginPage(driver)
        >>> login_page.input_email.send_keys("user@example.com")
    """

    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize BasePage with WebDriver instance and common utilities.

        This constructor establishes the foundation for all page objects by:
        1. Storing the WebDriver reference for element interaction
        2. Loading configuration via ConfigReader singleton
        3. Setting up default explicit wait timeout (config or 10s fallback)
        4. Creating WebDriverWait instance for element synchronization
        5. Initializing ActionChains for complex interactions
        6. Setting up logger for page object operations

        Args:
            driver: Selenium WebDriver instance for browser automation
                   Expected to be a thread-local instance from DriverManager
                   supporting parallel test execution

        Configuration:
            Attempts to load 'timeouts.default_explicit_wait' from config.yaml
            Falls back to 10 seconds if configuration key missing

        Example:
            >>> from selenium import webdriver
            >>> from pages.base_page import BasePage
            >>>
            >>> driver = webdriver.Chrome()
            >>> base_page = BasePage(driver)
            >>> # base_page.driver, base_page.wait, base_page.actions available
        """
        self.driver = driver
        self.config = ConfigReader()
        self._logger = logging.getLogger(__name__)

        # Configure default timeout from config.yaml or fallback to 10 seconds
        # Technical specification: "configure default timeout from config.yaml
        # 'timeouts.default_explicit_wait' with fallback to 10 seconds"
        try:
            self.default_timeout = self.config.get_property(
                'timeouts.default_explicit_wait',
                default=10
            )
            # Handle case where config value is string (convert to int)
            if isinstance(self.default_timeout, str):
                self.default_timeout = int(self.default_timeout)
            self._logger.debug(
                "BasePage initialized with default timeout: %ds (from configuration)",
                self.default_timeout
            )
        except (ValueError, TypeError) as err:
            self._logger.warning(
                "Failed to parse timeout from configuration, using 10s default: %s",
                err
            )
            self.default_timeout = 10

        # Initialize WebDriverWait with default timeout
        self.wait = WebDriverWait(self.driver, self.default_timeout)

        # Initialize ActionChains for drag-and-drop and complex interactions
        self.actions = ActionChains(self.driver)

        self._logger.info(
            "BasePage initialized for %s with timeout=%ds",
            self.__class__.__name__,
            self.default_timeout
        )

    def wait_for_element(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        Wait for element to be present in the DOM and return it.

        This method uses Selenium's expected_conditions.presence_of_element_located
        to wait for an element to appear in the DOM. The element may not be visible
        or interactable, but it exists in the page structure.

        Use Cases:
        - Waiting for hidden elements that will become visible
        - Confirming element existence without visibility requirement
        - Retrieving elements that may be off-screen but present

        Args:
            locator: Tuple of (By strategy, locator value)
                    Examples: (By.ID, 'login'), (By.XPATH, '//button[@type="submit"]')
            timeout: Custom timeout in seconds (optional)
                    If None, uses self.default_timeout from configuration
                    If provided, overrides default for this specific wait

        Returns:
            WebElement: The located element when present in DOM

        Raises:
            TimeoutException: If element not present within timeout period
                            Exception message includes locator details and timeout value

        Example:
            >>> from selenium.webdriver.common.by import By
            >>> # Using default timeout
            >>> element = base_page.wait_for_element((By.NAME, "username"))
            >>> # Using custom timeout
            >>> slow_element = base_page.wait_for_element(
            ...     (By.ID, "slow-loading"), timeout=30
            ... )
        """
        effective_timeout = timeout if timeout is not None else self.default_timeout
        self._logger.debug(
            "Waiting for element presence: %s (timeout=%ds)",
            locator,
            effective_timeout
        )

        try:
            wait_instance = WebDriverWait(self.driver, effective_timeout)
            element = wait_instance.until(
                EC.presence_of_element_located(locator),
                message=f"Element not present within {effective_timeout}s: {locator}"
            )
            self._logger.debug("Element found: %s", locator)
            return element

        except TimeoutException as timeout_err:
            self._logger.warning(
                "Element not found within %ds: %s",
                effective_timeout,
                locator
            )
            raise

    def wait_for_clickable(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        Wait for element to be clickable (visible and enabled) and return it.

        This method uses Selenium's expected_conditions.element_to_be_clickable
        to wait for an element to be both visible and enabled. This is the recommended
        wait strategy before performing click() operations.

        Clickable Requirements:
        1. Element must be visible on the page
        2. Element must be enabled (not disabled attribute)
        3. Element must not be obscured by other elements

        Use Cases:
        - Waiting for buttons before clicking
        - Ensuring form fields are enabled before interaction
        - Confirming links are clickable before navigation

        Args:
            locator: Tuple of (By strategy, locator value)
                    Examples: (By.ID, 'submit-button'), (By.LINK_TEXT, 'Login')
            timeout: Custom timeout in seconds (optional)
                    If None, uses self.default_timeout from configuration

        Returns:
            WebElement: The clickable element

        Raises:
            TimeoutException: If element not clickable within timeout period
                            Element may exist but still loading or disabled

        Example:
            >>> from selenium.webdriver.common.by import By
            >>> # Wait for button to be clickable then click
            >>> button = base_page.wait_for_clickable((By.ID, "submit"))
            >>> button.click()
            >>>
            >>> # Wait for link with custom timeout
            >>> link = base_page.wait_for_clickable(
            ...     (By.LINK_TEXT, "Next Page"),
            ...     timeout=15
            ... )
            >>> link.click()
        """
        effective_timeout = timeout if timeout is not None else self.default_timeout
        self._logger.debug(
            "Waiting for element clickability: %s (timeout=%ds)",
            locator,
            effective_timeout
        )

        try:
            wait_instance = WebDriverWait(self.driver, effective_timeout)
            element = wait_instance.until(
                EC.element_to_be_clickable(locator),
                message=f"Element not clickable within {effective_timeout}s: {locator}"
            )
            self._logger.debug("Element is clickable: %s", locator)
            return element

        except TimeoutException as timeout_err:
            self._logger.warning(
                "Element not clickable within %ds: %s",
                effective_timeout,
                locator
            )
            raise

    def wait_for_visibility(
        self,
        locator: Tuple[str, str],
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        Wait for element to be visible on the page and return it.

        This method uses Selenium's expected_conditions.visibility_of_element_located
        to wait for an element to be visible. An element is considered visible when:
        1. It exists in the DOM
        2. It has height and width greater than 0
        3. It's not hidden (display: none, visibility: hidden)

        Use Cases:
        - Confirming alerts or modals are displayed
        - Verifying success/error messages appear
        - Ensuring UI elements rendered before assertion
        - Waiting for animations to complete

        Args:
            locator: Tuple of (By strategy, locator value)
                    Examples: (By.CLASS_NAME, 'alert'), (By.ID, 'success-message')
            timeout: Custom timeout in seconds (optional)
                    If None, uses self.default_timeout from configuration

        Returns:
            WebElement: The visible element

        Raises:
            TimeoutException: If element not visible within timeout period
                            Element may be present but hidden or zero-sized

        Example:
            >>> from selenium.webdriver.common.by import By
            >>> # Wait for success message to appear
            >>> message = base_page.wait_for_visibility(
            ...     (By.CLASS_NAME, "success-message")
            ... )
            >>> assert "Success" in message.text
            >>>
            >>> # Wait for modal with custom timeout
            >>> modal = base_page.wait_for_visibility(
            ...     (By.ID, "confirmation-modal"),
            ...     timeout=5
            ... )
        """
        effective_timeout = timeout if timeout is not None else self.default_timeout
        self._logger.debug(
            "Waiting for element visibility: %s (timeout=%ds)",
            locator,
            effective_timeout
        )

        try:
            wait_instance = WebDriverWait(self.driver, effective_timeout)
            element = wait_instance.until(
                EC.visibility_of_element_located(locator),
                message=f"Element not visible within {effective_timeout}s: {locator}"
            )
            self._logger.debug("Element is visible: %s", locator)
            return element

        except TimeoutException as timeout_err:
            self._logger.warning(
                "Element not visible within %ds: %s",
                effective_timeout,
                locator
            )
            raise

    def wait_for_text(
        self,
        locator: Tuple[str, str],
        text: str,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for specific text to be present in an element.

        This method uses Selenium's expected_conditions.text_to_be_present_in_element
        to wait for an element to contain expected text. This is useful for verifying
        dynamic content updates or page state changes.

        Text Matching:
        - Case-sensitive substring match
        - Text must be present anywhere in element's visible text
        - Includes text from child elements

        Use Cases:
        - Verifying page title updates after navigation
        - Confirming dynamic content loaded
        - Validating form validation messages
        - Checking status indicators changed

        Args:
            locator: Tuple of (By strategy, locator value)
                    Examples: (By.ID, 'page-title'), (By.CLASS_NAME, 'status')
            text: Expected text string (case-sensitive substring)
            timeout: Custom timeout in seconds (optional)
                    If None, uses self.default_timeout from configuration

        Returns:
            bool: True if text present within timeout
                 (always True as TimeoutException raised on failure)

        Raises:
            TimeoutException: If text not present in element within timeout period

        Example:
            >>> from selenium.webdriver.common.by import By
            >>> # Wait for dashboard title to appear
            >>> base_page.wait_for_text(
            ...     (By.ID, "page-title"),
            ...     "Dashboard"
            ... )
            >>>
            >>> # Wait for status update with custom timeout
            >>> base_page.wait_for_text(
            ...     (By.CLASS_NAME, "status-indicator"),
            ...     "Active",
            ...     timeout=20
            ... )
        """
        effective_timeout = timeout if timeout is not None else self.default_timeout
        self._logger.debug(
            "Waiting for text '%s' in element: %s (timeout=%ds)",
            text,
            locator,
            effective_timeout
        )

        try:
            wait_instance = WebDriverWait(self.driver, effective_timeout)
            result = wait_instance.until(
                EC.text_to_be_present_in_element(locator, text),
                message=(
                    f"Text '{text}' not present in element {locator} "
                    f"within {effective_timeout}s"
                )
            )
            self._logger.debug("Text '%s' found in element: %s", text, locator)
            return result

        except TimeoutException as timeout_err:
            self._logger.warning(
                "Text '%s' not found in element %s within %ds",
                text,
                locator,
                effective_timeout
            )
            raise

    def get_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """
        Get all elements matching the locator.

        This method finds all elements matching the provided locator tuple.
        Unlike wait_for_element which waits for presence, this method immediately
        returns all matching elements (empty list if none found).

        Use Cases:
        - Retrieving dynamic collections (customer cards, table rows, list items)
        - Counting elements on the page
        - Iterating over multiple similar elements
        - Validating element collections

        Behavior:
        - Returns immediately (no explicit wait)
        - Returns empty list if no elements found (no exception)
        - Returns all matching elements in DOM order
        - Includes hidden and visible elements

        Note:
            If you need to wait for at least one element, use wait_for_element first:
            >>> base_page.wait_for_element((By.CLASS_NAME, "card"))
            >>> cards = base_page.get_elements((By.CLASS_NAME, "card"))

        Args:
            locator: Tuple of (By strategy, locator value)
                    Examples: (By.CLASS_NAME, 'customer-card'),
                             (By.XPATH, '//tr[@class="data-row"]')

        Returns:
            List[WebElement]: List of all matching elements (empty if none found)

        Example:
            >>> from selenium.webdriver.common.by import By
            >>> # Get all customer cards
            >>> cards = base_page.get_elements((By.CLASS_NAME, "customer-card"))
            >>> print(f"Found {len(cards)} customer cards")
            >>>
            >>> # Iterate over table rows
            >>> rows = base_page.get_elements((By.XPATH, "//table//tr"))
            >>> for row in rows:
            ...     print(row.text)
            >>>
            >>> # Check if elements exist
            >>> elements = base_page.get_elements((By.CLASS_NAME, "optional"))
            >>> if elements:
            ...     print("Optional elements found")
        """
        self._logger.debug("Getting all elements matching locator: %s", locator)

        try:
            elements = self.driver.find_elements(*locator)
            self._logger.debug(
                "Found %d element(s) matching locator: %s",
                len(elements),
                locator
            )
            return elements

        except Exception as exc:
            self._logger.error(
                "Error finding elements with locator %s: %s",
                locator,
                exc
            )
            # Return empty list rather than raising exception
            # Consistent with Selenium's find_elements behavior
            return []

    def drag_and_drop(
        self,
        source_locator: Tuple[str, str],
        target_locator: Tuple[str, str]
    ) -> None:
        """
        Perform drag-and-drop operation from source element to target element.

        This method uses Selenium ActionChains to perform complex drag-and-drop
        interactions. It waits for both source and target elements to be visible
        before attempting the drag operation.

        Operation Flow:
        1. Wait for source element visibility
        2. Wait for target element visibility
        3. Perform drag_and_drop action using ActionChains
        4. Execute the action chain
        5. Log success or failure

        Use Cases:
        - Dragging tasks between lists/columns
        - Reordering elements via drag-and-drop
        - Moving items in visual editors
        - Kanban board interactions

        Args:
            source_locator: Tuple of (By strategy, locator value) for element to drag
                          Example: (By.ID, "task-123")
            target_locator: Tuple of (By strategy, locator value) for drop target
                          Example: (By.ID, "column-done")

        Raises:
            TimeoutException: If source or target element not visible
            Exception: If drag-and-drop operation fails

        Example:
            >>> from selenium.webdriver.common.by import By
            >>> # Drag task to completed column
            >>> base_page.drag_and_drop(
            ...     source_locator=(By.ID, "task-123"),
            ...     target_locator=(By.ID, "column-done")
            ... )
            >>>
            >>> # Reorder list items
            >>> base_page.drag_and_drop(
            ...     source_locator=(By.XPATH, "//li[@data-id='1']"),
            ...     target_locator=(By.XPATH, "//li[@data-id='5']")
            ... )
        """
        self._logger.info(
            "Performing drag and drop from %s to %s",
            source_locator,
            target_locator
        )

        try:
            # Wait for source element to be visible
            source_element = self.wait_for_visibility(source_locator)
            self._logger.debug("Source element found and visible: %s", source_locator)

            # Wait for target element to be visible
            target_element = self.wait_for_visibility(target_locator)
            self._logger.debug("Target element found and visible: %s", target_locator)

            # Perform drag and drop using ActionChains
            self.actions.drag_and_drop(source_element, target_element).perform()

            self._logger.info(
                "Drag and drop completed successfully from %s to %s",
                source_locator,
                target_locator
            )

        except TimeoutException as timeout_err:
            self._logger.error(
                "Drag and drop failed - element not visible: %s",
                timeout_err
            )
            raise

        except Exception as exc:
            self._logger.exception(
                "Drag and drop failed from %s to %s: %s",
                source_locator,
                target_locator,
                exc
            )
            raise


# Example usage demonstrating BasePage capabilities
if __name__ == "__main__":
    """
    Module self-test demonstrating BasePage functionality.

    Note: This requires a running Selenium WebDriver instance and is primarily
    for documentation purposes. Actual usage should be in page object subclasses.
    """
    print("BasePage module loaded successfully")
    print("This is an abstract base class - use by inheriting in page objects")
    print("\nExample page object pattern:")
    print("""
    from pages.base_page import BasePage
    from selenium.webdriver.common.by import By

    class LoginPage(BasePage):
        # Define locators as private class constants
        _INPUT_EMAIL = (By.NAME, "login")
        _INPUT_PASSWORD = (By.NAME, "password")
        _BUTTON_LOGIN = (By.XPATH, "//button[.='Log in']")

        # Use properties that call wait methods for fresh element references
        @property
        def input_email(self):
            return self.wait_for_element(self._INPUT_EMAIL)

        @property
        def input_password(self):
            return self.wait_for_element(self._INPUT_PASSWORD)

        @property
        def button_login(self):
            return self.wait_for_clickable(self._BUTTON_LOGIN)

        # High-level action methods
        def login(self, username, password):
            '''Perform login with credentials'''
            self.input_email.send_keys(username)
            self.input_password.send_keys(password)
            self.button_login.click()
    """)
