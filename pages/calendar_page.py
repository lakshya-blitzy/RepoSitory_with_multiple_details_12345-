"""
Calendar Page Module

Page Object Model for Calendar/Meetings module in Testinium application.
Converted from CalendarP.java with property-based locators replacing PageFactory pattern.

Key Features:
- Calendar module navigation and interaction
- View selection (Day/Week/Month buttons)
- Date navigation and selection
- Meeting/note creation and editing interface
- Note summary management
- Tag management for categorization

Migration Context:
    Java Source: src/main/java/com/testinium/pages/CalendarP.java
    Migration Type: PageFactory @FindBy annotations → Python property-based locators
    Pattern: Public WebElement fields → Private locator tuples + @property methods

Technical Debt Documentation:
    1. DUPLICATE LOCATORS IDENTIFIED:
       - Lines 49-50 (createButton) and 58-59 (editButton) in Java source both use
         xpath='//button[@class="btn btn-sm btn-primary"]'
         This causes ambiguity when multiple matching buttons exist on the page.
         RECOMMENDATION: Add unique identifiers (data-testid, id) to application buttons

       - Lines 52-53 (getNote) and 73-74 (selectNote) both use
         xpath='//div[@class="o_field_name o_field_type_char"]'
         This duplicate locator may cause test failures if page structure changes.
         RECOMMENDATION: Use more specific locators or add unique attributes

    2. BRITTLE INDEX-BASED XPATH (HIGH RISK):
       - Line 40-41: xpath='(//td[@class="fc-widget-content"])[29]'
         This locator uses positional index [29] which breaks if:
         * Calendar view changes (different week displayed)
         * DOM structure modified (cells added/removed)
         * Screen resolution affects rendered cells
         PRESERVED FOR BEHAVIORAL EQUIVALENCE but flagged for future refactoring.
         RECOMMENDATION: Use date-based attributes or data-date selectors instead

Behavioral Preservation:
    All 21 element locators from CalendarP.java preserved exactly to maintain
    functional equivalence with Java implementation. Properties return fresh
    WebElement references on each access to prevent stale element exceptions.

Example Usage:
    >>> from selenium import webdriver
    >>> from pages.calendar_page import CalendarPage
    >>>
    >>> driver = webdriver.Chrome()
    >>> calendar_page = CalendarPage(driver)
    >>> calendar_page.calendar_button.click()
    >>> calendar_page.day.click()  # Switch to day view
    >>> calendar_page.summary_box.send_keys("Team Meeting")
    >>> calendar_page.create_button.click()
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CalendarPage(BasePage):
    """
    Page Object for Calendar/Meetings module with meeting management capabilities.

    This class provides access to all calendar interface elements including navigation,
    view controls, date selection, and meeting creation/editing functionality.
    Inherits from BasePage to leverage explicit wait strategies and prevent stale
    element references through property-based element access.

    Attributes:
        All locators defined as private class constants (tuples of By strategy and value)
        All elements exposed as @property methods returning fresh WebElement references

    Element Categories:
        - Navigation: calendar_button
        - View Controls: day, week, month buttons
        - Calendar Display: calendar_module, day_calendar, month_and_year_calendar
        - Date Selection: date_actual, date_box
        - Note Management: create_note, summary_box, get_note, select_note
        - Action Buttons: create_button, edit_button, save_button
        - Form Fields: edit_text, tags_checkbox
        - Modals: created_modele, created_note

    Technical Notes:
        - Duplicate locators exist for create_button/edit_button (same XPath)
        - Duplicate locators exist for get_note/select_note (same XPath)
        - date_box uses brittle index-based XPath [29] - preserved for equivalence

    Thread Safety:
        Thread-safe when each thread has its own WebDriver instance (via DriverManager)
    """

    # ====================
    # LOCATOR DEFINITIONS
    # ====================
    # Private locator constants as tuples of (By strategy, locator value)
    # Converted from Java @FindBy annotations

    # Page Title Element
    _TITLE = (By.XPATH, "//title[.='Meetings - Odoo']")

    # Navigation Element
    _CALENDAR_BUTTON = (By.PARTIAL_LINK_TEXT, "Calendar")

    # Calendar Container
    _CALENDAR_MODULE = (By.CLASS_NAME, "o_calendar_container")

    # View Selection Buttons (Day/Week/Month)
    _DAY_BUTTON = (By.XPATH, "//button[.='Day']")
    _WEEK_BUTTON = (By.XPATH, "//button[.='Week']")
    _MONTH_BUTTON = (By.XPATH, "//button[.='Month']")

    # Calendar Display Elements
    _DAY_CALENDAR = (By.CLASS_NAME, "ui-state-highlight")
    _MONTH_AND_YEAR_CALENDAR = (
        By.XPATH,
        "//td[@class=' ui-datepicker-days-cell-over  "
        "ui-datepicker-current-day ui-datepicker-today']"
    )

    # Date Information Elements
    _DATE_ACTUAL = (By.XPATH, "//div[@class='o_control_panel']/ol/li")

    # TECHNICAL DEBT: Brittle index-based locator [29]
    # This locator uses positional index which may break with DOM changes
    # Preserved for behavioral equivalence with Java implementation
    # TODO: Replace with date-based attribute selector when application supports it
    _DATE_BOX = (By.XPATH, "(//td[@class='fc-widget-content'])[29]")

    # Note Creation Modal Elements
    _CREATE_NOTE = (By.XPATH, "//div[@class='modal-header']")
    _SUMMARY_BOX = (By.XPATH, "//input[@name='name']")

    # TECHNICAL DEBT: Duplicate locator with _EDIT_BUTTON
    # Both create_button and edit_button use same XPath in Java source (lines 49-50, 58-59)
    # This causes ambiguity when both buttons present on page
    # Preserved for behavioral equivalence - consider unique identifiers in application
    _CREATE_BUTTON = (By.XPATH, "//button[@class='btn btn-sm btn-primary']")

    # Note Display Elements
    # TECHNICAL DEBT: Duplicate locator with _SELECT_NOTE
    # Both get_note and select_note use same XPath in Java source (lines 52-53, 73-74)
    _GET_NOTE = (By.XPATH, "//div[@class='o_field_name o_field_type_char']")
    _CREATED_NOTE = (By.CLASS_NAME, "o_field_name")

    # TECHNICAL DEBT: Duplicate locator with _CREATE_BUTTON (see above)
    _EDIT_BUTTON = (By.XPATH, "//button[@class='btn btn-sm btn-primary']")

    # Note Editing Elements
    _EDIT_TEXT = (By.ID, "o_field_input_46")
    _CREATED_MODELE = (By.XPATH, "//div[@class='modal-content']")
    _TAGS_CHECKBOX = (By.ID, "o_field_input_59")

    # Action Buttons
    _SAVE_BUTTON = (By.XPATH, "//span[.='Save']")

    # TECHNICAL DEBT: Duplicate locator with _GET_NOTE (see above)
    _SELECT_NOTE = (By.XPATH, "//div[@class='o_field_name o_field_type_char']")

    # ====================
    # INITIALIZATION
    # ====================

    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize CalendarPage with WebDriver instance.

        Calls BasePage.__init__ to set up driver, wait utilities, configuration,
        and action chains for calendar interactions.

        Args:
            driver: Selenium WebDriver instance for browser automation
                   Expected to be thread-local instance from DriverManager

        Example:
            >>> from utilities.driver_manager import DriverManager
            >>> driver = DriverManager.get_driver()
            >>> calendar_page = CalendarPage(driver)
        """
        super().__init__(driver)

    # ====================
    # ELEMENT PROPERTIES
    # ====================
    # Properties return fresh WebElement references on each access
    # Uses BasePage wait methods to ensure elements are available

    @property
    def title(self) -> WebElement:
        """
        Page title element containing 'Meetings - Odoo'.

        Returns:
            WebElement: Title element when present in DOM

        Raises:
            TimeoutException: If title not found within default timeout
        """
        return self.wait_for_element(self._TITLE)

    @property
    def calendar_button(self) -> WebElement:
        """
        Calendar navigation link for accessing calendar module.

        Use this element to navigate to the calendar/meetings page from other modules.

        Returns:
            WebElement: Clickable calendar navigation link

        Raises:
            TimeoutException: If calendar button not clickable within timeout

        Example:
            >>> calendar_page.calendar_button.click()
        """
        return self.wait_for_clickable(self._CALENDAR_BUTTON)

    @property
    def calendar_module(self) -> WebElement:
        """
        Main calendar container element.

        This element contains the entire calendar interface including view controls,
        date navigation, and calendar grid.

        Returns:
            WebElement: Calendar container when visible

        Raises:
            TimeoutException: If calendar module not visible within timeout
        """
        return self.wait_for_visibility(self._CALENDAR_MODULE)

    @property
    def day(self) -> WebElement:
        """
        Day view button to switch calendar to daily view.

        Returns:
            WebElement: Clickable 'Day' button

        Raises:
            TimeoutException: If day button not clickable within timeout

        Example:
            >>> calendar_page.day.click()  # Switch to day view
        """
        return self.wait_for_clickable(self._DAY_BUTTON)

    @property
    def week(self) -> WebElement:
        """
        Week view button to switch calendar to weekly view.

        Returns:
            WebElement: Clickable 'Week' button

        Raises:
            TimeoutException: If week button not clickable within timeout

        Example:
            >>> calendar_page.week.click()  # Switch to week view
        """
        return self.wait_for_clickable(self._WEEK_BUTTON)

    @property
    def month(self) -> WebElement:
        """
        Month view button to switch calendar to monthly view.

        Returns:
            WebElement: Clickable 'Month' button

        Raises:
            TimeoutException: If month button not clickable within timeout

        Example:
            >>> calendar_page.month.click()  # Switch to month view
        """
        return self.wait_for_clickable(self._MONTH_BUTTON)

    @property
    def day_calendar(self) -> WebElement:
        """
        Current day highlight element in calendar view.

        This element represents the currently selected or highlighted day in the
        calendar interface, typically styled to stand out from other dates.

        Returns:
            WebElement: Highlighted day element

        Raises:
            TimeoutException: If day calendar element not found within timeout
        """
        return self.wait_for_element(self._DAY_CALENDAR)

    @property
    def month_and_year_calendar(self) -> WebElement:
        """
        Current date cell in month/year calendar view.

        Represents the today's date cell with special styling in the calendar grid.
        Used for date selection and current date verification.

        Returns:
            WebElement: Today's date cell element

        Raises:
            TimeoutException: If date cell not found within timeout
        """
        return self.wait_for_element(self._MONTH_AND_YEAR_CALENDAR)

    @property
    def date_actual(self) -> WebElement:
        """
        Currently displayed date information in control panel.

        Shows the current date context (e.g., "Week 45, 2024" or "November 2024")
        depending on the active calendar view (day/week/month).

        Returns:
            WebElement: Date display element in control panel

        Raises:
            TimeoutException: If date element not found within timeout

        Example:
            >>> actual_date = calendar_page.date_actual.text
            >>> assert "2024" in actual_date
        """
        return self.wait_for_element(self._DATE_ACTUAL)

    @property
    def date_box(self) -> WebElement:
        """
        Specific date cell in calendar grid for meeting creation.

        WARNING - TECHNICAL DEBT:
        This locator uses a brittle index-based XPath selector [29] which may break
        if the calendar view changes or DOM structure is modified. This is preserved
        for behavioral equivalence with the Java implementation.

        Consider using date-based attributes (e.g., data-date="2024-11-07") if the
        application provides them for more stable element identification.

        Returns:
            WebElement: Date cell element at position [29]

        Raises:
            TimeoutException: If date box not found within timeout
            NoSuchElementException: If calendar structure changed and index invalid

        Example:
            >>> calendar_page.date_box.click()  # Open meeting creation dialog
        """
        return self.wait_for_clickable(self._DATE_BOX)

    @property
    def create_note(self) -> WebElement:
        """
        Modal header for note/meeting creation dialog.

        This element appears when creating a new meeting or note. Its presence
        indicates the creation modal is displayed.

        Returns:
            WebElement: Modal header element

        Raises:
            TimeoutException: If create note modal not visible within timeout

        Example:
            >>> assert calendar_page.create_note.is_displayed()
        """
        return self.wait_for_visibility(self._CREATE_NOTE)

    @property
    def summary_box(self) -> WebElement:
        """
        Input field for meeting/note summary (name/title).

        Primary input field where users enter the title or summary of a meeting or note.

        Returns:
            WebElement: Summary input field

        Raises:
            TimeoutException: If summary box not found within timeout

        Example:
            >>> calendar_page.summary_box.send_keys("Team Standup Meeting")
        """
        return self.wait_for_element(self._SUMMARY_BOX)

    @property
    def create_button(self) -> WebElement:
        """
        Button to create/save a new meeting or note.

        WARNING - TECHNICAL DEBT - DUPLICATE LOCATOR:
        This property shares the same XPath locator with edit_button:
        xpath='//button[@class="btn btn-sm btn-primary"]'

        If both create and edit buttons are present on the page simultaneously,
        Selenium may return the first matching element, which could be either button.

        This is preserved for behavioral equivalence with Java implementation
        (CalendarP.java lines 49-50 and 58-59 both use identical locators).

        RECOMMENDATION: Application should add unique identifiers:
        - data-testid="create-button" and data-testid="edit-button", OR
        - Unique id attributes for each button

        Returns:
            WebElement: Create button (or first matching primary button)

        Raises:
            TimeoutException: If create button not clickable within timeout

        Example:
            >>> calendar_page.summary_box.send_keys("Meeting")
            >>> calendar_page.create_button.click()
        """
        return self.wait_for_clickable(self._CREATE_BUTTON)

    @property
    def get_note(self) -> WebElement:
        """
        Note field element displaying meeting/note details.

        WARNING - TECHNICAL DEBT - DUPLICATE LOCATOR:
        This property shares the same XPath locator with select_note:
        xpath='//div[@class="o_field_name o_field_type_char"]'

        If multiple note field elements exist, Selenium returns the first match.
        The distinction between get_note and select_note in the Java implementation
        (lines 52-53 and 73-74) is unclear with identical locators.

        RECOMMENDATION: Use more specific locators or add unique attributes to
        distinguish different note field contexts in the application.

        Returns:
            WebElement: Note field element (or first matching field)

        Raises:
            TimeoutException: If note field not found within timeout

        Example:
            >>> note_text = calendar_page.get_note.text
        """
        return self.wait_for_element(self._GET_NOTE)

    @property
    def created_note(self) -> WebElement:
        """
        Display element for created note/meeting name.

        Shows the name/title of a successfully created meeting or note.
        Different from get_note/select_note by using className locator strategy.

        Returns:
            WebElement: Created note display element

        Raises:
            TimeoutException: If created note element not found within timeout

        Example:
            >>> assert "Team Meeting" in calendar_page.created_note.text
        """
        return self.wait_for_element(self._CREATED_NOTE)

    @property
    def edit_button(self) -> WebElement:
        """
        Button to edit an existing meeting or note.

        WARNING - TECHNICAL DEBT - DUPLICATE LOCATOR:
        This property shares the same XPath locator with create_button:
        xpath='//button[@class="btn btn-sm btn-primary"]'

        See create_button property documentation for full details on this issue.
        When both buttons present, Selenium may return either button (first match).

        This duplicate is preserved from Java implementation (CalendarP.java lines
        49-50 for createButton and 58-59 for editButton use identical XPath).

        Returns:
            WebElement: Edit button (or first matching primary button)

        Raises:
            TimeoutException: If edit button not clickable within timeout

        Example:
            >>> calendar_page.edit_button.click()
            >>> calendar_page.edit_text.clear()
            >>> calendar_page.edit_text.send_keys("Updated Meeting Title")
        """
        return self.wait_for_clickable(self._EDIT_BUTTON)

    @property
    def edit_text(self) -> WebElement:
        """
        Text input field for editing meeting/note content.

        This field appears in the edit mode of a meeting or note, allowing users
        to modify the meeting title or description.

        Note: Uses ID locator 'o_field_input_46' which may be dynamically generated.
        If the application uses dynamic IDs, this locator may become unreliable.

        Returns:
            WebElement: Edit text input field

        Raises:
            TimeoutException: If edit text field not found within timeout

        Example:
            >>> calendar_page.edit_text.clear()
            >>> calendar_page.edit_text.send_keys("Updated content")
        """
        return self.wait_for_element(self._EDIT_TEXT)

    @property
    def created_modele(self) -> WebElement:
        """
        Modal content container for created meeting/note.

        This element represents the modal dialog content area that displays
        after creating or opening a meeting/note.

        Returns:
            WebElement: Modal content container

        Raises:
            TimeoutException: If modal content not visible within timeout

        Example:
            >>> assert calendar_page.created_modele.is_displayed()
        """
        return self.wait_for_visibility(self._CREATED_MODELE)

    @property
    def tags_checkbox(self) -> WebElement:
        """
        Checkbox or input for selecting/managing meeting tags.

        Allows users to categorize meetings with tags for organization and filtering.

        Note: Uses ID locator 'o_field_input_59' which may be dynamically generated.
        If the application uses dynamic IDs, this locator may become unreliable.

        Returns:
            WebElement: Tags checkbox/input element

        Raises:
            TimeoutException: If tags checkbox not found within timeout

        Example:
            >>> calendar_page.tags_checkbox.click()
        """
        return self.wait_for_element(self._TAGS_CHECKBOX)

    @property
    def save_button(self) -> WebElement:
        """
        Save button to persist meeting/note changes.

        Finalizes edits or creation of meetings/notes by saving changes to the system.

        Returns:
            WebElement: Clickable save button

        Raises:
            TimeoutException: If save button not clickable within timeout

        Example:
            >>> calendar_page.edit_text.send_keys("Updated")
            >>> calendar_page.save_button.click()
        """
        return self.wait_for_clickable(self._SAVE_BUTTON)

    @property
    def select_note(self) -> WebElement:
        """
        Note selection element for interacting with specific notes.

        WARNING - TECHNICAL DEBT - DUPLICATE LOCATOR:
        This property shares the same XPath locator with get_note:
        xpath='//div[@class="o_field_name o_field_type_char"]'

        See get_note property documentation for full details on this duplication issue.

        Returns:
            WebElement: Note selection element (or first matching field)

        Raises:
            TimeoutException: If select note element not found within timeout
        """
        return self.wait_for_element(self._SELECT_NOTE)


