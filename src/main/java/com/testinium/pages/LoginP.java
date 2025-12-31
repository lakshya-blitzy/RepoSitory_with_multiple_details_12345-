package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object class representing the Login page in the Odoo web application.
 * 
 * <p>This class provides WebElement locators for the authentication workflow including:
 * <ul>
 *   <li>Email/username input field for user identification</li>
 *   <li>Password input field for user credentials</li>
 *   <li>Login button to submit authentication request</li>
 *   <li>Password reset link for account recovery</li>
 *   <li>Post-login verification elements (dashboard navbar)</li>
 *   <li>Error state verification elements (alert messages)</li>
 * </ul>
 * 
 * <p>This class follows the Page Object Model (POM) design pattern, which encapsulates
 * page-specific locators and behaviors into a single class, promoting code reusability
 * and maintainability in test automation.
 * 
 * <p><strong>Note:</strong> This class contains duplicate password field locators
 * ({@link #inputPassword} and {@link #bulletPass}) - both use the same
 * {@code name="password"} selector and will reference the same DOM element.
 * 
 * <p>All WebElement fields are initialized via
 * {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)}
 * using the WebDriver instance obtained from {@link Driver#getDriver()}.
 * 
 * <p><strong>Usage Example:</strong>
 * <pre>{@code
 * LoginP loginPage = new LoginP();
 * loginPage.inputEmail.sendKeys("user@example.com");
 * loginPage.inputPassword.sendKeys("password123");
 * loginPage.button.click();
 * }</pre>
 * 
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.PageFactory
 * @see org.openqa.selenium.support.FindBy
 */
public class LoginP {
    
    /**
     * Constructs a new LoginP Page Object instance and initializes all WebElement fields.
     * 
     * <p>This no-argument constructor uses {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)}
     * to bind all {@link FindBy} annotated WebElement fields to their corresponding
     * DOM elements. The WebDriver instance is obtained from {@link Driver#getDriver()},
     * which provides a thread-safe, reusable browser session.
     * 
     * <p>After construction, all WebElement fields are ready for interaction,
     * though actual element lookup is deferred until the element is accessed
     * (lazy initialization via proxy).
     */
    public LoginP(){
        PageFactory.initElements(Driver.getDriver(), this);
    }

    /**
     * WebElement locator for the login/email input field on the Odoo login form.
     * 
     * <p>Uses the {@code name="login"} attribute selector, which is the standard
     * field identifier for the Odoo authentication form. This field accepts
     * either a username or email address depending on the Odoo configuration.
     * 
     * <p><strong>Locator Strategy:</strong> {@code name="login"}
     * 
     * <p><strong>Usage:</strong> Enter the user's email or username for authentication.
     * <pre>{@code
     * loginPage.inputEmail.sendKeys("user@example.com");
     * }</pre>
     */
    @FindBy(name = "login")
    public WebElement inputEmail;

    /**
     * WebElement locator for the password input field on the Odoo login form.
     * 
     * <p>Uses the {@code name="password"} attribute selector to locate the
     * password input field. This field is typically rendered with password
     * masking (bullet characters) for security.
     * 
     * <p><strong>Locator Strategy:</strong> {@code name="password"}
     * 
     * <p><strong>Note:</strong> This is a duplicate locator - the same selector
     * ({@code name="password"}) is also used by {@link #bulletPass}. Both fields
     * will reference the same DOM element.
     * 
     * <p><strong>Usage:</strong> Enter the user's password for authentication.
     * <pre>{@code
     * loginPage.inputPassword.sendKeys("secretPassword123");
     * }</pre>
     */
    @FindBy(name="password")
    public WebElement inputPassword;

    /**
     * WebElement locator for the "Log in" submit button on the Odoo login form.
     * 
     * <p>Uses an XPath expression to locate the button element by its visible
     * text content "Log in". Clicking this button submits the login form and
     * initiates the authentication process with the Odoo server.
     * 
     * <p><strong>Locator Strategy:</strong> {@code //button[.='Log in']}
     * (XPath matching button with exact text content)
     * 
     * <p><strong>Usage:</strong> Submit the login form after entering credentials.
     * <pre>{@code
     * loginPage.button.click();
     * }</pre>
     * 
     * <p><strong>Expected Behavior:</strong>
     * <ul>
     *   <li>On successful authentication: Redirects to the Odoo dashboard</li>
     *   <li>On failed authentication: Displays error message in {@link #alertErrorMessage}</li>
     * </ul>
     */
    @FindBy(xpath = "//button[.='Log in']")
    public WebElement button;

    /**
     * WebElement locator for the "Reset Password" link on the Odoo login form.
     * 
     * <p>Uses an XPath expression to locate the anchor element by its visible
     * text content "Reset Password". Clicking this link navigates the user to
     * the password recovery workflow where they can request a password reset email.
     * 
     * <p><strong>Locator Strategy:</strong> {@code //a[.='Reset Password']}
     * (XPath matching anchor with exact text content)
     * 
     * <p><strong>Usage:</strong> Navigate to password recovery page.
     * <pre>{@code
     * loginPage.resetPass.click();
     * // Wait for password reset page to load
     * }</pre>
     */
    @FindBy(xpath = "//a[.='Reset Password']")
    public WebElement resetPass;

    /**
     * WebElement locator for the main menu navbar element in the Odoo dashboard.
     * 
     * <p>Uses the {@code id="oe_main_menu_navbar"} selector to locate the primary
     * navigation element that appears only after successful authentication.
     * This element serves as a verification marker to confirm that the user
     * has successfully logged in and the dashboard has loaded.
     * 
     * <p><strong>Locator Strategy:</strong> {@code id="oe_main_menu_navbar"}
     * (ID-based, highly reliable)
     * 
     * <p><strong>Usage:</strong> Verify successful login by checking dashboard presence.
     * <pre>{@code
     * // Wait for dashboard to be visible after login
     * WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
     * wait.until(ExpectedConditions.visibilityOf(loginPage.dashboard));
     * Assert.assertTrue(loginPage.dashboard.isDisplayed());
     * }</pre>
     * 
     * <p><strong>Note:</strong> This element is only present post-authentication.
     * Attempting to access it before login will result in a NoSuchElementException.
     */
    @FindBy(id = "oe_main_menu_navbar")
    public WebElement dashboard;

    /**
     * WebElement locator for the alert container that displays login error messages.
     * 
     * <p>Uses the {@code className="alert"} selector to locate the generic alert
     * container element. This element becomes visible when login fails and
     * typically contains error messages such as:
     * <ul>
     *   <li>"Wrong login/password" for invalid credentials</li>
     *   <li>"Account locked" for security lockouts</li>
     *   <li>Other authentication failure messages</li>
     * </ul>
     * 
     * <p><strong>Locator Strategy:</strong> {@code className="alert"}
     * (CSS class-based selector)
     * 
     * <p><strong>Usage:</strong> Detect and capture login failure messages.
     * <pre>{@code
     * if (loginPage.alertErrorMessage.isDisplayed()) {
     *     String errorText = loginPage.alertErrorMessage.getText();
     *     System.out.println("Login failed: " + errorText);
     * }
     * }</pre>
     * 
     * <p><strong>Note:</strong> The generic "alert" class may match other alert
     * elements on the page. Consider using explicit waits to ensure the correct
     * alert is targeted.
     */
    @FindBy(className = "alert")
    public WebElement alertErrorMessage;

    /**
     * WebElement locator for the password input field (alternate reference).
     * 
     * <p>Uses the {@code name="password"} attribute selector, which is the same
     * locator as {@link #inputPassword}. Both WebElement fields will reference
     * the same DOM element - the password input field.
     * 
     * <p><strong>Locator Strategy:</strong> {@code name="password"}
     * 
     * <p><strong>Note:</strong> This is a <em>duplicate locator</em> for the password
     * input field. The field name "bulletPass" suggests it may have been originally
     * intended for password masking verification (checking that characters are
     * displayed as bullets), but the locator is identical to {@link #inputPassword}.
     * Both fields can be used interchangeably to interact with the password input.
     * 
     * <p><strong>Recommendation:</strong> Consider using {@link #inputPassword}
     * for standard password entry operations to maintain code clarity, and reserve
     * this field for specific password masking or visibility toggle tests if needed.
     * 
     * <p><strong>Usage:</strong> Same as inputPassword - enter password for authentication.
     * <pre>{@code
     * loginPage.bulletPass.sendKeys("password123");
     * // Verify password is masked (displayed as bullets)
     * String inputType = loginPage.bulletPass.getAttribute("type");
     * Assert.assertEquals("password", inputType);
     * }</pre>
     */
    @FindBy(name="password")
    public WebElement bulletPass;
}
