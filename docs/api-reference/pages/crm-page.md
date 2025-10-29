# CrmPage API Reference

**Source:** `pages/crm_page.py`

## Overview

The `CrmPage` class provides a comprehensive page object for CRM (Customer Relationship Management) pipeline and opportunity management functionality within the Testinium application. This page object implements 28 element properties organized into six functional categories: navigation, opportunity creation, pipeline stage management, opportunity editing, customer management, and payment operations.

The class inherits from `BasePage` to leverage explicit wait utilities and ActionChains for drag-and-drop interactions, enabling robust test automation of CRM workflows including opportunity lifecycle management, pipeline visualization, and customer operations.

**Key Features:**
- CRM module navigation and opportunity creation forms
- Pipeline stage management with drag-and-drop support for moving opportunities
- Customer management operations (create, search, view)
- Opportunity editing with dynamic fields (revenue, probability)
- Print and payment operations
- Comprehensive technical debt documentation for maintainability

**Thread Safety:**
`CrmPage` instances are thread-safe when each thread has its own WebDriver instance (via `DriverManager` threading.local()). Each property access returns a fresh WebElement reference via explicit waits, preventing cross-thread element reference issues.

**Migration Context:**
Converted from Java `CrmP.java` PageFactory pattern to Python property-based locators. All 28 `@FindBy` annotations have been converted to private locator tuples with corresponding `@property` methods that use BasePage wait utilities. This prevents stale element references and provides better encapsulation than Java's public WebElement fields.

---

## Critical Technical Debt

!!! danger "Brittle Locators Requiring Attention"
    
    The CrmPage implementation contains several fragile locators that pose maintainability risks. These have been preserved from the Java implementation to maintain behavioral equivalence, but require attention:

### HIGHEST PRIORITY - Absolute XPath

**`_PRINT_BUTTON`** (Line 207-210)
- **Locator:** `/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button`
- **Risk Level:** CRITICAL
- **Issue:** Absolute XPath will break with ANY DOM structure change
- **Java Source:** Line 94 in CrmP.java
- **Recommendation:** Work with development team to add `data-testid` or stable ID attribute
- **Impact:** High - Print functionality tests will fail on any UI update

### HIGH PRIORITY - Generated Element IDs

**`_EXPECTED_REVENUE_EDIT`** (Line 174-177)
- **Locator:** `id='o_field_input_125'`
- **Risk Level:** HIGH
- **Issue:** ID appears auto-generated and may change between deployments
- **Java Source:** Line 52 in CrmP.java
- **Recommendation:** Request stable identifier or use name/data attributes

**`_PROBABILITY_EDIT`** (Line 179-182)
- **Locator:** `id='o_field_input_127'`
- **Risk Level:** HIGH
- **Issue:** ID appears auto-generated and may change between deployments
- **Java Source:** Line 55 in CrmP.java
- **Recommendation:** Request stable identifier or use name/data attributes

### MEDIUM PRIORITY - Index-Based XPath

**`_PRIORITY`** (Line 145-148)
- **Locator:** `//tr[4]//a[3]`
- **Risk Level:** MEDIUM
- **Issue:** Brittle to DOM structure changes (row/column position dependent)
- **Java Source:** Line 31 in CrmP.java
- **Recommendation:** Use semantic attributes instead of position-based selection

### MEDIUM PRIORITY - Data-ID Selectors

The following elements use `data-id` attributes that may be framework-generated:
- `_FIND_TITLE_TEST`: `data-id='1'`
- `_TOTAL_PRICE`: `data-id='1'`
- `_BUTTON_PIPELINE`: `data-id='1'`
- `_PROGRESS_PIPELINE`: `data-id='1'`
- `_PROGRESS_PIPELINE2`: `data-id='2'`
- `_TEST_VERIFY`: `data-id='2'`

**Status:** These appear intentional (framework data attributes)  
**Risk Level:** MEDIUM - May be stable if framework-generated, but requires verification

---

## Class Definition

```python
class CrmPage(BasePage):
    """Page object for CRM pipeline and opportunity management."""
```

