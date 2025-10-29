# Google Cloud Platform (GCP) Deployment Guide

## Overview

Google Cloud Platform (GCP) provides a comprehensive suite of cloud services for deploying and running the Testinium test automation framework at scale. This guide covers deployment strategies from simple VM-based execution to sophisticated Kubernetes orchestration and serverless architectures.

### Benefits of GCP Deployment

**Modern Cloud Infrastructure:**
- State-of-the-art data centers with global reach
- Advanced networking with premium tier routing
- Integrated machine learning and data analytics capabilities
- Comprehensive security and compliance certifications

**Kubernetes-Native Platform:**
- Google Kubernetes Engine (GKE) - the original Kubernetes environment
- Autopilot mode for hands-off cluster management
- Seamless integration with Cloud Build, Cloud Storage, and other services
- Industry-leading container orchestration capabilities

**Serverless Execution:**
- Cloud Run for containerized serverless workloads
- No infrastructure management required
- Pay only for actual execution time
- Automatic scaling from zero to thousands of instances

**Data and ML Integration:**
- BigQuery for test result analysis at scale
- Cloud AI/ML services for intelligent test optimization
- Dataflow for real-time test metrics processing
- Looker for advanced test analytics dashboards

**Competitive Pricing:**
- Sustained use discounts applied automatically
- Committed use discounts up to 57% for 1-3 year commitments
- Preemptible VMs for non-critical workloads (up to 80% savings)
- Custom machine types for optimal price-performance ratio

## Prerequisites

Before deploying the test automation framework to GCP, ensure you have the following:

### GCP Account and Project

**GCP Project Setup:**
- Active Google Cloud Platform account
- Billing enabled on your GCP project
- Project ID and project number documented
- Appropriate IAM permissions (Project Editor or Owner role)

**Required GCP APIs:**
Enable the following APIs in your project:
```bash
# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Google Cloud SDK (gcloud CLI)

**Installation:**

For Linux/macOS:
```bash
# Download and install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Restart shell
exec -l $SHELL

# Initialize gcloud
gcloud init
```

For Windows:
```bash
# Download installer from: https://cloud.google.com/sdk/docs/install
# Run GoogleCloudSDKInstaller.exe
# Initialize gcloud after installation
gcloud init
```

**Authentication:**
```bash
# Authenticate with your Google account
gcloud auth login

# Set default project
gcloud config set project YOUR_PROJECT_ID

# Configure default region and zone
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# Verify configuration
gcloud config list
```

### Understanding of GCP Resources

**Core Services Required:**
- **Compute Engine:** Virtual machine instances for test execution
- **Cloud Run:** Serverless container platform for on-demand testing
- **Google Kubernetes Engine (GKE):** Managed Kubernetes for orchestrated deployments
- **Cloud Storage (GCS):** Object storage for test reports and artifacts
- **Secret Manager:** Secure credential and secret storage
- **Cloud Build:** CI/CD pipeline automation
- **Cloud Logging:** Centralized log aggregation and analysis
- **Cloud Monitoring:** Infrastructure and application monitoring
- **Artifact Registry:** Container image storage and management

**Key Identifiers:**
- Project ID: Unique identifier for your GCP project
- Project Number: Numeric identifier used in IAM configurations
- Service Account Email: For automation and API access

### Local Development Tools

**Required Software:**
- Python 3.9+ installed locally
- Docker installed for container builds
- kubectl for Kubernetes management
- Git for source control

**Framework Repository:**
```bash
# Clone the test automation framework
git clone https://github.com/your-org/testinium-qa-python.git
cd testinium-qa-python

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Source References:**
- Configuration: `config/config.yaml`
- Environment template: `.env.example`
- Dependencies: `requirements.txt`

---

## Compute Engine Deployment

Google Compute Engine provides VM-based test execution with full control over the environment. This approach is ideal for organizations requiring specific OS configurations or needing persistent test infrastructure.

### Machine Type Selection

**Recommended Machine Types:**

For standard test execution:
```bash
# E2 series - cost-effective general-purpose
# e2-standard-2: 2 vCPUs, 8 GB memory
# e2-standard-4: 4 vCPUs, 16 GB memory
MACHINE_TYPE="e2-standard-2"
```

For performance-intensive testing:
```bash
# N2 series - balanced performance
# n2-standard-4: 4 vCPUs, 16 GB memory
# Better single-thread performance than E2
MACHINE_TYPE="n2-standard-4"
```

For parallel test execution:
```bash
# N2 or C2 series with more cores
# n2-standard-8: 8 vCPUs, 32 GB memory
# Supports running multiple test threads
MACHINE_TYPE="n2-standard-8"
```

**Machine Type Considerations:**
- **E2 series:** Best price-performance for standard workloads
- **N2 series:** Higher performance per core, better for CPU-intensive tests
- **C2 series:** Compute-optimized for maximum test throughput
- **Memory requirements:** 4-8 GB minimum for Chrome/Firefox browsers

### Boot Disk Configuration

**Operating System Selection:**
```bash
# Ubuntu 22.04 LTS (recommended)
IMAGE_FAMILY="ubuntu-2204-lts"
IMAGE_PROJECT="ubuntu-os-cloud"

# Debian 11 (alternative)
# IMAGE_FAMILY="debian-11"
# IMAGE_PROJECT="debian-cloud"
```

**Disk Type and Size:**
```bash
# Balanced persistent disk (recommended)
BOOT_DISK_TYPE="pd-balanced"
BOOT_DISK_SIZE="50GB"

# SSD persistent disk (for faster I/O)
# BOOT_DISK_TYPE="pd-ssd"
# BOOT_DISK_SIZE="50GB"
```

### VM Instance Creation

**Create Test Execution VM:**
```bash
# Set project and zone
export PROJECT_ID="your-project-id"
export ZONE="us-central1-a"
export INSTANCE_NAME="testinium-test-runner"

# Create VM instance
gcloud compute instances create ${INSTANCE_NAME} \
  --project=${PROJECT_ID} \
  --zone=${ZONE} \
  --machine-type=e2-standard-2 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --boot-disk-type=pd-balanced \
  --boot-disk-device-name=${INSTANCE_NAME} \
  --tags=test-automation,http-server \
  --metadata-from-file=startup-script=startup-script.sh \
  --scopes=cloud-platform

# Wait for instance to be ready
gcloud compute instances describe ${INSTANCE_NAME} \
  --zone=${ZONE} \
  --format="get(status)"
```

### Startup Script for Automation

Create `startup-script.sh` for automated framework installation:

```bash
#!/bin/bash
# Testinium Test Automation Framework - GCE Startup Script
# This script installs all dependencies and sets up the framework

set -e

# Update system packages
apt-get update
apt-get upgrade -y

# Install Python 3.11
apt-get install -y python3.11 python3.11-venv python3-pip

# Install Google Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Install ChromeDriver dependencies
apt-get install -y unzip xvfb libxi6 libgconf-2-4

# Install Firefox (optional)
apt-get install -y firefox

# Create application user
useradd -m -s /bin/bash testrunner
mkdir -p /home/testrunner/testinium
chown -R testrunner:testrunner /home/testrunner/testinium

# Switch to application user context
su - testrunner << 'EOF'
cd /home/testrunner/testinium

# Clone framework repository
git clone https://github.com/your-org/testinium-qa-python.git .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file from Secret Manager (see Secret Manager section)
gcloud secrets versions access latest --secret="test-credentials" > .env

# Verify installation
python -c "from utilities.driver_manager import DriverManager; print('Installation successful')"
EOF

echo "Testinium framework installation completed successfully"
```

**Source:** Configuration based on `requirements.txt` and framework dependencies

### SSH Access and Test Execution

**Connect to VM Instance:**
```bash
# SSH into the instance
gcloud compute ssh ${INSTANCE_NAME} \
  --zone=${ZONE} \
  --project=${PROJECT_ID}

# Switch to testrunner user
sudo su - testrunner
cd /home/testrunner/testinium

# Activate virtual environment
source venv/bin/activate
```

**Run Tests Manually:**
```bash
# Run all tests with default @Smoke tag
behave

# Run specific feature
behave features/Login.feature

# Run with specific tags
behave --tags=@Login

# Run with JSON and HTML reports
behave -f json -o reports/cucumber.json -f pretty

# Run with Allure reporting
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results
```

**Source:** Test execution commands from `behave.ini` configuration

### Automated Test Execution with Systemd

Create a systemd service for scheduled test execution:

**Create service file:** `/etc/systemd/system/testinium-tests.service`
```ini
[Unit]
Description=Testinium Test Automation Framework
After=network.target

[Service]
Type=oneshot
User=testrunner
WorkingDirectory=/home/testrunner/testinium
Environment="PATH=/home/testrunner/testinium/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/testrunner/testinium/venv/bin/behave --tags=@Smoke -f json -o reports/cucumber.json -f pretty
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Create timer for scheduled execution:** `/etc/systemd/system/testinium-tests.timer`
```ini
[Unit]
Description=Run Testinium tests every 6 hours
Requires=testinium-tests.service

[Timer]
OnBootSec=15min
OnUnitActiveSec=6h
Unit=testinium-tests.service

[Install]
WantedBy=timers.target
```

**Enable and start the timer:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable and start timer
sudo systemctl enable testinium-tests.timer
sudo systemctl start testinium-tests.timer

# Check timer status
sudo systemctl list-timers testinium-tests.timer

# View test execution logs
sudo journalctl -u testinium-tests.service -f
```

### Instance Groups for Scaling

**Create managed instance group for parallel execution:**

```bash
# Create instance template
gcloud compute instance-templates create testinium-test-template \
  --machine-type=e2-standard-2 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --boot-disk-type=pd-balanced \
  --tags=test-automation \
  --metadata-from-file=startup-script=startup-script.sh \
  --scopes=cloud-platform

# Create managed instance group
gcloud compute instance-groups managed create testinium-test-group \
  --base-instance-name=testinium-test \
  --template=testinium-test-template \
  --size=3 \
  --zone=${ZONE}

# Configure autoscaling
gcloud compute instance-groups managed set-autoscaling testinium-test-group \
  --zone=${ZONE} \
  --min-num-replicas=1 \
  --max-num-replicas=10 \
  --target-cpu-utilization=0.75 \
  --cool-down-period=300
```

---

## Cloud Run Deployment

Cloud Run provides a serverless platform for running containerized test workloads without managing infrastructure. Ideal for on-demand test execution and CI/CD integration.

### Docker Image Preparation

**Create Dockerfile for test framework:**

```dockerfile
# Dockerfile for Testinium Test Automation Framework
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy framework files
COPY requirements.txt .
COPY config/ ./config/
COPY features/ ./features/
COPY pages/ ./pages/
COPY utilities/ ./utilities/
COPY behave.ini .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create reports directory
RUN mkdir -p reports/screenshots reports/allure-results

# Set environment variables for headless execution
ENV HEADLESS=true
ENV BROWSER_TYPE=chrome

# Run tests as non-root user
RUN useradd -m testrunner && chown -R testrunner:testrunner /app
USER testrunner

# Entry point for Cloud Run
CMD ["behave", "--tags=@Smoke", "-f", "json", "-o", "reports/cucumber.json", "-f", "pretty"]
```

**Build and test locally:**
```bash
# Build Docker image
docker build -t testinium-tests:latest .

# Test locally
docker run --rm \
  -e BASE_URL=https://testinium.example.com \
  -e TEST_USERNAME=test@example.com \
  -e TEST_PASSWORD=password123 \
  testinium-tests:latest
```

### Container Registry Setup

**Using Artifact Registry (recommended):**

```bash
# Create Artifact Registry repository
gcloud artifacts repositories create testinium-images \
  --repository-format=docker \
  --location=us-central1 \
  --description="Testinium test automation framework images"

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Tag and push image
docker tag testinium-tests:latest \
  us-central1-docker.pkg.dev/${PROJECT_ID}/testinium-images/testinium-tests:latest

docker push us-central1-docker.pkg.dev/${PROJECT_ID}/testinium-images/testinium-tests:latest
```

**Using Container Registry (legacy):**
```bash
# Configure Docker authentication
gcloud auth configure-docker

# Tag and push image
docker tag testinium-tests:latest gcr.io/${PROJECT_ID}/testinium-tests:latest
docker push gcr.io/${PROJECT_ID}/testinium-tests:latest
```

### Cloud Run Service Deployment

**Deploy Cloud Run service:**

```bash
# Set variables
export SERVICE_NAME="testinium-test-runner"
export REGION="us-central1"
export IMAGE="us-central1-docker.pkg.dev/${PROJECT_ID}/testinium-images/testinium-tests:latest"

# Deploy service
gcloud run deploy ${SERVICE_NAME} \
  --image=${IMAGE} \
  --region=${REGION} \
  --platform=managed \
  --memory=4Gi \
  --cpu=2 \
  --timeout=900 \
  --max-instances=10 \
  --concurrency=1 \
  --no-allow-unauthenticated \
  --set-env-vars="BROWSER_TYPE=chrome,HEADLESS=true" \
  --set-secrets="TEST_USERNAME=test-username:latest,TEST_PASSWORD=test-password:latest"

# Get service URL
gcloud run services describe ${SERVICE_NAME} \
  --region=${REGION} \
  --format="value(status.url)"
```

**Service Configuration Options:**

| Parameter | Value | Reason |
|-----------|-------|--------|
| `--memory` | 4Gi | Sufficient for Chrome browser and test execution |
| `--cpu` | 2 | Adequate processing power for Selenium tests |
| `--timeout` | 900 | 15 minutes maximum for test suite execution |
| `--max-instances` | 10 | Limit concurrent test runs for cost control |
| `--concurrency` | 1 | One test suite per container instance |

**Source:** Memory and CPU requirements based on `requirements.txt` dependencies including Selenium and Chrome

### Invoking Tests via HTTP Trigger

**Create simple HTTP endpoint:**

Modify your framework to include a Flask app:

```python
# app.py - HTTP endpoint for Cloud Run
from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/run-tests', methods=['POST'])
def run_tests():
    """Execute test suite and return results."""
    try:
        # Run behave tests
        result = subprocess.run(
            ['behave', '--tags=@Smoke', '-f', 'json', '-o', 'reports/cucumber.json'],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        # Read results
        with open('reports/cucumber.json', 'r') as f:
            results = f.read()
        
        return jsonify({
            'status': 'completed',
            'exit_code': result.returncode,
            'results': results
        }), 200
    except subprocess.TimeoutExpired:
        return jsonify({'status': 'timeout', 'message': 'Tests exceeded time limit'}), 408
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
```

Update Dockerfile CMD:
```dockerfile
CMD ["python", "app.py"]
```

**Trigger tests with curl:**
```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
  --region=${REGION} \
  --format="value(status.url)")

# Invoke tests (requires authentication)
curl -X POST ${SERVICE_URL}/run-tests \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```

### Cloud Scheduler for Scheduled Execution

**Schedule periodic test execution:**

```bash
# Create service account for scheduler
gcloud iam service-accounts create cloud-scheduler-sa \
  --display-name="Cloud Scheduler Service Account"

# Grant permission to invoke Cloud Run
gcloud run services add-iam-policy-binding ${SERVICE_NAME} \
  --region=${REGION} \
  --member="serviceAccount:cloud-scheduler-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/run.invoker"

# Create scheduled job (every 6 hours)
gcloud scheduler jobs create http testinium-scheduled-tests \
  --location=${REGION} \
  --schedule="0 */6 * * *" \
  --uri="${SERVICE_URL}/run-tests" \
  --http-method=POST \
  --oidc-service-account-email="cloud-scheduler-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --oidc-token-audience="${SERVICE_URL}"

# Test the scheduled job
gcloud scheduler jobs run testinium-scheduled-tests --location=${REGION}
```

### Viewing Cloud Run Logs

**Stream service logs:**
```bash
# Stream logs in real-time
gcloud run services logs tail ${SERVICE_NAME} \
  --region=${REGION}

# Read recent logs
gcloud run services logs read ${SERVICE_NAME} \
  --region=${REGION} \
  --limit=50

# Filter logs by severity
gcloud run services logs read ${SERVICE_NAME} \
  --region=${REGION} \
  --log-filter="severity>=ERROR"
```

**Source:** Logging configuration from `behave.ini` lines 55-57

### Cold Start Considerations

**Minimizing Cold Start Impact:**

1. **Keep minimum instances:**
```bash
gcloud run services update ${SERVICE_NAME} \
  --region=${REGION} \
  --min-instances=1
```

2. **Optimize Docker image:**
- Use slim base images
- Minimize layers
- Use .dockerignore to exclude unnecessary files

3. **Implement health checks:**
```python
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200
```

---

## Google Kubernetes Engine (GKE) Deployment

GKE provides robust Kubernetes orchestration for large-scale test execution with advanced scheduling, autoscaling, and monitoring capabilities.

### GKE Cluster Creation

**Create standard GKE cluster:**

```bash
# Set cluster variables
export CLUSTER_NAME="testinium-test-cluster"
export CLUSTER_ZONE="us-central1-a"
export NODE_MACHINE_TYPE="e2-standard-4"

# Create cluster
gcloud container clusters create ${CLUSTER_NAME} \
  --zone=${CLUSTER_ZONE} \
  --machine-type=${NODE_MACHINE_TYPE} \
  --num-nodes=3 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=10 \
  --enable-autorepair \
  --enable-autoupgrade \
  --enable-ip-alias \
  --enable-stackdriver-kubernetes \
  --addons=HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver \
  --workload-pool=${PROJECT_ID}.svc.id.goog

# Get cluster credentials
gcloud container clusters get-credentials ${CLUSTER_NAME} \
  --zone=${CLUSTER_ZONE}

# Verify connection
kubectl cluster-info
kubectl get nodes
```

**Create Autopilot cluster (simplified management):**

```bash
# Autopilot mode - Google manages nodes automatically
gcloud container clusters create-auto ${CLUSTER_NAME} \
  --region=us-central1 \
  --project=${PROJECT_ID}

# Get credentials
gcloud container clusters get-credentials ${CLUSTER_NAME} \
  --region=us-central1
```

### kubectl Configuration

**Authenticate kubectl:**
```bash
# Already configured via get-credentials command above

# Verify authentication
kubectl config current-context

# Create namespace for test automation
kubectl create namespace testinium

# Set default namespace
kubectl config set-context --current --namespace=testinium
```

### Kubernetes Manifests

**ConfigMap for test configuration:**

Create `k8s/configmap.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: testinium-config
  namespace: testinium
data:
  BROWSER_TYPE: "chrome"
  HEADLESS: "true"
  BASE_URL: "https://testinium.example.com"
  TIMEOUT_EXPLICIT: "10"
  TIMEOUT_PAGE_LOAD: "30"
  SCREENSHOTS_ON_FAILURE: "true"
```

**Source:** Configuration from `config/config.yaml` lines 23-38 and `.env.example`

**Secret for credentials:**

Create `k8s/secret.yaml`:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: testinium-secrets
  namespace: testinium
type: Opaque
stringData:
  TEST_USERNAME: "test@example.com"
  TEST_PASSWORD: "your_secure_password"
  SALES_MANAGER_USERNAME: "sales@example.com"
  SALES_MANAGER_PASSWORD: "your_secure_password"
  POS_MANAGER_USERNAME: "pos@example.com"
  POS_MANAGER_PASSWORD: "your_secure_password"
```

**Better approach using Secret Manager (see Secret Manager section below)**

**Deployment for test execution:**

Create `k8s/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: testinium-test-runner
  namespace: testinium
spec:
  replicas: 2
  selector:
    matchLabels:
      app: testinium-tests
  template:
    metadata:
      labels:
        app: testinium-tests
    spec:
      serviceAccountName: testinium-sa
      containers:
      - name: test-runner
        image: us-central1-docker.pkg.dev/PROJECT_ID/testinium-images/testinium-tests:latest
        imagePullPolicy: Always
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        envFrom:
        - configMapRef:
            name: testinium-config
        - secretRef:
            name: testinium-secrets
        volumeMounts:
        - name: reports
          mountPath: /app/reports
      volumes:
      - name: reports
        emptyDir: {}
```

**CronJob for scheduled test execution:**

Create `k8s/cronjob.yaml`:
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: testinium-scheduled-tests
  namespace: testinium
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      template:
        metadata:
          labels:
            app: testinium-tests
            type: scheduled
        spec:
          serviceAccountName: testinium-sa
          restartPolicy: OnFailure
          containers:
          - name: test-runner
            image: us-central1-docker.pkg.dev/PROJECT_ID/testinium-images/testinium-tests:latest
            imagePullPolicy: Always
            command: ["behave"]
            args: ["--tags=@Smoke", "-f", "json", "-o", "reports/cucumber.json", "-f", "pretty"]
            resources:
              requests:
                memory: "2Gi"
                cpu: "1000m"
              limits:
                memory: "4Gi"
                cpu: "2000m"
            envFrom:
            - configMapRef:
                name: testinium-config
            - secretRef:
                name: testinium-secrets
            volumeMounts:
            - name: reports
              mountPath: /app/reports
          volumes:
          - name: reports
            emptyDir: {}
```

