# InventoryPage API Reference

## Overview

The `InventoryPage` class provides a page object implementation for Testinium's inventory and product management functionality. It offers element locators and interaction methods for navigating the Inventory module, creating products, and verifying product data.

This page object inherits from [`BasePage`](base-page.md) and follows the property-based locator pattern to ensure fresh element references with explicit waits, preventing stale element exceptions.

**Module:** `pages.inventory_page`

**Inherits From:** [`BasePage`](base-page.md)

**Thread Safety:** Thread-safe when used with thread-local WebDriver instances from `DriverManager`

**Source:** `pages/inventory_page.py`

---

## Migration Context

**Converted From:** `src/main/java/com/testinium/pages/InventoryP.java`

**Original Pattern:** Java PageFactory with `@FindBy` annotations and public `WebElement` fields

**Target Pattern:** Python properties with tuple-based locators and explicit waits

This page object was migrated from the Java/Cucumber test framework to Python/Behave, replacing PageFactory's annotation-based element location with property-based access that calls explicit wait methods.

---

## Class Definition

```python
class InventoryPage(BasePage):
    """Page Object for Testinium Inventory and Product Management."""
```

The `InventoryPage` class encapsulates all element locators and interaction patterns for the inventory management module, providing a clean API for test step definitions.

---

## Key Features

- **Inventory Module Navigation** - Access to main inventory module and products submenu
- **Product Creation Workflow** - Complete product creation flow from create button to save
- **Field Validation** - Error notification handling for form validation
- **Product Verification** - Elements for verifying created products and product lists
- **Property-Based Locators** - All elements accessed via properties with explicit waits
- **Technical Debt Documentation** - Explicit warnings for brittle generated ID locators

---

## ⚠️ Technical Debt Warning

The `product_name` property uses a **GENERATED DOM ID** `'o_field_input_479'` from the original Java implementation. This locator is **BRITTLE** and may break if:

- Application DOM structure changes
- Page rendering order changes
- Framework version updates

### Recommended Fix

Request the development team to add stable `data-testid` attributes:

```html
<input data-testid="product-name-input" id="o_field_input_479" ...>
```

Then update the locator to:

```python
_PRODUCT_NAME = (By.CSS_SELECTOR, "[data-testid='product-name-input']")
```

Until stable locators are available, the generated ID is preserved for behavioral equivalence with the Java test framework.

---

## Locator Strategy

The `InventoryPage` uses multiple locator strategies optimized for different element types:

| Locator Type | Used For | Examples |
|--------------|----------|----------|
| **Partial Link Text** | Module navigation | `inventory_module`, `products` |
| **Class Name** | Buttons, notifications | `create_button`, `field_error` |
| **XPath** | Specific attributes, text matching | `save_btn`, `products_list`, `created_product` |
| **ID** | Direct element access (⚠️ brittle) | `product_name` |

---

## Properties

All properties return `WebElement` instances with explicit waits ensuring elements are ready for interaction. Each property call returns a fresh element reference to prevent stale element exceptions.

### inventory_module

```python
@property
def inventory_module(self) -> WebElement
```

Get the Inventory module navigation link element.

**Returns:**
- `WebElement` - Inventory module link element with explicit wait for presence

**Raises:**
- `TimeoutException` - If element not found within default timeout period

**Locator:** Partial link text "Inventory"

**Example:**

```python
from pages.inventory_page import InventoryPage

inventory_page = InventoryPage(driver)
inventory_page.inventory_module.click()
```

**Source:** `pages/inventory_page.py:172-189`

---

### products

```python
@property
def products(self) -> WebElement
```

Get the Products submenu link element.

This property returns the Products submenu link within the Inventory module, used for accessing the products management section.

**Returns:**
- `WebElement` - Products submenu link with explicit wait for presence

**Raises:**
- `TimeoutException` - If element not found within default timeout period

**Locator:** Partial link text "Products"