**Inheritance:** [`BasePage`](base-page.md)

**Attributes:**
- Inherits all attributes from `BasePage`: `driver`, `wait`, `config`, `actions`
- 28 private locator constants (tuples of By strategy and selector)
- 28 public element properties (returning WebElement instances)

**Element Categories:**
1. **Navigation** (1 element): CRM module access
2. **Opportunity Creation** (7 elements): Form fields for creating new opportunities
3. **Pipeline Management** (7 elements): Pipeline visualization and drag-and-drop
4. **Opportunity Editing** (5 elements): Edit existing opportunity details
5. **Customer Management** (6 elements): Customer creation and search
6. **Payment Operations** (2 elements): Print and payment functionality

---

## Navigation Elements

### crm_link

```python
@property
def crm_link(self) -> WebElement
```

CRM module navigation link for accessing the CRM section of the application.

**Locator Strategy:** `By.PARTIAL_LINK_TEXT, "CRM"`

**Returns:**
- `WebElement`: Clickable link to access CRM module

**Wait Strategy:** `wait_for_clickable()` - Waits until element is both visible and clickable

**Example:**
```python
from pages.crm_page import CrmPage

crm_page = CrmPage(driver)
crm_page.crm_link.click()  # Navigate to CRM module
```

**Source:** `pages/crm_page.py:220-231`

---

## Opportunity Creation Elements

### create_button

```python
@property
def create_button(self) -> WebElement
```

Create button for initiating new opportunity creation workflow.

**Locator Strategy:** `By.XPATH, "//button[@accesskey='c']"`

**Returns:**
- `WebElement`: Clickable button with accesskey 'c' for keyboard shortcut support

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
crm_page.crm_link.click()
crm_page.create_button.click()  # Open opportunity creation form
```

**Source:** `pages/crm_page.py:235-246`

---

### opportunity_title

```python
@property
def opportunity_title(self) -> WebElement
```

Opportunity title input field for entering the name of a new opportunity.

**Locator Strategy:** `By.NAME, "name"`

**Returns:**
- `WebElement`: Input field for opportunity name/title

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
crm_page.opportunity_title.send_keys("Q4 Enterprise Deal")
```

**Source:** `pages/crm_page.py:248-259`

---

### customer

```python
@property
def customer(self) -> WebElement
```

Customer input field for selecting or entering customer name for the opportunity.

**Locator Strategy:** `By.XPATH, "//table[@class='o_group o_inner_group o_group_col_6']//div//div//input"`

**Returns:**
- `WebElement`: Input field for customer name/selection

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
crm_page.customer.send_keys("Acme Corporation")
```

**Source:** `pages/crm_page.py:261-272`

---

### customer_id

```python
@property
def customer_id(self) -> WebElement
```

Customer ID link element displaying the customer identifier (shows as '&CC').

**Locator Strategy:** `By.XPATH, "//a[.='&CC']"`

**Returns:**
- `WebElement`: Clickable link displaying customer ID

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
customer_id = crm_page.customer_id.text
crm_page.customer_id.click()  # View customer details
```

**Source:** `pages/crm_page.py:274-285`

---

### expected_revenue

```python
@property
def expected_revenue(self) -> WebElement
```

Expected revenue input field for entering the anticipated deal value.

**Locator Strategy:** `By.XPATH, "//div[@class='o_row']//input"`

**Returns:**
- `WebElement`: Input field for revenue amount

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
crm_page.expected_revenue.send_keys("50000")
```

**Source:** `pages/crm_page.py:287-298`

---

### priority

```python
@property
def priority(self) -> WebElement
```

Priority selection link for setting opportunity priority level.

!!! warning "Technical Debt"
    Uses index-based XPath (`//tr[4]//a[3]`) which is brittle to DOM structure changes. See [Technical Debt](#medium-priority---index-based-xpath) section.

**Locator Strategy:** `By.XPATH, "//table[@class='o_group o_inner_group o_group_col_6']//tr[4]//a[3]"`

