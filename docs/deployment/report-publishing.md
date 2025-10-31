# Advanced Report Publishing and Distribution

## Overview

Effective test report publishing is critical for modern test automation frameworks, providing visibility into test execution results and enabling data-driven quality decisions. This guide covers comprehensive strategies for publishing, hosting, and distributing test results from the Testinium QA Python framework.

### Why Report Publishing Matters

**Stakeholder Visibility:**
- Executive dashboards showing quality metrics and trends
- Development teams accessing detailed failure diagnostics
- Product managers tracking feature readiness
- QA teams monitoring test coverage and flakiness

**Historical Tracking:**
- Trend analysis across builds and releases
- Identification of degrading test suites
- Performance baseline comparisons
- Flaky test detection through statistical analysis

**Debugging Failed Tests:**
- Screenshots captured at failure points
- Browser console logs for client-side errors
- Step-by-step execution traces
- Environment configuration snapshots

**Compliance and Audit Trails:**
- Regulatory requirements for test evidence
- Quality gate documentation for releases
- Traceability from requirements to test results
- Retention policies for audit compliance

**Team Collaboration:**
- Shared access to test results across distributed teams
- Commenting and annotation on test failures
- Integration with communication tools (Slack, Teams)
- Assignment of failures to team members

## Report Format Overview

The Testinium QA framework supports multiple report formats, each serving specific use cases. Understanding when to use each format enables effective reporting strategies.

### HTML Reports

**Format:** Human-readable HTML with CSS styling  
**Generator:** behave-html-formatter  
**Configuration:** `behave.ini` line 59 (commented formatter option)

**Characteristics:**
- Self-contained HTML files with embedded CSS and JavaScript
- Expandable/collapsible scenario sections
- Color-coded pass/fail status
- Execution time metrics per scenario and step
- Screenshot thumbnails with lightbox viewing

**Use Cases:**
- Manual review by QA engineers and developers
- Sharing via email or static file hosting
- Quick debugging without specialized tools
- Archival of test results in human-readable format

**Generation Command:**
```bash
# Generate standalone HTML report
behave -f behave_html_formatter:HTMLFormatter -o reports/report.html -f pretty

# Or using multiple outputs
behave -f html -o reports/cucumber-reports.html -f json -o reports/cucumber.json
```

**Source:** `README.md:469-477`, `behave.ini:59`

### JSON Reports

**Format:** Structured JSON following Cucumber JSON schema  
**Generator:** Behave native JSON formatter  
**Configuration:** `behave.ini` line 20 (format=pretty, with JSON via command line)

**Characteristics:**
- Machine-parseable structured data
- Complete test execution metadata
- Cucumber JSON schema compatibility
- Suitable for programmatic analysis and data transformation

**Use Cases:**
- CI/CD pipeline processing and metrics extraction
- Custom dashboard data source
- Integration with external test management systems
- Historical data aggregation and analysis
- Feed for custom report generators

**Generation Command:**
```bash
# Generate JSON report for CI/CD tools
behave -f json -o reports/cucumber.json

# Combined with pretty console output
behave -f json -o reports/cucumber.json -f pretty
```

**Source:** `README.md:479-484`, `behave.ini:20-32`

### JUnit XML Reports

**Format:** JUnit XML schema for CI/CD integration  
**Generator:** Behave native JUnit formatter  
**Configuration:** `behave.ini` lines 36-37 (junit=true, junit_directory)

**Characteristics:**
- Industry-standard format for test results
- Direct integration with Jenkins, Azure DevOps, CircleCI, GitLab CI
- Test suite hierarchy with classname and testcase elements
- Execution time, error messages, and failure details
- Trend analysis support in CI/CD platforms

**Use Cases:**
- Jenkins test result publishing and trend charts
- Azure DevOps test run integration
- GitLab CI test reports tab
- CI/CD quality gates and build status determination
- Test result aggregation across pipelines

**Generation Command:**
```bash
# Generate JUnit XML report (already enabled in behave.ini)
behave  # JUnit XML automatically generated to reports/junit/

# Or explicitly via command line
behave --junit --junit-directory reports/junit
```

**Source:** `README.md:486-491`, `behave.ini:34-37`

### Allure Reports

**Format:** Enhanced HTML with interactive visualizations  
**Generator:** allure-behave formatter  
**Configuration:** `behave.ini` lines 77-82 (userdata.allure_results_dir)

**Characteristics:**
- Rich interactive HTML5 report with modern UI
- Historical trend graphs and timeline views
- Test case grouping by features, severity, and tags
- Screenshot and attachment integration
- Test retry and flaky test detection
- Execution environment metadata capture

**Use Cases:**
- Comprehensive test result analysis with stakeholders
- Historical trend analysis across builds
- Flaky test identification through retry tracking
- Detailed failure investigation with attachments
- Test suite health monitoring

**Generation Commands:**
```bash
# Generate Allure results
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# View Allure report locally (auto-opens browser)
allure serve reports/allure-results

# Generate static Allure report for hosting
allure generate reports/allure-results --output reports/allure-report --clean
```

**Source:** `README.md:493-504`, `behave.ini:77-82`, `config/config.yaml:127-134`

## GitHub Pages Hosting

GitHub Pages provides free static website hosting directly from GitHub repositories, making it an ideal solution for publishing test reports without additional infrastructure costs.

### Enabling GitHub Pages

**Repository Configuration:**

1. Navigate to repository **Settings** → **Pages**
2. Select **Source:** Deploy from a branch
3. Choose **Branch:** `gh-pages` (or `main` with `/docs` folder)
4. Click **Save**
5. GitHub provides the site URL: `https://<username>.github.io/<repository>/`

**Branch Configuration Options:**
- **gh-pages branch:** Dedicated branch for published reports (recommended)
- **main branch /docs folder:** Use existing branch with docs subfolder
- **main branch root:** Entire repository as website (not recommended for test projects)

### Automated Deployment with GitHub Actions

Create `.github/workflows/publish-reports.yml` for automatic report publishing after test execution:

```yaml
name: Publish Test Reports to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:  # Manual trigger option

# Required for GitHub Pages deployment
permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  test-and-publish:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3
      
      - name: Setup Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install Dependencies
        run: |
          pip install -r requirements.txt
          # Install Allure command-line tool
          wget https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz
          tar -zxvf allure-2.24.1.tgz
          sudo mv allure-2.24.1 /opt/allure
          echo "/opt/allure/bin" >> $GITHUB_PATH
      
      - name: Run Tests
        env:
          TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
          TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
          BASE_URL: ${{ secrets.BASE_URL }}
        run: |
          # Run tests with multiple report formats
          behave -f json -o reports/cucumber.json \
                 -f allure_behave.formatter:AllureFormatter -o reports/allure-results \
                 -f behave_html_formatter:HTMLFormatter -o reports/report.html \
                 -f pretty
        continue-on-error: true  # Publish reports even if tests fail
      
      - name: Generate Allure Report
        if: always()
        run: |
          allure generate reports/allure-results --output reports/allure-report --clean
      
      - name: Prepare GitHub Pages Structure
        if: always()
        run: |
          mkdir -p gh-pages
          # Copy reports to gh-pages directory
          cp -r reports/allure-report/* gh-pages/
          cp reports/report.html gh-pages/behave-report.html
          cp reports/cucumber.json gh-pages/cucumber.json
          cp -r reports/screenshots gh-pages/screenshots/ || true
          
          # Create index page with navigation
          cat > gh-pages/index.html << 'EOF'
          <!DOCTYPE html>
          <html lang="en">
          <head>
              <meta charset="UTF-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <title>Test Reports - Testinium QA</title>
              <style>
                  body { font-family: Arial, sans-serif; margin: 40px; }
                  h1 { color: #333; }
                  .report-links { margin: 20px 0; }
                  .report-links a { 
                      display: inline-block; 
                      margin: 10px 20px 10px 0; 
                      padding: 10px 20px; 
                      background: #4CAF50; 
                      color: white; 
                      text-decoration: none; 
                      border-radius: 4px;
                  }
                  .report-links a:hover { background: #45a049; }
                  .timestamp { color: #666; font-size: 0.9em; }
              </style>
          </head>
          <body>
              <h1>Testinium QA Test Reports</h1>
              <p class="timestamp">Last Updated: $(date -u +'%Y-%m-%d %H:%M:%S UTC')</p>
              <div class="report-links">
                  <a href="index.html">Allure Report (Interactive)</a>
                  <a href="behave-report.html">Behave HTML Report</a>
                  <a href="cucumber.json" download>Download JSON Report</a>
                  <a href="screenshots/">View Screenshots</a>
              </div>
          </body>
          </html>
          EOF
      
      - name: Deploy to GitHub Pages
        if: always()
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./gh-pages
          publish_branch: gh-pages
          force_orphan: true  # Clean history for space efficiency
```

**Source:** Referenced from `github-actions.md` deployment guide

### Accessing Published Reports

After successful deployment:

1. **Navigate to:** `https://<username>.github.io/<repository>/`
2. **Allure Report:** `https://<username>.github.io/<repository>/index.html`
3. **Behave HTML:** `https://<username>.github.io/<repository>/behave-report.html`
4. **Screenshots:** `https://<username>.github.io/<repository>/screenshots/`

### Custom Domain Configuration

**To use a custom domain (e.g., `reports.example.com`):**

1. Add `CNAME` file to gh-pages branch:
   ```
   reports.example.com
   ```

2. Configure DNS with your domain provider:
   ```
   Type: CNAME
   Name: reports (or subdomain of choice)
   Value: <username>.github.io
   ```

3. Enable **Enforce HTTPS** in repository settings (GitHub auto-provisions SSL)

### Report Structure for Navigation

Organize reports by build number or timestamp for historical access:

```
gh-pages/
├── index.html                    # Landing page with links
├── latest/                       # Latest test run (symlink or copy)
│   ├── allure-report/
│   ├── behave-report.html
│   └── screenshots/
├── builds/
│   ├── build-123/                # Historical builds
│   │   ├── allure-report/
│   │   └── behave-report.html
│   ├── build-124/
│   └── build-125/
└── CNAME                         # Custom domain (if configured)
```

**Workflow Enhancement for Build History:**

```yaml
- name: Prepare GitHub Pages with Build History
  if: always()
  run: |
    BUILD_NUMBER="${{ github.run_number }}"
    mkdir -p gh-pages/builds/build-${BUILD_NUMBER}
    
    # Copy current build reports
    cp -r reports/allure-report gh-pages/builds/build-${BUILD_NUMBER}/
    cp reports/report.html gh-pages/builds/build-${BUILD_NUMBER}/behave-report.html
    
    # Update latest symlink (for Unix-based Pages hosting)
    rm -rf gh-pages/latest
    cp -r gh-pages/builds/build-${BUILD_NUMBER} gh-pages/latest
    
    # Generate index with build history links
    # (Add script to list all builds with timestamps)
```

