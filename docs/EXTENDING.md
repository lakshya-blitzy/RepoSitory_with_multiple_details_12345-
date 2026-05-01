# Extending the Testinium-QA Framework

This guide provides comprehensive instructions for extending the Testinium-QA test automation framework. It covers adding new Page Object classes, creating Cucumber step definitions, integrating new test modules, and following best practices for maintainable test automation.

## Table of Contents

- [Introduction](#introduction)
- [Adding a New Page Object](#adding-a-new-page-object)
- [Creating Step Definitions](#creating-step-definitions)
- [Adding New Test Modules](#adding-new-test-modules)
- [Best Practices for Locators](#best-practices-for-locators)
- [Wait Strategy Guidelines](#wait-strategy-guidelines)
- [Feature File Guidelines](#feature-file-guidelines)
- [Testing Your Extensions](#testing-your-extensions)
- [See Also](#see-also)

---

## Introduction

The Testinium-QA framework is designed for extensibility. It follows the **Page Object Model (POM)** design pattern combined with **Cucumber BDD** for testing Odoo/Upgenix web applications. When adding new test coverage, you'll typically:

1. Create a **Page Object** class to encapsulate UI element locators
2. Create a **Step Definition** class to implement test logic
3. Create a **Feature File** with Gherkin scenarios
4. Configure the **Test Runner** to execute your tests

This guide walks through each step with concrete examples drawn from the existing codebase.

---

## Adding a New Page Object

Page Objects represent pages or components of the application under test. They encapsulate all WebElement locators and provide a clean interface for step definitions.

### File Location

All Page Object classes are located in:

```
src/main/java/com/testinium/pages/
```

### Package Declaration

Every Page Object must declare the correct package:

```java
package com.testinium.pages;
```

### Required Imports

A Page Object typically requires these imports:

```java
import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
```

For collections of elements, add:

```java
import java.util.List;
```

### Constructor Pattern

Every Page Object **must** include a constructor that initializes WebElements using `PageFactory`:

```java
public LoginP() {
    PageFactory.initElements(Driver.getDriver(), this);
}
```

*Source: src/main/java/com/testinium/pages/LoginP.java:59-61*

This provides **lazy initialization** - elements are located only when first accessed, improving performance and reducing flaky tests.

### @FindBy Annotation Strategies

The `@FindBy` annotation supports multiple locator strategies. Use them in this priority order:

| Priority | Strategy | Example | Use Case |
|----------|----------|---------|----------|
| 1st | `id` | `@FindBy(id = "oe_main_menu_navbar")` | Most stable, preferred when available |
| 2nd | `name` | `@FindBy(name = "login")` | Form elements, stable for HTML forms |
| 3rd | `css` | `@FindBy(css = ".alert-danger")` | CSS classes and complex selectors |
| 4th | `linkText` | `@FindBy(linkText = "Reset Password")` | Links with unique text |
| 5th | `xpath` | `@FindBy(xpath = "//button[.='Log in']")` | Complex queries, last resort |

#### Examples from the Framework

**Using `name` attribute** (preferred for form inputs):

```java
@FindBy(name = "login")
public WebElement inputEmail;

@FindBy(name = "password")
public WebElement inputPassword;
```

*Source: src/main/java/com/testinium/pages/LoginP.java:77-99*

**Using `id` attribute** (most stable locator):

```java
@FindBy(id = "oe_main_menu_navbar")
public WebElement dashboard;
```

*Source: src/main/java/com/testinium/pages/LoginP.java:166-167*

**Using `className` attribute** (for CSS class-based locators):

```java
@FindBy(className = "alert")
public WebElement alertErrorMessage;
```

*Source: src/main/java/com/testinium/pages/LoginP.java:196-197*

**Using `xpath`** (for complex element queries):

```java
@FindBy(xpath = "//button[.='Log in']")
public WebElement button;

@FindBy(xpath = "//a[.='Reset Password']")
public WebElement resetPass;
```

*Source: src/main/java/com/testinium/pages/LoginP.java:122-142*

### Complete Page Object Template

Use this template when creating a new Page Object:

```java
package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import java.util.List;

/**
 * Page Object representing the [Module Name] page of the Odoo application.
 * <p>
 * This class encapsulates all WebElement locators for the [Module] UI
 * and provides a clean interface for step definitions to interact with.
 * </p>
 * 
 * @see Driver
 * @see PageFactory
 */
public class ModuleNameP {

    /**
     * Constructor initializes all WebElements using PageFactory.
     * Elements are lazily loaded when first accessed.
     */
    public ModuleNameP() {
        PageFactory.initElements(Driver.getDriver(), this);
    }

    // ========== Navigation Elements ==========
    
    /**
     * Main module header/title element.
     * Locator: id attribute (most stable)
     */
    @FindBy(id = "module-header")
    public WebElement moduleHeader;

    // ========== Form Input Elements ==========
    
    /**
     * Primary text input field.
     * Locator: name attribute (form elements)
     */
    @FindBy(name = "input-name")
    public WebElement inputField;

    // ========== Button Elements ==========
    
    /**
     * Primary submit/action button.
     * Locator: xpath with text content (unique button text)
     */
    @FindBy(xpath = "//button[.='Submit']")
    public WebElement submitButton;

    // ========== Feedback Elements ==========
    
    /**
     * Error/success message container.
     * Locator: className (CSS class for alerts)
     */
    @FindBy(className = "alert")
    public WebElement alertMessage;

    // ========== List Elements ==========
    
    /**
     * Collection of table rows or list items.
     * Use List<WebElement> for multiple matching elements.
     */
    @FindBy(css = ".list-item")
    public List<WebElement> listItems;
}
```

### Naming Convention

Follow this naming convention for Page Object files:

```
<ModuleName>P.java
```

Examples:
- `LoginP.java` - Login page
- `ContactsP.java` - Contacts module
- `CrmP.java` - CRM module
- `SalesP.java` - Sales module
- `InventoryP.java` - Inventory module

---

## Creating Step Definitions

Step Definitions connect Gherkin feature file steps to actual Java code that interacts with the application through Page Objects.

### File Location

All Step Definition classes are located in:

```
src/main/java/com/testinium/step_definitions/
```

### Package Declaration

Every Step Definition must declare the correct package:

```java
package com.testinium.step_definitions;
```

### Required Imports

A Step Definition typically requires these imports:

```java
// Page Object import
import com.testinium.pages.LoginP;

// Utility imports
import com.testinium.utilities.ConfigurationReader;
import com.testinium.utilities.Driver;

// Cucumber annotation imports
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

// Assertion imports
import org.junit.Assert;

// Selenium wait imports
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
```

### Page Object Instantiation

Instantiate Page Objects as instance variables:

```java
LoginP loginP = new LoginP();
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:70*

### WebDriverWait Setup

Set up explicit waits for synchronization:

```java
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 3);
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:87*

The timeout (3 seconds in this example) should be appropriate for your application's responsiveness.

### Cucumber Annotations

Use the appropriate annotation based on the step type:

| Annotation | Purpose | Example Usage |
|------------|---------|---------------|
| `@Given` | Preconditions, setup steps | Navigate to page, log in, prepare data |
| `@When` | Actions the user performs | Click buttons, fill forms, select options |
| `@Then` | Assertions, verifications | Check page title, verify element visible |
| `@And` / `@But` | Additional steps (uses `@Given`, `@When`, or `@Then` internally) | Chain multiple actions |

#### @Given - Precondition Steps

```java
@Given("User is on the upgenix login page")
public void user_is_on_the_upgenix_login_page() {
    String url = ConfigurationReader.getProperty("web.table.url");
    Driver.getDriver().get(url);
}
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:105-110*

#### @When - Action Steps

```java
@When("User clicks the login button")
public void user_clicks_the_login_button() {
    loginP.button.click();
}
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:169-172*

#### @Then - Assertion Steps

```java
@Then("User should see the dashboard")
public void user_should_see_the_dashboard() {
    wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
    String expectedDashboard = "Odoo";
    String actualDashboard = Driver.getDriver().getTitle();
    Assert.assertEquals("The title is not same as the expected! ", expectedDashboard, actualDashboard);
}
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:195-201*

### Parameterized Steps

Use Cucumber expressions to create reusable steps with parameters:

```java
@When("User enters {string} username")
public void user_enters_username(String username) {
    loginP.inputEmail.sendKeys(username);
}

@When("User enters {string} password")
public void user_enters_password(String password) {
    loginP.inputPassword.sendKeys(password);
}
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:129-132*

Common Cucumber expression types:

| Expression | Java Type | Example |
|------------|-----------|---------|
| `{string}` | `String` | `"user@example.com"` |
| `{int}` | `int` | `42` |
| `{float}` | `float` | `3.14` |
| `{word}` | `String` | `Dashboard` (no quotes) |
| `{}` | `Object` | Any single word |

### Assertion Examples

The framework uses JUnit `Assert` for verifications:

**assertEquals** - Verify expected equals actual:

```java
Assert.assertEquals("The title is not same as the expected! ", expectedDashboard, actualDashboard);
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:200*

**assertTrue** - Verify a condition is true:

```java
Assert.assertTrue(loginP.alertErrorMessage.isDisplayed());
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:218*

**assertEquals with custom message**:

```java
String expectedMessage = Driver.getDriver().findElement(By.name("login")).getAttribute("validationMessage");
Assert.assertEquals(expectedMessage, alertMessage);
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:245-246*

**assertTrue with attribute comparison**:

```java
Assert.assertTrue(loginP.bulletPass.getAttribute("type").equals("password"));
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:270*

### Complete Step Definition Template

Use this template when creating a new Step Definition:

```java
package com.testinium.step_definitions;

import com.testinium.pages.ModuleNameP;
import com.testinium.utilities.ConfigurationReader;
import com.testinium.utilities.Driver;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Step definitions for the [Module Name] feature.
 * <p>
 * This class implements Cucumber step definitions for testing
 * the [Module] functionality of the Odoo application.
 * </p>
 * 
 * @see ModuleNameP
 * @see Driver
 */
public class ModuleNameSD {

    /** Page Object for interacting with [Module] page elements */
    ModuleNameP moduleNameP = new ModuleNameP();
    
    /** Explicit wait for synchronization (3 second timeout) */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 3);

    // ========== Precondition Steps (@Given) ==========
    
    /**
     * Navigates to the [Module] page.
     * Retrieves URL from configuration.properties.
     */
    @Given("User is on the module page")
    public void user_is_on_the_module_page() {
        String url = ConfigurationReader.getProperty("module.url");
        Driver.getDriver().get(url);
    }

    // ========== Action Steps (@When) ==========
    
    /**
     * Enters data into the input field.
     * 
     * @param inputData the text to enter
     */
    @When("User enters {string} into the field")
    public void user_enters_into_the_field(String inputData) {
        moduleNameP.inputField.sendKeys(inputData);
    }

    /**
     * Clicks the submit button.
     */
    @When("User clicks the submit button")
    public void user_clicks_the_submit_button() {
        moduleNameP.submitButton.click();
    }

    // ========== Verification Steps (@Then) ==========
    
    /**
     * Verifies the success message is displayed.
     * Uses explicit wait for element visibility.
     */
    @Then("User should see a success message")
    public void user_should_see_a_success_message() {
        wait.until(ExpectedConditions.visibilityOf(moduleNameP.alertMessage));
        Assert.assertTrue("Success message not displayed!", 
                          moduleNameP.alertMessage.isDisplayed());
    }

    /**
     * Verifies the page title matches expected.
     * 
     * @param expectedTitle the expected page title
     */
    @Then("The page title should be {string}")
    public void the_page_title_should_be(String expectedTitle) {
        String actualTitle = Driver.getDriver().getTitle();
        Assert.assertEquals("Page title mismatch!", expectedTitle, actualTitle);
    }
}
```

### Naming Convention

Follow this naming convention for Step Definition files:

```
<ModuleName>SD.java  or  <ModuleName>.java
```

Examples:
- `LoginSD.java` - Login step definitions
- `Contacts.java` - Contacts step definitions
- `LogOutSD.java` - Logout step definitions
- `Sales.java` - Sales step definitions

---

## Adding New Test Modules

When adding test coverage for a new Odoo module, follow this structured approach:

### Step 1: Analyze Target Odoo Module UI

Before writing any code:

1. Navigate to the module in your browser
2. Identify all interactive elements (buttons, forms, links, tables)
3. Note the page structure and navigation flow
4. Identify unique identifiers for elements

### Step 2: Identify Unique Locators Using Browser DevTools

Use browser Developer Tools (F12) to inspect elements:

1. **Right-click** the element → **Inspect**
2. Look for attributes in this priority order:
   - `id` attribute (most reliable)
   - `name` attribute (form elements)
   - `class` attribute (unique classes)
   - `data-*` attributes (test IDs)
   - Element text content (for XPath)

**Tips for finding stable locators in Odoo:**
- Avoid numeric IDs like `o_field_widget_12` (session-specific)
- Look for `data-field` attributes on form fields
- Use button text with XPath: `//button[.='Save']`
- Use `oe_` prefixed IDs when available (Odoo-specific)

### Step 3: Create Page Object with All WebElements

Create the Page Object file:

```
src/main/java/com/testinium/pages/NewModuleP.java
```

Include:
- All navigation elements (menus, tabs, breadcrumbs)
- All form inputs (text fields, dropdowns, checkboxes)
- All action buttons (save, cancel, delete)
- All display elements (tables, lists, labels)
- Error/success message containers

### Step 4: Create Step Definition with Test Logic

Create the Step Definition file:

```
src/main/java/com/testinium/step_definitions/NewModuleSD.java
```

Include:
- Navigation steps (Given)
- Data entry and action steps (When)
- Verification/assertion steps (Then)

### Step 5: Create Feature File

Create the feature file:

```
src/main/resources/features/NewModule.feature
```

Example structure:

```gherkin
@NewModule
Feature: New Module Functionality

  Background:
    Given User is on the upgenix login page
    When User enters "valid_username" username
    And User enters "valid_password" password
    And User clicks the login button
    Then User should see the dashboard

  @Smoke @NewModule
  Scenario: Verify user can access New Module
    When User navigates to New Module
    Then User should see the New Module page

  @NewModule @CreateRecord
  Scenario Outline: Create a new record
    When User navigates to New Module
    And User clicks create button
    And User enters "<name>" in name field
    And User clicks save button
    Then User should see record saved message

    Examples:
      | name        |
      | Test Record |
      | Sample Data |
```

### Step 6: Add Appropriate Tags

Use tags to organize and filter test execution:

| Tag | Purpose |
|-----|---------|
| `@Smoke` | Critical path tests, run frequently |
| `@Regression` | Full test suite |
| `@NewModule` | Module-specific tests |
| `@Negative` | Error/invalid input tests |
| `@WIP` | Work in progress, not ready |

### Step 7: Run Tests and Verify

1. Update `CukesRunner.java` tags to include your new tag:

```java
tags = "@NewModule"
```

2. Run from IDE or command line:

```bash
mvn test -Dcucumber.options="--tags @NewModule"
```

3. Check the Cucumber reports at `target/cucumber-reports.html`

---

## Best Practices for Locators

Effective locators are crucial for maintainable, stable tests. Follow these guidelines:

### Locator Priority

Use locators in this priority order (most to least preferred):

```
id > name > css > linkText > xpath
```

### Locator Type Guidelines

| Locator Type | When to Use | When to Avoid |
|--------------|-------------|---------------|
| `id` | Always preferred when unique and stable | Generated/dynamic IDs |
| `name` | Form elements, inputs | When duplicated on page |
| `css` | Unique class combinations | Styling-only classes |
| `linkText` | Links with unique, stable text | Dynamic/localized text |
| `xpath` | Complex relationships, no other option | Simple elements with id/name |

### XPath Best Practices

**Prefer relative XPath over absolute:**

```java
// GOOD - relative XPath, resilient to DOM changes
@FindBy(xpath = "//button[.='Log in']")
public WebElement loginButton;

// BAD - absolute XPath, brittle
@FindBy(xpath = "/html/body/div[3]/div[2]/form/button")
public WebElement loginButton;
```

**Use meaningful attributes in XPath:**

```java
// GOOD - uses text content
@FindBy(xpath = "//a[.='Reset Password']")
public WebElement resetLink;

// GOOD - uses data attribute
@FindBy(xpath = "//input[@data-field='email']")
public WebElement emailInput;

// BAD - uses position (brittle)
@FindBy(xpath = "//div/input[2]")
public WebElement secondInput;
```

### Avoid These Anti-Patterns

1. **Generated numeric IDs** (session-specific in Odoo):
   ```java
   // BAD - ID changes each session
   @FindBy(id = "o_field_widget_15")
   public WebElement field;
   ```

2. **Absolute XPath paths**:
   ```java
   // BAD - breaks with any DOM change
   @FindBy(xpath = "/html/body/div[2]/div/div/button")
   ```

3. **Index-based selectors alone**:
   ```java
   // BAD - depends on position
   @FindBy(xpath = "//input[3]")
   ```

4. **Styling-only classes**:
   ```java
   // BAD - may change with design updates
   @FindBy(className = "btn-primary")
   ```

### Document Locator Rationale

Add JavaDoc comments explaining why you chose a specific locator:

```java
/**
 * Login button element.
 * <p>
 * Uses XPath with text content because the button lacks id/name attributes.
 * Text "Log in" is stable across Odoo versions.
 * </p>
 */
@FindBy(xpath = "//button[.='Log in']")
public WebElement loginButton;
```

### Consider Test IDs

If you have control over the application, request `data-testid` attributes:

```java
// Best practice with test IDs
@FindBy(css = "[data-testid='login-button']")
public WebElement loginButton;
```

---

## Wait Strategy Guidelines

Proper synchronization prevents flaky tests. The framework supports both implicit and explicit waits.

### Framework Default: Implicit Wait

The framework configures a **10-second implicit wait** for all element lookups:

```java
driverPool.get().manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
```

*Source: src/main/java/com/testinium/utilities/Driver.java:155, 161*

This means Selenium will wait up to 10 seconds for elements to appear before throwing `NoSuchElementException`.

### When to Use Explicit Waits

Use explicit waits when you need to wait for specific conditions:

```java
WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 3);
wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
```

*Source: src/main/java/com/testinium/step_definitions/LoginSD.java:87, 197*

### Common ExpectedConditions

| Condition | Use Case | Example |
|-----------|----------|---------|
| `visibilityOf(element)` | Wait for element to be visible | Modal dialogs, loaded content |
| `elementToBeClickable(element)` | Wait for element to be interactive | Buttons that enable after loading |
| `presenceOfElementLocated(locator)` | Wait for element in DOM | Dynamic content loading |
| `invisibilityOf(element)` | Wait for element to disappear | Loading spinners |
| `textToBePresentInElement(element, text)` | Wait for specific text | Status messages |
| `alertIsPresent()` | Wait for JavaScript alert | Confirmation dialogs |
| `frameToBeAvailableAndSwitchToIt(locator)` | Wait for iframe | Embedded content |
| `numberOfElementsToBe(locator, number)` | Wait for element count | List loading |

### Example Usage

**Wait for element visibility:**

```java
@Then("User should see the dashboard")
public void user_should_see_the_dashboard() {
    wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
    // Now safe to interact with dashboard
}
```

**Wait for element to be clickable:**

```java
@When("User clicks the save button")
public void user_clicks_save() {
    wait.until(ExpectedConditions.elementToBeClickable(pageObject.saveButton));
    pageObject.saveButton.click();
}
```

**Wait for loading spinner to disappear:**

```java
@Then("Data should be loaded")
public void data_should_be_loaded() {
    wait.until(ExpectedConditions.invisibilityOf(pageObject.loadingSpinner));
    // Now data is loaded
}
```

### Avoid Thread.sleep

**Never use `Thread.sleep()` for synchronization:**

```java
// BAD - arbitrary delay, unreliable
Thread.sleep(3000);
element.click();

// GOOD - waits only as long as needed
wait.until(ExpectedConditions.elementToBeClickable(element));
element.click();
```

`Thread.sleep()` problems:
- Wastes time if element appears faster
- Still fails if element takes longer
- Hides underlying timing issues
- Increases test execution time

### Combining Implicit and Explicit Waits

**Warning:** Mixing implicit and explicit waits can cause unexpected delays.

Best practice:
- Keep implicit wait reasonable (10 seconds is good for most cases)
- Use explicit waits for specific conditions beyond simple presence
- Consider setting implicit wait to 0 when using many explicit waits

---

## Feature File Guidelines

Feature files describe test scenarios in Gherkin syntax that is readable by both technical and non-technical stakeholders.

### File Location

All feature files are located in:

```
src/main/resources/features/
```

### Basic Feature Structure

```gherkin
@ModuleName
Feature: Feature Name
  
  As a [role]
  I want to [action]
  So that [benefit]

  Background:
    Given common precondition steps

  @Tag1 @Tag2
  Scenario: Scenario Name
    Given precondition
    When action
    Then expected result
```

### Using Background for Common Setup

Use `Background` for steps that run before every scenario in the feature:

```gherkin
Feature: Sales Module Tests

  Background:
    Given User is on the upgenix login page
    When User enters "salesuser" username
    And User enters "password123" password
    And User clicks the login button
    Then User should see the dashboard
    When User navigates to Sales module
```

### Scenario Outline for Data-Driven Tests

Use `Scenario Outline` with `Examples` for parameterized tests:

```gherkin
@Login @DataDriven
Scenario Outline: Login with multiple credentials
  Given User is on the upgenix login page
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  Then User should see "<result>"

  Examples:
    | username          | password    | result              |
    | validuser@test.com| validpass   | the dashboard       |
    | invalid@test.com  | wrongpass   | error message       |
    |                   | password    | fill out this field |
```

### Tagging Best Practices

Apply tags to features and scenarios for organization and filtering:

```gherkin
@Sales @Regression
Feature: Sales Order Creation

  @Smoke @Priority1
  Scenario: Create basic sales order
    ...

  @Regression @Priority2
  Scenario: Create sales order with discount
    ...

  @Negative
  Scenario: Create sales order without customer
    ...
```

Tag categories:
- **Module tags:** `@Sales`, `@CRM`, `@Contacts`
- **Priority tags:** `@Smoke`, `@Regression`
- **Type tags:** `@Positive`, `@Negative`
- **Status tags:** `@WIP`, `@Known_Issue`

---

## Testing Your Extensions

After creating new Page Objects, Step Definitions, and Feature Files, verify they work correctly.

### Running a Single Feature

Modify `CukesRunner.java` to target your feature:

```java
@CucumberOptions(
    plugin = {
        "html:target/cucumber-reports.html",
        "json:target/cucumber.json",
        "rerun:target/rerun.txt",
        "me.jvt.cucumber.report.PrettyReports:target/cucumber"
    },
    features = "src/main/resources/features",
    glue = "com/testinium/step_definitions",
    dryRun = false,
    tags = "@YourNewTag"  // <-- Update this
)
public class CukesRunner {
}
```

*Source: src/main/java/com/testinium/runners/CukesRunner.java:119-132*

### Dry Run to Validate Step Mappings

Before running actual tests, validate that all steps have definitions:

```java
dryRun = true  // Validates step mappings without executing
```

*Source: src/main/java/com/testinium/runners/CukesRunner.java:129*

This will:
- Check that all Gherkin steps have matching Java methods
- Report any undefined steps
- Not launch a browser or execute test logic

### Running from Command Line

Execute tests via Maven:

```bash
# Run all tests with default tag
mvn test

# Run specific tag
mvn test -Dcucumber.options="--tags @YourNewTag"

# Run multiple tags (AND)
mvn test -Dcucumber.options="--tags '@Smoke and @Login'"

# Run multiple tags (OR)
mvn test -Dcucumber.options="--tags '@Smoke or @Login'"

# Exclude tags
mvn test -Dcucumber.options="--tags 'not @WIP'"
```

### Checking Test Reports

After test execution, review reports at:

| Report | Location | Format |
|--------|----------|--------|
| HTML Report | `target/cucumber-reports.html` | Single HTML file |
| JSON Report | `target/cucumber.json` | Machine-readable |
| Pretty Reports | `target/cucumber/` | Enhanced HTML with charts |
| Rerun File | `target/rerun.txt` | Failed scenario locations |

### Debugging Tips

1. **Enable verbose logging:** Add console plugin:
   ```java
   "pretty"  // Adds to plugin list
   ```

2. **Take screenshots:** Use `TakesScreenshot` interface for debugging

3. **Check element existence:** Add wait before interaction

4. **Use IDE debugging:** Set breakpoints in step definitions

---

## See Also

- [Architecture Overview](ARCHITECTURE.md) - Framework structure and design patterns
- [Configuration Guide](CONFIGURATION.md) - Runtime configuration options
- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues and solutions
- [Selenium WebDriver Documentation](https://www.selenium.dev/documentation/)
- [Cucumber Documentation](https://cucumber.io/docs/cucumber/)
- [JUnit 4 Documentation](https://junit.org/junit4/)
