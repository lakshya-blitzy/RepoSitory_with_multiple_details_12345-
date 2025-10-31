# GitLab CI/CD Integration Guide

## Overview

GitLab CI/CD provides a comprehensive, integrated DevOps platform for automated test execution with native support for the Testinium Python Behave test automation framework. This guide covers complete pipeline configuration for continuous integration and deployment of test suites.

### Why GitLab CI/CD?

**Key Advantages:**

- **Integrated DevOps Platform:** Built-in CI/CD, container registry, and package management in a single platform
- **GitLab Runner Support:** Flexible executor options (Docker, Kubernetes, shell, SSH) with auto-scaling
- **Merge Request Integration:** Automated test execution on merge requests with inline test result visualization
- **Comprehensive Pipeline Visualization:** DAG-based pipeline views, stage dependencies, and detailed job logs
- **Native Container Registry:** Build and store Docker images in GitLab without external registry
- **GitLab Pages:** Free static site hosting for test reports and documentation
- **Advanced Caching:** Distributed cache with S3/GCS backend for faster dependency restoration
- **Security Integration:** Built-in secret management, protected variables, and masked credentials

### What You'll Learn

This guide covers:

- Complete `.gitlab-ci.yml` pipeline configuration
- Multi-stage pipeline design (setup, test, report, deploy)
- Parallel test execution with matrix builds
- CI/CD variable and secret management
- Artifact and cache optimization
- GitLab Pages deployment for test reports
- Merge request pipeline integration
- Troubleshooting common GitLab CI issues

## Prerequisites

Before configuring GitLab CI/CD for your test framework, ensure:

### Required Setup

1. **GitLab Project with CI/CD Enabled**
   - GitLab.com (SaaS) or self-hosted GitLab instance (14.0+)
   - CI/CD pipelines enabled in project settings (Settings → General → Visibility → Pipelines)
   - Push access to repository

2. **GitLab Runner Configured**
   - At least one GitLab Runner registered with your project or group
   - Docker executor configured and tested
   - Runner tags documented for job targeting
   - Verify runner status: Settings → CI/CD → Runners

3. **.gitlab-ci.yml Understanding**
   - Familiarity with YAML syntax
   - Understanding of GitLab CI/CD stages and jobs
   - Knowledge of Docker basics (images, containers, volumes)

4. **Protected Branches Setup**
   - Main/master branch configured as protected
   - Merge request approval rules (optional but recommended)
   - Branch protection rules: Settings → Repository → Protected Branches

### Optional Enhancements

- **GitLab Container Registry:** For custom test runner images
- **GitLab Pages:** For hosting test reports
- **Slack/Email Notifications:** For pipeline status alerts
- **Shared Runners:** GitLab.com provides free shared runners (limited minutes)

## Complete `.gitlab-ci.yml` Configuration

### Basic Pipeline Structure

Create `.gitlab-ci.yml` in your repository root with the following structure:

```yaml
# GitLab CI/CD Pipeline Configuration for Testinium Python Behave Framework
# Automated test execution with parallel support and comprehensive reporting

# =============================================================================
# Global Configuration
# =============================================================================

# Default Docker image for all jobs (can be overridden per job)
image: python:3.11-slim

# Global environment variables available to all jobs
variables:
  # Browser configuration
  BROWSER_TYPE: chrome
  HEADLESS: "true"
  
  # pip caching configuration for faster dependency installation
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  
  # Python optimization
  PYTHONUNBUFFERED: "1"
  PYTHONDONTWRITEBYTECODE: "1"

# Pipeline stages executed in order
stages:
  - setup
  - test
  - report
  - deploy

# Common setup commands executed before each job script
before_script:
  - python --version
  - pip --version
  - echo "Pipeline ID - $CI_PIPELINE_ID | Job ID - $CI_JOB_ID"

# =============================================================================
# Stage 1: Setup - Dependency Installation and Environment Preparation
# =============================================================================

install_dependencies:
  stage: setup
  script:
    # Create and activate virtual environment
    - python -m venv venv
    - source venv/bin/activate
    
    # Upgrade pip to latest version
    - pip install --upgrade pip
    
    # Install project dependencies
    - pip install -r requirements.txt
    
    # Verify key packages
    - pip list | grep -E "(selenium|behave|pytest|allure)"
    
    # Create .env file from CI/CD variables
    - |
      cat > .env << EOF
      BROWSER_TYPE=${BROWSER_TYPE}
      HEADLESS=${HEADLESS}
      BASE_URL=${BASE_URL}
      TEST_USERNAME=${TEST_USERNAME}
      TEST_PASSWORD=${TEST_PASSWORD}
      SALES_MANAGER_USERNAME=${SALES_MANAGER_USERNAME}
      SALES_MANAGER_PASSWORD=${SALES_MANAGER_PASSWORD}
      POS_MANAGER_USERNAME=${POS_MANAGER_USERNAME}
      POS_MANAGER_PASSWORD=${POS_MANAGER_PASSWORD}
      EOF
    
    # Display configuration (without sensitive values)
    - echo "Configuration loaded - Browser: ${BROWSER_TYPE}, Headless: ${HEADLESS}"
  
  # Cache virtual environment and pip packages for subsequent jobs
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .cache/pip
      - venv/
  
  # Store virtual environment as artifact for test stages
  artifacts:
    paths:
      - venv/
      - .env
    expire_in: 1 hour

# =============================================================================
# Stage 2: Test - Execute Test Suites
# =============================================================================

chrome_tests:
  stage: test
  needs: [install_dependencies]
  variables:
    BROWSER_TYPE: chrome
  script:
    - source venv/bin/activate
    - behave --tags=@Smoke --junit --junit-directory=reports/junit
    - behave --tags=@Regression --junit --junit-directory=reports/junit
  artifacts:
    paths:
      - reports/
    reports:
      junit: reports/junit/*.xml
    expire_in: 1 week
    when: always
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .cache/pip
      - venv/
    policy: pull

firefox_tests:
  stage: test
  needs: [install_dependencies]
  variables:
    BROWSER_TYPE: firefox
  script:
    - source venv/bin/activate
    - behave --tags=@Smoke --junit --junit-directory=reports/junit-firefox
  artifacts:
    paths:
      - reports/
    reports:
      junit: reports/junit-firefox/*.xml
    expire_in: 1 week
    when: always
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .cache/pip
      - venv/
    policy: pull
  allow_failure: true  # Optional: Don't block pipeline on Firefox failures

smoke_tests:
  stage: test
  needs: [install_dependencies]
  tags:
    - docker
    - high-memory
  script:
    - source venv/bin/activate
    - behave --tags=@Smoke --format=json --outfile=reports/smoke-tests.json
    - behave --tags=@Smoke --junit --junit-directory=reports/junit-smoke
  artifacts:
    paths:
      - reports/
    reports:
      junit: reports/junit-smoke/*.xml
    expire_in: 1 week
    when: always
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .cache/pip
      - venv/
    policy: pull
  only:
    - merge_requests
    - main
    - develop

regression_tests:
  stage: test
  needs: [install_dependencies]
  script:
    - source venv/bin/activate
    - behave --tags=@Regression --junit --junit-directory=reports/junit-regression
  artifacts:
    paths:
      - reports/
    reports:
      junit: reports/junit-regression/*.xml
    expire_in: 1 week
    when: always
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .cache/pip
      - venv/
    policy: pull
  only:
    - schedules
    - main

# =============================================================================
# Stage 3: Report - Generate and Consolidate Test Reports
# =============================================================================

generate_reports:
  stage: report
  needs:
    - chrome_tests
    - firefox_tests
    - smoke_tests
  script:
    - source venv/bin/activate
    
    # Generate Allure report
    - pip install allure-behave
    - allure generate reports/allure-results -o reports/allure-report --clean
    
    # Consolidate HTML reports
    - mkdir -p public/reports
    - cp -r reports/allure-report public/reports/allure
    - cp -r reports/behave-reports public/reports/behave
    - cp -r reports/screenshots public/reports/screenshots
    
    # Generate index page for reports
    - |
      cat > public/index.html << 'EOF'
      <!DOCTYPE html>
      <html>
      <head>
        <title>Test Reports - Pipeline ${CI_PIPELINE_ID}</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; }
          h1 { color: #333; }
          .report-link { 
            display: block; 
            margin: 10px 0; 
            padding: 15px; 
            background: #f5f5f5; 
            text-decoration: none; 
            color: #007bff; 
            border-radius: 5px;
          }
          .report-link:hover { background: #e9ecef; }
        </style>
      </head>
      <body>
        <h1>Test Execution Reports</h1>
        <p>Pipeline ID: ${CI_PIPELINE_ID} | Build: ${CI_COMMIT_SHORT_SHA}</p>
        <a href="reports/allure/index.html" class="report-link">Allure Report</a>
        <a href="reports/behave/index.html" class="report-link">Behave HTML Report</a>
        <a href="reports/screenshots/" class="report-link">Failure Screenshots</a>
      </body>
      </html>
      EOF
    
    # Display report summary
    - echo "Reports generated successfully"
    - find public/reports -name "*.html" | head -10
  
  artifacts:
    paths:
      - public/
    expire_in: 30 days
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .cache/pip
      - venv/
    policy: pull

# =============================================================================
# Stage 4: Deploy - Publish Reports to GitLab Pages
# =============================================================================

pages:
  stage: deploy
  needs: [generate_reports]
  script:
    - echo "Deploying reports to GitLab Pages"
    - ls -la public/
  artifacts:
    paths:
      - public
  only:
    - main
  environment:
    name: production
    url: https://$CI_PROJECT_NAMESPACE.gitlab.io/$CI_PROJECT_NAME
```

**Source Configuration:** `behave.ini:34-37`, `config/config.yaml:23-38`, `.env.example:5-7`

## Stages and Jobs Configuration

### Understanding GitLab CI/CD Stages

GitLab pipelines organize jobs into **stages** that execute sequentially. Jobs within the same stage run in parallel.

```mermaid
graph LR
    A[setup] --> B[test]
    B --> C[report]
    C --> D[deploy]
    
    B1[chrome_tests] -.parallel.-> B
    B2[firefox_tests] -.parallel.-> B
    B3[smoke_tests] -.parallel.-> B
    B4[regression_tests] -.parallel.-> B
```

### Stage 1: Setup Stage

**Purpose:** Install dependencies and prepare test environment

```yaml
install_dependencies:
  stage: setup
  script:
    - python -m venv venv
    - source venv/bin/activate
    - pip install --upgrade pip
    - pip install -r requirements.txt
    
    # Create .env file from CI/CD variables
    - |
      cat > .env << EOF
      BROWSER_TYPE=${BROWSER_TYPE}
      HEADLESS=${HEADLESS}
      BASE_URL=${BASE_URL}
      TEST_USERNAME=${TEST_USERNAME}
      TEST_PASSWORD=${TEST_PASSWORD}
      SALES_MANAGER_USERNAME=${SALES_MANAGER_USERNAME}
      SALES_MANAGER_PASSWORD=${SALES_MANAGER_PASSWORD}
      POS_MANAGER_USERNAME=${POS_MANAGER_USERNAME}
      POS_MANAGER_PASSWORD=${POS_MANAGER_PASSWORD}
      EOF
  
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .cache/pip
      - venv/
  
  artifacts:
    paths:
      - venv/
      - .env
    expire_in: 1 hour
```

**Key Features:**
- Virtual environment creation for dependency isolation
- Environment file generation from CI/CD variables
- Caching of pip packages and virtual environment
- Artifacts passed to subsequent stages

**Source:** `requirements.txt:1-91`, `.env.example:1-31`

### Stage 2: Test Stage

**Purpose:** Execute test suites in parallel across different configurations

#### Browser-Specific Test Jobs

```yaml
chrome_tests:
  stage: test
  needs: [install_dependencies]
  variables:
    BROWSER_TYPE: chrome
  script:
    - source venv/bin/activate
    - behave --tags=@Smoke --junit --junit-directory=reports/junit
    - behave --tags=@Regression --junit --junit-directory=reports/junit
  artifacts:
    paths:
      - reports/
    reports:
      junit: reports/junit/*.xml
    expire_in: 1 week
    when: always
```

