# Report Generation Issues

Comprehensive troubleshooting guide for resolving report generation failures, formatter errors, missing reports, and CI/CD publishing issues in the Testinium QA Python test automation framework.

## Overview

The test automation framework supports multiple report formats including HTML, JSON, JUnit XML, Allure, and custom Behave formatters. This guide addresses common issues encountered during report generation, configuration problems, and deployment challenges.

**Report Formats Supported:**
- **Behave Pretty Format:** Default console output with scenario results
- **HTML Reports:** Human-readable reports via behave-html-formatter
- **JSON Reports:** Machine-readable cucumber.json for CI/CD integration
- **JUnit XML:** Jenkins and CI/CD compatible test results
- **Allure Reports:** Enhanced interactive HTML reports with detailed test execution data
- **Rerun Format:** Failed test tracking for selective re-execution

## Prerequisites

Before troubleshooting report generation issues, verify:

- Behave framework installed: `pip show behave` (version 1.2.6)
- Report formatters installed: `pip list | grep -E "allure|behave-html"`
- Reports directory exists: `mkdir -p reports/{behave-reports,junit,allure-results,screenshots}`
- behave.ini configuration present in project root
- Proper file system permissions for writing reports

## 1. Formatter Errors

### Issue: Invalid Format Specified in behave.ini

**Symptoms:**
```
ERROR: Unknown format 'html'. Available formats: json, plain, pretty, progress, ...
```

**Cause:**
The `format` option in behave.ini specifies a formatter that is not installed or uses incorrect syntax.

**Source Reference:** `behave.ini:20`

```ini
# Incorrect configuration in behave.ini
format = html  # ERROR: 'html' is not a valid Behave format name
```

**Solution:**

Use the correct formatter module path for HTML reports:

```bash
# Command line (recommended approach)
behave --format=behave_html_formatter:HTMLFormatter --outfile=reports/report.html
```

Or update `behave.ini`:

```ini
# Correct configuration - use pretty format as default
format = pretty

# HTML reports should be generated via command line:
# behave -f behave_html_formatter:HTMLFormatter -o reports/report.html
```

**Available Built-in Formats:**
- `pretty` - Default formatted console output
- `json` - JSON report output
- `plain` - Simple text output
- `progress` - Progress bar display
- `rerun` - Failed scenario tracking
- `junit` - JUnit XML (via --junit flag, not --format)

**Diagnostic Command:**
```bash
# List all available formatters
behave --format=help
```

### Issue: Formatter Not Installed

**Symptoms:**
```
ModuleNotFoundError: No module named 'allure_behave'
ModuleNotFoundError: No module named 'behave_html_formatter'
```

**Cause:**
Report formatter package is not installed in the Python environment.

**Solution:**

Install required formatter packages:

```bash
# Install Allure formatter
pip install allure-behave==2.13.2

# Install HTML formatter
pip install behave-html-formatter==0.9.10

# Verify installation
pip list | grep -E "allure-behave|behave-html-formatter"
```

**For CI/CD environments**, add to `requirements.txt`:

```
allure-behave==2.13.2
behave-html-formatter==0.9.10
```

**Diagnostic Command:**
```bash
# Check if formatter modules are importable
python -c "import allure_behave; print('Allure formatter OK')"
python -c "import behave_html_formatter; print('HTML formatter OK')"
```

### Issue: Format String Syntax Errors

**Symptoms:**
```
behave.formatter.bad_format: Bad format: allure_behave.formatter.AllureFormatter
```

**Cause:**
Incorrect syntax for specifying custom formatter module path.

**Correct Syntax:**

```bash
# Correct format specification (colon separator)
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results

# Incorrect (dot separator instead of colon before class name)
behave --format=allure_behave.formatter.AllureFormatter  # ERROR
```

**Source Reference:** `behave.ini:24,147`

### Issue: Multiple Format Conflicts

**Symptoms:**
- Only one report generated when multiple formats specified
- Reports overwriting each other
- Conflicting output paths

**Cause:**
Improper syntax for multiple formatter configuration or conflicting `--outfile` options.

**Solution:**

Use proper multi-formatter syntax with separate output paths:

```bash
# Correct: Multiple formatters with distinct output files
behave \
  --format=pretty \
  --format=json --outfile=reports/cucumber.json \
  --format=behave_html_formatter:HTMLFormatter --outfile=reports/report.html
```

