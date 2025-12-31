package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import java.util.List;

/**
 * Page Object class representing the Sales/Customers module in the Odoo application.
 * 
 * <p>This class provides locators for customer management operations including:
 * <ul>
 *   <li>Module navigation (Sales menu, Customers submenu)</li>
 *   <li>Customer creation workflow (create button, form fields)</li>
 *   <li>Address and state configuration (state dropdown, state creation dialog)</li>
 *   <li>Search functionality (search bar for filtering customers)</li>
 *   <li>Kanban card interactions (customer cards, details, verification)</li>
 * </ul>
 * 
 * <p>This class contains a {@link java.util.List} of {@link WebElement} ({@code allCustomers})
 * which enables iteration over multiple customer kanban cards for count verification or
 * specific card selection by index/content.
 * 
 * <p>Follows the Page Object Model (POM) design pattern, encapsulating page element
 * locators and providing a clean interface for test step definitions to interact
 * with the Sales/Customers module.
 * 
 * <p><strong>Stability Concern:</strong> Many locators in this class use generated numeric IDs
 * (e.g., {@code o_field_input_470}, {@code o_field_input_474}) and hard-coded menu/action IDs
 * (e.g., {@code menu_id=447&action=48}) that may change across Odoo versions, sessions,
 * or different environments. These locators should be monitored and updated as needed.
 * 
 * <p>All WebElement fields in this class are initialized via
 * {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)} using the
 * WebDriver instance obtained from {@link Driver#getDriver()}.
 * 
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.PageFactory
 * @see java.util.List
 */
public class SalesP {

    /**
     * Constructs a new SalesP Page Object and initializes all WebElement fields.
     * 
     * <p>This no-argument constructor initializes all {@link FindBy} annotated
     * WebElement fields using Selenium's {@link PageFactory}. The initialization
     * binds the locators to the active WebDriver instance obtained from
     * {@link Driver#getDriver()}.
     * 
     * <p>Note: This also initializes {@link java.util.List} of WebElement fields
     * (such as {@code allCustomers}), which will find all matching elements
     * when accessed.
     * 
     * @see PageFactory#initElements(org.openqa.selenium.WebDriver, Object)
     * @see Driver#getDriver()
     */
    public SalesP(){
        PageFactory.initElements(Driver.getDriver(),this);
    }

    /**
     * Partial link text locator for Sales module navigation.
     * 
     * <p>Used to navigate to the Sales module from the main menu by matching
     * any link containing "Sales" in its text.
     */
    @FindBy(partialLinkText = "Sales")
    public WebElement salesPartial;

    /**
     * XPath locator for the Customers submenu link with span child element.
     * 
     * <p>Used to navigate to the Customers section within the Sales module.
     * 
     * <p><strong>Stability Concern:</strong> Uses hard-coded menu_id=447 and action=48
     * which will break if Odoo menu IDs change in different environments or versions.
     */
    @FindBy(xpath  = "//a[@href='/web#menu_id=447&action=48']/span")
    public WebElement customersButton;

    /**
     * Class-based XPath locator for the kanban Create button.
     * 
     * <p>Uses the {@code o-kanban-button-new} class to identify the button.
     * Used to initiate new customer creation from the Customers kanban view.
     */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o-kanban-button-new btn-default']")
    public WebElement createButton;

    /**
     * ID-based XPath locator for the customer name input field.
     * 
     * <p>Used to enter the customer name when creating a new customer.
     * 
     * <p><strong>Stability Concern:</strong> Uses generated numeric ID
     * ({@code o_field_input_470}) which may vary across sessions,
     * environments, or Odoo versions.
     */
    @FindBy(xpath ="//input[@id='o_field_input_470']" )
    public WebElement customerName;

    /**
     * ID-based XPath locator for the address input field.
     * 
     * <p>Used to enter the customer street address.
     * 
     * <p><strong>Stability Concern:</strong> Uses generated numeric ID
     * ({@code o_field_input_474}) which may vary across sessions,
     * environments, or Odoo versions.
     */
    @FindBy(xpath = "//input[@id='o_field_input_474']")
    public WebElement address;

    /**
     * ID-based XPath locator for the state dropdown/autocomplete input.
     * 
     * <p>Used to select or create a customer state/province. Triggers an
     * autocomplete dropdown when text is entered.
     * 
     * <p><strong>Stability Concern:</strong> Uses generated numeric ID
     * ({@code o_field_input_477}) which may vary across sessions,
     * environments, or Odoo versions.
     */
    @FindBy(xpath = "//input[@id='o_field_input_477']")
    public WebElement stateOptions;

    /**
     * XPath locator for the "Create and Edit..." dropdown option by exact text.
     * 
     * <p>Used to open the full state creation dialog instead of quick create.
     * This option appears in the state dropdown when no matching state is found.
     */
    @FindBy(xpath = "//li[.='Create and Edit...']")
    public WebElement createAndEditState;

