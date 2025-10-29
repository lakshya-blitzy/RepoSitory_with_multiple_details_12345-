# Installation Guide

## Overview

This guide provides comprehensive, platform-specific instructions for installing and configuring the Testinium QA Python test automation framework. Whether you're setting up on Windows, macOS, or Linux, this guide will walk you through every step from Python installation to verifying your setup is working correctly.

**Expected Time to Complete:** 15-30 minutes (depending on your platform and whether Python is already installed)

**What You'll Install:**
- Python 3.9+ runtime environment
- Framework dependencies (Selenium, Behave, pytest, and supporting libraries)
- WebDriver management tools (automated browser driver setup)
- Development environment (optional IDE configuration)

## System Requirements

Before beginning installation, ensure your system meets these minimum requirements:

### Python Version

- **Required:** Python 3.9, 3.10, 3.11, or 3.12
- **Recommended:** Python 3.11 or 3.12 for best compatibility and performance
- **Not Supported:** Python 3.8 or earlier, Python 2.x

**Check your current Python version:**
```bash
# On macOS/Linux
python3 --version

# On Windows
python --version
```

Expected output: `Python 3.9.x`, `Python 3.10.x`, `Python 3.11.x`, or `Python 3.12.x`

### Package Manager

- **pip 20.0+** (included with Python 3.9+)
- **Recommended:** pip 23.0+ for improved dependency resolution

**Check your pip version:**
```bash
# On macOS/Linux
pip3 --version

# On Windows
pip --version
```

Expected output: `pip 20.x` or higher

### Hardware Requirements

| Resource | Minimum | Recommended | Notes |
|----------|---------|-------------|-------|
| **RAM** | 8 GB | 16 GB | 16GB recommended for parallel test execution |
| **Disk Space** | 2 GB free | 5 GB free | 500MB for dependencies, 1GB+ for test artifacts and reports |
| **CPU** | 2 cores | 4+ cores | More cores enable faster parallel execution |
| **Display** | 1024x768 | 1920x1080+ | Required for non-headless browser testing |

### Operating System Support

| Operating System | Versions | Notes |
|-----------------|----------|-------|
| **Windows** | Windows 10, 11 | Both 32-bit and 64-bit supported |
| **macOS** | 10.14 (Mojave) or later | Both Intel and Apple Silicon (M1/M2/M3) |
| **Linux** | Ubuntu 18.04+, Debian 10+, RHEL 8+, Fedora 32+ | Most modern distributions supported |

### Browser Requirements

At least one of the following browsers must be installed:

- **Google Chrome** 90+ or **Chromium** 90+ (recommended)
- **Mozilla Firefox** 88+ (supported)

Browser drivers are managed automatically by `webdriver-manager` - no manual driver installation required!

## Python Installation

### Windows Installation

#### Method 1: Official Python Installer (Recommended)

