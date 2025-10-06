"""
Configuration package for Testinium Python test automation framework.

This package provides centralized, type-safe configuration management for the test
automation framework, replacing the Java ConfigurationReader.java Properties-based
approach with a modern Python dataclass-based implementation.

The configuration module supports:
- YAML-based configuration files (config/config.yaml)
- Environment variable substitution for sensitive data (${VAR_NAME} syntax)
- Type-safe access via dataclasses with full IDE autocompletion
- Backward-compatible key-based access (config.get('browser.type'))
- Singleton pattern for convenient global access
- Comprehensive validation and error handling

Architecture:
-----------
This package enables two import patterns throughout the test framework:

1. Direct class imports:
   >>> from config import Config, BrowserConfig, TimeoutConfig
   >>> config = Config()
   >>> print(config.browser.type)

2. Submodule imports (explicit):
   >>> from config.test_config import Config, get_config
   >>> config = get_config()

Configuration Hierarchy:
-----------------------
- BrowserConfig: Browser settings (type, headless, window size, implicit waits)
- TimeoutConfig: Timeout values for WebDriver waits (explicit, page load, etc.)
- ApplicationConfig: Application URLs (base_url, login_url, web_table_url, etc.)
- CredentialsConfig: User credentials loaded from environment variables
- ReportingConfig: Test reporting settings (screenshots, formats, output paths)

Security:
--------
All credentials MUST be loaded from environment variables, never hardcoded.
This remediates the critical security vulnerability found in the original
EmployeeP.java file which contained hardcoded credentials.

Example .env file:
    TEST_USERNAME=user@example.com
    TEST_PASSWORD=secure_password
    SALES_MANAGER_USERNAME=sales@example.com
    SALES_MANAGER_PASSWORD=sales_password
    POS_MANAGER_USERNAME=pos@example.com
    POS_MANAGER_PASSWORD=pos_password

Usage Examples:
--------------
Basic usage with type-safe access:
    >>> from config import Config
    >>> config = Config()
    >>> print(config.browser.type)
    'chrome'
    >>> print(config.timeouts.explicit)
    10
    >>> print(config.application.base_url)
    'https://testinium.example.com'

Using singleton pattern:
    >>> from config import get_config
    >>> config = get_config()
    >>> driver_type = config.browser.type

Backward-compatible key access:
    >>> from config import Config
    >>> config = Config()
    >>> browser_type = config.get('browser.type', 'chrome')

In Behave step definitions:
    >>> # In features/environment.py
    >>> from config import Config
    >>> def before_all(context):
    >>>     context.config = Config()
    >>>     context.base_url = context.config.application.base_url

Type hints for better IDE support:
    >>> from config import Config, BrowserConfig, ReportingConfig
    >>> def setup_browser(browser_config: BrowserConfig) -> None:
    >>>     print(f"Setting up {browser_config.type} browser")

Migration Notes:
---------------
This package replaces:
- Java: ConfigurationReader.java with Properties file loading
- Java: Hardcoded configuration in Driver.java and step definitions
- Java: Unsafe credential storage in EmployeeP.java

Benefits over Java implementation:
- Type safety with IDE autocompletion
- Environment variable support for secure credential management
- Comprehensive validation and error handling (vs. swallowed IOExceptions)
- Flexible configuration formats (YAML instead of Properties)
- Better testability with singleton reset capability
"""

# Standard library imports
import logging


# Import all configuration classes and utilities from test_config module
# These imports enable convenient access pattern: 'from config import Config'
from config.test_config import (
    Config,
    BrowserConfig,
    TimeoutConfig,
    ApplicationConfig,
    CredentialsConfig,
    ReportingConfig,
    get_config,
    reset_config,
)

# Define public API for the config package
# This list controls what gets imported with 'from config import *'
# and provides clear documentation of the package's public interface
__all__ = [
    # Main configuration class providing type-safe access to all settings
    'Config',

    # Dataclass configuration sections for structured access
    'BrowserConfig',      # Browser settings (type, headless, window_size, implicit_wait)
    'TimeoutConfig',      # Timeout values (explicit, page_load, element_presence, clickability)
    'ApplicationConfig',  # Application URLs (base_url, login_url, web_table_url, empl_title)
    'CredentialsConfig',  # User credentials (username, password, role-based credentials)
    'ReportingConfig',    # Reporting settings (screenshot_on_failure, output_directory, formats)

    # Utility functions for singleton access pattern
    'get_config',   # Get or create singleton Config instance
    'reset_config', # Reset singleton (useful for testing)
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'Testinium QA Team'
__description__ = 'Type-safe configuration management for Python test automation framework'

logger = logging.getLogger(__name__)
logger.debug("Config package initialized - all configuration classes available for import")