    /**
     * ID-based XPath locator for the state name input in the state creation dialog.
     * 
     * <p>Used to enter the full state name when creating a new state record.
     * 
     * <p><strong>Stability Concern:</strong> Uses generated numeric ID
     * ({@code o_field_input_516}) which may vary across sessions,
     * environments, or Odoo versions.
     */
    @FindBy(xpath = "//input[@id='o_field_input_516']")
    public WebElement stateName;

    /**
     * ID-based XPath locator for the state code input.
     * 
     * <p>Used to enter the state abbreviation (e.g., "CA" for California)
     * when creating a new state record.
     * 
     * <p><strong>Stability Concern:</strong> Uses generated numeric ID
     * ({@code o_field_input_517}) which may vary across sessions,
     * environments, or Odoo versions.
     */
    @FindBy(xpath = "//input[@id='o_field_input_517']")
    public WebElement stateCode;

    /**
     * ID-based XPath locator for the country selector in the state creation dialog.
     * 
     * <p>Used to select the country associated with the state being created.
     * 
     * <p><strong>Stability Concern:</strong> Uses generated numeric ID
     * ({@code o_field_input_518}) which may vary across sessions,
     * environments, or Odoo versions.
     */
    @FindBy(xpath = "//input[@id='o_field_input_518']")
    public  WebElement countryStateButton;

    /**
     * ID-based XPath locator for a country option in the dropdown.
     * 
     * <p>Used to select a specific country from the country autocomplete dropdown.
     * 
     * <p><strong>Stability Concern:</strong> Uses fixed {@code ui-id-30} which is
     * specific to dropdown option position. Will break if the country list order
     * changes or the target country moves to a different position.
     */
    @FindBy(xpath = "//li[@id='ui-id-30']/a")
    public  WebElement countrySelection;

    /**
     * Class-based XPath locator for the Save button span within modal dialog.
     * 
     * <p>Uses {@code btn-primary} styling to identify the primary action button.
     * Used to save state creation in the modal dialog.
     */
    @FindBy(xpath = "//button[@class='btn btn-sm btn-primary']/span")
    public  WebElement saveButton;

    /**
     * Class-based XPath locator for the main form Save button.
     * 
     * <p>Uses the {@code o_form_button_save} class to identify the button.
     * Used to save a new customer record after filling in the form fields.
     */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']")
    public WebElement createCustomer;

    /**
     * XPath locator for the search bar input in the searchview container.
     * 
     * <p>Used for filtering customers by name or other criteria in the
     * Customers kanban/list view.
     */
    @FindBy(xpath = "//div[@class='o_searchview']/input")
    public WebElement searchBar;

    /**
     * Class-based XPath locator for customer name display in kanban card.
     * 
     * <p>Uses {@code o_kanban_record_title} and {@code oe_partner_heading} classes
     * to identify the customer name element. Used to verify customer name
     * after creation or search operations.
     */
    @FindBy(xpath = "//strong[@class='o_kanban_record_title oe_partner_heading']/span")
    public WebElement nameCheck;

    /**
     * Class-based XPath locator for the primary action button in warning dialog.
     * 
     * <p>Used to dismiss or confirm warning messages that appear during
     * customer management operations.
     */
    @FindBy(xpath = "//button[@class='btn btn-sm btn-primary']")
    public WebElement warningButton;

    /**
     * Class-based XPath locator for the notification manager container.
     * 
     * <p>Used to detect and verify validation errors, warnings, or success
     * messages displayed by Odoo's notification system.
     */
    @FindBy(xpath = "//div[@class='o_notification_manager']")
    public WebElement warning;

    /**
     * XPath-based List locator for ALL customer kanban cards matching the selector.
     * 
     * <p>Uses the {@code o_res_partner_kanban} class with global click handler
     * to identify all customer cards in the kanban view.
     * 
     * <p>Returns a list of WebElements enabling iteration over multiple customers.
     * Useful for:
     * <ul>
     *   <li>Verifying customer count after operations</li>
     *   <li>Selecting a specific customer card by index</li>
     *   <li>Iterating through cards to find one with specific content</li>
     * </ul>
     */
    @FindBy(xpath = "//div[@class='oe_kanban_global_click o_res_partner_kanban o_kanban_record']")
    public List<WebElement> allCustomers;

    /**
     * XPath locator for the customers link by exact href attribute.
     * 
     * <p>Similar to {@link #customersButton} but without the span child element.
     * Used as an alternative navigation path to the Customers section.
     * 
     * <p><strong>Stability Concern:</strong> Uses hard-coded menu_id=447 and action=48
     * which will break if Odoo menu IDs change in different environments or versions.
     */
    @FindBy(xpath = "//a[@href='/web#menu_id=447&action=48']")
    public WebElement link;

    /**
     * XPath locator for customer details span within kanban card.
     * 
     * <p>Used to access additional customer information displayed on the
     * kanban card, such as contact details or address information.
     */
    @FindBy(xpath = "//div[@class=\"oe_kanban_details\"]//span")
    public WebElement details;


}