**Example:**

```python
inventory_page = InventoryPage(driver)
inventory_page.inventory_module.click()
inventory_page.products.click()
```

**Source:** `pages/inventory_page.py:192-210`

---

### create_button

```python
@property
def create_button(self) -> WebElement
```

Get the Create button element for creating new products.

This property returns the 'Create' button typically displayed in Kanban view of the products list. The button is used to initiate the product creation workflow.

**Returns:**
- `WebElement` - Create button with explicit wait for clickability

**Raises:**
- `TimeoutException` - If button not clickable within default timeout period

**Locator:** Class name "o-kanban-button-new"

**Example:**

```python
inventory_page = InventoryPage(driver)
# Navigate to products first
inventory_page.inventory_module.click()
inventory_page.products.click()
# Click create button
inventory_page.create_button.click()
```

**Source:** `pages/inventory_page.py:213-234`

---

### save_btn

```python
@property
def save_btn(self) -> WebElement
```

Get the Save button element for product form submission.

This property returns the Save button used to submit the product creation or edit form. The button waits for clickability to ensure the form is ready for submission.

**Returns:**
- `WebElement` - Save button with explicit wait for clickability

**Raises:**
- `TimeoutException` - If button not clickable within default timeout period

**Locator:** XPath `//button[@class='btn btn-primary btn-sm o_form_button_save']`

**Example:**

```python
inventory_page = InventoryPage(driver)
# After filling product form
inventory_page.product_name.send_keys("New Product")
inventory_page.save_btn.click()
```

**Source:** `pages/inventory_page.py:237-257`

---

### field_error

```python
@property
def field_error(self) -> WebElement
```

Get the field error notification manager element.

This property returns the notification manager element that displays field validation errors. Used for verifying error states or confirming absence of errors after form submission.

**Returns:**
- `WebElement` - Notification manager element with explicit wait for presence

**Raises:**
- `TimeoutException` - If element not found within default timeout period

**Locator:** Class name "o_notification_manager"

**Note:** Element presence doesn't mean error is displayed. Check visibility or text content to determine actual error state.

**Example:**

```python
inventory_page = InventoryPage(driver)
# After form submission
try:
    error = inventory_page.field_error
    if error.is_displayed():
        print(f"Validation error: {error.text}")
except TimeoutException:
    print("No error notification found")
```

**Source:** `pages/inventory_page.py:260-290`

---

### product_name

```python
@property
def product_name(self) -> WebElement
```

Get the Product Name input field element.

This property returns the product name input field used for entering product names during creation or editing.

**⚠️ TECHNICAL DEBT WARNING:** This property uses a GENERATED DOM ID `'o_field_input_479'` which may break if the application DOM changes. See class-level technical debt warning for recommended fix.

**Returns:**
- `WebElement` - Product name input field with explicit wait for presence

**Raises:**
- `TimeoutException` - If input field not found within default timeout period

**Locator:** ID "o_field_input_479" (⚠️ brittle - see warning above)

**Example:**

```python
inventory_page = InventoryPage(driver)
# Enter product name
inventory_page.product_name.clear()
inventory_page.product_name.send_keys("Test Product XYZ")
```

**Source:** `pages/inventory_page.py:293-316`

---

### products_list

```python
@property
def products_list(self) -> WebElement
```

Get the specific product list element for verification.

This property returns a specific product element (containing text 'EY') used for product list verification in test scenarios. This appears to be a test-specific product name.

**Returns:**
- `WebElement` - Product list element with explicit wait for presence

**Raises:**
- `TimeoutException` - If product 'EY' not found within default timeout period

**Locator:** XPath `//span[.='EY']`

**Note:** This locator targets a specific test product name 'EY'. If testing with different products, additional locator methods may be needed.

**Example:**

```python
inventory_page = InventoryPage(driver)
# Verify product 'EY' exists in list
product = inventory_page.products_list
assert product.is_displayed()
assert "EY" in product.text
```

