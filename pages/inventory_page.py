"""
Inventory Page Module

Page Object for Testinium inventory and product management functionality.
This module provides element locators and interaction methods for the Inventory module,
including navigation, product creation, and product list verification.

Migration Context:
    Converted from: src/main/java/com/testinium/pages/InventoryP.java
    Original Pattern: Java PageFactory with @FindBy annotations and public WebElement fields
    Target Pattern: Python properties with tuple-based locators and explicit waits

Key Features:
- Inventory module navigation via partial link text
- Products submenu access
- Product creation workflow (create button, save button)
- Field error notification handling
- Product name input with generated ID (technical debt - see note below)
- Product list verification elements

Technical Debt Warning:
    The product_name property uses a GENERATED DOM ID 'o_field_input_479' from the
    original Java implementation. This locator is BRITTLE and may break if the
    application DOM structure changes or if the page is regenerated.

    **RECOMMENDATION**: Request development team to add stable data-test-id attributes
    such as data-testid="product-name-input" to enable more maintainable locators.
    Until then, this generated ID is preserved for behavioral equivalence with the
    Java test framework.

Example Usage:
    >>> from selenium import webdriver
    >>> from pages.inventory_page import InventoryPage
    >>>
    >>> driver = webdriver.Chrome()
    >>> inventory_page = InventoryPage(driver)
    >>>
    >>> # Navigate to inventory module
    >>> inventory_page.inventory_module.click()
    >>>
    >>> # Access products submenu
    >>> inventory_page.products.click()
    >>>
    >>> # Create new product
    >>> inventory_page.create_button.click()
    >>> inventory_page.product_name.send_keys("Test Product")
    >>> inventory_page.save_btn.click()
    >>>
    >>> # Verify no field errors
    >>> assert not inventory_page.field_error.is_displayed()
"""

