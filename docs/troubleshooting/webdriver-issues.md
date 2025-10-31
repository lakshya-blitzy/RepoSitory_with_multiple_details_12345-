# WebDriver Issues

Comprehensive troubleshooting guide for WebDriver-related problems in the Testinium QA Python test automation framework.

## Overview

WebDriver issues are among the most common problems in Selenium test automation. This guide covers diagnosis and resolution of driver binary provisioning, browser compatibility, headless mode configuration, and threading problems.

The framework uses **webdriver-manager** for automatic driver binary management, eliminating most manual setup issues. However, understanding common failure modes helps diagnose problems quickly.

**Prerequisites:**
- Python 3.9+ installed
- Framework dependencies installed (`pip install -r requirements.txt`)
- Chrome or Firefox browser installed

**Related Documentation:**
- [Architecture: Parallel Execution](../architecture/parallel-execution.md) - Threading patterns
- [Guide: Parallel Execution](../guides/parallel-execution.md) - Running tests in parallel
- [Configuration Management](../guides/configuration-management.md) - Browser configuration
- [API: DriverManager](../api-reference/utilities/driver-manager.md) - Driver lifecycle management

---

## Driver Not Found Errors

### Symptom: WebDriverException - Driver Executable Not in PATH

**Error Message:**
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH
```

or

```
selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH
```

**Cause:**

The WebDriver binary (chromedriver or geckodriver) is not found in the system PATH, and automatic provisioning failed.

**Solution 1: Verify webdriver-manager Installation**

The framework uses **webdriver-manager** to automatically download and manage driver binaries. Verify it's installed:

```bash
# Check if webdriver-manager is installed
pip show webdriver-manager

# If not installed or outdated:
pip install --upgrade webdriver-manager>=4.0.0
```

**Solution 2: Clear Driver Cache and Re-provision**

webdriver-manager caches drivers in `~/.wdm/drivers/`. Corrupted cache can cause provisioning failures:

```bash
# Clear webdriver-manager cache
rm -rf ~/.wdm/drivers/

# Run tests to trigger fresh download
behave features/Login.feature
```

On Windows:
```powershell
# PowerShell
Remove-Item -Recurse -Force $env:USERPROFILE\.wdm\drivers

# Run tests
behave features/Login.feature
```

**Solution 3: Manual Driver Installation (Fallback)**

If automatic provisioning fails persistently, download drivers manually:

**Chrome:**
```bash
# Download ChromeDriver matching your Chrome version
# Visit: https://chromedriver.chromium.org/downloads

# Check Chrome version first:
google-chrome --version  # Linux/macOS
# or
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version  # Windows

# Extract chromedriver and add to PATH:
sudo mv chromedriver /usr/local/bin/  # macOS/Linux
chmod +x /usr/local/bin/chromedriver

# Verify installation:
chromedriver --version
```

**Firefox:**
```bash
# Download GeckoDriver from:
# https://github.com/mozilla/geckodriver/releases

# Check Firefox version first:
firefox --version

# Extract geckodriver and add to PATH:
sudo mv geckodriver /usr/local/bin/  # macOS/Linux
chmod +x /usr/local/bin/geckodriver

# Verify installation:
geckodriver --version
```

**Solution 4: Enable Debug Logging**

Enable webdriver-manager logging to diagnose provisioning failures:

```python
# Temporary modification to utilities/driver_manager.py for debugging
import os
os.environ['WDM_LOG'] = '1'  # Enable webdriver-manager verbose logging
```

Check console output for download errors, network issues, or permission problems.

**Source:** `utilities/driver_manager.py:280-305` (Driver binary provisioning)

---

## Browser Version Mismatch

### Symptom: SessionNotCreatedException - Version Mismatch

**Error Message:**
```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: 
This version of ChromeDriver only supports Chrome version 120
```

or

```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created:
Unable to find a matching set of capabilities
```

**Cause:**

The WebDriver binary version does not match the installed browser version. This typically happens when:
- Browser auto-updated but driver cache is stale
- Manual driver installation is outdated
- Browser installed in non-standard location

**How webdriver-manager Handles Versions:**

The framework uses webdriver-manager which automatically detects browser version and downloads matching drivers:

```python
# From utilities/driver_manager.py
chrome_service = ChromeService(ChromeDriverManager().install())  # Auto-matches Chrome version
firefox_service = FirefoxService(GeckoDriverManager().install())  # Auto-matches Firefox version
```

**Source:** `utilities/driver_manager.py:283, 305`

**Solution 1: Check Browser Versions**

**Chrome:**
```bash
# Linux
google-chrome --version

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Windows (PowerShell)
(Get-Item "C:\Program Files\Google\Chrome\Application\chrome.exe").VersionInfo.ProductVersion

