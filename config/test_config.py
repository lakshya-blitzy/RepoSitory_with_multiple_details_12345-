"""
Type-safe configuration management for Testinium test automation framework.

This module provides structured, type-safe access to test configuration loaded from
config.yaml with support for environment variable overrides. It replaces the Java
ConfigurationReader.java pattern with a modern Python dataclass-based approach.

The configuration hierarchy includes:
- Browser settings (type, headless mode, window size, waits)
- Timeout values (explicit, page load, element presence, clickability)
- Application URLs (base, login, web table, employee title)
- Credentials (test user, sales manager, POS manager)
- Reporting options (screenshots, output directories, formats)

Environment variables can be injected using ${VAR_NAME} or ${VAR_NAME:default} syntax
in config.yaml, enabling secure credential management without hardcoding.

Example:
    >>> from config.test_config import Config
    >>> config = Config()
    >>> print(config.browser.type)  # 'chrome'
    >>> print(config.timeouts.explicit)  # 10
    >>> print(config.application.base_url)  # From environment or config
"""

import os
import re
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

import yaml
from dotenv import load_dotenv

# Configure logging for configuration management
logger = logging.getLogger(__name__)


@dataclass
class BrowserConfig:
    """
    Browser configuration settings.

    Attributes:
        type: Browser type ('chrome', 'firefox', 'edge', 'safari')
        headless: Whether to run browser in headless mode
        window_size: Browser window dimensions as (width, height) tuple
        implicit_wait: Implicit wait timeout in seconds (deprecated, use 0)
    """
    type: str
    headless: bool
    window_size: Tuple[int, int]
    implicit_wait: int = 0  # Default to 0 - use explicit waits instead


@dataclass
class TimeoutConfig:
    """
    Timeout configuration for WebDriver waits.

    All timeouts are in seconds. These replace hardcoded timeout values
    scattered throughout Java step definitions.

    Attributes:
        explicit: Default explicit wait timeout
        page_load: Page load timeout
        element_presence: Wait for element presence timeout
        clickability: Wait for element clickability timeout
    """
    explicit: int
    page_load: int
    element_presence: int
    clickability: int


@dataclass
class ApplicationConfig:
    """
    Application URL configuration.

    Supports environment variable substitution for deployment flexibility.

    Attributes:
        base_url: Base application URL
        login_url: Login page URL
        web_table_url: Web table page URL
        empl_title: Expected employee page title
    """
    base_url: str
    login_url: str
    web_table_url: str
    empl_title: str


@dataclass
class CredentialsConfig:
    """
    User credentials configuration.

    All credentials should be loaded from environment variables, never hardcoded.
    This remediates the security vulnerability found in EmployeeP.java.

    Attributes:
        username: Default test user username
        password: Default test user password
        sales_manager_username: Sales manager role username
        sales_manager_password: Sales manager role password
        pos_manager_username: POS manager role username
        pos_manager_password: POS manager role password
    """
    username: Optional[str] = None
    password: Optional[str] = None
    sales_manager_username: Optional[str] = None
    sales_manager_password: Optional[str] = None
    pos_manager_username: Optional[str] = None
    pos_manager_password: Optional[str] = None


@dataclass
class ReportingConfig:
    """
    Test reporting configuration.

    Controls screenshot capture, output directories, and report formats.

    Attributes:
        screenshot_on_failure: Whether to capture screenshots on test failures
        output_directory: Base output directory for all reports
        formats: List of report formats to generate (e.g., ['json', 'html', 'allure'])
        screenshot_directory: Directory for screenshot storage
    """
    screenshot_on_failure: bool
    output_directory: str
    formats: List[str] = field(default_factory=list)
    screenshot_directory: str = "reports/screenshots"


