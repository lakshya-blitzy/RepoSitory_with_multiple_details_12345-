"""
Contacts Page Module

Page object for the Contacts module in the Testinium application.
Provides element locators and interaction methods for contact management operations.

This module converts Java PageFactory pattern from ContactsP.java to Python property-based
locators, replacing @FindBy annotations with explicit locator tuples and property decorators.

Key Features:
- Contact module navigation
- Contact creation and editing (name, street, phone, email inputs)
- Contact list operations (create, edit, delete actions)
- Contact selection via checkbox selectors
- Action menu interactions for contact operations

Migration Context:
    Java Source: src/main/java/com/testinium/pages/ContactsP.java
    Pattern Change: PageFactory.initElements() → Property-based locators with explicit waits
    Encapsulation: Public WebElement fields → Private locator constants with @property accessors

Technical Debt:
    This page object contains position-dependent XPath selectors that are brittle and may
    break with DOM structure changes:

    1. _NEW_CONTACT: xpath='(//div[@class="o_checkbox"]/input)[12]'
       - Uses hardcoded index [12] to select specific checkbox
       - Risk: Breaks if contact order changes or new contacts added
       - Recommendation: Application should use data-test-id attributes

    2. _ACTION_INPUT: xpath='(//div[@class="o_cp_sidebar"]/div/div)[2]'
       - Uses hardcoded index [2] for sidebar element selection
       - Risk: Breaks if sidebar structure changes

    3. _FIRST_USER:
       xpath='(//div[@class="o_kanban_view o_res_partner_kanban o_kanban_ungrouped"]/div)[1]'
       - Uses index [1] to select first user in kanban view
       - Risk: Brittle with dynamic user lists

    These locators are preserved from the Java implementation for behavioral equivalence
    per migration requirements (Section 0.9.1: "Preserve all original locator strategies
    including brittle index-based XPath selectors for behavioral equivalence").

    Future Enhancement: Work with development team to add data-testid attributes:
    - data-testid="contact-checkbox-{contact_id}"
    - data-testid="sidebar-action-menu"
    - data-testid="contact-card-{index}"

Example Usage:
    >>> from selenium import webdriver
    >>> from pages.contacts_page import ContactsPage
    >>>
    >>> driver = webdriver.Chrome()
    >>> contacts_page = ContactsPage(driver)
    >>>
    >>> # Navigate to contacts module
    >>> contacts_page.contact_module.click()
    >>>
    >>> # Create new contact
    >>> contacts_page.create_contact.click()
    >>> contacts_page.name_input.send_keys("John Doe")
    >>> contacts_page.street_input.send_keys("123 Main St")
    >>> contacts_page.phone_no_input.send_keys("555-0100")
    >>> contacts_page.email_input.send_keys("john@example.com")
    >>> contacts_page.ok_btn.click()
    >>>
    >>> # Select and delete contact
    >>> contacts_page.new_contact.click()
    >>> contacts_page.action_input.click()
    >>> contacts_page.delete_input.click()
"""

