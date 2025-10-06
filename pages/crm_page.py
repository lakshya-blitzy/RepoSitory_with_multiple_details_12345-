"""
CRM Page Module

Page object for CRM pipeline and opportunity management functionality.
This module provides element locators and interaction methods for the CRM module
of the Testinium application.

Key Features:
- CRM module navigation and opportunity creation
- Pipeline stage management with drag-and-drop support
- Customer management operations (create, search, view)
- Opportunity editing with dynamic fields
- Print and payment operations

Technical Debt Documentation:
    CRITICAL - Brittle Locators Identified:
    
    1. Absolute XPath (_PRINT_BUTTON):
       Line 94 in Java source: /html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button
       Risk Level: HIGHEST - Will break with any DOM structure change
       Recommendation: Work with dev team to add data-testid or stable ID
    
    2. Generated IDs (Dynamic IDs):
       - _EXPECTED_REVENUE_EDIT: id='o_field_input_125' (line 52 in Java)
       - _PROBABILITY_EDIT: id='o_field_input_127' (line 55 in Java)
       Risk Level: HIGH - IDs appear auto-generated and may change
       Recommendation: Request stable IDs or use name/data attributes
    
    3. Data-ID Selectors (Framework-Specific):
       - _FIND_TITLE_TEST: data-id='1'
       - _TOTAL_PRICE: data-id='1'
       - _BUTTON_PIPELINE: data-id='1'
       - _PROGRESS_PIPELINE: data-id='1'
       - _PROGRESS_PIPELINE2: data-id='2'
       - _TEST_VERIFY: data-id='2'
       Status: These appear intentional (framework data attributes)
       Risk Level: MEDIUM - May be stable if framework-generated
    
    4. Index-Based XPath Patterns:
       - _PRIORITY: //tr[4]//a[3] (line 31 in Java)
       Risk Level: MEDIUM - Brittle to DOM structure changes

Migration Context:
    Converted from CrmP.java PageFactory pattern to Python property-based locators.
    All 28 @FindBy annotations converted to private locator tuples with corresponding
    @property methods that use BasePage wait utilities. This prevents stale element
    references and provides better encapsulation than Java's public WebElement fields.

Design Pattern:
    - Locators: Private class constants as tuples (By.STRATEGY, 'value')
    - Element Access: @property methods returning fresh WebElement references
    - Waits: Explicit waits via BasePage methods (no implicit waits)
    - Actions: Inherited ActionChains support for drag-and-drop pipeline operations

Example Usage:
    >>> from selenium import webdriver
    >>> from pages.crm_page import CrmPage
    >>>
    >>> driver = webdriver.Chrome()
    >>> crm_page = CrmPage(driver)
    >>> crm_page.crm_link.click()
    >>> crm_page.create_button.click()
    >>> crm_page.opportunity_title.send_keys("New Deal")
    >>> crm_page.drag_and_drop(
    ...     crm_page._PROGRESS_PIPELINE,
    ...     crm_page._PROGRESS_PIPELINE2
    ... )
"""

