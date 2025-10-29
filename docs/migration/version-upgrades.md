# Version Upgrade Guide

## Overview

This guide provides comprehensive information for upgrading between versions of the Python Selenium + Behave BDD test automation framework. It includes breaking changes, migration steps, compatibility matrices, and troubleshooting guidance for each version transition.

**Current Stable Version:** 1.0.0

**Prerequisites:**
- Understanding of the framework architecture
- Access to test environment for validation
- Backup of current framework version
- Review of [Migration from Java/Cucumber](from-java-cucumber.md) if coming from the original Java implementation

---

## Version History

### Quick Reference

| Version | Release Date | Status | Python Support | Key Changes |
|---------|-------------|--------|----------------|-------------|
| 1.0.0 | 2024 Q4 | Stable | 3.9 - 3.12 | Initial Python migration from Java |
| 0.9.x | N/A | Development | 3.9 - 3.12 | Pre-release versions (internal) |

---

## Version 1.0.0 - Initial Python Migration

### Release Information

**Release Date:** 2024 Q4  
**Status:** Stable  
**Migration Type:** Major rewrite (Java → Python)  
**Effort Estimate:** Complete framework replacement

### What's New in 1.0.0

This is the **initial production release** of the Python-based test automation framework, representing a complete migration from the legacy Java + Selenium + Cucumber stack.

#### Major Features

1. **Complete Python 3 Rewrite**
   - 24 Java files transformed into 44 Python modules
   - 17,367 lines of production-ready Python code
   - Zero placeholders or incomplete implementations

2. **Modern Technology Stack**
   - **Python 3.9-3.12** compatibility
   - **Selenium WebDriver 4.15.2** (upgraded from 3.x)
   - **Behave 1.2.6** BDD framework (replacing Cucumber)
   - **pytest 7.4.3** test runner support
   - **Allure 2.13.2** reporting

3. **Enhanced Architecture**
   - Property-based locator pattern (replacing PageFactory)
   - Thread-safe driver management with `threading.local()`
   - Centralized wait helpers with explicit waits only
   - Dataclass-based configuration management
   - Improved screenshot and logging utilities

4. **Security Improvements**
   - All hardcoded credentials removed
   - Environment variable-based secrets management
   - YAML configuration with variable interpolation

5. **Bug Fixes from Java Version**
   - Fixed 5 critical bugs identified in original Java implementation
   - Improved element staleness handling
   - Better timeout and wait strategies
   - Enhanced error reporting

6. **Comprehensive Testing**
   - 61 unit and integration tests
   - 100% test pass rate
   - Test coverage for all utility modules

#### Breaking Changes from Java Version

**⚠️ CRITICAL:** Version 1.0.0 is a complete rewrite. There is **no direct upgrade path** from the Java version. This is a fresh installation.

**Language and Framework Changes:**

| Java Pattern | Python 1.0.0 Equivalent | Migration Required |
|-------------|------------------------|-------------------|
| `@FindBy` annotations | Property methods with explicit locators | Complete page object rewrite |
| `PageFactory.initElements()` | Constructor with locator initialization | Pattern change required |
| `@Given/@When/@Then` (Cucumber) | `@given/@when/@then` (Behave) | Lowercase decorators |
| Maven `pom.xml` | `requirements.txt` / `pyproject.toml` | Dependency manifest change |
| JUnit test runner | Behave CLI / pytest | Command-line changes |
| Java Properties files | YAML config + `.env` | Configuration migration |
| `InheritableThreadLocal` | `threading.local()` | Driver management change |

**Configuration Changes:**

1. **File Format:** `config.properties` → `config/config.yaml` + `.env`
2. **Structure:** Flat properties → Nested YAML structure
3. **Secrets:** Inline credentials → Environment variables
4. **Browser Config:** Property-based → Dataclass-based

**API Changes:**

