package com.testinium.step_definitions;

import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import com.testinium.pages.InventoryP;
import com.testinium.utilities.Driver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Cucumber glue class providing step definitions for Inventory/Products module tests
 * in the Odoo application.
 * 
 * <p>This class implements Cucumber step definitions for product management functionality,
 * including:</p>
 * <ul>
 *   <li>Module navigation - accessing the Inventory module from the dashboard</li>
 *   <li>Product listing - viewing the products list page</li>
 *   <li>Product creation - initiating and completing new product creation</li>
 *   <li>Save operations - saving newly created products</li>
 *   <li>Required-field validation - handling error messages when mandatory fields are empty</li>
 *   <li>Product verification - confirming products appear after creation</li>
 * </ul>
 * 
 * <p>The class uses Gherkin step bindings via {@code @When} and {@code @Then} annotations
 * that map human-readable step text from feature files to executable Java methods.</p>
 * 
 * <p><strong>Wait Strategy:</strong> This class uses explicit waits via {@link WebDriverWait}
 * with a 20-second timeout to accommodate potentially slow Inventory module page loads.</p>
 * 
 * <p><strong>Known Issues:</strong> Several methods call {@code isDisplayed()} without
 * asserting the result, making them ineffective as verifications. The boolean return
 * values are computed but discarded, so these steps will pass regardless of element
 * visibility. These should be wrapped in {@code Assert.assertTrue()} calls.</p>
 * 
 * @see com.testinium.pages.InventoryP
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.ui.WebDriverWait
 */
public class Inventory {

    /**
     * Page object instance providing WebElement locators for Inventory/Products module
     * UI interactions.
     * 
     * <p>This field is initialized eagerly at field declaration time, which triggers
     * PageFactory initialization via the {@link InventoryP} constructor. This approach
     * assumes the WebDriver is available when the step definition class is instantiated
     * by Cucumber.</p>
     * 
     * @see InventoryP
     */
    InventoryP inventory = new InventoryP();
    
