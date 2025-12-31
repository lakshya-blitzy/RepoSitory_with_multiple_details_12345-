package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object class representing the Notes module in the Odoo web application.
 * 
 * <p>This class provides WebElement locators for note management operations including:
 * <ul>
 *   <li>Module navigation to access the Notes section</li>
 *   <li>Note creation via kanban view</li>
 *   <li>Tags input using jQuery UI autocomplete</li>
 *   <li>Rich-text body editing for note content</li>
 *   <li>Note organization through kanban cards grouped by stage/date</li>
 * </ul>
 * 
 * <p>This class follows the Page Object Model (POM) design pattern, encapsulating
 * all UI element locators for the Notes module in a single, maintainable class.
 * 
 * <p><strong>Note:</strong> This class contains locators with fixed {@code data-id} values
 * (e.g., 1193, 1194) for specific note group containers. These values reference database
 * stage IDs and may vary across different test environments or Odoo instances.
 * 
 * <p>All WebElement fields are initialized via 
 * {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)} using the
 * WebDriver instance obtained from {@link Driver#getDriver()}.
 * 
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.PageFactory
 */
public class NotesP {

    /**
     * Constructs a new NotesP Page Object instance.
     * 
     * <p>Initializes all {@link FindBy} annotated WebElement fields by binding
     * the locators to the active WebDriver instance obtained from 
     * {@link Driver#getDriver()}.
     * 
     * <p>The {@link PageFactory#initElements(org.openqa.selenium.WebDriver, Object)}
     * method processes all annotated fields and creates lazy-loading proxies
     * that resolve to actual WebElements when accessed.
     */
    public NotesP(){
        PageFactory.initElements(Driver.getDriver(), this);
    }

    /**
     * WebElement for the "Create and Edit..." dropdown option.
     * 
     * <p>Located via XPath using exact text match on the anchor element.
     * Used to open the full note editor dialog instead of the quick create
     * inline form in the kanban view.
     * 
     * <p><strong>Note:</strong> The variable name "tabindex" is misleading as it
     * suggests a tabindex attribute reference, but this locator actually finds
     * a link element by its text content "Create and Edit...".
     * 
     * <p>Locator: {@code //a[. = 'Create and Edit...']}
     */
    @FindBy(xpath = "//a[. = 'Create and Edit...']")
    public WebElement tabindex;

    /**
     * WebElement for the Notes module navigation link.
     * 
     * <p>Located via partial link text matching "Notes". Used to navigate
     * to the Notes module from the main application menu or module selector.
     * 
     * <p>Locator: {@code partialLinkText = "Notes"}
     */
    @FindBy(partialLinkText = "Notes")
    public WebElement notesModule;

    /**
     * WebElement for the kanban Create button to initiate new note creation.
     * 
     * <p>Located via XPath using the Odoo kanban button CSS classes. This button
     * appears at the top of the kanban view and initiates the note creation workflow.
     * Uses the {@code o-kanban-button-new} class with primary button styling.
     * 
     * <p>Locator: {@code //button[@class='btn btn-primary btn-sm o-kanban-button-new']}
     */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o-kanban-button-new']")
    public WebElement creatingNotes;

    /**
     * WebElement for the tags autocomplete input field.
     * 
     * <p>Located via XPath using the jQuery UI autocomplete input class.
     * Used for adding tags or categories to notes. The autocomplete functionality
     * provides tag suggestions as the user types.
     * 
     * <p>Uses the {@code ui-autocomplete-input} class from jQuery UI widget library.
     * 
     * <p>Locator: {@code //input[@class='o_input ui-autocomplete-input']}
     */
    @FindBy(xpath = "//input[@class='o_input ui-autocomplete-input']")
    public WebElement tagsN;

    /**
     * WebElement for the rich-text note body/content container.
     * 
     * <p>Located via XPath using the note-editable and panel-body CSS classes.
     * This is the main content area for composing note text. The element supports
     * rich text formatting including bold, italic, lists, and other formatting options.
     * 
     * <p>Uses the {@code note-editable} class for Odoo's rich text editor and
     * {@code panel-body} for Bootstrap panel styling.
     * 
     * <p>Locator: {@code //div[@class='note-editable panel-body']}
     */
    @FindBy(xpath = "//div[@class='note-editable panel-body']")
    public WebElement description;

    /**
     * WebElement for the success message displayed after note creation.
     * 
     * <p>Located via XPath using exact text match on a paragraph element
     * containing "Note created". Used to verify that a note was successfully
     * created and saved in the system.
     * 
     * <p>Locator: {@code //p[.='Note created']}
     */
    @FindBy(xpath = "//p[.='Note created']")
    public WebElement createdMessage;

    /**
     * WebElement for the Save button in the note form.
     * 
     * <p>Located via XPath using the Odoo form save button CSS classes.
     * Used to save new notes or persist changes to existing notes.
     * Uses the {@code o_form_button_save} class with primary button styling.
     * 
     * <p>Locator: {@code //button[@class='btn btn-primary btn-sm o_form_button_save']}
     */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']")
    public WebElement saveBtn;

    /**
     * WebElement for a specific note identified by its title text.
     * 
     * <p>Located via XPath using exact text match on a span element containing
     * "BDD Approach Framework with Cucumber". Used to locate and verify the
     * presence of a specific test note in the kanban view.
     * 
     * <p><strong>Stability Concern:</strong> This locator contains a hard-coded
     * test data value. The element will only be found if a note with this exact
     * title exists in the system. Consider parameterizing this locator or creating
     * the test data as part of the test setup.
     * 
     * <p>Locator: {@code //span[.='BDD Approach Framework with Cucumber']}
     */
    @FindBy(xpath = "//span[.='BDD Approach Framework with Cucumber']")
    public WebElement appK;

    /**
     * WebElement for a specific kanban column container (stage ID 1193).
     * 
     * <p>Located via indexed XPath targeting the second div child within a
     * kanban column container identified by {@code data-id='1193'}. This locator
     * targets a specific note grouping/stage in the kanban board, likely representing
     * a "New" or initial stage for notes.
     * 
     * <p><strong>Stability Concern:</strong> The fixed {@code data-id} value (1193)
     * references a specific stage/group ID stored in the database. This locator will
     * break if:
     * <ul>
     *   <li>Stage IDs are regenerated or differ between environments</li>
     *   <li>The database is recreated or migrated</li>
     *   <li>Testing against a different Odoo instance</li>
     * </ul>
     * Consider using a more stable locator strategy based on stage name or position.
     * 
     * <p>Locator: {@code (//div[@data-id='1193']/div)[2]}
     */
    @FindBy(xpath = "(//div[@data-id='1193']/div)[2]")
    public WebElement newTable;
    
    /**
     * WebElement for a specific kanban column container (stage ID 1194).
     * 
     * <p>Located via indexed XPath targeting the first div child within a
     * kanban column container identified by {@code data-id='1194'}. This locator
     * targets a specific note grouping/stage in the kanban board, likely representing
     * a "Today" or date-based note grouping.
     * 
     * <p><strong>Stability Concern:</strong> The fixed {@code data-id} value (1194)
     * references a specific stage/group ID stored in the database. This locator is
     * environment-dependent and will break if:
     * <ul>
     *   <li>Stage IDs are regenerated or differ between environments</li>
     *   <li>The database is recreated or migrated</li>
     *   <li>Testing against a different Odoo instance</li>
     * </ul>
     * Consider using a more stable locator strategy based on stage name or position.
     * 
     * <p>Locator: {@code (//div[@data-id='1194']/div)[1]}
     */
    @FindBy(xpath = "(//div[@data-id='1194']/div)[1]")
    public WebElement todayTable;

}