**Source:** `pages/inventory_page.py:319-344`

---

### created_product

```python
@property
def created_product(self) -> WebElement
```

Get the created product verification element.

This property returns the element representing a newly created or displayed product. The element is identified by Odoo-specific CSS classes indicating a required character field widget.

**Returns:**
- `WebElement` - Created product element with explicit wait for presence

**Raises:**
- `TimeoutException` - If element not found within default timeout period

**Locator:** XPath `//span[@class='o_field_char o_field_widget o_required_modifier']`

**Example:**

```python
inventory_page = InventoryPage(driver)
# After creating product, verify it appears
created = inventory_page.created_product
assert created.is_displayed()
print(f"Created product: {created.text}")
```

**Source:** `pages/inventory_page.py:347-368`

---

## Complete Usage Example

### Product Creation Workflow

```python
from selenium import webdriver
from pages.inventory_page import InventoryPage

# Initialize driver and page object
driver = webdriver.Chrome()
driver.get("https://testinium-app-url.com")
inventory_page = InventoryPage(driver)

# Navigate to Inventory module
inventory_page.inventory_module.click()

# Access Products submenu
inventory_page.products.click()

# Create new product
inventory_page.create_button.click()
inventory_page.product_name.send_keys("Test Product")
inventory_page.save_btn.click()

# Verify no field errors
try:
    error = inventory_page.field_error
    if error.is_displayed():
        print(f"Error occurred: {error.text}")
    else:
        print("Product created successfully")
except:
    print("No errors - product created successfully")

# Verify product appears
created = inventory_page.created_product
assert created.is_displayed(), "Product not visible after creation"
print(f"Verified product: {created.text}")

driver.quit()
```

**Source:** `pages/inventory_page.py:31-50`

---

## Behave Step Definition Integration

### Example Step Definitions

```python
from behave import given, when, then
from pages.inventory_page import InventoryPage

@when('User navigates to Inventory module')
def navigate_to_inventory(context):
    """Navigate to the Inventory module and products section."""
    inventory_page = InventoryPage(context.driver)
    inventory_page.inventory_module.click()
    inventory_page.products.click()

@when('User creates a new product named "{product_name}"')
def create_product(context, product_name):
    """Create a new product with the specified name."""
    inventory_page = InventoryPage(context.driver)
    inventory_page.create_button.click()
    inventory_page.product_name.send_keys(product_name)
    inventory_page.save_btn.click()

@then('Product should be created successfully')
def verify_product_created(context):
    """Verify that the product was created without errors."""
    inventory_page = InventoryPage(context.driver)
    # Verify no error notification
    try:
        error = inventory_page.field_error
        assert not error.is_displayed(), f"Error displayed: {error.text}"
    except:
        pass  # No error is expected
    # Verify product appears
    product = inventory_page.created_product
    assert product.is_displayed(), "Created product not visible"

@then('User should see product "{product_name}" in the list')
def verify_product_in_list(context, product_name):
    """Verify product appears in products list."""
    inventory_page = InventoryPage(context.driver)
    # Note: products_list currently targets specific product "EY"
    # For dynamic product names, additional locator methods needed
    products = inventory_page.products_list
    assert products.is_displayed(), f"Product {product_name} not found in list"
```

**Source:** `pages/inventory_page.py:382-404`

---

## Private Locator Constants

The `InventoryPage` defines all locators as private class-level constants. This separates locator definitions from element access logic and makes locator maintenance easier.

