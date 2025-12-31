package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object class representing the session/login functionality in the Odoo web application.
 * 
 * <p>This is a minimal Page Object class that provides only the essential locators required
 * for authentication: login input, password input, and login button. It follows the
 * Page Object Model (POM) design pattern to encapsulate web elements and their locators
 * in a maintainable structure.</p>
 * 
 * <p>This class is intentionally simplified and focused for reusable authentication flows.
 * Unlike {@link EmployeeP}, this Page Object contains no helper methods - only WebElement
 * field declarations with their corresponding locators.</p>
 * 
 * <p><strong>Comparison with LoginP:</strong> This class is similar to {@link LoginP} but
 * more minimal in scope. SessionP lacks the password reset link locator, dashboard marker,
 * and alert/error message locators that LoginP provides. Use SessionP when only basic
 * authentication elements are needed; use LoginP when additional login-related validations
 * are required.</p>
 * 
 * <p>All WebElement fields in this class are initialized via
 * {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)} using the
 * WebDriver instance obtained from {@link Driver#getDriver()}. This initialization
 * occurs in the constructor, binding all {@link FindBy} annotated fields to their
 * corresponding web elements.</p>
 * 
 * <p><strong>Usage Example:</strong></p>
 * <pre>{@code
 * SessionP sessionPage = new SessionP();
 * sessionPage.inputLogin.sendKeys("user@example.com");
 * sessionPage.inputPass.sendKeys("password123");
 * sessionPage.loginButton.click();
 * }</pre>
 * 
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.PageFactory
 * @see LoginP
 */
public class SessionP {

    /**
     * Constructs a new SessionP Page Object and initializes all WebElement fields.
     * 
     * <p>This no-argument constructor uses {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)}
     * to bind all {@link FindBy} annotated WebElement fields to their corresponding
     * elements in the DOM. The WebDriver instance is obtained from the thread-local
     * driver pool via {@link Driver#getDriver()}.</p>
     * 
     * <p>After construction, all WebElement fields (inputLogin, inputPass, loginButton)
     * are ready for interaction without additional initialization.</p>
     * 
     * @see Driver#getDriver()
     * @see PageFactory#initElements(org.openqa.selenium.WebDriver, Object)
     */
    public SessionP(){
        PageFactory.initElements(Driver.getDriver(),this);
    }

    /**
     * WebElement representing the login/email input field on the Odoo login page.
     * 
     * <p>This element is located using the ID-based locator strategy with {@code id="login"},
     * which is the standard identifier for the login form field in Odoo's authentication page.
     * The ID-based locator provides stable and reliable element identification.</p>
     * 
     * <p>This field is used for entering the username or email address during the
     * authentication process. It accepts text input via standard WebElement methods
     * such as {@code sendKeys()}.</p>
     * 
     * <p><strong>Note:</strong> This uses the same locator strategy as
     * {@code EmployeeP.inputLogin}, ensuring consistency across page objects that
     * interact with the login functionality.</p>
     * 
     * <p><strong>Locator:</strong> {@code @FindBy(id = "login")}</p>
     */
    @FindBy(id = "login")
    public WebElement inputLogin;

    /**
     * WebElement representing the password input field on the Odoo login page.
     * 
     * <p>This element is located using the ID-based locator strategy with {@code id="password"},
     * which is the standard identifier for the password field in Odoo's authentication page.
     * The ID-based locator provides stable and reliable element identification.</p>
     * 
     * <p>This field is used for entering the user's password during the authentication
     * process. It accepts text input via standard WebElement methods such as
     * {@code sendKeys()}. The input is typically masked as password characters in the UI.</p>
     * 
     * <p><strong>Note:</strong> This uses the same locator strategy as
     * {@code EmployeeP.inputPass}, ensuring consistency across page objects that
     * interact with the login functionality.</p>
     * 
     * <p><strong>Locator:</strong> {@code @FindBy(id = "password")}</p>
     */
    @FindBy(id = "password")
    public WebElement inputPass;

    /**
     * WebElement representing the "Log in" button on the Odoo login page.
     * 
     * <p>This element is located using an XPath locator that identifies the button
     * by its visible text content "Log in". The XPath expression
     * {@code //button[.='Log in']} matches any button element whose text content
     * exactly equals "Log in".</p>
     * 
     * <p>This button is used to submit the login form and initiate the authentication
     * process. After entering credentials in the login and password fields, clicking
     * this button sends the authentication request to the Odoo server.</p>
     * 
     * <p><strong>Note:</strong> This uses the same locator as {@code EmployeeP.loginButton}
     * and {@code LoginP.button}, ensuring consistency across page objects that interact
     * with the login functionality.</p>
     * 
     * <p><strong>Locator:</strong> {@code @FindBy(xpath = "//button[.='Log in']")}</p>
     */
    @FindBy(xpath = "//button[.='Log in']")
    public WebElement loginButton;

}
