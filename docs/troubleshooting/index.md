# Troubleshooting Guide

## Overview

Welcome to the comprehensive troubleshooting documentation for the Testinium QA Python test automation framework. This section provides systematic guidance for diagnosing and resolving common issues encountered during framework setup, test execution, and maintenance.

### Purpose

This troubleshooting section is designed to help you:

- **Quickly identify solutions** to common problems through symptom-based navigation
- **Understand root causes** of issues rather than just applying fixes
- **Follow diagnostic workflows** for systematic problem-solving
- **Access detailed guides** for complex troubleshooting scenarios
- **Learn best practices** to prevent future issues

### How to Use This Guide

1. **Start with symptoms:** Use the Quick Reference table below to find the guide matching your issue
2. **Check common errors first:** Review [common-errors.md](common-errors.md) for quick solutions to frequent problems
3. **Follow diagnostic workflow:** Use the systematic troubleshooting process outlined below
4. **Consult specific guides:** Dive deep into category-specific troubleshooting documentation
5. **Enable verbose logging:** Gather detailed diagnostic information when needed
6. **Seek community help:** Use the "Getting Help" section if issues persist

---

## Quick Reference: Symptoms to Solutions

Use this table to quickly navigate to the appropriate troubleshooting guide based on your symptoms:

| Symptom | Likely Category | Troubleshooting Guide |
|---------|----------------|----------------------|
| Python import errors, module not found | Installation | [installation-issues.md](installation-issues.md) |
| Tests won't run, framework not executing | Installation | [installation-issues.md](installation-issues.md) |
| Dependency conflicts, package version errors | Installation | [installation-issues.md](installation-issues.md) |
| Virtual environment issues | Installation | [installation-issues.md](installation-issues.md) |
| Browser not starting, driver not found | WebDriver | [webdriver-issues.md](webdriver-issues.md) |
| SessionNotCreatedException, driver crashes | WebDriver | [webdriver-issues.md](webdriver-issues.md) |
| Browser/driver version mismatch | WebDriver | [webdriver-issues.md](webdriver-issues.md) |
| Headless mode problems | WebDriver | [webdriver-issues.md](webdriver-issues.md) |
| StaleElementReferenceException | WebDriver | [webdriver-issues.md](webdriver-issues.md) |
| Configuration file not loading, YAML errors | Configuration | [configuration-issues.md](configuration-issues.md) |
| Environment variables not recognized | Configuration | [configuration-issues.md](configuration-issues.md) |
| Settings not taking effect, wrong precedence | Configuration | [configuration-issues.md](configuration-issues.md) |
| Test credentials not working | Configuration | [configuration-issues.md](configuration-issues.md) |
| Parallel execution fails, thread conflicts | Parallel Execution | [parallel-execution-issues.md](parallel-execution-issues.md) |
| Driver instances interfering with each other | Parallel Execution | [parallel-execution-issues.md](parallel-execution-issues.md) |
| Resource contention, race conditions | Parallel Execution | [parallel-execution-issues.md](parallel-execution-issues.md) |
| Tests passing serially but failing in parallel | Parallel Execution | [parallel-execution-issues.md](parallel-execution-issues.md) |
| Reports not generated, missing output files | Report Generation | [report-generation-issues.md](report-generation-issues.md) |
| Formatter errors, Allure failures | Report Generation | [report-generation-issues.md](report-generation-issues.md) |
| Screenshots not captured on failure | Report Generation | [report-generation-issues.md](report-generation-issues.md) |
| CI/CD report publishing problems | Report Generation | [report-generation-issues.md](report-generation-issues.md) |
| Specific error messages and stack traces | Common Errors | [common-errors.md](common-errors.md) |

---

## Troubleshooting Guide Index

### 1. Installation Issues

**Guide:** [installation-issues.md](installation-issues.md)

**Covers:**
- **Python version compatibility** - Ensuring Python 3.9-3.12 is correctly installed and configured
- **Dependency conflicts** - Resolving package version incompatibilities and pip installation errors
- **Virtual environment problems** - Creating, activating, and troubleshooting venv/virtualenv issues
- **Platform-specific challenges** - Windows, macOS, and Linux installation variations
- **Module import errors** - Fixing PYTHONPATH and package discovery issues
- **Development tools setup** - Installing optional tools for framework development

