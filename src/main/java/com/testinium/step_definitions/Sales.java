package com.testinium.step_definitions;

import com.testinium.pages.SalesP;
import com.testinium.utilities.Driver;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;
import org.openqa.selenium.Keys;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Cucumber glue class providing step definitions for Sales/Customers module tests in the Odoo application.
 * 
 * <p>This class implements step definitions for customer management operations including:
 * <ul>
 *   <li>Module navigation - clicking sales dashboard and customers button</li>
 *   <li>Customer creation - entering name, address, state (with "Create and Edit..." dialog), and country</li>
 *   <li>Saving customer records - handling both modal save and form save operations</li>
 *   <li>Search functionality - finding customers by name from the search bar</li>
 *   <li>Validation error handling - capturing required-field validation warnings</li>
 * </ul>
 * 
 * <p>Each step method is annotated with Cucumber {@code @When}, {@code @Then}, or {@code @And} annotations
 * that map Gherkin step text from feature files to executable Java methods. The step text patterns
 * define the natural language binding for behavior-driven development (BDD).
 * 
 * <p>This class uses explicit waits via {@link WebDriverWait} with a 4-second timeout to handle
 * asynchronous page loading and element visibility after user interactions.
 * 
 * <p><strong>Known Issues:</strong>
 * <ul>
 *   <li>{@link #user_click_customers_button()} - Assertion has swapped actual/expected values</li>
 *   <li>{@link #userCanFindHisNameFromSearchBar(String)} - Missing assertion, only prints to console</li>
 *   <li>{@link #userCanGetTheError()} - Missing assertion, only prints to console</li>
 * </ul>
 * 
 * @see com.testinium.pages.SalesP
 * @see com.testinium.utilities.Driver
 */
public class Sales {

    /**
     * SalesP page object instance providing WebElement locators for Sales/Customers module UI interactions.
     * 
     * <p>This page object encapsulates locators for:
     * <ul>
     *   <li>Navigation elements (salesPartial, customersButton)</li>
     *   <li>Create/Save buttons (createButton, saveButton, createCustomer)</li>
     *   <li>Customer form fields (customerName, address, stateOptions, etc.)</li>
     *   <li>Search functionality (searchBar)</li>
     *   <li>Kanban card elements (nameCheck, allCustomers)</li>
     *   <li>Notification elements (warning, warningButton)</li>
     * </ul>
     * 
     * <p>Initialized eagerly at field declaration, which triggers PageFactory initialization
     * upon instantiation of this step definition class.
     * 
     * @see SalesP
     */
    SalesP salesp = new SalesP();

    /**
     * WebDriverWait instance for explicit waits with 4-second timeout.
     * 
     * <p>Uses {@link Driver#getDriver()} at initialization time, coupling object instantiation
     * to driver availability. The wait is used throughout this class to synchronize with
     * asynchronous page updates after clicking elements.
     * 
     * <p>The 4-second timeout is a balance between test responsiveness and allowing sufficient
     * time for Odoo's JavaScript-heavy UI to render elements.
     * 
     * @see WebDriverWait
     * @see Driver#getDriver()
     */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),4);

    /**
     * Navigates to the Sales module by clicking the sales navigation link.
     * 
     * <p>This step corresponds to the Gherkin step: {@code When User click on the sales dashboard}
     * 
     * <p>Implementation details:
     * <ol>
     *   <li>Clicks the {@link SalesP#salesPartial} element (partial link text "Sales")</li>
     *   <li>Waits for the sales partial link to become visible (confirmation of navigation)</li>
     * </ol>
     * 
     * @throws InterruptedException if thread sleep is interrupted (declared but not currently used)
     * @see SalesP#salesPartial
     */
    @When("User click on the sales dashboard")
    public void user_click_on_the_sales_dashboard() throws InterruptedException {
        salesp.salesPartial.click();
        wait.until(ExpectedConditions.visibilityOf(salesp.salesPartial));
    }

    /**
     * Navigates to the Customers submenu and verifies the page title.
     * 
     * <p>This step corresponds to the Gherkin step: {@code When User click customers button}
     * 
     * <p>Implementation details:
     * <ol>
     *   <li>Clicks the {@link SalesP#customersButton} element (hard-coded menu_id/action URL)</li>
     *   <li>Waits for the customers button to become visible</li>
     *   <li>Performs title assertion with debug console output</li>
     * </ol>
     * 
     * <p><strong>BUG:</strong> The assertion has actual/expected values swapped:
     * <ul>
     *   <li>{@code actualTitle} is hard-coded to "Customers - Odoo"</li>
     *   <li>{@code expectedTitle} is dynamically computed but incorrectly prepends "Customers - " to the page title</li>
     * </ul>
     * Correct implementation should be:
     * {@code Assert.assertEquals(Driver.getDriver().getTitle(), "Customers - Odoo");}
     * 
     * @throws InterruptedException if thread sleep is interrupted (declared but not currently used)
     * @see SalesP#customersButton
     */
    @When("User click customers button")
    public void user_click_customers_button() throws InterruptedException {

        salesp.customersButton.click();
        wait.until(ExpectedConditions.visibilityOf(salesp.customersButton));

        String actualTitle = "Customers - Odoo";
        String expectedTitle = "Customers - "+Driver.getDriver().getTitle();

        System.out.println("actualTitle = " + actualTitle);
        System.out.println("expected = "+expectedTitle);

        Assert.assertEquals("The title is not same as the expected!", expectedTitle, actualTitle);
    }

    /**
     * Creates a customer with hard-coded test data.
     * 
     * <p>This step corresponds to the Gherkin step: {@code When User can create the customer}
     * 
     * <p>Test data used:
     * <ul>
     *   <li>Name: "Lucas"</li>
     *   <li>Address: "1 boulevard auguste rodin 75000"</li>
     *   <li>State: Opens "Create and Edit..." dialog, enters "Albania" with code "78"</li>
     *   <li>Country: Selects from dropdown via {@link SalesP#countrySelection} (ui-id-30)</li>
     * </ul>
     * 
     * <p>Implementation details:
     * <ol>
     *   <li>Clicks create button and waits for visibility</li>
     *   <li>Enters customer name "Lucas"</li>
     *   <li>Enters address</li>
     *   <li>Opens state dropdown and clicks "Create and Edit..." option</li>
     *   <li>In the state creation dialog, enters state name and code</li>
     *   <li>Clicks country state button to open country dropdown</li>
     *   <li>Selects country from dropdown</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> Uses generated numeric ID locators throughout (o_field_input_470,
     * o_field_input_474, etc.) which are brittle selectors that may break with Odoo updates.
     * 
     * @throws InterruptedException if thread sleep is interrupted (declared but not currently used)
     * @see SalesP#createButton
     * @see SalesP#customerName
     * @see SalesP#address
     * @see SalesP#stateOptions
     * @see SalesP#createAndEditState
     * @see SalesP#stateName
     * @see SalesP#stateCode
     * @see SalesP#countryStateButton
     * @see SalesP#countrySelection
     */
    @When("User can create the customer")
    public void user_can_create_the_customer() throws InterruptedException {
        salesp.createButton.click();
        wait.until(ExpectedConditions.visibilityOf(salesp.createButton));
        salesp.customerName.sendKeys("Lucas");
        salesp.address.sendKeys("1 boulevard auguste rodin 75000");
        salesp.stateOptions.click();
        salesp.createAndEditState.click();
        salesp.stateName.sendKeys("Albania");
        salesp.stateCode.sendKeys("78");
        salesp.countryStateButton.click();
        salesp.countrySelection.click();

    }

    /**
     * Saves the customer and returns to the customer list.
     * 
     * <p>This step corresponds to the Gherkin step: {@code When User can save the customer}
     * 
     * <p>Implementation details:
     * <ol>
     *   <li>Clicks {@link SalesP#saveButton} (modal save) and waits for visibility</li>
     *   <li>Clicks {@link SalesP#createCustomer} (form save) and waits for visibility</li>
     *   <li>Clicks {@link SalesP#customersButton} to navigate back to the customer list</li>
     * </ol>
     * 
     * @see SalesP#saveButton
     * @see SalesP#createCustomer
     * @see SalesP#customersButton
     */
    @When("User can save the customer")
    public void user_can_save_the_customer() {
        salesp.saveButton.click();
        wait.until(ExpectedConditions.visibilityOf(salesp.saveButton));
        salesp.createCustomer.click();
        wait.until(ExpectedConditions.visibilityOf(salesp.createCustomer));
        salesp.customersButton.click();
        wait.until(ExpectedConditions.visibilityOf(salesp.customersButton));

    }


    /**
     * Searches for a customer by name using the search bar and retrieves the result.
     * 
     * <p>This step corresponds to the Gherkin step: {@code Then User can find his name {string} from search bar}
     * 
     * <p>This is a parameterized step that accepts a customer name from the Cucumber feature file.
     * 
     * <p>Implementation details:
     * <ol>
     *   <li>Enters the search name in the search bar with {@link Keys#ENTER} to execute the search</li>
     *   <li>Waits for search bar visibility</li>
     *   <li>Retrieves customer name from the kanban card ({@link SalesP#nameCheck} element)</li>
     *   <li>Prints actual and expected names to console for debugging</li>
     * </ol>
     * 
     * <p><strong>BUG:</strong> No assertion is performed - the method only prints to console without
     * verifying the search result. Correct implementation should include:
     * {@code Assert.assertEquals(salesp.nameCheck.getText(), name);}
     * 
     * @param name the customer name to search for (from Cucumber step parameter)
     * @see SalesP#searchBar
     * @see SalesP#nameCheck
     */
    @Then("User can find his name {string} from search bar")
    public void userCanFindHisNameFromSearchBar(String name) {
        salesp.searchBar.sendKeys(name+ Keys.ENTER);
        wait.until(ExpectedConditions.visibilityOf(salesp.searchBar));

        String actualName = "Lucas";
        String expectedName = salesp.nameCheck.getText();

        System.out.println("actualName = " + actualName);
        System.out.println("expectedName = " + expectedName);


    }

    /**
     * Initiates customer creation and immediately clicks save to trigger validation.
     * 
     * <p>This step corresponds to the Gherkin step: {@code And User can create new customer}
     * 
     * <p>This step is used for testing required-field validation errors. By clicking create
     * and immediately attempting to save without filling required fields, the validation
     * warning should appear.
     * 
     * <p>Implementation details:
     * <ol>
     *   <li>Clicks {@link SalesP#createButton} to open the customer creation form</li>
     *   <li>Waits for the create button to become visible</li>
     *   <li>Immediately clicks {@link SalesP#createCustomer} to attempt save</li>
     * </ol>
     * 
     * @see SalesP#createButton
     * @see SalesP#createCustomer
     */
    @And("User can create new customer")
    public void userCanCreateNewCustomer() {
        salesp.createButton.click();
        wait.until(ExpectedConditions.visibilityOf(salesp.createButton));
        salesp.createCustomer.click();
    }

    /**
     * Captures the validation warning message text when required fields are not filled.
     * 
     * <p>This step corresponds to the Gherkin step: {@code Then User can get the error}
     * 
     * <p>Implementation details:
     * <ol>
     *   <li>Defines expected warning message "The following fields are invalid:"</li>
     *   <li>Retrieves actual warning text from {@link SalesP#warning} element</li>
     *   <li>Prints both values to console for debugging</li>
     * </ol>
     * 
     * <p><strong>BUG:</strong> No assertion is performed - the method only prints to console without
     * verifying the error message. Correct implementation should include:
     * {@code Assert.assertEquals(salesp.warning.getText(), "The following fields are invalid:");}
     * 
     * @see SalesP#warning
     */
    @Then("User can get the error")
    public void userCanGetTheError() {

        String actualWarning = "The following fields are invalid:";
        String expectedWarning = salesp.warning.getText();

        System.out.println("actualWarning = " + actualWarning);
        System.out.println("expectedWarning = " + expectedWarning);

    }


}