# Expected output: Google Chrome 120.0.6099.129
```

**Firefox:**
```bash
# Linux/macOS
firefox --version

# Windows
"C:\Program Files\Mozilla Firefox\firefox.exe" -v | more

# Expected output: Mozilla Firefox 121.0
```

**Solution 2: Force Driver Update**

Clear driver cache to force fresh download matching current browser version:

```bash
# Remove cached drivers
rm -rf ~/.wdm/drivers/

# Run test to trigger automatic re-provisioning
behave features/Login.feature

# webdriver-manager will detect browser version and download matching driver
```

**Solution 3: Update Browser**

Ensure browser is updated to latest stable version:

**Chrome:**
- Linux: `sudo apt update && sudo apt upgrade google-chrome-stable`
- macOS: Chrome > Help > About Google Chrome (auto-updates)
- Windows: Chrome > Help > About Google Chrome (auto-updates)

**Firefox:**
- Linux: `sudo apt update && sudo apt upgrade firefox`
- macOS: Firefox > Help > About Firefox (auto-updates)
- Windows: Firefox > Help > About Firefox (auto-updates)

**Solution 4: Specify Driver Version (Advanced)**

If specific driver version needed:

```python
# Temporary modification for testing (not recommended for production)
from webdriver_manager.chrome import ChromeDriverManager

# Force specific driver version
chrome_service = ChromeService(ChromeDriverManager(driver_version="120.0.6099.109").install())
```

**Note:** This disables automatic version matching. Only use for debugging.

**Verification:**

After resolution, verify driver and browser compatibility:

```python
# Run driver manager self-test
python -m utilities.driver_manager

# Expected output should show successful driver creation
```

**Source:** `utilities/driver_manager.py:549-607` (Self-test module)

---

## Headless Mode Issues

### Symptom: Tests Fail in CI But Pass Locally

**Error Patterns:**
- `ElementNotInteractableException` in CI but works locally
- Screenshots are blank or show rendering issues
- Font rendering errors in headless mode
- Display buffer errors on headless servers

**Cause:**

Headless browser mode behaves differently than headed mode:
- No GPU acceleration by default
- Different font rendering
- No display buffer on CI servers
- Missing visual feedback for element state

**Solution 1: Enable Headless Mode for CI/CD**

Configure headless mode in `config/config.yaml`:

```yaml
# config/config.yaml
browser:
  type: chrome
  headless: true  # Enable for CI/CD environments
```

Or override via environment variable:

```bash
# In Jenkins, GitHub Actions, GitLab CI, etc.
export HEADLESS=true
behave
```

**Source:** `config/config.yaml:28-29`

**Solution 2: Add Required Chrome Options for Headless Stability**

The framework already includes essential headless options:

```python
# From utilities/driver_manager.py:266-277
chrome_options = ChromeOptions()

if headless:
    chrome_options.add_argument('--headless=new')  # Selenium 4.x new headless mode

# Stability options for CI/CD (applied regardless of headless)
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')  # Required for Docker/containers
chrome_options.add_argument('--disable-dev-shm-usage')  # Prevents /dev/shm space issues
chrome_options.add_argument('--disable-extensions')
```

**Source:** `utilities/driver_manager.py:266-277`

**Solution 3: Fix Font Rendering in Headless Mode**

If screenshots show missing fonts in headless mode:

```bash
# Install required fonts on CI server (Debian/Ubuntu)
sudo apt-get update
sudo apt-get install -y \
    fonts-liberation \
    libappindicator3-1 \
    libnss3 \
    xdg-utils

# For CentOS/RHEL:
sudo yum install -y \
    liberation-fonts \
    nss \
    xdg-utils
