# Step Definitions API Reference

## Overview

The Step Definitions package (`features/steps/`) contains all Behave step implementations that map Gherkin scenario statements (Given/When/Then) to executable Python code. This package serves as the integration layer between human-readable feature files and the Page Object Model, enabling true Behavior-Driven Development (BDD) with executable specifications.

**Package:** `features.steps`  
**Framework:** Behave 1.2.6+  
**Total Modules:** 10 step definition modules  
**Total Steps:** 123 step implementations  
**Pattern:** Decorator-based step registration with auto-discovery

**Source:** `features/steps/__init__.py`

## Key Concepts

### Behave Step Definition Pattern

Step definitions are Python functions decorated with `@given`, `@when`, `@then`, or `@step` decorators that match Gherkin scenario statements. When Behave executes a scenario, it matches each step text to a registered step definition function and executes the associated code.

**Basic Pattern:**

```python
from behave import given, when, then

@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """Navigate to login page using configured URL."""
    config_reader = ConfigReader()
    login_url = config_reader.get_property('web.table.url')
    context.driver.get(login_url)

@when('User enters "{username}" username')
def step_enter_username(context, username):
    """Enter username with parameterized value from Examples table."""
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)

@then('User should see the dashboard')
def step_verify_dashboard(context):
    """Verify successful login by checking dashboard title."""
    login_page = LoginPage(context.driver)
    assert login_page.dashboard.text == "Odoo"
```

**Source Example:** `features/steps/login_steps.py:90-186`

### Step Decorators

Behave provides four step decorators for different scenario statement types:

| Decorator | Purpose | Typical Use Case | Example |
|-----------|---------|------------------|---------|
| `@given` | Preconditions | Setup initial state, navigate to starting page | `Given User is on the login page` |
| `@when` | Actions | User interactions, button clicks, form inputs | `When User enters "username" username` |
| `@then` | Assertions | Verify expected outcomes, validate results | `Then User should see the dashboard` |
| `@step` | Generic | Reusable steps that fit any category (And/But) | `And User clicks the save button` |

**Usage Guidelines:**
- Use `@given` for scenario preconditions and setup
- Use `@when` for user actions and state changes
- Use `@then` for assertions and verifications
- Use `@step` for generic steps that can be used with And/But keywords

### Parameterized Step Definitions

Step definitions support parameterization through curly brace placeholders `"{parameter}"` that extract values from scenario statements:

```python
@when('User enters "{username}" username')
def step_enter_username(context, username):
    # username parameter receives value from scenario step text
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)
```

**Scenario Usage:**
```gherkin
Scenario Outline: Multiple users login
    When User enters "<username>" username
    And User enters "<password>" password
    
    Examples:
      | username                  | password       |
      | salesmanager7@info.com   | salesmanager   |
      | posmanager5@info.com     | posmanager     |
```

Each row in the Examples table executes the scenario with substituted parameter values.

**Source:** `features/steps/login_steps.py:142-186`

### Context Object Pattern

Every step definition function receives a `context` parameter - Behave's mechanism for sharing state across steps within a scenario. The context object provides access to:

**Key Context Attributes:**

| Attribute | Type | Purpose | Usage |
|-----------|------|---------|-------|
| `context.driver` | WebDriver | Thread-local browser instance | Access to Selenium WebDriver for page interactions |
| `context.config` | ConfigReader | Configuration singleton | Retrieve test configuration values |
| `context.scenario` | Scenario | Current scenario metadata | Logging, tagging, scenario-specific logic |
| `context.feature` | Feature | Current feature metadata | Feature-level context and tags |

**Example Usage:**

```python
@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    # Access WebDriver through context
    config_reader = ConfigReader()
    login_url = config_reader.get_property('web.table.url')
    context.driver.get(login_url)  # Use context.driver for navigation

@when('User enters "{username}" username')
def step_enter_username(context, username):
    # Pass context.driver to page objects
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)
```

**Thread Safety:** Each scenario execution receives its own isolated context object with a thread-local WebDriver instance from `DriverManager.get_driver()`, ensuring parallel execution safety.

