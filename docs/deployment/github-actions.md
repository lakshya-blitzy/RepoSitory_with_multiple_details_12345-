# GitHub Actions CI/CD Integration

## Overview

GitHub Actions provides a powerful, cloud-native CI/CD platform that integrates seamlessly with your GitHub repository for automated test execution. This guide covers comprehensive GitHub Actions workflow configuration for the Testinium QA Python test automation framework.

### Benefits of GitHub Actions

**Native GitHub Integration:**
- No external CI/CD service configuration required
- Workflows defined directly in repository (`.github/workflows/`)
- Native integration with pull requests, issues, and releases
- Built-in secrets management and environment protection

**Cost-Effective:**
- Free for public repositories with unlimited minutes
- 2,000 free minutes/month for private repositories
- Additional minutes available at competitive pricing
- Concurrent workflows enable fast feedback

**YAML-Based Configuration:**
- Simple, readable workflow syntax
- Version-controlled workflow definitions
- Reusable workflows and composite actions
- Extensive marketplace with 10,000+ pre-built actions

**Extensive Marketplace:**
- Pre-built actions for common tasks (checkout, setup-python, cache)
- Community-contributed actions for specialized needs
- Easy integration with third-party services
- Actively maintained action ecosystem

**Concurrent Workflows:**
- Multiple jobs run in parallel by default
- Matrix strategy for testing across configurations
- Workflow dependencies with `needs` keyword
- Efficient resource utilization

### When to Use GitHub Actions

GitHub Actions is ideal for:
- Projects hosted on GitHub
- Teams requiring fast PR validation
- Multi-platform testing (Linux, macOS, Windows)
- Matrix builds across Python versions and browsers
- Automated deployment and release workflows
- Integration with GitHub-native features (Pages, Releases, Packages)

## Prerequisites

Before setting up GitHub Actions for your test automation framework:

**1. GitHub Repository Access:**
- Repository with GitHub Actions enabled (enabled by default)
- Write access to create workflow files in `.github/workflows/`
- Admin access for configuring secrets and environment protection rules

