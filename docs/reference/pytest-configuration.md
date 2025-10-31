# pytest Configuration Reference

## Overview

The **pytest.ini** configuration file provides optional pytest framework integration that complements the primary Behave BDD framework. This configuration was introduced as part of the Java JUnit to Python pytest migration, allowing the framework to support both Behave (for BDD-style feature testing) and pytest (for unit and integration testing of framework components).

**Purpose:**
- Enable pytest-based unit testing for framework utilities, page objects, and helper modules
- Provide parallel test execution capabilities via pytest-xdist
- Configure test discovery, logging, and reporting for pytest test runs
- Support selective test execution using custom markers
- Integrate with CI/CD systems via JUnit XML reporting

**When to Use pytest:**
- Unit testing framework components (utilities, helpers, configuration)
- Integration testing of page objects and step definitions
- Rapid test development with simpler syntax than Gherkin
- Parallel execution of component tests

**When to Use Behave:**
- BDD-style acceptance testing with Gherkin feature files
- Business-readable test scenarios
- End-to-end workflow testing
- Collaboration between technical and non-technical stakeholders

**Source:** `pytest.ini`

---

## pytest.ini File Structure

The pytest.ini file is located at the project root and contains the following sections:

```ini
[pytest]
# Core pytest configuration
minversion = 7.0
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = -ra -q --strict-markers --tb=short -v -n auto

# Console and file logging
log_cli = true
log_cli_level = INFO
log_file = logs/pytest_execution.log
log_file_level = DEBUG

# Test markers for categorization
markers =
    smoke: Smoke test cases
    regression: Regression suite
    # ... (see full marker list below)

# Warning filters
filterwarnings =
    ignore::DeprecationWarning
```

---

## Core Configuration Options

### [pytest] Section

Complete reference table for all pytest configuration options:

| Option | Type | Default | Description | Example |
|--------|------|---------|-------------|---------|
| `minversion` | string | None | Minimum pytest version required | `7.0` |
| `testpaths` | string/list | Current directory | Directories to search for tests | `tests` |
| `python_files` | string/list | `test_*.py *_test.py` | File patterns for test discovery | `test_*.py *_test.py` |
| `python_classes` | string/list | `Test` | Class patterns for test discovery | `Test*` |
| `python_functions` | string/list | `test` | Function patterns for test discovery | `test_*` |
| `addopts` | string | Empty | Default command-line options | `-ra -q --strict-markers` |
| `console_output_style` | string | `classic` | Console output format | `progress` or `classic` |
| `junit_family` | string | `xunit1` | JUnit XML report format | `xunit2` |
| `junit_suite_name` | string | pytest | JUnit XML suite name | `Testinium QA Python Test Suite` |

**Source:** `pytest.ini:6-54`

### Minimum Version Requirement

```ini
minversion = 7.0
```

**Purpose:** Ensures the project requires pytest 7.0 or higher, which provides:
- Modern assertion introspection
- Improved plugin compatibility
- Enhanced parallel execution support
- Better error reporting

**Source:** `pytest.ini:8`

### Test Discovery Configuration

pytest automatically discovers tests based on naming patterns:

| Configuration | Value | Finds |
|---------------|-------|-------|
| `testpaths` | `tests` | All tests under `tests/` directory |
| `python_files` | `test_*.py *_test.py` | Files named `test_*.py` or `*_test.py` |
| `python_classes` | `Test*` | Classes starting with `Test` |
| `python_functions` | `test_*` | Functions starting with `test_` |

**Example Test Discovery:**
```
tests/
├── test_config.py           # ✓ Discovered (matches test_*.py)
├── test_driver_manager.py   # ✓ Discovered (matches test_*.py)
├── utils_test.py            # ✓ Discovered (matches *_test.py)
└── helper.py                # ✗ Not discovered (no match)
```

**Source:** `pytest.ini:11-20`

### Default Command-Line Options (addopts)

The `addopts` setting provides default options for every pytest execution:

```ini
addopts = 
    -ra
    -q
    --strict-markers
    --tb=short
    -v
    -n auto
```

**Option Breakdown:**

