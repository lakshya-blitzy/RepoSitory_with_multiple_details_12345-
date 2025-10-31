# Installation Issues

This guide provides comprehensive troubleshooting solutions for common installation problems encountered when setting up the Testinium QA Python test automation framework.

**Source:** `README.md:45-136`, `requirements.txt`, `pyproject.toml`

## Overview

Installation issues can range from Python version mismatches to dependency conflicts and platform-specific problems. This guide covers all common scenarios with step-by-step solutions for Windows, macOS, and Linux platforms.

## Prerequisites

Before troubleshooting, ensure you have:
- Internet connection for downloading packages
- Administrator/sudo privileges (for system-level installations)
- Basic command-line familiarity
- Text editor for configuration files

---

## Python Version Issues

### Issue 1: Wrong Python Version Installed

**Symptoms:**
```bash
python --version
# Python 2.7.18 or Python 3.7.x (unsupported versions)
```

**Cause:** The framework requires Python 3.9 or higher (3.9-3.12 supported). Older versions lack required features.

**Solution:**

**On Windows:**
```bash
# Download Python 3.12 from python.org
# Run installer with "Add Python to PATH" checked
# Verify installation:
python --version
# Expected: Python 3.12.x

# If multiple versions exist, use py launcher:
py -3.12 --version
```

**On macOS:**
```bash
# Using Homebrew (recommended):
brew install python@3.12

# Verify installation:
python3 --version
# Expected: Python 3.12.x

# Add to PATH if needed (add to ~/.zshrc or ~/.bash_profile):
export PATH="/usr/local/opt/python@3.12/bin:$PATH"
source ~/.zshrc  # or source ~/.bash_profile
```

**On Linux (Ubuntu/Debian):**
```bash
# Add deadsnakes PPA for latest Python versions:
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.12:
sudo apt install python3.12 python3.12-venv python3.12-dev

# Verify installation:
python3.12 --version
# Expected: Python 3.12.x
```

**On Linux (RHEL/CentOS/Fedora):**
```bash
# Install Python 3.12:
sudo dnf install python3.12 python3.12-devel

# Verify installation:
python3.12 --version
```

---

### Issue 2: Multiple Python Installations Conflicting

**Symptoms:**
```bash
python --version
# Python 2.7.18
python3 --version
# Python 3.12.0
# But pip install installs to wrong version
```

**Cause:** System has multiple Python versions, and commands point to different installations.

**Solution:**

**Diagnostic Steps:**
```bash
# Check which Python is being used:
which python
which python3
which pip
which pip3

# Check all installed Python versions:
ls -la /usr/bin/python*  # Linux/macOS
where python             # Windows
```

**Use Python Module Execution:**
```bash
# Always use this pattern to ensure correct pip:
python3.12 -m pip install <package>

# Instead of:
pip install <package>  # May install to wrong Python version
```

**Create Alias (Linux/macOS):**
```bash
# Add to ~/.bashrc or ~/.zshrc:
alias python=python3.12
alias pip=python3.12 -m pip

# Reload configuration:
source ~/.bashrc  # or source ~/.zshrc
```

---

### Issue 3: Python Not in PATH

**Symptoms:**
```bash
python --version
# 'python' is not recognized as an internal or external command (Windows)
# command not found: python (macOS/Linux)
```

**Cause:** Python installation directory not added to system PATH.

**Solution:**

**On Windows:**
```bash
# Option 1: Reinstall Python with "Add Python to PATH" checked

# Option 2: Manually add to PATH:
# 1. Search "Environment Variables" in Start Menu
# 2. Click "Environment Variables" button
# 3. Under "System variables", find "Path" and click "Edit"
# 4. Click "New" and add:
#    C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python312\
#    C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python312\Scripts\
# 5. Click OK on all dialogs
# 6. Restart Command Prompt

# Verify:
python --version
```

**On macOS/Linux:**
```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.bash_profile:
export PATH="/usr/local/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"

# For Homebrew Python on macOS:
export PATH="/usr/local/opt/python@3.12/bin:$PATH"

# Reload configuration:
source ~/.bashrc  # or ~/.zshrc or ~/.bash_profile

# Verify:
python3 --version
```

