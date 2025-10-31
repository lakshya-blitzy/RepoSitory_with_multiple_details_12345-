# Behave Configuration Reference

Complete reference documentation for configuring the Behave BDD framework through `behave.ini`.

## Overview

The `behave.ini` file serves as the primary configuration file for the Behave BDD framework in this project. It replaces the Maven Surefire plugin and `CukesRunner.java` `@CucumberOptions` configuration from the original Java/Cucumber implementation.

**Purpose:**
- Centralize all Behave framework settings in one location
- Define default test execution behavior
- Configure output formats and report generation
- Set up logging and capture options
- Enable CI/CD integration through JUnit XML reports

**Location:** `behave.ini` in the project root directory

**Source:** `behave.ini:1-200`

## Configuration File Structure

The `behave.ini` file uses INI format with two main sections:

```ini
[behave]
# Main Behave framework configuration options

[behave.userdata]
# Custom user data for test execution
```

## [behave] Section Options

Complete reference table for all configuration options in the `[behave]` section:

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `paths` | string | `features/` | Feature files location (directory or specific .feature files) |
| `format` | string | `pretty` | Default output formatter (see Formatters section) |
| `outfiles` | string | - | Output file path for the specified format |
| `junit` | boolean | `false` | Enable JUnit XML report generation for CI/CD |
| `junit_directory` | string | - | Directory path for JUnit XML reports |
| `show_skipped` | boolean | `true` | Display skipped scenarios in output |
| `show_timings` | boolean | `true` | Display execution time for scenarios and steps |
| `stdout_capture` | boolean | `true` | Capture stdout during test execution |
| `stderr_capture` | boolean | `true` | Capture stderr during test execution |
| `log_capture` | boolean | `true` | Capture Python logging output |
| `logging_level` | string | `INFO` | Python logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `logging_format` | string | See below | Python logging format string |
| `logging_datefmt` | string | See below | Python logging date format string |
| `tags` | string | - | Default tag filter for test execution |
| `dry_run` | boolean | `false` | Validate step definitions without executing tests |
| `color` | boolean | `true` | Enable colorized terminal output |
| `summary` | boolean | `true` | Display detailed summary after test execution |

**Source:** `behave.ini:5-76`

### paths

Specifies the location of feature files to execute.

**Syntax:**
```ini
paths = features/
```

**Examples:**
```ini
# Single directory (all features)
paths = features/

# Multiple directories
paths = features/login
        features/crm

# Specific feature file
paths = features/Login.feature

# Multiple feature files
paths = features/Login.feature
        features/Logout.feature
```

**Java Equivalent:**
```java
// CukesRunner.java line 15
@CucumberOptions(features = "src/main/resources/features")
```

**Source:** `behave.ini:6-8`

### format

Defines the default output formatter for test execution.

**Syntax:**
```ini
format = pretty
```

**Available Formatters:**
- `pretty` - Human-readable colorized output with step details
- `json` - JSON format for integration with external tools
- `plain` - Simple text output without colors
- `progress` - Minimal progress indicator (dots)
- `allure_behave.formatter:AllureFormatter` - Allure report format
- `behave_html_formatter:HTMLFormatter` - HTML report format

**Multiple Formatters:**

Use command line for multiple formats:
```bash
behave -f json -o reports/cucumber.json -f pretty
```

**Source:** `behave.ini:14-25`

### outfiles

Specifies output file paths for the configured formatters.

**Syntax:**
```ini
outfiles = reports/output.txt
```

**Multiple Output Files:**
```bash
# Command line approach for multiple formats
behave -f json -o reports/cucumber.json -f html -o reports/report.html
```

**Source:** `behave.ini:26-32`

### junit and junit_directory

Enables JUnit XML report generation for CI/CD integration with Jenkins, Azure DevOps, and other platforms.

**Syntax:**
```ini
junit = true
junit_directory = reports/junit
```

**Purpose:**
- Jenkins test result publishing
- Trend analysis and historical tracking
- Azure DevOps test result integration
- GitLab CI test reporting

**Output:** Creates XML files in the specified directory (e.g., `reports/junit/TESTS-Login.xml`)

**Source:** `behave.ini:34-37`

### show_skipped

Controls whether skipped scenarios are displayed in output.

**Syntax:**
```ini
show_skipped = false
```

**Values:**
- `true` - Display skipped scenarios (helpful for debugging)
- `false` - Hide skipped scenarios (cleaner output)

