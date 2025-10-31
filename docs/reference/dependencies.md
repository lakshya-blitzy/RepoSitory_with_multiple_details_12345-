# Dependencies Reference

## Overview

The Testinium QA Python test automation framework uses Python's standard dependency management tools to manage all third-party packages. This document provides a comprehensive reference for all dependencies, their purposes, version requirements, and migration context from the original Java/Maven implementation.

### Python Dependency Management

Python dependencies are managed through multiple configuration files:

- **`requirements.txt`** - Primary dependency list with exact versions for reproducible installations
- **`pyproject.toml`** - Poetry configuration with semantic version ranges and development dependencies
- **`setup.py`** - Package installation configuration for distribution and setuptools integration

### Migration from Maven pom.xml

This framework was migrated from a Java + Cucumber + Maven project to Python + Behave. All Java dependencies have been carefully mapped to Python equivalents, maintaining behavioral compatibility while leveraging Python-native patterns.

**Source:** `requirements.txt:1-3`, `pyproject.toml:1-4`, `setup.py:1-6`

### Installation Commands

```bash
# Standard installation (using pip and requirements.txt)
pip install -r requirements.txt

# Poetry installation (with dependency resolution)
poetry install

# Development installation (includes code quality tools)
pip install -r requirements.txt
pip install -e .[dev]

# Or with Poetry:
poetry install --with dev
```

**Source:** `setup.py:18-61`, `pyproject.toml:23-67`

---

## Complete Dependency Reference

### Core Testing Framework

Core testing dependencies that provide BDD, WebDriver automation, and test execution capabilities.

| Package Name | Version | Purpose | Replaces (Java/Maven) | Notes |
|--------------|---------|---------|----------------------|-------|
| **selenium** | 4.15.2 | WebDriver automation library for browser control | selenium-java 3.141.59 | Upgraded to WebDriver 4.x API with improved stability and BiDi protocol support |
| **behave** | 1.2.6 | BDD framework for Gherkin feature files and step definitions | cucumber-java 7.2.3 | Python-native BDD framework with similar scenario execution model |
| **pytest** | 7.4.3 | Python testing framework with fixtures and assertions | junit 4.13.2 | Provides test discovery, fixtures, parametrization, and plugin ecosystem |
| **pytest-bdd** | 6.1.1 | BDD integration for pytest with Gherkin support | cucumber-junit 7.2.3 | Optional integration allowing pytest and Behave coexistence |

**Source:** `requirements.txt:9-19`, `pyproject.toml:25-29`, `setup.py:21-25`

**Key Migration Notes:**
- **Selenium 4.x**: WebDriver 4.x eliminates the need for separate driver executables when using webdriver-manager
- **Behave vs Cucumber**: Behave provides similar Gherkin syntax with Python-native step definitions using decorators (@given, @when, @then)
- **pytest**: More Pythonic than JUnit, with powerful fixture system replacing JUnit's setup/teardown

### WebDriver Management

Automated management of browser driver binaries (ChromeDriver, GeckoDriver, etc.).

| Package Name | Version | Purpose | Replaces (Java/Maven) | Notes |
|--------------|---------|---------|----------------------|-------|
| **webdriver-manager** | 4.0.1 | Automatic download and management of browser drivers | webdrivermanager 5.1.0 | Handles ChromeDriver, GeckoDriver, EdgeDriver automatic installation and PATH configuration |

**Source:** `requirements.txt:25-26`, `pyproject.toml:32`, `setup.py:27-28`

**Critical Fix:** GeckoDriverManager URL updated to resolve Mozilla server HTTP 403 errors (documented in Technical Specifications.md).

**Migration Note:** Eliminates need for manual driver downloads or Maven plugins for driver management.

### Test Data Generation

Tools for generating realistic test data (names, emails, addresses, etc.).

| Package Name | Version | Purpose | Replaces (Java/Maven) | Notes |
|--------------|---------|---------|----------------------|-------|
| **Faker** | 20.1.0 | Test data generation with locale support | javafaker 1.0.2 | Generates realistic fake data for test scenarios across multiple locales |