**Source:** `features/steps/login_steps.py:90-136`

### Auto-Discovery Mechanism

Behave automatically discovers and registers step definitions without requiring explicit imports or registration code. This auto-discovery mechanism works as follows:

**Discovery Process:**

1. **Package Recognition:** Behave identifies the `features/steps/` directory as the step definitions package through the presence of `__init__.py`

2. **Module Scanning:** Behave scans all Python files (`.py`) in the `features/steps/` directory

3. **Decorator Detection:** Behave identifies functions decorated with `@given`, `@when`, `@then`, or `@step`

4. **Pattern Registration:** Behave registers the step text pattern and associates it with the decorated function

5. **Runtime Matching:** During scenario execution, Behave matches step text from feature files to registered patterns

**No Explicit Imports Required:**

```python
# features/steps/__init__.py
"""
Step Definitions Package.

This __init__.py file marks the directory as a Python package, enabling
Behave to automatically discover and load all step definition functions
decorated with @given, @when, and @then from modules in this package.

No explicit imports required - Behave scans all Python files in the
steps/ directory and registers decorated functions as step definitions.
"""
```

**Benefits:**
- Simplified step organization - add new step modules without registration code
- Reduced boilerplate - no import statements in package initializer
- Convention over configuration - follows Behave's standard directory structure

**Source:** `features/steps/__init__.py:21-28`

### Gherkin-to-Code Mapping

Step definitions create a direct mapping between natural language Gherkin statements and executable Python code:

**Mapping Pattern:**

```
Gherkin Feature File          →  Step Definition Module
─────────────────────────────────────────────────────────
Given User is on login page   →  @given('User is on login page')
                                  def step_navigate_to_login_page(context):
                                      # Implementation

When User enters "user" email →  @when('User enters "{email}" email')
                                  def step_enter_email(context, email):
                                      # Implementation with email parameter

Then User should see dashboard →  @then('User should see dashboard')
                                   def step_verify_dashboard(context):
                                       # Implementation
```

**Pattern Matching Rules:**
- Text matching is exact (case-sensitive, whitespace-sensitive)
- Parameters use `"{name}"` placeholder syntax (quotes required in pattern)
- Regular expressions supported for complex patterns (not used in this framework)
- Multiple steps can match the same pattern (step definition reuse)

### Page Object Integration

Step definitions serve as the integration layer between Behave scenarios and the Page Object Model. Each step typically instantiates a page object with `context.driver` and delegates actions to page object methods:

**Integration Pattern:**

```python
@when('User enters "{username}" username')
def step_enter_username(context, username):
    """
    Step definition orchestration:
    1. Instantiate page object with WebDriver from context
    2. Delegate action to page object method
    3. Page object handles element location and interaction
    """
    # Create page object instance
    login_page = LoginPage(context.driver)
    
    # Delegate to page object (waits handled by property)
    login_page.input_email.send_keys(username)
    
    # No explicit waits needed - BasePage handles synchronization
```

**Architecture Layers:**

```
Gherkin Feature File (BDD Layer)
        ↓
Step Definition (Integration Layer) ← You are here
        ↓
Page Object (Abstraction Layer)
        ↓
BasePage (Utilities Layer)
        ↓
Selenium WebDriver (Infrastructure Layer)
```

**Step Definition Responsibilities:**
- **Scenario Orchestration:** Coordinate actions across multiple page objects
- **Context Management:** Access driver and configuration from context
- **Business Logic:** Implement test-specific logic not belonging in page objects
- **Assertions:** Verify expected outcomes (page objects provide data, steps assert)

**Page Object Responsibilities:**
- **Element Location:** Define locators and provide element access
- **Wait Strategies:** Ensure elements are ready before interaction
- **Action Methods:** Provide reusable interaction methods
- **Data Retrieval:** Extract data from page elements

**Source:** `features/steps/login_steps.py:142-186`

### Thread Safety in Parallel Execution

Step definitions are inherently thread-safe when using Behave's parallel execution capabilities (`pytest-xdist` or `behave-parallel`) due to the following architectural guarantees:

**Thread Safety Mechanisms:**

