package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object (POM element container) for the Employees module of the Odoo/Upgenix ERP under test,
 * including the login form used to reach it.
 *
 * <p>Each {@code public} {@code WebElement} field is annotated with {@code @FindBy} and bound by Selenium
 * {@code PageFactory} to a lazy proxy, so the element is located in the current DOM only when the field is used.
 * The step definitions in {@code com.testinium.step_definitions.EmployeeStage} construct this class and drive its
 * elements; the class contains no waits or assertions. Its {@link #login()} helpers type hard-coded credentials
 * rather than values from {@code configuration.properties}.
 */
public class EmployeeP {

    /**
     * Creates the page and initializes its {@code @FindBy} proxies by calling
     * {@code PageFactory.initElements(Driver.getDriver(), this)}. Step classes construct pages in field initializers.
     *
     * <p>{@link Driver#getDriver()} reuses this thread's {@code WebDriver}; with none, it starts one only if the {@code browser}
     * key is {@code chrome} or {@code firefox}, and a failed start throws. Any other value binds the proxies to a {@code null} driver,
     * so using an element throws {@code NullPointerException}; a missing key or configuration file makes this constructor throw it.
     */
    public EmployeeP(){
        PageFactory.initElements(Driver.getDriver(),this);
    }

    /** Login (email) input of the login form ({@code id="login"}). */
    @FindBy(id = "login")
    public WebElement inputLogin;

    /** Password input of the login form ({@code id="password"}). */
    @FindBy(id = "password")
    public WebElement inputPass;

    /** "Log in" button of the login form. */
    @FindBy(xpath = "//button[.='Log in']")
    public WebElement loginButton;

    /** Employees link in the main menu, located by partial link text. */
    @FindBy(partialLinkText = "Employees")
    public WebElement emplStage;

    /** Badges menu link. */
    @FindBy(partialLinkText = "Badges")
    public WebElement badgesBtn;

    /** Challenges menu link. */
    @FindBy(partialLinkText = "Challenges")
    public WebElement challengesBtn;

    /** Goals History menu link. */
    @FindBy(partialLinkText = "Goals History")
    public WebElement goalsHistoryBtn;

    /** Departments menu link. */
    @FindBy(partialLinkText = "Departments")
    public WebElement departmentsBtn;

    /** Kanban Create button of the Employees view. */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o-kanban-button-new btn-default']")
    public WebElement createBtn;

    /** Required employee name input on the create form. */
    @FindBy(xpath = "//input[@class='o_field_char o_field_widget o_input o_required_modifier']")
    public WebElement employeesName;

    /** Form Save button ({@code o_form_button_save}); despite its name it locates the button, not a message. */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']")
    public WebElement savedMessage;

    /** "Employee created" confirmation message. */
    @FindBy(xpath = "//p[.='Employee created']")
    public WebElement createdMessage;

    /** Employee record located by an absolute XPath and clicked to open it; fragile. */
    @FindBy(xpath = "//html/body/div[1]/div[2]/div[2]/div/div/div/div[1]")
    public WebElement chooseEmployee;

    /** Edit button located by an absolute XPath; fragile. */
    @FindBy(xpath = "//html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/button[1]")
    public WebElement editEmployee;

    /** Employee name input in edit mode, located by the generated id {@code o_field_input_678}; fragile. */
    @FindBy(xpath = "//*[@id=\"o_field_input_678\"]")
    public WebElement nameEdit;

    /**
     * Logs in with a hard-coded account: types it into {@link #inputLogin} and {@link #inputPass},
     * then clicks {@link #loginButton}.
     *
     * <p>The credentials are literals in this method, not values read from {@code configuration.properties}.
     * Called by {@code com.testinium.step_definitions.EmployeeStage} before navigating to Employees.
     */
    public void login(){
        this.inputLogin.sendKeys("posmanager50@info.com");
        this.inputPass.sendKeys("posmanager");
        this.loginButton.click();
    }

    /**
     * Ignores both arguments and logs in with the same hard-coded account as {@link #login()}: types it into
     * {@link #inputLogin} and {@link #inputPass}, then clicks {@link #loginButton}.
     *
     * <p>Known discrepancy, documented rather than fixed; no step definition calls this overload.
     *
     * @param inputLogin login name; ignored by the current implementation
     * @param inputPass  password; ignored by the current implementation
     */
    public void login(String inputLogin, String inputPass){
        this.inputLogin.sendKeys("posmanager50@info.com");
        this.inputPass.sendKeys("posmanager");
        this.loginButton.click();
    }
}
