# SalesPage API Reference

## Overview

The `SalesPage` class provides a comprehensive page object for the Testinium application's Sales module, enabling sales and customer management operations through automated tests. This class handles customer creation, search, list operations, and dynamic state/country selection with validation support.

**Source:** `pages/sales_page.py`

**Inherits from:** [`BasePage`](base-page.md)

## Purpose and Responsibilities

The SalesPage class encapsulates all element interactions within the Sales module, providing:

- **Sales module navigation** using partial link text matching
- **Customer list and details access** with kanban card support
- **Customer creation forms** with name, address, state, and country fields
- **Dynamic state/country selection** with 'Create and Edit' dropdown functionality
- **Search functionality** for filtering existing customers
- **Customer card collections** supporting dynamic list element operations
- **Warning notification handling** for validation and error messages
- **Save and create button interactions** for form submissions

## Migration Context

Converted from `SalesP.java` PageFactory pattern to Python property-based locators. The original Java implementation used `@FindBy` annotations with public `WebElement` fields and `PageFactory.initElements()` for element initialization. This Python version uses property decorators with explicit waits for fresh element references, preventing stale element exceptions common in the Java PageFactory pattern.

## Technical Debt Warning

⚠️ **Critical:** This page object contains **6 generated element IDs** that are brittle and subject to change with application updates:

- `o_field_input_470` (customer_name)
- `o_field_input_474` (address)
- `o_field_input_477` (state_options)
- `o_field_input_516` (state_name)
- `o_field_input_517` (state_code)
- `o_field_input_518` (country_state_button)

**Recommendation:** Post-migration, request the development team add stable test IDs (data-testid attributes) to these form inputs for more maintainable test automation.

## Design Pattern

Follows Page Object Model with:

- **Private locator constants** as class-level tuples `(By.STRATEGY, 'locator_value')`
- **Public @property methods** returning fresh WebElement references
- **Explicit waits** via `BasePage.wait_for_element()` and `wait_for_clickable()`
- **get_elements()** for dynamic collections (customer lists)
- **Separation of locator strategy** from element access logic

## Class Definition

```python
class SalesPage(BasePage):
    """
    Sales page object for Testinium application sales and customer management.
    
    Provides access to all sales module elements including customer
    creation forms, search functionality, customer lists, and state/country
    selection dropdowns.
    """
```

**Source:** `pages/sales_page.py:71-105`

## Attributes

Inherited from [`BasePage`](base-page.md):

| Attribute | Type | Description |
|-----------|------|-------------|
| `driver` | `WebDriver` | Selenium WebDriver instance for browser control |
| `wait` | `WebDriverWait` | Pre-configured WebDriverWait for explicit waits |
| `config` | `ConfigReader` | Configuration reader for framework settings |
| `default_timeout` | `int` | Default wait timeout in seconds |
| `actions` | `ActionChains` | ActionChains instance for complex interactions |

## Locator Summary

The SalesPage defines **20 private locator constants** organized by functionality:

### Navigation Elements (3 locators)
- Sales module link (partial link text)
- Customers submenu button
- Direct customers page link

### Action Buttons (3 locators)
- Create new customer button
- Save button (form submission)
- Create customer button (final submission)

### Customer Form Inputs (6 locators)
- Customer name input ⚠️ (generated ID)
- Address input ⚠️ (generated ID)
- State options input ⚠️ (generated ID)
- State name input ⚠️ (generated ID)
- State code input ⚠️ (generated ID)
- Country state button ⚠️ (generated ID)

### Dropdown Elements (2 locators)
- 'Create and Edit...' state option
- Country selection dropdown item

### Search and Validation (2 locators)
- Search bar input field
- Customer name display (validation)

### Notifications (2 locators)
- Warning dialog button
- Warning notification container

### Collections (1 locator)
- All customer kanban cards (dynamic list)

### Details (1 locator)
- Customer details span element

## Properties

### Navigation Properties

#### sales_partial

```python
@property
def sales_partial(self) -> WebElement
```

Sales module navigation link using partial link text match.

**Returns:**
- `WebElement`: Sales navigation link element

**Wait Strategy:** Uses `wait_for_clickable()` to ensure element is both visible and clickable

**Example:**
```python
from pages.sales_page import SalesPage

sales_page = SalesPage(driver)
sales_page.sales_partial.click()  # Navigate to Sales module
```

**Source:** `pages/sales_page.py:214-224`

---

#### customers_button

```python
@property
def customers_button(self) -> WebElement
```

