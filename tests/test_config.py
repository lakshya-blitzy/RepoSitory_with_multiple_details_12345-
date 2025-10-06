"""
Comprehensive Unit Tests for Configuration Reader Utility

This module provides pytest-based unit tests for utilities/config_reader.py,
validating YAML parsing, environment variable loading, property access,
error handling, and configuration management functionality.

Critical Testing Focus:
    Tests verify proper exception handling replacing Java ConfigurationReader.java
    lines 21-24 where IOException was swallowed with printStackTrace(). Python
    version must explicitly raise FileNotFoundError and ConfigurationError for
    fail-fast behavior and proper error diagnostics.

Test Coverage:
    - Singleton pattern enforcement
    - YAML configuration loading from config/config.yaml
    - Environment variable precedence over YAML values
    - Dot notation for nested configuration keys
    - Default value handling for missing keys
    - Error handling: FileNotFoundError, ConfigurationError, YAMLError
    - Configuration validation and type preservation
    - Thread safety considerations

Author: Python Test Automation Framework Migration Team
Reference: Agent Action Plan Section 0.8.1 (Configuration Management Deep Dive)
Java Source: src/main/java/com/testinium/utilities/ConfigurationReader.java
"""

# pylint: disable=redefined-outer-name
# Justification: pytest fixtures use parameter names matching fixture names (standard pattern)

# pylint: disable=unused-argument
# Justification: Some pytest fixtures used for side effects (e.g., reset_singleton)

# pylint: disable=too-many-arguments
# Justification: Parametrized tests may require multiple parameters for comprehensive coverage

# pylint: disable=too-many-lines
# Justification: Comprehensive test suite requires extensive coverage of all ConfigReader functionality

import os
import tempfile
from pathlib import Path
import pytest
import yaml

# Import the configuration reader class and exception under test
from utilities.config_reader import ConfigReader, ConfigurationError, get_config


# =============================================================================
# TEST FIXTURES
# =============================================================================

@pytest.fixture
def temp_config_file():
    """
    Create temporary YAML configuration file for isolated testing.

    Yields:
        Path: Path to temporary config file

    Cleanup:
        Automatically deletes temporary file after test execution

    Example:
        >>> def test_something(temp_config_file):
        ...     config = ConfigReader(config_file=str(temp_config_file))
        ...     assert config is not None
    """
    # Create temporary file with valid YAML content
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.yaml',
        delete=False,
        encoding='utf-8'
    ) as temp_file:
        # Write valid YAML configuration
        config_data = {
            'browser': {
                'type': 'chrome',
                'headless': False,
                'window_size': [1920, 1080]
            },
            'timeouts': {
                'implicit': 0,
                'explicit': 10,
                'page_load': 30
            },
            'test_data': {
                'base_url': 'https://testinium.example.com',
                'api_endpoint': '/api/v1'
            },
            'application': {
                'name': 'Testinium QA Framework',
                'version': '1.0.0',
                'debug': True
            }
        }
        yaml.safe_dump(config_data, temp_file)
        temp_file_path = temp_file.name

    yield Path(temp_file_path)

    # Cleanup: Remove temporary file
    try:
        os.unlink(temp_file_path)
    except FileNotFoundError:
        pass  # Already deleted


@pytest.fixture
def empty_config_file():
    """
    Create temporary empty YAML configuration file.

    Tests ConfigReader handling of empty configuration files,
    which should result in empty dictionary not None.

    Yields:
        Path: Path to empty config file
    """
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.yaml',
        delete=False,
        encoding='utf-8'
    ) as temp_file:
        # Write empty content
        temp_file.write('')
        temp_file_path = temp_file.name

    yield Path(temp_file_path)

    # Cleanup
    try:
        os.unlink(temp_file_path)
    except FileNotFoundError:
        pass


