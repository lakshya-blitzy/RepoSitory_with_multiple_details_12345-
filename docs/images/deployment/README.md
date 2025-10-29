# Deployment Images Directory

## Purpose

This directory stores deployment-related screenshots and images used throughout the deployment documentation guides located in `docs/deployment/`. These visual assets help illustrate CI/CD pipeline configurations, cloud provider setups, container deployments, and report publishing workflows.

All images in this directory support the comprehensive deployment documentation covering local development, Docker, Kubernetes, CI/CD platforms (Jenkins, GitHub Actions, GitLab CI, Azure DevOps), and cloud providers (AWS, Azure, GCP).

**Reference:** Image management standards defined in Agent Action Plan section 0.4

---

## Image Categories

### CI/CD Pipeline Screenshots

Screenshots demonstrating continuous integration and deployment pipeline configurations:

- **Jenkins Dashboard**: Pipeline execution views, build status displays, stage visualization, console output examples
- **GitHub Actions**: Workflow run pages, action logs, matrix build results, artifact publishing
- **GitLab CI**: Pipeline overview, job execution details, stage progression, CI/CD variables configuration
- **Azure DevOps**: Pipeline runs, release stages, test task outputs, artifact management

**Example files:**
- `jenkins-pipeline-success.png`
- `github-actions-workflow-matrix.png`
- `gitlab-ci-pipeline-stages.png`
- `azure-devops-test-results.png`

### Cloud Provider Screenshots

Screenshots showing cloud platform deployment configurations and monitoring:

- **AWS (Amazon Web Services)**: 
  - EC2 instance configuration for test execution
  - ECS task definitions for containerized tests
  - Lambda function setup for report processing
  - CloudWatch logs and metrics
  
- **Azure (Microsoft Azure)**:
  - Virtual Machine configuration for test runners
  - Container Instances deployment settings
  - App Service configuration for report hosting
  - Azure Monitor dashboards

- **GCP (Google Cloud Platform)**:
  - Compute Engine VM setup for test execution
  - Cloud Run service configuration for containerized tests
  - Container Registry image management
  - Cloud Logging and monitoring

**Example files:**
- `aws-ec2-deployment-config.png`
- `aws-ecs-task-definition.png`
- `azure-vm-test-runner-setup.png`
- `azure-container-instances-config.png`
- `gcp-compute-engine-instance.png`
- `gcp-cloud-run-deployment.png`

### Container Deployment

Screenshots illustrating container orchestration and deployment:

- **Kubernetes Dashboard**: Pod status displays, deployment configurations, service definitions, resource monitoring
- **Docker**: Container deployment commands, running containers list, container logs, image management

**Example files:**
- `kubernetes-dashboard-pods.png`
- `kubernetes-deployment-status.png`
- `docker-container-running.png`
- `docker-compose-services.png`

### Report Publishing Examples

Screenshots demonstrating test report generation and publishing across different environments:

- HTML report examples in various CI/CD platforms
- Allure report dashboards and hosting configurations
- JUnit report integration with CI tools
- Custom report publishing workflows

**Example files:**
- `allure-report-dashboard.png`
- `jenkins-html-report-published.png`
- `github-pages-report-hosting.png`
- `s3-hosted-reports.png`

---

## Naming Convention Standards

### Format Requirements

All image files must follow the **descriptive-kebab-case** naming pattern:

```
<platform-or-tool>-<specific-feature-or-view>-<context>.png
```

### Naming Rules

1. **Use lowercase only**: No uppercase letters or camelCase
2. **Separate words with hyphens**: Use `-` between words, not underscores or spaces
3. **Be descriptive**: Name should clearly indicate the content without viewing the image
4. **Include platform/tool name**: Start with the relevant technology (jenkins, aws, kubernetes, etc.)
5. **Add context**: Include what the screenshot shows (config, status, dashboard, etc.)
6. **Keep concise**: Aim for 3-5 words maximum

### Naming Examples

#### ✅ Good Naming Examples

| Filename | Why It's Good |
|----------|---------------|
| `jenkins-pipeline-success.png` | Clear platform, shows successful pipeline |
| `aws-ec2-deployment-config.png` | Platform (AWS), service (EC2), context (deployment config) |
| `kubernetes-pod-status-running.png` | Platform, resource type, status |
| `github-actions-workflow-matrix.png` | Platform, feature type, specific view |
| `allure-report-dashboard.png` | Tool, artifact type, view |
| `docker-compose-services-up.png` | Tool, command context, status |