**Source:** `behave.ini:39-42`

### show_timings

Controls whether execution time is displayed for scenarios and steps.

**Syntax:**
```ini
show_timings = true
```

**Output Example:**
```
Scenario: Users log in with valid credentials  # features/Login.feature:10
  Given User is on the Testinium login page ... passed in 2.145s
  When User enters "test@example.com" username ... passed in 0.234s
  And User enters "password" password ... passed in 0.198s
```

**Source:** `behave.ini:39-43`

### stdout_capture, stderr_capture, and log_capture

Controls output capture during test execution.

**Syntax:**
```ini
stdout_capture = false
stderr_capture = false
log_capture = true
```

**stdout_capture:**
- `true` - Captures `print()` statements (default)
- `false` - Displays `print()` statements immediately (useful for debugging)

**stderr_capture:**
- `true` - Captures error output (default)
- `false` - Displays error output immediately

**log_capture:**
- `true` - Captures Python `logging` output
- `false` - Displays logging output immediately

**Debugging Tip:** Set both stdout_capture and stderr_capture to `false` during development to see real-time output.

**Source:** `behave.ini:45-51`

### logging_level, logging_format, and logging_datefmt

Configures Python logging for test execution.

**Syntax:**
```ini
logging_level = INFO
logging_format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
logging_datefmt = %Y-%m-%d %H:%M:%S
```

**logging_level Values:**
- `DEBUG` - Detailed diagnostic information
- `INFO` - General informational messages (default)
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical error messages

**logging_format Placeholders:**
- `%(asctime)s` - Timestamp
- `%(name)s` - Logger name
- `%(levelname)s` - Log level (INFO, ERROR, etc.)
- `%(message)s` - Log message
- `%(filename)s` - Source filename
- `%(lineno)d` - Line number

**Output Example:**
```
2024-01-15 10:23:45 - utilities.driver_manager - INFO - Chrome WebDriver initialized successfully
```

**Source:** `behave.ini:53-57`

### tags

Specifies default tag filter for test execution (can be overridden via command line).

**Syntax:**
```ini
tags = @Smoke
```

**Tag Filter Examples:**
```ini
# Single tag
tags = @Login

# OR condition (comma-separated)
tags = @Login,@Logout

# AND condition (space-separated)
tags = @Smoke @SalesManager

# Negation (NOT)
tags = not @WIP
```

**Command Line Override:**
```bash
# Override default tags
behave --tags=@Login

# Multiple tag conditions
behave --tags=@Smoke --tags=@SalesManager  # AND
behave --tags=@Login,@Logout               # OR
behave --tags='not @WIP'                   # Exclude WIP tests
```

**Java Equivalent:**
```java
// CukesRunner.java line 18
@CucumberOptions(tags = "@Smoke")
```

**Source:** `behave.ini:59-62`

### dry_run

Validates step definitions without executing tests.

**Syntax:**
```ini
dry_run = false
```

**Purpose:**
- Verify all steps have matching step definitions
- Identify undefined steps
- Check Gherkin syntax
- No actual test execution or WebDriver initialization

**Usage:**
```bash
# Command line dry run
behave --dry-run

# Check specific feature
behave features/Login.feature --dry-run
```

**Output Example:**
```
Feature: Testinium app login feature
  Scenario: Users log in with valid credentials
    Given User is on the Testinium login page ... passed
    When User enters "test@example.com" username ... passed
    Then User should see the dashboard ... passed
```

**Java Equivalent:**
```java
// CukesRunner.java line 17
@CucumberOptions(dryRun = false)
```

**Source:** `behave.ini:64-67`

### color

Enables colorized terminal output for better readability.

**Syntax:**
```ini
color = true
```

**Values:**
- `true` - Colorized output (green for passed, red for failed, etc.)
- `false` - Plain text output (useful for CI/CD logs)

**Source:** `behave.ini:69-71`

### summary

Controls whether a detailed summary is displayed after test execution.

**Syntax:**
```ini
summary = true
```

**Summary Output Example:**
```
1 feature passed, 0 failed, 0 skipped
5 scenarios passed, 0 failed, 0 skipped
25 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m15.234s
```

**Source:** `behave.ini:73-75`

## [behave.userdata] Section

Custom user data section for framework-specific configurations that don't fit in standard Behave options.

**Syntax:**
```ini
[behave.userdata]
key = value
```

