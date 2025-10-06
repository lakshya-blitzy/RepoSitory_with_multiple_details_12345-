"""
Utilities Package

This package provides core infrastructure components for the Python Selenium + Behave
BDD test automation framework. It replaces the Java utilities package from the original
implementation with enhanced Python equivalents.

Package Contents:
    - DriverManager: Thread-safe WebDriver lifecycle management
    - DriverInitializationError: Custom exception for driver setup failures
    - ConfigReader: Singleton configuration management with YAML and environment variable support
    - ConfigurationError: Custom exception for configuration errors
    - WaitHelpers: Centralized explicit wait utilities eliminating Thread.sleep() anti-patterns
    - capture_screenshot: Screenshot capture for test failure diagnostics
    - capture_browser_logs: Browser console log collection for debugging
    - sanitize_filename: Cross-platform filename sanitization utility

Migration Context:
    This module is part of the Java-to-Python test framework migration, converting:
    - Java Driver.java → driver_manager.py (with Firefox driver bug fix)
    - Java ConfigurationReader.java → config_reader.py (with proper error handling)
    - New wait_helpers.py (eliminates Thread.sleep() and implicit/explicit wait mixing)
    - New screenshot_helper.py (extracts logic from Hooks.java with enhancements)

Key Architectural Improvements:
    1. Thread Safety: threading.local() replaces InheritableThreadLocal
    2. Wait Strategy: Explicit waits only (no implicit waits)
    3. Error Handling: Proper exception propagation vs silent failures
    4. Configuration: YAML + environment variables vs properties files
    5. Security: No hardcoded credentials, environment variable management
    6. Logging: Comprehensive logging throughout all utilities

Usage Examples:
    >>> # Driver management
    >>> from utilities import DriverManager
    >>> driver = DriverManager.get_driver()
    >>> # ... perform test actions ...
    >>> DriverManager.quit_driver()
    >>>
    >>> # Configuration access
    >>> from utilities import ConfigReader
    >>> config = ConfigReader()
    >>> browser_type = config.get_property('browser.type', default='chrome')
    >>>
    >>> # Wait helpers
    >>> from utilities import WaitHelpers
    >>> from selenium.webdriver.common.by import By
    >>> wait_helper = WaitHelpers(driver)
    >>> element = wait_helper.wait_for_element_clickable((By.ID, "submit"))
    >>>
    >>> # Screenshot capture
    >>> from utilities import capture_screenshot
    >>> screenshot_path = capture_screenshot(driver, "Test Failure Scenario")

Technical Specification Alignment:
    This package implements Section 0.9 requirements from the Agent Action Plan:
    - Complete Java to Python utilities migration
    - Bug fixes (Firefox driver on line 37)
    - Security fixes (no hardcoded credentials)
    - Modern Python patterns (type hints, properties, context managers)
    - Production-ready code with comprehensive error handling
"""

# Import utility classes and exceptions from driver_manager module
from utilities.driver_manager import (
    DriverManager,
    DriverInitializationError,
)

# Import configuration management classes from config_reader module
from utilities.config_reader import (
    ConfigReader,
    ConfigurationError,
)

# Import wait helper utilities from wait_helpers module
from utilities.wait_helpers import (
    WaitHelpers,
)

# Import screenshot and logging utilities from screenshot_helper module
from utilities.screenshot_helper import (
    capture_screenshot,
    capture_browser_logs,
    sanitize_filename,
)


# Define public API via __all__ for controlled exports
# This enables: from utilities import *
# While maintaining explicit control over exported symbols
__all__ = [
    # Driver management
    'DriverManager',
    'DriverInitializationError',
    
    # Configuration management
    'ConfigReader',
    'ConfigurationError',
    
    # Wait utilities
    'WaitHelpers',
    
    # Screenshot and diagnostic utilities
    'capture_screenshot',
    'capture_browser_logs',
    'sanitize_filename',
]


# Package metadata
__version__ = '1.0.0'
__author__ = 'Test Automation Team'
__description__ = 'Core utilities for Python Selenium + Behave test automation framework'


# Package-level convenience functions for common use cases
def get_driver():
    """
    Package-level convenience function to get WebDriver instance.
    
    This provides the shortest import path for the most common operation:
        from utilities import get_driver
        driver = get_driver()
    
    Returns:
        WebDriver: Thread-local WebDriver instance
        
    Raises:
        DriverInitializationError: If driver creation fails
    """
    return DriverManager.get_driver()


def quit_driver():
    """
    Package-level convenience function to quit WebDriver.
    
    Provides shortest import path:
        from utilities import quit_driver
        quit_driver()
    """
    DriverManager.quit_driver()


def get_config():
    """
    Package-level convenience function to get ConfigReader singleton.
    
    Provides shortest import path:
        from utilities import get_config
        config = get_config()
        browser = config.get_property('browser.type')
    
    Returns:
        ConfigReader: Singleton configuration reader instance
    """
    return ConfigReader()


# Add convenience functions to public API
__all__.extend([
    'get_driver',
    'quit_driver',
    'get_config',
])


# Module initialization logging
import logging
logger = logging.getLogger(__name__)
logger.debug(
    "Utilities package initialized (version: %s). "
    "Available components: %s",
    __version__, ', '.join(__all__)
)