**2. YAML Syntax Knowledge:**
- Understanding of YAML indentation and structure
- Familiarity with GitHub Actions workflow syntax
- See: [GitHub Actions Syntax Documentation](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

**3. Secrets Configuration:**
- Test user credentials configured in repository settings
- Environment-specific configuration values
- API tokens for third-party integrations (if applicable)

**4. Framework Understanding:**
- Familiarity with behave test execution commands
- Understanding of test tags and filtering
- Knowledge of report generation requirements

## Complete Workflow File Example

Create `.github/workflows/tests.yml` in your repository:

```yaml
name: Testinium QA Automated Tests

# Workflow Triggers
on:
  # Run on push to main branch
  push:
    branches: [main, develop]
  
  # Run on pull requests to main
  pull_request:
    branches: [main]
  
  # Scheduled nightly regression (2 AM UTC)
  schedule:
    - cron: '0 2 * * *'
  
  # Manual workflow dispatch
  workflow_dispatch:
    inputs:
      tags:
        description: 'Test tags to execute'
        required: false
        default: '@Smoke'
      browser:
        description: 'Browser type'
        required: false
        default: 'chrome'

# Environment variables at workflow level
env:
  BROWSER_TYPE: chrome
  HEADLESS: true
  SCREENSHOTS_ON_FAILURE: true

jobs:
  test:
    name: Test - Python ${{ matrix.python-version }} - ${{ matrix.browser }} - ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    
    strategy:
      # Don't cancel all jobs if one fails
      fail-fast: false
      
      # Matrix strategy for multiple configurations
      matrix:
        os: [ubuntu-latest]
        python-version: ['3.9', '3.10', '3.11', '3.12']
        browser: [chrome, firefox]
        
        # Include specific combinations for extended testing
        include:
          # Test on macOS with latest Python
          - os: macos-latest
            python-version: '3.12'
            browser: chrome
          
          # Test on Windows with latest Python
          - os: windows-latest
            python-version: '3.12'
            browser: chrome
        
        # Exclude unstable combinations
        exclude:
          # Firefox on Python 3.9 has known issues
          - python-version: '3.9'
            browser: firefox
    
    steps:
      # Step 1: Checkout repository
      - name: Checkout code
        uses: actions/checkout@v4
      
      # Step 2: Set up Python with caching
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
          cache-dependency-path: requirements.txt
      
      # Step 3: Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      # Step 4: Create .env file from secrets
      - name: Create environment configuration
        run: |
          echo "BROWSER_TYPE=${{ matrix.browser }}" >> .env
          echo "HEADLESS=true" >> .env
          echo "BASE_URL=${{ secrets.BASE_URL }}" >> .env
          echo "TEST_USERNAME=${{ secrets.TEST_USERNAME }}" >> .env
          echo "TEST_PASSWORD=${{ secrets.TEST_PASSWORD }}" >> .env
          echo "SALES_MANAGER_USERNAME=${{ secrets.SALES_MANAGER_USERNAME }}" >> .env
          echo "SALES_MANAGER_PASSWORD=${{ secrets.SALES_MANAGER_PASSWORD }}" >> .env
          echo "POS_MANAGER_USERNAME=${{ secrets.POS_MANAGER_USERNAME }}" >> .env
          echo "POS_MANAGER_PASSWORD=${{ secrets.POS_MANAGER_PASSWORD }}" >> .env
          echo "SCREENSHOTS_ON_FAILURE=true" >> .env
      
      # Step 5: Run tests with behave
      - name: Run tests
        run: |
          behave --tags="${{ github.event.inputs.tags || '@Smoke' }}" \
                 --format=pretty \
                 --format=json \
                 --outfile=reports/cucumber.json \
                 --junit \
                 --junit-directory=reports/junit \
                 --no-capture
      
      # Step 6: Generate Allure report results
      - name: Generate Allure results
        if: always()
        run: |
          behave --tags="${{ github.event.inputs.tags || '@Smoke' }}" \
                 --format=allure_behave.formatter:AllureFormatter \
                 --outfile=reports/allure-results \
                 --no-capture
      
      # Step 7: Upload test reports as artifacts
      - name: Upload test reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-reports-${{ matrix.os }}-py${{ matrix.python-version }}-${{ matrix.browser }}
          path: |
            reports/**
          retention-days: 30
      
      # Step 8: Upload screenshots on failure
      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: screenshots-${{ matrix.os }}-py${{ matrix.python-version }}-${{ matrix.browser }}
          path: reports/screenshots/
          retention-days: 14
      
      # Step 9: Publish test results
      - name: Publish test results
        if: always()
        uses: EnricoMi/publish-unit-test-result-action@v2
        with:
          files: reports/junit/*.xml
          check_name: Test Results - ${{ matrix.os }} - Python ${{ matrix.python-version }} - ${{ matrix.browser }}
```

**Source:** `.github/workflows/tests.yml` (example configuration)

## Detailed Job Configuration

### Workflow Triggers Explained

**Push Trigger:**
```yaml
on:
  push:
    branches: [main, develop]
```
- Automatically runs on every push to main or develop branches
- Provides immediate feedback on code changes
- Ensures main branch always has passing tests

**Pull Request Trigger:**
```yaml
on:
  pull_request:
    branches: [main]
```
- Runs on every pull request targeting main branch
- Validates changes before merge
- Status checks can be required for merge protection

**Scheduled Trigger:**
```yaml
on:
  schedule:
    - cron: '0 2 * * *'
```
- Runs nightly at 2 AM UTC
- Catches environment-related issues
- Validates test stability over time
- Cron syntax: minute hour day month day-of-week

**Manual Workflow Dispatch:**
```yaml
on:
  workflow_dispatch:
    inputs:
      tags:
        description: 'Test tags to execute'
        required: false
        default: '@Smoke'
```
- Allows manual workflow execution from Actions tab
- Accepts custom inputs (tags, browser, environment)
- Useful for on-demand testing and debugging

### Matrix Strategy Deep Dive

The matrix strategy enables parallel testing across multiple configurations:

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest]
    python-version: ['3.9', '3.10', '3.11', '3.12']
    browser: [chrome, firefox]
```

**Matrix Dimensions:**
- **os:** Operating system (ubuntu-latest, macos-latest, windows-latest)
- **python-version:** Python versions to test (3.9, 3.10, 3.11, 3.12)
- **browser:** Browser types (chrome, firefox)

**Total Job Combinations:**
- Base matrix: 1 OS × 4 Python versions × 2 browsers = 8 jobs
- With include/exclude: Can adjust for specific needs
- All jobs run in parallel (subject to runner availability)

**fail-fast: false:**
- Continues running all matrix jobs even if one fails
- Provides complete test results across all configurations
- Essential for identifying platform-specific issues

**Matrix Include for Additional Combinations:**
```yaml
include:
  - os: macos-latest
    python-version: '3.12'
    browser: chrome
```
- Adds specific configuration to matrix
- Tests critical platform combinations
- Example: Latest Python on macOS for Apple Silicon compatibility

**Matrix Exclude to Skip Combinations:**
```yaml
exclude:
  - python-version: '3.9'
    browser: firefox
```
- Removes specific combinations from matrix
- Skips known problematic configurations
- Reduces unnecessary test execution time

### Environment Variables Configuration

**Workflow-Level Environment Variables:**
```yaml
env:
  BROWSER_TYPE: chrome
  HEADLESS: true
  SCREENSHOTS_ON_FAILURE: true
