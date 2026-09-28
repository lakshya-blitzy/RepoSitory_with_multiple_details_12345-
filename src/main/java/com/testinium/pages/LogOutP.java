package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object (POM element container) for the user menu and logout flow of the Odoo/Upgenix ERP under test.
 *
 * <p>Each {@code public} {@code WebElement} field is annotated with {@code @FindBy} and bound by Selenium
 * {@code PageFactory} to a lazy proxy, so the element is located in the current DOM only when the field is used.
 * The step definitions in {@code com.testinium.step_definitions.LogOutSD} construct this class and drive its
 * elements; the class itself contains no waits or assertions.
 */
public class LogOutP {

    /**
     * Creates the page and initializes its {@code @FindBy} proxies by calling
     * {@code PageFactory.initElements(Driver.getDriver(), this)}.
     *
     * <p>{@link com.testinium.utilities.Driver#getDriver()} creates, or reuses, the current thread's
     * {@code WebDriver}, choosing the browser from the {@code browser} configuration key. Step classes
     * construct pages in field initializers, so constructing a page starts the browser if this thread has none yet.
     */
    public LogOutP(){
        PageFactory.initElements(Driver.getDriver(), this);
    }

    /** User menu toggle in the top bar ({@code o_user_menu}) that opens the account drop-down. */
    @FindBy(className = "o_user_menu")
    public WebElement popUpButton;

    /** "Log out" entry of the user menu. */
    @FindBy(xpath = "//a[.='Log out']")
    public WebElement logOutButton;

    /** Body of the warning dialog shown when navigating back after logging out. */
    @FindBy(xpath = "//div[@class= 'o_dialog_warning modal-body']")
    public WebElement warningMess;
}
