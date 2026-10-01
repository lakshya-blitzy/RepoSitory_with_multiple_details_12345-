package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object (POM element container) for the Inventory / Products screens of the Odoo/Upgenix ERP under test.
 *
 * <p>Each {@code public} {@code WebElement} field is annotated with {@code @FindBy} and bound by Selenium
 * {@code PageFactory} to a lazy proxy, so the element is located in the current DOM only when the field is used.
 * The step definitions in {@code com.testinium.step_definitions.Inventory} construct this class and drive its
 * elements ({@code com.testinium.step_definitions.Notes} also reuses {@link #saveBtn}); the class itself contains
 * no waits or assertions.
 */
public class InventoryP {

    /**
     * Creates the page and initializes its {@code @FindBy} proxies by calling
     * {@code PageFactory.initElements(Driver.getDriver(), this)}. Step classes construct pages in field initializers.
     *
     * <p>{@link Driver#getDriver()} reuses this thread's {@code WebDriver}; with none, it starts one only if the {@code browser}
     * key is {@code chrome} or {@code firefox}, and a failed start throws. Any other value binds the proxies to a {@code null} driver,
     * so using an element throws {@code NullPointerException}; a missing key or configuration file makes this constructor throw it.
     */
    public InventoryP(){
        PageFactory.initElements(Driver.getDriver(), this);
    }

    /** Inventory link in the main menu, located by partial link text. */
    @FindBy(partialLinkText = "Inventory")
    public WebElement inventoryModule;

    /** Products menu link. */
    @FindBy(partialLinkText = "Products")
    public WebElement products;

    /** Kanban Create button ({@code o-kanban-button-new}). */
    @FindBy(className = "o-kanban-button-new")
    public WebElement createBtn;

    /** Form Save button ({@code o_form_button_save}); also reused by the Notes step definitions to save note edits. */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']")
    public WebElement saveBtn;

    /** Notification manager container ({@code o_notification_manager}) that shows validation errors such as a missing required field. */
    @FindBy(className = "o_notification_manager")
    public WebElement fieldError;

    /** Product name input, located by the generated id {@code o_field_input_479}; fragile. */
    @FindBy(id = "o_field_input_479")
    public WebElement productName;

    /** Product entry whose text is "EY". Note: the Inventory step types a different hard-coded product name, so this hard-coded text does not match the product it creates. */
    @FindBy(xpath = "//span[.='EY']")
    public WebElement productsList;

    /** First {@code span} whose class marks a required character field; not specifically the product name, and the Inventory step ignores its {@code isDisplayed()} result. */
    @FindBy(xpath = "//span[@class='o_field_char o_field_widget o_required_modifier']")
    public WebElement createdProduct;


}