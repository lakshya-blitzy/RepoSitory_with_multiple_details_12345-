# Pull Request Process

This guide covers the complete pull request (PR) workflow for contributing to the Testinium QA Python test automation framework, from initial setup through merge.

## Overview

The pull request process ensures code quality, maintainability, and consistency across the framework. Our workflow follows these stages:

1. **Fork & Branch** - Create a feature branch from an up-to-date fork
2. **Develop** - Implement changes following our code standards
3. **Test** - Ensure all tests pass and coverage is maintained
4. **Document** - Update documentation for your changes
5. **PR Creation** - Submit a comprehensive pull request
6. **Review** - Collaborate with maintainers through code review
7. **Merge** - Integrate approved changes into main branch

**Expected Timeline:**
- Initial PR submission: ~1-2 hours (depending on change complexity)
- Review turnaround: Within 2 business days
- Total time to merge: 3-5 business days for most PRs

## Before You Start

### Prerequisites

Before beginning development, ensure you have:

1. **Read the Documentation:**
   - [Development Setup Guide](development-setup.md) - Development environment configuration
   - [Code Style Guide](code-style-guide.md) - Coding standards and conventions
   - [Testing Guidelines](testing-guidelines.md) - Test requirements and patterns
   - [Documentation Guidelines](documentation-guidelines.md) - Documentation standards