```

**Solution 4: Configure Display Buffer for Headless**

On headless CI servers, configure virtual display buffer:

**Option A: Xvfb (X Virtual Framebuffer)**
```bash
# Install Xvfb
sudo apt-get install -y xvfb

# Run tests with virtual display
xvfb-run --auto-servernum --server-args="-screen 0 1920x1080x24" behave

# Or in CI pipeline:
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
behave
```

**Option B: Use --headless=new (Recommended)**

Modern Chrome headless mode (`--headless=new`) doesn't require Xvfb:

```python
# Already configured in utilities/driver_manager.py:270
chrome_options.add_argument('--headless=new')
```

This is the **recommended approach** for Chrome 109+.

**Solution 5: Verify Screenshot Capture in Headless**

Test screenshot functionality in headless mode:

```python
# Test script to verify headless screenshots
from utilities.driver_manager import DriverManager

driver = DriverManager.get_driver()
driver.get("https://example.com")

# Capture screenshot
screenshot_path = "reports/screenshots/headless-test.png"
driver.save_screenshot(screenshot_path)

print(f"Screenshot saved: {screenshot_path}")
DriverManager.quit_driver()
```

Verify screenshot file is created and not blank.

**Troubleshooting Headless Rendering:**

```python
# Add window size for consistent rendering
chrome_options.add_argument('--window-size=1920,1080')

# Disable hardware acceleration if rendering issues persist
chrome_options.add_argument('--disable-software-rasterizer')

# Force CPU rendering instead of GPU
chrome_options.add_argument('--disable-gpu-compositing')
```

**Source:** `utilities/screenshot_helper.py` (Screenshot capture logic)

---

## ChromeDriver-Specific Issues

### Symptom: Chrome Binary Corrupted or Permission Denied

**Error Message:**
```
selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: exited normally
```

or

```
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome binary path is invalid
```

**Cause:**

ChromeDriver or Chrome binary has permission issues, is corrupted, or Chrome installed in non-standard location.

**Solution 1: Verify Chrome Installation**

```bash
# Check Chrome binary location
which google-chrome

# Verify Chrome is executable
google-chrome --version

# Check permissions
ls -l $(which google-chrome)
# Should show: -rwxr-xr-x (executable)
```

**Solution 2: Fix Binary Permissions**

```bash
# Make Chrome executable
sudo chmod +x /usr/bin/google-chrome

# Make chromedriver executable (if manually installed)
sudo chmod +x /usr/local/bin/chromedriver
```

**Solution 3: Specify Chrome Binary Path (Non-Standard Installation)**

If Chrome installed in custom location:

```python
# Modify utilities/driver_manager.py temporarily for debugging
chrome_options = ChromeOptions()
chrome_options.binary_location = "/path/to/chrome/binary"
```

**Common Chrome binary paths:**
- Linux: `/usr/bin/google-chrome`
- macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Windows: `C:\Program Files\Google\Chrome\Application\chrome.exe`

### Symptom: Sandbox Errors on Linux

**Error Message:**
```
selenium.common.exceptions.WebDriverException: Message: unknown error: DevToolsActivePort file doesn't exist
```

or

```
Failed to move to new namespace: PID namespaces supported, Network namespace supported, but failed: errno = Operation not permitted
```

**Cause:**

Chrome sandbox requires privileged operations not available in containers or restricted environments.

**Solution: Disable Sandbox (Already Configured)**

The framework disables Chrome sandbox by default for CI/CD compatibility:

```python
# From utilities/driver_manager.py:275
chrome_options.add_argument('--no-sandbox')
```

This is safe for test environments where Chrome runs in isolation.

**Source:** `utilities/driver_manager.py:275`

**Additional Docker/Container Options:**

If running in Docker containers, also add:

```python
chrome_options.add_argument('--disable-setuid-sandbox')
chrome_options.add_argument('--single-process')  # Last resort for very restricted environments
```

### Symptom: ChromeService Configuration Issues

**Error Message:**
```
TypeError: ChromeService.__init__() got an unexpected keyword argument 'executable_path'
```

**Cause:**

Selenium 4.x changed ChromeService API. Old syntax no longer supported.

**Solution: Use Selenium 4.x Service Pattern (Already Implemented)**

```python
# CORRECT (Selenium 4.x) - Already used in framework
from selenium.webdriver.chrome.service import Service as ChromeService
chrome_service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# INCORRECT (Selenium 3.x - deprecated):
# driver = webdriver.Chrome(executable_path=path, options=chrome_options)
```

**Source:** `utilities/driver_manager.py:283-286`

---

## GeckoDriver-Specific Issues

### Symptom: Firefox Tests Fail With ChromeDriver Error

**CRITICAL BUG FIX FROM JAVA MIGRATION:**

**Error Message (From Java Version):**
```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable cannot launch Firefox browser
```

**Root Cause:**

The original Java `Driver.java` line 37 had a critical bug:

```java
// INCORRECT - Java Driver.java line 37
case "firefox":
    WebDriverManager.chromedriver().setup();  // BUG! Should be geckodriver()
    driverPool.set(new FirefoxDriver());
