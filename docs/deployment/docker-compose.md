# Docker Compose Deployment Guide

## Overview

Docker Compose provides a powerful way to orchestrate multi-container test automation environments for the Testinium QA Python test automation framework. This guide covers everything you need to know about deploying and running tests using Docker Compose for complex testing scenarios.

### When to Use Docker Compose

Docker Compose is the ideal deployment solution when you need:

- **Multi-Browser Testing**: Run the same test suite simultaneously across Chrome, Firefox, and other browsers
- **Parallel Test Execution**: Scale test execution across multiple containers for faster feedback
- **Application + Tests Integration**: Run both the application under test and the test suite in an orchestrated environment
- **Complex Test Environments**: Manage multiple services with dependencies (database, API services, test runners)
- **Team Collaboration**: Share consistent, reproducible test environments across development teams
- **CI/CD Integration**: Deploy comprehensive testing pipelines with minimal configuration

### Advantages Over Single Container Deployment

| Feature | Docker (Single Container) | Docker Compose (Multi-Container) |
|---------|--------------------------|----------------------------------|
| Multi-browser testing | Manual container management | Automated with single command |
| Parallel execution | Limited to container resources | Scales across multiple containers |
| Service dependencies | Manual network configuration | Automatic service discovery |
| Report aggregation | Single container output | Consolidated multi-container reports |
| Environment complexity | Simple, single-service | Complex, multi-service orchestration |
| Setup overhead | Minimal | Higher initial setup, easier long-term |

## Prerequisites

Before proceeding with Docker Compose deployment, ensure you have:

### Required Software

- **Docker**: Version 20.10 or higher
  - Verify: `docker --version`
  - Installation: [docs/deployment/docker.md](./docker.md)
  
- **Docker Compose**: Version 2.0 or higher
  - Verify: `docker-compose --version` or `docker compose version`
  - Note: Docker Compose V2 is integrated into Docker CLI as `docker compose`

### Required Knowledge

- Basic understanding of Docker concepts (images, containers, volumes, networks)
- Familiarity with YAML syntax for docker-compose.yml configuration
- Understanding of the test automation framework structure
- Review [docs/deployment/docker.md](./docker.md) for single-container Docker basics

### System Requirements

- **RAM**: Minimum 8GB (16GB+ recommended for parallel execution)
- **CPU**: Multi-core processor (4+ cores recommended for parallel testing)
- **Disk Space**: 10GB+ for images, containers, and test reports
- **Network**: Internet access for pulling Docker images and accessing application under test

## Docker Compose Architecture

The following diagram illustrates the multi-container architecture managed by Docker Compose:

```mermaid
graph TB
    subgraph "Docker Compose Network: test-network"
        subgraph "Test Execution Services"
            ChromeTests["chrome-tests<br/>Selenium + Chrome<br/>Behave Test Runner"]
            FirefoxTests["firefox-tests<br/>Selenium + Firefox<br/>Behave Test Runner"]
            EdgeTests["edge-tests<br/>Selenium + Edge<br/>Behave Test Runner"]
        end
        
        subgraph "Application Services"
            App["app-under-test<br/>Web Application<br/>Port: 8080"]
            Database["database<br/>PostgreSQL/MySQL<br/>Test Data"]
        end
        
        subgraph "Shared Resources"
            Reports["shared-reports<br/>Volume Mount<br/>./reports:/app/reports"]
            Config["shared-config<br/>Volume Mount<br/>./config:/app/config"]
        end
    end
    
    ChromeTests -->|HTTP Requests| App
    FirefoxTests -->|HTTP Requests| App
    EdgeTests -->|HTTP Requests| App
    App -->|Query Data| Database
    
    ChromeTests -.->|Write Reports| Reports
    FirefoxTests -.->|Write Reports| Reports
    EdgeTests -.->|Write Reports| Reports
    
    ChromeTests -.->|Read Config| Config
    FirefoxTests -.->|Read Config| Config
    EdgeTests -.->|Read Config| Config
    
    style ChromeTests fill:#4285F4
    style FirefoxTests fill:#FF7139
    style EdgeTests fill:#0078D7
    style App fill:#00C853
    style Database fill:#336791
    style Reports fill:#FFA726
    style Config fill:#AB47BC
```

## Complete docker-compose.yml Configuration

Here's a comprehensive docker-compose.yml that demonstrates multi-browser testing with application integration:

```yaml
version: '3.8'

services:
  # =============================================================================
  # Chrome Test Execution Service
  # =============================================================================
  chrome-tests:
    build:
      context: .
      dockerfile: Dockerfile
    image: testinium-qa-python:latest
    container_name: testinium-chrome-tests
    environment:
      # Browser configuration from config/config.yaml
      BROWSER_TYPE: chrome
      HEADLESS: "true"
      
      # Application URL pointing to app service
      BASE_URL: http://app-under-test:8080
      
      # Credentials from environment variables (required)
      TEST_USERNAME: ${TEST_USERNAME}
      TEST_PASSWORD: ${TEST_PASSWORD}
      SALES_MANAGER_USERNAME: ${SALES_MANAGER_USERNAME}
      SALES_MANAGER_PASSWORD: ${SALES_MANAGER_PASSWORD}
      POS_MANAGER_USERNAME: ${POS_MANAGER_USERNAME}
      POS_MANAGER_PASSWORD: ${POS_MANAGER_PASSWORD}
      
      # Timeout configuration from config/config.yaml lines 45-60
      EXPLICIT_WAIT_TIMEOUT: "10"
      PAGE_LOAD_TIMEOUT: "30"
      
      # Reporting configuration
      SCREENSHOTS_ON_FAILURE: "true"
    volumes:
      # Shared volume for test reports
      - ./reports/chrome:/app/reports
      # Shared configuration files
      - ./config:/app/config:ro
      # Mount features for live editing during development
      - ./features:/app/features:ro
    networks:
      - test-network
    depends_on:
      app-under-test:
        condition: service_healthy
    command: >
      behave --tags=@Smoke
      -f json -o /app/reports/cucumber.json
      -f html -o /app/reports/report.html
      -f pretty
    restart: on-failure

  # =============================================================================
  # Firefox Test Execution Service
  # =============================================================================
  firefox-tests:
    build:
      context: .
      dockerfile: Dockerfile
    image: testinium-qa-python:latest
    container_name: testinium-firefox-tests
    environment:
      # Browser configuration - Firefox variant
      BROWSER_TYPE: firefox
      HEADLESS: "true"
      
      # Application URL pointing to app service
      BASE_URL: http://app-under-test:8080
      
      # Credentials (shared with chrome-tests)
      TEST_USERNAME: ${TEST_USERNAME}
      TEST_PASSWORD: ${TEST_PASSWORD}
      SALES_MANAGER_USERNAME: ${SALES_MANAGER_USERNAME}
      SALES_MANAGER_PASSWORD: ${SALES_MANAGER_PASSWORD}
      POS_MANAGER_USERNAME: ${POS_MANAGER_USERNAME}
      POS_MANAGER_PASSWORD: ${POS_MANAGER_PASSWORD}
      
      # Timeout configuration
      EXPLICIT_WAIT_TIMEOUT: "10"
      PAGE_LOAD_TIMEOUT: "30"
      
      # Reporting configuration
      SCREENSHOTS_ON_FAILURE: "true"
    volumes:
      # Separate report directory for Firefox results
      - ./reports/firefox:/app/reports
      - ./config:/app/config:ro
      - ./features:/app/features:ro
    networks:
      - test-network
    depends_on:
      app-under-test:
        condition: service_healthy
    command: >
      behave --tags=@Smoke
      -f json -o /app/reports/cucumber.json
      -f html -o /app/reports/report.html
      -f pretty
    restart: on-failure

  # =============================================================================
  # Application Under Test Service
  # =============================================================================
  app-under-test:
    image: your-application-image:latest
    container_name: testinium-app
    environment:
      # Application configuration
      DATABASE_URL: postgresql://testuser:testpass@database:5432/testdb
      APP_ENV: testing
    ports:
      - "8080:8080"
    networks:
      - test-network
    depends_on:
      database:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    restart: unless-stopped

  # =============================================================================
  # Database Service for Application
  # =============================================================================
  database:
    image: postgres:15-alpine
    container_name: testinium-db
    environment:
      POSTGRES_USER: testuser
      POSTGRES_PASSWORD: testpass
      POSTGRES_DB: testdb
    volumes:
      # Persist database data
      - db-data:/var/lib/postgresql/data
      # Load test data initialization scripts
      - ./database/init:/docker-entrypoint-initdb.d:ro
    networks:
      - test-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U testuser"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped

# =============================================================================
# Networks Configuration
# =============================================================================
networks:
  test-network:
    driver: bridge
    name: testinium-network

# =============================================================================
# Volumes Configuration
# =============================================================================
volumes:
  db-data:
    driver: local
```

**Source References:**
- Browser configuration: `config/config.yaml` lines 23-38
- Timeout settings: `config/config.yaml` lines 45-60
- Credentials: `config/config.yaml` lines 93-110
- Parallel execution patterns: `behave.ini` lines 95-128

