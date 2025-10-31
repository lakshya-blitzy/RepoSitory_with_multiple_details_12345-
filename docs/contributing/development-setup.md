# Development Environment Setup

This guide provides comprehensive instructions for setting up a local development environment for contributing to the Testinium QA Python test automation framework.

## Overview

This document covers:
- Python installation and version management
- Virtual environment setup
- Dependency installation
- IDE configuration
- Pre-commit hooks
- Development tools verification
- WebDriver setup
- Configuration management

## Prerequisites

Before you begin, ensure your system meets these requirements:

### System Requirements

- **Operating System:** Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+, Fedora 35+, etc.)
- **RAM:** Minimum 4GB (8GB+ recommended for running browsers during testing)
- **Disk Space:** At least 2GB free space for Python, dependencies, and browser drivers
- **Internet Connection:** Required for installing dependencies and downloading WebDriver binaries

### Required Software

#### Python 3.9-3.12

The framework supports Python versions 3.9 through 3.12. We recommend using the latest stable version (3.12) for optimal performance and security.

**Check if Python is installed:**
```bash
python3 --version
# or on Windows:
python --version
```

**Expected output:**
```
Python 3.12.0  # or 3.9.x, 3.10.x, 3.11.x
```

#### Installing Python

=== "Windows"

    **Option 1: Official Python Installer (Recommended)**
    
    1. Download Python from [python.org/downloads](https://www.python.org/downloads/)
    2. Run the installer
    3. **IMPORTANT:** Check "Add Python to PATH" during installation
    4. Select "Install Now" or customize installation location
    5. Verify installation:
       ```cmd
       python --version
       pip --version
       ```
    
    **Option 2: Windows Package Manager (winget)**
    
    ```powershell
    # Install latest Python 3.12
    winget install Python.Python.3.12
    
    # Verify installation
    python --version
    ```
    
    **Option 3: Chocolatey**
    
    ```powershell
    # Install Chocolatey first: https://chocolatey.org/install
    choco install python --version=3.12.0
    ```

=== "macOS"

    **Option 1: Official Python Installer**
    
    1. Download Python from [python.org/downloads/macos](https://www.python.org/downloads/macos/)
    2. Open the `.pkg` file and follow installation wizard
    3. Verify installation:
       ```bash
       python3 --version
       pip3 --version
       ```
    
    **Option 2: Homebrew (Recommended)**
    
    ```bash
    # Install Homebrew if not already installed
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Install Python 3.12
    brew install python@3.12
    
    # Link Python 3.12
    brew link python@3.12
    
    # Verify installation
    python3 --version
    ```
    
    **Option 3: pyenv (for multiple Python versions)**
    
    ```bash
    # Install pyenv
    brew install pyenv
    
    # Add to shell configuration (~/.zshrc or ~/.bash_profile)
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    source ~/.zshrc
    
    # Install Python 3.12
    pyenv install 3.12.0
    pyenv global 3.12.0
    
    # Verify installation
    python --version
    ```

=== "Linux"

    **Ubuntu/Debian:**
    
    ```bash
    # Update package index
    sudo apt update
    
    # Install Python 3.12 and pip
    sudo apt install python3.12 python3.12-venv python3-pip
    
    # Verify installation
    python3.12 --version
    pip3 --version
    ```
    
    **Fedora/RHEL/CentOS:**
    
    ```bash
    # Install Python 3.12
    sudo dnf install python3.12 python3.12-pip
    
    # Verify installation
    python3.12 --version
    pip3 --version
    ```
    
    **Using pyenv (any Linux distribution):**
    
    ```bash
    # Install dependencies
    sudo apt install -y make build-essential libssl-dev zlib1g-dev \
         libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
         libncurses5-dev libncursesw5-dev xz-utils tk-dev
    
    # Install pyenv
    curl https://pyenv.run | bash
    
    # Add to ~/.bashrc or ~/.zshrc
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    source ~/.bashrc
    
    # Install Python 3.12
    pyenv install 3.12.0
    pyenv global 3.12.0
    
    # Verify installation
    python --version
    ```

#### Git Version Control

Git is required for cloning the repository and committing changes.

**Check if Git is installed:**
```bash
git --version
```

**Install Git:**

=== "Windows"
    ```powershell
    # Download from: https://git-scm.com/download/win
    # Or use winget:
    winget install Git.Git
    ```

=== "macOS"
    ```bash
    # Using Homebrew:
    brew install git
    ```

=== "Linux"
    ```bash
    # Ubuntu/Debian:
    sudo apt install git
    
    # Fedora/RHEL:
    sudo dnf install git
    ```

## Clone the Repository

```bash
# Clone via HTTPS
git clone https://github.com/BalamiRR/Testinium-QA.git
cd Testinium-QA

# Or clone via SSH (if you have SSH keys configured)
git clone git@github.com:BalamiRR/Testinium-QA.git
cd Testinium-QA
```

## Virtual Environment Setup

Virtual environments isolate project dependencies from your system Python installation, preventing version conflicts.

### Option 1: Using venv (Standard Library - Recommended)

**Create Virtual Environment:**

=== "macOS/Linux"
    ```bash
    # Create virtual environment
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Your prompt should now show (venv)
    ```

=== "Windows (Command Prompt)"
    ```cmd
    # Create virtual environment
    python -m venv venv
    
    # Activate virtual environment
    venv\Scripts\activate.bat
    
    # Your prompt should now show (venv)
    ```

=== "Windows (PowerShell)"
    ```powershell
    # Create virtual environment
    python -m venv venv
    
    # Activate virtual environment
    venv\Scripts\Activate.ps1
    
    # If you get execution policy error, run:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

**Verify Activation:**
```bash
# Check that Python is using virtual environment
which python  # macOS/Linux
where python  # Windows

# Expected: path should point to venv/bin/python or venv\Scripts\python.exe
```

**Deactivate Virtual Environment (when done):**
```bash
deactivate
```

### Option 2: Using Poetry (Advanced)

Poetry provides advanced dependency management and packaging features.

**Install Poetry:**

=== "macOS/Linux"
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    
    # Add Poetry to PATH (add to ~/.bashrc or ~/.zshrc)
    export PATH="$HOME/.local/bin:$PATH"
    source ~/.bashrc  # or ~/.zshrc
    
    # Verify installation
    poetry --version
    ```

=== "Windows (PowerShell)"
    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    
    # Add to PATH (Poetry installer will show instructions)
    
    # Verify installation
    poetry --version
    ```

**Create and Activate Environment with Poetry:**
```bash
# Install dependencies and create virtual environment
poetry install

# Activate Poetry-managed virtual environment
poetry shell

# Your prompt should now show the virtualenv name
```

**Project Structure After Setup:**
```
testinium-qa-python/
├── venv/                      # Virtual environment (if using venv)
│   ├── bin/                   # Executables (macOS/Linux)
│   ├── Scripts/               # Executables (Windows)
│   ├── lib/                   # Installed packages
│   └── ...
├── .venv/                     # Virtual environment (if using Poetry)
├── config/
├── features/
├── pages/
├── utilities/
├── requirements.txt
├── pyproject.toml
└── ...
```

## Dependency Installation

### Install Production Dependencies

**Using pip (from requirements.txt):**
```bash
# Ensure virtual environment is activated
# You should see (venv) in your prompt

# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

**Using Poetry (from pyproject.toml):**
```bash
# Install production dependencies only
poetry install --no-dev

# Or install with development dependencies
poetry install
```

### Install Development Dependencies

Development dependencies include code quality tools (pylint, black, mypy, etc.).

**Using pip:**
```bash
# Development dependencies are already in requirements.txt
# To install them separately, create requirements-dev.txt with:
# pylint==3.0.3
# black==23.12.1
# mypy==1.7.1
# isort==5.13.0
# flake8==7.0.0
# bandit==1.7.5
# pytest-cov==4.1.0

# Install dev dependencies (if you have requirements-dev.txt)
pip install -r requirements-dev.txt
```

**Using Poetry:**
```bash
# Development dependencies are in pyproject.toml [tool.poetry.group.dev.dependencies]
# They are installed automatically with:
poetry install

# To install only dev dependencies:
poetry install --only dev
```

### Key Dependencies Installed

| Package | Version | Purpose |
|---------|---------|---------|
| selenium | 4.15.2 | WebDriver automation |
| behave | 1.2.6 | BDD test framework |
| pytest | 7.4.3 | Testing framework |
| webdriver-manager | 4.0.1 | Automatic WebDriver binary management |
| python-dotenv | 1.0.0 | Environment variable management |
| PyYAML | 6.0.1 | YAML configuration parsing |
| allure-behave | 2.13.2 | Enhanced test reporting |
| pylint | 3.0.3 | Code linting (dev) |
| black | 23.12.1 | Code formatting (dev) |
| mypy | 1.7.1 | Static type checking (dev) |
| isort | 5.13.0 | Import sorting (dev) |

**Source:** `requirements.txt` and `pyproject.toml`

## IDE Configuration

### Visual Studio Code (VS Code)

VS Code is a lightweight, powerful IDE with excellent Python support.

#### Install VS Code

Download from [code.visualstudio.com](https://code.visualstudio.com/)

#### Required Extensions

Install these extensions from VS Code marketplace (Ctrl+Shift+X or Cmd+Shift+X):

1. **Python** (ms-python.python)
   - Provides IntelliSense, debugging, linting
   - Essential for Python development

2. **Pylint** (ms-python.pylint)
   - Python linting integration
   - Highlights code quality issues

3. **Black Formatter** (ms-python.black-formatter)
   - Automatic code formatting
   - Formats code on save

4. **Behave VSCode** (jimasp.behave-vscode)
   - Gherkin syntax highlighting
   - Feature file support

5. **autoDocstring** (njpwerner.autodocstring)
   - Generate Python docstrings automatically
   - Supports Google-style docstrings

6. **GitLens** (eamodio.gitlens)
   - Enhanced Git integration
   - View file history, blame annotations

#### Workspace Settings

Create `.vscode/settings.json` in project root:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintPath": "${workspaceFolder}/venv/bin/pylint",
    "python.formatting.provider": "black",
    "python.formatting.blackPath": "${workspaceFolder}/venv/bin/black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "editor.formatOnSave": true,
    "editor.rulers": [100],
    "python.testing.pytestEnabled": true,
    "python.testing.pytestPath": "${workspaceFolder}/venv/bin/pytest",
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": [
        "tests",
        "-v"
    ],
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "python.analysis.extraPaths": [
        "${workspaceFolder}/pages",
        "${workspaceFolder}/utilities",
        "${workspaceFolder}/config",
        "${workspaceFolder}/features"
    ],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/venv": false,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true
    },
    "python.analysis.typeCheckingMode": "basic",
    "cucumberautocomplete.steps": [
        "features/steps/*.py"
    ],
    "cucumberautocomplete.syncfeatures": "features/**/*.feature"
}
```

#### Launch Configuration for Debugging

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Behave: Run Current Feature",
            "type": "python",
            "request": "launch",
            "module": "behave",
            "args": [
                "${file}",
                "--no-capture"
            ],
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Pytest: Run All Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": [
                "tests/",
                "-v"
            ],
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

**Source:** Based on `pyproject.toml` tool configurations

### PyCharm (Professional or Community)

PyCharm provides comprehensive Python IDE features out of the box.

#### Install PyCharm

Download from [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)
- **Professional Edition:** Full features (paid, free for students/open-source)
- **Community Edition:** Free, suitable for this project

#### Configure Python Interpreter

1. Open PyCharm
2. Open the project: `File` → `Open` → Select `testinium-qa-python` directory
3. Configure interpreter:
   - `File` → `Settings` (Windows/Linux) or `PyCharm` → `Preferences` (macOS)
   - `Project: testinium-qa-python` → `Python Interpreter`
   - Click gear icon → `Add Interpreter` → `Existing`
   - Select `venv/bin/python` (macOS/Linux) or `venv\Scripts\python.exe` (Windows)
   - Click `OK`

#### Configure Code Style

1. `File` → `Settings` → `Editor` → `Code Style` → `Python`
2. Set `Hard wrap at: 100` (matches Black configuration)
3. Enable `Wrap on typing: Yes`
4. `Tabs and Indents`:
   - Tab size: 4
   - Indent: 4
   - Continuation indent: 4

#### Enable Plugins

1. `File` → `Settings` → `Plugins`
2. Install/Enable:
   - **Gherkin** (Cucumber/Gherkin syntax support)
   - **Markdown** (documentation editing)
   - **Requirements** (requirements.txt support)
   - **.ignore** (gitignore support)

#### Configure External Tools (Black, Pylint, Mypy)

**Black Formatter:**
1. `File` → `Settings` → `Tools` → `External Tools` → `+` (Add)
2. Name: `Black`
3. Program: `$PyInterpreterDirectory$/black`
4. Arguments: `--line-length 100 $FilePath$`
5. Working directory: `$ProjectFileDir$`
6. Click `OK`

**Pylint:**
1. `File` → `Settings` → `Tools` → `External Tools` → `+` (Add)
2. Name: `Pylint`
3. Program: `$PyInterpreterDirectory$/pylint`
4. Arguments: `$FilePath$`
5. Working directory: `$ProjectFileDir$`
6. Click `OK`

**Usage:** Right-click on any Python file → `External Tools` → `Black` or `Pylint`

#### Configure Run Configurations

**Behave Tests:**
1. `Run` → `Edit Configurations` → `+` → `Python`
2. Name: `Behave All Tests`
3. Script path: `venv/bin/behave` (or `venv\Scripts\behave.exe` on Windows)
4. Parameters: `features/`
5. Working directory: `$ProjectFileDir$`
6. Click `OK`

**pytest Tests:**
1. `Run` → `Edit Configurations` → `+` → `Python tests` → `pytest`
2. Name: `pytest All Tests`
3. Target: `Script path`
4. Script: `tests/`
5. Click `OK`

**Source:** Based on `pyproject.toml` [tool.black] and [tool.pylint] configurations

## Pre-Commit Hooks Setup

Pre-commit hooks automatically run code quality checks before each commit, ensuring consistent code style.

### Install Pre-Commit Tool

```bash
# Install pre-commit (if not in requirements.txt)
pip install pre-commit