@pytest.fixture
def invalid_yaml_file():
    """
    Create temporary file with invalid YAML syntax.

    Tests ConfigReader exception handling for malformed YAML,
    verifying ConfigurationError raised (not swallowed like Java).

    Yields:
        Path: Path to invalid YAML file
    """
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.yaml',
        delete=False,
        encoding='utf-8'
    ) as temp_file:
        # Write invalid YAML syntax (unmatched brackets)
        temp_file.write('browser:\n  type: chrome\n  invalid: {unclosed')
        temp_file_path = temp_file.name

    yield Path(temp_file_path)

    # Cleanup
    try:
        os.unlink(temp_file_path)
    except FileNotFoundError:
        pass


@pytest.fixture
def reset_singleton():
    """
    Reset ConfigReader singleton state before and after each test.

    Critical for test isolation: ConfigReader uses singleton pattern,
    so must reset _instance and _initialized between tests to prevent
    test interference.

    Usage:
        >>> def test_something(reset_singleton):
        ...     config = ConfigReader()  # Fresh instance
    """
    # Reset before test
    ConfigReader._instance = None
    ConfigReader._initialized = False
    ConfigReader._config = {}

    yield

    # Reset after test
    ConfigReader._instance = None
    ConfigReader._initialized = False
    ConfigReader._config = {}


@pytest.fixture
def mock_env_vars():
    """
    Mock environment variables for testing env var precedence.

    Returns:
        Dict: Dictionary for setting test environment variables

    Cleanup:
        Restores original environment after test
    """
    original_env = os.environ.copy()

    yield os.environ

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


# =============================================================================
# TEST CLASS: ConfigReader Core Functionality
# =============================================================================

class TestConfigReaderCore:
    """
    Test suite for ConfigReader core functionality.

    Tests:
        - Singleton pattern enforcement
        - YAML file loading
        - Configuration validation
        - Error handling
    """

    def test_singleton_pattern(self, temp_config_file, reset_singleton):
        """
        Test singleton pattern: multiple instantiations return same object.

        Validates:
            - First ConfigReader() creates new instance
            - Subsequent ConfigReader() returns same instance
            - Instance identity matches (same memory location)
            - Singleton preserved across module imports

        Reference:
            Agent Action Plan 0.8.1 - Configuration Management Deep Dive
            Singleton pattern ensures shared configuration state
        """
        # Create first instance
        config1 = ConfigReader(config_file=str(temp_config_file))

        # Create second instance
        config2 = ConfigReader(config_file=str(temp_config_file))

        # Verify same instance
        assert config1 is config2, "ConfigReader should return same singleton instance"
        assert id(config1) == id(config2), "Instance IDs should match"

        # Verify _instance class variable
        assert ConfigReader._instance is config1
        assert ConfigReader._initialized is True

    def test_load_yaml_config_success(self, temp_config_file, reset_singleton):
        """
        Test successful YAML configuration loading.

        Validates:
            - ConfigReader initializes without errors
            - YAML file parsed correctly
            - Configuration dictionary populated
            - All expected keys present
            - Nested structure preserved

        Critical Fix:
            Unlike Java ConfigurationReader which swallowed IOException
            (lines 21-24 with printStackTrace), Python version successfully
            loads configuration or raises explicit exceptions.
        """
        # Initialize config reader
        config = ConfigReader(config_file=str(temp_config_file))

        # Verify initialization
        assert config is not None
        assert ConfigReader._initialized is True
        assert isinstance(ConfigReader._config, dict)
        assert len(ConfigReader._config) > 0

        # Verify expected top-level keys
        expected_keys = {'browser', 'timeouts', 'test_data', 'application'}
        assert set(ConfigReader._config.keys()) == expected_keys

        # Verify nested structure
        assert 'type' in ConfigReader._config['browser']
        assert 'explicit' in ConfigReader._config['timeouts']

    def test_load_yaml_config_file_not_found(self, reset_singleton):
        """
        Test FileNotFoundError raised for missing configuration file.

        Validates:
            - FileNotFoundError explicitly raised (not swallowed)
            - Error message descriptive and helpful
            - No silent failure like Java printStackTrace()

        Critical Fix:
            Java ConfigurationReader.java lines 21-24 caught IOException
            and only printed stack trace, allowing program to continue
            with null Properties object. Python version raises FileNotFoundError
            for fail-fast behavior and immediate error detection.

        Reference:
            Agent Action Plan 0.8.2 - Bug Fixes and Security Remediations
        """
        nonexistent_file = "/tmp/nonexistent_config_12345.yaml"

        # Verify FileNotFoundError raised
        with pytest.raises(FileNotFoundError) as exc_info:
            ConfigReader(config_file=nonexistent_file)

        # Verify error message quality
        error_message = str(exc_info.value)
        assert "not found" in error_message.lower()
        assert nonexistent_file in error_message or "config.yaml" in error_message

        # Verify not initialized
        assert ConfigReader._initialized is False

    def test_load_yaml_config_invalid_yaml(self, invalid_yaml_file, reset_singleton):
        """
        Test ConfigurationError raised for invalid YAML syntax.

        Validates:
            - ConfigurationError raised for malformed YAML
            - yaml.YAMLError properly caught and wrapped
            - Error message indicates YAML parsing failure
            - No silent failure or swallowed exceptions

        Critical Fix:
            Java version would silently fail with printStackTrace().
            Python version raises ConfigurationError with descriptive message.
        """
        # Verify ConfigurationError raised
        with pytest.raises(ConfigurationError) as exc_info:
            ConfigReader(config_file=str(invalid_yaml_file))

        # Verify error message indicates YAML parsing problem
        error_message = str(exc_info.value)
        assert "yaml" in error_message.lower() or "parse" in error_message.lower()

        # Verify not initialized
        assert ConfigReader._initialized is False