from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class CrmPage(BasePage):
    """
    Page object for CRM pipeline and opportunity management.
    
    This class provides access to all CRM module elements including opportunity
    creation forms, pipeline visualization, customer management, and payment operations.
    Inherits from BasePage to leverage explicit wait utilities and ActionChains for
    drag-and-drop interactions.
    
    Attributes:
        All locator constants (private _ELEMENT_NAME tuples)
        All element properties (public element_name methods)
        Inherited from BasePage: driver, wait, config, actions
    
    Element Categories:
        - Navigation: crm_link
        - Opportunity Creation: create_button, opportunity_title, customer, customer_id,
          expected_revenue, priority, create_pipeline
        - Pipeline Management: find_title_test, total_price, button_pipeline,
          progress_pipeline, progress_pipeline2, test_verify, pipeline_side_button
        - Opportunity Editing: edit_button, opportunity_title_edit, expected_revenue_edit,
          probability_edit, save_edit
        - Customer Management: customer_side_button, create_customer, input_name,
          create_customer_button, searching_text, name_customer
        - Payment Operations: print_button, due_payment_button
    
    Thread Safety:
        CrmPage instances are thread-safe when each thread has its own WebDriver
        instance (via DriverManager threading.local()). Each property access returns
        a fresh WebElement reference via explicit waits, preventing cross-thread
        element reference issues.
    
    Example:
        >>> # Navigate to CRM and create opportunity
        >>> crm_page = CrmPage(driver)
        >>> crm_page.crm_link.click()
        >>> crm_page.create_button.click()
        >>> crm_page.opportunity_title.send_keys("Q4 Enterprise Deal")
        >>> crm_page.customer.send_keys("Acme Corp")
        >>> crm_page.expected_revenue.send_keys("50000")
        >>> crm_page.create_pipeline.click()
        >>>
        >>> # Drag opportunity to different pipeline stage
        >>> crm_page.drag_and_drop(
        ...     crm_page._PROGRESS_PIPELINE,
        ...     crm_page._PROGRESS_PIPELINE2
        ... )
    """
    
    # ============================================================================
    # LOCATOR CONSTANTS
    # ============================================================================
    # All locators defined as private class constants in tuple format:
    # (By.STRATEGY, 'locator_value')
    # These tuples are passed to Selenium WebDriverWait expected_conditions
    
    # Navigation Elements
    _CRM_LINK: Tuple[str, str] = (By.PARTIAL_LINK_TEXT, "CRM")
    
    # Opportunity Creation Elements
    _CREATE_BUTTON: Tuple[str, str] = (By.XPATH, "//button[@accesskey='c']")
    _OPPORTUNITY_TITLE: Tuple[str, str] = (By.NAME, "name")
    _CUSTOMER: Tuple[str, str] = (
        By.XPATH,
        "//table[@class='o_group o_inner_group o_group_col_6']//div//div//input"
    )
    _CUSTOMER_ID: Tuple[str, str] = (By.XPATH, "//a[.='&CC']")
    _EXPECTED_REVENUE: Tuple[str, str] = (By.XPATH, "//div[@class='o_row']//input")
    # TECHNICAL DEBT: Index-based XPath //tr[4]//a[3] - brittle to DOM changes
    _PRIORITY: Tuple[str, str] = (
        By.XPATH,
        "//table[@class='o_group o_inner_group o_group_col_6']//tr[4]//a[3]"
    )
    _CREATE_PIPELINE: Tuple[str, str] = (By.XPATH, "//button[@name='close_dialog']")
    
    # Pipeline Management Elements (Data-ID based selectors)
    # NOTE: data-id='1' and data-id='2' appear to be framework-generated identifiers
    _FIND_TITLE_TEST: Tuple[str, str] = (
        By.XPATH,
        "//div[@data-id='1']/div[2]//strong//span"
    )
    _TOTAL_PRICE: Tuple[str, str] = (By.XPATH, "//div[@data-id='1']//b")
    _BUTTON_PIPELINE: Tuple[str, str] = (By.XPATH, "//div[@data-id='1']/div[2]")
    _PROGRESS_PIPELINE: Tuple[str, str] = (By.XPATH, "//div[@data-id='1']/div[2]")
    _PROGRESS_PIPELINE2: Tuple[str, str] = (By.XPATH, "//div[@data-id='2']/div[2]")
    _TEST_VERIFY: Tuple[str, str] = (
        By.XPATH,
        "//div[@data-id='2']//div[2]//strong//span"
    )
    _PIPELINE_SIDE_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//a[@href='/web#menu_id=274&action=365']/span"
    )
    
    # Opportunity Editing Elements
    _EDIT_BUTTON: Tuple[str, str] = (By.XPATH, "//button[@accesskey='a']")
    _OPPORTUNITY_TITLE_EDIT: Tuple[str, str] = (By.XPATH, "//input[@name='name']")
    # TECHNICAL DEBT: Generated ID 'o_field_input_125' - may change between deployments
    _EXPECTED_REVENUE_EDIT: Tuple[str, str] = (
        By.XPATH,
        "//input[@id='o_field_input_125']"
    )
    # TECHNICAL DEBT: Generated ID 'o_field_input_127' - may change between deployments
    _PROBABILITY_EDIT: Tuple[str, str] = (
        By.XPATH,
        "//input[@id='o_field_input_127']"
    )
    _SAVE_EDIT: Tuple[str, str] = (By.XPATH, "//button[@accesskey='s']")
    
    # Customer Management Elements
    _CUSTOMER_SIDE_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//a[@href='/web#menu_id=272&action=48']"
    )
    _CREATE_CUSTOMER: Tuple[str, str] = (By.XPATH, "//button[@accesskey='c']")
    _INPUT_NAME: Tuple[str, str] = (By.XPATH, "//input[@name='name']")
    _CREATE_CUSTOMER_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "//button[@name='close_dialog']"
    )
    _SEARCHING_TEXT: Tuple[str, str] = (
        By.XPATH,
        "//input[@class='o_searchview_input']"
    )
    _NAME_CUSTOMER: Tuple[str, str] = (By.XPATH, "//span[.='&CC']")
    
    # Payment and Print Operations
    _DUE_PAYMENT_BUTTON: Tuple[str, str] = (By.XPATH, "//a[@data-section='print']")
    # CRITICAL TECHNICAL DEBT: Absolute XPath - HIGHEST RISK
    # Original Java line 94: /html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button
    # This will break with ANY DOM structure change. Priority fix recommended.
    _PRINT_BUTTON: Tuple[str, str] = (
        By.XPATH,
        "/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button"
    )
    
    # ============================================================================
    # PROPERTY METHODS - Element Access
    # ============================================================================
    # All properties return fresh WebElement references using BasePage wait methods
    # This prevents stale element exceptions and provides automatic synchronization
    
    # Navigation Properties
    
    @property
    def crm_link(self) -> WebElement:
        """
        CRM module navigation link.
        
        Returns:
            WebElement: Clickable link to access CRM module
        
        Example:
            >>> crm_page.crm_link.click()
        """
        return self.wait_for_clickable(self._CRM_LINK)
    
    # Opportunity Creation Properties
    
    @property
    def create_button(self) -> WebElement:
        """
        Create button for new opportunity (accesskey='c').
        
        Returns:
            WebElement: Clickable button to initiate opportunity creation
        
        Example:
            >>> crm_page.create_button.click()
        """
        return self.wait_for_clickable(self._CREATE_BUTTON)
    
    @property
    def opportunity_title(self) -> WebElement:
        """
        Opportunity title input field (name='name').
        
        Returns:
            WebElement: Input field for opportunity name/title
        
        Example:
            >>> crm_page.opportunity_title.send_keys("Q4 Enterprise Deal")
        """
        return self.wait_for_element(self._OPPORTUNITY_TITLE)
    
    @property
    def customer(self) -> WebElement:
        """
        Customer input field for opportunity.
        
        Returns:
            WebElement: Input field for customer name/selection
        
        Example:
            >>> crm_page.customer.send_keys("Acme Corporation")
        """
        return self.wait_for_element(self._CUSTOMER)
    
    @property
    def customer_id(self) -> WebElement:
        """
        Customer ID link element (displays as '&CC').
        
        Returns:
            WebElement: Link displaying customer ID
        
        Example:
            >>> crm_page.customer_id.click()
        """
        return self.wait_for_clickable(self._CUSTOMER_ID)
    
    @property
    def expected_revenue(self) -> WebElement:
        """
        Expected revenue input field for opportunity.
        
        Returns:
            WebElement: Input field for revenue amount
        
        Example:
            >>> crm_page.expected_revenue.send_keys("50000")
        """
        return self.wait_for_element(self._EXPECTED_REVENUE)
    
    @property
    def priority(self) -> WebElement:
        """
        Priority selection link for opportunity.
        
        Note:
            Uses index-based XPath (//tr[4]//a[3]) - technical debt
        
        Returns:
            WebElement: Clickable priority selector
        
        Example:
            >>> crm_page.priority.click()
        """
        return self.wait_for_clickable(self._PRIORITY)
    
    @property
    def create_pipeline(self) -> WebElement:
        """
        Create/close dialog button for pipeline opportunity.
        
        Returns:
            WebElement: Button to complete opportunity creation
        
        Example:
            >>> crm_page.create_pipeline.click()
        """
        return self.wait_for_clickable(self._CREATE_PIPELINE)
    
    # Pipeline Management Properties
    
    @property
    def find_title_test(self) -> WebElement:
        """
        Opportunity title in pipeline stage (data-id='1').
        
        Returns:
            WebElement: Title element within pipeline card
        
        Example:
            >>> title_text = crm_page.find_title_test.text
        """
        return self.wait_for_element(self._FIND_TITLE_TEST)
    
    @property
    def total_price(self) -> WebElement:
        """
        Total price display in pipeline card (data-id='1').
        
        Returns:
            WebElement: Bold element showing revenue amount
        
        Example:
            >>> price = crm_page.total_price.text
        """
        return self.wait_for_element(self._TOTAL_PRICE)
    
    @property
    def button_pipeline(self) -> WebElement:
        """
        Pipeline stage button/card (data-id='1').
        
        Returns:
            WebElement: Clickable pipeline stage card
        
        Example:
            >>> crm_page.button_pipeline.click()
        """
        return self.wait_for_clickable(self._BUTTON_PIPELINE)
    
    @property
    def progress_pipeline(self) -> WebElement:
        """
        First pipeline progress stage (data-id='1').
        
        Used for drag-and-drop operations to move opportunities between stages.
        
        Returns:
            WebElement: Draggable pipeline stage element
        
        Example:
            >>> # Drag from progress_pipeline to progress_pipeline2
            >>> crm_page.drag_and_drop(
            ...     crm_page._PROGRESS_PIPELINE,
            ...     crm_page._PROGRESS_PIPELINE2
            ... )
        """
        return self.wait_for_visibility(self._PROGRESS_PIPELINE)
    
    @property
    def progress_pipeline2(self) -> WebElement:
        """
        Second pipeline progress stage (data-id='2').
        
        Used as drop target for drag-and-drop operations.
        
        Returns:
            WebElement: Drop target pipeline stage element
        
        Example:
            >>> # Drag opportunity to second stage
            >>> crm_page.drag_and_drop(
            ...     crm_page._PROGRESS_PIPELINE,
            ...     crm_page._PROGRESS_PIPELINE2
            ... )
        """
        return self.wait_for_visibility(self._PROGRESS_PIPELINE2)
    
    @property
    def test_verify(self) -> WebElement:
        """
        Verification element in second pipeline stage (data-id='2').
        
        Returns:
            WebElement: Element for verifying opportunity moved to stage 2
        
        Example:
            >>> verify_text = crm_page.test_verify.text
            >>> assert "Expected Title" in verify_text
        """
        return self.wait_for_element(self._TEST_VERIFY)
    
    @property
    def pipeline_side_button(self) -> WebElement:
        """
        Pipeline sidebar navigation button.
        
        Returns:
            WebElement: Sidebar link to pipeline view
        
        Example:
            >>> crm_page.pipeline_side_button.click()
        """
        return self.wait_for_clickable(self._PIPELINE_SIDE_BUTTON)
    
    # Opportunity Editing Properties
    
    @property
    def edit_button(self) -> WebElement:
        """
        Edit button for existing opportunity (accesskey='a').
        
        Returns:
            WebElement: Button to enter edit mode
        
        Example:
            >>> crm_page.edit_button.click()
        """
        return self.wait_for_clickable(self._EDIT_BUTTON)
    
    @property
    def opportunity_title_edit(self) -> WebElement:
        """
        Opportunity title input in edit mode.
        
        Returns:
            WebElement: Input field for editing opportunity title
        
        Example:
            >>> crm_page.opportunity_title_edit.clear()
            >>> crm_page.opportunity_title_edit.send_keys("Updated Deal Name")
        """
        return self.wait_for_element(self._OPPORTUNITY_TITLE_EDIT)
    
    @property
    def expected_revenue_edit(self) -> WebElement:
        """
        Expected revenue input in edit mode.
        
        Warning:
            Uses generated ID 'o_field_input_125' which may change.
            Technical debt - request stable identifier from dev team.
        
        Returns:
            WebElement: Input field for editing revenue amount
        
        Example:
            >>> crm_page.expected_revenue_edit.clear()
            >>> crm_page.expected_revenue_edit.send_keys("75000")
        """
        return self.wait_for_element(self._EXPECTED_REVENUE_EDIT)
    
    @property
    def probability_edit(self) -> WebElement:
        """
        Probability input in edit mode.
        
        Warning:
            Uses generated ID 'o_field_input_127' which may change.
            Technical debt - request stable identifier from dev team.
        
        Returns:
            WebElement: Input field for editing win probability
        
        Example:
            >>> crm_page.probability_edit.clear()
            >>> crm_page.probability_edit.send_keys("85")
        """
        return self.wait_for_element(self._PROBABILITY_EDIT)
    
    @property
    def save_edit(self) -> WebElement:
        """
        Save button in edit mode (accesskey='s').
        
        Returns:
            WebElement: Button to save opportunity changes
        
        Example:
            >>> crm_page.save_edit.click()
        """
        return self.wait_for_clickable(self._SAVE_EDIT)
    
    # Customer Management Properties
    
    @property
    def customer_side_button(self) -> WebElement:
        """
        Customer sidebar navigation button.
        
        Returns:
            WebElement: Sidebar link to customer management
        
        Example:
            >>> crm_page.customer_side_button.click()
        """
        return self.wait_for_clickable(self._CUSTOMER_SIDE_BUTTON)
    
    @property
    def create_customer(self) -> WebElement:
        """
        Create customer button (accesskey='c').
        
        Returns:
            WebElement: Button to initiate customer creation
        
        Example:
            >>> crm_page.create_customer.click()
        """
        return self.wait_for_clickable(self._CREATE_CUSTOMER)
    
    @property
    def input_name(self) -> WebElement:
        """
        Customer name input field.
        
        Returns:
            WebElement: Input field for customer name
        
        Example:
            >>> crm_page.input_name.send_keys("Acme Corporation")
        """
        return self.wait_for_element(self._INPUT_NAME)
    
    @property
    def create_customer_button(self) -> WebElement:
        """
        Create/close dialog button for customer creation.
        
        Returns:
            WebElement: Button to complete customer creation
        
        Example:
            >>> crm_page.create_customer_button.click()
        """
        return self.wait_for_clickable(self._CREATE_CUSTOMER_BUTTON)
    
    @property
    def searching_text(self) -> WebElement:
        """
        Search input field for finding customers.
        
        Returns:
            WebElement: Search input field
        
        Example:
            >>> crm_page.searching_text.send_keys("Acme")
            >>> crm_page.searching_text.send_keys(Keys.ENTER)
        """
        return self.wait_for_element(self._SEARCHING_TEXT)
    
    @property
    def name_customer(self) -> WebElement:
        """
        Customer name element in search results (displays as '&CC').
        
        Returns:
            WebElement: Customer name span in results
        
        Example:
            >>> customer_name = crm_page.name_customer.text
            >>> crm_page.name_customer.click()
        """
        return self.wait_for_element(self._NAME_CUSTOMER)
    
    # Payment and Print Operations Properties
    
    @property
    def due_payment_button(self) -> WebElement:
        """
        Due payment button (data-section='print').
        
        Returns:
            WebElement: Link to payment/print section
        
        Example:
            >>> crm_page.due_payment_button.click()
        """
        return self.wait_for_clickable(self._DUE_PAYMENT_BUTTON)
    
    @property
    def print_button(self) -> WebElement:
        """
        Print button for opportunity/invoice.
        
        Critical Warning:
            This element uses an absolute XPath which is extremely brittle:
            /html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/button
            
            This locator will break with ANY DOM structure change and is the
            HIGHEST PRIORITY technical debt item. Coordinate with development
            team to add a stable identifier (data-testid, unique ID, or class).
        
        Returns:
            WebElement: Print button (fragile locator)
        
        Example:
            >>> crm_page.print_button.click()
        """
        return self.wait_for_clickable(self._PRINT_BUTTON)
    
    # ============================================================================
    # HELPER METHODS - High-Level Actions
    # ============================================================================
    
    def drag_opportunity_to_stage(
        self,
        source_stage_data_id: str,
        target_stage_data_id: str
    ) -> None:
        """
        Drag an opportunity from one pipeline stage to another.
        
        This method encapsulates the drag-and-drop workflow for moving opportunities
        between pipeline stages. It uses the inherited drag_and_drop method from
        BasePage with ActionChains.
        
        Args:
            source_stage_data_id: The data-id attribute value of source stage
                                 Example: '1' for first stage
            target_stage_data_id: The data-id attribute value of target stage
                                 Example: '2' for second stage
        
        Raises:
            TimeoutException: If source or target stage not visible
            Exception: If drag-and-drop operation fails
        
        Example:
            >>> # Move opportunity from stage 1 to stage 2
            >>> crm_page.drag_opportunity_to_stage('1', '2')
            >>>
            >>> # Move opportunity from stage 2 to stage 3
            >>> crm_page.drag_opportunity_to_stage('2', '3')
        
        Note:
            This method dynamically constructs locators based on data-id attributes.
            If using the pre-defined properties (progress_pipeline, progress_pipeline2),
            use the inherited drag_and_drop method directly:
            >>> crm_page.drag_and_drop(
            ...     crm_page._PROGRESS_PIPELINE,
            ...     crm_page._PROGRESS_PIPELINE2
            ... )
        """
        source_locator = (
            By.XPATH,
            f"//div[@data-id='{source_stage_data_id}']/div[2]"
        )
        target_locator = (
            By.XPATH,
            f"//div[@data-id='{target_stage_data_id}']/div[2]"
        )
        
        self.drag_and_drop(source_locator, target_locator)


# Module-level documentation for usage examples
if __name__ == "__main__":
    """
    Module self-test demonstrating CrmPage functionality.
    
    Note: This requires a running Selenium WebDriver instance and is primarily
    for documentation purposes. Actual usage should be in step definitions.
    """
    print("CrmPage module loaded successfully")
    print("\nTechnical Debt Summary:")
    print("  CRITICAL: _PRINT_BUTTON uses absolute XPath (highest risk)")
    print("  HIGH: _EXPECTED_REVENUE_EDIT and _PROBABILITY_EDIT use generated IDs")
    print("  MEDIUM: _PRIORITY uses index-based XPath")
    print("  MEDIUM: Multiple data-id selectors (may be stable if framework-generated)")
    print("\nRecommendation: Work with development team to add stable identifiers")
    print("(data-testid attributes or consistent IDs) for fragile locators")

