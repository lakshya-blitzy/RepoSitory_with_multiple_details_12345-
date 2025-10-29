# Azure Cloud Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the Testinium QA Python test automation framework on Microsoft Azure cloud platform. Azure offers a robust and integrated ecosystem for running automated tests with enterprise-grade reliability and scalability.

### Azure Deployment Benefits

**Integrated Microsoft Ecosystem:**
- Seamless integration with Azure DevOps for complete DevOps lifecycle
- Native support for Microsoft development tools and services
- Unified identity management with Azure Active Directory
- Integrated monitoring and diagnostics with Azure Monitor

**Azure DevOps Native Integration:**
- Built-in CI/CD with Azure Pipelines
- Test results integration with Azure Test Plans
- Work item tracking with Azure Boards
- Artifact management with Azure Artifacts

**Hybrid Cloud Capabilities:**
- Azure Arc for hybrid and multi-cloud management
- ExpressRoute for private connectivity
- Azure Stack for on-premises Azure services
- Consistent tooling across cloud and on-premises

**Enterprise Support:**
- 24/7 technical support with SLA guarantees
- Compliance certifications (ISO, SOC, HIPAA, etc.)
- Global presence with 60+ regions worldwide
- Enterprise agreements and cost optimization programs

**Global Data Centers:**
- Presence in North America, Europe, Asia, Australia, Africa, South America
- Low-latency testing from multiple geographic locations
- Data residency compliance for regional requirements
- Availability zones for high availability within regions

## Prerequisites

Before deploying the test automation framework on Azure, ensure you have the following:

### Azure Subscription

- Active Azure subscription with appropriate permissions
- Resource creation rights (Contributor or Owner role)
- Budget and cost limits configured
- Subscription ID ready for deployment

### Azure CLI Installed

**Installation:**

```bash
# Windows (using Windows Package Manager)
winget install Microsoft.AzureCLI

# macOS (using Homebrew)
brew install azure-cli

# Linux (Ubuntu/Debian)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Linux (RHEL/CentOS)
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo dnf install azure-cli
```

**Verification:**

```bash
# Check Azure CLI version
az --version

# Expected output: azure-cli 2.55.0 or later

# Login to Azure
az login

# Set default subscription
az account set --subscription "Your Subscription Name"

# Verify current subscription
az account show
```

### Understanding of Azure Resources

Familiarity with the following Azure services is recommended:

**Azure Virtual Machines (VMs):**
- Infrastructure-as-a-Service (IaaS) compute instances
- Full control over operating system and software
- Support for custom images and extensions
- VM scale sets for auto-scaling

**Azure Container Instances (ACI):**
- Serverless containers without cluster management
- Fast startup times (seconds)
- Per-second billing
- Ideal for short-lived test executions

**Azure App Service:**
- Platform-as-a-Service (PaaS) for containerized applications
- Built-in scaling and load balancing
- Continuous deployment support
- Managed SSL and custom domains

**Azure Storage:**
- Blob Storage for file storage (test reports, screenshots)
- Access tiers (hot, cool, archive) for cost optimization
- Static website hosting capability
- Secure access via SAS tokens or managed identities

**Azure Key Vault:**
- Centralized secrets management service
- Hardware security module (HSM) backed
- RBAC and access policies for fine-grained control
- Audit logging for compliance

**Resource Groups:**
- Logical container for Azure resources
- Tag-based organization and cost tracking
- Lifecycle management for related resources
- Role-based access control (RBAC) at group level

## Azure Virtual Machines Deployment

Azure Virtual Machines provide full control over the test execution environment, ideal for complex test scenarios requiring specific configurations.

### VM Size Selection

Choose appropriate VM size based on test workload:

**Recommended Sizes:**

```bash
# Standard_D2s_v3: 2 vCPUs, 8 GB RAM - Good for sequential tests
# Standard_D4s_v3: 4 vCPUs, 16 GB RAM - Good for moderate parallelism
# Standard_D8s_v3: 8 vCPUs, 32 GB RAM - Good for high parallelism

# For compute-optimized parallel tests (recommended):
# Standard_F4s_v2: 4 vCPUs, 8 GB RAM - Cost-effective for CPU-intensive tests
# Standard_F8s_v2: 8 vCPUs, 16 GB RAM - High performance parallel execution
```

**Size Selection Criteria:**
- 1-2 parallel tests: Standard_D2s_v3 or Standard_F2s_v2
- 3-4 parallel tests: Standard_D4s_v3 or Standard_F4s_v2
- 5-8 parallel tests: Standard_D8s_v3 or Standard_F8s_v2
- 8+ parallel tests: Consider VM scale sets or larger compute-optimized sizes

### Image Selection

**Ubuntu 22.04 LTS from Azure Marketplace:**

```bash
# List available Ubuntu images
az vm image list --publisher Canonical --offer 0001-com-ubuntu-server-jammy --all --output table

# Recommended image
IMAGE_URN="Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest"
```

**Custom Image Creation Option:**

If you need a pre-configured environment, create a custom image:

```bash
# Create VM with your configuration
az vm create \
  --resource-group testinium-qa-rg \
  --name testinium-template-vm \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys

# SSH into VM and install framework
ssh azureuser@<VM_IP>

# Install Python, dependencies, and framework
# (See installation.md for setup steps)

# Generalize and capture image
sudo waagent -deprovision+user -force
exit

# Deallocate VM
az vm deallocate --resource-group testinium-qa-rg --name testinium-template-vm

# Mark as generalized
az vm generalize --resource-group testinium-qa-rg --name testinium-template-vm

# Create custom image
az image create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-python-image \
  --source testinium-template-vm
```

### Resource Group Creation

```bash
# Create resource group in preferred region
az group create \
  --name testinium-qa-rg \
  --location eastus \
  --tags Environment=Testing Project=TestiniumQA

# List available locations
az account list-locations --output table
```

### VM Creation Command

**Basic VM Creation:**

```bash
# Create VM with SSH key authentication
az vm create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm \
  --image UbuntuLTS \
  --size Standard_D4s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard \
  --nsg-rule SSH \
  --tags Environment=Testing Role=TestExecution

# Output includes public IP address for SSH access
```

**VM Creation with Custom Configuration:**

```bash
# Create VM with specific network and disk configuration
az vm create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm \
  --image UbuntuLTS \
  --size Standard_F4s_v2 \
  --admin-username azureuser \
  --ssh-key-values ~/.ssh/id_rsa.pub \
  --vnet-name testinium-vnet \
  --subnet testinium-subnet \
  --nsg testinium-nsg \
  --os-disk-size-gb 128 \
  --os-disk-name testinium-qa-vm-osdisk \
  --storage-sku Premium_LRS \
  --public-ip-address testinium-qa-pip \
  --public-ip-address-allocation static \
  --tags Environment=Testing Role=TestExecution CostCenter=QA

# Enable system-assigned managed identity
az vm identity assign \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm
```

### Custom Script Extension for Setup Automation

Automate framework installation using Azure VM extensions:

**Create setup script (setup-testinium-qa.sh):**

```bash
#!/bin/bash
set -e

# Update system
apt-get update
apt-get upgrade -y

# Install Python 3.11
apt-get install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install Chrome for Selenium tests
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Install ChromeDriver
apt-get install -y unzip
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1)
wget -q "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}" -O /tmp/chromedriver_version
CHROMEDRIVER_VERSION=$(cat /tmp/chromedriver_version)
wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -O /tmp/chromedriver.zip
unzip -o /tmp/chromedriver.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

# Create application directory
mkdir -p /opt/testinium-qa
cd /opt/testinium-qa

# Clone repository (replace with your repository URL)
# git clone https://github.com/your-org/testinium-qa-python.git .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create systemd service for scheduled test execution
cat > /etc/systemd/system/testinium-qa.service <<EOF
[Unit]
Description=Testinium QA Test Automation
After=network.target

[Service]
Type=oneshot
User=azureuser
WorkingDirectory=/opt/testinium-qa
Environment="PATH=/opt/testinium-qa/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/opt/testinium-qa/venv/bin/behave --tags=@Smoke
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create systemd timer for scheduled execution (daily at 2 AM)
cat > /etc/systemd/system/testinium-qa.timer <<EOF
[Unit]
Description=Testinium QA Test Automation Timer
Requires=testinium-qa.service

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Enable and start timer
systemctl daemon-reload
systemctl enable testinium-qa.timer
systemctl start testinium-qa.timer

echo "Testinium QA framework setup completed successfully"
```

**Deploy custom script extension:**

