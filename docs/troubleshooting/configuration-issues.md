# Configuration Issues Troubleshooting

## Overview

Configuration management is a critical part of the Testinium test automation framework, supporting multiple configuration sources with a defined precedence hierarchy. This guide helps diagnose and resolve common configuration-related issues including YAML parsing errors, environment variable problems, and configuration precedence conflicts.

**Configuration Precedence (highest to lowest):**
1. Environment variables (e.g., `BROWSER_TYPE`)
2. `.env` file variables
3. `config/config.yaml` values
4. Code default values

**Related Documentation:**
- [Configuration Options Reference](../reference/configuration-options.md) - Complete configuration reference
- [Environment Variables Reference](../reference/environment-variables.md) - All supported environment variables
- [Configuration Management Guide](../guides/configuration-management.md) - Advanced configuration patterns
- [Configuration Architecture](../architecture/configuration-management.md) - Precedence rules visualization

---

## YAML Parsing Errors

### Issue: YAML Syntax Errors in config.yaml

**Symptoms:**
```python
yaml.scanner.ScannerError: mapping values are not allowed here
  in "config/config.yaml", line 26, column 11
```

**Cause:** Invalid YAML syntax such as missing colons, incorrect indentation, or unquoted special characters.

**Common YAML Syntax Mistakes:**

**1. Missing colon after key:**
```yaml
# ❌ WRONG
browser
  type: chrome

# ✅ CORRECT
browser:
  type: chrome
```

**2. Inconsistent indentation:**
```yaml
# ❌ WRONG (mixing spaces and tabs, or inconsistent spacing)
browser:
  type: chrome
   headless: false  # 3 spaces instead of 2

# ✅ CORRECT (use 2 spaces consistently)
browser:
  type: chrome
  headless: false
```

**3. Unquoted special characters:**
```yaml
# ❌ WRONG (colon in value needs quotes)
application:
  base_url: https://example.com:8080/app

# ✅ CORRECT (quote values containing colons)
application:
  base_url: "https://example.com:8080/app"
```

**4. Incorrect list syntax:**
```yaml
# ❌ WRONG
reporting:
  formats: json, html, allure  # Comma-separated not valid

# ✅ CORRECT (use dash notation)
reporting:
  formats:
    - json
    - html
    - allure
```

**Solution: Validate YAML Syntax**

Use a YAML validator before running tests:

```bash
# Option 1: Use Python to validate YAML
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"

# Option 2: Install yamllint for comprehensive validation
pip install yamllint
yamllint config/config.yaml
```

**Create `.yamllint` configuration for consistent validation:**
```yaml
# .yamllint
extends: default
rules:
  line-length:
    max: 120
  indentation:
    spaces: 2
  comments:
    min-spaces-from-content: 1
```

**Source:** `config/test_config.py:258-260`, `utilities/config_reader.py:207-210`

---

### Issue: Environment Variable Interpolation Syntax Errors

**Symptoms:**
```python
ValueError: Required environment variable not set: BASE_URL:https
```

**Cause:** Incorrect syntax for environment variable interpolation in config.yaml.

**Common Interpolation Mistakes:**

**1. Using wrong bracket syntax:**
```yaml
# ❌ WRONG (shell-style expansion not supported)
base_url: $BASE_URL

# ❌ WRONG (double brackets)
base_url: ${{BASE_URL}}

# ✅ CORRECT (use ${VAR_NAME} syntax)
base_url: ${BASE_URL}
```

**2. Space in variable placeholders:**
```yaml
# ❌ WRONG (spaces inside curly braces)
username: ${ TEST_USERNAME }

# ✅ CORRECT (no spaces)
username: ${TEST_USERNAME}
```

**3. Incorrect default value syntax:**
```yaml
# ❌ WRONG (using = instead of :)
base_url: ${BASE_URL=https://default.com}

# ✅ CORRECT (use colon for defaults)
base_url: ${BASE_URL:https://default.com}
```

**Understanding Interpolation Syntax:**