1. **Isolated Context Objects:** Each scenario receives its own `context` object, preventing state sharing between parallel scenarios

2. **Thread-Local WebDriver:** `DriverManager.get_driver()` returns a thread-local WebDriver instance using Python's `threading.local()` pattern

3. **Stateless Step Functions:** Step definition functions are stateless - all state stored in context, not module or class variables

4. **Fresh Page Objects:** Page objects instantiated per-step with `PageObject(context.driver)` provide fresh element references

**Parallel Execution Pattern:**

```python
# Thread 1: Scenario A
@when('User enters "{username}" username')
def step_enter_username(context, username):
    # context → Thread 1 context object
    # context.driver → Thread 1 WebDriver instance
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)

# Thread 2: Scenario B (concurrent execution)
@when('User enters "{username}" username')
def step_enter_username(context, username):
    # context → Thread 2 context object (different from Thread 1)
    # context.driver → Thread 2 WebDriver instance (different from Thread 1)
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)
```

**Thread Isolation Guarantees:**
- No shared state between concurrent scenarios
- Independent browser instances per scenario
- Separate configuration access per thread
- No race conditions on element interactions

**Source:** `features/steps/login_steps.py:51-54`

## Step Definition Modules

The `features/steps/` package contains 10 specialized step definition modules, each implementing steps for a specific feature area of the application under test:

### Quick Reference Table

| Module | Feature Area | Step Count | Documentation | Source |
|--------|--------------|------------|---------------|--------|
| **login_steps** | Authentication | 9 steps | [Login Steps API](login-steps.md) | `features/steps/login_steps.py` |
| **logout_steps** | Session Termination | 11 steps | [Logout Steps API](logout-steps.md) | `features/steps/logout_steps.py` |
| **calendar_steps** | Calendar Management | 14 steps | [Calendar Steps API](calendar-steps.md) | `features/steps/calendar_steps.py` |
| **contacts_steps** | Contact Management | 20 steps | [Contacts Steps API](contacts-steps.md) | `features/steps/contacts_steps.py` |
| **crm_steps** | CRM Workflows | 8 steps | [CRM Steps API](crm-steps.md) | `features/steps/crm_steps.py` |
| **employee_steps** | Employee Management | 25 steps | [Employee Steps API](employee-steps.md) | `features/steps/employee_steps.py` |
| **inventory_steps** | Inventory Operations | 10 steps | [Inventory Steps API](inventory-steps.md) | `features/steps/inventory_steps.py` |
| **notes_steps** | Notes Functionality | 12 steps | [Notes Steps API](notes-steps.md) | `features/steps/notes_steps.py` |
| **sales_steps** | Sales Workflows | 8 steps | [Sales Steps API](sales-steps.md) | `features/steps/sales_steps.py` |
| **session_steps** | Session Management | 6 steps | [Session Steps API](session-steps.md) | `features/steps/session_steps.py` |
| **TOTAL** | **10 modules** | **123 steps** | — | — |

### Module Descriptions

#### Login Steps (`login_steps.py`)

Authentication workflow step definitions including user navigation, credential input, login validation, error handling, and field verification.

**Key Features:**
- Navigation to login page with configurable URL
- Parameterized username and password input
- Login button click and Enter key submission
- Dashboard title validation for successful authentication
- Error message visibility check for invalid credentials
- Field validation message verification
- Password input masking verification

**Step Count:** 9 steps (1 @given, 5 @when, 3 @then)

**Documentation:** [Login Steps API Reference](login-steps.md)

**Source:** `features/steps/login_steps.py`

#### Logout Steps (`logout_steps.py`)

Session termination step definitions for logout workflows including user menu navigation, logout action, and login page verification.

**Key Features:**
- User menu dropdown interactions
- Logout link click
- Redirect to login page verification
- Session termination validation
- Multi-user logout scenarios

**Step Count:** 11 steps

**Documentation:** [Logout Steps API Reference](logout-steps.md)

**Source:** `features/steps/logout_steps.py`

#### Calendar Steps (`calendar_steps.py`)

Calendar management step definitions for event creation, scheduling, editing, and calendar view operations.

