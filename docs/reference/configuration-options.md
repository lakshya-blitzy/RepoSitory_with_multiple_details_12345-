# Configuration Options Reference

Complete reference for all configuration options in `config/config.yaml`.

## Overview

The `config.yaml` file is the primary configuration file for the Testinium Python test automation framework. It provides a centralized, type-safe configuration system that replaces the missing `configuration.properties` file referenced in the original Java implementation (`ConfigurationReader.java`).

### Configuration File Location

**Source:** `config/config.yaml`

### Key Features

- **YAML Structure**: Human-readable, hierarchical configuration format
- **Environment Variable Interpolation**: Secure credential management using `${VAR_NAME}` syntax
- **Type-Safe Access**: Configuration loaded into Python dataclasses for IDE autocompletion
- **Migration from Java**: Replaces Properties file approach with modern YAML configuration

### Environment Variable Interpolation Syntax

The configuration file supports environment variable substitution with two syntax patterns:

1. **Required Variables**: `${VAR_NAME}` - Raises error if environment variable is not set
2. **Variables with Defaults**: `${VAR_NAME:default_value}` - Uses default if environment variable is not set

**Example:**
```yaml
application:
  base_url: ${BASE_URL:https://testinium.example.com}
```

**Source:** `config/test_config.py:265-309` (environment variable substitution logic)

### python-dotenv Integration

The framework uses `python-dotenv` to automatically load environment variables from a `.env` file before parsing the YAML configuration. This enables local development with secure credential management.

**Source:** `config/test_config.py:182` (load_dotenv() call)

## Configuration Sections

### Browser Configuration

Configures WebDriver browser settings for test execution. Corresponds to browser selection logic in Java `Driver.java` line 27.

**Source:** `config/config.yaml:18-38`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `browser.type` | string | `chrome` | Browser type for test execution. Valid values: `chrome`, `firefox`. Maps to `ConfigurationReader.getProperty("browser")` in Java Driver.java |
| `browser.headless` | boolean | `false` | Headless mode flag. Set to `true` for CI/CD environments, `false` for local debugging with visible browser |
| `browser.window_size` | array | `[1920, 1080]` | Browser window dimensions as `[width, height]` in pixels. Ensures consistent viewport across all test executions |
| `browser.implicit_wait` | integer | `0` | Implicit wait timeout in seconds. **MUST be 0** per Agent Action Plan section 0.8.1. Eliminates dangerous mixing of implicit and explicit waits from Java Driver.java line 34. All waits should use explicit WebDriverWait |

#### Browser Type

**Java Equivalent:** `Driver.java:27` - `ConfigurationReader.getProperty("browser")`

**Values:**
- `chrome` - Google Chrome browser (default)
- `firefox` - Mozilla Firefox browser

**Example:**
```yaml
browser:
  type: chrome
```

#### Headless Mode

Controls whether the browser runs with a visible GUI or in headless mode.

**Use Cases:**
- **Local Development**: `headless: false` - See browser interactions during test development and debugging
- **CI/CD Pipelines**: `headless: true` - Run tests in headless mode for faster execution and no GUI requirements

**Example:**
```yaml
browser:
  headless: true  # CI/CD mode
```

#### Window Size

Sets the browser window dimensions for consistent viewport across test executions.

**Format:** `[width, height]` array in pixels

**Example:**
```yaml
browser:
  window_size: [1920, 1080]  # Full HD resolution
```

#### Implicit Wait (Deprecated)

**CRITICAL:** This value **MUST be set to 0**. Implicit waits are disabled in favor of explicit waits only.

**Rationale:** The Java implementation in `Driver.java:34` used implicit waits, which caused timing issues when mixed with explicit waits. The Python implementation eliminates this anti-pattern by using only explicit WebDriverWait with expected_conditions.

**Source:** Agent Action Plan section 0.8.1, `config/test_config.py:54`

**Example:**
```yaml
browser:
  implicit_wait: 0  # Always 0 - use explicit waits instead
```

### Timeout Configuration

Standardized timeout values replacing inconsistent timeout ranges (2-20 seconds) hardcoded throughout Java step definitions (`LoginSD.java`, `Calendar.java`, etc.).