**Source:** `behave.ini:34-37`, `config/config.yaml:23-26`

#### Tag-Based Test Execution

```yaml
smoke_tests:
  stage: test
  needs: [install_dependencies]
  tags:
    - docker
    - high-memory
  script:
    - source venv/bin/activate
    - behave --tags=@Smoke --format=json --outfile=reports/smoke-tests.json
  only:
    - merge_requests
    - main
    - develop
```

**Source:** `behave.ini:59-62`

### Stage 3: Report Stage

**Purpose:** Generate comprehensive test reports from execution results

```yaml
generate_reports:
  stage: report
  needs:
    - chrome_tests
    - firefox_tests
    - smoke_tests
  script:
    - source venv/bin/activate
    - pip install allure-behave
    - allure generate reports/allure-results -o reports/allure-report --clean
    
    # Consolidate reports into public directory for GitLab Pages
    - mkdir -p public/reports
    - cp -r reports/allure-report public/reports/allure
    - cp -r reports/behave-reports public/reports/behave
    - cp -r reports/screenshots public/reports/screenshots
  
  artifacts:
    paths:
      - public/
    expire_in: 30 days
```

**Source:** `behave.ini:78-82`, `config/config.yaml:113-139`

### Stage 4: Deploy Stage

**Purpose:** Publish reports to GitLab Pages

```yaml
pages:
  stage: deploy
  needs: [generate_reports]
  script:
    - echo "Deploying reports to GitLab Pages"
    - ls -la public/
  artifacts:
    paths:
      - public
  only:
    - main
  environment:
    name: production
    url: https://$CI_PROJECT_NAMESPACE.gitlab.io/$CI_PROJECT_NAME
```

## Job Template with Detailed Specifications

### Complete Job Definition

A comprehensive job template with all available options:

```yaml
test_job_template:
  # Docker image for this specific job (overrides global image)
  image: python:3.11-slim
  
  # Stage assignment (required)
  stage: test
  
  # Job dependencies (parallel execution within stage)
  needs:
    - install_dependencies
  
  # Runner tags for executor selection
  tags:
    - docker
    - linux
    - high-memory
  
  # Job-specific environment variables
  variables:
    BROWSER_TYPE: chrome
    HEADLESS: "true"
    PYTEST_WORKERS: "4"
  
  # Additional Docker services (for complex scenarios)
  services:
    - name: selenium/standalone-chrome:latest
      alias: selenium-chrome
  
  # Main job execution script
  script:
    # Activate virtual environment
    - source venv/bin/activate
    
    # Run tests with behave
    - |
      behave \
        --tags=@Smoke \
        --junit \
        --junit-directory=reports/junit \
        --format=allure_behave.formatter:AllureFormatter \
        --outfile=reports/allure-results \
        --format=json \
        --outfile=reports/cucumber.json
    
    # Generate reports
    - allure generate reports/allure-results -o reports/allure-report
  
  # Artifact configuration
  artifacts:
    # Paths to preserve
    paths:
      - reports/
      - .env
    
    # JUnit XML integration for GitLab test visualization
    reports:
      junit: reports/junit/*.xml
    
    # Artifact retention period
    expire_in: 1 week
    
    # Preserve artifacts even on job failure
    when: always
  
  # Cache configuration
  cache:
    # Cache key (unique per branch)
    key: ${CI_COMMIT_REF_SLUG}
    
    # Paths to cache
    paths:
      - .cache/pip
      - venv/
    
    # Cache policy: pull-push (default), pull, push
    policy: pull
  
  # Execution rules
  only:
    # Branches
    - main
    - develop
    
    # Tags
    - /^v\d+\.\d+\.\d+$/
    
    # Merge requests
    - merge_requests
  
  except:
    # Exclude specific branches
    - /^wip-/
  
  # Alternative rules syntax (more powerful)
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: always
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: always
    - when: manual
  
  # Retry configuration
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
  
  # Timeout (maximum job execution time)
  timeout: 1h
  
  # Allow job to fail without blocking pipeline
  allow_failure: false
  
  # Environment deployment
  environment:
    name: staging
    url: https://staging.example.com
```

**Source:** `behave.ini:95-128`

## Parallel Execution Strategies

### Strategy 1: Parallel Keyword for Job Instances

Create multiple identical job instances:

```yaml
parallel_smoke_tests:
  stage: test
  script:
    - source venv/bin/activate
    - behave --tags=@Smoke
  parallel: 5  # Creates 5 identical jobs
```

**Result:** GitLab creates jobs `parallel_smoke_tests 1/5`, `parallel_smoke_tests 2/5`, ..., `parallel_smoke_tests 5/5`

### Strategy 2: Matrix Builds for Multi-Dimensional Testing

Test across multiple Python versions and browsers:

```yaml
matrix_tests:
  stage: test
  image: python:${PYTHON_VERSION}
  variables:
    BROWSER_TYPE: ${BROWSER}
  script:
    - python -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
    - behave --tags=@Smoke
  parallel:
    matrix:
      - PYTHON_VERSION: ["3.9", "3.10", "3.11", "3.12"]
        BROWSER: [chrome, firefox]
```

**Result:** GitLab creates 8 jobs (4 Python versions × 2 browsers)

**Job Names:**
- `matrix_tests: [3.9, chrome]`
- `matrix_tests: [3.9, firefox]`
- `matrix_tests: [3.10, chrome]`
- ...and so on

**Source:** `behave.ini:95-128`

### Strategy 3: Split Tests by Tag with Node Index

Distribute tests across parallel workers:

```yaml
parallel_tag_tests:
  stage: test
  script:
    - source venv/bin/activate
    - |
      # Define test tags
      TAGS=("@Login" "@Logout" "@Calendar" "@Contact" "@CRM" "@Employee" "@Inventory" "@Notes" "@Sales" "@Session")
      
      # Calculate tag index for this parallel instance
      TAG_INDEX=$(( $CI_NODE_INDEX - 1 ))
      SELECTED_TAG=${TAGS[$TAG_INDEX]}
      
      echo "Running tests with tag: $SELECTED_TAG"
      behave --tags=$SELECTED_TAG
  parallel: 10  # One job per tag
```