from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class ContactsPage(BasePage):
    """
    Page object for Contacts module providing element locators and interaction methods.

    This class follows the Page Object Model pattern by encapsulating all element locators
    and interaction logic for the Contacts module. It inherits from BasePage to leverage
    explicit wait utilities and common WebDriver operations.

    Attributes:
        All locator constants are private tuple pairs of (By strategy, locator value)
        All element properties are public and return fresh WebElement references via
        BasePage wait methods (wait_for_element, wait_for_clickable, wait_for_visibility)

    Locator Strategy Breakdown:
        - PARTIAL_LINK_TEXT: 1 locator (contact_module navigation)
        - XPATH with accesskey: 2 locators (create_contact, call_list buttons)
        - NAME attributes: 4 locators (form inputs: name, street, phone, email)
        - XPATH text match: 1 locator (ok_btn with text 'Ok')
        - XPATH position-based: 4 locators (brittle - see Technical Debt section)
        - XPATH class-based: 3 locators (edit_title, edit_btn, print_input)
        - XPATH with data-index: 1 locator (delete_input)

    Thread Safety:
        ContactsPage instances are thread-safe when each thread uses its own WebDriver
        instance (achieved via DriverManager's threading.local()). Each property call
        performs a fresh element lookup, preventing stale element references in parallel
        test execution.

    Behavioral Equivalence:
        All locators match the Java ContactsP.java implementation exactly to ensure
        test scenarios produce identical results during migration validation.

    Example:
        >>> from utilities.driver_manager import DriverManager
        >>> from pages.contacts_page import ContactsPage
        >>>
        >>> # In Behave step definition with context
        >>> driver = context.driver_manager.get_driver()
        >>> contacts_page = ContactsPage(driver)
        >>>
        >>> # Navigate and create contact
        >>> contacts_page.contact_module.click()
        >>> contacts_page.create_contact.click()
        >>> contacts_page.name_input.send_keys(contact_name)
    """

    # ============================================================================
    # PRIVATE LOCATOR CONSTANTS
    # ============================================================================
    # Following Python naming convention: UPPER_CASE for constants with leading
    # underscore to indicate private/internal use
    # ============================================================================

    # Navigation Locators
    _CONTACT_MODULE: Tuple[str, str] = (By.PARTIAL_LINK_TEXT, "Contacts")

    # Action Button Locators
    _CREATE_CONTACT_BUTTON: Tuple[str, str] = (By.XPATH, "//button[@accesskey='c']")
    _CALL_LIST_BUTTON: Tuple[str, str] = (By.XPATH, "//button[@accesskey='l']")

    # Form Input Locators (Name-based - stable strategy)
    _NAME_INPUT: Tuple[str, str] = (By.NAME, "name")
    _STREET_INPUT: Tuple[str, str] = (By.NAME, "street")
    _PHONE_INPUT: Tuple[str, str] = (By.NAME, "phone")
    _EMAIL_INPUT: Tuple[str, str] = (By.NAME, "email")

    # Dialog Button Locators
    _OK_BUTTON: Tuple[str, str] = (By.XPATH, "//span[.='Ok']")

    # Contact Selection Locators
    # TECHNICAL DEBT: Position-dependent locator using index [12]
    # This is brittle and will break if contact order changes or new contacts are added
    # Preserved from Java implementation for behavioral equivalence
    # Future: Request data-testid="contact-checkbox-{id}" from development team
    _NEW_CONTACT_CHECKBOX: Tuple[str, str] = (
        By.XPATH,
        "(//div[@class='o_checkbox']/input)[12]"
    )

    # Sidebar Action Locators
    # TECHNICAL DEBT: Position-dependent locator using index [2]
    # Brittle selector that assumes specific sidebar structure
    # Preserved from Java implementation for behavioral equivalence
    # Future: Request data-testid="sidebar-action-menu"
    _ACTION_INPUT: Tuple[str, str] = (
        By.XPATH,
        "(//div[@class='o_cp_sidebar']/div/div)[2]"
    )

    _DELETE_INPUT: Tuple[str, str] = (By.XPATH, "//a[@data-index='3']")

    # Contact List/Kanban View Locators
    # TECHNICAL DEBT: Position-dependent locator using index [1]
    # Assumes first user in kanban view - brittle with dynamic lists
    # Preserved from Java implementation for behavioral equivalence
    _FIRST_USER: Tuple[str, str] = (
        By.XPATH,
        "(//div[@class='o_kanban_view o_res_partner_kanban o_kanban_ungrouped']/div)[1]"
    )

    # Contact Edit Locators
    _EDIT_TITLE: Tuple[str, str] = (By.XPATH, "//div[@class='oe_title']")
    _EDIT_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//button[@class='btn btn-primary btn-sm o_form_button_edit']"
    )

    # Menu/Dropdown Locators
    _PRINT_INPUT: Tuple[str, str] = (By.XPATH, "//div[@class='btn-group o_dropdown open']")
    _DUE_PAYMENT: Tuple[str, str] = (
        By.XPATH,
        "(//div[@class='btn-group o_dropdown open']/button)"
    )

    # ============================================================================
    # PUBLIC PROPERTY-BASED ELEMENT ACCESSORS
    # ============================================================================
    # Each property returns a fresh WebElement reference using BasePage wait methods
    # This prevents stale element references and ensures thread safety
    # Property names match Java field names for migration traceability
    # ============================================================================

    @property
    def contact_module(self) -> WebElement:
        """
        Contacts module navigation link in the main menu.

        Locator Strategy: PARTIAL_LINK_TEXT
        Wait Strategy: Presence in DOM (may not be visible initially)

        Use Case:
            Click to navigate to the Contacts module from any page

        Returns:
            WebElement: The Contacts navigation link element

        Example:
            >>> contacts_page.contact_module.click()
        """
        return self.wait_for_element(self._CONTACT_MODULE)

    @property
    def create_contact(self) -> WebElement:
        """
        Create contact button with accesskey 'c' for keyboard shortcut.

        Locator Strategy: XPATH with accesskey attribute
        Wait Strategy: Clickable (visible and enabled)

        Use Case:
            Click to open the contact creation form
            Keyboard shortcut: Alt+C (Windows/Linux) or Control+Option+C (Mac)

        Returns:
            WebElement: The create contact button element

        Example:
            >>> contacts_page.create_contact.click()
        """
        return self.wait_for_clickable(self._CREATE_CONTACT_BUTTON)

    @property
    def name_input(self) -> WebElement:
        """
        Contact name input field in the contact creation/edit form.

        Locator Strategy: NAME attribute (stable strategy)
        Wait Strategy: Presence in DOM

        Use Case:
            Enter contact's full name during contact creation or editing

        Returns:
            WebElement: The name input field element

        Example:
            >>> contacts_page.name_input.send_keys("John Doe")
        """
        return self.wait_for_element(self._NAME_INPUT)

    @property
    def street_input(self) -> WebElement:
        """
        Contact street address input field in the contact form.

        Locator Strategy: NAME attribute (stable strategy)
        Wait Strategy: Presence in DOM

        Use Case:
            Enter contact's street address during contact creation or editing

        Returns:
            WebElement: The street input field element

        Example:
            >>> contacts_page.street_input.send_keys("123 Main Street")
        """
        return self.wait_for_element(self._STREET_INPUT)

    @property
    def phone_no_input(self) -> WebElement:
        """
        Contact phone number input field in the contact form.

        Locator Strategy: NAME attribute (stable strategy)
        Wait Strategy: Presence in DOM

        Use Case:
            Enter contact's phone number during contact creation or editing

        Returns:
            WebElement: The phone input field element

        Example:
            >>> contacts_page.phone_no_input.send_keys("555-0100")
        """
        return self.wait_for_element(self._PHONE_INPUT)

    @property
    def email_input(self) -> WebElement:
        """
        Contact email address input field in the contact form.

        Locator Strategy: NAME attribute (stable strategy)
        Wait Strategy: Presence in DOM

        Use Case:
            Enter contact's email address during contact creation or editing

        Returns:
            WebElement: The email input field element

        Example:
            >>> contacts_page.email_input.send_keys("john@example.com")
        """
        return self.wait_for_element(self._EMAIL_INPUT)

    @property
    def ok_btn(self) -> WebElement:
        """
        OK button to confirm and save contact form changes.

        Locator Strategy: XPATH text match (case-sensitive)
        Wait Strategy: Clickable (visible and enabled)

        Use Case:
            Click to save contact creation or edit form
            Confirms and closes the contact dialog

        Returns:
            WebElement: The OK button element

        Example:
            >>> contacts_page.ok_btn.click()
        """
        return self.wait_for_clickable(self._OK_BUTTON)

    @property
    def call_list(self) -> WebElement:
        """
        Call list button with accesskey 'l' for keyboard shortcut.

        Locator Strategy: XPATH with accesskey attribute
        Wait Strategy: Clickable (visible and enabled)

        Use Case:
            Click to access call list functionality for contacts
            Keyboard shortcut: Alt+L (Windows/Linux) or Control+Option+L (Mac)

        Returns:
            WebElement: The call list button element

        Example:
            >>> contacts_page.call_list.click()
        """
        return self.wait_for_clickable(self._CALL_LIST_BUTTON)

    @property
    def new_contact(self) -> WebElement:
        """
        Contact selection checkbox (position-dependent selector).

        ⚠️ TECHNICAL DEBT WARNING ⚠️
        This locator uses a hardcoded position index [12] which is brittle and may break
        if the contact order changes, new contacts are added, or the DOM structure changes.

        Locator Strategy: XPATH with position index [12] - BRITTLE
        Wait Strategy: Presence in DOM

        Original Java: @FindBy(xpath = "(//div[@class='o_checkbox']/input)[12]")

        Preservation Reason:
            Maintained from Java implementation for behavioral equivalence during migration
            (per Section 0.9.1: preserve all original locator strategies)

        Recommended Future Enhancement:
            Request development team to add data-testid attributes:
            <input data-testid="contact-checkbox-{contact_id}" />

            Then update locator to:
            _NEW_CONTACT = (By.XPATH, "//input[@data-testid='contact-checkbox-{id}']")

        Use Case:
            Select a specific contact via checkbox for bulk operations
            Currently assumes the 12th checkbox in the contacts list

        Returns:
            WebElement: The contact checkbox element (12th in list)

        Example:
            >>> contacts_page.new_contact.click()  # Select contact
        """
        return self.wait_for_element(self._NEW_CONTACT_CHECKBOX)

    @property
    def action_input(self) -> WebElement:
        """
        Action menu input element in the sidebar (position-dependent selector).

        ⚠️ TECHNICAL DEBT WARNING ⚠️
        This locator uses a hardcoded position index [2] which assumes specific sidebar
        structure. May break with sidebar layout changes.

        Locator Strategy: XPATH with position index [2] - BRITTLE
        Wait Strategy: Presence in DOM

        Original Java: @FindBy(xpath = "(//div[@class='o_cp_sidebar']/div/div)[2]")

        Preservation Reason:
            Maintained from Java implementation for behavioral equivalence

        Recommended Future Enhancement:
            Request data-testid="sidebar-action-menu" from development team

        Use Case:
            Access action menu for contact operations (edit, delete, etc.)

        Returns:
            WebElement: The sidebar action input element (2nd in structure)

        Example:
            >>> contacts_page.action_input.click()  # Open action menu
        """
        return self.wait_for_element(self._ACTION_INPUT)

    @property
    def delete_input(self) -> WebElement:
        """
        Delete action link in the contact action menu.

        Locator Strategy: XPATH with data-index attribute
        Wait Strategy: Clickable (visible and enabled)

        Use Case:
            Click to delete selected contact(s)
            Typically used after selecting contacts and opening action menu

        Returns:
            WebElement: The delete action link element

        Example:
            >>> contacts_page.new_contact.click()  # Select contact
            >>> contacts_page.action_input.click()  # Open menu
            >>> contacts_page.delete_input.click()  # Delete contact
        """
        return self.wait_for_clickable(self._DELETE_INPUT)

    @property
    def edit_btn(self) -> WebElement:
        """
        Edit button to modify existing contact details.

        Locator Strategy: XPATH with specific button class
        Wait Strategy: Clickable (visible and enabled)

        Use Case:
            Click to enter edit mode for a contact
            Enables form fields for modification

        Returns:
            WebElement: The edit button element

        Example:
            >>> contacts_page.first_user.click()  # Open contact
            >>> contacts_page.edit_btn.click()  # Enter edit mode
        """
        return self.wait_for_clickable(self._EDIT_BUTTON)

    @property
    def first_user(self) -> WebElement:
        """
        First user/contact card in the kanban view (position-dependent selector).

        ⚠️ TECHNICAL DEBT WARNING ⚠️
        This locator uses a hardcoded position index [1] which assumes first position
        in the kanban view. Brittle with dynamic user lists or sorting changes.

        Locator Strategy: XPATH with position index [1] - BRITTLE
        Wait Strategy: Clickable (visible and enabled)

        Original Java:
            @FindBy(xpath = "(//div[@class='o_kanban_view ...']/div)[1]")

        Preservation Reason:
            Maintained from Java implementation for behavioral equivalence

        Recommended Future Enhancement:
            Use data-testid with dynamic contact identifiers

        Use Case:
            Click to open the first contact in the kanban view
            Useful for testing default list state or first contact operations

        Returns:
            WebElement: The first contact card element in kanban view

        Example:
            >>> contacts_page.first_user.click()  # Open first contact
        """
        return self.wait_for_clickable(self._FIRST_USER)

    @property
    def edit_title(self) -> WebElement:
        """
        Edit title section element in the contact form.

        Locator Strategy: XPATH with class name
        Wait Strategy: Presence in DOM

        Use Case:
            Access or verify the title section of the contact edit form
            May contain contact name or form heading

        Returns:
            WebElement: The edit title div element

        Example:
            >>> title_text = contacts_page.edit_title.text
            >>> assert "Contact" in title_text
        """
        return self.wait_for_element(self._EDIT_TITLE)

    @property
    def print_input(self) -> WebElement:
        """
        Print dropdown menu element for contact printing operations.

        Locator Strategy: XPATH with dropdown class (requires dropdown to be open)
        Wait Strategy: Presence in DOM

        Use Case:
            Access print options for contacts
            Note: Dropdown must be open for element to exist

        Returns:
            WebElement: The print dropdown menu element

        Example:
            >>> # Open action menu first, then access print options
            >>> contacts_page.print_input.click()
        """
        return self.wait_for_element(self._PRINT_INPUT)

    @property
    def due_payment(self) -> WebElement:
        """
        Due payment button within the dropdown menu.

        Locator Strategy: XPATH with dropdown class (requires dropdown to be open)
        Wait Strategy: Clickable (visible and enabled)

        Use Case:
            Access due payment functionality for contacts
            Note: Dropdown menu must be open for element to be accessible

        Returns:
            WebElement: The due payment button element

        Example:
            >>> # Open dropdown first, then access due payment
            >>> contacts_page.due_payment.click()
        """
        return self.wait_for_clickable(self._DUE_PAYMENT)