```bash
# Upload script to Azure Storage or use public URL
az vm extension set \
  --resource-group testinium-qa-rg \
  --vm-name testinium-qa-vm \
  --name customScript \
  --publisher Microsoft.Azure.Extensions \
  --settings '{"fileUris": ["https://your-storage-account.blob.core.windows.net/scripts/setup-testinium-qa.sh"],"commandToExecute": "bash setup-testinium-qa.sh"}'
```

### Connecting via SSH and Executing Tests

```bash
# Get VM public IP
VM_IP=$(az vm show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm \
  --show-details \
  --query publicIps \
  --output tsv)

# SSH into VM
ssh azureuser@${VM_IP}

# Navigate to framework directory
cd /opt/testinium-qa
source venv/bin/activate

# Run tests
behave --tags=@Smoke

# Run tests with specific configuration
behave --tags=@Login -D browser=chrome -D headless=true

# Run parallel tests (if behave-parallel installed)
behave --processes 4 --parallel-element scenario --tags=@Regression

# View test results
ls -lh reports/

# Copy reports to local machine
exit
scp -r azureuser@${VM_IP}:/opt/testinium-qa/reports/ ./azure-test-results/
```

### VM Scale Sets for Auto-Scaling Test Capacity

For dynamic test workloads, use VM Scale Sets:

```bash
# Create VM scale set
az vmss create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vmss \
  --image UbuntuLTS \
  --vm-sku Standard_F4s_v2 \
  --instance-count 2 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --load-balancer testinium-lb \
  --vnet-name testinium-vnet \
  --subnet testinium-subnet \
  --upgrade-policy-mode Automatic \
  --custom-data setup-testinium-qa.sh

# Configure auto-scaling based on CPU usage
az monitor autoscale create \
  --resource-group testinium-qa-rg \
  --resource testinium-qa-vmss \
  --resource-type Microsoft.Compute/virtualMachineScaleSets \
  --name testinium-autoscale \
  --min-count 1 \
  --max-count 10 \
  --count 2

# Scale out rule: Add instance when CPU > 75%
az monitor autoscale rule create \
  --resource-group testinium-qa-rg \
  --autoscale-name testinium-autoscale \
  --condition "Percentage CPU > 75 avg 5m" \
  --scale out 1

# Scale in rule: Remove instance when CPU < 25%
az monitor autoscale rule create \
  --resource-group testinium-qa-rg \
  --autoscale-name testinium-autoscale \
  --condition "Percentage CPU < 25 avg 5m" \
  --scale in 1
```

## Azure Container Instances Deployment

Azure Container Instances provide a lightweight, fast-starting option for containerized test execution without managing infrastructure.

### Docker Image Preparation

**Build Docker image:**

```dockerfile
# Dockerfile for Testinium QA Python framework
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d'.' -f1) \
    && wget -q "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}" -O /tmp/chromedriver_version \
    && CHROMEDRIVER_VERSION=$(cat /tmp/chromedriver_version) \
    && wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip -o /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy framework code
COPY . .

# Set environment variables for headless Chrome
ENV BROWSER_TYPE=chrome
ENV HEADLESS=true

# Run tests by default
CMD ["behave", "--tags=@Smoke"]
```

**Build and test locally:**

```bash
# Build image
docker build -t testinium-qa-python:latest .

# Test locally
docker run --rm testinium-qa-python:latest

# Test with environment variables
docker run --rm \
  -e BASE_URL=https://testinium.example.com \
  -e TEST_USERNAME=testuser@example.com \
  -e TEST_PASSWORD=secure_password \
  testinium-qa-python:latest
```

### Push to Azure Container Registry

```bash
# Create Azure Container Registry
az acr create \
  --resource-group testinium-qa-rg \
  --name testiniumqaacr \
  --sku Basic \
  --admin-enabled true

# Login to ACR
az acr login --name testiniumqaacr

# Tag image
docker tag testinium-qa-python:latest testiniumqaacr.azurecr.io/testinium-qa-python:latest
docker tag testinium-qa-python:latest testiniumqaacr.azurecr.io/testinium-qa-python:v1.0.0

# Push image
docker push testiniumqaacr.azurecr.io/testinium-qa-python:latest
docker push testiniumqaacr.azurecr.io/testinium-qa-python:v1.0.0

# Verify image
az acr repository list --name testiniumqaacr --output table
az acr repository show-tags --name testiniumqaacr --repository testinium-qa-python --output table
```

### Container Registry Setup

```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name testiniumqaacr --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name testiniumqaacr --query passwords[0].value --output tsv)

# Or use managed identity (recommended for production)
az acr update --name testiniumqaacr --admin-enabled false

# Create service principal for ACR access
az ad sp create-for-rbac \
  --name testinium-qa-acr-sp \
  --role acrpull \
  --scopes $(az acr show --name testiniumqaacr --query id --output tsv)
```

### Container Group Creation

**Basic container instance:**

```bash
# Create container instance
az container create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci \
  --image testiniumqaacr.azurecr.io/testinium-qa-python:latest \
  --registry-login-server testiniumqaacr.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --cpu 2 \
  --memory 4 \
  --restart-policy Never \
  --environment-variables \
    BASE_URL=https://testinium.example.com \
    BROWSER_TYPE=chrome \
    HEADLESS=true \
  --secure-environment-variables \
    TEST_USERNAME=testuser@example.com \
    TEST_PASSWORD=secure_password

# Monitor container status
az container show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci \
  --query instanceView.state

# View logs
az container logs \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci
```

**Container instance with Azure Files mount for report persistence:**

```bash
# Create Azure Files share
STORAGE_ACCOUNT_NAME=testiniumqastorage
az storage account create \
  --resource-group testinium-qa-rg \
  --name $STORAGE_ACCOUNT_NAME \
  --sku Standard_LRS

STORAGE_KEY=$(az storage account keys list \
  --resource-group testinium-qa-rg \
  --account-name $STORAGE_ACCOUNT_NAME \
  --query [0].value \
  --output tsv)

az storage share create \
  --name testinium-reports \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_KEY

# Create container with mounted volume
az container create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci-reports \
  --image testiniumqaacr.azurecr.io/testinium-qa-python:latest \
  --registry-login-server testiniumqaacr.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --cpu 2 \
  --memory 4 \
  --restart-policy Never \
  --azure-file-volume-share-name testinium-reports \
  --azure-file-volume-account-name $STORAGE_ACCOUNT_NAME \
  --azure-file-volume-account-key $STORAGE_KEY \
  --azure-file-volume-mount-path /app/reports \
  --environment-variables \
    BASE_URL=https://testinium.example.com \
    BROWSER_TYPE=chrome \
    HEADLESS=true

# Download reports after test completion
az storage file download-batch \
  --destination ./local-reports \
  --source testinium-reports \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_KEY
```

### CPU and Memory Allocation

**Recommended Resource Allocation:**

| Test Type | CPU Cores | Memory (GB) | Notes |
|-----------|-----------|-------------|-------|
| Sequential tests | 1 | 2 | Basic test execution |
| Parallel (2-4 tests) | 2 | 4 | Recommended minimum |
| Parallel (5-8 tests) | 4 | 8 | High parallelism |
| Data-intensive tests | 2 | 8 | Large reports/screenshots |

**Configure resources:**

```bash
az container create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci \
  --image testiniumqaacr.azurecr.io/testinium-qa-python:latest \
  --cpu 2 \
  --memory 4 \
  # ... other parameters
```

### Scheduled Container Instances with Logic Apps

**Create Logic App for scheduled test execution:**

```bash
# Create Logic App
az logic workflow create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-scheduler \
  --definition @logic-app-definition.json

# Logic App definition (logic-app-definition.json)
```

```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "triggers": {
      "Recurrence": {
        "type": "Recurrence",
        "recurrence": {
          "frequency": "Day",
          "interval": 1,
          "schedule": {
            "hours": ["2"],
            "minutes": [0]
          },
          "timeZone": "UTC"
        }
      }
    },
    "actions": {
      "Create_Container_Instance": {
        "type": "Http",
        "inputs": {
          "method": "PUT",
          "uri": "https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/testinium-qa-rg/providers/Microsoft.ContainerInstance/containerGroups/testinium-qa-aci-scheduled?api-version=2021-09-01",
          "authentication": {
            "type": "ManagedServiceIdentity"
          },
          "body": {
            "location": "eastus",
            "properties": {
              "containers": [{
                "name": "testinium-qa-container",
                "properties": {
                  "image": "testiniumqaacr.azurecr.io/testinium-qa-python:latest",
                  "resources": {
                    "requests": {
                      "cpu": 2,
                      "memoryInGB": 4
                    }
                  },
                  "environmentVariables": [
                    {"name": "BASE_URL", "value": "https://testinium.example.com"},
                    {"name": "HEADLESS", "value": "true"}
                  ]
                }
              }],
              "osType": "Linux",
              "restartPolicy": "Never"
            }
          }
        }
      }
    }
  }
}
```

