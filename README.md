# :fallen_leaf: :leaves: Testinium-QA :leaves: :fallen_leaf:
Automating the Testinium browser (Python 3.9+, Selenium 4.x, Behave, pytest, Jira, Jenkins)

### Tools

<p align="left"> 

<a href="https://www.python.org" target="_blank" rel="noreferrer"> 
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="60" height="60"/> 
</a> 

<a href="https://www.selenium.dev" target="_blank" rel="noreferrer">
  <img src="https://selenium.dev/images/selenium_logo_square_green.png" alt="selenium" width="60" height="60"/> 
</a>    

<a href="https://behave.readthedocs.io/" target="_blank" rel="noreferrer"> 
  <img src="https://raw.githubusercontent.com/behave/behave/master/docs/_static/behave_logo1.png" alt="behave" width="120" height="60"/> 
</a>

<a href="https://pytest.org" target="_blank" rel="noreferrer">
  <img src="https://docs.pytest.org/en/stable/_static/pytest1.png" width="115" height="60"/> 
</a> 
<a href="https://www.atlassian.com/software/jira" target="_blank" rel="noreferrer">
  <img src="https://i0.wp.com/invotra.com/wp-content/uploads/2019/09/jira_software_logo-e1571063680300.png?fit=768%2C216&ssl=1" width="160" height="60"/> 
</a> 
<a href="https://www.jenkins.io" target="_blank" rel="noreferrer">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Jenkins_logo.svg/1200px-Jenkins_logo.svg.png" width="50" height="80"/> 
</a> 
</p>

* PYTHON 3.9+
* SELENIUM 4.x
* BEHAVE (BDD Framework)
* PYTEST
* JIRA
* JENKINS

### Testinium-QA

This repository contains a collection of sample `Testinium-QA` projects and libraries that demonstrate how to
use the tool and develop automation scripts using the Behave BDD framework with Python as the programming language.
It generates JSON, HTML, and Allure reports. It also generates `screenshots` for your tests and
`error screenshots` for failed test cases automatically.

### Installation (pre-requisites)