1. **Download Python:**
   - Visit [python.org/downloads](https://www.python.org/downloads/)
   - Download Python 3.11 or 3.12 installer (Windows 64-bit recommended)

2. **Run the Installer:**
   - **IMPORTANT:** Check "Add Python 3.x to PATH" at the bottom of the installer
   - Check "Install for all users" (optional, requires admin privileges)
   - Click "Install Now" for standard installation
   - Or click "Customize installation" for advanced options

3. **Verify Installation:**
   ```cmd
   python --version
   pip --version
   ```

4. **Configure PATH (if not done by installer):**
   - Open "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path"
   - Click "Edit" → "New"
   - Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\`
   - Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\Scripts\`
   - Click "OK" to save

**Troubleshooting Windows Installation:**
- If `python` command not found, use `py` instead: `py --version`
- If PATH not working, restart Command Prompt or PowerShell
- For permission errors, run installer as Administrator

### macOS Installation

#### Method 1: Using Homebrew (Recommended)

Homebrew is the preferred method for managing Python on macOS.

1. **Install Homebrew (if not installed):**
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python:**
   ```bash
   # Install Python 3.11 (recommended)
   brew install python@3.11
   
   # Link Python to make it available as python3
   brew link python@3.11
   ```

3. **Verify Installation:**
   ```bash
   python3 --version
   pip3 --version
   ```

#### Method 2: Official Python Installer

1. **Download Python:**
   - Visit [python.org/downloads/macos](https://www.python.org/downloads/macos/)
   - Download Python 3.11 or 3.12 macOS installer (Universal or Intel, depending on your Mac)

2. **Run the Installer:**
   - Open the `.pkg` file
   - Follow installation prompts
   - Installer will update PATH automatically

3. **Verify Installation:**
   ```bash
   python3 --version
   pip3 --version
   ```

**Troubleshooting macOS Installation:**
- **macOS ships with Python 2.7:** Always use `python3` and `pip3` commands
- **Command Line Tools:** If errors occur, install Xcode Command Line Tools:
  ```bash
  xcode-select --install
  ```
- **SSL Certificate Errors:** Run the "Install Certificates.command" in `/Applications/Python 3.x/`
- **Apple Silicon (M1/M2/M3):** Use Universal2 or ARM64 installer, not Intel-only

### Linux Installation

#### Ubuntu/Debian

1. **Update Package Index:**
   ```bash
   sudo apt update
   ```

2. **Install Python and Development Packages:**
   ```bash
   # Install Python 3.11 (adjust version as needed)
   sudo apt install -y python3.11 python3.11-dev python3.11-venv python3-pip
   
   # Or use the default Python 3 package
   sudo apt install -y python3 python3-dev python3-venv python3-pip
   ```

3. **Verify Installation:**
   ```bash
   python3 --version
   pip3 --version
   ```

#### RHEL/CentOS/Fedora

1. **Enable Required Repositories (RHEL/CentOS):**
   ```bash
   # RHEL 8/9 or CentOS Stream
   sudo dnf install -y epel-release
   ```

2. **Install Python:**
   ```bash
   # Fedora or RHEL 8+
   sudo dnf install -y python3.11 python3.11-devel python3-pip
   
   # Older RHEL/CentOS
   sudo yum install -y python39 python39-devel python3-pip
   ```

3. **Verify Installation:**
   ```bash
   python3 --version
   pip3 --version
   ```

**Troubleshooting Linux Installation:**
- **python3-dev/python3-devel required:** These packages provide header files needed for some dependencies
- **python3-venv required:** Needed for creating virtual environments
- **Permission errors:** Use `sudo` for system-wide installations, or use virtual environments (recommended)
- **Multiple Python versions:** Use `python3.11` explicitly if you have multiple versions

## Repository Setup

### Method 1: Git Clone (Recommended)

If you have Git installed, this is the preferred method:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/BalamiRR/Testinium-QA.git
   cd Testinium-QA
   ```

2. **Verify Repository Contents:**
   ```bash
   # On macOS/Linux
   ls -la
   
   # On Windows
   dir
   ```

   You should see: `config/`, `features/`, `pages/`, `utilities/`, `requirements.txt`, etc.

3. **Checkout Specific Branch (Optional):**
   ```bash
   # List available branches
   git branch -a
   
   # Checkout a specific branch
   git checkout branch-name
   ```

### Method 2: Manual Download

If you don't have Git or prefer a ZIP download:

1. **Download ZIP Archive:**
   - Visit [github.com/BalamiRR/Testinium-QA](https://github.com/BalamiRR/Testinium-QA)
   - Click the green "Code" button
   - Select "Download ZIP"

2. **Extract the Archive:**
   ```bash
   # On macOS/Linux
   unzip Testinium-QA-main.zip
   cd Testinium-QA-main
   
   # On Windows
   # Right-click ZIP file → "Extract All..." → Choose destination
   cd Testinium-QA-main
   ```

3. **Verify Extraction:**
   - Ensure all directories extracted correctly
   - Check that `requirements.txt` exists in the root directory

**Source:** `README.md:64-75`

## Virtual Environment Setup

Virtual environments isolate your project dependencies from system Python packages, preventing version conflicts and ensuring reproducible installations.

### Why Use Virtual Environments?

- **Isolation:** Project dependencies don't conflict with system packages
- **Reproducibility:** Same environment across development, CI/CD, and production
- **Clean Testing:** Easy to delete and recreate if issues occur
- **Multiple Projects:** Different projects can use different dependency versions

### Creating Virtual Environment

#### On macOS/Linux

```bash
# Navigate to project directory (if not already there)
cd Testinium-QA

# Create virtual environment named 'venv'
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation - your prompt should change to show (venv)
# Example: (venv) user@hostname:~/Testinium-QA$
```

#### On Windows (Command Prompt)

```cmd
# Navigate to project directory
cd Testinium-QA

# Create virtual environment named 'venv'
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation - your prompt should change to show (venv)
# Example: (venv) C:\Users\YourName\Testinium-QA>
```

#### On Windows (PowerShell)

```powershell
# Navigate to project directory
cd Testinium-QA

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# If you get "execution policy" error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then retry activation
```

### Verifying Virtual Environment Activation

When your virtual environment is active:

1. **Prompt Indicator:** Your command prompt will show `(venv)` at the beginning
2. **Python Location:** The `which python` or `where python` command points to the venv directory
3. **pip Location:** The `which pip` or `where pip` command points to the venv directory

```bash
# Verify Python location
which python3  # macOS/Linux
where python   # Windows

# Should show path containing 'venv', like:
# /path/to/Testinium-QA/venv/bin/python3
# C:\path\to\Testinium-QA\venv\Scripts\python.exe
```

### Deactivating Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
# Works on all platforms
deactivate
```

Your prompt will return to normal without the `(venv)` prefix.

**Source:** `README.md:77-95`

## Dependency Installation

With your virtual environment activated, install the framework dependencies.

### Standard Installation (pip + requirements.txt)

This is the primary installation method:

```bash
# Ensure virtual environment is activated (you should see "(venv)" in prompt)
# If not activated, activate it first:
# source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate     # Windows

# Upgrade pip to latest version (recommended)
pip install --upgrade pip

# Install all framework dependencies
pip install -r requirements.txt

# Installation typically takes 2-5 minutes depending on internet speed
```

Expected output:
```
Collecting selenium>=4.15.0 (from -r requirements.txt (line 1))
  Downloading selenium-4.15.2-py3-none-any.whl (...)
Collecting behave>=1.2.6 (from -r requirements.txt (line 2))
  Downloading behave-1.2.6-py3-none-any.whl (...)
...
Successfully installed selenium-4.15.2 behave-1.2.6 pytest-7.4.3 ...
```

### Alternative: Poetry Installation

If the project includes `pyproject.toml` and you prefer Poetry:

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Activate Poetry virtual environment
poetry shell
```

### Key Dependencies Installed

After installation completes, these critical packages will be available:

| Package | Version | Purpose |
|---------|---------|---------|
| **selenium** | 4.15.2+ | WebDriver automation for browser control |
| **behave** | 1.2.6+ | BDD framework for Gherkin feature files and step definitions |
| **pytest** | 7.4.3+ | Testing framework with advanced reporting |
| **webdriver-manager** | 4.0.1+ | Automatic browser driver download and management |
| **python-dotenv** | 1.0.0+ | Environment variable management from `.env` files |
| **PyYAML** | 6.0.1+ | YAML configuration file parsing |
| **allure-behave** | 2.13.2+ | Allure report generation for Behave tests |
| **behave-html-formatter** | 0.9.10+ | HTML report generation |
| **Faker** | 20.0.0+ | Test data generation for realistic test scenarios |

### Verifying Installation

Confirm all dependencies installed correctly:

```bash
# List all installed packages
pip list

# Check specific package versions
pip show selenium
pip show behave
pip show pytest

# Verify Behave CLI is available
behave --version

# Verify pytest CLI is available
pytest --version
```

### Troubleshooting Dependency Installation

#### Issue: SSL Certificate Errors

```bash
# Error: Could not fetch URL https://pypi.org/simple/selenium/: There was a problem confirming the ssl certificate

# Solution 1: Update certifi package
pip install --upgrade certifi

# Solution 2: Use --trusted-host (NOT recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Solution 3 (macOS): Install certificates
/Applications/Python\ 3.11/Install\ Certificates.command
```

#### Issue: Dependency Conflicts

```bash
# Error: ERROR: pip's dependency resolver does not currently take into account all the packages that are installed

# Solution 1: Upgrade pip
pip install --upgrade pip

# Solution 2: Clear pip cache
pip cache purge
pip install -r requirements.txt

# Solution 3: Use clean virtual environment
deactivate
rm -rf venv/  # or rmdir /s venv on Windows
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Issue: Permission Errors

```bash
# Error: Could not install packages due to an PermissionError

# Solution: NEVER use sudo with pip in virtual environment
# Ensure virtual environment is activated (check for "(venv)" in prompt)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then retry installation
pip install -r requirements.txt
```

#### Issue: Compilation Errors (C extensions)

```bash
# Error: error: Microsoft Visual C++ 14.0 or greater is required (Windows)
# or: error: command 'gcc' failed (Linux)

# Solution Windows: Install Microsoft C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Solution Linux: Install development packages
sudo apt install -y python3-dev build-essential  # Ubuntu/Debian
sudo dnf install -y python3-devel gcc gcc-c++    # RHEL/Fedora
```

**Source:** `README.md:98-106, 716-738`

## WebDriver Setup

The Testinium QA framework uses `webdriver-manager` for automatic browser driver management. **No manual driver installation is required!**

### Automatic Driver Management (Recommended)

The framework automatically downloads and manages browser drivers:

```python
# This happens automatically in utilities/driver_manager.py
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# ChromeDriver is downloaded automatically on first use
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```

**Benefits:**
- ✅ Drivers download automatically on first test run
- ✅ Compatible driver versions selected based on installed browser
- ✅ Cached locally after first download (fast subsequent runs)
- ✅ Cross-platform support (Windows, macOS, Linux)
- ✅ No PATH configuration needed

### First Run Driver Download

On your first test execution, you'll see driver download messages:

```
[WDM] - Downloading: 100%|████████████████████████| 6.84M/6.84M [00:02<00:00, 3.12MB/s]
[WDM] - Validating drivers
[WDM] - Driver [/Users/.../.wdm/drivers/chromedriver/mac64/119.0.6045.105/chromedriver] found in cache
```

This is normal and only happens once per driver version.

### Manual Driver Installation (Fallback)

If automatic driver management fails, you can install drivers manually:

#### Manual ChromeDriver Installation

1. **Check Chrome Version:**
   - Open Chrome → Help → About Google Chrome
   - Note the version number (e.g., 119.0.6045.105)

2. **Download Matching ChromeDriver:**
   - Visit [chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
   - Download the version matching your Chrome browser
   - Choose the correct platform (mac64, linux64, win32, win64)

3. **Install ChromeDriver:**
   ```bash
   # macOS/Linux
   unzip chromedriver_linux64.zip
   sudo mv chromedriver /usr/local/bin/
   sudo chmod +x /usr/local/bin/chromedriver
   
   # Windows
   # Extract chromedriver.exe
   # Move to C:\Windows\System32\ or add directory to PATH
   ```

4. **Verify Installation:**
   ```bash
   # macOS/Linux
   chromedriver --version
   
   # Windows
   chromedriver.exe --version
   ```

#### Manual GeckoDriver Installation (Firefox)

1. **Check Firefox Version:**
   - Open Firefox → Help → About Firefox
   - Note the version number

2. **Download GeckoDriver:**
   - Visit [github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)
   - Download the latest release for your platform

3. **Install GeckoDriver:**
   ```bash
   # macOS/Linux
   tar -xvzf geckodriver-v0.33.0-linux64.tar.gz
   sudo mv geckodriver /usr/local/bin/
   sudo chmod +x /usr/local/bin/geckodriver
   
   # Windows
   # Extract geckodriver.exe
   # Move to C:\Windows\System32\ or add to PATH
   ```

4. **Verify Installation:**
   ```bash
   geckodriver --version
   ```

### PATH Configuration for Manual Drivers

If using manual drivers, ensure they're in your system PATH:

#### macOS/Linux PATH Configuration

```bash
# Check current PATH
echo $PATH

# Add to PATH temporarily (current session only)
export PATH=$PATH:/path/to/driver/directory

# Add to PATH permanently
# Edit ~/.bashrc, ~/.zshrc, or ~/.bash_profile
echo 'export PATH=$PATH:/path/to/driver/directory' >> ~/.bashrc
source ~/.bashrc
```

#### Windows PATH Configuration

1. Open "Edit the system environment variables"
2. Click "Environment Variables"
3. Under "User variables" or "System variables", select "Path"
4. Click "Edit" → "New"
5. Add the directory containing `chromedriver.exe` or `geckodriver.exe`
6. Click "OK" to save
7. Restart Command Prompt

### Verifying WebDriver Setup

Test that WebDriver can launch a browser:

```bash
# With virtual environment activated
python3

# In Python interactive shell:
>>> from selenium import webdriver
>>> driver = webdriver.Chrome()  # Should open Chrome browser
>>> driver.get("https://www.google.com")
>>> driver.quit()
>>> exit()
```

If a browser window opens and navigates to Google, your WebDriver setup is working correctly!

**Source:** `README.md:56-61, 615-622, 642-649`

## IDE Setup

While not required, using an IDE enhances your development experience with features like code completion, debugging, and integrated testing.

### PyCharm (Recommended)

PyCharm provides excellent Python and Behave support out of the box.

#### PyCharm Installation

1. **Download PyCharm:**
   - **Community Edition (Free):** [jetbrains.com/pycharm/download](https://www.jetbrains.com/pycharm/download/)
   - **Professional Edition (Paid, 30-day trial):** Includes additional features like database tools

2. **Install PyCharm:**
   - Run the installer and follow prompts
   - On first launch, configure color scheme and keymap preferences

#### PyCharm Project Configuration

1. **Open Project:**
   - File → Open → Select `Testinium-QA` directory

2. **Configure Python Interpreter:**
   - File → Settings (or PyCharm → Preferences on macOS)
   - Project: Testinium-QA → Python Interpreter
   - Click gear icon → Add → Existing environment
   - Select: `Testinium-QA/venv/bin/python` (macOS/Linux) or `Testinium-QA\venv\Scripts\python.exe` (Windows)
   - Click "OK"

3. **Install Gherkin Plugin:**
   - File → Settings → Plugins
   - Search for "Gherkin"
   - Install "Gherkin" plugin by JetBrains
   - Restart PyCharm

4. **Configure Behave Support:**
   - Settings → Languages & Frameworks → BDD
   - Check "Enable Behave support"
   - Set "Step definitions" directory: `features/steps`

5. **Enable Code Completion:**
   - Settings → Editor → General → Code Completion
   - Enable "Show suggestions as you type"
   - Enable "Match case"

#### PyCharm Run Configurations

Create run configurations for easy test execution:

1. **Add Behave Configuration:**
   - Run → Edit Configurations → + → Python
   - Name: "Run All Tests"
   - Script path: `/path/to/venv/bin/behave` (or `venv\Scripts\behave.exe` on Windows)
   - Working directory: `/path/to/Testinium-QA`
   - Click "OK"

2. **Add Configuration for Tagged Tests:**
   - Duplicate previous configuration
   - Name: "Run Login Tests"
   - Add to Parameters: `--tags=@Login`

### Visual Studio Code

VS Code is a lightweight, highly customizable editor with excellent Python support.

#### VS Code Installation

1. **Download VS Code:**
   - Visit [code.visualstudio.com](https://code.visualstudio.com/)
   - Download for your platform and install

2. **Install Python Extension:**
   - Open VS Code
   - Click Extensions icon (or press Ctrl+Shift+X / Cmd+Shift+X)
   - Search for "Python" by Microsoft
   - Click "Install"

#### VS Code Recommended Extensions

Install these extensions for optimal experience:

| Extension | Publisher | Purpose |
|-----------|-----------|---------|
| **Python** | Microsoft | Python language support, IntelliSense, debugging |
| **Cucumber (Gherkin)** | Alexander Krechik | Gherkin syntax highlighting for .feature files |
| **Pylance** | Microsoft | Fast Python language server (auto-installed with Python extension) |
| **autoDocstring** | Nils Werner | Generate docstrings automatically |
| **GitLens** | GitKraken | Enhanced Git integration |
| **YAML** | Red Hat | YAML language support for config.yaml |

#### VS Code Python Configuration

1. **Select Python Interpreter:**
   - Press Cmd+Shift+P (macOS) or Ctrl+Shift+P (Windows/Linux)
   - Type "Python: Select Interpreter"
   - Choose: `./venv/bin/python` or `.\venv\Scripts\python.exe`

2. **Configure Settings (Optional):**
   - File → Preferences → Settings
   - Search for "python.linting.enabled" → Enable
   - Search for "python.formatting.provider" → Select "black"
   - Search for "python.linting.pylintEnabled" → Enable

3. **Create .vscode/settings.json (Optional):**
   ```json
   {
     "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
     "python.linting.enabled": true,
     "python.linting.pylintEnabled": true,
     "python.formatting.provider": "black",
     "editor.formatOnSave": true,
     "python.testing.pytestEnabled": true,
     "files.exclude": {
       "**/__pycache__": true,
       "**/*.pyc": true
     }
   }
   ```

#### Running Tests from VS Code

1. **Using Integrated Terminal:**
   - View → Terminal (or Ctrl+` / Cmd+`)
   - Ensure virtual environment is activated
   - Run: `behave` or `behave --tags=@Login`

2. **Using Tasks (Optional):**
   - Create `.vscode/tasks.json`:
   ```json
   {
     "version": "2.0.0",
     "tasks": [
       {
         "label": "Run All Tests",
         "type": "shell",
         "command": "${workspaceFolder}/venv/bin/behave",
         "group": "test",
         "presentation": {
           "reveal": "always",
           "panel": "new"
         }
       }
     ]
   }
   ```
   - Run task: Terminal → Run Task → Run All Tests

### Other IDEs and Editors

The framework works with any Python-compatible editor:

#### Sublime Text

1. Install Sublime Text from [sublimetext.com](https://www.sublimetext.com/)
2. Install Package Control
3. Install packages: "Anaconda", "Gherkin (Cucumber) Formatter"
4. Configure Python build system pointing to venv/bin/python

#### Vim/Neovim

1. Install vim-python and vim-behave plugins
2. Configure Python path in .vimrc to use venv
3. Use :terminal to run tests

#### Emacs

1. Install python-mode and feature-mode
2. Configure python-shell-interpreter to venv/bin/python
3. Use M-x shell to run tests

**Source:** `README.md:50-57`

## Verification

After completing installation, verify everything is set up correctly.

### Step 1: Verify Python and Pip

```bash
# Check Python version
python3 --version  # macOS/Linux
python --version   # Windows

# Expected: Python 3.9.x or later

# Check pip version
pip3 --version  # macOS/Linux
pip --version   # Windows

# Expected: pip 20.0 or later
```

### Step 2: Verify Virtual Environment

```bash
# Ensure virtual environment is activated
# Your prompt should show (venv)

# Check Python location points to venv
which python3  # macOS/Linux
where python   # Windows

# Expected: path should contain 'venv' directory
# Example: /path/to/Testinium-QA/venv/bin/python3
```

### Step 3: Verify Package Installation

```bash
# List all installed packages
pip list

# Verify key packages are installed
pip show selenium
pip show behave
pip show pytest
pip show webdriver-manager

# All should return package information
```

### Step 4: Verify Behave CLI

```bash
# Check Behave is available
behave --version

# Expected output:
# behave 1.2.6
```

### Step 5: Verify pytest CLI

```bash
# Check pytest is available
pytest --version

# Expected output:
# pytest 7.4.3
```

### Step 6: Run Framework Version Check

```bash
# Display framework information
python3 -c "import sys; print(f'Python: {sys.version}')"
python3 -c "import selenium; print(f'Selenium: {selenium.__version__}')"
python3 -c "import behave; print(f'Behave: {behave.__version__}')"
```

### Step 7: Test Driver Initialization

Create a simple test to verify WebDriver works:

```bash
# Create a temporary test file
cat > test_driver.py << 'EOF'
from utilities.driver_manager import DriverManager

try:
    driver = DriverManager.get_driver()
    print("✓ WebDriver initialized successfully")
    driver.get("https://www.google.com")
    print("✓ Browser navigation works")
    print(f"✓ Page title: {driver.title}")
    DriverManager.quit_driver()
    print("✓ Driver cleanup successful")
    print("\n✅ All verification checks passed!")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your installation and configuration.")
EOF

# Run the test
python3 test_driver.py

# Clean up
rm test_driver.py
```

Expected output:
```
✓ WebDriver initialized successfully
✓ Browser navigation works
✓ Page title: Google
✓ Driver cleanup successful

✅ All verification checks passed!
```

### Step 8: Run Sample Feature (Optional)

If you want to verify the complete test execution flow:

```bash
# Run a single feature file
behave features/Login.feature --dry-run

# This performs a "dry run" (doesn't execute, just validates syntax)
# Expected: No errors, scenario steps should be listed
```

**Source:** `README.md:100-106`

## Troubleshooting

### Installation Issues

#### Problem: Python Version Mismatch

**Symptoms:**
```bash
$ python3 --version
Python 3.8.10
# Or: command not found: python3
```

**Cause:** Wrong Python version installed or not in PATH

**Solutions:**

1. **Install correct Python version:**
   ```bash
   # macOS with Homebrew
   brew install python@3.11
   
   # Ubuntu/Debian
   sudo apt install python3.11
   
   # Windows: Download from python.org
   ```

2. **Use version-specific command:**
   ```bash
   python3.11 --version  # Instead of python3
   python3.11 -m venv venv
   ```

3. **Fix PATH on Windows:**
   - Reinstall Python with "Add to PATH" checked
   - Or manually add to PATH as described in Windows Installation section

#### Problem: pip Installation Failures

**Symptoms:**
```bash
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied
```

**Solutions:**

1. **Ensure virtual environment is activated:**
   ```bash
   # Check for (venv) in your prompt
   # If not present, activate:
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. **Never use sudo with virtual environment:**
   ```bash
   # ❌ WRONG
   sudo pip install -r requirements.txt
   
   # ✅ CORRECT
   pip install -r requirements.txt  # with venv activated
   ```

3. **Upgrade pip if outdated:**
   ```bash
   pip install --upgrade pip
   ```

#### Problem: Virtual Environment Activation Issues

**Symptoms (Windows PowerShell):**
```
venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system
```

**Solution:**
```powershell
# Allow script execution for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Retry activation
venv\Scripts\Activate.ps1
```

**Symptoms (macOS/Linux):**
```
bash: venv/bin/activate: No such file or directory
```

**Solution:**
```bash
# Virtual environment wasn't created properly
# Recreate it:
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### Dependency Issues

#### Problem: Dependency Conflicts During Installation

**Symptoms:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages installed.
This behavior is the source of the following dependency conflicts.
```

**Solutions:**

1. **Upgrade pip:**
   ```bash
   pip install --upgrade pip setuptools wheel
   ```

2. **Use clean virtual environment:**
   ```bash
   deactivate
   rm -rf venv/  # or rmdir /s venv on Windows
   python3 -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Clear pip cache:**
   ```bash
   pip cache purge
   pip install -r requirements.txt
   ```

#### Problem: SSL Certificate Verification Failed

**Symptoms:**
```
Could not fetch URL https://pypi.org/simple/selenium/: There was a problem confirming the ssl certificate
```

**Solutions:**

1. **macOS - Install certificates:**
   ```bash
   /Applications/Python\ 3.11/Install\ Certificates.command
   ```

2. **Update certifi:**
   ```bash
   pip install --upgrade certifi
   ```

3. **Temporary workaround (not recommended for production):**
   ```bash
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
   ```

### Platform-Specific Issues

#### Windows: "python not recognized" Error

**Symptoms:**
```cmd
'python' is not recognized as an internal or external command
```

**Solutions:**

1. **Use py launcher:**
   ```cmd
   py --version
   py -m pip install -r requirements.txt
   ```

2. **Add Python to PATH:**
   - Search Windows for "Edit the system environment variables"
   - Environment Variables → Path → Edit
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts\`
   - Restart Command Prompt

3. **Reinstall Python with PATH option:**
   - Uninstall current Python
   - Download installer from python.org
   - **Check "Add Python to PATH"** during installation

#### macOS: Multiple Python Versions Conflict

**Symptoms:**
```bash
$ python --version
Python 2.7.18

$ python3 --version
Python 3.9.6
```

**Solutions:**

1. **Always use python3:**
   ```bash
   python3 --version
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Create alias (optional):**
   ```bash
   # Add to ~/.zshrc or ~/.bashrc
   alias python=python3
   alias pip=pip3
   
   # Reload shell config
   source ~/.zshrc
   ```

3. **Use Homebrew Python exclusively:**
   ```bash
   brew install python@3.11
   brew link python@3.11
   ```

#### Linux: Missing Development Headers

**Symptoms:**
```
error: command 'gcc' failed: No such file or directory
fatal error: Python.h: No such file or directory
```

**Solutions:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3-dev python3-venv build-essential

# RHEL/Fedora/CentOS
sudo dnf install -y python3-devel gcc gcc-c++ make

# After installing, retry pip install
pip install -r requirements.txt
```

### WebDriver Issues

#### Problem: WebDriver Not Found

**Symptoms:**
```
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```

**Solutions:**

1. **Verify webdriver-manager is installed:**
   ```bash
   pip show webdriver-manager
   # If not found:
   pip install webdriver-manager
   ```

2. **Clear webdriver-manager cache:**
   ```bash
   # Remove cached drivers
   rm -rf ~/.wdm/  # macOS/Linux
   rmdir /s %USERPROFILE%\.wdm\  # Windows
   
   # Retry test execution
   ```

3. **Install driver manually (fallback):**
   - Follow "Manual Driver Installation" section above

#### Problem: Browser Version Mismatch

**Symptoms:**
```
SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 119
```

**Solutions:**

1. **Update browser:**
   - Chrome: Help → About Google Chrome (auto-updates)
   - Firefox: Help → About Firefox (auto-updates)

2. **Clear driver cache:**
   ```bash
   rm -rf ~/.wdm/
   # Next test run will download compatible driver
   ```

3. **Specify driver version explicitly (if needed):**
   ```python
   # In utilities/driver_manager.py, specify version:
   from webdriver_manager.chrome import ChromeDriverManager
   ChromeDriverManager(version="119.0.6045.105").install()
   ```

### IDE Issues

#### Problem: PyCharm Can't Find Modules

**Symptoms:** Import statements underlined in red, "Module not found" warnings

**Solutions:**

1. **Configure correct interpreter:**
   - File → Settings → Project → Python Interpreter
   - Select venv/bin/python (not system Python)

2. **Mark directories as sources:**
   - Right-click project root → Mark Directory as → Sources Root

3. **Invalidate caches:**
   - File → Invalidate Caches → Invalidate and Restart

#### Problem: VS Code Linting Errors Despite Working Code

**Symptoms:** Red squiggles on imports, but tests run successfully

**Solutions:**

1. **Select correct interpreter:**
   - Ctrl+Shift+P → "Python: Select Interpreter"
   - Choose: `./venv/bin/python`

2. **Reload window:**
   - Ctrl+Shift+P → "Developer: Reload Window"

3. **Install pylint in venv:**
   ```bash
   pip install pylint
   ```

## Next Steps

Congratulations! Your Testinium QA Python framework installation is complete. 

### Immediate Next Steps

1. **Configure the Framework:**
   - Continue to [Configuration Guide](configuration.md) to set up environment variables and test settings
   - Create your `.env` file with credentials
   - Customize `config/config.yaml` for your environment

2. **Run Your First Test:**
   - Proceed to [First Test Guide](first-test.md) to execute a sample test
   - Learn how to run tests with different tags and parameters
   - Understand test reporting and results

3. **Explore the Framework:**
   - Review [Project Structure](../architecture/system-overview.md) to understand the codebase organization
   - Read [Page Object Model Guide](../guides/page-object-model.md) to learn the framework's design pattern
   - Check [API Reference](../api-reference/index.md) for detailed documentation

### Learning Resources

- **BDD with Behave:** [behave.readthedocs.io](https://behave.readthedocs.io/)
- **Selenium Documentation:** [selenium.dev/documentation](https://selenium.dev/documentation/)
- **Python Testing:** [docs.pytest.org](https://docs.pytest.org/)

### Getting Help

If you encounter issues not covered in this guide:

1. **Check Troubleshooting Documentation:**
   - [Common Errors](../troubleshooting/common-errors.md)
   - [WebDriver Issues](../troubleshooting/webdriver-issues.md)
   - [Configuration Issues](../troubleshooting/configuration-issues.md)

2. **Review Existing Documentation:**
   - Check README.md in project root
   - Review inline code comments
   - Consult API reference documentation

3. **Community Support:**
   - Open an issue on GitHub repository
   - Check existing issues for similar problems
   - Consult project maintainers

**Source:** `README.md:45-108, 602-715`

---

**Installation Guide Version:** 1.0.0  
**Last Updated:** 2024  
**Framework Version:** Python 3.9+ / Selenium 4.x / Behave 1.2.6+