1. **Driver Access:** 
   ```java
   // Java
   WebDriver driver = Driver.getDriver();
   ```
   ```python
   # Python 1.0.0
   from utilities.driver_manager import DriverManager
   driver = DriverManager.get_driver()
   ```

2. **Page Object Initialization:**
   ```java
   // Java
   LoginPage loginPage = PageFactory.initElements(driver, LoginPage.class);
   ```
   ```python
   # Python 1.0.0
   from pages.login_page import LoginPage
   login_page = LoginPage(driver)
   ```

3. **Step Definition Context:**
   ```java
   // Java - instance variables
   private LoginPage loginPage;
   ```
   ```python
   # Python 1.0.0 - Behave context
   context.login_page = LoginPage(context.driver)
   ```

**Feature File Compatibility:**

- ✅ **Gherkin syntax unchanged:** Feature files are compatible
- ⚠️ **Tag format:** Same format but verify custom tags
- ⚠️ **Background sections:** Must contain only Given/When/Then steps (4 feature files had prose text issues)

**Removed Features:**

- Java-specific annotations and reflection
- Maven build system and plugins
- JUnit test runners and assertions
- PageFactory pattern
- Java Properties file format

**New Features (Not in Java Version):**

- Type hints throughout codebase
- Dataclass-based configuration
- Pytest integration option
- Enhanced wait helpers
- Improved screenshot management
- Allure-Behave integration
- Comprehensive unit tests

### Dependency Compatibility Matrix

**Python Version Requirements:**

| Framework Version | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 | Python 3.13 |
|------------------|-----------|------------|------------|------------|------------|
| 1.0.0 | ✅ Tested | ✅ Tested | ✅ Tested | ✅ Tested | ⚠️ Not Tested |

**Core Dependencies (Version 1.0.0):**

| Package | Version | Purpose | Upgrade Notes |
|---------|---------|---------|--------------|
| selenium | 4.15.2 | WebDriver automation | Pin to 4.x for stability |
| behave | 1.2.6 | BDD framework | Core framework dependency |
| pytest | 7.4.3 | Test runner (optional) | Alternative to Behave |
| python-dotenv | 1.0.0 | Environment variables | Required for configuration |
| PyYAML | 6.0.1 | Configuration parsing | Required for config.yaml |
| webdriver-manager | 4.0.1 | Driver management | Automatic driver downloads |
| allure-behave | 2.13.2 | Test reporting | Optional but recommended |
| allure-pytest | 2.13.2 | Test reporting (pytest) | If using pytest |
| pytest-html | 4.1.1 | HTML reports | Optional |
| behave-html-formatter | 0.9.10 | HTML reports (Behave) | Optional |

**Development Dependencies:**

| Package | Version | Purpose |
|---------|---------|---------|
| pylint | 3.0.3 | Code linting |
| black | 23.12.1 | Code formatting |
| mypy | 1.7.1 | Static type checking |
| isort | 5.13.0 | Import sorting |
| pytest-cov | 4.1.0 | Test coverage |

**Browser Driver Compatibility:**

| Browser | Minimum Version | Recommended Version | WebDriver | Notes |
|---------|----------------|-------------------|-----------|-------|
| Chrome | 90+ | 120+ | ChromeDriver 120+ | Auto-managed by webdriver-manager |
| Firefox | 90+ | 121+ | GeckoDriver 0.33+ | Auto-managed by webdriver-manager |
| Edge | 90+ | 120+ | EdgeDriver 120+ | Auto-managed by webdriver-manager |
| Safari | 14+ | 17+ | Built-in | macOS only, requires enabling |

### Migration Steps: Java to Python 1.0.0

**⚠️ Important:** This is a complete framework replacement, not an in-place upgrade.

#### Phase 1: Environment Preparation (1-2 hours)

1. **Install Python 3.9 or Higher**
   ```bash
   # Verify Python installation
   python --version  # Should show 3.9.x or higher
   
   # Or use Python 3.12 (recommended)
   python3.12 --version
   ```