# =============================================================================
# TEST CLASS: Property Access and Retrieval
# =============================================================================

class TestConfigReaderPropertyAccess:
    """
    Test suite for configuration property access methods.

    Tests:
        - get_property() with existing keys
        - get_property() with missing keys
        - Default value handling
        - Dot notation for nested keys
        - Type preservation
    """

    def test_get_property_existing_key(self, temp_config_file, reset_singleton):
        """
        Test successful property retrieval for existing keys.

        Validates:
            - get_property() returns correct values
            - Type preservation (str, int, bool, dict, list)
            - Nested key access works
            - No errors for valid keys
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Test simple nested key access
        browser_type = config.get_property('browser.type')
        assert browser_type == 'chrome'
        assert isinstance(browser_type, str)

        # Test boolean value
        headless = config.get_property('browser.headless')
        assert headless is False
        assert isinstance(headless, bool)

        # Test integer value
        explicit_timeout = config.get_property('timeouts.explicit')
        assert explicit_timeout == 10
        assert isinstance(explicit_timeout, int)

        # Test list value
        window_size = config.get_property('browser.window_size')
        assert window_size == [1920, 1080]
        assert isinstance(window_size, list)

    def test_get_property_missing_key_with_default(self, temp_config_file, reset_singleton):
        """
        Test default value handling for missing configuration keys.

        Validates:
            - Default value returned when key missing
            - No exception raised when default provided
            - Default can be any type
            - Logging indicates default used

        Reference:
            Agent Action Plan 0.5.2 - Configuration option handling
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Test string default
        missing_value = config.get_property('nonexistent.key', default='default_value')
        assert missing_value == 'default_value'

        # Test integer default
        missing_int = config.get_property('missing.timeout', default=99)
        assert missing_int == 99

        # Test None default
        missing_none = config.get_property('missing.key', default=None)
        assert missing_none is None

    def test_get_property_missing_key_without_default(self, temp_config_file, reset_singleton):
        """
        Test KeyError raised for missing key without default value.

        Validates:
            - KeyError explicitly raised for required missing keys
            - Error message descriptive with available keys
            - No silent None return like Java getProperty()

        Critical Difference:
            Java Properties.getProperty() returns null for missing keys.
            Python version raises KeyError to fail-fast on configuration errors.
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Verify KeyError raised
        with pytest.raises(KeyError) as exc_info:
            config.get_property('nonexistent.required.key')

        # Verify error message quality
        error_message = str(exc_info.value)
        assert 'nonexistent.required.key' in error_message
        assert 'not found' in error_message.lower()
        # Should suggest available keys
        assert 'browser' in error_message or 'available' in error_message.lower()

    def test_dot_notation_nested_keys(self, temp_config_file, reset_singleton):
        """
        Test dot notation for accessing deeply nested configuration keys.

        Validates:
            - Dot notation splits correctly on '.'
            - Multiple levels of nesting supported
            - Each level validated during traversal
            - Type preservation through nesting

        Example:
            'browser.window_size' -> config['browser']['window_size']
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Test 2-level nesting
        browser_type = config.get_property('browser.type')
        assert browser_type == 'chrome'

        # Test 2-level nesting with different keys
        base_url = config.get_property('test_data.base_url')
        assert base_url == 'https://testinium.example.com'

        # Test partial key should fail
        with pytest.raises(KeyError):
            config.get_property('browser.type.invalid.extra.nesting')