**Key Features:**
- Calendar navigation and view switching
- Event creation with date/time selection
- Event editing and deletion
- Recurring event management
- Calendar sharing and permissions

**Step Count:** 14 steps

**Documentation:** [Calendar Steps API Reference](calendar-steps.md)

**Source:** `features/steps/calendar_steps.py`

#### Contacts Steps (`contacts_steps.py`)

Contact management step definitions for creating, searching, editing, and organizing contacts.

**Key Features:**
- Contact creation with multiple fields
- Contact search and filtering
- Contact editing and updates
- Contact deletion and archiving
- Contact import/export operations
- Tag and category management

**Step Count:** 20 steps (largest step module)

**Documentation:** [Contacts Steps API Reference](contacts-steps.md)

**Source:** `features/steps/contacts_steps.py`

#### CRM Steps (`crm_steps.py`)

Customer Relationship Management workflow step definitions for pipeline management, opportunity creation, and customer operations.

**Key Features:**
- CRM dashboard navigation
- Pipeline view and management
- Opportunity creation and editing
- Drag-and-drop pipeline stage transitions
- Customer registration and search
- Revenue tracking and reporting

**Step Count:** 8 steps (1 @when, 5 @then, 2 @step)

**Documentation:** [CRM Steps API Reference](crm-steps.md)

**Source:** `features/steps/crm_steps.py`

#### Employee Steps (`employee_steps.py`)

Employee management step definitions for employee CRUD operations, profile management, and organizational hierarchy.

**Key Features:**
- Employee creation with comprehensive profile data
- Employee search and filtering
- Employee profile editing and updates
- Department and role assignment
- Employee deactivation and archiving
- Employee reporting and analytics

**Step Count:** 25 steps (largest module by step count)

**Documentation:** [Employee Steps API Reference](employee-steps.md)

**Source:** `features/steps/employee_steps.py`

#### Inventory Steps (`inventory_steps.py`)

Inventory management step definitions for stock operations, product management, and warehouse workflows.

**Key Features:**
- Inventory navigation and dashboard
- Product stock level verification
- Inventory adjustments and transfers
- Warehouse operations
- Stock replenishment workflows
- Inventory reporting

**Step Count:** 10 steps

**Documentation:** [Inventory Steps API Reference](inventory-steps.md)

**Source:** `features/steps/inventory_steps.py`

#### Notes Steps (`notes_steps.py`)

Notes functionality step definitions for note creation, editing, organization, and sharing.

**Key Features:**
- Note creation and editing
- Note categorization and tagging
- Note search and filtering
- Note sharing and collaboration
- Note deletion and archiving
- Rich text formatting

**Step Count:** 12 steps

**Documentation:** [Notes Steps API Reference](notes-steps.md)

**Source:** `features/steps/notes_steps.py`

#### Sales Steps (`sales_steps.py`)

Sales workflow step definitions for order processing, quotation management, and sales operations.

**Key Features:**
- Sales order creation and management
- Quotation generation and approval
- Order fulfillment tracking
- Invoice generation
- Payment processing
- Sales reporting

**Step Count:** 8 steps

**Documentation:** [Sales Steps API Reference](sales-steps.md)

**Source:** `features/steps/sales_steps.py`

#### Session Steps (`session_steps.py`)

Session management step definitions for user session handling, timeout verification, and multi-session scenarios.

**Key Features:**
- Session initialization and validation
- Session timeout handling
- Multi-session management
- Session persistence verification
- Session state validation
- Concurrent session testing

**Step Count:** 6 steps

**Documentation:** [Session Steps API Reference](session-steps.md)

**Source:** `features/steps/session_steps.py`

## Common Step Patterns

### Pattern 1: Navigation and Setup (Given Steps)

Precondition steps that establish initial state before test actions:

```python
@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """Navigate to starting page using configuration."""
    config_reader = ConfigReader()
    login_url = config_reader.get_property('web.table.url')
    context.driver.get(login_url)
```

**Usage:** Background sections, scenario preconditions

### Pattern 2: User Actions (When Steps)

Action steps that simulate user interactions with parameterization:

```python
@when('User enters "{username}" username')
def step_enter_username(context, username):
    """Parameterized input with data from Examples table."""
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)
```

**Usage:** Form inputs, button clicks, navigation actions

### Pattern 3: Verification (Then Steps)

Assertion steps that validate expected outcomes:

```python
@then('User should see the dashboard')
def step_verify_dashboard(context):
    """Assert expected state after actions."""
    login_page = LoginPage(context.driver)
    assert login_page.dashboard.text == "Odoo", "Dashboard not displayed"
```

**Usage:** Result verification, state validation, error checking

### Pattern 4: Reusable Generic Steps (Step Decorator)

Generic steps that work with And/But keywords across scenarios:

```python
@step('User clicks the save button')
def step_click_save(context):
    """Generic action step usable in any scenario."""
    # Implementation
```

**Usage:** Common actions used across multiple scenarios

### Pattern 5: Complex Interactions (ActionChains)

Steps involving drag-and-drop, hover, or multi-action sequences:

```python
@step('User can drag and drop the pipeline')
def step_drag_drop_pipeline(context):
    """Complex interaction using ActionChains."""
    crm_page = CrmPage(context.driver)
    actions = ActionChains(context.driver)
    actions.drag_and_drop(
        crm_page.source_element,
        crm_page.target_element
    ).perform()
```

**Usage:** Drag-and-drop, hover menus, keyboard combinations

**Source:** `features/steps/crm_steps.py` (drag-and-drop implementation)

## Best Practices

### Step Definition Guidelines

1. **Single Responsibility:** Each step should perform one logical action or verification
2. **Descriptive Names:** Step text should clearly describe the action or assertion
3. **Reusable Steps:** Write generic steps that can be reused across multiple scenarios
4. **Avoid Business Logic:** Delegate complex logic to page objects, keep steps orchestrative
5. **Proper Assertions:** Use descriptive assertion messages for clear test failure diagnosis

### Context Usage Best Practices

```python
# ✅ CORRECT: Access driver through context
login_page = LoginPage(context.driver)

# ❌ INCORRECT: Create new driver instance
driver = DriverManager.get_driver()  # Redundant, use context.driver

# ✅ CORRECT: Fresh page object per step
@when('User clicks login')
def step_click_login(context):
    login_page = LoginPage(context.driver)  # New instance
    login_page.login_button.click()

# ❌ INCORRECT: Reuse page object across steps (stale elements risk)
# Don't store page objects in context for reuse
```

### Parameterization Best Practices

```python
# ✅ CORRECT: Use descriptive parameter names
@when('User enters "{email_address}" email')
def step_enter_email(context, email_address):
    # Parameter name documents purpose

# ❌ INCORRECT: Generic parameter names
@when('User enters "{value}" email')
def step_enter_email(context, value):
    # Unclear what value represents

# ✅ CORRECT: Type conversion in step function
@when('User sets quantity to "{quantity}"')
def step_set_quantity(context, quantity):
    quantity_int = int(quantity)  # Convert string to int
    # Use quantity_int
```

### Wait Strategy in Steps

```python
# ✅ CORRECT: Let page objects handle waits
@when('User clicks submit button')
def step_click_submit(context):
    form_page = FormPage(context.driver)
    form_page.submit_button.click()  # Property handles wait

# ❌ INCORRECT: Explicit waits in step definitions
@when('User clicks submit button')
def step_click_submit(context):
    wait = WebDriverWait(context.driver, 10)  # Redundant
    element = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
    element.click()
    # Page objects already provide this functionality
```

**Rationale:** Page object properties use `BasePage.wait_for_element()` methods, eliminating the need for explicit waits in step definitions.

## Troubleshooting

### Common Issues

#### Issue: Step Not Found Error

**Symptoms:**
```
behave.parser.ParserError: undefined step: "User clicks the login button"
```

**Cause:** Step text in feature file doesn't match any registered step definition pattern

**Solutions:**
1. Verify step text exactly matches step definition pattern (case-sensitive, whitespace-sensitive)
2. Check step definition decorator (`@given`, `@when`, `@then`, `@step`)
3. Ensure step module is in `features/steps/` directory
4. Verify no syntax errors preventing module import