2. **Create Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Linux/macOS)
   source venv/bin/activate
   
   # Activate (Windows)
   venv\Scripts\activate
   ```

3. **Install Framework Dependencies**
   ```bash
   # Install from requirements.txt
   pip install -r requirements.txt
   
   # Or using Poetry
   poetry install
   ```

4. **Verify Installation**
   ```bash
   # Check Behave installation
   behave --version
   
   # Check Selenium installation
   python -c "import selenium; print(selenium.__version__)"
   ```

#### Phase 2: Configuration Migration (1-2 hours)

1. **Create Configuration Files**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Verify config.yaml exists
   ls config/config.yaml
   ```

2. **Migrate Configuration Values**
   
   **From Java properties:**
   ```properties
   # config.properties (Java)
   browser=chrome
   headless=false
   base.url=https://example.testinium.io
   timeout.explicit=10
   ```
   
   **To Python YAML + .env:**
   ```yaml
   # config/config.yaml
   browser:
     type: chrome
     headless: false
   
   timeouts:
     explicit: 10
   
   application:
     base_url: ${BASE_URL}
   ```
   
   ```bash
   # .env
   BASE_URL=https://example.testinium.io
   ADMIN_USERNAME=your_username
   ADMIN_PASSWORD=your_password
   ```

3. **Update Credentials**
   - Remove all hardcoded credentials from code
   - Add credentials to `.env` file
   - Verify `.env` is in `.gitignore`

#### Phase 3: Page Object Migration (8-16 hours)

1. **Convert Page Object Pattern**
   
   **Java PageFactory pattern:**
   ```java
   public class LoginPage {
       @FindBy(name = "login")
       private WebElement inputEmail;
       
       public LoginPage(WebDriver driver) {
           PageFactory.initElements(driver, this);
       }
   }
   ```
   
   **Python property-based pattern:**
   ```python
   from pages.base_page import BasePage
   from selenium.webdriver.common.by import By
   
   class LoginPage(BasePage):
       _INPUT_EMAIL = (By.NAME, "login")
       
       @property
       def input_email(self):
           return self.wait_for_element(self._INPUT_EMAIL)
   ```

2. **Inherit from BasePage**
   - All page objects must inherit from `pages.base_page.BasePage`
   - Use inherited wait methods: `wait_for_element()`, `wait_for_clickable()`, etc.
   - Initialize with `super().__init__(driver)`

3. **Convert Locators**
   - `@FindBy(name="x")` → `(By.NAME, "x")`
   - `@FindBy(id="x")` → `(By.ID, "x")`
   - `@FindBy(xpath="x")` → `(By.XPATH, "x")`
   - `@FindBy(css="x")` → `(By.CSS_SELECTOR, "x")`

#### Phase 4: Step Definition Migration (6-12 hours)

1. **Update Decorator Syntax**
   ```python
   # Change from Java Cucumber:
   # @Given("I am on the login page")
   
   # To Python Behave:
   from behave import given
   
   @given('I am on the login page')
   def step_impl(context):
       # Implementation
   ```

2. **Use Behave Context**
   ```python
   # Store objects in context
   context.driver = DriverManager.get_driver()
   context.login_page = LoginPage(context.driver)
   
   # Access from context
   context.login_page.input_email.send_keys("user@example.com")
   ```

3. **Update Step Implementations**
   - Replace Java-specific syntax with Python
   - Use context for sharing state between steps
   - Update assertions to Python format

#### Phase 5: Feature File Verification (1-2 hours)

1. **Verify Gherkin Syntax**
   ```bash
   # Parse all feature files
   behave --dry-run
   ```

2. **Fix Background Sections**
   - Background must contain only Given/When/Then steps
   - Move descriptive text to Feature description
   
   **Before (Invalid):**
   ```gherkin
   Background:
     This scenario covers the login functionality.
   ```
   
   **After (Valid):**
   ```gherkin
   Feature: Login Functionality
     This scenario covers the login functionality.
   
   Background:
     Given I am on the login page
   ```

