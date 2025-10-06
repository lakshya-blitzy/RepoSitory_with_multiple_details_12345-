"""
Wait Helpers Module

Centralized explicit wait utilities providing reusable wait methods for test automation.
This module eliminates Thread.sleep() anti-patterns and implicit/explicit wait mixing
from the original Java implementation.

Critical Problems Solved from Java Implementation:
1. Thread.sleep() scattered across step definitions (LoginSD.java line 27: 3s sleep,
   Contacts.java: 3s sleep, multiple locations with 2-7s hardcoded sleeps)
2. Global implicit wait of 10 seconds (Driver.java:34) mixed with explicit waits
   creating unpredictable compound wait behavior
3. Hardcoded timeout values throughout step definitions (2s, 3s, 7s, 20s)
4. No centralized wait strategy or reusable wait utilities

Migration Benefits:
- Predictable, condition-based synchronization
- Configurable timeout values from config.yaml
- Clear timeout visibility with comprehensive logging
- Consistent wait behavior across all test scenarios
- Eliminates flaky tests caused by race conditions

Example Usage:
    >>> from utilities.wait_helpers import WaitHelpers
    >>> from selenium.webdriver.common.by import By
    >>> 
    >>> wait_helper = WaitHelpers(driver)
    >>> # Wait for element presence in DOM
    >>> element = wait_helper.wait_for_element_presence((By.ID, "login-button"))
    >>> 
    >>> # Wait for element to be visible and clickable
    >>> button = wait_helper.wait_for_element_clickable((By.NAME, "submit"))
    >>> button.click()
    >>> 
    >>> # Wait for specific text to appear
    >>> wait_helper.wait_for_text_in_element((By.ID, "status"), "Success")
    >>> 
    >>> # Wait for URL change after navigation
    >>> wait_helper.wait_for_url_contains("/dashboard")
"""

import logging
from typing import Optional, Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utilities.config_reader import ConfigReader


# Configure module logger for wait operation tracking
logger = logging.getLogger(__name__)


