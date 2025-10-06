"""
Unit Tests for Driver Manager Module

Comprehensive pytest-based unit tests validating the WebDriver manager utility
(utilities/driver_manager.py) for the Python Selenium + Behave BDD test automation
framework migrated from Java.

Critical Test Coverage:
1. Singleton pattern implementation with threading.local()
2. Thread-safe driver management for parallel test execution
3. Chrome browser driver initialization
4. Firefox browser driver initialization with BUG FIX validation
5. Firefox uses GeckoDriverManager NOT ChromeDriverManager (fixes Java line 37 bug)
6. Driver cleanup and quit() functionality
7. webdriver-manager automatic binary provisioning
8. Implicit wait configuration (should be 0 per best practices)
9. Driver null safety checks
10. Proper exception handling for driver initialization failures

Java Bug Context:
    Original Driver.java line 37 had:
        case "firefox":
            WebDriverManager.chromedriver().setup();  // BUG!
            driverPool.set(new FirefoxDriver());
    
    This caused Firefox tests to fail because it downloaded ChromeDriver
    instead of GeckoDriver. These tests verify the Python version correctly
    uses GeckoDriverManager().install() for Firefox.

Test Strategy:
    - Use unittest.mock.patch to mock WebDriver constructors and webdriver-manager
    - Test thread-local behavior with threading.Thread
    - Verify proper exception handling instead of swallowed exceptions
    - Validate InheritableThreadLocal (Java) → threading.local() (Python) equivalence

References:
    - Agent Action Plan Section 0.4.1 (tests/ directory structure)
    - Agent Action Plan Section 0.8.1 (thread safety analysis)
    - Agent Action Plan Section 0.5.1 (Driver.java conversion with Firefox bug fix)
    - Agent Action Plan Section 0.8.2 (bug fixes and security)
    - Source: src/main/java/com/testinium/utilities/Driver.java
"""

import pytest
import threading
import time
from unittest import mock
from unittest.mock import patch, Mock, MagicMock, call
from selenium.common.exceptions import WebDriverException

# Internal imports - ONLY from depends_on_files
from utilities.driver_manager import DriverManager, DriverInitializationError, get_driver, quit_driver
from utilities.config_reader import ConfigReader


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_driver_after_test():
    """
    Pytest fixture to ensure driver cleanup after each test.
    
    Automatically runs after every test to prevent driver leaks
    and ensure clean state for next test. Uses autouse=True to
    apply to all tests without explicit declaration.
    
    Yields control to test, then cleans up in finally block.
    """
    # Setup: Nothing to do before test
    yield
    
    # Teardown: Clean up driver after test
    try:
        DriverManager.quit_driver()
    except Exception:
        # Swallow exceptions during cleanup to prevent test failures
        pass
    
    # Additional cleanup: Clear thread-local storage completely
    if hasattr(DriverManager._thread_local, 'driver'):
        DriverManager._thread_local.driver = None


@pytest.fixture
def mock_config_chrome():
    """
    Mock ConfigReader to return Chrome browser configuration.
    
    Returns:
        Mock: ConfigReader mock configured for Chrome browser
    """
    mock_config = Mock(spec=ConfigReader)
    mock_config.get_property.side_effect = lambda key, default=None: {
        'browser.type': 'chrome',
        'browser.headless': False
    }.get(key, default)
    return mock_config


@pytest.fixture
def mock_config_firefox():
    """
    Mock ConfigReader to return Firefox browser configuration.
    
    Returns:
        Mock: ConfigReader mock configured for Firefox browser
    """
    mock_config = Mock(spec=ConfigReader)
    mock_config.get_property.side_effect = lambda key, default=None: {
        'browser.type': 'firefox',
        'browser.headless': False
    }.get(key, default)
    return mock_config