```
- Available to all jobs in workflow
- Can be overridden at job or step level
- Use for common configuration across jobs

**Job-Level Environment Variables:**
```yaml
jobs:
  test:
    env:
      PYTHON_ENV: test
      LOG_LEVEL: INFO
```
- Specific to single job
- Overrides workflow-level variables
- Useful for job-specific configuration

**Step-Level Environment Variables:**
```yaml
- name: Run specific tests
  env:
    BEHAVE_TAGS: '@Smoke'
  run: behave
```
- Most specific scope
- Overrides job and workflow level
- Use for step-specific customization

**Matrix Variables in Environment:**
```yaml
env:
  BROWSER: ${{ matrix.browser }}
  PYTHON_VERSION: ${{ matrix.python-version }}
```
- Reference matrix values in environment variables
- Enable conditional logic based on matrix
- Pass to test execution commands

## Secrets Management

GitHub Actions provides secure secrets management for sensitive data like credentials and API tokens.

### Configuring Secrets in Repository Settings

**Navigate to Secrets:**
1. Go to repository **Settings**
2. Select **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Enter secret name and value
5. Click **Add secret**

**Required Secrets for Test Framework:**

Based on configuration requirements from `config/config.yaml` and `.env.example`:

| Secret Name | Description | Example Value | Required |
|-------------|-------------|---------------|----------|
| `BASE_URL` | Application base URL | `https://testinium.example.com` | Yes |
| `TEST_USERNAME` | Generic test user username | `testuser@example.com` | Yes |
| `TEST_PASSWORD` | Generic test user password | `SecureP@ssw0rd!` | Yes |
| `SALES_MANAGER_USERNAME` | Sales manager role username | `salesmanager@example.com` | Yes |
| `SALES_MANAGER_PASSWORD` | Sales manager role password | `SecureP@ssw0rd!` | Yes |
| `POS_MANAGER_USERNAME` | POS manager role username | `posmanager@example.com` | Yes |
| `POS_MANAGER_PASSWORD` | POS manager role password | `SecureP@ssw0rd!` | Yes |

**Source:** `config/config.yaml` lines 93-110, `.env.example` lines 16-28

### Accessing Secrets in Workflows

**Using Secrets in Steps:**
```yaml
- name: Create environment configuration
  run: |
    echo "BASE_URL=${{ secrets.BASE_URL }}" >> .env
    echo "TEST_USERNAME=${{ secrets.TEST_USERNAME }}" >> .env
    echo "TEST_PASSWORD=${{ secrets.TEST_PASSWORD }}" >> .env
```

**Security Best Practices:**
- Never print secrets to logs: `echo "Secret: ${{ secrets.PASSWORD }}"` ❌
- Use secrets only in secure contexts
- Secrets are automatically masked in logs
- Rotate secrets regularly
- Use environment-specific secrets for staging/production

### Environment-Specific Secrets

**For Multiple Environments:**
```yaml
jobs:
  test:
    environment: staging
    steps:
      - name: Use environment secrets
        run: |
          echo "URL: ${{ secrets.BASE_URL }}"
```

**Configure Environments:**
1. **Settings** → **Environments**
2. Create environments: development, staging, production
3. Add environment-specific secrets
4. Configure protection rules (required approvals, branch restrictions)

**Benefits:**
- Different credentials per environment
- Environment protection rules
- Deployment approval workflows
- Audit trail for deployments

## Artifact Management

GitHub Actions artifacts store test reports, screenshots, and logs for later analysis.

### Uploading Test Reports

**Upload All Reports:**
```yaml
- name: Upload test reports
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-reports-${{ matrix.os }}-py${{ matrix.python-version }}-${{ matrix.browser }}
    path: |
      reports/**
    retention-days: 30
```

**Key Configuration:**
- `if: always()`: Upload even if tests fail
- `name`: Unique artifact name with matrix variables
- `path`: Glob pattern for files to upload
- `retention-days`: How long GitHub stores artifacts (1-90 days)

**Artifact Paths Based on behave.ini Configuration:**
```
reports/
├── cucumber.json          # JSON test results
├── junit/*.xml           # JUnit XML for CI integration
├── allure-results/       # Allure report data
└── screenshots/          # Failure screenshots
```

**Source:** `behave.ini` lines 34-92

### Uploading Screenshots on Failure

**Conditional Upload:**
```yaml
- name: Upload screenshots
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: screenshots-${{ matrix.os }}-py${{ matrix.python-version }}-${{ matrix.browser }}
    path: reports/screenshots/
    retention-days: 14
```

**Key Features:**
- `if: failure()`: Only upload when tests fail
- Separate artifact for screenshots
- Shorter retention (14 days) to save storage
- Matrix-specific naming for identification

### Downloading Artifacts for Debugging

**From GitHub UI:**
1. Navigate to workflow run
2. Scroll to **Artifacts** section
3. Click artifact name to download ZIP

