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
 * Cucumber glue class providing step definitions for CRM (Customer Relationship Management)
 * module tests in the Odoo application.
 * 
 * <p>This class implements step definitions for comprehensive CRM pipeline management functionality,
 * including:</p>
 * <ul>
 *   <li>Opportunity creation with revenue and priority configuration</li>
 *   <li>Pipeline editing and information updates</li>
 *   <li>Drag-and-drop stage transitions using Selenium Actions API</li>
 *   <li>Customer registration workflows</li>
 *   <li>Print and due-payment report generation actions</li>
 * </ul>
 * 
 * <p>The class uses Gherkin step bindings ({@code @When}, {@code @Then}, {@code @And} annotations)
 * to map human-readable step text from feature files to executable Java methods. Each method
 * corresponds to a specific step in the CRM test scenarios.</p>
 * 
 * <p><strong>Implementation Notes:</strong></p>
 * <ul>
 *   <li>Uses Selenium {@link Actions} class for complex drag-and-drop operations between
 *       pipeline stages in the kanban view</li>
 *   <li>Employs explicit waits via {@link WebDriverWait} with a 2-second timeout. Note that
 *       this short timeout may cause flaky tests on slower environments or under heavy load</li>
 *   <li>Several methods contain hard-coded test data values, which limits test flexibility
 *       and reusability</li>
 * </ul>
 * 
 * @see com.testinium.pages.CrmP
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.interactions.Actions
 */
public class Crm {

    /**
     * CrmP page object instance providing WebElement locators for CRM module UI interactions.
     * 
     * <p>This field is initialized eagerly at field declaration time using the default
     * constructor of {@link CrmP}, which internally initializes all WebElements via
     * Selenium's PageFactory pattern.</p>
     * 
     * @see CrmP
     */
    CrmP crm = new CrmP();