**Source Reference:** `README.md:476`

**Common Mistake:**
```bash
# WRONG: Multiple --outfile without corresponding --format
behave --format=json --outfile=file1.json --outfile=file2.html  # Only file2.html created
```

## 2. Missing Reports

### Issue: Reports Directory Not Created

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'reports/cucumber.json'
IOError: [Errno 2] No such file or directory: 'reports/allure-results'
```

**Cause:**
The reports output directory does not exist, and Behave does not automatically create nested directories.

**Solution:**

Create reports directory structure before test execution:

```bash
# Create all required report directories
mkdir -p reports/behave-reports
mkdir -p reports/junit
mkdir -p reports/allure-results
mkdir -p reports/screenshots

# Verify directory creation
ls -la reports/
```

**For CI/CD pipelines**, add to build script:

```bash
# Jenkins/GitLab CI/GitHub Actions
- name: Setup report directories
  run: |
    mkdir -p reports/{behave-reports,junit,allure-results,screenshots}
    chmod -R 755 reports/
```

**Source Reference:** `behave.ini:82,86`

**Diagnostic Command:**
```bash
# Check directory existence and permissions
test -d reports/allure-results && echo "Directory exists" || echo "Directory missing"
test -w reports/allure-results && echo "Writable" || echo "Permission denied"
```

### Issue: Permission Issues Writing Reports

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: 'reports/cucumber.json'
OSError: [Errno 30] Read-only file system: 'reports/allure-results'
```

**Cause:**
Insufficient file system permissions for report output directory, common in containerized environments.

**Solution:**

**For local development:**
```bash
# Grant write permissions to reports directory
chmod -R 755 reports/

# Verify permissions
ls -ld reports/
# Expected: drwxr-xr-x (755)
```

**For Docker containers:**
```dockerfile
# In Dockerfile, ensure reports directory has correct permissions
RUN mkdir -p /app/reports && chmod -R 777 /app/reports
```

**For Jenkins:**
```groovy
// Ensure workspace has write permissions
sh 'chmod -R 755 ${WORKSPACE}/reports'
```

**Diagnostic Command:**
```bash
# Check file system permissions
stat -c "%a %U:%G %n" reports/
# Expected: 755 user:group reports/

# Test write capability
touch reports/test.txt && rm reports/test.txt && echo "Writable" || echo "Not writable"
```

### Issue: Wrong Output Path Specified

**Symptoms:**
- Reports generated in unexpected locations
- Cannot find generated report files
- Reports not archived in CI/CD

**Cause:**
Relative path resolution or incorrect `--outfile` path specified.

**Solution:**

Always use paths relative to project root:

```bash
# Correct: Relative to project root
behave --format=json --outfile=reports/cucumber.json

# Avoid: Absolute paths (not portable)
behave --format=json --outfile=/tmp/reports/cucumber.json
```

**Source Reference:** `behave.ini:26-32`

**Diagnostic Command:**
```bash
# Find all generated report files
find . -name "*.json" -o -name "*.html" -o -name "*.xml" | grep -v node_modules

# Check current working directory
pwd
# Expected: /path/to/testinium-qa-python
```

### Issue: --outfile Flag Missing

**Symptoms:**
- JSON/HTML report content printed to console instead of file
- No report file generated despite using --format

**Cause:**
The `--outfile` (or `-o`) flag is required for file-based formatters but was omitted.

**Incorrect:**
```bash
# Missing --outfile: Report content printed to stdout
behave --format=json
```

**Correct:**
```bash
# Specify output file
behave --format=json --outfile=reports/cucumber.json

# Short form
behave -f json -o reports/cucumber.json
```

**Source Reference:** `README.md:483`

## 3. HTML Report Issues

### Issue: behave-html-formatter Not Generating

**Symptoms:**
- No HTML report file created despite successful test execution
- Empty HTML file generated
- HTML formatter errors in console

**Cause:**
Incorrect formatter module path or missing dependency.

**Solution:**

1. **Verify installation:**
```bash
pip show behave-html-formatter
# Expected: Version 0.9.10 or compatible
```

2. **Use correct formatter syntax:**
```bash
# Correct HTML formatter invocation
behave --format=behave_html_formatter:HTMLFormatter --outfile=reports/report.html
```

