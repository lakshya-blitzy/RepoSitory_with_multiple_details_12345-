# Azure DevOps Pipeline Integration

## Overview

Azure DevOps provides a comprehensive DevOps platform for the Microsoft ecosystem, offering integrated CI/CD pipelines, work item tracking, and seamless Azure cloud integration for automated test execution.

### Benefits of Azure DevOps for Test Automation

**Enterprise Microsoft Integration:**
- Native integration with Azure Active Directory for authentication
- Seamless connectivity with Microsoft Teams for notifications
- Visual Studio and VS Code IDE integration
- Windows agent support for cross-platform testing

**Comprehensive DevOps Platform:**
- Unified platform for source control (Azure Repos), CI/CD (Azure Pipelines), work items, and test management
- Built-in test result visualization and trend analysis
- Integration with Azure Test Plans for test case management
- Wiki and documentation hosting

**Azure Cloud Integration:**
- Direct deployment to Azure services (App Service, Container Instances, Kubernetes Service)
- Managed agent pools with multiple OS options (Windows, Linux, macOS)
- Integration with Azure Key Vault for secrets management
- Azure Monitor integration for observability

**Work Item Tracking:**
- Link test results to user stories and bugs
- Automated work item updates based on test outcomes
- Rich query language for test result analysis
- Integration with Agile/Scrum boards

**Free Tier for Small Teams:**
- Free for up to 5 users with Azure Repos
- 1,800 pipeline minutes per month on Microsoft-hosted agents
- Unlimited self-hosted agents
- Free Azure Test Plans for stakeholders

### When to Use Azure DevOps

Use Azure DevOps when:
- Your organization uses Microsoft technology stack
- You need integrated work item tracking with test results
- You require Azure cloud deployment capabilities
- You want comprehensive test management with Azure Test Plans
- You need Windows-based test execution
- Your team prefers unified DevOps platform over separate tools

## Prerequisites

Before setting up Azure DevOps pipeline integration, ensure you have:

### Azure DevOps Organization and Project

1. **Azure DevOps Organization**: Create or access an existing organization at `https://dev.azure.com/{your-organization}`
2. **Project Setup**: Create a project or use an existing one with Azure Pipelines enabled
3. **Permissions**: Ensure you have `Build Administrator` or `Project Administrator` role

### Azure Pipelines Service Connection

1. **Repository Connection**: Connect your repository (Azure Repos, GitHub, Bitbucket, or external Git)
2. **Service Connections**: Configure any external service connections needed (Azure subscription, Docker registry, etc.)
3. **Pipeline Permissions**: Grant `Contribute` permission to build service account

### Agent Pool Configuration

**Microsoft-Hosted Agents:**
- Available images: `ubuntu-latest`, `windows-latest`, `macOS-latest`
- No setup required, but limited to 1,800 minutes/month (free tier)
- Pre-installed software includes Python 3.9-3.12, browsers, and common tools

**Self-Hosted Agents:**
- Install Azure Pipelines agent on your own infrastructure
- Unlimited minutes
- Full control over installed software and browser versions
- Required for network-restricted environments

### Understanding azure-pipelines.yml Syntax

**YAML Basics:**
- Indentation-based structure (2 spaces per level)
- Key-value pairs with colon separator
- Arrays use dash prefix
- Multi-line strings use `|` or `>` operators

**Pipeline Schema:**
- `trigger`: Define when pipeline runs automatically
- `pr`: Define pull request validation
- `pool`: Specify agent pool
- `variables`: Define pipeline variables
- `stages`: Organize pipeline into logical units
- `jobs`: Define work to be executed
- `steps`: Individual tasks within a job

### Repository Connected to Azure DevOps

**Azure Repos:**
- Repository already integrated, no additional setup needed
- Branch policies can require successful pipeline before merge

**GitHub:**
- Install Azure Pipelines app from GitHub Marketplace
- Authorize access to repositories
- Configure pipeline in Azure DevOps

**Other Git Providers:**
- Use generic Git service connection
- Provide repository URL and authentication credentials

## Complete Azure Pipelines Configuration

### Basic Pipeline Structure

Create `azure-pipelines.yml` in your repository root:

```yaml
# Azure Pipelines Configuration for Testinium Test Automation Framework
# Automated test execution with parallel browser testing and comprehensive reporting

# Trigger configuration - when pipeline runs automatically
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - features/**
      - pages/**
      - utilities/**
      - config/**
      - requirements.txt
      - azure-pipelines.yml
    exclude:
      - docs/**
      - README.md

# Pull request validation trigger
pr:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - features/**
      - pages/**
      - utilities/**
      - config/**
      - requirements.txt

# Agent pool specification
pool:
  vmImage: 'ubuntu-latest'  # Microsoft-hosted agent with Ubuntu

# Pipeline-level variables
variables:
  PYTHON_VERSION: '3.11'
  BROWSER_TYPE: 'chrome'
  HEADLESS: 'true'
  BASE_URL: 'https://testinium.example.com'
  
# Stages organize the pipeline into logical sections
stages:
  - stage: Build
    displayName: 'Build and Prepare Dependencies'
    jobs:
      - job: PrepareDependencies
        displayName: 'Install Python Dependencies'
        steps:
          - task: UsePythonVersion@0
            displayName: 'Set Python Version'
            inputs:
              versionSpec: '$(PYTHON_VERSION)'
              addToPath: true
              architecture: 'x64'
          
          - script: |
              python -m venv venv
              source venv/bin/activate
              pip install --upgrade pip
              pip install -r requirements.txt
            displayName: 'Create Virtual Environment and Install Dependencies'
          
          - task: Cache@2
            displayName: 'Cache Python Dependencies'
            inputs:
              key: 'python | "$(Agent.OS)" | requirements.txt'
              path: venv
              restoreKeys: |
                python | "$(Agent.OS)"

  - stage: Test
    displayName: 'Execute Test Suite'
    dependsOn: Build
    jobs:
      - job: ChromeTests
        displayName: 'Chrome Browser Tests'
        variables:
          BROWSER_TYPE: 'chrome'
        steps:
          - template: templates/test-execution-steps.yml
            parameters:
              browserType: 'chrome'
      
      - job: FirefoxTests
        displayName: 'Firefox Browser Tests'
        variables:
          BROWSER_TYPE: 'firefox'
        steps:
          - template: templates/test-execution-steps.yml
            parameters:
              browserType: 'firefox'

  - stage: Report
    displayName: 'Publish Test Results and Artifacts'
    dependsOn: Test
    condition: always()
    jobs:
      - job: PublishResults
        displayName: 'Publish Test Reports'
        steps:
          - task: PublishTestResults@2
            displayName: 'Publish JUnit Test Results'
            inputs:
              testResultsFormat: 'JUnit'
              testResultsFiles: 'reports/junit/**/*.xml'
              testRunTitle: 'Behave Test Results - $(Build.BuildNumber)'
              failTaskOnFailedTests: true
              publishRunAttachments: true
          
          - task: PublishPipelineArtifact@1
            displayName: 'Publish Test Report Artifacts'
            inputs:
              targetPath: 'reports'
              artifactName: 'test-reports-$(Build.BuildNumber)'
              publishLocation: 'pipeline'
```

**Source References:**
- Trigger paths based on repository structure
- JUnit directory from `behave.ini:37`
- Report configuration from `config/config.yaml:113-140`

## Detailed Stage and Job Configuration

### Build Stage - Dependency Preparation

The Build stage prepares the Python environment and installs all required dependencies:

```yaml
- stage: Build
  displayName: 'Build and Prepare Dependencies'
  jobs:
    - job: PrepareDependencies
      displayName: 'Install Python Dependencies'
      steps:
        # Step 1: Set Python version
        - task: UsePythonVersion@0
          displayName: 'Set Python Version $(PYTHON_VERSION)'
          inputs:
            versionSpec: '$(PYTHON_VERSION)'
            addToPath: true
            architecture: 'x64'
        
        # Step 2: Display Python version for verification
        - script: |
            python --version
            pip --version
          displayName: 'Verify Python Installation'
        
        # Step 3: Upgrade pip and install dependencies
        - script: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
          displayName: 'Install Dependencies from requirements.txt'
        
        # Step 4: Cache dependencies for faster subsequent builds
        - task: Cache@2
          displayName: 'Cache pip Packages'
          inputs:
            key: 'pip | "$(Agent.OS)" | requirements.txt'
            path: $(PIP_CACHE_DIR)
            restoreKeys: |
              pip | "$(Agent.OS)"
        
        # Step 5: Install browser drivers
        - script: |
            pip install webdriver-manager==4.0.1
            python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
            python -c "from webdriver_manager.firefox import GeckoDriverManager; GeckoDriverManager().install()"
          displayName: 'Install WebDriver Binaries'
```

**Source:** Based on `requirements.txt:1-91` dependencies

### Test Stage - Parallel Browser Execution

The Test stage executes tests across multiple browsers in parallel using strategy matrix:

```yaml
- stage: Test
  displayName: 'Execute Test Suite'
  dependsOn: Build
  jobs:
    - job: RunTests
      displayName: 'Run Tests on'
      strategy:
        matrix:
          Chrome_Python39:
            PYTHON_VERSION: '3.9'
            BROWSER_TYPE: 'chrome'
          Chrome_Python311:
            PYTHON_VERSION: '3.11'
            BROWSER_TYPE: 'chrome'
          Firefox_Python39:
            PYTHON_VERSION: '3.9'
            BROWSER_TYPE: 'firefox'
          Firefox_Python311:
            PYTHON_VERSION: '3.11'
            BROWSER_TYPE: 'firefox'
        maxParallel: 4
      
      steps:
        - task: UsePythonVersion@0
          inputs:
            versionSpec: '$(PYTHON_VERSION)'
        
        - script: pip install -r requirements.txt
          displayName: 'Install Dependencies'
        
        - script: |
            behave --tags=@Smoke \
              --format=json \
              --outfile=reports/behave-reports/cucumber.json \
              --junit \
              --junit-directory=reports/junit \
              -D browser=$(BROWSER_TYPE) \
              -D headless=true
          displayName: 'Execute Behave Tests - $(BROWSER_TYPE)'
          env:
            BASE_URL: $(BASE_URL)
            TEST_USERNAME: $(TEST_USERNAME)
            TEST_PASSWORD: $(TEST_PASSWORD)
            BROWSER_TYPE: $(BROWSER_TYPE)
            HEADLESS: 'true'
          continueOnError: true
        
        - task: PublishTestResults@2
          displayName: 'Publish Test Results - $(BROWSER_TYPE)'
          condition: always()
          inputs:
            testResultsFormat: 'JUnit'
            testResultsFiles: 'reports/junit/**/*.xml'
            testRunTitle: 'Tests - $(BROWSER_TYPE) - Python $(PYTHON_VERSION)'
            failTaskOnFailedTests: false
            mergeTestResults: false
        
        - task: PublishPipelineArtifact@1
          displayName: 'Publish Screenshots - $(BROWSER_TYPE)'
          condition: always()
          inputs:
            targetPath: 'reports/screenshots'
            artifactName: 'screenshots-$(BROWSER_TYPE)-$(PYTHON_VERSION)'
            publishLocation: 'pipeline'
```

