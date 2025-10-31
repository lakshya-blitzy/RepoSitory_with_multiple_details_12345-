# Environment Variables Reference

Complete reference for all environment variables supported by the Testinium Python test automation framework.

## Overview

Environment variables provide a secure and flexible way to configure the test framework without hardcoding sensitive information like credentials or environment-specific URLs. The framework uses the `python-dotenv` library to load variables from a `.env` file in the project root.

### .env File Purpose

The `.env` file allows developers to maintain environment-specific configuration locally without committing sensitive data to version control. This file should contain all necessary credentials, URLs, and runtime settings.

**SECURITY WARNING:** The `.env` file contains sensitive credentials and **MUST NEVER** be committed to version control. Always add `.env` to your `.gitignore` file.

**Source:** `.env.example` (template for environment variables)

### python-dotenv Integration

The framework automatically loads environment variables from the `.env` file using `python-dotenv` during configuration initialization. This happens before the YAML configuration is parsed, ensuring environment variables are available for interpolation.

**Source:** `config/test_config.py:182` (load_dotenv() call in Config.__init__)

### How It Works

1. **Local Development**: Create a `.env` file in the project root by copying `.env.example`
2. **Configuration Loading**: `python-dotenv` loads variables from `.env` into `os.environ`
3. **Variable Interpolation**: `config.yaml` references variables using `${VAR_NAME}` syntax
4. **Runtime Substitution**: Variables are substituted when configuration is loaded

**Source:** `config/test_config.py:265-309` (environment variable substitution logic)

### Relationship to config.yaml

Environment variables are referenced in `config/config.yaml` using interpolation syntax. This allows the YAML configuration to remain environment-agnostic while actual values come from environment-specific sources.

**Interpolation Syntax:**

| Syntax | Behavior | Example |
|--------|----------|---------|
| `${VAR_NAME}` | **Required variable** - Raises error if not set (except credentials) | `${BASE_URL}` |
| `${VAR_NAME:default}` | **Optional variable with default** - Uses default if not set | `${BASE_URL:https://testinium.example.com}` |

**Special Credential Handling**: Variables ending with `USERNAME` or `PASSWORD` are treated as optional. If not set, they default to an empty string and log a warning rather than raising an error. This allows test scenarios to gracefully skip tests requiring missing credentials.

**Source:** `config/test_config.py:300-304` (credential substitution behavior)

## Environment Variables Reference

### Browser Configuration

These variables override browser settings from `config.yaml`, providing runtime control over browser behavior.

| Variable Name | Purpose | Required/Optional | Default Value | Example | Used By |
|---------------|---------|-------------------|---------------|---------|---------|
| `BROWSER_TYPE` | Browser type for test execution | Optional | `chrome` (from config.yaml) | `chrome`, `firefox` | `config/test_config.py` BrowserConfig |
| `HEADLESS` | Run browser in headless mode | Optional | `false` (from config.yaml) | `true` (CI/CD), `false` (local) | `config/test_config.py` BrowserConfig |

#### BROWSER_TYPE

**Purpose:** Overrides the browser type specified in `config.yaml` at runtime. Useful for executing the same test suite against different browsers without modifying the configuration file.

**Valid Values:**
- `chrome` - Google Chrome browser (default)
- `firefox` - Mozilla Firefox browser

**Example:**
```bash
# Run tests in Firefox instead of default Chrome
export BROWSER_TYPE=firefox
behave
```

**Source:** `config/config.yaml:26` (browser.type default value)

#### HEADLESS

**Purpose:** Controls whether the browser runs with a visible GUI or in headless mode. Essential for CI/CD pipelines where no display is available.

**Valid Values:**
- `true` - Headless mode (no visible browser window)
- `false` - Normal mode with visible browser window

**Use Cases:**
- **CI/CD Pipelines**: Set to `true` for faster execution and compatibility with headless environments
- **Local Debugging**: Set to `false` to watch browser interactions during test development

**Example:**
```bash
# Enable headless mode for CI/CD
export HEADLESS=true
behave
```

**Source:** `config/config.yaml:29` (browser.headless default value)

### Application URLs

Application URL configuration for environment-specific deployments (dev, staging, production).

| Variable Name | Purpose | Required/Optional | Default Value | Example | Used By |
|---------------|---------|-------------------|---------------|---------|---------|
| `BASE_URL` | Application base URL | **Required** | `https://testinium.example.com` (fallback in config.yaml) | `https://testinium-dev.example.com` | `config/test_config.py` ApplicationConfig, all test scenarios |

#### BASE_URL

**Purpose:** Specifies the base URL of the application under test. This is the most critical environment variable as it determines which environment tests execute against.

**Required:** Yes - Tests cannot execute without a valid application URL.

**Environment-Specific Examples:**