| Constant | Locator Strategy | Value | Description |
|----------|------------------|-------|-------------|
| `_INVENTORY_MODULE` | `By.PARTIAL_LINK_TEXT` | "Inventory" | Inventory module navigation link |
| `_PRODUCTS` | `By.PARTIAL_LINK_TEXT` | "Products" | Products submenu link |
| `_CREATE_BUTTON` | `By.CLASS_NAME` | "o-kanban-button-new" | Create button in Kanban view |
| `_SAVE_BUTTON` | `By.XPATH` | `//button[@class='btn btn-primary btn-sm o_form_button_save']` | Save button for form submission |
| `_FIELD_ERROR` | `By.CLASS_NAME` | "o_notification_manager" | Field validation error notification |
| `_PRODUCT_NAME` | `By.ID` | "o_field_input_479" | ⚠️ Product name input (generated ID) |
| `_PRODUCTS_LIST` | `By.XPATH` | `//span[.='EY']` | Specific test product verification |
| `_CREATED_PRODUCT` | `By.XPATH` | `//span[@class='o_field_char o_field_widget o_required_modifier']` | Created product verification |

**Source:** `pages/inventory_page.py:107-165`

---

## Inheritance

`InventoryPage` inherits all methods from [`BasePage`](base-page.md), providing access to:

### Wait Methods
- `wait_for_element(locator, timeout=None)` - Wait for element presence
- `wait_for_clickable(locator, timeout=None)` - Wait for element to be clickable
- `wait_for_visibility(locator, timeout=None)` - Wait for element visibility
- `wait_for_text(locator, text, timeout=None)` - Wait for specific text in element

### Interaction Methods
- `click_element(locator, timeout=None)` - Click element with wait
- `enter_text(locator, text, timeout=None)` - Enter text with wait
- `get_element_text(locator, timeout=None)` - Get element text with wait
- `is_element_displayed(locator, timeout=None)` - Check element visibility

### Advanced Interaction
- `drag_and_drop(source_locator, target_locator)` - Perform drag-and-drop operation

See the [`BasePage` API documentation](base-page.md) for complete method details.

---

## Thread Safety

The `InventoryPage` class is thread-safe when used with thread-local WebDriver instances from `DriverManager`. Each `InventoryPage` instance is bound to a specific WebDriver instance passed during initialization, ensuring isolation in parallel test execution.

**Thread-Safe Usage Pattern:**

```python
from behave import given
from utilities.driver_manager import DriverManager
from pages.inventory_page import InventoryPage

@given('User is on the inventory page')
def step_impl(context):
    # Each thread gets its own WebDriver via threading.local()
    driver = DriverManager.get_driver()
    # Each thread gets its own InventoryPage instance
    inventory_page = InventoryPage(driver)
    # Safe for parallel execution
    inventory_page.inventory_module.click()
```

---

## Best Practices

### 1. Always Navigate Before Interacting

```python
# ✅ Correct - Navigate to module first
inventory_page.inventory_module.click()
inventory_page.products.click()
inventory_page.create_button.click()

# ❌ Incorrect - Direct interaction without navigation may fail
inventory_page.create_button.click()  # Element may not be accessible
```

### 2. Check Error Notifications After Form Submission

```python
# ✅ Correct - Verify no errors after save
inventory_page.save_btn.click()
try:
    error = inventory_page.field_error
    if error.is_displayed():
        raise AssertionError(f"Form error: {error.text}")
except TimeoutException:
    pass  # No error notification is good

# ❌ Incorrect - Assume success without verification
inventory_page.save_btn.click()
# Missing error check - might proceed with invalid data
```

### 3. Clear Input Fields Before Entering Text

```python
# ✅ Correct - Clear before entering new text
inventory_page.product_name.clear()
inventory_page.product_name.send_keys("New Product")

# ❌ Incorrect - Append to existing text
inventory_page.product_name.send_keys("New Product")  # May concatenate
```

### 4. Verify Created Products

```python
# ✅ Correct - Explicit verification
inventory_page.save_btn.click()
created = inventory_page.created_product
assert created.is_displayed(), "Product not created"

# ❌ Incorrect - No verification of creation
inventory_page.save_btn.click()
# Missing verification - test may pass even if creation failed
```

---

## Known Limitations

### 1. Generated ID Locator (product_name)

