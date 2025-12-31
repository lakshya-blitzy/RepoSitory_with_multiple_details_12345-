package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object class representing the Meetings/Calendar module in Odoo ERP application.
 * 
 * <p>This class follows the Page Object Model (POM) design pattern, encapsulating all web elements
 * and their locators for the Calendar/Meetings module. The POM pattern improves test maintenance
 * by centralizing element locators and providing a clear separation between test logic and page structure.</p>
 * 
 * <p>URL Pattern: This page is typically accessed via {@code /web#action=calendar_action&...} or through
 * the Calendar navigation link in the Odoo main menu.</p>
 * 
 * <p>All WebElement fields in this class are initialized via 
 * {@code PageFactory.initElements(Driver.getDriver(), this)} in the constructor. The PageFactory
 * uses lazy initialization - elements are located in the DOM only when first accessed, not at
 * instantiation time.</p>
 * 
 * <p>This class contains locators for:</p>
 * <ul>
 *   <li>Calendar navigation and module container elements</li>
 *   <li>View toggle buttons (Day/Week/Month)</li>
 *   <li>Date picker components (current day, month/year display)</li>
 *   <li>Calendar grid cells for date selection</li>
 *   <li>Modal dialogs for event/note creation and editing</li>
 *   <li>Form input fields (summary, tags, text)</li>
 *   <li>Action buttons (Create, Edit, Save)</li>
 * </ul>
 * 
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.PageFactory
 * @see org.openqa.selenium.support.FindBy
 */
public class CalendarP {
    
    /**
     * Constructs a new CalendarP Page Object instance.
     * 
     * <p>This no-argument constructor initializes all {@link FindBy} annotated WebElement fields
     * using Selenium's PageFactory. The {@code PageFactory.initElements} method binds all locators
     * to the active WebDriver instance obtained from {@link Driver#getDriver()}.</p>
     * 
     * <p>Note: PageFactory uses lazy initialization - WebElements are proxy objects that only
     * locate the actual DOM elements when first accessed (e.g., when calling {@code click()},
     * {@code sendKeys()}, or {@code getText()}). This means element lookup errors occur at
     * usage time, not at construction time.</p>
     * 
     * @see PageFactory#initElements(org.openqa.selenium.WebDriver, Object)
     * @see Driver#getDriver()
     */
    public CalendarP(){
        PageFactory.initElements(Driver.getDriver(),this);
    }

    /**
     * WebElement for the page title element matching "Meetings - Odoo".
     * 
     * <p>Locator Strategy: XPath targeting {@code <title>} element with exact text content.</p>
     * <p>Usage: Used for page verification to confirm navigation to the Meetings/Calendar page.</p>
     * 
     * <p><strong>Stability Note:</strong> XPath targeting {@code <title>} elements may not work
     * as expected in all browsers since the title element is in the document head, not the body.
     * Consider using {@code driver.getTitle()} method instead for title verification.</p>
     */
    @FindBy(xpath = "//title[.='Meetings - Odoo']" )
    public WebElement title;

    /**
     * WebElement for the Calendar module navigation link.
     * 
     * <p>Locator Strategy: Partial link text matching "Calendar".</p>
     * <p>Usage: Used to navigate to the Calendar view from other Odoo modules via the main menu
     * or sidebar navigation.</p>
     */
    @FindBy(partialLinkText = "Calendar")
    public WebElement calendarButton;

    /**
     * WebElement for the main calendar container element.
     * 
     * <p>Locator Strategy: CSS class name {@code o_calendar_container}.</p>
     * <p>Usage: Used to verify that the Calendar module has fully loaded and is visible
     * on the page. This container wraps all calendar-related UI components.</p>
     */
    @FindBy(className = "o_calendar_container")
    public WebElement calendarModule;

    /**
     * WebElement for the Day view toggle button.
     * 
     * <p>Locator Strategy: XPath targeting button element with exact text "Day".</p>
     * <p>Usage: Clicks this button to switch the calendar to single-day view display,
     * showing detailed hourly slots for the selected date.</p>
     */
    @FindBy(xpath = "//button[.='Day']")
    public WebElement day;

    /**
     * WebElement for the Week view toggle button.
     * 
     * <p>Locator Strategy: XPath targeting button element with exact text "Week".</p>
     * <p>Usage: Clicks this button to switch the calendar to week view display,
     * showing all seven days of the current week with their events.</p>
     */
    @FindBy(xpath = "//button[.='Week']")
    public WebElement week;

    /**
     * WebElement for the Month view toggle button.
     * 
     * <p>Locator Strategy: XPath targeting button element with exact text "Month".</p>
     * <p>Usage: Clicks this button to switch the calendar to month view display,
     * showing the full monthly calendar grid with all events.</p>
     */
    @FindBy(xpath = "//button[.='Month']")
    public WebElement month;

    /**
     * WebElement for the highlighted/current day in the date picker widget.
     * 
     * <p>Locator Strategy: CSS class name {@code ui-state-highlight}.</p>
     * <p>Usage: Identifies and interacts with the currently highlighted day in the jQuery UI
     * datepicker widget. This is typically today's date or the currently selected date.</p>
     * 
     * <p>Note: Uses jQuery UI datepicker CSS class conventions.</p>
     */
    @FindBy(className= "ui-state-highlight")
    public WebElement dayCalendar;

    /**
     * WebElement for the current day cell in the date picker with multiple state classes.
     * 
     * <p>Locator Strategy: Complex XPath targeting {@code <td>} element with multiple
     * space-separated class names including {@code ui-datepicker-days-cell-over},
     * {@code ui-datepicker-current-day}, and {@code ui-datepicker-today}.</p>
     * <p>Usage: Locates the cell representing today's date in the date picker when it has
     * hover, current, and today states simultaneously.</p>
     * 
     * <p><strong>Stability Concern:</strong> This locator is brittle as it relies on the exact
     * class attribute string with specific spacing. Class order changes or additional classes
     * added by Odoo updates may break this locator. Consider using CSS selector with
     * {@code contains(@class, 'ui-datepicker-today')} for more resilient matching.</p>
     */
    @FindBy(xpath = "//td[@class=' ui-datepicker-days-cell-over  ui-datepicker-current-day ui-datepicker-today']")
    public WebElement monthAndYearCalendar;

    /**
     * WebElement for the breadcrumb date display element in the control panel.
     * 
     * <p>Locator Strategy: XPath targeting list item ({@code <li>}) inside the ordered list
     * ({@code <ol>}) within the control panel div ({@code o_control_panel}).</p>
     * <p>Usage: Displays and retrieves the current calendar date context shown in the
     * breadcrumb navigation area. Used to verify the currently displayed date/period.</p>
     */
    @FindBy(xpath = "//div[@class='o_control_panel']/ol/li")
    public WebElement dateActual;

    /**
     * WebElement for a specific calendar grid cell at position 29.
     * 
     * <p>Locator Strategy: Indexed XPath targeting the 29th table cell ({@code <td>})
     * with class {@code fc-widget-content} in the FullCalendar grid.</p>
     * <p>Usage: Clicks on this specific calendar cell to select a date or create an event.
     * Position 29 typically represents a date in the middle of a month view.</p>
     * 
     * <p><strong>Stability Concern:</strong> This locator uses an absolute positional index [29]
     * which is highly fragile. The index position will correspond to different dates depending
     * on the current month and how the calendar grid is rendered. Consider using dynamic
     * locators based on date attributes or data values instead.</p>
     */
    @FindBy(xpath = "(//td[@class='fc-widget-content'])[29]")
    public WebElement dateBox;

    /**
     * WebElement for the modal dialog header element.
     * 
     * <p>Locator Strategy: XPath targeting {@code <div>} element with class {@code modal-header}.</p>
     * <p>Usage: Used to verify that the event/note creation modal dialog has opened successfully.
     * The presence of this element indicates the modal is displayed.</p>
     */
    @FindBy(xpath = "//div[@class='modal-header']")
    public WebElement createNote;

    /**
     * WebElement for the event summary/name input field.
     * 
     * <p>Locator Strategy: XPath targeting {@code <input>} element with {@code name="name"}
     * attribute.</p>
     * <p>Usage: Used for entering the event title/summary text when creating or editing
     * a calendar event or meeting. This is typically the main text field in the event form.</p>
     */
    @FindBy(xpath = "//input[@name='name']")
    public WebElement summaryBox;

    /**
     * WebElement for the primary Create action button in the modal dialog.
     * 
     * <p>Locator Strategy: XPath targeting {@code <button>} element with Bootstrap classes
     * {@code btn btn-sm btn-primary}.</p>
     * <p>Usage: Clicks this button to create/save a new calendar event or note.</p>
     * 
     * <p><strong>Note:</strong> This locator uses generic Bootstrap primary button classes
     * which may match multiple buttons on the page. The same XPath is shared with
     * {@link #editButton}. Test code must ensure proper modal context before clicking.</p>
     * 
     * @see #editButton
     */
    @FindBy(xpath= "//button[@class='btn btn-sm btn-primary']")
    public WebElement createButton;

    /**
     * WebElement for displaying created note content.
     * 
     * <p>Locator Strategy: XPath targeting {@code <div>} element with Odoo field classes
     * {@code o_field_name o_field_type_char}.</p>
     * <p>Usage: Retrieves and displays the content of a created note/event. Used for
     * verification after note creation.</p>
     * 
     * <p><strong>Note:</strong> This locator has the same XPath as {@link #selectNote}.
     * Consider consolidating these fields if they serve the same purpose.</p>
     * 
     * @see #selectNote
     * @see #createdNote
     */
    @FindBy(xpath = "//div[@class='o_field_name o_field_type_char']")
    public WebElement getNote;

    /**
     * WebElement for the note name field display using class-based locator.
     * 
     * <p>Locator Strategy: CSS class name {@code o_field_name}.</p>
     * <p>Usage: Alternative locator for accessing note/event name display. This locator
     * is less specific than {@link #getNote} and may match multiple elements.</p>
     * 
     * <p><strong>Note:</strong> This element serves a similar purpose to {@link #getNote}.
     * The class-only selector may be less reliable in contexts with multiple name fields.</p>
     * 
     * @see #getNote
     */
    @FindBy(className = "o_field_name")
    public WebElement createdNote;

    /**
     * WebElement for the Edit action button.
     * 
     * <p>Locator Strategy: XPath targeting {@code <button>} element with Bootstrap classes
     * {@code btn btn-sm btn-primary}.</p>
     * <p>Usage: Clicks this button to enter edit mode for an existing calendar event or note.</p>
     * 
     * <p><strong>Note:</strong> This locator uses an identical XPath selector to {@link #createButton}.
     * The same DOM element may be matched by either field depending on the current modal state
     * (create vs. edit mode). Consumer code must disambiguate by UI context - the button text
     * changes between "Create" and "Edit" but the locator matches the element by class only.</p>
     * 
     * @see #createButton
     */
    @FindBy(xpath = "//button[@class='btn btn-sm btn-primary']")
    public WebElement editButton;

    /**
     * WebElement for the text input field during edit mode.
     * 
     * <p>Locator Strategy: Element ID {@code o_field_input_46}.</p>
     * <p>Usage: Used for entering or modifying text content when editing an existing
     * calendar event or note.</p>
     * 
     * <p><strong>Stability Concern:</strong> This locator uses a generated numeric ID
     * ({@code o_field_input_46}) which is dynamically assigned by Odoo. This ID may change
     * across different Odoo versions, page reloads, or when the form field order changes.
     * Consider using a more stable locator strategy such as {@code name} attribute or
     * a relative XPath based on field labels.</p>
     */
    @FindBy(id = "o_field_input_46")
    public WebElement editText;

    /**
     * WebElement for the modal dialog content container.
     * 
     * <p>Locator Strategy: XPath targeting {@code <div>} element with class {@code modal-content}.</p>
     * <p>Usage: Used to verify that a modal dialog is visible and to interact with modal
     * content. This Bootstrap class wraps the entire modal body including header, body, and footer.</p>
     */
    @FindBy(xpath = "//div[@class='modal-content']")
    public WebElement createdModele;

    /**
     * WebElement for the tags input field or checkbox.
     * 
     * <p>Locator Strategy: Element ID {@code o_field_input_59}.</p>
     * <p>Usage: Used for selecting or entering tags when creating or editing calendar events.
     * May function as a checkbox, input field, or multi-select depending on the Odoo field configuration.</p>
     * 
     * <p><strong>Stability Concern:</strong> This locator uses a generated numeric ID
     * ({@code o_field_input_59}) which is dynamically assigned by Odoo. This ID is brittle
     * and may change across Odoo versions or when form fields are reordered. Consider using
     * a more stable locator based on field name or label text.</p>
     */
    @FindBy(id = "o_field_input_59")
    public WebElement tagsCheckbox;

    /**
     * WebElement for the Save button.
     * 
     * <p>Locator Strategy: XPath targeting {@code <span>} element with exact text "Save".</p>
     * <p>Usage: Clicks this button to save changes made to a calendar event or note during
     * edit mode. Triggers form submission and persists the modifications.</p>
     */
    @FindBy(xpath = "//span[.='Save']")
    public WebElement saveButton;

    /**
     * WebElement for selecting/clicking on a note element.
     * 
     * <p>Locator Strategy: XPath targeting {@code <div>} element with Odoo field classes
     * {@code o_field_name o_field_type_char}.</p>
     * <p>Usage: Used for selecting a note element to view its details or initiate editing.</p>
     * 
     * <p><strong>Note:</strong> This locator has an identical XPath selector to {@link #getNote}.
     * These appear to be duplicate locators for the same element. Consider consolidating
     * into a single WebElement field to reduce redundancy and improve maintainability.</p>
     * 
     * @see #getNote
     */
    @FindBy(xpath = "//div[@class='o_field_name o_field_type_char']")
    public WebElement selectNote;

}
