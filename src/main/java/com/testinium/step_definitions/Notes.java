package com.testinium.step_definitions;

import org.junit.Assert;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import com.testinium.pages.InventoryP;
import com.testinium.pages.NotesP;
import com.testinium.utilities.Driver;
import org.openqa.selenium.Keys;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Step Definition for the Notes module of the Odoo/Upgenix application, binding the steps of
 * {@code Notes.feature}.
 *
 * <p>The steps create a tagged note, edit a note's description, verify the Notes list, and drag a
 * card from the New column to the Today column with Selenium {@code Actions}.
 *
 * <p>Page Objects:
 * <ul>
 *   <li>{@link com.testinium.pages.NotesP} ({@code notesP}): the Notes module elements that every
 *       step drives.</li>
 *   <li>{@link com.testinium.pages.InventoryP} ({@code inventoryP}): used only for its save button,
 *       which {@link #user_enters_new_description()} clicks to save the edited note.</li>
 * </ul>
 *
 * <p>Both Page Objects and the 20-second {@code WebDriverWait} are created in field initializers
 * that call {@link com.testinium.utilities.Driver#getDriver()}, so instantiating this class opens,
 * or reuses, the current thread's browser session.
 */
public class Notes {

    /** Inventory Page Object, used only for its save button {@link com.testinium.pages.InventoryP#saveBtn}. */
    InventoryP inventoryP = new InventoryP();
    /** Notes Page Object whose elements every step in this class drives. */
    NotesP notesP = new NotesP();

    /** Explicit wait of 20 seconds on the thread's driver. */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 20);

    /**
     * Opens the Notes module: sleeps for 2 seconds, then clicks {@code notesP.notesModule}.
     * <p>
     * Gherkin: {@code User clicks the Notes module}
     *
     * @throws InterruptedException if interrupted during {@code Thread.sleep}
     */
    @When("User clicks the Notes module")
    public void user_clicks_the_notes_module() throws InterruptedException {
        Thread.sleep(2000);
        notesP.notesModule.click();
    }

    /**
     * Waits up to 20 seconds for {@code notesP.creatingNotes} to become visible, then clicks it to
     * open a new note form.
     * <p>
     * Gherkin: {@code User clicks create button in Notes module}
     */
    @When("User clicks create button in Notes module")
    public void user_clicks_create_button_in_notes_module() {
        wait.until(ExpectedConditions.visibilityOf(notesP.creatingNotes));
        notesP.creatingNotes.click();
    }

    /**
     * Types a hard-coded tag name followed by ENTER into the tags input {@code notesP.tagsN}, then
     * clicks {@code notesP.tabindex}, the create-and-edit entry of the tags drop-down.
     * <p>
     * Gherkin: {@code User enters a tag name}
     */
    @When("User enters a tag name")
    public void user_enters_a_tag_name() {
        notesP.tagsN.sendKeys("New Tag", Keys.ENTER);
        notesP.tabindex.click();
    }

    /**
     * Types a hard-coded description into {@code notesP.description} and then also clicks
     * {@code notesP.saveBtn}, so this step already saves the note. In {@code Notes.feature} the
     * following save step, {@link #user_clicks_save_button()}, clicks the save button a second time.
     * <p>
     * Gherkin: {@code User enters description}
     */
    @When("User enters description")
    public void user_enters_description() {
        notesP.description.sendKeys("This note is an example for the Testinium App");
        notesP.saveBtn.click();
    }
    /**
     * Waits up to 20 seconds for {@code notesP.saveBtn} to become visible, then clicks it to save
     * the note form.
     * <p>
     * Gherkin: {@code User clicks save button}
     */
    @When("User clicks save button")
    public void user_clicks_save_button() {
        wait.until(ExpectedConditions.visibilityOf(notesP.saveBtn));
        notesP.saveBtn.click();
    }
    /**
     * Verifies note creation: reads the text of {@code notesP.createdMessage} and asserts that it
     * equals a hard-coded confirmation text. {@code Assert.assertEquals} receives the actual value
     * first and the expected value second, the reverse of the JUnit (expected, actual) order, so a
     * failure message reports the two values swapped.
     * <p>
     * Gherkin: {@code User sees the created new notes}
     */
    @Then("User sees the created new notes")
    public void user_sees_the_created_new_notes() {
        String actualMessage = notesP.createdMessage.getText();
        String expecgedMessage = "Note created";
        Assert.assertEquals(actualMessage, expecgedMessage);
    }

    /**
     * Opens a note for editing by clicking {@code notesP.appK}, a note entry that must already exist
     * in the test data.
     * <p>
     * Gherkin: {@code User clicks the edit button}
     */
    @When("User clicks the edit button")
    public void user_clicks_the_edit_button() {
        notesP.appK.click();
    }

    /**
     * Replaces the note body: clears {@code notesP.description} and types a hard-coded text. The step
     * saves through {@code inventoryP.saveBtn}, the Inventory Page Object's save button locator
     * ({@link com.testinium.pages.InventoryP#saveBtn}), instead of {@code notesP.saveBtn}; both
     * fields use the same XPath, so they locate the same form save button. It then clicks
     * {@code notesP.notesModule} to return to the Notes list.
     * <p>
     * Gherkin: {@code User enters new description}
     */
    @When("User enters new description")
    public void user_enters_new_description() {
        notesP.description.clear();
        notesP.description.sendKeys("FKASDFGASDFADSFADS");
        inventoryP.saveBtn.click();
        notesP.notesModule.click();
    }

    /**
     * Waits up to 20 seconds for {@code notesP.notesModule} to become visible, clicks it, and asserts
     * that it is displayed. The assertion checks the Notes menu link, not the contents of the list.
     * <p>
     * Gherkin: {@code User should see the Notes list}
     */
    @Then("User should see the Notes list")
    public void user_should_see_the_notes_list() {
        wait.until(ExpectedConditions.visibilityOf(notesP.notesModule));
        notesP.notesModule.click();
        Assert.assertTrue(notesP.notesModule.isDisplayed());
    }

    /**
     * Drags a card from the New column to the Today column with Selenium {@code Actions}:
     * {@code clickAndHold} on {@code notesP.newTable}, a 2000 ms pause, {@code moveToElement} to
     * {@code notesP.todayTable}, another 2000 ms pause, then {@code release} and {@code perform}.
     * <p>
     * Gherkin: {@code User move element from New section to Today section}
     */
    @When("User move element from New section to Today section")
    public void user_move_element_from_new_section_to_today_section() {
        Actions actions = new Actions(Driver.getDriver());
        actions.clickAndHold(notesP.newTable).pause(2000).moveToElement(notesP.todayTable).pause(2000).release().perform();
    }

    /**
     * Verifies the drop target: reads the text of {@code notesP.todayTable} and asserts that it
     * equals a hard-coded column label. It compares only the drop target's text and does not look
     * for the dragged card. As in {@link #user_sees_the_created_new_notes()}, the actual value is
     * passed to {@code Assert.assertEquals} first and the expected value second.
     * <p>
     * Gherkin: {@code User sees Today new added element}
     */
    @Then("User sees Today new added element")
    public void user_sees_today_new_added_element() {
        String actualTable = notesP.todayTable.getText();
        String expectedTable = "Today";

        Assert.assertEquals(actualTable, expectedTable);
    }
}