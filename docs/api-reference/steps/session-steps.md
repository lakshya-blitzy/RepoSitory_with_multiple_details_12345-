# Session Step Definitions API Reference

## Overview

The Session step definitions module provides Behave step implementations for session management and authentication workflows in the Testinium test automation framework. This module contains step definitions that establish authenticated sessions as preconditions for testing other features, enabling test scenarios to start with users already logged in.

**Module:** `features/steps/session_steps.py`

**Purpose:** Lightweight authentication step for establishing test session preconditions

**Step Count:** 1 step definition (@when decorator)

**Dependencies:**
- `pages.session_page.SessionPage` - Session page object with login form elements
- `utilities.config_reader.ConfigReader` - Configuration reader for application URL
- `behave.runner.Context` - Behave context for WebDriver and shared state
- Environment variables: `TEST_USERNAME`, `TEST_PASSWORD`

## Migration Context

**Converted from:** `src/main/java/com/testinium/step_definitions/Session.java`

**Java Pattern:** Cucumber @When annotation with ConfigurationReader for credentials

**Python Pattern:** Behave @when decorator with environment variable credential access

### Key Changes from Java Implementation

1. **Decorator:** `@When` annotation → `@when` decorator from behave
2. **Page Object:** `SessionP session` instance → `SessionPage(context.driver)` instantiation
3. **Navigation:** `Driver.getDriver().get()` → `context.driver.get()` with Behave context
4. **Credentials:** `ConfigurationReader.getProperty()` → `os.getenv()` for security
5. **Element Access:** `session.inputLogin.sendKeys()` → `session_page.input_login.send_keys()`
6. **Wait Strategy:** Added explicit waits via property-based locators
7. **Error Handling:** Added comprehensive logging and credential validation
8. **Security:** Environment variables instead of configuration file credentials

### Critical Security Fix

**Original Java Implementation (INSECURE):**
```java
String username = ConfigurationReader.getProperty("username");
String password = ConfigurationReader.getProperty("password");
```

**Python Implementation (SECURE):**
```python
username = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")
```

The original Java implementation retrieved credentials from `configuration.properties` via ConfigurationReader, exposing credentials in configuration files committed to version control. This Python implementation uses environment variables following security best practices:

- Credentials never committed to repository
- Environment-specific credential injection (CI/CD, local, staging)
- Compliance with security remediation requirements

## Thread Safety

This module is **thread-safe** when used with Behave's context pattern. Each test scenario receives an isolated `context.driver` instance from DriverManager's `threading.local()` storage, supporting parallel test execution without session interference.

## Step Definitions

### user_login_to_test_other_features

Perform precondition login to establish authenticated session for testing other features.

**Decorator:** `@when("User login to test other features")`

**Gherkin Pattern:** `When User login to test other features`

**Source:** `features/steps/session_steps.py:78-268`

#### Description

This step definition provides lightweight authentication for test scenarios requiring pre-authenticated sessions. It navigates to the application login page, enters credentials from environment variables, and submits the login form. This step is typically used as a precondition (Given/When) for testing features that require authenticated user access.

#### Step Mapping

| Context | Step Pattern |
|---------|-------------|
| **Gherkin** | `When User login to test other features` |
| **Java** | `Session.java @When("User login to test other features")` |
| **Python** | `@when("User login to test other features")` |

#### Workflow

The step executes the following workflow:

1. **Retrieve Application URL** - Get base URL from configuration (`web.table.url`)
2. **Navigate to Login Page** - Use WebDriver to navigate to the application
3. **Retrieve Credentials** - Get credentials from environment variables (security fix)
4. **Instantiate SessionPage** - Create page object with Behave context.driver
5. **Enter Username** - Input username into `input_login` field
6. **Enter Password** - Input password into `input_password` field
7. **Submit Login** - Click `login_button` to submit credentials
8. **Wait for Navigation** - Browser handles page navigation automatically

#### Context Usage

| Attribute | Type | Purpose |
|-----------|------|---------|
| `context.driver` | WebDriver | Thread-local WebDriver instance from DriverManager |
| `context.config_reader` | ConfigReader | Optional ConfigReader singleton (if set in environment.py) |

