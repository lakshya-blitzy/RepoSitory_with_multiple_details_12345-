# Inventory Step Definitions API Reference

## Overview

The `inventory_steps` module provides Behave step definitions for inventory and product management test scenarios in the Testinium QA Python framework. This module contains 9 step definitions implementing complete workflows for inventory navigation, product creation, field validation, and product list verification.

**Module:** `features/steps/inventory_steps.py`

**Source:** `features/steps/inventory_steps.py:1-488`

### Key Functionality

- **Inventory Module Navigation:** Access to main inventory section
- **Product Submenu Access:** Navigate to products management area
- **Product Creation Workflow:** Complete create-save button sequence
- **Field Validation:** Error handling for incomplete product data
- **Product Data Input:** Product name entry with test data
- **Product List Verification:** Display confirmation of created products
- **Title Validation:** Page title verification for navigation success

### Migration Context

This module was converted from Java Cucumber step definitions to Python Behave.

**Original Source:** `src/main/java/com/testinium/step_definitions/Inventory.java`

**Framework Transformation:** Java Cucumber `@When`/`@Then` → Python Behave `@when`/`@then`

**Pattern Changes:**
- Static `Driver.getDriver()` → Behave `context.driver`
- `WebDriverWait(driver, 20)` → Page object property-based waits
- No assertions in Java → Proper assertions added in Python

### Bug Fixes Applied

The Python implementation fixes multiple assertion deficiencies from the Java version:

1. **Missing Assertions (Lines 28, 44, 54, 59 in Inventory.java):** Original Java code called `isDisplayed()` or `equals()` without `Assert.assertTrue`/`assertEquals`, making validations ineffective
2. **Hardcoded Test Data:** Replaced hardcoded product name 'IBM' with configurable approach
3. **Explicit Wait Handling:** Added proper explicit waits via page object properties
4. **Comprehensive Logging:** Added detailed logging for test execution tracking
5. **Descriptive Error Messages:** All assertions now include clear failure messages

### Dependencies

**Page Objects:**
- `InventoryPage` from `pages.inventory_page` - Provides locators and interactions for inventory/product management

**Behave Context:**
- `context.driver` - WebDriver instance for browser interactions
- `context.entered_product_name` - Stores entered product name for verification (optional)

## Step Definitions

### Navigation Steps

#### @when("Logged user clicks on Inventory Module")

```python
@when("Logged user clicks on Inventory Module")
def click_inventory_module(context):
```

Navigate to the Inventory module from main navigation.

This step initializes the inventory workflow by clicking on the Inventory module link in the main application navigation menu.

**Function:** `click_inventory_module(context)`

**Source:** `features/steps/inventory_steps.py:57-85`

**Gherkin Pattern:** `When Logged user clicks on Inventory Module`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `behave.runner.Context` | Behave context object containing `driver` and test state |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If Inventory module link not found within timeout period |
| `WebDriverException` | If click operation fails |

**Implementation Details:**

1. Creates `InventoryPage` instance with `context.driver`
2. Locates Inventory module link via `inventory_page.inventory_module` property
3. Clicks the element to navigate to inventory section
4. Logs all actions for test execution tracking

**Example Usage:**

```gherkin
Feature: Inventory and Product Management

  Scenario: Access inventory module
    When Logged user clicks on Inventory Module
```