| Option | Purpose | Effect |
|--------|---------|--------|
| `-ra` | Show all test outcomes | Displays summary of passed, failed, skipped, xfailed, xpassed tests |
| `-q` | Quiet mode | Reduces verbose output (overridden by `-v` for balanced output) |
| `--strict-markers` | Strict marker validation | Raises error if undefined marker is used (prevents typos) |
| `--tb=short` | Short traceback | Shows concise error tracebacks instead of full stack traces |
| `-v` | Verbose output | Displays individual test names as they run |
| `-n auto` | Parallel execution | Auto-detects CPU count and runs tests in parallel (requires pytest-xdist) |

**Usage Example:**
```bash
# These options are applied automatically
pytest tests/

# Equivalent to manually typing:
pytest tests/ -ra -q --strict-markers --tb=short -v -n auto

# Override defaults if needed
pytest tests/ --tb=long  # Use long traceback instead of short
```

**Source:** `pytest.ini:22-35`

### Console Output Style

```ini
console_output_style = progress
```

**Options:**
- `progress`: Shows progress bar with test count (modern, clean)
- `classic`: Shows traditional pytest output with dots

**Example Output (progress):**
```
tests/test_config.py::test_get_config PASSED                      [ 33%]
tests/test_config.py::test_reset_config PASSED                    [ 66%]
tests/test_driver_manager.py::test_get_driver_chrome PASSED      [100%]
```

**Source:** `pytest.ini:38`

---

## Logging Configuration

pytest provides comprehensive logging capabilities for both console and file output.

### Console Logging

**Configuration:**
```ini
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S
```

**Options Explained:**