---

### Issue 4: Python Version Verification Commands

**Diagnostic Commands:**
```bash
# Check Python version:
python --version
python3 --version
python3.12 --version

# Check pip version and associated Python:
pip --version
pip3 --version
python3.12 -m pip --version

# Check installed packages location:
python3.12 -m site

# Check all Python executables:
# Linux/macOS:
which -a python python3 python3.12
# Windows:
where python

# Verify Python can import key modules:
python3.12 -c "import sys; print(sys.version)"
python3.12 -c "import ssl; print(ssl.OPENSSL_VERSION)"
```

---

## Dependency Conflicts

### Issue 5: Package Version Mismatches

**Symptoms:**
```bash
pip install -r requirements.txt
# ERROR: Could not find a version that satisfies the requirement selenium==4.15.2
# ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/
```

**Cause:** Conflicting version requirements between packages or outdated pip.

**Solution:**

**Step 1: Upgrade pip, setuptools, and wheel:**
```bash
python3.12 -m pip install --upgrade pip setuptools wheel

# Verify pip version (should be 23.0+):
pip --version
```

**Step 2: Install dependencies with verbose output:**
```bash
pip install -r requirements.txt --verbose

# See which package causes conflict
```

**Step 3: Install dependencies one by one:**
```bash
# If requirements.txt fails, install core dependencies first:
pip install selenium==4.15.2
pip install behave==1.2.6
pip install pytest==7.4.3
pip install webdriver-manager==4.0.1

# Then install remaining dependencies:
pip install -r requirements.txt
```

**Step 4: Use pip constraint file if version conflicts persist:**
```bash
# Create constraints.txt:
pip freeze > constraints.txt

# Install with constraints:
pip install -r requirements.txt -c constraints.txt
```

---

### Issue 6: Conflicting Dependencies

**Symptoms:**
```bash
pip check
# selenium 4.15.2 requires urllib3[socks]<3,>=1.26, but you have urllib3 2.1.0.
# ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**Cause:** Dependencies have incompatible sub-dependencies.

**Solution:**

**Resolution Strategy 1: Use pip with backtracking:**
```bash
# Uninstall conflicting packages:
pip uninstall urllib3 -y

# Reinstall from requirements.txt:
pip install -r requirements.txt

# Verify resolution:
pip check
# Expected: No broken requirements found.
```

**Resolution Strategy 2: Use Poetry for dependency management:**
```bash
# Install Poetry:
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies using Poetry:
poetry install

# This uses pyproject.toml and resolves conflicts automatically
```

**Resolution Strategy 3: Pin compatible versions:**
```bash
# If conflicts persist, create requirements-resolved.txt:
pip install pip-tools

# Use pip-compile to resolve dependencies:
pip-compile requirements.txt -o requirements-resolved.txt

# Install from resolved file:
pip install -r requirements-resolved.txt
```

---

### Issue 7: SSL Certificate Errors During Installation

**Symptoms:**
```bash
pip install selenium
# WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None))
# Could not fetch URL https://pypi.org/simple/selenium/: There was a problem confirming the ssl certificate
# ERROR: Could not find a version that satisfies the requirement selenium
```

**Cause:** Corporate firewall, proxy, or outdated SSL certificates.

**Solution:**

**Temporary Workaround (NOT RECOMMENDED for production):**
```bash
# Install with --trusted-host flags:
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org selenium
```

**Proper Solution - Update SSL Certificates:**
```bash
# On macOS:
# Run Python's Install Certificates command:
/Applications/Python\ 3.12/Install\ Certificates.command

# Or install certifi and update:
pip install --upgrade certifi

# On Linux:
sudo apt update
sudo apt install --reinstall ca-certificates

# On Windows:
# Update Windows certificates via Windows Update
# Or install certifi:
pip install --upgrade certifi
```

**Proper Solution - Configure Corporate Proxy:**
```bash
# Set proxy environment variables:
# Linux/macOS:
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"

# Windows Command Prompt:
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080