**Returns:**
- `WebElement`: Clickable priority selector

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
crm_page.priority.click()  # Open priority dropdown
```

**Source:** `pages/crm_page.py:300-314`

---

### create_pipeline

```python
@property
def create_pipeline(self) -> WebElement
```

Create/close dialog button to complete opportunity creation and add to pipeline.

**Locator Strategy:** `By.XPATH, "//button[@name='close_dialog']"`

**Returns:**
- `WebElement`: Button to complete opportunity creation

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
# Complete opportunity creation flow
crm_page.create_button.click()
crm_page.opportunity_title.send_keys("New Deal")
crm_page.customer.send_keys("Acme Corp")
crm_page.expected_revenue.send_keys("50000")
crm_page.create_pipeline.click()  # Finalize creation
```

**Source:** `pages/crm_page.py:316-327`

---

## Pipeline Management Elements

### find_title_test

```python
@property
def find_title_test(self) -> WebElement
```

Opportunity title display within the first pipeline stage card.

**Locator Strategy:** `By.XPATH, "//div[@data-id='1']/div[2]//strong//span"`

**Returns:**
- `WebElement`: Title element within pipeline card (data-id='1')

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
title_text = crm_page.find_title_test.text
assert "Q4 Enterprise Deal" in title_text
```

**Source:** `pages/crm_page.py:331-342`

---

### total_price

```python
@property
def total_price(self) -> WebElement
```

Total price/revenue display in the first pipeline stage card.

**Locator Strategy:** `By.XPATH, "//div[@data-id='1']//b"`

**Returns:**
- `WebElement`: Bold element showing revenue amount

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
price = crm_page.total_price.text
assert "$50,000" in price
```

**Source:** `pages/crm_page.py:344-355`

---

### button_pipeline

```python
@property
def button_pipeline(self) -> WebElement
```

Pipeline stage button/card for the first pipeline stage (data-id='1').

**Locator Strategy:** `By.XPATH, "//div[@data-id='1']/div[2]"`

**Returns:**
- `WebElement`: Clickable pipeline stage card

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
crm_page.button_pipeline.click()  # Open opportunity details
```

**Source:** `pages/crm_page.py:357-368`

---

### progress_pipeline

```python
@property
def progress_pipeline(self) -> WebElement
```

First pipeline progress stage element used for drag-and-drop operations.

**Locator Strategy:** `By.XPATH, "//div[@data-id='1']/div[2]"`

**Returns:**
- `WebElement`: Draggable pipeline stage element

**Wait Strategy:** `wait_for_visibility()` - Required for drag-and-drop operations

**Example:**
```python
# Drag opportunity from stage 1 to stage 2
crm_page.drag_and_drop(
    crm_page._PROGRESS_PIPELINE,
    crm_page._PROGRESS_PIPELINE2
)
```

**Source:** `pages/crm_page.py:370-387`

---

### progress_pipeline2

```python
@property
def progress_pipeline2(self) -> WebElement
```

Second pipeline progress stage element used as drop target for drag-and-drop operations.

**Locator Strategy:** `By.XPATH, "//div[@data-id='2']/div[2]"`

**Returns:**
- `WebElement`: Drop target pipeline stage element

**Wait Strategy:** `wait_for_visibility()`

**Example:**
```python
# Move opportunity to second stage
crm_page.drag_and_drop(
    crm_page._PROGRESS_PIPELINE,
    crm_page._PROGRESS_PIPELINE2
)
# Verify move was successful
assert crm_page.test_verify.is_displayed()
```

**Source:** `pages/crm_page.py:389-406`

---

### test_verify

```python
@property
def test_verify(self) -> WebElement
```

Verification element in the second pipeline stage for confirming successful drag-and-drop operations.

**Locator Strategy:** `By.XPATH, "//div[@data-id='2']//div[2]//strong//span"`

**Returns:**
- `WebElement`: Element for verifying opportunity moved to stage 2

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
# Verify opportunity appears in second stage after drag
verify_text = crm_page.test_verify.text
assert "Expected Title" in verify_text
```

**Source:** `pages/crm_page.py:408-420`

---

### pipeline_side_button

```python
@property
def pipeline_side_button(self) -> WebElement
```

