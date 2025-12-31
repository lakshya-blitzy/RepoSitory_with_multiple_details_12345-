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
 * Cucumber glue class providing step definitions for Notes module tests in the Odoo application.
 * 
 * <p>This class implements step definitions for comprehensive note management functionality including:
 * <ul>
 *   <li>Notes module navigation from the main application menu</li>
 *   <li>Note creation with tags and rich-text description content</li>
 *   <li>Note editing with description updates</li>
 *   <li>Notes list verification and display validation</li>
 *   <li>Kanban drag-and-drop operations between "New" and "Today" columns using Selenium Actions API</li>
 * </ul>
 * 
 * <p>The class uses Gherkin step bindings through {@code @When} and {@code @Then} annotations
 * that map step text patterns to executable Java methods for Cucumber integration.
 * 
 * <p><b>Key Implementation Details:</b>
 * <ul>
 *   <li>Uses Selenium {@link Actions} class for complex drag-and-drop operations in kanban view</li>
 *   <li>Employs explicit waits via {@link WebDriverWait} with a 20-second timeout to handle
 *       potentially slow Notes module page loads and element visibility</li>
 *   <li>Contains a cross-page object dependency by importing {@link InventoryP} for saveBtn
 *       element reuse, which could be refactored for better maintainability</li>
 * </ul>
 * 
 * <p><b>Test Coverage:</b> Notes module CRUD operations and kanban board interactions
 * 
 * @see com.testinium.pages.NotesP
 * @see com.testinium.pages.InventoryP
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.interactions.Actions
 */
public class Notes {

    /**
     * InventoryP page object instance used for accessing shared UI elements.
     * 
     * <p><b>Note:</b> This page object is used only for {@code saveBtn} element access,
     * representing a cross-page object dependency. This design could be refactored by
     * either extracting common elements to a shared base page or ensuring each page
     * object is self-contained with its own save button locator.
     * 
     * @see InventoryP#saveBtn
     */
    InventoryP inventoryP = new InventoryP();

    /**
     * NotesP page object instance providing WebElement locators for Notes module UI interactions.
     * 
     * <p>This page object contains locators for:
     * <ul>
     *   <li>Navigation elements (notesModule)</li>
     *   <li>Note creation elements (creatingNotes, tagsN, description, saveBtn)</li>
     *   <li>Tag management elements (tabindex for "Create and Edit..." option)</li>
     *   <li>Kanban column elements (newTable, todayTable for drag-and-drop)</li>
     *   <li>Verification elements (createdMessage, appK)</li>
     * </ul>
     * 
     * <p>Initialized eagerly at field declaration time, which requires the WebDriver
     * to be available via {@link Driver#getDriver()} at object instantiation.
     * 
     * @see NotesP
     */
    NotesP notesP = new NotesP();

