"""
Driver Manager Module

Thread-safe WebDriver lifecycle management for parallel test execution.

This module replaces Java's Driver.java with Python implementation:
- Threading.local() replaces InheritableThreadLocal for thread safety
- webdriver-manager handles automatic driver binary provisioning
- Explicit waits ONLY (eliminates 10-second implicit wait anti-pattern)
- Configuration-driven browser selection (Chrome, Firefox)
- Lazy initialization with proper cleanup

CRITICAL BUG FIX:
    Original Java Driver.java line 37 incorrectly called:
        WebDriverManager.chromedriver().setup()
    for Firefox browser, causing Firefox tests to fail.

    This Python implementation correctly uses:
        GeckoDriverManager().install()
    for Firefox, ensuring proper GeckoDriver binary provisioning.

ARCHITECTURAL CHANGES FROM JAVA VERSION:
    1. NO implicit waits (Java had 10s on lines 34, 40) - explicit waits only
    2. threading.local() provides thread-level isolation (not child inheritance)
    3. webdriver-manager caches binaries in ~/.wdm/drivers/
    4. Comprehensive logging replaces System.out.println
    5. Proper exception handling replaces silent failures
    6. Selenium 4.x syntax (headless=new, ChromeService, FirefoxService)

Example Usage:
    >>> from utilities.driver_manager import DriverManager
    >>> # Get WebDriver instance for current thread
    >>> driver = DriverManager.get_driver()
    >>> driver.get("https://example.com")
    >>> # Cleanup after test
    >>> DriverManager.quit_driver()
"""

import threading
import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utilities.config_reader import ConfigReader


# Configure module logger
logger = logging.getLogger(__name__)


class DriverInitializationError(Exception):
    """
    Custom exception for WebDriver initialization failures.

    Raised when:
    - Unsupported browser type specified in configuration
    - WebDriver binary download fails
    - Browser process fails to start
    - Driver service initialization fails
    - Configuration missing or invalid

    This provides explicit error handling replacing Java's silent failures
    and generic exceptions.

    Example:
        >>> try:
        ...     driver = DriverManager.get_driver()
        ... except DriverInitializationError as e:
        ...     logger.error(f"Failed to initialize driver: {e}")
        ...     raise
    """