Pipeline sidebar navigation button for accessing the pipeline overview.

**Locator Strategy:** `By.XPATH, "//a[@href='/web#menu_id=274&action=365']/span"`

**Returns:**
- `WebElement`: Sidebar link to pipeline view

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
crm_page.pipeline_side_button.click()  # Navigate to pipeline view
```

**Source:** `pages/crm_page.py:422-433`

---

## Opportunity Editing Elements

### edit_button

```python
@property
def edit_button(self) -> WebElement
```

Edit button for entering edit mode on an existing opportunity.

**Locator Strategy:** `By.XPATH, "//button[@accesskey='a']"`

**Returns:**
- `WebElement`: Button to enter edit mode (accesskey='a')

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
# Open opportunity then edit
crm_page.button_pipeline.click()
crm_page.edit_button.click()
```

**Source:** `pages/crm_page.py:437-448`

---

### opportunity_title_edit

```python
@property
def opportunity_title_edit(self) -> WebElement
```

Opportunity title input field in edit mode for modifying the opportunity name.

**Locator Strategy:** `By.XPATH, "//input[@name='name']"`

**Returns:**
- `WebElement`: Input field for editing opportunity title

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
crm_page.edit_button.click()
crm_page.opportunity_title_edit.clear()
crm_page.opportunity_title_edit.send_keys("Updated Deal Name")
crm_page.save_edit.click()
```

**Source:** `pages/crm_page.py:450-462`

---

### expected_revenue_edit

```python
@property
def expected_revenue_edit(self) -> WebElement
```

Expected revenue input field in edit mode for modifying the deal value.

!!! danger "Critical Technical Debt"
    Uses generated ID `o_field_input_125` which may change between deployments. See [Technical Debt](#high-priority---generated-element-ids) section. This is a high-priority maintainability risk.

**Locator Strategy:** `By.XPATH, "//input[@id='o_field_input_125']"`

**Returns:**
- `WebElement`: Input field for editing revenue amount

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
crm_page.edit_button.click()
crm_page.expected_revenue_edit.clear()
crm_page.expected_revenue_edit.send_keys("75000")
crm_page.save_edit.click()
```

**Source:** `pages/crm_page.py:464-480`

---

### probability_edit

```python
@property
def probability_edit(self) -> WebElement
```

Probability input field in edit mode for modifying the win probability percentage.