1. **Python 3.9+** (Download from [python.org](https://www.python.org/downloads/))
2. **pip** (Python package manager - included with Python 3.9+)
3. **Virtual Environment** (recommended - `venv` or `virtualenv`)
4. **IDE/Editor** (recommended):
    - PyCharm (Community or Professional)
    - Visual Studio Code with Python extension
    - Any Python-compatible IDE
5. **IDE Plugins** (recommended):
    - Python extension
    - Gherkin/Cucumber syntax highlighting
6. **Browser Drivers** (automatically managed by `webdriver-manager`):
    - ChromeDriver (for Chrome/Chromium)
    - GeckoDriver (for Firefox)
    - No manual setup required!

### Framework Setup

#### 1. Clone the Repository

**Via Git:**
```bash
git clone https://github.com/BalamiRR/Testinium-QA.git
cd Testinium-QA
```

**Manually:**

Fork / Clone repository from [here](https://github.com/BalamiRR/Testinium-QA/archive/main.zip) or download zip and set
it up in your local workspace.

#### 2. Set Up Python Virtual Environment

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Alternatively, using Poetry (if pyproject.toml is available)
poetry install
```

#### 4. Configure Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials (DO NOT commit this file)
# Example:
# TEST_USERNAME=your_test_username@example.com
# TEST_PASSWORD=your_secure_password
# BASE_URL=https://testinium.example.com
```

#### 5. Configure Test Settings

Edit `config/config.yaml` to customize browser settings, timeouts, and other test configurations:

```yaml
browser:
  type: chrome  # Options: chrome, firefox
  headless: false  # Set to true for CI/CD environments

timeouts:
  implicit: 0  # Not recommended to use implicit waits
  explicit: 10  # Default explicit wait timeout in seconds
  page_load: 30
```



### Running Tests

#### Basic Test Execution

```bash
# Run all tests
behave

# Run tests with specific tag
behave --tags=@Login

# Run tests from specific feature file
behave features/Login.feature

# Run tests with multiple tags
behave --tags=@SalesManager,@Login

# Exclude specific tags
behave --tags=~@WIP

# Dry run (validate step definitions without execution)
behave --dry-run
```

#### Test Execution with Reporting

```bash
# Generate JSON report
behave --format=json --outfile=reports/cucumber.json

# Generate HTML report
behave --format=html --outfile=reports/report.html

# Generate multiple report formats
behave --format=json --outfile=reports/cucumber.json --format=html --outfile=reports/report.html

# Generate Allure report (if allure-behave is installed)
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results
allure serve reports/allure-results
```

#### Parallel Test Execution

```bash
# Install parallel execution support
pip install behave-parallel

# Run tests in parallel (4 processes)
behave --processes 4 --parallel-element scenario

# Run with pytest-xdist (alternative)
pytest tests/ -n 4 -v
```

### Behave Configuration

The framework uses `behave.ini` for configuration and `features/environment.py` for test hooks:

**behave.ini:**
```ini
[behave]
# Default format options
format = json
        html
        pretty
outfiles = reports/cucumber.json
          reports/report.html

# Show detailed output
show_skipped = true
show_timings = true

# Default tags (can be overridden via command line)
# tags = @Smoke

# Paths
paths = features/

# Step definitions location (automatically discovered in features/steps/)
```

**features/environment.py (Test Hooks):**
```python
from utilities.driver_manager import DriverManager
from utilities.config_reader import ConfigReader
from utilities.screenshot_helper import capture_screenshot
import allure

def before_all(context):
    """Runs once before all tests"""
    context.config_reader = ConfigReader()
    context.driver_manager = DriverManager(context.config_reader)

def before_scenario(context, scenario):
    """Runs before each scenario"""
    context.driver = context.driver_manager.get_driver()
    context.driver.maximize_window()

def after_scenario(context, scenario):
    """Runs after each scenario - captures screenshots on failure"""
    if scenario.status == 'failed':
        # Capture screenshot
        screenshot_path = capture_screenshot(
            context.driver, 
            scenario.name
        )
        
        # Attach to Allure report (if using Allure)
        if screenshot_path:
            allure.attach.file(
                screenshot_path,
                name=f"{scenario.name}_failure",
                attachment_type=allure.attachment_type.PNG
            )

def after_all(context):
    """Runs once after all tests"""
    context.driver_manager.quit_driver()
```

### Develop Automation Scripts Using BDD Approach - Behave with Python

There are already many predefined step definitions which are packaged under `features/steps/login_steps.py` that will help you speed
up your automation development with helpful utility methods.

Tests are written using the Behave BDD framework with Gherkin syntax.
Here is one of the scenarios:

```
@Login
Feature: Testinium app login feature
  User Story:
  As a user, I should be able to login with correct credentials to different accounts.

  Accounts are: PosManager, SalesManager

  Background: For the scenarios in the feature file, user is expected to be on login page
    Given User is on the Testinium login page

  #1-Users can log in with valid credentials (We have 5 types of users but will test only 2 user: PosManager, SalesManager)
  @UPGN-286
  Scenario Outline: Users log in with valid credentials
    When User enters "<username>" username
    And User enters "<password>" password
    And User clicks the login button
    Then User should see the dashboard
  
  #2-"Wrong login/password" should be displayed for invalid (valid username-invalid password and invalid username-valid password) credentials
  @UPGN-287
  Scenario Outline: Users log in with invalid email or invalid password credentials
    When User enters "<username>" username
    And User enters "<password>" password
    And User clicks the login button
    Then User sees error message
    
  #3- "Please fill out this field" message should be displayed if the password or username is empty
  @UPGN-288
  Scenario Outline:Users log in with invalid email or invalid password credentials
    When User enters "<password>" username
    And User clicks the login button
    Then User sees "Veuillez renseigner ce champ." message

    @SalesManager
    Examples: SalesManager's username and password
      |username               |password    |
      |salesmanager7@info.com |salesmanager|
      |salesmanager8@info.com |salesmanager|
      |salesmanager9@info.com |salesmanager|
      
    @PosManager
    Examples: PosManager's username and password
      |username               |password  |
      |posmanager5@info.com   |posmanager|
      |posmanager6@info.com   |posmanager|
```

### Step Definition Implementation (Python)

The corresponding step definitions are implemented in Python using the `@given`, `@when`, `@then` decorators:

**features/steps/login_steps.py:**
```python
from behave import given, when, then
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('User is on the Testinium login page')
def navigate_to_login_page(context):
    """Navigate to the Testinium login page"""
    base_url = context.config_reader.get_property('base_url')
    context.driver.get(base_url)
    context.login_page = LoginPage(context.driver)

@when('User enters "{username}" username')
def enter_username(context, username):
    """Enter username into the login form"""
    context.login_page.input_email.send_keys(username)

@when('User enters "{password}" password')
def enter_password(context, password):
    """Enter password into the login form"""
    context.login_page.input_password.send_keys(password)

@when('User clicks the login button')
def click_login_button(context):
    """Click the login button"""
    context.login_page.button_login.click()

@then('User should see the dashboard')
def verify_dashboard(context):
    """Verify user is redirected to dashboard"""
    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.url_contains('dashboard'))
    assert 'dashboard' in context.driver.current_url, \
        "User was not redirected to dashboard"

@then('User sees error message')
def verify_error_message(context):
    """Verify error message is displayed for invalid credentials"""
    wait = WebDriverWait(context.driver, 5)
    error_element = wait.until(
        EC.visibility_of_element_located(context.login_page._ERROR_MESSAGE)
    )
    assert error_element.is_displayed(), "Error message not displayed"
```

### Page Object Model (Python)

Page objects encapsulate web elements and interactions using Python properties:

**pages/login_page.py:**
```python
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):
    """Login page object for Testinium application"""
    
    # Locators as private class attributes
    _INPUT_EMAIL = (By.NAME, "login")
    _INPUT_PASSWORD = (By.NAME, "password")
    _BUTTON_LOGIN = (By.XPATH, "//button[.='Log in']")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    
    @property
    def input_email(self):
        """Email input field"""
        return self.wait_for_element(self._INPUT_EMAIL)
    
    @property
    def input_password(self):
        """Password input field"""
        return self.wait_for_element(self._INPUT_PASSWORD)
    
    @property
    def button_login(self):
        """Login button"""
        return self.wait_for_clickable(self._BUTTON_LOGIN)
    
    def login(self, username: str, password: str):
        """High-level login method"""
        self.input_email.send_keys(username)
        self.input_password.send_keys(password)
        self.button_login.click()
```

### Jenkins Integration

![alt text](./image/Jenkins-Cucumber-Reports.png)

The framework integrates seamlessly with Jenkins CI/CD pipeline:

**Jenkins Pipeline Configuration (Jenkinsfile):**
```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    behave --tags=@Smoke \
                           --format=json --outfile=reports/cucumber.json \
                           --format=html --outfile=reports/report.html \
                           --format=junit --outfile=reports/junit.xml
                '''
            }
        }
        
        stage('Generate Reports') {
            steps {
                // Publish HTML reports
                publishHTML([
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Behave Test Report'
                ])
                
                // Publish JUnit test results
                junit 'reports/junit.xml'
                
                // Generate Allure report (if configured)
                allure([
                    includeProperties: false,
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }
    }
    
    post {
        always {
            // Archive screenshots
            archiveArtifacts artifacts: 'reports/screenshots/*.png', allowEmptyArchive: true
        }
    }
}
```

### Report Generation

##### HTML Report:

```bash
# Generate HTML report
behave --format=html --outfile=reports/cucumber-reports.html

# Or with multiple formats simultaneously
behave --format=html --outfile=reports/report.html --format=json --outfile=reports/cucumber.json
```

##### JSON Report:

```bash
# Generate JSON report (for CI/CD tools)
behave --format=json --outfile=reports/cucumber.json
```

##### JUnit XML Report:

```bash
# Generate JUnit-compatible XML report (for Jenkins)
behave --format=junit --outfile=reports/junit.xml
```

##### Allure Report (Enhanced Reporting):

```bash
# Generate Allure results
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results

# View Allure report locally
allure serve reports/allure-results

# Generate static Allure report
allure generate reports/allure-results --output reports/allure-report --clean
```

##### Rerun Failed Tests:

```bash
# First run - generates rerun file for failed scenarios
behave --format=rerun --outfile=reports/rerun.txt

# Rerun only failed scenarios
behave @reports/rerun.txt
```

### Jira Test Execution

  ![alt text](./image/Jira-Test-Exectuion.png)

The framework maintains integration with Jira via test scenario tags:

- Test scenarios are tagged with Jira ticket IDs (e.g., `@UPGN-286`, `@UPGN-287`)
- Tags enable traceability between test execution and Jira issues
- Test results can be published to Jira using plugins like Xray or Zephyr
- Behave JSON reports can be imported into Jira test management tools

**Example Jira Integration:**
```bash
# Run tests for specific Jira ticket
behave --tags=@UPGN-286

# Run all tests under a Jira epic
behave --tags=@Login
```


### Project Structure

```
testinium-qa-python/
├── .env.example                    # Environment variable template
├── .gitignore                      # Python-specific ignores
├── README.md                       # This file
├── behave.ini                      # Behave configuration
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Poetry configuration (optional)
├── config/
│   ├── __init__.py
│   ├── config.yaml                # Test configuration
│   └── test_config.py             # Configuration management
├── features/
│   ├── Calendar.feature           # Gherkin feature files
│   ├── Contact.feature
│   ├── Crm.feature
│   ├── EmployeeFc.feature
│   ├── Inventory.feature
│   ├── Login.feature
│   ├── Logout.feature
│   ├── Notes.feature
│   ├── Sales.feature
│   ├── Session.feature
│   ├── environment.py             # Behave hooks (before/after)
│   └── steps/
│       ├── __init__.py
│       ├── calendar_steps.py      # Step definitions
│       ├── contacts_steps.py
│       ├── crm_steps.py
│       ├── employee_steps.py
│       ├── inventory_steps.py
│       ├── login_steps.py
│       ├── logout_steps.py
│       ├── notes_steps.py
│       ├── sales_steps.py
│       └── session_steps.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py               # Base page object class
│   ├── calendar_page.py           # Page object classes
│   ├── contacts_page.py
│   ├── crm_page.py
│   ├── employee_page.py
│   ├── inventory_page.py
│   ├── login_page.py
│   ├── logout_page.py
│   ├── notes_page.py
│   ├── sales_page.py
│   └── session_page.py
├── utilities/
│   ├── __init__.py
│   ├── driver_manager.py          # WebDriver management
│   ├── config_reader.py           # Configuration reader
│   ├── wait_helpers.py            # Wait utility functions
│   └── screenshot_helper.py       # Screenshot utilities
├── reports/                        # Generated test reports
│   ├── allure-results/
│   ├── screenshots/
│   └── *.html, *.json, *.xml
└── logs/                          # Test execution logs
    └── test_execution.log
```

### Troubleshooting

#### Common Issues and Solutions

**Issue 1: Module Not Found Error**
```bash
# Error: ModuleNotFoundError: No module named 'selenium'
# Solution: Ensure virtual environment is activated and dependencies are installed
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```

**Issue 2: WebDriver Not Found**
```bash
# Error: WebDriverException: 'chromedriver' executable needs to be in PATH
# Solution: The webdriver-manager package handles this automatically
# Ensure it's installed:
pip install webdriver-manager
# No manual driver download needed!
```

**Issue 3: Undefined Step Definitions**
```bash
# Error: Undefined step: "User is on the Testinium login page"
# Solution: Ensure step definitions are in features/steps/ directory
# Check that step text matches exactly (case-sensitive)
# Run with --dry-run to see undefined steps:
behave --dry-run
```

**Issue 4: Import Errors in Python**
```bash
# Error: ImportError: attempted relative import with no known parent package
# Solution: Ensure __init__.py files exist in all package directories
# Run tests from project root directory
# Check PYTHONPATH if needed:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Issue 5: Browser Not Starting**
```bash
# Error: SessionNotCreatedException: session not created
# Solution: Browser and driver version mismatch
# webdriver-manager will auto-update drivers, but ensure browser is updated:
# Chrome: Help > About Google Chrome (auto-updates)
# Firefox: Help > About Firefox (auto-updates)
```

**Issue 6: Stale Element Reference**
```python
# Error: StaleElementReferenceException
# Solution: Use property-based element accessors (already implemented)
# Elements are re-located on each access
# If issue persists, add explicit waits:
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located(locator))
```

**Issue 7: Tests Failing in CI but Passing Locally**
```bash
# Common cause: Headless mode not configured
# Solution: Set headless mode in config/config.yaml for CI:
browser:
  type: chrome
  headless: true  # Enable for CI/CD

# Or override via environment variable in Jenkins:
export HEADLESS=true
behave
```

**Issue 8: Screenshot Not Captured on Failure**
```bash
# Check: Is environment.py after_scenario hook properly configured?
# Verify: reports/screenshots/ directory exists and is writable
# Debug: Add logging to after_scenario function
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Debugging Tips

1. **Enable Verbose Output:**
   ```bash
   behave --verbose --no-capture
   ```

2. **Run Specific Scenario:**
   ```bash
   behave features/Login.feature:15  # Run scenario at line 15
   ```

3. **Check Step Definitions:**
   ```bash
   behave --dry-run --no-summary
   ```

4. **Python Debugger (pdb):**
   ```python
   # Add to step definition for debugging
   import pdb; pdb.set_trace()
   ```

5. **View WebDriver Logs:**
   ```python
   # In driver_manager.py, enable logging:
   chrome_options.add_argument('--enable-logging')
   chrome_options.add_argument('--v=1')
   ```

### Dependencies

**Core Framework:**
- `selenium>=4.15.0` - WebDriver automation
- `behave>=1.2.6` - BDD test framework
- `pytest>=7.4.0` - Testing framework (optional)
- `webdriver-manager>=4.0.0` - Automatic driver management

**Configuration & Utilities:**
- `python-dotenv>=1.0.0` - Environment variable management
- `PyYAML>=6.0` - YAML configuration parsing
- `Faker>=20.0.0` - Test data generation

**Reporting:**
- `allure-behave>=2.13.0` - Enhanced test reporting
- `behave-html-formatter>=0.9.0` - HTML report generation

**Code Quality:**
- `pylint>=3.0.0` - Code linting
- `black>=23.0.0` - Code formatting
- `mypy>=1.7.0` - Type checking

See `requirements.txt` for complete dependency list.

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow Python best practices (PEP 8)
4. Write tests for new features
5. Ensure all tests pass (`behave`)
6. Run code quality checks (`pylint`, `black`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Support

For issues, questions, or contributions, please open an issue on GitHub.

### License

This project is open source and available under the MIT License.

### THE END

