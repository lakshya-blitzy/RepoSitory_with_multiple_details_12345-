package com.testinium.step_definitions;

import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import com.testinium.pages.InventoryP;
import com.testinium.utilities.Driver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Step Definition for the Inventory to Products flow of the Odoo/Upgenix application
 * ({@code Inventory.feature}).
 * <p>
 * The steps cover opening the Inventory module, starting product creation, required-field
 * validation on save, and product-name entry. They drive the Page Object
 * {@link com.testinium.pages.InventoryP} through the {@code inventory} field.
 * <p>
 * The {@code inventory} Page Object and the 20-second {@code WebDriverWait} are created in
 * field initializers that call {@link com.testinium.utilities.Driver#getDriver()}, so
 * instantiating this class opens or reuses the current thread's browser session.
 * <p>
 * Known limitation: no step in this class asserts. The verification steps call
 * {@code isDisplayed()} or compare the page title and discard the result, so an
 * {@code isDisplayed()} check fails only when its element cannot be located, and the title
 * comparison never fails.
 */
public class Inventory {

    /** Inventory Page Object whose elements these steps drive. */
    InventoryP inventory = new InventoryP();
    /** Explicit wait of 20 seconds on the thread's driver. */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 20);

    /**
     * Clicks the Inventory module link ({@code inventory.inventoryModule}) in the main menu.
     * <p>
     * Gherkin: {@code Logged user clicks on Inventory Module}
     */
    @When("Logged user clicks on Inventory Module")
    public void logged_user_clicks_on_inventory_module() {
        inventory.inventoryModule.click();
    }

    /**
     * Waits up to 20 seconds for the Products menu link ({@code inventory.products}) to be
     * visible, then clicks it.
     * <p>
     * Gherkin: {@code User clicks on Product module}
     */
    @When("User clicks on Product module")
    public void user_clicks_on_product_module() {
        wait.until(ExpectedConditions.visibilityOf(inventory.products));
        inventory.products.click();
    }

    /**
     * Compares the current page title with a hard-coded expected value but discards the
     * boolean result, so nothing is asserted and the step never fails on a title mismatch.
     * <p>
     * Gherkin: {@code User see the products}
     */
    @When("User see the products")
    public void user_see_the_products() {
        Driver.getDriver().getTitle().equals("Products - Odoo");
    }

    /**
     * Clicks the Create button ({@code inventory.createBtn}) to open a new product form.
     * <p>
     * Gherkin: {@code User clicks create button}
     */
    @When("User clicks create button")
    public void user_clicks_create_button() {
        inventory.createBtn.click();
    }

    /**
     * Waits up to 20 seconds for the Save button ({@code inventory.saveBtn}) to be visible,
     * then clicks it.
     * <p>
     * Gherkin: {@code User clicks the save button}
     */
    @When("User clicks the save button")
    public void user_clicks_the_save_button() {
        wait.until(ExpectedConditions.visibilityOf(inventory.saveBtn));
        inventory.saveBtn.click();
    }

    /**
     * Calls {@code inventory.fieldError.isDisplayed()} on the notification that reports
     * invalid required fields, without asserting the result. The step fails only if the
     * element cannot be located, not if it is hidden.
     * <p>
     * Gherkin: {@code User should see the error}
     */
    @Then("User should see the error")
    public void user_should_see_the_error() {
        inventory.fieldError.isDisplayed();
    }

    /**
     * Types a hard-coded product name into the product name input
     * ({@code inventory.productName}).
     * <p>
     * Gherkin: {@code User enters Product Name}
     */
    @When("User enters Product Name")
    public void user_enters_product_name() {
        inventory.productName.sendKeys("IBM");
    }

    /**
     * Calls {@code inventory.productsList.isDisplayed()} without asserting the result.
     * Despite its wording, the step does not inspect the page title; it fails only if the
     * product-list element cannot be located. The
     * {@link com.testinium.pages.InventoryP#productsList} locator matches a fixed product text
     * that differs from the name typed by {@link #user_enters_product_name()}.
     * <p>
     * Gherkin: {@code User should see the title includes the Product Name}
     */
    @Then("User should see the title includes the Product Name")
    public void user_should_see_the_title_includes_the_product_name() {
        inventory.productsList.isDisplayed();
    }

    /**
     * Calls {@code inventory.createdProduct.isDisplayed()} on the required name field shown
     * after saving, without asserting the result. The step fails only if the element cannot
     * be located.
     * <p>
     * Gherkin: {@code User sees the created Product}
     */
    @Then("User sees the created Product")
    public void user_sees_the_created_product() {
        inventory.createdProduct.isDisplayed();
    }



}