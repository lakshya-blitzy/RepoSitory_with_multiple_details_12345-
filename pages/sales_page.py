"""
Sales Page Module

Page object for the Sales module providing sales and customer management functionality.
This module handles customer creation, search, and list operations with support for
dynamic state/country selection and validation.

Key Features:
- Sales module navigation (partial link text)
- Customer list and details access
- Customer creation form with name, address, state, country fields
- Dynamic state/country dropdown with 'Create and Edit' functionality
- Search functionality for existing customers
- Customer card collection support (dynamic list elements)
- Warning notification handling
- Save and create button interactions

Migration Context:
    Converted from SalesP.java PageFactory pattern to Python property-based locators.
    Original Java implementation used @FindBy annotations with public WebElement fields
    and PageFactory.initElements() for element initialization. This Python version uses
    property decorators with explicit waits for fresh element references, preventing
    stale element exceptions common in the Java PageFactory pattern.

Technical Debt:
    This page object contains generated element IDs (o_field_input_470, o_field_input_474,
    o_field_input_477, o_field_input_516, o_field_input_517, o_field_input_518) which are
    brittle and subject to change with application updates. Post-migration, recommend
    requesting development team add stable test IDs (data-testid attributes) to these
    form inputs for more maintainable test automation.

Design Pattern:
    Follows Page Object Model with:
    - Private locator constants as class-level tuples
    - Public @property methods returning fresh WebElement references
    - Explicit waits via BasePage.wait_for_element() and wait_for_clickable()
    - get_elements() for dynamic collections (all_customers list)
    - Separation of locator strategy from element access logic

Example Usage:
    >>> from selenium import webdriver
    >>> from pages.sales_page import SalesPage
    >>>
    >>> driver = webdriver.Chrome()
    >>> sales_page = SalesPage(driver)
    >>>
    >>> # Navigate to sales module
    >>> sales_page.sales_partial.click()
    >>> sales_page.customers_button.click()
    >>>
    >>> # Create new customer
    >>> sales_page.create_button.click()
    >>> sales_page.customer_name.send_keys("ACME Corp")
    >>> sales_page.address.send_keys("123 Main St")
    >>> sales_page.create_customer.click()
    >>>
    >>> # Search for customer
    >>> sales_page.search_bar.send_keys("ACME Corp")
    >>>
    >>> # Get all customer cards
    >>> customers = sales_page.all_customers
    >>> print(f"Found {len(customers)} customer cards")
"""