### allure_results_dir

Directory path for Allure report results.

**Syntax:**
```ini
allure_results_dir = reports/allure-results
```

**Usage:**
```bash
# Generate Allure results
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# Serve Allure report
allure serve reports/allure-results
```

**Java Equivalent:**
```java
// CukesRunner.java line 20
@CucumberOptions(plugin = {"me.jvt.cucumber.report.PrettyReports:target/cucumber"})
```

**Source:** `behave.ini:77-82`

### screenshot_dir

Directory path for capturing screenshots (used by `environment.py` hooks).

**Syntax:**
```ini
screenshot_dir = reports/screenshots
```

**Integration:** Used by `features/environment.py` `after_scenario` hook to capture screenshots on test failure.

**Source:** `behave.ini:84-86`

### rerun_file

File path for storing failed test scenarios for rerun.

**Syntax:**
```ini
rerun_file = reports/rerun.txt
```

**Usage:**
```bash
# Run tests (failures saved to rerun.txt)
behave

# Rerun only failed tests
behave @reports/rerun.txt
```

**Java Equivalent:**
```java
// FailedTestRunner.java reads target/rerun.txt
```

**Source:** `behave.ini:88-92`

## Output Formatters

Detailed information about available output formatters and their usage.

### Built-in Formatters

**pretty**
- **Description:** Human-readable colorized output with full step details
- **Best for:** Local development and debugging
- **Output:** Terminal only (no file output by default)

**json**
- **Description:** JSON format compatible with Cucumber JSON schema
- **Best for:** Integration with test management tools, custom dashboards
- **Output:** Requires `-o` flag to specify output file
- **Example:**
  ```bash
  behave -f json -o reports/cucumber.json
  ```

**plain**
- **Description:** Simple text output without colors
- **Best for:** CI/CD logs, file output
- **Output:** Terminal or file

**progress**
- **Description:** Minimal progress indicator (dots for passed, F for failed)
- **Best for:** Quick feedback on large test suites
- **Output:** Terminal

**Source:** `behave.ini:14-25`

### Third-Party Formatters

**allure_behave.formatter:AllureFormatter**
- **Description:** Generates Allure report format
- **Installation:** `pip install allure-behave`
- **Best for:** Rich HTML reports with history, attachments, test categorization
- **Usage:**
  ```bash
  behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results
  allure serve reports/allure-results
  ```
- **Configuration:** Requires `allure_results_dir` in `[behave.userdata]`

**behave_html_formatter:HTMLFormatter**
- **Description:** Generates standalone HTML report
- **Installation:** `pip install behave-html-formatter`
- **Best for:** Standalone HTML reports without dependencies
- **Usage:**
  ```bash
  behave -f behave_html_formatter:HTMLFormatter -o reports/report.html
  ```

**Source:** `behave.ini:22-25, 77-82`

### Multiple Formatters

Execute with multiple formatters simultaneously:

```bash
# JSON + Pretty
behave -f json -o reports/cucumber.json -f pretty

# Allure + Pretty
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results -f pretty

# HTML + JSON + Pretty
behave -f behave_html_formatter:HTMLFormatter -o reports/report.html -f json -o reports/cucumber.json -f pretty
```

**Note:** The `pretty` formatter is always useful to include for real-time terminal feedback.

**Source:** `behave.ini:145-148`

## Tag Filtering

Comprehensive guide to tag filtering syntax and usage patterns.

### Tag Syntax

Tags are defined in feature files using the `@` symbol:

```gherkin
@Login @Smoke
Feature: Testinium app login feature
  
  @UPGN-286 @SalesManager
  Scenario: SalesManager login
    Given User is on the Testinium login page
```

### Tag Filter Operations

**Single Tag:**
```bash
behave --tags=@Login
```
Executes all scenarios tagged with `@Login`.

**OR Condition (Comma-Separated):**
```bash
behave --tags=@Login,@Logout
```
Executes scenarios tagged with `@Login` OR `@Logout`.

**AND Condition (Multiple --tags Arguments):**
```bash
behave --tags=@Smoke --tags=@SalesManager
```
Executes scenarios tagged with BOTH `@Smoke` AND `@SalesManager`.

**NOT Condition (Negation):**
```bash
behave --tags='not @WIP'
```
Executes all scenarios EXCEPT those tagged with `@WIP`.

