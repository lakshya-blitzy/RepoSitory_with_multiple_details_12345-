# Initial Configuration

This guide walks you through configuring your test automation framework for the first time. You'll learn how to set up environment variables, customize test settings, and configure browser options.

## Overview

The test automation framework uses a three-layer configuration system:

1. **Environment Variables (.env)** - For secrets and environment-specific values
2. **Test Configuration (config.yaml)** - For framework defaults and test settings
3. **Behave Configuration (behave.ini)** - For test execution and reporting options

### Configuration Precedence

Configuration values are resolved with the following precedence (highest to lowest):

1. **Environment variables** (.env file or system environment) - **Highest priority**
2. **config.yaml** - Framework defaults and structured settings
3. **behave.ini** - Test execution defaults
4. **Framework defaults** - Built-in fallback values

This means values in your `.env` file will override corresponding values in `config.yaml`, allowing you to customize behavior per environment without modifying code.

**Source:** `config/config.yaml:1-16`, `.env.example:1-31`

## Environment Variables Setup

Environment variables provide a secure way to manage credentials and environment-specific configuration without committing sensitive data to version control.

### Creating Your .env File

**Step 1: Copy the Example File**

```bash
# From the project root directory
cp .env.example .env
```

**Step 2: Edit with Your Values**

Open `.env` in your text editor and replace the example values with your actual configuration:

```bash
# Environment Variables for Test Automation Framework
# NEVER commit this file to version control

# Browser Configuration (optional - overrides config.yaml)
BROWSER_TYPE=chrome
HEADLESS=false

# Test Environment
BASE_URL=https://your-test-environment.com

# Timeouts (optional - overrides config.yaml)
TIMEOUT_EXPLICIT=10
TIMEOUT_PAGE_LOAD=30

# Test Credentials (REQUIRED)
ADMIN_USERNAME=admin@yourcompany.com
ADMIN_PASSWORD=your_actual_password

POS_MANAGER_USERNAME=posmanager@yourcompany.com
POS_MANAGER_PASSWORD=your_actual_password

SALES_MANAGER_USERNAME=salesmanager@yourcompany.com
SALES_MANAGER_PASSWORD=your_actual_password

TEST_USERNAME=testuser@yourcompany.com
TEST_PASSWORD=your_actual_password

# Reporting
SCREENSHOTS_ON_FAILURE=true
```

### Environment Variable Groups

#### Browser Configuration

| Variable | Options | Default | Description |
|----------|---------|---------|-------------|
| `BROWSER_TYPE` | `chrome`, `firefox` | `chrome` | Which browser to use for test execution |
| `HEADLESS` | `true`, `false` | `false` | Run browser without GUI (recommended for CI/CD) |

**When to use:**
- Set `HEADLESS=true` in CI/CD pipelines for faster, resource-efficient execution
- Use `HEADLESS=false` locally for debugging and watching tests run
- Switch `BROWSER_TYPE` to test cross-browser compatibility

#### Test Environment

| Variable | Format | Description |
|----------|--------|-------------|
| `BASE_URL` | `https://hostname.com` | The base URL of the application under test |

**Examples for different environments:**

```bash
# Local development
BASE_URL=http://localhost:3000

# Development server
BASE_URL=https://dev.testinium.com

# Staging environment
BASE_URL=https://staging.testinium.com

# Production
BASE_URL=https://testinium.com
```

#### Timeouts

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `TIMEOUT_EXPLICIT` | Integer (seconds) | `10` | Default wait timeout for explicit waits |
| `TIMEOUT_PAGE_LOAD` | Integer (seconds) | `30` | Maximum time to wait for page loads |

**Adjust timeouts based on your application:**
- **Fast, modern SPA:** 5-10 seconds explicit, 15-20 seconds page load
- **Standard web application:** 10-15 seconds explicit, 30 seconds page load
- **Slow, legacy application:** 15-20 seconds explicit, 45-60 seconds page load

#### Test Credentials (REQUIRED)

The framework supports multiple user roles for comprehensive testing:

| Variable | Purpose |
|----------|---------|
| `ADMIN_USERNAME` | Administrator account for privileged operations |
| `ADMIN_PASSWORD` | Administrator password |
| `POS_MANAGER_USERNAME` | Point-of-Sale manager role |
| `POS_MANAGER_PASSWORD` | POS manager password |
| `SALES_MANAGER_USERNAME` | Sales manager role |
| `SALES_MANAGER_PASSWORD` | Sales manager password |
| `TEST_USERNAME` | Generic test user account |
| `TEST_PASSWORD` | Generic test user password |