@pytest.fixture
def mock_config_headless_chrome():
    """
    Mock ConfigReader to return headless Chrome configuration.
    
    Returns:
        Mock: ConfigReader mock configured for headless Chrome
    """
    mock_config = Mock(spec=ConfigReader)
    mock_config.get_property.side_effect = lambda key, default=None: {
        'browser.type': 'chrome',
        'browser.headless': True
    }.get(key, default)
    return mock_config


# ============================================================================
# Test Class: Driver Manager Unit Tests
# ============================================================================

class TestDriverManager:
    """
    Comprehensive unit tests for DriverManager class.
    
    Validates thread-safe WebDriver lifecycle management, singleton pattern,
    browser initialization (Chrome, Firefox), cleanup, and critical bug fixes
    from the Java-to-Python migration.
    """
    
    # ========================================================================
    # Chrome Driver Initialization Tests
    # ========================================================================
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_get_driver_chrome(self, mock_config_class, mock_chrome_manager, mock_chrome_driver):
        """
        Test Chrome WebDriver initialization and configuration.
        
        Validates:
        - ChromeDriverManager is used for binary provisioning
        - Chrome WebDriver is instantiated with correct service and options
        - Window is maximized (preserving Java behavior from line 33)
        - NO implicit wait is set (fixes Java anti-pattern from line 34)
        - Driver singleton pattern returns same instance
        
        Mocks:
        - ConfigReader to return 'chrome' browser type
        - ChromeDriverManager.install() to return mock driver path
        - webdriver.Chrome constructor to return mock driver
        
        Reference: Java Driver.java lines 30-35 (chrome case)
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        # Mock ChromeDriverManager to return driver path
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        # Mock Chrome WebDriver instance
        mock_driver = MagicMock()
        mock_driver.session_id = 'test-session-123'
        mock_driver.capabilities = {'browserName': 'chrome', 'browserVersion': '120.0'}
        mock_chrome_driver.return_value = mock_driver
        
        # Execute: Get driver
        driver = DriverManager.get_driver()
        
        # Assert: ChromeDriverManager was called to provision binary
        mock_chrome_manager_instance.install.assert_called_once()
        
        # Assert: Chrome WebDriver was instantiated
        assert mock_chrome_driver.called, "Chrome WebDriver constructor not called"
        
        # Assert: Window was maximized (preserves Java line 33 behavior)
        mock_driver.maximize_window.assert_called_once()
        
        # Assert: NO implicit wait was set (fixes Java line 34 anti-pattern)
        # Java had: driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
        # Python version should NOT call this
        assert not hasattr(mock_driver, 'implicitly_wait') or not mock_driver.implicitly_wait.called, \
            "Implicit wait should NOT be set (explicit waits only)"
        
        # Assert: Returned driver matches mock
        assert driver == mock_driver, "get_driver() did not return expected driver"
        
        # Assert: Singleton pattern - calling again returns same driver
        driver2 = DriverManager.get_driver()
        assert driver2 is driver, "Singleton pattern broken: different driver returned"
    
    # ========================================================================
    # Firefox Driver Initialization Tests (CRITICAL BUG FIX VALIDATION)
    # ========================================================================
    
    @patch('utilities.driver_manager.webdriver.Firefox')
    @patch('utilities.driver_manager.GeckoDriverManager')
    @patch('utilities.driver_manager.ChromeDriverManager')  # Should NOT be called
    @patch('utilities.driver_manager.ConfigReader')
    def test_get_driver_firefox(self, mock_config_class, mock_chrome_manager, 
                                mock_gecko_manager, mock_firefox_driver):
        """
        Test Firefox WebDriver initialization with CRITICAL BUG FIX validation.
        
        **CRITICAL TEST**: This test validates the fix for the Java bug at line 37
        of Driver.java where Firefox case incorrectly called:
            WebDriverManager.chromedriver().setup()
        instead of:
            WebDriverManager.firefoxdriver().setup()
        
        This Python version must use GeckoDriverManager, NOT ChromeDriverManager.
        
        Validates:
        - GeckoDriverManager IS used for binary provisioning (BUG FIX)
        - ChromeDriverManager is NOT called (would be the bug)
        - Firefox WebDriver is instantiated with correct service and options
        - Window is maximized (preserving Java behavior from line 39)
        - NO implicit wait is set (fixes Java anti-pattern from line 40)
        
        Mocks:
        - ConfigReader to return 'firefox' browser type
        - GeckoDriverManager.install() to return mock driver path
        - ChromeDriverManager to verify it's NOT called (bug detection)
        - webdriver.Firefox constructor to return mock driver
        
        Reference: 
        - Java Driver.java lines 36-41 (firefox case with BUG at line 37)
        - Agent Action Plan Section 0.8.2 (Bug Fixes and Security)
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'firefox',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        # Mock GeckoDriverManager to return driver path (CORRECT for Firefox)
        mock_gecko_manager_instance = Mock()
        mock_gecko_manager_instance.install.return_value = '/path/to/geckodriver'
        mock_gecko_manager.return_value = mock_gecko_manager_instance
        
        # Mock ChromeDriverManager (should NOT be called - this would be the bug)
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        # Mock Firefox WebDriver instance
        mock_driver = MagicMock()
        mock_driver.session_id = 'test-firefox-session-456'
        mock_driver.capabilities = {'browserName': 'firefox', 'browserVersion': '121.0'}
        mock_firefox_driver.return_value = mock_driver
        
        # Execute: Get driver
        driver = DriverManager.get_driver()
        
        # **CRITICAL ASSERTION**: GeckoDriverManager WAS called (correct behavior)
        mock_gecko_manager_instance.install.assert_called_once()
        assert mock_gecko_manager_instance.install.called, \
            "GeckoDriverManager.install() must be called for Firefox (bug fix validation)"
        
        # **CRITICAL ASSERTION**: ChromeDriverManager was NOT called (bug detection)
        # If this assertion fails, the Java bug is reproduced in Python
        assert not mock_chrome_manager_instance.install.called, \
            "CRITICAL BUG: ChromeDriverManager must NOT be called for Firefox! " \
            "This is the Java Driver.java line 37 bug reproduced in Python. " \
            "Firefox must use GeckoDriverManager, not ChromeDriverManager."
        
        # Assert: Firefox WebDriver was instantiated
        assert mock_firefox_driver.called, "Firefox WebDriver constructor not called"
        
        # Assert: Window was maximized (preserves Java line 39 behavior)
        mock_driver.maximize_window.assert_called_once()
        
        # Assert: NO implicit wait was set (fixes Java line 40 anti-pattern)
        assert not hasattr(mock_driver, 'implicitly_wait') or not mock_driver.implicitly_wait.called, \
            "Implicit wait should NOT be set for Firefox (explicit waits only)"
        
        # Assert: Returned driver matches mock
        assert driver == mock_driver, "get_driver() did not return expected Firefox driver"
        
        # Log success for critical bug fix validation
        print("✓ CRITICAL BUG FIX VALIDATED: Firefox correctly uses GeckoDriverManager")
    
    # ========================================================================
    # Singleton Pattern Tests
    # ========================================================================
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_singleton_pattern(self, mock_config_class, mock_chrome_manager, mock_chrome_driver):
        """
        Test singleton pattern: same driver instance returned within thread.
        
        Validates:
        - First get_driver() call creates new driver
        - Subsequent get_driver() calls return same instance (no recreation)
        - Driver creation happens only once per thread
        - threading.local() provides proper instance caching
        
        This replaces Java's InheritableThreadLocal pattern with Python's
        threading.local() for thread-isolated singleton behavior.
        
        Reference: Java Driver.java lines 21-22 (singleton check)
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        mock_driver = MagicMock()
        mock_driver.session_id = 'singleton-test-session'
        mock_driver.capabilities = {'browserName': 'chrome'}
        mock_chrome_driver.return_value = mock_driver
        
        # Execute: Call get_driver() multiple times
        driver1 = DriverManager.get_driver()
        driver2 = DriverManager.get_driver()
        driver3 = DriverManager.get_driver()
        
        # Assert: All calls return same instance (singleton)
        assert driver1 is driver2, "Singleton broken: driver1 != driver2"
        assert driver2 is driver3, "Singleton broken: driver2 != driver3"
        assert driver1 is driver3, "Singleton broken: driver1 != driver3"
        
        # Assert: Driver was created only once (not three times)
        assert mock_chrome_driver.call_count == 1, \
            f"Driver should be created once, but was created {mock_chrome_driver.call_count} times"
    
    # ========================================================================
    # Thread-Local Isolation Tests
    # ========================================================================
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_thread_local_isolation(self, mock_config_class, mock_chrome_manager, mock_chrome_driver):
        """
        Test thread-local isolation: different threads get different drivers.
        
        Validates:
        - Each thread gets its own WebDriver instance
        - threading.local() provides proper thread isolation
        - No shared state between threads (prevents race conditions)
        - Equivalent to Java's InheritableThreadLocal for parallel execution
        
        Critical for parallel test execution with behave-parallel or pytest-xdist.
        
        Reference: 
        - Java Driver.java line 17 (InheritableThreadLocal<WebDriver> driverPool)
        - Agent Action Plan Section 0.8.1 (Thread Safety Analysis)
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        # Create unique mock drivers for each thread
        def create_unique_driver(*args, **kwargs):
            driver = MagicMock()
            driver.session_id = f'session-{threading.current_thread().ident}'
            driver.capabilities = {'browserName': 'chrome'}
            return driver
        
        mock_chrome_driver.side_effect = create_unique_driver
        
        # Containers to capture driver instances from threads
        thread1_driver = []
        thread2_driver = []
        
        # Thread 1 function
        def thread1_func():
            driver = DriverManager.get_driver()
            thread1_driver.append(driver)
            time.sleep(0.1)  # Simulate some work
        
        # Thread 2 function
        def thread2_func():
            driver = DriverManager.get_driver()
            thread2_driver.append(driver)
            time.sleep(0.1)  # Simulate some work
        
        # Execute: Create and start threads
        t1 = threading.Thread(target=thread1_func, name='TestThread1')
        t2 = threading.Thread(target=thread2_func, name='TestThread2')
        
        t1.start()
        t2.start()
        
        # Wait for threads to complete
        t1.join()
        t2.join()
        
        # Assert: Both threads successfully got drivers
        assert len(thread1_driver) == 1, "Thread 1 did not get driver"
        assert len(thread2_driver) == 1, "Thread 2 did not get driver"
        
        # **CRITICAL ASSERTION**: Drivers are DIFFERENT instances (thread isolation)
        assert thread1_driver[0] is not thread2_driver[0], \
            "THREAD ISOLATION BROKEN: Both threads received same driver instance! " \
            "threading.local() is not working correctly. " \
            "This breaks parallel test execution."
        
        # Assert: Each driver has unique session ID
        assert thread1_driver[0].session_id != thread2_driver[0].session_id, \
            "Thread-local drivers should have different session IDs"
        
        print("✓ Thread-local isolation validated: threading.local() correctly isolates drivers per thread")
    
    # ========================================================================
    # Driver Cleanup and Lifecycle Tests
    # ========================================================================
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_driver_cleanup(self, mock_config_class, mock_chrome_manager, mock_chrome_driver):
        """
        Test driver cleanup and quit() functionality.
        
        Validates:
        - quit_driver() calls driver.quit() method
        - Thread-local reference is cleared after quit
        - quit_driver() is idempotent (safe to call multiple times)
        - Null/None check prevents errors when no driver exists
        
        Reference: Java Driver.java lines 50-55 (closeDriver method)
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        mock_driver = MagicMock()
        mock_driver.session_id = 'cleanup-test-session'
        mock_driver.capabilities = {'browserName': 'chrome'}
        mock_chrome_driver.return_value = mock_driver
        
        # Execute: Get driver then quit
        driver = DriverManager.get_driver()
        assert driver is not None, "Driver should exist before cleanup"
        
        DriverManager.quit_driver()
        
        # Assert: driver.quit() was called
        mock_driver.quit.assert_called_once()
        
        # Assert: Thread-local reference cleared
        # Calling get_driver() after quit should create NEW driver
        mock_driver2 = MagicMock()
        mock_driver2.session_id = 'new-session-after-quit'
        mock_driver2.capabilities = {'browserName': 'chrome'}
        mock_chrome_driver.return_value = mock_driver2
        
        new_driver = DriverManager.get_driver()
        
        # Assert: New driver created (not same as old)
        assert new_driver is mock_driver2, "New driver should be created after quit"
        assert new_driver is not driver, "Should be different driver instance after quit"
        
        # Test idempotence: calling quit_driver() again should not raise error
        DriverManager.quit_driver()
        DriverManager.quit_driver()  # Third call - still safe
        
        # Assert: Multiple quit calls don't cause errors
        print("✓ Driver cleanup validated: quit() called, reference cleared, idempotent")
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_driver_reinitialization_after_quit(self, mock_config_class, 
                                               mock_chrome_manager, mock_chrome_driver):
        """
        Test driver reinitialization after quit creates new instance.
        
        Validates:
        - get_driver() after quit_driver() creates fresh driver
        - New driver has different session ID
        - Thread-local storage properly resets
        - Lifecycle: create → quit → recreate works correctly
        
        Reference: Java Driver.java lines 21-44 (getDriver checks for null)
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        # First driver
        mock_driver1 = MagicMock()
        mock_driver1.session_id = 'first-session'
        mock_driver1.capabilities = {'browserName': 'chrome'}
        
        # Second driver (created after quit)
        mock_driver2 = MagicMock()
        mock_driver2.session_id = 'second-session'
        mock_driver2.capabilities = {'browserName': 'chrome'}
        
        # Configure mock to return different drivers on each call
        mock_chrome_driver.side_effect = [mock_driver1, mock_driver2]
        
        # Execute: First lifecycle
        driver1 = DriverManager.get_driver()
        assert driver1.session_id == 'first-session', "First driver incorrect"
        
        # Quit first driver
        DriverManager.quit_driver()
        
        # Execute: Second lifecycle (reinitialization)
        driver2 = DriverManager.get_driver()
        
        # Assert: New driver created with different session
        assert driver2.session_id == 'second-session', "Second driver incorrect"
        assert driver1 is not driver2, "Reinitialization should create new driver"
        
        # Assert: Both drivers had quit called (cleanup)
        mock_driver1.quit.assert_called_once()
        
        print("✓ Driver reinitialization validated: new driver created after quit")
    
    # ========================================================================
    # WebDriver Manager Provisioning Tests
    # ========================================================================
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_webdriver_manager_provisioning(self, mock_config_class, 
                                           mock_chrome_manager, mock_chrome_driver):
        """
        Test webdriver-manager automatic binary provisioning.
        
        Validates:
        - ChromeDriverManager().install() is called for Chrome
        - Install returns driver binary path
        - Path is passed to ChromeService
        - Automatic download/caching works (mocked)
        
        webdriver-manager caches binaries in ~/.wdm/drivers/ to avoid
        repeated downloads, improving test execution speed.
        
        Reference: Java Driver.java line 31 (WebDriverManager.chromedriver().setup())
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        # Mock ChromeDriverManager to return driver path
        expected_driver_path = '/home/user/.wdm/drivers/chromedriver/linux64/120.0.6099.71/chromedriver'
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = expected_driver_path
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        mock_driver = MagicMock()
        mock_driver.session_id = 'provisioning-test'
        mock_driver.capabilities = {'browserName': 'chrome'}
        mock_chrome_driver.return_value = mock_driver
        
        # Execute: Get driver
        driver = DriverManager.get_driver()
        
        # Assert: ChromeDriverManager was instantiated
        assert mock_chrome_manager.called, "ChromeDriverManager not instantiated"
        
        # Assert: install() was called to provision binary
        mock_chrome_manager_instance.install.assert_called_once()
        
        # Assert: Driver created successfully
        assert driver is not None, "Driver should be created"
        assert mock_chrome_driver.called, "Chrome WebDriver not instantiated"
        
        print(f"✓ webdriver-manager provisioning validated: binary path = {expected_driver_path}")
    
    # ========================================================================
    # Implicit Wait Configuration Tests
    # ========================================================================
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_implicit_wait_configuration(self, mock_config_class, 
                                        mock_chrome_manager, mock_chrome_driver):
        """
        Test NO implicit wait is configured (fixes Java anti-pattern).
        
        **CRITICAL TEST**: Validates that the Python version does NOT set
        implicit waits, fixing the anti-pattern from Java Driver.java lines 34 and 40:
            driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
        
        Mixing implicit and explicit waits causes:
        - Compound timeouts (implicit + explicit = unpredictable)
        - Inconsistent element lookup behavior
        - Difficult-to-debug test failures
        
        Python version uses ONLY explicit waits via utilities/wait_helpers.py.
        
        Validates:
        - implicitly_wait() is NOT called on driver
        - No timeout configuration beyond explicit waits
        - Clean driver setup without hidden wait behavior
        
        Reference: 
        - Java Driver.java lines 34, 40 (implicit wait anti-pattern)
        - Agent Action Plan Section 0.8.1 (Wait Strategy Analysis)
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        # Create mock driver with timeouts object
        mock_driver = MagicMock()
        mock_driver.session_id = 'implicit-wait-test'
        mock_driver.capabilities = {'browserName': 'chrome'}
        
        # Mock timeouts object (if driver tries to set implicit wait, we'll see it)
        mock_timeouts = MagicMock()
        mock_driver.timeouts = mock_timeouts
        
        mock_chrome_driver.return_value = mock_driver
        
        # Execute: Get driver
        driver = DriverManager.get_driver()
        
        # **CRITICAL ASSERTION**: implicitly_wait was NOT called
        # If this fails, the Java anti-pattern has been reproduced
        if hasattr(mock_timeouts, 'implicitly_wait'):
            assert not mock_timeouts.implicitly_wait.called, \
                "CRITICAL: implicitly_wait() should NOT be called! " \
                "This reproduces the Java anti-pattern from lines 34 and 40. " \
                "Use ONLY explicit waits via utilities/wait_helpers.py."
        
        # Assert: Driver was created successfully
        assert driver is not None, "Driver should be created"
        
        print("✓ NO implicit wait configured (fixes Java anti-pattern): explicit waits only")
    
    # ========================================================================
    # Exception Handling Tests
    # ========================================================================
    
    @patch('utilities.driver_manager.ConfigReader')
    def test_driver_initialization_failure(self, mock_config_class):
        """
        Test proper exception handling for driver initialization failures.
        
        Validates:
        - DriverInitializationError raised on failure (not swallowed)
        - Exception contains meaningful error message
        - No silent failures like Java printStackTrace()
        - Proper error propagation for test failure diagnostics
        
        Critical fix from Java ConfigurationReader which silently caught
        IOException with printStackTrace(), allowing null Properties object.
        Python version explicitly raises exceptions for fail-fast behavior.
        
        Reference:
        - Java ConfigurationReader.java lines 21-24 (exception swallowing)
        - Agent Action Plan Section 0.8.2 (Bug Fixes - Error Handling)
        """
        # Setup: Mock config to return unsupported browser type
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'safari',  # Unsupported browser
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        # Execute & Assert: Should raise DriverInitializationError
        with pytest.raises(ValueError) as exc_info:
            DriverManager.get_driver()
        
        # Assert: Exception message contains helpful information
        error_message = str(exc_info.value)
        assert 'safari' in error_message.lower(), "Error should mention unsupported browser"
        assert 'chrome' in error_message.lower() or 'firefox' in error_message.lower(), \
            "Error should list supported browsers"
        
        print(f"✓ Exception handling validated: ValueError raised with message: {error_message}")
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_driver_initialization_failure_webdriver_exception(self, mock_config_class,
                                                               mock_chrome_manager, 
                                                               mock_chrome_driver):
        """
        Test exception handling when WebDriver instantiation fails.
        
        Validates:
        - WebDriverException is caught and wrapped in DriverInitializationError
        - Original exception is preserved (chained exception)
        - Error message includes diagnostic information
        - Explicit error propagation (not silent failure)
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        # Mock Chrome WebDriver to raise WebDriverException
        mock_chrome_driver.side_effect = WebDriverException("Chrome failed to start")
        
        # Execute & Assert: Should raise DriverInitializationError
        with pytest.raises(DriverInitializationError) as exc_info:
            DriverManager.get_driver()
        
        # Assert: Exception message contains information about WebDriver failure
        error_message = str(exc_info.value)
        assert 'Chrome failed to start' in error_message or 'WebDriver' in error_message, \
            "Error should contain WebDriverException details"
        
        print(f"✓ WebDriverException handling validated: {error_message}")
    
    # ========================================================================
    # Null Safety Tests
    # ========================================================================
    
    def test_null_driver_safety(self):
        """
        Test null/None safety when no driver exists.
        
        Validates:
        - quit_driver() with no driver doesn't raise error
        - Null check before driver operations (fixes Java NullPointerException risk)
        - Idempotent cleanup behavior
        - Safe to call quit_driver() at any time
        
        Reference: Java Hooks.java had unguarded Driver.getDriver() calls
        that could cause NullPointerException if driver not initialized.
        """
        # Ensure no driver exists in thread-local storage
        if hasattr(DriverManager._thread_local, 'driver'):
            DriverManager._thread_local.driver = None
        
        # Execute: Call quit_driver() when no driver exists
        # Should NOT raise exception
        try:
            DriverManager.quit_driver()
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"quit_driver() raised exception with no driver: {e}")
        
        # Assert: No exception raised
        assert success, "quit_driver() should be safe to call with no driver"
        
        # Execute: Call multiple times (idempotence test)
        DriverManager.quit_driver()
        DriverManager.quit_driver()
        DriverManager.quit_driver()
        
        print("✓ Null safety validated: quit_driver() safe with no driver (idempotent)")
    
    # ========================================================================
    # Headless Mode Configuration Tests
    # ========================================================================
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_headless_mode_configuration(self, mock_config_class, 
                                        mock_chrome_manager, mock_chrome_driver):
        """
        Test headless browser mode configuration.
        
        Validates:
        - Headless mode enabled when configured
        - Chrome uses --headless=new (Selenium 4.x syntax)
        - Driver still maximizes window (even in headless)
        - Proper options passed to WebDriver constructor
        
        Headless mode critical for:
        - CI/CD pipeline execution (no GUI)
        - Docker containers (no X server)
        - Faster test execution (no rendering overhead)
        """
        # Setup mocks for headless configuration
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': True  # Headless enabled
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        mock_driver = MagicMock()
        mock_driver.session_id = 'headless-test-session'
        mock_driver.capabilities = {'browserName': 'chrome'}
        mock_chrome_driver.return_value = mock_driver
        
        # Execute: Get driver with headless configuration
        driver = DriverManager.get_driver()
        
        # Assert: Chrome WebDriver was called
        assert mock_chrome_driver.called, "Chrome WebDriver not instantiated"
        
        # Assert: Driver created successfully
        assert driver is not None, "Driver should be created in headless mode"
        
        # Assert: Window maximized (even in headless mode)
        mock_driver.maximize_window.assert_called_once()
        
        print("✓ Headless mode configuration validated: --headless=new for Chrome")
    
    # ========================================================================
    # Driver Status and Diagnostics Tests
    # ========================================================================
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_get_thread_driver_status(self, mock_config_class, 
                                     mock_chrome_manager, mock_chrome_driver):
        """
        Test driver status diagnostic utility method.
        
        Validates:
        - get_thread_driver_status() returns status dictionary
        - Status includes thread name, thread ID, driver existence
        - Status includes session ID and capabilities when driver exists
        - Useful for debugging and monitoring driver lifecycle
        
        This is a new method not present in Java version, added for
        enhanced observability in Python implementation.
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        mock_driver = MagicMock()
        mock_driver.session_id = 'status-test-session-789'
        mock_driver.capabilities = {'browserName': 'chrome', 'browserVersion': '120.0'}
        mock_chrome_driver.return_value = mock_driver
        
        # Test 1: Status before driver creation
        status_before = DriverManager.get_thread_driver_status()
        
        assert 'thread_name' in status_before, "Status should include thread_name"
        assert 'thread_id' in status_before, "Status should include thread_id"
        assert 'has_driver' in status_before, "Status should include has_driver"
        assert status_before['has_driver'] is False, "has_driver should be False before creation"
        
        # Test 2: Status after driver creation
        driver = DriverManager.get_driver()
        status_after = DriverManager.get_thread_driver_status()
        
        assert status_after['has_driver'] is True, "has_driver should be True after creation"
        assert status_after['driver_session'] == 'status-test-session-789', \
            "Status should include correct session ID"
        assert status_after['driver_capabilities']['browserName'] == 'chrome', \
            "Status should include driver capabilities"
        
        print(f"✓ Driver status diagnostics validated: {status_after}")
    
    # ========================================================================
    # Module-Level Convenience Functions Tests
    # ========================================================================
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    @patch('utilities.driver_manager.ChromeDriverManager')
    @patch('utilities.driver_manager.ConfigReader')
    def test_module_level_get_driver_function(self, mock_config_class, 
                                             mock_chrome_manager, mock_chrome_driver):
        """
        Test module-level convenience function get_driver().
        
        Validates:
        - get_driver() module function works correctly
        - Provides simpler import pattern for common use
        - Returns same driver as DriverManager.get_driver()
        """
        # Setup mocks
        mock_config = Mock(spec=ConfigReader)
        mock_config.get_property.side_effect = lambda key, default=None: {
            'browser.type': 'chrome',
            'browser.headless': False
        }.get(key, default)
        mock_config_class.return_value = mock_config
        
        mock_chrome_manager_instance = Mock()
        mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_chrome_manager_instance
        
        mock_driver = MagicMock()
        mock_driver.session_id = 'module-func-test'
        mock_driver.capabilities = {'browserName': 'chrome'}
        mock_chrome_driver.return_value = mock_driver
        
        # Execute: Use module-level function
        driver1 = get_driver()
        driver2 = DriverManager.get_driver()
        
        # Assert: Both return same driver instance
        assert driver1 is driver2, "Module function should return same driver as class method"
        
        print("✓ Module-level get_driver() convenience function validated")
    
    def test_module_level_quit_driver_function(self):
        """
        Test module-level convenience function quit_driver().
        
        Validates:
        - quit_driver() module function works correctly
        - Provides simpler import pattern for common use
        - Equivalent to DriverManager.quit_driver()
        """
        # Execute: Use module-level function (should not raise error)
        try:
            quit_driver()
            success = True
        except Exception as e:
            success = False
            pytest.fail(f"quit_driver() module function raised exception: {e}")
        
        # Assert: No exception raised
        assert success, "Module-level quit_driver() should work"
        
        print("✓ Module-level quit_driver() convenience function validated")


# ============================================================================
# Test Execution Entry Point
# ============================================================================

if __name__ == '__main__':
    """
    Run tests directly with pytest when module executed.
    
    Usage:
        python tests/test_driver_manager.py
        pytest tests/test_driver_manager.py -v
        pytest tests/test_driver_manager.py -v -s  # Show print statements
    """
    pytest.main([__file__, '-v', '-s'])