**When to use:** Start here if you're having trouble getting the framework installed or if tests won't run due to missing dependencies.

### 2. WebDriver Issues

**Guide:** [webdriver-issues.md](webdriver-issues.md)

**Covers:**
- **Driver not found errors** - Resolving chromedriver, geckodriver path issues (webdriver-manager should handle this automatically)
- **Browser version mismatches** - Ensuring driver version matches installed browser version
- **Headless mode problems** - Troubleshooting Chrome/Firefox headless execution for CI/CD environments
- **Threading issues** - Understanding thread-local driver management with `threading.local()`
- **Critical Firefox driver bug fix** - Documented fix for Firefox WebDriver initialization issue migrated from Java version
- **Browser-specific problems** - Chrome, Firefox, Edge, Safari-specific troubleshooting
- **StaleElementReferenceException** - Understanding property-based locator pattern that prevents this error

**When to use:** If browsers won't start, drivers can't be found, or you're experiencing WebDriver-related exceptions during test execution.

### 3. Configuration Issues

**Guide:** [configuration-issues.md](configuration-issues.md)

**Covers:**
- **YAML parsing errors** - Fixing syntax errors in `config/config.yaml`
- **Environment variable problems** - Setting up `.env` file correctly, variable interpolation issues
- **Configuration precedence** - Understanding `.env` > `config.yaml` > defaults resolution order
- **Missing configuration files** - Creating required config files from templates
- **Invalid configuration values** - Validating browser types, timeout values, URL formats
- **Credentials management** - Securely configuring test user credentials for different environments
- **behave.ini and pytest.ini** - Troubleshooting framework configuration files

**When to use:** If configuration values aren't being recognized, files aren't loading, or settings aren't taking effect as expected.

### 4. Parallel Execution Issues

**Guide:** [parallel-execution-issues.md](parallel-execution-issues.md)

**Covers:**
- **Thread-safety with threading.local()** - Understanding the framework's thread-local WebDriver pattern for safe parallel execution
- **Driver instance conflicts** - Preventing WebDriver instances from interfering across parallel tests
- **Resource contention** - Managing shared resources (files, network, test data) in parallel scenarios
- **behave-parallel vs pytest-xdist** - Choosing and configuring the right parallelization tool
- **Thread pool configuration** - Tuning worker count for optimal performance
- **Test isolation** - Ensuring tests don't have dependencies or shared state issues
- **Debugging parallel failures** - Techniques for diagnosing race conditions and timing issues

**When to use:** If tests pass when run serially but fail in parallel, or experiencing concurrency-related errors.

### 5. Report Generation Issues

**Guide:** [report-generation-issues.md](report-generation-issues.md)

**Covers:**
- **Formatter errors** - Troubleshooting behave HTML formatter, JUnit XML, JSON output issues
- **Missing report files** - Ensuring report directories exist and have correct permissions
- **Allure reporting problems** - Allure-behave integration, generating and serving Allure reports
- **Screenshot capture failures** - Debugging automatic screenshot-on-failure functionality in `environment.py`
- **CI/CD report publishing** - Publishing reports to Jenkins, GitHub Actions, GitLab CI, cloud storage
- **Custom reporter integration** - Troubleshooting custom Behave formatters
- **Report artifacts in Docker** - Preserving reports from containerized test execution

**When to use:** If reports aren't being generated, screenshots aren't captured, or report publishing to CI/CD fails.

### 6. Common Errors Reference

**Guide:** [common-errors.md](common-errors.md)

**Covers:**
- **Comprehensive error message catalog** - Detailed listing of frequent error messages with explanations
- **Root cause analysis** - Why each error occurs and what triggers it
- **Step-by-step solutions** - Exact commands and fixes for each error
- **Prevention strategies** - How to avoid each error in the future
- **Related issues** - Links to similar problems and broader troubleshooting guides
- **Examples from README** - Expanded coverage of the 8 common issues in README.md lines 606-684