The framework supports two interpolation patterns:

```yaml
# Pattern 1: Required variable (raises error if not set)
username: ${TEST_USERNAME}

# Pattern 2: Optional variable with default
base_url: ${BASE_URL:https://testinium.example.com}
```

**Source:** `config/test_config.py:265-309`, `config/config.yaml:7-15`

---

### Issue: Invalid YAML Data Types

**Symptoms:**
```python
TypeError: __init__() argument after ** must be a mapping, not list
```

**Cause:** Configuration value has wrong data type (e.g., list instead of dictionary, string instead of integer).

**Common Type Errors:**

**1. Boolean values not properly formatted:**
```yaml
# ❌ WRONG (string "true" instead of boolean)
browser:
  headless: "true"  # This becomes string "true", not boolean

# ✅ CORRECT (unquoted boolean)
browser:
  headless: true    # This is boolean True
```

**2. Numeric values as strings:**
```yaml
# ❌ WRONG (quoted numbers become strings)
timeouts:
  explicit: "10"    # String "10", not integer 10

# ✅ CORRECT (unquoted numbers)
timeouts:
  explicit: 10      # Integer 10
```

**3. Window size format errors:**
```yaml
# ❌ WRONG (list of strings)
browser:
  window_size: ["1920", "1080"]

# ❌ WRONG (string format)
browser:
  window_size: "1920x1080"

# ✅ CORRECT (list of integers)
browser:
  window_size: [1920, 1080]
```

**Solution: Type Validation Script**

Create a validation script to check configuration types:

```python
# validate_config.py
from config.test_config import Config

try:
    config = Config()
    print("✓ Configuration loaded successfully")
    print(f"  Browser type: {config.browser.type} (type: {type(config.browser.type).__name__})")
    print(f"  Headless: {config.browser.headless} (type: {type(config.browser.headless).__name__})")
    print(f"  Explicit timeout: {config.timeouts.explicit} (type: {type(config.timeouts.explicit).__name__})")
except Exception as e:
    print(f"✗ Configuration error: {e}")
```

**Source:** `config/test_config.py:191-217`

---

## Environment Variable Issues

### Issue: Missing .env File

**Symptoms:**
```python
WARNING:config.test_config:Credential environment variable not set: TEST_USERNAME
WARNING:config.test_config:Default test credentials not configured
```

**Cause:** The `.env` file doesn't exist, so environment variables for credentials aren't loaded.

**Solution:**

1. **Create `.env` from template:**
```bash
cp .env.example .env
```

2. **Edit `.env` with actual values:**
```bash
# .env
TEST_USERNAME=testuser@example.com
TEST_PASSWORD=your_secure_password_here

SALES_MANAGER_USERNAME=salesmanager@example.com
SALES_MANAGER_PASSWORD=manager_password_here

POS_MANAGER_USERNAME=posmanager@example.com
POS_MANAGER_PASSWORD=pos_password_here

BASE_URL=https://testinium.example.com
```

3. **Verify .env is loaded:**
```python
# test_env_loading.py
from dotenv import load_dotenv
import os

load_dotenv()
print(f"TEST_USERNAME loaded: {os.getenv('TEST_USERNAME') is not None}")
print(f"BASE_URL loaded: {os.getenv('BASE_URL')}")
```

**Important:** Never commit `.env` to version control. Ensure it's in `.gitignore`:
```bash
# Check .gitignore
grep "\.env" .gitignore
```

**Source:** `config/test_config.py:182-183`, `.env.example:1-31`

---

### Issue: Environment Variables Not Interpolated

**Symptoms:**
```bash
# Expected: https://staging.testinium.com
# Actual: ${BASE_URL}
```

**Cause:** Environment variables in config.yaml not being substituted due to:
1. Variable not set in environment or .env
2. Incorrect interpolation syntax
3. python-dotenv not loading before config parsing

**Diagnostic Steps:**