**Apply manifests:**
```bash
# Create namespace
kubectl create namespace testinium

# Apply ConfigMap
kubectl apply -f k8s/configmap.yaml

# Apply Secrets (or use Secret Manager - see below)
kubectl apply -f k8s/secret.yaml

# Apply Deployment
kubectl apply -f k8s/deployment.yaml

# Apply CronJob
kubectl apply -f k8s/cronjob.yaml

# Verify resources
kubectl get all -n testinium
```

**Source:** Kubernetes configuration based on `docker.md` and `kubernetes.md` deployment patterns

### Workload Identity for Secure Service Access

**Enable Workload Identity (recommended for production):**

```bash
# Create Kubernetes service account
kubectl create serviceaccount testinium-sa -n testinium

# Create GCP service account
gcloud iam service-accounts create testinium-gke-sa \
  --display-name="Testinium GKE Service Account"

# Grant permissions to GCP service account
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:testinium-gke-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:testinium-gke-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

# Bind Kubernetes SA to GCP SA
gcloud iam service-accounts add-iam-policy-binding \
  testinium-gke-sa@${PROJECT_ID}.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:${PROJECT_ID}.svc.id.goog[testinium/testinium-sa]"

# Annotate Kubernetes service account
kubectl annotate serviceaccount testinium-sa \
  -n testinium \
  iam.gke.io/gcp-service-account=testinium-gke-sa@${PROJECT_ID}.iam.gserviceaccount.com
```

### Cluster Autoscaling

**Configure cluster autoscaling:**
```bash
# Enable autoscaling on node pool
gcloud container clusters update ${CLUSTER_NAME} \
  --zone=${CLUSTER_ZONE} \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=20 \
  --node-pool=default-pool

# Configure autoscaling profile (optimize for utilization)
gcloud container clusters update ${CLUSTER_NAME} \
  --zone=${CLUSTER_ZONE} \
  --autoscaling-profile=optimize-utilization
```

**Horizontal Pod Autoscaling:**

Create `k8s/hpa.yaml`:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: testinium-hpa
  namespace: testinium
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: testinium-test-runner
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

Apply HPA:
```bash
kubectl apply -f k8s/hpa.yaml
kubectl get hpa -n testinium
```

---

## Cloud Storage for Test Reports

Google Cloud Storage provides scalable object storage for test reports, screenshots, and artifacts.

### Bucket Creation

**Create storage bucket:**
```bash
# Set bucket name (must be globally unique)
export BUCKET_NAME="${PROJECT_ID}-testinium-reports"
export BUCKET_LOCATION="us-central1"

# Create bucket
gcloud storage buckets create gs://${BUCKET_NAME} \
  --location=${BUCKET_LOCATION} \
  --uniform-bucket-level-access

# Set lifecycle policy for automatic cleanup
cat > lifecycle.json << EOF
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {
          "age": 90,
          "matchesPrefix": ["reports/"]
        }
      },
      {
        "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
        "condition": {
          "age": 30,
          "matchesPrefix": ["reports/"]
        }
      }
    ]
  }
}
EOF

gsutil lifecycle set lifecycle.json gs://${BUCKET_NAME}
```

### Uploading Reports

**Upload reports using gsutil:**
```bash
# Upload test reports after execution
gsutil -m cp -r reports/* gs://${BUCKET_NAME}/reports/$(date +%Y%m%d-%H%M%S)/

# Upload with metadata
gsutil -h "Content-Type:application/json" \
  cp reports/cucumber.json \
  gs://${BUCKET_NAME}/reports/$(date +%Y%m%d-%H%M%S)/cucumber.json
```

**Upload from Python code:**

Update `features/environment.py` to upload reports after test execution:

```python
# features/environment.py - Add to after_all hook
from google.cloud import storage

def after_all(context):
    """Upload test reports to Cloud Storage after all tests complete."""
    # Existing driver cleanup code...
    
    # Upload reports to GCS
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket('your-project-testinium-reports')
        
        import os
        from datetime import datetime
        
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        
        # Upload all files in reports directory
        for root, dirs, files in os.walk('reports'):
            for file in files:
                local_path = os.path.join(root, file)
                blob_path = f'reports/{timestamp}/{local_path}'
                blob = bucket.blob(blob_path)
                blob.upload_from_filename(local_path)
                print(f"Uploaded {local_path} to gs://{bucket.name}/{blob_path}")
    except Exception as e:
        print(f"Failed to upload reports to GCS: {e}")
```

**Install google-cloud-storage:**
```bash
pip install google-cloud-storage
```

Add to `requirements.txt`:
```
google-cloud-storage==2.10.0
```

### Public Access Configuration

**Make reports publicly accessible (optional):**
```bash
# Make bucket publicly readable
gsutil iam ch allUsers:objectViewer gs://${BUCKET_NAME}

# Access reports via URL
# https://storage.googleapis.com/${BUCKET_NAME}/reports/20240115-143000/cucumber.json
```

**Warning:** Only use public access for non-sensitive test reports.

### Signed URLs for Private Access

**Generate signed URLs for temporary access:**

```python
from google.cloud import storage
from datetime import timedelta

def generate_signed_url(bucket_name, blob_name, expiration_minutes=60):
    """Generate a signed URL for temporary access to a private object."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET"
    )
    
    return url

# Usage
url = generate_signed_url(
    'your-project-testinium-reports',
    'reports/20240115-143000/cucumber.json',
    expiration_minutes=120
)
print(f"Temporary URL: {url}")
```

---

## Secret Manager for Credentials

Google Secret Manager provides secure storage and access control for sensitive test credentials and configuration data.

### Enabling Secret Manager API

**Enable the API:**
```bash
gcloud services enable secretmanager.googleapis.com
```

### Creating Secrets

**Create secrets for test credentials:**
```bash
# Create secret for test username
echo -n "test@example.com" | \
  gcloud secrets create test-username \
  --data-file=- \
  --replication-policy="automatic"

# Create secret for test password
echo -n "your_secure_password" | \
  gcloud secrets create test-password \
  --data-file=- \
  --replication-policy="automatic"

# Create secrets for other credentials
echo -n "sales@example.com" | \
  gcloud secrets create sales-manager-username \
  --data-file=-

echo -n "sales_password" | \
  gcloud secrets create sales-manager-password \
  --data-file=-

echo -n "pos@example.com" | \
  gcloud secrets create pos-manager-username \
  --data-file=-

echo -n "pos_password" | \
  gcloud secrets create pos-manager-password \
  --data-file=-
```

**Source:** Credentials structure from `config/config.yaml` lines 93-110

### Secret Versions for Rotation

