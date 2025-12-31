package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object class representing the Inventory/Products module in Odoo ERP application.
 * 
 * <p>This class provides WebElement locators and page interactions for product management
 * operations within the Odoo Inventory module. It supports the following functionalities:</p>
 * <ul>
 *   <li>Module navigation - accessing the Inventory module from the main menu</li>
 *   <li>Product creation - initiating and completing new product entries</li>
 *   <li>Saving operations - persisting new or edited product data</li>
 *   <li>Validation/notification handling - capturing error messages and success notifications</li>
 * </ul>
 * 
 * <p>This class follows the Page Object Model (POM) design pattern, which encapsulates
 * page-specific locators and behaviors in a single class. This promotes code reusability,
 * maintainability, and separation of test logic from page structure.</p>
 * 
 * <p>All WebElement fields annotated with {@link FindBy} are automatically initialized
 * via {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)} in the
 * constructor, binding each locator to the active WebDriver instance obtained from
 * {@link Driver#getDriver()}.</p>
 * 
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.PageFactory
 * @see org.openqa.selenium.support.FindBy
 */
public class InventoryP {

    /**
     * Constructs a new InventoryP page object instance.
     * 
     * <p>This no-argument constructor initializes all {@link FindBy} annotated WebElement
     * fields using Selenium's PageFactory mechanism. The {@link PageFactory#initElements}
     * method binds each locator annotation to the active WebDriver instance retrieved
     * from {@link Driver#getDriver()}, enabling lazy initialization of WebElements
     * when they are first accessed.</p>
     * 
     * <p>The WebDriver instance is obtained from the thread-local driver pool managed
     * by the Driver utility class, ensuring thread-safe WebDriver access in parallel
     * test execution scenarios.</p>
     */
    public InventoryP(){
        PageFactory.initElements(Driver.getDriver(), this);
    }

    /**
     * WebElement locator for the Inventory module navigation link.
     * 
     * <p>Uses partial link text locator strategy to find the "Inventory" link
     * in the Odoo main navigation menu. This element is used to navigate from
     * the main dashboard or any other module to the Inventory module.</p>
     * 
     * <p>Locator Strategy: {@code partialLinkText = "Inventory"}</p>
     */
    @FindBy(partialLinkText = "Inventory")
    public WebElement inventoryModule;

    /**
     * WebElement locator for the Products submenu link within the Inventory module.
     * 
     * <p>Uses partial link text locator strategy to find the "Products" submenu item.
     * This element is used to navigate to the product management section within
     * the Inventory module, where products can be viewed, created, and edited.</p>
     * 
     * <p>Locator Strategy: {@code partialLinkText = "Products"}</p>
     */
    @FindBy(partialLinkText = "Products")
    public WebElement products;

    /**
     * WebElement locator for the Create button in Kanban view.
     * 
     * <p>Uses class name locator strategy to find the Create button that appears
     * in Odoo's Kanban view interface. The {@code o-kanban-button-new} class is
     * specific to Odoo's Kanban view styling. Clicking this button initiates
     * the creation of a new product record.</p>
     * 
     * <p>Locator Strategy: {@code className = "o-kanban-button-new"}</p>
     */
    @FindBy(className = "o-kanban-button-new")
    public WebElement createBtn;

    /**
     * WebElement locator for the Save button in the product form.
     * 
     * <p>Uses XPath locator strategy to find the Save button with primary button
     * styling in Odoo's form view. The button has the {@code o_form_button_save}
     * class along with Bootstrap's primary button classes. This element is used
     * to persist new or edited product data to the database.</p>
     * 
     * <p>Locator Strategy: {@code xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']"}</p>
     */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']")
    public WebElement saveBtn;

    /**
     * WebElement locator for Odoo's notification manager container.
     * 
     * <p>Uses class name locator strategy to find the notification manager element
     * that displays validation errors, warnings, or success messages in Odoo.
     * This element captures system feedback after user actions such as form
     * submissions, validation failures, or successful operations.</p>
     * 
     * <p>Locator Strategy: {@code className = "o_notification_manager"}</p>
     * 
     * <p>Common notification types include:</p>
     * <ul>
     *   <li>Validation errors for missing required fields</li>
     *   <li>Success messages after saving records</li>
     *   <li>Warning messages for potential issues</li>
     * </ul>
     */
    @FindBy(className = "o_notification_manager")
    public WebElement fieldError;

    /**
     * WebElement locator for the product name input field.
     * 
     * <p>Uses ID locator strategy to find the product name text input field.
     * This field is used to enter the name of a new product during creation
     * or to modify an existing product's name during editing.</p>
     * 
     * <p>Locator Strategy: {@code id = "o_field_input_479"}</p>
     * 
     * <p><strong>Stability Concern:</strong> This locator uses a generated numeric ID
     * ({@code o_field_input_479}) which may vary across different Odoo sessions,
     * versions, database instances, or page reloads. This ID is dynamically
     * generated by Odoo and is not stable for long-term test maintenance.
     * Consider using an alternative locator strategy such as:</p>
     * <ul>
     *   <li>XPath with field name attribute: {@code //input[@name='name']}</li>
     *   <li>CSS selector with data attributes if available</li>
     *   <li>XPath with label text association</li>
     * </ul>
     */
    @FindBy(id = "o_field_input_479")
    public WebElement productName;

    /**
     * WebElement locator for a specific product in the products list.
     * 
     * <p>Uses XPath locator strategy to find a span element containing the
     * exact text 'EY'. This element is used to verify that a specific product
     * appears in the product list after creation or search operations.</p>
     * 
     * <p>Locator Strategy: {@code xpath = "//span[.='EY']"}</p>
     * 
     * <p><strong>Stability Concern:</strong> This locator contains a hard-coded
     * test data value ('EY') which ties the locator to specific test data.
     * This approach has limited reusability and may cause test failures if
     * the test data changes. Consider parameterizing this locator or creating
     * a method that accepts the product name as a parameter to build a dynamic
     * XPath expression.</p>
     */
    @FindBy(xpath = "//span[.='EY']")
    public WebElement productsList;

    /**
     * WebElement locator for the created product's name field span.
     * 
     * <p>Uses XPath locator strategy to find a span element with Odoo's
     * required field modifier class. The {@code o_required_modifier} class
     * indicates that this is a mandatory field in the form. The full class
     * combination ({@code o_field_char o_field_widget o_required_modifier})
     * identifies this as a required character/text field widget.</p>
     * 
     * <p>This element is used to verify successful product creation by checking
     * that the product name field is populated and displayed with the required
     * field styling after a save operation.</p>
     * 
     * <p>Locator Strategy: {@code xpath = "//span[@class='o_field_char o_field_widget o_required_modifier']"}</p>
     */
    @FindBy(xpath = "//span[@class='o_field_char o_field_widget o_required_modifier']")
    public WebElement createdProduct;


}