**1. Check if environment variable is set:**
```bash
# Linux/macOS
echo $BASE_URL

# Windows (PowerShell)
echo $env:BASE_URL

# Python check
python -c "import os; print(f'BASE_URL: {os.getenv(\"BASE_URL\")}')"
```

**2. Verify .env file loading:**
```python
# debug_env_loading.py
from dotenv import load_dotenv
import os
from pathlib import Path

env_file = Path(".env")
print(f".env exists: {env_file.exists()}")

load_dotenv(verbose=True)  # Verbose mode shows what's loaded
print(f"BASE_URL after load_dotenv: {os.getenv('BASE_URL')}")
```

**3. Test interpolation directly:**
```python
# test_interpolation.py
import os
from config.test_config import Config

os.environ['BASE_URL'] = 'https://test.example.com'
config = Config()
print(f"Base URL: {config.application.base_url}")
# Expected: https://test.example.com
```

**Solution:**

If environment variables aren't being substituted:

```python
# Ensure load_dotenv() is called before Config instantiation
from dotenv import load_dotenv
from config.test_config import Config

# Load environment variables first
load_dotenv()

# Then instantiate config (it will use loaded env vars)
config = Config()
```

**Source:** `config/test_config.py:265-309`, `utilities/config_reader.py:129-136`

---

### Issue: Variable Name Mismatch

**Symptoms:**
```python
# In config.yaml: ${TEST_USER}
# In .env: TEST_USERNAME=user@example.com
# Result: ValueError: Required environment variable not set: TEST_USER
```

**Cause:** Environment variable name in config.yaml doesn't match the actual variable name in .env.

**Solution:**

**Check all variable references match:**

```yaml
# config.yaml - Variable names must match .env exactly
credentials:
  username: ${TEST_USERNAME}      # ✓ Matches .env
  password: ${TEST_PASSWORD}      # ✓ Matches .env
  
# Common mistakes:
# username: ${USER}               # ❌ Wrong variable name
# username: ${TEST_USER}          # ❌ Missing _NAME suffix
# username: ${testusername}       # ❌ Wrong case (must be uppercase)
```

```bash
# .env - Use uppercase with underscores
TEST_USERNAME=testuser@example.com
TEST_PASSWORD=secure_password
```

**Validation script:**
```python
# validate_env_vars.py
import re
from pathlib import Path

# Extract variables from config.yaml
config_yaml = Path("config/config.yaml").read_text()
vars_in_config = set(re.findall(r'\$\{([^}:]+)', config_yaml))

# Extract variables from .env
env_file = Path(".env")
if env_file.exists():
    env_content = env_file.read_text()
    vars_in_env = set(re.findall(r'^([A-Z_]+)=', env_content, re.MULTILINE))
else:
    vars_in_env = set()

# Find mismatches
missing = vars_in_config - vars_in_env
print(f"Variables in config.yaml but not in .env: {missing}")
```

**Source:** `config/test_config.py:284-309`, `config/config.yaml:97-110`

---

## Configuration Precedence Problems

### Issue: Environment Variables Not Overriding config.yaml

**Symptoms:**
```bash
# Environment variable set:
export BROWSER_TYPE=firefox

# But tests still run with Chrome
# (value from config.yaml: type: chrome)
```

**Cause:** ConfigReader uses specific environment variable naming convention that may not match what you set.

**Understanding Environment Variable Precedence:**

The `ConfigReader` class converts dot notation keys to environment variable names:

```python
# Conversion pattern:
# config.yaml key: browser.type
# Environment variable: BROWSER_TYPE (uppercase, dots become underscores)
```

**Correct Environment Variable Names:**

```bash
# Config key -> Environment variable mapping
browser.type              -> BROWSER_TYPE
browser.headless          -> BROWSER_HEADLESS
timeouts.explicit         -> TIMEOUTS_EXPLICIT
application.base_url      -> APPLICATION_BASE_URL
credentials.username      -> CREDENTIALS_USERNAME
```

**Solution:**

