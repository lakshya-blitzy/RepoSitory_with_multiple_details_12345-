package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object (POM element container) for the login page and post-login dashboard of the Odoo/Upgenix ERP under test.
 *
 * <p>Each {@code public} {@code WebElement} field is annotated with {@code @FindBy} and bound by Selenium
 * {@code PageFactory} to a lazy proxy, so the element is located in the current DOM only when the field is used.
 * The step definitions in {@code com.testinium.step_definitions.LoginSD} construct this class and drive its
 * elements; the class itself contains no waits or assertions.
 */
public class LoginP {
    /**
     * Creates the page and initializes its {@code @FindBy} proxies by calling
     * {@code PageFactory.initElements(Driver.getDriver(), this)}.
     *
     * <p>{@link com.testinium.utilities.Driver#getDriver()} creates, or reuses, the current thread's
     * {@code WebDriver}, choosing the browser from the {@code browser} configuration key. Step classes
     * construct pages in field initializers, so constructing a page starts the browser if this thread has none yet.
     */
    public LoginP(){
        PageFactory.initElements(Driver.getDriver(), this);
    }

    /** Email (login) input of the login form ({@code name="login"}). */
    @FindBy(name = "login")
    public WebElement inputEmail;

    /** Password input of the login form ({@code name="password"}). */
    @FindBy(name="password")
    public WebElement inputPassword;

    /** "Log in" button of the login form. */
    @FindBy(xpath = "//button[.='Log in']")
    public WebElement button;

    /** "Reset Password" link; not referenced by the current step definitions. */
    @FindBy(xpath = "//a[.='Reset Password']")
    public WebElement resetPass;

    /** Main menu navigation bar ({@code id="oe_main_menu_navbar"}) shown after a successful login. */
    @FindBy(id = "oe_main_menu_navbar")
    public WebElement dashboard;

    /** Alert element ({@code class="alert"}) shown when login fails. */
    @FindBy(className = "alert")
    public WebElement alertErrorMessage;

    /** Same password input as {@link #inputPassword} (duplicate locator), used to check that input is masked by {@code type="password"}. */
    @FindBy(name="password")
    public WebElement bulletPass;
}