#### Issue: Parameter Mismatch

**Symptoms:**
```
TypeError: step_enter_username() takes 1 positional argument but 2 were given
```

**Cause:** Step definition function signature doesn't match parameter count in step pattern

**Solutions:**
1. Add parameter to function signature: `def step_enter_username(context, username):`
2. Verify parameter placeholder in decorator: `@when('User enters "{username}" username')`
3. Ensure parameter names match (for clarity, not required)

#### Issue: Context Attribute Error

**Symptoms:**
```
AttributeError: 'Context' object has no attribute 'driver'
```

**Cause:** Context not initialized with driver in `environment.py` hooks

**Solutions:**
1. Verify `before_scenario()` hook in `features/environment.py` initializes `context.driver`
2. Check `DriverManager.get_driver()` executes successfully
3. Review error logs for driver initialization failures

#### Issue: Stale Element Reference

**Symptoms:**
```
selenium.common.exceptions.StaleElementReferenceException
```

**Cause:** Page object instance reused across steps after page state changed

**Solutions:**
1. Create fresh page object instance in each step: `page = LoginPage(context.driver)`
2. Use property-based locators (already implemented) that re-locate elements
3. Avoid storing page objects in context for reuse

## Related Documentation

### User Guides

- **[Writing Step Definitions Guide](../../guides/step-definitions.md)** - Comprehensive guide to creating custom step definitions
- **[Writing Feature Files Guide](../../guides/feature-files.md)** - Gherkin syntax and scenario patterns
- **[Page Object Model Guide](../../guides/page-object-model.md)** - Integrating page objects with step definitions
- **[Parallel Execution Guide](../../guides/parallel-execution.md)** - Thread-safe step definition patterns

### API References

- **[Pages API Reference](../pages/index.md)** - Page Object Model API for element interaction
- **[Features Environment API](../features/environment.md)** - Behave hooks and context initialization
- **[Configuration API](../config/index.md)** - Configuration access in step definitions

### Architecture Documentation

- **[Test Execution Lifecycle](../../architecture/test-execution-lifecycle.md)** - Behave scenario execution flow
- **[Parallel Execution Architecture](../../architecture/parallel-execution.md)** - Thread-local context and driver management

### Reference Documentation

- **[Gherkin Syntax Reference](../../reference/gherkin-syntax.md)** - Complete Gherkin keyword reference
- **[Behave Configuration](../../reference/behave-configuration.md)** - Behave framework configuration options

## Migration Notes

This step definitions package was migrated from Cucumber Java to Behave Python:

**Original Framework:** Cucumber Java 7.2.3  
**Target Framework:** Behave Python 1.2.6+  
**Source Package:** `src/main/java/com/testinium/step_definitions/`

**Key Transformations:**

| Java Pattern | Python Pattern | Rationale |
|--------------|----------------|-----------|
| `@Given("text")` annotation | `@given('text')` decorator | Python decorator syntax |
| Instance field `LoginP loginP` | Local variable `LoginPage(context.driver)` | Per-step instantiation prevents stale elements |
| `Driver.getDriver()` | `context.driver` | Behave context pattern for state management |
| `Assert.assertEquals()` | `assert x == y, "message"` | Python native assertions with messages |
| `WebDriverWait(driver, 3)` | Page object property waits | Centralized wait strategy in BasePage |
| Static utility classes | Context-based access | Better testability and thread safety |

**Source:** `features/steps/__init__.py:30-37`

## Package Information

**Package:** `features.steps`  
**Python Version:** 3.9+  
**Framework:** Behave 1.2.6+  
**Total Modules:** 10  
**Total Step Definitions:** 123  
**Thread-Safe:** Yes (with threading.local() pattern)  
**Parallel Execution:** Supported (pytest-xdist, behave-parallel)

**Package Initialization:** `features/steps/__init__.py`

---

**Navigation:**
- [← API Reference Index](../index.md)
- [Features API →](../features/index.md)
- [Pages API →](../pages/index.md)