⚠️ **SECURITY WARNING:** Never commit the `.env` file to version control. The `.env` file is already included in `.gitignore` to prevent accidental commits.

#### Reporting

| Variable | Options | Default | Description |
|----------|---------|---------|-------------|
| `SCREENSHOTS_ON_FAILURE` | `true`, `false` | `true` | Automatically capture screenshots when tests fail |

**Source:** `.env.example:1-31`

### Security Best Practices

1. **Verify .gitignore:** Ensure `.env` is listed in your `.gitignore` file

   ```bash
   # Check if .env is ignored
   git check-ignore .env
   # Should output: .env
   ```

2. **Use Secrets Management in CI/CD:**
   - **GitHub Actions:** Use encrypted secrets
   - **GitLab CI:** Use protected variables
   - **Jenkins:** Use credentials plugin
   - **Azure DevOps:** Use variable groups with secret variables

3. **Rotate Credentials Regularly:** Change test account passwords periodically

4. **Use Dedicated Test Accounts:** Never use production credentials in automated tests

5. **Limit Permissions:** Test accounts should have minimum necessary permissions

## Test Configuration File (config.yaml)

The `config.yaml` file provides structured configuration for the test framework with comprehensive documentation and examples.

### Location and Purpose

- **File:** `config/config.yaml`
- **Purpose:** Framework defaults, structured settings, and configuration documentation
- **When to modify:** Changing framework-wide defaults or adding new configuration options

### Configuration Structure

#### Browser Settings

```yaml
browser:
  type: chrome  # Options: chrome, firefox
  headless: false  # Set to true for CI/CD environments
  window_size: [1920, 1080]  # Browser window dimensions [width, height]
  implicit_wait: 0  # ALWAYS 0 - use explicit waits only
```

**Key Points:**
- `implicit_wait` is intentionally set to `0` to avoid dangerous mixing of implicit and explicit waits
- The framework uses explicit waits exclusively for more reliable and predictable test behavior
- `window_size` ensures consistent viewport across different execution environments

#### Timeout Configuration

```yaml
timeouts:
  explicit: 10  # Default explicit wait timeout in seconds
  page_load: 30  # Maximum time to wait for page load
  element_presence: 5  # Timeout for element presence in DOM
  clickability: 3  # Timeout for element to become clickable
```

**Timeout Usage:**
- `explicit`: Default for most `wait_for_*` operations
- `page_load`: Applied when navigating to new pages
- `element_presence`: Quick checks for element existence
- `clickability`: Waiting for buttons, links to become interactive

#### Application Settings

```yaml
application:
  base_url: ${BASE_URL:https://testinium.example.com}
  login_url: ${BASE_URL:https://testinium.example.com}/login
  web_table_url: ${BASE_URL:https://testinium.example.com}/web-tables
  empl_title: "Employee Management"
```

**Environment Variable Interpolation:**
- Syntax: `${VAR_NAME}` - Required variable (fails if not set)
- Syntax: `${VAR_NAME:default}` - Variable with fallback default
- Example: `${BASE_URL:https://testinium.example.com}` uses `BASE_URL` from environment, or falls back to the default

#### Credentials Configuration

```yaml
credentials:
  # Generic test user
  username: ${TEST_USERNAME}
  password: ${TEST_PASSWORD}
  
  # Role-specific credentials
  sales_manager_username: ${SALES_MANAGER_USERNAME}
  sales_manager_password: ${SALES_MANAGER_PASSWORD}
  
  pos_manager_username: ${POS_MANAGER_USERNAME}
  pos_manager_password: ${POS_MANAGER_PASSWORD}
```

**Security Note:** All credentials **must** be loaded from environment variables. Never hardcode credentials in `config.yaml`.

#### Reporting Settings

```yaml
reporting:
  screenshot_on_failure: true
  output_directory: reports/
  formats:
    - json
    - html
    - allure
  screenshot_directory: reports/screenshots/
```

**Report Formats:**
- **json:** Behave JSON output for custom processing
- **html:** Human-readable HTML report
- **allure:** Enhanced reporting with Allure framework

### Complete Annotated Example

Here's a complete `config.yaml` with explanations:

```yaml
# =============================================================================
# Test Configuration for Python Behave Test Automation Framework
# =============================================================================

# Browser Configuration
browser:
  type: chrome                 # Browser choice: chrome or firefox
  headless: false              # GUI mode for local debugging
  window_size: [1920, 1080]    # Full HD resolution
  implicit_wait: 0             # Disabled - use explicit waits only

# Timeout Configuration (in seconds)
timeouts:
  explicit: 10                 # Default wait timeout
  page_load: 30                # Page navigation timeout
  element_presence: 5          # Element existence check
  clickability: 3              # Interactive element wait

# Application Configuration
application:
  base_url: ${BASE_URL:https://testinium.example.com}
  login_url: ${BASE_URL:https://testinium.example.com}/login
  web_table_url: ${BASE_URL:https://testinium.example.com}/web-tables
  empl_title: "Employee Management"

# Credentials (loaded from environment)
credentials:
  username: ${TEST_USERNAME}
  password: ${TEST_PASSWORD}
  sales_manager_username: ${SALES_MANAGER_USERNAME}
  sales_manager_password: ${SALES_MANAGER_PASSWORD}
  pos_manager_username: ${POS_MANAGER_USERNAME}
  pos_manager_password: ${POS_MANAGER_PASSWORD}

# Reporting Configuration
reporting:
  screenshot_on_failure: true
  output_directory: reports/
  formats:
    - json
    - html
    - allure
  screenshot_directory: reports/screenshots/
```

**Source:** `config/config.yaml:1-162`

### When to Modify config.yaml vs .env

**Modify config.yaml when:**
- Changing framework-wide defaults
- Adding new configuration sections
- Updating structural settings (report formats, directories)
- Documenting configuration options

**Modify .env when:**
- Setting environment-specific values (URLs, timeouts)
- Providing secrets (credentials)
- Overriding defaults for local development
- Customizing per developer or CI environment

## Behave Configuration

The `behave.ini` file controls test execution behavior, output formats, and reporting options for the Behave BDD framework.

### Purpose and Location

- **File:** `behave.ini` (project root)
- **Purpose:** Test execution defaults, output formatting, CI/CD integration
- **Format:** INI-style configuration file

### Key Configuration Sections

#### Output Formats

```ini
[behave]
format = pretty  # Default console output format
junit = true     # Generate JUnit XML for CI/CD
junit_directory = reports/junit
```

**Available Formats:**
- `pretty`: Human-readable console output with color
- `json`: Machine-readable JSON for custom processing
- `plain`: Simple text output without color
- `progress`: Minimal output showing dots for pass/fail

#### Default Tags

```ini
tags = @Smoke  # Run only tests tagged with @Smoke by default
```

**Override on command line:**
```bash
behave --tags=@Login        # Run only login tests
behave --tags='not @WIP'    # Exclude work-in-progress tests
```

#### Logging Configuration

```ini
logging_level = INFO
logging_format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
log_capture = true
```

#### Screenshot and Allure Configuration

```ini
[behave.userdata]
allure_results_dir = reports/allure-results
screenshot_dir = reports/screenshots
```

**Source:** `behave.ini:1-200`

### When to Modify behave.ini

**Modify behave.ini when:**
- Changing default output formats
- Customizing report output directories
- Adjusting default tag filters
- Changing logging verbosity
- Adding custom formatters

**Examples:**

**For local development:**
```ini
format = pretty
show_timings = true
stdout_capture = false  # See print statements
```

**For CI/CD:**
```ini
format = progress
junit = true
junit_directory = reports/junit
```

## Configuration Verification

After setting up your configuration, verify everything is working correctly.

### Test Configuration Loading

```bash
# Verify configuration loads without errors
python -c "from config.test_config import get_config; config = get_config(); print('✓ Configuration loaded successfully')"
```

**Expected output:**
```
✓ Configuration loaded successfully
```

### Verify Environment Variables

```bash
# Check if .env file is being loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f\"BASE_URL: {os.getenv('BASE_URL')}\")"
```

**Expected output:**
```
BASE_URL: https://your-test-environment.com
```

### Run Dry-Run to Validate Setup

```bash
# Validate feature files and step definitions without executing tests
behave --dry-run
```

**Expected output:**
```
Feature: Login
  Scenario: Valid user login
    Given I navigate to login page ... untested
    When I enter valid credentials ... untested
    Then I should see dashboard ... untested

0 features passed, 0 failed, 0 skipped, 10 untested
0 scenarios passed, 0 failed, 0 skipped, 61 untested
0 steps passed, 0 failed, 0 skipped, 0 undefined, 183 untested
```

### Test Browser Launches

```bash
# Run a single quick test to verify browser configuration
behave --tags=@Smoke --dry-run=false features/Login.feature
```