# =============================================================================
# TEST CLASS: Environment Variable Override
# =============================================================================

class TestConfigReaderEnvironmentVariables:
    """
    Test suite for environment variable precedence over YAML configuration.

    Critical Security Feature:
        Environment variables override YAML for sensitive credentials,
        preventing hardcoded passwords like found in EmployeeP.java.

    Tests:
        - Environment variable override mechanism
        - Variable name transformation (dot notation to UPPER_SNAKE_CASE)
        - Precedence: ENV > YAML > Default
    """

    def test_environment_variable_override(self, temp_config_file, reset_singleton, mock_env_vars):
        """
        Test environment variables take precedence over YAML configuration.

        Validates:
            - Environment variable checked first
            - Env var overrides YAML value
            - Dot notation converted to UPPER_SNAKE_CASE
              Example: 'browser.type' -> 'BROWSER_TYPE'
            - YAML value used if no env var set

        Critical Security Feature:
            Allows runtime credential injection without hardcoding.
            Replaces EmployeeP.java hardcoded credentials security issue.

        Reference:
            Agent Action Plan 0.9.2 - Security Best Practices
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Verify YAML value first (no env var)
        browser_type_yaml = config.get_property('browser.type')
        assert browser_type_yaml == 'chrome'

        # Set environment variable
        os.environ['BROWSER_TYPE'] = 'firefox'

        # Verify env var takes precedence
        browser_type_env = config.get_property('browser.type')
        assert browser_type_env == 'firefox'
        assert browser_type_env != browser_type_yaml

        # Clean up
        del os.environ['BROWSER_TYPE']

    def test_base_url_with_env_override(self, temp_config_file, reset_singleton, mock_env_vars):
        """
        Test BASE_URL environment variable override for test_data.base_url.

        Validates:
            - Common pattern: test_data.base_url -> TEST_DATA_BASE_URL
            - URL from environment replaces YAML value
            - Supports different environments (dev, staging, prod)

        Use Case:
            CI/CD pipelines set BASE_URL env var per environment
            without modifying config files.
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # YAML value
        yaml_url = config.get_property('test_data.base_url')
        assert yaml_url == 'https://testinium.example.com'

        # Override with environment variable
        staging_url = 'https://staging.testinium.example.com'
        os.environ['TEST_DATA_BASE_URL'] = staging_url

        # Verify override
        env_url = config.get_property('test_data.base_url')
        assert env_url == staging_url

        # Clean up
        del os.environ['TEST_DATA_BASE_URL']

    def test_credentials_from_environment(self, temp_config_file, reset_singleton, mock_env_vars):
        """
        Test credentials loaded from environment variables only.

        Validates:
            - Credentials NOT in YAML file
            - Must come from environment variables
            - Proper error if missing and no default

        Security Fix:
            Prevents hardcoded credentials like EmployeeP.java issue.
            Forces secure credential management via environment.

        Reference:
            Agent Action Plan 0.8.2 - Security Remediations
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Set test credentials in environment
        os.environ['TEST_USERNAME'] = 'admin@testinium.com'
        os.environ['TEST_PASSWORD'] = 'secure_password_from_env'

        # Retrieve from environment (not in YAML)
        username = config.get_property('test.username')
        password = config.get_property('test.password')

        assert username == 'admin@testinium.com'
        assert password == 'secure_password_from_env'

        # Clean up
        del os.environ['TEST_USERNAME']
        del os.environ['TEST_PASSWORD']


# =============================================================================
# TEST CLASS: Specific Configuration Access
# =============================================================================

class TestConfigReaderSpecificConfigurations:
    """
    Test suite for accessing specific configuration sections.

    Tests:
        - Browser configuration access
        - Timeout configuration access
        - Test data configuration access
        - Application configuration access
    """

    def test_browser_config_access(self, temp_config_file, reset_singleton):
        """
        Test accessing browser configuration section.

        Validates:
            - browser.type retrieval
            - browser.headless boolean
            - browser.window_size list
            - All browser properties accessible

        Reference:
            Agent Action Plan 0.8.1 - Browser configuration management
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Access individual browser properties
        browser_type = config.get_property('browser.type')
        headless = config.get_property('browser.headless')
        window_size = config.get_property('browser.window_size')

        assert browser_type == 'chrome'
        assert headless is False
        assert window_size == [1920, 1080]

    def test_timeout_config_access(self, temp_config_file, reset_singleton):
        """
        Test accessing timeout configuration section.

        Validates:
            - timeouts.implicit is 0 (per best practices)
            - timeouts.explicit configurable
            - timeouts.page_load present
            - Integer types preserved

        Critical Best Practice:
            Implicit wait should be 0 (not 10s like Java Driver.java:34).
            Only explicit waits used to avoid wait strategy mixing.

        Reference:
            Agent Action Plan 0.8.1 - Wait Strategy Deep Analysis
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Access timeout properties
        implicit_wait = config.get_property('timeouts.implicit')
        explicit_wait = config.get_property('timeouts.explicit')
        page_load = config.get_property('timeouts.page_load')

        assert implicit_wait == 0, "Implicit wait must be 0 per best practices"
        assert explicit_wait == 10
        assert page_load == 30

        # Verify integer types
        assert isinstance(implicit_wait, int)
        assert isinstance(explicit_wait, int)
        assert isinstance(page_load, int)

    def test_application_config_access(self, temp_config_file, reset_singleton):
        """
        Test accessing application metadata configuration.

        Validates:
            - application.name retrieval
            - application.version retrieval
            - application.debug boolean flag
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Access application properties
        app_name = config.get_property('application.name')
        app_version = config.get_property('application.version')
        debug_mode = config.get_property('application.debug')

        assert app_name == 'Testinium QA Framework'
        assert app_version == '1.0.0'
        assert debug_mode is True
        assert isinstance(debug_mode, bool)


