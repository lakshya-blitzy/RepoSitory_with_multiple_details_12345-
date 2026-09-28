package com.testinium.step_definitions;

import com.testinium.pages.LogOutP;
import com.testinium.utilities.Driver;
import org.junit.Assert;
import org.openqa.selenium.support.ui.WebDriverWait;
import io.cucumber.java.en.Then;
import org.openqa.selenium.support.ui.ExpectedConditions;

/**
 * Step Definition for the Logout flow of the Odoo/Upgenix application, bound to the steps of
 * {@code Logout.feature}.
 *
 * <p>The steps drive the Page Object {@link com.testinium.pages.LogOutP} through the
 * {@code logOutP} field: they open the user menu and click its "Log out" entry, check the title of
 * the login page, and check the warning dialog shown when navigating back after logging out.
 *
 * <p>Both fields are created in field initializers that call
 * {@link com.testinium.utilities.Driver#getDriver()}: the 3-second {@code WebDriverWait}, declared
 * first, and {@code logOutP}, whose constructor binds its elements to the same driver.
 * Instantiating this class therefore opens the current thread's browser session, or reuses the
 * one the thread already holds.
 *
 * <p>Known discrepancy: {@code User click Log out option} performs an action but is bound with
 * {@code @Then}. Cucumber matches a step by its expression regardless of the keyword, so
 * {@code Logout.feature} can use it after {@code And}. The binding is left unchanged because this
 * change adds documentation only.
 */
public class LogOutSD {


    /** Explicit wait of 3 seconds on the thread's driver. */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),3);

    /** Logout Page Object holding the user menu, "Log out" entry and warning dialog elements. */
    LogOutP logOutP = new LogOutP();
    /**
     * Opens the user menu and clicks its "Log out" entry.
     *
     * <p>Uses the 3-second {@code wait} to wait until {@code logOutP.popUpButton} (the user menu) is
     * visible, clicks it, then clicks {@code logOutP.logOutButton}. This step performs an action yet
     * is bound with {@code @Then}; see the class comment.
     * <p>
     * Gherkin: {@code User click Log out option}
     */
    @Then("User click Log out option")
    public void user_clicks_the_account_icon_and_then_click_log_out_option() {
        wait.until(ExpectedConditions.visibilityOf(logOutP.popUpButton));
        logOutP.popUpButton.click();
        logOutP.logOutButton.click();
    }

    /**
     * Verifies that the browser shows the login page after logging out.
     *
     * <p>Reads the page title from {@link com.testinium.utilities.Driver#getDriver()} and asserts
     * with {@code Assert.assertEquals} that it equals the login-page title hard-coded in this method.
     * <p>
     * Gherkin: {@code User should see the login dashboard}
     */
    @Then("User should see the login dashboard")
    public void user_should_see_the_login_dashboard() {
        String expectedDashboard = "Login | Best solution for startups";
        String actualDashboard = Driver.getDriver().getTitle();
        Assert.assertEquals("The title is not same as the expected! ", expectedDashboard, actualDashboard);
    }

    /**
     * Verifies that navigating back after logging out does not return to the home page.
     *
     * <p>Calls {@code navigate().back()} on {@link com.testinium.utilities.Driver#getDriver()}, then
     * asserts with {@code Assert.assertTrue} that {@code logOutP.warningMess}, the body of the warning
     * dialog, is displayed. The element is located lazily, so if the dialog never appears the lookup
     * throws {@code NoSuchElementException} after the driver's implicit wait rather than failing the
     * assertion.
     * <p>
     * Gherkin: {@code User can not click the step back button to go the home page}
     */
    @Then("User can not click the step back button to go the home page")
    public void user_can_not_click_the_step_back_button_to_go_the_home_page() {
        Driver.getDriver().navigate().back();
        Assert.assertTrue(logOutP.warningMess.isDisplayed());
    }
}
