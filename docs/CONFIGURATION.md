# Testinium-QA Framework Configuration Guide

This document provides comprehensive documentation for configuring the Testinium-QA test automation framework, including the configuration file format, available properties, browser settings, and environment-specific configuration patterns.

## Table of Contents

- [Introduction](#introduction)
- [Configuration File Location](#configuration-file-location)
- [Available Configuration Keys](#available-configuration-keys)
- [Browser Configuration](#browser-configuration)
- [URL and Credential Settings](#url-and-credential-settings)
- [Timeouts and Wait Configuration](#timeouts-and-wait-configuration)
- [Environment-Specific Configuration](#environment-specific-configuration)
- [Runtime Configuration via System Properties](#runtime-configuration-via-system-properties)
- [Configuration Reader Usage](#configuration-reader-usage)
- [Best Practices](#best-practices)
- [See Also](#see-also)

---

## Introduction

The Testinium-QA framework uses a **centralized configuration management** approach to externalize test settings from the code. This enables:

- **Environment Flexibility**: Switch between test, staging, and production environments without code changes
- **Browser Selection**: Choose between Chrome and Firefox from configuration
- **Credential Management**: Store test credentials externally for security
- **Easy Maintenance**: Update URLs and settings without recompiling

The configuration system consists of two main components:

1. **`configuration.properties`** - A Java properties file containing key-value pairs
2. **`ConfigurationReader`** - A utility class that loads and provides access to configuration values

### Architecture Overview

```mermaid
graph LR
    subgraph "Configuration Layer"
        CF[configuration.properties<br/>Key-value settings]
        CR[ConfigurationReader<br/>Static accessor]
    end
    
    subgraph "Consumers"
        D[Driver.java<br/>Browser type]
        SD[Step Definitions<br/>URLs, credentials]
    end
    
    CF -->|FileInputStream| CR
    CR -->|getProperty()| D
    CR -->|getProperty()| SD
```

*Source: src/main/java/com/testinium/utilities/ConfigurationReader.java:1-30*

---

## Configuration File Location

### File Path

The configuration file must be placed at the **project root directory**:

```
project-root/
├── configuration.properties    <-- Configuration file
├── pom.xml
├── src/
│   └── main/
│       └── java/
│           └── com/testinium/
│               └── utilities/
│                   └── ConfigurationReader.java
```

### How It's Loaded

The `ConfigurationReader` class loads the configuration file using a **static initializer block**, which executes automatically when the class is first accessed:

```java
private static Properties properties = new Properties();

static {
    try {
        FileInputStream file = new FileInputStream("configuration.properties");
        properties.load(file);
        file.close();
    } catch (IOException e) {
        System.out.println("File is not found in the ConfigurationReader class");
        e.printStackTrace();
    }
}
```

*Source: src/main/java/com/testinium/utilities/ConfigurationReader.java:9-25*

### Key Loading Characteristics

| Aspect | Behavior |
|--------|----------|
| **File Path** | Relative path `configuration.properties` (project root) |
| **Load Timing** | Once, at class initialization (static block) |
| **Error Handling** | Prints error message and stack trace to console |
| **File Stream** | Properly closed after loading |
| **Thread Safety** | Read-only access after initialization |

### Error Handling

If the configuration file is missing or cannot be read, the framework prints:

```
File is not found in the ConfigurationReader class
java.io.FileNotFoundException: configuration.properties (No such file or directory)
    at java.io.FileInputStream.open0(Native Method)
    ...
```

*Source: src/main/java/com/testinium/utilities/ConfigurationReader.java:22*

> **Important**: Ensure `configuration.properties` exists at the project root before running tests. Missing configuration will cause `NullPointerException` when accessing properties.

---

## Available Configuration Keys

### Standard Configuration Properties

The framework recognizes the following configuration keys:

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `browser` | String | Yes | Browser type for test execution (`chrome` or `firefox`) |
| `web.table.url` | String | Yes | Base URL for the Odoo/Upgenix application |
| `username` | String | Optional | Test user email/username |
| `password` | String | Optional | Test user password |

### Example Configuration File

Create a `configuration.properties` file with the following format:

```properties
# ========================================
# Testinium-QA Framework Configuration
# ========================================

# Browser Configuration
# Supported values: chrome, firefox
browser=chrome

# Application URL
# The base URL of the Odoo/Upgenix web application
web.table.url=https://your-odoo-instance.com/web/login

# Test Credentials
# WARNING: Do not commit real credentials to version control
username=test@example.com
password=testpassword

# Additional Custom Properties
# Add your own key-value pairs as needed
# custom.property=value
```

### Property File Format Rules

- **Comments**: Lines starting with `#` or `!` are comments
- **Key-Value Pairs**: Use `key=value` or `key:value` format
- **Whitespace**: Leading/trailing whitespace is trimmed from values
- **Multi-line Values**: Use backslash `\` for line continuation
- **Special Characters**: Use `\` to escape special characters

---

## Browser Configuration

### Supported Browsers

The framework currently supports two browsers:

| Browser | Configuration Value | Driver Management |
|---------|---------------------|-------------------|
| Chrome | `chrome` | WebDriverManager auto-setup |
| Firefox | `firefox` | WebDriverManager auto-setup |

### Browser Selection

Set the browser in `configuration.properties`:

```properties
# For Chrome browser
browser=chrome

# For Firefox browser
browser=firefox
```

### Browser Initialization Process

When `Driver.getDriver()` is called, the browser is initialized based on the configuration:

```java
String browserType = ConfigurationReader.getProperty("browser");

switch(browserType){
    case "chrome":
        WebDriverManager.chromedriver().setup();
        driverPool.set(new ChromeDriver());
        driverPool.get().manage().window().maximize();
        driverPool.get().manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
        break;
    case "firefox":
        WebDriverManager.firefoxdriver().setup();
        driverPool.set(new FirefoxDriver());
        driverPool.get().manage().window().maximize();
        driverPool.get().manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
        break;
}
```

*Source: src/main/java/com/testinium/utilities/Driver.java:27-41*

### Browser Configuration Details

#### Chrome Configuration

| Setting | Value | Source |
|---------|-------|--------|
| Driver Setup | `WebDriverManager.chromedriver().setup()` | Driver.java:31 |
| Window State | Maximized | Driver.java:33 |
| Implicit Wait | 10 seconds | Driver.java:34 |

#### Firefox Configuration

| Setting | Value | Source |
|---------|-------|--------|
| Driver Setup | `WebDriverManager.firefoxdriver().setup()` | Driver.java:37 |
| Window State | Maximized | Driver.java:39 |
| Implicit Wait | 10 seconds | Driver.java:40 |

### Headless Mode (Advanced)

The current framework implementation does not include headless browser configuration. To enable headless mode, you would need to modify `Driver.java` to use browser-specific options:

```java
// Example: Chrome headless mode (requires code modification)
ChromeOptions options = new ChromeOptions();
options.addArguments("--headless");
options.addArguments("--disable-gpu");
options.addArguments("--window-size=1920,1080");
driverPool.set(new ChromeDriver(options));
```

> **Note**: This is shown for reference only. The current framework requires code changes to support headless execution.

### WebDriverManager Integration

The framework uses [WebDriverManager](https://bonigarcia.dev/webdrivermanager/) for automatic browser driver management:

- **Automatic Download**: Downloads the correct driver version for your browser
- **Version Management**: Ensures compatibility between browser and driver versions
- **No Manual Setup**: Eliminates need to download and configure drivers manually

*Source: Driver.java:31, 37; pom.xml dependency: io.github.bonigarcia:webdrivermanager:5.1.0*

---

## URL and Credential Settings

### Application URL Configuration

The application URL is stored with the key `web.table.url`:

```properties
web.table.url=https://your-odoo-instance.com/web/login
```

### URL Usage in Tests

Step definitions retrieve and use the URL as follows:

```java
@Given("User is on the upgenix login page")
public void user_is_on_the_upgenix_login_page() {
    String url = ConfigurationReader.getProperty("web.table.url");
    Driver.getDriver().get(url);
}
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:21-23*

### URL Configuration Examples

```properties
# Development environment
web.table.url=http://localhost:8069/web/login

# QA/Testing environment
web.table.url=https://qa.upgenix.example.com/web/login

# Staging environment
web.table.url=https://staging.upgenix.example.com/web/login

# Production (use with caution!)
web.table.url=https://app.upgenix.example.com/web/login
```

### Credential Management

Store test credentials in the configuration file:

```properties
# Test account credentials
username=test@example.com
password=testpassword
```

### Credential Usage Example

```java
// Retrieve credentials in step definitions
String username = ConfigurationReader.getProperty("username");
String password = ConfigurationReader.getProperty("password");

// Use in test
loginPage.inputEmail.sendKeys(username);
loginPage.inputPassword.sendKeys(password);
```

### Security Best Practices

> **⚠️ SECURITY WARNING**: Never commit real credentials to version control!

| Practice | Description |
|----------|-------------|
| **Use .gitignore** | Add `configuration.properties` to `.gitignore` |
| **Template File** | Commit `configuration.properties.example` with placeholder values |
| **Environment Variables** | Consider using environment variables for sensitive data |
| **CI/CD Secrets** | Use your CI/CD platform's secret management for credentials |

#### Example .gitignore Entry

```gitignore
# Ignore configuration with real credentials
configuration.properties

# But track the template
!configuration.properties.example
```

#### Example Template File (configuration.properties.example)

```properties
# Copy this file to configuration.properties and fill in actual values
browser=chrome
web.table.url=<your-odoo-url>
username=<your-username>
password=<your-password>
```

---

## Timeouts and Wait Configuration

### Implicit Wait

The framework configures a **10-second implicit wait** on all WebDriver instances. This provides a baseline synchronization mechanism for element location.

```java
driverPool.get().manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
```

*Source: src/main/java/com/testinium/utilities/Driver.java:34, 40*

### Implicit Wait Behavior

| Aspect | Behavior |
|--------|----------|
| **Duration** | 10 seconds |
| **Scope** | All `findElement()` and `findElements()` calls |
| **Retry** | Continuously polls DOM until element found or timeout |
| **Exception** | Throws `NoSuchElementException` after timeout |

### Explicit Waits

Step definitions can use **explicit waits** for more precise synchronization:

```java
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 3);
wait.until(ExpectedConditions.visibilityOf(element));
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:17, 43*

### Explicit Wait Examples

```java
// Wait for element visibility
wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));

// Wait for element to be clickable
wait.until(ExpectedConditions.elementToBeClickable(button));

// Wait for text to be present
wait.until(ExpectedConditions.textToBePresentInElement(element, "Expected Text"));

// Wait for URL to contain
wait.until(ExpectedConditions.urlContains("/dashboard"));
```

### Wait Strategy Recommendations

| Situation | Recommended Approach |
|-----------|---------------------|
| **Standard element lookup** | Rely on implicit wait (10s) |
| **Dynamic content loading** | Use explicit wait with visibility condition |
| **AJAX operations** | Use explicit wait for element state changes |
| **Page transitions** | Use explicit wait for URL or title conditions |
| **Animations/transitions** | Use explicit wait with custom timeout |

### Timeout Configuration Considerations

The current implementation hardcodes the implicit wait to 10 seconds. To make it configurable:

1. Add a property to `configuration.properties`:
   ```properties
   implicit.wait.seconds=10
   ```

2. Modify `Driver.java` to read the configuration:
   ```java
   int implicitWait = Integer.parseInt(
       ConfigurationReader.getProperty("implicit.wait.seconds")
   );
   driverPool.get().manage().timeouts()
       .implicitlyWait(implicitWait, TimeUnit.SECONDS);
   ```

> **Note**: This requires code modification to the `Driver` class.

---

## Environment-Specific Configuration

### Multiple Configuration Files Pattern

For managing multiple environments, create separate configuration files:

```
project-root/
├── configuration.properties           # Default/development
├── configuration-qa.properties        # QA environment
├── configuration-staging.properties   # Staging environment
└── configuration-prod.properties      # Production environment
```

### Environment File Examples

#### configuration-qa.properties

```properties
browser=chrome
web.table.url=https://qa.upgenix.example.com/web/login
username=qa-tester@example.com
password=qa-test-password
implicit.wait.seconds=15
```

#### configuration-staging.properties

```properties
browser=firefox
web.table.url=https://staging.upgenix.example.com/web/login
username=staging-user@example.com
password=staging-password
implicit.wait.seconds=10
```

### Environment Selection Strategies

#### Strategy 1: File Rename/Copy

Before running tests, copy the appropriate file:

```bash
# For QA environment
cp configuration-qa.properties configuration.properties
mvn test

# For Staging environment
cp configuration-staging.properties configuration.properties
mvn test
```

#### Strategy 2: Modify ConfigurationReader (Recommended)

Update `ConfigurationReader.java` to support environment selection:

```java
static {
    try {
        String env = System.getProperty("env", "default");
        String configFile = env.equals("default") 
            ? "configuration.properties" 
            : "configuration-" + env + ".properties";
        
        FileInputStream file = new FileInputStream(configFile);
        properties.load(file);
        file.close();
    } catch (IOException e) {
        System.out.println("Configuration file not found");
        e.printStackTrace();
    }
}
```

Then run with:

```bash
# Run with QA configuration
mvn test -Denv=qa

# Run with Staging configuration
mvn test -Denv=staging
```

> **Note**: This requires code modification to `ConfigurationReader.java`.

#### Strategy 3: Environment Variables

Use environment variables for sensitive or environment-specific values:

```java
public static String getProperty(String keyword) {
    // Check environment variable first
    String envValue = System.getenv(keyword.toUpperCase().replace(".", "_"));
    if (envValue != null) {
        return envValue;
    }
    // Fall back to properties file
    return properties.getProperty(keyword);
}
```

Set environment variables:

```bash
export BROWSER=chrome
export WEB_TABLE_URL=https://qa.upgenix.example.com/web/login
mvn test
```

---

## Runtime Configuration via System Properties

### Maven Command Line Overrides

Override configuration at runtime using Maven system properties:

```bash
# Override browser
mvn test -Dbrowser=firefox

# Override URL
mvn test -Dweb.table.url=https://staging.example.com/web/login

# Multiple overrides
mvn test -Dbrowser=chrome -Dweb.table.url=https://qa.example.com/web/login
```

> **Note**: The current `ConfigurationReader` implementation does not support system property overrides. This requires code modification.

### Enabling System Property Overrides

Modify `ConfigurationReader.getProperty()` to check system properties first:

```java
public static String getProperty(String keyword) {
    // Check system property first (allows -D override)
    String systemValue = System.getProperty(keyword);
    if (systemValue != null) {
        return systemValue;
    }
    // Fall back to properties file
    return properties.getProperty(keyword);
}
```

### Cucumber Options Override

Control Cucumber test execution via command line:

```bash
# Run specific tags
mvn test -Dcucumber.filter.tags="@Smoke"

# Run multiple tags (AND)
mvn test -Dcucumber.filter.tags="@Smoke and @Login"

# Run multiple tags (OR)
mvn test -Dcucumber.filter.tags="@Smoke or @Regression"

# Exclude tags
mvn test -Dcucumber.filter.tags="not @WIP"
```

### CI/CD Integration Example

#### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['qa', 'staging', 'prod'],
            description: 'Test environment'
        )
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox'],
            description: 'Browser for testing'
        )
        string(
            name: 'TAGS',
            defaultValue: '@Smoke',
            description: 'Cucumber tags to run'
        )
    }
    
    stages {
        stage('Test') {
            steps {
                sh """
                    mvn test \
                        -Denv=${params.ENVIRONMENT} \
                        -Dbrowser=${params.BROWSER} \
                        -Dcucumber.filter.tags="${params.TAGS}"
                """
            }
        }
    }
}
```

#### GitHub Actions

```yaml
name: Test Automation

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Test environment'
        required: true
        default: 'qa'
        type: choice
        options:
          - qa
          - staging
      browser:
        description: 'Browser'
        required: true
        default: 'chrome'
        type: choice
        options:
          - chrome
          - firefox

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '8'
      - name: Run Tests
        run: |
          mvn test \
            -Denv=${{ github.event.inputs.environment }} \
            -Dbrowser=${{ github.event.inputs.browser }}
```

---

## Configuration Reader Usage

### Basic Usage

The `ConfigurationReader` class provides static access to configuration values:

```java
// Import the class
import com.testinium.utilities.ConfigurationReader;

// Get a property value
String browser = ConfigurationReader.getProperty("browser");
String url = ConfigurationReader.getProperty("web.table.url");
```

*Source: src/main/java/com/testinium/utilities/ConfigurationReader.java:27-29*

### Method Signature

```java
public static String getProperty(String keyword)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `keyword` | String | The property key to look up |
| **Returns** | String | The property value, or `null` if not found |

### Usage Examples

#### In Step Definitions

```java
public class LoginSD {
    
    @Given("User is on the upgenix login page")
    public void user_is_on_the_upgenix_login_page() {
        String url = ConfigurationReader.getProperty("web.table.url");
        Driver.getDriver().get(url);
    }
}
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:19-24*

#### In Driver Initialization

```java
public static WebDriver getDriver() {
    if (driverPool.get() == null) {
        String browserType = ConfigurationReader.getProperty("browser");
        // ... browser initialization
    }
    return driverPool.get();
}
```

*Source: src/main/java/com/testinium/utilities/Driver.java:21-27*

### Return Value Handling

The `getProperty()` method returns `null` if the key is not found:

```java
String value = ConfigurationReader.getProperty("nonexistent.key");
// value is null

// Safe handling with default value
String browser = ConfigurationReader.getProperty("browser");
if (browser == null) {
    browser = "chrome"; // default value
}

// Or using Optional (Java 8+)
String timeout = Optional.ofNullable(
    ConfigurationReader.getProperty("timeout")
).orElse("10");
```

### Thread Safety

The `ConfigurationReader` is **thread-safe** for read operations:

- Properties are loaded once in the static initializer
- The `Properties` object is never modified after initialization
- Multiple threads can safely call `getProperty()` concurrently

*Source: src/main/java/com/testinium/utilities/ConfigurationReader.java:11-25*

---

## Best Practices

### Configuration Management

| Practice | Description |
|----------|-------------|
| **Single Source of Truth** | All configurable values should be in `configuration.properties` |
| **Meaningful Keys** | Use descriptive key names (e.g., `web.table.url` not `url1`) |
| **Comments** | Add comments explaining each property's purpose |
| **Defaults** | Document default values for optional properties |

### Security

| Practice | Description |
|----------|-------------|
| **No Hardcoding** | Never hardcode credentials in Java files |
| **gitignore** | Keep `configuration.properties` out of version control |
| **Template** | Provide a template file with placeholder values |
| **Rotation** | Use dedicated test accounts and rotate credentials regularly |

### Environment Management

| Practice | Description |
|----------|-------------|
| **Separate Files** | Use separate config files per environment |
| **CI/CD Integration** | Inject configuration via CI/CD pipeline |
| **Validation** | Add startup validation for required properties |
| **Documentation** | Document all required properties and valid values |

### Testing

| Practice | Description |
|----------|-------------|
| **Isolation** | Each test environment should be isolated |
| **Data Management** | Use test-specific data that won't affect production |
| **URL Verification** | Verify you're testing against the correct environment |
| **Cleanup** | Clean up test data after test execution |

---

## See Also

- [Framework Architecture](ARCHITECTURE.md) - Detailed architecture overview, including Driver and ConfigurationReader class design
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Solutions for configuration-related issues
- [Extending the Framework](EXTENDING.md) - Adding new configurable features

### External Resources

- [Java Properties Documentation](https://docs.oracle.com/javase/8/docs/api/java/util/Properties.html)
- [WebDriverManager Documentation](https://bonigarcia.dev/webdrivermanager/)
- [Selenium Timeouts Documentation](https://www.selenium.dev/documentation/webdriver/waits/)
- [Cucumber Configuration](https://cucumber.io/docs/cucumber/configuration/)

---

*This documentation is generated from source analysis of the Testinium-QA framework.*

*Key Sources:*
- *src/main/java/com/testinium/utilities/ConfigurationReader.java*
- *src/main/java/com/testinium/utilities/Driver.java*
- *src/main/java/com/testinium/step_definitions/LoginSD.java*