### Monitoring Container Logs

```bash
# View real-time logs
az container logs \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci \
  --follow

# View logs with timestamps
az container logs \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci \
  --timestamps

# Export logs to file
az container logs \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci > container-logs.txt

# Attach to container for interactive debugging
az container attach \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci
```

## Azure App Service Containerized Deployment

Azure App Service provides a fully managed platform for hosting containerized test automation with built-in scaling and deployment features.

### App Service Plan Creation

```bash
# Create Linux App Service plan
az appservice plan create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-plan \
  --is-linux \
  --sku B2 \
  --number-of-workers 1

# Recommended SKUs:
# B2: 2 cores, 3.5 GB RAM - Development/testing
# P1V2: 1 core, 3.5 GB RAM - Production (auto-scale capable)
# P2V2: 2 cores, 7 GB RAM - Production with moderate load
# P3V2: 4 cores, 14 GB RAM - Production with high load
```

### Web App Creation with Container

```bash
# Create web app with container
az webapp create \
  --resource-group testinium-qa-rg \
  --plan testinium-qa-plan \
  --name testinium-qa-app \
  --deployment-container-image-name testiniumqaacr.azurecr.io/testinium-qa-python:latest

# Configure container settings
az webapp config container set \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --docker-custom-image-name testiniumqaacr.azurecr.io/testinium-qa-python:latest \
  --docker-registry-server-url https://testiniumqaacr.azurecr.io \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Enable system-assigned managed identity
az webapp identity assign \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app

# Grant ACR pull permissions to managed identity
PRINCIPAL_ID=$(az webapp identity show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --query principalId \
  --output tsv)

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role acrpull \
  --scope $(az acr show --name testiniumqaacr --query id --output tsv)

# Remove registry credentials (use managed identity instead)
az webapp config container set \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --docker-custom-image-name testiniumqaacr.azurecr.io/testinium-qa-python:latest \
  --docker-registry-server-url https://testiniumqaacr.azurecr.io
```

### Continuous Deployment from ACR

```bash
# Enable continuous deployment (webhook from ACR)
az webapp deployment container config \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --enable-cd true

# Get webhook URL
WEBHOOK_URL=$(az webapp deployment container show-cd-url \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --query CI_CD_URL \
  --output tsv)

# Create ACR webhook
az acr webhook create \
  --resource-group testinium-qa-rg \
  --registry testiniumqaacr \
  --name testiniumQaWebhook \
  --actions push \
  --uri $WEBHOOK_URL \
  --scope testinium-qa-python:*
```

### Application Settings for Environment Variables

```bash
# Configure application settings (environment variables)
az webapp config appsettings set \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --settings \
    BASE_URL=https://testinium.example.com \
    BROWSER_TYPE=chrome \
    HEADLESS=true \
    TIMEOUT_EXPLICIT=10 \
    SCREENSHOTS_ON_FAILURE=true

# Configure secrets from Key Vault (recommended)
# See Azure Key Vault section below
```

### Startup Command Configuration

```bash
# Set custom startup command
az webapp config set \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --startup-file "behave --tags=@Smoke"

# For scheduled tests, use Azure Functions or Logic Apps
# App Service is better suited for API-triggered test execution
```

### Accessing Logs

```bash
# Enable application logging
az webapp log config \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --application-logging filesystem \
  --level information \
  --docker-container-logging filesystem

# Stream logs in real-time
az webapp log tail \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app

# Download logs
az webapp log download \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --log-file app-logs.zip

# View logs in Azure Portal
# Portal → App Service → Logs → Log stream
```

## Azure Blob Storage for Test Reports

Azure Blob Storage provides scalable, cost-effective storage for test reports, screenshots, and artifacts with global access capabilities.

### Storage Account Creation

```bash
# Create storage account
STORAGE_ACCOUNT_NAME=testiniumqastorage
az storage account create \
  --resource-group testinium-qa-rg \
  --name $STORAGE_ACCOUNT_NAME \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2 \
  --access-tier Hot \
  --https-only true \
  --min-tls-version TLS1_2

# Enable static website hosting for HTML reports
az storage blob service-properties update \
  --account-name $STORAGE_ACCOUNT_NAME \
  --static-website \
  --404-document 404.html \
  --index-document index.html

# Get static website URL
STATIC_WEBSITE_URL=$(az storage account show \
  --name $STORAGE_ACCOUNT_NAME \
  --query primaryEndpoints.web \
  --output tsv)

echo "Static website URL: $STATIC_WEBSITE_URL"
```

### Container Creation for Reports

```bash
# Get storage account key
STORAGE_KEY=$(az storage account keys list \
  --resource-group testinium-qa-rg \
  --account-name $STORAGE_ACCOUNT_NAME \
  --query [0].value \
  --output tsv)

# Create containers for different report types
az storage container create \
  --name test-reports \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_KEY \
  --public-access off

az storage container create \
  --name screenshots \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_KEY \
  --public-access off

az storage container create \
  --name allure-reports \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_KEY \
  --public-access blob

# Container for archival (will move to cool tier)
az storage container create \
  --name archived-reports \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_KEY \
  --public-access off
```

### Uploading Reports with Azure SDK

**Install Azure Storage SDK:**

```bash
# Add to requirements.txt
echo "azure-storage-blob==12.19.0" >> requirements.txt
pip install azure-storage-blob==12.19.0
```

**Update environment.py to upload reports:**

```python
# features/environment.py - Add after_all hook for report upload

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import os
from datetime import datetime

def after_all(context):
    """
    Upload test reports to Azure Blob Storage after all tests complete.
    
    Uses managed identity for authentication in Azure environments.
    Falls back to connection string for local development.
    """
    # Try managed identity first (production)
    try:
        account_url = f"https://{os.getenv('AZURE_STORAGE_ACCOUNT_NAME')}.blob.core.windows.net"
        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
    except Exception:
        # Fallback to connection string (development)
        connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if connection_string:
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        else:
            print("Warning: Azure Storage not configured. Skipping report upload.")
            return
    
    # Generate timestamp for report organization
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Upload reports directory
    reports_dir = 'reports'
    if os.path.exists(reports_dir):
        upload_directory_to_blob(
            blob_service_client,
            'test-reports',
            reports_dir,
            f"{timestamp}/"
        )
        print(f"Reports uploaded to Azure Blob Storage: test-reports/{timestamp}/")
    
def upload_directory_to_blob(blob_service_client, container_name, source_dir, blob_prefix):
    """Upload entire directory to Azure Blob Storage."""
    container_client = blob_service_client.get_container_client(container_name)
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Calculate blob name with prefix
            relative_path = os.path.relpath(file_path, source_dir)
            blob_name = blob_prefix + relative_path.replace(os.sep, '/')
            
            # Upload file
            with open(file_path, 'rb') as data:
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.upload_blob(data, overwrite=True)
                print(f"Uploaded: {blob_name}")
```

**Configure environment variables:**

```bash
# For managed identity (production - VMs, ACI, App Service)
export AZURE_STORAGE_ACCOUNT_NAME=testiniumqastorage

# For local development with connection string
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=testiniumqastorage;AccountKey=YOUR_KEY;EndpointSuffix=core.windows.net"
```

### Blob Access Tiers

**Configure lifecycle management for cost optimization:**

```bash
# Create lifecycle policy JSON
cat > lifecycle-policy.json <<EOF
{
  "rules": [
    {
      "enabled": true,
      "name": "MoveToArchive",
      "type": "Lifecycle",
      "definition": {
        "actions": {
          "baseBlob": {
            "tierToCool": {
              "daysAfterModificationGreaterThan": 30
            },
            "tierToArchive": {
              "daysAfterModificationGreaterThan": 90
            },
            "delete": {
              "daysAfterModificationGreaterThan": 365
            }
          }
        },
        "filters": {
          "blobTypes": ["blockBlob"],
          "prefixMatch": ["test-reports/", "screenshots/"]
        }
      }
    }
  ]
}
EOF

# Apply lifecycle policy
az storage account management-policy create \
  --account-name $STORAGE_ACCOUNT_NAME \
  --policy @lifecycle-policy.json
```