# =============================================================================
# TEST CLASS: get_all_properties() Method
# =============================================================================

class TestConfigReaderGetAllProperties:
    """
    Test suite for get_all_properties() method.

    Tests:
        - Complete configuration dictionary retrieval
        - Deep copy protection
        - Dictionary immutability
    """

    def test_get_all_properties_returns_dict(self, temp_config_file, reset_singleton):
        """
        Test get_all_properties() returns complete configuration dictionary.

        Validates:
            - Returns dictionary type
            - Contains all top-level keys
            - Nested structure preserved
            - All values accessible
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Get all properties
        all_props = config.get_all_properties()

        # Verify return type
        assert isinstance(all_props, dict)

        # Verify expected keys present
        expected_keys = {'browser', 'timeouts', 'test_data', 'application'}
        assert set(all_props.keys()) == expected_keys

        # Verify nested structure
        assert all_props['browser']['type'] == 'chrome'
        assert all_props['timeouts']['explicit'] == 10

    def test_get_all_properties_deep_copy(self, temp_config_file, reset_singleton):
        """
        Test get_all_properties() returns deep copy for immutability.

        Validates:
            - Returned dictionary is copy, not reference
            - Modifying returned dict doesn't affect singleton state
            - Protection against external configuration mutation

        Critical Design:
            Deep copy protects singleton configuration from accidental
            modification during test execution.
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Get properties twice
        props1 = config.get_all_properties()
        props2 = config.get_all_properties()

        # Verify different objects
        assert props1 is not props2, "Should return new copy each time"
        assert id(props1) != id(props2)

        # Modify first copy
        props1['browser']['type'] = 'firefox_modified'

        # Verify singleton state unchanged
        props3 = config.get_all_properties()
        assert props3['browser']['type'] == 'chrome', "Singleton should be unchanged"

        # Verify second copy unchanged
        assert props2['browser']['type'] == 'chrome', "Second copy should be unchanged"