from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """
    Page Object for Testinium Inventory and Product Management.

    This class provides element locators and methods for interacting with the
    inventory management module, including product creation and verification.
    Inherits common WebDriver utilities from BasePage for explicit waits and
    element interaction patterns.

    Locator Strategy:
        - Partial link text for module navigation (inventory_module, products)
        - Class names for buttons and notifications (create_button, field_error)
        - XPath for specific button attributes and product verification
        - ID for product name input (⚠️ GENERATED ID - see class docstring)

    Properties:
        inventory_module: Inventory module navigation link
        products: Products submenu link
        create_button: Button to create new product (Kanban view)
        save_btn: Save button for product form submission
        field_error: Notification manager for field validation errors
        product_name: Product name input field (⚠️ uses generated ID)
        products_list: Product list verification element (specific product "EY")
        created_product: Created product verification element

    Thread Safety:
        This class is thread-safe when used with thread-local WebDriver instances
        from DriverManager, as each InventoryPage instance is bound to a specific
        driver instance passed during initialization.

    Example:
        >>> # Initialize page object
        >>> inventory_page = InventoryPage(driver)
        >>>
        >>> # Navigate to inventory
        >>> inventory_page.inventory_module.click()
        >>> inventory_page.products.click()
        >>>
        >>> # Create product workflow
        >>> inventory_page.create_button.click()
        >>> inventory_page.product_name.send_keys("New Product")
        >>> inventory_page.save_btn.click()
        >>>
        >>> # Verify product created
        >>> product_element = inventory_page.created_product
        >>> assert "New Product" in product_element.text
    """

    # Private Locator Constants
    # Define all locators as private class-level tuples (By strategy, locator value)
    # This separates locator definitions from element access logic

    _INVENTORY_MODULE: Tuple[str, str] = (By.PARTIAL_LINK_TEXT, "Inventory")
    """Locator for Inventory module navigation link using partial link text"""

    _PRODUCTS: Tuple[str, str] = (By.PARTIAL_LINK_TEXT, "Products")
    """Locator for Products submenu link using partial link text"""

    _CREATE_BUTTON: Tuple[str, str] = (By.CLASS_NAME, "o-kanban-button-new")
    """Locator for 'Create' button in Kanban view using class name"""

    _SAVE_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//button[@class='btn btn-primary btn-sm o_form_button_save']"
    )
    """Locator for Save button using XPath with exact class attribute match"""

    _FIELD_ERROR: Tuple[str, str] = (By.CLASS_NAME, "o_notification_manager")
    """Locator for field validation error notification manager using class name"""

    _PRODUCT_NAME: Tuple[str, str] = (By.ID, "o_field_input_479")
    """
    Locator for Product Name input field using ID.

    ⚠️ TECHNICAL DEBT WARNING ⚠️
    This locator uses a GENERATED DOM ID 'o_field_input_479' which is BRITTLE.
    The ID may change if:
    - Application DOM structure is regenerated
    - Page rendering order changes
    - Framework version updates

    RECOMMENDED FIX:
    Request development team to add stable data-testid attribute:
    <input data-testid="product-name-input" id="o_field_input_479" ...>

    Then update locator to:
    _PRODUCT_NAME = (By.CSS_SELECTOR, "[data-testid='product-name-input']")

    This generated ID is preserved here for behavioral equivalence with the
    Java test framework (InventoryP.java line 29), but should be refactored
    as soon as stable locators are available.
    """

    _PRODUCTS_LIST: Tuple[str, str] = (By.XPATH, "//span[.='EY']")
    """
    Locator for specific product 'EY' in product list using XPath text match.
    This appears to be a test-specific product name for verification purposes.
    """

    _CREATED_PRODUCT: Tuple[str, str] = (
        By.XPATH,
        "//span[@class='o_field_char o_field_widget o_required_modifier']"
    )
    """
    Locator for created product verification element.
    Targets span with specific Odoo field classes indicating required character field.
    """

    # Property-Based Element Accessors
    # Each property returns a fresh WebElement reference with explicit waits
    # This prevents stale element exceptions and ensures elements are ready for interaction

    @property
    def inventory_module(self) -> WebElement:
        """
        Get the Inventory module navigation link element.

        This property returns the main Inventory module link used for navigating
        to the inventory management section of the application.

        Returns:
            WebElement: Inventory module link element with explicit wait for presence

        Raises:
            TimeoutException: If element not found within default timeout period

        Example:
            >>> inventory_page = InventoryPage(driver)
            >>> inventory_page.inventory_module.click()
        """
        return self.wait_for_element(self._INVENTORY_MODULE)

    @property
    def products(self) -> WebElement:
        """
        Get the Products submenu link element.

        This property returns the Products submenu link within the Inventory module,
        used for accessing the products management section.

        Returns:
            WebElement: Products submenu link with explicit wait for presence

        Raises:
            TimeoutException: If element not found within default timeout period

        Example:
            >>> inventory_page = InventoryPage(driver)
            >>> inventory_page.inventory_module.click()
            >>> inventory_page.products.click()
        """
        return self.wait_for_element(self._PRODUCTS)

    @property
    def create_button(self) -> WebElement:
        """
        Get the Create button element for creating new products.

        This property returns the 'Create' button typically displayed in Kanban view
        of the products list. The button is used to initiate product creation workflow.

        Returns:
            WebElement: Create button with explicit wait for clickability

        Raises:
            TimeoutException: If button not clickable within default timeout period

        Example:
            >>> inventory_page = InventoryPage(driver)
            >>> # Navigate to products first
            >>> inventory_page.inventory_module.click()
            >>> inventory_page.products.click()
            >>> # Click create button
            >>> inventory_page.create_button.click()
        """
        return self.wait_for_clickable(self._CREATE_BUTTON)

    @property
    def save_btn(self) -> WebElement:
        """
        Get the Save button element for product form submission.

        This property returns the Save button used to submit the product creation
        or edit form. The button waits for clickability to ensure the form is
        ready for submission.

        Returns:
            WebElement: Save button with explicit wait for clickability

        Raises:
            TimeoutException: If button not clickable within default timeout period

        Example:
            >>> inventory_page = InventoryPage(driver)
            >>> # After filling product form
            >>> inventory_page.product_name.send_keys("New Product")
            >>> inventory_page.save_btn.click()
        """
        return self.wait_for_clickable(self._SAVE_BUTTON)

    @property
    def field_error(self) -> WebElement:
        """
        Get the field error notification manager element.

        This property returns the notification manager element that displays
        field validation errors. Used for verifying error states or confirming
        absence of errors after form submission.

        Returns:
            WebElement: Notification manager element with explicit wait for presence

        Raises:
            TimeoutException: If element not found within default timeout period

        Note:
            Element presence doesn't mean error is displayed. Check visibility
            or text content to determine actual error state:
            >>> if inventory_page.field_error.is_displayed():
            ...     print(f"Error: {inventory_page.field_error.text}")

        Example:
            >>> inventory_page = InventoryPage(driver)
            >>> # After form submission
            >>> try:
            ...     error = inventory_page.field_error
            ...     if error.is_displayed():
            ...         print(f"Validation error: {error.text}")
            ... except TimeoutException:
            ...     print("No error notification found")
        """
        return self.wait_for_element(self._FIELD_ERROR)

    @property
    def product_name(self) -> WebElement:
        """
        Get the Product Name input field element.

        This property returns the product name input field used for entering
        product names during creation or editing.

        ⚠️ TECHNICAL DEBT WARNING ⚠️
        This property uses a GENERATED DOM ID 'o_field_input_479' which may break
        if the application DOM changes. See class docstring for recommended fix.

        Returns:
            WebElement: Product name input field with explicit wait for presence

        Raises:
            TimeoutException: If input field not found within default timeout period

        Example:
            >>> inventory_page = InventoryPage(driver)
            >>> # Enter product name
            >>> inventory_page.product_name.clear()
            >>> inventory_page.product_name.send_keys("Test Product XYZ")
        """
        return self.wait_for_element(self._PRODUCT_NAME)

    @property
    def products_list(self) -> WebElement:
        """
        Get the specific product list element for verification.

        This property returns a specific product element (containing text 'EY')
        used for product list verification in test scenarios. This appears to be
        a test-specific product name.

        Returns:
            WebElement: Product list element with explicit wait for presence

        Raises:
            TimeoutException: If product 'EY' not found within default timeout period

        Note:
            This locator targets a specific test product name 'EY'. If testing
            with different products, additional locator methods may be needed.

        Example:
            >>> inventory_page = InventoryPage(driver)
            >>> # Verify product 'EY' exists in list
            >>> product = inventory_page.products_list
            >>> assert product.is_displayed()
            >>> assert "EY" in product.text
        """
        return self.wait_for_element(self._PRODUCTS_LIST)

    @property
    def created_product(self) -> WebElement:
        """
        Get the created product verification element.

        This property returns the element representing a newly created or displayed
        product. The element is identified by Odoo-specific CSS classes indicating
        a required character field widget.

        Returns:
            WebElement: Created product element with explicit wait for presence

        Raises:
            TimeoutException: If element not found within default timeout period

        Example:
            >>> inventory_page = InventoryPage(driver)
            >>> # After creating product, verify it appears
            >>> created = inventory_page.created_product
            >>> assert created.is_displayed()
            >>> print(f"Created product: {created.text}")
        """
        return self.wait_for_element(self._CREATED_PRODUCT)


