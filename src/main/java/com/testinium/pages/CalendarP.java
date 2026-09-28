package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object (POM element container) for the Calendar (Meetings) module of the Odoo/Upgenix ERP under test.
 *
 * <p>Each {@code public} {@code WebElement} field is annotated with {@code @FindBy} and bound by Selenium
 * {@code PageFactory} to a lazy proxy, so the element is located in the current DOM only when the field is used.
 * The step definitions in {@code com.testinium.step_definitions.Calendar} construct this class and drive its
 * elements; the class itself contains no waits or assertions.
 */
public class CalendarP {
    /**
     * Creates the page and initializes its {@code @FindBy} proxies by calling
     * {@code PageFactory.initElements(Driver.getDriver(), this)}.
     *
     * <p>{@link com.testinium.utilities.Driver#getDriver()} creates, or reuses, the current thread's
     * {@code WebDriver}, choosing the browser from the {@code browser} configuration key. Step classes
     * construct pages in field initializers, so constructing a page starts the browser if this thread has none yet.
     */
    public CalendarP(){
        PageFactory.initElements(Driver.getDriver(),this);
    }

    /** Document {@code <title>} element whose text is "Meetings - Odoo", identifying the Calendar page; not referenced by the current step definitions. */
    @FindBy(xpath = "//title[.='Meetings - Odoo']" )
    public WebElement title;

    /** Calendar link in the main menu, located by partial link text; clicked to open the Calendar module. */
    @FindBy(partialLinkText = "Calendar")
    public WebElement calendarButton;

    /** Calendar view container ({@code o_calendar_container}), awaited to confirm the module has loaded. */
    @FindBy(className = "o_calendar_container")
    public WebElement calendarModule;

    /** Day view button of the calendar toolbar. */
    @FindBy(xpath = "//button[.='Day']")
    public WebElement day;

    /** Week view button of the calendar toolbar. */
    @FindBy(xpath = "//button[.='Week']")
    public WebElement week;

    /** Month view button of the calendar toolbar. */
    @FindBy(xpath = "//button[.='Month']")
    public WebElement month;

    /** Highlighted current day in the side date picker ({@code ui-state-highlight}); its text is the day of month. */
    @FindBy(className= "ui-state-highlight")
    public WebElement dayCalendar;

    /** Current-day cell of the side date picker; step definitions read its zero-based {@code data-month} and {@code data-year} attributes. The locator matches the exact {@code class} attribute string, so it is fragile. */
    @FindBy(xpath = "//td[@class=' ui-datepicker-days-cell-over  ui-datepicker-current-day ui-datepicker-today']")
    public WebElement monthAndYearCalendar;

    /** Control-panel breadcrumb showing the currently displayed date or date range. */
    @FindBy(xpath = "//div[@class='o_control_panel']/ol/li")
    public WebElement dateActual;

    /** Calendar grid cell selected by a fixed index (the 29th {@code fc-widget-content} cell). Fragile: the cell it matches depends on the rendered layout. */
    @FindBy(xpath = "(//td[@class='fc-widget-content'])[29]")
    public WebElement dateBox;

    /** Header of the quick-create modal that opens after clicking a grid cell. */
    @FindBy(xpath = "//div[@class='modal-header']")
    public WebElement createNote;

    /** Event summary input ({@code name="name"}) in the quick-create modal. */
    @FindBy(xpath = "//input[@name='name']")
    public WebElement summaryBox;

    /** Primary Create button of the quick-create modal. Shares its locator with {@link #editButton}. */
    @FindBy(xpath= "//button[@class='btn btn-sm btn-primary']")
    public WebElement createButton;

    /** Name field of the created event, read to verify the entered summary. Same locator as {@link #selectNote}. */
    @FindBy(xpath = "//div[@class='o_field_name o_field_type_char']")
    public WebElement getNote;

    /** Name field ({@code o_field_name}) of the created event, checked for visibility. */
    @FindBy(className = "o_field_name")
    public WebElement createdNote;

    /** Primary modal button clicked to edit an event. Same locator as {@link #createButton}, so the match depends on which modal is open. */
    @FindBy(xpath = "//button[@class='btn btn-sm btn-primary']")
    public WebElement editButton;

    /** Event name input in edit mode, located by the generated id {@code o_field_input_46}. Fragile: generated ids can change between page loads or releases. */
    @FindBy(id = "o_field_input_46")
    public WebElement editText;

    /** Content container of the event modal shown after selecting a created event, checked for visibility. */
    @FindBy(xpath = "//div[@class='modal-content']")
    public WebElement createdModele;

    /** Checkbox field in the event form, located by the generated id {@code o_field_input_59}. Fragile: generated ids can change; its selection state is read but not asserted by the step definitions. */
    @FindBy(id = "o_field_input_59")
    public WebElement tagsCheckbox;

    /** Save button of the event form (span text "Save"). */
    @FindBy(xpath = "//span[.='Save']")
    public WebElement saveButton;

    /** Created event entry clicked to open it. Same locator as {@link #getNote}. */
    @FindBy(xpath = "//div[@class='o_field_name o_field_type_char']")
    public WebElement selectNote;

}
