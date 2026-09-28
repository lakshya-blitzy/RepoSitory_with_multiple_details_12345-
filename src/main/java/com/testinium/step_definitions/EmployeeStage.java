package com.testinium.step_definitions;

import com.testinium.pages.EmployeeP;
import com.testinium.utilities.ConfigurationReader;
import com.testinium.utilities.Driver;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Step Definition for the Employees module of the Odoo/Upgenix application, binding the steps of
 * {@code EmployeeFc.feature}.
 *
 * <p>The steps log in, navigate the Employees, Badges, Challenges, Goals History and Departments
 * stages, create an employee and edit an employee's name. Every UI element comes from the
 * {@link com.testinium.pages.EmployeeP} Page Object held in {@code employeePage}; navigation and
 * title checks go through {@link com.testinium.utilities.Driver#getDriver()}.
 *
 * <p>Configuration keys read through
 * {@link com.testinium.utilities.ConfigurationReader#getProperty(String)} (names only):
 * <ul>
 *   <li>{@code web.table.url}: start URL opened by {@link #user_is_on_upgenix_login_page()}.</li>
 *   <li>{@code url}: application URL opened before logging in.</li>
 *   <li>{@code EmplTitle}: Employees page title awaited by {@link #user_clicks_employees_stage()}.</li>
 * </ul>
 * Logging in delegates to {@link com.testinium.pages.EmployeeP#login()}, which uses credentials
 * defined in that Page Object rather than configuration keys. The other title checks compare
 * against titles hard-coded in this class.
 *
 * <p>Instantiation: {@code employeePage} and the 3-second {@code WebDriverWait} are created in field
 * initializers calling {@link com.testinium.utilities.Driver#getDriver()}, so creating an instance reuses the
 * thread's session, or starts one if the {@code browser} key is {@code chrome} or {@code firefox}. With no
 * session and any other or absent key, or a failed start, creation throws. The class declares no constructor.
 *
 * <p>Synchronization: fixed {@code Thread.sleep} pauses of 3 to 7 seconds are used alongside the
 * explicit waits on {@code wait} and the 10-second implicit wait set by
 * {@link com.testinium.utilities.Driver#getDriver()}.
 */
public class EmployeeStage {
    /** Employees Page Object; its constructor binds the {@code @FindBy} elements to the thread's driver. */
    EmployeeP employeePage = new EmployeeP();
    /** Explicit wait of 3 seconds on the thread's driver. */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),3);

    /**
     * Opens the start page at the {@code web.table.url} configuration value. The phrase differs
     * from the {@code User is on the upgenix login page} step of
     * {@link com.testinium.step_definitions.LoginSD}, and no committed feature file uses it.
     * <p>
     * Gherkin: {@code User is on upgenix login page}
     */
    @When("User is on upgenix login page")
    public void user_is_on_upgenix_login_page() {
        String url = ConfigurationReader.getProperty("web.table.url");
        Driver.getDriver().get(url);
    }

    /**
     * Opens the application at the {@code url} configuration value and logs in through
     * {@link com.testinium.pages.EmployeeP#login()}.
     * <p>
     * Gherkin: {@code User is on the dashboard}
     */
    @When("User is on the dashboard")
    public void user_is_on_the_dashboard() {
        Driver.getDriver().get(ConfigurationReader.getProperty("url"));
        employeePage.login();
    }

    /**
     * Clicks the Employees menu link ({@code employeePage.emplStage}), waits up to 3 seconds until
     * the page title equals the {@code EmplTitle} configuration value, then asserts the title against
     * a hard-coded Employees title rather than the configured one.
     * <p>
     * Gherkin: {@code User clicks Employees stage}
     */
    @When("User clicks Employees stage")
    public void user_clicks_employees_stage() {
        employeePage.emplStage.click();
        wait.until(ExpectedConditions.titleIs(ConfigurationReader.getProperty("EmplTitle")));
        Assert.assertTrue(Driver.getDriver().getTitle().equals("Employees - Odoo"));
    }

    /**
     * Clicks the Badges, Challenges and Goals History menu links ({@code badgesBtn}, {@code challengesBtn}
     * and {@code goalsHistoryBtn}) in turn; after each click it waits for the link just clicked to be visible,
     * using {@code wait}, configured for 3 seconds; the 10-second implicit wait on each lookup can extend it.
     * <p>
     * Gherkin: {@code User clicks Challenges stage}
     */
    @When("User clicks Challenges stage")
    public void user_clicks_challenges_stage() {
        employeePage.badgesBtn.click();
        wait.until(ExpectedConditions.visibilityOf(employeePage.badgesBtn));
        employeePage.challengesBtn.click();
        wait.until(ExpectedConditions.visibilityOf(employeePage.challengesBtn));
        employeePage.goalsHistoryBtn.click();
        wait.until(ExpectedConditions.visibilityOf(employeePage.goalsHistoryBtn));
    }

    /**
     * Clicks the Departments menu link ({@code departmentsBtn}), then pauses for a fixed 7 seconds.
     * <p>
     * Gherkin: {@code User clicks Departments stage}
     *
     * @throws InterruptedException if the thread is interrupted during the fixed pause
     */
    @When("User clicks Departments stage")
    public void user_clicks_departments_stage() throws InterruptedException {
        employeePage.departmentsBtn.click();
        Thread.sleep(7000);
    }
    /**
     * Asserts that the page title equals a hard-coded Departments title. An alternative
     * {@code assertEquals} check of the same title is commented out below the assertion and does
     * not run.
     * <p>
     * Gherkin: {@code User should see the last stage title}
     */
    @Then("User should see the last stage title")
    public void user_should_see_the_last_stage_title() {
        Assert.assertTrue(Driver.getDriver().getTitle().equals("Departments - Odoo"));
        //String act = Driver.getDriver().getTitle();
        //String exp = "Departments - Odoo";
        //Assert.assertEquals(exp,act);
    }

    /**
     * Opens the application at the {@code url} configuration value, logs in through
     * {@link com.testinium.pages.EmployeeP#login()}, pauses for a fixed 3 seconds, then clicks the
     * Employees menu link ({@code emplStage}).
     * <p>
     * Gherkin: {@code User is on the employees dashboard}
     *
     * @throws InterruptedException if the thread is interrupted during the fixed pause
     */
    @When("User is on the employees dashboard")
    public void user_is_on_the_employees_dashboard() throws InterruptedException {
        Driver.getDriver().get(ConfigurationReader.getProperty("url"));
        employeePage.login();
        Thread.sleep(3000);
        employeePage.emplStage.click();
    }

    /**
     * Creates an employee: pauses 3 seconds, clicks Create ({@code createBtn}), pauses 3 seconds,
     * waits up to 3 seconds for the hard-coded new-record page title, types {@code name} into
     * {@code employeesName}, then clicks the Save button ({@code savedMessage}).
     * <p>
     * Gherkin: {@code User creates new employees {string} in the Employees stage}
     *
     * @param name the employee name bound to {@code {string}}; {@code EmployeeFc.feature} supplies it
     *             from the {@code name} column of each scenario outline's examples
     * @throws InterruptedException if the thread is interrupted during a fixed pause
     */
    @When("User creates new employees {string} in the Employees stage")
    public void user_creates_new_employees_in_the_employees_stage(String name) throws InterruptedException {
        Thread.sleep(3000);
        employeePage.createBtn.click();
        Thread.sleep(3000);
        wait.until(ExpectedConditions.titleIs("New - Odoo"));
        employeePage.employeesName.sendKeys(name);
        employeePage.savedMessage.click();
    }

    /**
     * Asserts that the Employee created confirmation ({@code employeePage.createdMessage}) is
     * displayed. A check that its text equals the expected message is commented out below the
     * assertion and does not run.
     * <p>
     * Gherkin: {@code User should see the Employee created message under full profile}
     */
    @Then("User should see the Employee created message under full profile")
    public void user_should_see_the_message_under_full_profile() {
        Assert.assertTrue(employeePage.createdMessage.isDisplayed());
        //String expected = "Employee created";
        //String actual = employeePage.createdMessage.getText();
        //Assert.assertEquals(expected,actual);
    }

    /**
     * Clicks the Employees menu link ({@code emplStage}), waits up to 3 seconds for the hard-coded
     * Employees page title, then asserts that title. It does not check that the created employee
     * appears in the list.
     * <p>
     * Gherkin: {@code User should see listed employees in the Employees stage}
     *
     * @throws InterruptedException declared by the signature but never thrown, because the body
     *         calls no {@code Thread.sleep}
     */
    @Then("User should see listed employees in the Employees stage")
    public void user_should_see_listed_employees_in_the_employees_stage() throws InterruptedException {
        employeePage.emplStage.click();
        wait.until(ExpectedConditions.titleIs("Employees - Odoo"));
        Assert.assertTrue(Driver.getDriver().getTitle().equals("Employees - Odoo"));
    }

    /**
     * Opens the application at the {@code url} configuration value, logs in through
     * {@link com.testinium.pages.EmployeeP#login()}, then opens the Employees menu link
     * ({@code emplStage}), an employee record ({@code chooseEmployee}) and its Edit button
     * ({@code editEmployee}). It clears the name input ({@code nameEdit}), types a hard-coded name
     * and clicks the Save button ({@code savedMessage}). Four fixed 3-second pauses separate these
     * actions. The record is the one {@code chooseEmployee}'s absolute XPath locates; it is not
     * looked up by the name of the employee created earlier.
     * <p>
     * Gherkin: {@code User edits created employees in the Employees module}
     *
     * @throws InterruptedException if the thread is interrupted during a fixed pause
     */
    @When("User edits created employees in the Employees module")
    public void user_edits_created_employees_in_the_employees_module() throws InterruptedException {
        Driver.getDriver().get(ConfigurationReader.getProperty("url"));
        employeePage.login();
        Thread.sleep(3000);
        employeePage.emplStage.click();
        Thread.sleep(3000);
        employeePage.chooseEmployee.click();
        employeePage.editEmployee.click();
        Thread.sleep(3000);
        employeePage.nameEdit.clear();
        employeePage.nameEdit.sendKeys("Sterling");
        Thread.sleep(3000);
        employeePage.savedMessage.click();
    }

    /**
     * Only clicks the Employees menu link ({@code emplStage}). It does not assert the edited name,
     * so it cannot detect a failed edit.
     * <p>
     * Gherkin: {@code User should see the edited name in the Employees module}
     */
    @Then("User should see the edited name in the Employees module")
    public void user_should_see_the_edited_name_in_the_employees_module() {
        employeePage.emplStage.click();
    }


}