| Environment | Example Value |
|-------------|---------------|
| Local Development | `http://localhost:3000` |
| Development | `https://testinium-dev.example.com` |
| Staging | `https://testinium-staging.example.com` |
| Production | `https://testinium.example.com` |

**Usage in config.yaml:**
```yaml
application:
  base_url: ${BASE_URL:https://testinium.example.com}
  login_url: ${BASE_URL:https://testinium.example.com}/login
  web_table_url: ${BASE_URL:https://testinium.example.com}/web-tables
```

**Example:**
```bash
# Point tests to staging environment
export BASE_URL=https://testinium-staging.example.com
behave
```

**Source:** `config/config.yaml:71` (base_url interpolation), `.env.example:10` (example value)

### Timeout Configuration

Timeout overrides for WebDriver waits, providing runtime control over wait durations.

| Variable Name | Purpose | Required/Optional | Default Value | Example | Used By |
|---------------|---------|-------------------|---------------|---------|---------|
| `TIMEOUT_EXPLICIT` | Default explicit wait timeout in seconds | Optional | `10` (from config.yaml) | `15` | `config/test_config.py` TimeoutConfig, `utilities/wait_helpers.py` |
| `TIMEOUT_PAGE_LOAD` | Page load timeout in seconds | Optional | `30` (from config.yaml) | `60` | `config/test_config.py` TimeoutConfig, WebDriver configuration |

#### TIMEOUT_EXPLICIT

**Purpose:** Overrides the default explicit wait timeout used by all WebDriverWait instances throughout the test suite.

**Use Cases:**
- **Slow Environments**: Increase timeout for slow test environments or heavy application loads
- **Fast Environments**: Decrease timeout for faster failure detection in well-performing environments

**Example:**
```bash
# Increase explicit wait timeout for slow staging environment
export TIMEOUT_EXPLICIT=15
behave
```

**Source:** `config/config.yaml:48` (timeouts.explicit default value)

#### TIMEOUT_PAGE_LOAD

**Purpose:** Overrides the maximum time the WebDriver will wait for a page to finish loading before throwing an error.

**Example:**
```bash
# Increase page load timeout for slow network conditions
export TIMEOUT_PAGE_LOAD=60
behave
```

**Source:** `config/config.yaml:52` (timeouts.page_load default value)

### Test Credentials

User credentials for authentication testing. These are the most security-sensitive environment variables.

!!! warning "Security Critical"
    All credential variables contain sensitive authentication information. They **MUST**:
    
    - Be loaded from secure sources (CI/CD secrets, environment variables, `.env` file)
    - **NEVER** be hardcoded in source files
    - **NEVER** be committed to version control
    - Be masked in logs and test reports

| Variable Name | Purpose | Required/Optional | Default Value | Example | Used By |
|---------------|---------|-------------------|---------------|---------|---------|
| `TEST_USERNAME` | Default test user email/username | **Required for most tests** | Empty string (logs warning) | `testuser@example.com` | Login tests, general test scenarios |
| `TEST_PASSWORD` | Default test user password | **Required for most tests** | Empty string (logs warning) | `SecurePass123!` | Login tests, general test scenarios |
| `ADMIN_USERNAME` | Admin role user email/username | Optional (for admin tests) | Empty string (logs warning) | `admin@example.com` | Admin-specific test scenarios |
| `ADMIN_PASSWORD` | Admin role user password | Optional (for admin tests) | Empty string (logs warning) | `AdminPass123!` | Admin-specific test scenarios |
| `POS_MANAGER_USERNAME` | POS Manager role username | Optional (for POS tests) | Empty string (logs warning) | `posmanager@example.com` | POS management test scenarios |
| `POS_MANAGER_PASSWORD` | POS Manager role password | Optional (for POS tests) | Empty string (logs warning) | `PosPass123!` | POS management test scenarios |
| `SALES_MANAGER_USERNAME` | Sales Manager role username | Optional (for sales tests) | Empty string (logs warning) | `salesmanager@example.com` | Sales management test scenarios |
| `SALES_MANAGER_PASSWORD` | Sales Manager role password | Optional (for sales tests) | Empty string (logs warning) | `SalesPass123!` | Sales management test scenarios |

#### Credential Substitution Behavior

The framework handles missing credential environment variables gracefully:

1. **Variable Not Set**: If a credential variable (ending with `USERNAME` or `PASSWORD`) is not set, the configuration system:
   - Logs a warning message indicating which credential is missing
   - Substitutes an empty string (`''`) instead of raising an error
   - Allows the test suite to start even without all credentials

2. **Test Execution**: Tests requiring missing credentials will typically:
   - Skip gracefully if the test framework detects empty credentials
   - Fail with clear authentication errors if the test attempts login with empty credentials

3. **Validation**: The `_validate_credentials()` method logs warnings for each missing credential set:

**Source:** `config/test_config.py:300-304` (credential substitution logic), `config/test_config.py:311-335` (credential validation warnings)

#### TEST_USERNAME and TEST_PASSWORD

**Purpose:** Default test user credentials for general authentication testing and scenarios that don't require specific roles.

**Required:** Yes - These credentials are required for most test scenarios as they represent the standard test user account.

**Validation:** If not set, the configuration logs a warning:
```
WARNING: Default test credentials not configured. Set TEST_USERNAME and TEST_PASSWORD environment variables.
```

**Example:**
```bash
export TEST_USERNAME=testuser@example.com
export TEST_PASSWORD=SecureTestPassword123!
```

**Usage in config.yaml:**
```yaml
credentials:
  username: ${TEST_USERNAME}
  password: ${TEST_PASSWORD}
```

**Source:** `.env.example:26-27`, `config/config.yaml:97-98`, `config/test_config.py:318-322`

#### ADMIN_USERNAME and ADMIN_PASSWORD

**Purpose:** Administrative user credentials for testing admin-specific functionality and elevated permission scenarios.

**Required:** Optional - Only needed for test scenarios requiring administrative access.

**Example:**
```bash
export ADMIN_USERNAME=admin@example.com
export ADMIN_PASSWORD=SecureAdminPassword123!
```

**Source:** `.env.example:17-18`

#### POS_MANAGER_USERNAME and POS_MANAGER_PASSWORD

**Purpose:** Point-of-Sale (POS) Manager role credentials for testing POS management workflows and role-based access control.

**Required:** Optional - Only needed for POS management test scenarios tagged with `@PosManager`.

**Validation:** If not set, the configuration logs a warning:
```
WARNING: POS manager credentials not configured. Set POS_MANAGER_USERNAME and POS_MANAGER_PASSWORD for role-based tests.
```

**Example:**
```bash
export POS_MANAGER_USERNAME=posmanager@example.com
export POS_MANAGER_PASSWORD=SecurePosPassword123!
```

**Usage in config.yaml:**
```yaml
credentials:
  pos_manager_username: ${POS_MANAGER_USERNAME}
  pos_manager_password: ${POS_MANAGER_PASSWORD}
```

**Source:** `.env.example:20-21`, `config/config.yaml:109-110`, `config/test_config.py:331-335`

#### SALES_MANAGER_USERNAME and SALES_MANAGER_PASSWORD

**Purpose:** Sales Manager role credentials for testing sales workflows and sales-specific role permissions.

**Required:** Optional - Only needed for sales management test scenarios tagged with `@SalesManager`.

**Validation:** If not set, the configuration logs a warning:
```
WARNING: Sales manager credentials not configured. Set SALES_MANAGER_USERNAME and SALES_MANAGER_PASSWORD for role-based tests.
```

**Example:**
```bash
export SALES_MANAGER_USERNAME=salesmanager@example.com
export SALES_MANAGER_PASSWORD=SecureSalesPassword123!
```

**Usage in config.yaml:**
```yaml
credentials:
  sales_manager_username: ${SALES_MANAGER_USERNAME}
  sales_manager_password: ${SALES_MANAGER_PASSWORD}
```

**Source:** `.env.example:23-24`, `config/config.yaml:103-104`, `config/test_config.py:324-329`

### Reporting Configuration

Reporting behavior configuration for screenshot capture and test artifact generation.

| Variable Name | Purpose | Required/Optional | Default Value | Example | Used By |
|---------------|---------|-------------------|---------------|---------|---------|
| `SCREENSHOTS_ON_FAILURE` | Enable automatic screenshot capture on test failures | Optional | `true` (from config.yaml) | `true`, `false` | `features/environment.py` after_scenario hook |

#### SCREENSHOTS_ON_FAILURE

**Purpose:** Controls whether screenshots are automatically captured when a test scenario fails. This is essential for debugging failed tests, especially in CI/CD environments where you cannot visually observe test execution.

**Valid Values:**
- `true` - Enable automatic screenshot capture on failures (recommended)
- `false` - Disable screenshot capture (useful for reducing artifact size in some scenarios)

**Use Cases:**
- **CI/CD Pipelines**: Keep enabled (`true`) to capture failure evidence
- **Local Debugging**: Can be disabled (`false`) if you're watching tests execute visually
- **Storage Constraints**: Disable if screenshot storage becomes problematic

**Example:**
```bash
# Disable screenshots for local development
export SCREENSHOTS_ON_FAILURE=false
behave
```

**Source:** `.env.example:30`, `config/config.yaml:121` (screenshot_on_failure configuration)

## Configuration Precedence

Understanding how environment variables interact with `config.yaml` is critical for proper configuration management.

### Precedence Order (Highest to Lowest)

1. **Environment Variables** (`.env` file or system environment) - **HIGHEST PRIORITY**
2. **config.yaml Default Values** (when using `${VAR:default}` syntax)
3. **config.yaml Static Values** (when no interpolation is used)