**1. Use correct environment variable names:**
```bash
# ✓ CORRECT (matches conversion pattern)
export BROWSER_TYPE=firefox
export BROWSER_HEADLESS=true
export TIMEOUTS_EXPLICIT=15

# ❌ WRONG (doesn't match pattern)
export BROWSERTYPE=firefox    # Missing underscore
export browser.type=firefox   # Lowercase with dots
export BROWSER-TYPE=firefox   # Dash instead of underscore
```

**2. Verify precedence with diagnostic script:**
```python
# diagnose_precedence.py
import os
from utilities.config_reader import ConfigReader

# Set environment variable
os.environ['BROWSER_TYPE'] = 'firefox'

config = ConfigReader()
browser_type = config.get_property('browser.type')
print(f"Browser type from config: {browser_type}")
print(f"BROWSER_TYPE env var: {os.getenv('BROWSER_TYPE')}")
print(f"Match: {browser_type == os.getenv('BROWSER_TYPE')}")
```

**3. Check which source is active:**
```python
# check_config_source.py
import os
from utilities.config_reader import ConfigReader
import logging

logging.basicConfig(level=logging.DEBUG)

# ConfigReader logs where values come from:
# DEBUG:utilities.config_reader:Retrieved config 'browser.type' from environment variable 'BROWSER_TYPE'
# DEBUG:utilities.config_reader:Retrieved config 'browser.headless' from YAML configuration

config = ConfigReader()
browser_type = config.get_property('browser.type')
```

**Source:** `utilities/config_reader.py:220-299`, `utilities/config_reader.py:265-273`

---

### Issue: Config Dataclass Not Using Environment Variables

**Symptoms:**
```bash
# Environment variable set:
export TEST_USERNAME=admin@example.com

# But Config dataclass still shows empty credentials
config = Config()
print(config.credentials.username)  # Output: '' (empty string)
```

**Cause:** `Config` class uses environment variable interpolation in config.yaml, not direct environment variable access. The variables must be referenced in config.yaml using `${VAR_NAME}` syntax.

**Understanding Two Configuration Patterns:**

The framework has two configuration access patterns:

**Pattern 1: ConfigReader (direct environment variable precedence):**
```python
from utilities.config_reader import ConfigReader

config = ConfigReader()
# This checks BROWSER_TYPE env var FIRST, then config.yaml
browser = config.get_property('browser.type')
```

**Pattern 2: Config dataclass (interpolation in config.yaml):**
```python
from config.test_config import Config

# This ONLY substitutes ${VAR_NAME} placeholders in config.yaml
config = Config()
username = config.credentials.username
```

**Solution:**

For Config dataclass to use environment variables, they must be referenced in config.yaml:

```yaml
# config/config.yaml
credentials:
  username: ${TEST_USERNAME}        # ✓ Will substitute from environment
  password: ${TEST_PASSWORD}        # ✓ Will substitute from environment
  
  # NOT this:
  # username: testuser              # ❌ Hardcoded, ignores environment
```

**Diagnostic: Check interpolation is working:**
```python
# test_config_interpolation.py
import os
from config.test_config import Config

# Set environment variable
os.environ['TEST_USERNAME'] = 'test@example.com'
os.environ['TEST_PASSWORD'] = 'password123'

# Create config (loads .env, then instantiates)
from dotenv import load_dotenv
load_dotenv()

config = Config()
print(f"Username from config: {config.credentials.username}")
print(f"Expected: test@example.com")
print(f"Match: {config.credentials.username == 'test@example.com'}")
```

**Source:** `config/test_config.py:265-309`, `config/config.yaml:93-110`

---

## Missing Configuration Files

### Issue: config.yaml Not Found

**Symptoms:**
```python
FileNotFoundError: Configuration file not found: config/config.yaml
```

**Cause:** The config.yaml file doesn't exist or the framework is running from the wrong directory.

**Solution:**

**1. Verify config.yaml exists:**
```bash
ls -la config/config.yaml

# If missing, restore from version control:
git checkout config/config.yaml
```