3. **Check for formatter errors:**
```bash
# Run with verbose output to see formatter errors
behave --format=behave_html_formatter:HTMLFormatter --outfile=reports/report.html --verbose
```

**Source Reference:** `behave.ini:148`

**Diagnostic Command:**
```bash
# Test formatter import
python -c "from behave_html_formatter import HTMLFormatter; print('Import successful')"
```

### Issue: CSS/JS Assets Missing

**Symptoms:**
- HTML report displays but lacks formatting
- Blank white page with no styles
- JavaScript functionality not working

**Cause:**
HTML formatter generates self-contained HTML but CDN resources may fail to load if offline or blocked.

**Solution:**

The `behave-html-formatter` generates self-contained HTML with embedded CSS/JS. If styles are missing:

1. **Check HTML file integrity:**
```bash
# Verify HTML file is not empty
ls -lh reports/report.html
# Should be > 100KB for valid report

# Check for HTML content
head -20 reports/report.html
# Should see <!DOCTYPE html> and <html> tags
```

2. **Open in different browser:**
```bash
# Some browsers block inline styles - try another
firefox reports/report.html
google-chrome reports/report.html
```

3. **Check network access (if using CDN):**
```bash
# Verify internet connectivity for CDN resources
curl -I https://cdn.jsdelivr.net/
```

### Issue: Report Corruption

**Symptoms:**
```
XML Parsing Error: not well-formed
SyntaxError: Unexpected end of JSON input (in HTML report viewing)
```

**Cause:**
Incomplete write operation, concurrent file access, or test interruption during report generation.

**Solution:**

1. **Avoid interrupting test execution:**
   - Let all tests complete before stopping execution
   - Use proper signals for graceful shutdown

2. **Ensure single-threaded formatter access:**
   - When running parallel tests, use separate output files per worker
   - Aggregate reports after all workers complete

3. **Validate report integrity:**
```bash
# Check file is not truncated
tail -10 reports/report.html
# Should see </html> closing tag

# Check file size is reasonable
ls -lh reports/report.html
# Empty or very small file indicates corruption
```

### Issue: Encoding Issues with Special Characters

**Symptoms:**
- Garbled text in HTML reports
- Special characters displayed as �
- Unicode decode errors

**Cause:**
Character encoding mismatch between test output and report generation.

**Solution:**

Ensure UTF-8 encoding throughout:

1. **Set Python environment encoding:**
```bash
# Add to environment or CI/CD configuration
export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
```

2. **Specify encoding in behave execution:**
```bash
# Ensure UTF-8 handling
LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 behave
```

3. **Check HTML meta charset:**
```bash
# Verify HTML has proper charset declaration
grep -i "charset" reports/report.html
# Should see: <meta charset="UTF-8">
```

## 4. JSON Report Issues

### Issue: Invalid JSON Structure

**Symptoms:**
```json
JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

**Cause:**
Malformed JSON output from Behave or test interruption during JSON generation.

**Solution:**

1. **Validate JSON structure:**
```bash
# Use jq to validate and pretty-print JSON
jq . reports/cucumber.json
# If valid, outputs formatted JSON

# Alternative: Python validation
python -m json.tool reports/cucumber.json
```

2. **Regenerate JSON report:**
```bash
# Clean and regenerate
rm -f reports/cucumber.json
behave --format=json --outfile=reports/cucumber.json
```

**Source Reference:** `README.md:483`

**Diagnostic Command:**
```bash
# Check for common JSON syntax errors
cat reports/cucumber.json | python -c "import sys, json; json.load(sys.stdin); print('Valid JSON')"
```

### Issue: cucumber.json Not Parseable by CI Tools

**Symptoms:**
- Jenkins cannot parse cucumber.json
- CI/CD pipeline fails to display test results
- "Invalid Cucumber JSON" errors in CI logs

**Cause:**
JSON format incompatibility or missing required fields for Cucumber JSON schema.

**Solution:**

Ensure proper JSON format specification:

```bash
# Generate Cucumber-compatible JSON
behave --format=json --outfile=reports/cucumber.json

