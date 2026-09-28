package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object (POM element container) for the Notes module of the Odoo/Upgenix ERP under test.
 *
 * <p>Each {@code public} {@code WebElement} field is annotated with {@code @FindBy} and bound by Selenium
 * {@code PageFactory} to a lazy proxy, so the element is located in the current DOM only when the field is used.
 * The step definitions in {@code com.testinium.step_definitions.Notes} construct this class and drive its
 * elements; the class itself contains no waits or assertions.
 */
public class NotesP {

    /**
     * Creates the page and initializes its {@code @FindBy} proxies by calling
     * {@code PageFactory.initElements(Driver.getDriver(), this)}. Step classes construct pages in field initializers.
     *
     * <p>{@link Driver#getDriver()} reuses this thread's {@code WebDriver}; with none, it starts one only if the {@code browser}
     * key is {@code chrome} or {@code firefox}, and a failed start throws. Any other value binds the proxies to a {@code null} driver,
     * so using an element throws {@code NullPointerException}; a missing key or configuration file makes this constructor throw it.
     */
    public NotesP(){
        PageFactory.initElements(Driver.getDriver(), this);
    }

    /** {@code Create and Edit...} entry of the tags autocomplete drop-down; despite its name, it does not locate a tabindex attribute. */
    @FindBy(xpath = "//a[. = 'Create and Edit...']")
    public WebElement tabindex;

    /** Notes module link in the main menu, located by the partial link text {@code Notes}. */
    @FindBy(partialLinkText = "Notes")
    public WebElement notesModule;

    /** Create button of the Notes kanban view ({@code o-kanban-button-new}). */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o-kanban-button-new']")
    public WebElement creatingNotes;

    /** Tags autocomplete input of the note form. */
    @FindBy(xpath = "//input[@class='o_input ui-autocomplete-input']")
    public WebElement tagsN;

    /** Rich-text body editor of the note form ({@code note-editable}). */
    @FindBy(xpath = "//div[@class='note-editable panel-body']")
    public WebElement description;

    /** "Note created" confirmation message, whose text is read to verify that the note was created. */
    @FindBy(xpath = "//p[.='Note created']")
    public WebElement createdMessage;

    /** Form Save button ({@code o_form_button_save}) of whichever form is open; the locator is not note-specific. Clicked by the Notes description and save steps, including the shared {@code User clicks save button} step that {@code Contact.feature} also uses to save a contact. */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']")
    public WebElement saveBtn;

    /** Note entry titled "BDD Approach Framework with Cucumber", clicked to open it for editing. Depends on existing test data. */
    @FindBy(xpath = "//span[.='BDD Approach Framework with Cucumber']")
    public WebElement appK;

    /** Card in the "New" stage column ({@code data-id='1193'}), the drag source of the move. Fragile: the stage id is fixed. */
    @FindBy(xpath = "(//div[@data-id='1193']/div)[2]")
    public WebElement newTable;
    
    /** First child of the "Today" stage column ({@code data-id='1194'}): the drop target, whose text must read {@code Today}. Fragile: the stage id is fixed. */
    @FindBy(xpath = "(//div[@data-id='1194']/div)[1]")
    public WebElement todayTable;

}