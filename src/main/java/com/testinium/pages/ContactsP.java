package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object class representing the Contacts module in the Odoo web application.
 * 
 * <p>This class provides WebElement locators for contact management operations including:
 * <ul>
 *   <li>Navigation to Contacts module</li>
 *   <li>CRUD operations (Create, Read, Update, Delete contacts)</li>
 *   <li>Form input fields (name, street, phone, email)</li>
 *   <li>Action dropdown menu interactions</li>
 *   <li>Kanban view interactions</li>
 *   <li>List view operations</li>
 * </ul>
 * 
 * <p>This class follows the Page Object Model (POM) design pattern, which encapsulates
 * the UI structure and behavior of the Contacts page. By centralizing element locators
 * in this class, test maintenance is simplified when UI changes occur.
 * 
 * <p>All WebElement fields are initialized via {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)}
 * using the WebDriver instance obtained from {@link Driver#getDriver()}. Elements use
 * lazy initialization - they are located in the DOM only when first accessed.
 * 
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.PageFactory
 * @see org.openqa.selenium.support.FindBy
 */
public class ContactsP {

    /**
     * Constructs a new ContactsP Page Object and initializes all WebElement fields.
     * 
     * <p>This no-argument constructor initializes all {@link FindBy} annotated WebElement
     * fields using Selenium's PageFactory pattern. The {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)}
     * method binds the locators to the active WebDriver instance obtained from
     * {@link Driver#getDriver()}.
     * 
     * <p>This follows lazy initialization - elements are not actually located in the DOM
     * at construction time. Instead, the element lookup occurs when each WebElement field
     * is first accessed during test execution. This approach improves performance and
     * allows for dynamic page content.
     */
    public ContactsP(){
        PageFactory.initElements(Driver.getDriver(), this);
    }

    /**
     * Navigation link to access the Contacts module from other modules.
     * 
     * <p>Uses partial link text locator strategy matching "Contacts" text.
     * This element is typically found in the main navigation menu or module
     * switcher of the Odoo application.
     * 
     * <p>Locator strategy: {@code partialLinkText = "Contacts"}
     */
    @FindBy(partialLinkText = "Contacts")
    public WebElement contactModule;

    /**
     * Create button to initiate new contact creation.
     * 
     * <p>Uses XPath locator targeting the button with accesskey 'c', which enables
     * keyboard shortcut accessibility (Alt+C on most browsers). This button
     * opens the contact creation form.
     * 
     * <p>Locator strategy: {@code xpath = "//button[@accesskey='c']"}
     */
    @FindBy(xpath = "//button[@accesskey='c']")
    public WebElement createContact;

    /**
     * List view button to switch contacts display to list/table format.
     * 
     * <p>Uses XPath locator targeting the button with accesskey 'l', which enables
     * keyboard shortcut accessibility (Alt+L on most browsers). Clicking this
     * button switches from kanban view to list/table view of contacts.
     * 
     * <p>Locator strategy: {@code xpath = "//button[@accesskey='l']"}
     */
    @FindBy(xpath = "//button[@accesskey='l']")
    public WebElement callList;

    /**
     * Input field for entering or editing the contact's full name.
     * 
     * <p>Uses name attribute locator strategy, which is stable for this form field.
     * This field is required for contact creation and typically appears at the
     * top of the contact form.
     * 
     * <p>Locator strategy: {@code name = "name"}
     */
    @FindBy(name = "name")
    public WebElement nameInput;

    /**
     * Input field for entering the contact's street address.
     * 
     * <p>Uses name attribute locator strategy. This field is part of the contact
     * address information section in the contact form.
     * 
     * <p>Locator strategy: {@code name = "street"}
     */
    @FindBy(name = "street")
    public WebElement streetInput;

    /**
     * Input field for entering the contact's phone number.
     * 
     * <p>Uses name attribute locator strategy. This field accepts phone numbers
     * in various formats and is part of the contact communication details.
     * 
     * <p>Locator strategy: {@code name = "phone"}
     */
    @FindBy(name = "phone")
    public WebElement phoneNoInput;

    /**
     * Input field for entering the contact's email address.
     * 
     * <p>Uses name attribute locator strategy. This field is used for entering
     * the contact's email address and is part of the contact communication details.
     * 
     * <p>Locator strategy: {@code name = "email"}
     */
    @FindBy(name = "email")
    public WebElement emailInput;

    /**
     * OK confirmation button for dialogs and form submissions.
     * 
     * <p>Uses XPath locator matching a span element with visible text "Ok".
     * This button is used to confirm dialogs, modal windows, or form submissions
     * throughout the Contacts module.
     * 
     * <p>Locator strategy: {@code xpath = "//span[.='Ok']"}
     */
    @FindBy(xpath="//span[.='Ok']")
    public WebElement okBtn;

    /**
     * Checkbox for selecting a specific contact in the list view.
     * 
     * <p>Uses indexed XPath targeting the 12th checkbox input within contact list checkboxes.
     * 
     * <p><strong>Stability concern:</strong> This locator uses a positional index [12] which
     * is fragile and depends on specific test data setup. If the order of contacts changes
     * or if there are fewer than 12 contacts, this locator will fail or select the wrong contact.
     * Consider using a more specific locator based on contact name or ID for production tests.
     * 
     * <p>Locator strategy: {@code xpath = "(//div[@class='o_checkbox']/input)[12]"}
     */
    @FindBy(xpath = "(//div[@class='o_checkbox']/input)[12]")
    public WebElement newContact;

    /**
     * Action dropdown menu in the sidebar for bulk operations.
     * 
     * <p>Uses indexed XPath targeting the 2nd div child within the sidebar control panel.
     * This dropdown provides actions like delete, export, and other bulk operations
     * that can be performed on selected contacts.
     * 
     * <p><strong>Stability concern:</strong> This locator uses a positional index [2] which
     * depends on the DOM structure remaining consistent. Changes to the sidebar layout
     * may cause this locator to fail or target the wrong element.
     * 
     * <p>Locator strategy: {@code xpath = "(//div[@class='o_cp_sidebar']/div/div)[2]"}
     */
    @FindBy(xpath = "(//div[@class='o_cp_sidebar']/div/div)[2]")
    public WebElement actionInput;

    /**
     * Delete action option within the action dropdown menu.
     * 
     * <p>Uses XPath locator targeting an anchor element with data-index attribute value of '3',
     * which corresponds to the delete action in the action dropdown menu.
     * 
     * <p>Locator strategy: {@code xpath = "//a[@data-index='3']"}
     */
    @FindBy(xpath = "//a[@data-index='3']")
    public WebElement deleteInput;

    /**
     * First contact card in the kanban view display.
     * 
     * <p>Uses indexed XPath targeting the first div child within the ungrouped partner
     * kanban view container. This element represents the first contact card displayed
     * in the kanban layout.
     * 
     * <p>Locator strategy: {@code xpath = "(//div[@class='o_kanban_view o_res_partner_kanban o_kanban_ungrouped']/div)[1]"}
     */
    @FindBy(xpath = "(//div[@class='o_kanban_view o_res_partner_kanban o_kanban_ungrouped']/div)[1]")
    public WebElement firstUser;

    /**
     * Title section element in the contact edit mode.
     * 
     * <p>Uses XPath locator targeting the div with class 'oe_title'. This element
     * is used to verify that the edit mode is active or to access the title area
     * of a contact being edited.
     * 
     * <p>Locator strategy: {@code xpath = "//div[@class='oe_title']"}
     */
    @FindBy(xpath = "//div[@class='oe_title']")
    public WebElement editTitle;

    /**
     * Edit button to initiate edit mode for the current contact.
     * 
     * <p>Uses XPath locator targeting a button with both 'btn btn-primary btn-sm'
     * and 'o_form_button_edit' classes. Clicking this button switches the contact
     * form from view mode to edit mode.
     * 
     * <p>Locator strategy: {@code xpath = "//button[@class='btn btn-primary btn-sm o_form_button_edit']"}
     */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_edit']")
    public WebElement editBtn;

    /**
     * Print dropdown menu in the expanded/open state.
     * 
     * <p>Uses XPath locator targeting a div with the 'open' class state within
     * the dropdown button group.
     * 
     * <p><strong>Stability concern:</strong> This locator relies on the "open" class being
     * present, which only occurs when the dropdown is already expanded. This element
     * will not be found if the dropdown is collapsed. Ensure the dropdown is clicked
     * to expand it before accessing this element.
     * 
     * <p>Locator strategy: {@code xpath = "//div[@class='btn-group o_dropdown open']"}
     */
    @FindBy(xpath = "//div[@class='btn-group o_dropdown open']")
    public WebElement printInput;


    /**
     * Due payment print action button within the expanded dropdown.
     * 
     * <p>Uses XPath locator targeting a button element within the open dropdown
     * container. This button triggers the due payment print action for the
     * selected contact.
     * 
     * <p><strong>Stability concern:</strong> This locator requires the parent dropdown
     * to be in the "open" state (have the "open" class) to match. Ensure the print
     * dropdown is expanded before attempting to interact with this element.
     * 
     * <p>Locator strategy: {@code xpath = "(//div[@class='btn-group o_dropdown open']/button)"}
     */
    @FindBy(xpath = "(//div[@class='btn-group o_dropdown open']/button)")
    public WebElement duePayment;


}