### Troubleshooting GitHub Pages

**Issue: 404 Page Not Found**
- **Cause:** gh-pages branch not selected or not yet deployed
- **Solution:** Verify Settings → Pages shows "Your site is published at..."
- **Check:** Ensure files exist in gh-pages branch root

**Issue: Reports Not Updating**
- **Cause:** GitHub Pages cache or deployment delay
- **Solution:** Wait 1-2 minutes for deployment, force refresh browser (Ctrl+Shift+R)
- **Check:** Verify GitHub Actions workflow completed successfully

**Issue: Allure Report Shows Blank Page**
- **Cause:** Missing index.html in allure-report directory or incorrect base path
- **Solution:** Verify `allure generate` created index.html in output directory
- **Check:** Ensure all Allure assets (CSS, JS) are present in published directory

## AWS S3 Static Website Hosting

Amazon S3 provides highly scalable, cost-effective static website hosting with global availability through CloudFront CDN integration. Ideal for enterprise deployments requiring reliability and performance.

### S3 Bucket Configuration

**Create and Configure S3 Bucket:**

```bash
# Create S3 bucket for report hosting
aws s3 mb s3://testinium-qa-reports --region us-east-1

# Enable static website hosting
aws s3 website s3://testinium-qa-reports \
  --index-document index.html \
  --error-document error.html
```

**Configure Bucket Policy for Public Read Access:**

Create `bucket-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::testinium-qa-reports/*"
    }
  ]
}
```

Apply policy:

```bash
aws s3api put-bucket-policy \
  --bucket testinium-qa-reports \
  --policy file://bucket-policy.json
```

### Uploading Reports with AWS CLI

**Manual Upload:**

```bash
# Upload entire reports directory
aws s3 sync reports/ s3://testinium-qa-reports/latest/ \
  --delete \
  --cache-control "max-age=3600" \
  --exclude "*.pyc" \
  --exclude "__pycache__/*"

# Upload with build number versioning
BUILD_NUMBER=$(date +%Y%m%d-%H%M%S)
aws s3 sync reports/ s3://testinium-qa-reports/builds/${BUILD_NUMBER}/ \
  --cache-control "max-age=86400"
```

**Automated Upload Script (upload_reports.py):**

```python
"""
AWS S3 report upload automation script.
Uploads test reports to S3 bucket with versioning and metadata.

Usage:
    python upload_reports.py --bucket testinium-qa-reports --build-number 123
"""

import os
import boto3
import argparse
from datetime import datetime
from pathlib import Path

def upload_reports_to_s3(bucket_name: str, build_number: str, reports_dir: str = "reports"):
    """
    Upload test reports to S3 with versioning and proper content types.
    
    Args:
        bucket_name: S3 bucket name for report hosting
        build_number: Build identifier for versioning
        reports_dir: Local reports directory path
        
    Returns:
        str: S3 URL of uploaded reports
    """
    s3_client = boto3.client('s3')
    reports_path = Path(reports_dir)
    
    if not reports_path.exists():
        raise FileNotFoundError(f"Reports directory not found: {reports_dir}")
    
    # Upload all files with appropriate content types
    content_types = {
        '.html': 'text/html',
        '.json': 'application/json',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.xml': 'application/xml'
    }
    
    uploaded_files = 0
    timestamp = datetime.utcnow().isoformat()
    
    for file_path in reports_path.rglob('*'):
        if file_path.is_file():
            # Calculate S3 key with build number prefix
            relative_path = file_path.relative_to(reports_path)
            s3_key = f"builds/{build_number}/{relative_path}"
            
            # Determine content type
            content_type = content_types.get(file_path.suffix, 'application/octet-stream')
            
            # Upload with metadata
            s3_client.upload_file(
                str(file_path),
                bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': 'max-age=3600',
                    'Metadata': {
                        'build-number': build_number,
                        'upload-timestamp': timestamp
                    }
                }
            )
            uploaded_files += 1
            print(f"Uploaded: {s3_key}")
    
    # Copy to 'latest' for easy access
    copy_source = {'Bucket': bucket_name, 'Key': f"builds/{build_number}/"}
    # Note: S3 doesn't support directory copy, would need to iterate files
    
    bucket_website_url = f"http://{bucket_name}.s3-website-us-east-1.amazonaws.com"
    print(f"\nUploaded {uploaded_files} files")
    print(f"Reports URL: {bucket_website_url}/builds/{build_number}/index.html")
    
    return f"{bucket_website_url}/builds/{build_number}/"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload test reports to S3")
    parser.add_argument('--bucket', required=True, help='S3 bucket name')
    parser.add_argument('--build-number', required=True, help='Build identifier')
    parser.add_argument('--reports-dir', default='reports', help='Reports directory')
    
    args = parser.parse_args()
    
    try:
        url = upload_reports_to_s3(args.bucket, args.build_number, args.reports_dir)
        print(f"\n✓ Reports published successfully: {url}")
    except Exception as e:
        print(f"\n✗ Upload failed: {e}")
        exit(1)
```

**Integration with Behave Hooks (`features/environment.py`):**

```python
def after_all(context):
    """
    Upload reports to S3 after all tests complete.
    Triggered automatically after test suite execution.
    """
    if os.getenv('UPLOAD_TO_S3', 'false').lower() == 'true':
        import subprocess
        
        bucket_name = os.getenv('S3_REPORTS_BUCKET', 'testinium-qa-reports')
        build_number = os.getenv('BUILD_NUMBER', datetime.now().strftime('%Y%m%d-%H%M%S'))
        
        try:
            subprocess.run([
                'python', 'upload_reports.py',
                '--bucket', bucket_name,
                '--build-number', build_number
            ], check=True)
            print(f"Reports uploaded to S3: s3://{bucket_name}/builds/{build_number}/")
        except subprocess.CalledProcessError as e:
            print(f"Failed to upload reports to S3: {e}")
```

### CloudFront Distribution for HTTPS and CDN

**Create CloudFront Distribution:**

```bash
# Create CloudFront distribution pointing to S3 bucket
aws cloudfront create-distribution \
  --origin-domain-name testinium-qa-reports.s3.amazonaws.com \
  --default-root-object index.html
```

**CloudFront Configuration JSON:**

```json
{
  "CallerReference": "testinium-qa-reports-2024",
  "Aliases": {
    "Quantity": 1,
    "Items": ["reports.example.com"]
  },
  "DefaultRootObject": "index.html",
  "Origins": {
    "Quantity": 1,
    "Items": [
      {
        "Id": "S3-testinium-qa-reports",
        "DomainName": "testinium-qa-reports.s3.amazonaws.com",
        "S3OriginConfig": {
          "OriginAccessIdentity": ""
        }
      }
    ]
  },
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-testinium-qa-reports",
    "ViewerProtocolPolicy": "redirect-to-https",
    "AllowedMethods": {
      "Quantity": 2,
      "Items": ["GET", "HEAD"]
    },
    "MinTTL": 0,
    "DefaultTTL": 3600,
    "MaxTTL": 86400
  },
  "PriceClass": "PriceClass_100",
  "Enabled": true
}
```

**Benefits of CloudFront:**
- HTTPS support with AWS Certificate Manager (ACM) certificates
- Global CDN with edge locations for low-latency access
- Custom domain support (CNAME records)
- DDoS protection via AWS Shield
- Access logs for report viewing analytics

### Custom Domain with Route53

**Configure DNS:**

```bash
# Create Route53 hosted zone (if not exists)
aws route53 create-hosted-zone --name example.com --caller-reference $(date +%s)

# Create CNAME record pointing to CloudFront distribution
aws route53 change-resource-record-sets \
  --hosted-zone-id Z1234567890ABC \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "reports.example.com",
        "Type": "CNAME",
        "TTL": 300,
        "ResourceRecords": [{"Value": "d1234567890.cloudfront.net"}]
      }
    }]
  }'
```

### Versioned Reports and Lifecycle Management

**Organize Reports by Build Number:**

```
s3://testinium-qa-reports/
├── builds/
│   ├── 20240115-120000/
│   │   ├── allure-report/
│   │   ├── report.html
│   │   └── screenshots/
│   ├── 20240115-150000/
│   └── 20240115-180000/
├── latest/                    # Symbolic link or latest copy
│   └── (latest build files)
└── index.html                 # Landing page with build history
```

**S3 Lifecycle Rules for Cleanup:**

Create `lifecycle-policy.json`:

```json
{
  "Rules": [
    {
      "Id": "DeleteOldReports",
      "Status": "Enabled",
      "Prefix": "builds/",
      "Expiration": {
        "Days": 90
      }
    },
    {
      "Id": "TransitionToGlacier",
      "Status": "Enabled",
      "Prefix": "builds/",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "GLACIER"
        }
      ]
    }
  ]
}
```

Apply lifecycle policy:

```bash
aws s3api put-bucket-lifecycle-configuration \
  --bucket testinium-qa-reports \
  --lifecycle-configuration file://lifecycle-policy.json
```

**Lifecycle Strategy:**
- **0-30 days:** Standard storage (frequently accessed)
- **30-90 days:** Glacier storage (archival, slower access)
- **90+ days:** Automatic deletion
- **Keep latest 10 builds:** Use separate prefix with no expiration

### Cost Optimization

**S3 Storage Tiers:**

| Tier | Use Case | Cost (per GB/month) | Retrieval Time |
|------|----------|---------------------|----------------|
| S3 Standard | Latest reports (0-30 days) | $0.023 | Instant |
| S3 Intelligent-Tiering | Automatic tier management | $0.023-0.0125 | Instant |
| S3 Glacier | Archive (30-90 days) | $0.004 | Minutes to hours |
| S3 Glacier Deep Archive | Long-term compliance | $0.00099 | 12 hours |

**Cost Reduction Strategies:**
1. **Compress reports before upload** (gzip HTML/JSON)
2. **Delete screenshots after 30 days** (keep only failure screenshots)
3. **Use S3 Intelligent-Tiering** for automatic cost optimization
4. **Clean up redundant Allure assets** (shared CSS/JS across builds)
5. **Implement build retention policy** (keep last 100 builds, delete older)

**Monthly Cost Estimate (1000 builds/month):**
- Storage: 50 GB × $0.023 = $1.15
- Data transfer out (10 GB): $0.90
- CloudFront requests: $0.10
- **Total: ~$2-3/month** for comprehensive report hosting

## Azure Blob Storage Static Websites

Azure Blob Storage provides static website hosting with built-in CDN integration, Azure AD authentication support, and seamless integration with Azure DevOps pipelines.

### Enable Static Website Feature

**Using Azure CLI:**

