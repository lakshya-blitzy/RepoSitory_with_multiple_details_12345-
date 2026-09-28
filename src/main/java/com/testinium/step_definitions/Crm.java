package com.testinium.step_definitions;

import com.testinium.pages.CrmP;
import com.testinium.utilities.Driver;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;
import org.openqa.selenium.Keys;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Step Definition for the CRM module of the Odoo/Upgenix ERP application, bound to the steps of
 * {@code Crm.feature}. That feature is tagged {@code @Smoke}, the tag {@code CukesRunner} selects by default.
 *
 * <p>The steps cover creating a pipeline opportunity and checking the stage total, editing an
 * opportunity, moving a card between pipeline stages by drag and drop with Selenium {@code Actions},
 * and registering a customer and opening its print options. The feature's Background login step is
 * bound in {@code com.testinium.step_definitions.Session}, not in this class.
 *
 * <p>Page Object: {@link com.testinium.pages.CrmP}, held in the {@code crm} field.
 *
 * <p>Instantiation: {@code crm} and the 2-second {@code WebDriverWait} are created in field
 * initializers that call {@link com.testinium.utilities.Driver#getDriver()}, so creating this class
 * opens the current thread's browser session, or reuses it if one is already open.
 *
 * <p>Known limitations, documented and left unchanged because this change adds documentation only:
 * <ul>
 *   <li>The data entered and the expected values checked are hard-coded in the method bodies, and the
 *       checks read the first card or the total of a fixed pipeline stage, so they depend on the data
 *       already present in the CRM instance.</li>
 *   <li>Several steps wait for the visibility of the element they have just clicked, which does not
 *       confirm that the click took effect.</li>
 * </ul>
 */
public class Crm {

    /** Page Object for the CRM screens; constructing it binds its elements to the thread's driver. */
    CrmP crm = new CrmP();

    /** Explicit wait of 2 seconds on the thread's driver. */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),2);


    /**
     * Opens the CRM module by clicking {@code crm.crmLink}, then waits up to 2 seconds for that link
     * to be visible.
     * <p>
     * Gherkin: {@code User click on the crm dashboard}
     */
    @When("User click on the crm dashboard")
    public void user_click_on_the_crm_dashboard() {
        crm.crmLink.click();
        wait.until(ExpectedConditions.visibilityOf(crm.crmLink));
    }

    /**
     * Opens the opportunity quick-create dialog by clicking {@code crm.createButton}, then waits up to
     * 2 seconds for that button to be visible.
     * <p>
     * Gherkin: {@code User click on the pipeline button}
     */
    @And("User click on the pipeline button")
    public void userClickOnThePipelineButton() {
        crm.createButton.click();
        wait.until(ExpectedConditions.visibilityOf(crm.createButton));

    }

    /**
     * Fills in and confirms the opportunity quick-create dialog.
     *
     * <p>Types a hard-coded title, followed by ENTER, into {@code crm.opportunityTitle}; picks the
     * customer by clicking {@code crm.customer} and then {@code crm.customerId}; clears
     * {@code crm.expectedRevenue} and types a hard-coded amount followed by ENTER; clicks
     * {@code crm.priority} and {@code crm.createPipeline}; then waits up to 2 seconds for
     * {@code crm.createPipeline} to be visible. The title and amount are the values that
     * {@link #userCanSeeNewPipeline()} and {@link #userCanSeeTheTotalPrice()} rely on.
     * <p>
     * Gherkin: {@code User can create the new pipeline}
     */
    @And("User can create the new pipeline")
    public void userCanCreateTheNewPipeline() {
        crm.opportunityTitle.sendKeys("test"+ Keys.ENTER);
        crm.customer.click();
        crm.customerId.click();
        crm.expectedRevenue.clear();
        crm.expectedRevenue.sendKeys("8"+Keys.ENTER);
        crm.priority.click();
        crm.createPipeline.click();
        wait.until(ExpectedConditions.visibilityOf(crm.createPipeline));
    }

    /**
     * Checks the expected-revenue total of pipeline stage {@code data-id='1'}.
     *
     * <p>Parses the text of {@code crm.totalPrice} as an {@code int}, adds a fixed amount equal to the
     * revenue typed by {@link #userCanCreateTheNewPipeline()}, prints the result and a hard-coded
     * expected total, and asserts with JUnit that the two are equal.
     *
     * <p>Known limitations, left unchanged:
     * <ul>
     *   <li>The expected total is a constant, so the check passes only when the displayed stage total
     *       plus the fixed amount equals it; the result depends on the opportunities already in that
     *       stage.</li>
     *   <li>{@code Integer.parseInt} throws a {@code NumberFormatException} when the displayed total is
     *       not a plain integer, for example when it carries a currency symbol or a thousands separator.</li>
     *   <li>The computed total is passed as the expected argument of {@code Assert.assertEquals}, so a
     *       failure message shows expected and actual swapped.</li>
     * </ul>
     * <p>
     * Gherkin: {@code User can see the total price}
     */
    @And("User can see the total price")
    public void userCanSeeTheTotalPrice() {
        int totalPrice= Integer.parseInt(crm.totalPrice.getText()) + 8;
        int price =89;

        System.out.println("totalPrice = " + totalPrice);
        System.out.println("price = " + price);

        Assert.assertEquals(totalPrice,price);

    }

    /**
     * Verifies that the new opportunity is shown in the pipeline: reads the text of
     * {@code crm.findTitleTest}, the first card title of pipeline stage {@code data-id='1'}, prints it
     * with the expected name, and asserts with JUnit that it equals the hard-coded title typed by
     * {@link #userCanCreateTheNewPipeline()}. The check assumes the new card is the first card of that
     * stage.
     * <p>
     * Gherkin: {@code User can see new pipeline}
     */
    @Then("User can see new pipeline")
    public void userCanSeeNewPipeline() {
        String actualName = crm.findTitleTest.getText();
        String expectedName = "test";

        System.out.println("actualName = " + actualName);
        System.out.println("expectedName = " + expectedName);

        Assert.assertEquals(expectedName,actualName);

    }

    /**
     * Opens the first opportunity of pipeline stage {@code data-id='1'} in edit mode and replaces its title,
     * expected revenue and probability.
     *
     * <p>Clicks {@code crm.buttonPipeline}, waits up to 2 seconds for it to be visible, and clicks
     * {@code crm.editButton}. It then clears {@code crm.opportunityTitleEdit},
     * {@code crm.expectedRevenueEdit} and {@code crm.probabilityEdit} in turn and types the matching
     * argument, followed by ENTER, into each. The changes are saved by {@link #userCanSaveInformation()}.
     * <p>
     * Gherkin: {@code User can change any user's information like {string} , {string} and {string}}
     *
     * @param opportunity the new opportunity title (first {@code {string}}), typed into
     *                    {@code crm.opportunityTitleEdit}
     * @param revenue     the new expected revenue (second {@code {string}}), typed into
     *                    {@code crm.expectedRevenueEdit}
     * @param probability the new probability (third {@code {string}}), typed into
     *                    {@code crm.probabilityEdit}
     */
    @And("User can change any user's information like {string} , {string} and {string}")
    public void userCanChangeAnyUserSInformationLikeAnd(String opportunity, String revenue, String probability) {
        crm.buttonPipeline.click();
        wait.until(ExpectedConditions.visibilityOf(crm.buttonPipeline));
        crm.editButton.click();
        crm.opportunityTitleEdit.clear();
        crm.opportunityTitleEdit.sendKeys(opportunity+Keys.ENTER);
        crm.expectedRevenueEdit.clear();
        crm.expectedRevenueEdit.sendKeys(revenue+Keys.ENTER);
        crm.probabilityEdit.clear();
        crm.probabilityEdit.sendKeys(probability+Keys.ENTER);
    }

    /**
     * Saves the edited opportunity: waits up to 2 seconds for {@code crm.probabilityEdit} to be visible,
     * then clicks {@code crm.saveEdit}.
     * <p>
     * Gherkin: {@code User can save information}
     */
    @And("User can save information")
    public void userCanSaveInformation() {
        wait.until(ExpectedConditions.visibilityOf(crm.probabilityEdit));
        crm.saveEdit.click();
    }

    /**
     * Verifies the edited opportunity: clicks {@code crm.pipelineSideButton} to return to the pipeline,
     * waits up to 2 seconds for {@code crm.buttonPipeline} to be visible, reads the text of
     * {@code crm.findTitleTest}, prints it with the expected name, and asserts with JUnit that it
     * equals a hard-coded expected name.
     *
     * <p>The expected name is not taken from the {@code opportunity} argument of
     * {@link #userCanChangeAnyUserSInformationLikeAnd(String, String, String)}, so the check passes
     * only for an Examples row whose opportunity value matches the hard-coded name.
     * <p>
     * Gherkin: {@code User can verify the information}
     */
    @Then("User can verify the information")
    public void userCanVerifyTheInformation() {
        crm.pipelineSideButton.click();
        wait.until(ExpectedConditions.visibilityOf(crm.buttonPipeline));

        String actualName = crm.findTitleTest.getText();
        String expectedName = "Test2";

        System.out.println("actualName = " + actualName);
        System.out.println("expectedName = " + expectedName);

        Assert.assertEquals(expectedName,actualName);



    }

    /**
     * Moves the first card of pipeline stage {@code data-id='1'} onto the first card of stage
     * {@code data-id='2'} by drag and drop.
     *
     * <p>Builds a Selenium {@code Actions} chain on {@link com.testinium.utilities.Driver#getDriver()}
     * that calls {@code clickAndHold} on {@code crm.progressPipeline}, pauses 2000 ms,
     * {@code moveToElement} on {@code crm.progressPipeline2}, pauses 2000 ms again, then calls
     * {@code release} and {@code perform}. It then sleeps for 2 seconds with {@code Thread.sleep} so the
     * board can update before {@link #userCanSeeTheNewChangesInProgress()} runs.
     * <p>
     * Gherkin: {@code User can drag and drop the pipeline}
     *
     * @throws InterruptedException if the thread is interrupted during the final {@code Thread.sleep}
     */
    @And("User can drag and drop the pipeline")
    public void userCanDragAndDropThePipeline() throws InterruptedException {
        Actions actions = new Actions(Driver.getDriver());

        actions.clickAndHold(crm.progressPipeline)
                .pause(2000)
                .moveToElement(crm.progressPipeline2)
                .pause(2000)
                .release()
                .perform();

        Thread.sleep(2000);

    }

    /**
     * Verifies the drag-and-drop move: reads the text of {@code crm.testVerify}, the card title in
     * pipeline stage {@code data-id='2'}, prints it with the expected name, and asserts with JUnit that it equals a
     * hard-coded name.
     * <p>
     * Gherkin: {@code User can see the new changes in progress}
     */
    @Then("User can see the new changes in progress")
    public void userCanSeeTheNewChangesInProgress() {
        String actualName = crm.testVerify.getText();
        String expectedName = "test";

        System.out.println("actualName = " + actualName);
        System.out.println("expectedName = " + expectedName);

        Assert.assertEquals(expectedName,actualName);
    }

    /**
     * Registers a customer and searches the customer list.
     *
     * <p>Clicks {@code crm.customerSideButton} and then {@code crm.createCustomer}, waiting up to
     * 2 seconds for each to be visible after its click; types a hard-coded name, followed by ENTER,
     * into {@code crm.inputName}; clicks {@code crm.createCustomerButton} and waits for it; then types
     * a hard-coded search term, followed by ENTER, into {@code crm.searchingText}. The step makes no
     * assertion.
     * <p>
     * Gherkin: {@code User can register new customer}
     */
    @And("User can register new customer")
    public void userCanRegisterNewCustomer() {
        crm.customerSideButton.click();
        wait.until(ExpectedConditions.visibilityOf(crm.customerSideButton));
        crm.createCustomer.click();
        wait.until(ExpectedConditions.visibilityOf(crm.createCustomer));
        crm.inputName.sendKeys("Test"+Keys.ENTER);
        crm.createCustomerButton.click();
        wait.until(ExpectedConditions.visibilityOf(crm.createCustomerButton));
        crm.searchingText.sendKeys("aa"+Keys.ENTER);

    }

    /**
     * Opens a customer profile and its print options: clicks {@code crm.nameCustomer} and waits up to
     * 2 seconds for it to be visible, clicks {@code crm.printButton}, waits for
     * {@code crm.duePaymentButton} and clicks it.
     *
     * <p>Known limitation, left unchanged: although annotated {@code @Then}, the step contains no
     * assertion, so it fails only when an element cannot be found or clicked, or a wait times out.
     * <p>
     * Gherkin: {@code User can print the profile}
     */
    @Then("User can print the profile")
    public void userCanPrintTheProfile() {
        crm.nameCustomer.click();
        wait.until(ExpectedConditions.visibilityOf(crm.nameCustomer));
        crm.printButton.click();
        wait.until(ExpectedConditions.visibilityOf(crm.duePaymentButton));
        crm.duePaymentButton.click();

    }
}
