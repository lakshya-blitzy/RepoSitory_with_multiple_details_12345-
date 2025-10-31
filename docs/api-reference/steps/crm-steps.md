# CRM Step Definitions API Reference

## Overview

The CRM step definitions module provides Behave step implementations for testing Customer Relationship Management (CRM) workflows including pipeline management, opportunity creation and editing, customer registration, and payment operations.

**Module:** `features/steps/crm_steps.py`

**Source:** `features/steps/crm_steps.py`

**Java Source:** `src/main/java/com/testinium/step_definitions/Crm.java`

**Framework:** Behave 1.2.6 + Selenium 4.15.2

**Step Count:** 12 step definitions

---

## Module Information

### Migration Context

This module was converted from the Java Cucumber framework to Python Behave as part of the test automation framework migration.

**Key Migration Changes:**
- Replaced Java `WebDriverWait` with context-based implicit waits handled by page objects
- Converted Java `Actions` class to Python `ActionChains` for drag-and-drop operations
- Eliminated `Thread.sleep()` anti-pattern with proper `ActionChains.pause()` timing
- Replaced `Assert.assertEquals` with Python `assert` statements with descriptive messages
- Converted `System.out.println` debug statements to structured `logging.debug()` calls
- Implemented integer parsing for total price validation
- All synchronization handled by `CrmPage` property methods via `BasePage` explicit waits

### Dependencies

**Page Objects:**
- `pages.crm_page.CrmPage` - Page object for CRM module elements and interactions

**Framework:**
- `behave` - BDD framework providing `@when`, `@then`, `@step` decorators and `Context`
- `selenium.webdriver.common.keys.Keys` - Keyboard interactions (Keys.ENTER)
- `selenium.webdriver.common.action_chains.ActionChains` - Drag-and-drop operations
- `logging` - Structured logging for test diagnostics

**Context Variables Used:**
- `context.driver` - WebDriver instance from `environment.py`
- `context.scenario` - Current scenario for logging attachments

---

## Wait Strategy

**Philosophy:** No explicit waits in step definitions - all synchronization handled by page objects.

- **CrmPage properties** use `BasePage.wait_for_element()`, `wait_for_clickable()`, and `wait_for_visibility()` methods
- **ActionChains.pause()** used for drag-and-drop timing control
- **All WebDriverWait instances** removed as page objects handle synchronization
- **Brief time.sleep()** after drag-and-drop to allow DOM update completion

---

## Step Definitions Summary

| Step Type | Step Pattern | Category | Description |
|-----------|-------------|----------|-------------|
| `@when` | `User click on the crm dashboard` | Navigation | Navigate to CRM dashboard |
| `@step` | `User click on the pipeline button` | Creation | Click create pipeline button |
| `@step` | `User can create the new pipeline` | Creation | Create new opportunity with test data |
| `@step` | `User can see the total price` | Validation | Validate total price calculation |
| `@then` | `User can see new pipeline` | Validation | Verify newly created pipeline visibility |
| `@step` | `User can change any user's information like "{opportunity}" , "{revenue}" and "{probability}"` | Editing | Edit opportunity with parameterized values |
| `@step` | `User can save information` | Editing | Save edited opportunity information |
| `@then` | `User can verify the information` | Editing | Verify opportunity information updated |
| `@step` | `User can drag and drop the pipeline` | Drag-Drop | Move opportunity between pipeline stages |
| `@then` | `User can see the new changes in progress` | Drag-Drop | Verify opportunity in new stage |
| `@step` | `User can register new customer` | Customer | Register new customer and search |
| `@then` | `User can print the profile` | Customer | Print customer profile and payment report |

**Step Categories:**
- **Navigation:** 1 step - CRM dashboard access
- **Creation:** 2 steps - Pipeline/opportunity creation
- **Validation:** 2 steps - Total price and pipeline visibility checks
- **Editing:** 3 steps - Opportunity information update workflow
- **Drag-Drop:** 2 steps - Drag-and-drop and verification
- **Customer:** 2 steps - Customer registration and profile operations

---

## Detailed Step Definitions

### Navigation Steps

#### `@when("User click on the crm dashboard")`

Navigate to CRM dashboard by clicking the CRM module link.