```bash
# Create storage account
az storage account create \
  --name testiniumqareports \
  --resource-group TestAutomationRG \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2

# Enable static website hosting
az storage blob service-properties update \
  --account-name testiniumqareports \
  --static-website \
  --index-document index.html \
  --404-document 404.html

# Get primary endpoint URL
az storage account show \
  --name testiniumqareports \
  --resource-group TestAutomationRG \
  --query "primaryEndpoints.web" \
  --output tsv
```

**Output:** `https://testiniumqareports.z13.web.core.windows.net/`

### Upload Reports with Azure CLI

**Manual Upload:**

```bash
# Upload reports to $web container (static website root)
az storage blob upload-batch \
  --account-name testiniumqareports \
  --source reports/ \
  --destination '$web/builds/build-123' \
  --content-cache-control "max-age=3600" \
  --pattern "*" \
  --content-type "text/html"
```

**Python Script Using azure-storage-blob:**

```python
"""
Azure Blob Storage report upload script.
Uploads test reports with proper content types and metadata.
"""

from azure.storage.blob import BlobServiceClient, ContentSettings
from pathlib import Path
import os
from datetime import datetime

def upload_to_azure_blob(
    connection_string: str,
    build_number: str,
    reports_dir: str = "reports"
) -> str:
    """
    Upload test reports to Azure Blob Storage static website.
    
    Args:
        connection_string: Azure Storage connection string
        build_number: Build identifier for versioning
        reports_dir: Local reports directory
        
    Returns:
        str: Public URL of uploaded reports
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = "$web"  # Static website container
    
    reports_path = Path(reports_dir)
    content_type_mapping = {
        '.html': 'text/html',
        '.json': 'application/json',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.png': 'image/png',
        '.jpg': 'image/jpeg'
    }
    
    uploaded_count = 0
    
    for file_path in reports_path.rglob('*'):
        if file_path.is_file():
            # Create blob path
            relative_path = file_path.relative_to(reports_path)
            blob_path = f"builds/{build_number}/{relative_path}"
            
            # Get blob client
            blob_client = blob_service_client.get_blob_client(
                container=container_name,
                blob=blob_path
            )
            
            # Determine content type
            content_type = content_type_mapping.get(
                file_path.suffix,
                'application/octet-stream'
            )
            
            # Upload with content settings
            with open(file_path, 'rb') as data:
                blob_client.upload_blob(
                    data,
                    overwrite=True,
                    content_settings=ContentSettings(
                        content_type=content_type,
                        cache_control='max-age=3600'
                    ),
                    metadata={
                        'build_number': build_number,
                        'upload_time': datetime.utcnow().isoformat()
                    }
                )
            
            uploaded_count += 1
            print(f"Uploaded: {blob_path}")
    
    # Get account name from connection string
    account_name = connection_string.split(';')[1].split('=')[1]
    report_url = f"https://{account_name}.z13.web.core.windows.net/builds/{build_number}/"
    
    print(f"\n✓ Uploaded {uploaded_count} files")
    print(f"Reports URL: {report_url}")
    
    return report_url

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Upload reports to Azure Blob")
    parser.add_argument('--connection-string', required=True, help='Azure connection string')
    parser.add_argument('--build-number', required=True, help='Build identifier')
    parser.add_argument('--reports-dir', default='reports', help='Reports directory')
    
    args = parser.parse_args()
    upload_to_azure_blob(args.connection_string, args.build_number, args.reports_dir)
```

### Azure CDN Integration

**Create CDN Profile and Endpoint:**

```bash
# Create CDN profile
az cdn profile create \
  --name TestiniumQAReportsCDN \
  --resource-group TestAutomationRG \
  --sku Standard_Microsoft

# Create CDN endpoint
az cdn endpoint create \
  --name testinium-reports \
  --profile-name TestiniumQAReportsCDN \
  --resource-group TestAutomationRG \
  --origin testiniumqareports.z13.web.core.windows.net \
  --origin-host-header testiniumqareports.z13.web.core.windows.net
```

**Access via CDN:** `https://testinium-reports.azureedge.net/`

### Custom Domain Mapping

```bash
# Map custom domain to CDN endpoint
az cdn custom-domain create \
  --endpoint-name testinium-reports \
  --hostname reports.example.com \
  --profile-name TestiniumQAReportsCDN \
  --resource-group TestAutomationRG \
  --name reports-example-com

# Enable HTTPS
az cdn custom-domain enable-https \
  --endpoint-name testinium-reports \
  --name reports-example-com \
  --profile-name TestiniumQAReportsCDN \
  --resource-group TestAutomationRG
```

### Access Control with SAS Tokens

For private reports requiring authentication:

```bash
# Generate SAS token with read permissions (valid for 24 hours)
az storage blob generate-sas \
  --account-name testiniumqareports \
  --container-name '$web' \
  --name 'builds/build-123/index.html' \
  --permissions r \
  --expiry $(date -u -d "24 hours" '+%Y-%m-%dT%H:%MZ') \
  --https-only \
  --output tsv
```

**Python script to generate time-limited report links:**

```python
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

def generate_report_url_with_sas(
    account_name: str,
    account_key: str,
    blob_path: str,
    expiry_hours: int = 24
) -> str:
    """Generate time-limited SAS URL for report access."""
    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name='$web',
        blob_name=blob_path,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=expiry_hours)
    )
    
    return f"https://{account_name}.blob.core.windows.net/$web/{blob_path}?{sas_token}"
```

## Google Cloud Storage Website Hosting

Google Cloud Storage provides static website hosting with global CDN, custom domain support via Cloud Load Balancing, and integration with Google Cloud Build.

### GCS Bucket Configuration

**Create and Configure Bucket:**

```bash
# Create bucket with website configuration
gsutil mb -c STANDARD -l us-east1 gs://testinium-qa-reports

# Configure as website
gsutil web set -m index.html -e 404.html gs://testinium-qa-reports

# Make bucket publicly readable
gsutil iam ch allUsers:objectViewer gs://testinium-qa-reports
```

**Alternative: Using gcloud storage commands:**

```bash
# Create bucket
gcloud storage buckets create gs://testinium-qa-reports \
  --location=us-east1 \
  --uniform-bucket-level-access

# Set website configuration
gcloud storage buckets update gs://testinium-qa-reports \
  --web-main-page-suffix=index.html \
  --web-error-page=404.html
```

### IAM Policy for Public Access

**Create public access policy (`bucket-policy.json`):**

```json
{
  "bindings": [
    {
      "role": "roles/storage.objectViewer",
      "members": [
        "allUsers"
      ]
    }
  ]
}
```

**Apply policy:**

```bash
gsutil iam set bucket-policy.json gs://testinium-qa-reports
```

### Upload Reports with gsutil

**Manual Upload:**

```bash
# Upload entire reports directory
gsutil -m rsync -r -d reports/ gs://testinium-qa-reports/builds/build-123/

# Set Cache-Control headers
gsutil -m setmeta -h "Cache-Control:public, max-age=3600" \
  "gs://testinium-qa-reports/builds/build-123/**"
```

**Python Script Using google-cloud-storage:**

```python
"""
Google Cloud Storage report upload automation.
"""

from google.cloud import storage
from pathlib import Path
import mimetypes
from datetime import datetime

def upload_to_gcs(
    bucket_name: str,
    build_number: str,
    reports_dir: str = "reports",
    project_id: str = None
) -> str:
    """
    Upload test reports to Google Cloud Storage.
    
    Args:
        bucket_name: GCS bucket name
        build_number: Build identifier
        reports_dir: Local reports directory
        project_id: GCP project ID (optional)
        
    Returns:
        str: Public URL of uploaded reports
    """
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    
    reports_path = Path(reports_dir)
    uploaded_count = 0
    
    for file_path in reports_path.rglob('*'):
        if file_path.is_file():
            # Create blob path
            relative_path = file_path.relative_to(reports_path)
            blob_path = f"builds/{build_number}/{relative_path}"
            
            # Create blob
            blob = bucket.blob(blob_path)
            
            # Guess content type
            content_type, _ = mimetypes.guess_type(str(file_path))
            if content_type:
                blob.content_type = content_type
            
            # Set cache control
            blob.cache_control = 'public, max-age=3600'
            
            # Set metadata
            blob.metadata = {
                'build_number': build_number,
                'upload_timestamp': datetime.utcnow().isoformat()
            }
            
            # Upload file
            blob.upload_from_filename(str(file_path))
            uploaded_count += 1
            print(f"Uploaded: {blob_path}")
    
    report_url = f"https://storage.googleapis.com/{bucket_name}/builds/{build_number}/"
    print(f"\n✓ Uploaded {uploaded_count} files")
    print(f"Reports URL: {report_url}")
    
    return report_url
```

### Cloud CDN Configuration

**Enable Cloud CDN:**

```bash
# Create backend bucket
gcloud compute backend-buckets create testinium-reports-backend \
  --gcs-bucket-name=testinium-qa-reports \
  --enable-cdn

# Create URL map
gcloud compute url-maps create testinium-reports-url-map \
  --default-backend-bucket=testinium-reports-backend

# Create HTTP(S) proxy
gcloud compute target-http-proxies create testinium-reports-proxy \
  --url-map=testinium-reports-url-map

# Create forwarding rule
gcloud compute forwarding-rules create testinium-reports-http-rule \
  --global \
  --target-http-proxy=testinium-reports-proxy \
  --ports=80
```

### Custom Domain with Cloud Load Balancing

**Configure custom domain:**

```bash
# Reserve static IP
gcloud compute addresses create testinium-reports-ip --global

# Get reserved IP address
gcloud compute addresses describe testinium-reports-ip --global --format="value(address)"

# Update DNS with A record:
# reports.example.com → [RESERVED_IP]

# Create SSL certificate
gcloud compute ssl-certificates create testinium-reports-cert \
  --domains=reports.example.com \
  --global

# Create HTTPS proxy
gcloud compute target-https-proxies create testinium-reports-https-proxy \
  --url-map=testinium-reports-url-map \
  --ssl-certificates=testinium-reports-cert

# Create HTTPS forwarding rule
gcloud compute forwarding-rules create testinium-reports-https-rule \
  --global \
  --target-https-proxy=testinium-reports-https-proxy \
  --ports=443 \
  --address=testinium-reports-ip
```

## Allure Report Server Deployment

Deploying a dedicated Allure Report Server enables persistent report hosting with historical trend analysis, real-time report viewing, and team collaboration features.

### Allure Docker Service

**Docker Deployment:**

```bash
# Pull Allure Docker Service image
docker pull frankescobar/allure-docker-service:latest

# Run Allure server with volume mounting
docker run -d \
  --name allure-server \
  -p 5050:5050 \
  -v ${PWD}/reports/allure-results:/app/allure-results \
  -v ${PWD}/reports/allure-reports:/app/default-reports \
  -e CHECK_RESULTS_EVERY_SECONDS=5 \
  -e KEEP_HISTORY=1 \
  frankescobar/allure-docker-service:latest

# Access Allure server
open http://localhost:5050/allure-docker-service/projects/default/reports/latest
```

