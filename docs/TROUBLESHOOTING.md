# Testinium-QA Framework Troubleshooting Guide

This document provides comprehensive troubleshooting guidance for common issues encountered when developing and executing tests with the Testinium-QA Selenium/Cucumber test automation framework.

## Table of Contents

- [Introduction](#introduction)
- [Common Selenium Errors](#common-selenium-errors)
  - [NoSuchElementException](#nosuchelementexception)
  - [StaleElementReferenceException](#staleelementreferenceexception)
  - [TimeoutException](#timeoutexception)
  - [SessionNotCreatedException](#sessionnotcreatedexception)
- [Locator Issues](#locator-issues)
  - [Brittle XPath Strategies](#brittle-xpath-strategies)
  - [Dynamic ID Handling](#dynamic-id-handling)
  - [Text-Based Locator Reliability](#text-based-locator-reliability)
  - [Locator Selection Best Practices](#locator-selection-best-practices)
- [Timing Problems](#timing-problems)
  - [Implicit Wait vs Explicit Wait](#implicit-wait-vs-explicit-wait)
  - [Thread.sleep Anti-Pattern](#threadsleep-anti-pattern)
  - [WebDriverWait Usage](#webdriverwait-usage)
  - [ExpectedConditions Catalog](#expectedconditions-catalog)
  - [Race Conditions and Synchronization](#race-conditions-and-synchronization)
- [Browser Driver Issues](#browser-driver-issues)
  - [WebDriverManager Configuration](#webdrivermanager-configuration)
  - [Chrome Driver Issues](#chrome-driver-issues)
  - [Firefox Driver Issues](#firefox-driver-issues)
  - [Headless Mode Configuration](#headless-mode-configuration)
  - [Browser Capability Settings](#browser-capability-settings)
- [Configuration Problems](#configuration-problems)
  - [Configuration File Not Found](#configuration-file-not-found)
  - [Missing Required Properties](#missing-required-properties)
  - [Environment-Specific Configuration](#environment-specific-configuration)
- [Screenshot Capture for Debugging](#screenshot-capture-for-debugging)
  - [Automatic Capture on Failure](#automatic-capture-on-failure)
  - [Manual Screenshot Capture](#manual-screenshot-capture)
  - [Screenshot File Location](#screenshot-file-location)
- [Debugging Tips](#debugging-tips)
  - [IDE Breakpoints and Debugging](#ide-breakpoints-and-debugging)
  - [Console Logging Strategies](#console-logging-strategies)
  - [Cucumber Report Analysis](#cucumber-report-analysis)
  - [Browser DevTools Integration](#browser-devtools-integration)
  - [Test Isolation Techniques](#test-isolation-techniques)
- [See Also](#see-also)

---

## Introduction

Automated UI testing with Selenium WebDriver can encounter various challenges related to element location, synchronization, browser compatibility, and configuration. This guide documents the most common issues encountered when working with the Testinium-QA framework and provides practical solutions.

### When to Use This Guide

- Tests are failing intermittently or consistently
- Elements cannot be found on the page
- Browser sessions fail to start
- Configuration is not being loaded correctly
- Tests pass locally but fail in CI/CD
- You need to debug test failures efficiently

### Framework Context

This troubleshooting guide is specific to the Testinium-QA framework, which uses:

| Component | Version | Configuration Location |
|-----------|---------|----------------------|
| Selenium WebDriver | 3.141.59 | `pom.xml:54` |
| WebDriverManager | 5.1.0 | `pom.xml:60` |
| Implicit Wait | 10 seconds | `Driver.java:155` |
| Browser Selection | Config-driven | `configuration.properties` |
| Screenshot on Failure | Automatic | `Hooks.java:117-119` |

*Source: pom.xml, src/main/java/com/testinium/utilities/Driver.java*

---

## Common Selenium Errors

### NoSuchElementException

The `NoSuchElementException` is thrown when WebDriver cannot locate an element on the page using the specified locator strategy.

#### Error Signature

```
org.openqa.selenium.NoSuchElementException: no such element: Unable to locate element: {"method":"xpath","selector":"//button[@id='submit']"}
```

#### Common Causes

| Cause | Description | Likelihood |
|-------|-------------|------------|
| **Wrong Locator** | The locator strategy or value is incorrect | High |
| **Element Not Loaded** | Page/element hasn't finished loading | High |
| **Element in iframe** | Element exists inside an iframe that isn't switched to | Medium |
| **Dynamic Content** | Element is rendered by JavaScript after page load | Medium |
| **Element Removed** | Element was present but removed from DOM | Low |

#### Solutions

**1. Verify the Locator**

Use browser DevTools (F12) to verify the element exists with the specified locator:

```javascript
// In browser console
document.querySelector("button[id='submit']")  // CSS
document.evaluate("//button[@id='submit']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue  // XPath
```

**2. Add Explicit Wait**

Replace immediate element access with an explicit wait:

```java
// Instead of immediate access
WebElement element = driver.findElement(By.id("submit"));

// Use explicit wait
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 10);
WebElement element = wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("submit")));
```

*Reference: src/main/java/com/testinium/step_definitions/LoginSD.java:87, 197*

**3. Check for iframes**

If the element is inside an iframe, switch to it first:

```java
// Switch to iframe by name, id, or index
driver.switchTo().frame("iframeName");
// Or by WebElement
driver.switchTo().frame(driver.findElement(By.tagName("iframe")));
// Find element inside iframe
WebElement element = driver.findElement(By.id("submit"));
// Switch back to main content
driver.switchTo().defaultContent();
```

**4. Use PageFactory with @FindBy**

The framework uses PageFactory for element location, which provides lazy initialization:

```java
// Page Object with @FindBy (LoginP.java pattern)
@FindBy(xpath = "//button[.='Log in']")
public WebElement button;
```

*Source: src/main/java/com/testinium/pages/LoginP.java*

---

### StaleElementReferenceException

The `StaleElementReferenceException` occurs when a previously located element is no longer attached to the DOM. The element reference becomes "stale" after the DOM is modified.

#### Error Signature

```
org.openqa.selenium.StaleElementReferenceException: stale element reference: element is not attached to the page document
```

#### Common Causes

| Cause | Description |
|-------|-------------|
| **Page Refresh** | The page was refreshed after locating the element |
| **DOM Update** | JavaScript modified the DOM structure |
| **Element Re-rendered** | A framework (React, Angular, Vue) re-rendered the component |
| **Navigation** | User navigated away and back to the page |
| **AJAX Update** | Asynchronous content update replaced the element |

#### Solutions

**1. Re-locate the Element**

After any action that might modify the DOM, re-locate the element:

```java
// Before page action
WebElement element = driver.findElement(By.id("dynamicContent"));
element.click();  // This might trigger DOM change

// Re-locate after DOM change
element = driver.findElement(By.id("dynamicContent"));
element.getText();  // Now safe to use
```

**2. Use Explicit Wait After Page Changes**

```java
// After clicking that triggers page update
loginP.button.click();

// Wait for new state before interacting
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 3);
wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:197*

**3. Use Retry Logic**

Implement a retry mechanism for operations that might fail due to stale elements:

```java
public WebElement waitForElement(By locator, int attempts) {
    WebElement element = null;
    int count = 0;
    while (count < attempts) {
        try {
            element = driver.findElement(locator);
            break;
        } catch (StaleElementReferenceException e) {
            count++;
            try { Thread.sleep(500); } catch (InterruptedException ie) {}
        }
    }
    return element;
}
```

---

### TimeoutException

The `TimeoutException` is thrown when an explicit wait condition is not met within the specified timeout period.

#### Error Signature

```
org.openqa.selenium.TimeoutException: Expected condition failed: waiting for visibility of element located by By.id: dashboard (tried for 3 second(s) with 500 milliseconds interval)
```

#### Common Causes

| Cause | Description |
|-------|-------------|
| **Slow Page Load** | Network or server latency exceeds timeout |
| **Element Never Appears** | The expected element is not present on this page state |
| **Wrong Expected Condition** | Using the wrong ExpectedCondition for the situation |
| **Insufficient Timeout** | The configured timeout is too short for the operation |
| **Wrong Locator** | The locator doesn't match the actual element |

#### Solutions

**1. Increase Timeout**

If the element appears but slowly, increase the wait timeout:

```java
// Current: 3 seconds (may be too short)
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 3);

// Increased timeout for slow pages
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 15);
```

*Reference: src/main/java/com/testinium/step_definitions/LoginSD.java:87*

**2. Verify Element Exists**

First confirm the element actually exists on the page using browser DevTools, then verify your locator matches.

**3. Check Expected Condition**

Use the appropriate ExpectedCondition:

```java
// For elements that need to be visible
wait.until(ExpectedConditions.visibilityOf(element));

// For elements that just need to exist in DOM
wait.until(ExpectedConditions.presenceOfElementLocated(By.id("hidden-element")));

// For elements that need to be clickable
wait.until(ExpectedConditions.elementToBeClickable(element));
```

**4. Add Debugging Information**

Catch the exception and add context:

```java
try {
    wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
} catch (TimeoutException e) {
    System.out.println("Current page title: " + Driver.getDriver().getTitle());
    System.out.println("Current URL: " + Driver.getDriver().getCurrentUrl());
    throw e;
}
```

---

### SessionNotCreatedException

The `SessionNotCreatedException` is thrown when WebDriver cannot create a new browser session. This typically indicates driver or browser installation issues.

#### Error Signature

```
org.openqa.selenium.SessionNotCreatedException: Could not start a new session. Response code 500. Message: session not created: This version of ChromeDriver only supports Chrome version 114
```

#### Common Causes

| Cause | Description |
|-------|-------------|
| **Version Mismatch** | Browser and driver versions are incompatible |
| **Driver Not Installed** | WebDriver executable is missing or not in PATH |
| **Browser Not Installed** | The browser is not installed on the system |
| **Port Conflict** | Another process is using the driver's port |
| **Permissions** | Insufficient permissions to execute driver |

#### Solutions

**1. Use WebDriverManager (Recommended)**

The framework uses WebDriverManager for automatic driver management:

```java
// Chrome driver auto-setup
WebDriverManager.chromedriver().setup();
driverPool.set(new ChromeDriver());
```

*Source: src/main/java/com/testinium/utilities/Driver.java:152-153*

**2. Verify Browser Installation**

Ensure the browser is properly installed:

```bash
# Check Chrome version (Linux/Mac)
google-chrome --version

# Check Firefox version
firefox --version
```

**3. Clear WebDriverManager Cache**

If drivers become stale, clear the cache:

```bash
# Default cache location
rm -rf ~/.cache/selenium
rm -rf ~/.m2/repository/.cache/selenium
```

**4. Force Driver Version**

If automatic detection fails, specify the version:

```java
WebDriverManager.chromedriver().browserVersion("120").setup();
```

**5. Check for Port Conflicts**

Ensure no zombie driver processes are running:

```bash
# Kill stale chromedriver processes (Linux/Mac)
pkill -f chromedriver
pkill -f geckodriver

# Windows
taskkill /F /IM chromedriver.exe
taskkill /F /IM geckodriver.exe
```

---

## Locator Issues

Locator problems are among the most common causes of test failures. The Testinium-QA framework uses Selenium's `@FindBy` annotations for element location, and understanding locator best practices is essential for creating reliable tests.

### Brittle XPath Strategies

**Problem**: Absolute XPath expressions break when the DOM structure changes, even for minor UI updates.

#### Signs of Brittle XPath

```java
// AVOID: Absolute XPath - extremely brittle
@FindBy(xpath = "/html/body/div[1]/div[2]/form/div[3]/button[1]")
public WebElement submitButton;

// AVOID: Index-dependent XPath - breaks with new elements
@FindBy(xpath = "//div[4]/table/tr[2]/td[3]")
public WebElement dataCell;
```

#### Better Alternatives

```java
// GOOD: Relative XPath with meaningful attributes
@FindBy(xpath = "//button[@type='submit']")
public WebElement submitButton;

// GOOD: Relative XPath with text content (used in framework)
@FindBy(xpath = "//button[.='Log in']")
public WebElement button;

// BEST: CSS selector when possible
@FindBy(css = "button[type='submit']")
public WebElement submitButton;
```

*Reference: src/main/java/com/testinium/pages/LoginP.java - uses relative XPath `//button[.='Log in']`*

#### Framework Examples of Good vs. Problematic Locators

| Type | Example | Reliability |
|------|---------|-------------|
| ID-based | `@FindBy(id = "oe_main_menu_navbar")` | High |
| Name-based | `@FindBy(name = "login")` | High |
| Class-based | `@FindBy(className = "alert")` | Medium |
| Text XPath | `@FindBy(xpath = "//button[.='Log in']")` | Medium |
| Absolute XPath | `@FindBy(xpath = "/html/body/div/...")` | Low |

*Source: src/main/java/com/testinium/pages/LoginP.java*

---

### Dynamic ID Handling

**Problem**: Odoo and many modern web applications generate dynamic IDs that include session-specific or random values, making them unreliable for locators.

#### Signs of Dynamic IDs

```html
<!-- Dynamic IDs - change on every page load -->
<input id="o_field_input_123">
<div id="react-select-5-option-2">
<button id="btn_a7f3d2e1">
```

#### Solutions

**1. Use Alternative Attributes**

```java
// Instead of dynamic ID
@FindBy(id = "o_field_input_123")  // AVOID - dynamic

// Use name attribute
@FindBy(name = "login")  // GOOD - stable

// Use data attributes
@FindBy(css = "[data-testid='login-input']")  // BEST - designed for testing
```

**2. Use Structural Relationships**

```java
// Find by label association
@FindBy(xpath = "//label[text()='Email']//following-sibling::input")
public WebElement emailInput;

// Find by parent/ancestor context
@FindBy(xpath = "//form[@id='login-form']//input[@type='email']")
public WebElement emailInput;
```

**3. Use Contains for Partial IDs**

```java
// Match partial static portion of ID
@FindBy(xpath = "//input[contains(@id, 'field_input')]")
public WebElement fieldInput;

// CSS alternative
@FindBy(css = "input[id*='field_input']")
public WebElement fieldInput;
```

---

### Text-Based Locator Reliability

**Problem**: Text-based locators can break when UI text changes due to internationalization, A/B testing, or content updates.

#### Considerations

```java
// Text might change
@FindBy(xpath = "//button[text()='Submit']")  // Exact match
@FindBy(xpath = "//button[contains(text(), 'Submit')]")  // Contains

// More reliable - structural/attribute based
@FindBy(css = "button[type='submit']")
@FindBy(xpath = "//form//button[@type='submit']")
```

#### When Text Locators Are Acceptable

- Login/Logout buttons (rarely change)
- Menu navigation items
- Verification of displayed content
- When no better alternative exists

*Framework usage: `@FindBy(xpath = "//button[.='Log in']")` is acceptable as login button text is stable.*

*Source: src/main/java/com/testinium/pages/LoginP.java*

---

### Locator Selection Best Practices

Follow this priority order when choosing locators:

```
┌─────────────────────────────────────────────────────┐
│ LOCATOR SELECTION PRIORITY (Most to Least Reliable) │
├─────────────────────────────────────────────────────┤
│ 1. id           - Unique, fastest, most reliable    │
│ 2. name         - Often unique within forms         │
│ 3. css selector - Flexible, performant              │
│ 4. linkText     - Good for anchor elements          │
│ 5. xpath        - Most flexible, use as last resort │
└─────────────────────────────────────────────────────┘
```

#### Framework Locator Examples

```java
// PRIORITY 1: ID (fastest, most reliable)
@FindBy(id = "oe_main_menu_navbar")
public WebElement dashboard;

// PRIORITY 2: Name (good for form elements)
@FindBy(name = "login")
public WebElement inputEmail;

@FindBy(name = "password")
public WebElement inputPassword;

// PRIORITY 3: CSS Selector (flexible, performant)
@FindBy(css = ".alert-danger")
public WebElement errorMessage;

// PRIORITY 4: Class Name (simple CSS)
@FindBy(className = "alert")
public WebElement alertErrorMessage;

// PRIORITY 5: XPath (use relative, with meaningful attributes)
@FindBy(xpath = "//button[.='Log in']")
public WebElement button;
```

*Source: src/main/java/com/testinium/pages/LoginP.java*

---

## Timing Problems

Synchronization issues are the leading cause of flaky tests. The Testinium-QA framework configures a default implicit wait, but understanding when to use explicit waits is crucial.

### Implicit Wait vs Explicit Wait

The framework configures a **10-second implicit wait** globally:

```java
driverPool.get().manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
```

*Source: src/main/java/com/testinium/utilities/Driver.java:155*

#### Comparison

| Aspect | Implicit Wait | Explicit Wait |
|--------|---------------|---------------|
| **Scope** | Global - all findElement calls | Specific - per element/condition |
| **Timeout** | Fixed (10s in this framework) | Configurable per wait |
| **Conditions** | Element presence only | Multiple conditions available |
| **Performance** | Can slow down failure detection | Fails fast on wrong locator |
| **Best For** | Basic element presence | Specific conditions (clickable, visible) |

#### Recommendations

```java
// Implicit wait is already configured globally (Driver.java:155)
// Use explicit waits for specific conditions:

WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 3);

// Wait for visibility (element in DOM AND visible)
wait.until(ExpectedConditions.visibilityOf(element));

// Wait for clickability (visible AND enabled)
wait.until(ExpectedConditions.elementToBeClickable(element));
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:87, 197*

---

### Thread.sleep Anti-Pattern

**Problem**: Using `Thread.sleep()` introduces fixed delays that are either too short (causing failures) or too long (wasting time).

#### Why Thread.sleep is Problematic

```java
// AVOID: Thread.sleep anti-pattern
loginP.button.click();
Thread.sleep(3000);  // Always waits 3 seconds, even if page loads in 500ms
loginP.dashboard.click();
```

**Issues**:
- Wastes time when page loads quickly
- Fails when page loads slowly
- No condition checking
- Not responsive to actual page state

#### Better Alternative: Explicit Waits

```java
// GOOD: Explicit wait - waits only as long as needed
loginP.button.click();

WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 10);
wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));

loginP.dashboard.click();
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:197*

#### When Thread.sleep Might Be Acceptable

- Debugging: Temporarily slow down to observe behavior
- Animation completion: When no better condition exists
- Third-party service delays: Rate limiting, API cooldowns

```java
// Acceptable use case - debugging only
Thread.sleep(1000);  // TODO: Remove before commit
```

---

### WebDriverWait Usage

The framework uses `WebDriverWait` for explicit synchronization:

```java
// Create wait instance with timeout
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 3);

// Wait for condition
wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:87, 197*

#### Common WebDriverWait Patterns

```java
// Wait with custom timeout
WebDriverWait shortWait = new WebDriverWait(driver, 3);
WebDriverWait longWait = new WebDriverWait(driver, 30);

// Wait with polling interval
WebDriverWait wait = new WebDriverWait(driver, 10);
wait.pollingEvery(Duration.ofMillis(250));

// Wait ignoring specific exceptions
wait.ignoring(StaleElementReferenceException.class);
```

#### Reusable Wait Utility Example

```java
public class WaitUtils {
    public static WebElement waitForVisibility(WebElement element, int seconds) {
        WebDriverWait wait = new WebDriverWait(Driver.getDriver(), seconds);
        return wait.until(ExpectedConditions.visibilityOf(element));
    }
    
    public static void waitForClickable(WebElement element, int seconds) {
        WebDriverWait wait = new WebDriverWait(Driver.getDriver(), seconds);
        wait.until(ExpectedConditions.elementToBeClickable(element));
    }
}
```

---

### ExpectedConditions Catalog

The `ExpectedConditions` class provides many predefined conditions for use with `WebDriverWait`:

#### Element Visibility Conditions

| Condition | Use Case |
|-----------|----------|
| `visibilityOf(element)` | Element is in DOM and visible |
| `visibilityOfElementLocated(locator)` | Find and wait for visibility |
| `visibilityOfAllElements(elements)` | All elements in list are visible |
| `invisibilityOf(element)` | Element is not visible (for loaders) |

#### Element Presence Conditions

| Condition | Use Case |
|-----------|----------|
| `presenceOfElementLocated(locator)` | Element exists in DOM |
| `presenceOfAllElementsLocatedBy(locator)` | Multiple elements exist |
| `numberOfElementsToBeMoreThan(locator, n)` | At least n elements exist |

#### Element State Conditions

| Condition | Use Case |
|-----------|----------|
| `elementToBeClickable(element)` | Visible and enabled |
| `elementToBeSelected(element)` | Checkbox/option is selected |
| `elementSelectionStateToBe(element, bool)` | Specific selection state |
| `stalenessOf(element)` | Element is no longer attached |

#### Page/Frame Conditions

| Condition | Use Case |
|-----------|----------|
| `titleIs(title)` | Exact title match |
| `titleContains(text)` | Title contains text |
| `urlContains(text)` | URL contains text |
| `frameToBeAvailableAndSwitchToIt(locator)` | Switch to iframe when ready |
| `alertIsPresent()` | JavaScript alert is displayed |

#### Usage Examples

```java
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 10);

// Wait for page title after login
wait.until(ExpectedConditions.titleIs("Odoo"));

// Wait for loading spinner to disappear
wait.until(ExpectedConditions.invisibilityOfElementLocated(By.className("loading")));

// Wait for element to be clickable
WebElement button = wait.until(ExpectedConditions.elementToBeClickable(loginP.button));
```

---

### Race Conditions and Synchronization

**Problem**: Tests fail intermittently when multiple operations compete for resources or when timing varies between test runs.

#### Common Race Condition Scenarios

1. **Click before clickable**: Element exists but not yet interactive
2. **Read before write**: Checking value before it's updated
3. **Parallel element modification**: Multiple scripts updating DOM
4. **Page transition**: Interacting during navigation

#### Solutions

**1. Explicit Wait Before Action**

```java
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 10);

// Wait for clickability before clicking
wait.until(ExpectedConditions.elementToBeClickable(element)).click();

// Wait for value before reading
wait.until(ExpectedConditions.textToBePresentInElement(element, "expected"));
String text = element.getText();
```

**2. Fluent Wait for Custom Polling**

```java
Wait<WebDriver> fluentWait = new FluentWait<>(Driver.getDriver())
    .withTimeout(Duration.ofSeconds(30))
    .pollingEvery(Duration.ofMillis(500))
    .ignoring(NoSuchElementException.class)
    .ignoring(StaleElementReferenceException.class);

WebElement element = fluentWait.until(driver -> driver.findElement(By.id("dynamic")));
```

**3. Retry Pattern**

```java
public void clickWithRetry(WebElement element, int maxAttempts) {
    int attempts = 0;
    while (attempts < maxAttempts) {
        try {
            new WebDriverWait(Driver.getDriver(), 5)
                .until(ExpectedConditions.elementToBeClickable(element))
                .click();
            return;
        } catch (StaleElementReferenceException | ElementClickInterceptedException e) {
            attempts++;
            if (attempts >= maxAttempts) throw e;
        }
    }
}
```

---

## Browser Driver Issues

Browser driver management can be challenging due to frequent browser updates and driver version compatibility requirements.

### WebDriverManager Configuration

The framework uses **WebDriverManager** to automatically download and configure browser drivers:

```java
// Chrome configuration
WebDriverManager.chromedriver().setup();
driverPool.set(new ChromeDriver());

// Firefox configuration (note: there's a bug - see below)
WebDriverManager.chromedriver().setup();  // BUG: Should be firefoxdriver()
driverPool.set(new FirefoxDriver());
```

*Source: src/main/java/com/testinium/utilities/Driver.java:152-159*

#### How WebDriverManager Works

1. Detects browser version installed on the system
2. Downloads the compatible driver version
3. Sets system property to driver path
4. Caches drivers for future use

#### Troubleshooting WebDriverManager

**Issue: Driver not downloading**

```bash
# Check network connectivity to GitHub (driver source)
curl -I https://github.com/nicku/chromedriver/releases

# Clear cache and force re-download
rm -rf ~/.cache/selenium
rm -rf ~/.m2/repository/.cache/selenium
```

**Issue: Wrong driver version**

```java
// Force specific version
WebDriverManager.chromedriver().browserVersion("120").setup();

// Use driver for specific browser path
WebDriverManager.chromedriver().browserPath("/opt/chrome/chrome").setup();
```

---

### Chrome Driver Issues

#### Common Chrome Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Version mismatch | `session not created: This version of ChromeDriver only supports Chrome version X` | Update browser or use WebDriverManager |
| Sandbox error | `Chrome failed to start: sandbox_linux.cc` | Add `--no-sandbox` argument |
| Headless crash | `DevToolsActivePort file doesn't exist` | Add `--disable-dev-shm-usage` |
| GPU issues | `GPU process isn't usable` | Add `--disable-gpu` |

#### Chrome Arguments for Common Problems

```java
ChromeOptions options = new ChromeOptions();

// For CI/CD environments
options.addArguments("--no-sandbox");
options.addArguments("--disable-dev-shm-usage");
options.addArguments("--disable-gpu");

// For headless execution
options.addArguments("--headless");

// For window sizing
options.addArguments("--window-size=1920,1080");

// For certificate errors
options.addArguments("--ignore-certificate-errors");

WebDriverManager.chromedriver().setup();
driverPool.set(new ChromeDriver(options));
```

#### Updating Chrome

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install --only-upgrade google-chrome-stable

# macOS (Homebrew)
brew upgrade --cask google-chrome

# Verify version
google-chrome --version
```

---

### Firefox Driver Issues

**IMPORTANT**: The current framework has a **bug in Firefox configuration**:

```java
// BUG in Driver.java:158 - uses chromedriver for Firefox!
case "firefox":
    WebDriverManager.chromedriver().setup();  // Should be firefoxdriver()
    driverPool.set(new FirefoxDriver());
```

*Source: src/main/java/com/testinium/utilities/Driver.java:158*

#### Corrected Firefox Configuration

```java
case "firefox":
    WebDriverManager.firefoxdriver().setup();  // CORRECT
    driverPool.set(new FirefoxDriver());
    driverPool.get().manage().window().maximize();
    driverPool.get().manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    break;
```

#### Common Firefox Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Geckodriver not found | `WebDriverException: geckodriver executable not found` | Install geckodriver via WebDriverManager |
| Profile issues | `Failed to start: unexpected browser quit` | Create fresh profile |
| Marionette error | `connection refused to host: 127.0.0.1` | Check Firefox installation |

#### Firefox Options

```java
FirefoxOptions options = new FirefoxOptions();

// Headless mode
options.addArguments("--headless");

// Custom profile
FirefoxProfile profile = new FirefoxProfile();
profile.setPreference("browser.download.folderList", 2);
profile.setPreference("browser.download.dir", "/tmp/downloads");
options.setProfile(profile);

// For CI environments
options.addArguments("--width=1920");
options.addArguments("--height=1080");

WebDriverManager.firefoxdriver().setup();
driverPool.set(new FirefoxDriver(options));
```

---

### Headless Mode Configuration

Headless mode runs the browser without a visible UI, useful for CI/CD environments.

**Note**: The current framework doesn't support headless mode out of the box. This requires modifying `Driver.java`.

#### Adding Headless Support

```java
// Enhanced browser configuration with headless support
String browserType = ConfigurationReader.getProperty("browser");
String headless = ConfigurationReader.getProperty("headless");  // "true" or "false"

switch(browserType) {
    case "chrome":
        ChromeOptions chromeOptions = new ChromeOptions();
        if ("true".equalsIgnoreCase(headless)) {
            chromeOptions.addArguments("--headless");
            chromeOptions.addArguments("--disable-gpu");
            chromeOptions.addArguments("--window-size=1920,1080");
        }
        WebDriverManager.chromedriver().setup();
        driverPool.set(new ChromeDriver(chromeOptions));
        break;
        
    case "firefox":
        FirefoxOptions firefoxOptions = new FirefoxOptions();
        if ("true".equalsIgnoreCase(headless)) {
            firefoxOptions.addArguments("--headless");
            firefoxOptions.addArguments("--width=1920");
            firefoxOptions.addArguments("--height=1080");
        }
        WebDriverManager.firefoxdriver().setup();
        driverPool.set(new FirefoxDriver(firefoxOptions));
        break;
}
```

---

### Browser Capability Settings

#### Chrome Capabilities

```java
ChromeOptions options = new ChromeOptions();

// Performance and stability
options.addArguments("--disable-extensions");
options.addArguments("--disable-infobars");
options.addArguments("--disable-notifications");

// Logging
options.setExperimentalOption("excludeSwitches", 
    Collections.singletonList("enable-logging"));

// Proxy configuration
options.addArguments("--proxy-server=http://proxy.example.com:8080");

// Download directory
Map<String, Object> prefs = new HashMap<>();
prefs.put("download.default_directory", "/tmp/downloads");
prefs.put("download.prompt_for_download", false);
options.setExperimentalOption("prefs", prefs);
```

#### Firefox Capabilities

```java
FirefoxOptions options = new FirefoxOptions();
FirefoxProfile profile = new FirefoxProfile();

// Download configuration
profile.setPreference("browser.download.folderList", 2);
profile.setPreference("browser.download.dir", "/tmp/downloads");
profile.setPreference("browser.helperApps.neverAsk.saveToDisk", 
    "application/pdf,application/octet-stream");

// Disable notifications
profile.setPreference("dom.webnotifications.enabled", false);

options.setProfile(profile);
```

---

## Configuration Problems

Configuration issues can cause tests to fail before they even start. The framework relies on `configuration.properties` for runtime settings.

### Configuration File Not Found

**Error Signature**:

```
File is not found in the ConfigurationReader class
java.io.FileNotFoundException: configuration.properties (No such file or directory)
```

*Source: src/main/java/com/testinium/utilities/ConfigurationReader.java:91-92*

#### Common Causes

| Cause | Description |
|-------|-------------|
| **File Missing** | `configuration.properties` doesn't exist at project root |
| **Wrong Location** | File exists but in wrong directory |
| **Wrong Working Directory** | Tests run from unexpected directory |
| **CI/CD Build Issue** | File not copied to build output |

#### Solutions

**1. Verify File Existence**

```bash
# Check if file exists at project root
ls -la configuration.properties

# Check current directory
pwd
```

**2. Create Configuration File**

Create `configuration.properties` at project root with required properties:

```properties
# Required configuration
browser=chrome
web.table.url=https://your-app-url.com/web/login

# Optional credentials
username=testuser@example.com
password=testpassword
```

**3. Verify Path in Code**

The configuration file path is hardcoded:

```java
FileInputStream file = new FileInputStream("configuration.properties");
```

*Source: src/main/java/com/testinium/utilities/ConfigurationReader.java:83*

This expects the file at the project root (where `pom.xml` is located).

**4. For CI/CD Environments**

Ensure `configuration.properties` is:
- Added to version control (with placeholder values)
- Copied to build directory
- Created dynamically with environment-specific values

```xml
<!-- Maven resources plugin ensures properties file is available -->
<build>
    <resources>
        <resource>
            <directory>.</directory>
            <includes>
                <include>configuration.properties</include>
            </includes>
        </resource>
    </resources>
</build>
```

---

### Missing Required Properties

**Error Signature**:

```
java.lang.NullPointerException: Cannot invoke "String.equals(Object)" because the return value of "com.testinium.utilities.ConfigurationReader.getProperty(String)" is null
```

#### Required Properties

| Property | Usage Location | Purpose |
|----------|----------------|---------|
| `browser` | `Driver.java:148` | Browser type selection |
| `web.table.url` | `LoginSD.java:108` | Application URL |

#### Solutions

**1. Add Missing Property**

```properties
# Ensure all required properties are present
browser=chrome
web.table.url=https://your-odoo-instance.com/web/login
```

**2. Add Default Value Handling**

Modify code to provide defaults:

```java
// In ConfigurationReader or calling code
public static String getProperty(String keyword) {
    String value = properties.getProperty(keyword);
    if (value == null) {
        System.err.println("WARNING: Property '" + keyword + "' not found in configuration.properties");
    }
    return value;
}

// Or with default value
public static String getPropertyOrDefault(String keyword, String defaultValue) {
    String value = properties.getProperty(keyword);
    return (value != null) ? value : defaultValue;
}
```

**3. Validate Configuration at Startup**

Add validation method to check required properties:

```java
public static void validateRequiredProperties() {
    String[] required = {"browser", "web.table.url"};
    List<String> missing = new ArrayList<>();
    
    for (String prop : required) {
        if (getProperty(prop) == null || getProperty(prop).isEmpty()) {
            missing.add(prop);
        }
    }
    
    if (!missing.isEmpty()) {
        throw new RuntimeException("Missing required properties: " + missing);
    }
}
```

---

### Environment-Specific Configuration

**Problem**: Tests need different configuration for different environments (local, QA, staging, production).

#### Solution 1: Multiple Properties Files

```
project-root/
├── configuration.properties          # Default/local
├── configuration-qa.properties       # QA environment
├── configuration-staging.properties  # Staging environment
└── configuration-prod.properties     # Production environment
```

Modify `ConfigurationReader` to support environment selection:

```java
static {
    try {
        String env = System.getProperty("env", "local");
        String fileName = "local".equals(env) 
            ? "configuration.properties" 
            : "configuration-" + env + ".properties";
        
        FileInputStream file = new FileInputStream(fileName);
        properties.load(file);
        file.close();
        
        System.out.println("Loaded configuration from: " + fileName);
    } catch (IOException e) {
        System.out.println("Configuration file not found: " + e.getMessage());
        e.printStackTrace();
    }
}
```

Usage:
```bash
mvn test -Denv=qa
```

#### Solution 2: System Property Overrides

```java
public static String getProperty(String keyword) {
    // Check system property first (allows runtime override)
    String systemValue = System.getProperty(keyword);
    if (systemValue != null && !systemValue.isEmpty()) {
        return systemValue;
    }
    return properties.getProperty(keyword);
}
```

Usage:
```bash
mvn test -Dbrowser=firefox -Dweb.table.url=https://staging.example.com
```

#### Solution 3: Environment Variables

```java
public static String getProperty(String keyword) {
    // Check environment variable (convert . to _ for env var naming)
    String envKey = keyword.toUpperCase().replace(".", "_");
    String envValue = System.getenv(envKey);
    if (envValue != null && !envValue.isEmpty()) {
        return envValue;
    }
    return properties.getProperty(keyword);
}
```

Usage:
```bash
export BROWSER=firefox
export WEB_TABLE_URL=https://staging.example.com
mvn test
```

---

## Screenshot Capture for Debugging

Screenshots are invaluable for debugging test failures, especially in CI/CD environments where you can't see the browser.

### Automatic Capture on Failure

The framework automatically captures screenshots when scenarios fail:

```java
@After
public void teardownScenario(Scenario scenario){
    if(scenario.isFailed()){
        byte [] screenshot = ((TakesScreenshot) Driver.getDriver()).getScreenshotAs(OutputType.BYTES);
        scenario.attach(screenshot, "image/png", scenario.getName());
    }
    Driver.closeDriver();
}
```

*Source: src/main/java/com/testinium/step_definitions/Hooks.java:115-122*

#### How It Works

1. **`@After` Hook**: Runs after every scenario
2. **Failure Check**: `scenario.isFailed()` returns `true` if scenario failed
3. **Screenshot Capture**: `getScreenshotAs(OutputType.BYTES)` captures current browser state
4. **Attach to Report**: `scenario.attach()` embeds image in Cucumber report
5. **Driver Cleanup**: `closeDriver()` always runs, ensuring resources are freed

#### Viewing Screenshots

Screenshots are embedded in Cucumber reports:
- **HTML Report**: `target/cucumber-reports.html` - Click on failed scenario to see screenshot
- **JSON Report**: `target/cucumber.json` - Contains base64-encoded image data

---

### Manual Screenshot Capture

For debugging during development, you can capture screenshots manually:

```java
// Capture screenshot to file
public void takeScreenshot(String fileName) {
    TakesScreenshot ts = (TakesScreenshot) Driver.getDriver();
    File source = ts.getScreenshotAs(OutputType.FILE);
    
    try {
        File destination = new File("screenshots/" + fileName + ".png");
        FileUtils.copyFile(source, destination);
        System.out.println("Screenshot saved: " + destination.getAbsolutePath());
    } catch (IOException e) {
        System.err.println("Failed to save screenshot: " + e.getMessage());
    }
}

// Usage in step definition
@When("I debug the current state")
public void debugCurrentState() {
    takeScreenshot("debug_" + System.currentTimeMillis());
}
```

#### Capture Specific Element

```java
public void takeElementScreenshot(WebElement element, String fileName) {
    File source = element.getScreenshotAs(OutputType.FILE);
    try {
        FileUtils.copyFile(source, new File("screenshots/" + fileName + ".png"));
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

#### Capture Full Page (Scrolling)

For pages longer than the viewport:

```java
public void takeFullPageScreenshot(String fileName) {
    JavascriptExecutor js = (JavascriptExecutor) Driver.getDriver();
    
    // Get full page dimensions
    long fullHeight = (Long) js.executeScript("return document.body.scrollHeight");
    long viewportHeight = (Long) js.executeScript("return window.innerHeight");
    
    // Scroll and capture logic (requires image stitching library)
    // Consider using AShot library for full-page screenshots
}
```

---

### Screenshot File Location

#### Default Location (Cucumber Reports)

Screenshots captured by `Hooks.java` are embedded in:
- `target/cucumber-reports.html`
- `target/cucumber.json`

#### Custom Screenshot Directory

Create a dedicated screenshot directory:

```java
// In step definition or utility class
private static final String SCREENSHOT_DIR = "target/screenshots";

static {
    File dir = new File(SCREENSHOT_DIR);
    if (!dir.exists()) {
        dir.mkdirs();
    }
}

public void saveScreenshot(String name) {
    String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
    String fileName = SCREENSHOT_DIR + "/" + name + "_" + timestamp + ".png";
    
    File src = ((TakesScreenshot) Driver.getDriver()).getScreenshotAs(OutputType.FILE);
    try {
        FileUtils.copyFile(src, new File(fileName));
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

#### Clean Screenshots Between Runs

Add to Maven build or test setup:

```xml
<!-- In pom.xml - clean plugin -->
<plugin>
    <artifactId>maven-clean-plugin</artifactId>
    <configuration>
        <filesets>
            <fileset>
                <directory>target/screenshots</directory>
            </fileset>
        </filesets>
    </configuration>
</plugin>
```

---

## Debugging Tips

Effective debugging strategies help identify issues quickly and reduce time spent troubleshooting.

### IDE Breakpoints and Debugging

#### Setting Breakpoints in IntelliJ IDEA

1. Click in the left gutter next to the code line
2. Run test in Debug mode (right-click → Debug)
3. Use debugging controls:
   - **Step Over (F8)**: Execute current line
   - **Step Into (F7)**: Enter method call
   - **Step Out (Shift+F8)**: Exit current method
   - **Resume (F9)**: Continue to next breakpoint

#### Useful Breakpoint Locations

| Location | Purpose |
|----------|---------|
| `Driver.java:143` | Inspect driver creation |
| `Driver.java:148` | Check browser type read from config |
| Step definition method start | Verify step is matched |
| Before `click()` calls | Verify element state |
| Before assertions | Inspect actual values |

#### Evaluate Expressions

While paused at breakpoint:
- Use **Evaluate Expression (Alt+F8)** to run code
- Check element attributes: `element.getAttribute("class")`
- Check page state: `Driver.getDriver().getTitle()`
- Check element visibility: `element.isDisplayed()`

#### Conditional Breakpoints

Right-click breakpoint → Add condition:
```java
// Only break when specific scenario
scenarioName.contains("Login")

// Only break on specific data
username.equals("invalid@test.com")
```

---

### Console Logging Strategies

#### Strategic Print Statements

```java
@Given("User is on the login page")
public void user_is_on_the_login_page() {
    String url = ConfigurationReader.getProperty("web.table.url");
    System.out.println("[DEBUG] Navigating to URL: " + url);
    
    Driver.getDriver().get(url);
    
    System.out.println("[DEBUG] Current page title: " + Driver.getDriver().getTitle());
    System.out.println("[DEBUG] Current URL: " + Driver.getDriver().getCurrentUrl());
}

@When("User enters {string} username")
public void user_enters_username(String username) {
    System.out.println("[DEBUG] Entering username: " + username);
    System.out.println("[DEBUG] Input field displayed: " + loginP.inputEmail.isDisplayed());
    
    loginP.inputEmail.sendKeys(username);
    
    System.out.println("[DEBUG] Input field value: " + loginP.inputEmail.getAttribute("value"));
}
```

#### Using Java Logging

```java
import java.util.logging.Logger;
import java.util.logging.Level;

public class LoginSD {
    private static final Logger logger = Logger.getLogger(LoginSD.class.getName());
    
    @Given("User is on the login page")
    public void user_is_on_the_login_page() {
        String url = ConfigurationReader.getProperty("web.table.url");
        logger.info("Navigating to: " + url);
        
        Driver.getDriver().get(url);
        
        logger.fine("Page title: " + Driver.getDriver().getTitle());
    }
}
```

#### Conditional Logging

```java
private static final boolean DEBUG = Boolean.parseBoolean(
    System.getProperty("debug", "false")
);

private void debug(String message) {
    if (DEBUG) {
        System.out.println("[DEBUG] " + message);
    }
}
```

Run with: `mvn test -Ddebug=true`

---

### Cucumber Report Analysis

#### HTML Report Location

Reports are generated at:
- `target/cucumber-reports.html` - Main HTML report
- `target/cucumber.json` - JSON data for processing

*Source: CukesRunner.java @CucumberOptions plugins configuration*

#### What to Look For

| Report Section | Information |
|----------------|-------------|
| **Summary** | Pass/fail counts, duration |
| **Feature** | High-level feature status |
| **Scenario** | Individual test results |
| **Step** | Which specific step failed |
| **Stack Trace** | Error details and location |
| **Screenshot** | Visual state at failure |

#### Reading Stack Traces

```
org.openqa.selenium.NoSuchElementException: no such element
    at org.openqa.selenium.support.FindBy...
    at com.testinium.pages.LoginP.<init>(LoginP.java:10)
    at com.testinium.step_definitions.LoginSD.user_enters_username(LoginSD.java:27)
```

Key information:
1. **Exception type**: `NoSuchElementException`
2. **Root cause**: PageFactory initialization
3. **Location**: `LoginSD.java:27`

#### Pretty Report Plugin

The framework uses `me.jvt.cucumber:reporting-plugin` for enhanced HTML reports with:
- Pie charts for pass/fail distribution
- Feature-level grouping
- Tag-based filtering
- Step timing analysis

---

### Browser DevTools Integration

#### Using DevTools During Test Development

1. **Pause test with breakpoint** in IDE
2. **Interact with browser** DevTools (F12):
   - Elements tab: Inspect DOM, verify locators
   - Console tab: Execute JavaScript queries
   - Network tab: Check XHR requests
   - Application tab: Cookies, storage

#### Console Commands for Locator Testing

```javascript
// Test CSS selector
document.querySelector("button[type='submit']")

// Test XPath
document.evaluate("//button[.='Log in']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue

// Test all matches
document.querySelectorAll(".alert")
```

#### Execute JavaScript from Selenium

```java
JavascriptExecutor js = (JavascriptExecutor) Driver.getDriver();

// Get element properties
String innerHTML = (String) js.executeScript(
    "return arguments[0].innerHTML;", element);

// Scroll element into view
js.executeScript("arguments[0].scrollIntoView(true);", element);

// Highlight element for debugging
js.executeScript(
    "arguments[0].style.border='3px solid red';", element);

// Get computed styles
String color = (String) js.executeScript(
    "return window.getComputedStyle(arguments[0]).color;", element);
```

---

### Test Isolation Techniques

**Problem**: Tests depend on each other or leave state that affects subsequent tests.

#### Ensure Clean State

```java
@Before
public void setUp() {
    // Clear cookies before each scenario
    Driver.getDriver().manage().deleteAllCookies();
    
    // Navigate to starting URL
    Driver.getDriver().get(ConfigurationReader.getProperty("web.table.url"));
}

@After
public void tearDown(Scenario scenario) {
    if(scenario.isFailed()){
        byte[] screenshot = ((TakesScreenshot) Driver.getDriver())
            .getScreenshotAs(OutputType.BYTES);
        scenario.attach(screenshot, "image/png", scenario.getName());
    }
    // Always close driver - fresh session per scenario
    Driver.closeDriver();
}
```

*Source: src/main/java/com/testinium/step_definitions/Hooks.java:115-122*

#### Run Single Scenario

Modify runner tags to isolate a test:

```java
@CucumberOptions(
    tags = "@Debug"  // Run only scenarios tagged with @Debug
)
```

Or from command line:
```bash
mvn test -Dcucumber.filter.tags="@Login"
```

#### Independent Test Data

Use unique data per test run:

```java
import com.github.javafaker.Faker;

Faker faker = new Faker();
String uniqueEmail = faker.internet().emailAddress();
String uniqueName = faker.name().fullName();
```

#### Check Prerequisites

```java
@Given("User is logged in as {string}")
public void user_is_logged_in(String userType) {
    // Don't assume previous state - explicitly log in
    Driver.getDriver().get(ConfigurationReader.getProperty("web.table.url"));
    
    // Perform login
    loginP.inputEmail.sendKeys(getCredentials(userType).email);
    loginP.inputPassword.sendKeys(getCredentials(userType).password);
    loginP.button.click();
    
    // Wait and verify login success
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 10);
    wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
}
```

---

## See Also

### Internal Documentation

- [Architecture Overview](ARCHITECTURE.md) - Framework design and component relationships
- [Configuration Guide](CONFIGURATION.md) - Detailed configuration options
- [Extending the Framework](EXTENDING.md) - Adding new page objects and step definitions

### External Resources

#### Selenium Documentation
- [Selenium WebDriver Documentation](https://www.selenium.dev/documentation/webdriver/)
- [WebDriver Waits](https://www.selenium.dev/documentation/webdriver/waits/)
- [Locator Strategies](https://www.selenium.dev/documentation/webdriver/elements/locators/)

#### Cucumber Documentation
- [Cucumber Reference](https://cucumber.io/docs/cucumber/)
- [Cucumber JVM](https://cucumber.io/docs/installation/java/)
- [Gherkin Syntax](https://cucumber.io/docs/gherkin/reference/)

#### WebDriverManager
- [WebDriverManager GitHub](https://github.com/bonigarcia/webdrivermanager)
- [WebDriverManager Documentation](https://bonigarcia.dev/webdrivermanager/)

#### Browser-Specific Resources
- [ChromeDriver Documentation](https://chromedriver.chromium.org/)
- [GeckoDriver Documentation](https://firefox-source-docs.mozilla.org/testing/geckodriver/)

#### Stack Overflow Tags
- [selenium-webdriver](https://stackoverflow.com/questions/tagged/selenium-webdriver)
- [cucumber-java](https://stackoverflow.com/questions/tagged/cucumber-java)
- [webdrivermanager](https://stackoverflow.com/questions/tagged/webdrivermanager)

---

*Document Version: 1.0*
*Last Updated: 2024*
*Framework Version: Testinium-QA with Selenium 3.141.59, Cucumber 7.2.3*