2. **Check Existing Work:**
   - Search [existing issues](https://github.com/testinium/testinium-qa-python/issues) to avoid duplication
   - Review [open pull requests](https://github.com/testinium/testinium-qa-python/pulls) for related work
   - Check [project board](https://github.com/testinium/testinium-qa-python/projects) for planned features

3. **Discuss Major Changes:**
   - For significant features or refactoring, open an issue first
   - Discuss approach and get maintainer feedback before implementing
   - This prevents wasted effort on changes that may not be accepted

4. **Development Environment Ready:**
   - Python 3.9+ installed and configured
   - Virtual environment created and activated
   - All dependencies installed (`pip install -r requirements.txt`)
   - All tests passing locally (`pytest tests/ && behave`)
   - Code quality tools installed (`pip install -r requirements-dev.txt`)

**Source:** `README.md:740-750`

## Branch Naming Conventions

Use descriptive branch names that clearly indicate the purpose of your changes. Follow these patterns:

### Branch Naming Patterns

| Branch Type | Pattern | Example |
|-------------|---------|---------|
| **New Feature** | `feature/description` | `feature/parallel-execution-enhancement` |
| **Bug Fix** | `bugfix/issue-number-description` | `bugfix/123-firefox-driver-crash` |
| **Documentation** | `docs/topic` | `docs/api-reference-utilities` |
| **Refactoring** | `refactor/component` | `refactor/driver-manager-cleanup` |
| **Tests** | `test/component` | `test/config-reader-unit-tests` |
| **Hotfix** | `hotfix/issue-description` | `hotfix/login-timeout-error` |

### Branch Naming Rules

- Use **lowercase** with **hyphens** as separators
- Keep names **concise** but **descriptive** (3-5 words)
- Include **issue number** when fixing a reported bug
- **Avoid** special characters, spaces, or underscores
- Use **present tense** for features (`add-` not `added-`)

### Good Branch Names ✓

```bash
feature/allure-report-integration
bugfix/287-stale-element-crm-page
docs/deployment-kubernetes-guide
refactor/wait-helpers-consolidation
test/employee-page-crud-operations
```

### Bad Branch Names ✗

```bash
fix                           # Too vague
feature/New_Feature          # Wrong case and underscores
my-branch                    # Not descriptive
update                       # Too generic
feature/add-really-cool-new-feature-that-does-many-things  # Too long
```

**Source:** Git branching best practices, `README.md:743`

## Development Workflow

Follow this workflow when implementing your changes:

### 1. Create Feature Branch

Start from an up-to-date main branch:

```bash
# Sync your fork with upstream
git checkout main
git pull upstream main
git push origin main

# Create and switch to feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Focused Changes

- **One feature or fix per PR** - Don't combine unrelated changes
- **Keep commits atomic** - Each commit should be a logical unit of work
- **Commit frequently** - Small, incremental commits are easier to review
- **Test as you go** - Run tests after each significant change

### 3. Follow Code Standards

All code must comply with project standards:

- **Black formatting** - 100 character line length
- **isort** - Organized imports with Black profile
- **pylint** - Code quality score ≥ 8.0/10
- **mypy** - Type hints on all function signatures
- **PEP 8** - Python style guide compliance

See [Code Style Guide](code-style-guide.md) for complete requirements.

**Source:** `pyproject.toml:93-173`, `README.md:744-747`

### 4. Write/Update Tests

Maintain comprehensive test coverage:

- **Unit tests** for utilities, config, and page objects
- **Integration tests** for step definitions if applicable
- **Maintain 90%+ coverage** for core packages (utilities, pages, config)
- **Test edge cases** and error conditions
- **Update existing tests** if behavior changes

See [Testing Guidelines](testing-guidelines.md) for test requirements.

**Source:** `pyproject.toml:174-194`, `README.md:745`

### 5. Update Documentation

Keep documentation synchronized with code:

- **API documentation** for new functions and classes
- **User guides** for new features
- **Inline docstrings** following Google style
- **README updates** if setup or configuration changes
- **CHANGELOG entry** for user-facing changes

See [Documentation Guidelines](documentation-guidelines.md) for standards.

**Source:** `README.md` documentation sections

### 6. Commit Changes

Commit incrementally with clear messages:

```bash
# Stage changes
git add path/to/changed/files

# Commit with descriptive message
git commit -m "feat: add parallel execution support for behave tests"

# Push to your fork
git push origin feature/your-feature-name
```

## Commit Message Standards

We follow [Conventional Commits](https://www.conventionalcommits.org/) for clear, semantic commit history.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| **feat** | New feature | `feat(pages): add inventory page object with CRUD operations` |
| **fix** | Bug fix | `fix(driver): resolve firefox driver crash on parallel execution` |
| **docs** | Documentation changes | `docs(api): add wait-helpers API reference with examples` |
| **test** | Test additions or modifications | `test(config): add unit tests for configuration precedence` |
| **refactor** | Code refactoring (no functional change) | `refactor(wait): consolidate wait helper methods in base page` |
| **style** | Code style changes (formatting, etc.) | `style: apply black formatting to pages package` |
| **chore** | Maintenance tasks | `chore: update selenium to 4.16.0` |
| **perf** | Performance improvements | `perf(driver): optimize driver initialization for parallel tests` |
| **ci** | CI/CD changes | `ci: add github actions workflow for documentation deployment` |

### Commit Message Rules

1. **Type is required** - Must be one of the types above
2. **Scope is optional** - Specify affected component (pages, utilities, config, etc.)
3. **Subject line:**
   - Use imperative mood ("add" not "added" or "adds")
   - Don't capitalize first letter
   - No period at the end
   - Maximum 50 characters
   - Clearly describe what the commit does

4. **Body (optional but recommended for complex changes):**
   - Explain the what and why, not the how
   - Wrap at 72 characters
   - Separate from subject with blank line
   - Use bullet points for multiple items

5. **Footer (optional):**
   - Reference issues: `Fixes #123`, `Closes #456`, `Ref #789`
   - Note breaking changes: `BREAKING CHANGE: description`

### Good Commit Messages ✓

```bash
feat(utilities): add screenshot capture on test failure

Implements automatic screenshot capture in environment.py after_scenario
hook. Screenshots are saved to reports/screenshots/ directory with
timestamped filenames.

- Capture browser logs in addition to screenshot
- Sanitize filenames to prevent path traversal issues
- Integrate with Allure for report attachment

Fixes #287
```

```bash
fix(pages): prevent stale element exception in crm page

Added explicit wait for element staleness before re-finding elements.
This resolves intermittent failures when CRM page elements are
dynamically reloaded during workflow operations.

The Java version had similar issues resolved in CrmPage.java:145.

Fixes #342
```

```bash
docs(deployment): add kubernetes deployment guide

Complete guide covering deployment.yaml configuration, ConfigMap setup,
Secrets management, and parallel execution with Job resources.

Ref #298
```

### Bad Commit Messages ✗

```bash
update code                    # Too vague
Fixed bug                      # Not descriptive, wrong tense
Added new feature.             # Generic, has period
FEAT: UPDATE LOGIN PAGE        # Wrong case
WIP                           # Not semantic
```

**Source:** Conventional Commits specification, Java migration commit history

## Pre-PR Checklist

Before creating your pull request, verify all items in this checklist:

### ✓ All Tests Pass

Run the complete test suite locally:

```bash
# Unit tests with pytest
pytest tests/ -v
Expected: All tests pass, no failures

# BDD feature validation (dry run)
behave --dry-run
Expected: All steps have definitions, no undefined steps

# BDD feature tests (if applicable to your changes)
behave
Expected: All scenarios pass (or affected scenarios if using tags)
```

**Source:** `README.md:746`, `pytest.ini:1-131`, `behave.ini:1-200`

### ✓ Code Quality Checks Pass

Run all code quality tools:

```bash
# Black formatting check
black --check .
Expected: "All done! ✨ 🍰 ✨"

# isort import ordering check
isort --check-only .
Expected: No import order issues

# pylint code quality analysis
pylint utilities/ pages/ config/ features/
Expected: Score ≥ 8.0/10, no critical issues

# mypy type checking
mypy utilities/ pages/ config/
Expected: No type errors
```

**Fix any issues before proceeding:**

```bash
# Auto-fix formatting
black .
isort .

# Address pylint and mypy errors manually
```

**Source:** `pyproject.toml:93-173`, `README.md:747`

### ✓ Code Coverage Maintained

Ensure test coverage meets standards:

```bash
# Run tests with coverage
pytest --cov=utilities --cov=pages --cov=config --cov-report=term-missing

# Coverage requirements:
# - utilities/: 90%+
# - pages/: 90%+
# - config/: 90%+
```

**If coverage drops:**
- Add tests for new code
- Ensure all branches are tested
- Test error conditions and edge cases

**Source:** `pyproject.toml:174-194`

### ✓ Documentation Updated

Verify documentation is complete:

- [ ] **API Documentation:** Docstrings added for new functions, classes, methods
- [ ] **User Guides:** Updated or created for new features
- [ ] **Inline Comments:** Complex logic has explanatory comments
- [ ] **README Updates:** Setup or configuration changes reflected
- [ ] **CHANGELOG Entry:** User-facing changes documented

**Docstring Requirements:**
- Module-level docstring explaining purpose
- Class docstrings with attributes and usage
- Method docstrings with Args, Returns, Raises, Example sections
- Follow Google-style Python docstrings

**Source:** Google Python Style Guide, existing docstrings in `utilities/driver_manager.py`

### ✓ No Secrets or Credentials

Security verification:

```bash
# Check for accidentally committed secrets
git diff main...HEAD | grep -i "password\|secret\|key\|token"

# Verify .env is not committed
git status | grep "\.env$"
Expected: .env should not appear (only .env.example is version controlled)
```

**If secrets found:**
- Remove from commits using `git rebase` or `git filter-branch`
- Rotate compromised credentials immediately
- Update .gitignore if needed

### ✓ Changelog Updated

For user-facing changes, add CHANGELOG entry:

```markdown
## [Unreleased]

### Added
- Parallel execution support for Behave scenarios (#287)
- Kubernetes deployment guide in documentation

### Fixed
- Stale element exception in CRM page workflows (#342)
- Firefox driver crash during parallel test execution (#356)

### Changed
- Upgraded Selenium from 4.15.2 to 4.16.0
```

**Source:** Keep a Changelog format

## Creating the Pull Request

Once your pre-PR checklist is complete, create your pull request:

### 1. Push Final Changes

```bash
# Ensure all commits are pushed
git push origin feature/your-feature-name
```

### 2. Open Pull Request

Navigate to your fork on GitHub and click "Compare & pull request"

### 3. Write Descriptive Title

Follow conventional commit format:

- ✓ `feat(pages): add inventory page object with CRUD operations`
- ✓ `fix(driver): resolve firefox driver crash on parallel execution`
- ✓ `docs(deployment): add kubernetes deployment guide`
- ✗ `Update code`
- ✗ `Bug fix`

### 4. Complete PR Description

Use the PR template to provide comprehensive information:

**What Changed:**
- Clear description of the changes made
- Why the changes were necessary
- Technical approach used

**Related Issues:**
- Link to related issues: `Fixes #123`, `Closes #456`, `Ref #789`
- Explain relationship to issue

**Testing Performed:**
- Unit tests added/updated
- Integration tests verified
- Manual testing scenarios
- Browser/environment tested

**Breaking Changes:**
- List any breaking changes
- Migration guide if applicable
- Deprecation warnings added

**Screenshots (if UI changes):**
- Before/after comparisons
- New UI elements
- Report examples

### 5. Use PR Template

Our repository includes a PR template (`.github/PULL_REQUEST_TEMPLATE.md`) that guides you through providing all necessary information:

```markdown
## Description

### What does this PR do?
Brief summary of changes in 2-3 sentences.

### Why is this change needed?
Explain the problem this PR solves or the feature it adds.

### Related Issues
- Fixes #123
- Ref #456

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Code refactoring (no functional changes)
- [ ] Test additions or modifications
- [ ] CI/CD changes
- [ ] Dependency updates

## Testing

### Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests verified
- [ ] All tests pass locally (`pytest tests/ && behave`)
- [ ] Coverage maintained at 90%+ for core packages

### Manual Testing
Describe manual testing performed:
- Browser(s) tested: Chrome, Firefox
- Operating system: macOS 14, Ubuntu 22.04
- Test scenarios executed: [list key scenarios]

## Code Quality

- [ ] Black formatting applied (`black .`)
- [ ] isort applied (`isort .`)
- [ ] pylint passes with score ≥ 8.0/10
- [ ] mypy type checking passes
- [ ] No pylint critical issues
- [ ] Code follows PEP 8 style guide

## Documentation

- [ ] Docstrings added/updated (Google style)
- [ ] API documentation updated
- [ ] User guides updated (if feature change)
- [ ] README updated (if setup/config changes)
- [ ] CHANGELOG updated (if user-facing changes)
- [ ] Inline comments added for complex logic

## Breaking Changes

### Does this PR introduce breaking changes?
- [ ] Yes
- [ ] No

If yes, describe breaking changes and migration path:

[Describe breaking changes here]

## Additional Context

### Screenshots (if applicable)
[Add screenshots here]

### Migration Notes (if applicable)
[Describe any migration steps needed]

### Performance Impact
[Describe any performance implications]

## Checklist

- [ ] I have read the [Code Style Guide](code-style-guide.md)
- [ ] I have read the [Testing Guidelines](testing-guidelines.md)
- [ ] I have read the [Documentation Guidelines](documentation-guidelines.md)
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published
- [ ] I have checked my code and corrected any misspellings
- [ ] I have not committed any secrets, passwords, or API keys
```

**Source:** GitHub PR best practices, project requirements

### 6. Request Reviewers

- **Tag relevant reviewers** based on the area of change
- **Add maintainers:** `@testinium-qa-team`
- **Domain experts:** For specific areas (e.g., Behave, Selenium, reporting)

### 7. Add Labels

Apply appropriate labels to help with categorization:

- `feature` - New feature implementation
- `bugfix` - Bug fix
- `documentation` - Documentation changes
- `test` - Test additions or improvements
- `refactor` - Code refactoring
- `breaking-change` - Breaking changes
- `needs-review` - Ready for review
- `wip` - Work in progress (not ready for review)

### 8. Link Related Issues

Use GitHub's issue linking:
- `Fixes #123` - Will auto-close issue when PR merges
- `Closes #456` - Will auto-close issue when PR merges
- `Ref #789` - Links to issue without closing

**Source:** GitHub documentation, `README.md:750`

## CI/CD Requirements

All pull requests must pass automated CI/CD checks before merge.

### Automated Checks

When you create a PR, the following checks run automatically:

#### 1. Test Suite Execution

```bash
# pytest unit tests
pytest tests/ -v -n auto
Required: All tests pass, no failures or errors
```

**Source:** `pytest.ini:1-131`

#### 2. Behave Feature Tests

```bash
# BDD feature validation
behave --dry-run
Required: All step definitions found

# Feature tests (if tagged scenarios exist)
behave --tags=@Smoke
Required: All smoke tests pass
```

**Source:** `behave.ini:1-200`

#### 3. Code Formatting Validation

```bash
# Black formatting check
black --check .
Required: All files properly formatted (line length 100)
```

**Source:** `pyproject.toml:93-112`

#### 4. Import Order Validation

```bash
# isort import ordering
isort --check-only .
Required: Imports organized according to Black profile
```

**Source:** `pyproject.toml:142-156`

#### 5. Code Quality Analysis

```bash
# pylint static analysis
pylint utilities/ pages/ config/ features/
Required: 
- Score ≥ 8.0/10
- No critical (C) or error (E) level issues
- Warnings (W) should be minimized
```

**Source:** `pyproject.toml:158-172`

#### 6. Type Checking

```bash
# mypy static type checking
mypy utilities/ pages/ config/
Required: No type errors for checked packages
```

**Source:** `pyproject.toml:114-140`

#### 7. Test Coverage

```bash
# Coverage analysis
pytest --cov=utilities --cov=pages --cov=config --cov-report=term-missing
Required:
- utilities/ ≥ 90% coverage
- pages/ ≥ 90% coverage  
- config/ ≥ 90% coverage
```

**Source:** `pyproject.toml:174-194`

### Build Artifacts

CI generates these artifacts for review:

- **Test Reports:** `reports/junit/*.xml` - JUnit XML test results
- **Coverage Report:** `reports/coverage/` - HTML coverage report
- **Allure Reports:** `reports/allure-results/` - Enhanced test reports (if applicable)
- **Screenshots:** `reports/screenshots/` - Failure screenshots (if tests failed)

### CI Failure Handling

If CI checks fail:

1. **Review CI Logs:**
   - Click "Details" next to failed check
   - Identify specific failures (test failures, linting issues, etc.)
   - Note the exact error messages

2. **Fix Issues Locally:**
   ```bash
   # Run the failing check locally
   pytest tests/ -v                    # If tests failed
   black .                              # If formatting failed
   isort .                              # If imports failed
   pylint utilities/ pages/ config/     # If linting failed
   mypy utilities/ pages/ config/       # If type checking failed
   ```

3. **Push Updates:**
   ```bash
   git add .
   git commit -m "fix: address CI failures"
   git push origin feature/your-feature-name
   ```

4. **Re-run Checks:**
   - CI automatically re-runs on new push
   - Alternatively, click "Re-run failed jobs" in GitHub Actions

5. **Seek Help if Stuck:**
   - Comment on PR describing the issue
   - Tag maintainers: `@testinium-qa-team`
   - Provide relevant logs and context

**Source:** CI/CD best practices, GitHub Actions workflows

## Code Review Process

All PRs require review and approval from at least one maintainer before merging.

### Review Criteria

Reviewers evaluate PRs based on:

#### Code Quality and Style

- **Follows code style guide:** Black formatting, PEP 8 compliance
- **Clear and readable:** Well-named variables, functions, classes
- **Proper structure:** Logical organization, appropriate abstraction
- **No code smells:** Duplicated code, overly complex methods, god objects
- **Efficient:** No obvious performance issues

**Source:** [Code Style Guide](code-style-guide.md), `pyproject.toml:93-172`

#### Test Coverage

- **Adequate test coverage:** New code is tested (≥90% coverage)
- **Meaningful tests:** Tests verify correct behavior, not just coverage
- **Edge cases tested:** Boundary conditions, error paths covered
- **Tests are maintainable:** Clear test names, good assertions

**Source:** [Testing Guidelines](testing-guidelines.md), `pyproject.toml:174-194`

#### Documentation Completeness

- **API documentation:** Docstrings for all public APIs
- **User guides updated:** New features have usage documentation
- **Clear comments:** Complex logic has explanatory comments
- **README updated:** Setup or configuration changes reflected

**Source:** [Documentation Guidelines](documentation-guidelines.md)

#### Security

- **No vulnerabilities:** No SQL injection, XSS, path traversal, etc.
- **No secrets committed:** Passwords, API keys, tokens are in .env or secrets management
- **Input validation:** User inputs are validated and sanitized
- **Dependencies secure:** No known vulnerabilities in dependencies

#### Thread Safety (For Parallel Execution)

- **WebDriver thread-local:** Uses `threading.local()` pattern in DriverManager
- **No shared mutable state:** Page objects don't share state between tests
- **Behave context safe:** Proper use of context object in step definitions
- **Fixtures properly scoped:** Pytest fixtures have appropriate scope

**Source:** `utilities/driver_manager.py:82-200`, `behave.ini:119-128`

#### Migration Equivalence (If Applicable)

- **Behavioral equivalence:** Python version matches Java functionality
- **Bug fixes applied:** Critical fixes from Java version are preserved
- **Pattern transformation:** Proper Python patterns (not direct Java translation)
- **Documentation cites Java:** Java equivalents referenced in docstrings

**Source:** `blitzy/documentation/Technical Specifications.md`

#### Performance Impact

- **No performance regressions:** New code doesn't slow down tests significantly
- **Efficient algorithms:** Appropriate data structures and algorithms used
- **Resource cleanup:** WebDriver, files, connections properly closed
- **Wait strategies:** Uses explicit waits (no sleep(), minimal implicit waits)

**Source:** `utilities/wait_helpers.py`, `pages/base_page.py`

### Reviewer Responsibilities

Reviewers should:

1. **Review Timely:** Respond within 2 business days
2. **Be Constructive:** Offer specific, actionable feedback
3. **Explain Reasoning:** Help author understand the why behind feedback
4. **Suggest Solutions:** Provide code examples or references when possible
5. **Approve When Ready:** Don't hold back approval for nitpicks
6. **Ask Questions:** Seek clarification on unclear implementations

### Author Responsibilities

As the PR author, you should:

1. **Address All Comments:** Respond to every review comment
2. **Ask for Clarification:** If feedback is unclear, ask questions
3. **Make Requested Changes:** Implement requested improvements
4. **Explain Decisions:** If you disagree with feedback, explain your reasoning
5. **Push Updates:** Push changes to the same branch (PR auto-updates)
6. **Resolve Conversations:** Mark conversations as resolved when addressed
7. **Re-request Review:** After updates, re-request review from reviewers

### Review Iterations

The review process is iterative:

1. **Initial Review:** Reviewer provides feedback
2. **Author Updates:** Author addresses comments and pushes changes
3. **Follow-up Review:** Reviewer checks updates
4. **Repeat:** Continue until all concerns addressed
5. **Approval:** Reviewer approves PR

**Typical iterations:** 1-3 rounds for most PRs

**Tips for faster reviews:**
- Respond to comments promptly (within 1-2 days)
- Make requested changes quickly
- Ask questions if stuck
- Keep PR scope focused (easier to review)

## Merge Process

Once your PR is approved and all checks pass, it can be merged.

### Pre-Merge Requirements

Before merging, verify:

- [ ] **At least 1 approval** from maintainer
- [ ] **All CI checks passing** (tests, linting, coverage)
- [ ] **No merge conflicts** with main branch
- [ ] **All review conversations resolved**
- [ ] **Final commit represents production-ready code**

### Merge Strategies

We use different merge strategies based on the type of PR:

#### Squash and Merge (Default for Feature Branches)

**When to use:** Most feature branches and bug fixes

**Benefits:**
- Clean, linear history on main branch
- One commit per feature/fix
- Easy to revert if needed

**How it works:**
```bash
# All commits in PR are squashed into single commit
git merge --squash feature/your-feature-name
```

**Commit message format:**
```
feat(pages): add inventory page object with CRUD operations (#287)

Complete implementation of inventory page object including:
- Add, edit, delete inventory item methods
- Search and filter functionality  
- Property-based locators for all elements
- Comprehensive docstrings with examples

Fixes #287
```

#### Regular Merge (For Release Branches)

**When to use:** Release branches, hotfixes, important merge commits

**Benefits:**
- Preserves commit history
- Shows individual commits
- Better for tracking complex changes

**How it works:**
```bash
git merge --no-ff release/1.1.0
```

### Merge Procedure

1. **Resolve Any Conflicts:**
   ```bash
   # Update your branch with latest main
   git checkout feature/your-feature-name
   git fetch upstream
   git merge upstream/main
   
   # Resolve conflicts
   # Edit conflicting files
   git add .
   git commit -m "merge: resolve conflicts with main"
   git push origin feature/your-feature-name
   ```

2. **Final Verification:**
   - Re-run tests locally after conflict resolution
   - Verify CI passes after conflict resolution
   - Ensure no accidental changes introduced

3. **Merge PR:**
   - Maintainer clicks "Squash and merge" button
   - Confirms commit message follows format
   - Completes merge to main branch

4. **Delete Feature Branch:**
   - GitHub prompts to delete branch after merge
   - Click "Delete branch" to clean up
   - Alternatively:
     ```bash
     git branch -d feature/your-feature-name  # Local
     git push origin --delete feature/your-feature-name  # Remote
     ```

**Source:** `README.md:750`, Git best practices

## Post-Merge Activities

After your PR is merged, complete these follow-up tasks:

### 1. Monitor CI on Main Branch

Verify the merge didn't break anything:

```bash
# Watch CI status for main branch
# Check GitHub Actions or CI system
# Ensure all checks pass after merge
```

If CI fails on main after merge:
- Investigate immediately
- Create hotfix PR if needed
- Notify maintainers

### 2. Verify Deployment (If Applicable)

For changes affecting deployments:
- Check staging environment
- Verify feature works as expected
- Monitor for errors or issues

### 3. Close Related Issues

Close issues resolved by your PR:
- GitHub auto-closes issues with `Fixes #123` syntax
- Manually close if not auto-closed
- Add closing comment referencing PR: `Fixed in #287`

### 4. Update Project Board (If Used)

If using GitHub Projects:
- Move issue/card to "Done" column
- Update status and labels
- Add completion notes

### 5. Update Your Fork

Keep your fork synchronized:

```bash
# Switch to main branch
git checkout main

# Pull latest from upstream
git pull upstream main

# Push to your fork
git push origin main

# Delete local feature branch
git branch -d feature/your-feature-name
```

### 6. Celebrate! 🎉

Your contribution is now part of the project. Thank you for contributing!

## Getting Help

If you need assistance with the PR process:

### Documentation Resources

- [Development Setup Guide](development-setup.md) - Environment configuration
- [Code Style Guide](code-style-guide.md) - Coding standards
- [Testing Guidelines](testing-guidelines.md) - Test requirements
- [Documentation Guidelines](documentation-guidelines.md) - Documentation standards
- [README](../../README.md) - Project overview and setup

### Ask Questions

**On GitHub:**
- Comment on your PR with questions
- Open a discussion in [Discussions](https://github.com/testinium/testinium-qa-python/discussions)
- Create an issue for bugs or feature requests

**Contact Maintainers:**
- Tag maintainers in comments: `@testinium-qa-team`
- Email: qa@testinium.com (for private concerns)

### Draft Pull Requests

For work-in-progress:

1. **Create Draft PR:**
   - Click "Create draft pull request" instead of "Create pull request"
   - Indicates PR is not ready for review
   - CI still runs, but reviewers won't be notified

2. **Use [WIP] Tag:**
   - Alternative: Add `[WIP]` to PR title
   - Example: `[WIP] feat(pages): add inventory page object`

3. **Mark Ready:**
   - Click "Ready for review" when done
   - Remove `[WIP]` from title
   - Request reviewers

**Source:** GitHub PR features

## Examples

### Complete PR Description Example

```markdown
## Description

This PR adds comprehensive parallel execution support for Behave scenarios, enabling faster test execution in CI/CD environments.

### What does this PR do?

Implements scenario-level parallelism using behave-parallel with thread-safe WebDriver management. Tests can now run concurrently across multiple worker processes while maintaining isolation.

### Why is this change needed?

Current test suite takes 45 minutes to run sequentially. With parallel execution, runtime reduces to ~12 minutes with 4 workers, significantly improving CI/CD pipeline efficiency.

### Related Issues

Fixes #287 - Add parallel execution support
Ref #298 - Improve CI/CD pipeline performance

## Type of Change

- [x] New feature (non-breaking change that adds functionality)
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation update

## Testing

### Test Coverage

- [x] Unit tests added for parallel driver management
- [x] Integration tests verified with 2, 4, and 8 workers
- [x] All tests pass locally: `pytest tests/ && behave`
- [x] Coverage maintained at 92% for utilities package

### Manual Testing

**Environments tested:**
- macOS 14 with Python 3.11
- Ubuntu 22.04 with Python 3.9, 3.10, 3.11
- Windows 11 with Python 3.11

**Test scenarios:**
```bash
# Sequential execution (baseline)
behave --tags=@Smoke
Result: 45 minutes, all pass

# Parallel with 2 workers
behave --processes 2 --parallel-element scenario --tags=@Smoke
Result: 24 minutes, all pass

# Parallel with 4 workers  
behave --processes 4 --parallel-element scenario --tags=@Smoke
Result: 12 minutes, all pass

# Parallel with 8 workers
behave --processes 8 --parallel-element scenario --tags=@Smoke
Result: 11 minutes, all pass (diminishing returns beyond 4)
```

## Code Quality

- [x] Black formatting applied
- [x] isort applied  
- [x] pylint score: 9.2/10
- [x] mypy passes with no errors
- [x] PEP 8 compliant

## Documentation

- [x] Docstrings added for parallel execution utilities
- [x] User guide created: `docs/guides/parallel-execution.md`
- [x] Architecture documentation updated: `docs/architecture/parallel-execution.md`
- [x] README updated with parallel execution examples
- [x] CHANGELOG entry added

## Breaking Changes

Does this PR introduce breaking changes?
- [ ] Yes
- [x] No

## Additional Context

### Performance Impact

Significant positive impact:
- 73% reduction in test execution time (4 workers)
- Linear scaling up to 4 workers
- No resource contention issues observed

### Migration Notes

No migration needed. Parallel execution is opt-in via command-line flag:

```bash
# Existing sequential execution still works
behave

# New parallel execution
behave --processes 4 --parallel-element scenario
```

### Screenshots

N/A - Command-line feature

## Checklist

- [x] I have read the Code Style Guide
- [x] I have read the Testing Guidelines
- [x] I have read the Documentation Guidelines
- [x] My code follows the project's style guidelines
- [x] I have performed a self-review of my own code
- [x] I have commented my code, particularly in hard-to-understand areas
- [x] I have made corresponding changes to the documentation
- [x] My changes generate no new warnings
- [x] I have added tests that prove my fix is effective or my feature works
- [x] New and existing unit tests pass locally with my changes
- [x] Any dependent changes have been merged and published
- [x] I have checked my code and corrected any misspellings
- [x] I have not committed any secrets, passwords, or API keys
```

### Good Commit Message Examples

```bash
# Feature addition
feat(utilities): add parallel execution support for behave tests

Implements scenario-level parallelism using threading.local() pattern
for WebDriver isolation. Each worker process gets independent driver
instance preventing resource conflicts.

- Add behave-parallel to requirements.txt
- Update DriverManager to use threading.local()
- Add parallel execution guide to documentation
- Test with 2, 4, 8 worker configurations

Fixes #287

# Bug fix
fix(pages): prevent stale element exception in crm page navigation

Added explicit wait for element staleness before re-finding elements
during CRM workflow transitions. This resolves intermittent test
failures when page elements are dynamically reloaded.

The Java version had similar issue resolved in CrmPage.java:145 using
ExpectedConditions.stalenessOf().

Fixes #342

# Documentation
docs(deployment): add complete kubernetes deployment guide

Comprehensive guide covering:
- Deployment.yaml configuration for test pods
- ConfigMap for config.yaml externalization
- Secrets for test credentials
- Job resources for parallel test execution
- Report collection via volume mounts

Includes working examples for GKE, EKS, and AKS.

Ref #298
```

### Branch Naming Examples

```bash
# Good examples
feature/allure-report-integration
feature/kubernetes-deployment-support
bugfix/287-stale-element-crm
bugfix/342-firefox-parallel-crash
docs/parallel-execution-guide
docs/api-reference-utilities
refactor/wait-helpers-consolidation
test/inventory-page-crud-tests

# Bad examples
fix                     # Too vague
my-branch              # Not descriptive  
update-stuff           # Too generic
NewFeature             # Wrong case
feature_add_tests      # Wrong separator
```

## Troubleshooting

### PR Creation Issues

**Issue:** Can't create PR from fork

**Solution:**
```bash
# Ensure your fork is up to date
git remote add upstream https://github.com/testinium/testinium-qa-python.git
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

**Issue:** PR shows too many commits

**Solution:**
```bash
# Squash commits before creating PR
git rebase -i HEAD~10  # Adjust number
# Mark commits as 'squash' or 'fixup'
# Force push: git push -f origin feature/your-branch
```

### CI Failures

**Issue:** Black formatting check fails

**Solution:**
```bash
black .
git add .
git commit -m "style: apply black formatting"
git push
```

**Issue:** Tests pass locally but fail in CI

**Common causes:**
- Environment differences (Python version, OS)
- Missing dependencies
- Race conditions in parallel tests
- Hardcoded paths

**Solution:** Check CI logs for specific errors and test in similar environment

### Review Process Issues

**Issue:** No response from reviewers

**Solution:**
- Wait 2 business days
- Comment on PR asking for review
- Tag maintainers: `@testinium-qa-team`

**Issue:** Requested changes unclear

**Solution:**
- Comment asking for clarification
- Request code examples
- Suggest alternative approaches

**Issue:** Merge conflicts

**Solution:**
```bash
# Update your branch with main
git checkout feature/your-branch
git fetch upstream
git merge upstream/main
# Resolve conflicts in files
git add .
git commit -m "merge: resolve conflicts with main"
git push origin feature/your-branch
```

---

**Thank you for contributing to Testinium QA Python!** Your efforts help improve test automation for the entire community.

**Source:** `README.md:740-760`, project contribution experience, GitHub documentation