**Source:** `config/config.yaml:40-60`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `timeouts.explicit` | integer | `10` | Default explicit wait timeout in seconds. Replaces hardcoded `WebDriverWait(driver, X)` values throughout Java step definitions |
| `timeouts.page_load` | integer | `30` | Page load timeout in seconds. Maximum time to wait for page load events |
| `timeouts.element_presence` | integer | `5` | Element presence timeout in seconds. Wait duration for element to be present in DOM |
| `timeouts.clickability` | integer | `3` | Element clickability timeout in seconds. Wait duration for element to be visible and enabled |

#### Explicit Wait Timeout

Default timeout for all explicit waits using `WebDriverWait`.

**Java Equivalent:** Replaces hardcoded values in `LoginSD.java`, `Calendar.java`, and other step definition files

**Usage in Framework:**
```python
from utilities.wait_helpers import WaitHelpers
# Uses config.timeouts.explicit
wait = WaitHelpers(driver)
element = wait.wait_for_element(locator)
```

**Source:** `config/test_config.py:58-74`

**Example:**
```yaml
timeouts:
  explicit: 10  # 10 seconds for explicit waits
```

#### Page Load Timeout

Maximum time to wait for the page load event to complete.

**Example:**
```yaml
timeouts:
  page_load: 30  # 30 seconds for full page load
```

#### Element Presence Timeout

Timeout for waiting until an element is present in the DOM (may not be visible).

**Example:**
```yaml
timeouts:
  element_presence: 5  # 5 seconds for element to appear in DOM
```

#### Clickability Timeout

Timeout for waiting until an element is both visible and enabled (clickable state).

**Example:**
```yaml
timeouts:
  clickability: 3  # 3 seconds for element to become clickable
```

### Application Configuration

Application URLs and environment-specific settings. Supports `ConfigurationReader.getProperty()` calls throughout step definitions.

**Source:** `config/config.yaml:62-85`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `application.base_url` | string | `${BASE_URL:https://testinium.example.com}` | Base application URL with environment variable override. Corresponds to `LoginSD.java:20` and `EmployeeStage.java:20` |
| `application.login_url` | string | `${BASE_URL:https://testinium.example.com}/login` | Login page URL derived from base_url. Used in `LoginSD.java` for navigation |
| `application.web_table_url` | string | `${BASE_URL:https://testinium.example.com}/web-tables` | Employee management web table URL. Referenced in `EmployeeStage.java:20` via `ConfigurationReader.getProperty("web.table.url")` |
| `application.empl_title` | string | `"Employee Management"` | Expected employee page title for verification. Used in `EmployeeStage.java:36` for title assertion after navigation |

#### Base URL

The base URL of the application under test, with environment variable override support.

**Java Equivalent:** `LoginSD.java:20`, `EmployeeStage.java:20` - `ConfigurationReader.getProperty("web.table.url")`

**Environment Variable Override:**
```bash
# .env file or CI/CD environment
BASE_URL=https://staging.testinium.com
```

**Example:**
```yaml
application:
  base_url: ${BASE_URL:https://testinium.example.com}
```

#### Login URL

URL for the application login page.

**Java Equivalent:** Used in `LoginSD.java` for driver.get() navigation

**Example:**
```yaml
application:
  login_url: ${BASE_URL:https://testinium.example.com}/login
```

#### Web Table URL

URL for the employee management web table page.

**Java Equivalent:** `EmployeeStage.java:20` - `ConfigurationReader.getProperty("web.table.url")`

**Example:**
```yaml
application:
  web_table_url: ${BASE_URL:https://testinium.example.com}/web-tables
```

#### Employee Page Title

Expected page title for employee management page, used for verification after navigation.

**Java Equivalent:** `EmployeeStage.java:36` - `driver.getTitle()` comparison

**Example:**
```yaml
application:
  empl_title: "Employee Management"
```

### Credentials Configuration

User credentials loaded from environment variables for security. **All credentials MUST be provided via environment variables or `.env` file.**