#### ❌ Poor Naming Examples

| Filename | Why It's Poor | Better Alternative |
|----------|---------------|-------------------|
| `Screenshot_2024_01_15.png` | No context, generic timestamp | `jenkins-build-status-2024-01.png` |
| `image1.png` | Completely non-descriptive | `aws-lambda-configuration.png` |
| `K8S_Dashboard.png` | Uses abbreviation, mixed case | `kubernetes-dashboard-overview.png` |
| `JenkinsConfig.png` | camelCase instead of kebab-case | `jenkins-configuration.png` |
| `my_screenshot.png` | Uses underscores, too generic | `gitlab-ci-pipeline-view.png` |
| `temp.png` | Temporary name, no context | `azure-vm-instance-details.png` |

---

## Technical Requirements

### Image Format

- **Primary Format**: PNG (Portable Network Graphics)
  - Lossless compression preserves screenshot quality
  - Supports transparency for annotations
  - Wide browser compatibility

- **Alternative Formats** (use sparingly):
  - SVG for custom diagrams (use Mermaid in documentation when possible)
  - JPEG only if file size is critical and quality loss acceptable

### Resolution Standards

- **Minimum Resolution**: High-DPI (2x scaling or 300 DPI)
  - Ensures clarity on high-resolution displays
  - Maintains readability when scaled
  - Prevents pixelation in documentation

- **Recommended Capture Settings**:
  - Use Retina/HiDPI display for captures
  - Capture at 2x native resolution
  - Ensure text is crisp and readable

### File Size Management

- **Target Size**: < 500 KB per image (preferred)
- **Maximum Size**: < 2 MB per image
- **Optimization Required**: If image exceeds 2 MB

**Optimization Techniques**:
1. Crop to show only relevant portions
2. Use PNG optimization tools (OptiPNG, TinyPNG)
3. Remove unnecessary UI chrome (browser tabs, OS elements)
4. Consider reducing color depth if appropriate
5. Remove metadata (EXIF data)

**Optimization Tools**:
```bash
# OptiPNG (lossless PNG optimization)
optipng -o7 image-name.png

# ImageMagick (resize if needed)
convert image-name.png -resize 50% image-name-optimized.png

# pngquant (lossy but high quality)
pngquant --quality=80-95 image-name.png
```

### Image Cropping Guidelines

- **Crop tightly**: Show only the relevant UI portion
- **Remove distractions**: Exclude personal information, unrelated UI elements
- **Maintain context**: Keep enough surrounding UI for orientation
- **Focus attention**: Crop to highlight the specific feature being documented

---

## Usage Guidelines

### Referencing Images in Documentation

#### Relative Path Format

From deployment guide documents in `docs/deployment/`, reference images using:

```markdown
![Alt text description](../../images/deployment/image-name.png)
```

**Path breakdown**:
- `../../` navigates up two levels from `docs/deployment/` to repository root
- `images/deployment/` navigates to this directory
- `image-name.png` the specific image file

#### Alt Text Requirements

Always provide **descriptive alt text** for accessibility:

**✅ Good alt text examples**:
```markdown
![Jenkins pipeline showing successful test execution with 5 stages completed](../../images/deployment/jenkins-pipeline-success.png)

![AWS EC2 instance configuration page with t3.medium instance type selected](../../images/deployment/aws-ec2-deployment-config.png)

![Kubernetes dashboard displaying 3 running pods in the test namespace](../../images/deployment/kubernetes-pod-status-running.png)
```

**❌ Poor alt text examples**:
```markdown
![screenshot](../../images/deployment/jenkins.png)
![image](../../images/deployment/aws.png)
![](../../images/deployment/kubernetes.png)  <!-- No alt text -->
```

### Image Annotations

When screenshots require additional clarification:

1. **Use annotation tools** to highlight specific features:
   - Red boxes/arrows to draw attention
   - Numbered callouts for step-by-step guides
   - Blurred sections to redact sensitive information

2. **Annotation best practices**:
   - Keep annotations minimal and clear
   - Use consistent colors (red for important, blue for info)
   - Ensure annotations don't obscure critical information
   - Save annotated version with `-annotated` suffix if keeping both