**Using GitHub CLI:**
```bash
# List artifacts for a run
gh run view <run-id> --log

# Download specific artifact
gh run download <run-id> --name test-reports-ubuntu-latest-py3.12-chrome

# Download all artifacts
gh run download <run-id>
```

### Artifact Matrix Strategy

**For Matrix Builds:**
- Each matrix job produces separate artifacts
- Naming includes matrix dimensions for identification
- Total artifacts = number of matrix jobs
- Example: 8 matrix jobs = 8 test report artifacts + screenshots (on failure)

**Managing Artifact Storage:**
- Default retention: 90 days
- Reduce retention for large artifacts
- Screenshots: 14 days (high volume)
- Test reports: 30 days (analysis needs)
- Critical releases: 90 days (long-term reference)

## Caching Strategies

Caching dependencies significantly reduces workflow execution time by reusing previously downloaded packages.

### Pip Dependency Caching

**Automatic Caching with setup-python:**
```yaml
- name: Set up Python ${{ matrix.python-version }}
  uses: actions/setup-python@v4
  with:
    python-version: ${{ matrix.python-version }}
    cache: 'pip'
    cache-dependency-path: requirements.txt
```

**How It Works:**
- Generates cache key from `requirements.txt` hash
- Restores cached dependencies if key matches
- Downloads and caches dependencies on cache miss
- Automatic invalidation when requirements.txt changes

**Benefits:**
- 30-60 second time savings per job
- Reduced PyPI server load
- Faster feedback on PR builds
- Automatic cache management

### Manual Pip Cache Configuration

**For Advanced Control:**
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
      ${{ runner.os }}-

- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

**Cache Key Components:**
- `runner.os`: Operating system (Linux, macOS, Windows)
- `hashFiles('requirements.txt')`: Content hash of requirements file
- `restore-keys`: Fallback keys if exact match not found

**Source:** `requirements.txt` - 91 lines of dependencies

### WebDriver Binary Caching

**Cache Browser Drivers:**
```yaml
- name: Cache WebDriver binaries
  uses: actions/cache@v3
  with:
    path: ~/.wdm
    key: ${{ runner.os }}-webdriver-${{ matrix.browser }}-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-webdriver-${{ matrix.browser }}-
      ${{ runner.os }}-webdriver-

- name: Install dependencies
  run: pip install -r requirements.txt
```

**Benefits:**
- Caches ChromeDriver and GeckoDriver binaries
- Reduces download time from external sources
- Framework uses `webdriver-manager==4.0.1` for driver management
- Cache invalidated on requirements.txt change

### Virtual Environment Caching

**Cache Entire venv (Advanced):**
```yaml
- name: Cache virtual environment
  uses: actions/cache@v3
  with:
    path: venv
    key: ${{ runner.os }}-venv-${{ matrix.python-version }}-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-venv-${{ matrix.python-version }}-

- name: Set up virtual environment
  run: |
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
```

**When to Use:**
- Very large dependency trees
- Slow installation dependencies (e.g., data science packages)
- Custom build steps for dependencies

**Caveats:**
- Larger cache size
- Platform-specific (separate caches per OS)
- May not work with all dependency configurations

### Cache Efficiency Tips

**Optimize Cache Performance:**
1. **Use smallest necessary cache scope:** Pip cache (hundreds of MB) vs venv cache (gigabytes)
2. **Leverage restore-keys:** Provide fallback keys for partial cache hits
3. **Cache stable dependencies:** Don't cache frequently changing files
4. **Monitor cache hit rates:** Check workflow logs for cache hit/miss
5. **Clean up old caches:** GitHub automatically removes caches not accessed in 7 days

**Cache Size Limits:**
- Maximum cache size per repository: 10 GB
- Caches exceeding limit are evicted (LRU policy)
- Check cache usage: Settings → Actions → Caches

## Report Publishing Strategies

Publish test reports for easy access and analysis by team members.

### GitHub Pages Deployment for HTML Reports

**Deploy HTML Reports to GitHub Pages:**

Create `.github/workflows/deploy-reports.yml`:

```yaml
name: Deploy Test Reports

on:
  workflow_run:
    workflows: ["Testinium QA Automated Tests"]
    types:
      - completed

jobs:
  deploy-reports:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: test-reports-ubuntu-latest-py3.12-chrome
          path: reports
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./reports
          publish_branch: gh-pages
          force_orphan: true
```

**Access Reports:**
- URL: `https://<username>.github.io/<repository>/`
- Configure: Settings → Pages → Source: gh-pages branch

### Allure Report Hosting

**Generate and Host Allure Reports:**

```yaml
- name: Generate Allure report
  if: always()
  run: |
    behave -f allure_behave.formatter:AllureFormatter -o allure-results
    allure generate allure-results -o allure-report --clean

- name: Deploy Allure report to GitHub Pages
  if: always()
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./allure-report
    destination_dir: allure
```