| Option | Value | Purpose |
|--------|-------|---------|
| `log_cli` | `true` | Enable live logging to console during test execution |
| `log_cli_level` | `INFO` | Minimum log level for console output (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `log_cli_format` | Custom format | Log message format with timestamp, level, and message |
| `log_cli_date_format` | `%Y-%m-%d %H:%M:%S` | Timestamp format for log entries |

**Example Console Output:**
```
2024-01-15 14:23:45 [    INFO] Initializing WebDriver for chrome
2024-01-15 14:23:46 [    INFO] WebDriver successfully created
2024-01-15 14:23:47 [ WARNING] Element not found, retrying...
2024-01-15 14:23:48 [    INFO] Element found after retry
```

**Source:** `pytest.ini:40-44`

### File Logging

**Configuration:**
```ini
log_file = logs/pytest_execution.log
log_file_level = DEBUG
log_file_format = %(asctime)s [%(levelname)8s] [%(filename)s:%(lineno)d] %(message)s
log_file_date_format = %Y-%m-%d %H:%M:%S
```

**Options Explained:**

| Option | Value | Purpose |
|--------|-------|---------|
| `log_file` | `logs/pytest_execution.log` | Path to log file (created automatically) |
| `log_file_level` | `DEBUG` | Minimum log level for file output (captures more detail than console) |
| `log_file_format` | Extended format | Includes filename and line number for debugging |
| `log_file_date_format` | `%Y-%m-%d %H:%M:%S` | Timestamp format for log file entries |

**Key Differences from Console Logging:**
- **More Verbose:** File logging uses DEBUG level (console uses INFO)
- **More Context:** Includes filename and line number in file logs
- **Persistent:** Logs are saved for later analysis
- **Location:** Logs directory must exist or be created

**Example File Log Entry:**
```
2024-01-15 14:23:45 [   DEBUG] [driver_manager.py:132] Checking for existing WebDriver in thread-local storage
2024-01-15 14:23:45 [    INFO] [driver_manager.py:145] Initializing WebDriver for chrome
2024-01-15 14:23:46 [   DEBUG] [driver_manager.py:158] Setting ChromeOptions: headless=False
2024-01-15 14:23:46 [    INFO] [driver_manager.py:175] WebDriver successfully created
```

**Creating Logs Directory:**
```bash
# Ensure logs directory exists before running tests
mkdir -p logs
```

**Source:** `pytest.ini:46-50`

---

## JUnit XML Configuration

For CI/CD integration (Jenkins, GitLab CI, GitHub Actions), pytest can generate JUnit XML reports.

**Configuration:**
```ini
junit_family = xunit2
junit_suite_name = Testinium QA Python Test Suite
```

**Options:**

| Option | Value | Purpose |
|--------|-------|---------|
| `junit_family` | `xunit2` | JUnit XML format version (xunit2 is recommended modern format) |
| `junit_suite_name` | Custom name | Suite name appearing in JUnit reports and CI dashboards |

**Generating JUnit XML:**
```bash
# Generate JUnit XML report
pytest tests/ --junit-xml=reports/pytest_results.xml

# Jenkins will automatically pick up reports/pytest_results.xml
```

**Example JUnit XML Output:**
```xml
<testsuite name="Testinium QA Python Test Suite" tests="10" failures="1" errors="0" skipped="2">
    <testcase classname="tests.test_config" name="test_get_config" time="0.245">
        <passed/>
    </testcase>
    <testcase classname="tests.test_driver_manager" name="test_get_driver_chrome" time="2.134">
        <failure message="AssertionError: Expected chrome, got firefox">...</failure>
    </testcase>
</testsuite>
```

**Source:** `pytest.ini:52-54`

---

## Test Markers

pytest markers enable selective test execution and categorization. All markers correspond to Behave/Cucumber tags from the original Java implementation.

### Complete Marker Reference

**Configuration:**
```ini
markers =
    smoke: Smoke test cases for critical functionality
    regression: Comprehensive regression test suite
    login: Login functionality tests (@Login tag equivalent)
    logout: Logout functionality tests (@Logout tag equivalent)
    calendar: Calendar module tests
    contact: Contact management tests
    crm: CRM module tests
    employee: Employee management tests
    inventory: Inventory management tests
    notes: Notes module tests
    sales: Sales module tests
    session: Session management tests
    sales_manager: Tests requiring Sales Manager role (@SalesManager tag equivalent)
    pos_manager: Tests requiring POS Manager role (@PosManager tag equivalent)
    slow: Tests that take significant time to execute
    fast: Quick-running tests suitable for pre-commit hooks
    integration: Integration tests requiring external dependencies
    unit: Unit tests for framework components
    wip: Work in progress tests (excluded from default runs)
```

**Source:** `pytest.ini:56-77`

### Marker Categories

#### Feature-Based Markers

Correspond to feature modules in the application:

| Marker | Cucumber Equivalent | Purpose | Example Test |
|--------|---------------------|---------|--------------|
| `login` | `@Login` | Login functionality | `test_successful_login` |
| `logout` | `@Logout` | Logout functionality | `test_logout_clears_session` |
| `calendar` | `@Calendar` | Calendar management | `test_create_calendar_event` |
| `contact` | `@Contact` | Contact management | `test_add_new_contact` |
| `crm` | `@CRM` | CRM workflows | `test_create_crm_opportunity` |
| `employee` | `@Employee` | Employee management | `test_add_employee` |
| `inventory` | `@Inventory` | Inventory operations | `test_update_stock_levels` |
| `notes` | `@Notes` | Notes functionality | `test_create_note` |
| `sales` | `@Sales` | Sales workflows | `test_create_sales_order` |
| `session` | `@Session` | Session management | `test_session_timeout` |

#### Test Suite Markers

Organize tests by execution strategy:

| Marker | Purpose | When to Use |
|--------|---------|-------------|
| `smoke` | Critical path tests | Pre-deployment validation, quick health checks |
| `regression` | Comprehensive test suite | Full regression before releases |
| `fast` | Quick-running tests (<5s) | Pre-commit hooks, rapid feedback |
| `slow` | Long-running tests (>30s) | Nightly builds, not for every commit |

#### Test Type Markers

Categorize by test scope:

| Marker | Purpose | Dependencies |
|--------|---------|--------------|
| `unit` | Unit tests for framework components | None (uses mocks) |
| `integration` | Integration tests | Requires external services (database, API, browser) |

#### Role-Based Markers

Tests requiring specific user roles:

| Marker | Cucumber Equivalent | Required Role |
|--------|---------------------|---------------|
| `sales_manager` | `@SalesManager` | Sales Manager role with elevated permissions |
| `pos_manager` | `@PosManager` | POS Manager role for retail operations |

#### Development Markers

| Marker | Purpose | Default Behavior |
|--------|---------|------------------|
| `wip` | Work in progress | Excluded from default test runs |

**Source:** `pytest.ini:58-77`

### Using Markers in Tests

**Apply Markers to Test Functions:**
```python
import pytest

@pytest.mark.smoke
@pytest.mark.login
def test_successful_login():
    """Smoke test for successful login workflow"""
    # Test implementation
    pass

@pytest.mark.fast
@pytest.mark.unit
def test_config_validation():
    """Fast unit test for configuration validation"""
    # Test implementation
    pass

@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.crm
def test_end_to_end_crm_workflow():
    """Slow integration test for complete CRM workflow"""
    # Test implementation
    pass

@pytest.mark.wip
def test_new_feature_under_development():
    """Test for feature still being developed"""
    # Test implementation
    pass
```

**Apply Markers to Test Classes:**
```python
import pytest

@pytest.mark.login
class TestLoginFunctionality:
    """All tests in this class are marked with 'login'"""
    
    @pytest.mark.smoke
    def test_valid_credentials(self):
        """Also marked as smoke test"""
        pass
    
    def test_invalid_credentials(self):
        """Only marked with login (from class)"""
        pass
```

### Selective Test Execution with Markers

**Run tests with specific marker:**
```bash
# Run only smoke tests
pytest -m smoke

# Run only login tests
pytest -m login

# Run fast unit tests
pytest -m "fast and unit"
```

**Combine markers with boolean logic:**
```bash
# Run smoke OR regression tests
pytest -m "smoke or regression"

# Run login tests that are NOT work in progress
pytest -m "login and not wip"

# Run fast tests excluding wip
pytest -m "fast and not wip"

# Run smoke tests for login OR logout
pytest -m "smoke and (login or logout)"
```

**Exclude markers:**
```bash
# Run all tests except slow ones
pytest -m "not slow"

# Run all tests except wip and slow
pytest -m "not wip and not slow"

# Run integration tests but skip slow ones
pytest -m "integration and not slow"
```

**Marker Expressions Reference:**

| Expression | Meaning | Example |
|------------|---------|---------|
| `pytest -m marker1` | Tests with marker1 | `pytest -m smoke` |
| `pytest -m "marker1 or marker2"` | Tests with marker1 OR marker2 | `pytest -m "smoke or regression"` |
| `pytest -m "marker1 and marker2"` | Tests with BOTH markers | `pytest -m "login and smoke"` |
| `pytest -m "not marker1"` | Tests WITHOUT marker1 | `pytest -m "not wip"` |
| `pytest -m "(marker1 or marker2) and not marker3"` | Complex logic | `pytest -m "(smoke or fast) and not slow"` |

**List all available markers:**
```bash
# Show all registered markers with descriptions
pytest --markers
```

**Expected output:**
```
@pytest.mark.smoke: Smoke test cases for critical functionality
@pytest.mark.regression: Comprehensive regression test suite
@pytest.mark.login: Login functionality tests (@Login tag equivalent)
@pytest.mark.logout: Logout functionality tests (@Logout tag equivalent)
...
```

**Source:** `pytest.ini:56-77`

---

## Warning Filters

pytest can filter warnings from dependencies to reduce noise in test output.

**Configuration:**
```ini
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
    ignore:.*urllib3.*:DeprecationWarning
    ignore:.*selenium.*:DeprecationWarning
```

**Filter Syntax:**
```
action:message:category:module:line
```

**Common Actions:**
- `ignore`: Suppress the warning entirely
- `default`: Print warning on first occurrence
- `error`: Turn warning into an exception
- `always`: Always print warning
- `module`: Print warning once per module
- `once`: Print warning only once

**Example Filters:**

| Filter | Purpose |
|--------|---------|
| `ignore::DeprecationWarning` | Suppress all deprecation warnings |
| `ignore::PendingDeprecationWarning` | Suppress pending deprecation warnings |
| `ignore:.*urllib3.*:DeprecationWarning` | Suppress urllib3-specific deprecation warnings |
| `ignore:.*selenium.*:DeprecationWarning` | Suppress Selenium-specific deprecation warnings |

**Why Filter Warnings:**
- Third-party dependencies often raise deprecation warnings that are not actionable
- Reduces noise in test output
- Focuses attention on actual test failures
- Framework users cannot fix warnings in dependencies

**View Suppressed Warnings:**
```bash
# Show all warnings including suppressed ones
pytest -W default
```

**Source:** `pytest.ini:79-85`

---

## Parallel Execution with pytest-xdist

The framework is configured for parallel test execution using pytest-xdist plugin.

### Configuration

**In pytest.ini addopts:**
```ini
addopts = -n auto
```

**Installation:**
```bash
pip install pytest-xdist
```

**Source:** `pytest.ini:104-109`

### Parallel Execution Options

**Auto-detect CPU count (recommended):**
```bash
pytest -n auto
```

**Specify number of workers:**
```bash
# Use 4 worker processes
pytest -n 4

# Use 8 worker processes for large test suites
pytest -n 8
```

**Disable parallel execution:**
```bash
# Run tests serially (override default -n auto)
pytest -n 0
```

### Distribution Strategies

**Load-based distribution (default):**
```bash
pytest -n auto --dist load
```
- Distributes tests evenly across workers
- Best for tests of similar duration

**Scope-based distribution:**
```bash
pytest -n auto --dist loadscope
```
- Groups tests by module for better resource sharing
- Recommended when tests share expensive setup (e.g., WebDriver initialization)

**Module-based distribution:**
```bash
pytest -n auto --dist loadfile
```
- Each worker processes entire test files
- Useful for tests with module-level fixtures

**No distribution (each worker runs all tests):**
```bash
pytest -n auto --dist no
```

### Parallel Execution Best Practices

**Early Exit on Failure:**
```bash
# Stop after first failure (useful for debugging)
pytest -n auto --maxfail=1

# Stop after 3 failures
pytest -n auto --maxfail=3
```

**Thread-Safe Implementation:**

The framework uses `threading.local()` for WebDriver management to ensure thread safety:

```python
# From utilities/driver_manager.py
class DriverManager:
    _drivers = threading.local()  # Thread-local storage
    
    def get_driver(self):
        """Get thread-local WebDriver instance"""
        if not hasattr(self._drivers, 'driver'):
            self._drivers.driver = self._create_driver()
        return self._drivers.driver
```

**Parallel Execution Limitations:**
- Tests must be independent (no shared state)
- Each worker gets separate WebDriver instance
- Database tests may need isolation (transactions, separate test databases)
- File I/O should use unique file names per test

**See also:** [Parallel Execution Guide](../guides/parallel-execution.md)

**Source:** `pytest.ini:104-109`, `README.md:180-191`

---

## Optional Plugins Configuration

pytest has a rich plugin ecosystem. Common plugins for test automation frameworks:

### pytest-timeout

**Purpose:** Prevent tests from hanging indefinitely

**Configuration (commented out in pytest.ini):**
```ini
# Uncomment to enable
timeout = 300           # 5 minutes per test
timeout_method = thread # thread or signal
```

**Usage:**
```bash
pip install pytest-timeout

# Override default timeout for specific test run
pytest --timeout=60
```

**Per-Test Timeout:**
```python
import pytest

@pytest.mark.timeout(10)  # 10 seconds timeout
def test_quick_operation():
    pass

@pytest.mark.timeout(300)  # 5 minutes timeout
def test_long_operation():
    pass
```

**Source:** `pytest.ini:111-113`

### pytest-randomly

**Purpose:** Randomize test execution order to detect test dependencies

**Configuration (commented out in pytest.ini):**
```ini
# Uncomment to enable
randomly_seed = 12345                # Fixed seed for reproducibility
randomly_dont_shuffle_modules = True # Keep modules in order, shuffle within
```

**Usage:**
```bash
pip install pytest-randomly

# Tests will run in random order
pytest

# Use specific seed for reproducibility
pytest --randomly-seed=12345

# Disable randomization for single run
pytest -p no:randomly
```

**Source:** `pytest.ini:115-117`

### pytest-cov

**Purpose:** Measure code coverage during test execution

**Configuration (commented out in pytest.ini):**
```ini
# [coverage:run]
# source = pages,utilities,features/steps  # Packages to measure
# omit = 
#     */tests/*
#     */venv/*
#     */__pycache__/*
# 
# [coverage:report]
# precision = 2         # Decimal places for percentages
# show_missing = True   # Show line numbers of missing coverage
# skip_covered = False  # Include fully covered files
# 
# [coverage:html]
# directory = reports/coverage_html  # HTML report location
```

**Usage:**
```bash
pip install pytest-cov

# Run tests with coverage
pytest --cov=utilities --cov=pages --cov=features/steps

# Generate HTML coverage report
pytest --cov=utilities --cov=pages --cov-report=html

# Coverage report will be in htmlcov/index.html
```

**Terminal Coverage Report:**
```
----------- coverage: platform linux, python 3.11.5 -----------
Name                                Stmts   Miss  Cover
-------------------------------------------------------
utilities/__init__.py                  12      0   100%
utilities/config_reader.py             45      3    93%
utilities/driver_manager.py            78      5    94%
utilities/screenshot_helper.py         34      8    76%
utilities/wait_helpers.py              56      2    96%
-------------------------------------------------------
TOTAL                                 225     18    92%
```

**Source:** `pytest.ini:87-103`

---

## Test Discovery Patterns

pytest automatically discovers tests based on configured patterns.

### How pytest Finds Tests

**1. Search Paths:**
```ini
testpaths = tests
```
pytest recursively searches the `tests/` directory.

**2. File Patterns:**
```ini
python_files = test_*.py *_test.py
```
Files must match `test_*.py` OR `*_test.py`

**3. Class Patterns:**
```ini
python_classes = Test*
```
Test classes must start with `Test`

**4. Function Patterns:**
```ini
python_functions = test_*
```
Test functions/methods must start with `test_`

**Source:** `pytest.ini:11-20`

### Discovery Examples

**✓ Discovered Tests:**

```python
# tests/test_config.py
def test_get_config():           # ✓ Matches test_*
    pass

class TestConfigReader:          # ✓ Matches Test*
    def test_read_yaml(self):    # ✓ Matches test_*
        pass

# tests/driver_test.py
def test_create_driver():        # ✓ Matches test_*
    pass
```

**✗ Not Discovered:**

```python
# tests/helper.py                # ✗ Doesn't match test_*.py or *_test.py
def test_something():
    pass

# tests/test_config.py
def validate_config():           # ✗ Doesn't start with test_
    pass

class ConfigTest:                # ✗ Doesn't start with Test
    def test_load(self):
        pass

class TestConfig:
    def validate(self):          # ✗ Doesn't start with test_
        pass
```

### Custom Discovery

**Override default patterns:**
```bash
# Discover tests in different directory
pytest src/

# Use custom file pattern
pytest --pyargs mypackage

# Discover specific file
pytest tests/test_login.py

# Discover specific test
pytest tests/test_login.py::test_valid_credentials
```

**Dry run to see discovered tests:**
```bash
# Show all tests that would be collected (without running)
pytest --collect-only

# Show tests with specific marker
pytest -m smoke --collect-only
```

**Example output:**
```
<Module tests/test_config.py>
  <Function test_get_config>
  <Function test_reset_config>
  <Class TestConfigReader>
    <Function test_read_yaml>
    <Function test_get_property>
<Module tests/test_driver_manager.py>
  <Function test_get_driver_chrome>
  <Function test_quit_driver>
```

---

## Complete Configuration Example

Here's a complete pytest.ini with all commonly used options:

```ini
[pytest]
# Minimum version requirement
minversion = 7.0

# Test discovery
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Default command-line options
addopts = 
    -ra                    # Show all test outcomes
    -q                     # Quiet mode
    --strict-markers       # Error on unknown markers
    --tb=short             # Short tracebacks
    -v                     # Verbose test names
    -n auto                # Parallel execution (auto-detect CPUs)

# Console output
console_output_style = progress

# Logging - Console
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# Logging - File
log_file = logs/pytest_execution.log
log_file_level = DEBUG
log_file_format = %(asctime)s [%(levelname)8s] [%(filename)s:%(lineno)d] %(message)s
log_file_date_format = %Y-%m-%d %H:%M:%S

# JUnit XML for CI/CD
junit_family = xunit2
junit_suite_name = Testinium QA Python Test Suite

# Test markers
markers =
    smoke: Smoke test cases for critical functionality
    regression: Comprehensive regression test suite
    login: Login functionality tests
    logout: Logout functionality tests
    calendar: Calendar module tests
    contact: Contact management tests
    crm: CRM module tests
    employee: Employee management tests
    inventory: Inventory management tests
    notes: Notes module tests
    sales: Sales module tests
    session: Session management tests
    sales_manager: Tests requiring Sales Manager role
    pos_manager: Tests requiring POS Manager role
    slow: Tests that take significant time to execute
    fast: Quick-running tests suitable for pre-commit hooks
    integration: Integration tests requiring external dependencies
    unit: Unit tests for framework components
    wip: Work in progress tests (excluded from default runs)

# Warning filters
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
    ignore:.*urllib3.*:DeprecationWarning
    ignore:.*selenium.*:DeprecationWarning
```

**Source:** `pytest.ini`

---

## Common pytest Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `pytest` | Run all tests | `pytest` |
| `pytest tests/` | Run tests in directory | `pytest tests/` |
| `pytest tests/test_config.py` | Run specific file | `pytest tests/test_config.py` |
| `pytest tests/test_config.py::test_get_config` | Run specific test | `pytest tests/test_config.py::test_get_config` |
| `pytest -m marker` | Run tests with marker | `pytest -m smoke` |
| `pytest -k expression` | Run tests matching expression | `pytest -k "config or driver"` |
| `pytest -v` | Verbose output | `pytest -v` |
| `pytest -s` | Show print statements | `pytest -s` |
| `pytest -x` | Stop on first failure | `pytest -x` |
| `pytest --maxfail=N` | Stop after N failures | `pytest --maxfail=3` |
| `pytest --lf` | Run last failed tests | `pytest --lf` |
| `pytest --ff` | Run failures first | `pytest --ff` |
| `pytest --collect-only` | Show discovered tests | `pytest --collect-only` |
| `pytest --markers` | List all markers | `pytest --markers` |
| `pytest -n auto` | Parallel execution | `pytest -n auto` |
| `pytest --cov=package` | Run with coverage | `pytest --cov=utilities` |
| `pytest --junit-xml=path` | Generate JUnit XML | `pytest --junit-xml=reports/results.xml` |

**See also:** [Command Reference](command-reference.md) (when available)

---

## Marker Usage Examples

### Smoke Testing

**Run critical path tests only:**
```bash
pytest -m smoke
```

**Run smoke tests for login:**
```bash
pytest -m "smoke and login"
```

### Regression Testing

**Run full regression suite:**
```bash
pytest -m regression
```

**Run regression excluding slow tests:**
```bash
pytest -m "regression and not slow"
```

### Fast Feedback Loop

**Run fast tests only (pre-commit hook):**
```bash
pytest -m fast
```

**Run fast unit tests:**
```bash
pytest -m "fast and unit"
```

### Feature-Specific Testing

**Run all login tests:**
```bash
pytest -m login
```

**Run CRM integration tests:**
```bash
pytest -m "crm and integration"
```

### Role-Based Testing

**Run tests for Sales Manager role:**
```bash
pytest -m sales_manager
```

**Run tests for POS Manager role:**
```bash
pytest -m pos_manager
```

### Development Workflow

**Run all tests except work in progress:**
```bash
pytest -m "not wip"
```

**Run only work in progress tests:**
```bash
pytest -m wip
```

### Complex Marker Combinations

**Smoke tests for login or logout:**
```bash
pytest -m "smoke and (login or logout)"
```

**Integration tests excluding slow and wip:**
```bash
pytest -m "integration and not slow and not wip"
```

**Fast smoke or regression tests:**
```bash
pytest -m "(smoke or regression) and fast"
```

---

## Troubleshooting

### Issue: Tests Not Discovered

**Symptoms:**
```
collected 0 items
```

**Causes and Solutions:**

1. **File naming doesn't match pattern:**
   - **Cause:** Test file doesn't start with `test_` or end with `_test.py`
   - **Solution:** Rename file to match pattern (e.g., `helper.py` → `test_helper.py`)

2. **Function naming doesn't match pattern:**
   - **Cause:** Test function doesn't start with `test_`
   - **Solution:** Rename function (e.g., `def validate()` → `def test_validate()`)

3. **Tests not in testpaths directory:**
   - **Cause:** Tests are outside `tests/` directory
   - **Solution:** Move tests to `tests/` or add directory to `testpaths` in pytest.ini

4. **Class naming doesn't match pattern:**
   - **Cause:** Test class doesn't start with `Test`
   - **Solution:** Rename class (e.g., `class LoginTest` → `class TestLogin`)

**Verify discovery:**
```bash
pytest --collect-only -v
```

### Issue: Unknown Marker Error

**Symptoms:**
```
PytestUnknownMarkWarning: Unknown pytest.mark.custom_marker
```

**Cause:** Using undefined marker with `--strict-markers` enabled

**Solution:**

1. **Register marker in pytest.ini:**
```ini
markers =
    custom_marker: Description of custom marker
```

2. **Or disable strict markers temporarily:**
```bash
pytest --no-strict-markers
```

### Issue: Parallel Execution Failures

**Symptoms:**
- Tests pass when run serially but fail with `-n auto`
- Intermittent failures in parallel mode
- "WebDriver is None" errors

**Causes and Solutions:**

1. **Shared state between tests:**
   - **Cause:** Tests modify global state or shared resources
   - **Solution:** Ensure test isolation, use fixtures for setup/teardown

2. **WebDriver not thread-safe:**
   - **Cause:** WebDriver instance shared across threads
   - **Solution:** Framework already uses `threading.local()` for thread safety
   - **Verify:** Check `utilities/driver_manager.py` implementation

3. **Database conflicts:**
   - **Cause:** Tests modifying same database records
   - **Solution:** Use separate test database per worker or transactions

**Debug parallel issues:**
```bash
# Run serially to confirm tests pass
pytest -n 0

# Run with 2 workers to narrow down concurrency issues
pytest -n 2

# Enable debug logging
pytest -n auto --log-cli-level=DEBUG
```

### Issue: Log File Not Created

**Symptoms:**
- No `logs/pytest_execution.log` file created
- Permission errors

**Solutions:**

1. **Create logs directory:**
```bash
mkdir -p logs
```

2. **Check file permissions:**
```bash
chmod 755 logs/
```

3. **Verify log_file path in pytest.ini:**
```ini
log_file = logs/pytest_execution.log  # Relative to project root
```

### Issue: JUnit XML Not Generated

**Symptoms:**
- No JUnit XML report created
- CI/CD not finding test results

**Solutions:**

1. **Specify output file explicitly:**
```bash
pytest --junit-xml=reports/pytest_results.xml
```

2. **Create reports directory:**
```bash
mkdir -p reports
```

3. **Verify junit_family setting:**
```ini
junit_family = xunit2  # Use modern format
```

### Issue: Coverage Plugin Not Found

**Symptoms:**
```
ERROR: usage: pytest [options] [file_or_dir] [file_or_dir] [...]
pytest: error: unrecognized arguments: --cov=utilities
```

**Cause:** pytest-cov plugin not installed

**Solution:**
```bash
pip install pytest-cov
```

### Issue: Marker Expression Syntax Error

**Symptoms:**
```
ERROR: Wrong expression passed to '-m': ...
```

**Cause:** Invalid boolean logic in marker expression

**Valid syntax:**
```bash
# ✓ Correct
pytest -m "smoke and not wip"
pytest -m "(smoke or regression) and fast"

# ✗ Incorrect
pytest -m smoke && not wip           # Wrong: shell && not pytest syntax
pytest -m "smoke, regression"        # Wrong: use 'or' not comma
```

---

## See Also

- **[Behave Configuration Reference](behave-configuration.md)** - Primary BDD framework configuration
- **[Command Reference](command-reference.md)** - Complete CLI command reference (when available)
- **[Parallel Execution Guide](../guides/parallel-execution.md)** - Detailed parallel testing guide
- **[Contributing: Testing Guidelines](../contributing/testing-guidelines.md)** - Writing tests for the framework

---

**Source Files:**
- `pytest.ini` - Complete pytest configuration
- `README.md:180-191` - pytest parallel execution examples
- `tests/` - Example pytest test implementations

---

**Last Updated:** 2024 (Auto-generated from pytest.ini)