**Access Tiers:**
- **Hot**: Recent reports (< 30 days) - Frequent access, higher storage cost
- **Cool**: Archived reports (30-90 days) - Infrequent access, lower storage cost
- **Archive**: Long-term retention (> 90 days) - Rare access, lowest storage cost

### Static Website Hosting for HTML Reports

```bash
# Upload HTML reports to $web container (static website)
az storage blob upload-batch \
  --destination '$web' \
  --source reports/behave-reports \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_KEY \
  --pattern "*.html" \
  --overwrite

# Upload Allure reports
az storage blob upload-batch \
  --destination '$web/allure' \
  --source reports/allure-results \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_KEY \
  --overwrite

# Access reports via static website URL
echo "View reports at: ${STATIC_WEBSITE_URL}"
```

### SAS Tokens for Secure Access

**Generate SAS token for time-limited access:**

```bash
# Generate SAS token valid for 7 days with read-only access
END_DATE=$(date -u -d "7 days" '+%Y-%m-%dT%H:%MZ')

SAS_TOKEN=$(az storage container generate-sas \
  --name test-reports \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_KEY \
  --permissions r \
  --expiry $END_DATE \
  --output tsv)

# Construct secure URL
REPORT_URL="https://${STORAGE_ACCOUNT_NAME}.blob.core.windows.net/test-reports/20240115_143000/report.html?${SAS_TOKEN}"

echo "Secure report URL (valid for 7 days): $REPORT_URL"
```

**Generate account-level SAS for programmatic access:**

```bash
# Account SAS for blob and file services
az storage account generate-sas \
  --account-name $STORAGE_ACCOUNT_NAME \
  --account-key $STORAGE_KEY \
  --services b \
  --resource-types sco \
  --permissions rl \
  --expiry $END_DATE \
  --https-only \
  --output tsv
```

### CDN Integration for Global Distribution

```bash
# Create Azure CDN profile
az cdn profile create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-cdn \
  --sku Standard_Microsoft

# Create CDN endpoint for static website
az cdn endpoint create \
  --resource-group testinium-qa-rg \
  --profile-name testinium-qa-cdn \
  --name testinium-qa-reports \
  --origin ${STORAGE_ACCOUNT_NAME}.z13.web.core.windows.net \
  --origin-host-header ${STORAGE_ACCOUNT_NAME}.z13.web.core.windows.net \
  --enable-compression true \
  --content-types-to-compress \
    "text/html" \
    "text/css" \
    "application/javascript" \
    "application/json"

# Get CDN endpoint URL
CDN_URL=$(az cdn endpoint show \
  --resource-group testinium-qa-rg \
  --profile-name testinium-qa-cdn \
  --name testinium-qa-reports \
  --query hostName \
  --output tsv)

echo "CDN URL: https://${CDN_URL}"
```

## Azure Key Vault for Secrets Management

Azure Key Vault provides centralized, secure storage for test credentials and sensitive configuration with hardware-backed encryption and audit logging.

### Key Vault Creation

```bash
# Create Key Vault
az keyvault create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-kv \
  --location eastus \
  --enable-rbac-authorization false \
  --enabled-for-deployment true \
  --enabled-for-template-deployment true

# Enable soft-delete and purge protection (recommended for production)
az keyvault update \
  --resource-group testinium-qa-rg \
  --name testinium-qa-kv \
  --enable-soft-delete true \
  --enable-purge-protection true
```

### Storing Secrets

**Store test credentials in Key Vault:**

```bash
# Store generic test user credentials
az keyvault secret set \
  --vault-name testinium-qa-kv \
  --name testinium-qa-test-username \
  --value "testuser@example.com"

az keyvault secret set \
  --vault-name testinium-qa-kv \
  --name testinium-qa-test-password \
  --value "secure_password_here"

# Store sales manager credentials (config.yaml lines 103-104)
az keyvault secret set \
  --vault-name testinium-qa-kv \
  --name testinium-qa-sales-manager-username \
  --value "salesmanager@example.com"

az keyvault secret set \
  --vault-name testinium-qa-kv \
  --name testinium-qa-sales-manager-password \
  --value "sales_secure_password"

# Store POS manager credentials (config.yaml lines 109-110)
az keyvault secret set \
  --vault-name testinium-qa-kv \
  --name testinium-qa-pos-manager-username \
  --value "posmanager@example.com"

az keyvault secret set \
  --vault-name testinium-qa-kv \
  --name testinium-qa-pos-manager-password \
  --value "pos_secure_password"

# Store database connection string (if applicable)
az keyvault secret set \
  --vault-name testinium-qa-kv \
  --name testinium-qa-db-connection-string \
  --value "Server=db.example.com;Database=testinium;User=dbuser;Password=dbpass"

# List all secrets
az keyvault secret list --vault-name testinium-qa-kv --output table
```

### Secret Naming Convention

**Recommended naming pattern:**
- Format: `<project>-<environment>-<secret-type>`
- Examples:
  - `testinium-qa-test-username`
  - `testinium-qa-test-password`
  - `testinium-qa-sales-manager-username`
  - `testinium-qa-db-connection-string`

### Accessing Secrets in Application

**Install Azure Key Vault SDK:**

```bash
# Add to requirements.txt
echo "azure-identity==1.15.0" >> requirements.txt
echo "azure-keyvault-secrets==4.7.0" >> requirements.txt
pip install azure-identity==1.15.0 azure-keyvault-secrets==4.7.0
```

**Update config_reader.py to retrieve secrets from Key Vault:**

```python
# utilities/config_reader.py - Add Key Vault integration

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError
import os

class ConfigReader:
    """Enhanced configuration reader with Azure Key Vault support."""
    
    def __init__(self):
        # Existing initialization...
        self._kv_client = None
        self._init_key_vault()
    
    def _init_key_vault(self):
        """Initialize Azure Key Vault client if configured."""
        vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
        if vault_name:
            try:
                vault_url = f"https://{vault_name}.vault.azure.net"
                credential = DefaultAzureCredential()
                self._kv_client = SecretClient(vault_url=vault_url, credential=credential)
                print(f"Azure Key Vault initialized: {vault_name}")
            except Exception as e:
                print(f"Warning: Could not initialize Key Vault: {e}")
                self._kv_client = None
    
    def get_secret(self, secret_name):
        """
        Retrieve secret from Azure Key Vault.
        
        Args:
            secret_name (str): Name of the secret in Key Vault
            
        Returns:
            str: Secret value or None if not found
        """
        if not self._kv_client:
            return None
        
        try:
            secret = self._kv_client.get_secret(secret_name)
            return secret.value
        except ResourceNotFoundError:
            return None
        except Exception as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            return None
    
    def get_property_with_keyvault(self, property_key, secret_name=None):
        """
        Get property with Key Vault fallback.
        
        First tries environment variable, then config file, then Key Vault.
        
        Args:
            property_key (str): Property key in config
            secret_name (str): Key Vault secret name (optional)
            
        Returns:
            str: Property value
        """
        # Try standard property resolution first
        value = self.get_property(property_key)
        
        # If not found and secret_name provided, try Key Vault
        if not value and secret_name and self._kv_client:
            value = self.get_secret(secret_name)
        
        return value
```

**Usage in step definitions:**

```python
# features/steps/login_steps.py - Use Key Vault for credentials

from utilities.config_reader import ConfigReader
import os

config = ConfigReader()

@given('I navigate to the login page')
def step_navigate_to_login(context):
    # Get credentials from Key Vault
    vault_name = os.getenv('AZURE_KEY_VAULT_NAME')  # testinium-qa-kv
    
    if vault_name:
        # Retrieve from Key Vault
        context.test_username = config.get_secret('testinium-qa-test-username')
        context.test_password = config.get_secret('testinium-qa-test-password')
    else:
        # Fallback to environment variables or config file
        context.test_username = config.get_property('credentials.username')
        context.test_password = config.get_property('credentials.password')
```

### Managed Identity for Key Vault Access

**Grant Key Vault access to managed identity:**