## Service Configuration Details

### Environment Variables

Each test service requires specific environment variables for configuration:

#### Browser Configuration Variables

| Variable | Required | Values | Description |
|----------|----------|--------|-------------|
| `BROWSER_TYPE` | Yes | `chrome`, `firefox`, `edge` | Browser to use for test execution |
| `HEADLESS` | No | `true`, `false` | Run browser in headless mode (default: `true` for Docker) |
| `WINDOW_SIZE` | No | `1920x1080` | Browser window dimensions |

**Source:** `config/config.yaml` lines 23-38

#### Application Configuration Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BASE_URL` | Yes | None | Base URL of application under test |
| `EXPLICIT_WAIT_TIMEOUT` | No | `10` | Default explicit wait timeout in seconds |
| `PAGE_LOAD_TIMEOUT` | No | `30` | Maximum page load timeout in seconds |

**Source:** `config/config.yaml` lines 45-80

#### Credentials Variables

All credential variables are **required** and must be provided via environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `TEST_USERNAME` | Generic test user login | `test.user@example.com` |
| `TEST_PASSWORD` | Generic test user password | `SecurePass123!` |
| `SALES_MANAGER_USERNAME` | Sales manager role login | `sales.mgr@example.com` |
| `SALES_MANAGER_PASSWORD` | Sales manager password | `SalesPass123!` |
| `POS_MANAGER_USERNAME` | POS manager role login | `pos.mgr@example.com` |
| `POS_MANAGER_PASSWORD` | POS manager password | `PosPass123!` |

**Security Note:** Never hardcode credentials in docker-compose.yml. Always use environment variables or Docker secrets.

**Source:** `config/config.yaml` lines 93-110

#### Reporting Configuration Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SCREENSHOTS_ON_FAILURE` | No | `true` | Capture screenshots on test failure |
| `REPORT_FORMAT` | No | `json,html` | Report output formats |

### Volume Mounts

#### Report Volume Mounts

```yaml
volumes:
  # Browser-specific report directory
  - ./reports/chrome:/app/reports
  - ./reports/firefox:/app/reports
```

**Purpose:**
- Persist test reports outside containers
- Aggregate reports from multiple browser test runs
- Enable report access after containers are removed

**Report Types Generated:**
- JSON reports: `/app/reports/cucumber.json`
- HTML reports: `/app/reports/report.html`
- Screenshots: `/app/reports/screenshots/*.png`
- JUnit XML: `/app/reports/junit/*.xml` (if enabled)
- Allure results: `/app/reports/allure-results/*` (if configured)

#### Configuration Volume Mounts

```yaml
volumes:
  # Read-only configuration files
  - ./config:/app/config:ro
  - ./features:/app/features:ro
```

**Purpose:**
- Share configuration across all test containers
- Enable live editing of test configuration during development
- Read-only (`:ro`) prevents containers from modifying source files

### Network Configuration

```yaml
networks:
  test-network:
    driver: bridge
    name: testinium-network
```

**Purpose:**
- Enable communication between test containers and application
- Provide service discovery (containers can reach each other by service name)
- Isolate test environment from host network

**Service Discovery Examples:**
- Test containers access app: `http://app-under-test:8080`
- App accesses database: `postgresql://testuser:testpass@database:5432/testdb`

## Multi-Browser Testing

### Running Tests Across Multiple Browsers

Docker Compose makes multi-browser testing straightforward by running separate services for each browser:

```bash
# Run tests on all browsers simultaneously
docker-compose up chrome-tests firefox-tests

# View logs in real-time
docker-compose logs -f chrome-tests firefox-tests

# Check test results
ls -la reports/chrome/
ls -la reports/firefox/
```

### Multi-Browser Configuration Pattern

```yaml
# Pattern for adding additional browsers
edge-tests:
  build:
    context: .
    dockerfile: Dockerfile
  environment:
    BROWSER_TYPE: edge  # Change browser type
    HEADLESS: "true"
    BASE_URL: http://app-under-test:8080
    # ... other environment variables
  volumes:
    - ./reports/edge:/app/reports  # Browser-specific reports
    - ./config:/app/config:ro
  networks:
    - test-network
  depends_on:
    app-under-test:
      condition: service_healthy
  command: behave --tags=@Smoke
```

### Browser-Specific Test Execution

You can run different test tags on different browsers:

```yaml
# docker-compose.override.yml for custom test execution
services:
  chrome-tests:
    command: behave --tags=@Smoke,@Critical

  firefox-tests:
    command: behave --tags=@Smoke

  edge-tests:
    command: behave --tags=@Visual
```