This will actually launch the browser and verify your WebDriver configuration is working.

## Common Configuration Patterns

### Local Development Configuration

Recommended settings for local development:

**.env:**
```bash
BROWSER_TYPE=chrome
HEADLESS=false
BASE_URL=http://localhost:3000
TIMEOUT_EXPLICIT=15
SCREENSHOTS_ON_FAILURE=true
```

**Why:**
- Visible browser for watching test execution
- Longer timeouts for stepping through with debugger
- Screenshots help diagnose local issues

### CI/CD Configuration

Recommended settings for continuous integration:

**.env (or CI environment variables):**
```bash
BROWSER_TYPE=chrome
HEADLESS=true
BASE_URL=https://staging.testinium.com
TIMEOUT_EXPLICIT=10
TIMEOUT_PAGE_LOAD=30
SCREENSHOTS_ON_FAILURE=true
```

**behave.ini adjustments:**
```ini
format = progress
junit = true
junit_directory = reports/junit
show_skipped = false
stdout_capture = true
```

**Why:**
- Headless mode for faster execution and no display requirements
- JUnit XML for test result integration
- Progress format for cleaner CI logs
- Screenshots captured for failure diagnosis

### Different Environment Configurations

**Development:**
```bash
BASE_URL=https://dev.testinium.com
TEST_USERNAME=dev.tester@example.com
```

**Staging:**
```bash
BASE_URL=https://staging.testinium.com
TEST_USERNAME=staging.tester@example.com
```

**Production (for smoke tests):**
```bash
BASE_URL=https://testinium.com
TEST_USERNAME=prod.readonly@example.com
TIMEOUT_EXPLICIT=20  # Production might be slower
```

### Multi-Browser Testing Setup

Run the same tests across different browsers:

```bash
# Run with Chrome
BROWSER_TYPE=chrome behave

# Run with Firefox
BROWSER_TYPE=firefox behave
```

Or create browser-specific .env files:

```bash
# .env.chrome
BROWSER_TYPE=chrome
HEADLESS=false

# .env.firefox
BROWSER_TYPE=firefox
HEADLESS=false

# Load specific configuration
env $(cat .env.chrome | xargs) behave
env $(cat .env.firefox | xargs) behave
```

## Troubleshooting

### Issue: .env File Not Loaded

**Symptoms:**
- Configuration errors about missing credentials
- `KeyError` for environment variables
- Tests use default values instead of your .env values

**Cause:**
- `python-dotenv` package not installed
- `.env` file in wrong location
- Incorrect variable names

**Solution:**

1. Verify python-dotenv is installed:
   ```bash
   pip show python-dotenv
   ```

2. Check .env file location:
   ```bash
   ls -la .env
   # Should be in project root, next to README.md
   ```

3. Verify file is being loaded:
   ```bash
   python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('BASE_URL'))"
   ```

### Issue: config.yaml Parsing Errors

**Symptoms:**
- `yaml.scanner.ScannerError` or `yaml.parser.ParserError`
- Tests fail to start with YAML syntax errors
- Configuration values not recognized

**Cause:**
- Invalid YAML syntax
- Incorrect indentation
- Missing colons or quotes

**Solution:**

1. Validate YAML syntax:
   ```bash
   python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
   ```

2. Common YAML mistakes:
   ```yaml
   # ❌ Wrong - inconsistent indentation
   browser:
     type: chrome
       headless: false
   
   # ✓ Correct - consistent 2-space indentation
   browser:
     type: chrome
     headless: false
   
   # ❌ Wrong - missing space after colon
   browser:
     type:chrome
   
   # ✓ Correct - space after colon
   browser:
     type: chrome
   ```

3. Use a YAML validator: https://www.yamllint.com/

### Issue: Environment Variable Interpolation Not Working

**Symptoms:**
- Literal `${VARIABLE}` appears in configuration instead of actual value
- Tests fail with URLs containing `${BASE_URL}`
- Credentials not loaded from environment

**Cause:**
- Environment variable not set
- Incorrect interpolation syntax
- Configuration loaded before environment variables

**Solution:**

1. Check variable interpolation syntax:
   ```yaml
   # ✓ Correct - required variable
   base_url: ${BASE_URL}
   
   # ✓ Correct - variable with default
   base_url: ${BASE_URL:https://default.com}
   
   # ❌ Wrong - shell syntax (this is YAML, not bash)
   base_url: $BASE_URL
   ```

