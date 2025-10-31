# Reference Documentation

## Overview

This section provides authoritative, quick-lookup reference documentation for the Testinium QA test automation framework. Reference documentation focuses on **what** options, commands, and syntax are available without tutorials or step-by-step instructions (those are in the [Guides](../guides/index.md) section).

**Use reference documentation when you need to:**
- Look up a specific configuration option and its values
- Check command-line syntax and available flags
- Verify environment variable names and formats
- Confirm Gherkin keyword usage and syntax rules
- Review dependency purposes and version requirements

## Configuration Reference

Complete specifications for all framework configuration files and options.

### [Configuration Options](configuration-options.md)
Complete `config.yaml` reference with all browser, timeout, application, credentials, and reporting settings. Covers browser type selection, headless mode, window sizing, timeout values, base URLs, credential management, and report format configuration.

**Quick lookup:** Browser types, timeout values, URL configuration, report formats

### [Environment Variables](environment-variables.md)
All supported environment variables from `.env` file with descriptions, security notes, and CI/CD integration patterns. Includes variable precedence rules and interpolation syntax.

**Quick lookup:** Credential variables, browser override variables, timeout overrides

### [Behave Configuration](behave-configuration.md)
Complete `behave.ini` options reference including feature paths, output formats, JUnit integration, logging configuration, tag execution, and parallel execution options.

**Quick lookup:** Tag syntax, output formats, parallel execution, JUnit reporting

### [pytest Configuration](pytest-configuration.md)
Complete `pytest.ini` options reference with test discovery patterns, markers, parallel execution with pytest-xdist, logging configuration, and coverage settings.

**Quick lookup:** Test markers, parallel execution flags, logging levels

## Command Reference

### [Command-Line Reference](command-reference.md)
Comprehensive command syntax for `behave` and `pytest` with all options, flags, and execution patterns. Covers running tests with tags, generating reports, parallel execution, dry runs, and rerun failed tests.

**Quick lookup:** behave commands, pytest commands, tag syntax, output format flags

## Dependencies Reference

### [Dependencies](dependencies.md)
All Python packages from `requirements.txt` with purposes, version specifications, Maven/Java equivalents for migration context, and compatibility notes. Includes core testing frameworks, WebDriver management, reporting tools, and development utilities.

**Quick lookup:** Package versions, migration equivalents, dependency purposes

## Syntax Reference

### [Gherkin Syntax](gherkin-syntax.md)
Complete BDD feature file syntax reference with keywords (Feature, Background, Scenario, Scenario Outline, Given, When, Then), tags, Examples tables, and best practices. Includes Jira integration tag patterns.

**Quick lookup:** Gherkin keywords, tag syntax, Examples table format, scenario patterns

## Quick Reference Links

**Most frequently referenced items:**

- **Run tests with specific tags:** `behave --tags=@Login` - See [Command Reference](command-reference.md#tag-execution)
- **Configure browser type:** `browser.type: chrome` - See [Configuration Options](configuration-options.md#browser-configuration)
- **Set timeout values:** `timeouts.explicit: 10` - See [Configuration Options](configuration-options.md#timeout-configuration)
- **Manage credentials securely:** Use environment variables - See [Environment Variables](environment-variables.md#credentials)
- **Enable parallel execution:** `behave --processes 4` - See [Behave Configuration](behave-configuration.md#parallel-execution)
- **Generate Allure reports:** `behave -f allure_behave.formatter:AllureFormatter` - See [Command Reference](command-reference.md#report-generation)

## Reference vs Guides: When to Use Each

### Use Reference Documentation When You Need To:

✅ **Look up specific options** - "What values can `browser.type` accept?"  
✅ **Check command syntax** - "What flags does `behave` support?"  
✅ **Verify variable names** - "What's the environment variable for base URL?"  
✅ **Confirm syntax rules** - "Can I use multiple tags with OR logic?"  
✅ **Review available markers** - "What pytest markers are defined?"

### Use Guide Documentation When You Need To:

📖 **Learn how to use features** - "How do I write a new page object?"  
📖 **Follow step-by-step tutorials** - "How do I set up parallel execution?"  
📖 **Understand workflows** - "How do login tests work end-to-end?"  
📖 **Troubleshoot issues** - "Why aren't my tests finding elements?"  
📖 **See complete examples** - "Show me a complete CRM testing example"

**See Also:**
- [Getting Started Guide](../getting-started/index.md) - First-time setup tutorials
- [User Guides](../guides/index.md) - Feature-specific how-to guides
- [Troubleshooting](../troubleshooting/index.md) - Problem-solving guides

## How to Use This Reference

### Search Effectively

Use your browser's search function (Ctrl+F or Cmd+F) or the documentation site's search feature to find specific:
- Configuration option names (e.g., `headless`, `timeout`, `base_url`)
- Environment variable names (e.g., `BROWSER_TYPE`, `TEST_USERNAME`)
- Command flags (e.g., `--tags`, `--processes`, `--junit`)
- Gherkin keywords (e.g., `Scenario Outline`, `Examples`, `Background`)

### Bookmark Frequently Used Pages

Add browser bookmarks for reference pages you consult often:
- Configuration options for quick environment setup
- Command reference for daily test execution
- Environment variables for CI/CD pipeline configuration
- Gherkin syntax for feature file authoring

### Understanding Reference Format

Reference pages show **specifications, not tutorials:**

**✅ Reference Style (what you'll find here):**
```
Option: browser.type
Type: string
Values: chrome | firefox
Default: chrome
Environment Override: BROWSER_TYPE
```

**📖 Guide Style (found in guides/):**
```
To configure Chrome for headless execution:
1. Open config/config.yaml
2. Set browser.headless to true
3. Run tests: behave --tags=@Login
4. Verify reports in reports/ directory
```

### Cross-References to Guides

Each reference page includes "See Also" sections linking to relevant guides for hands-on instructions and complete examples.

## Contributing to Reference Documentation

Reference documentation should be:
- **Authoritative** - Accurate specifications verified against source code
- **Concise** - Brief descriptions without elaboration
- **Complete** - All options, commands, and syntax elements documented
- **Current** - Updated when framework changes

To contribute reference documentation updates, see [Contributing Guidelines](../contributing/documentation-guidelines.md).

---

**Source:** Reference overview compiled from `config/config.yaml`, `behave.ini`, `pytest.ini`, `.env.example`, `requirements.txt`, and `features/Login.feature`

**Last Updated:** 2024 (Generated for framework version 1.0.0)
