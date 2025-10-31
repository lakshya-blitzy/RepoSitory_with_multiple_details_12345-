# Command-Line Reference

Complete command-line reference for running tests with Behave and pytest in the Testinium QA Python test automation framework.

## Overview

This reference provides comprehensive documentation for all command-line options, flags, and usage patterns for executing tests using:

- **Behave** - Primary BDD framework for feature file execution
- **pytest** - Optional framework for unit and integration testing

**Quick Navigation:**
- [Behave Commands](#behave-commands)
- [pytest Commands](#pytest-commands)
- [Framework Selection Guide](#framework-selection-guide)
- [Report Generation](#report-generation)
- [Rerun Failed Tests](#rerun-failed-tests)
- [Environment Variables](#environment-variables)
- [Debugging Options](#debugging-options)

**Source:** `behave.ini`, `pytest.ini`, `README.md`

---

## Behave Commands

Behave is the primary BDD framework for executing Gherkin feature files with Python step definitions.

### Basic Syntax

```bash
behave [options] [features]
```

**Parameters:**
- `options` - Command-line flags and arguments
- `features` - Optional paths to specific feature files or directories (defaults to `features/` from `behave.ini`)

**Source:** `behave.ini:8`, `README.md:139-161`

### Common Behave Options

Complete reference table for frequently used Behave command-line options:

| Option | Arguments | Description | Example |
|--------|-----------|-------------|---------|
| `--tags` | `TAG_EXPRESSION` | Filter scenarios by tag | `--tags=@Login` |
| `--format`, `-f` | `FORMATTER` | Output format | `-f json` |
| `--outfile`, `-o` | `FILE_PATH` | Output file path | `-o reports/cucumber.json` |
| `--no-capture` | None | Disable stdout/stderr capture (for debugging) | `--no-capture` |
| `--junit` | None | Generate JUnit XML reports | `--junit` |
| `--junit-directory` | `DIR_PATH` | JUnit XML output directory | `--junit-directory reports/junit` |
| `--dry-run` | None | Validate steps without execution | `--dry-run` |
| `--verbose` | None | Verbose output with detailed information | `--verbose` |
| `--quiet` | None | Minimal output | `--quiet` |
| `--no-summary` | None | Suppress test summary | `--no-summary` |
| `--no-timings` | None | Disable execution timing display | `--no-timings` |
| `--color` | None | Force colorized output | `--color` |
| `--no-color` | None | Disable colorized output | `--no-color` |
| `--define`, `-D` | `KEY=VALUE` | Define user data variables | `-D browser=firefox` |
| `--exclude` | `PATTERN` | Exclude features matching pattern | `--exclude WIP` |
| `--include` | `PATTERN` | Include only features matching pattern | `--include Login` |
| `--logging-level` | `LEVEL` | Set logging level | `--logging-level DEBUG` |
| `--processes` | `NUM` | Parallel processes (requires behave-parallel) | `--processes 4` |
| `--parallel-element` | `ELEMENT` | Parallelism granularity | `--parallel-element scenario` |

**Source:** `behave.ini:14-76`, `README.md:139-161`

### Tag Filtering

Execute scenarios based on tags defined in feature files.

**Single Tag:**
```bash
# Run all scenarios tagged with @Login
behave --tags=@Login
```

**Multiple Tags (OR Condition):**
```bash
# Run scenarios tagged with @Login OR @Logout
behave --tags=@Login,@Logout
```

**Multiple Tags (AND Condition):**
```bash
# Run scenarios tagged with BOTH @Smoke AND @SalesManager
behave --tags=@Smoke --tags=@SalesManager
```

**Tag Negation (NOT):**
```bash
# Run all scenarios EXCEPT those tagged @WIP
behave --tags='not @WIP'

# Alternative syntax
behave --tags=~@WIP
```

**Complex Tag Expressions:**
```bash
# (@Login OR @Logout) AND (NOT @WIP)
behave --tags=@Login,@Logout --tags='not @WIP'

# @Smoke AND (@SalesManager OR @PosManager)
behave --tags=@Smoke --tags='@SalesManager,@PosManager'
```

**Source:** `behave.ini:59-62, 138-143`, `README.md:147-158`

### Output Formats

Behave supports multiple output formatters for different reporting needs.

**Pretty Format (Default):**
```bash
# Human-readable colorized output
behave --format=pretty
# or simply
behave
```

**JSON Format:**
```bash
# Generate JSON report for integration with tools
behave --format=json --outfile=reports/cucumber.json
```

**Plain Text Format:**
```bash
# Simple text output without colors
behave --format=plain
```

**Progress Format:**
```bash
# Minimal progress indicator (dots)
behave --format=progress
```

**Allure Format:**
```bash
# Generate Allure report results
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results

# View Allure report
allure serve reports/allure-results
```

**HTML Format:**
```bash
# Generate standalone HTML report
behave --format=behave_html_formatter:HTMLFormatter --outfile=reports/report.html
```

**Multiple Formats Simultaneously:**
```bash
# JSON + Pretty output
behave -f json -o reports/cucumber.json -f pretty

# Allure + Pretty output
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results -f pretty

# HTML + JSON + Pretty output
behave -f behave_html_formatter:HTMLFormatter -o reports/report.html -f json -o reports/cucumber.json -f pretty
```

**Source:** `behave.ini:14-25, 145-148`, `README.md:163-178`

### Feature File Selection

Execute specific features, scenarios, or directories.

**Run All Features (Default):**
```bash
# Runs all features in features/ directory
behave
```

**Run Specific Feature File:**
```bash
# Run single feature file
behave features/Login.feature

# Run multiple feature files
behave features/Login.feature features/Logout.feature
```

**Run Specific Scenario by Line Number:**
```bash
# Run scenario starting at line 15
behave features/Login.feature:15

# Run multiple scenarios by line numbers
behave features/Login.feature:15 features/Login.feature:30
```

**Run Features from Specific Directory:**
```bash
# Run all features in a subdirectory
behave features/authentication/

# Run features from multiple directories
behave features/authentication/ features/crm/
```

**Source:** `behave.ini:6-8, 136-137, 150-151`, `README.md:149-151`

### JUnit XML Reports

Generate JUnit XML reports for CI/CD integration with Jenkins, GitLab CI, Azure DevOps.

**Enable JUnit Reports:**
```bash
# Generate JUnit XML files
behave --junit --junit-directory reports/junit

# With specific format
behave --junit --junit-directory reports/junit --format=pretty
```

**Configuration in behave.ini:**
```ini
[behave]
junit = true
junit_directory = reports/junit
```

**Output:** Creates XML files like `reports/junit/TESTS-Login.xml` for each feature.

**Source:** `behave.ini:34-37, 173-176`, `README.md:486-491`

### Parallel Execution

Run tests in parallel for faster execution (requires additional setup).

**Option 1: behave-parallel**

```bash
# Install behave-parallel
pip install behave-parallel

# Run with 4 parallel processes (scenario-level)
behave --processes 4 --parallel-element scenario

# Run with 8 parallel processes
behave --processes 8 --parallel-element scenario

# Feature-level parallelism
behave --processes 4 --parallel-element feature
```

**Option 2: GNU Parallel**

```bash
# Tag-based parallel execution
parallel behave --tags={} ::: @Login @Logout @Calendar @Contact

# Feature-level parallelism
parallel behave {} ::: features/Login.feature features/Logout.feature features/CRM.feature
```

**Thread Safety Requirements:**
- WebDriver instances use `threading.local()` for thread isolation
- Behave context is thread-safe by default
- Page objects must not share mutable state

**Source:** `behave.ini:94-128`, `README.md:180-191`

### Dry Run (Validation)

Validate step definitions without executing tests.

**Basic Dry Run:**
```bash
# Validate all features
behave --dry-run

# Validate specific feature
behave features/Login.feature --dry-run

# Quiet dry run (no step output)
behave --dry-run --no-summary
```

**Purpose:**
- Verify all steps have matching step definitions
- Identify undefined steps
- Check Gherkin syntax errors
- No WebDriver initialization or actual test execution

**Source:** `behave.ini:64-67, 153-154`, `README.md:159-161, 698-701`

### Complete Behave Examples

**Example 1: Run All Tests with Default Configuration**
```bash
behave
```

**Example 2: Run Smoke Tests with JSON Report**
```bash
behave --tags=@Smoke --format=json --outfile=reports/cucumber.json
```

**Example 3: Run Login Tests with Verbose Output**
```bash
behave features/Login.feature --verbose --no-capture
```

**Example 4: Run Tests with Multiple Tags**
```bash
# Run SalesManager smoke tests
behave --tags=@Smoke --tags=@SalesManager

# Run Login OR Logout tests, excluding WIP
behave --tags=@Login,@Logout --tags='not @WIP'
```

**Example 5: Generate Multiple Reports**
```bash
behave --tags=@Smoke \
       --format=json --outfile=reports/cucumber.json \
       --format=behave_html_formatter:HTMLFormatter --outfile=reports/report.html \
       --junit --junit-directory reports/junit \
       --format=pretty
```

**Example 6: CI/CD Execution (Jenkins Pipeline)**
```bash
# Headless execution with all reports
behave --tags=@Smoke \
       --format=json --outfile=reports/cucumber.json \
       --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results \
       --junit --junit-directory reports/junit \
       --no-capture
```

**Example 7: Debug Single Scenario**
```bash
# Run specific scenario with debug output
behave features/Login.feature:15 --verbose --no-capture --logging-level=DEBUG
```

**Example 8: Parallel Execution**
```bash
# Run tests on 4 cores
behave --processes 4 --parallel-element scenario --tags=@Smoke
```

**Source:** `behave.ini:130-168`, `README.md:139-191`

---

## pytest Commands

pytest provides optional testing capabilities for unit and integration tests of framework components.

### Basic Syntax

```bash
pytest [options] [file_or_dir] [file_or_dir] [...]
```

**Parameters:**
- `options` - Command-line flags and arguments
- `file_or_dir` - Optional paths to test files or directories (defaults to `tests/` from `pytest.ini`)

**Source:** `pytest.ini:11`, `README.md:190-191`

### Common pytest Options

Complete reference table for frequently used pytest command-line options:

| Option | Arguments | Description | Example |
|--------|-----------|-------------|---------|
| `-v`, `--verbose` | None | Verbose output with test names | `-v` |
| `-q`, `--quiet` | None | Quiet mode with minimal output | `-q` |
| `-s` | None | Disable output capture (show print statements) | `-s` |
| `--tb` | `STYLE` | Traceback print mode | `--tb=short` |
| `-ra` | None | Show all test outcome summaries | `-ra` |
| `-x`, `--exitfirst` | None | Exit on first failure | `-x` |
| `--maxfail` | `NUM` | Exit after NUM failures | `--maxfail=3` |
| `-k` | `EXPRESSION` | Filter tests by name pattern | `-k test_login` |
| `-m` | `MARKER` | Filter tests by marker | `-m smoke` |
| `--markers` | None | List all available markers | `--markers` |
| `-n` | `NUM` | Parallel execution with NUM workers | `-n 4` |
| `-n auto` | None | Auto-detect CPU count for parallel execution | `-n auto` |
| `--dist` | `MODE` | Distribution mode for parallel execution | `--dist loadscope` |
| `--junit-xml` | `FILE_PATH` | Generate JUnit XML report | `--junit-xml=reports/junit.xml` |
| `--html` | `FILE_PATH` | Generate HTML report (requires pytest-html) | `--html=reports/report.html` |
| `--cov` | `PACKAGE` | Code coverage (requires pytest-cov) | `--cov=utilities` |
| `--lf`, `--last-failed` | None | Rerun only failed tests from last run | `--lf` |
| `--ff`, `--failed-first` | None | Run failed tests first, then others | `--ff` |
| `--pdb` | None | Start Python debugger on failures | `--pdb` |
| `--collect-only` | None | Collect tests without executing | `--collect-only` |
| `--strict-markers` | None | Raise error on undefined markers | `--strict-markers` |

**Source:** `pytest.ini:22-35`, `README.md:190-191`

### Marker Filtering

Execute tests based on custom markers defined in `pytest.ini`.

**Run Tests by Single Marker:**
```bash
# Run smoke tests
pytest -m smoke

# Run login tests
pytest -m login

# Run unit tests
pytest -m unit
```

**Multiple Markers (OR Condition):**
```bash
# Run tests marked as smoke OR regression
pytest -m "smoke or regression"

# Run login OR logout tests
pytest -m "login or logout"
```

**Multiple Markers (AND Condition):**
```bash
# Run tests marked as smoke AND login
pytest -m "smoke and login"

# Run integration tests for CRM module
pytest -m "integration and crm"
```

**Marker Negation (NOT):**
```bash
# Run all tests EXCEPT wip (work in progress)
pytest -m "not wip"

# Run all tests except slow tests
pytest -m "not slow"
```

**Complex Marker Expressions:**
```bash
# (smoke OR regression) AND (NOT slow)
pytest -m "(smoke or regression) and not slow"

# Fast integration tests only
pytest -m "fast and integration"
```

**List Available Markers:**
```bash
# Show all defined markers
pytest --markers
```

**Source:** `pytest.ini:56-77`

### Test Name Filtering

Filter tests by name pattern using `-k` option.

**Substring Match:**
```bash
# Run tests with 'login' in the name
pytest -k login

# Run tests with 'config' in the name
pytest -k config
```

**Multiple Patterns (OR):**
```bash
# Run tests matching 'login' OR 'logout'
pytest -k "login or logout"

# Run tests matching 'driver' OR 'manager'
pytest -k "driver or manager"
```

**Exclude Pattern (NOT):**
```bash
# Run all tests EXCEPT those with 'slow' in name
pytest -k "not slow"

# Run tests but exclude integration tests
pytest -k "not integration"
```

**Complex Expressions:**
```bash
# Run tests with 'login' but not 'invalid'
pytest -k "login and not invalid"

# Run config or driver tests but not slow tests
pytest -k "(config or driver) and not slow"
```

**Source:** `pytest.ini` (standard pytest functionality)

### Parallel Execution

Run tests in parallel using pytest-xdist plugin.

**Auto-Detect CPU Count:**
```bash
# Automatically use all available CPU cores
pytest -n auto

# With load balancing by module
pytest -n auto --dist loadscope
```

**Specific Number of Workers:**
```bash
# Run with 4 parallel workers
pytest -n 4

# Run with 8 parallel workers
pytest -n 8 --dist loadscope
```

**Distribution Modes:**

| Mode | Description | Best For |
|------|-------------|----------|
| `loadscope` | Group tests by module for sharing fixtures | Tests with expensive setup |
| `loadfile` | Group tests by file | Tests needing file-level isolation |
| `load` | Distribute tests evenly | Independent tests |
| `each` | Run each test in all workers | Stress testing |

**Example:**
```bash
# Load balanced by module (recommended)
pytest -n auto --dist loadscope

# Distribute by file
pytest -n 4 --dist loadfile

# Even distribution
pytest -n auto --dist load
```

**Source:** `pytest.ini:35, 104-109`, `README.md:189-191`

### JUnit XML Reports

Generate JUnit XML reports for CI/CD integration.

**Basic JUnit Report:**
```bash
# Generate JUnit XML file
pytest --junit-xml=reports/junit.xml
```

**With Verbose Output:**
```bash
# JUnit report + detailed console output
pytest -v --junit-xml=reports/junit/pytest_results.xml
```

**Configuration in pytest.ini:**
```ini
[pytest]
junit_family = xunit2
junit_suite_name = Testinium QA Python Test Suite
```

**Source:** `pytest.ini:52-54`

### HTML Reports

Generate HTML test reports using pytest-html plugin.

**Installation:**
```bash
pip install pytest-html
```

**Generate HTML Report:**
```bash
# Basic HTML report
pytest --html=reports/pytest_report.html

# Self-contained HTML report (CSS embedded)
pytest --html=reports/pytest_report.html --self-contained-html
```

**With Screenshots and Logs:**
```bash
pytest --html=reports/pytest_report.html --self-contained-html -v
```

### Code Coverage

Measure code coverage using pytest-cov plugin.

**Installation:**
```bash
pip install pytest-cov
```

**Basic Coverage:**
```bash
# Coverage for specific package
pytest --cov=utilities

# Coverage for multiple packages
pytest --cov=utilities --cov=pages --cov=config
```

**Coverage with HTML Report:**
```bash
# Generate HTML coverage report
pytest --cov=utilities --cov-report=html

# View report: open htmlcov/index.html
```

**Coverage with Terminal Report:**
```bash
# Terminal coverage report with missing lines
pytest --cov=utilities --cov-report=term-missing

# Minimum coverage threshold (fail if below 80%)
pytest --cov=utilities --cov-fail-under=80
```

### Debugging Options

Debug failing tests with enhanced output and breakpoints.

**Show Print Statements:**
```bash
# Disable output capture to see print() statements
pytest -s

# With verbose output
pytest -s -v
```

**Detailed Tracebacks:**
```bash
# Short traceback (default)
pytest --tb=short

# Long traceback with full stack traces
pytest --tb=long

# Only show one line per failure
pytest --tb=line

# No traceback
pytest --tb=no
```

**Python Debugger (pdb):**
```bash
# Drop into pdb on first failure
pytest --pdb

# Drop into pdb on all failures
pytest --pdb --maxfail=1

# Trace test execution (step through)
pytest --trace
```

**Verbose Logging:**
```bash
# Show live logging during test execution
pytest -v --log-cli-level=DEBUG

# Capture full logs to file
pytest --log-file=logs/debug.log --log-file-level=DEBUG
```

**Source:** `pytest.ini:40-50`

### Complete pytest Examples

**Example 1: Run All Tests with Default Configuration**
```bash
pytest
```

**Example 2: Run Specific Test Module**
```bash
# Run single test file
pytest tests/test_config.py

# Run specific test function
pytest tests/test_config.py::test_get_config

# Run specific test class
pytest tests/test_driver_manager.py::TestDriverManager
```

**Example 3: Run Smoke Tests in Parallel**
```bash
pytest -m smoke -n auto -v
```

**Example 4: Run Tests with Coverage**
```bash
pytest --cov=utilities --cov=pages --cov-report=html --cov-report=term-missing -v
```

**Example 5: Debug Failing Test**
```bash
pytest tests/test_driver_manager.py::test_get_driver -s -v --tb=long --pdb
```

**Example 6: Generate Multiple Reports**
```bash
pytest -v -n auto \
       --junit-xml=reports/junit/pytest_results.xml \
       --html=reports/pytest_report.html \
       --self-contained-html \
       --cov=utilities \
       --cov-report=html
```

**Example 7: Run Failed Tests from Last Run**
```bash
# Rerun only failed tests
pytest --lf

# Run failed tests first, then rest
pytest --ff
```

**Example 8: CI/CD Execution**
```bash
pytest -v -n auto \
       --junit-xml=reports/junit/pytest_results.xml \
       --cov=utilities --cov=pages --cov=config \
       --cov-report=xml \
       --maxfail=5
```

**Source:** `pytest.ini`, `README.md:190-191`

---

## Framework Selection Guide

Choose the appropriate testing framework based on your testing needs.

### When to Use Behave

**Use Behave for:**

1. **BDD-Style Feature Testing**
   - Gherkin feature files for business-readable scenarios
   - Collaboration between technical and non-technical stakeholders
   - Living documentation of application behavior

2. **End-to-End Workflow Testing**
   - Complete user journeys (login → navigate → perform action → verify)
   - Multi-step scenarios with Given-When-Then structure
   - Integration testing of full application workflows

3. **Acceptance Testing**
   - Verifying business requirements
   - Stakeholder demonstrations
   - Regression testing of user-facing features

**Example:**
```bash
# Run end-to-end login workflow test
behave features/Login.feature --tags=@SalesManager
```

**Source:** `README.md:1-44, 259-313`

### When to Use pytest

**Use pytest for:**

1. **Unit Testing Framework Components**
   - Testing utilities (driver_manager, config_reader, wait_helpers)
   - Testing page object methods in isolation
   - Testing helper functions and utility classes

2. **Integration Testing**
   - Testing interactions between framework components
   - Mocking WebDriver for faster tests
   - Testing configuration loading and validation

3. **Rapid Test Development**
   - Simpler syntax than Gherkin (pure Python)
   - Faster test execution for small units
   - Better debugging tools (pdb, coverage)

**Example:**
```bash
# Run unit tests for utilities
pytest tests/test_driver_manager.py -v
```

**Source:** `pytest.ini:1-6`, `README.md:720-721`

### Combined Usage

**Typical Project Structure:**

- **Behave (features/)** - Business-facing acceptance tests
- **pytest (tests/)** - Developer-facing unit and integration tests

**Example Workflow:**

```bash
# Phase 1: Run unit tests (fast feedback)
pytest tests/ -m unit -n auto

# Phase 2: Run integration tests
pytest tests/ -m integration -n auto

# Phase 3: Run BDD acceptance tests
behave --tags=@Smoke

# Phase 4: Full regression
behave --tags=@Regression
```

**Source:** `README.md:537-600`

---

## Report Generation

Comprehensive guide to generating different report formats.

### Behave Report Formats

**JSON Report (Machine-Readable):**
```bash
# Basic JSON report
behave --format=json --outfile=reports/cucumber.json

# JSON + Pretty console output
behave -f json -o reports/cucumber.json -f pretty
```

**Use Cases:** CI/CD integration, custom dashboards, test management tools

**HTML Report (Human-Readable):**
```bash
# Standalone HTML report
behave --format=behave_html_formatter:HTMLFormatter --outfile=reports/behave_report.html

# Requires: pip install behave-html-formatter
```

**Use Cases:** Stakeholder sharing, archived test results, offline viewing

**JUnit XML Report (CI/CD Integration):**
```bash
# Generate JUnit XML files
behave --junit --junit-directory reports/junit

# Combined with other formats
behave --junit --junit-directory reports/junit -f pretty
```

**Use Cases:** Jenkins, GitLab CI, Azure DevOps, GitHub Actions

**Allure Report (Enhanced Reporting):**
```bash
# Generate Allure results
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Serve interactive Allure report
allure serve reports/allure-results

# Generate static Allure report
allure generate reports/allure-results --output reports/allure-report --clean

# Requires: pip install allure-behave
```

**Use Cases:** Rich HTML reports with history, screenshots, test categorization

**Source:** `behave.ini:14-25, 145-162`, `README.md:467-504`

### pytest Report Formats

**JUnit XML Report:**
```bash
# Generate JUnit XML
pytest --junit-xml=reports/junit/pytest_results.xml
```

**HTML Report:**
```bash
# Generate HTML report (requires pytest-html)
pytest --html=reports/pytest_report.html --self-contained-html
```

**Coverage Report:**
```bash
# HTML coverage report
pytest --cov=utilities --cov-report=html

# Terminal coverage report
pytest --cov=utilities --cov-report=term-missing

# XML coverage report (for SonarQube, Codecov)
pytest --cov=utilities --cov-report=xml
```

**Combined Reports:**
```bash
pytest -v \
       --junit-xml=reports/junit/pytest_results.xml \
       --html=reports/pytest_report.html \
       --self-contained-html \
       --cov=utilities --cov=pages \
       --cov-report=html \
       --cov-report=xml
```

### Multi-Format Report Generation

**Behave: Generate All Report Types**

```bash
behave --tags=@Smoke \
       -f json -o reports/cucumber.json \
       -f behave_html_formatter:HTMLFormatter -o reports/behave_report.html \
       -f allure_behave.formatter:AllureFormatter -o reports/allure-results \
       --junit --junit-directory reports/junit \
       -f pretty
```

**pytest: Generate All Report Types**

```bash
pytest -v -n auto \
       --junit-xml=reports/junit/pytest_results.xml \
       --html=reports/pytest_report.html \
       --self-contained-html \
       --cov=utilities --cov=pages --cov=config \
       --cov-report=html:reports/coverage_html \
       --cov-report=xml:reports/coverage.xml \
       --cov-report=term-missing
```

**Source:** `README.md:467-515`

---

## Rerun Failed Tests

Execute only failed tests from previous runs for faster debugging.

### Behave: Rerun Failed Scenarios

**Configuration:**
```ini
[behave.userdata]
rerun_file = reports/rerun.txt
```

**Usage:**

```bash
# Step 1: Run tests (failures saved to rerun.txt automatically)
behave

# Step 2: Rerun only failed scenarios
behave @reports/rerun.txt

# Step 3: Rerun with verbose output for debugging
behave @reports/rerun.txt --verbose --no-capture
```

**Manual Rerun File:**
```bash
# Specify custom rerun file location
behave --format=rerun --outfile=reports/custom_rerun.txt

# Rerun from custom file
behave @reports/custom_rerun.txt
```

**Source:** `behave.ini:88-92, 156-157`, `README.md:506-514`

### pytest: Rerun Failed Tests

**Built-in Failed Test Rerun:**

```bash
# Step 1: Run all tests
pytest

# Step 2: Rerun only failed tests from last run
pytest --lf
# or
pytest --last-failed

# Step 3: Run failed tests first, then rest of suite
pytest --ff
# or
pytest --failed-first
```

**pytest-rerunfailures Plugin:**

```bash
# Install plugin
pip install pytest-rerunfailures

# Rerun failed tests up to 3 times
pytest --reruns 3

# Rerun with 2-second delay between attempts
pytest --reruns 3 --reruns-delay 2

# Rerun only specific test
pytest tests/test_flaky.py --reruns 5
```

**Source:** `pytest.ini` (standard pytest functionality)

### Combined Approach

**CI/CD Pipeline Example:**

```bash
#!/bin/bash

# Run full test suite
behave || true

# If failures occurred, rerun failed tests once more
if [ -f reports/rerun.txt ]; then
    echo "Rerunning failed scenarios..."
    behave @reports/rerun.txt
fi
```

---

## Environment Variables

Override configuration settings using environment variables.

### Behave Environment Variables

Behave automatically recognizes environment variables prefixed with `BEHAVE_`.

**Naming Convention:**
```
BEHAVE_<OPTION_NAME>
```

Option names are converted to uppercase and underscores replace hyphens.

**Common Environment Variables:**

| Configuration Option | Environment Variable | Example Value |
|---------------------|---------------------|---------------|
| `format` | `BEHAVE_FORMAT` | `json` |
| `tags` | `BEHAVE_TAGS` | `@Smoke` |
| `paths` | `BEHAVE_PATHS` | `features/Login.feature` |
| `junit` | `BEHAVE_JUNIT` | `true` |
| `junit_directory` | `BEHAVE_JUNIT_DIRECTORY` | `reports/junit` |
| `show_timings` | `BEHAVE_SHOW_TIMINGS` | `true` |
| `logging_level` | `BEHAVE_LOGGING_LEVEL` | `DEBUG` |
| `dry_run` | `BEHAVE_DRY_RUN` | `true` |
| `color` | `BEHAVE_COLOR` | `false` |

**Usage Examples:**

```bash
# Override format
export BEHAVE_FORMAT="json"
behave

# Override tags
export BEHAVE_TAGS="@Login"
behave

# Override multiple options
export BEHAVE_TAGS="@Smoke"
export BEHAVE_FORMAT="json"
export BEHAVE_JUNIT="true"
export BEHAVE_JUNIT_DIRECTORY="reports/junit"
behave

# One-line override
BEHAVE_TAGS="@Login" BEHAVE_FORMAT="pretty" behave
```

**Source:** `behave.ini:188-199`

### pytest Environment Variables

pytest supports environment variables for configuration.

**Common pytest Environment Variables:**

| Configuration | Environment Variable | Example Value |
|--------------|---------------------|---------------|
| pytest options | `PYTEST_ADDOPTS` | `-v -n auto` |
| Current working directory | `PYTEST_CURRENT_TEST` | (Auto-set by pytest) |

**Usage Examples:**

```bash
# Add default options via environment
export PYTEST_ADDOPTS="-v -n auto --tb=short"
pytest

# Override markers
export PYTEST_ADDOPTS="-m smoke"
pytest

# One-line override
PYTEST_ADDOPTS="-v -m login" pytest
```

### Application Environment Variables

Override application configuration using environment variables (loaded via `python-dotenv`).

**Common Application Variables:**

```bash
# Browser configuration
export BROWSER_TYPE="firefox"
export HEADLESS="true"

# Test environment
export BASE_URL="https://staging.testinium.example.com"

# Timeouts
export TIMEOUT_EXPLICIT="20"
export TIMEOUT_PAGE_LOAD="60"

# Credentials (NEVER commit these!)
export TEST_USERNAME="testuser@example.com"
export TEST_PASSWORD="secure_password_here"

# Screenshot configuration
export SCREENSHOTS_ON_FAILURE="true"
export SCREENSHOT_DIR="reports/screenshots"
```

**CI/CD Example:**

```bash
# Jenkins/GitHub Actions/GitLab CI
export BROWSER_TYPE="chrome"
export HEADLESS="true"
export BASE_URL="https://staging.testinium.example.com"
export BEHAVE_TAGS="@Smoke"
export BEHAVE_FORMAT="json"
export BEHAVE_JUNIT="true"

# Run tests with overridden configuration
behave
```

**Source:** `.env.example`, `README.md:107-120`

---

## Debugging Options

Comprehensive debugging options for troubleshooting test failures.

### Behave Debugging

**Verbose Output:**
```bash
# Detailed step execution information
behave --verbose

# Even more verbose with step definitions
behave --verbose --format=plain
```

**Disable Output Capture:**
```bash
# See print() statements immediately
behave --no-capture

# Disable all capture (stdout, stderr, logging)
behave --no-capture --no-logcapture
```

**Debug Logging:**
```bash
# Set logging level to DEBUG
behave --logging-level=DEBUG

# With no capture for immediate output
behave --logging-level=DEBUG --no-capture

# Custom logging format
behave --logging-level=DEBUG --logging-format='%(levelname)s: %(message)s'
```

**Run Specific Scenario for Debugging:**
```bash
# Run single scenario by line number
behave features/Login.feature:15 --verbose --no-capture

# With debug logging
behave features/Login.feature:15 --verbose --no-capture --logging-level=DEBUG
```

**Dry Run to Check Steps:**
```bash
# Validate step definitions
behave --dry-run

# Check specific feature
behave features/Login.feature --dry-run --verbose
```

**Stop on First Failure:**
```bash
# Stop immediately after first failure (use Ctrl+C or --stop)
behave --stop
```

**Source:** `behave.ini:45-57, 164-165`, `README.md:686-715`

### pytest Debugging

**Verbose Output:**
```bash
# Show test names
pytest -v

# Very verbose (show full test names and docstrings)
pytest -vv

# Show setup and teardown
pytest -v --setup-show
```

**Disable Output Capture:**
```bash
# Show print() statements
pytest -s

# With verbose output
pytest -s -v
```

**Traceback Modes:**
```bash
# Short traceback (default, recommended)
pytest --tb=short

# Long traceback (full stack traces)
pytest --tb=long

# Only show one line per failure
pytest --tb=line

# Native Python traceback
pytest --tb=native

# No traceback
pytest --tb=no
```

**Python Debugger (pdb):**
```bash
# Drop into pdb on first failure
pytest --pdb

# Drop into pdb on first failure, then exit
pytest --pdb --maxfail=1

# Trace execution (step through every test)
pytest --trace
```

**Debug Logging:**
```bash
# Enable live logging with INFO level
pytest --log-cli-level=INFO

# Enable live logging with DEBUG level
pytest --log-cli-level=DEBUG -s

# Full log to file
pytest --log-file=logs/debug.log --log-file-level=DEBUG
```

**Collect Only (No Execution):**
```bash
# See which tests would run without executing
pytest --collect-only

# With verbose output
pytest --collect-only -v
```

**Stop on First Failure:**
```bash
# Exit on first failure
pytest -x
# or
pytest --exitfirst

# Exit after 3 failures
pytest --maxfail=3
```

**Source:** `pytest.ini:22-50`, `README.md:703-715`

### Combined Debugging Workflow

**Step 1: Identify Failing Tests**

```bash
# Run tests with minimal output
behave -q

# Or with pytest
pytest -q
```

**Step 2: Rerun Failed Tests with Verbose Output**

```bash
# Behave: Rerun failed with verbose output
behave @reports/rerun.txt --verbose --no-capture

# pytest: Rerun failed with verbose output
pytest --lf -v -s
```

**Step 3: Debug Specific Test**

```bash
# Behave: Debug single scenario
behave features/Login.feature:15 --verbose --no-capture --logging-level=DEBUG

# pytest: Debug with pdb
pytest tests/test_login.py::test_valid_login -s -v --pdb
```

**Step 4: Capture Browser Logs**

```python
# In environment.py after_scenario hook or pytest fixture
def after_scenario(context, scenario):
    if scenario.status == 'failed':
        # Capture browser console logs
        logs = context.driver.get_log('browser')
        for entry in logs:
            print(f"{entry['level']}: {entry['message']}")
```

---

## Quick Reference

### Most Common Commands

**Behave:**

```bash
# Run all tests
behave

# Run smoke tests
behave --tags=@Smoke

# Run specific feature
behave features/Login.feature

# Debug failing test
behave --no-capture --verbose

# Generate reports
behave -f json -o reports/cucumber.json --junit --junit-directory reports/junit -f pretty

# Rerun failed tests
behave @reports/rerun.txt
```

**pytest:**

```bash
# Run all tests
pytest

# Run smoke tests
pytest -m smoke

# Run with coverage
pytest --cov=utilities -v

# Debug failing test
pytest -s -v --pdb

# Parallel execution
pytest -n auto

# Rerun failed tests
pytest --lf
```

### Command Equivalents

| Purpose | Behave | pytest |
|---------|--------|--------|
| Run all tests | `behave` | `pytest` |
| Verbose output | `behave --verbose` | `pytest -v` |
| Disable capture | `behave --no-capture` | `pytest -s` |
| Filter tests | `behave --tags=@Smoke` | `pytest -m smoke` |
| Parallel execution | `behave --processes 4` | `pytest -n 4` |
| Generate JUnit XML | `behave --junit --junit-directory reports/junit` | `pytest --junit-xml=reports/junit.xml` |
| Dry run | `behave --dry-run` | `pytest --collect-only` |
| Rerun failed | `behave @reports/rerun.txt` | `pytest --lf` |
| Debug output | `behave --verbose --no-capture` | `pytest -v -s --pdb` |

---

## See Also

- **[Behave Configuration Reference](behave-configuration.md)** - Complete behave.ini configuration guide
- **[pytest Configuration Reference](pytest-configuration.md)** - Complete pytest.ini configuration guide
- **[Configuration Options Reference](configuration-options.md)** - config.yaml settings
- **[Environment Variables Reference](environment-variables.md)** - All environment variable options
- **[Parallel Execution Guide](../guides/parallel-execution.md)** - Detailed parallel execution setup
- **[Report Generation Guide](../deployment/report-publishing.md)** - Advanced report publishing
- **[Troubleshooting](../troubleshooting/common-errors.md)** - Common command-line issues

---

**Documentation Version:** 1.0.0  
**Last Updated:** 2024-01-15  
**Framework Versions:**  
- Behave: 1.2.6+  
- pytest: 7.0+  
- Python: 3.9+

**Source Files:**  
- `behave.ini:1-200`  
- `pytest.ini:1-131`  
- `README.md:139-715`