# Windows PowerShell:
$env:HTTP_PROXY="http://proxy.company.com:8080"
$env:HTTPS_PROXY="http://proxy.company.com:8080"

# Then install:
pip install -r requirements.txt
```

---

## Virtual Environment Problems

### Issue 8: Virtual Environment Creation Fails

**Symptoms:**
```bash
python3 -m venv venv
# Error: No module named venv
# Or: The virtual environment was not created successfully
```

**Cause:** Python venv module not installed or corrupted Python installation.

**Solution:**

**On Linux (Ubuntu/Debian):**
```bash
# Install python3-venv package:
sudo apt update
sudo apt install python3.12-venv

# Retry virtual environment creation:
python3.12 -m venv venv
```

**On Linux (RHEL/CentOS/Fedora):**
```bash
# Install python3-venv:
sudo dnf install python3.12-devel

# Retry:
python3.12 -m venv venv
```

**On macOS:**
```bash
# Reinstall Python with Homebrew:
brew reinstall python@3.12

# Retry:
python3.12 -m venv venv
```

**On Windows:**
```bash
# Repair Python installation:
# Go to "Add or Remove Programs"
# Find Python 3.12
# Click "Modify" > "Repair"

# Or reinstall Python
```

**Alternative - Use virtualenv:**
```bash
# Install virtualenv:
pip install virtualenv

# Create virtual environment:
virtualenv venv

# Or specify Python version:
virtualenv -p python3.12 venv
```

---

### Issue 9: Virtual Environment Activation Issues

**Symptoms:**
```bash
# On Windows:
venv\Scripts\activate
# 'activate' is not recognized as an internal or external command

# On Linux/macOS:
source venv/bin/activate
# bash: venv/bin/activate: No such file or directory
```

**Cause:** Virtual environment not created successfully or wrong activation command.

**Solution:**

**Verify Virtual Environment Exists:**
```bash
# Check if venv directory exists:
# Linux/macOS:
ls -la venv/
ls venv/bin/

# Windows:
dir venv\
dir venv\Scripts\
```

**Correct Activation Commands:**

**Windows Command Prompt:**
```bash
venv\Scripts\activate.bat
```

**Windows PowerShell:**
```bash
venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then retry activation
```

**Linux/macOS (bash/zsh):**
```bash
source venv/bin/activate

# Verify activation:
which python
# Should show: /path/to/project/venv/bin/python

# Check prompt changed:
(venv) user@machine:~/project$
```

**Windows PowerShell Execution Policy Error:**
```bash
# Symptom:
venv\Scripts\Activate.ps1
# cannot be loaded because running scripts is disabled on this system

# Solution:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verify:
Get-ExecutionPolicy
# Should show: RemoteSigned

# Retry activation:
venv\Scripts\Activate.ps1
```

---

### Issue 10: venv vs virtualenv Differences

**Symptoms:**
```bash
# Confusion about which tool to use
# Different behavior between venv and virtualenv
```

**Explanation:**

| Feature | venv | virtualenv |
|---------|------|------------|
| Built-in | Yes (Python 3.3+) | No (requires installation) |
| Speed | Faster | Slower |
| Python Version | Same as system Python | Can use different Python versions |
| Installation | N/A | `pip install virtualenv` |
| Command | `python -m venv venv` | `virtualenv venv` |

**Recommendation:**
```bash
# Use venv for simplicity (built-in):
python3.12 -m venv venv

# Use virtualenv only if you need:
# - Different Python version than system
# - Advanced features (--system-site-packages, etc.)
virtualenv -p python3.12 venv
```

---

### Issue 11: Permission Errors During Virtual Environment Creation

**Symptoms:**
```bash
python3 -m venv venv
# Permission denied: '/path/to/venv'
# [Errno 13] Permission denied
```

**Cause:** Insufficient permissions in directory or disk.

**Solution:**

**On Linux/macOS:**
```bash
# Check directory permissions:
ls -ld .

# If you don't own the directory:
sudo chown -R $USER:$USER /path/to/project

# Retry virtual environment creation:
python3.12 -m venv venv