**Docker Compose Configuration (`docker-compose.allure.yml`):**

```yaml
version: '3.8'

services:
  allure-server:
    image: frankescobar/allure-docker-service:latest
    container_name: testinium-allure-server
    ports:
      - "5050:5050"
    volumes:
      - ./reports/allure-results:/app/allure-results
      - ./reports/allure-reports:/app/default-reports
      - allure-history:/app/projects/default/reports/history
    environment:
      CHECK_RESULTS_EVERY_SECONDS: "5"
      KEEP_HISTORY: "1"
      KEEP_HISTORY_LATEST: "25"
    restart: unless-stopped
    networks:
      - testinium-network

  allure-ui:
    image: frankescobar/allure-docker-service-ui:latest
    container_name: testinium-allure-ui
    ports:
      - "5252:5252"
    environment:
      ALLURE_DOCKER_PUBLIC_API_URL: "http://localhost:5050"
      ALLURE_DOCKER_PUBLIC_API_URL_PREFIX: "/allure-docker-service"
    depends_on:
      - allure-server
    restart: unless-stopped
    networks:
      - testinium-network

volumes:
  allure-history:
    driver: local

networks:
  testinium-network:
    driver: bridge
```

**Start Allure services:**

```bash
docker-compose -f docker-compose.allure.yml up -d

# Access Allure UI with project management
open http://localhost:5252
```

### Kubernetes Deployment

**Kubernetes Deployment Manifest (`allure-server-deployment.yaml`):**

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: allure-reports-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: allure-server
  labels:
    app: allure-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: allure-server
  template:
    metadata:
      labels:
        app: allure-server
    spec:
      containers:
      - name: allure-server
        image: frankescobar/allure-docker-service:latest
        ports:
        - containerPort: 5050
        env:
        - name: CHECK_RESULTS_EVERY_SECONDS
          value: "5"
        - name: KEEP_HISTORY
          value: "1"
        - name: KEEP_HISTORY_LATEST
          value: "50"
        volumeMounts:
        - name: allure-reports
          mountPath: /app/projects/default/reports
      volumes:
      - name: allure-reports
        persistentVolumeClaim:
          claimName: allure-reports-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: allure-server-service
spec:
  type: LoadBalancer
  selector:
    app: allure-server
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5050
```

**Deploy to Kubernetes:**

```bash
kubectl apply -f allure-server-deployment.yaml

# Get external IP
kubectl get service allure-server-service

# Access Allure server
open http://[EXTERNAL_IP]/allure-docker-service/projects/default/reports/latest
```

### Upload Results from CI/CD Pipeline

**Upload Script (`upload_to_allure_server.sh`):**

```bash
#!/bin/bash
# Upload Allure results to Allure Docker Service

ALLURE_SERVER="http://allure-server:5050"
PROJECT_ID="default"
BUILD_NUMBER="${BUILD_NUMBER:-$(date +%s)}"

# Clean previous results on server
curl -X GET "${ALLURE_SERVER}/allure-docker-service/clean-results?project_id=${PROJECT_ID}"

# Upload all result files
for file in reports/allure-results/*; do
  curl -X POST \
    "${ALLURE_SERVER}/allure-docker-service/send-results?project_id=${PROJECT_ID}" \
    -H "Content-Type: multipart/form-data" \
    -F "files[]=@${file}"
done

# Generate report
curl -X GET \
  "${ALLURE_SERVER}/allure-docker-service/generate-report?project_id=${PROJECT_ID}&execution_name=Build-${BUILD_NUMBER}&execution_from=&execution_type=&force_project_creation=true"

echo "Report available at: ${ALLURE_SERVER}/allure-docker-service/projects/${PROJECT_ID}/reports/latest"
```

**Jenkins Pipeline Integration:**

```groovy
stage('Publish to Allure Server') {
    steps {
        script {
            sh '''
                chmod +x upload_to_allure_server.sh
                ./upload_to_allure_server.sh
            '''
        }
    }
}
```

**Source:** Referenced from `jenkins-integration.md` and `README.md:449-454`

### Authentication Setup for Private Reports

**Nginx Reverse Proxy with Basic Auth:**

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name reports.example.com;

    auth_basic "Allure Test Reports";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://allure-server:5050;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Create password file:**

```bash
# Install htpasswd utility
sudo apt-get install apache2-utils

# Create password file
htpasswd -c .htpasswd testuser

# Run Nginx with authentication
docker run -d \
  --name allure-nginx \
  -p 80:80 \
  -v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf:ro \
  -v $(pwd)/.htpasswd:/etc/nginx/.htpasswd:ro \
  --link allure-server:allure-server \
  nginx:alpine
```

### Trend Analysis with Historical Data

Allure's historical trend analysis automatically tracks:

- **Test execution duration trends:** Identify performance degradation
- **Pass/fail rate trends:** Monitor test stability
- **Test distribution by feature/severity:** Coverage analysis
- **Flaky test detection:** Tests with intermittent failures
- **Retry analysis:** Tests requiring multiple attempts

**Configuration for History Retention:**

In Docker Compose or Kubernetes, ensure:
- `KEEP_HISTORY=1` environment variable is set
- Persistent volume for `/app/projects/default/reports/history`
- `KEEP_HISTORY_LATEST=50` to retain last 50 builds

## CI/CD Native Report Publishing

Leverage built-in report publishing features of CI/CD platforms for seamless integration without additional infrastructure.

### Jenkins HTML Publisher Plugin

**Install Plugin:**
- Navigate to **Manage Jenkins** → **Manage Plugins**
- Search for "HTML Publisher"
- Install without restart

**Jenkinsfile Configuration:**

```groovy
pipeline {
    agent any
    
    stages {
        stage('Run Tests') {
            steps {
                sh '''
                    python -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    behave -f json -o reports/cucumber.json \
                           -f behave_html_formatter:HTMLFormatter -o reports/report.html
                '''
            }
        }
    }
    
    post {
        always {
            // Publish HTML report
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Behave Test Report',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: false
            ])
            
            // Publish JUnit test results
            junit 'reports/junit/**/*.xml'
            
            // Archive artifacts
            archiveArtifacts artifacts: 'reports/screenshots/*.png', allowEmptyArchive: true
        }
    }
}
```

**Source:** `README.md:440-464`

### Jenkins Allure Plugin

**Install and Configure:**

```groovy
pipeline {
    agent any
    
    stages {
        stage('Run Tests') {
            steps {
                sh 'behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results'
            }
        }
    }
    
    post {
        always {
            // Generate and publish Allure report
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'reports/allure-results']]
            ])
        }
    }
}
```

**Access Reports:**
- Navigate to build page → **Allure Report** link in left sidebar
- Historical trends available across builds

### GitHub Actions Artifacts and Pages

**Workflow with Artifacts (`test-and-report.yml`):**

```yaml
name: Test and Publish Reports

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install Dependencies
        run: pip install -r requirements.txt
      
      - name: Run Tests
        run: |
          behave -f json -o reports/cucumber.json \
                 -f behave_html_formatter:HTMLFormatter -o reports/report.html
        continue-on-error: true
      
      - name: Upload Test Reports
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-reports
          path: reports/
          retention-days: 30
      
      - name: Publish Test Results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          junit_files: 'reports/junit/**/*.xml'
```

**Accessing Artifacts:**
- Navigate to workflow run
- Scroll to **Artifacts** section
- Download `test-reports.zip`

### GitLab CI Pages Deployment

**`.gitlab-ci.yml` Configuration:**

```yaml
stages:
  - test
  - deploy

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - behave -f json -o reports/cucumber.json
  artifacts:
    paths:
      - reports/
    expire_in: 30 days