class DriverManager:
    """
    Thread-safe WebDriver lifecycle manager using threading.local().

    Provides centralized WebDriver instantiation, configuration, and cleanup
    with strict thread isolation for parallel test execution. Replaces Java's
    InheritableThreadLocal pattern with Python threading.local().

    Thread Safety:
        - Each thread gets its own WebDriver instance via threading.local()
        - No shared state between threads (prevents race conditions)
        - Compatible with behave-parallel (process-based parallelism)
        - Compatible with pytest-xdist (thread/process parallelism)

    Supported Browsers:
        - Chrome (default): ChromeDriverManager with Selenium 4.x
        - Firefox: GeckoDriverManager with Selenium 4.x (BUG FIXED)

    Configuration:
        Reads from config/config.yaml via ConfigReader:
        - browser.type: 'chrome' or 'firefox' (default: 'chrome')
        - browser.headless: true/false (default: false)
        - browser.window_size: [width, height] (optional)

    Critical Changes from Java Version:
        1. NO implicit waits (Java had 10s implicit wait causing issues)
        2. Correct Firefox driver setup (fixes line 37 bug)
        3. Comprehensive error handling and logging
        4. Selenium 4.x service pattern
        5. Modern headless syntax (--headless=new)

    Example:
        >>> # Get driver for current thread
        >>> driver = DriverManager.get_driver()
        >>> driver.get("https://example.com")
        >>>
        >>> # Each thread gets its own driver
        >>> # Thread 1: driver_1 = DriverManager.get_driver()
        >>> # Thread 2: driver_2 = DriverManager.get_driver()
        >>> # driver_1 != driver_2 (different instances)
        >>>
        >>> # Cleanup
        >>> DriverManager.quit_driver()
    """

    # Thread-local storage for WebDriver instances
    # Replaces Java's InheritableThreadLocal<WebDriver> driverPool
    _thread_local = threading.local()

    @classmethod
    def get_driver(cls) -> WebDriver:
        """
        Get WebDriver instance for current thread with lazy initialization.

        Returns same driver instance for repeated calls within same thread.
        Creates new driver on first call per thread using _create_driver().

        This replaces Java's getDriver() method with equivalent functionality:
        - Lazy initialization (create only when needed)
        - Thread-local storage (one driver per thread)
        - Configuration-driven browser selection

        Thread Safety:
            Each thread calling this method gets its own WebDriver instance
            stored in threading.local(). No synchronization needed since
            threading.local() provides thread-isolated storage.

        Returns:
            WebDriver: Thread-local WebDriver instance (Chrome or Firefox)

        Raises:
            DriverInitializationError: If driver creation fails
            ValueError: If unsupported browser type configured
            ConfigurationError: If required configuration missing

        Example:
            >>> driver = DriverManager.get_driver()
            >>> driver.get("https://example.com")
            >>> # Subsequent calls return same instance
            >>> same_driver = DriverManager.get_driver()
            >>> assert driver is same_driver
        """
        # Check if current thread already has a driver instance
        # hasattr() safely checks if attribute exists without raising AttributeError
        if not hasattr(cls._thread_local, 'driver') or cls._thread_local.driver is None:
            thread_name = threading.current_thread().name
            logger.info(
                "No WebDriver found for thread '%s', initializing new instance",
                thread_name
            )

            try:
                # Create new driver for this thread
                cls._thread_local.driver = cls._create_driver()
                logger.info(
                    "Successfully initialized WebDriver for thread '%s'",
                    thread_name
                )
            except Exception as e:
                logger.exception(
                    "Failed to initialize WebDriver for thread '%s': %s",
                    thread_name,
                    e
                )
                raise DriverInitializationError(
                    f"WebDriver initialization failed for thread '{thread_name}': {e}"
                ) from e
        else:
            thread_name = threading.current_thread().name
            logger.debug(
                "Returning existing WebDriver instance for thread '%s'",
                thread_name
            )

        return cls._thread_local.driver

    @classmethod
    def _create_driver(cls) -> WebDriver:
        """
        Create and configure new WebDriver instance based on configuration.

        Reads browser type from ConfigReader and instantiates appropriate
        WebDriver with Selenium 4.x service pattern and webdriver-manager
        for automatic driver binary provisioning.

        CRITICAL BUG FIX FROM JAVA VERSION:
            Original Java Driver.java line 37 had:
                case "firefox":
                    WebDriverManager.chromedriver().setup();  // BUG!
                    driverPool.set(new FirefoxDriver());

            This Python version correctly uses:
                elif browser_type == "firefox":
                    firefox_service = FirefoxService(GeckoDriverManager().install())
                    driver = webdriver.Firefox(service=firefox_service, options=firefox_options)

        CRITICAL CHANGE - NO IMPLICIT WAITS:
            Java version had driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
            on lines 34 and 40, creating anti-pattern of mixing implicit and explicit waits.

            This Python version uses NO implicit waits. All waits are explicit via
            utilities/wait_helpers.py. This provides predictable, controllable wait behavior.

        Configuration:
            - browser.type: 'chrome' or 'firefox' (default: 'chrome')
            - browser.headless: true/false (default: false)
            - browser.window_size: [width, height] (optional)

        Returns:
            WebDriver: Configured Chrome or Firefox WebDriver instance

        Raises:
            ValueError: If unsupported browser type specified
            DriverInitializationError: If driver creation or configuration fails
            ConfigurationError: If configuration retrieval fails

        Implementation Details:
            Chrome:
                - Uses ChromeDriverManager for binary provisioning
                - Configures --headless=new (Selenium 4.x syntax)
                - Adds --disable-gpu, --no-sandbox for CI/CD stability
                - Uses ChromeService with webdriver-manager path

            Firefox:
                - Uses GeckoDriverManager for binary provisioning (BUG FIX)
                - Configures --headless if enabled
                - Uses FirefoxService with webdriver-manager path
        """
        try:
            # Load configuration
            config = ConfigReader()
            browser_type = config.get_property('browser.type', default='chrome')
            headless = config.get_property('browser.headless', default=False)

            logger.info(
                "Creating WebDriver: browser_type='%s', headless=%s",
                browser_type,
                headless
            )

            driver: Optional[WebDriver] = None

            if browser_type.lower() == 'chrome':
                # Configure Chrome options
                chrome_options = ChromeOptions()

                if headless:
                    # Selenium 4.x new headless syntax
                    chrome_options.add_argument('--headless=new')
                    logger.debug("Chrome headless mode enabled")

                # Add stability options for CI/CD environments
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-extensions')
                logger.debug("Chrome stability options configured")

                # Use webdriver-manager to handle ChromeDriver binary
                # Caches drivers in ~/.wdm/drivers/
                logger.debug("Provisioning ChromeDriver binary via webdriver-manager")
                chrome_service = ChromeService(ChromeDriverManager().install())

                # Create Chrome driver
                driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
                logger.info("Chrome WebDriver created successfully")

            elif browser_type.lower() == 'firefox':
                # *** CRITICAL BUG FIX ***
                # Original Java code on line 37 incorrectly called:
                #     WebDriverManager.chromedriver().setup()
                # This Python version correctly uses GeckoDriverManager for Firefox

                # Configure Firefox options
                firefox_options = FirefoxOptions()

                if headless:
                    firefox_options.add_argument('--headless')
                    logger.debug("Firefox headless mode enabled")

                # Use webdriver-manager to handle GeckoDriver binary (BUG FIX)
                # This replaces the incorrect chromedriver().setup() from Java
                logger.debug("Provisioning GeckoDriver binary via webdriver-manager")
                firefox_service = FirefoxService(GeckoDriverManager().install())

                # Create Firefox driver
                driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
                logger.info("Firefox WebDriver created successfully (bug fixed)")

            else:
                # Unsupported browser type
                error_msg = (
                    f"Unsupported browser type: '{browser_type}'. "
                    f"Supported browsers: 'chrome', 'firefox'. "
                    f"Check configuration: browser.type in config/config.yaml "
                    f"or BROWSER_TYPE environment variable."
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

            # Configure WebDriver (applies to both Chrome and Firefox)
            if driver is not None:
                # Maximize window for consistent test execution
                # Preserves behavior from Java version (lines 33, 39)
                driver.maximize_window()
                logger.debug("Browser window maximized")

                # *** CRITICAL CHANGE: NO IMPLICIT WAIT ***
                # Java version had:
                #     driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
                # on lines 34 and 40.
                #
                # This Python version does NOT set implicit waits.
                # Mixing implicit and explicit waits causes unpredictable behavior:
                # - Compound timeouts (implicit + explicit)
                # - Inconsistent element lookup timing
                # - Difficult to debug failures
                #
                # Use explicit waits ONLY via utilities/wait_helpers.py:
                #     from utilities.wait_helpers import WaitHelpers
                #     waiter = WaitHelpers(driver)
                #     element = waiter.wait_for_element(locator, timeout=10)

                logger.debug(
                    "NO implicit wait configured (explicit waits only). "
                    "This fixes anti-pattern from Java version."
                )

                # Log driver capabilities for debugging
                logger.info(
                    "WebDriver configured: browser=%s, version=%s, session=%s",
                    driver.capabilities.get('browserName', 'unknown'),
                    driver.capabilities.get('browserVersion', 'unknown'),
                    driver.session_id
                )

                return driver
            else:
                # Should never reach here due to ValueError above, but defensive check
                raise DriverInitializationError("Driver creation returned None")

        except ValueError as ve:
            # Re-raise ValueError for unsupported browser types
            logger.error("Configuration error: %s", ve)
            raise

        except WebDriverException as wde:
            # Selenium WebDriver-specific exceptions
            error_msg = f"WebDriver initialization failed: {wde}"
            logger.exception(error_msg)
            raise DriverInitializationError(error_msg) from wde

        except Exception as exc:
            # Catch-all for unexpected errors
            error_msg = f"Unexpected error during driver creation: {exc}"
            logger.exception(error_msg)
            raise DriverInitializationError(error_msg) from exc

    @classmethod
    def quit_driver(cls) -> None:
        """
        Quit WebDriver and remove thread-local reference.

        Properly terminates WebDriver session and browser process, then
        removes driver reference from thread-local storage. This ensures
        clean shutdown and prevents stale driver references.

        Replaces Java's closeDriver() method with equivalent functionality:
        - Null/None check before quit
        - Proper exception handling
        - Thread-local reference removal

        Thread Safety:
            Only affects current thread's driver instance. Other threads'
            drivers remain unaffected. Safe to call from any thread.

        Idempotent:
            Safe to call multiple times. If no driver exists for current
            thread, method completes silently without error.

        Exception Handling:
            Swallows quit() exceptions to ensure thread-local cleanup always
            happens. Logs errors for debugging but doesn't raise to prevent
            test teardown failures.

        Example:
            >>> driver = DriverManager.get_driver()
            >>> driver.get("https://example.com")
            >>> # After test completion
            >>> DriverManager.quit_driver()
            >>> # Safe to call again
            >>> DriverManager.quit_driver()  # No error
        """
        thread_name = threading.current_thread().name

        # Check if current thread has a driver instance
        if hasattr(cls._thread_local, 'driver') and cls._thread_local.driver is not None:
            logger.info("Quitting WebDriver for thread '%s'", thread_name)

            try:
                # Attempt to quit driver gracefully
                cls._thread_local.driver.quit()
                logger.info(
                    "WebDriver quit successfully for thread '%s'",
                    thread_name
                )

            except WebDriverException as wde:
                # Log WebDriver-specific errors but don't raise
                # Ensures cleanup always completes
                logger.warning(
                    "WebDriverException during quit for thread '%s': %s",
                    thread_name,
                    wde
                )

            except Exception as exc:
                # Log unexpected errors but don't raise
                logger.error(
                    "Unexpected error during driver quit for thread '%s': %s",
                    thread_name,
                    exc,
                    exc_info=True
                )

            finally:
                # Always remove thread-local reference
                # Prevents stale driver reference on next get_driver() call
                # Equivalent to Java's driverPool.remove()
                cls._thread_local.driver = None
                logger.debug(
                    "Thread-local driver reference cleared for thread '%s'",
                    thread_name
                )

        else:
            # No driver exists for current thread
            logger.debug(
                "No WebDriver to quit for thread '%s' (already None or never created)",
                thread_name
            )

    @classmethod
    def get_thread_driver_status(cls) -> dict:
        """
        Get diagnostic information about current thread's driver status.

        Utility method for debugging and monitoring driver lifecycle.
        Not present in Java version - added for enhanced observability.

        Returns:
            dict: Status information containing:
                - thread_name: Current thread name
                - thread_id: Current thread identifier
                - has_driver: Whether driver exists in thread-local storage
                - driver_session: Session ID if driver exists, else None
                - driver_capabilities: Browser capabilities if driver exists, else None

        Example:
            >>> status = DriverManager.get_thread_driver_status()
            >>> print(status)
            {
                'thread_name': 'MainThread',
                'thread_id': 140234567890,
                'has_driver': True,
                'driver_session': '123abc456def',
                'driver_capabilities': {'browserName': 'chrome', ...}
            }
        """
        thread = threading.current_thread()
        has_driver = hasattr(cls._thread_local, 'driver') and cls._thread_local.driver is not None

        status = {
            'thread_name': thread.name,
            'thread_id': thread.ident,
            'has_driver': has_driver,
            'driver_session': None,
            'driver_capabilities': None
        }

        if has_driver:
            try:
                status['driver_session'] = cls._thread_local.driver.session_id
                status['driver_capabilities'] = cls._thread_local.driver.capabilities
            except Exception as exc:
                logger.debug("Could not retrieve driver details: %s", exc)

        return status


# Module-level convenience functions for backward compatibility
def get_driver() -> WebDriver:
    """
    Module-level convenience function to get WebDriver instance.

    Provides simpler import pattern for common use case:
        from utilities.driver_manager import get_driver
        driver = get_driver()

    Instead of:
        from utilities.driver_manager import DriverManager
        driver = DriverManager.get_driver()

    Returns:
        WebDriver: Thread-local WebDriver instance

    Raises:
        DriverInitializationError: If driver creation fails
    """
    return DriverManager.get_driver()


def quit_driver() -> None:
    """
    Module-level convenience function to quit WebDriver.

    Provides simpler import pattern for common use case:
        from utilities.driver_manager import quit_driver
        quit_driver()

    Instead of:
        from utilities.driver_manager import DriverManager
        DriverManager.quit_driver()
    """
    DriverManager.quit_driver()


# Example usage and validation (for documentation purposes)
if __name__ == "__main__":
    """
    Module self-test demonstrating driver manager functionality.
    Run this module directly to validate driver setup.
    """
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    try:
        print("=== Driver Manager Self-Test ===\n")

        # Test driver initialization
        print("1. Testing driver initialization...")
        driver = DriverManager.get_driver()
        print(f"   ✓ Driver initialized: {driver.capabilities.get('browserName')}")

        # Test driver reuse (should return same instance)
        print("\n2. Testing driver reuse...")
        driver2 = DriverManager.get_driver()
        assert driver is driver2, "Driver reuse failed!"
        print("   ✓ Driver reuse verified (same instance returned)")

        # Test driver status
        print("\n3. Testing driver status...")
        status = DriverManager.get_thread_driver_status()
        print(f"   ✓ Thread: {status['thread_name']}")
        print(f"   ✓ Has Driver: {status['has_driver']}")
        print(f"   ✓ Session ID: {status['driver_session']}")

        # Test navigation
        print("\n4. Testing browser navigation...")
        driver.get("https://www.example.com")
        print(f"   ✓ Navigated to: {driver.current_url}")
        print(f"   ✓ Page title: {driver.title}")

        # Test cleanup
        print("\n5. Testing driver cleanup...")
        DriverManager.quit_driver()
        print("   ✓ Driver quit successfully")

        # Test cleanup idempotence
        print("\n6. Testing cleanup idempotence...")
        DriverManager.quit_driver()  # Should not raise error
        print("   ✓ Cleanup is idempotent (no error on second call)")

        print("\n✓ All driver manager tests passed!")

    except DriverInitializationError as err:
        print(f"\n✗ Driver initialization error: {err}")
        print("  Check browser/driver installation and configuration")

    except Exception as exc:
        print(f"\n✗ Unexpected error: {exc}")
        logger.exception("Driver manager self-test failed")

    finally:
        # Ensure cleanup even if tests fail
        try:
            DriverManager.quit_driver()
        except Exception:
            pass