### How Precedence Works

When `config.yaml` uses environment variable interpolation syntax:

**Scenario 1: Variable with Default**
```yaml
base_url: ${BASE_URL:https://testinium.example.com}
```
- If `BASE_URL` environment variable is set → Uses environment variable value
- If `BASE_URL` is not set → Uses default value `https://testinium.example.com`

**Scenario 2: Required Variable**
```yaml
username: ${TEST_USERNAME}
```
- If `TEST_USERNAME` is set → Uses environment variable value
- If `TEST_USERNAME` is not set and variable ends with USERNAME/PASSWORD → Uses empty string, logs warning
- If `TEST_USERNAME` is not set and variable doesn't end with USERNAME/PASSWORD → Raises ValueError

**Scenario 3: Static Value (No Interpolation)**
```yaml
browser:
  type: chrome
```
- Always uses static value from `config.yaml`
- No environment variable override possible (unless the YAML value itself uses interpolation)

**Source:** `config/test_config.py:265-309` (environment variable substitution implementation)

### Precedence Examples

**Example 1: Override Browser Type**
```bash
# config.yaml has: browser.type: chrome
# Override to Firefox for this test run
export BROWSER_TYPE=firefox
behave
# Result: Tests run in Firefox
```

**Example 2: Environment-Specific URL**
```bash
# config.yaml has: base_url: ${BASE_URL:https://testinium.example.com}
# Point to staging environment
export BASE_URL=https://testinium-staging.example.com
behave
# Result: Tests execute against staging environment
```

**Example 3: Missing Optional Credential**
```bash
# config.yaml has: pos_manager_username: ${POS_MANAGER_USERNAME}
# POS_MANAGER_USERNAME is not set
behave --tags=@PosManager
# Result: Warning logged, credential is empty string, POS tests may skip or fail
```

## Security and Secrets Management

Proper credential management is critical for both security and operational excellence.

### Required Credentials

The following credentials are required for the test suite to execute successfully:

| Credential Set | Variables | Purpose | Impact if Missing |
|----------------|-----------|---------|-------------------|
| **Test User** | `TEST_USERNAME`, `TEST_PASSWORD` | Default authentication for most tests | Most test scenarios will fail authentication |
| **Admin User** (optional) | `ADMIN_USERNAME`, `ADMIN_PASSWORD` | Administrative operations testing | Only admin-specific tests affected |
| **POS Manager** (optional) | `POS_MANAGER_USERNAME`, `POS_MANAGER_PASSWORD` | POS role-based testing | Only POS management tests affected |
| **Sales Manager** (optional) | `SALES_MANAGER_USERNAME`, `SALES_MANAGER_PASSWORD` | Sales role-based testing | Only sales management tests affected |

### Local Development Best Practices

#### Step 1: Create .env File

Copy the example template and fill in actual credentials:

```bash
# Copy template
cp .env.example .env

# Edit .env file with real credentials
# NEVER commit this file to version control
```

#### Step 2: Verify .gitignore

Ensure `.env` is listed in `.gitignore` to prevent accidental commits:

```bash
# Check if .env is ignored
git check-ignore .env
# Should output: .env

# If not ignored, add to .gitignore
echo ".env" >> .gitignore
```

#### Step 3: Load and Verify

The framework automatically loads `.env` via `python-dotenv`. Verify variables are loaded:

```python
# Test script to verify environment variables
from dotenv import load_dotenv
import os

load_dotenv()
print(f"BASE_URL: {os.getenv('BASE_URL')}")
print(f"TEST_USERNAME: {os.getenv('TEST_USERNAME')}")
# Do NOT print passwords in production!
```

**Source:** `config/test_config.py:182` (automatic .env loading)

### CI/CD Secrets Management

Different CI/CD platforms provide secure ways to inject environment variables without exposing them in logs or source code.

#### GitHub Actions

Use GitHub Secrets to store credentials:

```yaml
# .github/workflows/tests.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Tests
        env:
          BASE_URL: ${{ secrets.BASE_URL }}
          TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
          TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
          SALES_MANAGER_USERNAME: ${{ secrets.SALES_MANAGER_USERNAME }}
          SALES_MANAGER_PASSWORD: ${{ secrets.SALES_MANAGER_PASSWORD }}
          POS_MANAGER_USERNAME: ${{ secrets.POS_MANAGER_USERNAME }}
          POS_MANAGER_PASSWORD: ${{ secrets.POS_MANAGER_PASSWORD }}
          HEADLESS: true
        run: |
          pip install -r requirements.txt
          behave
```

**Configuration:**
1. Navigate to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each credential as a separate secret
4. Reference in workflow using `${{ secrets.SECRET_NAME }}` syntax

