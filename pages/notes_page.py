"""
Notes Page Module

Page object for the Testinium Notes management interface.
This module provides element locators and interaction methods for notes module operations.

Key Features:
- Notes module navigation and access
- Note creation interface with form elements
- Tags input for categorizing notes
- Rich text description editor interaction
- Save functionality for note persistence
- Created message confirmation verification
- Table organization with status-based selectors
- Text-based navigation elements for module access

Migration Context:
    Converted from NotesP.java which used PageFactory pattern with @FindBy annotations.
    Java implementation exposed public WebElement fields. This Python version uses
    property-based locators with explicit waits through BasePage inheritance,
    preventing stale element exceptions and improving maintainability.

    Original Java class: src/main/java/com/testinium/pages/NotesP.java
    - 10 @FindBy annotated fields
    - PageFactory.initElements() in constructor
    - Public WebElement exposure (anti-pattern)

Locator Strategy:
    Preserves original Java locators for behavioral equivalence:
    - XPATH with exact text matching for navigation ('Create and Edit...')
    - PARTIAL_LINK_TEXT for module access ('Notes')
    - XPATH with class-based selectors for buttons and inputs
    - XPATH with exact text for confirmation messages ('Note created')
    - XPATH with data-id attributes for table organization (brittle - see note below)

IMPORTANT - Brittle Locators:
    The newTable and todayTable locators use data-id attributes with index-based XPath:
    - (//div[@data-id='1193']/div)[2]
    - (//div[@data-id='1194']/div)[1]
    
    These are FRAGILE and may break with DOM structure changes. They are preserved
    from the Java implementation to maintain behavioral equivalence during migration.
    
    RECOMMENDATION: Post-migration, work with development team to add stable test IDs
    or use more resilient selectors (e.g., aria-label, data-testid attributes).

Design Pattern:
    Follows Page Object Model with property-based element access:
    - Private locator constants (_UPPERCASE naming convention)
    - Public @property methods returning fresh WebElement references
    - All properties use BasePage wait methods (wait_for_element, wait_for_clickable)
    - Inherits driver, wait, config, and actions from BasePage

Thread Safety:
    Thread-safe when each test thread has its own WebDriver instance from DriverManager.
    Each NotesPage instance is bound to a specific driver, supporting parallel execution.

Example Usage:
    >>> from pages.notes_page import NotesPage
    >>> from utilities.driver_manager import DriverManager
    >>>
    >>> driver = DriverManager.get_driver()
    >>> notes_page = NotesPage(driver)
    >>> notes_page.notes_module.click()
    >>> notes_page.creating_notes.click()
    >>> notes_page.tags_n.send_keys("automation, testing")
    >>> notes_page.description.send_keys("Test note description")
    >>> notes_page.save_btn.click()
    >>> assert notes_page.created_message.is_displayed()
"""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class NotesPage(BasePage):
    """
    Page object for Testinium Notes management interface.

    This class provides access to all elements on the Notes page including:
    - Module navigation (notes_module, tab_index)
    - Note creation interface (creating_notes button)
    - Form inputs (tags_n, description editor)
    - Action buttons (save_btn)
    - Confirmation messages (created_message)
    - Application identifiers (app_k)
    - Table organization (new_table, today_table with data-id selectors)

    All element properties return fresh WebElement references via BasePage wait methods,
    preventing stale element exceptions common in PageFactory pattern.

    Attributes:
        _logger (Logger): Logger instance for notes page operations
        
    Inherited from BasePage:
        driver (WebDriver): Selenium WebDriver instance
        config (ConfigReader): Configuration reader singleton
        default_timeout (int): Default explicit wait timeout
        wait (WebDriverWait): Pre-configured WebDriverWait instance
        actions (ActionChains): ActionChains for complex interactions

    Element Properties:
        tab_index: Navigation link for 'Create and Edit...' tab
        notes_module: Module navigation link with partial text 'Notes'
        creating_notes: Button to initiate new note creation
        tags_n: Input field for note tags/categories
        description: Rich text editor for note content
        created_message: Confirmation message 'Note created'
        save_btn: Button to save note changes
        app_k: Application identifier element with text 'BDD Approach Framework with Cucumber'
        new_table: Table container with data-id='1193' (brittle selector)
        today_table: Table container with data-id='1194' (brittle selector)

    Example:
        >>> driver = webdriver.Chrome()
        >>> notes_page = NotesPage(driver)
        >>> notes_page.notes_module.click()
        >>> notes_page.creating_notes.click()
        >>> notes_page.tags_n.send_keys("test, automation")
        >>> notes_page.description.send_keys("This is a test note")
        >>> notes_page.save_btn.click()
        >>> assert "Note created" in notes_page.created_message.text
    """

    # Private locator constants following Python naming conventions
    # Format: _ELEMENT_NAME = (By.STRATEGY, 'locator_value')

    # Navigation elements - text-based selectors for module access
    _TAB_INDEX = (By.XPATH, "//a[. = 'Create and Edit...']")
    _NOTES_MODULE = (By.PARTIAL_LINK_TEXT, "Notes")

    # Note creation interface - button with class-based selector
    _CREATING_NOTES_BUTTON = (
        By.XPATH,
        "//button[@class='btn btn-primary btn-sm o-kanban-button-new']"
    )

    # Form input elements - class-based selectors for input fields
    _TAGS_INPUT = (By.XPATH, "//input[@class='o_input ui-autocomplete-input']")
    _DESCRIPTION_EDITOR = (By.XPATH, "//div[@class='note-editable panel-body']")

    # Confirmation and status elements - exact text matching
    _CREATED_MESSAGE = (By.XPATH, "//p[.='Note created']")

    # Action buttons - class-based selector for primary actions
    _SAVE_BUTTON = (
        By.XPATH,
        "//button[@class='btn btn-primary btn-sm o_form_button_save']"
    )

    # Application identifier - exact text matching for specific note title
    _APP_K = (By.XPATH, "//span[.='BDD Approach Framework with Cucumber']")

    # Table organization elements - BRITTLE data-id based selectors
    # WARNING: These selectors use data-id attributes with index-based XPath
    # They are fragile and may break with DOM changes. Preserved for behavioral equivalence.
    # TODO (post-migration): Replace with stable selectors (data-testid, aria-label)
    _NEW_TABLE = (By.XPATH, "(//div[@data-id='1193']/div)[2]")
    _TODAY_TABLE = (By.XPATH, "(//div[@data-id='1194']/div)[1]")

    def __init__(self, driver) -> None:
        """
        Initialize NotesPage with WebDriver instance.

        Calls BasePage constructor to set up:
        - WebDriver reference for element interaction
        - ConfigReader for configuration access
        - Default timeout from config.yaml
        - WebDriverWait instance for element synchronization
        - ActionChains for complex interactions
        - Logger for page object operations

        Args:
            driver: Selenium WebDriver instance (thread-local from DriverManager)

        Example:
            >>> from selenium import webdriver
            >>> from pages.notes_page import NotesPage
            >>>
            >>> driver = webdriver.Chrome()
            >>> notes_page = NotesPage(driver)
        """
        super().__init__(driver)
        self._logger = logging.getLogger(__name__)
        self._logger.info("NotesPage initialized")

    # Property-based element accessors with explicit waits
    # Each property returns a fresh WebElement reference, preventing stale element issues

    @property
    def tab_index(self) -> WebElement:
        """
        Navigation link for 'Create and Edit...' tab.

        Returns fresh WebElement reference using explicit wait for element presence.
        Uses exact text matching in XPath: //a[. = 'Create and Edit...']

        Returns:
            WebElement: The 'Create and Edit...' navigation link

        Raises:
            TimeoutException: If element not present within configured timeout

        Example:
            >>> notes_page.tab_index.click()
        """
        self._logger.debug("Accessing tab_index element")
        return self.wait_for_element(self._TAB_INDEX)

    @property
    def notes_module(self) -> WebElement:
        """
        Module navigation link with partial text 'Notes'.

        Returns fresh WebElement reference using explicit wait for element presence.
        Uses partial link text matching for flexible module access.

        Returns:
            WebElement: The Notes module navigation link

        Raises:
            TimeoutException: If element not present within configured timeout

        Example:
            >>> notes_page.notes_module.click()
        """
        self._logger.debug("Accessing notes_module element")
        return self.wait_for_element(self._NOTES_MODULE)

    @property
    def creating_notes(self) -> WebElement:
        """
        Button to initiate new note creation.

        Returns fresh WebElement reference using explicit wait for clickability.
        Ensures button is visible and enabled before returning.

        Returns:
            WebElement: The note creation button (clickable state)

        Raises:
            TimeoutException: If button not clickable within configured timeout

        Example:
            >>> notes_page.creating_notes.click()
        """
        self._logger.debug("Accessing creating_notes button")
        return self.wait_for_clickable(self._CREATING_NOTES_BUTTON)

    @property
    def tags_n(self) -> WebElement:
        """
        Input field for note tags/categories.

        Returns fresh WebElement reference using explicit wait for element presence.
        Used for entering comma-separated tags or categories for note organization.

        Returns:
            WebElement: The tags input field

        Raises:
            TimeoutException: If input field not present within configured timeout

        Example:
            >>> notes_page.tags_n.send_keys("automation, testing, BDD")
        """
        self._logger.debug("Accessing tags_n input field")
        return self.wait_for_element(self._TAGS_INPUT)

    @property
    def description(self) -> WebElement:
        """
        Rich text editor for note content/description.

        Returns fresh WebElement reference using explicit wait for element presence.
        This is a content-editable div used for entering note body text.

        Returns:
            WebElement: The description editor element

        Raises:
            TimeoutException: If editor not present within configured timeout

        Example:
            >>> notes_page.description.send_keys("This is my note content")
        """
        self._logger.debug("Accessing description editor")
        return self.wait_for_element(self._DESCRIPTION_EDITOR)

    @property
    def created_message(self) -> WebElement:
        """
        Confirmation message displaying 'Note created'.

        Returns fresh WebElement reference using explicit wait for visibility.
        Used to verify successful note creation. Waits for element to be visible
        on page, not just present in DOM.

        Returns:
            WebElement: The 'Note created' confirmation message (visible state)

        Raises:
            TimeoutException: If message not visible within configured timeout

        Example:
            >>> notes_page.save_btn.click()
            >>> assert notes_page.created_message.is_displayed()
            >>> assert "Note created" in notes_page.created_message.text
        """
        self._logger.debug("Accessing created_message confirmation")
        return self.wait_for_visibility(self._CREATED_MESSAGE)

    @property
    def save_btn(self) -> WebElement:
        """
        Button to save note changes.

        Returns fresh WebElement reference using explicit wait for clickability.
        Ensures button is visible and enabled before returning. Primary action
        button for persisting note data.

        Returns:
            WebElement: The save button (clickable state)

        Raises:
            TimeoutException: If button not clickable within configured timeout

        Example:
            >>> notes_page.save_btn.click()
        """
        self._logger.debug("Accessing save_btn button")
        return self.wait_for_clickable(self._SAVE_BUTTON)

    @property
    def app_k(self) -> WebElement:
        """
        Application identifier element with specific note title.

        Returns fresh WebElement reference using explicit wait for element presence.
        Contains exact text 'BDD Approach Framework with Cucumber' for identifying
        specific test note or application context.

        Returns:
            WebElement: The application identifier span element

        Raises:
            TimeoutException: If element not present within configured timeout

        Example:
            >>> assert "BDD Approach Framework with Cucumber" in notes_page.app_k.text
        """
        self._logger.debug("Accessing app_k application identifier")
        return self.wait_for_element(self._APP_K)

    @property
    def new_table(self) -> WebElement:
        """
        Table container with data-id='1193' for new notes organization.

        **WARNING: BRITTLE LOCATOR**
        This locator uses data-id attribute with index-based XPath:
        (//div[@data-id='1193']/div)[2]

        This is fragile and may break with DOM structure changes. Preserved from
        Java implementation for behavioral equivalence during migration.

        **RECOMMENDATION:** Post-migration, replace with stable selector:
        - data-testid attribute: //div[@data-testid='new-notes-table']
        - aria-label attribute: //div[@aria-label='New Notes']
        - Stable class: //div[@class='notes-table-new']

        Returns fresh WebElement reference using explicit wait for element presence.

        Returns:
            WebElement: The new notes table container

        Raises:
            TimeoutException: If element not present within configured timeout

        Example:
            >>> new_table_element = notes_page.new_table
            >>> # Verify table is displayed
            >>> assert new_table_element.is_displayed()
        """
        self._logger.debug("Accessing new_table element (BRITTLE data-id locator)")
        self._logger.warning(
            "new_table uses brittle data-id='1193' selector - "
            "recommend refactoring to stable locator post-migration"
        )
        return self.wait_for_element(self._NEW_TABLE)

    @property
    def today_table(self) -> WebElement:
        """
        Table container with data-id='1194' for today's notes organization.

        **WARNING: BRITTLE LOCATOR**
        This locator uses data-id attribute with index-based XPath:
        (//div[@data-id='1194']/div)[1]

        This is fragile and may break with DOM structure changes. Preserved from
        Java implementation for behavioral equivalence during migration.

        **RECOMMENDATION:** Post-migration, replace with stable selector:
        - data-testid attribute: //div[@data-testid='today-notes-table']
        - aria-label attribute: //div[@aria-label='Today Notes']
        - Stable class: //div[@class='notes-table-today']

        Returns fresh WebElement reference using explicit wait for element presence.

        Returns:
            WebElement: The today's notes table container

        Raises:
            TimeoutException: If element not present within configured timeout

        Example:
            >>> today_table_element = notes_page.today_table
            >>> # Verify table is displayed
            >>> assert today_table_element.is_displayed()
        """
        self._logger.debug("Accessing today_table element (BRITTLE data-id locator)")
        self._logger.warning(
            "today_table uses brittle data-id='1194' selector - "
            "recommend refactoring to stable locator post-migration"
        )
        return self.wait_for_element(self._TODAY_TABLE)


