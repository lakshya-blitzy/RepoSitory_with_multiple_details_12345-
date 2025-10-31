"""
Configuration Reader Module

This module provides centralized configuration management for the test automation framework.
Replaces Java ConfigurationReader.java with enhanced features:
- YAML configuration support (replacing missing configuration.properties)
- Environment variable integration with precedence
- Proper exception handling (fixes silent IOException swallowing from Java version)
- Singleton pattern for shared configuration access
- Dot notation for nested configuration keys
- Type-safe configuration retrieval with defaults

Critical Fix from Java Version:
    The original Java ConfigurationReader (lines 21-24) silently caught IOException
    with printStackTrace() allowing null Properties object. This Python version
    explicitly raises FileNotFoundError and yaml.YAMLError for proper error handling.

Example Usage:
    >>> from utilities.config_reader import ConfigReader
    >>> config = ConfigReader()
    >>> browser_type = config.get_property('browser.type', default='chrome')
    >>> base_url = config.get_property('test_data.base_url')
    >>> all_config = config.get_all_properties()
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from copy import deepcopy
import yaml
from dotenv import load_dotenv


# Configure module logger
logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """
    Custom exception for configuration-related errors.

    Raised when:
    - Configuration file is missing
    - YAML parsing fails
    - Required configuration key is missing
    - Invalid configuration format

    This replaces the silent exception swallowing from Java ConfigurationReader.
    """
    pass


class ConfigReader:
    """
    Singleton configuration reader supporting YAML files and environment variables.

    Features:
    - Singleton pattern: Only one instance exists per process
    - YAML configuration: Loads from config/config.yaml
    - Environment variable precedence: Env vars override YAML values
    - Dot notation: Access nested keys like 'browser.type'
    - Default values: Optional defaults for missing keys
    - Type preservation: Maintains YAML types (str, int, bool, float, list, dict)
    - Security: Sensitive credentials from environment variables only

    Configuration Precedence (highest to lowest):
    1. Environment variables (e.g., BROWSER_TYPE)
    2. .env file variables
    3. config/config.yaml values
    4. Provided default values

    Thread Safety:
        This singleton is NOT thread-safe during initialization. Ensure first
        instantiation happens in main thread before parallel test execution.

    Example:
        >>> config = ConfigReader()
        >>> browser = config.get_property('browser.type', default='chrome')
        >>> timeout = config.get_property('timeouts.explicit', default=10)
        >>> all_props = config.get_all_properties()
    """

    _instance: Optional['ConfigReader'] = None
    _config: Dict[str, Any] = {}
    _initialized: bool = False

    def __new__(cls, *args, **kwargs) -> 'ConfigReader':
        """
        Implement singleton pattern ensuring single instance per process.

        Args:
            *args: Positional arguments (passed to __init__)
            **kwargs: Keyword arguments (passed to __init__)

        Returns:
            ConfigReader: The singleton instance
        """
        if cls._instance is None:
            logger.debug("Creating new ConfigReader singleton instance")
            cls._instance = super(ConfigReader, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_file: str = "config/config.yaml") -> None:
        """
        Initialize configuration reader (runs only once due to singleton).

        Args:
            config_file: Path to YAML configuration file relative to project root
                        Defaults to 'config/config.yaml'

        Raises:
            FileNotFoundError: If configuration file doesn't exist
            ConfigurationError: If YAML parsing fails or file is invalid

        Note:
            Due to singleton pattern, __init__ is called multiple times but
            initialization logic runs only once (tracked by _initialized flag).
        """
        # Only initialize once (singleton pattern)
        if ConfigReader._initialized:
            logger.debug("ConfigReader already initialized, skipping re-initialization")
            return

        logger.info("Initializing ConfigReader with config file: %s", config_file)
        self._config_file = config_file

        try:
            # Load environment variables from .env file (if exists)
            # This supports local development with sensitive credentials
            env_file = Path(".env")
            if env_file.exists():
                logger.info("Loading environment variables from .env file")
                load_dotenv(dotenv_path=env_file)
            else:
                logger.debug(".env file not found, skipping dotenv loading")

            # Load YAML configuration
            self._load_configuration()

            ConfigReader._initialized = True
            logger.info("ConfigReader initialization complete")

        except Exception as e:
            logger.exception(f"Failed to initialize ConfigReader: {e}")
            raise

    def _load_configuration(self) -> None:
        """
        Load YAML configuration file into memory.

        Replaces Java Properties loading with YAML support for:
        - Nested configuration structures (dictionaries)
        - Type preservation (string, int, bool, float)
        - Lists and complex data structures
        - Multi-line strings
        - Comments in configuration

        Raises:
            FileNotFoundError: If config file doesn't exist
            ConfigurationError: If YAML parsing fails

        Critical Fix:
            Java version silently swallowed IOException (lines 21-24) allowing
            null Properties. This version explicitly raises exceptions for
            fail-fast behavior.
        """
        config_path = Path(self._config_file)

        # Validate file exists
        if not config_path.exists():
            error_msg = (
                f"Configuration file not found: {config_path.resolve()}. "
                f"Expected config/config.yaml in project root. "
                f"This replaces the missing configuration.properties file "
                f"referenced in Java ConfigurationReader."
            )
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        if not config_path.is_file():
            error_msg = f"Configuration path is not a file: {config_path.resolve()}"
            logger.error(error_msg)
            raise ConfigurationError(error_msg)

        # Load and parse YAML
        try:
            logger.debug("Reading YAML configuration from: %s", config_path.resolve())
            with open(config_path, 'r', encoding='utf-8') as file:
                ConfigReader._config = yaml.safe_load(file)

            # Validate loaded configuration
            if ConfigReader._config is None:
                ConfigReader._config = {}
                logger.warning("YAML file is empty, using empty configuration")

            if not isinstance(ConfigReader._config, dict):
                error_msg = (
                    f"Invalid YAML format: expected dictionary at root, "
                    f"got {type(ConfigReader._config).__name__}"
                )
                logger.error(error_msg)
                raise ConfigurationError(error_msg)

            logger.info("Successfully loaded configuration with %d top-level keys: %s", len(ConfigReader._config), list(ConfigReader._config.keys()))

        except yaml.YAMLError as yaml_err:
            error_msg = "Failed to parse YAML configuration: %s" % yaml_err
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from yaml_err

        except Exception as exc:
            error_msg = "Unexpected error loading configuration: %s" % exc
            logger.exception(error_msg)
            raise ConfigurationError(error_msg) from exc

    # Sentinel value to distinguish "no default" from "default=None"
    _NO_DEFAULT = object()

    def get_property(
        self,
        key: str,
        default: Any = _NO_DEFAULT
    ) -> Optional[Any]:
        """
        Retrieve configuration value by key with environment variable precedence.

        Supports:
        - Dot notation for nested keys: 'browser.type' -> config['browser']['type']
        - Environment variable override: 'browser.type' checks BROWSER_TYPE env var first
        - Default values: Returns default if key missing and default provided (including None)
        - Type preservation: Returns YAML types (str, int, bool, float, list, dict)

        Configuration Precedence (highest to lowest):
        1. Environment variable (BROWSER_TYPE)
        2. YAML configuration (browser.type)
        3. Provided default value

        Args:
            key: Configuration key using dot notation for nested access
                 Examples: 'browser.type', 'timeouts.explicit', 'test_data.base_url'
            default: Default value returned if key not found (optional, can be None)
                    If not provided and key missing, raises KeyError

        Returns:
            Configuration value from environment variable, YAML, or default
            Type matches YAML type (str, int, bool, float, list, dict)

        Raises:
            KeyError: If key not found and no default provided

        Example:
            >>> config = ConfigReader()
            >>> # Get with default
            >>> browser = config.get_property('browser.type', default='chrome')
            >>> # Get with None as default
            >>> optional = config.get_property('optional.key', default=None)
            >>> # Get from environment variable (BROWSER_TYPE)
            >>> browser = config.get_property('browser.type')
            >>> # Get nested value
            >>> timeout = config.get_property('timeouts.explicit', default=10)
            >>> # Get required value (raises KeyError if missing)
            >>> base_url = config.get_property('test_data.base_url')
        """
        # Convert dot notation to environment variable format
        # Example: 'browser.type' -> 'BROWSER_TYPE'
        env_key = key.upper().replace('.', '_')

        # Check environment variable first (highest precedence)
        env_value = os.getenv(env_key)
        if env_value is not None:
            logger.debug("Retrieved config '%s' from environment variable '%s'", key, env_key)
            return env_value

        # Navigate nested dictionary using dot notation
        # Example: 'browser.type' -> config['browser']['type']
        try:
            value = ConfigReader._config
            for key_part in key.split('.'):
                value = value[key_part]

            logger.debug("Retrieved config '%s' from YAML configuration", key)
            return value

        except (KeyError, TypeError) as key_err:
            # Key not found in configuration
            # Check if a default was provided (including None)
            if default is not ConfigReader._NO_DEFAULT:
                logger.debug("Config key '%s' not found, using default: %s", key, default)
                return default

            # No default provided - raise error for required key
            error_msg = (
                f"Required configuration key '{key}' not found. "
                f"Check config/config.yaml or set environment variable '{env_key}'. "
                f"Available top-level keys: {list(ConfigReader._config.keys())}"
            )
            logger.error(error_msg)
            raise KeyError(error_msg) from key_err

    def get_all_properties(self) -> Dict[str, Any]:
        """
        Retrieve complete configuration dictionary.

        Returns:
            Deep copy of entire configuration dictionary to prevent external
            modification of singleton state. This protects configuration
            integrity across test scenarios.

        Note:
            Environment variables are NOT included in this dictionary,
            only YAML configuration values. Use get_property() to access
            values with environment variable precedence.

        Example:
            >>> config = ConfigReader()
            >>> all_config = config.get_all_properties()
            >>> print(all_config['browser'])
            {'type': 'chrome', 'headless': False}
        """
        logger.debug("Returning deep copy of complete configuration")
        return deepcopy(ConfigReader._config)

    def __repr__(self) -> str:
        """
        String representation of ConfigReader instance.

        Returns:
            String showing configuration file path and key count
        """
        return (
            f"ConfigReader(config_file='{self._config_file}', "
            f"keys={len(ConfigReader._config)})"
        )


# Module-level convenience function for quick access
def get_config() -> ConfigReader:
    """
    Convenience function to get ConfigReader singleton instance.

    Returns:
        ConfigReader: The singleton configuration reader instance

    Example:
        >>> from utilities.config_reader import get_config
        >>> config = get_config()
        >>> browser = config.get_property('browser.type')
    """
    return ConfigReader()


# Example usage and validation (for documentation purposes)
if __name__ == "__main__":
    """
    Module self-test demonstrating configuration reader functionality.
    Run this module directly to validate configuration setup.
    """
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    try:
        # Initialize configuration reader
        config = ConfigReader()
        print(f"✓ ConfigReader initialized: {config}")

        # Test retrieving all properties
        all_props = config.get_all_properties()
        print(f"✓ Loaded configuration with {len(all_props)} top-level keys")

        # Test default value
        test_value = config.get_property('nonexistent.key', default='default_value')
        print(f"✓ Default value handling works: {test_value}")

        # Test singleton pattern
        config2 = ConfigReader()
        assert config is config2, "Singleton pattern failed!"
        print("✓ Singleton pattern verified")

        print("\n✓ All configuration reader tests passed!")

    except FileNotFoundError as err:
        print(f"✗ Configuration file not found: {err}")
        print("  Ensure config/config.yaml exists in project root")

    except ConfigurationError as err:
        print(f"✗ Configuration error: {err}")

    except Exception as exc:
        print(f"✗ Unexpected error: {exc}")
        logger.exception("Configuration reader self-test failed")