```bash
# For VM
VM_PRINCIPAL_ID=$(az vm identity show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm \
  --query principalId \
  --output tsv)

az keyvault set-policy \
  --name testinium-qa-kv \
  --object-id $VM_PRINCIPAL_ID \
  --secret-permissions get list

# For Container Instance (requires user-assigned identity)
# Create user-assigned identity
az identity create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-identity

IDENTITY_ID=$(az identity show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-identity \
  --query id \
  --output tsv)

IDENTITY_PRINCIPAL_ID=$(az identity show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-identity \
  --query principalId \
  --output tsv)

# Grant Key Vault access to identity
az keyvault set-policy \
  --name testinium-qa-kv \
  --object-id $IDENTITY_PRINCIPAL_ID \
  --secret-permissions get list

# Assign identity to container instance
az container create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci-kv \
  --image testiniumqaacr.azurecr.io/testinium-qa-python:latest \
  --assign-identity $IDENTITY_ID \
  --environment-variables \
    AZURE_KEY_VAULT_NAME=testinium-qa-kv \
  # ... other parameters

# For App Service
APP_PRINCIPAL_ID=$(az webapp identity show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --query principalId \
  --output tsv)

az keyvault set-policy \
  --name testinium-qa-kv \
  --object-id $APP_PRINCIPAL_ID \
  --secret-permissions get list
```

### RBAC Permissions for Secret Access

**Alternative to access policies (RBAC model - recommended for new deployments):**

```bash
# Enable RBAC authorization on Key Vault
az keyvault update \
  --resource-group testinium-qa-rg \
  --name testinium-qa-kv \
  --enable-rbac-authorization true

# Assign Key Vault Secrets User role to managed identity
az role assignment create \
  --assignee $VM_PRINCIPAL_ID \
  --role "Key Vault Secrets User" \
  --scope $(az keyvault show --name testinium-qa-kv --query id --output tsv)
```

### Avoiding Hardcoded Credentials

**Best practices:**

1. **Never commit credentials to source control**
   - Use `.gitignore` for `.env` files
   - Scan commits for exposed secrets

2. **Use managed identities in Azure**
   - No credentials in code or configuration
   - Automatic token management

3. **Rotate secrets regularly**
   - Set expiration dates on secrets
   - Implement rotation procedures

4. **Audit secret access**
   - Enable Key Vault diagnostic logging
   - Review access logs regularly

### Secret Rotation Policies

```bash
# Set secret expiration (90 days)
EXPIRY_DATE=$(date -u -d "90 days" '+%Y-%m-%dT%H:%M:%SZ')

az keyvault secret set \
  --vault-name testinium-qa-kv \
  --name testinium-qa-test-password \
  --value "new_secure_password" \
  --expires $EXPIRY_DATE

# Enable secret rotation notification
# Create Logic App or Azure Function to handle rotation
```

## Azure Monitor Integration

Azure Monitor provides comprehensive observability for test execution with logs, metrics, and alerting capabilities.

### Log Analytics Workspace Setup

```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group testinium-qa-rg \
  --workspace-name testinium-qa-workspace \
  --location eastus \
  --sku PerGB2018

# Get workspace ID
WORKSPACE_ID=$(az monitor log-analytics workspace show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-workspace \
  --query customerId \
  --output tsv)

echo "Workspace ID: $WORKSPACE_ID"
```

### Diagnostic Settings for VMs and Containers

**Enable diagnostics for VM:**

```bash
# Enable boot diagnostics for VM
az vm boot-diagnostics enable \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm \
  --storage https://${STORAGE_ACCOUNT_NAME}.blob.core.windows.net

# Install Log Analytics agent on VM (Linux)
az vm extension set \
  --resource-group testinium-qa-rg \
  --vm-name testinium-qa-vm \
  --name OmsAgentForLinux \
  --publisher Microsoft.EnterpriseCloud.Monitoring \
  --settings "{\"workspaceId\":\"$WORKSPACE_ID\"}" \
  --protected-settings "{\"workspaceKey\":\"$(az monitor log-analytics workspace get-shared-keys --resource-group testinium-qa-rg --workspace-name testinium-qa-workspace --query primarySharedKey --output tsv)\"}"
```

**Enable diagnostics for Container Instances:**

```bash
# Create container with Log Analytics integration
az container create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci-logs \
  --image testiniumqaacr.azurecr.io/testinium-qa-python:latest \
  --log-analytics-workspace $WORKSPACE_ID \
  --log-analytics-workspace-key $(az monitor log-analytics workspace get-shared-keys \
    --resource-group testinium-qa-rg \
    --workspace-name testinium-qa-workspace \
    --query primarySharedKey \
    --output tsv)
```

### Custom Logs from Test Execution

**Configure custom logging to Azure Monitor:**

```python
# features/environment.py - Add Azure Monitor logging

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
import os

def before_all(context):
    """Configure Azure Monitor logging before test execution."""
    
    # Get Application Insights connection string from environment
    connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
    
    if connection_string:
        # Configure Azure Monitor handler
        logger = logging.getLogger(__name__)
        logger.addHandler(AzureLogHandler(connection_string=connection_string))
        logger.setLevel(logging.INFO)
        
        context.azure_logger = logger
        context.azure_logger.info("Test execution started", extra={
            'custom_dimensions': {
                'test_suite': 'testinium-qa-python',
                'environment': os.getenv('BASE_URL', 'unknown')
            }
        })

def after_scenario(context, scenario):
    """Log scenario results to Azure Monitor."""
    
    if hasattr(context, 'azure_logger'):
        status = 'passed' if scenario.status == 'passed' else 'failed'
        context.azure_logger.info(f"Scenario {status}: {scenario.name}", extra={
            'custom_dimensions': {
                'scenario_name': scenario.name,
                'status': status,
                'duration': scenario.duration,
                'tags': ','.join(scenario.tags)
            }
        })
```

**Install dependencies:**

```bash
echo "opencensus-ext-azure==1.1.9" >> requirements.txt
pip install opencensus-ext-azure==1.1.9
```

### Application Insights for Detailed Telemetry

**Create Application Insights resource:**

```bash
# Create Application Insights (workspace-based)
az monitor app-insights component create \
  --resource-group testinium-qa-rg \
  --app testinium-qa-insights \
  --location eastus \
  --workspace $(az monitor log-analytics workspace show \
    --resource-group testinium-qa-rg \
    --workspace-name testinium-qa-workspace \
    --query id \
    --output tsv)

# Get connection string
APP_INSIGHTS_CONNECTION=$(az monitor app-insights component show \
  --resource-group testinium-qa-rg \
  --app testinium-qa-insights \
  --query connectionString \
  --output tsv)

echo "Application Insights Connection String: $APP_INSIGHTS_CONNECTION"

# Set as environment variable for tests
export APPLICATIONINSIGHTS_CONNECTION_STRING="$APP_INSIGHTS_CONNECTION"
```

### Query Logs with KQL

**Example KQL queries in Log Analytics:**

```kusto
-- Query container logs
ContainerInstanceLog_CL
| where TimeGenerated > ago(1h)
| where ContainerGroup_s == "testinium-qa-aci"
| project TimeGenerated, Message
| order by TimeGenerated desc

-- Query test execution custom logs
traces
| where customDimensions.test_suite == "testinium-qa-python"
| where timestamp > ago(24h)
| extend scenario_name = tostring(customDimensions.scenario_name)
| extend status = tostring(customDimensions.status)
| summarize count() by status, bin(timestamp, 1h)
| render timechart

-- Failed scenarios
traces
| where customDimensions.test_suite == "testinium-qa-python"
| where customDimensions.status == "failed"
| where timestamp > ago(7d)
| project timestamp, scenario_name = tostring(customDimensions.scenario_name)
| order by timestamp desc

-- Average test duration by scenario
traces
| where customDimensions.test_suite == "testinium-qa-python"
| extend scenario_name = tostring(customDimensions.scenario_name)
| extend duration = todouble(customDimensions.duration)
| summarize avg_duration = avg(duration) by scenario_name
| order by avg_duration desc

-- Test execution trends
traces
| where customDimensions.test_suite == "testinium-qa-python"
| where timestamp > ago(30d)
| extend status = tostring(customDimensions.status)
| summarize passed = countif(status == "passed"), 
            failed = countif(status == "failed") 
            by bin(timestamp, 1d)
| extend pass_rate = (passed * 100.0) / (passed + failed)
| render timechart
```

### Workbooks for Test Result Visualization

**Create custom workbook:**

1. Navigate to Azure Portal → Monitor → Workbooks
2. Click "New" to create blank workbook
3. Add queries for test metrics:
   - Test execution count over time
   - Pass/fail rate trends
   - Average test duration
   - Failed scenarios list
4. Save workbook as "Testinium QA Test Results Dashboard"

**Example workbook JSON template available in Azure Portal**

## Networking Configuration

Secure network configuration for test resources with virtual networks, network security groups, and private connectivity.

### Virtual Network (VNet) Setup