# Verify installation
pre-commit --version
```

### Create Pre-Commit Configuration

Create `.pre-commit-config.yaml` in project root:

```yaml
# Pre-commit hooks for Testinium QA Python
# See https://pre-commit.com for more information

repos:
  # General file checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: debug-statements

  # Black code formatter
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        args: ['--line-length=100']
        language_version: python3.9

  # isort import sorter
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ['--profile', 'black', '--line-length', '100']

  # Pylint linter
  - repo: https://github.com/PyCQA/pylint
    rev: v3.0.3
    hooks:
      - id: pylint
        args: ['--max-line-length=100']
        additional_dependencies:
          - selenium
          - behave
          - pytest
          - PyYAML
          - python-dotenv

  # Mypy type checker
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        args: ['--ignore-missing-imports']
        additional_dependencies:
          - types-PyYAML
          - types-requests

  # Security checks with bandit
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']
        additional_dependencies: ['bandit[toml]']
```

### Install Git Hooks

```bash
# Install the git hook scripts
pre-commit install

# Expected output:
# pre-commit installed at .git/hooks/pre-commit
```

### Test Pre-Commit Hooks

```bash
# Run all hooks on all files (first-time setup)
pre-commit run --all-files

# Expected: All checks should pass
# If failures occur, pre-commit will auto-fix some issues
# Review and commit the fixes
```

### Manual Hook Execution

You can run pre-commit hooks manually without committing:

```bash
# Run all hooks on staged files
pre-commit run

