package com.testinium.step_definitions;

import com.testinium.pages.SessionP;
import com.testinium.utilities.ConfigurationReader;
import com.testinium.utilities.Driver;
import io.cucumber.java.en.When;

/**
 * Cucumber glue class providing a reusable session/login step definition for the Odoo test automation framework.
 * 
 * <p>This class implements a single {@code @When} step for authentication that can be reused across
 * multiple test scenarios requiring a logged-in state. It serves as a foundational step definition
 * that establishes authenticated sessions for subsequent feature tests.</p>
 * 
 * <h2>External Configuration Dependency</h2>
 * <p>All login credentials and URLs are externalized and retrieved from {@code configuration.properties}
 * via {@link ConfigurationReader}. This design ensures:</p>
 * <ul>
 *     <li>Credentials are not hard-coded in source control (security best practice)</li>
 *     <li>Environment-specific configurations can be easily managed</li>
 *     <li>Single point of change for credentials across all tests</li>
 * </ul>
 * 
 * <h2>Centralized Login Mechanism</h2>
 * <p>Unlike {@code EmployeeP.login()} which uses hard-coded credentials, this step definition
 * provides a centralized, configurable login mechanism. Tests requiring authenticated access
 * should use this step as a prerequisite rather than implementing separate login logic.</p>
 * 
 * <h2>Gherkin Step Binding</h2>
 * <p>The {@code @When} annotation maps the Gherkin step text "User login to test other features"
 * to the executable Java method {@link #user_login_to_test_other_features()}. This binding
 * enables feature files to invoke authentication with a simple, human-readable step.</p>
 * 
 * <h2>Usage Example in Feature File</h2>
 * <pre>{@code
 * Scenario: Verify user can access dashboard after login
 *   When User login to test other features
 *   Then user should see the dashboard
 * }</pre>
 * 
 * @see com.testinium.pages.SessionP SessionP - Associated page object containing login form locators
 * @see com.testinium.utilities.Driver Driver - WebDriver management utility for browser operations
 * @see com.testinium.utilities.ConfigurationReader ConfigurationReader - Configuration property accessor
 */
public class Session {

    /**
     * SessionP page object instance providing minimal WebElement locators for the login page.
     * 
     * <p>This page object is initialized eagerly at field declaration time and contains
     * only the essential authentication locators:</p>
     * <ul>
     *     <li>{@link SessionP#inputLogin} - Username/email input field (id="login")</li>
     *     <li>{@link SessionP#inputPass} - Password input field (id="password")</li>
     *     <li>{@link SessionP#loginButton} - Login submit button (xpath="//button[.='Log in']")</li>
     * </ul>
     * 
     * <p>This is a focused page object with only essential authentication locators,
     * following the principle of minimal page object scope for specific functionality.</p>
     * 
     * @see SessionP
     */
    SessionP session = new SessionP();

    /**
     * Performs a complete login sequence using externalized configuration properties.
     * 
     * <p>This Cucumber step method executes the following authentication workflow:</p>
     * <ol>
     *     <li><strong>Navigation:</strong> Navigates to the login URL retrieved via
     *         {@code ConfigurationReader.getProperty("web.table.url")}</li>
     *     <li><strong>Username Entry:</strong> Enters username from
     *         {@code ConfigurationReader.getProperty("username")} into the {@link SessionP#inputLogin} field</li>
     *     <li><strong>Password Entry:</strong> Enters password from
     *         {@code ConfigurationReader.getProperty("password")} into the {@link SessionP#inputPass} field</li>
     *     <li><strong>Form Submission:</strong> Clicks the {@link SessionP#loginButton}
     *         ("Log in" by visible text) to submit the authentication request</li>
     * </ol>
     * 
     * <p>This step is designed as a prerequisite for scenarios testing features that require
     * an authenticated session. It should be invoked early in test scenarios that need
     * logged-in user access to the application.</p>
     * 
     * <p><strong>Required Configuration Keys:</strong>
     * The following keys must be defined in {@code configuration.properties}:</p>
     * <table border="1">
     *     <caption>Configuration Properties</caption>
     *     <tr><th>Key</th><th>Description</th><th>Example</th></tr>
     *     <tr><td>{@code web.table.url}</td><td>The login page URL</td><td>https://app.example.com/web/login</td></tr>
     *     <tr><td>{@code username}</td><td>The login username or email</td><td>user@example.com</td></tr>
     *     <tr><td>{@code password}</td><td>The login password</td><td>********</td></tr>
     * </table>
     * 
     * <p><strong>Benefits Over Hard-Coded Login:</strong></p>
     * <ul>
     *     <li><strong>Security:</strong> Credentials are not committed to source control</li>
     *     <li><strong>Flexibility:</strong> Environment-specific configuration is easily achieved</li>
     *     <li><strong>Maintainability:</strong> Single point of change for credentials across all tests</li>
     *     <li><strong>CI/CD Integration:</strong> Configuration can be injected at runtime</li>
     * </ul>
     * 
     * @see SessionP#inputLogin Username input WebElement
     * @see SessionP#inputPass Password input WebElement
     * @see SessionP#loginButton Login button WebElement
     * @see ConfigurationReader#getProperty(String) Configuration property accessor
     */
    @When("User login to test other features")
    public void user_login_to_test_other_features() {
        Driver.getDriver().get(ConfigurationReader.getProperty("web.table.url"));
        session.inputLogin.sendKeys(ConfigurationReader.getProperty("username"));
        session.inputPass.sendKeys(ConfigurationReader.getProperty("password"));
        session.loginButton.click();
    }
}
