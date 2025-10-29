# Quick Start Guide

Get up and running with the Testinium QA Python test automation framework in just 5 minutes. This guide provides the fastest path to executing your first BDD test.

## What You'll Learn

By following this quick start guide, you'll:

- Set up the framework in under 5 minutes
- Run your first automated test
- View the generated test report
- Understand next steps for deeper exploration

## Prerequisites Check

Before you begin, verify you have the following installed:

**Required:**

- **Python 3.9 or higher** - Check with `python3 --version` or `python --version`
- **pip** - Python's package manager (included with Python 3.9+)
- **git** - Version control system for cloning the repository

**Quick Verification:**

```bash
# Verify Python version (should show 3.9 or higher)
python3 --version

# Verify pip is available
pip --version

# Verify git is installed
git --version
```

If any of these commands fail, please install the missing tools before continuing.

## Quick Setup

### 1. Clone the Repository

Clone the Testinium QA framework to your local machine:

```bash
git clone https://github.com/BalamiRR/Testinium-QA.git
cd Testinium-QA
```

### 2. Create Virtual Environment

Create an isolated Python environment for the framework:

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

**Success Indicator:** Your terminal prompt should now show `(venv)` prefix.

### 3. Install Dependencies

Install all required Python packages:

```bash
# Install all framework dependencies
pip install -r requirements.txt
```

This command installs Selenium, Behave, pytest, and all other required packages. The installation typically takes 1-2 minutes.

## Quick Configuration

### Set Up Environment Variables

Copy the example environment file to create your configuration:

```bash
# Copy environment template
cp .env.example .env
```

**Note:** The default `.env` settings work out of the box for local testing. The framework will use sensible defaults from `config/config.yaml` for any missing values.

**Optional:** Edit `.env` to customize test user credentials or base URL if testing against a different environment.

## Run Your First Test

Execute a simple login test to verify everything is working:

```bash
# Run the login feature test
behave features/Login.feature --tags=@Login
```

### What Happens During Execution

1. **Browser Launch:** A Chrome browser window opens automatically
2. **Test Execution:** The test navigates to the login page and performs authentication
3. **Reporting:** Test results are captured in multiple formats
4. **Screenshots:** Failure screenshots are automatically captured (if any test fails)

### Expected Output

You should see output similar to:

```
Feature: Testinium app login feature

  Background:
    Given User is on the Testinium login page ... passed

  Scenario: Users log in with valid credentials
    When User enters "salesmanager7@info.com" username ... passed
    And User enters "salesmanager" password ... passed
    And User clicks the login button ... passed
    Then User should see the dashboard ... passed

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
5 steps passed, 0 failed, 0 skipped, 0 undefined
```

**Success Indicators:**

- ✅ All steps show `passed` status
- ✅ Browser opened and navigated to the application
- ✅ Test completed without errors

## View Results

### Test Reports

Your test execution generated multiple report formats:

**HTML Report:**

```bash
# Open the HTML report in your default browser
open reports/report.html        # macOS
xdg-open reports/report.html    # Linux
start reports/report.html       # Windows
```

The HTML report includes:

- Test execution summary (passed/failed/skipped)
- Detailed scenario steps with timing
- Screenshots for any failed tests
- Browser and environment information

**Report Locations:**

- HTML Report: `reports/report.html`
- JSON Report: `reports/cucumber.json`
- Screenshots: `reports/screenshots/`

## What's Next?

Now that you've successfully run your first test, explore these resources to deepen your understanding:

### Essential Next Steps

1. **[Detailed Installation Guide](installation.md)** - Set up the framework for production use with advanced configuration
2. **[Configuration Guide](configuration.md)** - Customize browser settings, timeouts, and test data
3. **[First Test Walkthrough](first-test.md)** - Understand what happened during your test execution and how the framework works

### Learn More

4. **[Authentication Testing Guide](../guides/authentication-testing.md)** - Deep dive into login/logout test scenarios
5. **[Page Object Model Guide](../guides/page-object-model.md)** - Learn how to create new page objects
6. **[Step Definitions Guide](../guides/step-definitions.md)** - Write custom Behave step definitions
7. **[Parallel Execution Guide](../guides/parallel-execution.md)** - Run tests faster with parallel execution

### Advanced Topics

8. **[API Reference](../api-reference/index.md)** - Complete framework API documentation
9. **[Deployment Guides](../deployment/index.md)** - Deploy to Jenkins, GitHub Actions, Docker, or cloud platforms
10. **[Architecture Overview](../architecture/system-overview.md)** - Understand framework internals and design patterns

## Troubleshooting

### Quick Fixes for Common Issues

**Issue: "ModuleNotFoundError: No module named 'selenium'"**

```bash
# Solution: Activate virtual environment and reinstall dependencies
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

**Issue: "WebDriver executable not found"**

No action needed! The framework uses `webdriver-manager` which automatically downloads and manages browser drivers. Ensure you have Chrome or Firefox installed and updated.

**Issue: "Undefined step" error during test execution**

```bash
# Solution: Verify step definitions exist and run from project root
behave --dry-run  # Check for undefined steps
```

**Issue: Tests pass locally but fail with "command not found: behave"**

```bash
# Solution: Virtual environment not activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

For more comprehensive troubleshooting, see the [Troubleshooting Guide](../troubleshooting/index.md).

## Summary

Congratulations! You've successfully:

✅ Set up the Testinium QA Python framework  
✅ Executed your first BDD test  
✅ Viewed the test execution report  
✅ Learned where to find additional resources

**Time Invested:** ~5 minutes  
**Ready for:** Writing your own test scenarios

---

**Source References:**
- Repository: [Testinium-QA on GitHub](https://github.com/BalamiRR/Testinium-QA)
- Detailed Setup: `README.md` lines 62-136
- Test Execution: `README.md` lines 139-161

**Need Help?** Open an issue on the [GitHub repository](https://github.com/BalamiRR/Testinium-QA/issues) or consult the [full documentation](../index.md).