**Usage:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

### Report Organization by Browser

```
reports/
├── chrome/
│   ├── cucumber.json
│   ├── report.html
│   ├── junit/
│   └── screenshots/
├── firefox/
│   ├── cucumber.json
│   ├── report.html
│   ├── junit/
│   └── screenshots/
└── edge/
    ├── cucumber.json
    ├── report.html
    ├── junit/
    └── screenshots/
```

## Parallel Test Execution

### Scaling Services for Parallel Execution

Docker Compose provides powerful scaling capabilities for parallel test execution:

```bash
# Scale chrome-tests service to run 3 parallel instances
docker-compose up --scale chrome-tests=3

# Scale multiple services simultaneously
docker-compose up --scale chrome-tests=2 --scale firefox-tests=2
```

**Source:** `behave.ini` lines 95-128 (Parallel execution documentation)

### Tag-Based Parallelism

Create separate services for different test tags to run in parallel:

```yaml
services:
  login-tests:
    extends: chrome-tests
    container_name: testinium-login
    command: behave --tags=@Login
    volumes:
      - ./reports/login:/app/reports

  crm-tests:
    extends: chrome-tests
    container_name: testinium-crm
    command: behave --tags=@CRM
    volumes:
      - ./reports/crm:/app/reports

  inventory-tests:
    extends: chrome-tests
    container_name: testinium-inventory
    command: behave --tags=@Inventory
    volumes:
      - ./reports/inventory:/app/reports
```

**Run all test groups in parallel:**
```bash
docker-compose up login-tests crm-tests inventory-tests
```

### Parallel Execution Architecture

```mermaid
sequenceDiagram
    participant DC as Docker Compose
    participant C1 as Chrome Test 1
    participant C2 as Chrome Test 2
    participant C3 as Chrome Test 3
    participant App as Application
    
    DC->>C1: Start Container (Scale 1)
    DC->>C2: Start Container (Scale 2)
    DC->>C3: Start Container (Scale 3)
    
    par Parallel Test Execution
        C1->>App: Execute @Login Tests
        C2->>App: Execute @CRM Tests
        C3->>App: Execute @Inventory Tests
    end
    
    C1->>DC: Write Reports (login/)
    C2->>DC: Write Reports (crm/)
    C3->>DC: Write Reports (inventory/)
    
    DC->>DC: Aggregate Results
```

### Thread-Safety Considerations

The framework uses thread-local WebDriver instances to ensure thread safety during parallel execution:

**Source:** `utilities/driver_manager.py` implements `threading.local()` pattern

```python
# Each container/thread gets isolated WebDriver instance
# No shared state between parallel test executions
# Configured automatically - no additional setup needed
```

### Behave Parallel Execution Options

For intra-container parallelism, use behave-parallel:

```yaml
chrome-tests:
  # ... other configuration
  command: >
    behave-parallel
    --processes 2
    --parallel-element scenario
    --tags=@Smoke
```

**Note:** Requires `behave-parallel` package in requirements.txt

**Source:** `behave.ini` lines 103-106

## Application Integration

### Running Application with Tests

The docker-compose.yml includes an `app-under-test` service demonstrating how to orchestrate both the application and test suite:

```yaml
services:
  app-under-test:
    image: your-application-image:latest
    environment:
      DATABASE_URL: postgresql://testuser:testpass@database:5432/testdb
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - test-network

  chrome-tests:
    depends_on:
      app-under-test:
        condition: service_healthy  # Wait for app to be healthy
    environment:
      BASE_URL: http://app-under-test:8080  # Service discovery
```

### Health Check Configuration

Health checks ensure the application is ready before tests start:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 10s      # Check every 10 seconds
  timeout: 5s        # Fail if check takes > 5 seconds
  retries: 5         # Retry 5 times before marking unhealthy
  start_period: 30s  # Grace period for app startup
```

### Database Service Integration

```yaml
database:
  image: postgres:15-alpine
  environment:
    POSTGRES_USER: testuser
    POSTGRES_PASSWORD: testpass
    POSTGRES_DB: testdb
  volumes:
    # Load test data initialization scripts
    - ./database/init:/docker-entrypoint-initdb.d:ro
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U testuser"]
    interval: 5s
    timeout: 3s
    retries: 5
```

**Test Data Initialization:**

Create `database/init/01-test-data.sql`:
```sql
-- Initialize test data for automated tests
INSERT INTO users (username, password, role) VALUES
  ('test.user@example.com', 'hashed_password', 'user'),
  ('sales.mgr@example.com', 'hashed_password', 'sales_manager'),
  ('pos.mgr@example.com', 'hashed_password', 'pos_manager');