**Source:** Test execution based on `behave.ini:95-128` parallel execution patterns

### Report Stage - Test Result Publishing

The Report stage consolidates and publishes all test results and artifacts:

```yaml
- stage: Report
  displayName: 'Generate and Publish Reports'
  dependsOn: Test
  condition: always()
  jobs:
    - job: ConsolidateReports
      displayName: 'Consolidate Test Reports'
      steps:
        - task: DownloadPipelineArtifact@2
          displayName: 'Download All Test Artifacts'
          inputs:
            buildType: 'current'
            targetPath: '$(Pipeline.Workspace)/artifacts'
        
        - script: |
            allure generate $(Pipeline.Workspace)/artifacts/allure-results \
              --clean \
              --output $(Pipeline.Workspace)/allure-report
          displayName: 'Generate Allure Report'
          condition: succeededOrFailed()
        
        - task: PublishPipelineArtifact@1
          displayName: 'Publish Allure Report'
          inputs:
            targetPath: '$(Pipeline.Workspace)/allure-report'
            artifactName: 'allure-report-$(Build.BuildNumber)'
            publishLocation: 'pipeline'
        
        - task: PublishTestResults@2
          displayName: 'Publish Consolidated Test Results'
          inputs:
            testResultsFormat: 'JUnit'
            testResultsFiles: '$(Pipeline.Workspace)/artifacts/**/junit/**/*.xml'
            testRunTitle: 'Consolidated Test Run - $(Build.BuildNumber)'
            mergeTestResults: true
            failTaskOnFailedTests: true
```

**Source:** Report formats from `config/config.yaml:127-134`

## Task-Level Configuration

### UsePythonVersion Task

Configure Python version for test execution:

```yaml
- task: UsePythonVersion@0
  displayName: 'Use Python $(PYTHON_VERSION)'
  inputs:
    versionSpec: '$(PYTHON_VERSION)'  # Python version to use (3.9, 3.10, 3.11, 3.12)
    addToPath: true                   # Add Python to PATH
    architecture: 'x64'               # Architecture (x64 or x86)
```

**Available Python Versions on Microsoft-Hosted Agents:**
- Python 3.9.x
- Python 3.10.x
- Python 3.11.x
- Python 3.12.x

### CmdLine and Bash Tasks

Execute shell commands for test execution:

```yaml
# Using CmdLine task (cross-platform)
- task: CmdLine@2
  displayName: 'Run Behave Tests'
  inputs:
    script: |
      behave --tags=@Smoke \
        --format=json \
        --outfile=reports/behave-reports/cucumber.json \
        --junit \
        --junit-directory=reports/junit
    workingDirectory: '$(System.DefaultWorkingDirectory)'
  env:
    BASE_URL: $(BASE_URL)
    TEST_USERNAME: $(TEST_USERNAME)
    TEST_PASSWORD: $(TEST_PASSWORD)
    BROWSER_TYPE: $(BROWSER_TYPE)
    HEADLESS: $(HEADLESS)

# Using Bash task (Linux/macOS only)
- task: Bash@3
  displayName: 'Run Behave Tests with Bash'
  inputs:
    targetType: 'inline'
    script: |
      #!/bin/bash
      set -e
      
      # Activate virtual environment
      source venv/bin/activate
      
      # Run tests
      behave --tags=@Smoke \
        --format=allure_behave.formatter:AllureFormatter \
        --outfile=reports/allure-results \
        --junit \
        --junit-directory=reports/junit
      
      # Generate Allure report
      allure generate reports/allure-results --clean --output reports/allure-report
    workingDirectory: '$(System.DefaultWorkingDirectory)'
```

**Source:** Behave execution commands from `behave.ini:131-168`

### PublishTestResults Task

Publish JUnit XML test results to Azure Pipelines:

```yaml
- task: PublishTestResults@2
  displayName: 'Publish Behave Test Results'
  condition: always()
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: 'reports/junit/**/*.xml'
    testRunTitle: 'Behave Test Results - $(Build.BuildNumber)'
    failTaskOnFailedTests: true
    publishRunAttachments: true
    mergeTestResults: true
```

**Configuration Options:**
- `testResultsFormat`: Format of test results (JUnit, NUnit, VSTest, XUnit, CTest)
- `testResultsFiles`: Pattern to match test result files
- `testRunTitle`: Display name for test run
- `failTaskOnFailedTests`: Fail pipeline if tests fail
- `publishRunAttachments`: Attach log files and screenshots
- `mergeTestResults`: Combine results from multiple test files

**Source:** JUnit directory from `behave.ini:37`

### PublishPipelineArtifact Task

Publish test reports and artifacts:

```yaml
- task: PublishPipelineArtifact@1
  displayName: 'Publish Test Report Artifacts'
  condition: always()
  inputs:
    targetPath: 'reports'
    artifactName: 'test-reports-$(Build.BuildNumber)'
    publishLocation: 'pipeline'
```