**2. Check current working directory:**
```bash
# The framework expects to run from project root
pwd
# Should show: /path/to/testinium-qa-python

# If in wrong directory, navigate to project root:
cd /path/to/testinium-qa-python
```

**3. Verify directory structure:**
```bash
# Expected structure:
testinium-qa-python/
├── config/
│   ├── config.yaml          # Must exist here
│   ├── test_config.py
│   └── __init__.py
├── utilities/
├── pages/
├── features/
└── behave.ini
```

**4. Custom config file location:**

If you need to use a config file from a different location:

```python
from config.test_config import Config

# Specify custom config file path
config = Config(config_file='custom/path/to/config.yaml')
```

**Source:** `config/test_config.py:236-240`, `utilities/config_reader.py:168-179`

---

### Issue: .env File Not Created

**Symptoms:**
```bash
# Tests run but use hardcoded defaults
# Warnings about missing credentials
WARNING:config.test_config:Default test credentials not configured
```

**Cause:** `.env` file not created from `.env.example` template.

**Solution:**

**1. Create .env from template:**
```bash
# Copy template
cp .env.example .env

# Verify .env created
ls -la .env
```

**2. Edit .env with actual values:**
```bash
# Edit .env file
nano .env  # or vim, code, etc.

# Fill in all required values:
TEST_USERNAME=your_actual_user@example.com
TEST_PASSWORD=your_actual_password
BASE_URL=https://your-testinium-instance.com
```

**3. Verify .env is gitignored:**
```bash
# Ensure .env won't be committed
git status
# Should NOT show .env as untracked

# If it shows .env, add to .gitignore:
echo ".env" >> .gitignore
```

**Source:** `.env.example:1-31`, `config/test_config.py:182-183`

---

## Invalid Configuration Values

### Issue: Invalid Browser Type

**Symptoms:**
```python
ValueError: Browser type 'chromium' not supported. Use 'chrome', 'firefox', 'edge', or 'safari'
```

**Cause:** config.yaml specifies a browser type not supported by the framework.

**Solution:**

**Supported browser types:**
```yaml
# config.yaml
browser:
  type: chrome     # ✓ Supported
  # OR
  type: firefox    # ✓ Supported
  # OR
  type: edge       # ✓ Supported (Windows/macOS)
  # OR
  type: safari     # ✓ Supported (macOS only)
  
  # NOT supported:
  # type: chromium   # ❌ Use 'chrome'
  # type: ie         # ❌ IE not supported
  # type: opera      # ❌ Not implemented
```

**Override via environment variable:**
```bash
export BROWSER_TYPE=firefox
behave
```

**Source:** `config/test_config.py:41-54`, `utilities/driver_manager.py`

---

### Issue: Negative or Invalid Timeout Values

**Symptoms:**
```python
# Timeouts don't work as expected
# Or tests hang indefinitely
```

**Cause:** Timeout values in config.yaml are negative, zero, or unreasonably large.

**Solution:**

**Valid timeout configuration:**
```yaml
# config.yaml
timeouts:
  explicit: 10          # ✓ Good (10 seconds)
  page_load: 30         # ✓ Good (30 seconds)
  element_presence: 5   # ✓ Good (5 seconds)
  clickability: 3       # ✓ Good (3 seconds)
  
  # Invalid values:
  # explicit: -5        # ❌ Negative (use positive integers)
  # explicit: 0         # ❌ Zero timeout (no waiting)
  # explicit: 999999    # ❌ Too large (tests will hang)
  # explicit: "10"      # ❌ String (use integer)
```

**Recommended timeout ranges:**
- Explicit wait: 5-15 seconds (default: 10)
- Page load: 20-45 seconds (default: 30)
- Element presence: 3-10 seconds (default: 5)
- Clickability: 2-5 seconds (default: 3)