2. Verify variable is set:
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f'BASE_URL={os.getenv(\"BASE_URL\")}')"
   ```

3. Check load order in code:
   ```python
   # ✓ Correct order
   from dotenv import load_dotenv
   load_dotenv()  # Load .env first
   from config.test_config import get_config  # Then load config
   
   # ❌ Wrong order
   from config.test_config import get_config  # Config loads before .env
   from dotenv import load_dotenv
   load_dotenv()  # Too late
   ```

### Issue: Browser Driver Not Found

**Symptoms:**
- `WebDriverException`: 'chromedriver' executable needs to be in PATH
- `WebDriverException`: Unable to find a matching set of capabilities
- Tests fail immediately when trying to launch browser

**Cause:**
- WebDriver not installed
- WebDriver version doesn't match browser version
- WebDriver not in system PATH

**Solution:**

1. The framework uses `webdriver-manager` for automatic driver management:
   ```bash
   pip install webdriver-manager
   ```

2. Verify webdriver-manager is configured:
   ```python
   # In utilities/driver_manager.py, this should handle drivers automatically
   from webdriver_manager.chrome import ChromeDriverManager
   from selenium.webdriver.chrome.service import Service
   
   service = Service(ChromeDriverManager().install())
   ```

3. Manual driver installation (if automatic fails):
   ```bash
   # Chrome
   # Download from: https://chromedriver.chromium.org/
   # Add to PATH
   
   # Firefox
   # Download from: https://github.com/mozilla/geckodriver/releases
   # Add to PATH
   ```

4. Check browser and driver compatibility:
   ```bash
   # Check Chrome version
   google-chrome --version  # Linux
   chrome --version  # Mac
   
   # Check ChromeDriver version
   chromedriver --version
   
   # Versions should match (e.g., Chrome 120.x needs ChromeDriver 120.x)
   ```

### Issue: Timeout Too Short

**Symptoms:**
- Tests fail with `TimeoutException`
- "Element not found" or "Element not clickable" errors
- Tests work locally but fail in CI/CD

**Cause:**
- Application is slower than configured timeout
- Network latency in test environment
- Explicit wait timeout too aggressive

**Solution:**

1. Increase explicit wait timeout:
   ```bash
   # In .env file
   TIMEOUT_EXPLICIT=20  # Increase from 10 to 20 seconds
   ```

2. Increase page load timeout:
   ```bash
   TIMEOUT_PAGE_LOAD=60  # Increase from 30 to 60 seconds
   ```

3. For specific slow operations, use longer waits in test code:
   ```python
   # In step definitions or page objects
   from utilities.wait_helpers import WaitHelpers
   
   # Use longer timeout for specific slow element
   wait_helpers.wait_for_element(locator, timeout=30)  # Override default
   ```

4. Check if issue is environment-specific:
   ```bash
   # Test with very long timeout to confirm timeout is the issue
   TIMEOUT_EXPLICIT=60 behave --tags=@Smoke
   ```

### Issue: Tests Use Wrong Configuration

**Symptoms:**
- Tests connect to wrong environment
- Wrong browser launched
- Unexpected timeout values

**Cause:**
- Configuration precedence misunderstood
- Environment variables not properly set
- Configuration cached

**Solution:**

1. Understand precedence: Environment variables → config.yaml → defaults

2. Force reset configuration:
   ```python
   from config.test_config import reset_config
   reset_config()  # Clear cached configuration
   ```

3. Check which configuration is actually loaded:
   ```bash
   python -c "from config.test_config import get_config; config = get_config(); print(f'Browser: {config.browser.type}'); print(f'Base URL: {config.application.base_url}'); print(f'Timeout: {config.timeouts.explicit}')"
   ```

4. Verify environment variables take precedence:
   ```bash
   # Set environment variable
   export BROWSER_TYPE=firefox
   
   # Should show firefox, not chrome
   python -c "from config.test_config import get_config; print(get_config().browser.type)"
   ```

## Next Steps

Now that your configuration is set up, you're ready to run your first test!

**Continue to:** [Running Your First Test](first-test.md)

**See also:**
- [Advanced Configuration Management](../guides/configuration-management.md) - Learn about configuration precedence, environment-specific configs, and secrets management
- [Configuration Options Reference](../reference/configuration-options.md) - Complete reference of all configuration options
- [Environment Variables Reference](../reference/environment-variables.md) - Detailed documentation of all environment variables
- [Behave Configuration Reference](../reference/behave-configuration.md) - Complete behave.ini options

**Need help?** Check the [Troubleshooting Guide](../troubleshooting/configuration-issues.md) for more configuration-related issues and solutions.
