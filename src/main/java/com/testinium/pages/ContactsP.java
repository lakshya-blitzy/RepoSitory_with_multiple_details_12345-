package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object (POM element container) for the Contacts module of the Odoo/Upgenix ERP under test.
 *
 * <p>Each {@code public} {@code WebElement} field is annotated with {@code @FindBy} and bound by Selenium
 * {@code PageFactory} to a lazy proxy, so the element is located in the current DOM only when the field is used.
 * The step definitions in {@code com.testinium.step_definitions.Contacts} construct this class and drive its
 * elements; the class itself contains no waits or assertions.
 */
public class ContactsP {

    /**
     * Creates the page and initializes its {@code @FindBy} proxies by calling
     * {@code PageFactory.initElements(Driver.getDriver(), this)}. Step classes construct pages in field initializers.
     *
     * <p>{@link Driver#getDriver()} reuses this thread's {@code WebDriver}; with none, it starts one only if the {@code browser}
     * key is {@code chrome} or {@code firefox}, and a failed start throws. Any other value binds the proxies to a {@code null} driver,
     * so using an element throws {@code NullPointerException}; a missing key or configuration file makes this constructor throw it.
     */
    public ContactsP(){
        PageFactory.initElements(Driver.getDriver(), this);
    }

    /** Contacts link in the main menu, located by partial link text. */
    @FindBy(partialLinkText = "Contacts")
    public WebElement contactModule;

    /** Create button of the control panel (access key {@code c}). */
    @FindBy(xpath = "//button[@accesskey='c']")
    public WebElement createContact;

    /** List-view switch button (access key {@code l}). */
    @FindBy(xpath = "//button[@accesskey='l']")
    public WebElement callList;

    /** Contact name input ({@code name="name"}) on the create form. */
    @FindBy(name = "name")
    public WebElement nameInput;

    /** Street address input ({@code name="street"}); {@code Contacts.user_enters(String)} types into it on the create and edit forms without clearing it first. */
    @FindBy(name = "street")
    public WebElement streetInput;

    /** Phone number input ({@code name="phone"}); {@code Contacts.user_enters_and(String, String)} types its first value into it on the create and edit forms without clearing it first. */
    @FindBy(name = "phone")
    public WebElement phoneNoInput;

    /** Email input ({@code name="email"}); {@code Contacts.user_enters_and(String, String)} types its second value into it on the create and edit forms without clearing it first. */
    @FindBy(name = "email")
    public WebElement emailInput;

    /** First {@code <span>} on the page whose text is exactly {@code Ok}, clicked by the created-contact step as a dialog's Ok control; the locator is scoped to neither a button nor a dialog. */
    @FindBy(xpath="//span[.='Ok']")
    public WebElement okBtn;

    /** Twelfth input directly inside an {@code o_checkbox} div, counted across the whole page and clicked to choose a profile; it is not scoped to a list row, so earlier matching checkboxes change which element it finds. */
    @FindBy(xpath = "(//div[@class='o_checkbox']/input)[12]")
    public WebElement newContact;

    /** Action dropdown toggle in the sidebar (second sidebar group, index-based). */
    @FindBy(xpath = "(//div[@class='o_cp_sidebar']/div/div)[2]")
    public WebElement actionInput;

    /** First link with {@code data-index='3'} on the page, clicked as the Action dropdown's Delete entry; the deleted-profile step compares its label with {@code "Deleted"}, which does not verify that the contact was removed. */
    @FindBy(xpath = "//a[@data-index='3']")
    public WebElement deleteInput;

    /** First contact card in the kanban view. */
    @FindBy(xpath = "(//div[@class='o_kanban_view o_res_partner_kanban o_kanban_ungrouped']/div)[1]")
    public WebElement firstUser;

    /** Title area ({@code oe_title}) of the opened contact form, waited on after opening a contact. */
    @FindBy(xpath = "//div[@class='oe_title']")
    public WebElement editTitle;

    /** Edit button of the contact form. */
    @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_edit']")
    public WebElement editBtn;

    /** Print dropdown group, matched only while the dropdown is open ({@code o_dropdown open}). */
    @FindBy(xpath = "//div[@class='btn-group o_dropdown open']")
    public WebElement printInput;


    /** First {@code <button>} directly inside the open Print dropdown group; the locator names no Due Payments entry, so which button it finds depends on the rendered dropdown. */
    @FindBy(xpath = "(//div[@class='btn-group o_dropdown open']/button)")
    public WebElement duePayment;


}