**Source:** `requirements.txt:32-33`, `pyproject.toml:35`, `setup.py:30-31`

**Usage Example:**
```python
from faker import Faker
fake = Faker('en_US')
test_user = {
    'name': fake.name(),
    'email': fake.email(),
    'phone': fake.phone_number()
}
```

### Configuration Management

Dependencies for managing configuration files, environment variables, and test settings.

| Package Name | Version | Purpose | Replaces (Java/Maven) | Notes |
|--------------|---------|---------|----------------------|-------|
| **python-dotenv** | 1.0.0 | Load environment variables from .env files | N/A (Java System.getenv) | Enables environment-specific configuration without code changes |
| **PyYAML** | 6.0.1 | YAML file parsing for config.yaml | snakeyaml (transitive) | Parse structured configuration files with nested settings |

**Source:** `requirements.txt:39-43`, `pyproject.toml:37-39`, `setup.py:33-35`

**Configuration Precedence:** `.env` variables override `config.yaml` values, which override framework defaults.

**Migration Note:** Python's environment variable handling is more straightforward than Java's System.getProperty() pattern.

### Reporting and Visualization

Test report generation in multiple formats (HTML, JSON, XML, Allure).

| Package Name | Version | Purpose | Replaces (Java/Maven) | Notes |
|--------------|---------|---------|----------------------|-------|
| **allure-behave** | 2.13.2 | Allure report generation for Behave tests | reporting-plugin 7.2.0 | Rich HTML reports with test history, trends, and screenshots |
| **allure-pytest** | 2.13.2 | Allure report generation for pytest tests | reporting-plugin 7.2.0 | Unified Allure reporting across both test frameworks |
| **pytest-html** | 4.1.1 | Simple HTML report generation for pytest | maven-surefire-report-plugin | Standalone HTML reports without external dependencies |
| **behave-html-formatter** | 0.9.10 | HTML report formatter for Behave | cucumber-reporting 5.7.0 | Self-contained HTML reports with scenario results |

**Source:** `requirements.txt:49-59`, `pyproject.toml:41-45`, `setup.py:37-40`

**Report Generation Examples:**
```bash
# Allure reports
behave -f allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results

# Behave HTML reports
behave -f behave_html_formatter:HTMLFormatter -o reports/behave-report.html

# pytest HTML reports
pytest --html=reports/pytest-report.html --self-contained-html
```

### Parallel Execution

Dependencies enabling concurrent test execution for faster test suite completion.

| Package Name | Version | Purpose | Replaces (Java/Maven) | Notes |
|--------------|---------|---------|----------------------|-------|
| **pytest-xdist** | 3.5.0 | Distributed testing across multiple processes/machines | maven-surefire-plugin parallel | Thread-safe parallel execution with worker management |

**Source:** `requirements.txt:65-66`, `pyproject.toml:48`, `setup.py:43-44`

**Usage:**
```bash
# Run tests on 4 CPU cores
pytest -n 4

# Auto-detect number of CPUs
pytest -n auto

# Behave parallel execution (requires behave-parallel plugin)
behave --processes 4 --parallel-element feature
```

**Thread Safety:** Framework uses `threading.local()` in DriverManager to ensure each thread has isolated WebDriver instances.

### Code Quality and Linting

Development dependencies for maintaining code quality, formatting, and type safety.

| Package Name | Version | Purpose | Category | Notes |
|--------------|---------|---------|----------|-------|
| **pylint** | 3.0.3 | Python linter for code quality checks | Development | Configurable linting rules in pyproject.toml |
| **black** | 23.12.1 | Opinionated code formatter | Development | Enforces consistent code style (line length: 100) |
| **mypy** | 1.7.1 | Static type checker for Python | Development | Type hint validation and type safety enforcement |
| **isort** | 5.13.0 | Import statement organizer | Development | Sorts imports alphabetically and by category |
| **pytest-cov** | 4.1.0 | Code coverage measurement for pytest | Development | Generates coverage reports in multiple formats |
| **flake8** | 7.0.0 | Style guide enforcement (PEP 8) | Development | Additional style checking beyond pylint |
| **bandit** | 1.7.5 | Security vulnerability scanner | Development | Identifies common security issues in Python code |
| **safety** | 2.3.5 | Dependency vulnerability checker | Development | Scans dependencies for known security vulnerabilities |