    /**
     * WebDriverWait instance configured for explicit waits with a 20-second timeout.
     * 
     * <p>The longer timeout (20 seconds vs. typical 10 seconds) accommodates potentially
     * slow Inventory module page loads in the Odoo application, which may involve
     * complex data retrieval operations.</p>
     * 
     * <p><strong>Note:</strong> This field is initialized at declaration time using
     * {@code Driver.getDriver()}, which couples object instantiation to driver availability.
     * The driver must be initialized before this class is instantiated.</p>
     * 
     * @see Driver#getDriver()
     * @see org.openqa.selenium.support.ui.WebDriverWait
     */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 20);

    /**
     * Clicks on the Inventory module navigation link to navigate from the dashboard.
     * 
     * <p>This step is typically used after a successful login to navigate to the
     * Inventory module. The step name "Logged user clicks on Inventory Module"
     * assumes the user is already authenticated.</p>
     * 
     * <p>Gherkin binding: {@code @When("Logged user clicks on Inventory Module")}</p>
     * 
     * @see InventoryP#inventoryModule
     */
    @When("Logged user clicks on Inventory Module")
    public void logged_user_clicks_on_inventory_module() {
        inventory.inventoryModule.click();
    }

    /**
     * Waits for the Products submenu link to become visible, then clicks to navigate
     * to the product management page.
     * 
     * <p>This method uses an explicit wait before clicking to ensure element stability,
     * as the Products submenu may take time to render after the Inventory module loads.</p>
     * 
     * <p>Gherkin binding: {@code @When("User clicks on Product module")}</p>
     * 
     * @see InventoryP#products
     * @see org.openqa.selenium.support.ui.ExpectedConditions#visibilityOf
     */
    @When("User clicks on Product module")
    public void user_clicks_on_product_module() {
        wait.until(ExpectedConditions.visibilityOf(inventory.products));
        inventory.products.click();
    }

    /**
     * Verifies that the Products page has loaded by checking the page title.
     * 
     * <p>Gherkin binding: {@code @When("User see the products")}</p>
     * 
     * <p><strong>BUG:</strong> This method computes a title comparison result but does not
     * assert it. The boolean result of {@code equals()} is computed and immediately discarded,
     * making this step ineffective as a verification. The step will always pass regardless
     * of the actual page title.</p>
     * 
     * <p>Recommended fix:</p>
     * <pre>{@code
     * Assert.assertTrue(Driver.getDriver().getTitle().equals("Products - Odoo"));
     * }</pre>
     * 
     * @see Driver#getDriver()
     */
    @When("User see the products")
    public void user_see_the_products() {
        Driver.getDriver().getTitle().equals("Products - Odoo");
    }

    /**
     * Clicks the Create button to initiate new product creation.
     * 
     * <p>This action opens the product creation form where users can enter product
     * details. The button is identified by the Odoo-specific CSS class
     * {@code o-kanban-button-new}.</p>
     * 
     * <p>Gherkin binding: {@code @When("User clicks create button")}</p>
     * 
     * @see InventoryP#createBtn
     */
    @When("User clicks create button")
    public void user_clicks_create_button() {
        inventory.createBtn.click();
    }

    /**
     * Waits for the Save button to become visible, then clicks to save the product.
     * 
     * <p>This method uses an explicit wait before clicking to ensure the Save button
     * is fully rendered. The button is identified by the Odoo-specific CSS class
     * {@code o_form_button_save} with primary button styling.</p>
     * 
     * <p>Gherkin binding: {@code @When("User clicks the save button")}</p>
     * 
     * @see InventoryP#saveBtn
     * @see org.openqa.selenium.support.ui.ExpectedConditions#visibilityOf
     */
    @When("User clicks the save button")
    public void user_clicks_the_save_button() {
        wait.until(ExpectedConditions.visibilityOf(inventory.saveBtn));
        inventory.saveBtn.click();
    }

    /**
     * Verifies that a validation error is displayed when attempting to save
     * without filling required fields.
     * 
     * <p>This step uses the notification manager container ({@code fieldError})
     * to detect the presence of an error message in Odoo's notification system.</p>
     * 
     * <p>Gherkin binding: {@code @Then("User should see the error")}</p>
     * 
     * <p><strong>BUG:</strong> This method calls {@code isDisplayed()} but does not
     * assert the result. The boolean return value is computed and immediately discarded,
     * making this step ineffective as a verification. The step will always pass regardless
     * of whether the error is actually displayed.</p>
     * 
     * <p>Recommended fix:</p>
     * <pre>{@code
     * Assert.assertTrue(inventory.fieldError.isDisplayed());
     * }</pre>
     * 
     * @see InventoryP#fieldError
     */
    @Then("User should see the error")
    public void user_should_see_the_error() {
        inventory.fieldError.isDisplayed();
    }

    /**
     * Enters a product name into the product name input field.
     * 
     * <p>This method enters the hard-coded product name "IBM" into the product
     * name field. The locator uses a generated numeric ID ({@code o_field_input_479})
     * which may be brittle and subject to change across Odoo versions or page reloads.</p>
     * 
     * <p>Gherkin binding: {@code @When("User enters Product Name")}</p>
     * 
     * <p><strong>Note:</strong> The test data is hard-coded rather than parameterized,
     * limiting the flexibility of this step for data-driven testing scenarios.</p>
     * 
     * @see InventoryP#productName
     */
    @When("User enters Product Name")
    public void user_enters_product_name() {
        inventory.productName.sendKeys("IBM");
    }

    /**
     * Verifies that a product appears in the products list.
     * 
     * <p>Gherkin binding: {@code @Then("User should see the title includes the Product Name")}</p>
     * 
     * <p><strong>Note:</strong> Despite the step text mentioning "title", this method
     * actually checks for an element in the products list, not the page title.</p>
     * 
     * <p><strong>BUG:</strong> This method calls {@code isDisplayed()} but does not
     * assert the result. The boolean return value is computed and immediately discarded,
     * making this step ineffective as a verification.</p>
     * 
     * <p>Recommended fix:</p>
     * <pre>{@code
     * Assert.assertTrue(inventory.productsList.isDisplayed());
     * }</pre>
     * 
     * @see InventoryP#productsList
     */
    @Then("User should see the title includes the Product Name")
    public void user_should_see_the_title_includes_the_product_name() {
        inventory.productsList.isDisplayed();
    }

    /**
     * Verifies that the created product is displayed on the page.
     * 
     * <p>This step checks for the presence of a required character field element
     * to confirm that the product was successfully created and saved.</p>
     * 
     * <p>Gherkin binding: {@code @Then("User sees the created Product")}</p>
     * 
     * <p><strong>BUG:</strong> This method calls {@code isDisplayed()} but does not
     * assert the result. The boolean return value is computed and immediately discarded,
     * making this step ineffective as a verification.</p>
     * 
     * <p>Recommended fix:</p>
     * <pre>{@code
     * Assert.assertTrue(inventory.createdProduct.isDisplayed());
     * }</pre>
     * 
     * @see InventoryP#createdProduct
     */
    @Then("User sees the created Product")
    public void user_sees_the_created_product() {
        inventory.createdProduct.isDisplayed();
    }



}