**When to use:** When you encounter a specific error message and need an immediate solution - check here first.

---

## Diagnostic Workflow

Follow this systematic troubleshooting process for efficient problem resolution:

### Step 1: Identify Error Category

Determine which category your issue falls into:

```
Is the framework installed and importable?
├─ NO  → Installation Issues
└─ YES → Continue to Step 2

Can you start a browser manually via Python?
├─ NO  → WebDriver Issues  
└─ YES → Continue to Step 3

Are configuration files loaded correctly?
├─ NO  → Configuration Issues
└─ YES → Continue to Step 4

Are you running tests in parallel?
├─ YES → Check parallel-specific issues
└─ NO  → Continue to Step 5

Are reports being generated?
├─ NO  → Report Generation Issues
└─ YES → Check Common Errors for specific messages
```

### Step 2: Consult Quick Solutions

Before diving deep, check these quick-win resources:

1. **Check [common-errors.md](common-errors.md)** - Many issues have documented solutions
2. **Review README.md Troubleshooting** - 8 common issues covered in [README.md lines 602-715](../../README.md#troubleshooting)
3. **Verify basic setup** - Python version, virtual environment activated, dependencies installed

### Step 3: Deep Dive into Specific Guide

Navigate to the appropriate category-specific troubleshooting guide:

- Installation problems → [installation-issues.md](installation-issues.md)
- Browser/driver problems → [webdriver-issues.md](webdriver-issues.md)
- Configuration problems → [configuration-issues.md](configuration-issues.md)
- Parallel execution problems → [parallel-execution-issues.md](parallel-execution-issues.md)
- Reporting problems → [report-generation-issues.md](report-generation-issues.md)

### Step 4: Enable Verbose Logging

Gather detailed diagnostic information:

```bash
# Enable Behave verbose output
behave --verbose --no-capture

# Enable Python debug logging
export LOG_LEVEL=DEBUG
behave

# Enable WebDriver logging (add to driver_manager.py temporarily)
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--v=1')
```

### Step 5: Verify Environment Setup

Confirm your environment is correctly configured:

```bash
# Check Python version (should be 3.9-3.12)
python --version

# Verify virtual environment is activated
which python  # Should show path in venv directory

# Confirm dependencies are installed
pip list | grep -E "(selenium|behave|pytest)"

# Validate configuration files exist
ls -la config/config.yaml .env

# Test basic framework imports
python -c "from utilities.driver_manager import DriverManager; print('OK')"
```

### Step 6: Create Minimal Reproducible Case

Isolate the problem:

```bash
# Run single scenario to reproduce issue
behave features/Login.feature:15

# Run with dry-run to check step definitions
behave --dry-run --no-summary

# Test specific feature file only
behave features/Login.feature
```

### Step 7: Gather Diagnostic Information

Collect information for further investigation or support:

- **Error messages:** Full stack trace including line numbers
- **Environment:** Python version, OS, browser versions
- **Configuration:** Relevant config.yaml and .env settings (redact credentials)
- **Logs:** Output from verbose mode execution
- **Test output:** Screenshots captured on failure (if applicable)
- **Reproducibility:** Steps to consistently reproduce the issue

---

## General Troubleshooting Tips

### Essential Checks (Do These First)

1. **Verify README first:** Check [README.md Troubleshooting section](../../README.md#troubleshooting) for basic issues (lines 602-715)

2. **Activate virtual environment:**
   ```bash
   # On macOS/Linux
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   
   # Verify activation (prompt should show (venv))
   which python
   ```

3. **Install/update dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or if using Poetry
   poetry install
   ```

4. **Check Python version compatibility:**
   ```bash
   python --version
   # Must be 3.9.x, 3.10.x, 3.11.x, or 3.12.x
   ```

5. **Review framework logs:**
   ```bash
   # Behave logs
   cat logs/behave.log
   
   # Check screenshot directory for failure screenshots
   ls -lt reports/screenshots/
   ```

### Best Practices

1. **Test in isolation before parallel execution** - Always verify tests pass serially before running in parallel
2. **Use explicit waits consistently** - The framework provides wait helpers; avoid `time.sleep()`
3. **Keep browsers updated** - Browser/driver mismatches are a common source of issues
4. **Validate configuration after changes** - Test config loading with a simple scenario after modifications
5. **Use property-based locators** - Framework's property pattern prevents StaleElementReference errors
6. **Check thread-local driver pattern** - `threading.local()` in DriverManager ensures thread safety

### Configuration Validation

```bash
# Quick configuration test
python -c "from config.test_config import get_config; c = get_config(); print(f'Browser: {c.browser.type}, URL: {c.application.base_url}')"

# Verify environment variables loaded
python -c "import os; print('BASE_URL:', os.getenv('BASE_URL', 'NOT SET'))"

# Test YAML parsing
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

### Common Anti-Patterns to Avoid

❌ **Don't:** Run tests without activating virtual environment  
✅ **Do:** Always activate venv before running tests

❌ **Don't:** Use hardcoded `time.sleep()` for waits  
✅ **Do:** Use WaitHelpers or BasePage wait methods

❌ **Don't:** Run parallel tests without understanding thread safety  
✅ **Do:** Review parallel execution guide first

❌ **Don't:** Modify framework source code for quick fixes  
✅ **Do:** Use configuration and extension patterns

❌ **Don't:** Ignore deprecation warnings  
✅ **Do:** Update deprecated patterns proactively

---

## Getting Help

### Before Asking for Help

Ensure you've completed these steps:

1. ✅ Checked [common-errors.md](common-errors.md) for your specific error message
2. ✅ Reviewed the relevant category-specific troubleshooting guide
3. ✅ Followed the diagnostic workflow above
4. ✅ Collected diagnostic information (error messages, environment details, logs)
5. ✅ Created a minimal reproducible test case
6. ✅ Verified the issue isn't covered in README.md troubleshooting section

### Reporting Issues

When reporting bugs or requesting help:

**Include This Information:**

```
**Environment:**
- Python version: (python --version)
- OS: (e.g., Ubuntu 22.04, macOS 13.1, Windows 11)
- Browser: (e.g., Chrome 120.0.6099.71)
- Framework version: (git rev-parse HEAD)

**Issue Description:**
Clear description of what you expected vs. what happened

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Error Messages:**
```
[Paste full stack trace here]
```

**Configuration:**
- config.yaml browser type: 
- Headless mode: 
- Any custom configuration:

**Attempted Solutions:**
What troubleshooting steps you've already tried
```

### Where to Report

- **Bug Reports:** Create GitHub issue with `bug` label (use `.github/ISSUE_TEMPLATE/bug_report.md` template)
- **Feature Requests:** Create GitHub issue with `enhancement` label
- **Questions:** Check documentation first, then create GitHub discussion
- **Security Issues:** Report privately to repository maintainers (see SECURITY.md if available)

### Community Resources

- **Documentation:** [Full framework documentation](../index.md)
- **README:** [Quick reference and basic troubleshooting](../../README.md)
- **API Reference:** [API documentation for framework internals](../api-reference/index.md)
- **Architecture:** [System architecture and design patterns](../architecture/index.md)
- **Contributing:** [Development guidelines](../contributing/index.md)

---

## Cross-References

### Related Documentation

- **[Getting Started Guide](../getting-started/index.md)** - Initial setup and installation procedures
- **[Configuration Guide](../guides/configuration-management.md)** - Understanding configuration hierarchy and precedence
- **[Parallel Execution Guide](../guides/parallel-execution.md)** - Best practices for running tests in parallel
- **[API Reference](../api-reference/index.md)** - Understanding framework internals for deep troubleshooting
- **[Architecture Documentation](../architecture/index.md)** - Design patterns and architectural decisions

### README Troubleshooting Section

The main README.md contains a comprehensive troubleshooting section covering 8 common issues:

**Source:** [README.md lines 602-715](../../README.md#troubleshooting)

**Issues Covered:**
1. Module Not Found Error
2. WebDriver Not Found
3. Undefined Step Definitions
4. Import Errors in Python
5. Browser Not Starting
6. Stale Element Reference
7. Tests Failing in CI but Passing Locally
8. Screenshot Not Captured on Failure

**Plus debugging tips for:**
- Verbose output
- Running specific scenarios
- Checking step definitions
- Python debugger usage
- WebDriver log viewing

### Quick Navigation

| Documentation Section | Purpose | Link |
|----------------------|---------|------|
| Installation Issues | Setup and dependency problems | [installation-issues.md](installation-issues.md) |
| WebDriver Issues | Browser and driver problems | [webdriver-issues.md](webdriver-issues.md) |
| Configuration Issues | Config loading and precedence | [configuration-issues.md](configuration-issues.md) |
| Parallel Execution Issues | Threading and concurrency | [parallel-execution-issues.md](parallel-execution-issues.md) |
| Report Generation Issues | Reporting and screenshots | [report-generation-issues.md](report-generation-issues.md) |
| Common Errors | Specific error messages | [common-errors.md](common-errors.md) |

---

## Troubleshooting Quick Checklist

Use this checklist when encountering issues:

### Pre-Execution Checklist

- [ ] Python 3.9-3.12 installed and accessible
- [ ] Virtual environment created and activated (prompt shows `(venv)`)
- [ ] All dependencies installed via `pip install -r requirements.txt`
- [ ] Configuration files exist (`config/config.yaml`, `.env`)
- [ ] Test credentials configured in `.env` file
- [ ] Project run from repository root directory
- [ ] `PYTHONPATH` includes project root (usually automatic)

### Execution Checklist

- [ ] Can import framework modules: `python -c "from utilities import DriverManager"`
- [ ] Configuration loads successfully: `python -c "from config import get_config; get_config()"`
- [ ] Behave can discover features: `behave --dry-run --no-summary`
- [ ] WebDriver can initialize: Run simple test scenario
- [ ] Screenshots directory exists: `mkdir -p reports/screenshots`
- [ ] Appropriate browser installed and updated

### Parallel Execution Checklist

- [ ] Tests pass serially first
- [ ] Understand thread-local driver pattern (`threading.local()`)
- [ ] No shared state between tests
- [ ] Configured appropriate worker count
- [ ] Resource contention considered
- [ ] Reviewed [parallel-execution-issues.md](parallel-execution-issues.md)

### Reporting Issues Checklist

- [ ] Error message and full stack trace captured
- [ ] Environment details documented (Python, OS, browser versions)
- [ ] Minimal reproducible example created
- [ ] Checked [common-errors.md](common-errors.md) first
- [ ] Reviewed relevant troubleshooting guide
- [ ] Attempted diagnostic workflow steps
- [ ] Configuration details ready (with credentials redacted)

---

## Summary

This troubleshooting section provides comprehensive problem-solving resources for the Testinium QA Python test automation framework. Whether you're facing installation challenges, WebDriver issues, configuration problems, parallel execution difficulties, or reporting failures, you'll find systematic guidance and solutions here.

**Key Principles:**
- **Start with quick reference** - Find your symptom and navigate directly to solutions
- **Follow diagnostic workflow** - Systematic approach saves time
- **Consult specific guides** - Deep dives into each problem category
- **Enable logging** - Gather information for effective troubleshooting
- **Verify basics first** - Python version, venv activation, dependency installation
- **Seek help properly** - Provide complete diagnostic information when reporting issues

**Next Steps:**
1. Use the [Quick Reference table](#quick-reference-symptoms-to-solutions) to find your issue
2. Consult the appropriate category-specific guide
3. Follow the [Diagnostic Workflow](#diagnostic-workflow) for systematic resolution
4. Check [Getting Help](#getting-help) if issues persist

For immediate assistance with common problems, start with [common-errors.md](common-errors.md) or the [README.md Troubleshooting section](../../README.md#troubleshooting).

---

**Documentation Version:** 1.0.0  
**Last Updated:** 2024  
**Framework Version:** Python 3.9+ | Selenium 4.x | Behave 1.2.6+

**Source References:**
- README.md lines 602-715 (Troubleshooting section)
- blitzy/documentation/Project Guide.md (Framework architecture)
- blitzy/documentation/Technical Specifications.md (Migration context)