**Source:** `requirements.txt:72-79`, `pyproject.toml:53-66`, `setup.py:52-59`

**Development Installation:**
```bash
# Install development dependencies
pip install -e .[dev]

# Or with Poetry:
poetry install --with dev
```

**Code Quality Commands:**
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
pylint pages utilities config features

# Type check
mypy pages utilities config

# Check coverage
pytest --cov=pages --cov=utilities --cov=config --cov-report=html

# Security scan
bandit -r pages utilities config features
safety check
```

### Optional Utilities

Additional utilities that enhance framework capabilities.

| Package Name | Version | Purpose | Replaces (Java/Maven) | Notes |
|--------------|---------|---------|----------------------|-------|
| **selenium-page-factory** | 2.7 | Page Factory pattern support (optional) | PageFactory class in Selenium Java | Not actively used; framework uses property-based locators instead |
| **requests** | 2.31.0 | HTTP library for API testing | RestAssured / Apache HttpClient | Enables API testing alongside UI automation |

**Source:** `requirements.txt:85-90`, `pyproject.toml:51`, `setup.py:46-47`

**Note:** The framework primarily uses property-based element locators (via `@property` decorators) rather than Selenium's PageFactory pattern, providing better Pythonic design.

---

## Version Compatibility Matrix

### Python Version Support

The framework supports Python 3.9 through 3.12, ensuring compatibility with modern Python features while maintaining backward compatibility.

| Python Version | Support Status | Notes |
|----------------|----------------|-------|
| **3.9** | ✅ Fully Supported | Minimum required version |
| **3.10** | ✅ Fully Supported | Recommended for new projects |
| **3.11** | ✅ Fully Supported | Performance improvements |
| **3.12** | ✅ Fully Supported | Latest features and optimizations |
| 3.8 and below | ❌ Not Supported | End of life or incompatible dependencies |

**Source:** `pyproject.toml:17-21`, `setup.py:85`, `pyproject.toml:24`

### Browser Compatibility

Selenium 4.15.2 supports modern browser versions with automatic driver management:

| Browser | Minimum Version | Notes |
|---------|----------------|-------|
| **Chrome** | 90+ | Fully supported with ChromeDriver auto-management |
| **Firefox** | 90+ | Fully supported with GeckoDriver auto-management |
| **Edge** | 90+ | Fully supported with EdgeDriver auto-management |
| **Safari** | 14+ | Supported on macOS only |

### Operating System Compatibility

| OS | Support Status | Notes |
|----|----------------|-------|
| **Linux** | ✅ Fully Supported | Primary CI/CD environment |
| **macOS** | ✅ Fully Supported | Development and Safari testing |
| **Windows** | ✅ Fully Supported | Development environment |

---

## Dependency Upgrade Guidelines

### Upgrade Testing Procedure

Before upgrading any dependency, follow this systematic testing approach:

1. **Create Isolated Environment:**
   ```bash
   # Create new virtual environment for testing
   python -m venv test-upgrade-venv
   source test-upgrade-venv/bin/activate  # or test-upgrade-venv\Scripts\activate on Windows
   ```

2. **Install Upgraded Dependency:**
   ```bash
   # Install new version
   pip install <package>==<new-version>
   
   # Install remaining dependencies
   pip install -r requirements.txt
   ```

3. **Run Full Test Suite:**
   ```bash
   # Run all tests
   behave
   pytest
   
   # Check for deprecation warnings
   pytest -W default
   behave --no-capture --no-logcapture
   ```

4. **Verify Reports Generate:**
   ```bash
   # Test all report formats
   behave -f allure_behave.formatter:AllureFormatter -o allure-results
   behave -f behave_html_formatter:HTMLFormatter -o reports/test.html
   pytest --html=reports/pytest.html
   ```

5. **Run Code Quality Checks:**
   ```bash
   # Ensure code still passes linting
   pylint pages utilities config features
   black --check .
   mypy pages utilities config
   ```

6. **Update Dependency Files:**
   ```bash
   # Update requirements.txt
   pip freeze > requirements-new.txt
   # Review changes and update requirements.txt
   
   # Update pyproject.toml
   poetry update <package>
   
   # Update setup.py
   # Manually edit version in install_requires
   ```

### Semantic Versioning Adherence

Dependencies follow semantic versioning (MAJOR.MINOR.PATCH):

- **PATCH updates (x.y.Z)**: Generally safe, bug fixes only
  - Example: `selenium 4.15.2 → 4.15.3`
  - Action: Update after basic smoke tests

- **MINOR updates (x.Y.z)**: New features, backward compatible
  - Example: `pytest 7.4.3 → 7.5.0`
  - Action: Update after full test suite validation

- **MAJOR updates (X.y.z)**: Breaking changes possible
  - Example: `selenium 4.15.2 → 5.0.0`
  - Action: Thorough testing, code changes may be required

### Compatibility Verification Checklist

Before finalizing any dependency upgrade:

- [ ] All Behave tests pass without errors
- [ ] All pytest tests pass without errors
- [ ] No new deprecation warnings in test output
- [ ] All report formats generate successfully (HTML, JSON, XML, Allure)
- [ ] Parallel execution works without thread safety issues
- [ ] Code quality checks pass (pylint, black, mypy)
- [ ] WebDriver initialization works for all configured browsers
- [ ] Configuration loading works (.env and config.yaml)
- [ ] Screenshot capture works on test failures
- [ ] Documentation still accurate for changed APIs

### Known Upgrade Issues

**Selenium 4.x to 5.x (Future):**
- Major API changes expected
- W3C WebDriver protocol changes
- Action chains API updates
- Wait strategy modifications

**Behave 1.2.x:**
- No major upgrade path currently available
- Behave 2.x not yet released
- Monitor project for future releases

**webdriver-manager:**
- URL changes for driver downloads may require updates
- Browser version detection improvements in newer versions
- GeckoDriver download fix applied in version 4.0.1 (see Technical Specifications)

---

## Migration Notes: Java to Python Dependencies

Complete mapping of Java Maven dependencies to Python pip packages, showing the migration path from the original Java implementation.

| Java/Maven Dependency | Python/pip Equivalent | Version Mapping | Behavioral Notes |
|----------------------|----------------------|-----------------|------------------|
| **selenium-java 3.141.59** | selenium 4.15.2 | 3.x → 4.x (major upgrade) | WebDriver 4.x API changes: deprecated methods removed, improved stability, BiDi protocol support |
| **cucumber-java 7.2.3** | behave 1.2.6 | Direct replacement | Gherkin syntax identical, step definitions use Python decorators instead of annotations |
| **cucumber-junit 7.2.3** | pytest-bdd 6.1.1 | Direct replacement | JUnit runner replaced by pytest with Behave integration |
| **junit 4.13.2** | pytest 7.4.3 | Direct replacement | @Test annotations → test_ function prefix, @Before/@After → pytest fixtures |
| **webdrivermanager 5.1.0** | webdriver-manager 4.0.1 | Direct replacement | Automatic driver management with improved URL handling and version detection |
| **javafaker 1.0.2** | Faker 20.1.0 | Direct replacement | API similar, both support locales and realistic fake data generation |
| **reporting-plugin 7.2.0** | allure-behave 2.13.2, allure-pytest 2.13.2 | Direct replacement | Unified Allure reporting across frameworks with enhanced HTML visualization |
| **cucumber-reporting 5.7.0** | behave-html-formatter 0.9.10 | Direct replacement | Standalone HTML reports without external dependencies |
| **maven-surefire-plugin (parallel)** | pytest-xdist 3.5.0 | Functionality replacement | Process-based parallelism instead of thread-based |
| **snakeyaml (transitive)** | PyYAML 6.0.1 | Direct replacement | YAML parsing with similar API and capabilities |
| **Apache HttpClient** | requests 2.31.0 | Functionality replacement | Simpler API for HTTP requests in API testing scenarios |
| **PageFactory class** | selenium-page-factory 2.7 | Optional replacement | Framework uses property-based locators, PageFactory not actively used |

**Source:** `requirements.txt:2-3`, `pyproject.toml:4`, `setup.py:2-6`

### Key Architectural Transformations

1. **Annotations to Decorators:**
   ```java
   // Java Cucumber
   @Given("^I am on the login page$")
   public void iAmOnLoginPage() { }
   ```
   ```python
   # Python Behave
   @given('I am on the login page')
   def step_impl(context):
       pass
   ```

2. **PageFactory to Property-Based Locators:**
   ```java
   // Java PageFactory
   @FindBy(name = "login")
   private WebElement emailInput;
   ```
   ```python
   # Python Property-Based
   _INPUT_EMAIL = (By.NAME, "login")
   
   @property
   def input_email(self):
       return self.wait_for_element(self._INPUT_EMAIL)
   ```

3. **JUnit to pytest:**
   ```java
   // Java JUnit
   @Before
   public void setUp() { }
   
   @Test
   public void testLogin() { }
   ```
   ```python
   # Python pytest
   @pytest.fixture
   def setup():
       yield
   
   def test_login(setup):
       pass
   ```

---

## Installation Scenarios

### Production Installation

Minimal installation for test execution without development tools:

```bash
# Clone repository
git clone https://github.com/testinium/testinium-qa-python.git
cd testinium-qa-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import selenium, behave, pytest; print('Dependencies installed successfully')"
```

**Source:** `requirements.txt`, `setup.py:18-48`

### Development Installation with Extras

Installation including code quality tools for framework development:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install package in editable mode with dev extras
pip install -e .[dev]

# Or install requirements.txt + manual dev tools
pip install -r requirements.txt
pip install pylint black mypy isort pytest-cov flake8 bandit safety

# Verify dev tools
black --version
pylint --version
mypy --version
```