```

### Service Dependency Chain

```mermaid
graph LR
    Database["database<br/>(PostgreSQL)"] -->|healthy| App["app-under-test<br/>(Web Application)"]
    App -->|healthy| ChromeTests["chrome-tests<br/>(Selenium Tests)"]
    App -->|healthy| FirefoxTests["firefox-tests<br/>(Selenium Tests)"]
    
    style Database fill:#336791
    style App fill:#00C853
    style ChromeTests fill:#4285F4
    style FirefoxTests fill:#FF7139
```

## Running Tests with Docker Compose

### Basic Commands

#### Start All Services

```bash
# Build images and start all services
docker-compose up

# Build images (if needed) and start in detached mode
docker-compose up -d

# Rebuild images before starting
docker-compose up --build
```

#### Start Specific Services

```bash
# Run only Chrome tests
docker-compose up chrome-tests

# Run Chrome and Firefox tests
docker-compose up chrome-tests firefox-tests

# Run tests without starting application (if already running)
docker-compose up --no-deps chrome-tests
```

#### Stop and Clean Up

```bash
# Stop all running services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop, remove containers, networks, images, and volumes
docker-compose down --rmi all -v
```

### Custom Test Execution

#### Run with Custom Behave Commands

```bash
# Run specific feature file
docker-compose run chrome-tests behave features/Login.feature

# Run with specific tags
docker-compose run chrome-tests behave --tags=@Login,@Smoke

# Run with multiple output formats
docker-compose run chrome-tests behave \
  -f json -o /app/reports/cucumber.json \
  -f html -o /app/reports/report.html \
  -f allure_behave.formatter:AllureFormatter \
  -o /app/reports/allure-results

# Run specific scenario by line number
docker-compose run chrome-tests behave features/Login.feature:15

# Dry run (validate step definitions)
docker-compose run chrome-tests behave --dry-run
```

**Source:** `behave.ini` lines 131-168 (Execution examples)

#### Run with Environment Variable Overrides

```bash
# Override browser type
docker-compose run -e BROWSER_TYPE=firefox chrome-tests behave

# Override base URL
docker-compose run -e BASE_URL=https://staging.example.com chrome-tests behave

# Run in non-headless mode (for debugging)
docker-compose run -e HEADLESS=false chrome-tests behave
```

### Viewing Logs

```bash
# View logs from all services
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs from specific service
docker-compose logs chrome-tests

# View last 50 lines of logs
docker-compose logs --tail=50 chrome-tests

# View logs with timestamps
docker-compose logs -t chrome-tests
```

### Monitoring Test Execution

```bash
# Check service status
docker-compose ps

# View resource usage
docker stats

# Execute command in running container
docker-compose exec chrome-tests bash

# Inspect container
docker-compose exec chrome-tests env
```

### Test Execution Workflow

```mermaid
sequenceDiagram
    participant User as Developer
    participant DC as Docker Compose
    participant Build as Build Process
    participant Services as Test Services
    participant Reports as Report Volume
    
    User->>DC: docker-compose up
    DC->>Build: Build images (if needed)
    Build-->>DC: Images ready
    
    DC->>Services: Start database
    Services->>Services: Database healthcheck
    
    DC->>Services: Start app-under-test
    Services->>Services: App healthcheck
    
    DC->>Services: Start test containers
    
    par Parallel Test Execution
        Services->>Services: Execute chrome-tests
        Services->>Services: Execute firefox-tests
    end
    
    Services->>Reports: Write test reports
    Services->>Reports: Write screenshots
    
    Services-->>DC: Tests complete
    DC-->>User: Exit with status code
    
    User->>Reports: View consolidated reports
```

## Report Aggregation

### Consolidated Report Structure

When running multiple test services, reports are organized by browser/service:

```
reports/
├── chrome/
│   ├── cucumber.json          # JSON report for Chrome tests
│   ├── report.html           # HTML report for Chrome tests
│   ├── junit/                # JUnit XML reports
│   │   ├── TESTS-Login.xml
│   │   └── TESTS-CRM.xml
│   ├── screenshots/          # Failure screenshots
│   │   ├── login_failed_20240115_143052.png
│   │   └── crm_error_20240115_143127.png
│   └── allure-results/       # Allure report data
│       ├── result-*.json
│       └── container-*.json
├── firefox/
│   ├── cucumber.json
│   ├── report.html
│   ├── junit/
│   ├── screenshots/
│   └── allure-results/
└── consolidated/
    ├── merged-report.html    # Merged HTML report
    ├── merged-results.json   # Merged JSON results
    └── dashboard.html        # Custom dashboard