**Source:** `behave.ini:95-128`

### Strategy 4: Feature-Level Parallelism

Run each feature file in a separate job:

```yaml
.parallel_feature_template: &parallel_feature
  stage: test
  script:
    - source venv/bin/activate
    - behave features/${FEATURE_FILE}
  artifacts:
    reports:
      junit: reports/junit/*.xml
    when: always

login_feature:
  <<: *parallel_feature
  variables:
    FEATURE_FILE: Login.feature

crm_feature:
  <<: *parallel_feature
  variables:
    FEATURE_FILE: Crm.feature

employee_feature:
  <<: *parallel_feature
  variables:
    FEATURE_FILE: EmployeeFc.feature
```

## CI/CD Variables and Secrets

### Defining Variables in Project Settings

**Navigate to:** Settings → CI/CD → Variables → Expand

**Add Variables:**

| Variable Key | Value | Type | Protected | Masked |
|--------------|-------|------|-----------|--------|
| `BASE_URL` | `https://testinium.example.com` | Variable | No | No |
| `TEST_USERNAME` | `testuser@example.com` | Variable | Yes | No |
| `TEST_PASSWORD` | `secure_password` | Variable | Yes | Yes |
| `SALES_MANAGER_USERNAME` | `salesmanager@example.com` | Variable | Yes | No |
| `SALES_MANAGER_PASSWORD` | `secure_password` | Variable | Yes | Yes |
| `POS_MANAGER_USERNAME` | `posmanager@example.com` | Variable | Yes | No |
| `POS_MANAGER_PASSWORD` | `secure_password` | Variable | Yes | Yes |

**Source:** `config/config.yaml:93-110`, `.env.example:16-28`

### Variable Types

**1. Environment Variable (env_var)**
- Default type
- Accessible as environment variable in job
- Usage: `echo $VARIABLE_NAME`

**2. File Variable**
- Value written to temporary file
- Path stored in environment variable
- Usage: `cat $VARIABLE_NAME`
- Use case: Certificates, configuration files

**Example File Variable:**
```yaml
variables:
  DATABASE_CONFIG:
    value: |
      {
        "host": "localhost",
        "port": 5432,
        "database": "test_db"
      }
    description: "Database configuration JSON"
```

### Protected and Masked Variables

**Protected Variables:**
- Only available to jobs running on protected branches or protected tags
- Prevents accidental credential exposure in feature branches
- **Use for:** Production credentials, API keys

**Masked Variables:**
- Value hidden in job logs (replaced with `[masked]`)
- Prevents credential leakage in console output
- **Requirements:** Minimum 8 characters, single-line, alphanumeric + `@:_.`

### Accessing Variables in Pipeline

**In .gitlab-ci.yml:**
```yaml
test_with_variables:
  script:
    - echo "Testing against: $BASE_URL"
    - echo "Username: $TEST_USERNAME"
    - behave -D base_url=$BASE_URL -D username=$TEST_USERNAME
```

**In Python code (via os.environ):**
```python
import os

base_url = os.getenv('BASE_URL')
username = os.getenv('TEST_USERNAME')
password = os.getenv('TEST_PASSWORD')
```

**Source:** `config/config.yaml:67-71`, `.env.example:9-10`

### Environment-Specific Variables

Use GitLab environments to manage different configuration sets:

```yaml
deploy_staging:
  stage: deploy
  script:
    - echo "Deploying to staging"
  environment:
    name: staging
    url: https://staging.example.com
  variables:
    BASE_URL: https://staging.example.com
  only:
    - develop

deploy_production:
  stage: deploy
  script:
    - echo "Deploying to production"
  environment:
    name: production
    url: https://testinium.example.com
  variables:
    BASE_URL: https://testinium.example.com
  only:
    - main
```

## Artifact Management

### Artifact Paths Configuration

Preserve test results and reports:

```yaml
test_job:
  script:
    - behave --junit --junit-directory=reports/junit
  artifacts:
    paths:
      - reports/              # All reports
      - reports/junit/*.xml    # Specific JUnit files
      - reports/screenshots/   # Failure screenshots
      - reports/allure-results/ # Allure raw results
      - .env                   # Environment configuration (for debugging)
    expire_in: 1 week          # Retention period
    when: always               # Preserve even on failure
```

**Source:** `behave.ini:34-37`, `config/config.yaml:125-139`

### JUnit Report Integration

Enable test result visualization in GitLab merge requests:

```yaml
test_job:
  artifacts:
    reports:
      junit: reports/junit/*.xml
```

**Features:**
- Test pass/fail counts in merge request widget
- Failed test details with stack traces
- Test trend charts over time
- Direct links to failed tests in job logs

**Source:** `behave.ini:34-37`

### Artifact Passing Between Stages

Use `dependencies` or `needs` to pass artifacts:

```yaml
# Stage 1: Generate test results
run_tests:
  stage: test
  script:
    - behave --junit --junit-directory=reports/junit
  artifacts:
    paths:
      - reports/

# Stage 2: Generate reports (depends on run_tests artifacts)
generate_reports:
  stage: report
  needs:
    - run_tests  # Automatically downloads run_tests artifacts
  script:
    - allure generate reports/allure-results -o reports/allure-report
```

### Downloading Artifacts

**Via GitLab UI:**
1. Navigate to: CI/CD → Pipelines → [Pipeline ID] → [Job Name]
2. Click "Browse" button to explore artifacts
3. Click "Download" button to download artifact archive

**Via GitLab API:**
```bash
# Download artifacts from latest successful pipeline
curl --header "PRIVATE-TOKEN: <your_access_token>" \
     "https://gitlab.example.com/api/v4/projects/<project_id>/jobs/artifacts/main/download?job=test_job" \
     --output artifacts.zip
```

### Artifact Expiration

Configure retention based on importance:

```yaml
artifacts:
  paths:
    - reports/
  expire_in: 1 week  # Options: never, 1 day, 1 week, 1 month, 1 year
```

**Best Practices:**
- **Smoke test results:** 1 week
- **Regression test results:** 1 month
- **Release test results:** 1 year or never
- **Debug artifacts:** 3 days

