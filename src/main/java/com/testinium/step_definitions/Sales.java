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
 * Step Definition for the Sales to Customers flow of the Odoo/Upgenix application, bound to the
 * steps of {@code Sales.feature}.
 *
 * <p>The steps open Sales and then Customers, create a customer with a new state, save it,
 * search for a customer by name, and cover blank-name validation by reading the warning shown when
 * a customer is saved with a blank name. The feature's Background login step is bound in
 * {@link com.testinium.step_definitions.Session}, not in this class.
 *
 * <p>Page Object: {@link com.testinium.pages.SalesP}, held in the {@code salesp} field.
 *
 * <p>Both {@code salesp} and the 4-second {@code WebDriverWait} are created in field
 * initializers that call {@link com.testinium.utilities.Driver#getDriver()}: the
 * {@code SalesP} constructor passes it to {@code PageFactory.initElements}, and the wait is built
 * on it directly. Cucumber instantiates this class for each scenario that runs one of its steps,
 * and that instantiation opens the current thread's browser session, or reuses it if one is
 * already open. Each wait in this class waits for the element the step has just clicked or typed
 * into to be visible.
 *
 * <p>Known limitation: the search step
 * ({@link #userCanFindHisNameFromSearchBar(String)}) and the error step
 * ({@link #userCanGetTheError()}) read a value from the page and print it next to a hard-coded
 * value, but assert nothing, so they pass whatever text the page shows. The title check in
 * {@link #user_click_customers_button()} does assert, but with inverted operand naming; see that
 * method.
 */
public class Sales {

    /** Sales Page Object whose elements every step in this class drives. */
    SalesP salesp = new SalesP();

    /** Explicit wait of 4 seconds on the thread's driver. */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),4);

    /**
     * Opens the Sales application: clicks {@code salesp.salesPartial}, then waits for that element
     * to be visible.
     * <p>
     * Gherkin: {@code User click on the sales dashboard}
     *
     * @throws InterruptedException declared by the signature; the current body does not call {@code Thread.sleep}
     */
    @When("User click on the sales dashboard")
    public void user_click_on_the_sales_dashboard() throws InterruptedException {
        salesp.salesPartial.click();
        wait.until(ExpectedConditions.visibilityOf(salesp.salesPartial));
    }

    /**
     * Opens the Customers view and checks the page title: clicks {@code salesp.customersButton},
     * waits for that element to be visible, prints two title strings and asserts that they are
     * equal.
     * <p>
     * Gherkin: {@code User click customers button}
     *
     * <p>Known discrepancy: the operand naming is inverted. {@code actualTitle} holds a hard-coded
     * literal, while {@code expectedTitle} is a constant prefix concatenated with the current
     * browser title from {@link com.testinium.utilities.Driver#getDriver()}, and
     * {@code expectedTitle} is passed as the expected value of {@code Assert.assertEquals}. Because
     * the literal starts with the same prefix, the check passes only when the browser title is the
     * bare application name.
     *
     * @throws InterruptedException declared by the signature; the current body does not call {@code Thread.sleep}
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
     * Fills the new-customer form and creates a new state for it: clicks
     * {@code salesp.createButton} and waits for it, types a hard-coded customer name into
     * {@code salesp.customerName} and a hard-coded address into {@code salesp.address}, opens
     * {@code salesp.stateOptions} and chooses {@code salesp.createAndEditState}, types a
     * hard-coded state name and code into {@code salesp.stateName} and {@code salesp.stateCode},
     * then clicks {@code salesp.countryStateButton} and {@code salesp.countrySelection}.
     * <p>
     * Gherkin: {@code User can create the customer}
     *
     * <p>The step saves neither the state dialog nor the customer; the next step,
     * {@link #user_can_save_the_customer()}, does both.
     *
     * @throws InterruptedException declared by the signature; the current body does not call {@code Thread.sleep}
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
     * Saves the new state and the customer, then returns to the Customers view: clicks
     * {@code salesp.saveButton} (the state dialog's Save), {@code salesp.createCustomer} (the form
     * Save) and {@code salesp.customersButton}, waiting after each click for the clicked element to
     * be visible.
     * <p>
     * Gherkin: {@code User can save the customer}
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
     * Searches the Customers view by name: types {@code name} followed by ENTER into
     * {@code salesp.searchBar} and waits for that element to be visible, then reads the text of
     * {@code salesp.nameCheck} and prints it next to a hard-coded name.
     * <p>
     * Gherkin: {@code User can find his name {string} from search bar}
     *
     * <p>Known limitation: the step asserts nothing. It does not compare the name found with
     * {@code name} or with the hard-coded name, so it passes whatever card title the page shows.
     *
     * @param name the customer name bound to {@code {string}} and typed into the search bar
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
     * Saves an empty new-customer form to trigger validation: clicks {@code salesp.createButton},
     * waits for it, then clicks {@code salesp.createCustomer} (the form Save) without filling in any
     * field.
     * <p>
     * Gherkin: {@code User can create new customer}
     */
    @And("User can create new customer")
    public void userCanCreateNewCustomer() {
        salesp.createButton.click();
        wait.until(ExpectedConditions.visibilityOf(salesp.createButton));
        salesp.createCustomer.click();
    }

    /**
     * Reads the validation warning: reads the text of {@code salesp.warning} and prints it next to
     * a hard-coded expected warning.
     * <p>
     * Gherkin: {@code User can get the error}
     *
     * <p>Known limitation: the step asserts nothing, so it passes whatever text the notification
     * area shows, including none.
     */
    @Then("User can get the error")
    public void userCanGetTheError() {

        String actualWarning = "The following fields are invalid:";
        String expectedWarning = salesp.warning.getText();

        System.out.println("actualWarning = " + actualWarning);
        System.out.println("expectedWarning = " + expectedWarning);

    }


}
