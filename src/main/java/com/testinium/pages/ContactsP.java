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
     * {@code PageFactory.initElements(Driver.getDriver(), this)}.
     *
     * <p>{@link com.testinium.utilities.Driver#getDriver()} creates, or reuses, the current thread's
     * {@code WebDriver}, choosing the browser from the {@code browser} configuration key. Step classes
     * construct pages in field initializers, so constructing a page starts the browser if this thread has none yet.
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

    /** Street address input ({@code name="street"}). */
    @FindBy(name = "street")
    public WebElement streetInput;

    /** Phone number input ({@code name="phone"}). */
    @FindBy(name = "phone")
    public WebElement phoneNoInput;

    /** Email input ({@code name="email"}). */
    @FindBy(name = "email")
    public WebElement emailInput;

    /** Ok button of a confirmation dialog (span text "Ok"). */
    @FindBy(xpath="//span[.='Ok']")
    public WebElement okBtn;

    /** List row checkbox selected by a fixed index (the 12th checkbox); fragile, depends on list contents. */
    @FindBy(xpath = "(//div[@class='o_checkbox']/input)[12]")
    public WebElement newContact;

    /** Action dropdown toggle in the sidebar (second sidebar group, index-based). */
    @FindBy(xpath = "(//div[@class='o_cp_sidebar']/div/div)[2]")
    public WebElement actionInput;

    /** Delete entry of the Action dropdown ({@code data-index='3'}); its text is also read to verify the deletion. */
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


    /** Button inside the open Print dropdown, used for the due-payment print action. */
    @FindBy(xpath = "(//div[@class='btn-group o_dropdown open']/button)")
    public WebElement duePayment;


}