!!! danger "Critical Technical Debt"
    Uses generated ID `o_field_input_127` which may change between deployments. See [Technical Debt](#high-priority---generated-element-ids) section. This is a high-priority maintainability risk.

**Locator Strategy:** `By.XPATH, "//input[@id='o_field_input_127']"`

**Returns:**
- `WebElement`: Input field for editing win probability

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
crm_page.edit_button.click()
crm_page.probability_edit.clear()
crm_page.probability_edit.send_keys("85")
crm_page.save_edit.click()
```

**Source:** `pages/crm_page.py:482-498`

---

### save_edit

```python
@property
def save_edit(self) -> WebElement
```

Save button in edit mode to persist changes to the opportunity.

**Locator Strategy:** `By.XPATH, "//button[@accesskey='s']"`

**Returns:**
- `WebElement`: Button to save opportunity changes (accesskey='s')

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
# Complete edit workflow
crm_page.edit_button.click()
crm_page.opportunity_title_edit.send_keys(" - Updated")
crm_page.save_edit.click()
```

**Source:** `pages/crm_page.py:500-511`

---

## Customer Management Elements

### customer_side_button

```python
@property
def customer_side_button(self) -> WebElement
```

Customer sidebar navigation button for accessing customer management section.

**Locator Strategy:** `By.XPATH, "//a[@href='/web#menu_id=272&action=48']"`

**Returns:**
- `WebElement`: Sidebar link to customer management

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
crm_page.customer_side_button.click()  # Navigate to customers
```

**Source:** `pages/crm_page.py:515-526`

---

### create_customer

```python
@property
def create_customer(self) -> WebElement
```

Create customer button to initiate new customer creation workflow.

**Locator Strategy:** `By.XPATH, "//button[@accesskey='c']"`

**Returns:**
- `WebElement`: Button to initiate customer creation (accesskey='c')

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
crm_page.customer_side_button.click()
crm_page.create_customer.click()
```

**Source:** `pages/crm_page.py:528-539`

---

### input_name

```python
@property
def input_name(self) -> WebElement
```

Customer name input field for entering the customer's company or individual name.

**Locator Strategy:** `By.XPATH, "//input[@name='name']"`

**Returns:**
- `WebElement`: Input field for customer name

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
crm_page.create_customer.click()
crm_page.input_name.send_keys("Acme Corporation")
crm_page.create_customer_button.click()
```

**Source:** `pages/crm_page.py:541-552`

---

### create_customer_button

```python
@property
def create_customer_button(self) -> WebElement
```

Create/close dialog button to complete customer creation.

**Locator Strategy:** `By.XPATH, "//button[@name='close_dialog']"`

**Returns:**
- `WebElement`: Button to complete customer creation

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
# Complete customer creation
crm_page.create_customer.click()
crm_page.input_name.send_keys("New Customer")
crm_page.create_customer_button.click()
```

**Source:** `pages/crm_page.py:554-565`

---

### searching_text

```python
@property
def searching_text(self) -> WebElement
```

Search input field for finding existing customers by name or other criteria.

**Locator Strategy:** `By.XPATH, "//input[@class='o_searchview_input']"`

**Returns:**
- `WebElement`: Search input field

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
from selenium.webdriver.common.keys import Keys

crm_page.customer_side_button.click()
crm_page.searching_text.send_keys("Acme")
crm_page.searching_text.send_keys(Keys.ENTER)
```

**Source:** `pages/crm_page.py:567-579`

---

### name_customer

```python
@property
def name_customer(self) -> WebElement
```

Customer name element in search results, displaying as '&CC'.

**Locator Strategy:** `By.XPATH, "//span[.='&CC']"`

**Returns:**
- `WebElement`: Customer name span in search results

**Wait Strategy:** `wait_for_element()`

**Example:**
```python
# Search and select customer
crm_page.searching_text.send_keys("&CC")
customer_name = crm_page.name_customer.text
crm_page.name_customer.click()  # View customer details
```

**Source:** `pages/crm_page.py:581-593`

---

## Payment Operations Elements

### due_payment_button

```python
@property
def due_payment_button(self) -> WebElement
```

Due payment button for accessing payment and print operations section.

**Locator Strategy:** `By.XPATH, "//a[@data-section='print']"`

**Returns:**
- `WebElement`: Link to payment/print section

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
crm_page.button_pipeline.click()  # Open opportunity
crm_page.due_payment_button.click()  # Access payment section
```

**Source:** `pages/crm_page.py:597-608`

---

### print_button

```python
@property
def print_button(self) -> WebElement
```

Print button for generating printable versions of opportunities or invoices.

!!! danger "CRITICAL TECHNICAL DEBT - HIGHEST PRIORITY"
    This element uses an **absolute XPath** which is extremely brittle:
    ```
    /html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button
    ```
    
    **Risk:** This locator will break with ANY DOM structure change and represents the highest priority technical debt in the entire CrmPage implementation.
    
    **Java Source:** Line 94 in CrmP.java
    
    **Impact:** Print functionality tests will immediately fail on any UI update
    
    **Recommendation:** Coordinate with development team immediately to add a stable identifier (`data-testid`, unique ID, or semantic class name).

**Locator Strategy:** `By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button"`

**Returns:**
- `WebElement`: Print button (fragile locator)

**Wait Strategy:** `wait_for_clickable()`

**Example:**
```python
crm_page.due_payment_button.click()
crm_page.print_button.click()  # Generate print view
```

**Source:** `pages/crm_page.py:610-629`

---

## Helper Methods

### drag_opportunity_to_stage

```python
def drag_opportunity_to_stage(
    source_stage_data_id: str,
    target_stage_data_id: str
) -> None
```

Drag an opportunity card from one pipeline stage to another using ActionChains.

This method encapsulates the drag-and-drop workflow for moving opportunities between pipeline stages. It dynamically constructs locators based on `data-id` attributes and uses the inherited `drag_and_drop` method from BasePage with ActionChains.

**Parameters:**
- `source_stage_data_id` (str): The data-id attribute value of the source stage  
  Example: '1' for first stage
- `target_stage_data_id` (str): The data-id attribute value of the target stage  
  Example: '2' for second stage

**Returns:**
- None

**Raises:**
- `TimeoutException`: If source or target stage is not visible within the configured timeout
- `Exception`: If the drag-and-drop operation fails (e.g., element not draggable, JavaScript errors)

**Examples:**

```python
# Move opportunity from stage 1 to stage 2
crm_page.drag_opportunity_to_stage('1', '2')

# Move opportunity from stage 2 to stage 3
crm_page.drag_opportunity_to_stage('2', '3')

# Complete workflow with verification
crm_page.create_button.click()
crm_page.opportunity_title.send_keys("Test Opportunity")
crm_page.create_pipeline.click()

# Drag to next stage
crm_page.drag_opportunity_to_stage('1', '2')

# Verify move was successful
verify_text = crm_page.test_verify.text
assert "Test Opportunity" in verify_text
```

**Alternative Usage:**

If using the pre-defined properties (`progress_pipeline`, `progress_pipeline2`), use the inherited `drag_and_drop` method directly:

```python
crm_page.drag_and_drop(
    crm_page._PROGRESS_PIPELINE,
    crm_page._PROGRESS_PIPELINE2
)
```

**Source:** `pages/crm_page.py:635-682`

---

## Complete Usage Examples

### Creating a New Opportunity

```python
from selenium import webdriver
from pages.crm_page import CrmPage
from utilities.driver_manager import DriverManager

# Initialize driver and page object
driver = DriverManager.get_driver()
crm_page = CrmPage(driver)

# Navigate to CRM module
crm_page.crm_link.click()

# Create new opportunity
crm_page.create_button.click()
crm_page.opportunity_title.send_keys("Q4 Enterprise Deal")
crm_page.customer.send_keys("Acme Corporation")
crm_page.expected_revenue.send_keys("50000")
crm_page.priority.click()  # Select priority
crm_page.create_pipeline.click()

# Verify opportunity created
assert crm_page.find_title_test.text == "Q4 Enterprise Deal"
assert "$50,000" in crm_page.total_price.text
```

### Moving Opportunity Through Pipeline Stages

```python
from pages.crm_page import CrmPage

crm_page = CrmPage(driver)
crm_page.crm_link.click()

# Drag opportunity from stage 1 to stage 2
crm_page.drag_and_drop(
    crm_page._PROGRESS_PIPELINE,
    crm_page._PROGRESS_PIPELINE2
)

# Verify opportunity moved to second stage
verify_text = crm_page.test_verify.text
assert "Expected Title" in verify_text

# Alternative: Use helper method for dynamic stage IDs
crm_page.drag_opportunity_to_stage('2', '3')  # Move to stage 3
```

### Editing an Existing Opportunity

```python
from pages.crm_page import CrmPage

crm_page = CrmPage(driver)
crm_page.crm_link.click()

# Open opportunity
crm_page.button_pipeline.click()

# Enter edit mode
crm_page.edit_button.click()

# Update fields
crm_page.opportunity_title_edit.clear()
crm_page.opportunity_title_edit.send_keys("Updated Enterprise Deal")
crm_page.expected_revenue_edit.clear()
crm_page.expected_revenue_edit.send_keys("75000")
crm_page.probability_edit.clear()
crm_page.probability_edit.send_keys("85")

# Save changes
crm_page.save_edit.click()
```

### Creating and Searching for Customers

```python
from selenium.webdriver.common.keys import Keys
from pages.crm_page import CrmPage

crm_page = CrmPage(driver)

# Navigate to customer management
crm_page.customer_side_button.click()

# Create new customer
crm_page.create_customer.click()
crm_page.input_name.send_keys("Acme Corporation")
crm_page.create_customer_button.click()

# Search for customer
crm_page.searching_text.send_keys("Acme")
crm_page.searching_text.send_keys(Keys.ENTER)

# Verify customer appears in results
customer_name = crm_page.name_customer.text
assert "Acme" in customer_name
```

### Print Operations

```python
from pages.crm_page import CrmPage

crm_page = CrmPage(driver)
crm_page.crm_link.click()

# Open opportunity
crm_page.button_pipeline.click()

# Access print section
crm_page.due_payment_button.click()

# Generate print view (note: brittle locator)
crm_page.print_button.click()
```

---

## Thread Safety Notes

The `CrmPage` class is thread-safe when used with thread-local WebDriver instances provided by `DriverManager`:

- Each property method calls BasePage wait utilities, which use the `self.driver` instance
- `DriverManager` uses `threading.local()` to ensure each thread gets its own WebDriver
- Property methods return fresh WebElement references on each access, preventing stale element issues
- No shared state between page object instances beyond the thread-local driver

**Thread-Safe Usage Pattern:**

```python
import concurrent.futures
from utilities.driver_manager import DriverManager
from pages.crm_page import CrmPage

def test_crm_workflow(opportunity_name):
    # Each thread gets its own driver instance
    driver = DriverManager.get_driver()
    crm_page = CrmPage(driver)
    
    crm_page.crm_link.click()
    crm_page.create_button.click()
    crm_page.opportunity_title.send_keys(opportunity_name)
    crm_page.create_pipeline.click()
    
    DriverManager.quit_driver()

# Run tests in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    opportunities = ["Deal 1", "Deal 2", "Deal 3"]
    executor.map(test_crm_workflow, opportunities)
```

---

## Design Patterns

### Property-Based Locator Pattern

`CrmPage` implements the property-based locator pattern, which provides several advantages over Java's PageFactory:

```python
# Private locator constant (tuple)
_OPPORTUNITY_TITLE: Tuple[str, str] = (By.NAME, "name")

# Property method returns fresh WebElement
@property
def opportunity_title(self) -> WebElement:
    return self.wait_for_element(self._OPPORTUNITY_TITLE)
```

**Benefits:**
1. **Fresh Element References:** Each property access returns a new WebElement, preventing stale element exceptions
2. **Explicit Waits Built-In:** All properties use BasePage wait utilities for synchronization
3. **Better Encapsulation:** Private locators prevent external code from bypassing wait logic
4. **Type Safety:** Type hints provide IDE autocomplete and static analysis support
5. **Testability:** Locator constants can be accessed directly for dynamic locator construction

### Migration from Java PageFactory

```java
// Java (CrmP.java) - Public WebElement fields
@FindBy(name = "name")
public WebElement opportunityTitle;

// Python (crm_page.py) - Property-based locators
_OPPORTUNITY_TITLE = (By.NAME, "name")

@property
def opportunity_title(self) -> WebElement:
    return self.wait_for_element(self._OPPORTUNITY_TITLE)
```

**Key Differences:**
- Java: Public fields initialized once by PageFactory
- Python: Properties return fresh elements on each access
- Java: No built-in wait strategy
- Python: Explicit waits integrated into every property
- Java: Can become stale in dynamic UIs
- Python: Always fetches current element state

---

## Related Documentation

- [BasePage API Reference](base-page.md) - Base class providing wait utilities and ActionChains
- [CRM Testing Guide](../../guides/crm-testing.md) - Complete guide to testing CRM workflows
- [Page Object Model Guide](../../guides/page-object-model.md) - Creating new page objects
- [Wait Strategies Architecture](../../architecture/wait-strategies.md) - Explicit wait patterns
- [Parallel Execution Guide](../../guides/parallel-execution.md) - Thread-safe test execution

---

## See Also

- **Source Code:** `pages/crm_page.py`
- **Java Source:** `CrmP.java` (original PageFactory implementation)
- **Step Definitions:** `features/steps/crm_steps.py`
- **Feature File:** `features/Crm.feature`
- **Related Pages:** [LoginPage](login-page.md), [ContactsPage](contacts-page.md), [SalesPage](sales-page.md)