The step accesses `context.driver` for browser automation and optionally uses `context.config_reader` for configuration access. Both are typically set in `features/environment.py` during scenario setup.

#### Configuration Requirements

**YAML Configuration (`config/config.yaml`):**
```yaml
web:
  table:
    url: https://app.testinium.com/login
```

**Environment Variables (`.env` file):**
```bash
TEST_USERNAME=salesmanager1@testinium.com
TEST_PASSWORD=UserUser
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `behave.runner.Context` | Behave context object providing WebDriver instance and shared state |

#### Returns

**Return Type:** `None`

This step does not return a value. Login success is implicit and should be verified in subsequent Then steps.

#### Raises

| Exception | Condition |
|-----------|-----------|
| `KeyError` | If `web.table.url` configuration key is missing in config.yaml |
| `EnvironmentError` | If `TEST_USERNAME` or `TEST_PASSWORD` not set in environment |
| `TimeoutException` | If login page elements not found within timeout period (default 10s) |
| `WebDriverException` | If browser automation encounters errors during navigation or interaction |

#### Usage Example

**Behave Context Setup (`features/environment.py`):**
```python
from utilities.driver_manager import DriverManager
from utilities.config_reader import ConfigReader

def before_scenario(context, scenario):
    """Initialize WebDriver and configuration for each scenario."""
    context.driver = DriverManager.get_driver()
    context.config_reader = ConfigReader()
```

**Feature File (`features/Session.feature`):**
```gherkin
Feature: Session Management
  
  Scenario: Precondition login for feature testing
    When User login to test other features
    Then User should see the authenticated dashboard
```

**Environment Variables (`.env` file):**
```bash
# Test account credentials (not committed to git)
TEST_USERNAME=salesmanager1@testinium.com
TEST_PASSWORD=UserUser

# Application configuration
WEB_TABLE_URL=https://app.testinium.com/login
```

**Execution:**
```bash
# Run session feature
behave features/Session.feature

# Run with specific scenario
behave features/Session.feature --name="Precondition login"

# Run all features using session precondition
behave --tags=@session_required
```

#### Implementation Details

**Security Implementation:**

The step uses environment variables for credential retrieval instead of configuration files:

```python
username = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")

if not username:
    raise EnvironmentError(
        "TEST_USERNAME environment variable not set. "
        "Set TEST_USERNAME in .env file or CI/CD configuration."
    )

if not password:
    raise EnvironmentError(
        "TEST_PASSWORD environment variable not set. "
        "Set TEST_PASSWORD in .env file or CI/CD configuration."
    )
```

**Page Object Interaction:**

The step uses property-based element access with automatic explicit waits:

```python
session_page = SessionPage(context.driver)

# Property access automatically waits for element presence
session_page.input_login.send_keys(username)

# Property access automatically waits for element visibility
session_page.input_password.send_keys(password)

# Property access automatically waits for element to be clickable
session_page.login_button.click()
```

**Logging:**

The step includes comprehensive logging without exposing sensitive credentials:

```python
logger.info("Executing precondition login for session establishment")
logger.info("Retrieved application URL from configuration: %s", base_url)
logger.info(
    "Retrieved credentials from environment: username=%s, password=***",
    username
)
logger.info("Login button clicked, waiting for page navigation")
```

#### Notes

- This step is typically used as a **precondition** (Given/When) for other features
- Login success is **implicit**; verification should be in subsequent Then steps
- Page navigation after login is handled **automatically** by the browser
- Session persistence maintained by **browser cookies** (WebDriver session)
- No explicit waits needed after login; subsequent steps will wait for expected elements

#### Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| **Execution Time** | ~2-5 seconds | Network dependent, includes navigation and element interactions |
| **Wait Timeout** | 10 seconds default | Configurable via `timeouts.default_explicit_wait` in config.yaml |
| **Waits Used** | Explicit waits only | No `Thread.sleep()` calls (follows wait strategy remediation) |
| **Network Calls** | 2-3 requests | Initial page load, form submission, redirect after login |

#### Thread Safety Guarantees

- **Thread-safe** when `context.driver` is thread-local WebDriver instance from DriverManager
- Each parallel test execution has **isolated driver** and SessionPage instances
- No shared state between test threads
- Supports **parallel execution** with behave-parallel or pytest-xdist

## Feature File Examples

### Basic Session Precondition

**Source:** `features/Session.feature`

```gherkin
Feature: Default
  
  Scenario: Users log in to access additional feature
    When User login to test other features