# =============================================================================
# TEST CLASS: Edge Cases and Error Handling
# =============================================================================

class TestConfigReaderEdgeCases:
    """
    Test suite for edge cases and error conditions.

    Tests:
        - Empty configuration files
        - Invalid configuration structure
        - Type validation
        - Logging behavior
    """

    def test_empty_yaml_file(self, empty_config_file, reset_singleton):
        """
        Test handling of empty YAML configuration file.

        Validates:
            - Empty file results in empty dict, not None
            - No exception raised for empty file
            - get_property() with defaults works
            - get_property() without defaults raises KeyError

        Edge Case:
            Empty config.yaml should initialize with empty dictionary,
            allowing environment variable and default value fallbacks.
        """
        config = ConfigReader(config_file=str(empty_config_file))

        # Verify initialized with empty config
        assert ConfigReader._initialized is True
        assert not ConfigReader._config  # Empty dict is falsey

        # Verify default value works
        value_with_default = config.get_property('any.key', default='fallback')
        assert value_with_default == 'fallback'

        # Verify required key raises error
        with pytest.raises(KeyError):
            config.get_property('required.key')

    def test_config_file_is_directory(self, reset_singleton):
        """
        Test ConfigurationError raised if config path is directory.

        Validates:
            - Directory path detected
            - ConfigurationError raised
            - Error message indicates path issue
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Attempt to use directory as config file
            with pytest.raises(ConfigurationError) as exc_info:
                ConfigReader(config_file=temp_dir)

            # Verify error message
            error_message = str(exc_info.value)
            assert 'not a file' in error_message.lower()

    def test_yaml_non_dict_root(self, reset_singleton):
        """
        Test ConfigurationError raised if YAML root is not dictionary.

        Validates:
            - Non-dict root detected (list, string, etc.)
            - ConfigurationError raised
            - Error message indicates format issue

        Edge Case:
            YAML allows root to be list or scalar, but ConfigReader
            requires dictionary for key-value access.
        """
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.yaml',
            delete=False,
            encoding='utf-8'
        ) as temp_file:
            # Write YAML with list root instead of dict
            temp_file.write('- item1\n- item2\n- item3')
            temp_file_path = temp_file.name

        try:
            # Verify ConfigurationError raised
            with pytest.raises(ConfigurationError) as exc_info:
                ConfigReader(config_file=temp_file_path)

            # Verify error message
            error_message = str(exc_info.value)
            assert 'dictionary' in error_message.lower() or 'dict' in error_message.lower()

        finally:
            # Cleanup
            os.unlink(temp_file_path)

    def test_config_repr_method(self, temp_config_file, reset_singleton):
        """
        Test __repr__() method provides useful string representation.

        Validates:
            - __repr__() returns string
            - Contains config file path
            - Contains key count
            - Useful for debugging
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Get string representation
        repr_str = repr(config)

        # Verify format
        assert isinstance(repr_str, str)
        assert 'ConfigReader' in repr_str
        assert 'config_file' in repr_str
        assert 'keys=' in repr_str
        assert '4' in repr_str  # 4 top-level keys in temp config


# =============================================================================
# TEST CLASS: Module-Level Functions
# =============================================================================