# Run specific hook on all files
pre-commit run black --all-files
pre-commit run pylint --all-files
pre-commit run mypy --all-files

# Skip hooks for a commit (not recommended)
git commit --no-verify -m "Commit message"
```

**Source:** Based on `pyproject.toml` tool configurations for Black, isort, Pylint, and Mypy

## Development Tools Verification

After installing dependencies, verify all development tools are working correctly.

### Python and pip

```bash
# Check Python version
python --version
# Expected: Python 3.9.x - 3.12.x

# Check pip version
pip --version
# Expected: pip 23.x or higher

# Check virtual environment is active
which python  # macOS/Linux: should show path to venv/bin/python
where python  # Windows: should show path to venv\Scripts\python.exe
```

### Core Testing Frameworks

```bash
# Verify Selenium installation
python -c "import selenium; print(f'Selenium: {selenium.__version__}')"
# Expected: Selenium: 4.15.2

# Verify Behave installation
behave --version
# Expected: behave 1.2.6

# Verify pytest installation
pytest --version
# Expected: pytest 7.4.3
```

### WebDriver Manager

```bash
# Verify webdriver-manager installation
python -c "from webdriver_manager.chrome import ChromeDriverManager; print('WebDriver Manager: OK')"
# Expected: WebDriver Manager: OK
```

### Code Quality Tools

```bash
# Check Black formatter
black --version
# Expected: black, 23.12.1 (compiled: yes)