**Validation:**
```python
# validate_timeouts.py
from config.test_config import Config

config = Config()
timeouts = [
    ('explicit', config.timeouts.explicit),
    ('page_load', config.timeouts.page_load),
    ('element_presence', config.timeouts.element_presence),
    ('clickability', config.timeouts.clickability),
]

for name, value in timeouts:
    if not isinstance(value, int):
        print(f"✗ {name}: {value} is not an integer")
    elif value <= 0:
        print(f"✗ {name}: {value} is not positive")
    elif value > 120:
        print(f"⚠ {name}: {value} is very large (may cause hangs)")
    else:
        print(f"✓ {name}: {value} seconds is valid")
```

**Source:** `config/test_config.py:57-74`, `config/config.yaml:42-60`

---

### Issue: Malformed URLs

**Symptoms:**
```python
InvalidArgumentException: invalid argument: 'BASE_URL' is not a valid URL
```

**Cause:** URL in config.yaml is missing protocol, has typos, or invalid format.

**Solution:**

**Valid URL formats:**
```yaml
# config.yaml
application:
  base_url: https://testinium.example.com     # ✓ HTTPS with domain
  # OR
  base_url: http://localhost:8080              # ✓ HTTP with port
  # OR
  base_url: http://192.168.1.100:3000         # ✓ IP address with port
  
  # Invalid formats:
  # base_url: testinium.example.com           # ❌ Missing protocol
  # base_url: https://                        # ❌ Protocol only
  # base_url: ${BASE_URL}                     # ❌ If env var not set
  # base_url: "https://example.com:443/path"  # ✓ But quote if contains colon
```

**URL validation script:**
```python
# validate_urls.py
from config.test_config import Config
from urllib.parse import urlparse

config = Config()
urls = {
    'base_url': config.application.base_url,
    'login_url': config.application.login_url,
    'web_table_url': config.application.web_table_url,
}

for name, url in urls.items():
    parsed = urlparse(url)
    if not parsed.scheme:
        print(f"✗ {name}: Missing protocol (http/https)")
    elif not parsed.netloc:
        print(f"✗ {name}: Missing domain/host")
    elif parsed.scheme not in ['http', 'https']:
        print(f"✗ {name}: Invalid protocol '{parsed.scheme}'")
    else:
        print(f"✓ {name}: {url} is valid")
```

**Source:** `config/test_config.py:77-93`, `config/config.yaml:63-85`

---

### Issue: Type Validation Errors from Dataclasses

**Symptoms:**
```python
TypeError: __init__() got an unexpected keyword argument 'window_size'
# OR
TypeError: BrowserConfig.__init__() missing 1 required positional argument: 'type'
```

**Cause:** config.yaml structure doesn't match dataclass field definitions in test_config.py.

**Solution:**

**Match dataclass field names exactly:**

```yaml
# config.yaml - Field names must match dataclass definitions
browser:
  type: chrome              # ✓ Matches BrowserConfig.type
  headless: false           # ✓ Matches BrowserConfig.headless
  window_size: [1920, 1080] # ✓ Matches BrowserConfig.window_size
  implicit_wait: 0          # ✓ Matches BrowserConfig.implicit_wait (optional)
  
  # Common mistakes:
  # browser_type: chrome    # ❌ Wrong field name (should be 'type')
  # is_headless: false      # ❌ Wrong field name (should be 'headless')
  # size: [1920, 1080]      # ❌ Wrong field name (should be 'window_size')
```

**Check dataclass definitions:**

```python
# From config/test_config.py:40-54
@dataclass
class BrowserConfig:
    type: str                    # Required
    headless: bool               # Required
    window_size: Tuple[int, int] # Required
    implicit_wait: int = 0       # Optional (has default)
```

**Validation script:**
```python
# validate_structure.py
from config.test_config import Config, BrowserConfig
import yaml
from pathlib import Path

# Load raw YAML
config_yaml = yaml.safe_load(Path("config/config.yaml").read_text())

# Check browser config structure
browser_config = config_yaml.get('browser', {})
required_fields = ['type', 'headless', 'window_size']

for field in required_fields:
    if field not in browser_config:
        print(f"✗ Missing required field in browser config: {field}")
    else:
        print(f"✓ Found field: {field} = {browser_config[field]}")

# Try instantiating (will raise TypeError if structure wrong)
try:
    config = Config()
    print("✓ Configuration structure is valid")
except TypeError as e:
    print(f"✗ Configuration structure error: {e}")
```

