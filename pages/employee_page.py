"""
Employee Page Module

Page object for Employee and HR management functionality in the Testinium application.
This module replaces EmployeeP.java with property-based element access and security
remediation for credential management.

Key Features:
- Login form element locators (input_login, input_password, login_button)
- Employee management navigation (Employees, Badges, Challenges, Goals History, Departments)
- Employee creation form fields (create button, employee name input, save/create messages)
- Employee editing elements (choose employee, edit employee, name edit field)
- Property-based element access with explicit waits
- Environment variable-based credential management (SECURITY REMEDIATION)

Security Remediation:
    This module addresses CRITICAL security vulnerability in EmployeeP.java lines 59-63
    and 65-69 which contained hardcoded credentials:
        - Username: "posmanager50@info.com"
        - Password: "posmanager"
    
    The Python implementation uses environment variables via os.getenv():
        - POS_MANAGER_USERNAME
        - POS_MANAGER_PASSWORD
    
    Credentials must be provided via .env files (python-dotenv), CI/CD secret management
    (Jenkins credentials, GitHub Secrets), or system environment variables.

Bug Fixes:
    The Java implementation had a bug in the parameterized login() method (lines 65-69)
    which ignored its input parameters and always used hardcoded credentials. This is
    corrected in the Python implementation by completely removing credential hardcoding.

Migration Context:
    Source: src/main/java/com/testinium/pages/EmployeeP.java
    Target: pages/employee_page.py
    Pattern: PageFactory @FindBy annotations → Property-based locators
    Security: Hardcoded credentials → Environment variables

Element Locators:
    - input_login: Login email input field (By.ID, 'login')
    - input_password: Login password input field (By.ID, 'password')
    - login_button: Login submit button (By.XPATH, "//button[.='Log in']")
    - empl_stage: Employees section link (By.PARTIAL_LINK_TEXT, 'Employees')
    - badges_btn: Badges section link (By.PARTIAL_LINK_TEXT, 'Badges')
    - challenges_btn: Challenges section link (By.PARTIAL_LINK_TEXT, 'Challenges')
    - goals_history_btn: Goals History section link (By.PARTIAL_LINK_TEXT, 'Goals History')
    - departments_btn: Departments section link (By.PARTIAL_LINK_TEXT, 'Departments')
    - create_btn: Create new employee button (By.XPATH, Kanban create button class)
    - employees_name: Employee name input field (By.XPATH, required input field)
    - saved_message: Save button (By.XPATH, form save button class)
    - created_message: Employee created confirmation (By.XPATH, "//p[.='Employee created']")
    - choose_employee: Select employee from list (By.XPATH, employee selection div)
    - edit_employee: Edit employee button (By.XPATH, form edit button)
    - name_edit: Employee name edit field (By.XPATH, dynamically generated field ID)

Example Usage:
    >>> from pages.employee_page import EmployeePage
    >>> from utilities.driver_manager import DriverManager
    >>> import os
    >>>
    >>> # Set environment variables (or use .env file)
    >>> os.environ['POS_MANAGER_USERNAME'] = 'posmanager50@info.com'
    >>> os.environ['POS_MANAGER_PASSWORD'] = 'posmanager'
    >>>
    >>> driver = DriverManager.get_driver()
    >>> employee_page = EmployeePage(driver)
    >>> employee_page.enter_pos_manager_credentials()
    >>> employee_page.empl_stage.click()
"""

import os
import logging
from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage


class EmployeePage(BasePage):
    """
    Employee page object for Testinium application HR and employee management.

    This class provides access to employee management functionality including:
    - Authentication with POS Manager credentials
    - Navigation to employee-related sections (Employees, Badges, Challenges, Goals, Departments)
    - Employee creation and editing workflows
    - Employee selection and management

    Security Notice:
        This page object requires POS_MANAGER_USERNAME and POS_MANAGER_PASSWORD
        environment variables to be set. The enter_pos_manager_credentials() method
        will raise ValueError if these are not configured.

        Never commit credentials to version control. Use:
        - .env files with python-dotenv (development)
        - Jenkins Credentials plugin (CI/CD)
        - GitHub Secrets (GitHub Actions)
        - AWS Secrets Manager / HashiCorp Vault (production)

    Attributes:
        All attributes inherited from BasePage:
            driver (WebDriver): Selenium WebDriver instance
            config (ConfigReader): Configuration reader
            wait (WebDriverWait): Explicit wait instance
            actions (ActionChains): Action chains for complex interactions
        
        Element access via properties:
            input_login: Login email input field
            input_password: Login password input field
            login_button: Login submit button
            empl_stage: Employees section navigation link
            badges_btn: Badges section navigation link
            challenges_btn: Challenges section navigation link
            goals_history_btn: Goals History section navigation link
            departments_btn: Departments section navigation link
            create_btn: Create new employee button
            employees_name: Employee name input field
            saved_message: Save button for employee form
            created_message: Employee created confirmation message
            choose_employee: Employee selection element
            edit_employee: Edit employee button
            name_edit: Employee name edit field

    Example:
        >>> from selenium import webdriver
        >>> from pages.employee_page import EmployeePage
        >>> import os
        >>>
        >>> os.environ['POS_MANAGER_USERNAME'] = 'user@example.com'
        >>> os.environ['POS_MANAGER_PASSWORD'] = 'password'
        >>>
        >>> driver = webdriver.Chrome()
        >>> employee_page = EmployeePage(driver)
        >>> employee_page.enter_pos_manager_credentials()
        >>> employee_page.empl_stage.click()
    """

    # Private locator constants - converted from Java @FindBy annotations
    # Pattern: _ELEMENT_NAME: Tuple[str, str] = (By.STRATEGY, 'locator_value')

    # Login form locators (converted from @FindBy annotations)
    _INPUT_LOGIN: Tuple[str, str] = (By.ID, 'login')
    _INPUT_PASSWORD: Tuple[str, str] = (By.ID, 'password')
    _LOGIN_BUTTON: Tuple[str, str] = (By.XPATH, "//button[.='Log in']")

    # Employee management navigation locators (partial link text for menu items)
    _EMPL_STAGE: Tuple[str, str] = (By.PARTIAL_LINK_TEXT, 'Employees')
    _BADGES_BTN: Tuple[str, str] = (By.PARTIAL_LINK_TEXT, 'Badges')
    _CHALLENGES_BTN: Tuple[str, str] = (By.PARTIAL_LINK_TEXT, 'Challenges')
    _GOALS_HISTORY_BTN: Tuple[str, str] = (By.PARTIAL_LINK_TEXT, 'Goals History')
    _DEPARTMENTS_BTN: Tuple[str, str] = (By.PARTIAL_LINK_TEXT, 'Departments')

    # Employee creation and management locators
    _CREATE_BTN: Tuple[str, str] = (
        By.XPATH,
        "//button[@class='btn btn-primary btn-sm o-kanban-button-new btn-default']"
    )
    _EMPLOYEES_NAME: Tuple[str, str] = (
        By.XPATH,
        "//input[@class='o_field_char o_field_widget o_input o_required_modifier']"
    )
    _SAVED_MESSAGE: Tuple[str, str] = (
        By.XPATH,
        "//button[@class='btn btn-primary btn-sm o_form_button_save']"
    )
    _CREATED_MESSAGE: Tuple[str, str] = (By.XPATH, "//p[.='Employee created']")

    # Employee selection and editing locators
    _CHOOSE_EMPLOYEE: Tuple[str, str] = (
        By.XPATH,
        "//html/body/div[1]/div[2]/div[2]/div/div/div/div[1]"
    )
    _EDIT_EMPLOYEE: Tuple[str, str] = (
        By.XPATH,
        "//html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/button[1]"
    )
    _NAME_EDIT: Tuple[str, str] = (By.XPATH, "//*[@id='o_field_input_678']")

    def __init__(self, driver):
        """
        Initialize EmployeePage with WebDriver instance.

        Inherits from BasePage to gain access to common WebDriver utilities
        including explicit wait helpers, configuration access, and logging.

        Args:
            driver: Selenium WebDriver instance for browser automation
                   Expected to be thread-local instance from DriverManager

        Example:
            >>> from selenium import webdriver
            >>> from pages.employee_page import EmployeePage
            >>>
            >>> driver = webdriver.Chrome()
            >>> employee_page = EmployeePage(driver)
        """
        super().__init__(driver)
        self._logger = logging.getLogger(__name__)
        self._logger.info("EmployeePage initialized")

    # Property-based element accessors with explicit waits
    # Pattern: Replace Java's public WebElement fields with @property methods
    # that return fresh element references using wait_for_element()

    @property
    def input_login(self) -> WebElement:
        """
        Login email input field.

        Converted from Java:
            @FindBy(id = "login")
            public WebElement inputLogin;

        Returns:
            WebElement: Login email input field with explicit wait

        Example:
            >>> employee_page.input_login.send_keys("user@example.com")
        """
        self._logger.debug("Locating input_login element")
        return self.wait_for_element(self._INPUT_LOGIN)

    @property
    def input_password(self) -> WebElement:
        """
        Login password input field.

        Converted from Java:
            @FindBy(id = "password")
            public WebElement inputPass;

        Returns:
            WebElement: Login password input field with explicit wait

        Example:
            >>> employee_page.input_password.send_keys("password123")
        """
        self._logger.debug("Locating input_password element")
        return self.wait_for_element(self._INPUT_PASSWORD)

    @property
    def login_button(self) -> WebElement:
        """
        Login submit button.

        Converted from Java:
            @FindBy(xpath = "//button[.='Log in']")
            public WebElement loginButton;

        Returns:
            WebElement: Login button that is clickable

        Example:
            >>> employee_page.login_button.click()
        """
        self._logger.debug("Locating login_button element")
        return self.wait_for_clickable(self._LOGIN_BUTTON)

    @property
    def empl_stage(self) -> WebElement:
        """
        Employees section navigation link.

        Converted from Java:
            @FindBy(partialLinkText = "Employees")
            public WebElement emplStage;

        Returns:
            WebElement: Employees navigation link that is clickable

        Example:
            >>> employee_page.empl_stage.click()
        """
        self._logger.debug("Locating empl_stage element")
        return self.wait_for_clickable(self._EMPL_STAGE)

    @property
    def badges_btn(self) -> WebElement:
        """
        Badges section navigation link.

        Converted from Java:
            @FindBy(partialLinkText = "Badges")
            public WebElement badgesBtn;

        Returns:
            WebElement: Badges navigation link that is clickable

        Example:
            >>> employee_page.badges_btn.click()
        """
        self._logger.debug("Locating badges_btn element")
        return self.wait_for_clickable(self._BADGES_BTN)

    @property
    def challenges_btn(self) -> WebElement:
        """
        Challenges section navigation link.

        Converted from Java:
            @FindBy(partialLinkText = "Challenges")
            public WebElement challengesBtn;

        Returns:
            WebElement: Challenges navigation link that is clickable

        Example:
            >>> employee_page.challenges_btn.click()
        """
        self._logger.debug("Locating challenges_btn element")
        return self.wait_for_clickable(self._CHALLENGES_BTN)

    @property
    def goals_history_btn(self) -> WebElement:
        """
        Goals History section navigation link.

        Converted from Java:
            @FindBy(partialLinkText = "Goals History")
            public WebElement goalsHistoryBtn;

        Returns:
            WebElement: Goals History navigation link that is clickable

        Example:
            >>> employee_page.goals_history_btn.click()
        """
        self._logger.debug("Locating goals_history_btn element")
        return self.wait_for_clickable(self._GOALS_HISTORY_BTN)

    @property
    def departments_btn(self) -> WebElement:
        """
        Departments section navigation link.

        Converted from Java:
            @FindBy(partialLinkText = "Departments")
            public WebElement departmentsBtn;

        Returns:
            WebElement: Departments navigation link that is clickable

        Example:
            >>> employee_page.departments_btn.click()
        """
        self._logger.debug("Locating departments_btn element")
        return self.wait_for_clickable(self._DEPARTMENTS_BTN)

    @property
    def create_btn(self) -> WebElement:
        """
        Create new employee button (Kanban board create button).

        Converted from Java:
            @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o-kanban-button-new btn-default']")
            public WebElement createBtn;

        Returns:
            WebElement: Create employee button that is clickable

        Example:
            >>> employee_page.create_btn.click()
        """
        self._logger.debug("Locating create_btn element")
        return self.wait_for_clickable(self._CREATE_BTN)

    @property
    def employees_name(self) -> WebElement:
        """
        Employee name input field in creation form.

        Converted from Java:
            @FindBy(xpath = "//input[@class='o_field_char o_field_widget o_input o_required_modifier']")
            public WebElement employeesName;

        Returns:
            WebElement: Employee name input field with explicit wait

        Example:
            >>> employee_page.employees_name.send_keys("John Doe")
        """
        self._logger.debug("Locating employees_name element")
        return self.wait_for_element(self._EMPLOYEES_NAME)

    @property
    def saved_message(self) -> WebElement:
        """
        Save button for employee form.

        Converted from Java:
            @FindBy(xpath = "//button[@class='btn btn-primary btn-sm o_form_button_save']")
            public WebElement savedMessage;

        Note: Despite the name "savedMessage" in the original Java code,
        this element is actually the save button, not a message element.

        Returns:
            WebElement: Save button that is clickable

        Example:
            >>> employee_page.saved_message.click()
        """
        self._logger.debug("Locating saved_message element (save button)")
        return self.wait_for_clickable(self._SAVED_MESSAGE)

    @property
    def created_message(self) -> WebElement:
        """
        Employee created confirmation message.

        Converted from Java:
            @FindBy(xpath = "//p[.='Employee created']")
            public WebElement createdMessage;

        Returns:
            WebElement: Confirmation message element with visibility wait

        Example:
            >>> assert "Employee created" in employee_page.created_message.text
        """
        self._logger.debug("Locating created_message element")
        return self.wait_for_visibility(self._CREATED_MESSAGE)

    @property
    def choose_employee(self) -> WebElement:
        """
        Employee selection element from employee list.

        Converted from Java:
            @FindBy(xpath = "//html/body/div[1]/div[2]/div[2]/div/div/div/div[1]")
            public WebElement chooseEmployee;

        Note: This uses an absolute XPath which is brittle. Consider updating
        to a more stable locator strategy if possible.

        Returns:
            WebElement: Employee selection element that is clickable

        Example:
            >>> employee_page.choose_employee.click()
        """
        self._logger.debug("Locating choose_employee element")
        return self.wait_for_clickable(self._CHOOSE_EMPLOYEE)

    @property
    def edit_employee(self) -> WebElement:
        """
        Edit employee button in employee form.

        Converted from Java:
            @FindBy(xpath = "//html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/button[1]")
            public WebElement editEmployee;

        Note: This uses an absolute XPath which is brittle. Consider updating
        to a more stable locator strategy if possible.

        Returns:
            WebElement: Edit employee button that is clickable

        Example:
            >>> employee_page.edit_employee.click()
        """
        self._logger.debug("Locating edit_employee element")
        return self.wait_for_clickable(self._EDIT_EMPLOYEE)

    @property
    def name_edit(self) -> WebElement:
        """
        Employee name edit field (dynamically generated ID).

        Converted from Java:
            @FindBy(xpath = "//*[@id='o_field_input_678']")
            public WebElement nameEdit;

        Note: This uses a dynamically generated ID which may change between
        application versions or sessions. Monitor for stability.

        Returns:
            WebElement: Employee name edit field with explicit wait

        Example:
            >>> employee_page.name_edit.clear()
            >>> employee_page.name_edit.send_keys("Updated Name")
        """
        self._logger.debug("Locating name_edit element")
        return self.wait_for_element(self._NAME_EDIT)

    def enter_pos_manager_credentials(self) -> None:
        """
        Enter POS Manager credentials from environment variables and submit login.

        SECURITY REMEDIATION: This method replaces the hardcoded credentials
        from EmployeeP.java lines 59-63 and 65-69 which contained:
            - Username: "posmanager50@info.com"
            - Password: "posmanager"

        The Python implementation retrieves credentials from environment variables:
            - POS_MANAGER_USERNAME
            - POS_MANAGER_PASSWORD

        Environment Variable Setup:
            Development (using .env file):
                POS_MANAGER_USERNAME=posmanager50@info.com
                POS_MANAGER_PASSWORD=posmanager

            CI/CD (Jenkins):
                withCredentials([usernamePassword(...)]) { ... }

            CI/CD (GitHub Actions):
                env:
                  POS_MANAGER_USERNAME: ${{ secrets.POS_MANAGER_USERNAME }}
                  POS_MANAGER_PASSWORD: ${{ secrets.POS_MANAGER_PASSWORD }}

            Command Line:
                export POS_MANAGER_USERNAME='posmanager50@info.com'
                export POS_MANAGER_PASSWORD='posmanager'
                behave features/

        Raises:
            ValueError: If POS_MANAGER_USERNAME or POS_MANAGER_PASSWORD environment
                       variables are not set. This ensures explicit failure rather
                       than silent credential absence.

        Example:
            >>> import os
            >>> from pages.employee_page import EmployeePage
            >>>
            >>> # Set environment variables
            >>> os.environ['POS_MANAGER_USERNAME'] = 'posmanager50@info.com'
            >>> os.environ['POS_MANAGER_PASSWORD'] = 'posmanager'
            >>>
            >>> employee_page = EmployeePage(driver)
            >>> employee_page.enter_pos_manager_credentials()
        """
        self._logger.info("Attempting to enter POS Manager credentials from environment")

        # Retrieve credentials from environment variables
        username = os.getenv('POS_MANAGER_USERNAME')
        password = os.getenv('POS_MANAGER_PASSWORD')

        # Validate that both credentials are present
        if not username or not password:
            error_msg = (
                "Missing required environment variables: POS_MANAGER_USERNAME and/or "
                "POS_MANAGER_PASSWORD. Please configure credentials via .env file, "
                "CI/CD secrets, or system environment variables."
            )
            self._logger.error(error_msg)
            raise ValueError(error_msg)

        self._logger.debug("Retrieved POS Manager credentials from environment variables")
        self._logger.debug("Username: %s", username)
        self._logger.debug("Password: %s", "*" * len(password))  # Mask password in logs

        try:
            # Enter username
            self._logger.debug("Entering username into login field")
            self.input_login.send_keys(username)

            # Enter password
            self._logger.debug("Entering password into password field")
            self.input_password.send_keys(password)

            # Click login button
            self._logger.debug("Clicking login button")
            self.login_button.click()

            self._logger.info("POS Manager credentials submitted successfully")

        except Exception as exc:
            self._logger.exception(
                "Failed to enter POS Manager credentials: %s",
                exc
            )
            raise