from typing import List, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class SalesPage(BasePage):
    """
    Sales page object for Testinium application sales and customer management.

    This class provides access to all sales module elements including customer
    creation forms, search functionality, customer lists, and state/country
    selection dropdowns. Implements property-based element access with explicit
    waits for reliable element interaction.

    Attributes (inherited from BasePage):
        driver (WebDriver): Selenium WebDriver instance
        wait (WebDriverWait): Pre-configured WebDriverWait instance
        config (ConfigReader): Configuration reader for settings
        default_timeout (int): Default wait timeout in seconds
        actions (ActionChains): ActionChains for complex interactions

    Locators:
        All locators defined as private class constants using tuple format:
        (By.STRATEGY, 'locator_value')

    Properties:
        20 single-element properties returning WebElement with explicit waits
        1 multi-element property (all_customers) returning List[WebElement]

    Thread Safety:
        Each SalesPage instance is tied to a specific WebDriver instance.
        Thread safety achieved via thread-local WebDriver from DriverManager.

    Example:
        >>> sales_page = SalesPage(driver)
        >>> sales_page.sales_partial.click()
        >>> sales_page.customers_button.click()
        >>> sales_page.create_button.click()
        >>> sales_page.customer_name.send_keys("Test Customer")
    """

    # =========================================================================
    # LOCATOR CONSTANTS - Private Class Attributes
    # =========================================================================
    # Locators defined as tuples: (By.STRATEGY, 'locator_value')
    # Converted from Java @FindBy annotations to Python tuple format
    # Preserved all original locator strategies for behavioral equivalence

    # Navigation elements
    _SALES_PARTIAL: Tuple[str, str] = (By.PARTIAL_LINK_TEXT, "Sales")
    _CUSTOMERS_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//a[@href='/web#menu_id=447&action=48']/span"
    )
    _LINK: Tuple[str, str] = (
        By.XPATH,
        "//a[@href='/web#menu_id=447&action=48']"
    )

    # Customer creation and action buttons
    _CREATE_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//button[@class='btn btn-primary btn-sm o-kanban-button-new btn-default']"
    )
    _SAVE_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//button[@class='btn btn-sm btn-primary']/span"
    )
    _CREATE_CUSTOMER: Tuple[str, str] = (
        By.XPATH,
        "//button[@class='btn btn-primary btn-sm o_form_button_save']"
    )

    # Customer form input fields
    # TECHNICAL DEBT: Generated IDs (o_field_input_*) are brittle
    # Recommend requesting stable test IDs from development team
    _CUSTOMER_NAME: Tuple[str, str] = (
        By.XPATH,
        "//input[@id='o_field_input_470']"
    )
    _ADDRESS: Tuple[str, str] = (
        By.XPATH,
        "//input[@id='o_field_input_474']"
    )
    _STATE_OPTIONS: Tuple[str, str] = (
        By.XPATH,
        "//input[@id='o_field_input_477']"
    )
    _STATE_NAME: Tuple[str, str] = (
        By.XPATH,
        "//input[@id='o_field_input_516']"
    )
    _STATE_CODE: Tuple[str, str] = (
        By.XPATH,
        "//input[@id='o_field_input_517']"
    )
    _COUNTRY_STATE_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//input[@id='o_field_input_518']"
    )

    # State and country selection dropdowns
    _CREATE_AND_EDIT_STATE: Tuple[str, str] = (
        By.XPATH,
        "//li[.='Create and Edit...']"
    )
    _COUNTRY_SELECTION: Tuple[str, str] = (
        By.XPATH,
        "//li[@id='ui-id-30']/a"
    )

    # Search and validation elements
    _SEARCH_BAR: Tuple[str, str] = (
        By.XPATH,
        "//div[@class='o_searchview']/input"
    )
    _NAME_CHECK: Tuple[str, str] = (
        By.XPATH,
        "//strong[@class='o_kanban_record_title oe_partner_heading']/span"
    )

    # Warning and notification elements
    _WARNING_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//button[@class='btn btn-sm btn-primary']"
    )
    _WARNING: Tuple[str, str] = (
        By.XPATH,
        "//div[@class='o_notification_manager']"
    )

    # Customer list and details - dynamic collection
    _ALL_CUSTOMERS: Tuple[str, str] = (
        By.XPATH,
        "//div[@class='oe_kanban_global_click o_res_partner_kanban o_kanban_record']"
    )
    _DETAILS: Tuple[str, str] = (
        By.XPATH,
        "//div[@class=\"oe_kanban_details\"]//span"
    )

    # =========================================================================
    # PROPERTY METHODS - Public Element Accessors
    # =========================================================================
    # Each property returns fresh WebElement reference with explicit wait
    # Prevents stale element exceptions from Java PageFactory pattern

    @property
    def sales_partial(self) -> WebElement:
        """
        Sales module navigation link (partial link text match).

        Returns:
            WebElement: Sales navigation link element

        Example:
            >>> sales_page.sales_partial.click()
        """
        return self.wait_for_clickable(self._SALES_PARTIAL)

    @property
    def customers_button(self) -> WebElement:
        """
        Customers submenu button with specific href navigation.

        Returns:
            WebElement: Customers button span element

        Example:
            >>> sales_page.customers_button.click()
        """
        return self.wait_for_clickable(self._CUSTOMERS_BUTTON)

    @property
    def create_button(self) -> WebElement:
        """
        Create new customer button in kanban view.

        Returns:
            WebElement: Create button element

        Example:
            >>> sales_page.create_button.click()
        """
        return self.wait_for_clickable(self._CREATE_BUTTON)

    @property
    def customer_name(self) -> WebElement:
        """
        Customer name input field.

        Technical Debt:
            Uses generated ID 'o_field_input_470' which may change with app updates.
            Recommend stable test ID attribute.

        Returns:
            WebElement: Customer name input element

        Example:
            >>> sales_page.customer_name.send_keys("ACME Corporation")
        """
        return self.wait_for_element(self._CUSTOMER_NAME)

    @property
    def address(self) -> WebElement:
        """
        Customer address input field.

        Technical Debt:
            Uses generated ID 'o_field_input_474' which may change with app updates.

        Returns:
            WebElement: Address input element

        Example:
            >>> sales_page.address.send_keys("123 Main Street")
        """
        return self.wait_for_element(self._ADDRESS)

    @property
    def state_options(self) -> WebElement:
        """
        State selection dropdown input field.

        Technical Debt:
            Uses generated ID 'o_field_input_477' which may change with app updates.

        Returns:
            WebElement: State options input element

        Example:
            >>> sales_page.state_options.click()
        """
        return self.wait_for_element(self._STATE_OPTIONS)

    @property
    def create_and_edit_state(self) -> WebElement:
        """
        'Create and Edit...' option in state dropdown.

        Returns:
            WebElement: Create and edit list item element

        Example:
            >>> sales_page.create_and_edit_state.click()
        """
        return self.wait_for_clickable(self._CREATE_AND_EDIT_STATE)

    @property
    def state_name(self) -> WebElement:
        """
        State name input field in state creation dialog.

        Technical Debt:
            Uses generated ID 'o_field_input_516' which may change with app updates.

        Returns:
            WebElement: State name input element

        Example:
            >>> sales_page.state_name.send_keys("California")
        """
        return self.wait_for_element(self._STATE_NAME)

    @property
    def state_code(self) -> WebElement:
        """
        State code input field in state creation dialog.

        Technical Debt:
            Uses generated ID 'o_field_input_517' which may change with app updates.

        Returns:
            WebElement: State code input element

        Example:
            >>> sales_page.state_code.send_keys("CA")
        """
        return self.wait_for_element(self._STATE_CODE)

    @property
    def country_state_button(self) -> WebElement:
        """
        Country selection button for state association.

        Technical Debt:
            Uses generated ID 'o_field_input_518' which may change with app updates.

        Returns:
            WebElement: Country state button input element

        Example:
            >>> sales_page.country_state_button.click()
        """
        return self.wait_for_element(self._COUNTRY_STATE_BUTTON)

    @property
    def country_selection(self) -> WebElement:
        """
        Country selection item in dropdown (specific UI ID).

        Returns:
            WebElement: Country selection link element

        Example:
            >>> sales_page.country_selection.click()
        """
        return self.wait_for_clickable(self._COUNTRY_SELECTION)

    @property
    def save_button(self) -> WebElement:
        """
        Save button for state/country form submission.

        Returns:
            WebElement: Save button span element

        Example:
            >>> sales_page.save_button.click()
        """
        return self.wait_for_clickable(self._SAVE_BUTTON)

    @property
    def create_customer(self) -> WebElement:
        """
        Create customer button for final customer form submission.

        Returns:
            WebElement: Create customer button element

        Example:
            >>> sales_page.create_customer.click()
        """
        return self.wait_for_clickable(self._CREATE_CUSTOMER)

    @property
    def search_bar(self) -> WebElement:
        """
        Search input field for filtering customer list.

        Returns:
            WebElement: Search bar input element

        Example:
            >>> sales_page.search_bar.send_keys("ACME")
            >>> sales_page.search_bar.send_keys(Keys.RETURN)
        """
        return self.wait_for_element(self._SEARCH_BAR)

    @property
    def name_check(self) -> WebElement:
        """
        Customer name display in kanban card (for validation).

        Returns:
            WebElement: Customer name span element

        Example:
            >>> displayed_name = sales_page.name_check.text
            >>> assert displayed_name == "ACME Corporation"
        """
        return self.wait_for_element(self._NAME_CHECK)

    @property
    def warning_button(self) -> WebElement:
        """
        Warning dialog button (primary action button).

        Returns:
            WebElement: Warning button element

        Example:
            >>> sales_page.warning_button.click()
        """
        return self.wait_for_clickable(self._WARNING_BUTTON)

    @property
    def warning(self) -> WebElement:
        """
        Warning notification container element.

        Returns:
            WebElement: Warning notification manager div

        Example:
            >>> if sales_page.warning.is_displayed():
            ...     print("Warning notification shown")
        """
        return self.wait_for_visibility(self._WARNING)

    @property
    def all_customers(self) -> List[WebElement]:
        """
        Collection of all customer kanban cards in current view.

        Note:
            This property returns a list of WebElements representing dynamic customer
            cards. Unlike single-element properties, this uses get_elements() which
            returns immediately without explicit wait. If you need to ensure at least
            one customer exists, wait for first element visibility before calling:

            >>> # Wait for at least one customer card
            >>> sales_page.wait_for_element(sales_page._ALL_CUSTOMERS)
            >>> # Then get all cards
            >>> customers = sales_page.all_customers

        Returns:
            List[WebElement]: List of customer card elements (empty if none found)

        Example:
            >>> customers = sales_page.all_customers
            >>> print(f"Found {len(customers)} customers")
            >>> for customer in customers:
            ...     print(customer.text)
        """
        return self.get_elements(self._ALL_CUSTOMERS)

    @property
    def link(self) -> WebElement:
        """
        Direct link to customers page (alternative navigation).

        Returns:
            WebElement: Customers page link element

        Example:
            >>> sales_page.link.click()
        """
        return self.wait_for_clickable(self._LINK)

    @property
    def details(self) -> WebElement:
        """
        Customer details span within kanban card.

        Returns:
            WebElement: Customer details span element

        Example:
            >>> details_text = sales_page.details.text
            >>> print(f"Customer details: {details_text}")
        """
        return self.wait_for_element(self._DETAILS)


# Module-level validation
if __name__ == "__main__":
    # Module self-test demonstrating SalesPage structure.
    # Note: This requires a running WebDriver instance and is for documentation.
    # Actual usage occurs in Behave step definitions.
    print("SalesPage module loaded successfully")
    print("Total locators defined: 20")
    print("Total properties exposed: 20 single elements + 1 list property")
    print("\nLocator summary:")
    print("  - Navigation: 3 elements (sales_partial, customers_button, link)")
    print("  - Action buttons: 3 elements (create_button, save_button, create_customer)")
    print("  - Form inputs: 6 elements (customer_name, address, state fields)")
    print("  - Dropdowns: 2 elements (create_and_edit_state, country_selection)")
    print("  - Search/Validation: 2 elements (search_bar, name_check)")
    print("  - Notifications: 2 elements (warning_button, warning)")
    print("  - Collections: 1 list (all_customers)")
    print("  - Details: 1 element (details)")
    print("\nTechnical Debt Alert:")
    print("  6 locators use generated IDs (o_field_input_470, 474, 477, 516, 517, 518)")
    print("  Recommend requesting stable test IDs from development team")