**Access Allure Reports:**
- URL: `https://<username>.github.io/<repository>/allure/`
- Interactive HTML report with test history
- Detailed test execution graphs and trends

**Source:** `behave.ini` lines 77-82 (Allure configuration)

### PR Comment with Test Results

**Post Test Summary to Pull Request:**

```yaml
- name: Comment PR with test results
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const testResults = fs.readFileSync('reports/cucumber.json', 'utf8');
      const results = JSON.parse(testResults);
      
      let passed = 0;
      let failed = 0;
      let skipped = 0;
      
      results.forEach(feature => {
        feature.elements.forEach(scenario => {
          scenario.steps.forEach(step => {
            if (step.result.status === 'passed') passed++;
            else if (step.result.status === 'failed') failed++;
            else if (step.result.status === 'skipped') skipped++;
          });
        });
      });
      
      const comment = `## Test Results\n\n` +
        `✅ Passed: ${passed}\n` +
        `❌ Failed: ${failed}\n` +
        `⏭️ Skipped: ${skipped}\n\n` +
        `[View detailed reports](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }})`;
      
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: comment
      });
```

**Benefits:**
- Immediate visibility of test results in PR
- No need to navigate to Actions tab
- Quick decision on PR merge readiness

### JUnit Report Publishing

**Publish JUnit XML Results:**

```yaml
- name: Publish test results
  if: always()
  uses: EnricoMi/publish-unit-test-result-action@v2
  with:
    files: reports/junit/*.xml
    check_name: Test Results - ${{ matrix.os }} - Python ${{ matrix.python-version }}
    comment_mode: always
    fail_on: 'errors'
```

**Features:**
- Native GitHub check annotations
- Test result trends over time
- Failed test details in PR checks
- Automatic pass/fail status

**Source:** `behave.ini` lines 34-37 (JUnit configuration)

## Advanced Workflows

### Reusable Workflows

**Create Reusable Test Workflow:**

`.github/workflows/reusable-test.yml`:

```yaml
name: Reusable Test Workflow

on:
  workflow_call:
    inputs:
      python-version:
        required: true
        type: string
      browser:
        required: true
        type: string
      tags:
        required: false
        type: string
        default: '@Smoke'
    secrets:
      TEST_USERNAME:
        required: true
      TEST_PASSWORD:
        required: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ inputs.python-version }}
          cache: 'pip'
      
      - name: Run tests
        run: |
          pip install -r requirements.txt
          behave --tags="${{ inputs.tags }}"
```

**Use Reusable Workflow:**

```yaml
jobs:
  smoke-tests:
    uses: ./.github/workflows/reusable-test.yml
    with:
      python-version: '3.12'
      browser: 'chrome'
      tags: '@Smoke'
    secrets:
      TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
      TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
```

### Composite Actions

**Create Custom Setup Action:**

`.github/actions/setup-test-environment/action.yml`:

```yaml
name: 'Setup Test Environment'
description: 'Sets up Python, installs dependencies, configures environment'

inputs:
  python-version:
    description: 'Python version'
    required: true
  browser:
    description: 'Browser type'
    required: true

runs:
  using: 'composite'
  steps:
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ inputs.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      shell: bash
      run: pip install -r requirements.txt
    
    - name: Create .env file
      shell: bash
      run: |
        echo "BROWSER_TYPE=${{ inputs.browser }}" >> .env
        echo "HEADLESS=true" >> .env
```

**Use Composite Action:**

```yaml
steps:
  - uses: actions/checkout@v4
  
  - name: Setup environment
    uses: ./.github/actions/setup-test-environment
    with:
      python-version: '3.12'
      browser: 'chrome'
```

### Workflow Dependencies

**Sequential Job Execution:**

```yaml
jobs:
  smoke-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run smoke tests
        run: behave --tags=@Smoke
  
  regression-tests:
    needs: smoke-tests
    runs-on: ubuntu-latest
    steps:
      - name: Run regression tests
        run: behave --tags=@Regression
  
  deploy:
    needs: [smoke-tests, regression-tests]
    runs-on: ubuntu-latest
    steps:
      - name: Deploy application
        run: echo "Deploying..."
```

**Benefits:**
- Control job execution order
- Skip dependent jobs if prerequisites fail
- Create complex workflows with multiple stages

### Conditional Execution

**Run Steps Based on Conditions:**

```yaml
- name: Run only on main branch
  if: github.ref == 'refs/heads/main'
  run: behave --tags=@Production

- name: Run on failure
  if: failure()
  run: |
    echo "Tests failed, sending notification..."

- name: Run on success
  if: success()
  run: |
    echo "All tests passed!"

- name: Always run
  if: always()
  run: |
    echo "This runs regardless of previous step status"
```

**Common Conditions:**
- `success()`: Previous steps succeeded
- `failure()`: Any previous step failed
- `always()`: Run regardless of status
- `cancelled()`: Workflow was cancelled
- `github.event_name == 'pull_request'`: PR event
- `contains(github.ref, 'release')`: Branch name contains "release"

## Integration Patterns

### Pull Request Validation Workflow

**Automated PR Validation:**

```yaml
name: PR Validation

on:
  pull_request:
    branches: [main, develop]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run smoke tests
        run: behave --tags=@Smoke
      
      - name: Check code quality
        run: |
          pylint **/*.py
          black --check .
      
      - name: Security scan
        run: |
          pip install safety
          safety check