class WaitHelpers:
    """
    Centralized explicit wait utilities for Selenium WebDriver automation.
    
    Provides reusable wait methods with configurable timeouts, eliminating:
    - Thread.sleep() anti-pattern from Java implementation
    - Implicit/explicit wait mixing (10s implicit + varying explicit)
    - Hardcoded timeout values scattered across test code
    
    Features:
    - Configurable timeout values loaded from config.yaml
    - Comprehensive logging for debugging timeout issues
    - Multiple wait conditions: presence, visibility, clickability, text, staleness, URL
    - Graceful timeout handling with descriptive error messages
    - Type hints for IDE autocomplete and static type checking
    
    Timeout Configuration:
        Loads timeout values from config/config.yaml under 'timeouts' section:
        - default_timeout: Standard wait duration for most operations (default: 10s)
        - long_timeout: Extended wait for slow operations (default: 20s)
        - short_timeout: Quick wait for fast operations (default: 5s)
    
    Thread Safety:
        Instance-based design with driver reference - each thread should create
        its own WaitHelpers instance with thread-local driver.
    
    Example:
        >>> from utilities.wait_helpers import WaitHelpers
        >>> from utilities.driver_manager import DriverManager
        >>> from selenium.webdriver.common.by import By
        >>> 
        >>> driver = DriverManager.get_driver()
        >>> wait_helper = WaitHelpers(driver)
        >>> 
        >>> # Wait for element with default timeout
        >>> element = wait_helper.wait_for_element_presence((By.ID, "email"))
        >>> 
        >>> # Wait with custom timeout
        >>> button = wait_helper.wait_for_element_clickable(
        ...     (By.XPATH, "//button[@type='submit']"),
        ...     timeout=15
        ... )
        >>> 
        >>> # Wait for page navigation
        >>> wait_helper.wait_for_url_contains("/dashboard", timeout=5)
    """
    
    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize wait helpers with WebDriver instance and load timeout configuration.
        
        Args:
            driver: Selenium WebDriver instance for wait operations
        
        Raises:
            ValueError: If driver is None
            ConfigurationError: If timeout configuration is invalid
        
        Note:
            Timeout values are loaded from config/config.yaml under 'timeouts' section.
            If configuration keys are missing, defaults are used:
            - default_timeout: 10 seconds
            - long_timeout: 20 seconds
            - short_timeout: 5 seconds
        """
        if driver is None:
            raise ValueError("WebDriver instance cannot be None")
        
        self.driver = driver
        logger.debug("Initializing WaitHelpers for driver: %s", type(driver).__name__)
        
        # Load timeout configuration from config.yaml
        try:
            config = ConfigReader()
            
            # Load timeout values with fallback defaults
            # Original Java had: implicit 10s + varying explicit (2s-20s)
            # Python standardizes: short(5s), default(10s), long(20s)
            self.default_timeout = config.get_property(
                'timeouts.explicit',
                default=10
            )
            self.long_timeout = config.get_property(
                'timeouts.page_load',
                default=20
            )
            self.short_timeout = config.get_property(
                'timeouts.short',
                default=5
            )
            
            # Type conversion and validation for timeout values
            try:
                self.default_timeout = int(self.default_timeout)
                self.long_timeout = int(self.long_timeout)
                self.short_timeout = int(self.short_timeout)
            except (ValueError, TypeError) as err:
                logger.warning(
                    "Invalid timeout configuration values, using defaults: %s", err
                )
                self.default_timeout = 10
                self.long_timeout = 20
                self.short_timeout = 5
            
            # Validate timeout values are positive
            if self.default_timeout <= 0 or self.long_timeout <= 0 or self.short_timeout <= 0:
                logger.warning(
                    "Timeout values must be positive, using defaults. "
                    "Got: default=%s, long=%s, short=%s",
                    self.default_timeout, self.long_timeout, self.short_timeout
                )
                self.default_timeout = 10
                self.long_timeout = 20
                self.short_timeout = 5
            
            logger.info(
                "WaitHelpers configured with timeouts - "
                "default: %ss, long: %ss, short: %ss",
                self.default_timeout, self.long_timeout, self.short_timeout
            )
            
        except Exception as exc:
            # If configuration fails, use safe defaults and log warning
            logger.warning(
                "Failed to load timeout configuration, using defaults: %s", exc
            )
            self.default_timeout = 10
            self.long_timeout = 20
            self.short_timeout = 5
    
    def wait_for_element_presence(
        self,
        locator: Tuple[By, str],
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        Wait for element to be present in the DOM (not necessarily visible).
        
        Replaces Java pattern:
            WebElement element = driver.findElement(By.id("field"));
        
        With explicit wait:
            element = wait_helper.wait_for_element_presence((By.ID, "field"))
        
        Use this when:
        - Element must exist in DOM (may be hidden)
        - Checking for element presence before interaction
        - Loading dynamic content via AJAX
        
        Args:
            locator: Tuple of (By strategy, locator string)
                    Examples: (By.ID, "email"), (By.XPATH, "//button[@type='submit']")
            timeout: Maximum wait time in seconds (optional)
                    Uses self.default_timeout if not provided
        
        Returns:
            WebElement: Located element ready for interaction
        
        Raises:
            TimeoutException: If element not found within timeout period
            ValueError: If locator format is invalid
        
        Example:
            >>> # Replace Thread.sleep(3) + findElement pattern
            >>> element = wait_helper.wait_for_element_presence((By.NAME, "login"))
            >>> element.send_keys("user@example.com")
        """
        if not isinstance(locator, tuple) or len(locator) != 2:
            raise ValueError(
                f"Locator must be tuple of (By, str), got: {locator}"
            )
        
        effective_timeout = timeout if timeout is not None else self.default_timeout
        logger.debug(
            "Waiting for element presence: %s='%s' (timeout: %ss)",
            locator[0], locator[1], effective_timeout
        )
        
        try:
            wait = WebDriverWait(self.driver, effective_timeout)
            element = wait.until(
                EC.presence_of_element_located(locator),
                message=f"Element not present in DOM after {effective_timeout}s: {locator}"
            )
            logger.debug("Element found: %s='%s'", locator[0], locator[1])
            return element
            
        except TimeoutException as timeout_err:
            logger.error(
                "Timeout waiting for element presence: %s='%s' (timeout: %ss)",
                locator[0], locator[1], effective_timeout
            )
            raise TimeoutException(
                f"Element not found after {effective_timeout}s: "
                f"{locator[0]}='{locator[1]}'. "
                f"Check element locator or increase timeout."
            ) from timeout_err
    
    def wait_for_element_visible(
        self,
        locator: Tuple[By, str],
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        Wait for element to be visible (present in DOM and displayed).
        
        Replaces Java pattern with Thread.sleep:
            Thread.sleep(3000);  // Wait for page load
            WebElement element = driver.findElement(By.id("field"));
        
        With condition-based wait:
            element = wait_helper.wait_for_element_visible((By.ID, "field"))
        
        Use this when:
        - Element must be visible to user (not just in DOM)
        - Waiting for animations or transitions to complete
        - Ensuring element is ready for user interaction
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Maximum wait time in seconds (optional)
        
        Returns:
            WebElement: Visible element ready for interaction
        
        Raises:
            TimeoutException: If element not visible within timeout
        
        Example:
            >>> # Replace Thread.sleep(7000) from Java code
            >>> modal = wait_helper.wait_for_element_visible((By.CLASS_NAME, "modal"))
            >>> assert modal.is_displayed()
        """
        if not isinstance(locator, tuple) or len(locator) != 2:
            raise ValueError(
                f"Locator must be tuple of (By, str), got: {locator}"
            )
        
        effective_timeout = timeout if timeout is not None else self.default_timeout
        logger.debug(
            "Waiting for element visibility: %s='%s' (timeout: %ss)",
            locator[0], locator[1], effective_timeout
        )
        
        try:
            wait = WebDriverWait(self.driver, effective_timeout)
            element = wait.until(
                EC.visibility_of_element_located(locator),
                message=f"Element not visible after {effective_timeout}s: {locator}"
            )
            logger.debug("Element visible: %s='%s'", locator[0], locator[1])
            return element
            
        except TimeoutException as timeout_err:
            logger.error(
                "Timeout waiting for element visibility: %s='%s' (timeout: %ss)",
                locator[0], locator[1], effective_timeout
            )
            raise TimeoutException(
                f"Element not visible after {effective_timeout}s: "
                f"{locator[0]}='{locator[1]}'. "
                f"Element may be hidden, covered, or have display:none."
            ) from timeout_err
    
    def wait_for_element_clickable(
        self,
        locator: Tuple[By, str],
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        Wait for element to be clickable (visible and enabled).
        
        Replaces Java pattern with hardcoded sleep:
            Thread.sleep(2000);  // Wait for button to be enabled
            WebElement button = driver.findElement(By.name("submit"));
            button.click();
        
        With proper wait condition:
            button = wait_helper.wait_for_element_clickable((By.NAME, "submit"))
            button.click()
        
        Use this when:
        - About to click an element
        - Waiting for button/link to become enabled
        - Ensuring element is interactive before action
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Maximum wait time in seconds (optional)
        
        Returns:
            WebElement: Clickable element ready for click action
        
        Raises:
            TimeoutException: If element not clickable within timeout
        
        Example:
            >>> # Replace Thread.sleep(3000) before click
            >>> login_btn = wait_helper.wait_for_element_clickable(
            ...     (By.XPATH, "//button[.='Log in']")
            ... )
            >>> login_btn.click()
        """
        if not isinstance(locator, tuple) or len(locator) != 2:
            raise ValueError(
                f"Locator must be tuple of (By, str), got: {locator}"
            )
        
        effective_timeout = timeout if timeout is not None else self.default_timeout
        logger.debug(
            "Waiting for element to be clickable: %s='%s' (timeout: %ss)",
            locator[0], locator[1], effective_timeout
        )
        
        try:
            wait = WebDriverWait(self.driver, effective_timeout)
            element = wait.until(
                EC.element_to_be_clickable(locator),
                message=f"Element not clickable after {effective_timeout}s: {locator}"
            )
            logger.debug("Element clickable: %s='%s'", locator[0], locator[1])
            return element
            
        except TimeoutException as timeout_err:
            logger.error(
                "Timeout waiting for element to be clickable: %s='%s' (timeout: %ss)",
                locator[0], locator[1], effective_timeout
            )
            raise TimeoutException(
                f"Element not clickable after {effective_timeout}s: "
                f"{locator[0]}='{locator[1]}'. "
                f"Element may be disabled, covered, or not visible."
            ) from timeout_err
    
    def wait_for_text_in_element(
        self,
        locator: Tuple[By, str],
        text: str,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for specific text to appear in an element.
        
        Replaces Java pattern with polling:
            for (int i = 0; i < 10; i++) {
                if (element.getText().contains("Success")) break;
                Thread.sleep(1000);
            }
        
        With proper wait condition:
            wait_helper.wait_for_text_in_element((By.ID, "status"), "Success")
        
        Use this when:
        - Waiting for dynamic text to load (AJAX responses)
        - Validating success/error messages appear
        - Confirming page state through text content
        
        Args:
            locator: Tuple of (By strategy, locator string)
            text: Expected text to appear in element (case-sensitive substring match)
            timeout: Maximum wait time in seconds (optional)
        
        Returns:
            bool: True if text appears within timeout
        
        Raises:
            TimeoutException: If text doesn't appear within timeout
        
        Example:
            >>> # Wait for success message after form submission
            >>> wait_helper.wait_for_text_in_element(
            ...     (By.ID, "message"),
            ...     "Registration successful"
            ... )
        """
        if not isinstance(locator, tuple) or len(locator) != 2:
            raise ValueError(
                f"Locator must be tuple of (By, str), got: {locator}"
            )
        
        effective_timeout = timeout if timeout is not None else self.default_timeout
        logger.debug(
            "Waiting for text '%s' in element: %s='%s' (timeout: %ss)",
            text, locator[0], locator[1], effective_timeout
        )
        
        try:
            wait = WebDriverWait(self.driver, effective_timeout)
            result = wait.until(
                EC.text_to_be_present_in_element(locator, text),
                message=(
                    f"Text '{text}' not present in element after {effective_timeout}s: "
                    f"{locator}"
                )
            )
            logger.debug(
                "Text '%s' found in element: %s='%s'",
                text, locator[0], locator[1]
            )
            return result
            
        except TimeoutException as timeout_err:
            logger.error(
                "Timeout waiting for text '%s' in element: %s='%s' (timeout: %ss)",
                text, locator[0], locator[1], effective_timeout
            )
            # Try to get actual text for debugging
            try:
                element = self.driver.find_element(*locator)
                actual_text = element.text
                logger.error("Actual element text: '%s'", actual_text)
            except Exception:
                actual_text = "[unable to retrieve]"
            
            raise TimeoutException(
                f"Text '{text}' not found in element after {effective_timeout}s: "
                f"{locator[0]}='{locator[1]}'. Actual text: '{actual_text}'"
            ) from timeout_err
    
    def wait_for_element_staleness(
        self,
        element: WebElement,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to become stale (removed from DOM or DOM updated).
        
        Replaces Java pattern with polling:
            WebElement oldElement = driver.findElement(By.id("item"));
            button.click();  // Triggers DOM update
            Thread.sleep(2000);  // Hope element is replaced
            WebElement newElement = driver.findElement(By.id("item"));
        
        With staleness check:
            old_element = driver.find_element(By.ID, "item")
            button.click()
            wait_helper.wait_for_element_staleness(old_element)
            new_element = wait_helper.wait_for_element_presence((By.ID, "item"))
        
        Use this when:
        - Waiting for DOM updates after AJAX operations
        - Confirming page reload or partial refresh
        - Avoiding StaleElementReferenceException
        
        Args:
            element: WebElement instance to check for staleness
            timeout: Maximum wait time in seconds (optional)
        
        Returns:
            bool: True if element becomes stale within timeout
        
        Raises:
            TimeoutException: If element doesn't become stale within timeout
        
        Example:
            >>> # Wait for table row to be removed after delete action
            >>> row = driver.find_element(By.ID, "row-123")
            >>> delete_button.click()
            >>> wait_helper.wait_for_element_staleness(row)
        """
        if element is None:
            raise ValueError("WebElement cannot be None")
        
        effective_timeout = timeout if timeout is not None else self.default_timeout
        logger.debug(
            "Waiting for element staleness: %s (timeout: %ss)",
            element, effective_timeout
        )
        
        try:
            wait = WebDriverWait(self.driver, effective_timeout)
            result = wait.until(
                EC.staleness_of(element),
                message=f"Element not stale after {effective_timeout}s: {element}"
            )
            logger.debug("Element became stale: %s", element)
            return result
            
        except TimeoutException as timeout_err:
            logger.error(
                "Timeout waiting for element staleness: %s (timeout: %ss)",
                element, effective_timeout
            )
            raise TimeoutException(
                f"Element did not become stale after {effective_timeout}s. "
                f"DOM may not have updated as expected."
            ) from timeout_err
    
    def wait_for_url_contains(
        self,
        url_fragment: str,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for current URL to contain specified fragment.
        
        Replaces Java pattern with sleep:
            loginButton.click();
            Thread.sleep(5000);  // Wait for redirect
            String currentUrl = driver.getCurrentUrl();
            Assert.assertTrue(currentUrl.contains("/dashboard"));
        
        With proper wait:
            login_button.click()
            wait_helper.wait_for_url_contains("/dashboard")
            assert "/dashboard" in driver.current_url
        
        Use this when:
        - Waiting for navigation after action (login, form submit)
        - Confirming redirect to expected page
        - Validating routing in single-page applications
        
        Args:
            url_fragment: Expected substring in URL (e.g., "/dashboard", "success")
            timeout: Maximum wait time in seconds (optional)
        
        Returns:
            bool: True if URL contains fragment within timeout
        
        Raises:
            TimeoutException: If URL doesn't contain fragment within timeout
        
        Example:
            >>> # Wait for login redirect
            >>> login_button.click()
            >>> wait_helper.wait_for_url_contains("/home")
            >>> print(f"Navigated to: {driver.current_url}")
        """
        effective_timeout = timeout if timeout is not None else self.default_timeout
        logger.debug(
            "Waiting for URL to contain: '%s' (timeout: %ss)",
            url_fragment, effective_timeout
        )
        
        try:
            wait = WebDriverWait(self.driver, effective_timeout)
            result = wait.until(
                EC.url_contains(url_fragment),
                message=(
                    f"URL does not contain '{url_fragment}' after {effective_timeout}s"
                )
            )
            current_url = self.driver.current_url
            logger.debug("URL contains '%s': %s", url_fragment, current_url)
            return result
            
        except TimeoutException as timeout_err:
            current_url = self.driver.current_url
            logger.error(
                "Timeout waiting for URL to contain '%s' (timeout: %ss). "
                "Current URL: %s",
                url_fragment, effective_timeout, current_url
            )
            raise TimeoutException(
                f"URL does not contain '{url_fragment}' after {effective_timeout}s. "
                f"Current URL: {current_url}"
            ) from timeout_err
    
    def wait_for_url_to_be(
        self,
        url: str,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for current URL to exactly match expected URL.
        
        Use this when:
        - Expecting exact URL match after navigation
        - Validating complete URL including parameters
        - Stricter validation than url_contains
        
        Args:
            url: Complete expected URL
            timeout: Maximum wait time in seconds (optional)
        
        Returns:
            bool: True if URL matches exactly within timeout
        
        Raises:
            TimeoutException: If URL doesn't match within timeout
        
        Example:
            >>> # Wait for exact URL after redirect
            >>> logout_link.click()
            >>> wait_helper.wait_for_url_to_be("https://app.example.com/login")
        """
        effective_timeout = timeout if timeout is not None else self.default_timeout
        logger.debug(
            "Waiting for URL to be: '%s' (timeout: %ss)",
            url, effective_timeout
        )
        
        try:
            wait = WebDriverWait(self.driver, effective_timeout)
            result = wait.until(
                EC.url_to_be(url),
                message=f"URL is not '{url}' after {effective_timeout}s"
            )
            logger.debug("URL matches expected: %s", url)
            return result
            
        except TimeoutException as timeout_err:
            current_url = self.driver.current_url
            logger.error(
                "Timeout waiting for URL to be '%s' (timeout: %ss). "
                "Current URL: %s",
                url, effective_timeout, current_url
            )
            raise TimeoutException(
                f"URL is not '{url}' after {effective_timeout}s. "
                f"Current URL: {current_url}"
            ) from timeout_err
    
    def wait_for_title_contains(
        self,
        title_fragment: str,
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for page title to contain specified text.
        
        Replaces Java pattern:
            Thread.sleep(3000);
            String title = driver.getTitle();
            Assert.assertTrue(title.contains("Dashboard"));
        
        With condition-based wait:
            wait_helper.wait_for_title_contains("Dashboard")
        
        Use this when:
        - Waiting for page load completion
        - Validating correct page after navigation
        - Checking for dynamic title updates
        
        Args:
            title_fragment: Expected substring in page title
            timeout: Maximum wait time in seconds (optional)
        
        Returns:
            bool: True if title contains fragment within timeout
        
        Raises:
            TimeoutException: If title doesn't contain fragment within timeout
        
        Example:
            >>> # Validate page title after navigation
            >>> dashboard_link.click()
            >>> wait_helper.wait_for_title_contains("User Dashboard")
            >>> assert "Dashboard" in driver.title
        """
        effective_timeout = timeout if timeout is not None else self.default_timeout
        logger.debug(
            "Waiting for title to contain: '%s' (timeout: %ss)",
            title_fragment, effective_timeout
        )
        
        try:
            wait = WebDriverWait(self.driver, effective_timeout)
            result = wait.until(
                EC.title_contains(title_fragment),
                message=(
                    f"Title does not contain '{title_fragment}' after {effective_timeout}s"
                )
            )
            current_title = self.driver.title
            logger.debug("Title contains '%s': %s", title_fragment, current_title)
            return result
            
        except TimeoutException as timeout_err:
            current_title = self.driver.title
            logger.error(
                "Timeout waiting for title to contain '%s' (timeout: %ss). "
                "Current title: '%s'",
                title_fragment, effective_timeout, current_title
            )
            raise TimeoutException(
                f"Title does not contain '{title_fragment}' after {effective_timeout}s. "
                f"Current title: '{current_title}'"
            ) from timeout_err
    
    def __repr__(self) -> str:
        """
        String representation of WaitHelpers instance.
        
        Returns:
            String showing timeout configuration
        """
        return (
            f"WaitHelpers(default={self.default_timeout}s, "
            f"long={self.long_timeout}s, short={self.short_timeout}s)"
        )


# Module-level convenience functions for quick access
def create_wait_helper(driver: WebDriver) -> WaitHelpers:
    """
    Convenience function to create WaitHelpers instance.
    
    Args:
        driver: Selenium WebDriver instance
    
    Returns:
        WaitHelpers: Configured wait helper instance
    
    Example:
        >>> from utilities.wait_helpers import create_wait_helper
        >>> wait = create_wait_helper(driver)
        >>> wait.wait_for_element_clickable((By.ID, "submit"))
    """
    return WaitHelpers(driver)


# Example usage and validation (for documentation purposes)
if __name__ == "__main__":
    """
    Module self-test demonstrating wait helper functionality.
    Run this module directly to validate wait helper setup.
    """
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("WaitHelpers Module - Self Test")
    print("=" * 50)
    
    # Note: Actual WebDriver required for functional testing
    # This self-test validates initialization and configuration only
    
    try:
        from unittest.mock import Mock
        
        # Create mock driver for initialization test
        mock_driver = Mock(spec=WebDriver)
        mock_driver.current_url = "http://example.com"
        mock_driver.title = "Example Page"
        
        # Test initialization
        wait_helper = WaitHelpers(mock_driver)
        print(f"✓ WaitHelpers initialized: {wait_helper}")
        
        # Validate timeout configuration
        assert wait_helper.default_timeout > 0, "default_timeout must be positive"
        assert wait_helper.long_timeout > 0, "long_timeout must be positive"
        assert wait_helper.short_timeout > 0, "short_timeout must be positive"
        print(f"✓ Timeout configuration valid")
        
        # Validate timeout relationships
        assert wait_helper.short_timeout <= wait_helper.default_timeout, \
            "short_timeout should be <= default_timeout"
        assert wait_helper.default_timeout <= wait_helper.long_timeout, \
            "default_timeout should be <= long_timeout"
        print(f"✓ Timeout relationships correct")
        
        print("\n✓ All wait helper self-tests passed!")
        print(f"\nConfigured Timeouts:")
        print(f"  - Short: {wait_helper.short_timeout}s")
        print(f"  - Default: {wait_helper.default_timeout}s")
        print(f"  - Long: {wait_helper.long_timeout}s")
        
    except ImportError as err:
        print(f"✗ Import error (unittest.mock required for self-test): {err}")
        
    except Exception as exc:
        print(f"✗ Unexpected error: {exc}")
        logger.exception("WaitHelpers self-test failed")