**Source:** `setup.py:50-61`, `pyproject.toml:53-66`

### Poetry Installation

Installation using Poetry dependency manager:

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Install with development dependencies
poetry install --with dev

# Activate Poetry shell
poetry shell

# Run tests
poetry run behave
poetry run pytest
```

**Source:** `pyproject.toml:1-67`

### Docker Installation

Containerized installation with all dependencies pre-installed:

```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for browser automation
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    chromium \
    chromium-driver \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run tests
CMD ["behave"]
```

```bash
# Build Docker image
docker build -t testinium-qa-python .

# Run tests in container
docker run --rm testinium-qa-python

# Run with volume mount for reports
docker run --rm -v $(pwd)/reports:/app/reports testinium-qa-python
```

### CI/CD Installation

Lightweight installation for CI/CD pipelines:

```bash
# GitHub Actions / GitLab CI / Jenkins
python -m pip install --upgrade pip
pip install -r requirements.txt

# Skip optional dependencies if not needed
pip install selenium behave pytest webdriver-manager allure-behave

# Verify critical dependencies only
python -c "import selenium; import behave; print('CI dependencies ready')"
```

---

## Troubleshooting

### Version Conflict Errors

**Symptom:** `pip install` fails with version conflict messages

**Cause:** Incompatible dependency versions or Python version mismatch

**Solution:**
```bash
# Check Python version (must be 3.9+)
python --version