# Verify JSON contains required Cucumber fields
jq '.[0] | keys' reports/cucumber.json
# Expected: ["elements", "id", "keyword", "name", "tags", "uri"]
```

**For Jenkins Cucumber Reports Plugin:**

```groovy
// Jenkinsfile configuration
cucumber buildStatus: 'UNSTABLE',
         fileIncludePattern: 'reports/cucumber.json',
         trendsLimit: 10,
         classifications: [
             [key: 'Browser', value: 'Chrome']
         ]
```

**Diagnostic Command:**
```bash
# Verify JSON schema compliance
jq 'if type == "array" then "Valid Cucumber JSON array" else "Invalid structure" end' reports/cucumber.json
```

### Issue: JSON Formatting with --format=json --outfile Syntax

**Symptoms:**
- Multiple JSON formatters creating confusion
- JSON output not properly formatted

**Solution:**

Use correct syntax per README.md documentation:

```bash
# Single JSON output (recommended)
behave --format=json --outfile=reports/cucumber.json

# Multiple outputs (JSON + pretty console)
behave --format=json --outfile=reports/cucumber.json --format=pretty
```

**Source Reference:** `README.md:476-477`

## 5. Allure Report Issues

### Issue: allure-behave Formatter Configuration

**Symptoms:**
```
ModuleNotFoundError: No module named 'allure_behave'
AttributeError: module 'allure_behave' has no attribute 'formatter'
```

**Cause:**
Missing or incorrectly configured allure-behave package.

**Solution:**

1. **Install allure-behave:**
```bash
pip install allure-behave==2.13.2

# Verify installation
pip show allure-behave
```

2. **Use correct formatter path:**
```bash
# Correct Allure formatter specification
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results
```

**Source Reference:** `README.md:497`, `behave.ini:77-82`

**Configuration in behave.ini:**
```ini
[behave.userdata]
allure_results_dir = reports/allure-results
```

**Diagnostic Command:**
```bash
# Test Allure formatter import
python -c "from allure_behave.formatter import AllureFormatter; print('Allure formatter OK')"
```

### Issue: allure Command Not Found

**Symptoms:**
```bash
$ allure serve reports/allure-results
bash: allure: command not found
```

**Cause:**
Allure command-line tool not installed. Note that `allure-behave` (Python package) is separate from `allure` CLI tool.

**Solution:**

Install Allure CLI tool:

**Option 1: Manual installation (recommended for local development)**
```bash
# Download from Allure GitHub releases
# https://github.com/allure-framework/allure2/releases

# Extract and add to PATH
export PATH=$PATH:/path/to/allure/bin

# Verify installation
allure --version
# Expected: 2.24.0 or higher
```

**Option 2: Package manager installation**
```bash
# macOS (Homebrew)
brew install allure

# Linux (manual download)
curl -o allure-2.24.0.tgz -Ls https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.tgz
tar -zxf allure-2.24.0.tgz
sudo mv allure-2.24.0 /opt/allure
sudo ln -s /opt/allure/bin/allure /usr/local/bin/allure

