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
 * Step Definition for the Login module of the Odoo/Upgenix application, binding the steps of
 * {@code Login.feature}. {@code Logout.feature} also reuses the {@code @Given} step of this class in
 * its Background.
 *
 * <p>The steps drive the login form through the Login Page Object
 * {@link com.testinium.pages.LoginP} (field {@code loginP}) and use
 * {@link com.testinium.utilities.Driver#getDriver()} for browser-level actions such as navigation,
 * title checks and reading element attributes. The login page URL is read from the {@code web.table.url}
 * configuration key with {@link com.testinium.utilities.ConfigurationReader#getProperty(String)}.
 *
 * <p>Field-initializer note: {@code loginP} and the 3-second {@code WebDriverWait} ({@code wait}) both call
 * {@link com.testinium.utilities.Driver#getDriver()} in field initializers, so an instance reuses this thread's browser
 * or, if none, starts the {@code chrome} or {@code firefox} browser named by the {@code browser} key; if that key is
 * missing or holds any other value, instantiation throws {@code NullPointerException}. Cucumber's default object factory
 * creates an instance per scenario the first time it runs one of these steps; a dry run runs no step and opens no browser.
 */
public class LoginSD {

    /** Login Page Object whose form elements, dashboard bar and error alert these steps use. */
    LoginP loginP = new LoginP();
    /** Explicit wait of 3 seconds on the thread's driver. */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),3);

    /**
     * Attempts to open the Upgenix login page: navigates the thread's driver to the URL read from the required
     * {@code web.table.url} key with {@link com.testinium.utilities.ConfigurationReader#getProperty(String)}. If the
     * key is missing, {@code get(String)} receives {@code null} and throws {@code NullPointerException} without navigating.
     * The commented-out expected-title line in the body is inactive; this step performs no assertion.
     * <p>
     * Gherkin: {@code User is on the upgenix login page}
     */
    @Given("User is on the upgenix login page")
    public void user_is_on_the_upgenix_login_page() {
        //String expectedTitle = "Login | Best solution for startups";
        String url = ConfigurationReader.getProperty("web.table.url");
        Driver.getDriver().get(url);
    }

    /**
     * Types the given value into the email (username) input {@code loginP.inputEmail}.
     * <p>
     * Gherkin: {@code User enters {string} username}
     *
     * @param username the value bound to the {@code {string}} placeholder: the text typed into the
     *                 email input
     */
    @When("User enters {string} username")
    public void user_enters_username(String username) {
        loginP.inputEmail.sendKeys(username);
    }

    /**
     * Types the given value into the password input {@code loginP.inputPassword}.
     * <p>
     * Gherkin: {@code User enters {string} password}
     *
     * @param password the value bound to the {@code {string}} placeholder: the text typed into the
     *                 password input
     */
    @When("User enters {string} password")
    public void user_enters_password(String password) {
        loginP.inputPassword.sendKeys(password);
    }

    /**
     * Clicks the "Log in" button {@code loginP.button} to attempt form submission; an empty required input can block it.
     * <p>
     * Gherkin: {@code User clicks the login button}
     */
    @When("User clicks the login button")
    public void user_clicks_the_login_button() {
        loginP.button.click();
    }

    /**
     * Verifies a successful login: waits for the main menu bar {@code loginP.dashboard} to become visible, with a
     * configured 3-second timeout ({@code wait}); each check looks the bar up under the driver's 10-second implicit wait,
     * so the step can run past 3 seconds. It then asserts that the page title equals the expected title hard-coded here.
     * <p>
     * Gherkin: {@code User should see the dashboard}
     */
    @Then("User should see the dashboard")
    public void user_should_see_the_dashboard() {
        wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
        String expectedDashboard = "Odoo";
        String actualDashboard = Driver.getDriver().getTitle();
        Assert.assertEquals("The title is not same as the expected! ", expectedDashboard, actualDashboard);
    }

    /**
     * Asserts that the login error alert is displayed after the login attempt: {@code loginP.alertErrorMessage}, the first
     * {@code alert}-class element. Its text and the session state go unchecked, so this does not prove the login was rejected.
     * <p>
     * Gherkin: {@code User sees error message}
     */
    @Then("User sees error message")
    public void user_sees_error_message() {
        Assert.assertTrue(loginP.alertErrorMessage.isDisplayed());
    }

    /**
     * Verifies the browser's HTML5 form-validation text: reads the {@code validationMessage} attribute of
     * the email input, located directly with {@code By.name} on the thread's driver (the same locator as
     * {@link com.testinium.pages.LoginP#inputEmail}), and asserts that it equals {@code alertMessage}.
     * <p>
     * Naming note: the local variable {@code expectedMessage} actually holds the browser's (actual) value
     * and is passed as JUnit's expected argument, with {@code alertMessage} as the actual one, so a
     * failure message reports the two values in swapped roles.
     * <p>
     * Gherkin: {@code User sees {string} message}
     *
     * @param alertMessage the value bound to the {@code {string}} placeholder: the expected browser
     *                     validation text
     */
    @Then("User sees {string} message")
    public void user_sees_please_fill_out_this_field_message(String alertMessage) {
        String expectedMessage = Driver.getDriver().findElement(By.name("login")).getAttribute("validationMessage");
        Assert.assertEquals(expectedMessage, alertMessage);
    }

    /**
     * Verifies that the password input is masked by asserting that the {@code type} attribute of
     * {@code loginP.bulletPass} is {@code password}.
     * <p>
     * Gherkin: {@code User should see the password in bullet signs}
     */
    @Then("User should see the password in bullet signs")
    public void user_should_see_the_password_in_bullet_signs() {
        Assert.assertTrue(loginP.bulletPass.getAttribute("type").equals("password"));
    }

    /**
     * Clicks the same "Log in" button {@code loginP.button} as the login-button step.
     * <p>
     * Behavior note: despite its wording, this step sends no Enter key press; it performs a mouse click and so
     * duplicates the login-button step. The {@code Login.feature} scenario using it is intended to test the keyboard
     * Enter key, but it only checks the dashboard after this click.
     * <p>
     * Gherkin: {@code User clicks the enter button}
     */
    @When("User clicks the enter button")
    public void user_clicks_the_enter_button() {
        loginP.button.click();
    }
}
