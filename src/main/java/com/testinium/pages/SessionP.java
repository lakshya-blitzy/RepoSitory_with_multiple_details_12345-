package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object (POM element container) for the login form of the Odoo/Upgenix ERP under test, used by the shared
 * login step that other features run first.
 *
 * <p>Each {@code public} {@code WebElement} field is annotated with {@code @FindBy} and bound by Selenium
 * {@code PageFactory} to a lazy proxy, so the element is located in the current DOM only when the field is used.
 * The step definitions in {@code com.testinium.step_definitions.Session} construct this class and fill it from the
 * {@code username} and {@code password} configuration keys; the class itself contains no waits or assertions.
 */
public class SessionP {

    /**
     * Creates the page and initializes its {@code @FindBy} proxies by calling
     * {@code PageFactory.initElements(Driver.getDriver(), this)}. Step classes construct pages in field initializers.
     *
     * <p>{@link Driver#getDriver()} reuses this thread's {@code WebDriver}; with none, it starts one only if the {@code browser}
     * key is {@code chrome} or {@code firefox}, and a failed start throws. Any other value binds the proxies to a {@code null} driver,
     * so using an element throws {@code NullPointerException}; a missing key or configuration file makes this constructor throw it.
     */
    public SessionP(){
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

}
