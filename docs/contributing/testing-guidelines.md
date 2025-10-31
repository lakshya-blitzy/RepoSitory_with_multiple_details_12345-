# Testing Guidelines

Comprehensive testing guidelines for contributors to the Testinium QA Python test automation framework. This guide covers pytest-based unit testing practices, mocking patterns, coverage requirements, and best practices for testing the framework itself.

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Test Structure and Organization](#test-structure-and-organization)
- [pytest Fixtures](#pytest-fixtures)
- [Mocking Patterns](#mocking-patterns)
- [Thread-Safety Testing](#thread-safety-testing)
- [Test Parametrization](#test-parametrization)
- [Coverage Requirements](#coverage-requirements)
- [Test Execution Commands](#test-execution-commands)
- [Assertions and Best Practices](#assertions-and-best-practices)
- [Test Naming Conventions](#test-naming-conventions)
- [Test Documentation](#test-documentation)
- [Common Testing Patterns](#common-testing-patterns)
- [Migration Testing](#migration-testing)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Example Test Walkthrough](#example-test-walkthrough)
- [See Also](#see-also)

## Testing Philosophy

The test suite for this framework validates the Python implementation against the original Java Selenium + Cucumber framework, ensuring:

### Framework Reliability

All framework components must be thoroughly tested to ensure reliability when users depend on our utilities, page objects, and configuration management. The test suite validates:

- **WebDriver lifecycle management**: Proper initialization, reuse, and cleanup
- **Configuration loading**: YAML parsing, environment variable precedence, error handling
- **Thread-local isolation**: Ensuring each thread gets its own WebDriver instance
- **Singleton patterns**: Verifying shared state is managed correctly

### Behavioral Equivalence

Tests verify behavioral equivalence with the Java version while validating critical bug fixes:

- **Firefox driver bug fix**: Java Driver.java line 37 incorrectly used ChromeDriverManager for Firefox
- **Exception handling**: Java ConfigurationReader swallowed IOException with printStackTrace()
- **Implicit wait removal**: Java Driver.java line 34 used implicit waits (anti-pattern)
- **Security fixes**: Hardcoded credentials removed in favor of environment variables

**Source:** `tests/__init__.py:43-48`

### Comprehensive Coverage

Target 90%+ code coverage for core framework packages:

- `utilities/` - Driver management, configuration, wait helpers, screenshots
- `pages/` - Base page and all page object implementations
- `config/` - Configuration dataclasses and readers

**Source:** `pyproject.toml:174-183`

## Test Structure and Organization

### pytest Discovery Patterns

Tests must follow pytest naming conventions for automatic discovery:

```python
# Test files must match these patterns
test_*.py
*_test.py

# Test classes must start with 'Test'
class TestDriverManager:
    pass

# Test functions must start with 'test_'
def test_get_driver_chrome():
    pass
```

**Configuration:** `pytest.ini:14-20`

### Test Module Organization

**One test module per source module pattern:**

| Source Module | Test Module | Purpose |
|---------------|-------------|---------|
| `utilities/driver_manager.py` | `tests/test_driver_manager.py` | Tests WebDriver lifecycle, thread safety, browser initialization |
| `utilities/config_reader.py` | `tests/test_config.py` | Tests YAML parsing, env vars, error handling |

**Source:** `tests/__init__.py:16-19`

### Test Class Organization by Behavior

Organize tests into classes grouped by behavior or feature area:

```python
class TestDriverManagerCore:
    """Tests for core driver initialization functionality."""
    def test_get_driver_chrome(self):
        pass
    
    def test_get_driver_firefox(self):
        pass


class TestDriverManagerThreadSafety:
    """Tests for thread-local isolation and parallel execution."""
    def test_thread_local_isolation(self):
        pass
    
    def test_concurrent_thread_execution(self):
        pass


class TestDriverManagerEdgeCases:
    """Tests for error handling and edge cases."""
    def test_unsupported_browser_raises_error(self):
        pass
    
    def test_driver_initialization_failure(self):
        pass
```

**Example:** `tests/test_driver_manager.py:140-147`

**Benefits:**
- Clear test organization and navigation
- Isolated setup/teardown per behavior group
- Easy to run specific test groups: `pytest tests/test_driver_manager.py::TestDriverManagerThreadSafety -v`

## pytest Fixtures

Fixtures provide reusable test setup and teardown logic. Use fixtures for:

- Creating temporary test files
- Mocking external dependencies
- Resetting singleton state
- Cleaning up resources

### Autouse Cleanup Fixture

The `cleanup_driver_after_test` fixture automatically runs after every test to prevent driver leaks:

```python
@pytest.fixture(autouse=True)
def cleanup_driver_after_test():
    """
    Pytest fixture to ensure driver cleanup after each test.
    
    Automatically runs after every test to prevent driver leaks
    and ensure clean state for next test. Uses autouse=True to
    apply to all tests without explicit declaration.
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
```

**Source:** `tests/test_driver_manager.py:62-86`

**Key Points:**
- `autouse=True` applies to all tests without explicit declaration
- Yields control to test, then cleans up in `finally` block equivalent
- Prevents driver leaks between tests
- Ensures clean state for each test

### Parametrized Fixtures

Use parametrized fixtures for testing multiple browser configurations:

```python
@pytest.fixture
def mock_config_chrome():
    """Mock ConfigReader to return Chrome browser configuration."""
    mock_config = Mock(spec=ConfigReader)
    mock_config.get_property.side_effect = lambda key, default=None: {
        'browser.type': 'chrome',
        'browser.headless': False
    }.get(key, default)
    return mock_config


@pytest.fixture
def mock_config_firefox():
    """Mock ConfigReader to return Firefox browser configuration."""
    mock_config = Mock(spec=ConfigReader)
    mock_config.get_property.side_effect = lambda key, default=None: {
        'browser.type': 'firefox',
        'browser.headless': False
    }.get(key, default)
    return mock_config


@pytest.fixture
def mock_config_headless_chrome():
    """Mock ConfigReader to return headless Chrome configuration."""
    mock_config = Mock(spec=ConfigReader)
    mock_config.get_property.side_effect = lambda key, default=None: {
        'browser.type': 'chrome',
        'browser.headless': True
    }.get(key, default)
    return mock_config
```

**Source:** `tests/test_driver_manager.py:88-134`

### Fixture Scope Management

Control fixture lifespan with `scope` parameter:

```python
@pytest.fixture(scope="function")  # Default - runs for each test
def temp_file():
    pass

@pytest.fixture(scope="module")  # Runs once per test module
def database_connection():
    pass

@pytest.fixture(scope="session")  # Runs once per pytest session
def test_environment():
    pass
```

### Fixture Composition

Fixtures can depend on other fixtures:

```python
@pytest.fixture
def reset_singleton():
    """Reset ConfigReader singleton state before and after each test."""
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
def config_with_temp_file(temp_config_file, reset_singleton):
    """Fixture that combines temp file creation with singleton reset."""
    config = ConfigReader(config_file=str(temp_config_file))
    return config
```

**Source:** `tests/test_config.py:172-196`

### Temp File Fixtures

Create temporary configuration files for isolated testing:

```python
@pytest.fixture
def temp_config_file():
    """
    Create temporary YAML configuration file for isolated testing.
    
    Yields:
        Path: Path to temporary config file
    
    Cleanup:
        Automatically deletes temporary file after test execution
    """
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
```

**Source:** `tests/test_config.py:56-110`

## Mocking Patterns

Use `unittest.mock` to isolate external dependencies and control test behavior.

### Mocking ConfigReader

Control configuration values returned during tests:

```python
from unittest.mock import Mock, patch

@patch('utilities.driver_manager.ConfigReader')
def test_something(mock_config_class):
    # Setup mock configuration
    mock_config = Mock(spec=ConfigReader)
    mock_config.get_property.side_effect = lambda key, default=None: {
        'browser.type': 'chrome',
        'browser.headless': False
    }.get(key, default)
    mock_config_class.return_value = mock_config
    
    # Now DriverManager.get_driver() will use mocked config
    driver = DriverManager.get_driver()
```

**Pattern:** Use `side_effect` with a dictionary to simulate configuration lookup.

**Source:** `tests/test_driver_manager.py:156-180`

### Mocking WebDriver Constructors

Mock `webdriver.Chrome` and `webdriver.Firefox` to avoid actual browser launches:

```python
from unittest.mock import MagicMock, patch

@patch('utilities.driver_manager.webdriver.Chrome')
@patch('utilities.driver_manager.ChromeDriverManager')
@patch('utilities.driver_manager.ConfigReader')
def test_chrome_initialization(mock_config_class, mock_chrome_manager, mock_chrome_driver):
    # Mock ChromeDriverManager.install() to return driver path
    mock_chrome_manager_instance = Mock()
    mock_chrome_manager_instance.install.return_value = '/path/to/chromedriver'
    mock_chrome_manager.return_value = mock_chrome_manager_instance
    
    # Mock Chrome WebDriver instance
    mock_driver = MagicMock()
    mock_driver.session_id = 'test-session-123'
    mock_driver.capabilities = {'browserName': 'chrome', 'browserVersion': '120.0'}
    mock_chrome_driver.return_value = mock_driver
    
    # Execute test
    driver = DriverManager.get_driver()
    
    # Verify WebDriver was created
    assert mock_chrome_driver.called
    assert driver == mock_driver
```

**Key Points:**
- Use `MagicMock()` for WebDriver instance to auto-mock all methods
- Mock `ChromeDriverManager.install()` to return fake driver path
- Verify manager and driver were called correctly

**Source:** `tests/test_driver_manager.py:153-200`

### Mocking GeckoDriverManager (Firefox)

**Critical for bug fix validation:** Ensure Firefox uses `GeckoDriverManager`, not `ChromeDriverManager`:

```python
@patch('utilities.driver_manager.webdriver.Firefox')
@patch('utilities.driver_manager.GeckoDriverManager')
@patch('utilities.driver_manager.ChromeDriverManager')  # Should NOT be called
@patch('utilities.driver_manager.ConfigReader')
def test_firefox_uses_gecko_manager(mock_config_class, mock_chrome_manager,
                                    mock_gecko_manager, mock_firefox_driver):
    # Mock GeckoDriverManager (CORRECT for Firefox)
    mock_gecko_manager_instance = Mock()
    mock_gecko_manager_instance.install.return_value = '/path/to/geckodriver'
    mock_gecko_manager.return_value = mock_gecko_manager_instance
    
    # Mock ChromeDriverManager (should NOT be called - would be the bug)
    mock_chrome_manager_instance = Mock()
    mock_chrome_manager.return_value = mock_chrome_manager_instance
    
    # Execute
    driver = DriverManager.get_driver()
    
    # CRITICAL ASSERTION: GeckoDriverManager WAS called
    mock_gecko_manager_instance.install.assert_called_once()
    
    # CRITICAL ASSERTION: ChromeDriverManager was NOT called
    assert not mock_chrome_manager_instance.install.called, \
        "CRITICAL BUG: ChromeDriverManager must NOT be called for Firefox!"
```

**This test validates the fix for Java Driver.java line 37 bug.**

**Source:** `tests/test_driver_manager.py:222-293`

### Threading-Based Test Isolation

For parallel execution tests, use `threading.Thread` with mocks:

```python
import threading

@patch('utilities.driver_manager.webdriver.Chrome')
@patch('utilities.driver_manager.ChromeDriverManager')
@patch('utilities.driver_manager.ConfigReader')
def test_thread_local_isolation(mock_config_class, mock_chrome_manager, mock_chrome_driver):
    # Create unique mock drivers for each thread
    driver_instances = []
    
    def create_unique_driver(*args, **kwargs):
        driver = MagicMock()
        driver.session_id = f'session-{len(driver_instances)}'
        driver_instances.append(driver)
        return driver
    
    mock_chrome_driver.side_effect = create_unique_driver
    
    # Storage for drivers retrieved by each thread
    thread_drivers = {}
    
    def get_driver_in_thread(thread_id):
        driver = DriverManager.get_driver()
        thread_drivers[thread_id] = driver
    
    # Create and start threads
    threads = []
    for i in range(3):
        thread = threading.Thread(target=get_driver_in_thread, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    # Verify each thread got a different driver
    assert len(set(t.session_id for t in thread_drivers.values())) == 3
```

**Source:** `tests/test_driver_manager.py:370-430`

### Proper Cleanup to Prevent Cross-Test Leakage

Always reset mocked singletons and thread-local storage:

```python
@pytest.fixture
def reset_singleton():
    """Reset ConfigReader singleton state."""
    ConfigReader._instance = None
    ConfigReader._initialized = False
    ConfigReader._config = {}
    
    yield
    
    # Cleanup after test
    ConfigReader._instance = None
    ConfigReader._initialized = False
    ConfigReader._config = {}
```

**Why this matters:** Singletons persist across tests, causing state leakage if not reset.

**Source:** `tests/test_config.py:172-196`

## Thread-Safety Testing

Validate thread-local isolation for parallel test execution.

### Concurrent Thread Execution

Test that multiple threads can safely get drivers simultaneously:

```python
import threading
import time

def test_concurrent_driver_access():
    """Test multiple threads accessing DriverManager concurrently."""
    results = {'thread1': None, 'thread2': None, 'thread3': None}
    errors = []
    
    def worker(name):
        try:
            driver = DriverManager.get_driver()
            results[name] = driver.session_id
            time.sleep(0.1)  # Simulate work
            DriverManager.quit_driver()
        except Exception as e:
            errors.append((name, e))
    
    # Start threads
    threads = [
        threading.Thread(target=worker, args=('thread1',)),
        threading.Thread(target=worker, args=('thread2',)),
        threading.Thread(target=worker, args=('thread3',)),
    ]
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Verify no errors
    assert len(errors) == 0, f"Errors occurred: {errors}"
    
    # Verify all threads got drivers (not None)
    assert all(results.values())
```

### Distinct Session ID Assertions

Verify each thread gets a unique WebDriver instance:

```python
def test_distinct_session_ids():
    """Test that each thread gets its own WebDriver with distinct session ID."""
    session_ids = {}
    
    def get_session_id(thread_id):
        driver = DriverManager.get_driver()
        session_ids[thread_id] = driver.session_id
    
    threads = []
    for i in range(5):
        thread = threading.Thread(target=get_session_id, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Verify all session IDs are unique
    unique_sessions = set(session_ids.values())
    assert len(unique_sessions) == 5, \
        f"Expected 5 unique sessions, got {len(unique_sessions)}: {session_ids}"
```

### Threading.local() Validation

Verify `threading.local()` provides proper isolation:

```python
def test_threading_local_storage():
    """Validate threading.local() provides thread-isolated storage."""
    # Main thread driver
    main_driver = DriverManager.get_driver()
    main_session = main_driver.session_id
    
    # Storage for thread driver
    thread_data = {'session': None, 'is_different': False}
    
    def check_thread_isolation():
        thread_driver = DriverManager.get_driver()
        thread_session = thread_driver.session_id
        
        thread_data['session'] = thread_session
        thread_data['is_different'] = (thread_session != main_session)
    
    # Execute in thread
    thread = threading.Thread(target=check_thread_isolation)
    thread.start()
    thread.join()
    
    # Verify thread got different driver
    assert thread_data['is_different'], \
        f"Thread session {thread_data['session']} should differ from main {main_session}"
```

### Resource Contention Testing

Test behavior under resource contention (many threads):

```python
def test_resource_contention():
    """Test driver manager under heavy concurrent load."""
    NUM_THREADS = 20
    success_count = {'value': 0}
    lock = threading.Lock()
    
    def stress_test():
        try:
            driver = DriverManager.get_driver()
            assert driver is not None
            with lock:
                success_count['value'] += 1
        except Exception:
            pass  # Count failures by omission
    
    threads = [threading.Thread(target=stress_test) for _ in range(NUM_THREADS)]
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Expect all threads to succeed
    assert success_count['value'] == NUM_THREADS
```

**Source:** `tests/test_driver_manager.py:370-450`

## Test Parametrization

Use `pytest.mark.parametrize` to run the same test with different inputs.

### Browser Type Parametrization

Test multiple browser types with one test:

```python
@pytest.mark.parametrize("browser_type", ["chrome", "firefox"])
def test_driver_initialization_multiple_browsers(browser_type):
    """Test driver initialization for multiple browser types."""
    # Mock config to return specified browser
    with patch('utilities.driver_manager.ConfigReader') as mock_config_class:
        mock_config = Mock()
        mock_config.get_property.return_value = browser_type
        mock_config_class.return_value = mock_config
        
        # Test initialization
        driver = DriverManager.get_driver()
        assert driver is not None
```

### Configuration Combinations

Test multiple configuration combinations:

```python
@pytest.mark.parametrize("headless,window_size", [
    (True, [1920, 1080]),
    (False, [1920, 1080]),
    (True, [1280, 720]),
    (False, [1280, 720]),
])
def test_browser_configurations(headless, window_size):
    """Test various browser configuration combinations."""
    # Setup and test with parameters
    pass
```

### Error Scenarios

Test multiple error conditions:

```python
@pytest.mark.parametrize("browser_type,expected_error", [
    ("safari", DriverInitializationError),
    ("edge", DriverInitializationError),
    ("opera", DriverInitializationError),
    ("unknown", DriverInitializationError),
])
def test_unsupported_browsers_raise_errors(browser_type, expected_error):
    """Test that unsupported browsers raise DriverInitializationError."""
    with pytest.raises(expected_error):
        # Mock config to return unsupported browser
        with patch('utilities.driver_manager.ConfigReader') as mock_config_class:
            mock_config = Mock()
            mock_config.get_property.return_value = browser_type
            mock_config_class.return_value = mock_config
            
            DriverManager.get_driver()
```

### Type Preservation Testing

Verify YAML type preservation:

```python
@pytest.mark.parametrize("key,expected_value,expected_type", [
    ('browser.type', 'chrome', str),
    ('browser.headless', False, bool),
    ('timeouts.implicit', 0, int),
    ('timeouts.explicit', 10, int),
    ('test_data.base_url', 'https://testinium.example.com', str),
    ('application.debug', True, bool),
])
def test_property_types_preserved(temp_config_file, reset_singleton, 
                                 key, expected_value, expected_type):
    """Test YAML type preservation for various configuration keys."""
    config = ConfigReader(config_file=str(temp_config_file))
    value = config.get_property(key)
    
    assert value == expected_value
    assert isinstance(value, expected_type)
```

**Source:** `tests/test_config.py:975-1005`

## Coverage Requirements

### Minimum Coverage Targets

The framework enforces 90%+ code coverage for core packages:

```bash
# Run tests with coverage
pytest tests/ --cov=utilities --cov=pages --cov=config --cov-report=html

# Coverage targets:
# utilities/ - 90%+
# pages/     - 90%+
# config/    - 90%+
```

**Configuration:** `pyproject.toml:174-195`

### Coverage Configuration

```toml
[tool.coverage.run]
source = ["pages", "utilities", "config"]
omit = [
    "*/tests/*",
    "*/test_*.py",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*",
]

[tool.coverage.report]
precision = 2
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

**Source:** `pyproject.toml:174-195`

### Exclude Patterns

Files and directories excluded from coverage:

- `tests/` - Test code itself not counted
- `__pycache__/` - Python bytecode cache
- `venv/`, `.venv/` - Virtual environments
- Lines with `pragma: no cover` comment
- `__repr__` methods (string representation)
- `if __name__ == "__main__":` blocks

### Coverage Reports

HTML coverage report generated in `htmlcov/` directory:

```bash
# Generate HTML report
pytest tests/ --cov=utilities --cov=pages --cov=config --cov-report=html

# Open report in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

**Terminal coverage report:**

```bash
# Quick terminal output
pytest tests/ --cov=utilities --cov=pages --cov=config --cov-report=term
```

## Test Execution Commands

### Run All Tests

Execute complete test suite with verbose output:

```bash
# Verbose output with test names
pytest tests/ -v

# Extra verbose with output capture disabled
pytest tests/ -vv -s
```

**Source:** `tests/__init__.py:22-32`

### Run Specific Test Module

Test a single module:

```bash
# Test driver manager only
pytest tests/test_driver_manager.py -v

# Test config reader only
pytest tests/test_config.py -v
```

### Run Specific Test Class

Test all methods in a test class:

```bash
# Test specific class
pytest tests/test_driver_manager.py::TestDriverManager -v

# Using node ID syntax
pytest tests/test_config.py::TestConfigReader -v
```

### Run Specific Test Method

Execute single test method:

```bash
# Specific test method
pytest tests/test_driver_manager.py::TestDriverManager::test_get_driver_chrome_default -v

# Specific test with keyword
pytest tests/ -k "test_firefox" -v
```

### Run with Coverage

Execute tests with coverage analysis:

```bash
# Coverage for utilities, pages, config
pytest tests/ --cov=utilities --cov=pages --cov=config --cov-report=html

# Coverage for single package
pytest tests/test_driver_manager.py --cov=utilities --cov-report=term
```

### Parallel Execution

Run tests in parallel using pytest-xdist:

```bash
# Auto-detect CPU cores
pytest tests/ -n auto

# Specific number of workers
pytest tests/ -n 4

# With verbose output
pytest tests/ -n auto -v
```

**Configuration:** `pytest.ini:6` (addopts includes `-n auto`)

### Run by Markers

Execute tests with specific markers:

```bash
# Run smoke tests only
pytest tests/ -m smoke -v

# Run regression tests
pytest tests/ -m regression -v

# Run login-related tests
pytest tests/ -m login -v

# Exclude slow tests
pytest tests/ -m "not slow" -v
```

**Available markers:** `pytest.ini:15-29`

### Test Discovery Pattern

Pytest discovers tests matching these patterns:

- **Files:** `test_*.py` or `*_test.py`
- **Classes:** `Test*`
- **Functions:** `test_*`

**Configuration:** `pytest.ini:9-11`

## Assertions and Best Practices

### Clear Failure Messages

Always provide descriptive assertion messages:

```python
# Bad: No context
assert driver is not None

# Good: Clear failure message
assert driver is not None, "DriverManager.get_driver() returned None"

# Better: Detailed context
assert driver is not None, \
    f"DriverManager.get_driver() returned None for browser={browser_type}"
```

### Type Checking

Verify types explicitly:

```python
# Check type and value
config_value = config.get_property('browser.type')
assert isinstance(config_value, str), \
    f"browser.type should be str, got {type(config_value)}"
assert config_value == 'chrome'
```

**Source:** `tests/test_config.py:975-1005`

### Exception Testing

Use `pytest.raises` for exception validation:

```python
# Test that exception is raised
with pytest.raises(FileNotFoundError) as exc_info:
    ConfigReader(config_file='/nonexistent/path.yaml')

# Verify exception message
assert 'config.yaml' in str(exc_info.value)

# Test specific exception attributes
with pytest.raises(DriverInitializationError) as exc_info:
    DriverManager.get_driver()
    
assert exc_info.value.browser_type == 'safari'
```

**Source:** `tests/test_config.py:198-223`, `tests/test_driver_manager.py:512-545`

### Mock Call Verification

Verify mocks were called correctly:

```python
# Verify called once
mock_chrome_driver.assert_called_once()

# Verify called with specific arguments
mock_chrome_driver.assert_called_once_with(service=mock_service)

# Verify call count
assert mock_config.get_property.call_count == 3

# Verify never called
assert not mock_chrome_manager.install.called
```

### Assertion Patterns

Common assertion patterns from test suite:

```python
# Not None assertion
assert driver is not None

# Session ID validation (non-empty string)
assert driver.session_id
assert len(driver.session_id) > 0

# Type validation
assert isinstance(driver, webdriver.Chrome)

# Collection size
assert len(results) == expected_count

# Set uniqueness
assert len(set(session_ids)) == len(session_ids), "Session IDs must be unique"

# Dictionary key presence
assert 'browser' in config_dict
assert config_dict['browser']['type'] == 'chrome'

# Boolean flags
assert driver.headless is False
assert config.debug_mode is True
```

## Test Naming Conventions

### Match Source Code Structure

Test names should mirror the source being tested:

```python
# Source: DriverManager.get_driver()
def test_get_driver_chrome_default():
    """Test get_driver() returns Chrome driver with default config."""
    pass

# Source: DriverManager.quit_driver()
def test_quit_driver_closes_browser():
    """Test quit_driver() properly closes browser instance."""
    pass

# Source: ConfigReader.get_property()
def test_get_property_returns_yaml_value():
    """Test get_property() retrieves value from YAML."""
    pass
```

### Descriptive Test Names

Include context in test name:

```python
# Bad: Vague
def test_driver():
    pass

# Good: Specific
def test_get_driver_chrome_creates_new_instance():
    pass

# Better: Very specific
def test_get_driver_chrome_with_headless_true_creates_headless_instance():
    pass
```

### Naming Pattern

**Pattern:** `test_<method>_<scenario>_<expected_outcome>`

```python
# Pattern examples
test_get_driver_firefox_returns_firefox_webdriver()
test_get_property_missing_key_raises_keyerror()
test_quit_driver_with_no_driver_does_not_raise_exception()
test_get_driver_concurrent_threads_return_different_instances()
```

## Test Documentation

### Test Docstrings

Every test must have a docstring explaining what is tested and why:

```python
def test_get_driver_firefox_uses_gecko_manager():
    """
    Test that Firefox driver uses GeckoDriverManager, not ChromeDriverManager.
    
    This test validates the critical bug fix from Java Driver.java line 37
    where Firefox incorrectly used chromedriver setup instead of geckodriver.
    
    Expected Behavior:
        - GeckoDriverManager.install() IS called
        - ChromeDriverManager.install() is NOT called
        - Firefox WebDriver instance is created successfully
    
    Regression Prevention:
        - Ensures the Java bug is not reintroduced
        - Validates correct driver manager selection
    """
    pass
```

**Source:** `tests/test_driver_manager.py:222-293`

### Module Docstrings

Test modules should document their purpose:

```python
"""
Unit tests for DriverManager utility.

Tests validate:
    - WebDriver lifecycle management (create, reuse, quit)
    - Thread-local isolation for parallel execution
    - Browser driver initialization (Chrome, Firefox)
    - Critical bug fix: Firefox using GeckoDriverManager (not ChromeDriverManager)
    - Singleton pattern correctness
    - Error handling for unsupported browsers

References:
    - Source: utilities/driver_manager.py
    - Java equivalent: Driver.java (with bug fixes applied)
"""
```

**Source:** `tests/test_driver_manager.py:1-50`

### Inline Comments

Add comments for complex test logic:

```python
def test_thread_local_isolation():
    # Create unique session IDs for each mock driver
    session_counter = {'count': 0}
    
    def create_driver_with_unique_session(*args, **kwargs):
        session_counter['count'] += 1
        driver = MagicMock()
        driver.session_id = f'session-{session_counter["count"]}'
        return driver
    
    # Each thread should get a different driver instance
    # due to threading.local() storage in DriverManager
    mock_chrome.side_effect = create_driver_with_unique_session
```

## Common Testing Patterns

### Singleton Reset Fixture

Reset singleton state between tests:

```python
@pytest.fixture
def reset_config_singleton():
    """Reset ConfigReader singleton before and after each test."""
    # Reset before test
    ConfigReader._instance = None
    ConfigReader._initialized = False
    ConfigReader._config = {}
    
    yield
    
    # Cleanup after test
    ConfigReader._instance = None
    ConfigReader._initialized = False
    ConfigReader._config = {}
```

**Why:** Singletons retain state across tests, causing flaky tests.

**Source:** `tests/test_config.py:172-196`

### Environment Variable Preservation

Preserve and restore environment variables:

```python
import os

@pytest.fixture
def preserve_env():
    """Preserve environment variables during test."""
    original_env = os.environ.copy()
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

def test_env_override(preserve_env):
    # Set test environment variable
    os.environ['BROWSER_TYPE'] = 'firefox'
    
    # Test uses modified environment
    config = ConfigReader()
    assert config.get_property('browser.type') == 'firefox'
    
    # Original environment restored automatically after test
```

### Temporary File Cleanup

Create and cleanup temporary config files:

```python
import tempfile
import yaml
from pathlib import Path

@pytest.fixture
def temp_config_file():
    """Create temporary config.yaml for testing."""
    config_data = {
        'browser': {
            'type': 'chrome',
            'headless': False
        },
        'timeouts': {
            'explicit': 10,
            'page_load': 30
        }
    }
    
    # Create temp file
    temp_dir = tempfile.mkdtemp()
    config_path = Path(temp_dir) / 'config.yaml'
    
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
    
    yield config_path
    
    # Cleanup
    config_path.unlink()
    Path(temp_dir).rmdir()
```

**Source:** `tests/test_config.py:42-70`

### WebDriver Mock Setup

Reusable pattern for mocking WebDriver:

```python
from unittest.mock import MagicMock, Mock, patch

def create_mock_driver(session_id='test-session', browser_name='chrome'):
    """Create standardized mock WebDriver instance."""
    mock_driver = MagicMock()
    mock_driver.session_id = session_id
    mock_driver.capabilities = {
        'browserName': browser_name,
        'browserVersion': '120.0'
    }
    return mock_driver

@pytest.fixture
def mock_chrome_setup():
    """Setup all mocks needed for Chrome driver testing."""
    with patch('utilities.driver_manager.webdriver.Chrome') as mock_chrome, \
         patch('utilities.driver_manager.ChromeDriverManager') as mock_manager, \
         patch('utilities.driver_manager.ConfigReader') as mock_config:
        
        # Configure mocks
        mock_manager_instance = Mock()
        mock_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_manager.return_value = mock_manager_instance
        
        mock_chrome.return_value = create_mock_driver()
        
        mock_config_instance = Mock()
        mock_config_instance.get_property.return_value = 'chrome'
        mock_config.return_value = mock_config_instance
        
        yield {
            'chrome': mock_chrome,
            'manager': mock_manager,
            'config': mock_config
        }
```

### Cleanup Fixture (autouse)

Automatic cleanup after each test:

```python
@pytest.fixture(autouse=True)
def cleanup_driver_after_test():
    """
    Automatically cleanup DriverManager after each test.
    
    Prevents driver instances from leaking between tests,
    ensuring clean state for each test execution.
    """
    yield  # Test runs here
    
    # Cleanup after test
    try:
        DriverManager.quit_driver()
    except Exception:
        pass  # Already cleaned or never created
    
    # Reset thread-local storage
    if hasattr(DriverManager._drivers, 'driver'):
        delattr(DriverManager._drivers, 'driver')
```

**Source:** `tests/test_driver_manager.py:107-131`

## Migration Testing

### Validating Java Bug Fixes

The test suite validates critical fixes from the Java-to-Python migration:

#### Firefox Driver Initialization Bug

**Java Bug (Driver.java:37):** Firefox case incorrectly called `chromedriver` setup.

**Test Validation:**

```python
def test_firefox_driver_uses_geckodriver_not_chromedriver():
    """
    CRITICAL: Test that Firefox uses GeckoDriverManager, NOT ChromeDriverManager.
    
    Original Java Bug (Driver.java line 37):
        case "firefox":
            WebDriverManager.chromedriver().setup();  // WRONG!
            driver = new FirefoxDriver();
    
    Python Fix (driver_manager.py):
        elif browser_type.lower() == "firefox":
            service = Service(GeckoDriverManager().install())  // CORRECT
            driver = webdriver.Firefox(service=service)
    """
    with patch('utilities.driver_manager.GeckoDriverManager') as mock_gecko, \
         patch('utilities.driver_manager.ChromeDriverManager') as mock_chrome:
        
        # ... mock setup ...
        
        driver = DriverManager.get_driver()
        
        # MUST use GeckoDriverManager
        mock_gecko_instance.install.assert_called_once()
        
        # MUST NOT use ChromeDriverManager
        assert not mock_chrome_instance.install.called, \
            "REGRESSION: Firefox is using ChromeDriverManager (Java bug reintroduced)!"
```

**Source:** `tests/test_driver_manager.py:222-293`

#### IOException Swallowed Bug

**Java Bug (ConfigurationReader.java):** IOException caught and swallowed with `printStackTrace()`.

**Test Validation:**

```python
def test_missing_config_file_raises_exception():
    """
    Test that missing config file raises FileNotFoundError.
    
    Original Java Bug (ConfigurationReader.java):
        try {
            FileInputStream stream = new FileInputStream("config.yaml");
        } catch (IOException e) {
            e.printStackTrace();  // WRONG! Exception swallowed
        }
    
    Python Fix:
        Raises FileNotFoundError explicitly, allowing caller to handle.
    """
    with pytest.raises(FileNotFoundError) as exc_info:
        ConfigReader(config_file='/nonexistent/config.yaml')
    
    assert 'config.yaml' in str(exc_info.value)
```

**Source:** `tests/test_config.py:198-223`

#### Security: Hardcoded Credentials

**Java Issue:** Credentials hardcoded in source code.

**Test Validation:**

```python
def test_credentials_from_environment_variables():
    """
    Test that credentials are loaded from environment variables.
    
    Security Fix:
        - No hardcoded credentials in source code
        - All credentials from environment variables
        - Fails gracefully if credentials missing
    """
    os.environ['TEST_USERNAME'] = 'test_user'
    os.environ['TEST_PASSWORD'] = 'secure_password'
    
    config = ConfigReader()
    username = config.get_property('credentials.username')
    password = config.get_property('credentials.password')
    
    assert username == 'test_user'
    assert password == 'secure_password'
    
    # Verify not hardcoded
    assert 'admin' not in username  # Common hardcoded value
    assert 'password123' not in password  # Common hardcoded value
```

### Behavioral Equivalence Testing

Ensure Python behaves the same as Java (when Java was correct):

```python
def test_implicit_wait_not_configured():
    """
    Test that implicit waits are NOT configured.
    
    Design Decision:
        - Use explicit waits only (via WaitHelpers)
        - No implicit waits (anti-pattern)
        - Matches Java framework design (when used correctly)
    """
    driver = DriverManager.get_driver()
    
    # Verify implicit wait is 0 (not configured)
    # WebDriver doesn't expose this directly, so we test behavior
    start_time = time.time()
    
    try:
        driver.find_element(By.ID, 'nonexistent-element')
    except NoSuchElementException:
        elapsed = time.time() - start_time
        
        # Should fail immediately (< 1 second), not wait 10+ seconds
        assert elapsed < 1.0, \
            f"Element lookup took {elapsed}s, suggesting implicit wait is configured"
```

## Anti-Patterns to Avoid

### Test Interdependence

**Bad:** Tests depend on execution order:

```python
# DON'T DO THIS
driver_instance = None

def test_create_driver():
    global driver_instance
    driver_instance = DriverManager.get_driver()
    assert driver_instance is not None

def test_use_driver():
    global driver_instance
    driver_instance.get('https://example.com')  # Fails if test_create_driver didn't run
```

**Good:** Each test is independent:

```python
# DO THIS
def test_create_driver():
    driver = DriverManager.get_driver()
    assert driver is not None
    DriverManager.quit_driver()

def test_use_driver():
    driver = DriverManager.get_driver()
    driver.get('https://example.com')
    DriverManager.quit_driver()
```

### Shared State Without Cleanup

**Bad:** Tests share state:

```python
# DON'T DO THIS
def test_set_config():
    config = ConfigReader()
    config._config['test_key'] = 'test_value'

def test_read_config():
    config = ConfigReader()  # Gets same instance due to singleton
    # Fails if test_set_config didn't run, or gets unexpected value
    assert 'test_key' not in config._config
```

**Good:** Reset state between tests:

```python
# DO THIS
@pytest.fixture(autouse=True)
def reset_config():
    ConfigReader._instance = None
    yield
    ConfigReader._instance = None

def test_set_config(reset_config):
    config = ConfigReader()
    config._config['test_key'] = 'test_value'

def test_read_config(reset_config):
    config = ConfigReader()
    assert 'test_key' not in config._config  # Clean state
```

### Incomplete Mocking

**Bad:** Partial mocking causes external calls:

```python
# DON'T DO THIS
@patch('utilities.driver_manager.webdriver.Chrome')
def test_driver_creation(mock_chrome):
    # ChromeDriverManager not mocked - will try to download real driver!
    driver = DriverManager.get_driver()
```

**Good:** Mock all external dependencies:

```python
# DO THIS
@patch('utilities.driver_manager.webdriver.Chrome')
@patch('utilities.driver_manager.ChromeDriverManager')
@patch('utilities.driver_manager.ConfigReader')
def test_driver_creation(mock_config, mock_manager, mock_chrome):
    # All external dependencies mocked
    driver = DriverManager.get_driver()
```

### Timing-Dependent Assertions

**Bad:** Tests depend on execution timing:

```python
# DON'T DO THIS
def test_async_operation():
    start_operation()
    time.sleep(2)  # Hope it's done in 2 seconds
    assert operation_complete()  # Flaky: might fail on slow systems
```

**Good:** Use explicit waits or polling:

```python
# DO THIS
def test_async_operation():
    start_operation()
    
    # Poll until complete or timeout
    timeout = time.time() + 10
    while time.time() < timeout:
        if operation_complete():
            break
        time.sleep(0.1)
    
    assert operation_complete(), "Operation did not complete within 10 seconds"
```

### Over-Mocking

**Bad:** Mock implementation details:

```python
# DON'T DO THIS - Too brittle
@patch('utilities.driver_manager.threading.local')
@patch('utilities.driver_manager.hasattr')
@patch('utilities.driver_manager.getattr')
def test_get_driver(mock_getattr, mock_hasattr, mock_local):
    # Testing implementation, not behavior
    pass
```

**Good:** Mock external boundaries only:

```python
# DO THIS - Test behavior
@patch('utilities.driver_manager.webdriver.Chrome')
@patch('utilities.driver_manager.ChromeDriverManager')
@patch('utilities.driver_manager.ConfigReader')
def test_get_driver(mock_config, mock_manager, mock_chrome):
    driver = DriverManager.get_driver()
    assert driver is not None  # Test public interface
```

## Example Test Walkthrough

Let's walk through a complete test from `test_driver_manager.py`:

```python
@pytest.mark.smoke
def test_get_driver_chrome_default(cleanup_driver_after_test):
    """
    Test DriverManager.get_driver() returns Chrome WebDriver with default configuration.
    
    This test validates:
        1. Driver manager correctly reads 'chrome' from configuration
        2. ChromeDriverManager is used (not GeckoDriverManager)
        3. Chrome WebDriver instance is created
        4. Driver has valid session ID
        5. Thread-local storage works correctly
    
    Configuration:
        - browser.type: chrome (from config.yaml default)
        - browser.headless: false (default)
    
    Expected Behavior:
        - ChromeDriverManager.install() called once
        - webdriver.Chrome() called with service object
        - Returned driver is not None
        - Driver has session_id attribute
    
    Source: tests/test_driver_manager.py:153-200
    """
    # === ARRANGE: Setup mocks ===
    with patch('utilities.driver_manager.webdriver.Chrome') as mock_chrome_driver, \
         patch('utilities.driver_manager.ChromeDriverManager') as mock_chrome_manager, \
         patch('utilities.driver_manager.ConfigReader') as mock_config_class:
        
        # Mock ChromeDriverManager to return fake driver path
        mock_manager_instance = Mock()
        mock_manager_instance.install.return_value = '/path/to/chromedriver'
        mock_chrome_manager.return_value = mock_manager_instance
        
        # Mock Chrome WebDriver to return fake driver instance
        mock_driver = MagicMock()
        mock_driver.session_id = 'test-session-abc123'
        mock_driver.capabilities = {'browserName': 'chrome', 'browserVersion': '120.0'}
        mock_chrome_driver.return_value = mock_driver
        
        # Mock ConfigReader to return 'chrome'
        mock_config_instance = Mock()
        mock_config_instance.get_property.side_effect = lambda key: {
            'browser.type': 'chrome',
            'browser.headless': False,
            'browser.window_size': '1920,1080'
        }.get(key)
        mock_config_class.return_value = mock_config_instance
        
        # === ACT: Execute the method under test ===
        driver = DriverManager.get_driver()
        
        # === ASSERT: Verify behavior ===
        
        # 1. Verify ChromeDriverManager was called
        mock_chrome_manager.assert_called_once()
        mock_manager_instance.install.assert_called_once()
        
        # 2. Verify Chrome WebDriver was created
        mock_chrome_driver.assert_called_once()
        
        # 3. Verify returned driver is the mock
        assert driver == mock_driver
        
        # 4. Verify driver has session ID
        assert driver.session_id == 'test-session-abc123'
        
        # 5. Verify driver is not None
        assert driver is not None, "DriverManager.get_driver() returned None"
        
        # 6. Verify configuration was read
        assert mock_config_instance.get_property.called
        assert mock_config_instance.get_property.call_count >= 1
```

**Key Elements:**

1. **Test Marker:** `@pytest.mark.smoke` - Run with `pytest -m smoke`
2. **Fixture:** `cleanup_driver_after_test` - Ensures cleanup
3. **Docstring:** Comprehensive explanation of what is tested
4. **Arrange-Act-Assert:** Clear test structure
5. **Multiple Patches:** All external dependencies mocked
6. **Mock Configuration:** `side_effect` with dictionary for config lookup
7. **Assertions:** Multiple assertions validating different aspects
8. **Clear Messages:** Assertion messages for failures

**Source:** `tests/test_driver_manager.py:153-200`

## See Also

- **[Development Setup](./development-setup.md)** - Setting up development environment
- **[Code Style Guide](./code-style-guide.md)** - Python code formatting standards
- **[Pull Request Process](./pull-request-process.md)** - Submitting contributions
- **API Reference**:
  - [DriverManager API](../api-reference/utilities/driver-manager.md)
  - [ConfigReader API](../api-reference/utilities/config-reader.md)
- **Configuration**:
  - [pytest Configuration Reference](../reference/pytest-configuration.md)
  - [Dependencies Reference](../reference/dependencies.md)

---

**Source Files:**
- `tests/__init__.py` - Test suite overview and execution commands
- `tests/test_driver_manager.py` - DriverManager unit tests with thread-safety validation
- `tests/test_config.py` - ConfigReader unit tests with temp file fixtures
- `pytest.ini` - pytest configuration with markers and discovery patterns
- `pyproject.toml` - Project dependencies and tool configurations

**Last Updated:** 2024 (Migration from Java Selenium + Cucumber framework completed)