# Module self-test and usage example
if __name__ == "__main__":
    # CalendarPage module self-documentation and usage examples.
    # This section provides usage patterns for the CalendarPage class.
    # Actual test execution should be done through Behave step definitions.
    print("CalendarPage module loaded successfully")
    print("\nPage Object: CalendarPage")
    print("Source: Converted from CalendarP.java (PageFactory pattern)")
    print("\nElement Categories:")
    print("  - Navigation: calendar_button")
    print("  - View Controls: day, week, month")
    print("  - Calendar Display: calendar_module, day_calendar, month_and_year_calendar")
    print("  - Date Selection: date_actual, date_box")
    print("  - Note Management: create_note, summary_box, get_note, select_note, created_note")
    print("  - Action Buttons: create_button, edit_button, save_button")
    print("  - Form Fields: edit_text, tags_checkbox")
    print("  - Modals: created_modele")
    print("\nTechnical Debt Notes:")
    print("  ⚠ Duplicate locators: create_button/edit_button use same XPath")
    print("  ⚠ Duplicate locators: get_note/select_note use same XPath")
    print("  ⚠ Brittle locator: date_box uses index-based XPath [29]")
    print("\nUsage Example:")
    print("""
    from utilities.driver_manager import DriverManager
    from pages.calendar_page import CalendarPage

    # Get thread-local driver instance
    driver = DriverManager.get_driver()

    # Initialize page object
    calendar_page = CalendarPage(driver)

    # Navigate to calendar module
    calendar_page.calendar_button.click()

    # Switch to day view
    calendar_page.day.click()

    # Create a new meeting
    calendar_page.date_box.click()
    calendar_page.summary_box.send_keys("Team Standup")
    calendar_page.create_button.click()

    # Verify creation
    assert "Team Standup" in calendar_page.created_note.text
    """)