```

### Viewing Reports

#### HTML Reports

```bash
# Open Chrome test report
open reports/chrome/report.html

# Open Firefox test report
open reports/firefox/report.html

# On Linux
xdg-open reports/chrome/report.html
```

#### JSON Reports

```bash
# View JSON report
cat reports/chrome/cucumber.json | jq '.'

# Count passed/failed scenarios
cat reports/chrome/cucumber.json | jq '[.[] | .elements[] | .steps[] | .result.status] | group_by(.) | map({status: .[0], count: length})'
```

#### Allure Reports

```bash
# Generate and serve Allure report for Chrome tests
allure serve reports/chrome/allure-results

# Generate Allure report for all browsers (consolidated)
allure generate reports/chrome/allure-results reports/firefox/allure-results \
  -o reports/consolidated/allure-report

# Open consolidated Allure report
allure open reports/consolidated/allure-report
```

### Report Aggregation Script

Create `scripts/aggregate-reports.sh` to merge reports from multiple browsers:

```bash
#!/bin/bash
# Aggregate test reports from multiple browser containers

REPORT_DIR="reports"
CONSOLIDATED_DIR="${REPORT_DIR}/consolidated"

# Create consolidated directory
mkdir -p "${CONSOLIDATED_DIR}"

# Merge JSON reports
echo "Merging JSON reports..."
jq -s 'add' \
  ${REPORT_DIR}/chrome/cucumber.json \
  ${REPORT_DIR}/firefox/cucumber.json \
  > ${CONSOLIDATED_DIR}/merged-results.json

# Generate consolidated Allure report
echo "Generating consolidated Allure report..."
allure generate \
  ${REPORT_DIR}/chrome/allure-results \
  ${REPORT_DIR}/firefox/allure-results \
  -o ${CONSOLIDATED_DIR}/allure-report \
  --clean