**Complex Expressions:**
```bash
# (@Login OR @Logout) AND (NOT @WIP)
behave --tags=@Login,@Logout --tags='not @WIP'

# @Smoke AND (@SalesManager OR @PosManager)
behave --tags=@Smoke --tags='@SalesManager,@PosManager'
```

### Tag Best Practices

**Feature-Level Tags:**
```gherkin
@Login
Feature: Login functionality
```
Apply to all scenarios in the feature.

**Scenario-Level Tags:**
```gherkin
@UPGN-286 @Critical
Scenario: Valid login
```
Apply to specific scenario only.

**Tag Naming Conventions:**
- `@FeatureName` - Feature category (e.g., `@Login`, `@CRM`, `@Inventory`)
- `@SmokeTest` or `@Smoke` - Critical path tests
- `@RegressionTest` - Full regression suite
- `@WIP` - Work in progress (usually excluded)
- `@JIRA-123` - Jira ticket reference (e.g., `@UPGN-286`)
- `@UserRole` - User-specific tests (e.g., `@SalesManager`, `@PosManager`)

**Source:** `behave.ini:59-62, 138-143`

## Parallel Execution Configuration

Comprehensive guide to parallel test execution options and thread-safety requirements.

### Overview

The framework supports parallel test execution for faster test suite completion. The original Java implementation used Maven Surefire with parallel execution:

```xml
<!-- Java equivalent: pom.xml -->
<parallel>methods</parallel>
<useUnlimitedThreads>true</useUnlimitedThreads>
```

**Python Equivalent Options:**
1. behave-parallel
2. pytest-bdd with pytest-xdist
3. GNU Parallel

**Source:** `behave.ini:94-128`

### Option 1: behave-parallel

**Installation:**
```bash
pip install behave-parallel
```

**Usage:**
```bash
# Run with 4 parallel processes (scenario-level parallelism)
behave --processes 4 --parallel-element scenario

# Run with 8 parallel processes
behave --processes 8 --parallel-element scenario

# Feature-level parallelism
behave --processes 4 --parallel-element feature
```

**Configuration:**
```ini
[behave.parallel]
processes = 4
parallel_element = scenario
```

**Best For:**
- Independent test scenarios
- Scenario-level isolation
- Simple parallel execution needs

**Source:** `behave.ini:103-107`

### Option 2: pytest-bdd with pytest-xdist

**Installation:**
```bash
pip install pytest-bdd pytest-xdist
```

**Usage:**
```bash
# Auto-detect CPU cores
pytest -n auto --dist loadscope

# Specific number of workers
pytest -n 4 --dist loadscope

# Feature-level distribution
pytest -n 4 --dist loadfile
```

**Best For:**
- Large test suites
- More flexible parallelism control
- Better reporting and test discovery
- Integration with pytest plugins

**Source:** `behave.ini:108-112`

### Option 3: GNU Parallel

**Usage:**
```bash
# Tag-based parallel execution
parallel behave --tags={} ::: @Login @Logout @Calendar @Contact

# Feature-level parallelism
parallel behave {} ::: features/Login.feature features/Logout.feature features/CRM.feature
```

**Best For:**
- Feature-level parallelism
- Tag-based distribution
- Simple shell-based orchestration

**Source:** `behave.ini:114-117`

### Thread Safety Requirements

**Critical:** When running tests in parallel, ensure thread safety across all components.

**WebDriver Thread-Local Storage:**
```python
# utilities/driver_manager.py uses threading.local()
class DriverManager:
    _drivers = threading.local()  # Thread-safe WebDriver instances
    
    @classmethod
    def get_driver(cls):
        if not hasattr(cls._drivers, 'driver'):
            cls._drivers.driver = cls._create_driver()
        return cls._drivers.driver
```

**Requirements:**
- **WebDriver:** Must use `threading.local()` for thread isolation
- **Behave Context:** Thread-safe by default (separate context per thread)
- **Page Objects:** Must not share mutable state between tests
- **Configuration:** Singleton pattern with immutable configuration
- **Screenshots:** Unique filenames per thread (timestamp + thread ID)

**Source:** `behave.ini:119-123`

### Parallel Execution Best Practices