3. **Example**:
   ```
   aws-ec2-config.png               (original screenshot)
   aws-ec2-config-annotated.png     (version with arrows/boxes)
   ```

### Keeping Images Current

- **Review quarterly**: Check if UI has changed significantly
- **Update with major version changes**: When documented tools release major updates
- **Document update dates**: Note in deployment guide when screenshots were last updated
- **Archive outdated images**: Move to `archived/` subdirectory rather than deleting

**Version tracking example** (in deployment guide):
```markdown
> **Note**: Screenshots updated January 2024 for Jenkins 2.440, GitHub Actions UI v2, AWS Console 2024 version.
```

---

## Organization Tips

### Current Structure

```
docs/images/deployment/
├── README.md                          (this file)
├── jenkins-pipeline-success.png
├── jenkins-build-status.png
├── aws-ec2-deployment-config.png
├── azure-vm-test-runner-setup.png
├── kubernetes-dashboard-pods.png
└── docker-container-running.png
```

### Scaling for Growth

As the number of images increases, consider organizing into subdirectories:

#### Option 1: By Platform/Tool

```
docs/images/deployment/
├── README.md
├── jenkins/
│   ├── pipeline-success.png
│   ├── build-status.png
│   └── plugin-config.png
├── aws/
│   ├── ec2-deployment-config.png
│   ├── ecs-task-definition.png
│   └── lambda-configuration.png
├── azure/
│   └── vm-test-runner-setup.png
├── kubernetes/
│   ├── dashboard-pods.png
│   └── deployment-status.png
└── docker/
    └── container-running.png
```

**Path update**: `../../images/deployment/jenkins/pipeline-success.png`

#### Option 2: By Deployment Type

```
docs/images/deployment/
├── README.md
├── cicd/
│   ├── jenkins-pipeline-success.png
│   ├── github-actions-workflow.png
│   └── gitlab-ci-pipeline.png
├── cloud/
│   ├── aws-ec2-config.png
│   ├── azure-vm-setup.png
│   └── gcp-compute-instance.png
├── containers/
│   ├── kubernetes-dashboard.png
│   └── docker-compose-services.png
└── reports/
    ├── allure-report-dashboard.png
    └── html-report-published.png
```

### Documentation of Structure Changes

**If subdirectories are created**, update this README with:
1. Clear directory structure tree
2. Updated path examples in usage section
3. Guidelines for which images go in which subdirectory
4. Migration notes if moving existing images

---

## Update Triggers

### When to Add/Update Images

1. **New Deployment Guides**
   - Add screenshots when authoring new deployment documentation
   - Capture key configuration screens and successful deployments
   - Document any unusual or complex UI interactions

2. **Tool/Platform UI Changes**
   - Update screenshots when CI/CD tools undergo major UI redesigns
   - Replace outdated images when they no longer match current interface
   - Document UI version in deployment guide

3. **New Platform Documentation**
   - Add comprehensive screenshots when documenting new deployment targets
   - Capture end-to-end deployment flow
   - Include both configuration and verification screens

4. **Quality Improvements**
   - Replace low-resolution images with high-DPI versions
   - Improve cropping to better focus on relevant content
   - Add annotations when user feedback indicates confusion
   - Optimize oversized images

5. **Security/Privacy**
   - Replace images containing sensitive information
   - Update screenshots that expose credentials or internal URLs
   - Redact or blur private data in existing images

### Maintenance Schedule

- **Quarterly Review** (Every 3 months):
  - Audit all images for outdated UI
  - Check file sizes and optimize if needed
  - Verify all images are still referenced in documentation
  - Remove orphaned images no longer in use

- **With Major Version Updates**:
  - Review deployment tool versions documented
  - Update screenshots for significant UI changes
  - Note version compatibility in deployment guides

---

## Current Status

### Project Scope Notes

Per the project requirements (Agent Action Plan section 0.3):

- ✅ **Documentation Structure**: This directory structure is established and ready
- ✅ **Guidelines**: Comprehensive image management guidelines provided
- ⚠️ **Actual Deployment Setup**: Out of scope for current documentation project
- 📋 **Screenshot Addition**: Images will be added progressively as deployment guides are authored

### Expected Growth