**Issue:** The `product_name` property uses generated ID `'o_field_input_479'` which is brittle.

**Impact:** Tests may break if application DOM structure changes.

**Workaround:** Monitor for `NoSuchElementException` or `TimeoutException` on `product_name` access and update locator if needed.

**Permanent Fix:** Request stable `data-testid` attributes from development team (see Technical Debt Warning above).

### 2. Specific Product Name Hardcoded (products_list)

**Issue:** The `products_list` property targets specific product "EY" with hardcoded XPath.

**Impact:** Cannot verify different product names without modifying page object.

**Workaround:** Add parameterized method for flexible product verification:

```python
def verify_product_by_name(self, product_name: str) -> WebElement:
    """Verify product exists by name (custom method - not in current implementation)."""
    locator = (By.XPATH, f"//span[.='{product_name}']")
    return self.wait_for_element(locator)
```

### 3. Single Created Product Element

**Issue:** The `created_product` property returns only one element matching the XPath.

**Impact:** Cannot distinguish between multiple created products in the same session.

**Workaround:** Use `driver.find_elements()` directly for multiple products:

```python
from selenium.webdriver.common.by import By

# Get all created products
created_products = driver.find_elements(
    By.XPATH, 
    "//span[@class='o_field_char o_field_widget o_required_modifier']"
)
print(f"Found {len(created_products)} products")
```

---

## Troubleshooting

### TimeoutException on product_name

**Error:**
```
selenium.common.exceptions.TimeoutException: Message: 
Element with ID 'o_field_input_479' not found
```

**Cause:** Generated ID changed due to DOM structure update.

**Solution:**
1. Inspect the product name input field in the browser
2. Identify the current ID or a more stable locator
3. Update `_PRODUCT_NAME` locator in `pages/inventory_page.py`
4. Consider requesting `data-testid` attribute from development team

### Element Not Clickable: create_button

**Error:**
```
selenium.common.exceptions.ElementClickInterceptedException: 
Element <button class="o-kanban-button-new"> is not clickable
```

**Cause:** Navigation to products page not completed before clicking create button.

**Solution:**
```python
# Ensure navigation completes
inventory_page.inventory_module.click()
time.sleep(1)  # Allow page transition
inventory_page.products.click()
time.sleep(1)  # Allow products page load
inventory_page.create_button.click()
```

Or use explicit wait for product page to load:
```python
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

inventory_page.inventory_module.click()
inventory_page.products.click()
# Wait for product list to be visible
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "o-kanban-button-new"))
)
inventory_page.create_button.click()
```

### field_error Not Displayed

**Issue:** Test expects error but `field_error.is_displayed()` returns `False`.

**Cause:** Element exists in DOM but is hidden until error occurs.

**Solution:** Use try-except pattern to handle optional error display:

```python
try:
    error = inventory_page.field_error
    is_error_visible = error.is_displayed()
    if is_error_visible:
        print(f"Error: {error.text}")
except TimeoutException:
    # Element not found at all - no error
    print("No error notification")
```

---

## See Also

- **[BasePage API](base-page.md)** - Parent class with common WebDriver utilities
- **[Page Object Model Guide](../../guides/page-object-model.md)** - Creating custom page objects
- **[Inventory Testing Guide](../../guides/inventory-testing.md)** - Inventory feature test workflows
- **[Wait Strategies Guide](../../guides/wait-strategies.md)** - Explicit wait patterns and best practices
- **[Configuration Reference](../../reference/configuration-options.md)** - Timeout configuration options

---

## Related Step Definitions

- **`features/steps/inventory_steps.py`** - Step definitions using InventoryPage
- **`features/Inventory.feature`** - Gherkin scenarios for inventory testing

---

**Last Updated:** 2024 (Migration from Java/Cucumber framework)

**Maintainer:** Test Automation Team

**Migration Reference:** `src/main/java/com/testinium/pages/InventoryP.java`