```bash
# Create Virtual Network
az network vnet create \
  --resource-group testinium-qa-rg \
  --name testinium-vnet \
  --address-prefix 10.0.0.0/16 \
  --location eastus

# Create subnet for test VMs
az network vnet subnet create \
  --resource-group testinium-qa-rg \
  --vnet-name testinium-vnet \
  --name testinium-vm-subnet \
  --address-prefix 10.0.1.0/24

# Create subnet for App Service integration
az network vnet subnet create \
  --resource-group testinium-qa-rg \
  --vnet-name testinium-vnet \
  --name testinium-app-subnet \
  --address-prefix 10.0.2.0/24 \
  --delegations Microsoft.Web/serverFarms

# Create subnet for private endpoints
az network vnet subnet create \
  --resource-group testinium-qa-rg \
  --vnet-name testinium-vnet \
  --name testinium-pe-subnet \
  --address-prefix 10.0.3.0/24 \
  --disable-private-endpoint-network-policies true
```

### Network Security Groups (NSG)

```bash
# Create NSG for test VMs
az network nsg create \
  --resource-group testinium-qa-rg \
  --name testinium-vm-nsg \
  --location eastus

# Allow SSH from specific IP (replace with your IP)
az network nsg rule create \
  --resource-group testinium-qa-rg \
  --nsg-name testinium-vm-nsg \
  --name AllowSSH \
  --priority 1000 \
  --source-address-prefixes <YOUR_IP>/32 \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 22 \
  --access Allow \
  --protocol Tcp \
  --description "Allow SSH from management IP"

# Allow outbound HTTPS for test execution
az network nsg rule create \
  --resource-group testinium-qa-rg \
  --nsg-name testinium-vm-nsg \
  --name AllowOutboundHTTPS \
  --priority 2000 \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 443 \
  --access Allow \
  --protocol Tcp \
  --direction Outbound \
  --description "Allow outbound HTTPS for test execution"

# Deny all other inbound traffic
az network nsg rule create \
  --resource-group testinium-qa-rg \
  --nsg-name testinium-vm-nsg \
  --name DenyAllInbound \
  --priority 4096 \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges '*' \
  --access Deny \
  --protocol '*' \
  --description "Deny all other inbound traffic"

# Associate NSG with subnet
az network vnet subnet update \
  --resource-group testinium-qa-rg \
  --vnet-name testinium-vnet \
  --name testinium-vm-subnet \
  --network-security-group testinium-vm-nsg
```

### Private Endpoints for Secure Service Access

**Create private endpoint for Storage Account:**

```bash
# Disable public network access to storage account
az storage account update \
  --resource-group testinium-qa-rg \
  --name $STORAGE_ACCOUNT_NAME \
  --default-action Deny

# Create private endpoint
az network private-endpoint create \
  --resource-group testinium-qa-rg \
  --name testinium-storage-pe \
  --vnet-name testinium-vnet \
  --subnet testinium-pe-subnet \
  --private-connection-resource-id $(az storage account show \
    --resource-group testinium-qa-rg \
    --name $STORAGE_ACCOUNT_NAME \
    --query id \
    --output tsv) \
  --group-id blob \
  --connection-name testinium-storage-connection

# Create private DNS zone
az network private-dns zone create \
  --resource-group testinium-qa-rg \
  --name privatelink.blob.core.windows.net

# Link DNS zone to VNet
az network private-dns link vnet create \
  --resource-group testinium-qa-rg \
  --zone-name privatelink.blob.core.windows.net \
  --name testinium-dns-link \
  --virtual-network testinium-vnet \
  --registration-enabled false

# Create DNS records for private endpoint
az network private-endpoint dns-zone-group create \
  --resource-group testinium-qa-rg \
  --endpoint-name testinium-storage-pe \
  --name testinium-storage-dns-group \
  --private-dns-zone privatelink.blob.core.windows.net \
  --zone-name privatelink.blob.core.windows.net
```

**Create private endpoint for Key Vault:**

```bash
# Disable public access to Key Vault
az keyvault update \
  --resource-group testinium-qa-rg \
  --name testinium-qa-kv \
  --public-network-access Disabled

# Create private endpoint for Key Vault
az network private-endpoint create \
  --resource-group testinium-qa-rg \
  --name testinium-kv-pe \
  --vnet-name testinium-vnet \
  --subnet testinium-pe-subnet \
  --private-connection-resource-id $(az keyvault show \
    --resource-group testinium-qa-rg \
    --name testinium-qa-kv \
    --query id \
    --output tsv) \
  --group-id vault \
  --connection-name testinium-kv-connection

# Configure private DNS for Key Vault
az network private-dns zone create \
  --resource-group testinium-qa-rg \
  --name privatelink.vaultcore.azure.net

az network private-dns link vnet create \
  --resource-group testinium-qa-rg \
  --zone-name privatelink.vaultcore.azure.net \
  --name testinium-kv-dns-link \
  --virtual-network testinium-vnet \
  --registration-enabled false

az network private-endpoint dns-zone-group create \
  --resource-group testinium-qa-rg \
  --endpoint-name testinium-kv-pe \
  --name testinium-kv-dns-group \
  --private-dns-zone privatelink.vaultcore.azure.net \
  --zone-name privatelink.vaultcore.azure.net
```

### VNet Integration for App Service

```bash
# Enable VNet integration for App Service
az webapp vnet-integration add \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app \
  --vnet testinium-vnet \
  --subnet testinium-app-subnet

# Verify VNet integration
az webapp vnet-integration list \
  --resource-group testinium-qa-rg \
  --name testinium-qa-app
```

### Azure Bastion for Secure VM Access

**Deploy Azure Bastion for SSH without public IPs:**

```bash
# Create subnet for Bastion (must be named AzureBastionSubnet)
az network vnet subnet create \
  --resource-group testinium-qa-rg \
  --vnet-name testinium-vnet \
  --name AzureBastionSubnet \
  --address-prefix 10.0.255.0/27

# Create public IP for Bastion
az network public-ip create \
  --resource-group testinium-qa-rg \
  --name testinium-bastion-pip \
  --sku Standard \
  --location eastus

# Create Azure Bastion host
az network bastion create \
  --resource-group testinium-qa-rg \
  --name testinium-bastion \
  --vnet-name testinium-vnet \
  --public-ip-address testinium-bastion-pip \
  --location eastus

# Access VMs via Azure Portal → Virtual Machines → Connect → Bastion
# Or use Azure CLI (requires az extension add -n ssh)
az network bastion ssh \
  --resource-group testinium-qa-rg \
  --name testinium-bastion \
  --target-resource-id $(az vm show \
    --resource-group testinium-qa-rg \
    --name testinium-qa-vm \
    --query id \
    --output tsv) \
  --auth-type ssh-key \
  --username azureuser \
  --ssh-key ~/.ssh/id_rsa
```

## Azure DevOps Integration

Azure DevOps provides native integration with Azure services for complete CI/CD pipeline management.

### Azure Pipelines Integration

**For detailed Azure DevOps pipeline configuration, see [azure-devops.md](azure-devops.md).**

**Quick integration overview:**

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '3.11'

stages:
  - stage: Test
    jobs:
      - job: RunTests
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '$(pythonVersion)'
          
          - script: |
              python -m venv venv
              source venv/bin/activate
              pip install -r requirements.txt
            displayName: 'Install dependencies'
          
          - script: |
              source venv/bin/activate
              behave --tags=@Smoke --junit --junit-directory $(Build.ArtifactStagingDirectory)/junit
            displayName: 'Run tests'
          
          - task: PublishTestResults@2
            inputs:
              testResultsFormat: 'JUnit'
              testResultsFiles: '$(Build.ArtifactStagingDirectory)/junit/*.xml'
```

### Azure Repos for Source Control

- Native Git repository integration
- Pull request workflows
- Branch policies and approvals
- Code review features

### Azure Boards for Test Tracking

- Work item tracking for test cases
- Integration with test execution results
- Sprint planning and backlog management
- Jira integration available via marketplace

### Azure Artifacts for Package Management

- Python package hosting
- Private PyPI feed
- Dependency caching for faster builds

## Cost Management

Optimize Azure costs while maintaining test execution performance and reliability.

### Azure Cost Management

```bash
# View current costs for resource group
az costmanagement query \
  --type Usage \
  --dataset-filter "{\"and\":[{\"or\":[{\"dimensions\":{\"name\":\"ResourceGroupName\",\"operator\":\"In\",\"values\":[\"testinium-qa-rg\"]}}]}]}" \
  --timeframe MonthToDate \
  --dataset-aggregation "{\"totalCost\":{\"name\":\"PreTaxCost\",\"function\":\"Sum\"}}" \
  --dataset-grouping name=ResourceType function=Sum

