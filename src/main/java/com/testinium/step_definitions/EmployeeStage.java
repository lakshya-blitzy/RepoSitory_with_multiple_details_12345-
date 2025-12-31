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
 * Cucumber glue class providing step definitions for Employee module tests in the Odoo application.
 * 
 * <p>This class implements step definitions for comprehensive employee management test scenarios,
 * including:
 * <ul>
 *   <li>Login and navigation using configured URLs from configuration.properties</li>
 *   <li>Employee listing and verification</li>
 *   <li>Employee creation with parameterized name input</li>
 *   <li>Editing existing employee records</li>
 *   <li>Department and gamification module navigation (Badges, Challenges, Goals History)</li>
 * </ul>
 * 
 * <p>The class uses Gherkin step bindings via {@code @When} and {@code @Then} annotations
 * that map human-readable step text from feature files to executable Java methods.
 * 
 * <p><strong>Configuration:</strong> This class relies on {@link ConfigurationReader} for
 * externalized URLs and credentials, allowing test configuration without code changes.
 * Key properties used include:
 * <ul>
 *   <li>{@code url} - Main application URL</li>
 *   <li>{@code web.table.url} - Upgenix login page URL</li>
 *   <li>{@code EmplTitle} - Expected Employees page title</li>
 * </ul>
 * 
 * <p><strong>Wait Strategy:</strong> This class employs a hybrid wait approach:
 * <ul>
 *   <li>Explicit waits via {@link WebDriverWait} with 3-second timeout for condition-based waiting</li>
 *   <li>Multiple {@link Thread#sleep(long)} calls for UI stabilization where explicit waits are insufficient</li>
 * </ul>
 * 
 * <p><strong>Note:</strong> The use of Thread.sleep calls (ranging from 3 to 7 seconds) indicates
 * areas where the application under test may have timing issues. Consider replacing with more
 * robust explicit wait conditions in future refactoring.
 * 
 * @see com.testinium.pages.EmployeeP
 * @see com.testinium.utilities.Driver
 * @see com.testinium.utilities.ConfigurationReader
 */
public class EmployeeStage {
    
    /**
     * EmployeeP page object instance providing WebElement locators and the {@code login()} 
     * helper method for Employee module UI interactions.
     * 
     * <p>This page object is initialized eagerly at field declaration time, which requires
     * the WebDriver to be available via {@link Driver#getDriver()} at object construction.
     * The page object encapsulates all Employee module UI element locators and common
     * actions such as login authentication.
     * 
     * @see EmployeeP
     */
    EmployeeP employeePage = new EmployeeP();
    
    /**
     * WebDriverWait instance configured for explicit waits with a 3-second timeout.
     * 
     * <p>This wait object is initialized using {@link Driver#getDriver()} at field
     * declaration time, coupling object instantiation to driver availability. The
     * 3-second timeout is used for waiting on expected conditions such as page title
     * changes and element visibility.
     * 
     * <p><strong>Usage:</strong> Combined with {@link ExpectedConditions} for robust
     * synchronization, e.g., {@code wait.until(ExpectedConditions.titleIs("Expected Title"))}.
     * 
     * @see WebDriverWait
     * @see ExpectedConditions
     */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),3);

    /**
     * Navigates the browser to the Upgenix login page.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @When "User is on upgenix login page"}</pre>
     * 
     * <p>The URL is retrieved from configuration.properties using the key {@code web.table.url},
     * allowing the login page URL to be configured externally without code changes.
     * 
     * @see ConfigurationReader#getProperty(String)
     */
    @When("User is on upgenix login page")
    public void user_is_on_upgenix_login_page() {
        String url = ConfigurationReader.getProperty("web.table.url");
        Driver.getDriver().get(url);
    }

    /**
     * Navigates to the main application URL and performs login authentication.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @When "User is on the dashboard"}</pre>
     * 
     * <p>The method performs two actions:
     * <ol>
     *   <li>Navigates to the main application URL from configuration property {@code url}</li>
     *   <li>Calls {@link EmployeeP#login()} helper method for authentication with hard-coded credentials</li>
     * </ol>
     * 
     * @see EmployeeP#login()
     * @see ConfigurationReader#getProperty(String)
     */
    @When("User is on the dashboard")
    public void user_is_on_the_dashboard() {
        Driver.getDriver().get(ConfigurationReader.getProperty("url"));
        employeePage.login();
    }

    /**
     * Clicks the Employees navigation link, waits for the page to load, and verifies the page title.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @When "User clicks Employees stage"}</pre>
     * 
     * <p>The method performs the following actions:
     * <ol>
     *   <li>Clicks the Employees stage navigation link via {@link EmployeeP#emplStage}</li>
     *   <li>Waits for the page title to match the configured {@code EmplTitle} property</li>
     *   <li>Asserts that the page title equals "Employees - Odoo"</li>
     * </ol>
     * 
     * @see EmployeeP#emplStage
     * @see ConfigurationReader#getProperty(String)
     */
    @When("User clicks Employees stage")
    public void user_clicks_employees_stage() {
        employeePage.emplStage.click();
        wait.until(ExpectedConditions.titleIs(ConfigurationReader.getProperty("EmplTitle")));
        Assert.assertTrue(Driver.getDriver().getTitle().equals("Employees - Odoo"));
    }

    /**
     * Navigates through the gamification submenus: Badges, Challenges, and Goals History.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @When "User clicks Challenges stage"}</pre>
     * 
     * <p>The method clicks each navigation button sequentially with visibility waits between clicks:
     * <ol>
     *   <li>Clicks Badges button and waits for its visibility</li>
     *   <li>Clicks Challenges button and waits for its visibility</li>
     *   <li>Clicks Goals History button and waits for its visibility</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> This method does not verify page titles or content after navigation.
     * The visibility waits ensure elements are present but do not confirm successful navigation.
     * 
     * @see EmployeeP#badgesBtn
     * @see EmployeeP#challengesBtn
     * @see EmployeeP#goalsHistoryBtn
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
     * Clicks the Departments navigation link and waits for page load.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @When "User clicks Departments stage"}</pre>
     * 
     * <p>The method clicks the Departments button and waits 7 seconds via Thread.sleep
     * for the page to fully load.
     * 
     * <p><strong>Note:</strong> The 7-second sleep suggests slow page load times. Consider
     * replacing with an explicit wait condition (e.g., waiting for a specific element or
     * page title) for more robust synchronization.
     * 
     * @throws InterruptedException if the thread sleep is interrupted
     * @see EmployeeP#departmentsBtn
     */
    @When("User clicks Departments stage")
    public void user_clicks_departments_stage() throws InterruptedException {
        employeePage.departmentsBtn.click();
        Thread.sleep(7000);
    }
    
    /**
     * Asserts that the page title equals "Departments - Odoo" to validate successful navigation.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @Then "User should see the last stage title"}</pre>
     * 
     * <p>This verification step validates that the user has successfully navigated to the
     * Departments module by checking the page title.
     * 
     * <p><strong>Note:</strong> Contains commented-out alternative assertEquals approach
     * that could be used for more explicit assertion messaging.
     */
    @Then("User should see the last stage title")
    public void user_should_see_the_last_stage_title() {
        Assert.assertTrue(Driver.getDriver().getTitle().equals("Departments - Odoo"));
        //String act = Driver.getDriver().getTitle();
        //String exp = "Departments - Odoo";
        //Assert.assertEquals(exp,act);
    }

    /**
     * Performs complete navigation flow to the Employees dashboard: loads URL, logs in, and navigates.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @When "User is on the employees dashboard"}</pre>
     * 
     * <p>The method performs a complete navigation flow:
     * <ol>
     *   <li>Navigates to the main application URL from configuration</li>
     *   <li>Performs login via {@link EmployeeP#login()}</li>
     *   <li>Waits 3 seconds for UI stabilization after login</li>
     *   <li>Clicks the Employees stage navigation link</li>
     * </ol>
     * 
     * @throws InterruptedException if the thread sleep is interrupted
     * @see EmployeeP#login()
     * @see EmployeeP#emplStage
     */
    @When("User is on the employees dashboard")
    public void user_is_on_the_employees_dashboard() throws InterruptedException {
        Driver.getDriver().get(ConfigurationReader.getProperty("url"));
        employeePage.login();
        Thread.sleep(3000);
        employeePage.emplStage.click();
    }

    /**
     * Creates a new employee with the specified name in the Employees stage.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @When "User creates new employees {string} in the Employees stage"}</pre>
     * 
     * <p>The parameterized step allows dynamic employee name input from the feature file.
     * The method performs the following workflow:
     * <ol>
     *   <li>Waits 3 seconds for UI stabilization</li>
     *   <li>Clicks the Create button to open the new employee form</li>
     *   <li>Waits 3 seconds for form to load</li>
     *   <li>Waits for page title to become "New - Odoo" via explicit wait</li>
     *   <li>Enters the employee name into the name field</li>
     *   <li>Clicks the save button</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> Multiple Thread.sleep calls are used for UI stabilization.
     * Consider replacing with explicit waits for more robust synchronization.
     * 
     * @param name the employee name to enter, provided as a Cucumber step parameter
     *             enclosed in quotes in the feature file
     * @throws InterruptedException if the thread sleep is interrupted
     * @see EmployeeP#createBtn
     * @see EmployeeP#employeesName
     * @see EmployeeP#savedMessage
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
     * Asserts that the "Employee created" confirmation message is displayed.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @Then "User should see the Employee created message under full profile"}</pre>
     * 
     * <p>This verification step confirms that the employee creation was successful by
     * checking that the {@link EmployeeP#createdMessage} element is displayed on the page.
     * The element contains the text "Employee created".
     * 
     * <p><strong>Note:</strong> Contains commented-out alternative text assertion approach
     * that could verify the exact message text rather than just element visibility.
     */
    @Then("User should see the Employee created message under full profile")
    public void user_should_see_the_message_under_full_profile() {
        Assert.assertTrue(employeePage.createdMessage.isDisplayed());
        //String expected = "Employee created";
        //String actual = employeePage.createdMessage.getText();
        //Assert.assertEquals(expected,actual);
    }

    /**
     * Navigates to the Employees stage and verifies the page title.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @Then "User should see listed employees in the Employees stage"}</pre>
     * 
     * <p>The method performs:
     * <ol>
     *   <li>Clicks the Employees stage navigation link</li>
     *   <li>Waits for the page title to become "Employees - Odoo"</li>
     *   <li>Asserts that the page title equals "Employees - Odoo"</li>
     * </ol>
     * 
     * @throws InterruptedException if the thread sleep is interrupted (declared but not used)
     * @see EmployeeP#emplStage
     */
    @Then("User should see listed employees in the Employees stage")
    public void user_should_see_listed_employees_in_the_employees_stage() throws InterruptedException {
        employeePage.emplStage.click();
        wait.until(ExpectedConditions.titleIs("Employees - Odoo"));
        Assert.assertTrue(Driver.getDriver().getTitle().equals("Employees - Odoo"));
    }

    /**
     * Performs a complete employee edit workflow including navigation, selection, and data modification.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @When "User edits created employees in the Employees module"}</pre>
     * 
     * <p>The method performs a comprehensive edit workflow:
     * <ol>
     *   <li>Navigates to the main application URL and logs in</li>
     *   <li>Waits 3 seconds and navigates to the Employees stage</li>
     *   <li>Waits 3 seconds and selects an employee via {@link EmployeeP#chooseEmployee}</li>
     *   <li>Clicks the edit button via {@link EmployeeP#editEmployee}</li>
     *   <li>Waits 3 seconds and clears the name edit field</li>
     *   <li>Enters the hard-coded name "Sterling" into the name field</li>
     *   <li>Waits 3 seconds and clicks save</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> The {@code chooseEmployee} locator uses an absolute XPath
     * ({@code //html/body/div[1]/div[2]/div[2]/div/div/div/div[1]}), which is brittle and
     * may break with minor UI changes. Consider using a more robust locator strategy.
     * 
     * <p><strong>Note:</strong> Multiple 3-second Thread.sleep calls are used throughout
     * this method for UI stabilization. Consider replacing with explicit wait conditions.
     * 
     * @throws InterruptedException if any thread sleep is interrupted
     * @see EmployeeP#chooseEmployee
     * @see EmployeeP#editEmployee
     * @see EmployeeP#nameEdit
     * @see EmployeeP#savedMessage
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
     * Navigates to the Employees stage after editing an employee.
     * 
     * <p>This step definition corresponds to the Gherkin step:
     * <pre>{@code @Then "User should see the edited name in the Employees module"}</pre>
     * 
     * <p>This method clicks the Employees stage navigation link to return to the employee list.
     * 
     * <p><strong>Note:</strong> This method only performs navigation and does not include
     * any assertion to verify that the edit was successful. The verification of the edited
     * name is not implemented - consider adding an assertion to check the employee name
     * was updated correctly.
     * 
     * @see EmployeeP#emplStage
     */
    @Then("User should see the edited name in the Employees module")
    public void user_should_see_the_edited_name_in_the_employees_module() {
        employeePage.emplStage.click();
    }


}
