package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object class representing the Employees module in the Odoo application.
 * 
 * <p>This class provides WebElement locators and methods for the complete authentication workflow
 * and employee management functionality, including:
 * <ul>
 *   <li>Login form interaction (username/password entry and form submission)</li>
 *   <li>Employees module navigation from the sidebar</li>
 *   <li>Submenu navigation (Badges, Challenges, Goals History, Departments)</li>
 *   <li>Employee CRUD operations (Create, Read, Update via kanban view)</li>
 * </ul>
 * 
 * <p>This class follows the <strong>Page Object Model (POM)</strong> design pattern, encapsulating
 * all page-specific locators and interactions within a single class to improve test maintainability
 * and reduce code duplication across step definitions.
 * 
 * <p><strong>Note:</strong> Unlike other page objects in this framework, this class includes two
 * {@code login()} helper methods for performing authentication. This is an intentional design choice
 * to encapsulate the complete login workflow within the employee module context.
 * 
 * <p><strong>Warning:</strong> The parameterized {@link #login(String, String)} method currently
 * ignores its parameters and uses hard-coded credentials instead. This is a known issue that should
 * be addressed by using the provided parameters or by utilizing {@link com.testinium.utilities.ConfigurationReader}
 * for configurable test credentials.
 * 
 * <p>All WebElement fields in this class are automatically initialized via
 * {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)} using the WebDriver
 * instance obtained from {@link Driver#getDriver()}.
 * 
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.PageFactory
 * @see com.testinium.utilities.ConfigurationReader
 */
public class EmployeeP {

    /**
     * Constructs a new EmployeeP Page Object instance.
     * 
     * <p>This no-argument constructor initializes all {@link FindBy} annotated WebElement fields
     * by invoking {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)}.
     * The PageFactory binds the annotated locator definitions to the active WebDriver instance
     * obtained from {@link Driver#getDriver()}, enabling lazy initialization of WebElements.
     * 
     * <p>The WebDriver instance is retrieved from the thread-local driver pool managed by the
     * {@link Driver} utility class, ensuring thread-safety in parallel test execution scenarios.
     */
    public EmployeeP(){
        PageFactory.initElements(Driver.getDriver(),this);
    }

    /**
     * WebElement locator for the login/email input field on the authentication page.
     * 
     * <p>Uses ID-based locator strategy targeting the element with {@code id="login"}.
     * This field is used for entering the username or email address during the
     * authentication workflow.
     * 
     * <p><strong>Locator Strategy:</strong> ID (most reliable and performant)
     */
    @FindBy(id = "login")
    public WebElement inputLogin;

    /**
     * WebElement locator for the password input field on the authentication page.
     * 
     * <p>Uses ID-based locator strategy targeting the element with {@code id="password"}.
     * This field is used for entering the user's password during authentication.
     * 
     * <p><strong>Locator Strategy:</strong> ID (most reliable and performant)
     */
    @FindBy(id = "password")
    public WebElement inputPass;

    /**
     * WebElement locator for the "Log in" button on the authentication page.
     * 
     * <p>Uses XPath locator strategy targeting a button element by its visible text content.
     * Clicking this button submits the login form with the entered credentials.
     * 
     * <p><strong>Locator Strategy:</strong> XPath by visible text
     * <p><strong>Selector:</strong> {@code //button[.='Log in']}
     */
    @FindBy(xpath = "//button[.='Log in']")
    public WebElement loginButton;

    /**
     * WebElement locator for the Employees module navigation link in the sidebar.
     * 
     * <p>Uses partial link text locator strategy to find the "Employees" menu item.
     * Clicking this element navigates to the employee management section from the
     * main application sidebar.
     * 
     * <p><strong>Locator Strategy:</strong> Partial Link Text
     */
    @FindBy(partialLinkText = "Employees")
    public WebElement emplStage;

    /**
     * WebElement locator for the Badges submenu item within the Employees module.
     * 
     * <p>Uses partial link text locator strategy to find the "Badges" navigation link.
     * Clicking this element navigates to the employee badges/gamification section
     * for managing employee recognition and achievement badges.
     * 
     * <p><strong>Locator Strategy:</strong> Partial Link Text
     */
    @FindBy(partialLinkText = "Badges")
    public WebElement badgesBtn;

    /**
     * WebElement locator for the Challenges submenu item within the Employees module.
     * 
     * <p>Uses partial link text locator strategy to find the "Challenges" navigation link.
     * Clicking this element navigates to the employee challenges section for managing
     * gamification challenges and team competitions.
     * 
     * <p><strong>Locator Strategy:</strong> Partial Link Text
     */
    @FindBy(partialLinkText = "Challenges")
    public WebElement challengesBtn;

    /**
     * WebElement locator for the Goals History submenu item within the Employees module.
     * 
     * <p>Uses partial link text locator strategy to find the "Goals History" navigation link.
     * Clicking this element navigates to view the historical record of employee goals
     * and their completion status over time.
     * 
     * <p><strong>Locator Strategy:</strong> Partial Link Text
     */
    @FindBy(partialLinkText = "Goals History")
    public WebElement goalsHistoryBtn;

    /**
     * WebElement locator for the Departments submenu item within the Employees module.
     * 
     * <p>Uses partial link text locator strategy to find the "Departments" navigation link.
     * Clicking this element navigates to the department management section for
     * creating, viewing, and managing organizational departments.
     * 
     * <p><strong>Locator Strategy:</strong> Partial Link Text
     */
    @FindBy(partialLinkText = "Departments")
    public WebElement departmentsBtn;

    /**
     * WebElement locator for the Create button in the kanban view.
     * 
     * <p>Uses XPath with class-based selector targeting the Odoo kanban "Create" button.
     * The selector targets the {@code o-kanban-button-new} CSS class which identifies
     * the primary action button for creating new records in kanban views.
     * 
     * <p>Clicking this button initiates the workflow to create a new employee record.
     * 
     * <p><strong>Locator Strategy:</strong> XPath by CSS class
     * <p><strong>Selector:</strong> {@code //button[@class='btn btn-primary btn-sm o-kanban-button-new btn-default']}
     */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o-kanban-button-new btn-default']")
    public WebElement createBtn;

    /**
     * WebElement locator for the employee name input field in the create/edit form.
     * 
     * <p>Uses XPath with class-based selector targeting an input field with the
     * {@code o_required_modifier} CSS class, indicating this is a required field
     * in the Odoo form.
     * 
     * <p>This field is used for entering or editing the employee's name during
     * CRUD operations.
     * 
     * <p><strong>Locator Strategy:</strong> XPath by CSS class
     * <p><strong>Selector:</strong> {@code //input[@class='o_field_char o_field_widget o_input o_required_modifier']}
     */
    @FindBy(xpath = "//input[@class='o_field_char o_field_widget o_input o_required_modifier']")
    public WebElement employeesName;

    /**
     * WebElement locator for the Save button in the employee form.
     * 
     * <p>Uses XPath with class-based selector targeting the Odoo form Save button.
     * Clicking this button saves the current employee record.
     * 
     * <p><strong>Note:</strong> The variable name {@code savedMessage} is misleading as the
     * selector actually targets a Save button element, not a confirmation message.
     * Consider renaming to {@code saveBtn} for clarity.
     * 
     * <p><strong>Locator Strategy:</strong> XPath by CSS class
     * <p><strong>Selector:</strong> {@code //button[@class='btn btn-primary btn-sm o_form_button_save']}
     */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']")
    public WebElement savedMessage;

    /**
     * WebElement locator for the "Employee created" success message.
     * 
     * <p>Uses XPath to target a paragraph element containing the exact text "Employee created".
     * This element appears after successfully creating a new employee record and is used
     * for verifying successful employee creation in test assertions.
     * 
     * <p><strong>Locator Strategy:</strong> XPath by text content
     * <p><strong>Selector:</strong> {@code //p[.='Employee created']}
     */
    @FindBy(xpath = "//p[.='Employee created']")
    public WebElement createdMessage;

    /**
     * WebElement locator for selecting an employee from the list/kanban view.
     * 
     * <p>Uses absolute XPath to target an employee card element in the view.
     * 
     * <p><strong>Stability Concern:</strong> This locator uses a full absolute XPath
     * ({@code //html/body/div[1]/div[2]/div[2]/div/div/div/div[1]}) which is extremely
     * brittle and will break if the DOM structure changes. Consider using a more
     * robust selector such as CSS class, data attribute, or relative XPath.
     * 
     * <p><strong>Locator Strategy:</strong> Absolute XPath (not recommended)
     */
    @FindBy(xpath = "//html/body/div[1]/div[2]/div[2]/div/div/div/div[1]")
    public WebElement chooseEmployee;

    /**
     * WebElement locator for the Edit button in the employee detail view.
     * 
     * <p>Uses absolute XPath to target the Edit button for modifying employee records.
     * 
     * <p><strong>Stability Concern:</strong> This locator uses a full absolute XPath
     * ({@code //html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/button[1]}) which
     * is extremely brittle and will break with any DOM structure changes. Consider using
     * a more stable selector strategy such as CSS class, aria-label, or data attributes.
     * 
     * <p><strong>Locator Strategy:</strong> Absolute XPath (not recommended)
     */
    @FindBy(xpath = "//html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/button[1]")
    public WebElement editEmployee;

    /**
     * WebElement locator for the name input field in edit mode.
     * 
     * <p>Uses XPath with ID-based selector to target the employee name field during editing.
     * 
     * <p><strong>Stability Concern:</strong> This locator uses a generated numeric ID
     * ({@code o_field_input_678}) which is dynamically assigned by Odoo and will vary
     * across different sessions, environments, or Odoo versions. This selector is highly
     * unreliable and should be replaced with a stable locator such as a CSS class,
     * name attribute, or relative position to a labeled element.
     * 
     * <p><strong>Locator Strategy:</strong> XPath by generated ID (not recommended)
     * <p><strong>Selector:</strong> {@code //*[@id="o_field_input_678"]}
     */
    @FindBy(xpath = "//*[@id=\"o_field_input_678\"]")
    public WebElement nameEdit;

    /**
     * Performs a complete login workflow using hard-coded test credentials.
     * 
     * <p>This method executes the following authentication steps:
     * <ol>
     *   <li>Enters the hard-coded email address "posmanager50@info.com" into the login field</li>
     *   <li>Enters the hard-coded password "posmanager" into the password field</li>
     *   <li>Clicks the login button to submit the authentication form</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> This method uses hard-coded test credentials which are not
     * suitable for production environments or scenarios requiring configurable credentials.
     * For more flexible authentication, consider using {@link com.testinium.utilities.ConfigurationReader#getProperty(String)}
     * to load credentials from the configuration file.
     * 
     * <p><strong>Usage Example:</strong>
     * <pre>
     * EmployeeP employeePage = new EmployeeP();
     * employeePage.login();
     * // User is now authenticated and can proceed with employee operations
     * </pre>
     * 
     * @see com.testinium.utilities.ConfigurationReader
     */
    public void login(){
        this.inputLogin.sendKeys("posmanager50@info.com");
        this.inputPass.sendKeys("posmanager");
        this.loginButton.click();
    }

    /**
     * Parameterized login method intended for configurable credentials.
     * 
     * <p><strong>WARNING: CRITICAL BUG - PARAMETERS ARE IGNORED!</strong></p>
     * 
     * <p>This method is designed to accept configurable username and password parameters,
     * but <strong>the parameters are completely ignored</strong>. Instead, the method uses
     * the same hard-coded credentials as the no-argument {@link #login()} method:
     * <ul>
     *   <li>Email: "posmanager50@info.com" (ignores {@code inputLogin} parameter)</li>
     *   <li>Password: "posmanager" (ignores {@code inputPass} parameter)</li>
     * </ul>
     * 
     * <p><strong>This appears to be a copy-paste error.</strong> To fix this bug, the method
     * should be updated to use the provided parameters:
     * <pre>
     * // Recommended fix:
     * this.inputLogin.sendKeys(inputLogin);
     * this.inputPass.sendKeys(inputPass);
     * </pre>
     * 
     * <p><strong>Current (buggy) behavior:</strong> Both parameters are accepted but never used.
     * The method performs the same actions as {@link #login()} regardless of input.
     * 
     * @param inputLogin the intended username or email address for authentication
     *                   (currently IGNORED - hard-coded value used instead)
     * @param inputPass  the intended password for authentication
     *                   (currently IGNORED - hard-coded value used instead)
     * @see #login()
     * @see com.testinium.utilities.ConfigurationReader
     */
    public void login(String inputLogin, String inputPass){
        this.inputLogin.sendKeys("posmanager50@info.com");
        this.inputPass.sendKeys("posmanager");
        this.loginButton.click();
    }
}