# Cost by resource
az costmanagement query \
  --type Usage \
  --dataset-filter "{\"dimensions\":{\"name\":\"ResourceGroupName\",\"operator\":\"In\",\"values\":[\"testinium-qa-rg\"]}}" \
  --timeframe MonthToDate \
  --dataset-aggregation "{\"totalCost\":{\"name\":\"PreTaxCost\",\"function\":\"Sum\"}}" \
  --dataset-grouping name=ResourceId function=Sum \
  --query "[].{Resource:name,Cost:properties.cost}" \
  --output table
```

### Budget Alerts

```bash
# Create budget with alert
az consumption budget create \
  --resource-group testinium-qa-rg \
  --budget-name testinium-qa-budget \
  --amount 500 \
  --time-grain Monthly \
  --start-date 2024-01-01T00:00:00Z \
  --end-date 2025-12-31T23:59:59Z \
  --notifications \
    Actual_GreaterThan_80_Percent='{
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 80,
      "contactEmails": ["admin@example.com"],
      "contactRoles": ["Contributor"],
      "contactGroups": [],
      "thresholdType": "Actual"
    }' \
    Forecasted_GreaterThan_100_Percent='{
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 100,
      "contactEmails": ["admin@example.com"],
      "contactRoles": ["Contributor"],
      "contactGroups": [],
      "thresholdType": "Forecasted"
    }'
```

### Reserved Instances for VMs

**Save up to 72% with reserved instances:**

```bash
# List available reserved instance offers
az reservations catalog show \
  --subscription-id $(az account show --query id --output tsv) \
  --reserved-resource-type VirtualMachines \
  --location eastus

# Purchase 1-year reserved instance
az reservations reservation-order purchase \
  --reservation-order-id <order-id> \
  --sku Standard_D4s_v3 \
  --location eastus \
  --quantity 1 \
  --term P1Y \
  --billing-plan Monthly
```

### Spot VMs for Non-Critical Tests

**Save up to 90% with spot VMs (may be evicted):**

```bash
# Create spot VM
az vm create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-spot-vm \
  --image UbuntuLTS \
  --size Standard_D4s_v3 \
  --priority Spot \
  --max-price -1 \
  --eviction-policy Deallocate \
  --admin-username azureuser \
  --generate-ssh-keys

# Use for non-critical test runs or parallel execution
```

### Auto-Shutdown Schedules

```bash
# Configure auto-shutdown for VM
az vm auto-shutdown \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm \
  --time 1900 \
  --email admin@example.com

# Auto-start requires Azure Automation or Logic Apps
```

### Blob Lifecycle Management

**Automatically move old reports to cheaper storage tiers:**

See "Blob Access Tiers" section above for lifecycle policy configuration.

## High Availability and Scaling

Design for resilience and scalability in test execution infrastructure.

### Availability Zones for VMs

```bash
# Create VM in availability zone
az vm create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm-az1 \
  --image UbuntuLTS \
  --size Standard_D4s_v3 \
  --zone 1 \
  --admin-username azureuser \
  --generate-ssh-keys

# Create additional VMs in other zones
az vm create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm-az2 \
  --image UbuntuLTS \
  --size Standard_D4s_v3 \
  --zone 2 \
  --admin-username azureuser \
  --generate-ssh-keys
```

### VM Scale Sets with Auto-Scale Rules

**See "VM Scale Sets for Auto-Scaling Test Capacity" section above for complete configuration.**

### Container Group Replication

```bash
# Deploy container instances in multiple regions
REGIONS=("eastus" "westus" "northeurope")

for region in "${REGIONS[@]}"; do
  az container create \
    --resource-group testinium-qa-rg \
    --name testinium-qa-aci-${region} \
    --image testiniumqaacr.azurecr.io/testinium-qa-python:latest \
    --location ${region} \
    --cpu 2 \
    --memory 4 \
    --restart-policy Never
done
```

### App Service Auto-Scale Configuration

```bash
# Enable auto-scale for App Service plan
az monitor autoscale create \
  --resource-group testinium-qa-rg \
  --resource testinium-qa-plan \
  --resource-type Microsoft.Web/serverfarms \
  --name testinium-app-autoscale \
  --min-count 1 \
  --max-count 5 \
  --count 1

# Scale out when CPU > 70%
az monitor autoscale rule create \
  --resource-group testinium-qa-rg \
  --autoscale-name testinium-app-autoscale \
  --condition "CpuPercentage > 70 avg 10m" \
  --scale out 1

# Scale in when CPU < 30%
az monitor autoscale rule create \
  --resource-group testinium-qa-rg \
  --autoscale-name testinium-app-autoscale \
  --condition "CpuPercentage < 30 avg 10m" \
  --scale in 1
```

### Azure Load Balancer for Distributed Load

```bash
# Create load balancer for VM scale set
az network lb create \
  --resource-group testinium-qa-rg \
  --name testinium-lb \
  --sku Standard \
  --frontend-ip-name testinium-frontend \
  --backend-pool-name testinium-backend

# Create health probe
az network lb probe create \
  --resource-group testinium-qa-rg \
  --lb-name testinium-lb \
  --name health-probe \
  --protocol http \
  --port 80 \
  --path /health

# Load balancer automatically configured with VM scale set
```

## Monitoring and Alerting

Proactive monitoring and alerting for test execution health and performance.

### Azure Monitor Alerts for Test Failures

```bash
# Create action group for notifications
az monitor action-group create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-alerts \
  --short-name TQAlerts \
  --email-receiver \
    name=AdminEmail \
    email-address=admin@example.com \
  --webhook-receiver \
    name=SlackWebhook \
    service-uri=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Create alert rule for failed tests
az monitor metrics alert create \
  --resource-group testinium-qa-rg \
  --name testinium-test-failures \
  --scopes $(az monitor log-analytics workspace show \
    --resource-group testinium-qa-rg \
    --workspace-name testinium-qa-workspace \
    --query id \
    --output tsv) \
  --condition "count traces where customDimensions.status == 'failed' > 5" \
  --window-size 15m \
  --evaluation-frequency 5m \
  --action testinium-qa-alerts \
  --description "Alert when more than 5 tests fail in 15 minutes"
```

### Action Groups for Notifications

**Notification channels:**
- Email
- SMS
- Azure mobile app push notifications
- Webhooks (Slack, Microsoft Teams, PagerDuty, etc.)
- Azure Functions
- Logic Apps
- ITSM integration

### Integration with Microsoft Teams

```bash
# Create action group with Teams webhook
az monitor action-group create \
  --resource-group testinium-qa-rg \
  --name testinium-teams-alerts \
  --short-name TQTeams \
  --webhook-receiver \
    name=TeamsChannel \
    service-uri=https://outlook.office.com/webhook/YOUR/TEAMS/WEBHOOK
```

### Metrics for Custom Test KPIs

**Custom metrics via Application Insights:**

```python
# features/environment.py - Log custom metrics

from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module
import os

def before_all(context):
    """Configure custom metrics."""
    
    connection_string = os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
    if not connection_string:
        return
    
    # Create metrics exporter
    exporter = metrics_exporter.new_metrics_exporter(connection_string=connection_string)
    
    # Create measures
    context.test_duration_measure = measure_module.MeasureFloat(
        "test_duration",
        "Test scenario duration in seconds",
        "seconds"
    )
    
    context.test_count_measure = measure_module.MeasureInt(
        "test_count",
        "Number of tests executed",
        "tests"
    )
    
    # Create views
    test_duration_view = view_module.View(
        "test_duration_distribution",
        "Distribution of test durations",
        [],
        context.test_duration_measure,
        aggregation_module.DistributionAggregation([1.0, 5.0, 10.0, 30.0, 60.0, 120.0])
    )
    
    test_count_view = view_module.View(
        "test_count_total",
        "Total test count",
        [],
        context.test_count_measure,
        aggregation_module.CountAggregation()
    )
    
    # Register views
    view_manager = stats_module.stats.view_manager
    view_manager.register_view(test_duration_view)
    view_manager.register_view(test_count_view)
    view_manager.register_exporter(exporter)
    
    context.stats_recorder = stats_module.stats.stats_recorder

def after_scenario(context, scenario):
    """Record custom metrics after each scenario."""
    
    if hasattr(context, 'stats_recorder') and hasattr(context, 'test_duration_measure'):
        mmap = context.stats_recorder.new_measurement_map()
        tmap = tag_map_module.TagMap()
        
        # Record test duration
        mmap.measure_float_put(context.test_duration_measure, scenario.duration)
        mmap.measure_int_put(context.test_count_measure, 1)
        
        # Add tags
        tmap.insert("scenario", scenario.name)
        tmap.insert("status", scenario.status.name)
        
        mmap.record(tmap)