```

**Branch Protection Rules:**
1. **Settings** → **Branches** → **Branch protection rules**
2. Require status checks to pass: ✅ PR Validation
3. Require branches to be up to date before merging
4. Include administrators in restrictions

### Nightly Regression Workflow

**Comprehensive Nightly Testing:**

```yaml
name: Nightly Regression

on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC daily
  workflow_dispatch:

jobs:
  regression:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        tags: ['@Login', '@CRM', '@Employee', '@Inventory', '@Sales']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run feature tests
        run: behave --tags=${{ matrix.tags }}
      
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: regression-${{ matrix.tags }}
          path: reports/**
  
  notify:
    needs: regression
    runs-on: ubuntu-latest
    if: failure()
    steps:
      - name: Send failure notification
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{"text":"🚨 Nightly regression tests failed! Check GitHub Actions for details."}'
```

**Source:** Test tags from `behave.ini` line 62

### Release Workflow

**Automated Release Testing:**

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  test:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run all tests
        run: behave --tags='not @WIP'
      
      - name: Create release
        if: success()
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body: |
            ## Test Results
            ✅ All tests passed
            
            [View test reports](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }})
          draft: false
          prerelease: false
```

### Selective Test Execution on File Changes

**Run Tests Only for Changed Features:**

```yaml
name: Smart Test Execution

on:
  pull_request:
    paths:
      - 'features/**'
      - 'pages/**'
      - 'utilities/**'

jobs:
  test-changed:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Get changed files
        id: changed-files
        run: |
          CHANGED=$(git diff --name-only origin/main...HEAD | grep '\.feature$' || true)
          echo "files=$CHANGED" >> $GITHUB_OUTPUT
      
      - name: Run tests for changed features
        if: steps.changed-files.outputs.files != ''
        run: |
          for file in ${{ steps.changed-files.outputs.files }}; do
            behave $file
          done
```

## Notification Configuration

### GitHub Native Notifications

GitHub Actions provides built-in notifications for workflow events:

**Email Notifications:**
- Automatic for workflow failures
- Configure: **Settings** → **Notifications** → **Actions**
- Options: All workflows, only failures, or none

**Web Notifications:**
- Bell icon in GitHub UI shows workflow status
- Real-time updates on workflow runs
- Click notification to view workflow details

### Slack Notification Integration

**Send Slack Notifications:**

```yaml
- name: Slack notification
  if: always()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Test Results for ${{ github.repository }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Test Execution Complete*\n*Status:* ${{ job.status }}\n*Branch:* ${{ github.ref }}\n*Commit:* ${{ github.sha }}"
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "View Results"
                },
                "url": "https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}"
              }
            ]
          }
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

**Setup Slack Webhook:**
1. Go to Slack API → **Incoming Webhooks**
2. Create new webhook for your channel
3. Copy webhook URL
4. Add to GitHub secrets as `SLACK_WEBHOOK`

### Email Notification on Failure

**Send Email for Failed Tests:**

```yaml
- name: Send email notification
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: "🚨 Test Failure - ${{ github.repository }}"
    to: team@example.com
    from: github-actions@example.com
    body: |
      Test execution failed for ${{ github.repository }}
      
      Branch: ${{ github.ref }}
      Commit: ${{ github.sha }}
      Author: ${{ github.actor }}
      
      View details: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

### Microsoft Teams Notification

**Post to Teams Channel:**

```yaml
- name: Teams notification
  if: always()
  run: |
    curl -H 'Content-Type: application/json' \
         -d '{
           "@type": "MessageCard",
           "summary": "Test Results",
           "sections": [{
             "activityTitle": "Test Execution Complete",
             "facts": [
               {"name": "Repository", "value": "${{ github.repository }}"},
               {"name": "Status", "value": "${{ job.status }}"},
               {"name": "Branch", "value": "${{ github.ref }}"}
             ],
             "potentialAction": [{
               "@type": "OpenUri",
               "name": "View Results",
               "targets": [{
                 "os": "default",
                 "uri": "https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}"
               }]
             }]
           }]
         }' \
         ${{ secrets.TEAMS_WEBHOOK }}
```

## Performance Optimization

### Concurrent Job Limits

**Control Concurrency to Prevent Resource Exhaustion:**

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    # Job definition...
```

**Benefits:**
- Cancels outdated workflow runs when new commits are pushed
- Saves compute resources
- Faster feedback on latest changes
- Prevents queue backlog

### Selective Test Execution Based on Changes

**Path-Based Triggers:**

```yaml
on:
  pull_request:
    paths:
      - 'features/**'
      - 'pages/**'
      - 'utilities/**'
      - 'config/**'
      - 'requirements.txt'
```

**Skip Workflows for Documentation Changes:**

```yaml
on:
  push:
    paths-ignore:
      - 'docs/**'
      - '**.md'
      - 'LICENSE'
```

### Parallel Matrix Execution

**Optimize Matrix for Parallelism:**

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.11', '3.12']  # Skip 3.10 if not critical
    browser: [chrome]  # Test only chrome for PR, full matrix nightly
```

**PR Validation (Fast):**
- Python 3.12 only
- Chrome only
- Smoke tests only

**Nightly Regression (Comprehensive):**
- All Python versions
- Chrome and Firefox
- All test tags

### Caching Best Practices

**Optimal Cache Configuration:**

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.cache/pip
      ~/.wdm
    key: ${{ runner.os }}-deps-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-deps-
```

**Benefits:**
- Single cache action for multiple paths
- Reduces cache overhead
- Faster cache restore

### Reduce Workflow Execution Time

**Time-Saving Strategies:**

1. **Use `--fail-fast` for Quick Feedback (PR validation):**
   ```yaml
   strategy:
     fail-fast: true  # Stop on first failure for PRs
   ```

2. **Shallow Checkout:**
   ```yaml
   - uses: actions/checkout@v4
     with:
       fetch-depth: 1  # Only fetch latest commit
   ```

3. **Parallel Test Execution:**
   ```bash
   behave --processes 4 --parallel-element scenario
   ```

4. **Skip Non-Critical Tests in PR:**
   ```bash
   behave --tags="@Smoke and not @Slow"
   ```

**Source:** Parallel execution patterns from `behave.ini` lines 95-128

## Troubleshooting

### Action Version Compatibility Issues

**Issue:** Workflow fails with "Action not found" error

**Symptoms:**
```
Error: Unable to resolve action `actions/checkout@v5`
```

**Cause:** Action version doesn't exist or repository access issue

**Solution:**
1. Verify action version exists: https://github.com/actions/checkout/releases
2. Use latest stable version (e.g., `@v4`)
3. Pin to specific version for stability: `actions/checkout@v4.1.0`

**Best Practice:**
```yaml
# Use major version for auto-updates
- uses: actions/checkout@v4  # Recommended

# Pin to specific version for critical workflows
- uses: actions/checkout@v4.1.0  # For production
```

### Secret Not Found Errors

**Issue:** Workflow fails accessing secrets

**Symptoms:**
```
Error: Secret `TEST_USERNAME` is not set
```

**Cause:** Secret not configured or incorrect name

**Solution:**
1. Verify secret exists: **Settings** → **Secrets and variables** → **Actions**
2. Check exact secret name (case-sensitive)
3. Ensure secret is accessible to workflow
4. For organization secrets, verify repository access

**Debug Secret Availability:**
```yaml
- name: Check secrets
  run: |
    if [ -z "${{ secrets.TEST_USERNAME }}" ]; then
      echo "TEST_USERNAME secret is not set"
      exit 1
    fi
```

### Artifact Upload Failures

**Issue:** Artifact upload fails or artifacts not found

**Symptoms:**
```
Error: Unable to find any artifacts for the associated workflow
```

**Causes:**
- Path doesn't exist
- Incorrect glob pattern
- Artifact too large (>2 GB per artifact)

**Solutions:**

1. **Verify Path Exists:**
   ```yaml
   - name: List files before upload
     run: ls -R reports/
   
   - name: Upload artifacts
     uses: actions/upload-artifact@v3
     with:
       path: reports/**
   ```

2. **Check File Existence:**
   ```yaml
   - name: Upload artifacts
     if: hashFiles('reports/**') != ''
     uses: actions/upload-artifact@v3
     with:
       path: reports/**
   ```

3. **Handle Large Artifacts:**
   ```yaml
   # Upload multiple smaller artifacts
   - name: Upload JSON reports
     uses: actions/upload-artifact@v3
     with:
       name: json-reports
       path: reports/*.json
   
   - name: Upload screenshots
     uses: actions/upload-artifact@v3
     with:
       name: screenshots
       path: reports/screenshots/
   ```

### Matrix Job Failures

**Issue:** Specific matrix combinations fail

**Symptoms:**
- Firefox tests fail on Python 3.9
- Tests pass locally but fail in CI

**Solutions:**

1. **Exclude Problematic Combinations:**
   ```yaml
   matrix:
     python-version: ['3.9', '3.10', '3.11', '3.12']
     browser: [chrome, firefox]
     exclude:
       - python-version: '3.9'
         browser: firefox
   ```

2. **Add Conditional Steps:**
   ```yaml
   - name: Install Firefox-specific dependency
     if: matrix.browser == 'firefox'
     run: pip install selenium-firefox-plugin
   ```

3. **Debug Matrix Variables:**
   ```yaml
   - name: Debug matrix
     run: |
       echo "OS: ${{ matrix.os }}"
       echo "Python: ${{ matrix.python-version }}"
       echo "Browser: ${{ matrix.browser }}"
   ```

### Rate Limiting Issues

**Issue:** Workflow fails with rate limit errors

**Symptoms:**
```
Error: API rate limit exceeded
```

**Causes:**
- Too many API calls to GitHub
- Frequent workflow runs
- Large number of artifacts

**Solutions:**

1. **Use GITHUB_TOKEN Instead of Personal Access Token:**
   ```yaml
   - uses: actions/checkout@v4
     with:
       token: ${{ secrets.GITHUB_TOKEN }}  # Higher rate limit
   ```

2. **Reduce Workflow Frequency:**
   ```yaml
   on:
     schedule:
       - cron: '0 */6 * * *'  # Every 6 hours instead of hourly
   ```

3. **Implement Concurrency Control:**
   ```yaml
   concurrency:
     group: ${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true
   ```

### Timeout Problems

**Issue:** Workflow times out after 6 hours

**Symptoms:**
```
Error: The job running on runner 'GitHub Actions 1' has exceeded the maximum execution time of 360 minutes
```

**Causes:**
- Long-running tests
- Hanging tests (waiting for elements)
- Large test suite

**Solutions:**

1. **Set Job Timeout:**
   ```yaml
   jobs:
     test:
       timeout-minutes: 60  # Default is 360 minutes
   ```

2. **Optimize Test Execution:**
   ```bash
   # Parallel execution
   behave --processes 4 --parallel-element scenario
   ```

3. **Split into Multiple Jobs:**
   ```yaml
   jobs:
     test-login:
       runs-on: ubuntu-latest
       steps:
         - run: behave --tags=@Login
     
     test-crm:
       runs-on: ubuntu-latest
       steps:
         - run: behave --tags=@CRM
   ```

4. **Set Browser Timeouts:**
   - Check `config/config.yaml` timeout values
   - Ensure `timeouts.explicit: 10` is reasonable
   - Reduce `timeouts.page_load: 30` if tests hang

**Source:** `config/config.yaml` lines 45-60

### Browser Driver Issues

**Issue:** ChromeDriver or GeckoDriver not found

**Symptoms:**
```
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```

**Cause:** WebDriver binaries not installed or wrong version

**Solution:**

1. **Ensure webdriver-manager is Installed:**
   ```yaml
   - name: Install dependencies
     run: pip install -r requirements.txt  # Includes webdriver-manager==4.0.1
   ```

2. **Install Browser on CI Runner:**
   ```yaml
   # Chrome is pre-installed on ubuntu-latest
   
   # For Firefox
   - name: Setup Firefox
     uses: browser-actions/setup-firefox@latest
   ```

3. **Explicit Driver Installation:**
   ```yaml
   - name: Install ChromeDriver
     run: |
       python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
   ```

**Source:** `requirements.txt` line 26 (webdriver-manager==4.0.1)

## See Also

**Related Documentation:**
- [Local Development Setup](local-development.md) - Setting up local environment
- [Docker Deployment](docker.md) - Container-based deployment
- [Jenkins Integration](jenkins-integration.md) - Jenkins CI/CD pipeline
- [GitLab CI](gitlab-ci.md) - GitLab CI/CD configuration

**API Reference:**
- [Configuration Management](../reference/configuration-options.md) - config.yaml reference
- [Environment Variables](../reference/environment-variables.md) - .env reference
- [Behave Configuration](../reference/behave-configuration.md) - behave.ini reference

**Guides:**
- [Parallel Execution](../guides/parallel-execution.md) - Thread-safe parallel testing
- [Configuration Management](../guides/configuration-management.md) - Advanced configuration
- [Screenshot Management](../guides/screenshot-management.md) - Handling test artifacts

**External Resources:**
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Behave Documentation](https://behave.readthedocs.io/)
- [Selenium Python Documentation](https://selenium-dev.github.io/selenium/docs/api/py/)

---

**Source References:**
- `requirements.txt` - Python dependencies (lines 1-91)
- `behave.ini` - Behave configuration (lines 1-200)
- `config/config.yaml` - Application configuration (lines 1-163)
- `.env.example` - Environment variable template (lines 1-31)