This configuration remediates the hardcoded credentials vulnerability found in the original Java `EmployeeP.java` file.

**Source:** `config/config.yaml:87-110`

| Option | Type | Required | Description |
|--------|------|----------|-------------|
| `credentials.username` | string | Yes | Generic test user username. Used in `Session.java:16-17` via `ConfigurationReader.getProperty("username")` |
| `credentials.password` | string | Yes | Generic test user password. Used in `Session.java:16-17` via `ConfigurationReader.getProperty("password")` |
| `credentials.sales_manager_username` | string | Optional | Sales Manager role username. Used in `Login.feature` scenarios with `@SalesManager` tag |
| `credentials.sales_manager_password` | string | Optional | Sales Manager role password. Required for sales manager role-based testing |
| `credentials.pos_manager_username` | string | Optional | POS Manager role username. Used in `Login.feature` scenarios with `@PosManager` tag |
| `credentials.pos_manager_password` | string | Optional | POS Manager role password. Required for POS manager role-based testing |

#### Security Notes

- **Never commit credentials to version control**
- All credential values use environment variable interpolation: `${VAR_NAME}`
- Missing credentials log warnings but don't fail configuration loading
- Credentials validation in `config/test_config.py:311-335`

**Source:** `config/test_config.py:96-117` (CredentialsConfig dataclass)

#### Generic Test User Credentials

Default test user credentials for standard test scenarios.

**Java Equivalent:** `Session.java:16-17` - username and password property access

**Environment Variables:**
```bash
TEST_USERNAME=test.user@example.com
TEST_PASSWORD=secure_password_here
```

**Example:**
```yaml
credentials:
  username: ${TEST_USERNAME}
  password: ${TEST_PASSWORD}
```

#### Sales Manager Credentials

Role-based credentials for Sales Manager permission level testing.

**Used In:** `Login.feature` scenarios with `@SalesManager` tag

**Environment Variables:**
```bash
SALES_MANAGER_USERNAME=sales.manager@example.com
SALES_MANAGER_PASSWORD=secure_password_here
```

**Example:**
```yaml
credentials:
  sales_manager_username: ${SALES_MANAGER_USERNAME}
  sales_manager_password: ${SALES_MANAGER_PASSWORD}
```

#### POS Manager Credentials

Role-based credentials for POS Manager permission level testing.

**Used In:** `Login.feature` scenarios with `@PosManager` tag

**Environment Variables:**
```bash
POS_MANAGER_USERNAME=pos.manager@example.com
POS_MANAGER_PASSWORD=secure_password_here
```

**Example:**
```yaml
credentials:
  pos_manager_username: ${POS_MANAGER_USERNAME}
  pos_manager_password: ${POS_MANAGER_PASSWORD}
```

### Reporting Configuration

Test execution reporting and artifact generation settings. Corresponds to screenshot capture and report generation in Java `Hooks.java`.

**Source:** `config/config.yaml:112-139`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `reporting.screenshot_on_failure` | boolean | `true` | Enable automatic screenshot capture on test failure. Implements after_scenario hook in `features/environment.py`, replacing `Hooks.java` @After screenshot logic |
| `reporting.output_directory` | string | `reports/` | Base output directory for all test artifacts (JSON reports, HTML reports, screenshots) |
| `reporting.formats` | array | `[json, html, allure]` | List of report formats to generate. Supports: `json` (Behave JSON), `html` (Behave HTML), `allure` (Allure test report) |
| `reporting.screenshot_directory` | string | `reports/screenshots/` | Screenshot storage directory. Screenshots named with timestamp and scenario name for failure diagnostics |

#### Screenshot on Failure

Controls automatic screenshot capture when test scenarios fail.

**Java Equivalent:** `Hooks.java` @After annotation with screenshot logic

**Implementation:** `features/environment.py` after_scenario hook

**Source:** `config/test_config.py:120-136` (ReportingConfig dataclass)

**Example:**
```yaml
reporting:
  screenshot_on_failure: true
```

#### Output Directory

Base directory for all test execution artifacts.