# Module self-test and example usage
if __name__ == "__main__":
    """
    Module self-test demonstrating EmployeePage functionality.

    Note: This requires environment variables and running WebDriver instance.
    Primarily for documentation purposes.
    """
    print("EmployeePage module loaded successfully")
    print("\n" + "="*70)
    print("SECURITY NOTICE")
    print("="*70)
    print("\nThis page object requires environment variables:")
    print("  - POS_MANAGER_USERNAME")
    print("  - POS_MANAGER_PASSWORD")
    print("\nNEVER commit credentials to version control!")
    print("\nRecommended credential management:")
    print("  Development: .env file with python-dotenv")
    print("  CI/CD: Jenkins Credentials / GitHub Secrets")
    print("  Production: AWS Secrets Manager / HashiCorp Vault")
    print("="*70)
    print("\nExample usage:")
    print("""
    import os
    from selenium import webdriver
    from pages.employee_page import EmployeePage

    # Set environment variables (or use .env file)
    os.environ['POS_MANAGER_USERNAME'] = 'posmanager50@info.com'
    os.environ['POS_MANAGER_PASSWORD'] = 'posmanager'

    # Initialize page object
    driver = webdriver.Chrome()
    employee_page = EmployeePage(driver)

    # Navigate to application and login
    driver.get('https://testinium.example.com')
    employee_page.enter_pos_manager_credentials()

    # Navigate to Employees section
    employee_page.empl_stage.click()

    # Create new employee
    employee_page.create_btn.click()
    employee_page.employees_name.send_keys('John Doe')
    employee_page.saved_message.click()

    # Verify employee created
    assert 'Employee created' in employee_page.created_message.text
    """)
