package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object class representing the CRM (Customer Relationship Management) pipeline module in Odoo.
 * 
 * <p>This class provides locators and WebElement references for CRM operations including:
 * <ul>
 *   <li>Pipeline management and navigation</li>
 *   <li>Opportunity and lead creation</li>
 *   <li>Customer management and lookup</li>
 *   <li>Expected revenue tracking</li>
 *   <li>Priority settings for opportunities</li>
 *   <li>Kanban card interactions</li>
 * </ul>
 * 
 * <p>This class follows the Page Object Model (POM) design pattern, encapsulating all UI element
 * locators for the CRM module in a single class. This promotes code reusability and maintainability
 * by separating page structure from test logic.
 * 
 * <p><strong>Locator Strategy Notes:</strong>
 * <ul>
 *   <li>Contains locators with fixed data-id attributes for kanban cards (data-id='1', data-id='2')</li>
 *   <li>Uses hard-coded menu_id and action values for sidebar navigation URLs</li>
 *   <li>Some locators use accesskey attributes for button identification</li>
 * </ul>
 * 
 * <p><strong>Stability Concerns:</strong>
 * <ul>
 *   <li>Many locators use generated numeric IDs (e.g., o_field_input_125, o_field_input_127) 
 *       that may break across Odoo versions or after database resets</li>
 *   <li>Hard-coded navigation URLs with menu_id and action values are version-specific</li>
 *   <li>Some locators contain hard-coded test data values (e.g., '&amp;CC' customer name)</li>
 *   <li>Absolute XPath locators are extremely brittle and will break with DOM structure changes</li>
 * </ul>
 * 
 * <p>All WebElement fields are initialized via {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)}
 * using the WebDriver instance obtained from {@link Driver#getDriver()}.
 * 
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.PageFactory
 */
public class CrmP {

    /**
     * Constructs a new CrmP Page Object and initializes all WebElement fields.
     * 
     * <p>This no-argument constructor initializes all {@link FindBy} annotated WebElement fields
     * by calling {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)}.
     * The PageFactory binds each locator annotation to the active WebDriver instance
     * obtained from {@link Driver#getDriver()}.
     * 
     * <p>After construction, all WebElement fields are ready for interaction without
     * requiring explicit element lookups.
     */
    public CrmP(){
        PageFactory.initElements(Driver.getDriver(),this);
    }

    /**
     * Link element for navigating to the CRM module from the main menu.
     * 
     * <p>Uses partial link text locator strategy to match any link containing "CRM".
     * This element is typically found in the main application menu or navigation bar.
     */
    @FindBy(partialLinkText = "CRM")
    public WebElement crmLink;

    /**
     * Create button element for initiating new opportunity creation.
     * 
     * <p>Uses XPath locator targeting the button with accesskey='c'. The accesskey
     * attribute provides keyboard shortcut support (Alt+C on most browsers).
     * This button opens the opportunity creation form/dialog.
     */
    @FindBy(xpath = "//button[@accesskey='c']")
    public WebElement createButton;

    /**
     * Input field for entering the opportunity or lead title/name.
     * 
     * <p>Uses name attribute locator strategy. This is the primary identifier
     * field for new opportunities in the CRM module.
     */
    @FindBy(name = "name")
    public  WebElement opportunityTitle;

    /**
     * Customer lookup input field within the grouped table structure.
     * 
     * <p>Uses complex XPath targeting an input within nested table/div elements.
     * This field provides autocomplete functionality for selecting existing customers.
     * 
     * <p><strong>Stability Concern:</strong> This locator relies on a specific nested
     * table/div structure (o_group o_inner_group o_group_col_6) which may change
     * with Odoo UI updates.
     */
    @FindBy(xpath = "//table[@class='o_group o_inner_group o_group_col_6']//div//div//input")
    public WebElement customer;

    /**
     * Link element for the customer with ID/name '&amp;CC'.
     * 
     * <p>Used to select a specific customer from the autocomplete dropdown.
     * 
     * <p><strong>Stability Concern:</strong> This locator contains a hard-coded test data
     * value ('&amp;CC'). Tests relying on this element require this specific customer
     * to exist in the database.
     */
    @FindBy(xpath = "//a[.='&CC']")
    public WebElement customerId;

    /**
     * Input field for entering the expected revenue amount.
     * 
     * <p>Located within an o_row div element. Used for entering the monetary value
     * representing the expected revenue from an opportunity.
     */
    @FindBy(xpath = "//div[@class='o_row']//input")
    public WebElement expectedRevenue;

    /**
     * Priority selector element for setting opportunity priority level.
     * 
     * <p>Uses indexed XPath targeting the 3rd link element in the 4th table row.
     * Typically represents a star rating or priority level selector.
     * 
     * <p><strong>Stability Concern:</strong> This locator uses positional indices
     * (tr[4], a[3]) which are extremely brittle and may break with any UI
     * restructuring or additional form fields.
     */
    @FindBy(xpath = "//table[@class='o_group o_inner_group o_group_col_6']//tr[4]//a[3]")
    public WebElement priority;

    /**
     * Button element for confirming and creating a new pipeline entry.
     * 
     * <p>Uses name attribute locator targeting the close_dialog button.
     * Clicking this button submits the opportunity creation form and
     * creates the new pipeline entry.
     */
    @FindBy(xpath = "//button[@name='close_dialog']")
    public WebElement createPipeline;

    /**
     * Element displaying the title of a test opportunity in kanban card with data-id='1'.
     * 
     * <p>Located within the kanban card structure, targeting the title span in the
     * second div of the first kanban card. Used to verify that an opportunity
     * was successfully created with the expected title.
     * 
     * <p><strong>Stability Concern:</strong> Fixed data-id='1' assumes the target
     * opportunity is always in the first kanban card position.
     */
    @FindBy(xpath = "//div[@data-id='1']/div[2]//strong//span")
    public  WebElement findTitleTest;

    /**
     * Element displaying the total price/revenue in kanban card with data-id='1'.
     * 
     * <p>Shows the aggregated monetary value for opportunities in the first
     * pipeline stage kanban card.
     */
    @FindBy(xpath = "//div[@data-id='1']//b")
    public WebElement totalPrice;

    /**
     * Pipeline kanban card action area element for data-id='1'.
     * 
     * <p>Represents the clickable area of the first kanban card in the pipeline view.
     * Used for triggering interactions such as opening the opportunity details
     * or initiating drag-and-drop operations.
     */
    @FindBy(xpath = "//div[@data-id='1']/div[2]")
    public WebElement buttonPipeline;

    /**
     * Edit button element for entering opportunity edit mode.
     * 
     * <p>Uses XPath locator targeting the button with accesskey='a'. The accesskey
     * attribute provides keyboard shortcut support for quick access.
     * Clicking this button enables editing of the currently viewed opportunity.
     */
    @FindBy(xpath = "//button[@accesskey='a']")
    public WebElement editButton;

    /**
     * Input field for editing the opportunity title in edit mode.
     * 
     * <p>Uses XPath with name attribute targeting the name input field.
     * This is functionally equivalent to {@link #opportunityTitle} but uses
     * XPath syntax for consistency with other edit mode locators.
     */
    @FindBy(xpath = "//input[@name='name']")
    public WebElement opportunityTitleEdit;

    /**
     * Input field for editing expected revenue in edit mode.
     * 
     * <p>Uses ID-based XPath locator for the expected revenue field.
     * 
     * <p><strong>Stability Concern:</strong> This locator uses a generated numeric
     * ID (o_field_input_125) which is likely auto-generated by Odoo and may change
     * between sessions, database resets, or Odoo version updates.
     */
    @FindBy(xpath = "//input[@id='o_field_input_125']")
    public WebElement expectedRevenueEdit;

    /**
     * Input field for editing the probability percentage in edit mode.
     * 
     * <p>Used to set the win probability percentage for an opportunity.
     * 
     * <p><strong>Stability Concern:</strong> This locator uses a generated numeric
     * ID (o_field_input_127) which is likely auto-generated by Odoo and may change
     * between sessions, database resets, or Odoo version updates.
     */
    @FindBy(xpath = "//input[@id='o_field_input_127']")
    public WebElement probabilityEdit;

    /**
     * Save button element for saving edited opportunity changes.
     * 
     * <p>Uses XPath locator targeting the button with accesskey='s'. The accesskey
     * attribute provides keyboard shortcut support (Alt+S on most browsers).
     * Clicking this button saves all changes made in edit mode.
     */
    @FindBy(xpath = "//button[@accesskey='s']")
    public WebElement  saveEdit;

    /**
     * Sidebar link element for navigating to the Pipeline view.
     * 
     * <p>Uses href attribute XPath targeting a specific menu and action combination.
     * 
     * <p><strong>Stability Concern:</strong> This locator contains hard-coded menu_id=274
     * and action=365 values which are specific to the Odoo installation/version.
     * These IDs will likely break if Odoo menu structure changes or after
     * database migrations.
     */
    @FindBy(xpath = "//a[@href='/web#menu_id=274&action=365']/span")
    public WebElement pipelineSideButton;

    /**
     * Pipeline stage card element representing the first stage (data-id='1').
     * 
     * <p>Used for verifying pipeline progress and stage transitions.
     * Targets the second div within the first pipeline stage kanban card.
     */
    @FindBy(xpath = "//div[@data-id='1']/div[2]")
    public WebElement progressPipeline;

    /**
     * Pipeline stage card element representing the second stage (data-id='2').
     * 
     * <p>Used for multi-stage pipeline testing and verification of stage transitions.
     * Targets the second div within the second pipeline stage kanban card.
     */
    @FindBy(xpath = "//div[@data-id='2']/div[2]")
    public WebElement progressPipeline2;

    /**
     * Verification element within the second pipeline stage card.
     * 
     * <p>Used to confirm pipeline state and opportunity placement within
     * the second stage (data-id='2') of the pipeline.
     */
    @FindBy(xpath = "//div[@data-id='2']//div[2]//strong//span")
    public WebElement testVerify;

    /**
     * Sidebar link element for navigating to the Customers view.
     * 
     * <p>Uses href attribute XPath targeting a specific menu and action combination
     * for the Customers module section.
     * 
     * <p><strong>Stability Concern:</strong> This locator contains hard-coded menu_id=272
     * and action=48 values which are specific to the Odoo installation/version.
     * These IDs will likely break if Odoo menu structure changes.
     */
    @FindBy(xpath = "//a[@href='/web#menu_id=272&action=48']")
    public WebElement customerSideButton;

    /**
     * Create button element for creating a new customer.
     * 
     * <p>Uses XPath locator targeting the button with accesskey='c'.
     * 
     * <p><strong>Note:</strong> This element uses the same XPath selector as
     * {@link #createButton}. Both reference buttons with accesskey='c',
     * which means context (current page) determines which button is targeted.
     */
    @FindBy(xpath = "//button[@accesskey='c']")
    public WebElement createCustomer;

    /**
     * Input field for entering a new customer or entity name.
     * 
     * <p>Uses XPath with name attribute targeting the name input field.
     * 
     * <p><strong>Note:</strong> This element uses the same selector pattern as
     * {@link #opportunityTitleEdit}. Both target inputs with name='name',
     * which means context (current form) determines which input is targeted.
     */
    @FindBy(xpath = "//input[@name='name']")
    public WebElement inputName;

    /**
     * Button element for confirming and creating a new customer.
     * 
     * <p>Uses name attribute XPath targeting the close_dialog button.
     * 
     * <p><strong>Note:</strong> This element uses the same selector as
     * {@link #createPipeline}. Both target the close_dialog button,
     * which means context (current dialog) determines which button is targeted.
     */
    @FindBy(xpath = "//button[@name='close_dialog']")
    public WebElement createCustomerButton;

    /**
     * Search bar input field for filtering customers and opportunities.
     * 
     * <p>Uses class-based XPath targeting the Odoo search view input.
     * Allows entering search queries to filter displayed records.
     */
    @FindBy(xpath = "//input[@class='o_searchview_input']")
    public WebElement searchingText;

    /**
     * Element displaying the customer name '&amp;CC' in search results or list view.
     * 
     * <p>Used to verify customer existence or selection in filtered results.
     * 
     * <p><strong>Stability Concern:</strong> This locator contains a hard-coded test
     * data value ('&amp;CC'). Tests relying on this element require this specific
     * customer name to exist in the database.
     */
    @FindBy(xpath =  "//span[.='&CC']")
    public WebElement nameCustomer;

    /**
     * Button element for accessing the due payment report or print action.
     * 
     * <p>Uses data-section attribute XPath targeting the print action section.
     * Clicking this button opens payment-related report options.
     */
    @FindBy(xpath = "//a[@data-section='print']")
    public WebElement duePaymentButton;

    /**
     * Print button element for printing reports or documents.
     * 
     * <p>Uses absolute XPath path from the html root element.
     * 
     * <p><strong>Stability Concern:</strong> This locator uses a full absolute XPath
     * path (starting from /html/body) which is extremely brittle and will break
     * with virtually any change to the page DOM structure. This should be
     * refactored to use more stable locator strategies such as ID, name,
     * data attributes, or relative XPath.
     */
    @FindBy(xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button")
    public WebElement printButton;

}