class Config:  # pylint: disable=too-many-instance-attributes
    """
    Main configuration class providing type-safe access to test configuration.

    Loads configuration from config.yaml with environment variable substitution.
    Uses python-dotenv to load .env files before parsing YAML, enabling secure
    credential injection.

    This class provides two access patterns:
    1. Type-safe dot notation: config.browser.type
    2. Backward-compatible key access: config.get('browser.type')

    Example:
        >>> config = Config()
        >>> print(config.browser.type)
        'chrome'
        >>> print(config.get('browser.type'))
        'chrome'
        >>> print(config.timeouts.explicit)
        10

    Args:
        config_file: Path to YAML configuration file (default: 'config/config.yaml')

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If YAML parsing fails
        ValueError: If required configuration keys are missing
    """

    def __init__(self, config_file: str = 'config/config.yaml'):
        """
        Initialize configuration by loading YAML and creating dataclass instances.

        Args:
            config_file: Path to YAML configuration file

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML parsing fails
            ValueError: If required configuration is missing
        """
        # Load environment variables from .env file if present
        load_dotenv()
        logger.info("Environment variables loaded from .env file")

        # Load and parse YAML configuration
        self._config_file = config_file
        self._raw_config = self._load_yaml(config_file)
        logger.info("Configuration loaded from %s", config_file)

        # Instantiate nested configuration dataclasses
        try:
            self.browser = BrowserConfig(**self._raw_config['browser'])
            logger.debug("Browser config: type=%s, headless=%s",
                         self.browser.type, self.browser.headless)

            self.timeouts = TimeoutConfig(**self._raw_config['timeouts'])
            logger.debug("Timeout config: explicit=%ss, page_load=%ss",
                         self.timeouts.explicit, self.timeouts.page_load)

            self.application = ApplicationConfig(**self._raw_config['application'])
            logger.debug("Application config: base_url=%s",
                         self.application.base_url)

            # Credentials may be None if environment variables not set
            credentials_data = self._raw_config.get('credentials', {})
            self.credentials = CredentialsConfig(**credentials_data)
            self._validate_credentials()

            self.reporting = ReportingConfig(**self._raw_config['reporting'])
            logger.debug("Reporting config: formats=%s", self.reporting.formats)

        except KeyError as e:
            logger.error("Missing required configuration section: %s", e)
            raise ValueError(f"Missing required configuration section: {e}") from e
        except TypeError as e:
            logger.error("Invalid configuration structure: %s", e)
            raise ValueError(f"Invalid configuration structure: {e}") from e

    def _load_yaml(self, config_file: str) -> Dict[str, Any]:
        """
        Load YAML configuration file with environment variable substitution.

        Supports ${VAR_NAME} and ${VAR_NAME:default_value} syntax for
        environment variable injection.

        Args:
            config_file: Path to YAML configuration file

        Returns:
            Parsed configuration dictionary

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        config_path = Path(config_file)

        if not config_path.exists():
            logger.error("Configuration file not found: %s", config_file)
            raise FileNotFoundError(f"Configuration file not found: {config_file}")

        try:
            with config_path.open('r', encoding='utf-8') as f:
                yaml_content = f.read()

            # Substitute environment variables before parsing YAML
            yaml_content = self._substitute_env_vars(yaml_content)

            # Parse YAML safely
            config_dict = yaml.safe_load(yaml_content)

            if config_dict is None:
                logger.error("Configuration file is empty or invalid")
                raise ValueError("Configuration file is empty or invalid")

            return config_dict

        except yaml.YAMLError as e:
            logger.exception("Failed to parse YAML configuration: %s", e)
            raise
        except Exception as e:
            logger.exception("Unexpected error loading configuration: %s", e)
            raise

    def _substitute_env_vars(self, yaml_content: str) -> str:
        """
        Substitute environment variable placeholders in YAML content.

        Supports two formats:
        - ${VAR_NAME}: Required environment variable (raises error if missing)
        - ${VAR_NAME:default}: Optional with default value

        Args:
            yaml_content: Raw YAML content string

        Returns:
            YAML content with environment variables substituted

        Example:
            Input: "base_url: ${BASE_URL:https://default.com}"
            Output: "base_url: https://testinium.example.com" (if BASE_URL is set)
        """
        # Pattern matches ${VAR_NAME} or ${VAR_NAME:default_value}
        env_var_pattern = re.compile(r'\$\{([^}:]+)(?::([^}]*))?\}')

        def replace_env_var(match):
            var_name = match.group(1)
            default_value = match.group(2)

            # Get environment variable value
            env_value = os.getenv(var_name)

            if env_value is not None:
                logger.debug("Substituted environment variable: %s", var_name)
                return env_value
            if default_value is not None:
                logger.debug("Using default value for %s: %s",
                             var_name, default_value)
                return default_value
            # For credentials, log warning but don't fail (they're optional)
            if var_name.endswith(('USERNAME', 'PASSWORD')):
                logger.warning("Credential environment variable not set: %s",
                               var_name)
                return ''  # Return empty string for optional credentials
            logger.error("Required environment variable not set: %s",
                         var_name)
            raise ValueError(f"Required environment variable not set: {var_name}")

        return env_var_pattern.sub(replace_env_var, yaml_content)

    def _validate_credentials(self) -> None:
        """
        Validate that required credentials are available.

        Logs warnings for missing credentials but doesn't fail, as some tests
        may not require all credential types.
        """
        if not self.credentials.username or not self.credentials.password:
            logger.warning(
                "Default test credentials not configured. "
                "Set TEST_USERNAME and TEST_PASSWORD environment variables."
            )

        if (not self.credentials.sales_manager_username or
                not self.credentials.sales_manager_password):
            logger.warning(
                "Sales manager credentials not configured. "
                "Set SALES_MANAGER_USERNAME and SALES_MANAGER_PASSWORD for role-based tests."
            )

        if not self.credentials.pos_manager_username or not self.credentials.pos_manager_password:
            logger.warning(
                "POS manager credentials not configured. "
                "Set POS_MANAGER_USERNAME and POS_MANAGER_PASSWORD for role-based tests."
            )

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation key.

        Provides backward compatibility with ConfigurationReader.getProperty(key)
        pattern from Java implementation. Supports nested key access using dots.

        Args:
            key: Configuration key in dot notation (e.g., 'browser.type')
            default: Default value to return if key not found

        Returns:
            Configuration value or default if key not found

        Example:
            >>> config.get('browser.type')
            'chrome'
            >>> config.get('browser.headless')
            False
            >>> config.get('timeouts.explicit')
            10
            >>> config.get('nonexistent.key', 'default_value')
            'default_value'
        """
        try:
            # Split key by dots and traverse nested structure
            keys = key.split('.')

            # First level maps to dataclass attributes
            if len(keys) == 1:
                return getattr(self, keys[0], default)

            # Navigate nested structure
            obj = getattr(self, keys[0], None)
            if obj is None:
                return default

            for k in keys[1:]:
                obj = getattr(obj, k, None)
                if obj is None:
                    return default

            return obj

        except AttributeError:
            logger.warning("Configuration key not found: %s", key)
            return default

    def __repr__(self) -> str:
        """
        String representation of configuration.

        Masks sensitive credentials for security.

        Returns:
            Configuration summary string
        """
        return (
            f"Config(\n"
            f"  browser={self.browser},\n"
            f"  timeouts={self.timeouts},\n"
            f"  application=ApplicationConfig(base_url='{self.application.base_url}', ...),\n"
            f"  credentials=CredentialsConfig(username='***', password='***', ...),\n"
            f"  reporting={self.reporting}\n"
            f")"
        )


# Singleton instance for convenient access across test framework
_config_instance: Optional[Config] = None


def get_config(config_file: str = 'config/config.yaml') -> Config:
    """
    Get or create singleton Config instance.

    Provides convenient access to configuration throughout the test framework
    without needing to pass config objects explicitly.

    Args:
        config_file: Path to YAML configuration file

    Returns:
        Singleton Config instance

    Example:
        >>> from config.test_config import get_config
        >>> config = get_config()
        >>> print(config.browser.type)
    """
    global _config_instance  # pylint: disable=global-statement

    if _config_instance is None:
        _config_instance = Config(config_file)
        logger.info("Singleton Config instance created")

    return _config_instance


def reset_config() -> None:
    """
    Reset singleton Config instance.

    Useful for testing or reloading configuration after changes.
    """
    global _config_instance  # pylint: disable=global-statement
    _config_instance = None
    logger.info("Config instance reset")