**Add new secret version:**
```bash
# Update secret with new value
echo -n "new_password_value" | \
  gcloud secrets versions add test-password \
  --data-file=-

# List all versions
gcloud secrets versions list test-password

# Access specific version
gcloud secrets versions access 2 --secret="test-password"

# Disable old version
gcloud secrets versions disable 1 --secret="test-password"

# Destroy old version (after grace period)
gcloud secrets versions destroy 1 --secret="test-password"
```

### Accessing Secrets in Application

**Install Secret Manager Python library:**
```bash
pip install google-cloud-secret-manager
```

Add to `requirements.txt`:
```
google-cloud-secret-manager==2.16.0
```

**Access secrets in Python code:**

```python
# utilities/secret_manager.py
from google.cloud import secretmanager
import os

class SecretManagerClient:
    """Client for accessing secrets from Google Secret Manager."""
    
    def __init__(self, project_id=None):
        self.project_id = project_id or os.environ.get('GCP_PROJECT_ID')
        self.client = secretmanager.SecretManagerServiceClient()
    
    def access_secret(self, secret_id, version_id="latest"):
        """
        Access a secret from Secret Manager.
        
        Args:
            secret_id (str): The ID of the secret
            version_id (str): The version (default: "latest")
        
        Returns:
            str: The secret value
        """
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

# Usage in test configuration
def load_credentials_from_secret_manager():
    """Load test credentials from Secret Manager."""
    sm = SecretManagerClient()
    
    credentials = {
        'TEST_USERNAME': sm.access_secret('test-username'),
        'TEST_PASSWORD': sm.access_secret('test-password'),
        'SALES_MANAGER_USERNAME': sm.access_secret('sales-manager-username'),
        'SALES_MANAGER_PASSWORD': sm.access_secret('sales-manager-password'),
        'POS_MANAGER_USERNAME': sm.access_secret('pos-manager-username'),
        'POS_MANAGER_PASSWORD': sm.access_secret('pos-manager-password'),
    }
    
    # Set as environment variables
    for key, value in credentials.items():
        os.environ[key] = value
    
    return credentials
```

**Update environment.py to load secrets:**

```python
# features/environment.py - Add to before_all
from utilities.secret_manager import load_credentials_from_secret_manager

def before_all(context):
    """Setup executed before all tests."""
    # Load credentials from Secret Manager in GCP environments
    if os.environ.get('GOOGLE_CLOUD_PROJECT'):
        try:
            load_credentials_from_secret_manager()
            print("Loaded credentials from Secret Manager")
        except Exception as e:
            print(f"Failed to load secrets: {e}")
            # Fall back to .env file for local development
    
    # Rest of existing before_all code...
```

### Workload Identity for GKE Secret Access

**Configure GKE pods to access Secret Manager:**

```bash
# Grant Secret Manager access to GKE service account
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:testinium-gke-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

Pods using Workload Identity (configured earlier) can now access secrets directly.

### Service Account Key for Compute Engine/Cloud Run

**Create service account key (if not using Workload Identity):**

```bash
# Create service account
gcloud iam service-accounts create testinium-sa \
  --display-name="Testinium Test Automation Service Account"

# Grant Secret Manager access
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:testinium-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Create and download key (store securely!)
gcloud iam service-accounts keys create testinium-sa-key.json \
  --iam-account=testinium-sa@${PROJECT_ID}.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="path/to/testinium-sa-key.json"
```

**Warning:** Service account keys should be avoided in production. Use Workload Identity for GKE or attached service accounts for Compute Engine/Cloud Run.

---

## Service Accounts and IAM

Proper IAM configuration ensures secure access to GCP resources with least-privilege permissions.

### Service Account Creation

**Create dedicated service account for test execution:**

```bash
# Create service account
gcloud iam service-accounts create testinium-test-runner \
  --display-name="Testinium Test Automation Runner" \
  --description="Service account for automated test execution"

# Verify creation
gcloud iam service-accounts list --filter="email:testinium-test-runner@*"
```

### Granting Least-Privilege Roles

**Grant only necessary permissions:**

```bash
export SA_EMAIL="testinium-test-runner@${PROJECT_ID}.iam.gserviceaccount.com"

# Storage permissions for report uploads
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/storage.objectAdmin" \
  --condition="expression=resource.name.startsWith('projects/_/buckets/${BUCKET_NAME}'),title=testinium-reports-only"

# Secret Manager access
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"

# Logging permissions
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/logging.logWriter"

# Monitoring metrics (optional)
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/monitoring.metricWriter"
```

### Attaching Service Account to Resources

**Compute Engine VM:**
```bash
gcloud compute instances create testinium-runner \
  --service-account=${SA_EMAIL} \
  --scopes=cloud-platform \
  # ... other parameters
```

**Cloud Run service:**
```bash
gcloud run deploy testinium-test-runner \
  --service-account=${SA_EMAIL} \
  # ... other parameters
```

**GKE Workload Identity (already configured above):**
Uses Kubernetes service account bound to GCP service account.

### Avoiding User Account Usage

**Best Practices:**
- Never use personal user accounts for automation
- Always use service accounts for CI/CD and automated testing
- Implement service account key rotation policies
- Use Workload Identity when possible (no keys needed)
- Audit service account usage regularly

---

## Cloud Logging Integration

Google Cloud Logging provides centralized log management and analysis for test execution monitoring.

### Viewing Logs in Cloud Console

**Access logs via Console:**
1. Navigate to: **Cloud Console → Logging → Logs Explorer**
2. Filter by resource type:
   - Compute Engine: `resource.type="gce_instance"`
   - Cloud Run: `resource.type="cloud_run_revision"`
   - GKE: `resource.type="k8s_container"`

**Filter by test execution:**
```
resource.labels.namespace_name="testinium"
labels.app="testinium-tests"
severity>=INFO
```

### Advanced Log Queries

**Query test results:**
```
resource.type="cloud_run_revision"
resource.labels.service_name="testinium-test-runner"
jsonPayload.message=~"Scenario:"
```

**Query failures only:**
```
resource.type="k8s_container"
resource.labels.namespace_name="testinium"
severity>=ERROR
```

**Query with time range:**
```
resource.type="gce_instance"
resource.labels.instance_id="testinium-test-runner"
timestamp>="2024-01-15T00:00:00Z"
timestamp<"2024-01-16T00:00:00Z"
```

### Log-Based Metrics

**Create custom metric for test failures:**

```bash
# Create log-based metric
gcloud logging metrics create test_failures \
  --description="Count of failed test scenarios" \
  --log-filter='
    resource.type="cloud_run_revision"
    resource.labels.service_name="testinium-test-runner"
    jsonPayload.status="failed"
  ' \
  --value-extractor='EXTRACT(jsonPayload.scenario_name)' \
  --metric-kind=DELTA \
  --value-type=INT64
```

### Exporting Logs to BigQuery

**Create log sink for long-term analysis:**

```bash
# Create BigQuery dataset
bq mk --dataset ${PROJECT_ID}:testinium_logs

