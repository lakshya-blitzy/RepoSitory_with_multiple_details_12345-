package com.testinium.step_definitions;

import com.testinium.pages.ContactsP;
import com.testinium.utilities.Driver;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Step Definition for the Contacts module of the Odoo/Upgenix ERP under test, bound to the steps of
 * {@code Contact.feature}.
 *
 * <p>The steps cover creating a contact, choosing a profile from the list view, deleting it through
 * the Action menu, selecting and editing a profile, and printing due payments. Every UI element is
 * reached through the Page Object {@link com.testinium.pages.ContactsP}, held in {@code contactP}.
 * {@code Contact.feature} also uses {@code User login to test other features}, bound in
 * {@link com.testinium.step_definitions.Session}, and {@code User clicks save button}, bound in
 * {@link com.testinium.step_definitions.Notes}.
 *
 * <p>Both {@code contactP} and the 20-second {@code WebDriverWait} are created in field initializers
 * that call {@link com.testinium.utilities.Driver#getDriver()}, so instantiating this class, which
 * Cucumber does for each scenario, opens or reuses the current thread's browser session.
 *
 * <p>Several steps pause with a fixed {@code Thread.sleep(3000)} instead of an explicit wait and
 * therefore declare {@code InterruptedException}.
 *
 * <p>Known gaps, left unchanged because this change adds documentation only:
 * <ul>
 *   <li>{@link #user_sees_the_created_new_contact_details_at_dashboard()} and
 *       {@link #user_sees_the_updated_contact_details_at_dashboard()} make no assertion.</li>
 *   <li>{@link #user_can_see_the_downloaded_file()} does not verify any downloaded file.</li>
 *   <li>{@link #user_sees_deleted_profile()} checks the text of the Action menu's Delete entry, not
 *       that the contact was removed.</li>
 * </ul>
 */
public class Contacts {

    /** Contacts Page Object; its constructor binds the {@code @FindBy} elements to the thread's driver. */
    ContactsP contactP = new ContactsP();

    /** Explicit wait of 20 seconds on the thread's driver. */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 20);

    /**
     * Pauses for 3 seconds, then opens the Contacts module by clicking {@code contactP.contactModule}.
     * <p>
     * Gherkin: {@code User is at Contact dashboard}
     *
     * @throws InterruptedException if interrupted during {@code Thread.sleep}
     */
    @When("User is at Contact dashboard")
    public void user_is_at_contact_dashboard() throws InterruptedException {
        Thread.sleep(3000);
        contactP.contactModule.click();
    }

    /**
     * Pauses for 3 seconds, then clicks the Create button {@code contactP.createContact}.
     * <p>
     * Gherkin: {@code User clicks the create button}
     *
     * @throws InterruptedException if interrupted during {@code Thread.sleep}
     */
    @When("User clicks the create button")
    public void user_clicks_the_create_button() throws InterruptedException {
        Thread.sleep(3000);
        contactP.createContact.click();
    }

    /**
     * Waits until the name input {@code contactP.nameInput} is visible, clears it and types the given
     * contact name.
     * <p>
     * Gherkin: {@code User enters name {string}}
     *
     * @param string the contact name bound to {@code {string}}
     */
    @When("User enters name {string}")
    public void user_enters_name(String string) {
        wait.until(ExpectedConditions.visibilityOf(contactP.nameInput));
        contactP.nameInput.clear();
        contactP.nameInput.sendKeys(string);
    }

    /**
     * Types the given street into the street input {@code contactP.streetInput}. The input is not
     * cleared first, so the text is added to any value it already holds.
     * <p>
     * Gherkin: {@code User enters {string}}
     *
     * @param streetName the street bound to {@code {string}}
     */
    @When("User enters {string}")
    public void user_enters(String streetName) {
        contactP.streetInput.sendKeys(streetName);
    }

    /**
     * Types the given phone number into {@code contactP.phoneNoInput} and the given email address into
     * {@code contactP.emailInput}. Neither input is cleared first.
     * <p>
     * Gherkin: {@code User enters {string} and {string}}
     *
     * @param phoneNo the phone number bound to the first {@code {string}}
     * @param eMail the email address bound to the second {@code {string}}
     */
    @When("User enters {string} and {string}")
    public void user_enters_and(String phoneNo, String eMail) {
        contactP.phoneNoInput.sendKeys(phoneNo);
        contactP.emailInput.sendKeys(eMail);
    }

    /**
     * Clicks the Contacts module link {@code contactP.contactModule}, waits until it is visible, then
     * clicks the Ok button {@code contactP.okBtn}. It makes no assertion, so it does not verify that
     * the new contact's details are shown.
     * <p>
     * Gherkin: {@code User sees the created new contact details at dashboard}
     */
    @Then("User sees the created new contact details at dashboard")
    public void user_sees_the_created_new_contact_details_at_dashboard() {
        contactP.contactModule.click();
        wait.until(ExpectedConditions.visibilityOf(contactP.contactModule));
        contactP.okBtn.click();
    }

    /**
     * Clicks the list-view button {@code contactP.callList}, pauses for 3 seconds, then clicks the list
     * row checkbox {@code contactP.newContact} to choose a profile.
     * <p>
     * Gherkin: {@code User clicks list section and choose the profile}
     *
     * @throws InterruptedException if interrupted during {@code Thread.sleep}
     */
    @When("User clicks list section and choose the profile")
    public void user_clicks_list_section_and_choose_the_profile() throws InterruptedException {
        contactP.callList.click();
        Thread.sleep(3000);
        contactP.newContact.click();
    }

    /**
     * Opens the Action dropdown {@code contactP.actionInput}, pauses for 3 seconds, then clicks its
     * Delete entry {@code contactP.deleteInput}.
     * <p>
     * Gherkin: {@code User clicks Action to choose delete button}
     *
     * @throws InterruptedException if interrupted during {@code Thread.sleep}
     */
    @When("User clicks Action to choose delete button")
    public void user_clicks_action_to_choose_delete_button() throws InterruptedException {
        contactP.actionInput.click();
        Thread.sleep(3000);
        contactP.deleteInput.click();
    }
    /**
     * Clicks the Edit button {@code contactP.editBtn} of the contact form.
     * <p>
     * Gherkin: {@code User clicks for editing button}
     */
    @When("User clicks for editing button")
    public void user_clicks_for_editing_button() {
        contactP.editBtn.click();
    }

    /**
     * Asserts that the text of {@code contactP.deleteInput} equals the hard-coded label
     * {@code "Deleted"}. It reads the same Delete entry that
     * {@link #user_clicks_action_to_choose_delete_button()} clicks and does not check that the contact
     * was removed. {@code Assert.assertEquals} receives the actual value first, so a failure message
     * reports the expected and actual values reversed.
     * <p>
     * Gherkin: {@code User sees deleted profile}
     */
    @Then("User sees deleted profile")
    public void user_sees_deleted_profile() {
        String actualMsg = contactP.deleteInput.getText();
        String expectedMsg = "Deleted";
        Assert.assertEquals(actualMsg, expectedMsg);
    }

    /**
     * Clicks the first contact card {@code contactP.firstUser}, then waits until the form title
     * {@code contactP.editTitle} is visible.
     * <p>
     * Gherkin: {@code User selects the profile}
     */
    @When("User selects the profile")
    public void user_selects_the_profile() {
        contactP.firstUser.click();
        wait.until(ExpectedConditions.visibilityOf(contactP.editTitle));
    }

    /**
     * Clicks the Contacts module link {@code contactP.contactModule} and nothing else. It makes no
     * assertion, so it does not verify that the updated contact details are shown.
     * <p>
     * Gherkin: {@code User sees the updated contact details at dashboard}
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
     * Clicks the Print dropdown {@code contactP.printInput}, then pauses for 3 seconds. The due-payment
     * entry is selected by the next step, {@link #user_can_see_the_downloaded_file()}.
     * <p>
     * Gherkin: {@code User clicks the print button and then select due payments}
     *
     * @throws InterruptedException if interrupted during {@code Thread.sleep}
     */
    @When("User clicks the print button and then select due payments")
    public void user_clicks_the_print_button_and_then_select_due_payments() throws InterruptedException {
        contactP.printInput.click();
        Thread.sleep(3000);
    }

    /**
     * Clicks the due-payment entry {@code contactP.duePayment} of the open Print dropdown. It does not
     * verify that any file was downloaded.
     * <p>
     * Gherkin: {@code User can see the downloaded file}
     */
    @Then("User can see the downloaded file")
    public void user_can_see_the_downloaded_file() {
        contactP.duePayment.click();
    }
}