**Configuration Options:**
- `targetPath`: Directory or file to publish
- `artifactName`: Name of artifact (appears in pipeline)
- `publishLocation`: Where to publish (pipeline, fileshare)

**Artifact Types to Publish:**
- JUnit XML results: `reports/junit/**/*.xml`
- HTML reports: `reports/behave-reports/**/*.html`
- Allure results: `reports/allure-results/**/*`
- Screenshots: `reports/screenshots/**/*.png`
- Cucumber JSON: `reports/behave-reports/cucumber.json`

## Variable Groups and Secrets Management

### Creating Variable Groups in Azure DevOps Library

Variable groups centralize configuration and secrets across pipelines:

**Step 1: Navigate to Library**
1. Open Azure DevOps project
2. Go to Pipelines → Library
3. Click "+ Variable group"

**Step 2: Create Variable Group**
```
Name: testinium-credentials
Description: Test automation credentials and configuration

Variables:
- TEST_USERNAME: testuser@example.com
- TEST_PASSWORD: ************ (click lock icon to mark as secret)
- SALES_MANAGER_USERNAME: salesmanager@example.com
- SALES_MANAGER_PASSWORD: ************ (secret)
- POS_MANAGER_USERNAME: posmanager@example.com
- POS_MANAGER_PASSWORD: ************ (secret)
- BASE_URL: https://testinium.example.com
- BROWSER_TYPE: chrome
- HEADLESS: true
```

**Step 3: Link Azure Key Vault (Optional)**

For enhanced security, link variable group to Azure Key Vault:
1. Toggle "Link secrets from an Azure key vault as variables"
2. Select Azure subscription
3. Select Key Vault name
4. Authorize Azure Pipelines to access Key Vault
5. Add secrets from Key Vault

### Using Variable Groups in Pipelines

Reference variable groups in `azure-pipelines.yml`:

```yaml
variables:
  # Pipeline-level variables
  - name: PYTHON_VERSION
    value: '3.11'
  
  # Import variables from Library
  - group: testinium-credentials
  
  # Environment-specific variable groups
  - ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/main') }}:
    - group: testinium-production
  - ${{ if eq(variables['Build.SourceBranch'], 'refs/heads/develop') }}:
    - group: testinium-staging
```

### Environment-Specific Variable Groups

Create separate variable groups for each environment:

**testinium-dev (Development):**
```
BASE_URL: https://dev.testinium.example.com
TEST_USERNAME: dev.testuser@example.com
TEST_PASSWORD: ************
HEADLESS: false
```

**testinium-staging (Staging):**
```
BASE_URL: https://staging.testinium.example.com
TEST_USERNAME: staging.testuser@example.com
TEST_PASSWORD: ************
HEADLESS: true
```

**testinium-production (Production):**
```
BASE_URL: https://testinium.example.com
TEST_USERNAME: prod.testuser@example.com
TEST_PASSWORD: ************
HEADLESS: true
```

### Accessing Variables in Scripts

Access variables in pipeline steps:

```yaml
- script: |
    echo "Base URL: $(BASE_URL)"
    echo "Browser: $(BROWSER_TYPE)"
    behave --tags=@Smoke
  displayName: 'Run Tests with Variables'
  env:
    BASE_URL: $(BASE_URL)
    TEST_USERNAME: $(TEST_USERNAME)
    TEST_PASSWORD: $(TEST_PASSWORD)
```

**Source:** Credentials configuration from `config/config.yaml:93-110` and `.env.example:16-28`

## Strategy Matrix for Parallel Execution

### Matrix Configuration

Execute tests across multiple configurations simultaneously:

```yaml
jobs:
  - job: ParallelTests
    displayName: 'Parallel Test Execution'
    strategy:
      matrix:
        Chrome_Python39:
          PYTHON_VERSION: '3.9'
          BROWSER_TYPE: 'chrome'
        Chrome_Python310:
          PYTHON_VERSION: '3.10'
          BROWSER_TYPE: 'chrome'
        Chrome_Python311:
          PYTHON_VERSION: '3.11'
          BROWSER_TYPE: 'chrome'
        Firefox_Python39:
          PYTHON_VERSION: '3.9'
          BROWSER_TYPE: 'firefox'
        Firefox_Python310:
          PYTHON_VERSION: '3.10'
          BROWSER_TYPE: 'firefox'
        Firefox_Python311:
          PYTHON_VERSION: '3.11'
          BROWSER_TYPE: 'firefox'
      maxParallel: 6
    
    steps:
      - task: UsePythonVersion@0
        inputs:
          versionSpec: '$(PYTHON_VERSION)'
      
      - script: |
          pip install -r requirements.txt
          behave --tags=@Smoke -D browser=$(BROWSER_TYPE)
        displayName: 'Test - $(BROWSER_TYPE) / Python $(PYTHON_VERSION)'
```

### Accessing Matrix Variables

Matrix variables are automatically available in steps:

```yaml
- script: |
    echo "Python Version: $(PYTHON_VERSION)"
    echo "Browser Type: $(BROWSER_TYPE)"
    behave --tags=@Smoke \
      -D browser=$(BROWSER_TYPE) \
      -D python_version=$(PYTHON_VERSION)
  displayName: 'Execute Tests'
```

### Concurrency Control

Control how many matrix jobs run simultaneously:

```yaml
strategy:
  matrix:
    # ... matrix configurations ...
  maxParallel: 4  # Run up to 4 jobs simultaneously
```