# Clear pip cache
pip cache purge

# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Install with --no-deps to identify conflicting package
pip install --no-deps -r requirements.txt

# Use Poetry for better dependency resolution
poetry install
```

### Platform-Specific Installation Issues

**Symptom:** Installation fails on Windows with compiler errors

**Cause:** Some packages require C extensions and Visual C++ compiler

**Solution:**
```bash
# Windows: Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Or use pre-built wheels from PyPI (usually automatic)
pip install --only-binary :all: <package-name>

# Upgrade to latest pip which has better wheel support
python -m pip install --upgrade pip
```

**Symptom:** Installation fails on Linux with missing dependencies

**Cause:** System libraries required by some packages not installed

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev build-essential libssl-dev libffi-dev

# CentOS/RHEL
sudo yum install python3-devel gcc openssl-devel libffi-devel

# Retry installation
pip install -r requirements.txt
```

### SSL Certificate Errors

**Symptom:** `SSL: CERTIFICATE_VERIFY_FAILED` during pip install

**Cause:** Corporate proxy or outdated SSL certificates

**Solution:**
```bash
# Update SSL certificates
pip install --upgrade certifi

# Use trusted host (temporary workaround)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Configure pip to use corporate proxy
pip config set global.proxy http://proxy.company.com:8080

# Or use environment variable
export PIP_TRUSTED_HOST="pypi.org files.pythonhosted.org"
pip install -r requirements.txt
```

