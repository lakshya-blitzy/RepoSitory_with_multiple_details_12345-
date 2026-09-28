package com.testinium.pages;

import com.testinium.utilities.Driver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

/**
 * Page Object (POM element container) for the CRM pipeline and customer screens of the Odoo/Upgenix ERP under test.
 *
 * <p>Each {@code public} {@code WebElement} field is annotated with {@code @FindBy} and bound by Selenium
 * {@code PageFactory} to a lazy proxy, so the element is located in the current DOM only when the field is used.
 * The step definitions in {@code com.testinium.step_definitions.Crm} construct this class and drive its
 * elements; the class itself contains no waits or assertions. Several locators depend on fixed kanban
 * {@code data-id} values, generated field ids or an absolute XPath and break when the data or DOM changes.
 */
public class CrmP {
    /**
     * Creates the page and initializes its {@code @FindBy} proxies by calling
     * {@code PageFactory.initElements(Driver.getDriver(), this)}.
     *
     * <p>{@link com.testinium.utilities.Driver#getDriver()} creates, or reuses, the current thread's
     * {@code WebDriver}, choosing the browser from the {@code browser} configuration key. Step classes
     * construct pages in field initializers, so constructing a page starts the browser if this thread has none yet.
     */
    public CrmP(){
        PageFactory.initElements(Driver.getDriver(),this);
    }

    /** CRM link in the main menu, located by partial link text. */
    @FindBy(partialLinkText = "CRM")
    public WebElement crmLink;

    /** Create button (access key {@code c}) that opens the opportunity quick-create dialog. */
    @FindBy(xpath = "//button[@accesskey='c']")
    public WebElement createButton;

    /** Opportunity title input ({@code name="name"}) in the quick-create dialog. */
    @FindBy(name = "name")
    public  WebElement opportunityTitle;

    /** Customer input of the quick-create dialog, located by a structural XPath. */
    @FindBy(xpath = "//table[@class='o_group o_inner_group o_group_col_6']//div//div//input")
    public WebElement customer;

    /** Autocomplete entry for the customer named {@code &CC}. */
    @FindBy(xpath = "//a[.='&CC']")
    public WebElement customerId;

    /** Expected revenue input of the quick-create dialog. */
    @FindBy(xpath = "//div[@class='o_row']//input")
    public WebElement expectedRevenue;

    /** Priority star in the quick-create dialog, located by row and index. */
    @FindBy(xpath = "//table[@class='o_group o_inner_group o_group_col_6']//tr[4]//a[3]")
    public WebElement priority;

    /** Confirm button of the quick-create dialog ({@code name="close_dialog"}); same locator as {@link #createCustomerButton}. */
    @FindBy(xpath = "//button[@name='close_dialog']")
    public WebElement createPipeline;

    /** Title of the first card in pipeline stage {@code data-id='1'}, read to verify creation and edits. */
    @FindBy(xpath = "//div[@data-id='1']/div[2]//strong//span")
    public  WebElement findTitleTest;

    /** Total expected revenue shown for pipeline stage {@code data-id='1'}. */
    @FindBy(xpath = "//div[@data-id='1']//b")
    public WebElement totalPrice;

    /** First card in pipeline stage {@code data-id='1'}, clicked to open the opportunity; same locator as {@link #progressPipeline}. */
    @FindBy(xpath = "//div[@data-id='1']/div[2]")
    public WebElement buttonPipeline;

    /** Edit button of the opportunity form (access key {@code a}). */
    @FindBy(xpath = "//button[@accesskey='a']")
    public WebElement editButton;

    /** Opportunity title input in edit mode. */
    @FindBy(xpath = "//input[@name='name']")
    public WebElement opportunityTitleEdit;

    /** Expected revenue input in edit mode, located by the generated id {@code o_field_input_125}; fragile. */
    @FindBy(xpath = "//input[@id='o_field_input_125']")
    public WebElement expectedRevenueEdit;

    /** Probability input in edit mode, located by the generated id {@code o_field_input_127}; fragile. */
    @FindBy(xpath = "//input[@id='o_field_input_127']")
    public WebElement probabilityEdit;

    /** Save button of the form (access key {@code s}). */
    @FindBy(xpath = "//button[@accesskey='s']")
    public WebElement  saveEdit;

    /** Pipeline link in the CRM menu, located by a hard-coded menu/action href. */
    @FindBy(xpath = "//a[@href='/web#menu_id=274&action=365']/span")
    public WebElement pipelineSideButton;

    /** First card in stage {@code data-id='1'}; drag source of the stage-change step. */
    @FindBy(xpath = "//div[@data-id='1']/div[2]")
    public WebElement progressPipeline;

    /** First card in stage {@code data-id='2'}; drop target of the stage-change step. */
    @FindBy(xpath = "//div[@data-id='2']/div[2]")
    public WebElement progressPipeline2;

    /** Card title in stage {@code data-id='2'}, read to verify the drag-and-drop move. */
    @FindBy(xpath = "//div[@data-id='2']//div[2]//strong//span")
    public WebElement testVerify;

    /** Customers link in the CRM menu, located by a hard-coded menu/action href. */
    @FindBy(xpath = "//a[@href='/web#menu_id=272&action=48']")
    public WebElement customerSideButton;

    /** Create button (access key {@code c}) on the customers view; same locator as {@link #createButton}. */
    @FindBy(xpath = "//button[@accesskey='c']")
    public WebElement createCustomer;

    /** Customer name input ({@code name="name"}). */
    @FindBy(xpath = "//input[@name='name']")
    public WebElement inputName;

    /** Confirm button of the customer dialog ({@code name="close_dialog"}); same locator as {@link #createPipeline}. */
    @FindBy(xpath = "//button[@name='close_dialog']")
    public WebElement createCustomerButton;

    /** Search view input ({@code o_searchview_input}). */
    @FindBy(xpath = "//input[@class='o_searchview_input']")
    public WebElement searchingText;

    /** Customer entry whose text is {@code &CC}, clicked to open that customer. */
    @FindBy(xpath =  "//span[.='&CC']")
    public WebElement nameCustomer;

    /** Print-section entry ({@code data-section='print'}) used for the due-payment action. */
    @FindBy(xpath = "//a[@data-section='print']")
    public WebElement duePaymentButton;

    /** Print button located by an absolute XPath; fragile. */
    @FindBy(xpath = "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button")
    public WebElement printButton;






}