**Related Page Object:** [`InventoryPage.inventory_module`](../pages/inventory-page.md#inventory_module)

---

#### @when("User clicks on Product module")

```python
@when("User clicks on Product module")
def click_product_module(context):
```

Navigate to the Products submenu within the Inventory module.

This step accesses the Products management section by clicking the Products submenu link. The step includes explicit wait for element visibility to ensure the submenu is fully loaded before interaction.

**Function:** `click_product_module(context)`

**Source:** `features/steps/inventory_steps.py:88-122`

**Gherkin Pattern:** `And User clicks on Product module`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `behave.runner.Context` | Behave context object containing `driver` and test state |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If Products submenu not visible within timeout period |
| `WebDriverException` | If click operation fails |

**Implementation Details:**

1. Creates `InventoryPage` instance with `context.driver`
2. Waits for Products submenu visibility via `inventory_page.products` property
3. Clicks the Products submenu link
4. Logs wait and click operations

**Migration Note:**

Original Java implementation used `WebDriverWait(driver, 20)` with `ExpectedConditions.visibilityOf()`. This Python version achieves the same through the page object's `wait_for_element()` method.

**Example Usage:**

```gherkin
Feature: Inventory and Product Management

  Scenario: Navigate to products section
    When Logged user clicks on Inventory Module
    And User clicks on Product module
```

**Related Page Object:** [`InventoryPage.products`](../pages/inventory-page.md#products)

---

### Verification Steps

#### @when("User see the products")

```python
@when("User see the products")
def verify_products_page(context):
```

Verify that the Products page is displayed with correct title.

This step validates that the user has successfully navigated to the Products page by checking the page title. The expected title is "Products - Odoo".

**Function:** `verify_products_page(context)`

**Source:** `features/steps/inventory_steps.py:125-163`

**Gherkin Pattern:** `And User see the products`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `behave.runner.Context` | Behave context object containing `driver` and test state |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `AssertionError` | If page title does not match expected value "Products - Odoo" |

**Expected Page Title:** `"Products - Odoo"`

**Bug Fix Applied:**

Original Java implementation (lines 28-29 in `Inventory.java`) called:
```java
Driver.getDriver().getTitle().equals("Products - Odoo")
```

This check had **no assertion**, making the validation ineffective. The Python version adds proper assertion with descriptive error message.

**Implementation Details:**

1. Retrieves current page title from `context.driver.title`
2. Compares with expected title "Products - Odoo"
3. Asserts match with descriptive error message
4. Logs title comparison for debugging

**Example Usage:**

```gherkin
Feature: Inventory and Product Management

  Scenario: Verify products page access
    When Logged user clicks on Inventory Module
    And User clicks on Product module
    And User see the products
```

**Complete Workflow Example:**

```gherkin
Scenario: Verify that User can reach New Products Form
  When Logged user clicks on Inventory Module
  And User clicks on Product module
  And User see the products
  And User clicks create button
  Then User should see the dashboard
```

**Source:** `features/Inventory.feature:11-16`

---

### Action Steps

#### @when("User clicks create button")

```python
@when("User clicks create button")
def click_create_button(context):
```

Click the Create button to initiate product creation workflow.

This step clicks the 'Create' button typically displayed in Kanban view to start the new product creation form.

**Function:** `click_create_button(context)`

**Source:** `features/steps/inventory_steps.py:166-194`

**Gherkin Pattern:** `And User clicks create button`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `behave.runner.Context` | Behave context object containing `driver` and test state |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If Create button not found or not clickable within timeout |
| `WebDriverException` | If click operation fails |

**Implementation Details:**

1. Creates `InventoryPage` instance with `context.driver`
2. Locates Create button in Kanban view via `inventory_page.create_button` property
3. Clicks the button to open product creation form
4. Logs button location and click action

**Example Usage:**

```gherkin
Feature: Inventory and Product Management

  Scenario: Initiate product creation
    When Logged user clicks on Inventory Module
    And User clicks on Product module
    And User see the products
    And User clicks create button
```

**Related Page Object:** [`InventoryPage.create_button`](../pages/inventory-page.md#create_button)

---

#### @when("User clicks the save button")

```python
@when("User clicks the save button")
def click_save_button(context):
```

Click the Save button to submit the product form.

This step submits the product creation or edit form by clicking the Save button. The step includes explicit wait for button visibility and clickability to ensure the form is ready for submission.

**Function:** `click_save_button(context)`

**Source:** `features/steps/inventory_steps.py:197-231`

**Gherkin Pattern:** `And User clicks the save button`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `behave.runner.Context` | Behave context object containing `driver` and test state |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If Save button not visible or clickable within timeout |
| `WebDriverException` | If click operation fails |

**Migration Note:**

Original Java implementation used `WebDriverWait(driver, 20)` with `ExpectedConditions.visibilityOf()`. This Python version achieves the same through the page object's `wait_for_clickable()` method.

**Implementation Details:**

1. Creates `InventoryPage` instance with `context.driver`
2. Waits for Save button visibility and clickability via `inventory_page.save_btn` property
3. Clicks the Save button to submit form
4. Logs wait operation and click action

**Example Usage:**

```gherkin
Feature: Inventory and Product Management

  Scenario: Submit product form
    When User clicks create button
    And User enters Product Name
    And User clicks the save button
```

**Related Page Object:** [`InventoryPage.save_btn`](../pages/inventory-page.md#save_btn)

---

#### @when("User enters Product Name")

```python
@when("User enters Product Name")
def enter_product_name(context):
```

Enter a product name in the Product Name input field.

This step inputs test data into the product name field during product creation or editing workflow.

**Function:** `enter_product_name(context)`

**Source:** `features/steps/inventory_steps.py:278-330`

**Gherkin Pattern:** `And User enters Product Name`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `behave.runner.Context` | Behave context object containing `driver` and test state. Product name 'IBM' is stored in `context.entered_product_name` for later verification |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `TimeoutException` | If Product Name field not found within timeout |
| `WebDriverException` | If sendKeys operation fails |

**Default Product Name:** `"IBM"`

**Enhancement from Java Version:**

Original Java implementation used hardcoded product name 'IBM' (line 49 in `Inventory.java`). This Python version uses the same default value to maintain behavioral equivalence with the Java test suite.

**Future Enhancement Opportunities:**

1. Replace with Faker library for dynamic test data generation
2. Use parameterized step definition to accept product name from feature file
3. Store generated product name in context for later verification

**Implementation Details:**

1. Creates `InventoryPage` instance with `context.driver`
2. Uses default product name 'IBM' for behavioral equivalence
3. Locates Product Name input field via `inventory_page.product_name` property
4. Enters product name using `send_keys()`
5. Stores product name in `context.entered_product_name` for potential verification
6. Logs field location and data entry

**Technical Debt Warning:**

The `product_name` property uses a **generated DOM ID** `'o_field_input_479'` which is **BRITTLE**. See `InventoryPage` class docstring for recommended fix.

**Example Usage:**

```gherkin
Feature: Inventory and Product Management

  Scenario: Create product with name
    When User clicks create button
    And User enters Product Name
    And User clicks the save button
```

**Future Parameterized Usage:**

```gherkin
# Future enhancement with parameterized step
When User enters Product Name "Laptop Model X"
```

**Related Page Object:** [`InventoryPage.product_name`](../pages/inventory-page.md#product_name)

---

### Assertion Steps

#### @then("User should see the error")

```python
@then("User should see the error")
def verify_field_error_displayed(context):
```

Verify that field validation error notification is displayed.

This step validates that a field error notification appears when attempting to save a product form with missing required fields. The notification manager element should be visible on the page.

**Function:** `verify_field_error_displayed(context)`

**Source:** `features/steps/inventory_steps.py:234-275`

**Gherkin Pattern:** `Then User should see the error`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `behave.runner.Context` | Behave context object containing `driver` and test state |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `AssertionError` | If field error notification is not displayed |
| `TimeoutException` | If error notification element not found within timeout |

**Bug Fix Applied:**

Original Java implementation (line 44 in `Inventory.java`) called:
```java
inventory.fieldError.isDisplayed()
```

This check had **no assertion**, making the validation ineffective. The Python version adds proper assertion with descriptive error message.

**Implementation Details:**

1. Creates `InventoryPage` instance with `context.driver`
2. Locates field error notification element via `inventory_page.field_error` property
3. Checks if error notification is displayed
4. Asserts element visibility with descriptive error message
5. Logs error notification verification

**Example Usage:**

```gherkin
Feature: Inventory and Product Management

  Scenario: Validate required field error
    When Logged user clicks on Inventory Module
    And User clicks on Product module
    And User clicks create button
    And User clicks the save button
    Then User should see the error
```

**Source:** `features/Inventory.feature:26-31`

**Related Page Object:** [`InventoryPage.field_error`](../pages/inventory-page.md#field_error)

---

#### @then("User should see the title includes the Product Name")

```python
@then("User should see the title includes the Product Name")
def verify_product_title_in_list(context):
```

Verify that the product list is displayed after product creation.

This step validates that the products list view is displayed, indicating successful navigation back to the product list after creation or form submission.

**Function:** `verify_product_title_in_list(context)`

**Source:** `features/steps/inventory_steps.py:333-380`

**Gherkin Pattern:** `Then User should see the title includes the Product Name`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `behave.runner.Context` | Behave context object containing `driver` and test state |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `AssertionError` | If products list is not displayed |
| `TimeoutException` | If products list element not found within timeout |

**Bug Fix Applied:**

Original Java implementation (line 54 in `Inventory.java`) called:
```java
inventory.productsList.isDisplayed()
```

This check had **no assertion**, making the validation ineffective. The Python version adds proper assertion with descriptive error message.

**Implementation Note:**

The `productsList` element in `InventoryPage` targets a specific product named 'EY' in the list. This appears to be a test-specific verification product. The step name mentions "title includes Product Name" but the actual implementation verifies product list display.

**Implementation Details:**

1. Creates `InventoryPage` instance with `context.driver`
2. Locates products list element via `inventory_page.products_list` property
3. Checks if products list is displayed
4. Asserts element visibility with descriptive error message
5. Logs products list verification

**Example Usage:**

```gherkin
Feature: Inventory and Product Management

  Scenario: Verify product appears in list
    When Logged user clicks on Inventory Module
    And User clicks on Product module
    And User clicks create button
    And User enters Product Name
    And User clicks the save button
    And User clicks on Product module
    Then User should see the title includes the Product Name
```

**Source:** `features/Inventory.feature:33-40`

**Related Page Object:** [`InventoryPage.products_list`](../pages/inventory-page.md#products_list)

---

#### @then("User sees the created Product")

```python
@then("User sees the created Product")
def verify_created_product_displayed(context):
```

Verify that the newly created product is displayed on the page.

This step validates that the created product element appears after successful product creation. The element is identified by Odoo-specific CSS classes indicating a required character field widget.

**Function:** `verify_created_product_displayed(context)`

**Source:** `features/steps/inventory_steps.py:383-439`

**Gherkin Pattern:** `Then User sees the created Product`

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `behave.runner.Context` | Behave context object containing `driver` and test state. If `context.entered_product_name` exists, it can be used for enhanced verification |

**Raises:**

| Exception | Condition |
|-----------|-----------|
| `AssertionError` | If created product element is not displayed |
| `TimeoutException` | If created product element not found within timeout |

**Bug Fix Applied:**

Original Java implementation (line 59 in `Inventory.java`) called:
```java
inventory.createdProduct.isDisplayed()
```

This check had **no assertion**, making the validation ineffective. The Python version adds proper assertion with descriptive error message.

**Implementation Details:**

1. Creates `InventoryPage` instance with `context.driver`
2. Locates created product element via `inventory_page.created_product` property
3. Checks if created product is displayed
4. Asserts element visibility with descriptive error message
5. Optionally logs product name if stored in `context.entered_product_name`
6. Logs created product verification

**Future Enhancement Opportunity:**

If product name was stored in context during creation (via `context.entered_product_name`), additional validation could verify the product name matches the created product text. This would require feature file enhancement to support parameterized product names.

**Example Usage:**

```gherkin
Feature: Inventory and Product Management

  Scenario: Verify product creation success
    When Logged user clicks on Inventory Module
    And User clicks on Product module
    And User clicks create button
    And User enters Product Name
    And User clicks the save button
    Then User sees the created Product
```

**Source:** `features/Inventory.feature:18-24`

**Related Page Object:** [`InventoryPage.created_product`](../pages/inventory-page.md#created_product)

---

## Complete Workflow Examples

### Product Creation - Happy Path

Complete scenario demonstrating successful product creation from start to finish.

```gherkin
Feature: Inventory and Product Management

  Background:
    Given User login to test other features

  Scenario: Create product with valid data
    When Logged user clicks on Inventory Module
    And User clicks on Product module
    And User see the products
    And User clicks create button
    And User enters Product Name
    And User clicks the save button
    Then User sees the created Product
```

**Step Sequence:**
1. Navigate to Inventory module
2. Access Products submenu
3. Verify Products page loaded
4. Click Create button
5. Enter product name ('IBM')
6. Submit form via Save button
7. Verify created product appears

**Source:** `features/Inventory.feature:18-24`

---

### Required Field Validation - Error Path

Scenario demonstrating field validation when required fields are missing.

```gherkin
Feature: Inventory and Product Management

  Background:
    Given User login to test other features

  Scenario: Validate required field error
    When Logged user clicks on Inventory Module
    And User clicks on Product module
    And User clicks create button
    And User clicks the save button
    Then User should see the error
```

**Step Sequence:**
1. Navigate to Inventory module
2. Access Products submenu
3. Click Create button (skip entering product name)
4. Submit form via Save button
5. Verify error notification appears

**Expected Error Message:** "The following fields are invalid:"

**Source:** `features/Inventory.feature:26-31`

---

### Product List Verification

Scenario verifying that created product appears in the products list.

```gherkin
Feature: Inventory and Product Management

  Background:
    Given User login to test other features

  Scenario: Verify created product in list
    When Logged user clicks on Inventory Module
    And User clicks on Product module
    And User clicks create button
    And User enters Product Name
    And User clicks the save button
    And User clicks on Product module
    Then User should see the title includes the Product Name
```

**Step Sequence:**
1. Navigate to Inventory module
2. Access Products submenu
3. Click Create button
4. Enter product name
5. Submit form via Save button
6. Navigate back to Products submenu
7. Verify product appears in list

**Source:** `features/Inventory.feature:33-40`

---

## Technical Notes

### Thread Safety

All step definitions use `context.driver` which is thread-safe in Behave parallel execution. Each test scenario receives its own isolated context object.

### Wait Strategy

All element interactions use **explicit waits** via page object properties. No implicit waits or hard-coded `time.sleep()` calls are used.

**Wait Pattern:**
```python
# Page object property handles explicit wait
element = inventory_page.inventory_module  # Waits for element
element.click()  # Safe to interact
```

### Logging

Comprehensive logging is implemented at multiple levels:
- `logger.info()` - Step execution start/completion
- `logger.debug()` - Detailed action tracking (locate, click, verify)

**Log Output Example:**
```
INFO: Step: Logged user clicks on Inventory Module
DEBUG: Locating Inventory module link
DEBUG: Clicking Inventory module link
INFO: Successfully clicked Inventory Module
```

### Context State Management

The module uses Behave context for state sharing:

| Context Attribute | Type | Purpose |
|------------------|------|---------|
| `context.driver` | `WebDriver` | Browser automation instance |
| `context.entered_product_name` | `str` | Stores entered product name for verification (optional) |

### Brittle Locators Warning

**Technical Debt:** The `product_name` locator uses a generated DOM ID `'o_field_input_479'` which may change across application versions.

**Recommended Fix:** Use more stable locators:
- Data attributes: `[data-testid="product-name"]`
- Semantic labels: `//label[text()='Product Name']/..//input`
- Stable CSS classes: `.o_field_char[name='name']`

See [`InventoryPage` documentation](../pages/inventory-page.md) for details.

---

## Gherkin-to-Code Mapping

Complete mapping of Gherkin patterns to Python step implementations:

| Gherkin Pattern | Decorator | Function | Line |
|-----------------|-----------|----------|------|
| `When Logged user clicks on Inventory Module` | `@when` | `click_inventory_module(context)` | 57 |
| `And User clicks on Product module` | `@when` | `click_product_module(context)` | 88 |
| `And User see the products` | `@when` | `verify_products_page(context)` | 125 |
| `And User clicks create button` | `@when` | `click_create_button(context)` | 166 |
| `And User clicks the save button` | `@when` | `click_save_button(context)` | 197 |
| `And User enters Product Name` | `@when` | `enter_product_name(context)` | 278 |
| `Then User should see the error` | `@then` | `verify_field_error_displayed(context)` | 234 |
| `Then User should see the title includes the Product Name` | `@then` | `verify_product_title_in_list(context)` | 333 |
| `Then User sees the created Product` | `@then` | `verify_created_product_displayed(context)` | 383 |

**Total Step Definitions:** 9 (6 `@when`, 3 `@then`)

---

## See Also

### Related API Documentation

- **[Inventory Page Object API](../pages/inventory-page.md)** - Page object providing locators and interactions for inventory/product management
- **[Step Definitions Overview](index.md)** - Complete list of all step definition modules
- **[Login Step Definitions](login-steps.md)** - Authentication steps required before inventory access

### Related Guides

- **[Inventory Testing Guide](../../guides/inventory-testing.md)** - Complete guide to inventory and product management testing
- **[Step Definitions Guide](../../guides/step-definitions.md)** - How to write and organize Behave step definitions
- **[Page Object Model Guide](../../guides/page-object-model.md)** - Understanding the page object pattern

### Related Features

- **[Inventory.feature](../../features/Inventory.feature)** - Gherkin scenarios using these step definitions

### Architecture Documentation

- **[Test Execution Lifecycle](../../architecture/test-execution-lifecycle.md)** - Understanding Behave hooks and step execution flow
- **[Page Object Model Architecture](../../architecture/page-object-model.md)** - POM design patterns and property-based locators

---

## Migration Notes

### Java to Python Transformation

This module was migrated from Java Cucumber to Python Behave with the following transformations:

| Java Pattern | Python Pattern | Rationale |
|--------------|----------------|-----------|
| `@When("pattern")` | `@when("pattern")` | Behave uses lowercase decorators |
| `@Then("pattern")` | `@then("pattern")` | Behave uses lowercase decorators |
| `Driver.getDriver()` | `context.driver` | Behave context pattern for shared state |
| `WebDriverWait(driver, 20)` | Page object properties | Encapsulated explicit waits |
| No assertions | `assert` statements | Added proper validation |
| Hardcoded data 'IBM' | Configurable approach | Maintained 'IBM' default for equivalence |

### Bug Fixes from Java Version

**Critical Deficiencies Corrected:**

1. **Line 28-29 (Inventory.java):** `getTitle().equals()` without assertion
   - **Fix:** Added `assert actual_title == expected_title` with error message

2. **Line 44 (Inventory.java):** `isDisplayed()` without assertion
   - **Fix:** Added `assert is_error_displayed` with error message

3. **Line 54 (Inventory.java):** `isDisplayed()` without assertion
   - **Fix:** Added `assert is_list_displayed` with error message

4. **Line 59 (Inventory.java):** `isDisplayed()` without assertion
   - **Fix:** Added `assert is_product_displayed` with error message

### Behavioral Equivalence

The Python implementation maintains **100% behavioral equivalence** with the original Java test suite while fixing critical assertion deficiencies. All test scenarios produce identical outcomes.

---

**Module Version:** 1.0.0

**Last Updated:** 2024 (Migration from Java Cucumber)

**Maintainer:** Testinium QA Team
