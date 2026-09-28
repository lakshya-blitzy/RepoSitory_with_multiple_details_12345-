package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import java.util.List;


/**
 * Page Object (POM element container) for the Sales / Customers screens of the Odoo/Upgenix ERP under test.
 *
 * <p>Each {@code public} {@code WebElement} field (and the {@code List<WebElement>} {@link #allCustomers}) is annotated
 * with {@code @FindBy} and bound by Selenium {@code PageFactory} to a lazy proxy, so elements are located in the
 * current DOM only when the field is used. The step definitions in {@code com.testinium.step_definitions.Sales}
 * construct this class and drive its elements; the class itself contains no waits or assertions. Many form inputs
 * are located by generated field ids and break when the form layout changes.
 */
public class SalesP {

    /**
     * Creates the page and initializes its {@code @FindBy} proxies by calling
     * {@code PageFactory.initElements(Driver.getDriver(), this)}.
     *
     * <p>{@link com.testinium.utilities.Driver#getDriver()} creates, or reuses, the current thread's
     * {@code WebDriver}, choosing the browser from the {@code browser} configuration key. Step classes
     * construct pages in field initializers, so constructing a page starts the browser if this thread has none yet.
     */
    public SalesP(){
        PageFactory.initElements(Driver.getDriver(),this);
    }

    /** Sales link in the main menu, located by partial link text. */
    @FindBy(partialLinkText = "Sales")
    public WebElement salesPartial;

    /** Customers menu entry (label span), located by a hard-coded menu/action href. */
    @FindBy(xpath  = "//a[@href='/web#menu_id=447&action=48']/span")
    public WebElement customersButton;

    /** Kanban Create button of the Customers view. */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o-kanban-button-new btn-default']")
    public WebElement createButton;

    /** Customer name field on the create form, located by the generated id {@code o_field_input_470}; fragile. */
    @FindBy(xpath ="//input[@id='o_field_input_470']" )
    public WebElement customerName;

    /** Street address field on the create form (generated id {@code o_field_input_474}). */
    @FindBy(xpath = "//input[@id='o_field_input_474']")
    public WebElement address;

    /** State selection field on the create form (generated id {@code o_field_input_477}). */
    @FindBy(xpath = "//input[@id='o_field_input_477']")
    public WebElement stateOptions;

    /** "Create and Edit..." entry of the State drop-down, which opens the state-create dialog. */
    @FindBy(xpath = "//li[.='Create and Edit...']")
    public WebElement createAndEditState;

    /** State name input in the state-create dialog (generated id {@code o_field_input_516}). */
    @FindBy(xpath = "//input[@id='o_field_input_516']")
    public WebElement stateName;

    /** State code input in the state-create dialog (generated id {@code o_field_input_517}). */
    @FindBy(xpath = "//input[@id='o_field_input_517']")
    public WebElement stateCode;

    /** Country input in the state-create dialog (generated id {@code o_field_input_518}). */
    @FindBy(xpath = "//input[@id='o_field_input_518']")
    public  WebElement countryStateButton;

    /** Country option in the autocomplete list, located by the generated id {@code ui-id-30}; fragile. */
    @FindBy(xpath = "//li[@id='ui-id-30']/a")
    public  WebElement countrySelection;

    /** Save button (label span) of the state-create dialog. */
    @FindBy(xpath = "//button[@class='btn btn-sm btn-primary']/span")
    public  WebElement saveButton;

    /** Form Save button ({@code o_form_button_save}) that saves the new customer. */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']")
    public WebElement createCustomer;

    /** Search view input used to find a customer by name. */
    @FindBy(xpath = "//div[@class='o_searchview']/input")
    public WebElement searchBar;

    /** Title of a customer kanban card, read after searching. */
    @FindBy(xpath = "//strong[@class='o_kanban_record_title oe_partner_heading']/span")
    public WebElement nameCheck;

    /** Primary button of a modal dialog; not referenced by the current step definitions. */
    @FindBy(xpath = "//button[@class='btn btn-sm btn-primary']")
    public WebElement warningButton;

    /** Notification manager container whose text is read as the validation warning. */
    @FindBy(xpath = "//div[@class='o_notification_manager']")
    public WebElement warning;

    /** All customer kanban cards on the Customers view, as a {@code List<WebElement>}; not referenced by the current step definitions. */
    @FindBy(xpath = "//div[@class='oe_kanban_global_click o_res_partner_kanban o_kanban_record']")
    public List<WebElement> allCustomers;

    /** Customers menu anchor with the same hard-coded href as {@link #customersButton}; not referenced by the current step definitions. */
    @FindBy(xpath = "//a[@href='/web#menu_id=447&action=48']")
    public WebElement link;

    /** Detail text span inside a customer kanban card; not referenced by the current step definitions. */
    @FindBy(xpath = "//div[@class=\"oe_kanban_details\"]//span")
    public WebElement details;


}