# Module-level documentation for testing and validation
if __name__ == "__main__":
    # ContactsPage module self-documentation.
    #
    # This module cannot be executed directly as it requires a WebDriver instance.
    # Actual usage should be within Behave step definitions or pytest-bdd tests.
    #
    # Migration Validation Checklist:
    # ✓ All 16 Java @FindBy locators converted to Python tuples
    # ✓ All public WebElement fields converted to @property methods
    # ✓ Inherits from BasePage for wait utilities
    # ✓ Uses explicit waits (no implicit waits)
    # ✓ Preserves brittle position-dependent locators for behavioral equivalence
    # ✓ Documents technical debt for future refactoring
    # ✓ Type hints on all properties (returns WebElement)
    # ✓ Comprehensive docstrings with use cases and examples
    # ✓ Property names match Java field names for traceability
    # ✓ Thread-safe via fresh element lookups on each property access
    print("ContactsPage module loaded successfully")
    print("\nMigration Summary:")
    print("  Java Source: src/main/java/com/testinium/pages/ContactsP.java")
    print("  Python Target: pages/contacts_page.py")
    print("  Pattern: PageFactory → Property-based locators")
    print("  Locators: 16 total (3 position-dependent/brittle)")
    print("\nLocator Breakdown:")
    print("  ✓ 1 PARTIAL_LINK_TEXT (navigation)")
    print("  ✓ 2 XPATH with accesskey (buttons)")
    print("  ✓ 4 NAME attributes (form inputs)")
    print("  ✓ 1 XPATH text match (OK button)")
    print("  ⚠ 3 XPATH position-based (BRITTLE - technical debt)")
    print("  ✓ 5 XPATH class/attribute-based (edit, delete, print)")
    print("\nTechnical Debt:")
    print("  ⚠ _NEW_CONTACT_CHECKBOX: Position index [12]")
    print("  ⚠ _ACTION_INPUT: Position index [2]")
    print("  ⚠ _FIRST_USER: Position index [1]")
    print("\n  Recommendation: Request data-testid attributes from development team")
    print("\nUsage Example:")
    print("""
    from pages.contacts_page import ContactsPage

    @when('User creates a new contact with name "{name}"')
    def create_contact(context, name):
        contacts_page = ContactsPage(context.driver)
        contacts_page.contact_module.click()
        contacts_page.create_contact.click()
        contacts_page.name_input.send_keys(name)
        contacts_page.street_input.send_keys("123 Main St")
        contacts_page.phone_no_input.send_keys("555-0100")
        contacts_page.email_input.send_keys(f"{name.lower().replace(' ', '.')}@example.com")
        contacts_page.ok_btn.click()
    """)
