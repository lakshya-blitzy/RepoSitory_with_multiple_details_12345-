package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object class representing the logout functionality in the Odoo web application.
 * 
 * <p>This class provides locators for the session termination workflow, including:
 * <ul>
 *   <li>User menu trigger button</li>
 *   <li>Logout link within the dropdown menu</li>
 *   <li>Warning dialog handling for unsaved changes</li>
 * </ul>
 * 
 * <p>This class follows the Page Object Model (POM) design pattern, encapsulating
 * all logout-related UI elements in a single, reusable class. It is intentionally
 * minimal with only 3 WebElement fields, providing focused functionality for
 * session termination operations.
 * 
 * <p>All WebElement fields are initialized via 
 * {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)} 
 * using the active WebDriver instance obtained from {@link Driver#getDriver()}.
 * 
 * <p>Usage example:
 * <pre>{@code
 * LogOutP logOutPage = new LogOutP();
 * logOutPage.popUpButton.click();
 * logOutPage.logOutButton.click();
 * }</pre>
 * 
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.PageFactory
 */
public class LogOutP {

    /**
     * Constructs a new LogOutP Page Object instance.
     * 
     * <p>This no-argument constructor initializes all {@link FindBy} annotated 
     * WebElement fields using Selenium's PageFactory pattern. The 
     * {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)} 
     * method binds the locators defined in this class to the active WebDriver 
     * instance retrieved from {@link Driver#getDriver()}.
     * 
     * <p>After construction, all WebElement fields (popUpButton, logOutButton, 
     * warningMess) are ready for interaction without additional initialization.
     */
    public LogOutP(){
        PageFactory.initElements(Driver.getDriver(), this);
    }

    /**
     * WebElement representing the user menu dropdown trigger button.
     * 
     * <p>Uses class-based locator targeting the {@code o_user_menu} CSS class,
     * which is the Odoo standard user menu button located in the navigation bar.
     * Clicking this element reveals the user settings dropdown menu containing
     * the logout option and other user-related settings.
     * 
     * <p>Locator strategy: {@code className = "o_user_menu"}
     */
    @FindBy(className = "o_user_menu")
    public WebElement popUpButton;

    /**
     * WebElement representing the logout link within the user menu dropdown.
     * 
     * <p>Uses XPath locator to find the anchor element by its visible text 'Log out'.
     * This element is located within the user menu dropdown that appears after
     * clicking the {@link #popUpButton}. Clicking this element initiates session
     * termination and redirects the user to the login page.
     * 
     * <p>Locator strategy: {@code xpath = "//a[.='Log out']"}
     * 
     * <p><strong>Note:</strong> Ensure the user menu dropdown is visible before
     * interacting with this element.
     */
    @FindBy(xpath = "//a[.='Log out']")
    public WebElement logOutButton;

    /**
     * WebElement representing the warning dialog modal body.
     * 
     * <p>Uses XPath locator targeting the combination of {@code o_dialog_warning}
     * and {@code modal-body} CSS classes. This element is used to detect and
     * handle any warning dialogs that may appear during the logout process,
     * such as prompts about unsaved changes or active sessions.
     * 
     * <p>Locator strategy: {@code xpath = "//div[@class= 'o_dialog_warning modal-body']"}
     * 
     * <p><strong>Note:</strong> This element may not always be present. Check for
     * its existence before interaction when warning dialogs are expected.
     */
    @FindBy(xpath = "//div[@class= 'o_dialog_warning modal-body']")
    public WebElement warningMess;
}