**Source:** `config/test_config.py:40-137`, `config/config.yaml:18-38`

---

## behave.ini Configuration Issues

### Issue: Invalid Behave Format Options

**Symptoms:**
```bash
behave.configuration.ConfigError: BAD_FORMAT: unknown format 'cucumber-json'
```

**Cause:** Invalid format name in behave.ini `format` option.

**Solution:**

**Valid behave format options:**
```ini
# behave.ini
[behave]
# Valid built-in formats:
format = pretty           # ✓ Human-readable output
# OR
format = progress        # ✓ Progress dots
# OR
format = json            # ✓ JSON output
# OR
format = junit           # ✓ JUnit XML output
# OR
format = plain           # ✓ Simple text output

# Multiple formats (comma-separated):
format = pretty,json,junit

# Custom formatter (must be installed):
format = allure_behave.formatter:AllureFormatter

# Invalid formats:
# format = cucumber-json  # ❌ Use 'json' instead
# format = html           # ❌ No built-in HTML (use plugin)
```

**Source:** `behave.ini`, Behave documentation

---

### Issue: Behave Path Configuration Errors

**Symptoms:**
```bash
ConfigError: No features directory found at: features
```

**Cause:** behave.ini `paths` option points to non-existent directory.

**Solution:**

```ini
# behave.ini
[behave]
paths = features          # ✓ Correct (features/ directory exists)

# Common mistakes:
# paths = tests           # ❌ Wrong directory name
# paths = ./features/     # ⚠ Usually works but 'features' preferred
# paths = Features        # ❌ Case-sensitive (must be 'features')
```

**Verify features directory exists:**
```bash
ls -ld features/
# Should show: drwxr-xr-x ... features/
```

---

## pytest.ini Configuration Issues

### Issue: Invalid pytest Markers

**Symptoms:**
```bash
PytestUnknownMarkWarning: Unknown pytest.mark.smoke
```

**Cause:** Using markers not registered in pytest.ini.

**Solution:**

**Register all markers in pytest.ini:**
```ini
# pytest.ini
[pytest]
markers =
    smoke: Quick smoke tests
    regression: Full regression suite
    login: Login-related tests
    critical: Critical path tests
    wip: Work in progress tests
```

**Check marker usage:**
```bash
# List all markers in use
grep -r "@pytest.mark" tests/

# Run tests with specific marker
pytest -m smoke
```

---

## Configuration Validation and Debugging

### Verify YAML Syntax

**Command-line YAML validation:**
```bash
# Quick syntax check
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"

# Detailed validation with yamllint
pip install yamllint
yamllint config/config.yaml

# Custom yamllint rules
echo "extends: default" > .yamllint
yamllint config/config.yaml
```

---

### Test Environment Variable Interpolation

**Interactive interpolation test:**
```python
# test_env_interpolation.py
import os
import re
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read config.yaml
config_content = Path("config/config.yaml").read_text()

# Find all ${VAR_NAME} and ${VAR_NAME:default} patterns
pattern = r'\$\{([^}:]+)(?::([^}]*))?\}'
matches = re.findall(pattern, config_content)

print("Environment Variable Interpolation Check:")
print("=" * 60)

for var_name, default_value in matches:
    env_value = os.getenv(var_name)
    
    if env_value:
        print(f"✓ {var_name}: {env_value[:20]}... (from environment)")
    elif default_value:
        print(f"⚠ {var_name}: {default_value} (using default)")
    else:
        print(f"✗ {var_name}: NOT SET (will cause error)")

print("=" * 60)
```

---

### Check Configuration Loading with get_config()

