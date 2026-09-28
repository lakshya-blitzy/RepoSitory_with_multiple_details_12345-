package com.testinium.step_definitions;

import com.testinium.pages.SessionP;
import com.testinium.utilities.ConfigurationReader;
import com.testinium.utilities.Driver;
import io.cucumber.java.en.When;

/**
 * Step Definition providing the shared login step that other feature files reuse before they
 * exercise their own module.
 *
 * <p>{@code Calendar.feature}, {@code Contact.feature}, {@code Crm.feature},
 * {@code Inventory.feature}, {@code Notes.feature} and {@code Sales.feature} run
 * {@link #user_login_to_test_other_features()} in their Background sections, and
 * {@code Session.feature} runs it as its only step. The method is annotated with {@code @When},
 * but Cucumber matches steps by their text rather than their keyword, so the Background
 * sections call it with {@code Given}.
 *
 * <p>The step drives the login form through the {@link com.testinium.pages.SessionP} Page Object
 * held in the {@code session} field. That field is created in a field initializer, and the
 * {@code SessionP} constructor calls {@link com.testinium.utilities.Driver#getDriver()}, so when
 * Cucumber instantiates this class for a scenario, the current thread's browser session is opened
 * or reused.
 *
 * <p>The class uses no {@code WebDriverWait} and declares no constructor.
 */
public class Session {

    /** Session (login) Page Object bound to the current thread's driver. */
    SessionP session = new SessionP();

    /**
     * Logs in to the application under test with the configured account.
     *
     * <p>The step navigates the current thread's driver to the URL stored under the
     * {@code web.table.url} key. It then types the values of the {@code username} and
     * {@code password} keys, read with
     * {@link com.testinium.utilities.ConfigurationReader#getProperty(String)}, into the login and
     * password fields, and clicks the login button.
     *
     * <p>The step performs no wait or assertion on the result, so it does not verify that the login
     * succeeded; a failed login surfaces only in the steps that follow.
     *
     * <p>
     * Gherkin: {@code User login to test other features}
     */
    @When("User login to test other features")
    public void user_login_to_test_other_features() {
        Driver.getDriver().get(ConfigurationReader.getProperty("web.table.url"));
        session.inputLogin.sendKeys(ConfigurationReader.getProperty("username"));
        session.inputPass.sendKeys(ConfigurationReader.getProperty("password"));
        session.loginButton.click();
    }
}