# Create log sink
gcloud logging sinks create testinium-logs-sink \
  bigquery.googleapis.com/projects/${PROJECT_ID}/datasets/testinium_logs \
  --log-filter='
    resource.labels.namespace_name="testinium"
    OR resource.labels.service_name="testinium-test-runner"
  '

# Grant BigQuery access to log sink service account
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:$(gcloud logging sinks describe testinium-logs-sink --format='value(writerIdentity)')" \
  --role="roles/bigquery.dataEditor"
```

### Structured Logging with JSON

**Implement structured logging in tests:**

```python
# utilities/logger.py
import json
import logging

class StructuredLogger:
    """Logger that outputs JSON-formatted logs for Cloud Logging."""
    
    def __init__(self, name):
        self.logger = logging.getLogger(name)
    
    def log_scenario_start(self, scenario_name, tags):
        """Log scenario start event."""
        log_entry = {
            'event': 'scenario_start',
            'scenario_name': scenario_name,
            'tags': tags,
            'severity': 'INFO'
        }
        self.logger.info(json.dumps(log_entry))
    
    def log_scenario_result(self, scenario_name, status, duration):
        """Log scenario result."""
        log_entry = {
            'event': 'scenario_result',
            'scenario_name': scenario_name,
            'status': status,
            'duration_seconds': duration,
            'severity': 'INFO' if status == 'passed' else 'ERROR'
        }
        self.logger.info(json.dumps(log_entry))
```

**Source:** Logging configuration from `behave.ini` lines 55-57

---

## Cloud Monitoring

Google Cloud Monitoring enables proactive monitoring of test infrastructure and test execution metrics.

### Custom Metrics for Test Execution

**Create custom metrics:**

```python
# utilities/metrics.py
from google.cloud import monitoring_v3
import time

class TestMetrics:
    """Custom metrics reporter for Cloud Monitoring."""
    
    def __init__(self, project_id):
        self.project_id = project_id
        self.client = monitoring_v3.MetricServiceClient()
        self.project_name = f"projects/{project_id}"
    
    def report_test_result(self, test_suite, passed, failed, skipped):
        """Report test execution results as custom metrics."""
        series = monitoring_v3.TimeSeries()
        series.metric.type = 'custom.googleapis.com/testinium/test_results'
        series.resource.type = 'global'
        
        # Add labels
        series.metric.labels['test_suite'] = test_suite
        series.metric.labels['result'] = 'passed'
        
        # Add data point
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)
        interval = monitoring_v3.TimeInterval(
            {"end_time": {"seconds": seconds, "nanos": nanos}}
        )
        point = monitoring_v3.Point({
            "interval": interval,
            "value": {"int64_value": passed}
        })
        series.points = [point]
        
        # Write time series
        self.client.create_time_series(
            name=self.project_name,
            time_series=[series]
        )
```

### Uptime Checks

**Monitor test infrastructure availability:**

```bash
# Create uptime check for Cloud Run service
gcloud monitoring uptime create testinium-service-uptime \
  --display-name="Testinium Service Health Check" \
  --resource-type=uptime-url \
  --monitored-resource-labels="project_id=${PROJECT_ID},host=${SERVICE_URL}" \
  --http-check-path="/health" \
  --check-interval=300s \
  --timeout=10s
```

### Alerting Policies

**Create alert for test failures:**

```bash
# Create notification channel (email)
gcloud alpha monitoring channels create \
  --display-name="Test Alerts Email" \
  --type=email \
  --channel-labels=email_address=team@example.com

# Create alerting policy
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Test Failure Rate" \
  --condition-display-name="Test failure rate > 20%" \
  --condition-threshold-value=0.2 \
  --condition-threshold-duration=300s \
  --condition-filter='
    metric.type="custom.googleapis.com/testinium/test_results"
    metric.label.result="failed"
  '
```

### Dashboards for Test Visualization

**Create custom dashboard:**

Via Cloud Console:
1. Navigate to **Monitoring → Dashboards → Create Dashboard**
2. Add charts for:
   - Test pass/fail rate over time
   - Test execution duration
   - Infrastructure resource utilization
   - Error rates by test suite

---

## Cloud Build for CI/CD

Google Cloud Build provides managed CI/CD pipelines for automated test execution triggered by code commits.

### cloudbuild.yaml Configuration

Create `cloudbuild.yaml` in repository root:

```yaml
# Cloud Build configuration for Testinium test automation
steps:
  # Step 1: Build Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'us-central1-docker.pkg.dev/${PROJECT_ID}/testinium-images/testinium-tests:${SHORT_SHA}'
      - '-t'
      - 'us-central1-docker.pkg.dev/${PROJECT_ID}/testinium-images/testinium-tests:latest'
      - '.'
  
  # Step 2: Push image to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - '--all-tags'
      - 'us-central1-docker.pkg.dev/${PROJECT_ID}/testinium-images/testinium-tests'
  
  # Step 3: Run tests
  - name: 'us-central1-docker.pkg.dev/${PROJECT_ID}/testinium-images/testinium-tests:${SHORT_SHA}'
    args: ['behave', '--tags=@Smoke', '-f', 'json', '-o', 'reports/cucumber.json']
    env:
      - 'BROWSER_TYPE=chrome'
      - 'HEADLESS=true'
      - 'BASE_URL=https://testinium.example.com'
    secretEnv: ['TEST_USERNAME', 'TEST_PASSWORD']
  
  # Step 4: Deploy to Cloud Run (if tests pass)
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'testinium-test-runner'
      - '--image=us-central1-docker.pkg.dev/${PROJECT_ID}/testinium-images/testinium-tests:${SHORT_SHA}'
      - '--region=us-central1'
      - '--platform=managed'

# Access secrets from Secret Manager
availableSecrets:
  secretManager:
    - versionName: projects/${PROJECT_ID}/secrets/test-username/versions/latest
      env: 'TEST_USERNAME'
    - versionName: projects/${PROJECT_ID}/secrets/test-password/versions/latest
      env: 'TEST_PASSWORD'

# Store build artifacts
artifacts:
  objects:
    location: 'gs://${PROJECT_ID}-testinium-reports/builds/${BUILD_ID}/'
    paths:
      - 'reports/**'

# Build options
options:
  machineType: 'E2_HIGHCPU_8'
  logging: CLOUD_LOGGING_ONLY
  
timeout: 1800s  # 30 minutes
```

### Triggers from Source Repositories

**Connect Cloud Build to GitHub:**

```bash
# Install Cloud Build GitHub app (one-time setup)
# Visit: https://github.com/apps/google-cloud-build

# Create trigger
gcloud builds triggers create github \
  --repo-name=testinium-qa-python \
  --repo-owner=your-org \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --description="Run tests on main branch commits"
```

**Create trigger for pull requests:**

```bash
gcloud builds triggers create github \
  --repo-name=testinium-qa-python \
  --repo-owner=your-org \
  --pull-request-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --comment-control=COMMENTS_ENABLED \
  --description="Run tests on PRs targeting main"
```

**Trigger from Cloud Source Repositories:**

```bash
# Create Cloud Source Repository
gcloud source repos create testinium-qa-python