1. **Isolate Test Data:** Each test should use unique test data (separate user accounts, unique identifiers)
2. **Avoid Shared State:** Tests must be completely independent
3. **Use Thread-Local WebDriver:** Always access driver through `DriverManager.get_driver()`
4. **Unique Screenshots:** Include thread ID or timestamp in screenshot filenames
5. **Database Transactions:** Use database transactions if modifying shared data
6. **Resource Limits:** Don't exceed available CPU cores and memory

## CI/CD Integration

Configuration guidance for integrating with CI/CD platforms.

### Jenkins Integration

**Pipeline Configuration:**
```groovy
pipeline {
    agent any
    
    stages {
        stage('Test') {
            steps {
                sh '''
                    # Activate virtual environment
                    source venv/bin/activate
                    
                    # Run tests with JUnit output
                    behave --junit --junit-directory reports/junit
                '''
            }
        }
    }
    
    post {
        always {
            # Publish JUnit test results
            junit 'reports/junit/*.xml'
            
            # Archive HTML reports
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            
            # Archive screenshots
            archiveArtifacts artifacts: 'reports/screenshots/*.png', allowEmptyArchive: true
        }
    }
}
```

**Required Configuration:**
```ini
[behave]
junit = true
junit_directory = reports/junit
```

**Source:** `behave.ini:170-177`

### GitHub Actions Integration

**Workflow Example:**
```yaml
name: Behave Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          behave --junit --junit-directory reports/junit
      
      - name: Publish Test Results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: reports/junit/*.xml
      
      - name: Upload Screenshots
        uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: screenshots
          path: reports/screenshots/
```

### GitLab CI Integration

**Pipeline Example:**
```yaml
test:
  stage: test
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - behave --junit --junit-directory reports/junit
  artifacts:
    when: always
    reports:
      junit: reports/junit/*.xml
    paths:
      - reports/
    expire_in: 1 week
```

### Azure DevOps Integration

**Pipeline Configuration:**
```yaml
steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'
  
- script: |
    pip install -r requirements.txt
    behave --junit --junit-directory reports/junit
  displayName: 'Run Behave Tests'

- task: PublishTestResults@2
  condition: always()
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: 'reports/junit/*.xml'
    mergeTestResults: true

- task: PublishBuildArtifacts@1
  condition: always()
  inputs:
    pathToPublish: 'reports'
    artifactName: 'test-reports'
```

**Source:** `behave.ini:183-186`

### Jira Integration

Tag scenarios with Jira ticket references:

```gherkin
@UPGN-286
Scenario: Valid login test
  Given User is on the Testinium login page
```

**Integration Options:**
- **Xray Plugin:** Sync test results with Jira Xray
- **Zephyr Plugin:** Sync test results with Jira Zephyr
- **Custom Integration:** Parse tags from JSON report and update Jira via API

**Source:** `behave.ini:179-181`

## Configuration Precedence

Understanding how configuration values are resolved when specified in multiple locations.

### Precedence Order (Highest to Lowest)

1. **Command-Line Arguments** (highest priority)
2. **Environment Variables** (`BEHAVE_*`)
3. **behave.ini Configuration File**
4. **Default Behave Settings** (lowest priority)

### Examples

**Scenario:** `behave.ini` sets `tags = @Smoke`, but you want to run `@Login` tests.

**Command Line Override:**
```bash
behave --tags=@Login
```
Result: Only `@Login` tests run (command line overrides behave.ini).

**Environment Variable Override:**
```bash
export BEHAVE_TAGS="@Login"
behave
```
Result: Only `@Login` tests run (environment variable overrides behave.ini).

### Environment Variable Mapping

Behave automatically recognizes environment variables prefixed with `BEHAVE_`:

```bash
# Override format
export BEHAVE_FORMAT="json"

# Override tags
export BEHAVE_TAGS="@Smoke"

# Override paths
export BEHAVE_PATHS="features/Login.feature"

# Override junit
export BEHAVE_JUNIT="true"
export BEHAVE_JUNIT_DIRECTORY="reports/junit"
```

**Naming Convention:**
- Environment variable: `BEHAVE_<OPTION_NAME>`
- Option name converted to uppercase
- Example: `show_timings` → `BEHAVE_SHOW_TIMINGS`

**Source:** `behave.ini:188-199`

### Configuration Debugging

**Check Effective Configuration:**
```bash
# Verbose mode shows configuration values
behave --verbose --dry-run
```

**Verify Configuration Loading:**
```python
# In environment.py or test code
import behave.configuration

config = behave.configuration.Configuration()
print(f"Tags: {config.tags}")
print(f"Format: {config.format}")
print(f"Paths: {config.paths}")
```

