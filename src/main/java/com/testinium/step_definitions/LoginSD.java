package com.testinium.step_definitions;

import com.testinium.pages.LoginP;
import com.testinium.utilities.ConfigurationReader;
import com.testinium.utilities.Driver;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Cucumber step definitions class providing glue code for login functionality tests
 * in the Odoo web application.
 * 
 * <p>This class implements step definitions for the following authentication scenarios:</p>
 * <ul>
 *   <li>Successful login with dashboard verification - validates user authentication
 *       and subsequent navigation to the Odoo dashboard</li>
 *   <li>Invalid credentials handling with error message display - verifies appropriate
 *       error feedback when authentication fails</li>
 *   <li>HTML5 validation message assertion for empty fields - tests browser-native
 *       form validation using the validationMessage attribute</li>
 *   <li>Password masking verification - confirms password input field displays
 *       bullet signs instead of plain text for security</li>
 * </ul>
 * 
 * <p>The step methods use Gherkin annotations ({@code @Given}, {@code @When}, {@code @Then})
 * to bind Cucumber feature file steps to executable Java methods. Each annotation's value
 * specifies the step text pattern to match, with parameters enclosed in curly braces
 * (e.g., {@code {string}}) for parameterized steps.</p>
 * 
 * <p>Configuration and Dependencies:</p>
 * <ul>
 *   <li>Uses {@link ConfigurationReader} for externalized URL configuration,
 *       allowing test environment URLs to be managed outside the codebase</li>
 *   <li>Employs explicit waits via {@link WebDriverWait} with a 3-second timeout
 *       to handle dynamic page loading and element visibility</li>
 *   <li>Leverages HTML5 {@code validationMessage} attribute for testing browser-native
 *       form validation behavior (note: messages may vary by browser)</li>
 * </ul>
 * 
 * @see com.testinium.pages.LoginP
 * @see com.testinium.utilities.Driver
 * @see com.testinium.utilities.ConfigurationReader
 */
public class LoginSD {

    /**
     * Page Object instance providing WebElement locators and interactions for the
     * login page UI components.
     * 
     * <p>This field provides access to the following login page elements:</p>
     * <ul>
     *   <li>{@code inputEmail} - Email/username input field (name="login")</li>
     *   <li>{@code inputPassword} - Password input field (name="password")</li>
     *   <li>{@code button} - "Log in" submit button</li>
     *   <li>{@code alertErrorMessage} - Error message alert element (class="alert")</li>
     *   <li>{@code dashboard} - Dashboard navbar marker (id="oe_main_menu_navbar")</li>
     *   <li>{@code bulletPass} - Password field for type attribute verification</li>
     * </ul>
     * 
     * <p>Initialized eagerly at field declaration time, which triggers PageFactory
     * element initialization when this step definitions class is instantiated.</p>
     * 
     * @see com.testinium.pages.LoginP
     */
    LoginP loginP = new LoginP();