3. **Verify Tag Compatibility**
   - Ensure all tags are recognized
   - Update any Java-specific tags

#### Phase 6: Testing and Validation (4-8 hours)

1. **Run Unit Tests**
   ```bash
   # Run framework unit tests
   pytest tests/
   
   # Expected: All tests pass
   ```

2. **Run Smoke Tests**
   ```bash
   # Run login feature only
   behave features/Login.feature
   
   # Verify successful execution
   ```

3. **Run Full Test Suite**
   ```bash
   # Run all features
   behave
   
   # Or with specific tags
   behave --tags=@smoke
   ```

4. **Verify Reports**
   ```bash
   # Check HTML report
   open target/cucumber/cucumber-html-reports/overview-features.html
   
   # Check Allure report
   allure serve allure-results
   ```

#### Phase 7: CI/CD Integration (2-4 hours)

1. **Update Jenkins Pipeline**
   ```groovy
   pipeline {
       agent any
       
       stages {
           stage('Setup') {
               steps {
                   sh 'python -m venv venv'
                   sh '. venv/bin/activate && pip install -r requirements.txt'
               }
           }
           
           stage('Test') {
               steps {
                   sh '. venv/bin/activate && behave'
               }
           }
           
           stage('Report') {
               steps {
                   allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
               }
           }
       }
   }
   ```

2. **Update Environment Variables**
   - Add `.env` variables to Jenkins credentials
   - Configure secret text for sensitive values
   - Inject during build execution

### Upgrade Checklist: Installing Version 1.0.0

Use this checklist to ensure a successful migration to the Python framework:

#### Pre-Migration

- [ ] **Backup current Java framework** (create git tag or branch)
- [ ] **Document current test execution results** (baseline for comparison)
- [ ] **Review all feature files** for Gherkin syntax compliance
- [ ] **Inventory custom extensions** in Java version (if any)
- [ ] **Identify all configuration values** to migrate
- [ ] **Export test credentials** to secure location
- [ ] **Notify team** of upcoming migration and downtime

#### Environment Setup

- [ ] **Install Python 3.9+** (3.12 recommended)
- [ ] **Verify pip** is installed and up to date
- [ ] **Create virtual environment** for isolation
- [ ] **Activate virtual environment**
- [ ] **Install framework dependencies** (`pip install -r requirements.txt`)
- [ ] **Verify Behave installation** (`behave --version`)
- [ ] **Verify Selenium installation** (`python -c "import selenium"`)

#### Configuration

- [ ] **Copy `.env.example` to `.env`**
- [ ] **Add all credentials to `.env`** (admin, user, test accounts)
- [ ] **Verify `config/config.yaml`** has correct settings
- [ ] **Set `BROWSER_TYPE`** environment variable
- [ ] **Set `BASE_URL`** for target environment
- [ ] **Configure timeout values** in config.yaml
- [ ] **Verify `.env` is in `.gitignore`**

#### Code Migration

- [ ] **Migrate all page objects** to Python (use property-based locators)
- [ ] **Inherit all page objects from `BasePage`**
- [ ] **Convert all step definitions** to Behave decorators
- [ ] **Update context usage** in step definitions
- [ ] **Verify all imports** are correct
- [ ] **Run static type checking** (`mypy` if configured)
- [ ] **Run linting** (`pylint` to catch issues)
- [ ] **Format code** (`black` for consistency)

#### Feature Files

- [ ] **Parse all feature files** (`behave --dry-run`)
- [ ] **Fix Background sections** (remove prose text)
- [ ] **Verify tag syntax** is correct
- [ ] **Update any Java-specific references**
- [ ] **Ensure step definitions exist for all steps**

#### Testing

- [ ] **Run unit tests** (`pytest tests/`)
- [ ] **All unit tests pass** (61/61 expected)
- [ ] **Run single feature test** (e.g., Login.feature)
- [ ] **Verify screenshot capture** on failure
- [ ] **Check log output** for errors
- [ ] **Run full test suite** (`behave`)
- [ ] **Compare results with Java baseline** (same pass/fail status)
- [ ] **Generate HTML report** and verify
- [ ] **Generate Allure report** and verify