## Complete Configuration Examples

### Example 1: Local Development

**Purpose:** Full output, debugging enabled, pretty format.

```ini
[behave]
paths = features/
format = pretty
show_skipped = true
show_timings = true
stdout_capture = false
stderr_capture = false
log_capture = true
logging_level = DEBUG
color = true
summary = true

[behave.userdata]
screenshot_dir = reports/screenshots
```

### Example 2: CI/CD Pipeline

**Purpose:** JUnit reports, JSON output, minimal console output.

```ini
[behave]
paths = features/
format = json
outfiles = reports/cucumber.json
junit = true
junit_directory = reports/junit
show_skipped = false
show_timings = true
stdout_capture = true
stderr_capture = true
log_capture = true
logging_level = INFO
color = false
summary = true
tags = @Smoke

[behave.userdata]
allure_results_dir = reports/allure-results
screenshot_dir = reports/screenshots
rerun_file = reports/rerun.txt
```

### Example 3: Smoke Test Suite

**Purpose:** Quick validation with critical tests only.

```ini
[behave]
paths = features/
format = pretty
show_skipped = false
show_timings = true
tags = @Smoke
color = true
summary = true

[behave.userdata]
screenshot_dir = reports/screenshots
```

### Example 4: Full Regression with Allure

**Purpose:** Complete test suite with rich Allure reporting.

```ini
[behave]
paths = features/
format = pretty
junit = true
junit_directory = reports/junit
show_skipped = false
show_timings = true
stdout_capture = false
log_capture = true
logging_level = INFO
color = true
summary = true

[behave.userdata]
allure_results_dir = reports/allure-results
screenshot_dir = reports/screenshots
rerun_file = reports/rerun.txt
```

**Execution:**
```bash
# Run with Allure formatter
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results -f pretty

# Serve Allure report
allure serve reports/allure-results
```

**Source:** `behave.ini:130-168`

## Common Configuration Patterns

### Pattern 1: Selective Test Execution

**Use Case:** Run specific test subsets for faster feedback.

```bash
# Smoke tests only
behave --tags=@Smoke

# Feature-specific tests
behave features/Login.feature

# User role tests
behave --tags=@SalesManager

# Exclude WIP tests
behave --tags='not @WIP'

# Critical + Login tests
behave --tags=@Critical,@Login
```

### Pattern 2: Report Generation

**Use Case:** Generate multiple report formats for different audiences.

```bash
# JSON for dashboards + Pretty for developers
behave -f json -o reports/cucumber.json -f pretty

# Allure for stakeholders + JUnit for CI
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results --junit --junit-directory reports/junit -f pretty

# HTML standalone report
behave -f behave_html_formatter:HTMLFormatter -o reports/report.html
```

### Pattern 3: Debugging Failed Tests

**Use Case:** Investigate test failures with maximum visibility.

```bash
# Disable output capture to see print statements
behave --no-capture --verbose

# Run with debug logging
behave --no-capture --logging-level=DEBUG

# Capture browser logs
behave --no-capture --define browser_logs=true
```

**Configuration:**
```ini
[behave]
stdout_capture = false
stderr_capture = false
logging_level = DEBUG
show_skipped = true
show_timings = true
```

### Pattern 4: Rerun Failed Tests

**Use Case:** Re-execute only failed tests after fixes.

```bash
# Initial run (failures saved to rerun.txt)
behave

# Rerun only failed scenarios
behave @reports/rerun.txt
```

**Configuration:**
```ini
[behave.userdata]
rerun_file = reports/rerun.txt
```

## See Also

- **[Command Reference](command-reference.md)** - Complete Behave CLI command reference
- **[Environment Variables Reference](environment-variables.md)** - All supported environment variables
- **[Configuration Options Reference](configuration-options.md)** - config.yaml settings
- **[Parallel Execution Guide](../guides/parallel-execution.md)** - Detailed parallel execution setup
- **[CI/CD Integration Guide](../deployment/jenkins-integration.md)** - Jenkins, GitHub Actions, GitLab CI
- **[Troubleshooting](../troubleshooting/configuration-issues.md)** - Configuration-related issues

---

**Documentation Version:** 1.0.0  
**Last Updated:** 2024-01-15  
**Behave Version:** 1.2.6  
**Source Files:** `behave.ini`, `README.md`
