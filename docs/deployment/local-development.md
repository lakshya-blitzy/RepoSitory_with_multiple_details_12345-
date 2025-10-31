# Local Development Deployment Guide

## Overview

This guide provides comprehensive instructions for setting up and running the Testinium QA test automation framework on your local development workstation. Local development is ideal for:

- **Learning the Framework**: Understanding how the framework works through hands-on exploration
- **Debugging Tests**: Iterating quickly with immediate feedback and debugging capabilities
- **Rapid Iteration**: Fast test-write-run cycles without CI/CD pipeline overhead
- **Developing New Features**: Creating new page objects, step definitions, and test scenarios
- **Offline Work**: Working without network connectivity (after initial setup)
- **Interactive Testing**: Seeing browser interactions in real-time with non-headless mode

**When to Use Local Development:**
- Initial framework exploration and learning
- Writing and debugging new test scenarios
- Troubleshooting failing tests with visual browser feedback
- Creating new page objects and step definitions
- Running specific tests or test suites quickly
- Development without CI/CD integration

**When to Use Other Deployment Methods:**
- Automated regression testing → [CI/CD Integration](jenkins-integration.md)
- Scheduled test execution → [Jenkins](jenkins-integration.md) or [GitHub Actions](github-actions.md)
- Parallel large-scale testing → [Kubernetes](kubernetes.md)
- Production test monitoring → [Cloud Providers](aws.md)

**Source:** Based on `README.md:45-750`

---

## Prerequisites

Before setting up the local development environment, ensure you have the following installed and configured:

### Required Software

#### 1. Python 3.9 - 3.12

The framework requires Python 3.9 or higher (up to Python 3.12 tested and supported).

**Verify Python Installation:**
```bash
python --version
# Expected output: Python 3.9.x, 3.10.x, 3.11.x, or 3.12.x

# On some systems, use python3:
python3 --version
```

**Installation Instructions:**
- **Windows**: Download from [python.org](https://www.python.org/downloads/) and run installer (check "Add Python to PATH")
- **macOS**: Use Homebrew: `brew install python@3.11` or download from python.org
- **Linux**: Use system package manager:
  - Ubuntu/Debian: `sudo apt install python3.11 python3.11-venv`
  - Fedora/RHEL: `sudo dnf install python3.11`
  - Arch: `sudo pacman -S python`

#### 2. pip (Python Package Manager)

pip is included with Python 3.9+ installations. Verify version 23.0 or higher.

**Verify pip Installation:**
```bash
pip --version
# Expected output: pip 23.x.x or higher

# On some systems:
pip3 --version
```

**Upgrade pip (if needed):**
```bash
python -m pip install --upgrade pip
```

#### 3. Git Version Control

Git 2.30 or higher is required for repository management.

**Verify Git Installation:**
```bash
git --version
# Expected output: git version 2.30.x or higher
```

**Installation Instructions:**
- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win)
- **macOS**: Install via Homebrew: `brew install git` or use Xcode Command Line Tools
- **Linux**: Use system package manager: `sudo apt install git` (Ubuntu/Debian)

#### 4. Web Browsers

At least one supported browser must be installed:

- **Google Chrome** (recommended): [Download Chrome](https://www.google.com/chrome/)
- **Mozilla Firefox**: [Download Firefox](https://www.mozilla.org/firefox/)

**Note**: Browser drivers (ChromeDriver, GeckoDriver) are automatically managed by the `webdriver-manager` package - no manual installation needed!

### Recommended Software

#### IDE/Code Editor

While not strictly required, an IDE greatly enhances development productivity:

**Recommended IDEs:**
- **PyCharm** (Community or Professional): [Download PyCharm](https://www.jetbrains.com/pycharm/download/)
- **Visual Studio Code** with Python extension: [Download VS Code](https://code.visualstudio.com/)
- **Alternatives**: Sublime Text, Atom, or any Python-compatible editor

#### IDE Plugins/Extensions

**For PyCharm:**
- Python (built-in)
- Gherkin (built-in in Professional, install plugin in Community)
- Cucumber for Python (optional)

**For VS Code:**
- Python (ms-python.python)
- Cucumber (Gherkin) Full Support (alexkrechik.cucumberautocomplete)
- Python Test Explorer (littlefoxteam.vscode-python-test-adapter)

**Source:** `README.md:45-61`, `setup.py:85`

---

## Step-by-Step Setup Process

### Step 1: Clone the Repository

Clone the Testinium QA repository to your local machine.

**Using Git:**
```bash
# Clone the repository
git clone https://github.com/BalamiRR/Testinium-QA.git

# Navigate to project directory
cd Testinium-QA
```

**Alternative: Download ZIP**

If Git is not available, download the repository as a ZIP file:
1. Visit the repository URL in your browser
2. Click "Code" → "Download ZIP"
3. Extract to your desired location
4. Navigate to the extracted directory

**Verify Repository Structure:**
```bash
# List directory contents
ls -la

# Expected folders:
# - config/       (Configuration files)
# - features/     (Gherkin feature files)
# - pages/        (Page Object Model)
# - utilities/    (Core utilities)
# - tests/        (pytest tests)
# - requirements.txt (Dependencies)
```

**Source:** `README.md:64-75`

### Step 2: Create Python Virtual Environment

A virtual environment isolates project dependencies from system-wide Python packages, preventing conflicts.

**Why Virtual Environments?**
- Isolate project dependencies
- Avoid version conflicts with other Python projects
- Easy to recreate or delete without affecting system Python
- Required for best practices in Python development

#### On macOS/Linux:

```bash
# Create virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Verify activation - prompt should show (venv)
# Example: (venv) user@machine:~/Testinium-QA$
```

#### On Windows:

```bash
# Create virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment (Command Prompt)
venv\Scripts\activate

# Activate the virtual environment (PowerShell)
venv\Scripts\Activate.ps1

# Verify activation - prompt should show (venv)
# Example: (venv) C:\Users\YourName\Testinium-QA>
```

**Troubleshooting Virtual Environment Activation:**

**Issue: PowerShell execution policy prevents activation**
```powershell
# Error: cannot be loaded because running scripts is disabled
# Solution: Temporarily allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then retry activation
venv\Scripts\Activate.ps1
```

**Issue: Virtual environment not activating**
```bash
# Solution: Ensure you're in the project root directory
cd /path/to/Testinium-QA
pwd  # Verify current directory

# Recreate virtual environment if corrupted
rm -rf venv/  # or rmdir /s venv on Windows
python3 -m venv venv
source venv/bin/activate
```

**To Deactivate Virtual Environment (when finished):**
```bash
deactivate
```

**Source:** `README.md:77-95`

### Step 3: Install Project Dependencies

Install all required Python packages from `requirements.txt`.

```bash
# Ensure virtual environment is activated (prompt shows (venv))

# Install all dependencies
pip install -r requirements.txt

# Expected output:
# Successfully installed selenium-4.15.2 behave-1.2.6 pytest-7.4.3 ...
```

**What Gets Installed:**
- **selenium 4.15.2**: WebDriver automation library
- **behave 1.2.6**: BDD framework for Gherkin scenarios
- **pytest 7.4.3**: Testing framework
- **webdriver-manager 4.0.1**: Automatic browser driver management
- **allure-behave 2.13.2**: Enhanced reporting
- **python-dotenv 1.0.0**: Environment variable management
- **PyYAML 6.0.1**: YAML configuration parsing
- And more... (see `requirements.txt` for complete list)

**Alternative: Install with Development Dependencies**

If you plan to contribute to the framework or run code quality checks:

```bash
# Install framework with development tools
pip install -e ".[dev]"

# This installs additional tools:
# - pylint (code linting)
# - black (code formatting)
# - mypy (type checking)
# - pytest-cov (code coverage)
```

**Verify Installation:**
```bash
# Check installed packages
pip list

# Verify key packages are installed
pip show selenium
pip show behave
pip show webdriver-manager
```

**Troubleshooting Installation:**

**Issue: pip command not found**
```bash
# Solution: Use python -m pip instead
python -m pip install -r requirements.txt
```

**Issue: Permission denied errors**
```bash
# Solution: Ensure virtual environment is activated
# Do NOT use sudo with pip when using virtual environment
source venv/bin/activate  # Activate first
pip install -r requirements.txt
```

**Issue: Network timeout or connection errors**
```bash
# Solution: Increase timeout and retry
pip install --timeout=120 -r requirements.txt

# Or use a different mirror
pip install --index-url https://pypi.org/simple -r requirements.txt
```

**Issue: Dependency conflict warnings**
```bash
# Solution: Upgrade pip and setuptools first
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Source:** `README.md:97-105`, `requirements.txt:1-91`

### Step 4: Configure Environment Variables

Create a `.env` file with your test credentials and configuration.

**Copy the Template:**
```bash
# Copy .env.example to .env
cp .env.example .env

# On Windows (Command Prompt):
copy .env.example .env

# On Windows (PowerShell):
Copy-Item .env.example .env
```

**Edit `.env` File:**

Open `.env` in your text editor and configure the following variables:

```bash
# Browser Configuration
BROWSER_TYPE=chrome        # Options: chrome, firefox
HEADLESS=false            # Set true for headless mode

# Test Environment
BASE_URL=https://testinium.example.com  # Replace with actual URL

# Timeouts (seconds)
TIMEOUT_EXPLICIT=10
TIMEOUT_PAGE_LOAD=30

# Test Credentials (REQUIRED)
ADMIN_USERNAME=admin@example.com
ADMIN_PASSWORD=your_actual_password_here

POS_MANAGER_USERNAME=posmanager@example.com
POS_MANAGER_PASSWORD=your_actual_password_here

SALES_MANAGER_USERNAME=salesmanager@example.com
SALES_MANAGER_PASSWORD=your_actual_password_here

TEST_USERNAME=testuser@example.com
TEST_PASSWORD=your_actual_password_here

# Reporting
SCREENSHOTS_ON_FAILURE=true
```

**CRITICAL SECURITY NOTES:**
- **NEVER commit `.env` to version control** - it contains sensitive credentials
- `.env` is already in `.gitignore` - verify this before committing
- Use strong, unique passwords for test accounts
- For production testing, use secrets management tools

**Configuration Precedence:**

The framework loads configuration in this order (later overrides earlier):
1. Default values in `config/test_config.py`
2. Values from `config/config.yaml`
3. Environment variables from `.env` (highest priority)

**Source:** `README.md:107-120`, `.env.example:1-31`

### Step 5: Configure Test Settings (Optional)

The framework includes sensible defaults, but you can customize behavior in `config/config.yaml`.

**Edit `config/config.yaml`:**

```yaml
browser:
  type: chrome              # Options: chrome, firefox
  headless: false          # Set true for CI/CD or headless testing
  window_size: 1920x1080   # Browser window size

timeouts:
  implicit: 0              # NOT recommended - use explicit waits instead
  explicit: 10             # Default wait timeout (seconds)
  page_load: 30           # Page load timeout (seconds)

application:
  base_url: https://testinium.example.com  # Can be overridden by BASE_URL env var

reporting:
  screenshots_on_failure: true
  screenshot_dir: reports/screenshots
  allure_results_dir: reports/allure-results
```

**Common Customizations:**

**For Faster Local Testing:**
```yaml
timeouts:
  explicit: 5   # Reduce wait times if application is fast
  page_load: 15
```

**For Firefox Testing:**
```yaml
browser:
  type: firefox
  headless: false
```

**For Debugging (Slower Execution):**
```yaml
browser:
  window_size: 1920x1080  # Maximize window for visibility

timeouts:
  explicit: 20  # Longer waits to observe behavior
```

**Source:** `README.md:122-136`

---

## IDE-Specific Configuration

Configuring your IDE properly enhances productivity with features like debugging, test running, and auto-completion.

### PyCharm Configuration

PyCharm (Community or Professional) provides excellent Python and testing support.

#### 1. Open Project in PyCharm

```bash
# Launch PyCharm and select "Open"
# Navigate to Testinium-QA directory
# Click "OK"
```

#### 2. Configure Python Interpreter

1. Open **Settings/Preferences** (`Ctrl+Alt+S` on Windows/Linux, `Cmd+,` on macOS)
2. Navigate to **Project: Testinium-QA → Python Interpreter**
3. Click gear icon → **Add...**
4. Select **Existing environment**
5. Browse to `venv/bin/python` (macOS/Linux) or `venv\Scripts\python.exe` (Windows)
6. Click **OK** → **Apply**

**Verify**: Status bar at bottom should show Python 3.x (venv)

#### 3. Configure Test Runner

**For Behave Tests:**

1. Open **Run → Edit Configurations...**
2. Click **+** → **Python**
3. Configure:
   - **Name**: "Run All Behave Tests"
   - **Script path**: Path to `behave` executable in `venv/bin/behave`
   - **Working directory**: Project root directory
   - **Python interpreter**: venv Python
4. Click **Apply** → **OK**

**For pytest Tests:**

1. Open **Settings → Tools → Python Integrated Tools**
2. Set **Default test runner** to **pytest**
3. Click **Apply**

#### 4. Install Recommended Plugins

1. Open **Settings → Plugins**
2. Search and install:
   - **Gherkin** (Cucumber for Python) - if not already installed
   - **EnvFile** - for .env file support
   - **.ignore** - for .gitignore support
3. Restart PyCharm

#### 5. Enable Gherkin Syntax Highlighting

1. Open any `.feature` file
2. PyCharm should recognize it automatically
3. If not: Right-click file → **Associate with File Type** → **Gherkin**

#### 6. Configure Debugging

**Debug a Specific Scenario:**

1. Open feature file (e.g., `features/Login.feature`)
2. Right-click on scenario line
3. Select **Debug 'Scenario...'**
4. PyCharm will stop at breakpoints in step definitions

**Set Breakpoints in Step Definitions:**

1. Open step definition file (e.g., `features/steps/login_steps.py`)
2. Click in left gutter next to line number to set breakpoint (red dot appears)
3. Run tests in debug mode
4. Execution will pause at breakpoint
5. Use debug toolbar to step through code, inspect variables

**PyCharm Debug Shortcuts:**
- `F8` - Step Over
- `F7` - Step Into
- `Shift+F8` - Step Out
- `F9` - Resume Program
- `Ctrl+F8` - Toggle Breakpoint

### Visual Studio Code Configuration

VS Code is a lightweight, extensible editor with excellent Python support.

#### 1. Open Project in VS Code

```bash
# From command line
cd Testinium-QA
code .

# Or: Launch VS Code → File → Open Folder → Select Testinium-QA
```

#### 2. Install Required Extensions

1. Open **Extensions** view (`Ctrl+Shift+X`)
2. Search and install:
   - **Python** (ms-python.python) - Essential
   - **Cucumber (Gherkin) Full Support** (alexkrechik.cucumberautocomplete)
   - **Python Test Explorer** (littlefoxteam.vscode-python-test-adapter) - Optional
   - **GitLens** (eamodio.gitlens) - Optional but recommended
3. Reload VS Code if prompted

#### 3. Select Python Interpreter

1. Open Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Type **Python: Select Interpreter**
3. Select the virtual environment interpreter:
   - `./venv/bin/python` (macOS/Linux)
   - `.\venv\Scripts\python.exe` (Windows)
4. Status bar should show `3.x.x ('venv': venv)`

#### 4. Configure launch.json for Debugging

Create `.vscode/launch.json` for debugging configurations:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Behave All Tests",
            "type": "python",
            "request": "launch",
            "module": "behave",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Python: Behave Current Feature",
            "type": "python",
            "request": "launch",
            "module": "behave",
            "args": [
                "${file}"
            ],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Python: pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "-v",
                "tests/"
            ],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

**Usage**:
- Press `F5` to start debugging
- Select configuration from dropdown in Debug view
- Set breakpoints by clicking left of line numbers

#### 5. Configure settings.json (Optional)

Create/edit `.vscode/settings.json`:

```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true
    },
    "cucumberautocomplete.steps": [
        "features/steps/*.py"
    ],
    "cucumberautocomplete.syncfeatures": "features/**/*.feature"
}
```

#### 6. Using Integrated Terminal

VS Code's integrated terminal respects virtual environment:

1. Open terminal (`Ctrl+` `)
2. Virtual environment should auto-activate (you'll see `(venv)` prefix)
3. Run commands directly:
   ```bash
   behave
   behave --tags=@Login
   pytest tests/
   ```

---

## Running Tests Locally

Once setup is complete, you can run tests using various commands and options.

### Basic Test Execution

**Run All Tests:**
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Run all feature files
behave
```

**Run Specific Feature File:**
```bash
# Run only Login feature
behave features/Login.feature

# Run specific feature
behave features/Crm.feature
```

**Run Specific Scenario by Line Number:**
```bash
# Run scenario starting at line 10
behave features/Login.feature:10

# Run scenario at line 25
behave features/EmployeeFc.feature:25
```

### Tag-Based Execution

Tests can be filtered by tags defined in feature files (`@TagName`).

**Run Tests with Specific Tag:**
```bash
# Run only @Login tagged scenarios
behave --tags=@Login

# Run @SalesManager scenarios
behave --tags=@SalesManager

# Run @Smoke test suite
behave --tags=@Smoke
```

**Run Multiple Tags (OR logic):**
```bash
# Run scenarios tagged with @Login OR @Logout
behave --tags=@Login,@Logout
```

**Combine Tags (AND logic):**
```bash
# Run scenarios with both @Login AND @Smoke
behave --tags=@Login --tags=@Smoke
```

**Exclude Tags:**
```bash
# Run all scenarios except @WIP (Work in Progress)
behave --tags=~@WIP

# Exclude @Slow scenarios
behave --tags=~@Slow
```

**Complex Tag Expressions:**
```bash
# Run @Smoke tests but exclude @Slow ones
behave --tags=@Smoke --tags=~@Slow

# Run (@Login OR @Logout) AND @Critical
behave --tags=@Login,@Logout --tags=@Critical
```

### Verbose and Debug Modes

**Verbose Output (Shows Step Details):**
```bash
# Show detailed test execution
behave --verbose

# Show stack traces and Python output
behave --verbose --no-capture

# Maximum verbosity
behave -v -v
```

**Dry Run (Validate Without Execution):**
```bash
# Check which steps would run without executing
behave --dry-run

# Find undefined step definitions
behave --dry-run --no-summary
```

**Show Timings:**
```bash
# Display execution time for each step
behave --format=pretty --no-capture
```

### pytest Execution (Unit Tests)

Run framework unit tests with pytest:

```bash
# Run all unit tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_driver_manager.py

# Run specific test function
pytest tests/test_driver_manager.py::test_get_driver_chrome_default

# Run with coverage report
pytest tests/ --cov=utilities --cov=pages --cov=config
```

### Generating Reports Locally

**HTML Report:**
```bash
# Generate HTML report
behave --format=html --outfile=reports/report.html

# Open report in browser (macOS)
open reports/report.html

# Open report (Linux)
xdg-open reports/report.html

# Open report (Windows)
start reports/report.html
```

**JSON Report:**
```bash
# Generate JSON report for processing
behave --format=json --outfile=reports/cucumber.json
```

**Allure Report:**
```bash
# Generate Allure results
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results

# Serve Allure report (opens in browser)
allure serve reports/allure-results

# Generate static Allure report
allure generate reports/allure-results --clean -o reports/allure-report
```

**Multiple Report Formats:**
```bash
# Generate JSON and HTML simultaneously
behave --format=json --outfile=reports/cucumber.json --format=html --outfile=reports/report.html
```

**Source:** `README.md:139-191`

---

## Debugging Techniques

Effective debugging is essential for local development. Here are various debugging approaches.

### 1. Print Statement Debugging

Add print statements in step definitions to inspect values:

```python
# In features/steps/login_steps.py
@when('User enters "{username}" username')
def step_impl(context, username):
    print(f"DEBUG: Entering username: {username}")  # Debug output
    context.login_page.input_email.send_keys(username)
    print(f"DEBUG: Username entered successfully")
```

**Run with output visible:**
```bash
# Print statements appear with --no-capture flag
behave --no-capture

# Or use verbose mode
behave --verbose --no-capture
```

### 2. Python Debugger (pdb)

Use Python's built-in debugger for interactive debugging:

```python
# In any step definition or page object method
import pdb

@when('User clicks the login button')
def step_impl(context):
    pdb.set_trace()  # Execution pauses here
    context.login_page.login_button.click()
```

**pdb Commands:**
- `n` (next) - Execute next line
- `s` (step) - Step into function
- `c` (continue) - Continue execution
- `p variable` - Print variable value
- `pp variable` - Pretty-print variable
- `l` - List source code
- `w` - Show stack trace
- `q` - Quit debugger

**Run with pdb:**
```bash
behave --no-capture
# Test will pause at pdb.set_trace()
# Use pdb commands interactively
```

### 3. IDE Debugger (PyCharm)

**Set Breakpoint:**
1. Open step definition file
2. Click left gutter next to line number (red dot appears)
3. Right-click on feature file → **Debug 'Feature...'**
4. Execution pauses at breakpoint

**Debug Toolbar:**
- **Step Over** (F8) - Execute current line, move to next
- **Step Into** (F7) - Enter function/method
- **Step Out** (Shift+F8) - Exit current function
- **Resume** (F9) - Continue until next breakpoint
- **Evaluate Expression** (Alt+F8) - Inspect variables

**Variables View:**
- See all local and global variables
- Expand objects to inspect attributes
- Right-click variable → **Set Value** to modify during debugging

### 4. IDE Debugger (VS Code)

**Set Breakpoint:**
1. Open step definition file
2. Click left of line number (red dot appears)
3. Press `F5` → Select "Python: Behave Current Feature"
4. Execution pauses at breakpoint

**Debug Actions:**
- **Continue** (F5) - Resume execution
- **Step Over** (F10) - Execute current line
- **Step Into** (F11) - Enter function
- **Step Out** (Shift+F11) - Exit function
- **Restart** (Ctrl+Shift+F5) - Restart debugging

**Debug Console:**
- Evaluate expressions while paused
- Type variable names to inspect values
- Execute Python code in current context

### 5. Inspecting WebDriver State

When debugging browser interactions, inspect WebDriver state:

```python
# In step definition
@when('User clicks the login button')
def step_impl(context):
    driver = context.driver
    
    # Print current URL
    print(f"Current URL: {driver.current_url}")
    
    # Print page title
    print(f"Page title: {driver.title}")
    
    # Check if element exists
    elements = driver.find_elements(By.NAME, "login")
    print(f"Found {len(elements)} elements with name='login'")
    
    # Get element attributes
    button = context.login_page.login_button
    print(f"Button text: {button.text}")
    print(f"Button displayed: {button.is_displayed()}")
    print(f"Button enabled: {button.is_enabled()}")
    
    # Capture screenshot for manual inspection
    from utilities.screenshot_helper import capture_screenshot
    screenshot_path = capture_screenshot(driver, "debug_login_button")
    print(f"Screenshot saved: {screenshot_path}")
```

### 6. Browser Console Logs

Capture browser console logs for JavaScript errors:

```python
# In features/environment.py or step definition
def capture_browser_logs(driver):
    """Capture browser console logs"""
    logs = driver.get_log('browser')
    for log in logs:
        print(f"[{log['level']}] {log['message']}")

# Use in after_scenario hook
def after_scenario(context, scenario):
    if scenario.status == 'failed':
        capture_browser_logs(context.driver)
```

### 7. Slow Down Execution

Add delays to observe browser interactions:

```python
import time

@when('User enters "{username}" username')
def step_impl(context, username):
    context.login_page.input_email.send_keys(username)
    time.sleep(2)  # Pause for 2 seconds to observe
```

**Better approach: Use explicit waits**
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait and watch element interaction
wait = WebDriverWait(context.driver, 10)
element = wait.until(EC.visibility_of(context.login_page.input_email))
element.send_keys(username)
```

### 8. Screenshot on Every Step (Debug Mode)

Modify `features/environment.py` to capture screenshot after each step:

```python
def after_step(context, step):
    """Capture screenshot after each step in debug mode"""
    if context.config.userdata.get('debug') == 'true':
        from utilities.screenshot_helper import capture_screenshot
        screenshot_name = f"{step.name.replace(' ', '_')}"
        capture_screenshot(context.driver, screenshot_name)
```

**Run with debug mode:**
```bash
behave -D debug=true
```

**Source:** `README.md:686-714`

---

## Local Report Viewing

After test execution, view generated reports to analyze results.

### HTML Report

**Generate HTML Report:**
```bash
behave --format=html --outfile=reports/report.html
```

**View Report:**
```bash
# macOS
open reports/report.html

# Linux
xdg-open reports/report.html

# Windows
start reports/report.html

# Or open manually in any browser
# File → Open → Select reports/report.html
```

**HTML Report Contents:**
- Feature-by-feature breakdown
- Scenario pass/fail status
- Step execution details
- Execution timestamps
- Duration for each test

### Allure Report

Allure provides rich, interactive test reports with trends and analytics.

**Generate Allure Results:**
```bash
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results
```

**Serve Allure Report (Recommended for Local Viewing):**
```bash
# Install Allure command-line tool (one-time setup)
# macOS:
brew install allure

# Linux:
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure

# Windows (with Scoop):
scoop install allure

# Serve report (opens in browser automatically)
allure serve reports/allure-results
```

**Generate Static Allure Report:**
```bash
# Generate HTML report in reports/allure-report/
allure generate reports/allure-results --clean -o reports/allure-report

# Open generated report
open reports/allure-report/index.html  # macOS
xdg-open reports/allure-report/index.html  # Linux
start reports\allure-report\index.html  # Windows
```

**Allure Report Features:**
- Dashboard with test statistics
- Trend charts across multiple runs
- Test categorization by features
- Screenshot attachments for failures
- Execution timeline
- Suites and test case details

### JSON Report

JSON reports are useful for processing test results programmatically.

**Generate JSON Report:**
```bash
behave --format=json --outfile=reports/cucumber.json
```

**View JSON Report:**
```bash
# Pretty-print JSON in terminal
python -m json.tool reports/cucumber.json

# Or open in any text editor / JSON viewer
```

**Use Cases:**
- Custom report generation
- Integration with external tools
- CI/CD pipeline processing
- Test result analytics

### Screenshots

Failed test screenshots are automatically captured (configured in `features/environment.py`).

**Screenshot Location:**
```
reports/screenshots/
```

**View Screenshots:**
```bash
# List all screenshots
ls reports/screenshots/

# Open specific screenshot
open reports/screenshots/login_failure.png  # macOS
xdg-open reports/screenshots/login_failure.png  # Linux
start reports\screenshots\login_failure.png  # Windows
```

**Screenshot Naming Convention:**
```
{scenario_name}_{timestamp}.png
```

Example: `Users_log_in_with_valid_credentials_20240115_143022.png`

---

## Troubleshooting

Common issues encountered during local development and their solutions.

### Python Version Issues

**Issue: "Python version not supported"**

```bash
# Symptom:
ERROR: This package requires Python >=3.9

# Solution: Verify Python version
python --version
python3 --version

# If version < 3.9, upgrade Python:
# - Download from python.org
# - Or use version manager (pyenv recommended)
```

**Issue: Multiple Python versions installed**

```bash
# Solution: Use python3 explicitly
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Dependency Conflict Issues

**Issue: "ERROR: Cannot install X and Y because these package versions have conflicting dependencies"**

```bash
# Solution 1: Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Solution 2: Create fresh virtual environment
deactivate
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Solution 3: Install dependencies one by one to identify conflict
pip install selenium==4.15.2
pip install behave==1.2.6
# Continue one by one...
```

**Issue: "Package X is not compatible with this Python version"**

```bash
# Solution: Check requirements.txt for version constraints
# Verify Python version meets requirements (3.9-3.12)
# If using Python 3.13 (not yet tested), downgrade to 3.12
```

### Virtual Environment Issues

**Issue: Virtual environment not activating**

```bash
# Symptom: Prompt doesn't show (venv), pip installs globally

# Solution 1: Verify activation command
# macOS/Linux:
source venv/bin/activate

# Windows Command Prompt:
venv\Scripts\activate.bat

# Windows PowerShell:
venv\Scripts\Activate.ps1

# Solution 2: Recreate virtual environment
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
```

**Issue: "Command not found: behave" after installation**

```bash
# Symptom: behave command not found even after pip install

# Solution: Ensure virtual environment is activated
source venv/bin/activate

# Verify behave is installed in venv
which behave  # Should point to venv/bin/behave

# If still not found, reinstall
pip install --force-reinstall behave
```

### WebDriver Download Issues

**Issue: "WebDriverException: Message: 'chromedriver' executable needs to be in PATH"**

```bash
# This should NOT happen with webdriver-manager, but if it does:

# Solution 1: Verify webdriver-manager is installed
pip show webdriver-manager

# Solution 2: Reinstall webdriver-manager
pip install --upgrade webdriver-manager

# Solution 3: Manually trigger driver download
python
>>> from selenium import webdriver
>>> from webdriver_manager.chrome import ChromeDriverManager
>>> driver = webdriver.Chrome(ChromeDriverManager().install())
>>> driver.quit()
>>> exit()
```

**Issue: "ConnectionError: Network unreachable" during driver download**

```bash
# Symptom: Cannot download ChromeDriver/GeckoDriver

# Solution 1: Check internet connectivity
ping google.com

# Solution 2: Use proxy if behind corporate firewall
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
pip install --upgrade webdriver-manager

# Solution 3: Manual driver download (last resort)
# Download ChromeDriver from https://chromedriver.chromium.org/
# Place in PATH or project directory
```

### Browser Version Mismatch

**Issue: "SessionNotCreatedException: session not created: This version of ChromeDriver only supports Chrome version X"**

```bash
# Symptom: Browser version doesn't match driver version

# Solution 1: Update browser
# Chrome: Help → About Google Chrome (auto-updates)
# Firefox: Help → About Firefox (auto-updates)

# Solution 2: Clear driver cache and re-download
rm -rf ~/.wdm/  # Driver cache location
# Next test run will download matching driver

# Solution 3: Explicitly set driver version (if needed)
# In driver_manager.py, pass version parameter:
ChromeDriverManager(version="114.0.5735.90").install()
```

**Issue: "Browser not starting in headless mode"**

```bash
# Symptom: Tests fail with headless=true but work with headless=false

# Solution 1: Add required headless arguments
# In utilities/driver_manager.py, ensure:
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Solution 2: Use config.yaml setting
browser:
  headless: true

# Solution 3: Check for headless-specific issues
# Some tests may require visible browser (CAPTCHA, etc.)
```

### Port Conflicts

**Issue: "Address already in use" when running tests**

```bash
# Symptom: Port conflict if running multiple test instances

# Solution 1: Kill existing process
# Find process using port
lsof -i :4444  # macOS/Linux
netstat -ano | findstr :4444  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Solution 2: Wait for previous test run to complete
# Don't run multiple behave instances simultaneously

# Solution 3: Use different ports if running parallel tests
# Configure in behave.ini or environment variables
```

### Configuration Issues

**Issue: "Tests using wrong environment URL"**

```bash
# Symptom: Tests connect to wrong BASE_URL

# Solution: Check configuration precedence
# 1. Verify .env file exists and contains BASE_URL
cat .env | grep BASE_URL

# 2. Verify .env is being loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('BASE_URL'))"

# 3. Check config.yaml doesn't override
cat config/config.yaml | grep base_url

# 4. Explicitly set environment variable
export BASE_URL=https://correct-url.example.com
behave
```

**Issue: "Credentials not working"**

```bash
# Symptom: Login tests fail with valid credentials

# Solution 1: Verify .env file contains correct credentials
cat .env | grep USERNAME
cat .env | grep PASSWORD

# Solution 2: Check for spaces or special characters
# Edit .env carefully, no spaces around =
TEST_USERNAME=user@example.com
TEST_PASSWORD=password123

# Solution 3: Test credential loading
python
>>> from utilities.config_reader import ConfigReader
>>> config = ConfigReader()
>>> print(config.get_property('credentials.test.username'))
>>> exit()
```

### Import Errors

**Issue: "ModuleNotFoundError: No module named 'utilities'"**

```bash
# Symptom: Python can't find project modules

# Solution 1: Run from project root directory
pwd  # Verify you're in Testinium-QA/
behave

# Solution 2: Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
behave

# Solution 3: Ensure __init__.py exists in packages
ls utilities/__init__.py
ls pages/__init__.py
ls config/__init__.py

# Solution 4: Verify virtual environment is activated
source venv/bin/activate
```

### Test Execution Errors

**Issue: "Undefined step" errors**

```bash
# Symptom: Step definition not found

# Solution 1: Check step text matches exactly
# Compare feature file with step definition (case-sensitive)

# Solution 2: Verify step definitions are in features/steps/
ls features/steps/*.py

# Solution 3: Check for typos in step text
behave --dry-run  # Shows undefined steps

# Solution 4: Verify step imports context parameter
# Correct:
@when('User clicks button')
def step_impl(context):  # 'context' parameter required
    pass
```

**Issue: "StaleElementReferenceException"**

```bash
# Symptom: Element no longer exists in DOM

# Solution: Framework already uses property-based locators
# Elements are re-located on each access

# If issue persists, add explicit wait:
from utilities.wait_helpers import WaitHelpers
wait_helpers = WaitHelpers(driver)
element = wait_helpers.wait_for_element(locator, timeout=10)
```

**Issue: Tests passing locally but would fail in CI**

```bash
# Common causes:
# 1. Timing issues (implicit waits, sleep statements)
# 2. Hardcoded paths
# 3. Display resolution differences

# Solutions:
# 1. Use only explicit waits (already implemented)
# 2. Use relative paths, not absolute
# 3. Test in headless mode locally:
export HEADLESS=true
behave

# 4. Test with same window size as CI:
# In config.yaml:
browser:
  window_size: 1920x1080
```

### IDE-Specific Issues

**PyCharm: "Cannot find Python interpreter"**

```bash
# Solution:
# Settings → Project → Python Interpreter
# Click gear → Add → Existing environment
# Browse to venv/bin/python
```

**VS Code: "Python extension not working"**

```bash
# Solution:
# 1. Reload window: Ctrl+Shift+P → "Developer: Reload Window"
# 2. Reinstall Python extension
# 3. Select interpreter: Ctrl+Shift+P → "Python: Select Interpreter"
```

**Both: Debugger not stopping at breakpoints**

```bash
# Solution:
# 1. Ensure you're running in debug mode (not normal run)
# 2. Verify breakpoint is on executable line (not blank/comment)
# 3. Check breakpoint is enabled (red dot, not gray)
# 4. Try adding: import pdb; pdb.set_trace()
```

### Performance Issues

**Issue: Tests running very slowly**

```bash
# Solutions:
# 1. Reduce explicit wait timeouts for local testing
# In config.yaml:
timeouts:
  explicit: 5  # Reduce from 10 if application is responsive

# 2. Disable screenshot capture for passing tests
# In features/environment.py, only capture on failure (already implemented)

# 3. Use headless mode for faster execution
export HEADLESS=true
behave

# 4. Disable browser extensions and DevTools
# In utilities/driver_manager.py:
chrome_options.add_argument('--disable-extensions')
```

**Issue: High memory/CPU usage**

```bash
# Solutions:
# 1. Close unused browser instances
ps aux | grep chrome  # Find stray processes
kill -9 <PID>

# 2. Limit parallel execution
behave  # Run serially instead of parallel

# 3. Increase timeout for slower machines
# In config.yaml:
timeouts:
  explicit: 15
  page_load: 45
```

### Getting Help

If you encounter issues not covered here:

1. **Check Documentation**: See main [README.md](../../README.md) and other [deployment guides](index.md)
2. **Search Issues**: Check GitHub repository issues for similar problems
3. **Enable Verbose Logging**: Run `behave --verbose --no-capture` for detailed output
4. **Review Logs**: Check `reports/` directory for error logs and screenshots
5. **Ask for Help**: Create detailed issue on GitHub with:
   - Error message (full stack trace)
   - Steps to reproduce
   - Environment details (OS, Python version, browser version)
   - Configuration files (sanitize credentials)

**Source:** `README.md:602-714`

---

## Next Steps

Now that you have the framework running locally, explore these resources:

- **[Quick Start Guide](../getting-started/quick-start.md)**: 5-minute introduction to running your first test
- **[Configuration Management](../guides/configuration-management.md)**: Advanced configuration options
- **[Page Object Model Guide](../guides/page-object-model.md)**: Creating new page objects
- **[Writing Step Definitions](../guides/step-definitions.md)**: Adding new test steps
- **[Deployment Guides](index.md)**: Other deployment options (Docker, Kubernetes, CI/CD)

---

**Document Version**: 1.0.0  
**Last Updated**: 2024-01-15  
**Maintained By**: Testinium QA Team