**Contents:**
- `cucumber.json` - Behave JSON output
- `cucumber-reports.html` - Behave HTML report
- `allure-results/` - Allure report data
- `screenshots/` - Failure screenshots

**Example:**
```yaml
reporting:
  output_directory: reports/
```

#### Report Formats

List of report formats to generate during test execution.

**Available Formats:**
- **`json`**: Behave JSON output format → `reports/cucumber.json`
- **`html`**: Behave HTML report → `reports/cucumber-reports.html`
- **`allure`**: Allure test report format for enhanced visualization

**Example:**
```yaml
reporting:
  formats:
    - json
    - html
    - allure
```

#### Screenshot Directory

Directory where failure screenshots are stored.

**Naming Convention:** `{timestamp}_{scenario_name}.png`

**Attachment:** Screenshots are attached to test reports for debugging failed scenarios

**Example:**
```yaml
reporting:
  screenshot_directory: reports/screenshots/
```

## Configuration Access Patterns

The framework provides two ways to access configuration values:

### 1. ConfigReader Access Pattern (Backward Compatible)

Legacy access pattern compatible with Java `ConfigurationReader.getProperty()` approach.

**Source:** `utilities/config_reader.py`

**Example:**
```python
from utilities.config_reader import ConfigReader

config = ConfigReader()
browser_type = config.get_property("browser.type")
timeout = config.get_property("timeouts.explicit")
base_url = config.get_property("application.base_url")
```

### 2. Dataclass Access Pattern (Type-Safe, Recommended)

Modern, type-safe access via Python dataclasses with full IDE autocompletion.

**Source:** `config/test_config.py`

**Example:**
```python
from config.test_config import Config

config = Config()
browser_type = config.browser.type          # 'chrome'
timeout = config.timeouts.explicit          # 10
base_url = config.application.base_url      # From environment or config
headless = config.browser.headless          # False
```

### 3. Singleton Access Pattern

Convenient global access without passing config objects explicitly.

**Source:** `config/test_config.py:409-433`

**Example:**
```python
from config.test_config import get_config

config = get_config()
print(config.browser.type)
```

## Environment Variable Interpolation

### Syntax

The configuration file supports two environment variable interpolation syntaxes:

#### Required Variables

Syntax: `${VAR_NAME}`

Raises a `ValueError` if the environment variable is not set.

**Example:**
```yaml
credentials:
  username: ${TEST_USERNAME}  # ERROR if TEST_USERNAME not set
```

#### Variables with Default Values

Syntax: `${VAR_NAME:default_value}`

Uses the default value if the environment variable is not set.

**Example:**
```yaml
application:
  base_url: ${BASE_URL:https://testinium.example.com}
  # Uses https://testinium.example.com if BASE_URL not set
```

### Credential Variables Exception

Credential-related environment variables (ending with `USERNAME` or `PASSWORD`) are treated specially:
- Missing credentials log warnings but don't fail configuration loading
- Return empty string if not set, allowing tests to skip scenarios requiring those credentials

**Source:** `config/test_config.py:300-304`

### Precedence Rules

Configuration value resolution follows this precedence (highest to lowest):

1. **Environment Variable** - If set, always takes precedence
2. **Default Value** - If provided in `${VAR:default}` syntax and environment variable not set
3. **Config File Value** - If no environment variable interpolation syntax used

## Migration Notes from Java

This section documents the mapping between the Python configuration system and the original Java implementation.

### Java Configuration Files Replaced

| Java File | Python Replacement | Notes |
|-----------|-------------------|-------|
| `configuration.properties` | `config/config.yaml` | Properties file missing in Java project; YAML provides better structure |
| `ConfigurationReader.java` | `config/test_config.py` | Singleton Properties reader replaced with type-safe dataclass approach |
| Hardcoded values in `Driver.java` | `config.yaml` browser section | Browser settings centralized in configuration |
| Hardcoded credentials in `EmployeeP.java` | Environment variables | Security vulnerability remediated |

**Source:** `config/config.yaml:4-5`, `config/test_config.py:1-24`

### ConfigurationReader.getProperty() Mapping

Java method calls mapped to Python configuration access:

| Java Call | Python Equivalent (ConfigReader) | Python Equivalent (Dataclass) |
|-----------|----------------------------------|-------------------------------|
| `ConfigurationReader.getProperty("browser")` | `config.get_property("browser.type")` | `config.browser.type` |
| `ConfigurationReader.getProperty("web.table.url")` | `config.get_property("application.web_table_url")` | `config.application.web_table_url` |
| `ConfigurationReader.getProperty("username")` | `config.get_property("credentials.username")` | `config.credentials.username` |
| `ConfigurationReader.getProperty("password")` | `config.get_property("credentials.password")` | `config.credentials.password` |

### Driver.java Settings Mapping

| Driver.java Line | Setting | config.yaml Location |
|------------------|---------|---------------------|
| Line 27 | Browser type selection | `browser.type` |
| Line 34 | Implicit wait (10 seconds) | `browser.implicit_wait` (now 0) |
| N/A (hardcoded) | Headless mode | `browser.headless` |
| N/A (hardcoded) | Window size | `browser.window_size` |

### Step Definition Timeout Mapping

Hardcoded timeouts in Java step definitions replaced with centralized configuration:

| Java File | Java Timeout | config.yaml Setting |
|-----------|--------------|-------------------|
| `LoginSD.java` | `WebDriverWait(driver, 2)` to `WebDriverWait(driver, 20)` | `timeouts.explicit: 10` |
| `Calendar.java` | Various hardcoded waits | `timeouts.explicit: 10` |
| Various step files | Inconsistent timeout values | Standardized in `timeouts` section |

## Configuration Validation

The framework performs comprehensive validation when loading configuration.

**Source:** `config/test_config.py:169-217`

### Validation on Load

The `Config` class validates configuration during initialization:

#### File Existence Check

```python
# Raises FileNotFoundError if config file doesn't exist
config = Config(config_file='config/config.yaml')
```

**Exception:** `FileNotFoundError` - Configuration file not found

**Source:** `config/test_config.py:238-240`

#### YAML Parsing Validation

```python
# Raises yaml.YAMLError if YAML syntax is invalid
config_dict = yaml.safe_load(yaml_content)
```

**Exception:** `yaml.YAMLError` - Failed to parse YAML configuration

**Source:** `config/test_config.py:258-260`

#### Required Section Validation

```python
# Raises ValueError if required configuration sections are missing
self.browser = BrowserConfig(**self._raw_config['browser'])
```

**Exception:** `ValueError` - Missing required configuration section

**Source:** `config/test_config.py:212-214`

#### Type Validation

Configuration values are validated against dataclass type hints:

```python
@dataclass
class BrowserConfig:
    type: str                    # Must be string
    headless: bool               # Must be boolean
    window_size: Tuple[int, int] # Must be [int, int] array
    implicit_wait: int = 0       # Must be integer
```

**Exception:** `TypeError` or `ValueError` - Invalid configuration structure

**Source:** `config/test_config.py:215-217`

### Credentials Validation

Credentials are validated with warnings (not errors) to allow tests to run without all role-based credentials:

```python
def _validate_credentials(self) -> None:
    """
    Validate that required credentials are available.
    
    Logs warnings for missing credentials but doesn't fail.
    """
```

**Validation Checks:**
- Default test credentials (`TEST_USERNAME`, `TEST_PASSWORD`)
- Sales manager credentials (`SALES_MANAGER_USERNAME`, `SALES_MANAGER_PASSWORD`)
- POS manager credentials (`POS_MANAGER_USERNAME`, `POS_MANAGER_PASSWORD`)

**Behavior:** Missing credentials log warnings but don't prevent configuration loading

**Source:** `config/test_config.py:311-335`

## Complete Configuration Example

Here's a complete, working `config.yaml` example with all sections:

```yaml
# =============================================================================
# Test Configuration for Python Behave Test Automation Framework
# =============================================================================

# -----------------------------------------------------------------------------
# Browser Configuration
# -----------------------------------------------------------------------------
browser:
  type: chrome
  headless: false
  window_size: [1920, 1080]
  implicit_wait: 0  # Always 0 - use explicit waits

# -----------------------------------------------------------------------------
# Timeout Configuration
# -----------------------------------------------------------------------------
timeouts:
  explicit: 10
  page_load: 30
  element_presence: 5
  clickability: 3

# -----------------------------------------------------------------------------
# Application Configuration
# -----------------------------------------------------------------------------
application:
  base_url: ${BASE_URL:https://testinium.example.com}
  login_url: ${BASE_URL:https://testinium.example.com}/login
  web_table_url: ${BASE_URL:https://testinium.example.com}/web-tables
  empl_title: "Employee Management"

# -----------------------------------------------------------------------------
# Credentials Configuration
# -----------------------------------------------------------------------------
credentials:
  username: ${TEST_USERNAME}
  password: ${TEST_PASSWORD}
  sales_manager_username: ${SALES_MANAGER_USERNAME}
  sales_manager_password: ${SALES_MANAGER_PASSWORD}
  pos_manager_username: ${POS_MANAGER_USERNAME}
  pos_manager_password: ${POS_MANAGER_PASSWORD}

# -----------------------------------------------------------------------------
# Reporting Configuration
# -----------------------------------------------------------------------------
reporting:
  screenshot_on_failure: true
  output_directory: reports/
  formats:
    - json
    - html
    - allure
  screenshot_directory: reports/screenshots/
```

## Environment Variables Example

Corresponding `.env` file for local development:

```bash
# Application URLs
BASE_URL=https://testinium.example.com

# Test User Credentials
TEST_USERNAME=test.user@example.com
TEST_PASSWORD=secure_password_here

# Role-Based Credentials
SALES_MANAGER_USERNAME=sales.manager@example.com
SALES_MANAGER_PASSWORD=secure_password_here
POS_MANAGER_USERNAME=pos.manager@example.com
POS_MANAGER_PASSWORD=secure_password_here
```

**Source:** `.env.example` (template for local development)

## Usage Examples

### Basic Configuration Loading

```python
from config.test_config import Config

# Load configuration with defaults
config = Config()

# Access browser settings
print(f"Browser: {config.browser.type}")           # 'chrome'
print(f"Headless: {config.browser.headless}")      # False
print(f"Window Size: {config.browser.window_size}") # (1920, 1080)

# Access timeouts
print(f"Explicit Wait: {config.timeouts.explicit}s")  # 10

# Access application URLs
print(f"Base URL: {config.application.base_url}")
print(f"Login URL: {config.application.login_url}")

# Access credentials (if configured)
if config.credentials.username:
    print(f"Username: {config.credentials.username}")
```

### Singleton Pattern

```python
from config.test_config import get_config

# Get singleton instance
config = get_config()

# Use throughout application
browser_type = config.browser.type
```

### Backward Compatible Access

```python
from config.test_config import Config

config = Config()

# Dot notation key access
browser = config.get('browser.type', 'chrome')
timeout = config.get('timeouts.explicit', 10)
url = config.get('application.base_url')
```

### In Behave Environment Hooks

```python
# features/environment.py
from config.test_config import Config

def before_all(context):
    """Initialize configuration before test suite."""
    context.config = Config()
    context.base_url = context.config.application.base_url
    
def before_scenario(context, scenario):
    """Access configuration in scenarios."""
    if context.config.browser.headless:
        # Headless mode specific setup
        pass
```

## See Also

- [Environment Variables Reference](environment-variables.md) - Complete list of environment variables
- [Configuration Management Guide](../guides/configuration-management.md) - Advanced configuration patterns
- [Config API Documentation](../api-reference/config/test-config.md) - API reference for Config classes
- [Behave Configuration Reference](behave-configuration.md) - Behave framework configuration
- [pytest Configuration Reference](pytest-configuration.md) - pytest framework configuration

## Source References

- Configuration File: `config/config.yaml`
- Configuration Module: `config/test_config.py`
- Package Exports: `config/__init__.py`
- Java Migration Context: `config/test_config.py:1-24` (module docstring)
- Validation Logic: `config/test_config.py:219-335`
- Environment Variable Substitution: `config/test_config.py:265-309`