As the deployment documentation is created (13 deployment guides planned):

1. **docs/deployment/jenkins-integration.md** → Jenkins pipeline screenshots
2. **docs/deployment/github-actions.md** → GitHub Actions workflow screenshots
3. **docs/deployment/gitlab-ci.md** → GitLab CI pipeline screenshots
4. **docs/deployment/azure-devops.md** → Azure DevOps screenshots
5. **docs/deployment/docker.md** → Docker deployment screenshots
6. **docs/deployment/kubernetes.md** → Kubernetes dashboard screenshots
7. **docs/deployment/aws.md** → AWS console screenshots
8. **docs/deployment/azure.md** → Azure portal screenshots
9. **docs/deployment/gcp.md** → GCP console screenshots
10. **docs/deployment/report-publishing.md** → Report hosting screenshots

### Placeholder Status

This directory serves as the organizational foundation for deployment imagery. Images will be populated by documentation authors following these guidelines.

**Documentation Team**: When adding images, please:
1. Follow the naming conventions strictly
2. Optimize images before committing
3. Provide descriptive alt text in documentation
4. Update this README if creating subdirectories

---

## Related Documentation

### Deployment Guides (docs/deployment/)

Once created, these guides will reference images from this directory:

- [Jenkins Integration](../../../deployment/jenkins-integration.md) - CI/CD pipeline setup
- [GitHub Actions](../../../deployment/github-actions.md) - Workflow configuration
- [GitLab CI](../../../deployment/gitlab-ci.md) - Pipeline setup
- [Azure DevOps](../../../deployment/azure-devops.md) - Pipeline configuration
- [Docker Deployment](../../../deployment/docker.md) - Container setup
- [Kubernetes Deployment](../../../deployment/kubernetes.md) - Orchestration configuration
- [AWS Deployment](../../../deployment/aws.md) - Cloud infrastructure
- [Azure Deployment](../../../deployment/azure.md) - Cloud infrastructure
- [GCP Deployment](../../../deployment/gcp.md) - Cloud infrastructure
- [Report Publishing](../../../deployment/report-publishing.md) - Test report hosting

### Documentation Standards

- [Agent Action Plan Section 0.4](../../../../blitzy/documentation/Project%20Guide.md) - Image management standards
- [Documentation Guidelines](../../../contributing/documentation-guidelines.md) - Overall documentation standards
- [Screenshot Best Practices](#technical-requirements) - This document's technical requirements

---

## Quick Reference

### Image Checklist for Contributors

Before committing deployment images, verify:

- [ ] Filename follows `descriptive-kebab-case.png` pattern
- [ ] Platform/tool name is in the filename
- [ ] File size is under 2MB (preferably under 500KB)
- [ ] Image is high-resolution (2x/300 DPI)
- [ ] Cropped to show only relevant content
- [ ] Personal/sensitive information removed or redacted
- [ ] Alt text is descriptive and accessible
- [ ] Referenced correctly in deployment guide
- [ ] Image format is PNG (preferred)
- [ ] Optimized with OptiPNG or similar tool

### Common Commands

```bash
# Check image dimensions and size
file image-name.png
identify image-name.png  # requires ImageMagick

# Optimize PNG
optipng -o7 image-name.png

# Batch optimize all PNGs in directory
find . -name "*.png" -exec optipng -o7 {} \;

# Check file sizes
du -h *.png | sort -h

# Find large images (>1MB)
find . -name "*.png" -size +1M -exec ls -lh {} \;
```

---

## Questions or Issues?

If you have questions about deployment image management:

1. **Naming Convention**: Review [Naming Convention Standards](#naming-convention-standards)
2. **File Size**: Follow [Technical Requirements](#technical-requirements) optimization guide
3. **Organization**: See [Organization Tips](#organization-tips) for structure guidance
4. **Documentation**: Reference the [Agent Action Plan](../../../../blitzy/documentation/Project%20Guide.md)

For additional assistance, refer to the [Contributing Documentation Guidelines](../../../contributing/documentation-guidelines.md) or open an issue in the project repository.

---

**Last Updated**: Documentation structure established as part of comprehensive documentation enhancement project (Section 0 - Agent Action Plan).

**Maintained By**: Documentation team following guidelines in `docs/contributing/documentation-guidelines.md`.