    /**
     * WebDriverWait instance configured for explicit waits with a 2-second timeout.
     * 
     * <p><strong>Warning:</strong> The 2-second timeout is very short and may cause flaky
     * tests on slower environments, networks with latency, or systems under heavy load.
     * Consider increasing this timeout for more stable test execution.</p>
     * 
     * <p>This wait object uses {@link Driver#getDriver()} at initialization time, which
     * couples the object instantiation to driver availability. The driver must be
     * initialized before this class is instantiated.</p>
     * 
     * @see WebDriverWait
     * @see Driver#getDriver()
     */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),2);


    /**
     * Navigates to the CRM module by clicking the CRM dashboard link.
     * 
     * <p>This step clicks on the CRM navigation link and then waits for the link
     * element to become visible, confirming successful navigation to the CRM module.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code When User click on the crm dashboard}</p>
     * 
     * @see CrmP#crmLink
     */
    @When("User click on the crm dashboard")
    public void user_click_on_the_crm_dashboard() {
        crm.crmLink.click();
        wait.until(ExpectedConditions.visibilityOf(crm.crmLink));
    }

    /**
     * Clicks the create button to initiate new pipeline/opportunity creation.
     * 
     * <p>This step clicks the create button (identified by accesskey='c') which opens
     * the form for creating a new opportunity/pipeline entry in the CRM module.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code And User click on the pipeline button}</p>
     * 
     * @see CrmP#createButton
     */
    @And("User click on the pipeline button")
    public void userClickOnThePipelineButton() {
        crm.createButton.click();
        wait.until(ExpectedConditions.visibilityOf(crm.createButton));

    }

    /**
     * Creates a new opportunity/pipeline entry with hard-coded test data.
     * 
     * <p>This step performs the following actions to create a new pipeline entry:</p>
     * <ol>
     *   <li>Enters "test" as the opportunity title and submits with {@link Keys#ENTER}</li>
     *   <li>Selects a customer by clicking the customer field and choosing '&amp;CC' customer</li>
     *   <li>Clears existing expected revenue value and enters "8"</li>
     *   <li>Clicks the priority selector to set priority level</li>
     *   <li>Confirms creation by clicking the createPipeline button</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> This method uses hard-coded test data values ("test", "8"),
     * which limits test reusability. Consider parameterizing these values for more
     * flexible test scenarios.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code And User can create the new pipeline}</p>
     * 
     * @see CrmP#opportunityTitle
     * @see CrmP#customer
     * @see CrmP#customerId
     * @see CrmP#expectedRevenue
     * @see CrmP#priority
     * @see CrmP#createPipeline
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
     * Verifies the total price calculation after adding a new pipeline entry.
     * 
     * <p>This step performs the following verification logic:</p>
     * <ol>
     *   <li>Parses the current total price from the {@link CrmP#totalPrice} element text</li>
     *   <li>Adds 8 (the revenue value entered in the previous step) to the parsed value</li>
     *   <li>Asserts that the result equals the expected value of 89</li>
     * </ol>
     * 
     * <p><strong>Warning:</strong> This test uses a hard-coded expected value of 89, making
     * it a fragile test that depends on a specific data state. The test will fail if the
     * initial total price is not 81 (89 - 8). Consider using dynamic calculations or
     * data-driven approaches for more robust testing.</p>
     * 
     * <p>Debug output is printed to console showing actual and expected values.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code And User can see the total price}</p>
     * 
     * @see CrmP#totalPrice
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
     * Verifies that the newly created pipeline entry appears in the kanban view.
     * 
     * <p>This step asserts that the text content of the {@link CrmP#findTitleTest} element
     * equals "test", confirming that the pipeline entry created in the previous steps
     * is visible in the CRM kanban board.</p>
     * 
     * <p>Debug output is printed to console showing actual and expected name values.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code Then User can see new pipeline}</p>
     * 
     * @see CrmP#findTitleTest
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
     * Edits an existing pipeline/opportunity with parameterized values.
     * 
     * <p>This step performs the following actions to update a pipeline entry:</p>
     * <ol>
     *   <li>Clicks on the pipeline card to select it</li>
     *   <li>Enters edit mode by clicking the edit button</li>
     *   <li>Clears and updates the opportunity title field with the new value</li>
     *   <li>Clears and updates the expected revenue field with the new value</li>
     *   <li>Clears and updates the probability field with the new value</li>
     * </ol>
     * 
     * <p>Each field update uses {@link Keys#ENTER} after entering the value to submit
     * the change. Note that the edit fields use generated ID locators (e.g., 
     * {@code o_field_input_125}), which may be unstable across different Odoo
     * installations or versions.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code And User can change any user's information like {string} , {string} and {string}}</p>
     * 
     * @param opportunity the new opportunity title to enter in the edit form
     * @param revenue the new expected revenue value to enter
     * @param probability the new probability percentage to enter (0-100)
     * @see CrmP#buttonPipeline
     * @see CrmP#editButton
     * @see CrmP#opportunityTitleEdit
     * @see CrmP#expectedRevenueEdit
     * @see CrmP#probabilityEdit
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
     * Saves the edited opportunity information by clicking the save button.
     * 
     * <p>This step waits for the probability field to become visible (confirming the
     * edit form is ready), then clicks the save button (identified by accesskey='s')
     * to persist all changes made to the opportunity record.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code And User can save information}</p>
     * 
     * @see CrmP#probabilityEdit
     * @see CrmP#saveEdit
     */
    @And("User can save information")
    public void userCanSaveInformation() {
        wait.until(ExpectedConditions.visibilityOf(crm.probabilityEdit));
        crm.saveEdit.click();
    }

    /**
     * Verifies that the edited opportunity information was saved correctly.
     * 
     * <p>This step performs the following verification:</p>
     * <ol>
     *   <li>Clicks the pipeline sidebar navigation button to return to the pipeline view</li>
     *   <li>Waits for the pipeline button to become visible</li>
     *   <li>Retrieves the text from the {@link CrmP#findTitleTest} element</li>
     *   <li>Asserts that the title equals "Test2" (the expected edited value)</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> This test uses a hard-coded expected value of "Test2",
     * assuming that specific edit operations were performed in the preceding steps.
     * This creates a tight coupling between test steps.</p>
     * 
     * <p>Debug output is printed to console showing actual and expected name values.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code Then User can verify the information}</p>
     * 
     * @see CrmP#pipelineSideButton
     * @see CrmP#findTitleTest
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
     * Performs a drag-and-drop operation to move a pipeline entry between stages.
     * 
     * <p>This step uses the Selenium {@link Actions} API to execute a drag-and-drop
     * operation that moves a pipeline card from one kanban stage to another. The
     * action sequence is:</p>
     * <ol>
     *   <li>Click and hold on the {@link CrmP#progressPipeline} element (source)</li>
     *   <li>Pause for 2 seconds to allow UI to register the drag state</li>
     *   <li>Move to the {@link CrmP#progressPipeline2} element (target stage)</li>
     *   <li>Pause for 2 seconds to allow UI to recognize the drop target</li>
     *   <li>Release the mouse button to complete the drop</li>
     *   <li>Perform the complete action chain</li>
     * </ol>
     * 
     * <p>An additional 2-second {@link Thread#sleep(long)} is executed after the
     * drag-and-drop operation to allow the UI to fully update and persist the
     * stage change.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code And User can drag and drop the pipeline}</p>
     * 
     * @throws InterruptedException if the thread sleep operation is interrupted
     * @see org.openqa.selenium.interactions.Actions
     * @see CrmP#progressPipeline
     * @see CrmP#progressPipeline2
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
     * Verifies that the pipeline entry was successfully moved to the new stage.
     * 
     * <p>This step verifies the drag-and-drop operation succeeded by checking that
     * the text content in the new stage location (data-id='2' card area) contains
     * the expected pipeline entry. The {@link CrmP#testVerify} element targets
     * the card content in the second kanban column.</p>
     * 
     * <p>The assertion confirms that the actual text contains "test" (the name
     * of the moved pipeline entry).</p>
     * 
     * <p>Debug output is printed to console showing actual and expected name values.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code Then User can see the new changes in progress}</p>
     * 
     * @see CrmP#testVerify
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
     * Registers a new customer in the CRM module.
     * 
     * <p>This step performs the following actions to create a new customer:</p>
     * <ol>
     *   <li>Clicks the customer sidebar button to navigate to the customers section</li>
     *   <li>Clicks the create customer button to open the customer creation form</li>
     *   <li>Enters "Test" as the customer name with {@link Keys#ENTER} to submit</li>
     *   <li>Clicks the create customer confirmation button</li>
     *   <li>Enters "aa" in the search bar with {@link Keys#ENTER} (search purpose unclear)</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> This method uses hard-coded test data values ("Test", "aa").
     * The purpose of the final search action with "aa" is not clear and may be a
     * verification step or cleanup action.</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code And User can register new customer}</p>
     * 
     * @see CrmP#customerSideButton
     * @see CrmP#createCustomer
     * @see CrmP#inputName
     * @see CrmP#createCustomerButton
     * @see CrmP#searchingText
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
     * Initiates the print/due-payment workflow for a customer profile.
     * 
     * <p>This step performs the following actions to generate a due payment report:</p>
     * <ol>
     *   <li>Clicks the {@link CrmP#nameCustomer} element to select the customer profile</li>
     *   <li>Clicks the {@link CrmP#printButton} to open the print options menu</li>
     *   <li>Clicks the {@link CrmP#duePaymentButton} to generate the due payment report</li>
     * </ol>
     * 
     * <p><strong>Warning:</strong> The {@link CrmP#printButton} uses an absolute XPath
     * locator ({@code /html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button}),
     * which is an extremely brittle selector. This locator is highly likely to break
     * with any UI changes and should be replaced with a more stable locator strategy
     * (e.g., by class, ID, or relative XPath).</p>
     * 
     * <p><strong>Gherkin Step:</strong> {@code Then User can print the profile}</p>
     * 
     * @see CrmP#nameCustomer
     * @see CrmP#printButton
     * @see CrmP#duePaymentButton
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
