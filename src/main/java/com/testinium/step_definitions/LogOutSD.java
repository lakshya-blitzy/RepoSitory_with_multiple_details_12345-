package com.testinium.step_definitions;

import com.testinium.pages.LogOutP;
import com.testinium.utilities.Driver;
import org.junit.Assert;
import org.openqa.selenium.support.ui.WebDriverWait;
import io.cucumber.java.en.Then;
import org.openqa.selenium.support.ui.ExpectedConditions;

/**
 * Cucumber glue class providing step definitions for logout functionality tests in the Odoo application.
 * 
 * <p>This class implements steps for the session termination workflow, including:</p>
 * <ul>
 *     <li>User menu interaction - expanding the user dropdown menu</li>
 *     <li>Logout click - clicking the "Log out" option to terminate the session</li>
 *     <li>Login page verification - asserting redirect to the login dashboard</li>
 *     <li>Back-navigation warning detection - verifying session security after logout</li>
 * </ul>
 * 
 * <p>The class uses {@code @Then} annotations to bind Gherkin step text from feature files
 * to executable Java methods, following the Cucumber BDD framework pattern.</p>
 * 
 * <p><strong>Wait Strategy:</strong> This class employs explicit waits via {@link WebDriverWait}
 * with a 3-second timeout to handle dynamic element loading during the logout process.</p>
 * 
 * <p><strong>Security Testing:</strong> A key focus of this class is testing security behavior
 * by ensuring users cannot navigate back to protected pages after logout. The warning message
 * verification step validates that browser history navigation is blocked after session termination.</p>
 * 
 * <p>This step definition class follows the Page Object Model pattern by delegating
 * UI interactions to the {@link LogOutP} page object class.</p>
 * 
 * @see com.testinium.pages.LogOutP
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.ui.WebDriverWait
 * @see io.cucumber.java.en.Then
 */
public class LogOutSD {


    /**
     * WebDriverWait instance configured for explicit waits with a 3-second timeout.
     * 
     * <p>This wait object is used to synchronize test execution with dynamic UI elements,
     * particularly waiting for the user menu button to become visible before interaction.</p>
     * 
     * <p><strong>Note:</strong> The wait is initialized at field declaration time using
     * {@link Driver#getDriver()}, which couples object instantiation to driver availability.
     * This means the WebDriver must be initialized before this class is instantiated.</p>
     * 
     * @see Driver#getDriver()
     * @see org.openqa.selenium.support.ui.ExpectedConditions
     */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),3);

    /**
     * LogOutP page object instance providing WebElement locators for logout functionality UI interactions.
     * 
     * <p>This page object encapsulates the following UI elements:</p>
     * <ul>
     *     <li>{@link LogOutP#popUpButton} - User menu button (class: o_user_menu)</li>
     *     <li>{@link LogOutP#logOutButton} - Logout link (xpath: //a[.='Log out'])</li>
     *     <li>{@link LogOutP#warningMess} - Warning dialog for session expiration (class: o_dialog_warning)</li>
     * </ul>
     * 
     * <p>The page object is initialized eagerly at field declaration, which triggers
     * PageFactory.initElements() to bind WebElement fields to their locators.</p>
     * 
     * @see LogOutP
     */
    LogOutP logOutP = new LogOutP();

    /**
     * Executes the complete logout sequence for the Odoo application.
     * 
     * <p>This step definition is bound to the Gherkin step: <strong>"User click Log out option"</strong></p>
     * 
     * <p>The method performs the following actions in sequence:</p>
     * <ol>
     *     <li>Waits for the user menu button (o_user_menu) to become visible using explicit wait</li>
     *     <li>Clicks the {@link LogOutP#popUpButton} to expand the user dropdown menu</li>
     *     <li>Clicks the {@link LogOutP#logOutButton} ("Log out" link) to terminate the session</li>
     * </ol>
     * 
     * <p>Upon successful execution, the user is redirected to the login page,
     * completing the session termination workflow.</p>
     * 
     * @see LogOutP#popUpButton
     * @see LogOutP#logOutButton
     * @see org.openqa.selenium.support.ui.ExpectedConditions#visibilityOf
     */
    @Then("User click Log out option")
    public void user_clicks_the_account_icon_and_then_click_log_out_option() {
        wait.until(ExpectedConditions.visibilityOf(logOutP.popUpButton));
        logOutP.popUpButton.click();
        logOutP.logOutButton.click();
    }

    /**
     * Verifies successful logout by asserting the page title matches the expected login page title.
     * 
     * <p>This step definition is bound to the Gherkin step: <strong>"User should see the login dashboard"</strong></p>
     * 
     * <p>The method retrieves the current page title using {@link Driver#getDriver()}.getTitle()
     * and compares it against the expected login page title.</p>
     * 
     * <p><strong>Expected title:</strong> "Login | Best solution for startups"</p>
     * 
     * <p><strong>Note:</strong> The expected title text suggests Upgenix/startup-themed branding
     * for the application under test. If the title does not match, a custom assertion message
     * is provided: "The title is not same as the expected!"</p>
     * 
     * @throws AssertionError if the actual page title does not match the expected title
     * @see Driver#getDriver()
     * @see org.junit.Assert#assertEquals
     */
    @Then("User should see the login dashboard")
    public void user_should_see_the_login_dashboard() {
        String expectedDashboard = "Login | Best solution for startups";
        String actualDashboard = Driver.getDriver().getTitle();
        Assert.assertEquals("The title is not same as the expected! ", expectedDashboard, actualDashboard);
    }

    /**
     * Tests session security by verifying users cannot access protected pages via browser back navigation after logout.
     * 
     * <p>This step definition is bound to the Gherkin step: 
     * <strong>"User can not click the step back button to go the home page"</strong></p>
     * 
     * <p>The method performs the following security validation:</p>
     * <ol>
     *     <li>Uses browser back navigation via {@link Driver#getDriver()}.navigate().back()</li>
     *     <li>Asserts that a warning message dialog is displayed (indicating session expired/invalid)</li>
     * </ol>
     * 
     * <p>This validates that users cannot access protected pages via browser history
     * after their session has been terminated through logout. The warning message element
     * uses the CSS class {@code o_dialog_warning} to identify the session expiration dialog.</p>
     * 
     * @throws AssertionError if the warning message dialog is not displayed after back navigation
     * @see LogOutP#warningMess
     * @see Driver#getDriver()
     * @see org.junit.Assert#assertTrue
     */
    @Then("User can not click the step back button to go the home page")
    public void user_can_not_click_the_step_back_button_to_go_the_home_page() {
        Driver.getDriver().navigate().back();
        Assert.assertTrue(logOutP.warningMess.isDisplayed());
    }
}