## Caching for Performance

### Cache Key Strategies

**Per-Branch Caching:**
```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}  # Unique key per branch
  paths:
    - .cache/pip
    - venv/
```

**Per-Job Caching:**
```yaml
cache:
  key: ${CI_JOB_NAME}  # Unique key per job
  paths:
    - .cache/pip
```

**Composite Cache Key:**
```yaml
cache:
  key: 
    files:
      - requirements.txt  # Cache invalidated when requirements.txt changes
  paths:
    - .cache/pip
    - venv/
```

### Cache Paths

**Recommended Paths for Python Projects:**

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .cache/pip/          # pip package cache
    - venv/                # Virtual environment
    - .pytest_cache/       # pytest cache
    - .mypy_cache/         # mypy type checking cache
```

**Source:** `requirements.txt:1-91`

### Cache Policy

Control cache read/write behavior:

```yaml
# Default: pull-push (download cache, run job, upload cache)
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - venv/
  policy: pull-push

# Pull only (download cache, don't upload)
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - venv/
  policy: pull

# Push only (don't download cache, upload after job)
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - venv/
  policy: push
```

**Use Cases:**
- **pull-push:** Setup/dependency installation jobs
- **pull:** Test execution jobs (read-only cache)
- **push:** Initial cache population jobs

### Distributed Cache with S3/GCS

Configure GitLab Runner for distributed caching (requires runner configuration):

**config.toml (on GitLab Runner):**
```toml
[[runners]]
  [runners.cache]
    Type = "s3"
    Shared = true
    [runners.cache.s3]
      ServerAddress = "s3.amazonaws.com"
      AccessKey = "AKIAIOSFODNN7EXAMPLE"
      SecretKey = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
      BucketName = "gitlab-runner-cache"
      BucketLocation = "us-east-1"
```

**Benefits:**
- Shared cache across multiple runners
- Faster cache restoration
- Reduced runner disk usage

## Docker Integration

### Using Additional Services

Run Selenium Grid alongside tests:

```yaml
test_with_selenium_grid:
  stage: test
  services:
    - name: selenium/standalone-chrome:latest
      alias: selenium-chrome
    - name: selenium/standalone-firefox:latest
      alias: selenium-firefox
  variables:
    SELENIUM_REMOTE_URL: "http://selenium-chrome:4444/wd/hub"
  script:
    - source venv/bin/activate
    - behave --tags=@Smoke
```

**Service Configuration:**
- `name`: Docker image for service
- `alias`: DNS alias for service communication
- Services run in parallel with job container
- Services destroyed after job completion

**Source:** `config/config.yaml:23-26`

### Custom Docker Image from GitLab Container Registry

Build and use custom test runner image:

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy test framework
COPY . .

# Set entrypoint
CMD ["behave"]
```

**.gitlab-ci.yml:**
```yaml
stages:
  - build
  - test

build_test_image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  only:
    - main

test_with_custom_image:
  stage: test
  image: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  script:
    - behave --tags=@Smoke
```

**Source:** `requirements.txt:1-91`

### Building Test Image in Pipeline

Optimize image builds with layer caching:

```yaml
build_optimized_image:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_DRIVER: overlay2
    DOCKER_BUILDKIT: 1
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    # Pull previous image for layer caching
    - docker pull $CI_REGISTRY_IMAGE:latest || true
    
    # Build with cache
    - |
      docker build \
        --cache-from $CI_REGISTRY_IMAGE:latest \
        --tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA \
        --tag $CI_REGISTRY_IMAGE:latest \
        .
    
    # Push images
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
```

## Merge Request Integration

### Merge Request Pipelines

Automatically run tests on merge requests:

```yaml
mr_smoke_tests:
  stage: test
  script:
    - source venv/bin/activate
    - behave --tags=@Smoke
  only:
    - merge_requests
```

**Alternative with rules:**
```yaml
mr_smoke_tests:
  stage: test
  script:
    - source venv/bin/activate
    - behave --tags=@Smoke
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: always
```

### Merge Request Widgets

Test results appear in merge request widgets:

**JUnit Test Results:**
```yaml
test_job:
  artifacts:
    reports:
      junit: reports/junit/*.xml
```

**Merge Request View:**
- ✅ Tests passed: 45/50
- ❌ Tests failed: 5/50
- Expandable list of failed tests with error messages

### Code Quality Reports

Integrate code quality checks:

```yaml
code_quality:
  stage: test
  image: python:3.11
  script:
    - pip install pylint black mypy
    - pylint **/*.py --output-format=json > code-quality-report.json || true
  artifacts:
    reports:
      codequality: code-quality-report.json
```

### Coverage Reports

Track test coverage in merge requests:

```yaml
test_with_coverage:
  stage: test
  script:
    - pip install pytest-cov
    - pytest --cov=. --cov-report=xml:coverage.xml
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
```

### Merge When Pipeline Succeeds

**Project Settings:** Settings → Merge Requests → Merge checks

Enable options:
- ☑ **Pipelines must succeed:** Block merge if pipeline fails
- ☑ **All threads must be resolved:** Require discussion resolution
- ☑ **Require approval from code owners:** Enforce code review

## GitLab Pages Deployment for Reports

### Pages Job Specification

Deploy test reports to GitLab Pages:

```yaml
pages:
  stage: deploy
  needs: [generate_reports]
  script:
    # GitLab Pages serves content from 'public' directory
    - echo "Deploying to GitLab Pages"
    - ls -la public/
  artifacts:
    paths:
      - public  # REQUIRED: Must be named 'public'
  only:
    - main  # Only deploy from main branch
  environment:
    name: production
    url: https://$CI_PROJECT_NAMESPACE.gitlab.io/$CI_PROJECT_NAME
```

**Requirements:**
- Job must be named `pages`
- Artifacts must include `public/` directory
- Only one `pages` job per pipeline

**Source:** `behave.ini:78-82`

### Public Directory Structure

Organize reports in public directory:

```bash
public/
├── index.html              # Landing page
├── reports/
│   ├── allure/
│   │   └── index.html      # Allure report
│   ├── behave/
│   │   └── index.html      # Behave HTML report
│   └── screenshots/        # Failure screenshots
│       ├── login_failure_2024-01-15.png
│       └── ...
└── assets/
    ├── css/
    └── js/
```

### Accessing GitLab Pages

**URL Format:**
```
https://<namespace>.gitlab.io/<project-name>
```

**Examples:**
- User project: `https://johndoe.gitlab.io/testinium-qa`
- Group project: `https://testinium-group.gitlab.io/qa-automation`

**Direct Report Links:**
- Allure: `https://johndoe.gitlab.io/testinium-qa/reports/allure`
- Behave HTML: `https://johndoe.gitlab.io/testinium-qa/reports/behave`

### HTML Report Index Page

Create index.html for report navigation:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Reports - Testinium QA</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
        }
        .meta {
            color: #666;
            margin-bottom: 40px;
            font-size: 14px;
        }
        .report-link {
            display: block;
            margin: 20px 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: transform 0.2s, box-shadow 0.2s;
            font-size: 18px;
            font-weight: 500;
        }
        .report-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        .report-link .description {
            display: block;
            font-size: 14px;
            opacity: 0.9;
            margin-top: 5px;
            font-weight: normal;
        }
        .status {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 10px;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
        }
        .status.failure {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test Execution Reports</h1>
        <div class="meta">
            <span class="status success">Pipeline: ${CI_PIPELINE_ID}</span>
            <span class="status success">Commit: ${CI_COMMIT_SHORT_SHA}</span>
            <span class="status success">Branch: ${CI_COMMIT_REF_NAME}</span>
        </div>
        
        <a href="reports/allure/index.html" class="report-link">
            📊 Allure Report
            <span class="description">Comprehensive test results with trends, timelines, and categorization</span>
        </a>
        
        <a href="reports/behave/index.html" class="report-link">
            📝 Behave HTML Report
            <span class="description">Scenario-level test results with step details and screenshots</span>
        </a>
        
        <a href="reports/screenshots/" class="report-link">
            🖼️ Failure Screenshots
            <span class="description">Visual evidence of test failures for debugging</span>
        </a>
    </div>
</body>
</html>
```

### Allure Report Hosting

Generate and host Allure reports:

```yaml
generate_allure_report:
  stage: report
  script:
    - source venv/bin/activate
    - pip install allure-behave
    
    # Generate Allure report
    - allure generate reports/allure-results -o public/reports/allure --clean
    
    # Copy additional reports
    - mkdir -p public/reports/behave
    - cp -r reports/behave-reports/* public/reports/behave/
    - cp -r reports/screenshots public/reports/
  artifacts:
    paths:
      - public/
```

**Source:** `behave.ini:78-82`

## Advanced Pipeline Features

### Parent-Child Pipelines

Break complex pipelines into manageable components:

**Parent pipeline (.gitlab-ci.yml):**
```yaml
trigger_smoke_tests:
  stage: test
  trigger:
    include: .gitlab-ci-smoke.yml
    strategy: depend

trigger_regression_tests:
  stage: test
  trigger:
    include: .gitlab-ci-regression.yml
    strategy: depend
```

**Child pipeline (.gitlab-ci-smoke.yml):**
```yaml
smoke_chrome:
  stage: test
  script:
    - behave --tags=@Smoke

smoke_firefox:
  stage: test
  script:
    - behave --tags=@Smoke
  variables:
    BROWSER_TYPE: firefox
```

### Trigger Keyword for Downstream Pipelines

Trigger pipelines in other projects:

```yaml
trigger_integration_tests:
  stage: deploy
  trigger:
    project: testinium/integration-tests
    branch: main
    strategy: depend
  variables:
    UPSTREAM_COMMIT: $CI_COMMIT_SHA
    TEST_ENV: staging
```

### Include for Template Reuse

Share common configuration across files:

**templates/test-template.yml:**
```yaml
.test_template:
  stage: test
  image: python:3.11-slim
  before_script:
    - source venv/bin/activate
  script:
    - behave --tags=${TEST_TAG}
  artifacts:
    reports:
      junit: reports/junit/*.xml
```

**.gitlab-ci.yml:**
```yaml
include:
  - local: templates/test-template.yml

smoke_tests:
  extends: .test_template
  variables:
    TEST_TAG: "@Smoke"

regression_tests:
  extends: .test_template
  variables:
    TEST_TAG: "@Regression"
```

### Rules for Advanced Conditional Execution

**Run on Merge Requests:**
```yaml
mr_tests:
  script:
    - behave --tags=@Smoke
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: always
```

**Run on Main Branch:**
```yaml
main_branch_tests:
  script:
    - behave --tags=@Regression
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: always
```

**Run on Tags:**
```yaml
release_tests:
  script:
    - behave --tags=@Smoke,@Regression
  rules:
    - if: '$CI_COMMIT_TAG =~ /^v\d+\.\d+\.\d+$/'
      when: always
```

**Manual Trigger:**
```yaml
manual_tests:
  script:
    - behave --tags=@WIP
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
      when: manual
```

**Complex Conditions:**
```yaml
conditional_tests:
  script:
    - behave
  rules:
    # Run automatically on MR to main
    - if: '$CI_MERGE_REQUEST_TARGET_BRANCH_NAME == "main"'
      when: always
    
    # Run manually on feature branches
    - if: '$CI_COMMIT_BRANCH =~ /^feature-/'
      when: manual
    
    # Skip on WIP branches
    - if: '$CI_COMMIT_BRANCH =~ /^wip-/'
      when: never
    
    # Default: manual
    - when: manual
```

### Needs Keyword for DAG Pipelines

Create Directed Acyclic Graph (DAG) pipelines for faster execution:

```yaml
stages:
  - build
  - test
  - report

build_dependencies:
  stage: build
  script:
    - pip install -r requirements.txt

unit_tests:
  stage: test
  needs: [build_dependencies]
  script:
    - pytest tests/unit

integration_tests:
  stage: test
  needs: [build_dependencies]
  script:
    - pytest tests/integration

smoke_tests:
  stage: test
  needs: [build_dependencies]
  script:
    - behave --tags=@Smoke

generate_report:
  stage: report
  needs:
    - unit_tests
    - integration_tests
    - smoke_tests
  script:
    - allure generate reports/allure-results
```

**Without `needs`:** Jobs wait for all previous stage jobs to complete
**With `needs`:** Jobs start immediately after specified dependencies complete

**Result:** Faster pipeline execution through parallelization

## Monitoring and Notifications

### GitLab Pipeline Emails

**Enable in User Settings:**
1. Navigate to: User Settings → Notifications
2. Configure notification level:
   - **Global:** All events
   - **Watch:** All activity
   - **Participate:** Only assigned or mentioned
   - **Custom:** Configure per-event
3. Pipeline-specific settings:
   - ☑ Successful pipeline
   - ☑ Failed pipeline
   - ☑ Fixed pipeline

### Slack Notifications via Webhooks

**1. Create Slack Incoming Webhook:**
- Go to Slack App Directory → Incoming Webhooks
- Add to Slack workspace
- Select channel (e.g., #test-results)
- Copy Webhook URL

**2. Configure in .gitlab-ci.yml:**

```yaml
.notify_slack: &notify_slack
  - |
    curl -X POST -H 'Content-type: application/json' \
    --data "{
      \"text\": \"Pipeline <${CI_PIPELINE_URL}|#${CI_PIPELINE_ID}> ${STATUS}\",
      \"attachments\": [{
        \"color\": \"${COLOR}\",
        \"fields\": [
          {\"title\": \"Project\", \"value\": \"${CI_PROJECT_NAME}\", \"short\": true},
          {\"title\": \"Branch\", \"value\": \"${CI_COMMIT_REF_NAME}\", \"short\": true},
          {\"title\": \"Commit\", \"value\": \"<${CI_PROJECT_URL}/-/commit/${CI_COMMIT_SHA}|${CI_COMMIT_SHORT_SHA}>\", \"short\": true},
          {\"title\": \"Author\", \"value\": \"${GITLAB_USER_NAME}\", \"short\": true}
        ]
      }]
    }" \
    ${SLACK_WEBHOOK_URL}

notify_success:
  stage: .post
  script:
    - export STATUS="✅ succeeded"
    - export COLOR="good"
    - *notify_slack
  when: on_success
  only:
    - main

notify_failure:
  stage: .post
  script:
    - export STATUS="❌ failed"
    - export COLOR="danger"
    - *notify_slack
  when: on_failure
  only:
    - main
```

**3. Store Webhook URL as CI/CD Variable:**
- Settings → CI/CD → Variables
- Add variable: `SLACK_WEBHOOK_URL` (masked)

### Custom Notification Scripts

**Email notification with test summary:**

```yaml
send_email_report:
  stage: .post
  script:
    - |
      python3 - <<EOF
      import smtplib
      from email.mime.multipart import MIMEMultipart
      from email.mime.text import MIMEText
      import os
      
      # Email configuration
      smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
      smtp_port = int(os.getenv('SMTP_PORT', '587'))
      sender_email = os.getenv('SENDER_EMAIL')
      sender_password = os.getenv('SENDER_PASSWORD')
      recipient_email = os.getenv('RECIPIENT_EMAIL')
      
      # Create message
      msg = MIMEMultipart()
      msg['From'] = sender_email
      msg['To'] = recipient_email
      msg['Subject'] = f"Test Results - Pipeline {os.getenv('CI_PIPELINE_ID')}"
      
      # Email body
      body = f"""
      Pipeline: {os.getenv('CI_PIPELINE_URL')}
      Branch: {os.getenv('CI_COMMIT_REF_NAME')}
      Commit: {os.getenv('CI_COMMIT_SHORT_SHA')}
      
      Status: {os.getenv('CI_JOB_STATUS')}
      
      View full report: https://{os.getenv('CI_PROJECT_NAMESPACE')}.gitlab.io/{os.getenv('CI_PROJECT_NAME')}
      """
      
      msg.attach(MIMEText(body, 'plain'))
      
      # Send email
      server = smtplib.SMTP(smtp_server, smtp_port)
      server.starttls()
      server.login(sender_email, sender_password)
      server.send_message(msg)
      server.quit()
      EOF
  when: always
```

### Pipeline Status Badges

Add pipeline status badge to README.md:

**Markdown:**
```markdown
[![Pipeline Status](https://gitlab.com/<namespace>/<project>/badges/main/pipeline.svg)](https://gitlab.com/<namespace>/<project>/-/commits/main)
```

**HTML:**
```html
<img src="https://gitlab.com/<namespace>/<project>/badges/main/pipeline.svg" alt="Pipeline Status">
```

**Coverage Badge:**
```markdown
[![Coverage](https://gitlab.com/<namespace>/<project>/badges/main/coverage.svg)](https://gitlab.com/<namespace>/<project>/-/commits/main)
```

## Troubleshooting

### Runner Not Picking Up Jobs

**Symptoms:**
- Jobs stuck in "pending" state
- No runner assigned to job

**Causes and Solutions:**

**1. No Available Runners**
- **Check:** Settings → CI/CD → Runners
- **Solution:** Register a new runner or ensure existing runners are online

**2. Tag Mismatch**
- **Check:** Job has `tags:` that don't match any runner tags
- **Solution:** Remove `tags:` from job or add tags to runner configuration

**3. Runner Paused**
- **Check:** Runner status in Settings → CI/CD → Runners
- **Solution:** Click "Resume" on paused runner

**4. Concurrent Job Limit Reached**
- **Check:** Runner configuration `concurrent` value
- **Solution:** Increase `concurrent` in `/etc/gitlab-runner/config.toml`

```toml
concurrent = 10  # Increase from default 1
```

### Docker Executor Issues

**Symptoms:**
- "Cannot connect to Docker daemon"
- "docker: command not found"
- Image pull failures

**Solutions:**

**1. Docker Daemon Not Running**
```yaml
# Ensure Docker-in-Docker service is included
services:
  - docker:dind

variables:
  DOCKER_HOST: tcp://docker:2376
  DOCKER_TLS_CERTDIR: "/certs"
```

**2. Docker Executor Not Configured**
- **Check:** Runner configuration uses Docker executor
- **Verify:** `/etc/gitlab-runner/config.toml`

```toml
[[runners]]
  executor = "docker"
  [runners.docker]
    image = "python:3.11-slim"
    privileged = false
    volumes = ["/cache"]
```

**3. Image Pull Authentication**
```yaml
# Login to GitLab Container Registry
before_script:
  - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
```

### Cache Not Restoring

**Symptoms:**
- Dependencies reinstalled every job
- Cache key mismatch warnings
- No cache download log

**Solutions:**

**1. Cache Key Mismatch**
```yaml
# Ensure consistent cache key across jobs
cache:
  key: ${CI_COMMIT_REF_SLUG}  # Use branch name
  paths:
    - .cache/pip
    - venv/
```

**2. Cache Paths Don't Exist**
```yaml
# Create directories before caching
script:
  - mkdir -p .cache/pip
  - python -m venv venv
```

**3. Cache Expired**
- **Default:** GitLab caches expire after 7 days of no access
- **Solution:** Rebuild cache or configure longer expiration (runner config)

**4. Distributed Cache Configuration**
- **Check:** Runner cache configuration in `/etc/gitlab-runner/config.toml`
- **Verify:** S3/GCS credentials and bucket access

### Artifacts Not Found

**Symptoms:**
- "No files to upload" warning
- Artifacts not available for download
- Missing artifacts in downstream jobs

**Solutions:**

**1. Artifacts Path Doesn't Exist**
```yaml
# Ensure paths are generated before artifact collection
script:
  - behave --junit --junit-directory=reports/junit
  - ls -la reports/  # Verify artifacts exist

artifacts:
  paths:
    - reports/
```

**2. Artifacts Expired**
```yaml
artifacts:
  paths:
    - reports/
  expire_in: 1 week  # Extend if needed
```

**3. Job Failed Before Artifact Upload**
```yaml
artifacts:
  paths:
    - reports/
  when: always  # Upload artifacts even on job failure
```

**4. Dependencies Missing**
```yaml
downstream_job:
  needs:
    - upstream_job  # Automatically downloads artifacts
```

### GitLab Pages 404 Error

**Symptoms:**
- Accessing GitLab Pages URL returns 404
- "The page you're looking for could not be found"

**Solutions:**

**1. Job Not Named 'pages'**
```yaml
# MUST be named 'pages'
pages:
  stage: deploy
  script:
    - echo "Deploying"
```

**2. Missing 'public' Directory**
```yaml
pages:
  script:
    - mkdir -p public
    - cp -r reports/* public/
  artifacts:
    paths:
      - public  # MUST be named 'public'
```

**3. Job Only Runs on Protected Branch**
```yaml
pages:
  only:
    - main  # Ensure job runs on correct branch
```

**4. GitLab Pages Not Enabled**
- **Check:** Settings → Pages
- **Enable:** GitLab Pages feature in project settings

### Parallel Job Failures

**Symptoms:**
- Some parallel jobs fail while others succeed
- Inconsistent test results across parallel jobs
- Race conditions or resource conflicts

**Solutions:**

**1. Shared State Issues**
```python
# Use thread-local storage for WebDriver
import threading

driver_storage = threading.local()

def get_driver():
    if not hasattr(driver_storage, 'driver'):
        driver_storage.driver = webdriver.Chrome()
    return driver_storage.driver
```

**Source:** `utilities/driver_manager.py` (implementation details)

**2. Test Data Conflicts**
```yaml
# Isolate test data per job
parallel_tests:
  parallel: 5
  script:
    - export TEST_USER="user_${CI_NODE_INDEX}"
    - behave --tags=@Smoke
```

**3. Resource Limits**
```yaml
# Increase job resources
parallel_tests:
  tags:
    - docker
    - high-memory  # Use runners with more resources
  parallel: 5
```

**4. Flaky Tests**
```yaml
# Add retry logic
parallel_tests:
  retry:
    max: 2
    when:
      - script_failure
```

### Secret Variable Not Accessible

**Symptoms:**
- Variable value is empty in job
- "Variable not found" error
- Tests fail due to missing credentials

**Solutions:**

**1. Variable Not Defined**
- **Check:** Settings → CI/CD → Variables
- **Verify:** Variable key matches exactly (case-sensitive)

**2. Protected Variable on Non-Protected Branch**
- **Check:** Variable is marked "Protected"
- **Solution:** Either:
  - Run job on protected branch (main, master)
  - Uncheck "Protected" flag (less secure)

**3. Variable Scope Mismatch**
- **Check:** Variable environment scope matches job environment
- **Solution:** Use `*` for all environments or define environment-specific variables

**4. Masked Variable Logging**
```yaml
# Variable is accessible but masked in logs
script:
  - echo $TEST_PASSWORD  # Shows [masked]
  - behave  # Variable IS available to tests
```

## See Also

### Related Documentation

- [Local Development Setup](local-development.md) - Run tests locally before CI/CD
- [Docker Deployment](docker.md) - Containerized test execution
- [Jenkins Integration](jenkins-integration.md) - Alternative CI/CD platform
- [GitHub Actions Integration](github-actions.md) - Alternative CI/CD platform
- [Report Publishing](report-publishing.md) - Advanced report hosting options

### External Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/) - Official GitLab CI/CD guide
- [GitLab Runner Documentation](https://docs.gitlab.com/runner/) - Runner installation and configuration
- [.gitlab-ci.yml Reference](https://docs.gitlab.com/ee/ci/yaml/) - Complete YAML syntax reference
- [GitLab Pages Documentation](https://docs.gitlab.com/ee/user/project/pages/) - Pages hosting guide
- [Behave Documentation](https://behave.readthedocs.io/) - BDD framework reference

### Framework Documentation

- [Configuration Management Guide](../guides/configuration-management.md) - Environment configuration
- [Parallel Execution Guide](../guides/parallel-execution.md) - Thread-safety and parallelization
- [Behave Configuration Reference](../reference/behave-configuration.md) - Complete behave.ini options

---

**Document Version:** 1.0  
**Last Updated:** 2024-01-15  
**Maintained By:** Testinium QA Team