```

This caused Firefox tests to fail because ChromeDriver cannot drive Firefox.

**Python Fix (Already Implemented):**

```python
# CORRECT - utilities/driver_manager.py:289-309
elif browser_type.lower() == 'firefox':
    firefox_options = FirefoxOptions()
    
    if headless:
        firefox_options.add_argument('--headless')
    
    # CRITICAL FIX: Use GeckoDriverManager for Firefox (not ChromeDriverManager)
    firefox_service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
```

**Source:** `utilities/driver_manager.py:14-20, 289-309` (Bug fix documentation)

**Verification:**

Test Firefox driver creation:

```python
# Test Firefox driver with explicit configuration
from utilities.config_reader import ConfigReader
config = ConfigReader()

# Temporarily override browser type
import os
os.environ['BROWSER_TYPE'] = 'firefox'

# Create driver
from utilities.driver_manager import DriverManager
driver = DriverManager.get_driver()
print(f"Browser: {driver.capabilities['browserName']}")  # Should print 'firefox'

DriverManager.quit_driver()
```

### Symptom: GeckoDriver Port Conflicts

**Error Message:**
```
selenium.common.exceptions.WebDriverException: Message: Reached error page: about:neterror?e=connectionFailure
```

or

```
Address already in use
```

**Cause:**

GeckoDriver uses port 4444 by default. Conflicts occur if multiple Firefox instances run simultaneously without proper isolation.

**Solution: Thread-Local Driver Isolation (Already Implemented)**

The framework uses `threading.local()` to ensure each test thread gets its own WebDriver instance:

```python
# From utilities/driver_manager.py:127-129
class DriverManager:
    # Thread-local storage for WebDriver instances
    _thread_local = threading.local()
```

This prevents port conflicts in parallel execution.

**Source:** `utilities/driver_manager.py:127-129`

See [Architecture: Parallel Execution](../architecture/parallel-execution.md) for threading.local() pattern details.

### Symptom: Firefox Profile Errors

**Error Message:**
```
selenium.common.exceptions.SessionNotCreatedException: Message: Failed to set preferences: Profile does not exist
```

**Cause:**

Firefox profile configuration issues or corrupted profile.

**Solution: Let WebDriver Manage Profiles**

The framework uses default Firefox profile management (no custom profiles):

```python
# From utilities/driver_manager.py:296-308
firefox_options = FirefoxOptions()
# No custom profile specified - WebDriver creates temporary profile

firefox_service = FirefoxService(GeckoDriverManager().install())
driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
```

If custom profile needed (advanced use case):

```python
# Custom Firefox profile (not standard in framework)
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

profile = FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.dir", "/tmp/downloads")

firefox_options = FirefoxOptions()
firefox_options.profile = profile
```

---

## Driver Binary Caching

### Cache Location

webdriver-manager caches downloaded drivers in:

**Linux/macOS:**
```
~/.wdm/drivers/chromedriver/linux64/120.0.6099.109/chromedriver
~/.wdm/drivers/geckodriver/linux64/0.34.0/geckodriver
```

**Windows:**
```
C:\Users\<username>\.wdm\drivers\chromedriver\win64\120.0.6099.109\chromedriver.exe
C:\Users\<username>\.wdm\drivers\geckodriver\win64\0.34.0\geckodriver.exe
```

### Symptom: Cache Corruption

**Error Message:**
```
PermissionError: [Errno 13] Permission denied: '/home/user/.wdm/drivers/chromedriver/...'
```

or

```
OSError: [Errno 8] Exec format error
```

**Cause:**

Corrupted cache from interrupted downloads, permission issues, or disk full errors.

**Solution: Clear and Rebuild Cache**

```bash
# Linux/macOS
rm -rf ~/.wdm/