    /**
     * WebDriverWait instance configured for explicit waits with a 3-second timeout.
     * 
     * <p>Used to wait for specific conditions (e.g., element visibility) before
     * proceeding with assertions or interactions. This helps handle timing issues
     * with dynamic page content and AJAX-loaded elements.</p>
     * 
     * <p>Note: This field is initialized at declaration time using
     * {@link Driver#getDriver()}, which couples the instantiation of this
     * step definitions class to WebDriver availability. The driver must be
     * initialized before this class is instantiated by Cucumber.</p>
     * 
     * @see org.openqa.selenium.support.ui.WebDriverWait
     * @see com.testinium.utilities.Driver#getDriver()
     */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),3);

    /**
     * Navigates the browser to the Upgenix/Odoo login page.
     * 
     * <p>This step is typically the entry point for login-related test scenarios,
     * establishing the initial state by navigating to the application's login URL.</p>
     * 
     * <p>The URL is retrieved from the external configuration file via
     * {@link ConfigurationReader#getProperty(String)} using the key
     * {@code "web.table.url"}. This allows the test environment URL to be
     * changed without modifying the source code.</p>
     * 
     * <p>Implementation note: Contains commented-out code for expected title
     * verification which may be enabled for additional validation if needed.</p>
     * 
     * @see ConfigurationReader#getProperty(String)
     */
    @Given("User is on the upgenix login page")
    public void user_is_on_the_upgenix_login_page() {
        //String expectedTitle = "Login | Best solution for startups";
        String url = ConfigurationReader.getProperty("web.table.url");
        Driver.getDriver().get(url);
    }

    /**
     * Enters the specified username/email into the login form's email input field.
     * 
     * <p>This parameterized step accepts a username value from the Cucumber feature
     * file and sends it directly to the email input field without any transformation
     * or validation. The input field is located by the {@code name="login"} attribute.</p>
     * 
     * <p>Example Gherkin usage:</p>
     * <pre>
     *   When User enters "user@example.com" username
     * </pre>
     * 
     * @param username the username or email address to enter in the login form,
     *                 passed from the Cucumber step parameter (enclosed in quotes
     *                 in the feature file)
     * @see LoginP#inputEmail
     */
    @When("User enters {string} username")
    public void user_enters_username(String username) {
        loginP.inputEmail.sendKeys(username);
    }

    /**
     * Enters the specified password into the login form's password input field.
     * 
     * <p>This parameterized step accepts a password value from the Cucumber feature
     * file and sends it directly to the password input field. The input field is
     * located by the {@code name="password"} attribute and is configured with
     * {@code type="password"} to mask the entered characters.</p>
     * 
     * <p>Example Gherkin usage:</p>
     * <pre>
     *   When User enters "secretPassword123" password
     * </pre>
     * 
     * @param password the password to enter in the login form, passed from the
     *                 Cucumber step parameter (enclosed in quotes in the feature file)
     * @see LoginP#inputPassword
     */
    @When("User enters {string} password")
    public void user_enters_password(String password) {
        loginP.inputPassword.sendKeys(password);
    }

    /**
     * Clicks the "Log in" button to submit the login form.
     * 
     * <p>This step initiates the authentication request by clicking the login
     * button, which submits the form with the previously entered credentials.
     * After clicking, the application will either navigate to the dashboard
     * (on success) or display an error message (on failure).</p>
     * 
     * <p>The button is located using an XPath expression matching the button
     * element containing the text "Log in".</p>
     * 
     * @see LoginP#button
     */
    @When("User clicks the login button")
    public void user_clicks_the_login_button() {
        loginP.button.click();
    }

    /**
     * Verifies successful login by checking for dashboard elements and page title.
     * 
     * <p>This assertion step validates that the user has successfully authenticated
     * and reached the Odoo dashboard by performing two checks:</p>
     * <ol>
     *   <li>Waits for the dashboard navbar element ({@code id="oe_main_menu_navbar"})
     *       to become visible, indicating the dashboard has loaded</li>
     *   <li>Asserts that the page title equals "Odoo", confirming navigation to
     *       the correct application page</li>
     * </ol>
     * 
     * <p>The explicit wait ensures the dashboard has fully loaded before the
     * title assertion is performed, preventing false failures due to page
     * load timing.</p>
     * 
     * <p>A custom assertion message "The title is not same as the expected!"
     * is provided to aid in debugging test failures.</p>
     * 
     * @see LoginP#dashboard
     */
    @Then("User should see the dashboard")
    public void user_should_see_the_dashboard() {
        wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
        String expectedDashboard = "Odoo";
        String actualDashboard = Driver.getDriver().getTitle();
        Assert.assertEquals("The title is not same as the expected! ", expectedDashboard, actualDashboard);
    }

    /**
     * Verifies that a login failure error message is displayed.
     * 
     * <p>This assertion step validates that the application displays an error
     * message when login fails (e.g., due to invalid credentials). The error
     * message element is identified by the CSS class {@code "alert"}.</p>
     * 
     * <p>The assertion uses {@link org.openqa.selenium.WebElement#isDisplayed()}
     * to verify the element is visible on the page. This step is typically used
     * in negative test scenarios to confirm proper error handling.</p>
     * 
     * @see LoginP#alertErrorMessage
     */
    @Then("User sees error message")
    public void user_sees_error_message() {
        Assert.assertTrue(loginP.alertErrorMessage.isDisplayed());
    }

    /**
     * Verifies the HTML5 browser validation message for empty or invalid form fields.
     * 
     * <p>This step tests the browser-native form validation by retrieving the
     * {@code validationMessage} attribute from the login input element and
     * comparing it against the expected message. HTML5 form validation is
     * triggered when required fields are empty or contain invalid data.</p>
     * 
     * <p>The validation message is retrieved from the element located by
     * {@code name="login"}, which is the username/email input field.</p>
     * 
     * <p>Example Gherkin usage:</p>
     * <pre>
     *   Then User sees "Please fill out this field." message
     * </pre>
     * 
     * <p><strong>Important:</strong> HTML5 validation messages are browser-dependent
     * and may vary between browsers (Chrome, Firefox, Edge, etc.) and browser
     * locales. Tests using this step should account for browser-specific message text.</p>
     * 
     * @param alertMessage the expected HTML5 validation message text, such as
     *                     "Please fill out this field." (exact text varies by browser)
     */
    @Then("User sees {string} message")
    public void user_sees_please_fill_out_this_field_message(String alertMessage) {
        String expectedMessage = Driver.getDriver().findElement(By.name("login")).getAttribute("validationMessage");
        Assert.assertEquals(expectedMessage, alertMessage);
    }

    /**
     * Verifies that the password input field masks characters (displays bullet signs).
     * 
     * <p>This security verification step ensures that the password input field
     * is properly configured to hide the entered password. It asserts that the
     * {@code type} attribute of the password input element equals {@code "password"},
     * which causes browsers to display masked characters (bullets or asterisks)
     * instead of the actual password text.</p>
     * 
     * <p>This test validates a critical security requirement: user credentials
     * must not be visible to observers when entered into the login form.</p>
     * 
     * <p>The assertion reads the {@code type} attribute from the {@code bulletPass}
     * WebElement (located by {@code name="password"}) and verifies it equals
     * the string "password".</p>
     * 
     * @see LoginP#bulletPass
     */
    @Then("User should see the password in bullet signs")
    public void user_should_see_the_password_in_bullet_signs() {
        Assert.assertTrue(loginP.bulletPass.getAttribute("type").equals("password"));
    }

    /**
     * Alternative step for clicking the login button using different Gherkin wording.
     * 
     * <p>This step provides an alternative Gherkin step text ("User clicks the enter button")
     * that maps to the same action as {@link #user_clicks_the_login_button()}.
     * Both steps click the same login button element to submit the form.</p>
     * 
     * <p>This duplicate functionality allows feature file authors to use either
     * "User clicks the login button" or "User clicks the enter button" based on
     * the scenario context and preferred terminology.</p>
     * 
     * <p><strong>Note:</strong> This method performs the same action as
     * {@link #user_clicks_the_login_button()}. Consider using that method
     * for consistency, or refactoring both methods to call a shared private
     * helper method to reduce code duplication.</p>
     * 
     * @see #user_clicks_the_login_button()
     * @see LoginP#button
     */
    @When("User clicks the enter button")
    public void user_clicks_the_enter_button() {
        loginP.button.click();
    }
}