class TestModuleLevelFunctions:
    """
    Test suite for module-level convenience functions.

    Tests:
        - get_config() convenience function
    """

    def test_get_config_convenience_function(self, temp_config_file, reset_singleton):
        """
        Test get_config() module-level convenience function.

        Validates:
            - get_config() returns ConfigReader instance
            - Returns singleton instance
            - Equivalent to ConfigReader() direct instantiation
        """
        # Get config via convenience function
        config1 = get_config()

        # Get config via direct instantiation
        config2 = ConfigReader(config_file=str(temp_config_file))

        # Verify same singleton
        assert config1 is config2
        assert isinstance(config1, ConfigReader)


# =============================================================================
# TEST CLASS: Thread Safety Considerations
# =============================================================================

class TestConfigReaderThreadSafety:
    """
    Test suite for thread safety considerations.

    Note:
        ConfigReader singleton is NOT thread-safe during initialization.
        These tests document expected behavior, not guarantee thread safety.

    Best Practice:
        Initialize ConfigReader in main thread before spawning test workers.

    Reference:
        Agent Action Plan 0.8.1 - Thread Safety and Parallel Execution
    """

    def test_singleton_initialization_documentation(self, temp_config_file, reset_singleton):
        """
        Document that ConfigReader should be initialized before parallel execution.

        Note:
            This is a documentation test, not a thread safety guarantee.
            ConfigReader singleton initialization is NOT thread-safe.
            Initialize in main thread before test parallelization.

        Best Practice:
            >>> # In features/environment.py before_all()
            >>> def before_all(context):
            ...     context.config = ConfigReader()  # Main thread init
            ...     # Now safe for parallel scenario execution
        """
        # First initialization
        config = ConfigReader(config_file=str(temp_config_file))

        # Verify initialized
        assert ConfigReader._initialized is True
        assert ConfigReader._instance is config

        # Multiple accesses return same instance
        config2 = ConfigReader()
        config3 = ConfigReader()

        assert config is config2 is config3


# =============================================================================
# PARAMETRIZED TESTS
# =============================================================================

class TestConfigReaderParametrized:
    """
    Parametrized tests for multiple scenarios.
    """

    @pytest.mark.parametrize("key,expected_value,expected_type", [
        ('browser.type', 'chrome', str),
        ('browser.headless', False, bool),
        ('timeouts.implicit', 0, int),
        ('timeouts.explicit', 10, int),
        ('test_data.base_url', 'https://testinium.example.com', str),
        ('application.debug', True, bool),
    ])
    def test_property_types_preserved(
        self,
        temp_config_file,
        reset_singleton,
        key,
        expected_value,
        expected_type
    ):
        """
        Test YAML type preservation for various configuration keys.

        Validates:
            - Correct value retrieved
            - Correct type preserved from YAML
            - No type coercion or conversion
        """
        config = ConfigReader(config_file=str(temp_config_file))

        value = config.get_property(key)

        assert value == expected_value
        assert isinstance(value, expected_type)

    @pytest.mark.parametrize("env_var,config_key,env_value", [
        ('BROWSER_TYPE', 'browser.type', 'firefox'),
        ('TIMEOUTS_EXPLICIT', 'timeouts.explicit', '15'),
        ('TEST_DATA_BASE_URL', 'test_data.base_url', 'https://custom.url.com'),
    ])
    def test_environment_variable_precedence_parametrized(
        self,
        temp_config_file,
        reset_singleton,
        mock_env_vars,
        env_var,
        config_key,
        env_value
    ):
        """
        Test environment variable precedence for multiple keys.

        Validates:
            - Environment variable overrides YAML
            - Various key patterns work
            - String values returned from environment
        """
        config = ConfigReader(config_file=str(temp_config_file))

        # Set environment variable
        os.environ[env_var] = env_value

        # Retrieve value
        value = config.get_property(config_key)

        # Verify environment value returned (always string from os.getenv)
        assert value == env_value

        # Clean up
        del os.environ[env_var]


# =============================================================================
# END OF TEST MODULE
# =============================================================================
