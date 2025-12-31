package com.testinium.step_definitions;

import com.testinium.pages.ContactsP;
import com.testinium.utilities.Driver;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Cucumber glue class providing step definitions for Contacts module tests in the Odoo application.
 * 
 * <p>This class implements step definitions for contact CRUD (Create, Read, Update, Delete) operations
 * including:</p>
 * <ul>
 *   <li>Navigation to Contacts module dashboard</li>
 *   <li>Contact creation with name, street address, phone, and email fields</li>
 *   <li>Profile selection in both kanban and list views</li>
 *   <li>Contact deletion via Action menu dropdown</li>
 *   <li>Contact editing operations</li>
 *   <li>Print and due payment actions for contacts</li>
 * </ul>
 * 
 * <p>Each public method in this class is annotated with Cucumber annotations ({@code @When}, {@code @Then})
 * that bind Gherkin step text from feature files to executable Java methods. The step text patterns
 * support both literal matching and parameterized inputs using {@code {string}} placeholders.</p>
 * 
 * <p>This class uses explicit waits via {@link WebDriverWait} with a 20-second timeout to handle
 * asynchronous page loading and element visibility conditions. Additionally, some methods employ
 * {@link Thread#sleep(long)} for page stabilization after navigation actions.</p>
 * 
 * @see com.testinium.pages.ContactsP
 * @see com.testinium.utilities.Driver
 * @see io.cucumber.java.en.When
 * @see io.cucumber.java.en.Then
 */
public class Contacts {

    /**
     * ContactsP page object instance providing WebElement locators for Contacts module UI interactions.
     * 
     * <p>This field is initialized eagerly at field declaration time, which triggers PageFactory
     * initialization for all {@code @FindBy} annotated elements in the ContactsP class. The page object
     * encapsulates all WebElement locators specific to the Contacts module including navigation links,
     * form inputs, action buttons, and list/kanban view elements.</p>
     * 
     * @see ContactsP
     */
    ContactsP contactP = new ContactsP();

    /**
     * WebDriverWait instance for explicit waits with 20-second timeout.
     * 
     * <p>Uses {@link Driver#getDriver()} at initialization time, which couples this object's
     * instantiation to driver availability. The 20-second timeout provides sufficient wait time
     * for Odoo's AJAX-heavy UI to complete loading and element rendering operations.</p>
     * 
     * <p>This wait instance is used throughout the step definitions for visibility conditions
     * before interacting with elements that may load asynchronously.</p>
     * 
     * @see Driver#getDriver()
     * @see WebDriverWait
     * @see ExpectedConditions
     */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 20);

    /**
     * Navigates to the Contacts module dashboard in the Odoo application.
     * 
     * <p>This step definition handles the {@code @When "User is at Contact dashboard"} Gherkin step.
     * It performs navigation by clicking the contactModule link element which represents the
     * "Contacts" entry in the Odoo main navigation menu.</p>
     * 
     * <p>A 3-second {@link Thread#sleep(long)} is used before clicking to allow for page
     * stabilization, particularly after login or other navigation events that may trigger
     * asynchronous content loading.</p>
     * 
     * @throws InterruptedException if the thread sleep is interrupted while waiting for page stabilization
     * @see ContactsP#contactModule
     */
    @When("User is at Contact dashboard")
    public void user_is_at_contact_dashboard() throws InterruptedException {
        Thread.sleep(3000);
        contactP.contactModule.click();
    }

    /**
     * Clicks the create button to initiate new contact creation.
     * 
     * <p>This step definition handles the {@code @When "User clicks the create button"} Gherkin step.
     * It clicks the create button identified by accesskey='c' to open the contact creation form
     * in the Odoo Contacts module.</p>
     * 
     * <p>A 3-second {@link Thread#sleep(long)} is used before clicking to ensure the dashboard
     * has fully loaded and the create button is interactable.</p>
     * 
     * @throws InterruptedException if the thread sleep is interrupted while waiting for page stabilization
     * @see ContactsP#createContact
     */
    @When("User clicks the create button")
    public void user_clicks_the_create_button() throws InterruptedException {
        Thread.sleep(3000);
        contactP.createContact.click();
    }

    /**
     * Enters the contact name into the name input field.
     * 
     * <p>This step definition handles the {@code @When "User enters name {string}"} Gherkin step.
     * It is a parameterized step that accepts the contact name from the Cucumber step parameter.</p>
     * 
     * <p>The method waits for the name input field to become visible using explicit wait,
     * clears any existing value in the field, and then sends the new name value. This ensures
     * clean input even when editing an existing contact.</p>
     * 
     * @param string the contact name to enter, provided from the Cucumber step parameter enclosed in quotes
     * @see ContactsP#nameInput
     * @see ExpectedConditions#visibilityOf(org.openqa.selenium.WebElement)
     */
    @When("User enters name {string}")
    public void user_enters_name(String string) {
        wait.until(ExpectedConditions.visibilityOf(contactP.nameInput));
        contactP.nameInput.clear();
        contactP.nameInput.sendKeys(string);
    }

    /**
     * Enters the street address into the street input field.
     * 
     * <p>This step definition handles the {@code @When "User enters {string}"} Gherkin step.
     * It is a parameterized step that accepts the street address from the Cucumber step parameter.</p>
     * 
     * <p>Unlike the name input, this method sends the street name directly to the input field
     * without clearing existing content, which appends to any pre-existing text.</p>
     * 
     * @param streetName the street address to enter, provided from the Cucumber step parameter enclosed in quotes
     * @see ContactsP#streetInput
     */
    @When("User enters {string}")
    public void user_enters(String streetName) {
        contactP.streetInput.sendKeys(streetName);
    }

    /**
     * Enters the phone number and email address into their respective input fields.
     * 
     * <p>This step definition handles the {@code @When "User enters {string} and {string}"} Gherkin step.
     * It is a dual-parameterized step that accepts both phone number and email values from
     * the Cucumber step parameters.</p>
     * 
     * <p>Both values are sent directly to their respective input fields without clearing,
     * completing the contact form with communication details.</p>
     * 
     * @param phoneNo the phone number to enter, provided as the first quoted string parameter
     * @param eMail the email address to enter, provided as the second quoted string parameter
     * @see ContactsP#phoneNoInput
     * @see ContactsP#emailInput
     */
    @When("User enters {string} and {string}")
    public void user_enters_and(String phoneNo, String eMail) {
        contactP.phoneNoInput.sendKeys(phoneNo);
        contactP.emailInput.sendKeys(eMail);
    }

    /**
     * Navigates back to the Contacts dashboard and confirms any dialog after contact creation.
     * 
     * <p>This step definition handles the {@code @Then "User sees the created new contact details at dashboard"}
     * Gherkin step. It performs navigation back to the main Contacts module and handles the
     * confirmation dialog that may appear when leaving an unsaved form.</p>
     * 
     * <p>The method clicks the contactModule link, waits for it to become visible (indicating
     * page transition), and then clicks the Ok button to confirm any pending dialog.</p>
     * 
     * @see ContactsP#contactModule
     * @see ContactsP#okBtn
     * @see ExpectedConditions#visibilityOf(org.openqa.selenium.WebElement)
     */
    @Then("User sees the created new contact details at dashboard")
    public void user_sees_the_created_new_contact_details_at_dashboard() {
        contactP.contactModule.click();
        wait.until(ExpectedConditions.visibilityOf(contactP.contactModule));
        contactP.okBtn.click();
    }

    /**
     * Switches to list view and selects a contact profile via checkbox.
     * 
     * <p>This step definition handles the {@code @When "User clicks list section and choose the profile"}
     * Gherkin step. It performs two actions:</p>
     * <ol>
     *   <li>Clicks the list button (accesskey='l') to switch from kanban to list view</li>
     *   <li>After a 3-second stabilization pause, clicks the checkbox to select a contact profile</li>
     * </ol>
     * 
     * <p>The profile selection is performed via the newContact checkbox element, which represents
     * a specific contact row's checkbox in the list view (identified by index position 12).</p>
     * 
     * @throws InterruptedException if the thread sleep is interrupted while waiting for view switch
     * @see ContactsP#callList
     * @see ContactsP#newContact
     */
    @When("User clicks list section and choose the profile")
    public void user_clicks_list_section_and_choose_the_profile() throws InterruptedException {
        contactP.callList.click();
        Thread.sleep(3000);
        contactP.newContact.click();
    }

    /**
     * Opens the Action dropdown menu and selects the delete option.
     * 
     * <p>This step definition handles the {@code @When "User clicks Action to choose delete button"}
     * Gherkin step. It performs the delete action through the Odoo sidebar action menu:</p>
     * <ol>
     *   <li>Clicks the actionInput to expand the Action dropdown menu</li>
     *   <li>Waits 3 seconds for the dropdown to fully render</li>
     *   <li>Clicks the deleteInput (identified by data-index='3') to select the delete action</li>
     * </ol>
     * 
     * <p>This action requires a contact to be pre-selected in the list view for the delete
     * operation to apply to the selected record(s).</p>
     * 
     * @throws InterruptedException if the thread sleep is interrupted while waiting for dropdown expansion
     * @see ContactsP#actionInput
     * @see ContactsP#deleteInput
     */
    @When("User clicks Action to choose delete button")
    public void user_clicks_action_to_choose_delete_button() throws InterruptedException {
        contactP.actionInput.click();
        Thread.sleep(3000);
        contactP.deleteInput.click();
    }

    /**
     * Clicks the Edit button to enter edit mode for the selected contact.
     * 
     * <p>This step definition handles the {@code @When "User clicks for editing button"} Gherkin step.
     * It clicks the primary Edit button in the contact detail view to switch the form from
     * read-only mode to edit mode, enabling field modifications.</p>
     * 
     * @see ContactsP#editBtn
     */
    @When("User clicks for editing button")
    public void user_clicks_for_editing_button() {
        contactP.editBtn.click();
    }

    /**
     * Verifies that the contact deletion was successful by checking the delete confirmation.
     * 
     * <p>This step definition handles the {@code @Then "User sees deleted profile"} Gherkin step.
     * It performs an assertion to verify the deletion operation result.</p>
     * 
     * <p><strong>Note:</strong> The current assertion logic may be incorrect as it compares the
     * text of the deleteInput dropdown option against "Deleted". This likely does not represent
     * the actual deletion confirmation message. The expected behavior should verify a deletion
     * confirmation dialog or success message instead.</p>
     * 
     * @see ContactsP#deleteInput
     * @see Assert#assertEquals(Object, Object)
     */
    @Then("User sees deleted profile")
    public void user_sees_deleted_profile() {
        String actualMsg = contactP.deleteInput.getText();
        String expectedMsg = "Deleted";
        Assert.assertEquals(actualMsg, expectedMsg);
    }

    /**
     * Selects the first contact in kanban view and waits for the profile detail view to load.
     * 
     * <p>This step definition handles the {@code @When "User selects the profile"} Gherkin step.
     * It performs selection by clicking the first user card in the kanban view, then waits
     * for the edit title element to become visible, indicating that the contact detail/profile
     * view has fully loaded.</p>
     * 
     * <p>The explicit wait ensures proper synchronization before subsequent steps attempt to
     * interact with profile elements.</p>
     * 
     * @see ContactsP#firstUser
     * @see ContactsP#editTitle
     * @see ExpectedConditions#visibilityOf(org.openqa.selenium.WebElement)
     */
    @When("User selects the profile")
    public void user_selects_the_profile() {
        contactP.firstUser.click();
        wait.until(ExpectedConditions.visibilityOf(contactP.editTitle));
    }

    /**
     * Navigates back to the Contacts dashboard after editing a contact.
     * 
     * <p>This step definition handles the {@code @Then "User sees the updated contact details at dashboard"}
     * Gherkin step. It performs navigation back to the main Contacts module by clicking
     * the contactModule link.</p>
     * 
     * <p><strong>Note:</strong> This method only performs navigation and does not include any
     * assertion to verify that the contact updates are reflected on the dashboard. Verification
     * of the update is not implemented in the current version.</p>
     * 
     * @see ContactsP#contactModule
     */
    @Then("User sees the updated contact details at dashboard")
    public void user_sees_the_updated_contact_details_at_dashboard() {
        contactP.contactModule.click();
    }

//    @When("User clicks and goes directly to the profile")
//    public void user_clicks_and_goes_directly_to_the_profile() {
//
//    }

    /**
     * Clicks the print dropdown trigger to open the print options menu.
     * 
     * <p>This step definition handles the {@code @When "User clicks the print button and then select due payments"}
     * Gherkin step. It clicks the printInput element which represents a dropdown trigger
     * button in an open dropdown state.</p>
     * 
     * <p>A 3-second {@link Thread#sleep(long)} is used after clicking to allow the dropdown
     * menu to fully expand and render its options. This step relies on the dropdown being
     * in an "open" state class for subsequent action selection.</p>
     * 
     * <p><strong>Note:</strong> The step name mentions selecting "due payments" but this method
     * only opens the dropdown; the actual due payment selection is performed by the subsequent
     * step {@link #user_can_see_the_downloaded_file()}.</p>
     * 
     * @throws InterruptedException if the thread sleep is interrupted while waiting for dropdown expansion
     * @see ContactsP#printInput
     */
    @When("User clicks the print button and then select due payments")
    public void user_clicks_the_print_button_and_then_select_due_payments() throws InterruptedException {
        contactP.printInput.click();
        Thread.sleep(3000);
    }

    /**
     * Clicks the due payment option to initiate the download or print action.
     * 
     * <p>This step definition handles the {@code @Then "User can see the downloaded file"} Gherkin step.
     * It clicks the duePayment element to trigger the due payment report generation or download.</p>
     * 
     * <p><strong>Note:</strong> The step name implies file verification ("User can see the downloaded file")
     * but the actual implementation only performs a click action on the due payment option.
     * No file system verification or download confirmation is implemented in the current version.</p>
     * 
     * @see ContactsP#duePayment
     */
    @Then("User can see the downloaded file")
    public void user_can_see_the_downloaded_file() {
        contactP.duePayment.click();
    }
}