**Considerations:**
- Microsoft-hosted agents: Limited concurrent jobs (depends on Azure DevOps plan)
- Self-hosted agents: Based on available agent capacity
- Resource constraints: Browser tests can be resource-intensive

**Source:** Parallel execution patterns from `behave.ini:95-128`

## Test Result Publishing and Visualization

### JUnit XML Publishing

Publish test results for visualization in Azure Pipelines:

```yaml
- task: PublishTestResults@2
  displayName: 'Publish Test Results'
  condition: always()
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: 'reports/junit/**/*.xml'
    testRunTitle: 'Behave Tests - $(Build.BuildNumber)'
    failTaskOnFailedTests: true
    publishRunAttachments: true
```

### Test Result Trends

Azure Pipelines automatically creates test result trends:

**Available Metrics:**
- Pass rate over time
- Test duration trends
- Flaky test identification
- Test failure analysis

**Accessing Test Trends:**
1. Navigate to Pipelines → Select pipeline
2. Click "Analytics" tab
3. View test trends and insights

### Test Failure Analysis

Analyze test failures directly in Azure Pipelines:

**Features:**
- Failed test details with error messages
- Stack traces and logs
- Screenshots (if published as attachments)
- Historical failure data
- Failure grouping by type

**Publishing Failure Details:**
```yaml
- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: 'reports/junit/**/*.xml'
    publishRunAttachments: true  # Include screenshots and logs
```

### Code Coverage Publishing

If using pytest with coverage:

```yaml
- script: |
    pip install pytest-cov
    pytest --cov=utilities --cov=pages --cov=config \
      --cov-report=xml:reports/coverage.xml \
      --cov-report=html:reports/coverage
  displayName: 'Run Tests with Coverage'

- task: PublishCodeCoverageResults@1
  displayName: 'Publish Code Coverage'
  inputs:
    codeCoverageTool: 'Cobertura'
    summaryFileLocation: 'reports/coverage.xml'
    reportDirectory: 'reports/coverage'
```

## Artifact Publishing

### Pipeline Artifacts

Publish test reports as pipeline artifacts:

```yaml
- task: PublishPipelineArtifact@1
  displayName: 'Publish HTML Reports'
  condition: always()
  inputs:
    targetPath: 'reports/behave-reports'
    artifactName: 'html-reports'
    publishLocation: 'pipeline'

- task: PublishPipelineArtifact@1
  displayName: 'Publish Screenshots'
  condition: always()
  inputs:
    targetPath: 'reports/screenshots'
    artifactName: 'test-screenshots'
    publishLocation: 'pipeline'

- task: PublishPipelineArtifact@1
  displayName: 'Publish Allure Results'
  condition: always()
  inputs:
    targetPath: 'reports/allure-results'
    artifactName: 'allure-results'
    publishLocation: 'pipeline'
```

### File Share Artifacts

Publish artifacts to network file share:

```yaml
- task: PublishBuildArtifacts@1
  displayName: 'Publish to File Share'
  inputs:
    pathToPublish: 'reports'
    artifactName: 'test-reports'
    publishLocation: 'fileshare'
    fileSharePath: '\\server\share\test-reports\$(Build.BuildNumber)'
```

### Artifact Retention Policies

Configure artifact retention:

1. Navigate to Project Settings → Pipelines → Settings
2. Set retention policies:
   - Days to keep: 30 days (default)
   - Minimum to keep: 1
   - Days to keep pull request runs: 10 days

### Downloading Artifacts

Download artifacts for local analysis:

**Via Azure DevOps Web UI:**
1. Open pipeline run
2. Click "Artifacts" in summary
3. Click download icon next to artifact name

**Via Azure CLI:**
```bash
az pipelines runs artifact download \
  --organization https://dev.azure.com/{org} \
  --project {project} \
  --run-id {run-id} \
  --artifact-name test-reports \
  --path ./downloaded-reports
```

**Source:** Report directory structure from `config/config.yaml:125-139`

## Advanced Pipeline Features

### Deployment Stages with Environments

Create deployment stages with approval gates:

```yaml
stages:
  - stage: Test
    displayName: 'Run Tests'
    jobs:
      - job: RunTests
        steps:
          - script: behave --tags=@Smoke
            displayName: 'Execute Tests'

  - stage: DeployToStaging
    displayName: 'Deploy to Staging'
    dependsOn: Test
    condition: succeeded()
    jobs:
      - deployment: DeployStaging
        displayName: 'Deploy to Staging Environment'
        environment: 'staging'  # Requires approval
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploy to staging"

  - stage: ProductionTests
    displayName: 'Production Smoke Tests'
    dependsOn: DeployToStaging
    jobs:
      - job: ProductionSmokeTests
        steps:
          - script: behave --tags=@ProductionSmoke
            displayName: 'Run Production Smoke Tests'
            env:
              BASE_URL: https://testinium.example.com

  - stage: DeployToProduction
    displayName: 'Deploy to Production'
    dependsOn: ProductionTests
    condition: succeeded()
    jobs:
      - deployment: DeployProduction
        displayName: 'Deploy to Production Environment'
        environment: 'production'  # Requires approval
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploy to production"
```

**Creating Environments:**
1. Navigate to Pipelines → Environments
2. Click "New environment"
3. Name: staging / production
4. Add approval and checks

### Template Pipelines for Reuse

Create reusable pipeline templates:

**templates/test-execution-steps.yml:**
```yaml
parameters:
  - name: browserType
    type: string
  - name: tags
    type: string
    default: '@Smoke'

steps:
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.11'
  
  - script: pip install -r requirements.txt
    displayName: 'Install Dependencies'
  
  - script: |
      behave --tags=${{ parameters.tags }} \
        -D browser=${{ parameters.browserType }} \
        --junit \
        --junit-directory=reports/junit
    displayName: 'Run Tests - ${{ parameters.browserType }}'
    env:
      BROWSER_TYPE: ${{ parameters.browserType }}
  
  - task: PublishTestResults@2
    condition: always()
    inputs:
      testResultsFormat: 'JUnit'
      testResultsFiles: 'reports/junit/**/*.xml'
      testRunTitle: 'Tests - ${{ parameters.browserType }}'
```

**Using Templates:**
```yaml
jobs:
  - job: ChromeTests
    steps:
      - template: templates/test-execution-steps.yml
        parameters:
          browserType: 'chrome'
          tags: '@Smoke'
  
  - job: FirefoxTests
    steps:
      - template: templates/test-execution-steps.yml
        parameters:
          browserType: 'firefox'
          tags: '@Smoke'
```

### Extends Keyword for Base Templates

Create base template with common configuration:

**templates/base-pipeline.yml:**
```yaml
parameters:
  - name: pythonVersion
    type: string
    default: '3.11'

stages:
  - stage: Build
    jobs:
      - job: Setup
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: ${{ parameters.pythonVersion }}
          - script: pip install -r requirements.txt

  - ${{ parameters.stages }}
```

**azure-pipelines.yml extends base:**
```yaml
extends:
  template: templates/base-pipeline.yml
  parameters:
    pythonVersion: '3.11'
    stages:
      - stage: Test
        jobs:
          - job: RunTests
            steps:
              - script: behave
```

### Parameters for Pipeline Customization

Accept runtime parameters:

```yaml
parameters:
  - name: environment
    displayName: 'Target Environment'
    type: string
    default: 'staging'
    values:
      - dev
      - staging
      - production
  
  - name: browserType
    displayName: 'Browser Type'
    type: string
    default: 'chrome'
    values:
      - chrome
      - firefox
  
  - name: testTags
    displayName: 'Test Tags'
    type: string
    default: '@Smoke'

stages:
  - stage: Test
    jobs:
      - job: RunTests
        steps:
          - script: |
              behave --tags=${{ parameters.testTags }} \
                -D browser=${{ parameters.browserType }}
            displayName: 'Run Tests - ${{ parameters.environment }}'
            env:
              BASE_URL: ${{ variables[format('{0}_BASE_URL', parameters.environment)] }}
```

### Conditions for Conditional Execution

Control when stages/jobs execute:

```yaml
stages:
  - stage: Test
    condition: always()  # Always run

  - stage: SecurityTests
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    # Only run on main branch if previous stages succeeded

  - stage: DeployProduction
    condition: |
      and(
        succeeded(),
        eq(variables['Build.SourceBranch'], 'refs/heads/main'),
        ne(variables['Build.Reason'], 'PullRequest')
      )
    # Only deploy from main branch, not from PRs
```

### Dependencies Between Jobs

Control job execution order:

```yaml
jobs:
  - job: UnitTests
    steps:
      - script: pytest tests/unit

  - job: IntegrationTests
    dependsOn: UnitTests
    condition: succeeded()
    steps:
      - script: pytest tests/integration

  - job: E2ETests
    dependsOn:
      - UnitTests
      - IntegrationTests
    condition: succeeded()
    steps:
      - script: behave --tags=@E2E
```

## Azure Repos Integration

### Branch Policies with Build Validation

Require successful pipeline before merging:

**Step 1: Navigate to Branch Policies**
1. Go to Repos → Branches
2. Click "..." next to main branch
3. Select "Branch policies"

**Step 2: Add Build Validation**
1. Click "+ Add build policy"
2. Select build pipeline
3. Configure:
   - Trigger: Automatic
   - Policy requirement: Required
   - Build expiration: Immediately
   - Display name: "Automated Tests"

**Step 3: Additional Policies**
- Require a minimum number of reviewers
- Check for linked work items
- Check for comment resolution
- Require merge strategy: Squash merge

### Pull Request Status Checks

Pipeline status appears on pull requests:

**PR Status Indicators:**
- ✓ All checks passed
- ✗ Checks failed
- ⏱ Checks in progress

**Viewing Details:**
1. Open pull request
2. Click "Checks" tab
3. View pipeline run details
4. Review test results and logs

### Code Review Integration

Pipeline results integrate with code review:

**Features:**
- Failed tests show in PR overview
- Comment on PR with test results
- Block merge if tests fail
- Automatically request re-review on failures

### Comment Threading on Failures

Automatically comment on PR when tests fail:

```yaml
- task: GitHubComment@0
  condition: failed()
  inputs:
    gitHubConnection: 'GitHub-Connection'
    repositoryName: '$(Build.Repository.Name)'
    comment: |
      ## ❌ Tests Failed

      **Build:** [$(Build.BuildNumber)]($(System.TeamFoundationCollectionUri)$(System.TeamProject)/_build/results?buildId=$(Build.BuildId))
      
      Please review test failures and fix before merging.
```

## Azure Test Plans Integration

### Associating Test Results with Test Plans

Link automated tests to manual test cases:

**Step 1: Create Test Plan**
1. Navigate to Test Plans
2. Create new test plan
3. Add test suites and test cases