# Module-level docstring for direct execution
if __name__ == "__main__":
    # Module self-test demonstrating NotesPage functionality.
    #
    # Note: This requires a running Selenium WebDriver instance and is primarily
    # for documentation purposes. Actual usage should be in step definition files.
    print("NotesPage module loaded successfully")
    print("\nPage Object Model Pattern Implementation:")
    print("- 10 element properties with explicit waits")
    print("- Inherits from BasePage for common utilities")
    print("- Property-based locators prevent stale element exceptions")
    print("- Thread-safe for parallel test execution")
    print("\nWARNING: Contains brittle data-id selectors (new_table, today_table)")
    print("Recommend refactoring to stable locators post-migration")
    print("\nExample usage in step definitions:")
    print("""
    from behave import given, when, then
    from pages.notes_page import NotesPage

    @when('User navigates to Notes module')
    def navigate_to_notes(context):
        notes_page = NotesPage(context.driver)
        notes_page.notes_module.click()

    @when('User creates a new note with tags "{tags}" and description "{description}"')
    def create_note(context, tags, description):
        notes_page = NotesPage(context.driver)
        notes_page.creating_notes.click()
        notes_page.tags_n.send_keys(tags)
        notes_page.description.send_keys(description)
        notes_page.save_btn.click()

    @then('User should see note created confirmation')
    def verify_note_created(context):
        notes_page = NotesPage(context.driver)
        assert notes_page.created_message.is_displayed()
        assert "Note created" in notes_page.created_message.text
    """)