Customers submenu button with specific href navigation (`/web#menu_id=447&action=48`).

**Returns:**
- `WebElement`: Customers button span element

**Wait Strategy:** Uses `wait_for_clickable()` to ensure element is interactable

**Example:**
```python
sales_page.customers_button.click()  # Navigate to Customers view
```

**Source:** `pages/sales_page.py:227-237`

---

#### link

```python
@property
def link(self) -> WebElement
```

Direct link to customers page providing alternative navigation path.

**Returns:**
- `WebElement`: Customers page link element

**Wait Strategy:** Uses `wait_for_clickable()`

**Example:**
```python
sales_page.link.click()  # Alternative navigation to Customers
```

**Source:** `pages/sales_page.py:484-494`

---

### Action Button Properties

#### create_button

```python
@property
def create_button(self) -> WebElement
```

Create new customer button in kanban view. Opens the customer creation form.

**Returns:**
- `WebElement`: Create button element with classes `btn btn-primary btn-sm o-kanban-button-new btn-default`

**Wait Strategy:** Uses `wait_for_clickable()`

**Example:**
```python
sales_page.create_button.click()  # Open customer creation form
```

**Source:** `pages/sales_page.py:240-250`

---

#### save_button

```python
@property
def save_button(self) -> WebElement
```

Save button for state/country form submission.

**Returns:**
- `WebElement`: Save button span element

**Wait Strategy:** Uses `wait_for_clickable()`

**Example:**
```python
# After filling state/country form
sales_page.save_button.click()
```

**Source:** `pages/sales_page.py:376-386`

---

#### create_customer

```python
@property
def create_customer(self) -> WebElement
```

Create customer button for final customer form submission. Click this after filling all customer details.

**Returns:**
- `WebElement`: Create customer button element with class `btn btn-primary btn-sm o_form_button_save`

**Wait Strategy:** Uses `wait_for_clickable()`

**Example:**
```python
# After filling customer form
sales_page.customer_name.send_keys("ACME Corporation")
sales_page.address.send_keys("123 Main Street")
sales_page.create_customer.click()  # Submit customer
```

**Source:** `pages/sales_page.py:389-399`

---

### Customer Form Input Properties

#### customer_name

```python
@property
def customer_name(self) -> WebElement
```

Customer name input field for entering company or individual name.

⚠️ **Technical Debt:** Uses generated ID `o_field_input_470` which may change with application updates. Recommend stable test ID attribute.

**Returns:**
- `WebElement`: Customer name input element

**Wait Strategy:** Uses `wait_for_element()` for presence check

**Example:**
```python
sales_page.customer_name.send_keys("ACME Corporation")
```

**Source:** `pages/sales_page.py:252-267`

---

#### address

```python
@property
def address(self) -> WebElement
```

Customer address input field for street address entry.

⚠️ **Technical Debt:** Uses generated ID `o_field_input_474` which may change with app updates.

**Returns:**
- `WebElement`: Address input element

**Wait Strategy:** Uses `wait_for_element()`

**Example:**
```python
sales_page.address.send_keys("123 Main Street, Suite 100")
```

**Source:** `pages/sales_page.py:270-283`

---

#### state_options

```python
@property
def state_options(self) -> WebElement
```

State selection dropdown input field. Click to open state selection menu.

⚠️ **Technical Debt:** Uses generated ID `o_field_input_477` which may change with app updates.

**Returns:**
- `WebElement`: State options input element

**Wait Strategy:** Uses `wait_for_element()`

**Example:**
```python
sales_page.state_options.click()  # Open state dropdown
sales_page.create_and_edit_state.click()  # Select 'Create and Edit...'
```

**Source:** `pages/sales_page.py:286-299`

---

#### state_name

```python
@property
def state_name(self) -> WebElement
```

State name input field in state creation dialog. Available after selecting 'Create and Edit...' option.

⚠️ **Technical Debt:** Uses generated ID `o_field_input_516` which may change with app updates.

**Returns:**
- `WebElement`: State name input element

**Wait Strategy:** Uses `wait_for_element()`

**Example:**
```python
sales_page.state_options.click()
sales_page.create_and_edit_state.click()
sales_page.state_name.send_keys("California")
```

**Source:** `pages/sales_page.py:315-328`

---

#### state_code

```python
@property
def state_code(self) -> WebElement
```

State code input field in state creation dialog for entering standard state abbreviations.

⚠️ **Technical Debt:** Uses generated ID `o_field_input_517` which may change with app updates.