### WebDriver Installation Issues

**Symptom:** `webdriver-manager` fails to download driver binaries

**Cause:** Network issues, firewall blocking downloads, or GitHub API rate limits

**Solution:**
```bash
# Verify network connectivity
curl -I https://github.com/mozilla/geckodriver/releases

# Use custom cache directory
export WDM_LOCAL=1
export WDM_CACHE_DIR=/path/to/cache

# Manual driver download as fallback
# ChromeDriver: https://chromedriver.chromium.org/downloads
# GeckoDriver: https://github.com/mozilla/geckodriver/releases

# Place drivers in PATH
export PATH=$PATH:/path/to/drivers
```

### Dependency Vulnerability Warnings

**Symptom:** `safety check` or `bandit` reports vulnerabilities

**Cause:** Known security issues in dependencies

**Solution:**
```bash
# Check for vulnerable dependencies
safety check

# Review safety report
safety check --full-report

# Update vulnerable package (if available)
pip install --upgrade <vulnerable-package>

# If no update available, check for alternatives
# Review CVE details and assess risk
# Consider pinning to known-good version temporarily
pip install <package>==<safe-version>
```

### Import Errors After Installation

**Symptom:** `ModuleNotFoundError` despite successful installation

**Cause:** Virtual environment not activated or wrong Python interpreter

**Solution:**
```bash
# Verify virtual environment is activated
which python  # Should point to venv/bin/python

# If not activated
source venv/bin/activate  # Windows: venv\Scripts\activate

# Verify package installed in correct environment
pip list | grep selenium

# Reinstall if package missing
pip install --force-reinstall selenium

# Check Python path
python -c "import sys; print(sys.path)"
```

### Poetry Lock File Issues

**Symptom:** `poetry install` fails with lock file errors

**Cause:** Outdated or corrupted `poetry.lock` file

**Solution:**
```bash
# Update lock file
poetry lock --no-update

# Full lock file regeneration
rm poetry.lock
poetry lock

# Install with updated lock
poetry install

# Verify lock file is in sync
poetry check
```

---

## See Also

- **[Installation Guide](../getting-started/installation.md)** - Detailed installation instructions for different environments
- **[Configuration Options](configuration-options.md)** - Configure dependency behavior (browser types, timeouts, etc.)
- **[Migration Guide](../migration/from-java-cucumber.md)** - Complete Java to Python migration patterns
- **[Troubleshooting Guide](../troubleshooting/installation-issues.md)** - Comprehensive troubleshooting for installation problems
- **[Docker Deployment](../deployment/docker.md)** - Containerized deployment with dependencies pre-installed
- **[CI/CD Integration](../deployment/jenkins-integration.md)** - Dependency installation in CI/CD pipelines

---

**Document Version:** 1.0.0  
**Last Updated:** 2024  
**Framework Version:** 1.0.0