# Module self-test and documentation
if __name__ == "__main__":
    """
    Module self-test demonstrating InventoryPage usage.

    This section provides usage examples and serves as executable documentation.
    It does not run actual tests but shows the expected usage patterns.
    """
    print("InventoryPage module loaded successfully")
    print("\nThis page object provides inventory and product management elements")
    print("\n⚠️  TECHNICAL DEBT NOTICE:")
    print("    product_name property uses generated ID 'o_field_input_479'")
    print("    Recommend requesting stable data-testid attributes from dev team")
    print("\nExample usage in step definitions:")
    print("""
    from behave import given, when, then
    from pages.inventory_page import InventoryPage

    @when('User navigates to Inventory module')
    def navigate_to_inventory(context):
        inventory_page = InventoryPage(context.driver)
        inventory_page.inventory_module.click()
        inventory_page.products.click()

    @when('User creates a new product named "{product_name}"')
    def create_product(context, product_name):
        inventory_page = InventoryPage(context.driver)
        inventory_page.create_button.click()
        inventory_page.product_name.send_keys(product_name)
        inventory_page.save_btn.click()

    @then('Product should be created successfully')
    def verify_product_created(context):
        inventory_page = InventoryPage(context.driver)
        product = inventory_page.created_product
        assert product.is_displayed(), "Created product not visible"
    """)
    print("\nLocators defined in this page object:")
    print("  - _INVENTORY_MODULE: Partial link text 'Inventory'")
    print("  - _PRODUCTS: Partial link text 'Products'")
    print("  - _CREATE_BUTTON: Class name 'o-kanban-button-new'")
    print("  - _SAVE_BUTTON: XPath for save button with specific classes")
    print("  - _FIELD_ERROR: Class name 'o_notification_manager'")
    print("  - _PRODUCT_NAME: ID 'o_field_input_479' (⚠️ GENERATED ID)")
    print("  - _PRODUCTS_LIST: XPath for product 'EY'")
    print("  - _CREATED_PRODUCT: XPath for required field widget")