# Alternative - create in user directory:
cd ~
mkdir -p projects/testinium-qa
cd projects/testinium-qa
python3.12 -m venv venv
```

**On Windows:**
```bash
# Run Command Prompt or PowerShell as Administrator
# Right-click > "Run as administrator"

# Or change folder permissions:
# Right-click folder > Properties > Security > Edit > Add Full Control
```

---

## pip Installation Failures

### Issue 12: pip Upgrade Needed

**Symptoms:**
```bash
pip install selenium
# WARNING: You are using pip version 19.2.3; however, version 23.3.1 is available.
# ERROR: Could not find a version that satisfies the requirement selenium==4.15.2
```

**Cause:** Outdated pip version lacks newer package resolution features.

**Solution:**
```bash
# Upgrade pip to latest version:
python3.12 -m pip install --upgrade pip

# Verify pip version:
pip --version
# Expected: pip 23.3.1 or higher

# Retry package installation:
pip install -r requirements.txt
```

---

### Issue 13: pip Cache Corruption

**Symptoms:**
```bash
pip install selenium
# ERROR: Could not install packages due to an OSError: [Errno 28] No space left on device
# Or: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE
```

**Cause:** Corrupted pip cache or insufficient disk space.

**Solution:**

**Clear pip cache:**
```bash
# View cache location:
pip cache dir

# Clear all cache:
pip cache purge

# Retry installation:
pip install -r requirements.txt

# Or install without cache:
pip install --no-cache-dir -r requirements.txt
```

**Check disk space:**
```bash
# Linux/macOS:
df -h .

# Windows:
dir

# If low disk space, free up space or change pip cache location:
export PIP_NO_CACHE_DIR=1  # Disable cache temporarily
pip install -r requirements.txt
```

---

### Issue 14: Network Issues and Timeouts

**Symptoms:**
```bash
pip install selenium
# WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None))
# ERROR: Could not install packages due to an OSError: HTTPSConnectionPool: Read timed out.
```

**Cause:** Slow network, firewall, or PyPI server issues.

**Solution:**

**Increase timeout:**
```bash
# Install with increased timeout (default: 15 seconds):
pip install --timeout=120 -r requirements.txt
```

**Use alternative PyPI mirror:**
```bash
# China PyPI mirror (if in China):
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# Use pip configuration for permanent change:
pip config set global.index-url https://pypi.org/simple
pip config set global.timeout 120
```

**Download packages offline:**
```bash
# On machine with internet:
pip download -r requirements.txt -d packages/

# Transfer packages/ directory to offline machine
# On offline machine:
pip install --no-index --find-links=packages/ -r requirements.txt
```

---

## Platform-Specific Issues

### Windows-Specific Issues

#### Issue 15: Long Path Support

**Symptoms:**
```bash
# Installation fails with:
# FileNotFoundError: [Errno 2] No such file or directory: 'C:\\Users\\...\\very\\long\\path\\...'
```

**Cause:** Windows has 260-character path limit by default.

**Solution:**
```bash
# Enable long path support (Windows 10 1607+):
# 1. Open Registry Editor (regedit)
# 2. Navigate to: HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
# 3. Set LongPathsEnabled to 1
# 4. Restart computer

# Or use Group Policy:
# 1. Run: gpedit.msc
# 2. Navigate to: Local Computer Policy > Computer Configuration > Administrative Templates > System > Filesystem
# 3. Enable "Enable Win32 long paths"
# 4. Restart

# Workaround - use shorter project path:
cd C:\
mkdir qa
cd qa
# Clone repository here
```

#### Issue 16: PowerShell Execution Policy

**Symptoms:**
```bash
venv\Scripts\Activate.ps1
# Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

**Cause:** PowerShell execution policy blocks scripts.

**Solution:**
```bash
# Check current policy:
Get-ExecutionPolicy

# Change policy for current user:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verify:
Get-ExecutionPolicy
# Expected: RemoteSigned

# Retry activation:
venv\Scripts\Activate.ps1

# Alternative - use Command Prompt instead of PowerShell:
cmd
venv\Scripts\activate.bat
```

---

### macOS-Specific Issues

#### Issue 17: Command Line Tools Dependency