# Check Pylint linter
pylint --version
# Expected: pylint 3.0.3

# Check Mypy type checker
mypy --version
# Expected: mypy 1.7.1 (compiled: yes)

# Check isort import sorter
isort --version
# Expected: 5.13.0
```

### Configuration Parsers

```bash
# Verify python-dotenv
python -c "import dotenv; print('python-dotenv: OK')"
# Expected: python-dotenv: OK

# Verify PyYAML
python -c "import yaml; print('PyYAML: OK')"
# Expected: PyYAML: OK
```

### All-In-One Verification Script

Create a file `verify_setup.py` in project root:

```python
#!/usr/bin/env python3
"""
Verify Development Environment Setup
Checks all required dependencies and tools are installed correctly.
"""

import sys

def check_import(module_name, display_name=None):
    """Check if a module can be imported."""
    if display_name is None:
        display_name = module_name
    try:
        __import__(module_name)
        print(f"✓ {display_name}: OK")
        return True
    except ImportError as e:
        print(f"✗ {display_name}: FAILED - {e}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Development Environment Verification")
    print("=" * 60)
    print()
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    if sys.version_info < (3, 9):
        print("✗ Python 3.9+ required")
        return False
    print("✓ Python version: OK")
    print()
    
    # Core dependencies
    print("Checking core dependencies...")
    checks = [
        ("selenium", "Selenium WebDriver"),
        ("behave", "Behave BDD Framework"),
        ("pytest", "pytest Testing Framework"),
        ("webdriver_manager", "WebDriver Manager"),
        ("dotenv", "python-dotenv"),
        ("yaml", "PyYAML"),
        ("allure_behave", "Allure Behave Reporter"),
    ]
    
    core_ok = all(check_import(module, display) for module, display in checks)
    print()
    
    # Development tools
    print("Checking development tools...")
    dev_checks = [
        ("pylint", "Pylint Linter"),
        ("black", "Black Formatter"),
        ("mypy", "Mypy Type Checker"),
        ("isort", "isort Import Sorter"),
    ]
    
    dev_ok = all(check_import(module, display) for module, display in dev_checks)
    print()
    
    # Summary
    print("=" * 60)
    if core_ok and dev_ok:
        print("✓ All checks passed! Environment is ready for development.")
        print("=" * 60)
        return True
    else:
        print("✗ Some checks failed. Please review and install missing dependencies.")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