    /**
     * WebDriverWait instance configured for explicit waits with a 20-second timeout.
     * 
     * <p>The longer timeout (20 seconds compared to typical 10-second defaults) is used
     * to accommodate potentially slow Notes module loads, especially when dealing with
     * rich-text editors and kanban board rendering.
     * 
     * <p><b>Note:</b> This wait instance is initialized at field declaration time using
     * {@link Driver#getDriver()}, which couples object instantiation to driver availability.
     * The wait is used throughout step methods for element visibility conditions.
     * 
     * @see WebDriverWait
     * @see ExpectedConditions
     */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(), 20);

    /**
     * Navigates to the Notes module by clicking on the Notes menu item.
     * 
     * <p>This step implements the Gherkin step: <b>"User clicks the Notes module"</b>
     * 
     * <p>The method includes a 2-second Thread.sleep before clicking to allow for
     * page stabilization after previous navigation actions. While explicit waits
     * are generally preferred, this sleep ensures the Notes module link is fully
     * interactive.
     * 
     * @throws InterruptedException if the thread sleep is interrupted during execution
     * @see NotesP#notesModule
     */
    @When("User clicks the Notes module")
    public void user_clicks_the_notes_module() throws InterruptedException {
        Thread.sleep(2000);
        notesP.notesModule.click();
    }

    /**
     * Initiates note creation by clicking the Create button in the Notes module.
     * 
     * <p>This step implements the Gherkin step: <b>"User clicks create button in Notes module"</b>
     * 
     * <p>The method waits for the Create button (identified by CSS class {@code o-kanban-button-new})
     * to become visible before clicking. This opens the note creation form/dialog where users
     * can enter note details including tags and description.
     * 
     * @see NotesP#creatingNotes
     * @see ExpectedConditions#visibilityOf
     */
    @When("User clicks create button in Notes module")
    public void user_clicks_create_button_in_notes_module() {
        wait.until(ExpectedConditions.visibilityOf(notesP.creatingNotes));
        notesP.creatingNotes.click();
    }

    /**
     * Enters a tag name for the note using the autocomplete tag input field.
     * 
     * <p>This step implements the Gherkin step: <b>"User enters a tag name"</b>
     * 
     * <p>The method performs the following actions:
     * <ol>
     *   <li>Enters the hard-coded tag name "New Tag" into the tags autocomplete field</li>
     *   <li>Sends {@link Keys#ENTER} to confirm the tag selection</li>
     *   <li>Clicks the "Create and Edit..." option (tabindex element) to open the full tag editor</li>
     * </ol>
     * 
     * <p>The input field uses jQuery UI autocomplete-style interaction, requiring the
     * ENTER key to confirm selections from the dropdown suggestions.
     * 
     * @see NotesP#tagsN
     * @see NotesP#tabindex
     * @see Keys#ENTER
     */
    @When("User enters a tag name")
    public void user_enters_a_tag_name() {
        notesP.tagsN.sendKeys("New Tag", Keys.ENTER);
        notesP.tabindex.click();
    }

    /**
     * Enters a description for the note and saves it.
     * 
     * <p>This step implements the Gherkin step: <b>"User enters description"</b>
     * 
     * <p>The method enters the hard-coded description text
     * "This note is an example for the Testinium App" into the rich-text note body
     * (identified by CSS class {@code note-editable panel-body}), then immediately
     * clicks the save button to persist the note.
     * 
     * @see NotesP#description
     * @see NotesP#saveBtn
     */
    @When("User enters description")
    public void user_enters_description() {
        notesP.description.sendKeys("This note is an example for the Testinium App");
        notesP.saveBtn.click();
    }

    /**
     * Clicks the save button to save the current note form.
     * 
     * <p>This step implements the Gherkin step: <b>"User clicks save button"</b>
     * 
     * <p>The method waits for the Save button (identified by CSS class
     * {@code o_form_button_save}) to become visible before clicking.
     * This ensures the form is ready for submission.
     * 
     * @see NotesP#saveBtn
     * @see ExpectedConditions#visibilityOf
     */
    @When("User clicks save button")
    public void user_clicks_save_button() {
        wait.until(ExpectedConditions.visibilityOf(notesP.saveBtn));
        notesP.saveBtn.click();
    }

    /**
     * Verifies that a note was successfully created by checking the success message.
     * 
     * <p>This step implements the Gherkin step: <b>"User sees the created new notes"</b>
     * 
     * <p>The method retrieves the text from the {@code createdMessage} element and
     * asserts that it equals "Note created" to confirm successful note creation.
     * 
     * <p><b>Note:</b> The local variable name contains a typo - "expecgedMessage"
     * should be "expectedMessage". This is a cosmetic issue that doesn't affect
     * test execution.
     * 
     * @see NotesP#createdMessage
     * @see Assert#assertEquals
     */
    @Then("User sees the created new notes")
    public void user_sees_the_created_new_notes() {
        String actualMessage = notesP.createdMessage.getText();
        String expecgedMessage = "Note created";
        Assert.assertEquals(actualMessage, expecgedMessage);
    }

    /**
     * Clicks on a note to select or edit it.
     * 
     * <p>This step implements the Gherkin step: <b>"User clicks the edit button"</b>
     * 
     * <p>The method clicks on a specific note identified by its title
     * "BDD Approach Framework with Cucumber". This locator is hard-coded and
     * assumes a note with this exact title exists in the system.
     * 
     * <p><b>Note:</b> The method name suggests clicking an "edit button", but the
     * implementation actually clicks on the note title element ({@code appK}).
     * This naming discrepancy may cause confusion during maintenance.
     * 
     * @see NotesP#appK
     */
    @When("User clicks the edit button")
    public void user_clicks_the_edit_button() {
        notesP.appK.click();
    }

    /**
     * Clears and enters a new description for an existing note, then saves and navigates back.
     * 
     * <p>This step implements the Gherkin step: <b>"User enters new description"</b>
     * 
     * <p>The method performs the following sequence:
     * <ol>
     *   <li>Clears the existing description text</li>
     *   <li>Enters the new hard-coded text "FKASDFGASDFADSFADS"</li>
     *   <li>Clicks the save button from {@link InventoryP} (cross-page object dependency)</li>
     *   <li>Navigates back to the Notes module list view</li>
     * </ol>
     * 
     * <p><b>Note:</b> This method reuses {@code inventoryP.saveBtn} instead of
     * {@code notesP.saveBtn}. While both may locate the same element, this creates
     * a maintenance concern as changes to the Inventory page could affect Notes tests.
     * 
     * @see NotesP#description
     * @see InventoryP#saveBtn
     * @see NotesP#notesModule
     */
    @When("User enters new description")
    public void user_enters_new_description() {
        notesP.description.clear();
        notesP.description.sendKeys("FKASDFGASDFADSFADS");
        inventoryP.saveBtn.click();
        notesP.notesModule.click();
    }

    /**
     * Verifies that the Notes list is displayed in the Notes module.
     * 
     * <p>This step implements the Gherkin step: <b>"User should see the Notes list"</b>
     * 
     * <p>The method performs the following actions:
     * <ol>
     *   <li>Waits for the Notes module element to become visible</li>
     *   <li>Clicks on the Notes module element</li>
     *   <li>Asserts that the Notes module element is displayed</li>
     * </ol>
     * 
     * <p><b>Note:</b> The assertion appears redundant after the explicit wait and click,
     * as the wait already ensures visibility. The click action may also be unnecessary
     * for a verification step.
     * 
     * @see NotesP#notesModule
     * @see ExpectedConditions#visibilityOf
     * @see Assert#assertTrue
     */
    @Then("User should see the Notes list")
    public void user_should_see_the_notes_list() {
        wait.until(ExpectedConditions.visibilityOf(notesP.notesModule));
        notesP.notesModule.click();
        Assert.assertTrue(notesP.notesModule.isDisplayed());
    }

    /**
     * Performs a drag-and-drop operation to move a note from the "New" section to the "Today" section.
     * 
     * <p>This step implements the Gherkin step: <b>"User move element from New section to Today section"</b>
     * 
     * <p>The method uses Selenium {@link Actions} API to perform a complex drag-and-drop sequence:
     * <ol>
     *   <li>{@code clickAndHold} on the source element ({@code newTable}, data-id='1193')</li>
     *   <li>{@code pause} for 2 seconds to allow UI to register the drag state</li>
     *   <li>{@code moveToElement} to the target element ({@code todayTable}, data-id='1194')</li>
     *   <li>{@code pause} for 2 seconds to allow UI to recognize the drop target</li>
     *   <li>{@code release} to complete the drop action</li>
     *   <li>{@code perform} to execute the entire action chain</li>
     * </ol>
     * 
     * <p>The 2-second pauses during the drag operation allow the Odoo kanban board UI
     * to properly render hover states and drop zone indicators.
     * 
     * <p><b>Note:</b> The locators rely on fixed {@code data-id} attribute values (1193 and 1194)
     * which may vary between Odoo environments or after database resets, potentially
     * causing test failures in different environments.
     * 
     * @see org.openqa.selenium.interactions.Actions
     * @see NotesP#newTable
     * @see NotesP#todayTable
     * @see Driver#getDriver()
     */
    @When("User move element from New section to Today section")
    public void user_move_element_from_new_section_to_today_section() {
        Actions actions = new Actions(Driver.getDriver());
        actions.clickAndHold(notesP.newTable).pause(2000).moveToElement(notesP.todayTable).pause(2000).release().perform();
    }

    /**
     * Verifies that a note was successfully moved to the "Today" section.
     * 
     * <p>This step implements the Gherkin step: <b>"User sees Today new added element"</b>
     * 
     * <p>The method retrieves the text from the {@code todayTable} element and asserts
     * that it equals "Today" to verify the kanban column is properly identified.
     * 
     * <p><b>Note:</b> This assertion verifies the column header text ("Today") rather
     * than confirming the moved note actually appears in the Today column. A more
     * robust verification would check that the specific note title exists within
     * the Today column's child elements.
     * 
     * @see NotesP#todayTable
     * @see Assert#assertEquals
     */
    @Then("User sees Today new added element")
    public void user_sees_today_new_added_element() {
        String actualTable = notesP.todayTable.getText();
        String expectedTable = "Today";

        Assert.assertEquals(actualTable, expectedTable);
    }
}