**Step 2: Link Automated Tests**
```yaml
- task: PublishTestResults@2
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: 'reports/junit/**/*.xml'
    testRunTitle: 'Behave Automated Tests'
    testPlan: $(TestPlanId)
    testSuite: $(TestSuiteId)
```

### Work Item Integration

Link test results to user stories and bugs:

**Automatic Linking:**
- Tests linked to work items via branch name
- Tests linked via commit messages with #WorkItemId
- Tests linked via test case association

**Viewing Work Item Links:**
1. Open test run in Azure Pipelines
2. Click test result
3. View "Associated work items"

### Manual Testing Complement

Combine automated and manual testing:

**Workflow:**
1. Automated tests run on every PR
2. Manual exploratory testing in Azure Test Plans
3. Both results appear in test runs
4. Combined pass/fail metrics

## Notifications and Dashboards

### Pipeline Notification Rules

Configure email notifications:

**Step 1: Personal Notifications**
1. Click user profile → Notification settings
2. Navigate to Pipelines
3. Configure rules:
   - Build completed
   - Build failed
   - Build partially succeeded

**Step 2: Team Notifications**
1. Project Settings → Notifications
2. Add team notification
3. Configure delivery options

### Azure DevOps Dashboard Widgets

Create dashboard for test results:

**Step 1: Create Dashboard**
1. Navigate to Overview → Dashboards
2. Click "New Dashboard"
3. Name: "Test Automation Metrics"

**Step 2: Add Widgets**
- **Chart for Test Results**: Test pass rate trend
- **Build History**: Recent pipeline runs
- **Test Results Trend**: Test count over time
- **Requirements Quality**: Work item status
- **Pipeline Runs**: Recent runs with status

**Step 3: Configure Widgets**
```
Test Results Widget:
- Pipeline: testinium-tests
- Time period: Last 30 days
- Chart type: Line chart
- Metrics: Passed tests, Failed tests, Pass rate
```

### Custom Queries for Test Failures

Create queries to track test failures:

**Query Example:**
```
Work Item Type = Bug
State = Active
Tags Contains "AutomatedTestFailure"
Created Date >= @Today - 7
```

### Email Notifications

Configure email notifications for test failures:

```yaml
- task: SendEmail@1
  condition: failed()
  inputs:
    To: 'team@example.com'
    From: 'azure-pipelines@example.com'
    Subject: 'Test Failures - Build $(Build.BuildNumber)'
    Body: |
      Automated tests failed in build $(Build.BuildNumber)
      
      View results: $(System.TeamFoundationCollectionUri)$(System.TeamProject)/_build/results?buildId=$(Build.BuildId)
      
      Failed tests: $(Agent.JobStatus)
    SmtpServer: 'smtp.example.com'
```

## Agent Pool Considerations

### Microsoft-Hosted Agents

Pre-configured agents managed by Microsoft:

**Available Images:**
- `ubuntu-latest`: Ubuntu 22.04
- `ubuntu-20.04`: Ubuntu 20.04
- `windows-latest`: Windows Server 2022
- `windows-2019`: Windows Server 2019
- `macOS-latest`: macOS 12 Monterey
- `macOS-11`: macOS 11 Big Sur

**Pre-installed Software:**
- Python 3.9, 3.10, 3.11, 3.12
- Chrome, Firefox, Edge browsers
- Git, Azure CLI, Docker
- Node.js, Java, .NET

**Specifications:**
- 2 CPU cores
- 7 GB RAM
- 14 GB SSD storage

**Usage Limits:**
- Free tier: 1,800 minutes/month
- Microsoft 365 subscribers: 1,800 minutes/month
- Additional: Purchase parallel jobs

### Self-Hosted Agents

Install agents on your own infrastructure:

**Step 1: Download Agent**
1. Navigate to Project Settings → Agent pools
2. Click "New agent"
3. Download agent for your OS

**Step 2: Configure Agent**
```bash
# Extract agent
mkdir myagent && cd myagent
tar zxvf ~/Downloads/vsts-agent-linux-x64-*.tar.gz

# Configure
./config.sh

# Enter server URL: https://dev.azure.com/{organization}
# Enter PAT token
# Enter agent pool: Default
# Enter agent name: my-agent

# Run as service
sudo ./svc.sh install
sudo ./svc.sh start
```

**Step 3: Use Self-Hosted Agent**
```yaml
pool:
  name: 'Default'  # Self-hosted pool name
  demands:
    - agent.name -equals my-agent
```

### Agent Capabilities and Demands

Specify agent requirements:

**Agent Capabilities:**
- Automatically detected: OS, Python versions, browsers
- User-defined: Custom software, environment variables

**Demands in Pipeline:**
```yaml
pool:
  name: 'Default'
  demands:
    - python3.11
    - chrome
    - docker
```

### Parallel Job Limits

Control concurrent job execution:

**Free Tier:**
- 1 parallel job (Microsoft-hosted)
- Unlimited self-hosted agents

**Paid Plans:**
- Additional parallel jobs: $40/month per job
- Unlimited minutes with Microsoft-hosted agents

**Pipeline Configuration:**
```yaml
strategy:
  matrix:
    # ... configurations ...
  maxParallel: 2  # Don't exceed available parallel jobs
```

## Troubleshooting

### Python Version Not Found

**Symptoms:**
```
##[error]Version spec 3.13 for architecture x64 did not match any version in Agent.ToolsDirectory.
```

**Cause:** Specified Python version not available on agent