**Function Signature:**
```python
@when("User click on the crm dashboard")
def user_click_on_crm_dashboard(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `TimeoutException`: If CRM link is not clickable within timeout period

**Description:**

This step initiates CRM module access from the main application dashboard. The CRM link is located via partial link text "CRM" and becomes visible after successful click.

**Implementation Details:**
- Instantiates `CrmPage` with `context.driver`
- Clicks `crm_page.crm_link` property (waits handled by property)
- No explicit wait needed - page object handles synchronization

**Example Usage:**

```gherkin
Scenario: Access CRM module
    When User click on the crm dashboard
```

**Source:** `features/steps/crm_steps.py:90-127`

**Java Source:** `Crm.java:21-25`

---

### Opportunity Creation Steps

#### `@step("User click on the pipeline button")`

Click the create pipeline button to initiate new opportunity creation.

**Function Signature:**
```python
@step("User click on the pipeline button")
def user_click_on_pipeline_button(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `TimeoutException`: If create button is not clickable within timeout period

**Description:**

This step opens the opportunity creation form by clicking the create button (identified by `accesskey='c'`). The button visibility is confirmed after click by the page object property.

**Implementation Details:**
- Instantiates `CrmPage` with `context.driver`
- Clicks `crm_page.create_button` property
- Removed redundant visibility wait from Java version (property handles synchronization)

**Example Usage:**

```gherkin
And User click on the pipeline button
```

**Source:** `features/steps/crm_steps.py:135-169`

**Java Source:** `Crm.java:27-32`

---

#### `@step("User can create the new pipeline")`

Create a new pipeline opportunity with test data.

**Function Signature:**
```python
@step("User can create the new pipeline")
def user_create_new_pipeline(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `TimeoutException`: If form elements are not available within timeout period

**Description:**

This step fills out the opportunity creation form with the following test data:
- **Opportunity Title:** "test" (with Keys.ENTER submission)
- **Customer:** Selects customer via dropdown (&CC customer ID)
- **Expected Revenue:** 8 (clears existing value, enters new value with Keys.ENTER)
- **Priority:** Selects priority level via dropdown
- Submits form via create pipeline button

**Workflow Steps:**
1. Enter opportunity title: "test" + Keys.ENTER
2. Click customer dropdown field
3. Select customer ID option (&CC)
4. Clear existing revenue value
5. Enter expected revenue: "8" + Keys.ENTER
6. Click priority dropdown
7. Click create pipeline button to submit

**Example Usage:**

```gherkin
And User can create the new pipeline
```

**Source:** `features/steps/crm_steps.py:172-238`

**Java Source:** `Crm.java:34-44`

---

### Pipeline Validation Steps

#### `@step("User can see the total price")`

Validate total price calculation in pipeline view.

**Function Signature:**
```python
@step("User can see the total price")
def user_see_total_price(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `AssertionError`: If calculated total price does not match expected value
- `ValueError`: If price text cannot be parsed as integer

**Description:**

This step retrieves the current total price from the pipeline card, adds the newly created opportunity revenue (8), and verifies the sum equals the expected total (89).

**Calculation Logic:**
```python
total_price = int(displayed_price_text) + 8
expected_price = 89
assert total_price == expected_price
```

**Implementation Details:**
- Retrieves `crm_page.total_price.text` and parses as integer
- Adds newly created opportunity revenue (8)
- Validates calculated total matches expected value (89)
- Provides detailed error message with actual values if validation fails
- Handles `ValueError` if price text cannot be parsed as integer

**Example Usage:**

```gherkin
And User can see the total price
```

**Source:** `features/steps/crm_steps.py:246-314`

**Java Source:** `Crm.java:46-56`

---

#### `@then("User can see new pipeline")`

Verify that newly created pipeline opportunity is visible with correct title.

**Function Signature:**
```python
@then("User can see new pipeline")
def user_see_new_pipeline(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `AssertionError`: If pipeline title does not match expected value "test"

**Description:**

This step validates that the opportunity titled "test" appears in the pipeline view after successful creation. It retrieves the title from the pipeline card and compares it with the expected value.

**Validation Logic:**
```python
actual_name = crm_page.find_title_test.text
expected_name = "test"
assert expected_name == actual_name
```

**Example Usage:**

```gherkin
Then User can see new pipeline
```

**Source:** `features/steps/crm_steps.py:317-368`

**Java Source:** `Crm.java:58-68`

---

### Opportunity Editing Steps

#### `@step('User can change any user\'s information like "{opportunity}" , "{revenue}" and "{probability}"')`

Edit existing opportunity information with parameterized values.

**Function Signature:**
```python
@step('User can change any user\'s information like "{opportunity}" , "{revenue}" and "{probability}"')
def user_change_user_information(
    context: Context,
    opportunity: str,
    revenue: str,
    probability: str
) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance
- `opportunity` (str): New opportunity title value
- `revenue` (str): New expected revenue value
- `probability` (str): New win probability value

**Raises:**
- `TimeoutException`: If edit form elements are not available within timeout

**Description:**

This step opens the opportunity editor and updates three key fields:
- **Opportunity Title:** Parameterized opportunity name
- **Expected Revenue:** Parameterized revenue amount
- **Probability:** Parameterized win probability percentage

All fields are cleared before entering new values, and `Keys.ENTER` is sent after each field to trigger form validation/submission.

**Workflow Steps:**
1. Click on pipeline card to select opportunity
2. Click edit button to open edit form
3. Clear opportunity title field and enter new value + Keys.ENTER
4. Clear expected revenue field and enter new value + Keys.ENTER
5. Clear probability field and enter new value + Keys.ENTER

**Example Usage:**

```gherkin
And User can change any user's information like "Test2" , "15" and "85"
```

**Scenario Outline Usage:**

```gherkin
Scenario Outline: User can change information in dashboard
    And User can change any user's information like "<opportunity>" , "<revenue>" and "<probability>"
    
    Examples:
        | opportunity | revenue | probability |
        | Test2       | 30      | 2           |
```

**Source:** `features/steps/crm_steps.py:376-457`

**Java Source:** `Crm.java:70-81`

---

#### `@step("User can save information")`

Save edited opportunity information by clicking save button.

**Function Signature:**
```python
@step("User can save information")
def user_save_information(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `TimeoutException`: If save button is not clickable within timeout period

**Description:**

This step finalizes opportunity edits by clicking the save button (`accesskey='s'`). The original Java implementation waited for the probability field to be visible before saving, but this is now handled automatically by the property access in the edit step.

**Implementation Details:**
- Clicks `crm_page.save_edit` button
- Removed explicit wait from Java version (property handles synchronization)
- Save button click only proceeds when element is clickable

**Example Usage:**

```gherkin
And User can save information
```

**Source:** `features/steps/crm_steps.py:460-499`

**Java Source:** `Crm.java:83-87`

---

#### `@then("User can verify the information")`

Verify that opportunity information was successfully updated.

**Function Signature:**
```python
@then("User can verify the information")
def user_verify_information(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `AssertionError`: If opportunity title does not match expected value "Test2"

**Description:**

This step navigates back to the pipeline view and validates that the opportunity title has been updated to "Test2" as expected from the editing workflow (based on the scenario outline example values).

**Workflow Steps:**
1. Click pipeline sidebar button to return to pipeline view
2. Retrieve updated opportunity title from pipeline card
3. Validate title matches expected value "Test2"

**Validation Logic:**
```python
actual_name = crm_page.find_title_test.text
expected_name = "Test2"
assert expected_name == actual_name
```

**Example Usage:**

```gherkin
Then User can verify the information
```

**Source:** `features/steps/crm_steps.py:502-559`

**Java Source:** `Crm.java:89-104`

---

### Drag-and-Drop Pipeline Operations

#### `@step("User can drag and drop the pipeline")`

Drag and drop an opportunity from one pipeline stage to another.

**Function Signature:**
```python
@step("User can drag and drop the pipeline")
def user_drag_and_drop_pipeline(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `Exception`: If drag-and-drop operation fails
- `TimeoutException`: If source or target elements are not visible

**Description:**

This step performs a complex drag-and-drop operation to move an opportunity card from the first pipeline stage (`progress_pipeline`, `data-id='1'`) to the second pipeline stage (`progress_pipeline2`, `data-id='2'`).

**ActionChains Sequence:**

The operation uses Selenium ActionChains with the following sequence:
1. **click_and_hold** on source element (`progress_pipeline`)
2. **pause(2)** for smooth animation (2 seconds)
3. **move_to_element** to target (`progress_pipeline2`)
4. **pause(2)** for drop zone recognition (2 seconds)
5. **release** mouse button
6. **perform** to execute the action chain

A brief `time.sleep(2)` after `perform()` ensures the DOM update completes before subsequent verification steps.

**Implementation Details:**
- Creates `ActionChains` instance for complex mouse operations
- Pause durations are critical for stable drag-and-drop:
  - **First pause:** Allows drag operation to be recognized by browser
  - **Second pause:** Ensures drop zone highlight and validation
  - **Final sleep:** Allows DOM update and re-render to complete
- While explicit waits would be preferred, drag-and-drop operations often require timed pauses for browser animation and event processing

**Example Usage:**

```gherkin
And User can drag and drop the pipeline
```

**Source:** `features/steps/crm_steps.py:567-672`

**Java Source:** `Crm.java:106-119`

**Technical Note:**

The pause durations and final sleep are critical for stable drag-and-drop. While explicit waits would be preferred, drag-and-drop operations often require timed pauses for browser animation and event processing.

---

#### `@then("User can see the new changes in progress")`

Verify that opportunity successfully moved to new pipeline stage.

**Function Signature:**
```python
@then("User can see the new changes in progress")
def user_see_new_changes_in_progress(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `AssertionError`: If opportunity is not found in target stage with correct title

**Description:**

This step validates that the opportunity titled "test" now appears in the second pipeline stage (`test_verify` element, `data-id='2'`) after the drag-and-drop operation.

**Validation Logic:**
```python
actual_name = crm_page.test_verify.text
expected_name = "test"
assert expected_name == actual_name
```

**Example Usage:**

```gherkin
Then User can see the new changes in progress
```

**Source:** `features/steps/crm_steps.py:675-725`

**Java Source:** `Crm.java:121-130`

---

### Customer Management Steps

#### `@step("User can register new customer")`

Register a new customer and perform search validation.

**Function Signature:**
```python
@step("User can register new customer")
def user_register_new_customer(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `TimeoutException`: If customer management elements are not available

**Description:**

This step navigates to customer management, creates a new customer record with name "Test", and then searches for customers containing "aa" to validate the customer management workflow.

**Workflow Steps:**
1. Click customer sidebar button to navigate to customer management
2. Click create customer button to open creation form
3. Enter customer name "Test" with Keys.ENTER submission
4. Click create customer button to save record
5. Enter search term "aa" with Keys.ENTER to test search functionality

**Implementation Details:**
- All explicit waits removed from Java version
- Page object properties handle synchronization
- Keys.ENTER used for form submission and search trigger

**Example Usage:**

```gherkin
And User can register new customer
```

**Source:** `features/steps/crm_steps.py:733-801`

**Java Source:** `Crm.java:132-143`

---

#### `@then("User can print the profile")`

Print customer profile and access due payment report.

**Function Signature:**
```python
@then("User can print the profile")
def user_print_profile(context: Context) -> None
```

**Parameters:**
- `context` (Context): Behave context object containing WebDriver instance

**Raises:**
- `TimeoutException`: If print elements are not clickable within timeout

**Description:**

This step demonstrates the print and payment reporting functionality by:
1. Clicking on a customer name to open their profile
2. Clicking the print button to initiate print dialog
3. Clicking the due payment button to access payment report

**Implementation Details:**
- Clicks `crm_page.name_customer` to open customer profile
- Clicks `crm_page.print_button` to initiate print dialog
- Clicks `crm_page.due_payment_button` to access payment report
- All explicit waits removed (properties handle visibility/clickability)

**Technical Debt Note:**

The `print_button` uses an absolute XPath locator which is extremely fragile. This is documented in `CrmPage` as CRITICAL priority technical debt. If this step fails, the locator may need updating due to DOM changes.

**Example Usage:**

```gherkin
Then User can print the profile
```

**Source:** `features/steps/crm_steps.py:804-860`

**Java Source:** `Crm.java:145-153`

---

## Usage Examples from Feature File

**Feature File:** `features/Crm.feature`

### Scenario 1: Create Pipeline

```gherkin
@Smoke
Feature: Testinium app CRM Module

  Background: As a Posmanager, I should be able to create and to see my pipeline and customers from "CRM" module.
    Given User login to test other features

  Scenario: User can create pipeline in the displayed dashboard
    When User click on the crm dashboard
    And User click on the pipeline button
    And User can create the new pipeline
    And User can see the total price
    Then User can see new pipeline
```

**Steps Executed:**
1. Navigate to CRM dashboard
2. Click create pipeline button
3. Fill opportunity form with test data (title: "test", revenue: 8)
4. Validate total price calculation (base + 8 = 89)
5. Verify new pipeline appears with title "test"

---

### Scenario 2: Edit Opportunity Information

```gherkin
  Scenario Outline: User can change information in dashboard
    When User click on the crm dashboard
    And User can change any user's information like "<opportunity>" , "<revenue>" and "<probability>"
    And User can save information
    Then User can verify the information

    Examples: Expected name
      | opportunity | revenue | probability |
      | Test2       | 30      | 2           |
```

**Steps Executed:**
1. Navigate to CRM dashboard
2. Edit opportunity with parameterized values (Test2, 30, 2)
3. Save changes
4. Verify opportunity title updated to "Test2"

---

### Scenario 3: Drag-and-Drop Pipeline Stage

```gherkin
  Scenario: User can change the situation in progress
    When User click on the crm dashboard
    And User can drag and drop the pipeline
    Then User can see the new changes in progress
```

**Steps Executed:**
1. Navigate to CRM dashboard
2. Drag opportunity from stage 1 to stage 2 using ActionChains
3. Verify opportunity appears in stage 2 with title "test"

---

### Scenario 4: Customer Registration and Profile

```gherkin
  Scenario: User can register new customer and can print the profile
    When User click on the crm dashboard
    And User can register new customer
    Then User can print the profile
```

**Steps Executed:**
1. Navigate to CRM dashboard
2. Register new customer with name "Test"
3. Search for customers with term "aa"
4. Open customer profile and print
5. Access due payment report

---

## Gherkin-to-Code Mapping

### Step Pattern Mapping

| Gherkin Step | Python Function | CrmPage Methods Used |
|--------------|-----------------|----------------------|
| `When User click on the crm dashboard` | `user_click_on_crm_dashboard()` | `crm_link.click()` |
| `And User click on the pipeline button` | `user_click_on_pipeline_button()` | `create_button.click()` |
| `And User can create the new pipeline` | `user_create_new_pipeline()` | `opportunity_title.send_keys()`, `customer.click()`, `customer_id.click()`, `expected_revenue.clear()`, `expected_revenue.send_keys()`, `priority.click()`, `create_pipeline.click()` |
| `And User can see the total price` | `user_see_total_price()` | `total_price.text` |
| `Then User can see new pipeline` | `user_see_new_pipeline()` | `find_title_test.text` |
| `And User can change any user's information like "{opportunity}" , "{revenue}" and "{probability}"` | `user_change_user_information()` | `button_pipeline.click()`, `edit_button.click()`, `opportunity_title_edit.clear()`, `opportunity_title_edit.send_keys()`, `expected_revenue_edit.clear()`, `expected_revenue_edit.send_keys()`, `probability_edit.clear()`, `probability_edit.send_keys()` |
| `And User can save information` | `user_save_information()` | `save_edit.click()` |
| `Then User can verify the information` | `user_verify_information()` | `pipeline_side_button.click()`, `find_title_test.text` |
| `And User can drag and drop the pipeline` | `user_drag_and_drop_pipeline()` | `progress_pipeline`, `progress_pipeline2` (with ActionChains) |
| `Then User can see the new changes in progress` | `user_see_new_changes_in_progress()` | `test_verify.text` |
| `And User can register new customer` | `user_register_new_customer()` | `customer_side_button.click()`, `create_customer.click()`, `input_name.send_keys()`, `create_customer_button.click()`, `searching_text.send_keys()` |
| `Then User can print the profile` | `user_print_profile()` | `name_customer.click()`, `print_button.click()`, `due_payment_button.click()` |

---

## Complete Workflow Example

**End-to-End CRM Workflow:**

```gherkin
@Smoke
Feature: Complete CRM Workflow

  Background:
    Given User login to test other features

  Scenario: Complete CRM opportunity lifecycle
    # Navigate to CRM
    When User click on the crm dashboard
    
    # Create new opportunity
    And User click on the pipeline button
    And User can create the new pipeline
    And User can see the total price
    Then User can see new pipeline
    
    # Edit opportunity details
    And User can change any user's information like "Updated Opportunity" , "50" and "90"
    And User can save information
    Then User can verify the information
    
    # Move opportunity through pipeline stages
    And User can drag and drop the pipeline
    Then User can see the new changes in progress
    
    # Manage customers
    And User can register new customer
    Then User can print the profile
```

**Python Implementation:**

All steps are automatically discovered by Behave from the `features/steps/crm_steps.py` module. Each Gherkin step maps to a corresponding Python function decorated with `@when`, `@then`, or `@step`.

**Execution:**

```bash
# Run all CRM scenarios
behave features/Crm.feature

# Run only @Smoke tagged scenarios
behave --tags=@Smoke features/Crm.feature

# Run specific scenario by name
behave features/Crm.feature --name="User can create pipeline"
```

---

## Best Practices

### Step Definition Best Practices

1. **Single Responsibility:** Each step does one logical action or verification
2. **Reusable Steps:** Use `@step` decorator for steps that can be @Given, @When, or @Then
3. **Parameterization:** Use step parameters for data-driven testing (Scenario Outlines)
4. **No Waits in Steps:** All synchronization handled by page objects
5. **Descriptive Assertions:** Provide clear error messages for assertion failures
6. **Structured Logging:** Use `logger.debug()` and `logger.info()` for diagnostics

### CRM Testing Best Practices

1. **Pipeline Management:**
   - Always verify total price calculations after opportunity creation
   - Validate opportunity titles match expected values
   - Clear form fields before entering new values to avoid concatenation

2. **Drag-and-Drop Operations:**
   - Use `ActionChains` with proper pause timing
   - Allow brief sleep after `perform()` for DOM updates
   - Verify opportunity moved to correct stage after drop

3. **Customer Management:**
   - Use unique customer names to avoid conflicts
   - Perform search validation after registration
   - Handle absolute XPath locators with caution (print_button)

4. **Data-Driven Testing:**
   - Use Scenario Outlines for parameterized tests
   - Validate all parameter combinations
   - Keep test data realistic

---

## Common Issues and Solutions

### Issue: Drag-and-Drop Failures

**Symptoms:** Opportunity doesn't move to target stage

**Causes:**
- Insufficient pause timing in ActionChains
- Browser animation not completing
- DOM not updated before verification

**Solutions:**
- Increase `pause()` durations (currently 2 seconds each)
- Add brief `time.sleep()` after `perform()` (currently 2 seconds)
- Verify source and target elements are visible before drag

### Issue: Total Price Calculation Mismatch

**Symptoms:** `AssertionError` with total price mismatch

**Causes:**
- Pre-existing opportunities in pipeline
- Revenue value not saved correctly
- Calculation logic incorrect

**Solutions:**
- Start with clean pipeline state
- Verify revenue field accepts numeric input
- Check `total_price.text` can be parsed as integer
- Validate base price + added revenue = expected total

### Issue: Print Button Not Found

**Symptoms:** `TimeoutException` when clicking print button

**Causes:**
- Absolute XPath locator changed due to DOM update
- Print button not visible in customer profile view
- JavaScript rendering delay

**Solutions:**
- Update print_button XPath locator in `CrmPage`
- Verify customer profile fully loaded before print
- Consider using more stable locator strategy (ID, name, data attribute)

### Issue: Opportunity Edit Not Saved

**Symptoms:** Verification step fails to find updated title

**Causes:**
- Save button not clicked successfully
- Form validation errors
- Network delay before save completes

**Solutions:**
- Verify all required fields filled before save
- Check for validation error messages
- Add brief wait after save before navigating away
- Verify `save_edit` button is clickable

---

## See Also

### Related API Documentation

- **[CRM Page Object API](../pages/crm-page.md)** - Complete CrmPage API reference with all locators and methods
- **[Base Page API](../pages/base-page.md)** - BasePage wait utilities and interaction methods
- **[Step Definitions Index](index.md)** - All step definition modules

### Related Guides

- **[CRM Testing Guide](../../guides/crm-testing.md)** - Comprehensive CRM workflow testing guide with advanced patterns
- **[Step Definitions Guide](../../guides/step-definitions.md)** - Writing and organizing step definitions
- **[Feature Files Guide](../../guides/feature-files.md)** - Writing effective Gherkin scenarios

### Related Architecture

- **[Wait Strategies](../../architecture/wait-strategies.md)** - Framework wait strategy and synchronization patterns
- **[Page Object Model](../../architecture/page-object-model.md)** - Page Object pattern implementation

---

**Module Metadata:**

- **Total Steps:** 12
- **Java Source:** `src/main/java/com/testinium/step_definitions/Crm.java`
- **Python Source:** `features/steps/crm_steps.py`
- **Feature File:** `features/Crm.feature`
- **Page Object:** `pages/crm_page.py`
- **Migration Date:** Python Behave BDD Framework Migration
- **Framework Version:** Behave 1.2.6 + Selenium 4.15.2