pages:
  stage: deploy
  dependencies:
    - test
  script:
    - mkdir -p public
    - cp -r reports/* public/
  artifacts:
    paths:
      - public
  only:
    - main
```

**Access Reports:**
- **URL:** `https://<username>.gitlab.io/<project>/`
- Reports automatically deployed to GitLab Pages on main branch

### Azure Pipelines Test Results

**`azure-pipelines.yml` Configuration:**

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'
    
- script: |
    pip install -r requirements.txt
    behave --junit --junit-directory $(System.DefaultWorkingDirectory)/reports/junit
  displayName: 'Run Tests'
  continueOnError: true

- task: PublishTestResults@2
  condition: always()
  inputs:
    testResultsFormat: 'JUnit'
    testResultsFiles: '**/junit/*.xml'
    mergeTestResults: true
    failTaskOnFailedTests: false
    testRunTitle: 'Behave Test Results'

- task: PublishBuildArtifacts@1
  condition: always()
  inputs:
    PathtoPublish: '$(System.DefaultWorkingDirectory)/reports'
    ArtifactName: 'test-reports'
```

**View Results:**
- Navigate to pipeline run → **Tests** tab
- Download artifacts from **Summary** page

## Custom Dashboard Creation

Building custom dashboards enables aggregated views of test results across multiple projects, environments, and time periods with tailored metrics and visualizations.

### Aggregating Test Results from Multiple Runs

**Data Extraction from JSON Reports:**

```python
"""
Test results aggregator for custom dashboard.
Extracts metrics from Behave JSON reports.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

class TestResultsAggregator:
    """Aggregates test results from multiple JSON report files."""
    
    def __init__(self, reports_directory: str = "reports"):
        self.reports_dir = Path(reports_directory)
    
    def extract_metrics(self, json_file: Path) -> Dict[str, Any]:
        """
        Extract key metrics from Behave JSON report.
        
        Args:
            json_file: Path to JSON report file
            
        Returns:
            dict: Extracted metrics including pass rate, duration, failures
        """
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        total_scenarios = 0
        passed_scenarios = 0
        failed_scenarios = 0
        skipped_scenarios = 0
        total_duration = 0
        failed_tests = []
        
        for feature in data:
            feature_name = feature.get('name', 'Unknown')
            
            for scenario in feature.get('elements', []):
                if scenario.get('type') == 'scenario':
                    total_scenarios += 1
                    scenario_status = self._get_scenario_status(scenario)
                    scenario_duration = self._get_scenario_duration(scenario)
                    
                    total_duration += scenario_duration
                    
                    if scenario_status == 'passed':
                        passed_scenarios += 1
                    elif scenario_status == 'failed':
                        failed_scenarios += 1
                        failed_tests.append({
                            'feature': feature_name,
                            'scenario': scenario.get('name'),
                            'error': self._get_failure_message(scenario)
                        })
                    elif scenario_status == 'skipped':
                        skipped_scenarios += 1
        
        pass_rate = (passed_scenarios / total_scenarios * 100) if total_scenarios > 0 else 0
        
        return {
            'timestamp': json_file.stat().st_mtime,
            'total_scenarios': total_scenarios,
            'passed': passed_scenarios,
            'failed': failed_scenarios,
            'skipped': skipped_scenarios,
            'pass_rate': round(pass_rate, 2),
            'total_duration_seconds': round(total_duration, 2),
            'average_duration': round(total_duration / total_scenarios, 2) if total_scenarios > 0 else 0,
            'failed_tests': failed_tests
        }
    
    def _get_scenario_status(self, scenario: Dict) -> str:
        """Determine scenario status from steps."""
        steps = scenario.get('steps', [])
        if not steps:
            return 'skipped'
        
        for step in steps:
            result = step.get('result', {})
            status = result.get('status', 'skipped')
            if status == 'failed':
                return 'failed'
            elif status == 'skipped':
                return 'skipped'
        
        return 'passed'
    
    def _get_scenario_duration(self, scenario: Dict) -> float:
        """Calculate total scenario duration."""
        total = 0
        for step in scenario.get('steps', []):
            result = step.get('result', {})
            duration = result.get('duration', 0)
            total += duration
        return total
    
    def _get_failure_message(self, scenario: Dict) -> str:
        """Extract failure error message."""
        for step in scenario.get('steps', []):
            result = step.get('result', {})
            if result.get('status') == 'failed':
                return result.get('error_message', 'Unknown error')
        return 'Unknown error'
    
    def aggregate_multiple_reports(self, json_files: List[Path]) -> List[Dict]:
        """Aggregate metrics from multiple report files."""
        return [self.extract_metrics(f) for f in json_files]
```

### Building Dashboard with Flask Backend

**Flask API Server (`dashboard_server.py`):**

```python
"""
Flask REST API for test results dashboard.
Serves aggregated test metrics and historical data.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from pathlib import Path
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# In production, use database (PostgreSQL, MongoDB)
# For demo, using JSON file storage
RESULTS_DB = Path("dashboard_data/results.json")

@app.route('/api/latest-results', methods=['GET'])
def get_latest_results():
    """Get latest test execution results."""
    if not RESULTS_DB.exists():
        return jsonify({'error': 'No results found'}), 404
    
    with open(RESULTS_DB, 'r') as f:
        all_results = json.load(f)
    
    # Return most recent result
    latest = max(all_results, key=lambda x: x['timestamp'])
    return jsonify(latest)

@app.route('/api/historical-results', methods=['GET'])
def get_historical_results():
    """Get historical test results for trend analysis."""
    days = request.args.get('days', default=30, type=int)
    
    if not RESULTS_DB.exists():
        return jsonify([])
    
    with open(RESULTS_DB, 'r') as f:
        all_results = json.load(f)
    
    # Filter by date range
    cutoff_timestamp = (datetime.now() - timedelta(days=days)).timestamp()
    filtered = [r for r in all_results if r['timestamp'] >= cutoff_timestamp]
    
    return jsonify(filtered)

@app.route('/api/test-details/<test_id>', methods=['GET'])
def get_test_details(test_id: str):
    """Get detailed information about specific test."""
    # Implementation depends on data structure
    return jsonify({'test_id': test_id, 'details': 'Test details here'})

@app.route('/api/flaky-tests', methods=['GET'])
def get_flaky_tests():
    """Identify tests with intermittent failures."""
    if not RESULTS_DB.exists():
        return jsonify([])
    
    with open(RESULTS_DB, 'r') as f:
        all_results = json.load(f)
    
    # Analyze failure patterns
    test_runs = {}
    for result in all_results:
        for failed_test in result.get('failed_tests', []):
            test_key = f"{failed_test['feature']}-{failed_test['scenario']}"
            if test_key not in test_runs:
                test_runs[test_key] = {'passes': 0, 'failures': 0}
            test_runs[test_key]['failures'] += 1
    
    # Identify flaky tests (tests that both pass and fail)
    flaky = [
        {'test': test, 'failure_rate': stats['failures'] / (stats['failures'] + stats['passes'])}
        for test, stats in test_runs.items()
        if stats['passes'] > 0 and stats['failures'] > 0
    ]
    
    return jsonify(flaky)

@app.route('/api/metrics-summary', methods=['GET'])
def get_metrics_summary():
    """Get aggregated metrics summary."""
    if not RESULTS_DB.exists():
        return jsonify({'error': 'No data'}), 404
    
    with open(RESULTS_DB, 'r') as f:
        all_results = json.load(f)
    
    if not all_results:
        return jsonify({'error': 'No data'}), 404
    
    # Calculate aggregate metrics
    total_runs = len(all_results)
    avg_pass_rate = sum(r['pass_rate'] for r in all_results) / total_runs
    avg_duration = sum(r['total_duration_seconds'] for r in all_results) / total_runs
    
    return jsonify({
        'total_runs': total_runs,
        'average_pass_rate': round(avg_pass_rate, 2),
        'average_duration': round(avg_duration, 2),
        'last_run': max(all_results, key=lambda x: x['timestamp'])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
```

### Frontend Dashboard (React/Vue Example)

**Simple HTML/JavaScript Dashboard:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Results Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .metrics { display: flex; gap: 20px; margin: 20px 0; }
        .metric-card { 
            background: #f0f0f0; 
            padding: 20px; 
            border-radius: 8px; 
            flex: 1; 
            text-align: center;
        }
        .metric-value { font-size: 2em; font-weight: bold; }
        .metric-label { color: #666; }
        .chart-container { margin: 20px 0; }
        canvas { max-height: 400px; }
    </style>
</head>
<body>
    <h1>Testinium QA Test Dashboard</h1>
    
    <div class="metrics" id="metrics">
        <!-- Dynamically populated -->
    </div>
    
    <div class="chart-container">
        <canvas id="passRateChart"></canvas>
    </div>
    
    <div class="chart-container">
        <canvas id="durationChart"></canvas>
    </div>
    
    <script>
        const API_URL = 'http://localhost:5000/api';
        
        // Fetch and display metrics
        async function loadMetrics() {
            const response = await fetch(`${API_URL}/metrics-summary`);
            const data = await response.json();
            
            document.getElementById('metrics').innerHTML = `
                <div class="metric-card">
                    <div class="metric-value">${data.total_runs}</div>
                    <div class="metric-label">Total Test Runs</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${data.average_pass_rate}%</div>
                    <div class="metric-label">Average Pass Rate</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${data.average_duration}s</div>
                    <div class="metric-label">Average Duration</div>
                </div>
            `;
        }
        
        // Load historical data and render charts
        async function loadCharts() {
            const response = await fetch(`${API_URL}/historical-results?days=30`);
            const data = await response.json();
            
            const labels = data.map(r => new Date(r.timestamp * 1000).toLocaleDateString());
            const passRates = data.map(r => r.pass_rate);
            const durations = data.map(r => r.total_duration_seconds);
            
            // Pass rate trend chart
            new Chart(document.getElementById('passRateChart'), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Pass Rate (%)',
                        data: passRates,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: { display: true, text: 'Pass Rate Trend (Last 30 Days)' }
                    }
                }
            });
            
            // Duration trend chart
            new Chart(document.getElementById('durationChart'), {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Duration (seconds)',
                        data: durations,
                        backgroundColor: 'rgb(54, 162, 235)'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: { display: true, text: 'Execution Duration Trend' }
                    }
                }
            });
        }
        
        // Initialize dashboard
        loadMetrics();
        loadCharts();
    </script>
</body>
</html>
```

### Storing Results in Database

**PostgreSQL Schema:**

```sql
CREATE TABLE test_runs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    build_number VARCHAR(50),
    environment VARCHAR(50),
    total_scenarios INTEGER,
    passed INTEGER,
    failed INTEGER,
    skipped INTEGER,
    pass_rate DECIMAL(5,2),
    duration_seconds DECIMAL(10,2)
);

CREATE TABLE test_failures (
    id SERIAL PRIMARY KEY,
    test_run_id INTEGER REFERENCES test_runs(id),
    feature_name VARCHAR(255),
    scenario_name VARCHAR(255),
    error_message TEXT,
    screenshot_path VARCHAR(500)
);

CREATE INDEX idx_test_runs_timestamp ON test_runs(timestamp);
CREATE INDEX idx_test_failures_run_id ON test_failures(test_run_id);
```

### Embedding Allure Reports in Dashboard

```html
<div class="allure-embed">
    <h2>Latest Allure Report</h2>
    <iframe 
        src="https://reports.example.com/allure-report/index.html" 
        width="100%" 
        height="800px" 
        frameborder="0">
    </iframe>
</div>
```

## Test Result APIs

Creating RESTful APIs for test results enables programmatic access, external integrations, and custom automation workflows.

### FastAPI REST Service

**Complete API Implementation (`test_results_api.py`):**

```python
"""
FastAPI REST API for test results with authentication.
"""

from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
from pathlib import Path

app = FastAPI(title="Testinium QA Test Results API", version="1.0")

# API Key authentication
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In production, store in environment variable or secret manager
VALID_API_KEYS = {"test-api-key-12345", "ci-cd-integration-key"}

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# Pydantic models
class TestRun(BaseModel):
    id: int
    timestamp: datetime
    build_number: str
    total_scenarios: int
    passed: int
    failed: int
    pass_rate: float
    duration_seconds: float

class TestFailure(BaseModel):
    feature: str
    scenario: str
    error_message: str
    screenshot_url: Optional[str]

# Endpoints
@app.get("/api/v1/runs/latest", response_model=TestRun)
async def get_latest_run(api_key: APIKey = Depends(get_api_key)):
    """Get latest test run results."""
    # Implementation: Query database for latest run
    return TestRun(
        id=123,
        timestamp=datetime.now(),
        build_number="456",
        total_scenarios=50,
        passed=48,
        failed=2,
        pass_rate=96.0,
        duration_seconds=120.5
    )

@app.get("/api/v1/runs", response_model=List[TestRun])
async def get_runs(
    limit: int = 10,
    api_key: APIKey = Depends(get_api_key)
):
    """Get recent test runs."""
    # Implementation: Query database with limit
    return []

@app.get("/api/v1/runs/{run_id}/failures", response_model=List[TestFailure])
async def get_run_failures(
    run_id: int,
    api_key: APIKey = Depends(get_api_key)
):
    """Get failures for specific test run."""
    # Implementation: Query failures for run_id
    return []

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint (no auth required)."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
```

**Run API Server:**

```bash
# Install FastAPI and uvicorn
pip install fastapi uvicorn

# Run server
uvicorn test_results_api:app --host 0.0.0.0 --port 8000 --reload

# Access API docs
open http://localhost:8000/docs
```

### Integration with Slack/Teams Bots

**Slack Webhook Integration:**

```python
"""
Send test results notification to Slack channel.
"""

import requests
import json

def send_slack_notification(webhook_url: str, test_results: dict):
    """
    Send test results summary to Slack.
    
    Args:
        webhook_url: Slack incoming webhook URL
        test_results: Dict with test metrics
    """
    pass_rate = test_results['pass_rate']
    status_emoji = "✅" if pass_rate >= 95 else "⚠️" if pass_rate >= 80 else "❌"
    
    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{status_emoji} Test Results - Build #{test_results['build_number']}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Pass Rate:*\n{pass_rate}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Duration:*\n{test_results['duration']}s"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Passed:*\n{test_results['passed']}/{test_results['total']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Failed:*\n{test_results['failed']}"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "View Full Report"},
                        "url": test_results['report_url']
                    }
                ]
            }
        ]
    }
    
    response = requests.post(webhook_url, json=message)
    response.raise_for_status()

# Usage in environment.py after_all hook
def after_all(context):
    if os.getenv('SLACK_WEBHOOK_URL'):
        send_slack_notification(
            os.getenv('SLACK_WEBHOOK_URL'),
            {
                'build_number': os.getenv('BUILD_NUMBER', 'local'),
                'pass_rate': 95.5,
                'duration': 120,
                'passed': 48,
                'failed': 2,
                'total': 50,
                'report_url': 'https://reports.example.com/latest'
            }
        )
```

**Microsoft Teams Webhook Integration:**

```python
"""
Send test results notification to Microsoft Teams channel.
"""

import requests
import json

def send_teams_notification(webhook_url: str, test_results: dict):
    """
    Send test results to Microsoft Teams using Adaptive Card.
    
    Args:
        webhook_url: Teams incoming webhook URL
        test_results: Dict with test metrics
    """
    pass_rate = test_results['pass_rate']
    
    # Determine status color
    if pass_rate >= 95:
        color = "good"
        status = "Success"
    elif pass_rate >= 80:
        color = "warning"
        status = "Warning"
    else:
        color = "attention"
        status = "Failed"
    
    message = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": f"Test Results - Build #{test_results['build_number']}",
        "themeColor": color,
        "title": f"Test Execution {status}",
        "sections": [
            {
                "activityTitle": f"Build #{test_results['build_number']}",
                "facts": [
                    {"name": "Pass Rate", "value": f"{pass_rate}%"},
                    {"name": "Duration", "value": f"{test_results['duration']}s"},
                    {"name": "Total Tests", "value": str(test_results['total'])},
                    {"name": "Passed", "value": str(test_results['passed'])},
                    {"name": "Failed", "value": str(test_results['failed'])}
                ]
            }
        ],
        "potentialAction": [
            {
                "@type": "OpenUri",
                "name": "View Full Report",
                "targets": [
                    {"os": "default", "uri": test_results['report_url']}
                ]
            }
        ]
    }
    
    response = requests.post(webhook_url, json=message)
    response.raise_for_status()
```

**Email Report Integration:**

```python
"""
Send email report with test results summary.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_report(smtp_config: dict, test_results: dict, recipients: list):
    """
    Send HTML email report with test results.
    
    Args:
        smtp_config: SMTP server configuration
        test_results: Test execution results
        recipients: List of email addresses
    """
    # Create HTML email body
    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .summary {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
            .metric {{ display: inline-block; margin: 10px; }}
            .metric-value {{ font-size: 24px; font-weight: bold; }}
            .pass {{ color: green; }}
            .fail {{ color: red; }}
        </style>
    </head>
    <body>
        <h2>Test Execution Report - Build #{test_results['build_number']}</h2>
        
        <div class="summary">
            <div class="metric">
                <div class="metric-value pass">{test_results['pass_rate']}%</div>
                <div>Pass Rate</div>
            </div>
            <div class="metric">
                <div class="metric-value">{test_results['passed']}</div>
                <div>Passed</div>
            </div>
            <div class="metric">
                <div class="metric-value fail">{test_results['failed']}</div>
                <div>Failed</div>
            </div>
            <div class="metric">
                <div class="metric-value">{test_results['duration']}s</div>
                <div>Duration</div>
            </div>
        </div>
        
        <p><a href="{test_results['report_url']}">View Full Report</a></p>
    </body>
    </html>
    """
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Test Results - Build #{test_results['build_number']}"
    msg['From'] = smtp_config['from_address']
    msg['To'] = ', '.join(recipients)
    
    msg.attach(MIMEText(html_body, 'html'))
    
    # Send email
    with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
        if smtp_config.get('use_tls'):
            server.starttls()
        if smtp_config.get('username'):
            server.login(smtp_config['username'], smtp_config['password'])
        server.send_message(msg)
```

**PagerDuty Integration for Critical Failures:**

```python
"""
Trigger PagerDuty incident for critical test failures.
"""

import requests

def trigger_pagerduty_incident(integration_key: str, test_results: dict):
    """
    Create PagerDuty incident when pass rate falls below threshold.
    
    Args:
        integration_key: PagerDuty Events API v2 integration key
        test_results: Test execution results
    """
    if test_results['pass_rate'] < 80:  # Critical threshold
        event = {
            "routing_key": integration_key,
            "event_action": "trigger",
            "payload": {
                "summary": f"Critical test failure - Build #{test_results['build_number']}",
                "severity": "error",
                "source": "testinium-qa",
                "custom_details": {
                    "pass_rate": f"{test_results['pass_rate']}%",
                    "failed_tests": test_results['failed'],
                    "build_number": test_results['build_number'],
                    "report_url": test_results['report_url']
                }
            },
            "links": [
                {
                    "href": test_results['report_url'],
                    "text": "View Test Report"
                }
            ]
        }
        
        response = requests.post(
            'https://events.pagerduty.com/v2/enqueue',
            json=event
        )
        response.raise_for_status()
```

## Historical Trend Analysis

Tracking test results over time reveals patterns, identifies flaky tests, and helps measure quality improvements.

### Storing Test Results Over Time

**Database Schema for Historical Tracking:**

```sql
-- Extended schema with historical tracking
CREATE TABLE test_run_history (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    build_number VARCHAR(50),
    branch VARCHAR(100),
    environment VARCHAR(50),
    total_scenarios INTEGER,
    passed INTEGER,
    failed INTEGER,
    skipped INTEGER,
    pass_rate DECIMAL(5,2),
    duration_seconds DECIMAL(10,2),
    commit_sha VARCHAR(40),
    triggered_by VARCHAR(100)
);

CREATE TABLE test_case_history (
    id SERIAL PRIMARY KEY,
    test_run_id INTEGER REFERENCES test_run_history(id),
    feature_name VARCHAR(255),
    scenario_name VARCHAR(255),
    status VARCHAR(20), -- passed, failed, skipped
    duration_seconds DECIMAL(10,2),
    error_message TEXT
);

-- Indexes for efficient querying
CREATE INDEX idx_history_timestamp ON test_run_history(timestamp);
CREATE INDEX idx_history_branch ON test_run_history(branch);
CREATE INDEX idx_case_history_scenario ON test_case_history(scenario_name);
```

### Calculating Metrics

**Trend Analysis Script:**

```python
"""
Calculate historical test metrics and trends.
"""

from datetime import datetime, timedelta
from typing import List, Dict
import psycopg2

class TrendAnalyzer:
    """Analyzes test execution trends over time."""
    
    def __init__(self, db_config: dict):
        self.conn = psycopg2.connect(**db_config)
    
    def calculate_pass_rate_trend(self, days: int = 30) -> List[Dict]:
        """Calculate daily pass rate trend."""
        query = """
        SELECT 
            DATE(timestamp) as date,
            AVG(pass_rate) as avg_pass_rate,
            COUNT(*) as num_runs
        FROM test_run_history
        WHERE timestamp >= NOW() - INTERVAL '%s days'
        GROUP BY DATE(timestamp)
        ORDER BY date
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (days,))
            return [
                {
                    'date': row[0].isoformat(),
                    'pass_rate': float(row[1]),
                    'num_runs': row[2]
                }
                for row in cur.fetchall()
            ]
    
    def calculate_execution_time_trend(self, days: int = 30) -> List[Dict]:
        """Calculate execution time trends."""
        query = """
        SELECT 
            DATE(timestamp) as date,
            AVG(duration_seconds) as avg_duration,
            MIN(duration_seconds) as min_duration,
            MAX(duration_seconds) as max_duration
        FROM test_run_history
        WHERE timestamp >= NOW() - INTERVAL '%s days'
        GROUP BY DATE(timestamp)
        ORDER BY date
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (days,))
            return [
                {
                    'date': row[0].isoformat(),
                    'avg_duration': float(row[1]),
                    'min_duration': float(row[2]),
                    'max_duration': float(row[3])
                }
                for row in cur.fetchall()
            ]
    
    def identify_flaky_tests(self, min_runs: int = 10) -> List[Dict]:
        """
        Identify tests with intermittent failures (flaky tests).
        
        A test is considered flaky if it has both passes and failures
        in recent runs.
        """
        query = """
        SELECT 
            scenario_name,
            feature_name,
            COUNT(*) as total_runs,
            SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) as passes,
            SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failures,
            ROUND(
                100.0 * SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) / COUNT(*),
                2
            ) as failure_rate
        FROM test_case_history tch
        JOIN test_run_history trh ON tch.test_run_id = trh.id
        WHERE trh.timestamp >= NOW() - INTERVAL '30 days'
        GROUP BY scenario_name, feature_name
        HAVING COUNT(*) >= %s
            AND SUM(CASE WHEN status = 'passed' THEN 1 ELSE 0 END) > 0
            AND SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) > 0
        ORDER BY failure_rate DESC
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (min_runs,))
            return [
                {
                    'scenario': row[0],
                    'feature': row[1],
                    'total_runs': row[2],
                    'passes': row[3],
                    'failures': row[4],
                    'failure_rate': float(row[5])
                }
                for row in cur.fetchall()
            ]
    
    def identify_top_failures(self, limit: int = 10) -> List[Dict]:
        """Get most frequently failing tests."""
        query = """
        SELECT 
            scenario_name,
            feature_name,
            COUNT(*) as failure_count,
            MAX(timestamp) as last_failure
        FROM test_case_history tch
        JOIN test_run_history trh ON tch.test_run_id = trh.id
        WHERE status = 'failed'
            AND timestamp >= NOW() - INTERVAL '30 days'
        GROUP BY scenario_name, feature_name
        ORDER BY failure_count DESC
        LIMIT %s
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (limit,))
            return [
                {
                    'scenario': row[0],
                    'feature': row[1],
                    'failure_count': row[2],
                    'last_failure': row[3].isoformat()
                }
                for row in cur.fetchall()
            ]
    
    def detect_regressions(self, baseline_days: int = 7) -> List[Dict]:
        """
        Detect new test failures (regressions).
        
        Compares recent failures against baseline period.
        """
        query = """
        WITH baseline AS (
            SELECT DISTINCT scenario_name, feature_name
            FROM test_case_history tch
            JOIN test_run_history trh ON tch.test_run_id = trh.id
            WHERE status = 'passed'
                AND timestamp >= NOW() - INTERVAL '%s days'
                AND timestamp < NOW() - INTERVAL '1 day'
        ),
        recent_failures AS (
            SELECT DISTINCT scenario_name, feature_name
            FROM test_case_history tch
            JOIN test_run_history trh ON tch.test_run_id = trh.id
            WHERE status = 'failed'
                AND timestamp >= NOW() - INTERVAL '1 day'
        )
        SELECT rf.scenario_name, rf.feature_name
        FROM recent_failures rf
        JOIN baseline b ON rf.scenario_name = b.scenario_name 
            AND rf.feature_name = b.feature_name
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (baseline_days,))
            return [
                {'scenario': row[0], 'feature': row[1]}
                for row in cur.fetchall()
            ]
```

### Visualizing Trends

**Matplotlib Chart Generation:**

```python
"""
Generate trend visualization charts.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def plot_pass_rate_trend(data: List[Dict], output_file: str):
    """Generate pass rate trend line chart."""
    dates = [datetime.fromisoformat(d['date']) for d in data]
    pass_rates = [d['pass_rate'] for d in data]
    
    plt.figure(figsize=(12, 6))
    plt.plot(dates, pass_rates, marker='o', linewidth=2, markersize=6)
    plt.axhline(y=95, color='g', linestyle='--', label='Target (95%)')
    plt.axhline(y=80, color='r', linestyle='--', label='Critical (80%)')
    
    plt.title('Test Pass Rate Trend (Last 30 Days)', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Pass Rate (%)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()

def plot_duration_trend(data: List[Dict], output_file: str):
    """Generate execution duration trend chart."""
    dates = [datetime.fromisoformat(d['date']) for d in data]
    avg_durations = [d['avg_duration'] for d in data]
    min_durations = [d['min_duration'] for d in data]
    max_durations = [d['max_duration'] for d in data]
    
    plt.figure(figsize=(12, 6))
    plt.plot(dates, avg_durations, marker='o', label='Average', linewidth=2)
    plt.fill_between(dates, min_durations, max_durations, alpha=0.3, label='Min-Max Range')
    
    plt.title('Test Execution Duration Trend', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Duration (seconds)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    plt.close()
```

## Report Access Control

Implementing access control ensures sensitive test results are only accessible to authorized users.

### Authentication Strategies

**Basic Authentication (Nginx):**

```nginx
# nginx.conf for basic auth protected reports
server {
    listen 80;
    server_name reports.example.com;
    
    location / {
        root /var/www/test-reports;
        index index.html;
        
        # Enable basic authentication
        auth_basic "Test Reports Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        
        # Deny access to sensitive files
        location ~ /\. {
            deny all;
        }
    }
}
```

**Create Password File:**

```bash
# Install apache2-utils for htpasswd
sudo apt-get install apache2-utils

# Create password file
sudo htpasswd -c /etc/nginx/.htpasswd admin
sudo htpasswd /etc/nginx/.htpasswd developer

# Reload nginx
sudo nginx -s reload
```

**OAuth2 Integration (Example with Auth0):**

```python
"""
Flask app with OAuth2 authentication for reports.
"""

from flask import Flask, redirect, session, url_for, render_template
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    api_base_url=f"https://{os.getenv('AUTH0_DOMAIN')}",
    access_token_url=f"https://{os.getenv('AUTH0_DOMAIN')}/oauth/token",
    authorize_url=f"https://{os.getenv('AUTH0_DOMAIN')}/authorize",
    client_kwargs={
        'scope': 'openid profile email',
    },
)

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/callback')
def callback():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    
    session['user'] = userinfo
    return redirect('/reports')

@app.route('/reports')
def reports():
    if 'user' not in session:
        return redirect('/login')
    
    # Serve reports only to authenticated users
    return render_template('reports.html', user=session['user'])
```

### Role-Based Access Control

**RBAC Implementation:**

```python
"""
Role-based access control for test reports.
"""

from enum import Enum
from functools import wraps
from flask import session, abort

class Role(Enum):
    VIEWER = "viewer"       # Can view reports only
    EDITOR = "editor"       # Can view and regenerate reports
    ADMIN = "admin"         # Full access including deletion

# User role mapping (in production, store in database)
USER_ROLES = {
    'admin@example.com': Role.ADMIN,
    'developer@example.com': Role.EDITOR,
    'qa@example.com': Role.EDITOR,
    'manager@example.com': Role.VIEWER
}

def require_role(required_role: Role):
    """Decorator to enforce role-based access."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                abort(401)  # Unauthorized
            
            user_email = session['user']['email']
            user_role = USER_ROLES.get(user_email, Role.VIEWER)
            
            # Check if user has required role
            role_hierarchy = {
                Role.ADMIN: 3,
                Role.EDITOR: 2,
                Role.VIEWER: 1
            }
            
            if role_hierarchy[user_role] < role_hierarchy[required_role]:
                abort(403)  # Forbidden
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usage examples
@app.route('/reports/view')
@require_role(Role.VIEWER)
def view_reports():
    return "Report viewing page"

@app.route('/reports/regenerate', methods=['POST'])
@require_role(Role.EDITOR)
def regenerate_report():
    return "Report regeneration endpoint"

@app.route('/reports/delete', methods=['DELETE'])
@require_role(Role.ADMIN)
def delete_report():
    return "Report deletion endpoint"
```

### IP Whitelisting

**AWS S3 Bucket Policy with IP Restriction:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RestrictToOfficeIP",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::test-reports-bucket/*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": [
            "203.0.113.0/24",
            "198.51.100.0/24"
          ]
        }
      }
    }
  ]
}
```

### Audit Logging

**Log Report Access:**

```python
"""
Audit logging for report access.
"""

import logging
from datetime import datetime

# Configure audit logger
audit_logger = logging.getLogger('audit')
audit_handler = logging.FileHandler('logs/report_access_audit.log')
audit_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(message)s')
)
audit_logger.addHandler(audit_handler)
audit_logger.setLevel(logging.INFO)

def log_report_access(user_email: str, report_id: str, action: str, ip_address: str):
    """Log report access for audit trail."""
    audit_logger.info(
        f"USER={user_email} | ACTION={action} | REPORT={report_id} | IP={ip_address}"
    )

# Usage in Flask route
@app.route('/reports/<report_id>')
def view_report(report_id):
    user_email = session['user']['email']
    ip_address = request.remote_addr
    
    log_report_access(user_email, report_id, 'VIEW', ip_address)
    
    return render_report(report_id)
```

## Report Retention and Cleanup

Implementing retention policies prevents unbounded storage growth and maintains compliance with data retention regulations.

### Retention Policies by Environment

**Configuration (`retention_config.yaml`):**

```yaml
retention_policies:
  development:
    days: 7
    description: "Keep dev reports for 1 week"
  
  staging:
    days: 30
    description: "Keep staging reports for 1 month"
  
  production:
    days: 90
    description: "Keep production reports for 3 months"
  
  release:
    days: 365
    description: "Keep release reports for 1 year"
```

### Automated Cleanup Scripts

**Cleanup Script (`cleanup_old_reports.py`):**

```python
"""
Automated cleanup of old test reports based on retention policy.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import yaml

def load_retention_policy(config_file: str = "retention_config.yaml") -> dict:
    """Load retention policies from config file."""
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config['retention_policies']

def cleanup_old_reports(reports_dir: str, environment: str, retention_days: int):
    """
    Delete reports older than retention period.
    
    Args:
        reports_dir: Base directory containing reports
        environment: Environment name (dev, staging, prod)
        retention_days: Number of days to retain reports
    """
    reports_path = Path(reports_dir) / environment
    if not reports_path.exists():
        print(f"Reports directory not found: {reports_path}")
        return
    
    cutoff_date = datetime.now() - timedelta(days=retention_days)
    deleted_count = 0
    freed_space = 0
    
    for report_dir in reports_path.iterdir():
        if not report_dir.is_dir():
            continue
        
        # Get directory modification time
        dir_mtime = datetime.fromtimestamp(report_dir.stat().st_mtime)
        
        if dir_mtime < cutoff_date:
            # Calculate size before deletion
            dir_size = sum(
                f.stat().st_size for f in report_dir.rglob('*') if f.is_file()
            )
            
            # Delete directory
            shutil.rmtree(report_dir)
            deleted_count += 1
            freed_space += dir_size
            
            print(f"Deleted: {report_dir.name} (age: {(datetime.now() - dir_mtime).days} days)")
    
    freed_space_mb = freed_space / (1024 * 1024)
    print(f"\nCleanup complete:")
    print(f"  - Deleted {deleted_count} report directories")
    print(f"  - Freed {freed_space_mb:.2f} MB")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python cleanup_old_reports.py <environment>")
        sys.exit(1)
    
    environment = sys.argv[1]
    policies = load_retention_policy()
    
    if environment not in policies:
        print(f"Unknown environment: {environment}")
        print(f"Available: {list(policies.keys())}")
        sys.exit(1)
    
    retention_days = policies[environment]['days']
    print(f"Cleaning up {environment} reports older than {retention_days} days")
    
    cleanup_old_reports('reports', environment, retention_days)
```

**Cron Job Setup:**

```bash
# Add to crontab for daily cleanup at 2 AM
crontab -e

# Add these lines:
0 2 * * * /usr/bin/python3 /path/to/cleanup_old_reports.py development
0 2 * * * /usr/bin/python3 /path/to/cleanup_old_reports.py staging
0 2 * * * /usr/bin/python3 /path/to/cleanup_old_reports.py production
```

### Archiving to Cold Storage

**AWS S3 Lifecycle Policy:**

```json
{
  "Rules": [
    {
      "Id": "ArchiveOldReports",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "reports/"
      },
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 365
      }
    }
  ]
}
```

**Apply Lifecycle Policy:**

```bash
# Save policy to file: s3-lifecycle-policy.json
# Apply to bucket
aws s3api put-bucket-lifecycle-configuration \
    --bucket test-reports-bucket \
    --lifecycle-configuration file://s3-lifecycle-policy.json
```

### Database Cleanup

**Database Retention Script:**

```sql
-- Stored procedure for cleaning old test run history
CREATE OR REPLACE FUNCTION cleanup_old_test_runs(retention_days INTEGER)
RETURNS TABLE(deleted_runs INTEGER, deleted_cases INTEGER) AS $$
DECLARE
    cutoff_date TIMESTAMP;
    runs_deleted INTEGER;
    cases_deleted INTEGER;
BEGIN
    cutoff_date := NOW() - (retention_days || ' days')::INTERVAL;
    
    -- Delete test case history for old runs
    DELETE FROM test_case_history
    WHERE test_run_id IN (
        SELECT id FROM test_run_history WHERE timestamp < cutoff_date
    );
    GET DIAGNOSTICS cases_deleted = ROW_COUNT;
    
    -- Delete old test runs
    DELETE FROM test_run_history WHERE timestamp < cutoff_date;
    GET DIAGNOSTICS runs_deleted = ROW_COUNT;
    
    RETURN QUERY SELECT runs_deleted, cases_deleted;
END;
$$ LANGUAGE plpgsql;

-- Execute cleanup (keep last 90 days)
SELECT * FROM cleanup_old_test_runs(90);
```

## Advanced Patterns

### Parallel Test Run Report Aggregation

When running tests in parallel, combine results from multiple executions into a single unified report.

**Aggregate Parallel Behave Results:**

```python
"""
Aggregate JSON reports from parallel test executions.
"""

import json
from pathlib import Path
from typing import List

def aggregate_parallel_reports(report_files: List[Path], output_file: Path):
    """
    Combine multiple Behave JSON reports into single unified report.
    
    Args:
        report_files: List of JSON report files from parallel runs
        output_file: Output path for aggregated report
    """
    all_features = []
    
    for report_file in report_files:
        with open(report_file, 'r') as f:
            features = json.load(f)
            all_features.extend(features)
    
    # Write aggregated report
    with open(output_file, 'w') as f:
        json.dump(all_features, f, indent=2)
    
    print(f"Aggregated {len(report_files)} reports into {output_file}")
    print(f"Total features: {len(all_features)}")

# Usage
if __name__ == '__main__':
    reports_dir = Path('reports/parallel')
    json_files = list(reports_dir.glob('worker_*.json'))
    aggregate_parallel_reports(json_files, Path('reports/aggregated_report.json'))
```

### Comparison Reports

**Compare Current vs Previous Run:**

```python
"""
Generate comparison report between two test runs.
"""

from typing import Dict, List

def compare_test_runs(current_results: Dict, previous_results: Dict) -> Dict:
    """
    Compare two test runs and identify changes.
    
    Returns:
        Dict with new failures, fixed tests, and status changes
    """
    current_failures = set(
        f"{t['feature']}-{t['scenario']}" 
        for t in current_results['failed_tests']
    )
    previous_failures = set(
        f"{t['feature']}-{t['scenario']}" 
        for t in previous_results['failed_tests']
    )
    
    new_failures = current_failures - previous_failures
    fixed_tests = previous_failures - current_failures
    
    pass_rate_change = current_results['pass_rate'] - previous_results['pass_rate']
    
    return {
        'new_failures': list(new_failures),
        'fixed_tests': list(fixed_tests),
        'pass_rate_change': round(pass_rate_change, 2),
        'status': 'improved' if pass_rate_change > 0 else 'degraded'
    }
```

### Screenshot Gallery

**Generate HTML Gallery from Failed Test Screenshots:**

```python
"""
Create HTML gallery of failure screenshots.
"""

from pathlib import Path
from jinja2 import Template

GALLERY_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Failure Screenshots</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .screenshot { border: 1px solid #ccc; padding: 10px; }
        .screenshot img { width: 100%; height: auto; }
        .screenshot-title { font-weight: bold; margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>Test Failure Screenshots</h1>
    <div class="gallery">
    {% for screenshot in screenshots %}
        <div class="screenshot">
            <div class="screenshot-title">{{ screenshot.title }}</div>
            <img src="{{ screenshot.path }}" alt="{{ screenshot.title }}">
            <div>{{ screenshot.timestamp }}</div>
        </div>
    {% endfor %}
    </div>
</body>
</html>
"""

def generate_screenshot_gallery(screenshots_dir: Path, output_file: Path):
    """Generate HTML gallery of screenshots."""
    screenshots = []
    
    for img_file in screenshots_dir.glob('*.png'):
        screenshots.append({
            'title': img_file.stem.replace('_', ' '),
            'path': img_file.name,
            'timestamp': img_file.stat().st_mtime
        })
    
    template = Template(GALLERY_TEMPLATE)
    html = template.render(screenshots=screenshots)
    
    output_file.write_text(html)
    print(f"Generated screenshot gallery: {output_file}")
```

### Integration with Test Management Systems

**TestRail Integration:**

```python
"""
Push test results to TestRail test management system.
"""

import requests
from typing import Dict, List

class TestRailClient:
    """Client for TestRail API integration."""
    
    def __init__(self, base_url: str, username: str, api_key: str):
        self.base_url = base_url
        self.auth = (username, api_key)
    
    def add_test_results(self, run_id: int, test_results: List[Dict]):
        """
        Submit test results to TestRail run.
        
        Args:
            run_id: TestRail test run ID
            test_results: List of test results
        """
        url = f"{self.base_url}/index.php?/api/v2/add_results_for_cases/{run_id}"
        
        # Format results for TestRail API
        results = {
            "results": [
                {
                    "case_id": result['case_id'],
                    "status_id": 1 if result['status'] == 'passed' else 5,
                    "comment": result.get('comment', ''),
                    "elapsed": f"{result['duration']}s"
                }
                for result in test_results
            ]
        }
        
        response = requests.post(url, json=results, auth=self.auth)
        response.raise_for_status()
        
        return response.json()
```

**Source:** Advanced patterns from industry best practices and requirements analysis

## Troubleshooting

### Report Generation Failures

**Issue: Behave HTML Report Not Generated**

**Symptoms:**
- Expected HTML report file missing
- behave command completes but no HTML output

**Causes:**
- HTML formatter not installed
- Incorrect format specification in behave.ini
- Output directory doesn't exist

**Solution:**

```bash
# Install HTML formatter
pip install behave-html-formatter

# Verify behave.ini configuration
# Ensure line exists:
# format = html:reports/behave-report.html

# Create output directory
mkdir -p reports

# Run with explicit format
behave --format html --outfile reports/behave-report.html
```

**Issue: JSON Report Empty or Malformed**

**Symptoms:**
- JSON file exists but empty
- JSON parsing errors

**Causes:**
- Test execution interrupted
- Multiple processes writing to same file
- Disk space full

**Solution:**

```bash
# Check disk space
df -h

# Use unique output files for parallel execution
behave --format json --outfile reports/report-${BUILD_NUMBER}.json

# Validate JSON after generation
python -m json.tool reports/report.json
```

### Missing Screenshots in Reports

**Issue: Screenshots Not Appearing in HTML/Allure Reports**

**Symptoms:**
- Screenshot files exist in directory
- Reports don't display screenshots

**Causes:**
- Relative path mismatch
- Screenshots not attached to Allure report
- Incorrect permissions

**Solution:**

```python
# In environment.py after_step hook
def after_step(context, step):
    if step.status == 'failed':
        screenshot_path = capture_screenshot(
            context.driver, 
            f"failure_{step.name}"
        )
        
        # Attach to Allure report
        if screenshot_path:
            with open(screenshot_path, 'rb') as f:
                allure.attach(
                    f.read(),
                    name=f"failure_{step.name}",
                    attachment_type=allure.attachment_type.PNG
                )
```

### Allure History Not Appearing

**Issue: Allure Report Shows No Historical Trends**

**Symptoms:**
- Allure report generates but no trend graphs
- "Trends" section empty

**Causes:**
- allure-results/history not preserved between runs
- History directory not copied

**Solution:**

```bash
# Before generating new report, copy history from previous report
mkdir -p reports/allure-results/history
cp -r reports/allure-report/history/* reports/allure-results/history/ 2>/dev/null || true

# Generate report with history
allure generate reports/allure-results --clean -o reports/allure-report
```

**Docker Persistent History:**

```dockerfile
# In Dockerfile
VOLUME ["/app/reports/allure-results/history"]

# In docker-compose.yml
volumes:
  - allure-history:/app/reports/allure-results/history

volumes:
  allure-history:
```

### Permissions Errors on Hosting Platforms

**Issue: 403 Forbidden on S3/Azure/GCS**

**Symptoms:**
- Reports upload successfully
- HTTP 403 when accessing URLs

**Causes:**
- Bucket/container not public
- Missing public read policy
- CORS configuration missing

**Solution for AWS S3:**

```bash
# Make bucket public
aws s3api put-public-access-block \
    --bucket test-reports-bucket \
    --public-access-block-configuration \
    BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false

# Add bucket policy
aws s3api put-bucket-policy \
    --bucket test-reports-bucket \
    --policy file://public-read-policy.json
```

### CDN Cache Issues

**Issue: Old Reports Showing After Update**

**Symptoms:**
- New reports published
- Old version displays in browser
- CDN serving stale content

**Causes:**
- CloudFront/CDN caching
- Browser cache
- Aggressive cache headers

**Solution:**

```bash
# Invalidate CloudFront cache
aws cloudfront create-invalidation \
    --distribution-id E1234EXAMPLE \
    --paths "/reports/*"

# Or invalidate everything
aws cloudfront create-invalidation \
    --distribution-id E1234EXAMPLE \
    --paths "/*"
```

**Set Cache Headers:**

```python
# When uploading to S3, set cache control
s3_client.upload_file(
    local_file,
    bucket_name,
    s3_key,
    ExtraArgs={
        'ContentType': 'text/html',
        'CacheControl': 'max-age=300'  # 5 minutes
    }
)
```

### Large Report Files Causing Upload Timeouts

**Issue: Report Upload Fails with Timeout**

**Symptoms:**
- Upload starts but times out
- Works for small reports, fails for large ones

**Causes:**
- Large screenshot files
- Network timeout too short
- Many test cases in single report

**Solution:**

```python
# Compress screenshots before including in report
from PIL import Image

def compress_screenshot(input_path: str, output_path: str, quality: int = 75):
    """Compress screenshot to reduce file size."""
    img = Image.open(input_path)
    img.save(output_path, 'JPEG', quality=quality, optimize=True)

# Increase upload timeout
s3_client = boto3.client(
    's3',
    config=Config(
        connect_timeout=300,
        read_timeout=300
    )
)

# Use multipart upload for large files
s3_client.upload_file(
    large_file,
    bucket,
    key,
    Config=TransferConfig(
        multipart_threshold=1024 * 25,  # 25 MB
        max_concurrency=10
    )
)
```

**Source:** `README.md:602-714` troubleshooting patterns, expanded with deployment-specific scenarios

## See Also

- [Local Development Setup](local-development.md) - Setting up reports locally
- [Jenkins Integration](jenkins-integration.md) - CI/CD report publishing
- [GitHub Actions](github-actions.md) - Automated deployment workflows
- [Docker Deployment](docker.md) - Containerized report generation
- [Configuration Reference](../reference/configuration-options.md) - Report configuration options

**Source:** `README.md:467-514`, `behave.ini:1-92`, `config/config.yaml:1-37`