# Add remote
git remote add google https://source.developers.google.com/p/${PROJECT_ID}/r/testinium-qa-python

# Push code
git push google main

# Create trigger
gcloud builds triggers create cloud-source-repositories \
  --repo=testinium-qa-python \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

### Build History and Logs

**View build history:**
```bash
# List recent builds
gcloud builds list --limit=10

# Get build details
gcloud builds describe BUILD_ID

# Stream build logs
gcloud builds log BUILD_ID --stream
```

### Integration with Cloud Deploy

**Progressive delivery with Cloud Deploy:**

Create `clouddeploy.yaml`:
```yaml
apiVersion: deploy.cloud.google.com/v1
kind: DeliveryPipeline
metadata:
  name: testinium-pipeline
description: Progressive test deployment pipeline
serialPipeline:
  stages:
  - targetId: staging
    profiles: []
  - targetId: production
    profiles: []
---
apiVersion: deploy.cloud.google.com/v1
kind: Target
metadata:
  name: staging
description: Staging test environment
run:
  location: projects/${PROJECT_ID}/locations/us-central1
---
apiVersion: deploy.cloud.google.com/v1
kind: Target
metadata:
  name: production
description: Production test environment
run:
  location: projects/${PROJECT_ID}/locations/us-central1
```

---

## Networking Configuration

### VPC Network Setup

**Create dedicated VPC network:**

```bash
# Create VPC network
gcloud compute networks create testinium-vpc \
  --subnet-mode=custom \
  --bgp-routing-mode=regional

# Create subnet
gcloud compute networks subnets create testinium-subnet \
  --network=testinium-vpc \
  --region=us-central1 \
  --range=10.0.0.0/24 \
  --enable-private-ip-google-access
```

### Firewall Rules

**Configure firewall rules:**

```bash
# Allow internal communication
gcloud compute firewall-rules create testinium-allow-internal \
  --network=testinium-vpc \
  --allow=tcp,udp,icmp \
  --source-ranges=10.0.0.0/24

# Allow SSH from IAP (Identity-Aware Proxy)
gcloud compute firewall-rules create testinium-allow-iap-ssh \
  --network=testinium-vpc \
  --allow=tcp:22 \
  --source-ranges=35.235.240.0/20

# Allow health checks
gcloud compute firewall-rules create testinium-allow-health-checks \
  --network=testinium-vpc \
  --allow=tcp:80,tcp:443 \
  --source-ranges=35.191.0.0/16,130.211.0.0/22
```

### Cloud NAT for Private VM Internet Access

**Enable Cloud NAT:**

```bash
# Create Cloud Router
gcloud compute routers create testinium-router \
  --network=testinium-vpc \
  --region=us-central1

# Create NAT gateway
gcloud compute routers nats create testinium-nat \
  --router=testinium-router \
  --region=us-central1 \
  --nat-all-subnet-ip-ranges \
  --auto-allocate-nat-external-ips
```

### Private Google Access

**Enable Private Google Access for GCS/Secret Manager without public IPs:**

```bash
# Already enabled in subnet creation with --enable-private-ip-google-access

# Verify
gcloud compute networks subnets describe testinium-subnet \
  --region=us-central1 \
  --format="get(privateIpGoogleAccess)"
```

### VPC Service Controls

**Create security perimeter (for sensitive environments):**

```bash
# Create access policy (organization-level)
gcloud access-context-manager policies create \
  --organization=ORGANIZATION_ID \
  --title="Testinium Security Policy"

# Create service perimeter
gcloud access-context-manager perimeters create testinium_perimeter \
  --title="Testinium Test Automation Perimeter" \
  --resources=projects/${PROJECT_NUMBER} \
  --restricted-services=storage.googleapis.com,secretmanager.googleapis.com \
  --policy=POLICY_ID
```

---

## Cost Optimization

### Committed Use Discounts

**Purchase committed use contracts:**

```bash
# 1-year commitment (up to 37% discount)
gcloud compute commitments create testinium-1year \
  --region=us-central1 \
  --plan=12-month \
  --resources=vcpu=8,memory=32GB

# 3-year commitment (up to 57% discount)
gcloud compute commitments create testinium-3year \
  --region=us-central1 \
  --plan=36-month \
  --resources=vcpu=16,memory=64GB
```

### Sustained Use Discounts

**Automatic discounts:**
- Applied automatically by GCP
- Up to 30% discount for instances running >25% of the month
- No action required
- Review in billing reports

### Preemptible VMs for Non-Critical Tests

**Create preemptible instance:**

```bash
gcloud compute instances create testinium-preemptible \
  --zone=us-central1-a \
  --machine-type=e2-standard-4 \
  --preemptible \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB
```

**Savings:** Up to 80% compared to regular instances

**Considerations:**
- Can be terminated at any time
- Maximum runtime: 24 hours
- Suitable for retry-safe test suites
- Implement checkpoint/resume logic for long test runs

### Cloud Storage Lifecycle Policies

**Optimize storage costs:**

```bash
# Lifecycle policy (already shown above)
# - Move to Nearline after 30 days (50% savings)
# - Delete after 90 days
# - Apply to reports older than retention requirement
```

### Budget Alerts

**Set up budget alerts:**

```bash
# Create budget
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Testinium Monthly Budget" \
  --budget-amount=1000USD \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=75 \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100
```

### Cost Monitoring

**Review costs regularly:**
1. Navigate to **Cloud Console → Billing → Reports**
2. Filter by:
   - Service: Compute Engine, Cloud Run, GKE, Cloud Storage
   - Labels: `app=testinium`
3. Export to BigQuery for detailed analysis
4. Set up custom dashboards in Looker Studio

---

## Regional Considerations

### Selecting Appropriate Region

**Factors to consider:**

| Factor | Recommendation | Example |
|--------|---------------|---------|
| **Latency to AUT** | Choose region closest to application | EU app → europe-west1 |
| **Data residency** | Comply with regulations (GDPR, CCPA) | EU data → EU region |
| **Cost** | Some regions are more expensive | Us-central1 often cheapest |
| **Service availability** | Not all services in all regions | Check service availability |

**Popular regions:**
- `us-central1` (Iowa) - Most cost-effective, good availability
- `us-east1` (South Carolina) - Low latency to East Coast
- `europe-west1` (Belgium) - EU data residency
- `asia-east1` (Taiwan) - Asia-Pacific coverage

### Multi-Regional Cloud Storage

**High availability for critical reports:**

```bash
# Create multi-regional bucket
gcloud storage buckets create gs://${BUCKET_NAME} \
  --location=us \
  --uniform-bucket-level-access

# Multi-regional locations: us, eu, asia
```

**Cost:** ~$0.026/GB/month (vs ~$0.020 for regional)

### Cross-Region Replication

**Replicate test infrastructure across regions:**