#### CI/CD Integration

- [ ] **Update Jenkins pipeline** to Python commands
- [ ] **Configure environment variables** in Jenkins
- [ ] **Test pipeline execution** on staging
- [ ] **Verify report publishing** works
- [ ] **Set up parallel execution** if needed
- [ ] **Configure scheduled runs**

#### Post-Migration

- [ ] **Document any differences** from Java version
- [ ] **Update team documentation** with new commands
- [ ] **Train team** on Python framework usage
- [ ] **Archive Java framework** (don't delete immediately)
- [ ] **Monitor first week** of production usage
- [ ] **Address any issues** that arise
- [ ] **Collect team feedback** on migration

#### Validation Criteria

- [ ] **All 6 working feature files execute successfully**
- [ ] **Test execution time comparable** to Java version
- [ ] **Reports generated correctly** (HTML, Allure, JUnit)
- [ ] **Screenshots captured on failures**
- [ ] **Logs are comprehensive and readable**
- [ ] **Parallel execution works** (if used)
- [ ] **CI/CD pipeline green**

### Rollback Procedures

**Scenario:** Migration to Python 1.0.0 is unsuccessful and you need to revert to the Java version.

#### Immediate Rollback (< 1 hour)

1. **Restore Java Codebase**
   ```bash
   # If using git branch for migration
   git checkout java-stable
   
   # If using git tag
   git checkout tags/java-final-version
   
   # If using backup directory
   cd ../testinium-java-backup
   ```

2. **Restore Java Environment**
   ```bash
   # Verify Java version
   java -version  # Should show Java 8+
   
   # Rebuild Maven project
   mvn clean install
   
   # Verify tests execute
   mvn test
   ```

3. **Restore Configuration**
   ```bash
   # Restore config.properties
   cp config.properties.backup config.properties
   
   # Restore credentials
   # (Restore from secure backup)
   ```

4. **Re-enable CI/CD**
   ```bash
   # Revert Jenkins pipeline to Java version
   git checkout java-stable Jenkinsfile
   
   # Push changes
   git push origin java-stable
   ```

5. **Verify Java Tests Run**
   ```bash
   # Run smoke test
   mvn test -Dcucumber.options="--tags @smoke"
   
   # Run full suite
   mvn test
   ```

#### Partial Rollback (Hybrid Approach)

If only some tests are failing in Python:

1. **Keep Python Framework** for working tests
2. **Maintain Java Framework** for failing tests temporarily
3. **Run both frameworks** in parallel during transition
4. **Gradually migrate** remaining tests as issues are resolved

```bash
# Run Python tests
cd testinium-python
source venv/bin/activate
behave --tags=@working

# Run Java tests
cd ../testinium-java
mvn test -Dcucumber.options="--tags @problematic"
```

### Testing Strategy After Upgrade

**Objective:** Ensure the Python framework produces equivalent results to the Java version.

#### Test Phases

**Phase 1: Smoke Testing (30 minutes)**

Execute critical path tests to verify basic functionality:

```bash
# Run login and logout tests
behave --tags=@smoke

# Expected: All smoke tests pass
# Verify:
# - Login successful
# - Basic navigation works
# - Logout successful
# - Screenshots captured on failure
```

**Phase 2: Feature-by-Feature Validation (2-4 hours)**

Test each feature area individually:

```bash
# Test each feature file
behave features/Login.feature
behave features/Contact.feature
behave features/Crm.feature
behave features/EmployeeFc.feature
behave features/Logout.feature
behave features/Session.feature

# Document results for each
```

**Validation Criteria per Feature:**
- [ ] All scenarios execute without errors
- [ ] Pass/fail results match Java baseline
- [ ] Execution time is comparable (±20%)
- [ ] Screenshots captured correctly
- [ ] Logs are detailed and readable

**Phase 3: Regression Testing (4-8 hours)**

Run full test suite multiple times:

```bash
# Run full suite 3 times
for i in {1..3}; do
    echo "Run $i"
    behave
    sleep 60
done

# Compare results across runs
```

**Validation Criteria:**
- [ ] Consistent pass/fail results across runs
- [ ] No flaky tests (intermittent failures)
- [ ] No memory leaks or resource issues
- [ ] Reports generated successfully each time

**Phase 4: Parallel Execution Testing (2-4 hours)**

If using parallel execution:

```bash
# Run tests in parallel
behave --processes 4

# Verify:
# - No thread safety issues
# - No driver conflicts
# - No shared state problems
```

**Phase 5: Integration Testing (2-4 hours)**

Verify CI/CD integration:

```bash
# Trigger Jenkins build
# Verify:
# - Build executes successfully
# - Tests run in CI environment
# - Reports published correctly
# - Artifacts archived properly
```

#### Test Comparison Matrix

| Test Area | Java Result | Python Result | Status | Notes |
|-----------|------------|--------------|--------|-------|
| Login - Valid Credentials | ✅ Pass | ✅ Pass | ✅ Equivalent | - |
| Login - Invalid Credentials | ✅ Pass | ✅ Pass | ✅ Equivalent | - |
| CRM - Create Contact | ✅ Pass | ✅ Pass | ✅ Equivalent | - |
| CRM - Edit Contact | ✅ Pass | ✅ Pass | ✅ Equivalent | - |
| ... | ... | ... | ... | ... |

**Action Items:**
- ✅ **Equivalent:** No action needed
- ⚠️ **Acceptable Difference:** Document reason
- ❌ **Failure:** Investigate and fix

### Common Upgrade Issues and Solutions

#### Issue 1: Import Errors After Migration

**Symptoms:**
```
ModuleNotFoundError: No module named 'selenium'
```

**Cause:** Dependencies not installed in virtual environment

**Solution:**
```bash
# Verify virtual environment is activated
which python  # Should show venv/bin/python

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep selenium
```

#### Issue 2: Feature File Parse Errors

**Symptoms:**
```
ParserError: Failed to parse Background section
```

**Cause:** Background section contains prose text instead of steps

**Solution:**
```gherkin
# Before (Invalid):
Background:
  This test validates calendar functionality

# After (Valid):
Feature: Calendar Management
  This test validates calendar functionality

Background:
  Given I am logged in as admin
  And I am on the calendar page
```

**Affected Files (from Java migration):**
- `Calendar.feature`
- `Inventory.feature`
- `Notes.feature`
- `Sales.feature`

#### Issue 3: WebDriver Not Found

**Symptoms:**
```
WebDriverException: 'chromedriver' executable needs to be in PATH
```

**Cause:** webdriver-manager not downloading driver automatically

**Solution:**
```bash
# Manual driver installation
pip install webdriver-manager

# Or download manually:
# Chrome: https://chromedriver.chromium.org/
# Firefox: https://github.com/mozilla/geckodriver/releases

# Add to PATH or configure in config.yaml
```

#### Issue 4: Configuration Not Loaded

**Symptoms:**
```
KeyError: 'BASE_URL'
FileNotFoundError: .env file not found
```

**Cause:** `.env` file not created or not in correct location

**Solution:**
```bash
# Copy example file
cp .env.example .env

# Edit with actual values
nano .env  # or your preferred editor

# Verify file location (must be in project root)
ls -la .env

# Verify python-dotenv is installed
pip show python-dotenv
```

#### Issue 5: Stale Element Reference

**Symptoms:**
```
StaleElementReferenceException: element is no longer attached to DOM
```

**Cause:** Element refresh needed between actions

**Solution:**
```python
# Use property-based locators (auto-refresh):
@property
def input_email(self):
    return self.wait_for_element(self._INPUT_EMAIL)

# Access property each time (fresh element):
self.input_email.send_keys("user@example.com")
self.input_email.clear()  # Property accessed again, element refreshed
```

**Source:** Property-based pattern in `pages/base_page.py`

#### Issue 6: Timeout Errors

**Symptoms:**
```
TimeoutException: Message: Element not found within 10 seconds
```

**Cause:** Timeouts too short or element selector incorrect

**Solution:**
```yaml
# Increase timeout in config/config.yaml:
timeouts:
  explicit: 20  # Increased from 10
  page_load: 60

# Or use longer wait in specific case:
element = self.wait_for_element(locator, timeout=30)
```

#### Issue 7: Parallel Execution Failures

**Symptoms:**
```
WebDriverException: Session not created
Multiple tests failing only in parallel mode
```

**Cause:** Thread safety issue or driver conflicts

**Solution:**
```python
# Verify threading.local() usage in DriverManager
# Each thread gets its own driver instance

# In utilities/driver_manager.py:
_drivers = threading.local()

# Verify each step gets driver from context:
@given('I am on the login page')
def step_impl(context):
    driver = context.driver  # Thread-local driver
    context.login_page = LoginPage(driver)
```

**Source:** `utilities/driver_manager.py:128-129`

#### Issue 8: Reports Not Generated

**Symptoms:**
```
No HTML report in target/ directory
Allure results directory empty
```

**Cause:** Report formatter not configured or execution failed

**Solution:**
```bash
# Verify behave.ini configuration:
[behave]
format = html
outfile = target/cucumber/cucumber-html-reports/overview-features.html

# For Allure:
format = allure_behave.formatter:AllureFormatter
outfile = allure-results

# Ensure target directory exists:
mkdir -p target/cucumber/cucumber-html-reports
mkdir -p allure-results

# Run with explicit formatter:
behave -f html -o target/report.html
```

#### Issue 9: Test Data Issues

**Symptoms:**
```
Tests pass individually but fail when run together
Data conflicts between tests
```

**Cause:** Test isolation issue or shared test data

**Solution:**
```python
# Use unique test data per scenario:
import uuid

@given('I create a new contact')
def step_impl(context):
    unique_id = str(uuid.uuid4())[:8]
    context.contact_name = f"Test Contact {unique_id}"
    context.contact_email = f"test_{unique_id}@example.com"

# Or use scenario-level cleanup:
def after_scenario(context, scenario):
    # Clean up test data created during scenario
    if hasattr(context, 'created_contact_id'):
        delete_contact(context.created_contact_id)
```

**Source:** `features/environment.py` hooks

#### Issue 10: Credential/Authentication Failures

**Symptoms:**
```
Login fails in automated tests
Authentication error: Invalid credentials
```

**Cause:** Credentials not loaded from `.env` or incorrect format

**Solution:**
```python
# Verify .env format:
ADMIN_USERNAME=admin@example.com
ADMIN_PASSWORD=SecurePassword123

# No quotes, no spaces around =

# Verify loading in code:
from config.test_config import get_config
config = get_config()
print(config.credentials.admin_username)  # Debug output

# Verify .env is in project root:
ls -la .env
```

**Source:** `config/test_config.py` and `.env.example`

---

## Future Version Upgrade Template

This section provides a template for documenting future version upgrades (1.1.0, 2.0.0, etc.).

### Version X.Y.Z - [Version Name]

**Release Date:** YYYY-MM-DD  
**Status:** Planned / Beta / Stable  
**Upgrade Type:** Major / Minor / Patch  
**Effort Estimate:** Low / Medium / High (hours)

#### What's New

**New Features:**
- Feature 1 description
- Feature 2 description

**Enhancements:**
- Enhancement 1 description
- Enhancement 2 description

**Bug Fixes:**
- Fix 1 description
- Fix 2 description

#### Breaking Changes

**API Changes:**

| Changed API | Before | After | Migration Required |
|------------|--------|-------|-------------------|
| Example | `old_method()` | `new_method()` | Yes - update all calls |

**Configuration Changes:**

```yaml
# Before:
old_config:
  setting: value

# After:
new_config:
  setting: value
```

**Deprecated Features:**

| Feature | Deprecated In | Removed In | Replacement |
|---------|--------------|-----------|-------------|
| Example | X.Y.Z | X+1.0.0 | new_feature |

#### Dependency Updates

| Package | Previous Version | New Version | Notes |
|---------|-----------------|-------------|-------|
| selenium | 4.15.2 | 4.X.X | Breaking changes: ... |

#### Migration Steps

1. **Preparation:**
   - Backup current version
   - Review breaking changes
   - Plan migration timeline

2. **Update Dependencies:**
   ```bash
   pip install --upgrade package==X.Y.Z
   ```

3. **Update Configuration:**
   - Change A to B in config.yaml
   - Add new setting C

4. **Update Code:**
   - Replace deprecated calls
   - Update API usage

5. **Test:**
   - Run unit tests
   - Run integration tests
   - Verify in staging

#### Upgrade Checklist

- [ ] Review release notes
- [ ] Backup current version
- [ ] Update dependencies
- [ ] Update configuration
- [ ] Update code for breaking changes
- [ ] Run tests
- [ ] Verify reports
- [ ] Deploy to staging
- [ ] Verify in staging
- [ ] Deploy to production
- [ ] Monitor production

#### Rollback Procedure

If upgrade fails:

1. Restore from backup
2. Revert dependency versions
3. Revert configuration changes
4. Verify tests pass
5. Document issues encountered

#### Known Issues

- Issue 1: Description and workaround
- Issue 2: Description and workaround

---

## Getting Help

### Documentation Resources

- **Main Documentation:** [docs/index.md](../index.md)
- **Migration from Java:** [from-java-cucumber.md](from-java-cucumber.md)
- **API Reference:** [docs/api-reference/](../api-reference/index.md)
- **Troubleshooting Guide:** [docs/troubleshooting/](../troubleshooting/index.md)

### Support Channels

- **Issues:** Report bugs or issues in the project issue tracker
- **Discussions:** Ask questions in project discussions
- **Email:** Contact maintainers for private inquiries

### Before Reporting Issues

Please provide:
1. Framework version (`pip show behave`)
2. Python version (`python --version`)
3. Operating system and version
4. Full error message and stack trace
5. Steps to reproduce
6. Expected vs actual behavior

---

## Appendix

### Version Numbering Scheme

This framework follows [Semantic Versioning 2.0.0](https://semver.org/):

**Format:** MAJOR.MINOR.PATCH

- **MAJOR:** Breaking changes, incompatible API changes
- **MINOR:** New features, backwards-compatible
- **PATCH:** Bug fixes, backwards-compatible

**Examples:**
- `1.0.0` → `1.0.1`: Bug fix, safe to upgrade
- `1.0.1` → `1.1.0`: New features, safe to upgrade
- `1.9.0` → `2.0.0`: Breaking changes, review migration guide

### Release Schedule

- **Major versions:** Annual (approx.)
- **Minor versions:** Quarterly (approx.)
- **Patch versions:** As needed for critical bugs

### Support Policy

- **Current major version:** Full support
- **Previous major version:** Security fixes only for 6 months
- **Older versions:** No support (upgrade recommended)

**Current Support Status:**
- **1.x.x:** ✅ Full support
- **0.x.x:** ❌ No support (development versions)

### Deprecation Policy

Features marked as deprecated:
1. Announced in release notes
2. Warning logged when used
3. Maintained for at least 2 minor versions
4. Removed in next major version

**Example Timeline:**
- Deprecated in 1.2.0
- Warning in 1.2.0, 1.3.0, 1.4.0
- Removed in 2.0.0

---

**Last Updated:** 2024 Q4  
**Document Version:** 1.0  
**Maintained By:** Framework Team