**Symptoms:**
```bash
pip install -r requirements.txt
# clang: error: invalid version number in '-mmacosx-version-min=10.9'
# error: command 'clang' failed with exit code 1
```

**Cause:** Missing or outdated Xcode Command Line Tools.

**Solution:**
```bash
# Install Command Line Tools:
xcode-select --install

# If already installed, update:
sudo rm -rf /Library/Developer/CommandLineTools
xcode-select --install

# Verify installation:
xcode-select -p
# Expected: /Library/Developer/CommandLineTools

# Retry:
pip install -r requirements.txt
```

#### Issue 18: Homebrew Conflicts

**Symptoms:**
```bash
python3 --version
# Python 3.9.6 (Homebrew)
# But pip installs to system Python 3.8
```

**Cause:** Multiple Python installations from Homebrew and system.

**Solution:**
```bash
# Unlink old Python versions:
brew unlink python@3.9

# Install latest Python:
brew install python@3.12

# Link new Python:
brew link python@3.12

# Update PATH in ~/.zshrc or ~/.bash_profile:
export PATH="/usr/local/opt/python@3.12/bin:$PATH"

# Reload shell:
source ~/.zshrc  # or source ~/.bash_profile

# Verify:
which python3
# Expected: /usr/local/opt/python@3.12/bin/python3
python3 --version
# Expected: Python 3.12.x
```

---

### Linux-Specific Issues

#### Issue 19: System Python vs User Python

**Symptoms:**
```bash
sudo pip install selenium
# Successfully installed selenium-4.15.2
# But:
python3 -c "import selenium"
# ModuleNotFoundError: No module named 'selenium'
```

**Cause:** Installing with sudo installs to system Python, but user Python is different.

**Solution:**
```bash
# NEVER use sudo with pip for user installations
# Instead, use virtual environment:
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Or install to user directory:
pip install --user -r requirements.txt

# Ensure ~/.local/bin is in PATH:
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Issue 20: Missing apt Dependencies

**Symptoms:**
```bash
pip install -r requirements.txt
# ERROR: Could not build wheels for cryptography, which is required to install pyproject.toml-based projects
```

**Cause:** Missing system-level development packages.

**Solution:**

**Ubuntu/Debian:**
```bash
# Install required development packages:
sudo apt update
sudo apt install -y \
    python3.12-dev \
    python3.12-venv \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-pip \
    git

# Retry installation:
pip install -r requirements.txt
```

**RHEL/CentOS/Fedora:**
```bash
# Install required packages:
sudo dnf install -y \
    python3.12-devel \
    gcc \
    gcc-c++ \
    make \
    openssl-devel \
    libffi-devel \
    git

# Retry installation:
pip install -r requirements.txt
```

---

## webdriver-manager Installation

### Issue 21: webdriver-manager Binary Download Failures

**Symptoms:**
```bash
pip install webdriver-manager
# Successfully installed webdriver-manager-4.0.1

# But when running tests:
selenium.common.exceptions.WebDriverException: Message: Can not get version for Chromedriver: Message: 403 Client Error: Forbidden
```

**Cause:** Network restrictions, firewall blocking driver downloads, or GitHub rate limiting.

**Solution:**

**Option 1: Configure webdriver-manager cache:**
```bash
# Set custom cache location:
export WDM_LOCAL=1  # Use local cached drivers
export WDM_LOG_LEVEL=0  # Disable logging

# Or in Python code (utilities/driver_manager.py):
# from webdriver_manager.chrome import ChromeDriverManager
# ChromeDriverManager(cache_valid_range=30).install()
```

**Option 2: Manual driver download:**
```bash
# Download ChromeDriver manually:
# Visit: https://chromedriver.chromium.org/downloads
# Download version matching your Chrome browser

# Place in PATH or specify in code:
# driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
```

**Option 3: Use proxy settings:**
```bash
# Set proxy environment variables:
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"

# Retry test execution
```

---

### Issue 22: webdriver-manager Permission Issues

**Symptoms:**
```bash
# When running tests:
PermissionError: [Errno 13] Permission denied: '/home/user/.wdm/drivers/chromedriver/...'
```

**Cause:** webdriver-manager cache directory not writable.

**Solution:**
```bash
# Check cache location:
ls -la ~/.wdm/