**Returns:**
- `WebElement`: State code input element

**Wait Strategy:** Uses `wait_for_element()`

**Example:**
```python
sales_page.state_code.send_keys("CA")
```

**Source:** `pages/sales_page.py:331-344`

---

#### country_state_button

```python
@property
def country_state_button(self) -> WebElement
```

Country selection button for state association. Used to link a state with its country.

⚠️ **Technical Debt:** Uses generated ID `o_field_input_518` which may change with app updates.

**Returns:**
- `WebElement`: Country state button input element

**Wait Strategy:** Uses `wait_for_element()`

**Example:**
```python
sales_page.country_state_button.click()  # Open country dropdown
sales_page.country_selection.click()  # Select country
```

**Source:** `pages/sales_page.py:347-360`

---

### Dropdown Selection Properties

#### create_and_edit_state

```python
@property
def create_and_edit_state(self) -> WebElement
```

'Create and Edit...' option in state dropdown menu. Selecting this opens a dialog for creating new states.

**Returns:**
- `WebElement`: Create and edit list item element

**Wait Strategy:** Uses `wait_for_clickable()`

**Example:**
```python
sales_page.state_options.click()
sales_page.create_and_edit_state.click()  # Open state creation dialog
```

**Source:** `pages/sales_page.py:302-312`

---

#### country_selection

```python
@property
def country_selection(self) -> WebElement
```

Country selection item in dropdown with specific UI ID (`ui-id-30`).

**Returns:**
- `WebElement`: Country selection link element

**Wait Strategy:** Uses `wait_for_clickable()`

**Example:**
```python
sales_page.country_selection.click()  # Select country from dropdown
```

**Source:** `pages/sales_page.py:363-373`

---

### Search and Validation Properties

#### search_bar

```python
@property
def search_bar(self) -> WebElement
```

Search input field for filtering customer list. Enter text to search customers by name or other attributes.

**Returns:**
- `WebElement`: Search bar input element

**Wait Strategy:** Uses `wait_for_element()`

**Example:**
```python
from selenium.webdriver.common.keys import Keys

sales_page.search_bar.send_keys("ACME")
sales_page.search_bar.send_keys(Keys.RETURN)  # Execute search
```

**Source:** `pages/sales_page.py:402-413`

---

#### name_check

```python
@property
def name_check(self) -> WebElement
```

Customer name display in kanban card used for validation after customer creation.

**Returns:**
- `WebElement`: Customer name span element with classes `o_kanban_record_title oe_partner_heading`

**Wait Strategy:** Uses `wait_for_element()`

**Example:**
```python
displayed_name = sales_page.name_check.text
assert displayed_name == "ACME Corporation", "Customer name mismatch"
```

**Source:** `pages/sales_page.py:416-427`

---

### Notification Properties

#### warning_button

```python
@property
def warning_button(self) -> WebElement
```

Warning dialog button for primary action in warning notifications.

**Returns:**
- `WebElement`: Warning button element with class `btn btn-sm btn-primary`

**Wait Strategy:** Uses `wait_for_clickable()`

**Example:**
```python
# Handle warning dialog if present
if sales_page.warning.is_displayed():
    sales_page.warning_button.click()  # Dismiss warning
```

**Source:** `pages/sales_page.py:430-440`

---

#### warning

```python
@property
def warning(self) -> WebElement
```

Warning notification container element for detecting validation messages or errors.

**Returns:**
- `WebElement`: Warning notification manager div with class `o_notification_manager`

**Wait Strategy:** Uses `wait_for_visibility()`

**Example:**
```python
if sales_page.warning.is_displayed():
    print("Warning notification detected")
    warning_text = sales_page.warning.text
    print(f"Warning message: {warning_text}")
```

**Source:** `pages/sales_page.py:443-454`

---

### Collection Properties

#### all_customers

```python
@property
def all_customers(self) -> List[WebElement]
```

Collection of all customer kanban cards in current view. Returns dynamic list of customer elements.

**Returns:**
- `List[WebElement]`: List of customer card elements (empty list if none found)

**Wait Strategy:** Uses `get_elements()` which returns immediately without explicit wait

**Important Note:**

This property returns a list of WebElements representing dynamic customer cards. Unlike single-element properties, this uses `get_elements()` which returns immediately. If you need to ensure at least one customer exists, wait for the first element before calling:

```python
# Wait for at least one customer card
sales_page.wait_for_element(sales_page._ALL_CUSTOMERS)
# Then get all cards
customers = sales_page.all_customers
```

**Example:**
```python
# Get all customer cards
customers = sales_page.all_customers
print(f"Found {len(customers)} customers")

# Iterate through customers
for customer in customers:
    print(f"Customer: {customer.text}")
    
# Count specific customers
acme_customers = [c for c in customers if "ACME" in c.text]
print(f"Found {len(acme_customers)} ACME customers")
```

**Source:** `pages/sales_page.py:457-481`

---

### Detail Properties

#### details

```python
@property
def details(self) -> WebElement
```

Customer details span element within kanban card displaying additional customer information.

**Returns:**
- `WebElement`: Customer details span element

**Wait Strategy:** Uses `wait_for_element()`

**Example:**
```python
details_text = sales_page.details.text
print(f"Customer details: {details_text}")
```

**Source:** `pages/sales_page.py:497-508`

---

## Complete Workflow Examples

### Example 1: Basic Customer Creation

Complete workflow for creating a new customer with minimal information:

```python
from selenium import webdriver
from pages.sales_page import SalesPage
from utilities.driver_manager import DriverManager

# Get WebDriver instance
driver = DriverManager.get_driver()
sales_page = SalesPage(driver)

# Navigate to Sales > Customers
sales_page.sales_partial.click()
sales_page.customers_button.click()

# Create new customer
sales_page.create_button.click()
sales_page.customer_name.send_keys("ACME Corporation")
sales_page.address.send_keys("123 Main Street")
sales_page.create_customer.click()

# Verify customer created
assert sales_page.name_check.text == "ACME Corporation"
print("Customer created successfully!")
```

### Example 2: Customer Creation with State/Country

Advanced workflow including dynamic state and country selection:

```python
from pages.sales_page import SalesPage

sales_page = SalesPage(driver)

# Navigate to customers
sales_page.sales_partial.click()
sales_page.customers_button.click()

# Start customer creation
sales_page.create_button.click()
sales_page.customer_name.send_keys("Tech Industries Inc")
sales_page.address.send_keys("456 Innovation Drive")

# Create new state
sales_page.state_options.click()
sales_page.create_and_edit_state.click()
sales_page.state_name.send_keys("California")
sales_page.state_code.send_keys("CA")

# Select country for state
sales_page.country_state_button.click()
sales_page.country_selection.click()
sales_page.save_button.click()  # Save state

# Complete customer creation
sales_page.create_customer.click()

# Verify
assert "Tech Industries Inc" in sales_page.name_check.text
```

### Example 3: Searching for Customers

Search for existing customers and verify results:

```python
from selenium.webdriver.common.keys import Keys
from pages.sales_page import SalesPage

sales_page = SalesPage(driver)

# Navigate to customers list
sales_page.sales_partial.click()
sales_page.customers_button.click()

# Search for customer
search_term = "ACME"
sales_page.search_bar.send_keys(search_term)
sales_page.search_bar.send_keys(Keys.RETURN)

# Wait for search results and verify
sales_page.wait_for_element(sales_page._ALL_CUSTOMERS)
customers = sales_page.all_customers

# Filter and verify
matching_customers = [c for c in customers if search_term.upper() in c.text.upper()]
print(f"Found {len(matching_customers)} customers matching '{search_term}'")

for customer in matching_customers:
    print(f"  - {customer.text}")
```

### Example 4: Working with Customer Collections

Iterate through all customers and perform operations:

```python
from pages.sales_page import SalesPage

sales_page = SalesPage(driver)

# Navigate to customers
sales_page.sales_partial.click()
sales_page.customers_button.click()

# Wait for customers to load
sales_page.wait_for_element(sales_page._ALL_CUSTOMERS)

# Get all customer cards
customers = sales_page.all_customers
total_customers = len(customers)

print(f"Total customers in view: {total_customers}")

# Process each customer
for index, customer in enumerate(customers, 1):
    customer_name = customer.find_element(By.TAG_NAME, "strong").text
    print(f"{index}. {customer_name}")
    
    # Click to view details
    customer.click()
    
    # Get detailed information
    details = sales_page.details.text
    print(f"   Details: {details}")
    
    # Navigate back to list (implementation depends on your app)
    # driver.back()
```

### Example 5: Handling Warnings

Handle warning notifications during customer operations:

```python
from selenium.common.exceptions import TimeoutException
from pages.sales_page import SalesPage

sales_page = SalesPage(driver)

# Navigate to customers
sales_page.sales_partial.click()
sales_page.customers_button.click()

# Attempt customer creation
sales_page.create_button.click()

# Try to save without required fields (may trigger warning)
sales_page.create_customer.click()

# Check for warning notification
try:
    if sales_page.warning.is_displayed():
        warning_text = sales_page.warning.text
        print(f"Warning detected: {warning_text}")
        
        # Dismiss warning
        sales_page.warning_button.click()
        
        # Now fill required fields
        sales_page.customer_name.send_keys("Required Name")
        sales_page.create_customer.click()
except TimeoutException:
    print("No warning displayed - operation successful")
```

## Thread Safety

Each `SalesPage` instance is tied to a specific WebDriver instance. Thread safety is achieved through:

- **Thread-local WebDriver instances** from `DriverManager.get_driver()`
- **Instance-level state** - each page object operates on its own driver
- **Stateless property accessors** - each property call fetches fresh elements
- **No shared mutable state** between page object instances

When running tests in parallel, each thread receives its own WebDriver instance and corresponding page objects, ensuring complete isolation.

## Common Patterns

### Pattern 1: Navigation Pattern

Standard navigation to Sales customers view:

```python
sales_page.sales_partial.click()
sales_page.customers_button.click()
```

### Pattern 2: Form Filling Pattern

Fill customer form with explicit waits handled automatically:

```python
sales_page.customer_name.send_keys("Customer Name")
sales_page.address.send_keys("Address")
sales_page.create_customer.click()
```

### Pattern 3: Dynamic Collection Pattern

Work with dynamic customer lists safely:

```python
# Wait for first element
sales_page.wait_for_element(sales_page._ALL_CUSTOMERS)
# Then get all
customers = sales_page.all_customers
```

### Pattern 4: Validation Pattern

Validate customer creation or modifications:

```python
expected_name = "ACME Corporation"
actual_name = sales_page.name_check.text
assert actual_name == expected_name, f"Expected {expected_name}, got {actual_name}"
```

## Troubleshooting

### Issue: Generated ID Elements Not Found

**Symptoms:** NoSuchElementException for customer_name, address, or state fields

**Cause:** Generated IDs (o_field_input_470, 474, 477, 516, 517, 518) changed after application update

**Solution:**
1. Inspect the element in browser to find new generated ID
2. Update the locator constant in `pages/sales_page.py`
3. Better long-term: Request stable data-testid attributes from development team

### Issue: Customer List Empty

**Symptoms:** `all_customers` returns empty list `[]`

**Cause:** Elements not yet loaded, or no customers exist in current view

**Solution:**
```python
# Add explicit wait before getting collection
sales_page.wait_for_element(sales_page._ALL_CUSTOMERS, timeout=10)
customers = sales_page.all_customers

if not customers:
    print("No customers found in current view")
```

### Issue: State/Country Dropdown Not Working

**Symptoms:** Dropdown options not clickable or not appearing

**Cause:** Timing issue - dropdown not fully rendered before interaction

**Solution:**
```python
# Add small delay for dropdown animation
import time
sales_page.state_options.click()
time.sleep(0.5)  # Allow dropdown animation
sales_page.create_and_edit_state.click()
```

### Issue: Warning Notification Blocking Interaction

**Symptoms:** Elements not interactable due to overlay warning

**Cause:** Warning notification displayed and not dismissed

**Solution:**
```python
# Check and dismiss warnings before proceeding
try:
    if sales_page.warning.is_displayed():
        sales_page.warning_button.click()
except:
    pass  # No warning present
```

## See Also

- **[BasePage API Reference](base-page.md)** - Parent class with wait utilities and element interaction methods
- **[Sales Testing Guide](../../guides/sales-testing.md)** - Comprehensive guide for testing sales workflows
- **[Configuration Reference](../../reference/configuration-options.md)** - Configuration options for browser and timeouts
- **[Wait Strategies Guide](../../guides/wait-strategies.md)** - Best practices for explicit waits
- **[Page Object Model Guide](../../guides/page-object-model.md)** - Understanding the POM pattern implementation

## Related Page Objects

- **[CrmPage](crm-page.md)** - CRM pipeline and opportunity management
- **[ContactsPage](contacts-page.md)** - Contact management operations
- **[InventoryPage](inventory-page.md)** - Inventory and product management

---

**Documentation Version:** 1.0.0  
**Last Updated:** 2024  
**Source File:** `pages/sales_page.py` (lines 1-531)