**Source:** See `docs/deployment/github-actions.md` for complete GitHub Actions setup

#### Jenkins

Use Jenkins Credentials plugin:

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        BASE_URL = credentials('testinium-base-url')
        TEST_USERNAME = credentials('testinium-test-username')
        TEST_PASSWORD = credentials('testinium-test-password')
        SALES_MANAGER_USERNAME = credentials('testinium-sales-username')
        SALES_MANAGER_PASSWORD = credentials('testinium-sales-password')
        POS_MANAGER_USERNAME = credentials('testinium-pos-username')
        POS_MANAGER_PASSWORD = credentials('testinium-pos-password')
        HEADLESS = 'true'
    }
    
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'behave'
            }
        }
    }
}
```

**Configuration:**
1. Navigate to Jenkins → Credentials → System → Global credentials
2. Click "Add Credentials"
3. Select "Secret text" kind
4. Enter credential value and ID (e.g., `testinium-test-username`)
5. Reference in Jenkinsfile using `credentials('credential-id')` syntax

**Source:** See `docs/deployment/jenkins-integration.md` for complete Jenkins setup

#### GitLab CI

Use GitLab CI/CD Variables:

```yaml
# .gitlab-ci.yml
test:
  stage: test
  image: python:3.11
  variables:
    HEADLESS: "true"
  script:
    - pip install -r requirements.txt
    - behave
```

**Configuration:**
1. Navigate to project Settings → CI/CD → Variables
2. Click "Add variable"
3. Enter key (e.g., `TEST_USERNAME`) and value
4. Mark as "Protected" and "Masked" for security
5. Variables are automatically available as environment variables

**Source:** See `docs/deployment/gitlab-ci.md` for complete GitLab CI setup

#### Azure Key Vault Integration

For enterprise deployments, integrate with Azure Key Vault:

```python
# Example: Load credentials from Azure Key Vault
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

def load_secrets_from_keyvault():
    """Load secrets from Azure Key Vault into environment variables."""
    vault_url = os.getenv("AZURE_KEYVAULT_URL")
    if vault_url:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_url, credential=credential)
        
        # Load secrets
        os.environ["TEST_USERNAME"] = client.get_secret("test-username").value
        os.environ["TEST_PASSWORD"] = client.get_secret("test-password").value
        # Load other secrets...