# Fix permissions:
chmod -R 755 ~/.wdm/

# Or set custom cache location with write permissions:
export WDM_LOCAL=1
export WDM_LOG_LEVEL=0

# Or clear cache and retry:
rm -rf ~/.wdm/
# Driver will be re-downloaded on next test execution
```

---

## Diagnostic Steps

### Complete Installation Verification Checklist

Run these commands to verify your installation:

```bash
# 1. Verify Python version (3.9-3.12):
python3 --version
# Expected: Python 3.12.x (or 3.9, 3.10, 3.11)

# 2. Verify pip version:
pip --version
# Expected: pip 23.0+ from /path/to/venv/

# 3. Verify virtual environment is activated:
which python  # Linux/macOS
where python  # Windows
# Expected: /path/to/project/venv/bin/python

# 4. List installed packages:
pip list
# Expected: selenium, behave, pytest, webdriver-manager, etc.

# 5. Verify core packages:
pip show selenium
pip show behave
pip show pytest
pip show webdriver-manager

# 6. Test imports:
python -c "import selenium; print(selenium.__version__)"
# Expected: 4.15.2

python -c "import behave; print(behave.__version__)"
# Expected: 1.2.6

python -c "from selenium import webdriver; print('Selenium imports OK')"
# Expected: Selenium imports OK

# 7. Check for dependency conflicts:
pip check
# Expected: No broken requirements found.

# 8. Verify project structure:
ls -la
# Expected: config/, features/, pages/, utilities/, requirements.txt, etc.

# 9. Test configuration loading:
python -c "from config.test_config import get_config; config = get_config(); print('Config loaded OK')"
# Expected: Config loaded OK

# 10. Verify behave can find features:
behave --dry-run
# Expected: List of scenarios without errors
```

---

## Quick Diagnostic Commands

**Check Installation Health:**
```bash
# All-in-one diagnostic script:
python3 --version && \
pip --version && \
pip check && \
python -c "import selenium, behave, pytest; print('All core packages OK')"
```

**Installation Summary:**
```bash
# Generate installation report:
echo "Python Version:" && python3 --version
echo "pip Version:" && pip --version
echo "Virtual Environment:" && which python
echo "Installed Packages:" && pip list | wc -l
echo "Dependency Check:" && pip check
```

---

## Common Error Messages and Solutions

### ERROR: Could not find a version that satisfies the requirement

**Solution:**
1. Upgrade pip: `python -m pip install --upgrade pip`
2. Check Python version compatibility (3.9-3.12)
3. Verify package name spelling in requirements.txt

### ERROR: Microsoft Visual C++ 14.0 or greater is required (Windows)

**Solution:**
Install Visual Studio Build Tools:
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Install "Desktop development with C++"
- Restart and retry installation

### ERROR: [SSL: CERTIFICATE_VERIFY_FAILED]

**Solution:**
- Update SSL certificates (see Issue 7 above)
- Configure corporate proxy
- Temporarily use `--trusted-host` flags (not recommended)

### ModuleNotFoundError: No module named 'selenium'

**Solution:**
1. Ensure virtual environment is activated
2. Verify package installed: `pip show selenium`
3. Reinstall: `pip install selenium==4.15.2`
4. Check PYTHONPATH if running from IDE

---

## See Also

- [Getting Started: Installation Guide](../getting-started/installation.md) - Detailed installation instructions
- [Reference: Dependencies](../reference/dependencies.md) - Complete dependency list and purposes
- [Troubleshooting: Common Errors](./common-errors.md) - General error troubleshooting
- [README Installation Section](../../README.md#installation-pre-requisites) - Quick installation overview

---

**Last Updated:** 2024 (Based on Python 3.9-3.12, Selenium 4.15.2, Behave 1.2.6)

**Sources:**
- `README.md:45-136` - Installation prerequisites and setup
- `requirements.txt` - Package dependencies and versions
- `pyproject.toml:23-52` - Poetry dependency configuration