**Comprehensive configuration check:**
```python
# check_config.py
import logging
from config.test_config import get_config, Config
from utilities.config_reader import ConfigReader

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(message)s'
)

print("Configuration Loading Diagnostic")
print("=" * 60)

# Test Config dataclass
try:
    config = get_config()
    print("✓ Config dataclass loaded successfully")
    print(f"  Browser: {config.browser.type} (headless: {config.browser.headless})")
    print(f"  Timeout: {config.timeouts.explicit}s")
    print(f"  Base URL: {config.application.base_url}")
    print(f"  Username: {'***' if config.credentials.username else 'NOT SET'}")
except Exception as e:
    print(f"✗ Config dataclass failed: {e}")

print()

# Test ConfigReader
try:
    config_reader = ConfigReader()
    print("✓ ConfigReader loaded successfully")
    browser = config_reader.get_property('browser.type')
    print(f"  Browser (via ConfigReader): {browser}")
except Exception as e:
    print(f"✗ ConfigReader failed: {e}")

print("=" * 60)
```

---

### Debug Configuration with Logging

**Enable comprehensive logging:**
```python
# debug_config_loading.py
import logging
import sys

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# Now import and use config (all debug logs will show)
from config.test_config import Config
from utilities.config_reader import ConfigReader

print("\n" + "="*60)
print("Loading Config dataclass:")
print("="*60)
config = Config()

print("\n" + "="*60)
print("Loading ConfigReader:")
print("="*60)
config_reader = ConfigReader()
```

**Expected debug output:**
```
2024-01-15 10:30:00 - config.test_config - INFO - Environment variables loaded from .env file
2024-01-15 10:30:00 - config.test_config - INFO - Configuration loaded from config/config.yaml
2024-01-15 10:30:00 - config.test_config - DEBUG - Browser config: type=chrome, headless=False
2024-01-15 10:30:00 - config.test_config - DEBUG - Timeout config: explicit=10s, page_load=30s
2024-01-15 10:30:00 - config.test_config - DEBUG - Application config: base_url=https://testinium.example.com
2024-01-15 10:30:00 - utilities.config_reader - INFO - Loading environment variables from .env file
2024-01-15 10:30:00 - utilities.config_reader - INFO - Successfully loaded configuration with 5 top-level keys
```

---

## Quick Reference: Common Configuration Errors

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `yaml.scanner.ScannerError: mapping values not allowed` | Invalid YAML syntax | Check indentation, colons, quotes |
| `FileNotFoundError: config.yaml` | Missing config file or wrong directory | Ensure config/config.yaml exists, run from project root |
| `ValueError: Required environment variable not set` | Missing environment variable | Create .env file from .env.example, set all required variables |
| `KeyError: Required configuration key not found` | Missing config section or typo | Check key name matches config.yaml exactly |
| `TypeError: __init__() missing required argument` | Config structure mismatch | Ensure config.yaml structure matches dataclass definitions |
| `WARNING: Credential environment variable not set` | Missing credentials in .env | Add TEST_USERNAME, TEST_PASSWORD to .env |
| `ConfigurationError: Invalid YAML format` | YAML root is not a dictionary | Ensure config.yaml starts with top-level keys (browser:, timeouts:, etc.) |

---

## Additional Resources

- **Configuration Options Reference:** [docs/reference/configuration-options.md](../reference/configuration-options.md)
- **Environment Variables Reference:** [docs/reference/environment-variables.md](../reference/environment-variables.md)
- **Configuration Management Guide:** [docs/guides/configuration-management.md](../guides/configuration-management.md)
- **Architecture Documentation:** [docs/architecture/configuration-management.md](../architecture/configuration-management.md)
- **Installation Troubleshooting:** [docs/troubleshooting/installation-issues.md](./installation-issues.md)

---

**Document Status:** Complete  
**Last Updated:** 2024  
**Framework Version:** 1.0.0  
**Source Files Referenced:**
- `config/test_config.py` (lines 1-445)
- `config/config.yaml` (lines 1-163)
- `.env.example` (lines 1-31)
- `utilities/config_reader.py` (lines 1-395)
- `README.md` (lines 602-714)