**Solution:**
```yaml
# Use available Python versions
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'  # Use 3.9, 3.10, 3.11, or 3.12
```

**Verify Available Versions:**
```yaml
- script: |
    ls -la /opt/hostedtoolcache/Python
  displayName: 'List Available Python Versions'
```

### Agent Not Picking Job

**Symptoms:** Job queued but never starts

**Causes:**
- No agents available in pool
- Agent demands not met
- All parallel jobs in use

**Solutions:**

1. **Check Agent Status:**
   - Navigate to Project Settings → Agent pools
   - Select pool → Agents tab
   - Verify agents are online

2. **Review Demands:**
```yaml
pool:
  vmImage: 'ubuntu-latest'
  # Remove or adjust demands
  demands: []
```

3. **Increase Parallel Jobs:**
   - Purchase additional parallel jobs
   - Use self-hosted agents (unlimited)

### Variable Not Resolved

**Symptoms:**
```
##[error]The term '$(TEST_USERNAME)' is not recognized
```

**Cause:** Variable not defined or not accessible

**Solutions:**

1. **Define Variable:**
```yaml
variables:
  - name: TEST_USERNAME
    value: 'testuser@example.com'
```

2. **Link Variable Group:**
```yaml
variables:
  - group: testinium-credentials
```

3. **Check Variable Scope:**
   - Stage-level variables only accessible in that stage
   - Job-level variables only accessible in that job

### Test Results Not Published

**Symptoms:** No test results appear in pipeline

**Causes:**
- Test result files not generated
- Incorrect file path pattern
- PublishTestResults task not run

**Solutions:**

1. **Verify Files Exist:**
```yaml
- script: |
    ls -la reports/junit/
    cat reports/junit/*.xml
  displayName: 'Debug Test Results'
  condition: always()
```

2. **Check File Pattern:**
```yaml
- task: PublishTestResults@2
  inputs:
    testResultsFiles: 'reports/junit/**/*.xml'  # Correct pattern
    # Not: reports/junit/*.xml  # Would miss subdirectories
```

3. **Ensure Task Runs:**
```yaml
- task: PublishTestResults@2
  condition: always()  # Run even if tests fail
```

### Artifact Upload Failure

**Symptoms:**
```
##[error]Failed to upload artifact: Request timeout
```

**Causes:**
- Artifact too large
- Network issues
- Disk space issues

**Solutions:**

1. **Check Artifact Size:**
```yaml
- script: du -sh reports/
  displayName: 'Check Artifact Size'
```

2. **Compress Artifacts:**
```yaml
- script: tar -czf reports.tar.gz reports/
  displayName: 'Compress Reports'

- task: PublishPipelineArtifact@1
  inputs:
    targetPath: 'reports.tar.gz'
    artifactName: 'test-reports'
```

3. **Split Large Artifacts:**
```yaml
- task: PublishPipelineArtifact@1
  inputs:
    targetPath: 'reports/screenshots'
    artifactName: 'screenshots'

- task: PublishPipelineArtifact@1
  inputs:
    targetPath: 'reports/junit'
    artifactName: 'test-results'
```

### Matrix Job Timeout

**Symptoms:** Matrix jobs exceed time limit and timeout

**Causes:**
- Too many matrix combinations
- Tests running serially instead of parallel
- Resource contention

**Solutions:**

1. **Reduce Matrix Size:**
```yaml
strategy:
  matrix:
    Chrome_Latest:
      PYTHON_VERSION: '3.11'
      BROWSER_TYPE: 'chrome'
    Firefox_Latest:
      PYTHON_VERSION: '3.11'
      BROWSER_TYPE: 'firefox'
  maxParallel: 2
```

2. **Increase Job Timeout:**
```yaml
jobs:
  - job: RunTests
    timeoutInMinutes: 60  # Default is 60, max is 360
```

3. **Optimize Test Execution:**
```yaml
- script: |
    behave --tags=@Smoke  # Run only smoke tests
    # Not: behave  # Don't run all tests
  displayName: 'Run Smoke Tests Only'
```

### Approval Gate Issues

**Symptoms:** Deployment stuck waiting for approval

**Causes:**
- No approvers configured
- Approvers not notified
- Approval timeout

**Solutions:**

1. **Configure Approvers:**
   - Navigate to Pipelines → Environments
   - Select environment → Approvals and checks
   - Add users/groups as approvers

2. **Check Notifications:**
   - Verify approvers receive email notifications
   - Check notification settings in user profile

3. **Manual Approval:**
   - Open pipeline run
   - Click "Review" button
   - Approve or reject deployment

**Source References:**
- Behave configuration: `behave.ini:1-200`
- Test configuration: `config/config.yaml:1-163`
- Environment variables: `.env.example:1-31`
- Dependencies: `requirements.txt:1-91`

## See Also

- [Jenkins Integration](jenkins-integration.md) - Alternative CI/CD platform
- [GitHub Actions](github-actions.md) - GitHub-native CI/CD
- [GitLab CI](gitlab-ci.md) - GitLab-native CI/CD
- [Docker Deployment](docker.md) - Containerized test execution
- [Configuration Reference](../reference/configuration-options.md) - Complete configuration guide
- [Parallel Execution Guide](../guides/parallel-execution.md) - Advanced parallel testing
- [Troubleshooting Guide](../troubleshooting/index.md) - Additional troubleshooting resources

---

**Last Updated:** 2024
**Framework Version:** 1.0.0