**Run verification:**
```bash
python verify_setup.py
```

**Expected output:**
```
============================================================
Development Environment Verification
============================================================

Python Version: 3.12.0 (main, Oct  2 2023, 12:00:00)
✓ Python version: OK

Checking core dependencies...
✓ Selenium WebDriver: OK
✓ Behave BDD Framework: OK
✓ pytest Testing Framework: OK
✓ WebDriver Manager: OK
✓ python-dotenv: OK
✓ PyYAML: OK
✓ Allure Behave Reporter: OK

Checking development tools...
✓ Pylint Linter: OK
✓ Black Formatter: OK
✓ Mypy Type Checker: OK
✓ isort Import Sorter: OK

============================================================
✓ All checks passed! Environment is ready for development.
============================================================
```

**Source:** Dependencies from `requirements.txt` and `pyproject.toml`

## WebDriver Setup

The framework uses `webdriver-manager` for automatic WebDriver binary management. No manual driver downloads are required!

### How WebDriver Manager Works

1. **First Run:** When you run tests for the first time, `webdriver-manager` automatically:
   - Detects your installed browser versions
   - Downloads the matching WebDriver binaries (ChromeDriver, GeckoDriver)
   - Caches binaries in `~/.wdm/` directory

2. **Subsequent Runs:** Uses cached WebDriver binaries for faster test startup

3. **Updates:** Automatically downloads new WebDriver versions when your browser updates

### Browser Installation

Ensure you have at least one of these browsers installed:

**Google Chrome:**
- Download from [google.com/chrome](https://www.google.com/chrome/)
- Or use package manager:
  ```bash
  # macOS
  brew install --cask google-chrome
  
  # Ubuntu/Debian
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  sudo dpkg -i google-chrome-stable_current_amd64.deb
  ```

**Mozilla Firefox:**
- Download from [mozilla.org/firefox](https://www.mozilla.org/firefox/)
- Or use package manager:
  ```bash
  # macOS
  brew install --cask firefox
  
  # Ubuntu/Debian
  sudo apt install firefox
  ```

### Verify WebDriver Functionality

Create a test script `test_webdriver.py`:

```python
"""
Quick test to verify WebDriver setup is working.
"""
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def test_chrome_driver():
    """Test Chrome WebDriver setup."""
    print("Testing Chrome WebDriver...")
    
    # Create Chrome driver with webdriver-manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # Navigate to test page
    driver.get("https://www.google.com")
    print(f"Page title: {driver.title}")
    
    # Cleanup
    driver.quit()
    print("✓ Chrome WebDriver: OK")

if __name__ == "__main__":
    test_chrome_driver()
```

**Run test:**
```bash
python test_webdriver.py
```

**Expected output:**
```
Testing Chrome WebDriver...
[WDM] - ====== WebDriver manager ======
[WDM] - Current google-chrome version is 120.0.6099
[WDM] - Get LATEST chromedriver version for google-chrome
[WDM] - Driver [/Users/username/.wdm/drivers/chromedriver/120.0.6099/chromedriver] found in cache
Page title: Google
✓ Chrome WebDriver: OK
```

**Source:** `utilities/driver_manager.py` implementation

### Configure Browser Preferences

Edit `config/config.yaml` to customize browser behavior:

```yaml
browser:
  type: chrome  # Options: chrome, firefox
  headless: false  # Set to true for CI/CD or background execution
  window_size: 1920x1080  # Browser window dimensions

timeouts:
  explicit: 10  # Default explicit wait timeout (seconds)
  page_load: 30  # Page load timeout (seconds)
```

**Source:** `config/config.yaml`

## Configuration Setup

### Create Environment Variables File

The `.env` file stores environment-specific configurations and credentials. **Never commit this file to version control.**

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual values
nano .env  # or use any text editor
```

**Example `.env` file:**
```ini
# Browser Configuration
BROWSER_TYPE=chrome
HEADLESS=false

# Application URL
BASE_URL=https://testinium-demo.com

# Test Timeouts (seconds)
TIMEOUT_EXPLICIT=10
TIMEOUT_PAGE_LOAD=30

# Test Credentials (use test accounts, not real credentials)
TEST_USERNAME=salesmanager7@info.com
TEST_PASSWORD=salesmanager

POSMANAGER_USERNAME=posmanager5@info.com
POSMANAGER_PASSWORD=posmanager

SALESMANAGER_USERNAME=salesmanager7@info.com
SALESMANAGER_PASSWORD=salesmanager

# Reporting Configuration
SCREENSHOTS_ON_FAILURE=true
ALLURE_RESULTS_DIR=reports/allure-results

# Logging
LOG_LEVEL=INFO
```

**Security Note:** The `.env` file is already in `.gitignore` and will not be committed.

**Source:** `.env.example`

### Verify Configuration Loading

Test that configuration is loaded correctly:

```python
# test_config_load.py
"""Test configuration loading."""
from config.test_config import get_config

config = get_config()
print(f"Browser Type: {config.browser.type}")
print(f"Headless Mode: {config.browser.headless}")
print(f"Base URL: {config.application.base_url}")
print(f"Explicit Timeout: {config.timeouts.explicit} seconds")
print("✓ Configuration loaded successfully")
```

**Run test:**
```bash
python test_config_load.py
```

**Expected output:**
```
Browser Type: chrome
Headless Mode: False
Base URL: https://testinium-demo.com
Explicit Timeout: 10 seconds
✓ Configuration loaded successfully
```

**Source:** `config/test_config.py`

## Run a Test to Verify Setup

Verify your complete development environment by running an actual test:

```bash
# Run a single feature file
behave features/Login.feature

# Or run with specific tag
behave --tags=@Login

# Or run all tests
behave
```

**Expected output:**
```
Feature: Testinium app login feature  # features/Login.feature:2

  Background:   # features/Login.feature:7

  Scenario Outline: Users log in with valid credentials  # features/Login.feature:18
    Given User is on the Testinium login page              # features/steps/login_steps.py:12
    When User enters "salesmanager7@info.com" username    # features/steps/login_steps.py:18
    And User enters "salesmanager" password               # features/steps/login_steps.py:24
    And User clicks the login button                      # features/steps/login_steps.py:30
    Then User should see the dashboard                    # features/steps/login_steps.py:36

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
5 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m15.234s
```

## Troubleshooting

### Issue 1: Python Not Found

**Symptoms:**
```bash
$ python --version
bash: python: command not found
```

**Solutions:**

=== "macOS/Linux"
    ```bash
    # Try python3 instead
    python3 --version
    
    # Create alias (add to ~/.bashrc or ~/.zshrc)
    echo 'alias python=python3' >> ~/.bashrc
    source ~/.bashrc
    
    # Or create symlink
    sudo ln -s /usr/bin/python3 /usr/bin/python
    ```

=== "Windows"
    ```cmd
    # Python not in PATH
    # Reinstall Python and check "Add Python to PATH" option
    # Or manually add to PATH:
    # System Properties → Environment Variables → Path → Add:
    # C:\Python312
    # C:\Python312\Scripts
    ```

### Issue 2: Virtual Environment Activation Fails

**Symptoms (Windows PowerShell):**
```powershell
PS> venv\Scripts\Activate.ps1
cannot be loaded because running scripts is disabled on this system
```

**Solution:**
```powershell
# Change execution policy for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
venv\Scripts\Activate.ps1
```

**Symptoms (Permission Denied):**
```bash
$ source venv/bin/activate
-bash: venv/bin/activate: Permission denied
```

**Solution:**
```bash
# Make script executable
chmod +x venv/bin/activate

# Then activate
source venv/bin/activate
```

### Issue 3: Dependency Installation Failures

**Symptoms:**
```bash
$ pip install -r requirements.txt
ERROR: Could not find a version that satisfies the requirement selenium==4.15.2
```

**Solutions:**

**Check Python version:**
```bash
python --version
# Must be 3.9 or higher
```

**Upgrade pip:**
```bash
python -m pip install --upgrade pip
```

**Clear pip cache:**
```bash
pip cache purge
pip install -r requirements.txt
```

**Install with verbose output:**
```bash
pip install -r requirements.txt --verbose
```

**Network issues (use alternative index):**
```bash
pip install -r requirements.txt --index-url https://mirrors.aliyun.com/pypi/simple/
```

### Issue 4: ChromeDriver/GeckoDriver Issues

**Symptoms:**
```bash
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: 
This version of ChromeDriver only supports Chrome version 119
Current browser version is 120.0.6099.109
```

**Solutions:**

**Update browser:**
- Chrome: `Help` → `About Google Chrome` (auto-updates)
- Firefox: `Help` → `About Firefox` (auto-updates)

**Clear WebDriver cache:**
```bash
# Remove cached drivers
rm -rf ~/.wdm/  # macOS/Linux
rmdir /s %USERPROFILE%\.wdm\  # Windows

# Next test run will download fresh drivers
```

**Manually specify driver version (if needed):**
```python
# In utilities/driver_manager.py
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager(version="120.0.6099").install())
```

### Issue 5: Import Errors

**Symptoms:**
```bash
$ python features/steps/login_steps.py
ModuleNotFoundError: No module named 'pages'
```

**Solutions:**

**Ensure running from project root:**
```bash
# Check current directory
pwd
# Should show: /path/to/testinium-qa-python

# If not, navigate to project root
cd /path/to/testinium-qa-python
```

**Add project root to PYTHONPATH:**
```bash
# Temporary (current session)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export PYTHONPATH="${PYTHONPATH}:/path/to/testinium-qa-python"' >> ~/.bashrc
source ~/.bashrc
```

**Verify __init__.py files exist:**
```bash
# These files must exist for Python to recognize packages
ls config/__init__.py
ls pages/__init__.py
ls utilities/__init__.py
ls features/steps/__init__.py
```

### Issue 6: pytest vs behave Confusion

**Symptoms:**
```bash
$ pytest features/Login.feature
ERROR: file not found: features/Login.feature
```

**Solution:**

**Use correct command for each framework:**
```bash
# Behave for .feature files (Gherkin/BDD)
behave features/Login.feature

# pytest for test_*.py files (unit/integration tests)
pytest tests/test_driver_manager.py
```

### Issue 7: Black/Pylint Configuration Not Applied

**Symptoms:**
- Black formats with wrong line length
- Pylint shows unexpected errors

**Solutions:**

**Verify configuration files exist:**
```bash
# Check pyproject.toml contains [tool.black] and [tool.pylint]
grep -A 5 "\[tool.black\]" pyproject.toml
grep -A 5 "\[tool.pylint" pyproject.toml
```

**Run with explicit config:**
```bash
# Black with explicit line length
black --line-length 100 filename.py

# Pylint with explicit config
pylint --rcfile=pyproject.toml filename.py
```

**VS Code: Reload window after configuration changes:**
- Press `Ctrl+Shift+P` (Cmd+Shift+P on macOS)
- Type "Reload Window"
- Press Enter

### Issue 8: Pre-Commit Hooks Failing

**Symptoms:**
```bash
$ git commit -m "Fix"
black....................................Failed
- hook id: black
- files were modified by this hook
```

**Solution:**

This is expected behavior! Pre-commit hooks auto-fix code formatting.

**Workflow:**
```bash
# 1. Stage your changes
git add filename.py

# 2. Try to commit
git commit -m "Your message"
# Hooks run and may modify files

# 3. Review changes made by hooks
git diff

# 4. Stage the auto-fixed changes
git add filename.py

# 5. Commit again
git commit -m "Your message"
# Now hooks pass and commit succeeds
```

**Bypass hooks (not recommended):**
```bash
git commit --no-verify -m "Commit message"
```

### Issue 9: Port Already in Use (pytest-html server)

**Symptoms:**
```bash
OSError: [Errno 48] Address already in use
```

**Solution:**

**Find and kill process using the port:**

=== "macOS/Linux"
    ```bash
    # Find process on port 8000 (example)
    lsof -i :8000
    
    # Kill process by PID
    kill -9 <PID>
    ```

=== "Windows"
    ```cmd
    # Find process on port 8000
    netstat -ano | findstr :8000
    
    # Kill process by PID
    taskkill /PID <PID> /F
    ```

### Getting Help

If you encounter issues not covered here:

1. **Check existing documentation:**
   - Main [README.md](../../README.md)
   - [Troubleshooting Guide](../troubleshooting/index.md)
   - [API Reference](../api-reference/index.md)

2. **Search GitHub Issues:**
   - [Repository Issues](https://github.com/BalamiRR/Testinium-QA/issues)

3. **Ask for help:**
   - Open a new [GitHub Issue](https://github.com/BalamiRR/Testinium-QA/issues/new)
   - Provide detailed information: OS, Python version, error messages, steps to reproduce

## Next Steps

Now that your development environment is set up:

1. **Read the Contributing Guidelines:**
   - [Contributing Guide](./index.md)
   - [Code Style Guide](./code-style-guide.md)
   - [Testing Guidelines](./testing-guidelines.md)

2. **Explore the Framework:**
   - [Architecture Overview](../architecture/system-overview.md)
   - [Page Object Model Guide](../guides/page-object-model.md)
   - [Step Definitions Guide](../guides/step-definitions.md)

3. **Write Your First Test:**
   - [Feature Files Guide](../guides/feature-files.md)
   - [Authentication Testing Guide](../guides/authentication-testing.md)

4. **Run Tests:**
   - [Getting Started - First Test](../getting-started/first-test.md)
   - [Parallel Execution Guide](../guides/parallel-execution.md)

## Summary

You now have a fully configured development environment with:

- ✓ Python 3.9-3.12 installed
- ✓ Virtual environment created and activated
- ✓ All dependencies installed (production + development)
- ✓ IDE configured (VS Code or PyCharm)
- ✓ Pre-commit hooks set up for code quality
- ✓ Development tools verified
- ✓ WebDriver automatically managed
- ✓ Configuration loaded from .env and config.yaml
- ✓ Test execution verified

Happy testing! 🎉

**Source References:**
- Installation instructions: `README.md:45-136`
- Dependencies: `requirements.txt` and `pyproject.toml`
- Tool configurations: `pyproject.toml:[tool.*]` sections
- WebDriver management: `utilities/driver_manager.py`
- Configuration management: `config/test_config.py`, `config/config.yaml`, `.env.example`

---

*Last updated: 2024-01-15*