# Call before loading configuration
load_secrets_from_keyvault()
```

### Security Best Practices

!!! danger "Critical Security Rules"
    
    **NEVER:**
    - Commit `.env` file to version control
    - Hardcode credentials in source code
    - Log credential values (even masked ones can leak information)
    - Share credentials via insecure channels (email, chat, etc.)
    - Use production credentials in test environments
    
    **ALWAYS:**
    - Use separate credentials for each environment (dev, staging, production)
    - Rotate credentials regularly (every 90 days minimum)
    - Use strong passwords (minimum 16 characters, mixed case, numbers, symbols)
    - Limit credential access to minimum required personnel
    - Audit credential usage through CI/CD logs

### Credential Rotation Procedure

When credentials change, update them in all locations:

1. **Local Development**: Update `.env` file
2. **CI/CD**: Update secrets in GitHub/Jenkins/GitLab
3. **Documentation**: Update `.env.example` with new format (but not actual values)
4. **Team Communication**: Notify team members to update their local `.env` files

## Variable Interpolation Syntax in config.yaml

The `config.yaml` file uses a special syntax to reference environment variables. Understanding this syntax is essential for creating flexible, environment-agnostic configurations.

### Syntax Reference

| Syntax | Name | Behavior | Example |
|--------|------|----------|---------|
| `${VAR_NAME}` | Required Variable | Raises `ValueError` if environment variable is not set (except credentials) | `${BASE_URL}` |
| `${VAR_NAME:default_value}` | Variable with Default | Uses `default_value` if environment variable is not set | `${BASE_URL:https://testinium.example.com}` |

### Implementation Details

**Regex Pattern:** `\$\{([^}:]+)(?::([^}]*))?\}`

The substitution logic in `config/test_config.py` uses a regular expression to find and replace environment variable placeholders:

- **Group 1**: Variable name (e.g., `BASE_URL`)
- **Group 2**: Optional default value after `:` (e.g., `https://testinium.example.com`)

**Source:** `config/test_config.py:284` (environment variable regex pattern)

### Required Variable Syntax

**Syntax:** `${VAR_NAME}`

**Behavior:**
- Looks up `VAR_NAME` in environment variables (via `os.getenv()`)
- If found: Substitutes the environment variable value
- If not found and variable name ends with `USERNAME` or `PASSWORD`: 
  - Logs warning
  - Substitutes empty string
- If not found and variable name does NOT end with `USERNAME` or `PASSWORD`:
  - Logs error
  - Raises `ValueError` with message "Required environment variable not set: VAR_NAME"

**Example:**
```yaml
credentials:
  username: ${TEST_USERNAME}
```

**Result:**
- If `TEST_USERNAME=testuser@example.com` → `username: testuser@example.com`
- If `TEST_USERNAME` not set → `username: ""` (empty string), warning logged

**Source:** `config/test_config.py:286-307` (environment variable substitution logic)

### Variable with Default Syntax

**Syntax:** `${VAR_NAME:default_value}`

**Behavior:**
- Looks up `VAR_NAME` in environment variables
- If found: Substitutes the environment variable value
- If not found: Substitutes `default_value`
- Never raises an error (always has fallback)

**Example:**
```yaml
application:
  base_url: ${BASE_URL:https://testinium.example.com}
```

**Result:**
- If `BASE_URL=https://testinium-staging.example.com` → `base_url: https://testinium-staging.example.com`
- If `BASE_URL` not set → `base_url: https://testinium.example.com` (default used)

**Source:** `config/test_config.py:296-299` (default value substitution)

### Substitution Examples

#### Example 1: Base URL with Default

**config.yaml:**
```yaml
application:
  base_url: ${BASE_URL:https://testinium.example.com}
```

**Scenario A: Environment variable set**
```bash
export BASE_URL=https://testinium-dev.example.com
```
**Result:** `base_url: https://testinium-dev.example.com`

**Scenario B: Environment variable not set**
```bash
# BASE_URL not set
```
**Result:** `base_url: https://testinium.example.com` (default used)

#### Example 2: Required Credential

**config.yaml:**
```yaml
credentials:
  username: ${TEST_USERNAME}
  password: ${TEST_PASSWORD}
```

**Scenario A: Environment variables set**
```bash
export TEST_USERNAME=testuser@example.com
export TEST_PASSWORD=SecurePass123!
```
**Result:** 
- `username: testuser@example.com`
- `password: SecurePass123!`

**Scenario B: Environment variables not set**
```bash
# TEST_USERNAME and TEST_PASSWORD not set
```
**Result:** 
- `username: ""` (empty string)
- `password: ""` (empty string)
- Warning logged: "Credential environment variable not set: TEST_USERNAME"
- Warning logged: "Credential environment variable not set: TEST_PASSWORD"

#### Example 3: Timeout Override

**config.yaml:**
```yaml
timeouts:
  explicit: ${TIMEOUT_EXPLICIT:10}
  page_load: ${TIMEOUT_PAGE_LOAD:30}
```

**Scenario A: Override explicit timeout only**
```bash
export TIMEOUT_EXPLICIT=15
# TIMEOUT_PAGE_LOAD not set
```
**Result:**
- `explicit: 15` (from environment variable)
- `page_load: 30` (from default)

## Local Development Setup

Step-by-step guide for configuring environment variables in local development.

### Step 1: Copy .env.example

Create your local `.env` file from the template:

```bash
# Navigate to project root
cd /path/to/testinium-qa-python

# Copy template
cp .env.example .env
```

**Result:** Creates `.env` file with example values that you'll customize.

### Step 2: Edit .env File

Open `.env` in your text editor and replace example values with real credentials:

```bash
# .env file content (example)

# Browser Configuration (optional - overrides config.yaml)
BROWSER_TYPE=chrome
HEADLESS=false

# Test Environment
BASE_URL=https://testinium-dev.example.com

# Timeouts (optional - overrides config.yaml)
TIMEOUT_EXPLICIT=10
TIMEOUT_PAGE_LOAD=30

# Test Credentials (REQUIRED)
TEST_USERNAME=your.email@example.com
TEST_PASSWORD=YourActualSecurePassword123!

# Role-based Credentials (optional - only if you run role-specific tests)
ADMIN_USERNAME=admin@example.com
ADMIN_PASSWORD=AdminPassword123!

POS_MANAGER_USERNAME=posmanager@example.com
POS_MANAGER_PASSWORD=PosPassword123!

SALES_MANAGER_USERNAME=salesmanager@example.com
SALES_MANAGER_PASSWORD=SalesPassword123!

# Reporting
SCREENSHOTS_ON_FAILURE=true
```

### Step 3: Verify .env is Ignored

Ensure `.env` file is in `.gitignore` to prevent accidental commits:

```bash
# Check if .env is ignored
git check-ignore .env

# Expected output: .env
# If no output, .env is NOT ignored - add it to .gitignore

# Add to .gitignore if needed
echo ".env" >> .gitignore

# Verify again
git check-ignore .env
```

### Step 4: Test Configuration Loading

Verify environment variables are loaded correctly:

```bash
# Run a simple configuration test
python -c "from config.test_config import get_config; config = get_config(); print(f'Base URL: {config.application.base_url}'); print(f'Browser: {config.browser.type}'); print(f'Username configured: {bool(config.credentials.username)}')"
```

**Expected Output:**
```
Base URL: https://testinium-dev.example.com
Browser: chrome
Username configured: True
```

**Source:** `config/test_config.py` (Config class initialization)

### Step 5: Run Tests

Execute tests to verify everything works:

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run all tests
behave

# Run specific feature
behave features/Login.feature

# Run with specific tags
behave --tags=@Login
```

### Troubleshooting Local Setup

#### Issue: Configuration not loading .env file

**Symptoms:** Environment variables from `.env` not being used

**Solution:**
```bash
# Verify .env file exists
ls -la .env

# Verify python-dotenv is installed
pip show python-dotenv

# If not installed
pip install python-dotenv
```

#### Issue: Credentials not working

**Symptoms:** Authentication failures, empty credential warnings

**Solution:**
1. Verify `.env` file has correct variable names (case-sensitive)
2. Check for trailing spaces in variable values
3. Ensure no quotes around values unless actually needed
4. Verify credentials are valid in the test environment

**Example of common mistake:**
```bash
# WRONG: Extra quotes
TEST_USERNAME="testuser@example.com"

# CORRECT: No quotes needed
TEST_USERNAME=testuser@example.com
```

## CI/CD Integration Examples

Comprehensive examples for major CI/CD platforms showing how to securely inject environment variables.

### GitHub Actions

Complete workflow file with all environment variables:

```yaml
# .github/workflows/tests.yml
name: Testinium Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2 AM UTC

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
        browser: [chrome, firefox]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run tests
        env:
          # Application Configuration
          BASE_URL: ${{ secrets.BASE_URL }}
          
          # Browser Configuration
          BROWSER_TYPE: ${{ matrix.browser }}
          HEADLESS: true
          
          # Timeout Configuration
          TIMEOUT_EXPLICIT: 15
          TIMEOUT_PAGE_LOAD: 60
          
          # Test Credentials
          TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
          TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
          ADMIN_USERNAME: ${{ secrets.ADMIN_USERNAME }}
          ADMIN_PASSWORD: ${{ secrets.ADMIN_PASSWORD }}
          POS_MANAGER_USERNAME: ${{ secrets.POS_MANAGER_USERNAME }}
          POS_MANAGER_PASSWORD: ${{ secrets.POS_MANAGER_PASSWORD }}
          SALES_MANAGER_USERNAME: ${{ secrets.SALES_MANAGER_USERNAME }}
          SALES_MANAGER_PASSWORD: ${{ secrets.SALES_MANAGER_PASSWORD }}
          
          # Reporting Configuration
          SCREENSHOTS_ON_FAILURE: true
        run: |
          behave --format json --outfile reports/cucumber.json
          behave --format html --outfile reports/cucumber-reports.html
      
      - name: Upload test reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-reports-${{ matrix.python-version }}-${{ matrix.browser }}
          path: reports/
```

**Setup Instructions:**
1. Go to repository Settings → Secrets and variables → Actions
2. Add repository secrets:
   - `BASE_URL`
   - `TEST_USERNAME`
   - `TEST_PASSWORD`
   - `ADMIN_USERNAME`
   - `ADMIN_PASSWORD`
   - `POS_MANAGER_USERNAME`
   - `POS_MANAGER_PASSWORD`
   - `SALES_MANAGER_USERNAME`
   - `SALES_MANAGER_PASSWORD`

**Source:** See `docs/deployment/github-actions.md` for complete guide

### Jenkins

Complete Jenkinsfile with credentials binding:

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'production'],
            description: 'Target environment'
        )
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox'],
            description: 'Browser for test execution'
        )
    }
    
    environment {
        // Browser Configuration
        BROWSER_TYPE = "${params.BROWSER}"
        HEADLESS = 'true'
        
        // Timeout Configuration
        TIMEOUT_EXPLICIT = '15'
        TIMEOUT_PAGE_LOAD = '60'
        
        // Reporting Configuration
        SCREENSHOTS_ON_FAILURE = 'true'
        
        // Application URL based on environment
        BASE_URL = credentials("testinium-${params.ENVIRONMENT}-base-url")
        
        // Credentials - loaded from Jenkins credentials store
        TEST_USERNAME = credentials('testinium-test-username')
        TEST_PASSWORD = credentials('testinium-test-password')
        ADMIN_USERNAME = credentials('testinium-admin-username')
        ADMIN_PASSWORD = credentials('testinium-admin-password')
        POS_MANAGER_USERNAME = credentials('testinium-pos-username')
        POS_MANAGER_PASSWORD = credentials('testinium-pos-password')
        SALES_MANAGER_USERNAME = credentials('testinium-sales-username')
        SALES_MANAGER_PASSWORD = credentials('testinium-sales-password')
    }
    
    stages {
        stage('Setup') {
            steps {
                echo "Setting up Python environment"
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "Running tests against ${params.ENVIRONMENT} with ${params.BROWSER}"
                sh '''
                    . venv/bin/activate
                    behave --format json --outfile reports/cucumber.json
                    behave --format html --outfile reports/cucumber-reports.html
                    behave --format allure -o reports/allure
                '''
            }
        }
        
        stage('Publish Reports') {
            steps {
                publishHTML([
                    reportDir: 'reports',
                    reportFiles: 'cucumber-reports.html',
                    reportName: 'Test Report'
                ])
                allure includeProperties: false, results: [[path: 'reports/allure']]
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
            junit 'reports/**/*.xml'
        }
        failure {
            echo "Tests failed - check reports for details"
        }
    }
}
```

**Setup Instructions:**
1. Navigate to Jenkins → Credentials → System → Global credentials
2. Add credentials for each environment:
   - `testinium-dev-base-url`: `https://testinium-dev.example.com`
   - `testinium-staging-base-url`: `https://testinium-staging.example.com`
   - `testinium-production-base-url`: `https://testinium.example.com`
3. Add test credentials:
   - `testinium-test-username`
   - `testinium-test-password`
   - (Add all other credential types similarly)

**Source:** See `docs/deployment/jenkins-integration.md` for complete guide

### GitLab CI

Complete `.gitlab-ci.yml` with variables:

```yaml
# .gitlab-ci.yml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  BROWSER_TYPE: "chrome"
  HEADLESS: "true"
  TIMEOUT_EXPLICIT: "15"
  TIMEOUT_PAGE_LOAD: "60"
  SCREENSHOTS_ON_FAILURE: "true"

cache:
  paths:
    - .cache/pip
    - venv/

stages:
  - test
  - report

.test_template: &test_definition
  stage: test
  image: python:3.11
  before_script:
    - python -m venv venv
    - source venv/bin/activate
    - pip install --upgrade pip
    - pip install -r requirements.txt
  script:
    - behave --format json --outfile reports/cucumber.json
    - behave --format html --outfile reports/cucumber-reports.html
  artifacts:
    when: always
    paths:
      - reports/
    expire_in: 30 days
  retry:
    max: 2
    when: runner_system_failure

test:chrome:
  <<: *test_definition
  variables:
    BROWSER_TYPE: "chrome"

test:firefox:
  <<: *test_definition
  variables:
    BROWSER_TYPE: "firefox"

pages:
  stage: report
  dependencies:
    - test:chrome
  script:
    - mkdir -p public
    - cp -r reports/* public/
  artifacts:
    paths:
      - public
  only:
    - main
```

**Setup Instructions:**
1. Navigate to GitLab project → Settings → CI/CD → Variables
2. Add protected and masked variables:
   - `BASE_URL`: Environment-specific application URL
   - `TEST_USERNAME`: Test user username
   - `TEST_PASSWORD`: Test user password (masked)
   - `ADMIN_USERNAME`: Admin username
   - `ADMIN_PASSWORD`: Admin password (masked)
   - `POS_MANAGER_USERNAME`: POS manager username
   - `POS_MANAGER_PASSWORD`: POS manager password (masked)
   - `SALES_MANAGER_USERNAME`: Sales manager username
   - `SALES_MANAGER_PASSWORD`: Sales manager password (masked)
3. Mark all password variables as "Masked" for security
4. Mark all variables as "Protected" to limit access to protected branches

**Source:** See `docs/deployment/gitlab-ci.md` for complete guide

## See Also

### Related Documentation

- **[Configuration Options Reference](configuration-options.md)** - Complete reference for `config.yaml` options
- **[Behave Configuration](behave-configuration.md)** - Behave framework configuration options
- **[Configuration Management Guide](../guides/configuration-management.md)** - Advanced configuration patterns and best practices

### Deployment Guides

- **[Local Development Setup](../deployment/local-development.md)** - Setting up local development environment
- **[Jenkins Integration](../deployment/jenkins-integration.md)** - Complete Jenkins CI/CD setup
- **[GitHub Actions Integration](../deployment/github-actions.md)** - GitHub Actions workflow setup
- **[GitLab CI Integration](../deployment/gitlab-ci.md)** - GitLab CI pipeline configuration
- **[Docker Deployment](../deployment/docker.md)** - Containerized test execution
- **[Kubernetes Deployment](../deployment/kubernetes.md)** - Kubernetes-based test execution

### Troubleshooting

- **[Configuration Issues](../troubleshooting/configuration-issues.md)** - Troubleshooting configuration problems
- **[Common Errors](../troubleshooting/common-errors.md)** - Common error messages and solutions

### Source Files

- **`.env.example`** - Template file with all environment variables
- **`config/config.yaml`** - Main configuration file with environment variable interpolation
- **`config/test_config.py`** - Configuration loading and substitution logic