# Windows PowerShell
Remove-Item -Recurse -Force $env:USERPROFILE\.wdm

# Run tests to rebuild cache
behave features/Login.feature
```

### Cache Management Best Practices

**CI/CD Caching:**

Cache the `~/.wdm/` directory in CI pipelines to speed up builds:

**GitHub Actions:**
```yaml
- name: Cache WebDriver binaries
  uses: actions/cache@v3
  with:
    path: ~/.wdm
    key: ${{ runner.os }}-wdm-${{ hashFiles('requirements.txt') }}
```

**Jenkins:**
```groovy
// Cache in Jenkinsfile
dir("${env.HOME}/.wdm") {
    // Persist across builds
}
```

**Docker:**

Include driver provisioning in Docker image build:

```dockerfile
# Dockerfile
RUN python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
RUN python -c "from webdriver_manager.firefox import GeckoDriverManager; GeckoDriverManager().install()"
```

**Cache Invalidation:**

Clear cache when:
- Browser version updated
- webdriver-manager version upgraded
- Persistent driver issues occur

---

## Threading Issues with WebDriver

### Architecture: Thread-Local Pattern

The framework uses `threading.local()` for thread-safe WebDriver management:

```python
# From utilities/driver_manager.py:127-129
class DriverManager:
    # Each thread gets its own WebDriver instance
    _thread_local = threading.local()
    
    @classmethod
    def get_driver(cls) -> WebDriver:
        # Check if current thread has driver
        if not hasattr(cls._thread_local, 'driver') or cls._thread_local.driver is None:
            # Create new driver for this thread
            cls._thread_local.driver = cls._create_driver()
        return cls._thread_local.driver
```

**Source:** `utilities/driver_manager.py:82-196`

**Why Thread-Local?**

- **Isolation:** Each test thread gets its own WebDriver instance
- **No Race Conditions:** No shared state between threads
- **Port Conflicts Prevented:** Each driver uses different port
- **Clean Separation:** Driver lifecycle independent per thread

See [Architecture: Parallel Execution](../architecture/parallel-execution.md) for detailed threading.local() pattern explanation.

### Symptom: Driver Conflicts in Parallel Execution

**Error Patterns:**
- Tests interfere with each other
- Driver operations fail with "session not found"
- Port conflicts
- Stale driver references

**Cause:**

Improper WebDriver instance sharing between threads.

**Solution: Always Use DriverManager (Already Correct)**

**CORRECT (Framework Standard):**
```python
# In step definitions (features/steps/*.py)
from utilities.driver_manager import DriverManager

@when('User clicks login button')
def step_impl(context):
    # Get thread-local driver
    driver = DriverManager.get_driver()
    driver.find_element(By.ID, "login").click()
```

**INCORRECT (Causes Threading Issues):**
```python
# DON'T DO THIS - Shared driver instance
driver = webdriver.Chrome()  # Global driver - shared across threads!

@when('User clicks login button')
def step_impl(context):
    driver.find_element(By.ID, "login").click()  # Race condition!
```

### Parallel Execution Configuration

**Behave Parallel Execution:**

```bash
# Run scenarios in parallel (process-based)
behave --processes 4 --parallel-element scenario
```

**pytest-xdist Parallel Execution:**

```bash
# Run tests in parallel (thread-based)
pytest -n 4 tests/
```

Both approaches work correctly with `threading.local()` pattern.

**Source:** See [Guide: Parallel Execution](../guides/parallel-execution.md)

---

## Diagnostic Commands

### Check Browser Versions

**Chrome:**
```bash
# Linux
google-chrome --version

# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Windows (PowerShell)
(Get-Item "C:\Program Files\Google\Chrome\Application\chrome.exe").VersionInfo.ProductVersion
```

**Firefox:**
```bash
# Linux/macOS
firefox --version

# Windows
"C:\Program Files\Mozilla Firefox\firefox.exe" -v | more
```

### Verify Driver Binary

**ChromeDriver:**
```bash
# Check chromedriver in cache
ls -la ~/.wdm/drivers/chromedriver/