```bash
# Create instance template in multiple regions
gcloud compute instance-templates create testinium-us-central \
  --region=us-central1 \
  # ... other parameters

gcloud compute instance-templates create testinium-europe-west \
  --region=europe-west1 \
  # ... other parameters

# Create regional managed instance groups
gcloud compute instance-groups managed create testinium-group-us \
  --region=us-central1 \
  --template=testinium-us-central \
  --size=2

gcloud compute instance-groups managed create testinium-group-eu \
  --region=europe-west1 \
  --template=testinium-europe-west \
  --size=2
```

### Data Residency Compliance

**Ensure data stays in specific regions:**

1. **Organization policy constraints:**
```bash
# Restrict resource locations (requires organization permissions)
gcloud resource-manager org-policies set-policy policy.yaml

# policy.yaml:
# constraint: constraints/gcp.resourceLocations
# listPolicy:
#   allowedValues:
#     - in:eu-locations
```

2. **Bucket location locks:**
- Once created, bucket location cannot be changed
- Choose carefully for compliance requirements

---

## Troubleshooting

### gcloud Authentication Issues

**Problem:** `ERROR: (gcloud.auth.login) There was a problem with web authentication`

**Solution:**
```bash
# Try alternative authentication
gcloud auth login --no-launch-browser

# Or use service account
gcloud auth activate-service-account --key-file=sa-key.json
```

**Problem:** `You do not currently have an active account selected`

**Solution:**
```bash
# List accounts
gcloud auth list

# Set active account
gcloud config set account your-email@example.com
```

### VM SSH Connection Failures

**Problem:** Cannot SSH into VM instance

**Solutions:**

1. **Check firewall rules:**
```bash
gcloud compute firewall-rules list --filter="name~ssh"
```

2. **Use IAP tunnel:**
```bash
gcloud compute ssh INSTANCE_NAME \
  --zone=ZONE \
  --tunnel-through-iap
```

3. **Check VM status:**
```bash
gcloud compute instances describe INSTANCE_NAME --zone=ZONE
```

4. **View serial console output:**
```bash
gcloud compute instances get-serial-port-output INSTANCE_NAME --zone=ZONE
```

### Cloud Run Deployment Errors

**Problem:** `ERROR: (gcloud.run.deploy) Image XXXX does not exist`

**Solution:**
```bash
# Verify image exists
gcloud artifacts docker images list us-central1-docker.pkg.dev/${PROJECT_ID}/testinium-images

# Check authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Rebuild and push image
docker build -t IMAGE_URL .
docker push IMAGE_URL
```

**Problem:** `Container failed to start. Failed to start and then listen on the port defined by the PORT environment variable`

**Solution:**
- Ensure application listens on `0.0.0.0:$PORT`
- Cloud Run sets PORT environment variable (default 8080)
- Update Dockerfile CMD to start HTTP server

### Image Pull from Registry Fails

**Problem:** `Failed to pull image: unauthorized`

**Solution:**

For GKE:
```bash
# Verify Workload Identity configuration
kubectl describe serviceaccount testinium-sa -n testinium

# Grant Artifact Registry Reader role
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:testinium-gke-sa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"
```

For Compute Engine:
```bash
# Ensure service account has artifact registry reader role
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:VM_SERVICE_ACCOUNT" \
  --role="roles/artifactregistry.reader"
```

### Secret Manager Permission Denied

**Problem:** `ERROR: (gcloud.secrets.versions.access) Permission denied`

**Solution:**
```bash
# Grant Secret Manager Secret Accessor role
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
  --role="roles/secretmanager.secretAccessor"

# Verify permissions
gcloud secrets get-iam-policy SECRET_NAME
```

### Cloud Storage Upload Errors

**Problem:** `AccessDeniedException: 403 Insufficient Permission`

**Solution:**
```bash
# Grant Storage Object Admin role
gsutil iam ch serviceAccount:SA_EMAIL:objectAdmin gs://BUCKET_NAME

# Or grant Storage Object Creator (write-only)
gsutil iam ch serviceAccount:SA_EMAIL:objectCreator gs://BUCKET_NAME

# Verify permissions
gsutil iam get gs://BUCKET_NAME
```

### GKE Pod Scheduling Issues

**Problem:** Pods stuck in `Pending` state

**Diagnosis:**
```bash
# Describe pod to see events
kubectl describe pod POD_NAME -n testinium

# Check node resources
kubectl top nodes

# Check resource requests vs limits
kubectl describe nodes
```

**Solutions:**

1. **Insufficient resources:**
```bash
# Scale up cluster
gcloud container clusters resize CLUSTER_NAME \
  --num-nodes=5 \
  --zone=ZONE
```

2. **Resource requests too high:**
- Reduce resource requests in deployment.yaml
- Use Vertical Pod Autoscaler for recommendations

3. **Node affinity issues:**
- Check node labels and pod affinity rules
- Ensure nodeSelector matches available nodes

### Service Account Key Management Problems

**Problem:** Service account key expired or invalid

**Solution:**
```bash
# List keys
gcloud iam service-accounts keys list \
  --iam-account=SA_EMAIL

# Delete old key
gcloud iam service-accounts keys delete KEY_ID \
  --iam-account=SA_EMAIL

# Create new key
gcloud iam service-accounts keys create new-key.json \
  --iam-account=SA_EMAIL

# Update GOOGLE_APPLICATION_CREDENTIALS
export GOOGLE_APPLICATION_CREDENTIALS="path/to/new-key.json"
```

**Best Practice:** Use Workload Identity instead of service account keys to avoid key management issues.

### Test Framework Issues in GCP

**Problem:** Tests fail with "WebDriver not found" in Cloud Run/GKE

**Solution:**
- Ensure ChromeDriver is installed in Docker image
- Verify PATH includes ChromeDriver location
- Check Dockerfile includes all Selenium dependencies

**Problem:** Tests timeout in Cloud Run

**Solution:**
- Increase `--timeout` parameter (max 3600s)
- Optimize test suite for faster execution
- Use parallel execution with multiple Cloud Run instances

**Problem:** Headless browser crashes

**Solution:**
```dockerfile
# Add to Dockerfile
RUN apt-get install -y \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libgbm1
```

---

## See Also

- **[Local Development Setup](local-development.md)** - Set up framework locally before GCP deployment
- **[Docker Deployment](docker.md)** - Container fundamentals referenced in Cloud Run and GKE sections
- **[Kubernetes Deployment](kubernetes.md)** - Detailed Kubernetes manifests for GKE
- **[CI/CD Integration](jenkins-integration.md)** - Jenkins pipeline for hybrid GCP deployments
- **[Configuration Reference](../reference/configuration-options.md)** - Complete framework configuration options
- **[Troubleshooting Guide](../troubleshooting/index.md)** - General troubleshooting beyond GCP-specific issues

**External Resources:**
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Secret Manager Best Practices](https://cloud.google.com/secret-manager/docs/best-practices)
- [GCP Cost Optimization](https://cloud.google.com/cost-management)

---

**Document Version:** 1.0  
**Last Updated:** 2024-01-15  
**Maintained by:** DevOps & Test Automation Team

**Source References:**
- Test configuration: `config/config.yaml`
- Environment variables: `.env.example`
- Test execution: `behave.ini`
- Framework dependencies: `requirements.txt`