# Copy all screenshots to consolidated directory
echo "Copying screenshots..."
mkdir -p ${CONSOLIDATED_DIR}/screenshots
cp ${REPORT_DIR}/*/screenshots/*.png ${CONSOLIDATED_DIR}/screenshots/ 2>/dev/null || true

# Generate summary report
echo "Generating summary..."
cat > ${CONSOLIDATED_DIR}/summary.txt << EOF
Test Execution Summary
======================
Date: $(date)

Chrome Results: $(jq '[.[] | .elements[] | .steps[] | select(.result.status == "passed")] | length' ${REPORT_DIR}/chrome/cucumber.json) passed
Firefox Results: $(jq '[.[] | .elements[] | .steps[] | select(.result.status == "passed")] | length' ${REPORT_DIR}/firefox/cucumber.json) passed

Total Screenshots: $(ls ${CONSOLIDATED_DIR}/screenshots/*.png 2>/dev/null | wc -l)
EOF

echo "Report aggregation complete!"
echo "View consolidated report: ${CONSOLIDATED_DIR}/allure-report/index.html"
```

**Usage:**
```bash
# After tests complete
./scripts/aggregate-reports.sh

# View consolidated report
open reports/consolidated/allure-report/index.html
```

### Archiving Results

```bash
# Archive all test results with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf test-results-${TIMESTAMP}.tar.gz reports/

# Upload to artifact storage (example: AWS S3)
aws s3 cp test-results-${TIMESTAMP}.tar.gz s3://test-artifacts/docker-compose/

# Clean up old reports (keep last 10 runs)
ls -t test-results-*.tar.gz | tail -n +11 | xargs rm -f
```

## Advanced Configuration

### Environment-Specific Configuration

Create separate docker-compose files for different environments:

**docker-compose.yml** (base configuration)
```yaml
services:
  chrome-tests:
    build:
      context: .
    # ... base configuration
```

**docker-compose.dev.yml** (development overrides)
```yaml
services:
  chrome-tests:
    environment:
      HEADLESS: "false"  # Visual browser for debugging
      LOG_LEVEL: DEBUG
    volumes:
      - .:/app  # Live code mounting
```

**docker-compose.ci.yml** (CI/CD overrides)
```yaml
services:
  chrome-tests:
    environment:
      HEADLESS: "true"
      CI: "true"
    command: >
      behave --tags='not @WIP'
      --junit --junit-directory /app/reports/junit
```

**Usage:**
```bash
# Development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# CI/CD environment
docker-compose -f docker-compose.yml -f docker-compose.ci.yml up
```

### Resource Limits

Prevent test containers from consuming excessive resources:

```yaml
services:
  chrome-tests:
    deploy:
      resources:
        limits:
          cpus: '2.0'      # Maximum 2 CPU cores
          memory: 4G       # Maximum 4GB RAM
        reservations:
          cpus: '0.5'      # Minimum 0.5 CPU cores
          memory: 1G       # Minimum 1GB RAM
```

### Restart Policies

```yaml
services:
  chrome-tests:
    restart: on-failure       # Restart only on failure
    # restart: always         # Always restart
    # restart: unless-stopped # Restart unless manually stopped
    # restart: no             # Never restart (default)
```

## CI/CD Integration

### GitHub Actions Integration

`.github/workflows/docker-compose-tests.yml`:
```yaml
name: Docker Compose Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up environment variables
        run: |
          echo "TEST_USERNAME=${{ secrets.TEST_USERNAME }}" >> .env
          echo "TEST_PASSWORD=${{ secrets.TEST_PASSWORD }}" >> .env
          echo "SALES_MANAGER_USERNAME=${{ secrets.SALES_MANAGER_USERNAME }}" >> .env
          echo "SALES_MANAGER_PASSWORD=${{ secrets.SALES_MANAGER_PASSWORD }}" >> .env
          echo "POS_MANAGER_USERNAME=${{ secrets.POS_MANAGER_USERNAME }}" >> .env
          echo "POS_MANAGER_PASSWORD=${{ secrets.POS_MANAGER_PASSWORD }}" >> .env
      
      - name: Build and run tests
        run: docker-compose up --abort-on-container-exit --exit-code-from chrome-tests
      
      - name: Aggregate reports
        if: always()
        run: ./scripts/aggregate-reports.sh
      
      - name: Upload test reports
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-reports
          path: reports/
          retention-days: 30
      
      - name: Publish test results
        if: always()
        uses: EnricoMi/publish-unit-test-result-action@v2
        with:
          files: reports/**/junit/*.xml
```

### Jenkins Integration

`Jenkinsfile`:
```groovy
pipeline {
    agent any
    
    environment {
        TEST_USERNAME = credentials('test-username')
        TEST_PASSWORD = credentials('test-password')
        SALES_MANAGER_USERNAME = credentials('sales-manager-username')
        SALES_MANAGER_PASSWORD = credentials('sales-manager-password')
        POS_MANAGER_USERNAME = credentials('pos-manager-username')
        POS_MANAGER_PASSWORD = credentials('pos-manager-password')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker-compose build'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    docker-compose up \
                      --abort-on-container-exit \
                      --exit-code-from chrome-tests
                '''
            }
        }
        
        stage('Aggregate Reports') {
            steps {
                sh './scripts/aggregate-reports.sh'
            }
        }
    }
    
    post {
        always {
            junit 'reports/**/junit/*.xml'
            publishHTML([
                reportDir: 'reports/consolidated/allure-report',
                reportFiles: 'index.html',
                reportName: 'Allure Report'
            ])
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            sh 'docker-compose down -v'
        }
    }
}
```

## Troubleshooting

### Issue: Service Startup Order Problems

**Symptoms:**
- Tests start before application is ready
- Connection refused errors
- Random test failures at the beginning

**Cause:**
- `depends_on` without health check only waits for container start, not readiness

**Solution:**
```yaml
services:
  chrome-tests:
    depends_on:
      app-under-test:
        condition: service_healthy  # Wait for health check
```

**Verify health check:**
```bash
# Check service health status
docker-compose ps

# View health check logs
docker inspect testinium-app | jq '.[0].State.Health'
```

### Issue: Network Connectivity Between Containers

**Symptoms:**
- Tests cannot reach application
- `curl: (6) Could not resolve host` errors
- Connection timeout errors

**Cause:**
- Services not on same network
- Incorrect service name in BASE_URL
- Firewall rules blocking inter-container communication

**Solution:**
```yaml
# Ensure all services are on the same network
services:
  chrome-tests:
    networks:
      - test-network
  app-under-test:
    networks:
      - test-network

networks:
  test-network:
    driver: bridge
```

**Diagnostic commands:**
```bash
# Test connectivity from test container to app
docker-compose exec chrome-tests ping app-under-test

# Check network configuration
docker network inspect testinium-network

# Test HTTP connectivity
docker-compose exec chrome-tests curl http://app-under-test:8080/health
```

### Issue: Volume Permission Problems

**Symptoms:**
- Permission denied errors when writing reports
- Cannot create directories in mounted volumes
- Screenshots not saved

**Cause:**
- User ID mismatch between host and container
- Read-only volumes for directories that need write access

**Solution:**

**Option 1: Match user IDs in Dockerfile**
```dockerfile
# Set user ID to match host user
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g ${GROUP_ID} testuser && \
    useradd -m -u ${USER_ID} -g testuser testuser

USER testuser
```

**Build with current user ID:**
```bash
docker-compose build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)
```

**Option 2: Fix permissions on host**
```bash
# Make reports directory writable
chmod -R 777 reports/

# Or change ownership to match container user
sudo chown -R 1000:1000 reports/
```

### Issue: Resource Limits Causing Failures

**Symptoms:**
- Container crashes with exit code 137 (Out of Memory)
- Slow test execution
- Browser process killed unexpectedly

**Cause:**
- Insufficient memory allocation
- Too many parallel containers
- Resource limits too restrictive

**Solution:**

**Check resource usage:**
```bash
# Monitor container resource usage
docker stats

# Check container exit codes
docker-compose ps -a
```

**Increase resource limits:**
```yaml
services:
  chrome-tests:
    deploy:
      resources:
        limits:
          memory: 8G        # Increase from 4G
          cpus: '4.0'       # Increase from 2.0
```

**Adjust Docker daemon limits** (`/etc/docker/daemon.json`):
```json
{
  "default-ulimits": {
    "memlock": {
      "Hard": -1,
      "Name": "memlock",
      "Soft": -1
    },
    "nofile": {
      "Hard": 64000,
      "Name": "nofile",
      "Soft": 64000
    }
  }
}
```

### Issue: Port Conflicts

**Symptoms:**
- `bind: address already in use` error
- Cannot start application service
- Port mapping failures

**Cause:**
- Another service already using the port
- Previous container not fully stopped

**Solution:**

**Check what's using the port:**
```bash
# Find process using port 8080
lsof -i :8080
netstat -tulpn | grep 8080

# Kill process using the port
kill -9 <PID>
```

**Change port mapping in docker-compose.yml:**
```yaml
services:
  app-under-test:
    ports:
      - "8081:8080"  # Map to different host port
```

**Stop all containers completely:**
```bash
# Force remove all containers
docker-compose down -v
docker ps -a | grep testinium | awk '{print $1}' | xargs docker rm -f
```

### Issue: Test Results Not Appearing

**Symptoms:**
- Report directories empty
- No JSON/HTML reports generated
- Tests run but no output files

**Cause:**
- Incorrect volume mount paths
- Container exiting before reports are written
- Insufficient permissions on report directory

**Solution:**

**Verify volume mounts:**
```bash
# Check volume mounts
docker-compose config

# Inspect running container
docker-compose exec chrome-tests ls -la /app/reports/
```

**Ensure reports directory exists:**
```bash
# Create report directories before running
mkdir -p reports/{chrome,firefox}/{junit,screenshots,allure-results}
chmod -R 777 reports/
```

**Add explicit report flushing** (in `features/environment.py`):
```python
def after_all(context):
    """Ensure all reports are flushed before exit."""
    import sys
    sys.stdout.flush()
    sys.stderr.flush()
```

### Issue: Slow Test Execution

**Symptoms:**
- Tests take significantly longer than expected
- High CPU usage
- Container resource throttling

**Cause:**
- Insufficient resources allocated
- Too many containers running simultaneously
- Network latency between containers

**Solution:**

**Optimize resource allocation:**
```bash
# Run fewer parallel containers
docker-compose up --scale chrome-tests=2  # Instead of 4

# Allocate more resources per container
# See "Resource Limits" section above
```

**Enable parallel execution within containers:**
```yaml
chrome-tests:
  command: >
    behave-parallel
    --processes 2
    --parallel-element scenario
    --tags=@Smoke
```

**Use faster image layers:**
```dockerfile
# Use specific Python version for better caching
FROM python:3.11-slim

# Cache dependencies separately
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
```

## See Also

- **[Docker Deployment Guide](./docker.md)** - Single container Docker deployment
- **[Kubernetes Deployment Guide](./kubernetes.md)** - Container orchestration at scale
- **[CI/CD Integration Guide](./jenkins-integration.md)** - Jenkins pipeline integration
- **[Parallel Execution Guide](../guides/parallel-execution.md)** - Framework parallelism patterns
- **[Configuration Management Guide](../guides/configuration-management.md)** - Environment-specific configuration

---

**Source References:**
- Configuration: `config/config.yaml` lines 1-163
- Parallel execution: `behave.ini` lines 95-128
- Dependencies: `requirements.txt` lines 1-91
- Docker basics: `docs/deployment/docker.md`

**Document Status:** Complete and production-ready
**Last Updated:** 2024-01-15