# Windows (Scoop)
scoop install allure
```

**Source Reference:** `README.md:500`

### Issue: allure-results Directory Empty

**Symptoms:**
- `reports/allure-results/` directory exists but contains no files
- Allure command shows "No test results found"

**Cause:**
Allure formatter not invoked during test execution or output path misconfigured.

**Solution:**

1. **Verify formatter was used:**
```bash
# Ensure Allure formatter is specified
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results
```

2. **Check directory contents:**
```bash
# List Allure results files
ls -la reports/allure-results/
# Expected: *-result.json, *-container.json, *-attachment.* files
```

3. **Verify behave.ini configuration:**
```ini
[behave.userdata]
allure_results_dir = reports/allure-results
```

**Source Reference:** `behave.ini:81-82`

**Diagnostic Command:**
```bash
# Count Allure result files
find reports/allure-results -name "*-result.json" | wc -l
# Should match number of executed scenarios
```

### Issue: Report Not Generating with allure serve

**Symptoms:**
```
ERROR: Could not read report data
ERROR: Allure report generation failed
```

**Cause:**
Corrupted Allure results files or incompatible Allure CLI version.

**Solution:**

1. **Validate Allure results format:**
```bash
# Check JSON validity of result files
for f in reports/allure-results/*-result.json; do
    echo "Validating $f"
    python -m json.tool "$f" > /dev/null
done
```

2. **Clean and regenerate:**
```bash
# Remove old results
rm -rf reports/allure-results/*

# Regenerate Allure results
behave --format=allure_behave.formatter:AllureFormatter --outfile=reports/allure-results
```

3. **Check Allure CLI compatibility:**
```bash
# Verify Allure version
allure --version
# Recommended: 2.20.0 or higher

# Generate report (instead of serve for debugging)
allure generate reports/allure-results --output reports/allure-report --clean
```

**Source Reference:** `README.md:500-503`

### Issue: Attachments Not Showing

**Symptoms:**
- Screenshots captured but not visible in Allure report
- Logs not attached to test results

**Cause:**
Attachments not properly linked to Allure results or incorrect attachment format.

**Solution:**

Verify attachment integration in `features/environment.py`:

**Source Reference:** `features/environment.py:364-367`

```python
# Correct screenshot attachment implementation
from utilities.screenshot_helper import capture_screenshot

def after_scenario(context, scenario):
    if scenario.status == 'failed':
        if hasattr(context, 'driver') and context.driver is not None:
            screenshot_path = capture_screenshot(
                driver=context.driver,
                scenario_name=scenario.name,
                attach_to_allure=True  # Ensure Allure attachment enabled
            )
```

**Diagnostic Command:**
```bash
# Check for attachment files in Allure results
find reports/allure-results -name "*-attachment.*" -ls

# Verify screenshot files referenced in result JSON
grep -r "attachments" reports/allure-results/*.json
```

### Issue: Screenshot Not Attached per environment.py after_scenario Hook

**Symptoms:**
- Tests fail but no screenshots in reports
- Screenshot files exist but not linked to test results

**Cause:**
Screenshot capture logic not properly configured or driver unavailable.

**Solution:**

Review `after_scenario` hook implementation:

**Source Reference:** `features/environment.py:280-380`

```python
def after_scenario(context: Context, scenario) -> None:
    # Ensure proper screenshot capture on failure
    if scenario.status == 'failed':
        # CRITICAL: Check driver exists before screenshot
        if hasattr(context, 'driver') and context.driver is not None:
            logger.info("Capturing failure screenshot for scenario: %s", scenario.name)
            
            try:
                screenshot_path = capture_screenshot(
                    driver=context.driver,
                    scenario_name=scenario.name,
                    attach_to_allure=True
                )
                
                if screenshot_path:
                    logger.info("Screenshot saved: %s", screenshot_path)
            except Exception as e:
                logger.error("Screenshot capture failed: %s", e)
```

**Diagnostic Command:**
```bash
# Verify screenshot_helper is working
python -c "from utilities.screenshot_helper import capture_screenshot; print('Import OK')"

# Check SCREENSHOTS_ON_FAILURE configuration
grep -i screenshot config/config.yaml .env
```

## 6. JUnit XML Report Issues

### Issue: --format=junit for Jenkins Integration

**Symptoms:**
- Jenkins not displaying test results
- Test Results Analyzer showing "No tests found"
- JUnit plugin cannot parse XML files

**Cause:**
JUnit XML is not generated via `--format=junit` but via `--junit` flag in Behave.

**Solution:**

Use correct JUnit generation syntax:

```bash
# Correct: Use --junit flag (not --format=junit)
behave --junit --junit-directory reports/junit

# Verify XML files generated
ls -la reports/junit/
# Expected: TESTS-*.xml files
```

**Source Reference:** `behave.ini:36-37`, `README.md:489-490`

**Configuration in behave.ini:**
```ini
[behave]
junit = true
junit_directory = reports/junit
```

**Jenkins Configuration:**
```groovy
// Publish JUnit test results
junit testResults: 'reports/junit/*.xml', allowEmptyResults: false
```

**Diagnostic Command:**
```bash
# Validate XML syntax
xmllint --noout reports/junit/*.xml && echo "Valid XML" || echo "Invalid XML"
```

### Issue: XML Parsing Errors in Jenkins

**Symptoms:**
```
ERROR: Test reports were found but none of them are new
FATAL: Invalid XML: Content is not allowed in prolog
```

**Cause:**
Malformed XML, encoding issues, or empty XML files.

**Solution:**

1. **Validate XML structure:**
```bash
# Check for BOM or encoding issues
file reports/junit/*.xml
# Expected: UTF-8 Unicode text

# Validate XML with xmllint
xmllint --format reports/junit/TESTS-*.xml
```

2. **Regenerate JUnit reports:**
```bash
# Clean old reports
rm -rf reports/junit/*

# Generate fresh reports
behave --junit --junit-directory reports/junit
```

3. **Verify XML contains test results:**
```bash
# Check for testsuite elements
grep -c "<testsuite" reports/junit/*.xml
# Should be > 0

# Check for testcase elements
grep -c "<testcase" reports/junit/*.xml
# Should match number of executed scenarios
```

**Source Reference:** `behave.ini:34-37`

### Issue: Test Results Not Showing Correctly

**Symptoms:**
- Tests pass locally but show as failed in Jenkins
- Test counts don't match executed scenarios
- Duration metrics incorrect

**Cause:**
JUnit XML timestamp or status mapping issues.

**Solution:**

1. **Verify test execution completed:**
```bash
# Check for proper testsuite closure
tail -5 reports/junit/TESTS-*.xml
# Should see </testsuite> closing tag
```

2. **Review test status mapping:**
```bash
# Check for failure/error/skipped status
grep -E "<(failure|error|skipped)" reports/junit/*.xml

# Verify passed tests have no failure elements
```

3. **Check Jenkins JUnit plugin version:**
   - Ensure JUnit plugin is updated (1.50+)
   - Review Jenkins system log for parsing errors

**Diagnostic Command:**
```bash
# Extract test statistics from JUnit XML
xmllint --xpath "//testsuite/@tests" reports/junit/*.xml
xmllint --xpath "//testsuite/@failures" reports/junit/*.xml
xmllint --xpath "//testsuite/@errors" reports/junit/*.xml
```

## 7. Screenshot Attachment Failures

### Issue: screenshot_helper.py capture_screenshot() Not Working

**Symptoms:**
- No screenshots captured on test failure
- Empty screenshots directory
- Errors in environment.py after_scenario hook

**Cause:**
Driver unavailable, permission issues, or screenshot_helper misconfiguration.

**Solution:**

**Source Reference:** `utilities/screenshot_helper.py:97-150`

1. **Verify driver availability:**
```python
# In environment.py after_scenario hook
if hasattr(context, 'driver') and context.driver is not None:
    # Driver available for screenshot
    screenshot_path = capture_screenshot(context.driver, scenario.name)
else:
    logger.error("Driver not available for screenshot")
```

2. **Check screenshot directory:**
```bash
# Ensure directory exists and is writable
mkdir -p reports/screenshots
chmod 755 reports/screenshots
```

3. **Test screenshot_helper directly:**
```python
# Test screenshot capture
from utilities.screenshot_helper import capture_screenshot
from utilities.driver_manager import DriverManager

driver = DriverManager.get_driver()
driver.get("https://example.com")
path = capture_screenshot(driver, "test_screenshot")
print(f"Screenshot saved: {path}")
```

**Diagnostic Command:**
```bash
# Check screenshot_helper imports
python -c "from utilities.screenshot_helper import capture_screenshot, sanitize_filename; print('OK')"

# Verify screenshots directory
ls -la reports/screenshots/
```

### Issue: File Path Issues

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'reports/screenshots/...'
```

**Cause:**
Relative path resolution issues or incorrect working directory.

**Solution:**

Ensure consistent path handling:

**Source Reference:** `utilities/screenshot_helper.py:150-170`

```python
# screenshot_helper.py uses Path for cross-platform compatibility
from pathlib import Path

# Get project root
project_root = Path(__file__).parent.parent
screenshot_dir = project_root / "reports" / "screenshots"

# Create directory if not exists
screenshot_dir.mkdir(parents=True, exist_ok=True)
```

**Diagnostic Command:**
```bash
# Verify working directory during test execution
python -c "import os; print(f'CWD: {os.getcwd()}')"

# Check if reports/screenshots exists relative to project root
test -d "$(pwd)/reports/screenshots" && echo "Path OK" || echo "Path issue"
```

### Issue: Screenshot Directory Not Writable

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: 'reports/screenshots/Login_Failed.png'
```

**Cause:**
File system permission restrictions.

**Solution:**

```bash
# Fix permissions
chmod -R 755 reports/screenshots

# For Docker containers
RUN mkdir -p /app/reports/screenshots && chmod -R 777 /app/reports/screenshots
```

**Source Reference:** `behave.ini:86`

### Issue: SCREENSHOTS_ON_FAILURE Configuration

**Symptoms:**
- Screenshots not captured even though tests fail
- Inconsistent screenshot capture behavior

**Cause:**
SCREENSHOTS_ON_FAILURE environment variable or configuration not set.

**Solution:**

Check configuration files:

```yaml
# config/config.yaml
reporting:
  screenshots_on_failure: true
  screenshot_directory: "reports/screenshots"
```

```bash
# .env file
SCREENSHOTS_ON_FAILURE=true
```

**Source Reference:** `config/config.yaml`, `.env.example`

**Diagnostic Command:**
```bash
# Check configuration value
python -c "from config.test_config import get_config; print(get_config().reporting.screenshots_on_failure)"
```

## 8. Report Publishing in CI/CD

### Issue: Jenkins publishHTML Plugin Configuration

**Symptoms:**
- HTML reports not visible in Jenkins job page
- "No HTML reports found" error
- Reports archived but not published

**Cause:**
Incorrect publishHTML plugin configuration or missing plugin.

**Solution:**

**Source Reference:** `README.md:456-463`

Install and configure publishHTML plugin:

```groovy
// Jenkinsfile
post {
    always {
        // Publish HTML reports
        publishHTML([
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: 'reports/behave-reports',
            reportFiles: 'report.html',
            reportName: 'Behave HTML Report',
            reportTitles: 'Test Execution Report'
        ])
        
        // Publish Allure report
        allure([
            includeProperties: false,
            results: [[path: 'reports/allure-results']]
        ])
        
        // Archive screenshots
        archiveArtifacts artifacts: 'reports/screenshots/*.png', 
                         allowEmptyArchive: true
    }
}
```

**Diagnostic Command:**
```bash
# Verify report files exist before publishing
find reports/ -name "*.html" -o -name "*.json" -o -name "*.xml"
```

### Issue: GitHub Actions Artifact Upload

**Symptoms:**
- Artifacts not uploaded to GitHub Actions
- "No files were found" warning
- Reports not accessible after workflow completion

**Solution:**

Configure artifact upload in GitHub Actions workflow:

```yaml
# .github/workflows/tests.yml
- name: Upload Test Reports
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-reports
    path: |
      reports/behave-reports/
      reports/cucumber.json
      reports/junit/
      reports/screenshots/
    retention-days: 30

- name: Upload Allure Results
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: allure-results
    path: reports/allure-results/
    retention-days: 30
```

**Diagnostic Command:**
```bash
# Verify artifacts before upload
ls -R reports/
```

### Issue: GitLab CI Artifacts Syntax

**Symptoms:**
- Artifacts not available in GitLab CI job page
- Reports not downloadable
- "No artifacts" message

**Solution:**

Configure artifacts in `.gitlab-ci.yml`:

```yaml
test:
  script:
    - behave --format=json --outfile=reports/cucumber.json
  artifacts:
    when: always
    paths:
      - reports/
    reports:
      junit: reports/junit/*.xml
    expire_in: 1 week
```

### Issue: Report Aggregation in Parallel Execution

**Symptoms:**
- Multiple report files generated
- Reports overwrite each other
- Incomplete test results

**Cause:**
Parallel workers writing to same output file.

**Solution:**

Use separate output files per worker:

```bash
# behave-parallel with unique output per process
behave --processes 4 --parallel-element scenario \
  --format=json \
  --outfile=reports/cucumber-{WORKER_ID}.json

# Aggregate reports after completion
jq -s 'add' reports/cucumber-*.json > reports/cucumber-combined.json
```

### Issue: Archiving Screenshots per Jenkins Example

**Symptoms:**
- Screenshots not visible in Jenkins artifacts
- Old screenshots not cleaned up
- Screenshot storage growing unbounded

**Solution:**

**Source Reference:** `README.md:461`

```groovy
post {
    always {
        // Archive screenshots with proper configuration
        archiveArtifacts(
            artifacts: 'reports/screenshots/*.png',
            allowEmptyArchive: true,
            fingerprint: true,
            onlyIfSuccessful: false
        )
    }
}
```

**Cleanup old artifacts:**
```groovy
// Configure build discarder
properties([
    buildDiscarder(
        logRotator(
            artifactDaysToKeepStr: '30',
            artifactNumToKeepStr: '10'
        )
    )
])
```

## 9. Report Viewing Issues

### Issue: Local Server for Allure

**Symptoms:**
- Cannot view Allure report locally
- Browser shows connection refused
- `allure serve` not starting

**Cause:**
Port conflict or Allure server not running.

**Solution:**

**Source Reference:** `README.md:500`

```bash
# Start Allure server
allure serve reports/allure-results
# Server starts on http://localhost:random-port

# Generate static report (no server needed)
allure generate reports/allure-results --output reports/allure-report --clean

# View static report
open reports/allure-report/index.html
```

**Alternative ports:**
```bash
# Specify custom port
allure serve -p 8080 reports/allure-results
```

### Issue: Browser CORS Issues

**Symptoms:**
```
CORS policy: No 'Access-Control-Allow-Origin' header
Failed to load resource: net::ERR_FAILED
```

**Cause:**
Opening HTML reports directly from file system triggers CORS restrictions.

**Solution:**

Use local web server:

```bash
# Python built-in server
cd reports/
python -m http.server 8000
# Access: http://localhost:8000/report.html

# Alternatively: Use browser extensions
# Chrome: "Web Server for Chrome"
# Firefox: Disable CORS for local files (developer mode)
```

### Issue: file:// Protocol Limitations

**Symptoms:**
- JavaScript not executing in HTML reports
- Resources failing to load
- Interactive features not working

**Cause:**
Modern browsers restrict file:// protocol for security.

**Solution:**

Always use HTTP server for viewing reports:

```bash
# Option 1: Python http.server
python -m http.server 8000 --directory reports/

# Option 2: Node.js http-server
npx http-server reports/ -p 8000

# Option 3: PHP built-in server
php -S localhost:8000 -t reports/

# Access report
open http://localhost:8000/behave-reports/report.html
```

## Diagnostic Checklist

Use this checklist to systematically diagnose report generation issues:

**[ ] Formatter Installation**
```bash
pip list | grep -E "behave|allure"
```

**[ ] Directory Structure**
```bash
ls -la reports/
```

**[ ] Permissions**
```bash
test -w reports/ && echo "OK" || echo "FAIL"
```

**[ ] Configuration Files**
```bash
cat behave.ini | grep -E "format|junit|allure"
```

**[ ] Recent Test Execution**
```bash
find reports/ -type f -mmin -10  # Files modified in last 10 minutes
```

**[ ] Report File Integrity**
```bash
# JSON validation
jq . reports/cucumber.json
# XML validation
xmllint --noout reports/junit/*.xml
```

**[ ] Screenshot Capture**
```bash
ls -lt reports/screenshots/ | head -5
```

**[ ] Log Files**
```bash
grep -i "error\|exception\|failed" behave.log
```

## See Also

- **[Behave Configuration Reference](../reference/behave-configuration.md)** - Complete behave.ini options
- **[Jenkins Integration Guide](../deployment/jenkins-integration.md)** - CI/CD setup for Jenkins
- **[GitHub Actions Guide](../deployment/github-actions.md)** - GitHub Actions workflow configuration
- **[GitLab CI Guide](../deployment/gitlab-ci.md)** - GitLab CI pipeline setup
- **[Environment Hooks API](../api-reference/features/environment.md)** - Lifecycle hooks documentation
- **[Screenshot Management Guide](../guides/screenshot-management.md)** - Screenshot capture best practices
- **[Common Errors](./common-errors.md)** - General troubleshooting guide

## Getting Help

If issues persist after following this guide:

1. **Check Behave version compatibility:**
   ```bash
   behave --version
   pip show behave allure-behave behave-html-formatter
   ```

2. **Enable verbose logging:**
   ```bash
   behave --verbose --no-capture --logging-level=DEBUG
   ```

3. **Review log files:**
   ```bash
   tail -100 behave.log
   ```

4. **Consult documentation:**
   - [Behave Official Docs](https://behave.readthedocs.io/)
   - [Allure Framework Docs](https://docs.qameta.io/allure/)

5. **Community support:**
   - GitHub Issues
   - Stack Overflow (tags: behave, selenium, allure)