# Test chromedriver execution
chromedriver --version

# Check PATH
which chromedriver
```

**GeckoDriver:**
```bash
# Check geckodriver in cache
ls -la ~/.wdm/drivers/geckodriver/

# Test geckodriver execution
geckodriver --version

# Check PATH
which geckodriver
```

### Test Driver Initialization

**Run DriverManager Self-Test:**
```bash
# Execute driver manager module directly
python -m utilities.driver_manager

# Expected output:
# === Driver Manager Self-Test ===
# 1. Testing driver initialization...
#    ✓ Driver initialized: chrome
# 2. Testing driver reuse...
#    ✓ Driver reuse verified (same instance returned)
# ...
# ✓ All driver manager tests passed!
```

**Source:** `utilities/driver_manager.py:549-613` (Self-test implementation)

**Test Specific Browser:**
```bash
# Test Chrome
export BROWSER_TYPE=chrome
python -m utilities.driver_manager

# Test Firefox
export BROWSER_TYPE=firefox
python -m utilities.driver_manager
```

### Enable WebDriver Logging

**ChromeDriver Logging:**

```python
# Temporary modification for debugging
chrome_options = ChromeOptions()
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--v=1')  # Verbosity level 1-3

# Set log path
import logging
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.DEBUG)
```

**GeckoDriver Logging:**

```python
# Enable GeckoDriver verbose logging
import os
os.environ['GECKODRIVER_LOG'] = 'trace'  # Options: fatal, error, warn, info, config, debug, trace

firefox_service = FirefoxService(
    GeckoDriverManager().install(),
    log_path='reports/geckodriver.log'
)
```

**Selenium Wire Protocol Logging:**

```python
# Enable Selenium wire protocol logging (very verbose)
import logging
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.DEBUG)
```

### Check Framework Configuration

```python
# Verify configuration loading
from utilities.config_reader import ConfigReader

config = ConfigReader()
print(f"Browser Type: {config.get_property('browser.type')}")
print(f"Headless: {config.get_property('browser.headless')}")
print(f"Timeout: {config.get_property('timeouts.explicit')}")
```

### Network and Proxy Diagnostics

**Check Network Connectivity:**
```bash
# Test driver download URLs
curl -I https://chromedriver.storage.googleapis.com/
curl -I https://github.com/mozilla/geckodriver/releases/
```

**Configure Proxy for webdriver-manager:**
```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1

# Run tests with proxy
behave
```

---

## Quick Reference: Common Fixes

| Issue | Quick Fix |
|-------|-----------|
| Driver not found | `rm -rf ~/.wdm/` then re-run tests |
| Version mismatch | Update browser to latest version |
| CI tests fail | Set `headless: true` in config.yaml |
| Sandbox errors | Already fixed with `--no-sandbox` option |
| Port conflicts | Use DriverManager (thread-local pattern) |
| Cache corruption | `rm -rf ~/.wdm/` to clear cache |
| Firefox using ChromeDriver | Already fixed in Python version (line 14-20 bug) |
| Permission denied | `chmod +x` on driver binary |
| Blank screenshots | Use `--headless=new` for Chrome 109+ |

---

## Still Having Issues?

If problems persist after trying solutions in this guide:

1. **Enable Debug Logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Run Driver Self-Test:**
   ```bash
   python -m utilities.driver_manager
   ```

3. **Check Other Troubleshooting Guides:**
   - [Installation Issues](installation-issues.md)
   - [Configuration Issues](configuration-issues.md)
   - [Parallel Execution Issues](parallel-execution-issues.md)

4. **Review Architecture Documentation:**
   - [System Architecture](../architecture/system-overview.md)
   - [Threading Patterns](../architecture/parallel-execution.md)

5. **Consult API Documentation:**
   - [DriverManager API](../api-reference/utilities/driver-manager.md)
   - [ConfigReader API](../api-reference/utilities/config-reader.md)

**Source Code References:**
- Driver Management: `utilities/driver_manager.py`
- Configuration: `config/config.yaml`
- Browser Options: `utilities/driver_manager.py:264-309`

---

**Document Version:** 1.0.0  
**Last Updated:** 2024  
**Applies To:** Python Selenium + Behave Framework v1.0+