```

### Session with Verification

```gherkin
Feature: Authenticated Session Management
  
  Scenario: Establish authenticated session for testing
    When User login to test other features
    Then User should see the dashboard
    And User's name should be displayed in header
```

### Using Session as Precondition

```gherkin
Feature: CRM Management
  
  Background:
    When User login to test other features
  
  Scenario: Create new customer record
    Given User navigates to CRM section
    When User creates a new customer
    Then Customer should be saved successfully
```

### Tagged Session Requirements

```gherkin
Feature: Inventory Management
  
  @session_required @inventory
  Scenario: Update inventory levels
    When User login to test other features
    And User navigates to inventory section
    When User updates product quantity to 100
    Then Inventory should reflect updated quantity
```

## Configuration Examples

### Local Development Configuration

**`.env` file (not committed to git):**
```bash
# Application URL
WEB_TABLE_URL=https://app.testinium.com/login

# Test credentials (local development)
TEST_USERNAME=salesmanager1@testinium.com
TEST_PASSWORD=UserUser

# Browser configuration
BROWSER_TYPE=chrome
HEADLESS=false
```

**`config/config.yaml`:**
```yaml
application:
  web:
    table:
      url: ${WEB_TABLE_URL:https://app.testinium.com/login}

browser:
  type: ${BROWSER_TYPE:chrome}
  headless: ${HEADLESS:false}

timeouts:
  default_explicit_wait: 10
  page_load: 30
```

### CI/CD Environment Configuration

**GitHub Actions:**
```yaml
env:
  TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
  TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
  WEB_TABLE_URL: https://app.testinium.com/login
  BROWSER_TYPE: chrome
  HEADLESS: true
```

**Jenkins:**
```groovy
environment {
    TEST_USERNAME = credentials('testinium-username')
    TEST_PASSWORD = credentials('testinium-password')
    WEB_TABLE_URL = 'https://app.testinium.com/login'
    HEADLESS = 'true'
}
```

**GitLab CI:**
```yaml
variables:
  WEB_TABLE_URL: "https://app.testinium.com/login"
  BROWSER_TYPE: "chrome"
  HEADLESS: "true"

# Secrets stored in GitLab CI/CD Variables:
# TEST_USERNAME (protected, masked)
# TEST_PASSWORD (protected, masked)
```

## Error Handling Examples

### Missing Configuration

```python
# If web.table.url is not in config.yaml:
KeyError: "Missing required configuration 'web.table.url'. 
Check config/config.yaml or set WEB_TABLE_URL environment variable."
```

**Solution:**
```yaml
# Add to config/config.yaml:
web:
  table:
    url: https://app.testinium.com/login
```

### Missing Credentials

```python
# If TEST_USERNAME is not set:
EnvironmentError: "TEST_USERNAME environment variable not set. 
Set TEST_USERNAME in .env file (local development) or 
CI/CD environment configuration."
```

**Solution:**
```bash
# Add to .env file:
TEST_USERNAME=salesmanager1@testinium.com
TEST_PASSWORD=UserUser
```

### Element Not Found

```python
# If login page elements not found:
TimeoutException: "Element not found: (By.ID, 'login')"
```

**Possible Causes:**
- Login page not loaded correctly
- Element locator changed in application
- Network timeout or slow page load

**Solution:**
```bash
# Increase timeout in config.yaml:
timeouts:
  default_explicit_wait: 20  # Increased from 10 to 20 seconds
```

## Related Documentation

### API References

- [SessionPage API](../pages/session-page.md) - Session page object with login form elements
- [ConfigReader API](../utilities/config-reader.md) - Configuration management singleton
- [DriverManager API](../utilities/driver-manager.md) - WebDriver lifecycle management
- [BasePage API](../pages/base-page.md) - Base page object with wait utilities

### User Guides

- [Session Testing Guide](../../guides/session-testing.md) - Session management testing workflows
- [Authentication Testing Guide](../../guides/authentication-testing.md) - Login/logout testing patterns
- [Configuration Management](../../guides/configuration-management.md) - Configuration best practices
- [Parallel Execution Guide](../../guides/parallel-execution.md) - Thread-safety and parallel testing

### Reference Documentation

- [Configuration Options](../../reference/configuration-options.md) - Complete configuration reference
- [Environment Variables](../../reference/environment-variables.md) - Environment variable reference
- [Gherkin Syntax](../../reference/gherkin-syntax.md) - Gherkin language reference

### Troubleshooting

- [Configuration Issues](../../troubleshooting/configuration-issues.md) - Configuration troubleshooting
- [WebDriver Issues](../../troubleshooting/webdriver-issues.md) - WebDriver troubleshooting
- [Common Errors](../../troubleshooting/common-errors.md) - Common error solutions

## Best Practices

### 1. Use as Precondition in Background

```gherkin
Feature: Multi-Feature Testing

  Background:
    When User login to test other features
  
  Scenario: Test feature A
    # Test starts with authenticated session
  
  Scenario: Test feature B
    # Test starts with authenticated session
```

### 2. Secure Credential Management

**Never commit credentials to repository:**

```bash
# Add to .gitignore:
.env
*.env
.env.local
credentials.yaml
```

**Use environment-specific credentials:**

```bash
# .env.local (local development)
TEST_USERNAME=dev-user@example.com
TEST_PASSWORD=dev-password

# .env.staging (staging environment)
TEST_USERNAME=staging-user@example.com
TEST_PASSWORD=staging-password

# .env.production (production environment - never commit!)
TEST_USERNAME=prod-user@example.com
TEST_PASSWORD=prod-password
```

### 3. Verify Login Success in Subsequent Steps

```gherkin
Scenario: Verify successful authentication
  When User login to test other features
  Then User should see the dashboard
  And User menu should display username
  And Logout button should be visible
```

### 4. Tag Scenarios Requiring Authentication

```gherkin
@authenticated @session_required
Scenario: Access protected feature
  When User login to test other features
  And User navigates to protected section
  Then Protected content should be visible
```

### 5. Use Appropriate Timeouts

```yaml
# config/config.yaml
timeouts:
  default_explicit_wait: 10  # Standard wait for element presence
  page_load: 30              # Extended wait for full page load
  implicit_wait: 0           # Never use implicit waits
```

## Advanced Usage

### Multiple User Sessions

```gherkin
Scenario: Test with multiple user roles
  Given Admin user logs in
  And Manager user logs in
  When Admin creates a report
  And Manager accesses the report
  Then Both users should see the same data
```

**Implementation:**
```python
@given("Admin user logs in")
def admin_login(context):
    context.admin_driver = DriverManager.get_driver()
    # Login with admin credentials

@given("Manager user logs in")
def manager_login(context):
    context.manager_driver = DriverManager.get_driver()
    # Login with manager credentials
```

### Session State Validation

```gherkin
Scenario: Validate session persistence
  When User login to test other features
  And User navigates to multiple pages
  Then Session should remain active
  And User should stay authenticated
```

### Session Timeout Testing

```gherkin
Scenario: Handle session timeout
  When User login to test other features
  And User waits for session timeout
  Then User should be redirected to login
  And Error message should indicate timeout
```

## See Also

- [Login Step Definitions](login-steps.md) - Dedicated login/logout step definitions
- [All Step Definitions](index.md) - Complete step definitions overview
- [Behave Hooks](../features/environment.md) - Test lifecycle management
- [Page Object Model Guide](../../guides/page-object-model.md) - POM architecture patterns

---

**Last Updated:** 2024-01-09 (automatically managed by git)

**Module Version:** 1.0.0

**Documentation Status:** Complete

**Source Code:** `features/steps/session_steps.py`