```

## Troubleshooting

Common issues and solutions when deploying on Azure.

### VM Not Accessible

**Symptoms:**
- Cannot SSH to VM
- Connection timeout
- Connection refused

**Causes and Solutions:**

1. **NSG blocking SSH:**
   ```bash
   # Check NSG rules
   az network nsg show \
     --resource-group testinium-qa-rg \
     --name testinium-vm-nsg
   
   # Add SSH rule
   az network nsg rule create \
     --resource-group testinium-qa-rg \
     --nsg-name testinium-vm-nsg \
     --name AllowSSH \
     --priority 1000 \
     --source-address-prefixes <YOUR_IP>/32 \
     --destination-port-ranges 22 \
     --access Allow \
     --protocol Tcp
   ```

2. **VM stopped or deallocated:**
   ```bash
   # Check VM status
   az vm get-instance-view \
     --resource-group testinium-qa-rg \
     --name testinium-qa-vm \
     --query instanceView.statuses[1].displayStatus
   
   # Start VM if stopped
   az vm start \
     --resource-group testinium-qa-rg \
     --name testinium-qa-vm
   ```

3. **No public IP assigned:**
   ```bash
   # Check for public IP
   az vm show \
     --resource-group testinium-qa-rg \
     --name testinium-qa-vm \
     --show-details \
     --query publicIps
   
   # Assign public IP if missing
   az network public-ip create \
     --resource-group testinium-qa-rg \
     --name testinium-qa-vm-pip
   
   az network nic ip-config update \
     --resource-group testinium-qa-rg \
     --nic-name $(az vm show --resource-group testinium-qa-rg \
       --name testinium-qa-vm \
       --query networkProfile.networkInterfaces[0].id \
       --output tsv | xargs basename) \
     --name ipconfig1 \
     --public-ip-address testinium-qa-vm-pip
   ```

### Container Instance Fails to Start

**Symptoms:**
- Container status "Failed" or "Terminated"
- Container exits immediately

**Diagnostic steps:**

```bash
# Check container status
az container show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci \
  --query instanceView.state

# View container logs
az container logs \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci

# View container events
az container show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci \
  --query instanceView.events
```

**Common solutions:**

1. **Missing environment variables:**
   - Check required variables: BASE_URL, TEST_USERNAME, TEST_PASSWORD
   - Add missing variables to container creation command

2. **Image pull failure:**
   - Verify ACR credentials
   - Check image exists: `az acr repository show-tags --name testiniumqaacr --repository testinium-qa-python`

3. **Insufficient resources:**
   - Increase CPU/memory allocation
   - Check quota limits in subscription

### Image Pull from ACR Fails

**Symptoms:**
- "Failed to pull image" error
- Authentication errors

**Solutions:**

```bash
# Verify ACR credentials
az acr credential show --name testiniumqaacr

# Test ACR login
az acr login --name testiniumqaacr

# Check image exists
az acr repository show \
  --name testiniumqaacr \
  --repository testinium-qa-python

# For managed identity issues:
# Verify identity has acrpull role
az role assignment list \
  --assignee <identity-principal-id> \
  --scope $(az acr show --name testiniumqaacr --query id --output tsv)

# Grant acrpull role if missing
az role assignment create \
  --assignee <identity-principal-id> \
  --role acrpull \
  --scope $(az acr show --name testiniumqaacr --query id --output tsv)
```

### Key Vault Access Denied

**Symptoms:**
- "Access denied" when retrieving secrets
- 403 Forbidden errors

**Solutions:**

```bash
# Check access policies
az keyvault show \
  --name testinium-qa-kv \
  --query properties.accessPolicies

# Grant access policy to managed identity
az keyvault set-policy \
  --name testinium-qa-kv \
  --object-id <identity-principal-id> \
  --secret-permissions get list

# For RBAC-enabled Key Vault
az role assignment create \
  --assignee <identity-principal-id> \
  --role "Key Vault Secrets User" \
  --scope $(az keyvault show --name testinium-qa-kv --query id --output tsv)

# Check managed identity is properly assigned
az vm identity show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm
```

### Blob Upload Permission Errors

**Symptoms:**
- "Authorization permission mismatch" errors
- Cannot write to storage account

**Solutions:**

```bash
# Check storage account access
az storage account show \
  --resource-group testinium-qa-rg \
  --name $STORAGE_ACCOUNT_NAME \
  --query networkRuleSet.defaultAction

# Grant Storage Blob Data Contributor role
az role assignment create \
  --assignee <identity-principal-id> \
  --role "Storage Blob Data Contributor" \
  --scope $(az storage account show \
    --resource-group testinium-qa-rg \
    --name $STORAGE_ACCOUNT_NAME \
    --query id \
    --output tsv)

# For connection string authentication:
# Verify connection string is correct
az storage account show-connection-string \
  --resource-group testinium-qa-rg \
  --name $STORAGE_ACCOUNT_NAME
```

### Network Connectivity Issues

**Symptoms:**
- Cannot access external URLs from VM/container
- DNS resolution failures

**Solutions:**

```bash
# Check NSG rules allow outbound traffic
az network nsg show \
  --resource-group testinium-qa-rg \
  --name testinium-vm-nsg \
  --query securityRules

# Add outbound rule for HTTPS
az network nsg rule create \
  --resource-group testinium-qa-rg \
  --nsg-name testinium-vm-nsg \
  --name AllowOutboundHTTPS \
  --priority 2000 \
  --direction Outbound \
  --access Allow \
  --protocol Tcp \
  --destination-port-ranges 443

# Test DNS resolution from VM
ssh azureuser@<VM_IP> "nslocalhost google.com"

# Test outbound connectivity
ssh azureuser@<VM_IP> "curl -I https://testinium.example.com"
```

### Managed Identity Not Working

**Symptoms:**
- DefaultAzureCredential authentication fails
- "No managed identity endpoint found" errors

**Solutions:**

```bash
# Verify managed identity is enabled
az vm identity show \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm

# Enable system-assigned identity if missing
az vm identity assign \
  --resource-group testinium-qa-rg \
  --name testinium-qa-vm

# For Container Instances, use user-assigned identity
az identity create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-identity

# Assign identity to container
az container create \
  --resource-group testinium-qa-rg \
  --name testinium-qa-aci \
  --assign-identity $(az identity show \
    --resource-group testinium-qa-rg \
    --name testinium-qa-identity \
    --query id \
    --output tsv) \
  # ... other parameters

# Inside application, verify IMDS endpoint is accessible
# curl 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/' -H Metadata:true
```

### Application Insights Not Receiving Data

**Symptoms:**
- No telemetry in Application Insights
- No logs or metrics appearing

**Solutions:**

```bash
# Verify connection string is correct
az monitor app-insights component show \
  --resource-group testinium-qa-rg \
  --app testinium-qa-insights \
  --query connectionString

# Check environment variable is set
# In VM/container:
echo $APPLICATIONINSIGHTS_CONNECTION_STRING

# Test telemetry ingestion
# Install packages
pip install opencensus-ext-azure

# Test script
python3 << EOF
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging
import os

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string=os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING')
))
logger.setLevel(logging.INFO)
logger.info("Test message from Azure VM")
EOF

# Check ingestion delay (can take 2-5 minutes)
# View in Azure Portal: Application Insights → Logs → traces table
```

## See Also

- [Azure DevOps Integration](azure-devops.md) - Detailed Azure DevOps pipeline configuration
- [Docker Deployment](docker.md) - Docker image creation and containerization
- [Kubernetes Deployment](kubernetes.md) - Kubernetes orchestration patterns
- [GitHub Actions Integration](github-actions.md) - GitHub Actions workflows
- [Configuration Reference](../reference/configuration-options.md) - Framework configuration options
- [Parallel Execution Guide](../guides/parallel-execution.md) - Parallel test execution best practices

**Source References:**
- Configuration: `config/config.yaml` (lines 93-110 for credentials)
- Test execution: `behave.ini` (lines 1-200)
- Dependencies: `requirements.txt` (lines 1-91)
- Environment variables: `.env.example` (lines 1-31)

---

**Documentation Version:** 1.0.0  
**Last Updated:** 2024-01-15  
**Azure CLI Version:** 2.55.0+  
**Python Version:** 3.11+
