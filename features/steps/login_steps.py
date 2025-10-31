"""
Login Step Definitions Module

Behave step definitions for login authentication workflows including user navigation,
credential input, login validation, error handling, and field verification.

Migration Context:
    Converted from: src/main/java/com/testinium/step_definitions/LoginSD.java
    Original Pattern: Cucumber @Given/@When/@Then annotations with WebDriver field
    Target Pattern: Behave decorators with context-based driver and page object access

Critical Changes Applied:
    **WAIT STRATEGY FIX**: Original Java implementation (line 17) used hardcoded 3-second
    WebDriverWait instantiation: `WebDriverWait wait = new WebDriverWait(Driver.getDriver(),3)`.
    This Python implementation leverages BasePage's configurable wait utilities accessed
    through LoginPage properties, eliminating hardcoded timeouts as specified in Agent
    Action Plan Section 0.4.3 and 0.9.1.

    **CONTEXT PATTERN**: Java's instance field `LoginP loginP = new LoginP()` (line 16)
    replaced with Behave context pattern `LoginPage(context.driver)` for proper test
    isolation and thread safety in parallel execution.

    **ASSERTION MIGRATION**: Java's JUnit Assert.assertEquals and Assert.assertTrue
    replaced with Python assert statements with descriptive error messages.

Key Features:
    - Navigation to login page with configurable URL from config.yaml
    - Parameterized username and password input from Scenario Outline Examples
    - Login button click and Enter key submission
    - Dashboard title validation ("Odoo") for successful authentication
    - Error message visibility check for invalid credentials
    - Field validation message verification for empty inputs
    - Password input masking verification (type="password" attribute)
    - Support for data-driven testing with Examples tables

Scenario Coverage:
    Implements step definitions for Login.feature scenarios:
    - @UPGN-286: Valid credentials login (SalesManager, PosManager)
    - @UPGN-287: Invalid credentials error handling
    - @UPGN-288: Empty field validation messages
    - @UPGN-289: Password masking verification
    - @UPGN-290: Enter key alternative login method

Design Pattern:
    Follows Behave step definition pattern with context object for state sharing.
    Each step function receives context parameter providing access to:
    - context.driver: Thread-local WebDriver instance from DriverManager
    - context.config: ConfigReader singleton for configuration access
    - Page object instantiation per step for fresh element references

Thread Safety:
    Step definitions are thread-safe when using parallel execution (pytest-xdist or
    behave-parallel) because each scenario receives isolated context object with
    thread-local WebDriver from DriverManager's threading.local() implementation.

Example Usage (from Login.feature):
    Scenario Outline: Users log in with valid credentials
        Given User is on the upgenix login page
        When User enters "<username>" username
        And User enters "<password>" password
        And User clicks the login button
        Then User should see the dashboard

        Examples:
          |username               |password    |
          |salesmanager7@info.com |salesmanager|

Dependencies:
    - behave: BDD framework providing step decorators and context
    - selenium.webdriver.common.by: Locator strategies for element identification
    - pages.login_page.LoginPage: Page object for login page elements and actions
    - utilities.config_reader.ConfigReader: Configuration management for test URLs
"""

import logging
from behave import given, when, then
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from utilities.config_reader import ConfigReader


# Configure module logger
logger = logging.getLogger(__name__)


# ============================================================================
# GIVEN STEPS - Preconditions and Setup
# ============================================================================

@given('User is on the upgenix login page')
def step_navigate_to_login_page(context):
    """
    Navigate to login page using configured URL from config.yaml.

    This step implements the Background step from Login.feature, executed before
    each scenario to ensure user starts on the login page. Replaces Java
    implementation from LoginSD.java lines 19-24.

    Java equivalent:
        @Given("User is on the upgenix login page")
        public void user_is_on_the_upgenix_login_page() {
            String url = ConfigurationReader.getProperty("web.table.url");
            Driver.getDriver().get(url);
        }

    Configuration:
        Retrieves login URL from config.yaml via ConfigReader.get_property('web.table.url').
        Falls back to BASE_URL environment variable if key not found in YAML.

    Args:
        context: Behave context object containing driver and configuration
                context.driver: WebDriver instance for browser navigation

    Raises:
        KeyError: If 'web.table.url' configuration key missing and no default provided
        WebDriverException: If navigation to URL fails

    Example:
        Given User is on the upgenix login page
        # Browser navigates to https://testinium.example.com/login
    """
    logger.info("Navigating to login page")

    # Retrieve login URL from configuration
    # Replaces: ConfigurationReader.getProperty("web.table.url")
    config_reader = ConfigReader()
    login_url = config_reader.get_property('web.table.url')

    logger.debug("Retrieved login URL from configuration: %s", login_url)

    # Navigate to login page
    # Replaces: Driver.getDriver().get(url)
    context.driver.get(login_url)

    logger.info("Successfully navigated to login page: %s", login_url)


# ============================================================================
# WHEN STEPS - Actions and User Interactions
# ============================================================================

@when('User enters "{username}" username')
def step_enter_username(context, username):
    """
    Enter username/email into login form email input field.

    This step supports parameterized username input from Scenario Outline Examples
    tables, enabling data-driven testing with multiple user credentials.

    Java equivalent:
        @When("User enters {string} username")
        public void user_enters_username(String username) {
            loginP.inputEmail.sendKeys(username);
        }

    Implementation Details:
        - Instantiates LoginPage with context.driver for element access
        - Uses LoginPage.input_email property (waits for element presence)
        - Sends keys directly without explicit clear() as field is typically empty
        - Property-based locator prevents stale element exceptions

    Args:
        context: Behave context object containing WebDriver instance
        username: Parameterized username value from Examples table
                 Example values: "salesmanager7@info.com", "posmanager5@info.com"

    Raises:
        TimeoutException: If email input element not found within default timeout
        WebDriverException: If send_keys operation fails

    Example:
        When User enters "salesmanager7@info.com" username
        # Email input field populated with salesmanager7@info.com
    """
    logger.info("Entering username: %s", username)

    # Instantiate LoginPage with current WebDriver
    # Replaces: LoginP loginP = new LoginP()
    login_page = LoginPage(context.driver)

    # Enter username into email input field
    # Replaces: loginP.inputEmail.sendKeys(username)
    login_page.input_email.send_keys(username)

    logger.debug("Successfully entered username: %s", username)


@when('User enters "{password}" password')
def step_enter_password(context, password):
    """
    Enter password into login form password input field.

    This step supports parameterized password input from Scenario Outline Examples
    tables for testing various password scenarios including valid passwords, invalid
    passwords, and password masking verification.

    Java equivalent:
        @When("User enters {string} password")
        public void user_enters_password(String password) {
            loginP.inputPassword.sendKeys(password);
        }

    Implementation Details:
        - Uses LoginPage.input_password property (deduplicated from Java)
        - Original Java had duplicate password fields (inputPassword and bulletPass)
        - Python implementation consolidates to single input_password property
        - Property returns fresh element reference with explicit wait
        - Password value NOT logged for security (only confirmation logged)

    Args:
        context: Behave context object containing WebDriver instance
        password: Parameterized password value from Examples table
                 Example values: "salesmanager", "posmanager", "SaLeSMaNaGeR"

    Raises:
        TimeoutException: If password input element not found within default timeout
        WebDriverException: If send_keys operation fails

    Security Note:
        Password parameter is not logged in detail to prevent credential exposure
        in test logs. Only confirmation of action is logged.

    Example:
        When User enters "salesmanager" password
        # Password input field populated with masked password
    """
    logger.info("Entering password (value not logged for security)")

    # Instantiate LoginPage with current WebDriver
    login_page = LoginPage(context.driver)

    # Enter password into password input field
    # Replaces: loginP.inputPassword.sendKeys(password)
    # Note: Consolidates duplicate Java fields (inputPassword and bulletPass)
    login_page.input_password.send_keys(password)

    logger.debug("Successfully entered password")


@when('User clicks the login button')
def step_click_login_button(context):
    """
    Click the login button to submit authentication credentials.

    This step triggers the login form submission, initiating server-side
    authentication with previously entered username and password.

    Java equivalent:
        @When("User clicks the login button")
        public void user_clicks_the_login_button() {
            loginP.button.click();
        }

    Implementation Details:
        - Uses LoginPage.login_button property with wait_for_clickable
        - Ensures button is visible, enabled, and interactable before click
        - BasePage wait utilities prevent click failures from element not ready
        - Click triggers JavaScript form submission and page navigation

    Args:
        context: Behave context object containing WebDriver instance

    Raises:
        TimeoutException: If login button not clickable within default timeout
        WebDriverException: If click operation fails or element intercepted

    Expected Outcomes:
        - Success: Browser navigates to dashboard (title becomes "Odoo")
        - Failure: Error message alert appears with validation message
        - Empty field: Browser shows native validation message

    Example:
        When User clicks the login button
        # Form submitted, awaiting authentication response
    """
    logger.info("Clicking login button")

    # Instantiate LoginPage with current WebDriver
    login_page = LoginPage(context.driver)

    # Click login button to submit credentials
    # Replaces: loginP.button.click()
    login_page.login_button.click()

    logger.debug("Successfully clicked login button")


@when('User clicks the enter button')
def step_click_enter_button(context):
    """
    Click the login button using Enter key alternative submission method.

    This step verifies that Enter key submission works as alternative to mouse click,
    supporting accessibility and keyboard-only navigation scenarios. Java implementation
    (line 67) actually calls button.click() despite method name suggesting Enter key.

    Java equivalent:
        @When("User clicks the enter button")
        public void user_clicks_the_enter_button() {
            loginP.button.click();
        }

    Implementation Details:
        - Current implementation matches Java behavior (button click)
        - For true Enter key functionality, could use send_keys(Keys.ENTER) on password field
        - Maintains behavioral equivalence with Java version as required
        - Alternative implementation: login_page.input_password.send_keys(Keys.ENTER)

    Args:
        context: Behave context object containing WebDriver instance

    Raises:
        TimeoutException: If login button not clickable within default timeout
        WebDriverException: If click operation fails

    Note:
        Despite step name suggesting Enter key press, this maintains functional
        equivalence with Java implementation which calls button.click() directly.
        Both approaches submit the form successfully.

    Example:
        When User clicks the enter button
        # Login form submitted via button click (functionally equivalent to Enter key)
    """
    logger.info("Clicking enter button (login button click for submission)")

    # Instantiate LoginPage with current WebDriver
    login_page = LoginPage(context.driver)

    # Click login button (maintains Java behavioral equivalence)
    # Java line 67: loginP.button.click()
    login_page.login_button.click()

    logger.debug("Successfully clicked enter button")


# ============================================================================
# THEN STEPS - Assertions and Verifications
# ============================================================================

@then('User should see the dashboard')
def step_verify_dashboard(context):
    """
    Verify successful login by validating dashboard appears and page title is 'Odoo'.

    This step confirms authentication succeeded by checking:
    1. Dashboard element is visible on the page
    2. Browser page title matches expected value "Odoo"

    Java equivalent:
        @Then("User should see the dashboard")
        public void user_should_see_the_dashboard() {
            wait.until(ExpectedConditions.visibilityOf(loginP.dashboard));
            String expectedDashboard = "Odoo";
            String actualDashboard = Driver.getDriver().getTitle();
            Assert.assertEquals("The title is not same as the expected! ", 
                               expectedDashboard, actualDashboard);
        }

    Critical Fix Applied:
        **HARDCODED WAIT ELIMINATION**: Java implementation (line 17) instantiated
        hardcoded 3-second WebDriverWait: `WebDriverWait wait = new WebDriverWait(Driver.getDriver(),3)`.
        Python implementation uses LoginPage.dashboard property which internally calls
        BasePage.wait_for_visibility with configurable timeout from config.yaml,
        eliminating hardcoded wait as specified in Agent Action Plan.

    Implementation Details:
        - LoginPage.dashboard property automatically waits for visibility
        - Replaces explicit wait.until(ExpectedConditions.visibilityOf())
        - Uses Python assert with descriptive message instead of JUnit Assert.assertEquals
        - Page title verification confirms successful post-login navigation

    Args:
        context: Behave context object containing WebDriver instance

    Raises:
        TimeoutException: If dashboard element not visible within default timeout
                         Indicates login failed or page navigation error
        AssertionError: If page title doesn't match expected "Odoo"
                       Indicates navigation to wrong page after login

    Expected State:
        - User successfully authenticated with valid credentials
        - Browser navigated to dashboard page (URL changed from login page)
        - Dashboard navbar visible with id="oe_main_menu_navbar"
        - Page title equals "Odoo"

    Example:
        Then User should see the dashboard
        # Dashboard visible, page title verified as "Odoo"
    """
    logger.info("Verifying dashboard visibility and page title")

    # Instantiate LoginPage with current WebDriver
    login_page = LoginPage(context.driver)

    # Wait for dashboard element to be visible (replaces explicit WebDriverWait)
    # Java line 43: wait.until(ExpectedConditions.visibilityOf(loginP.dashboard))
    # Python: Property automatically waits for visibility via BasePage.wait_for_visibility
    dashboard_element = login_page.dashboard

    # Verify dashboard element is actually displayed
    assert dashboard_element.is_displayed(), \
        "Dashboard element not displayed after login"

    logger.debug("Dashboard element visible")

    # Verify page title matches expected value "Odoo"
    # Java lines 44-46: Assert.assertEquals("The title is not same as the expected! ", 
    #                                        expectedDashboard, actualDashboard)
    expected_title = "Odoo"
    actual_title = context.driver.title

    assert actual_title == expected_title, \
        f"Page title mismatch! Expected: '{expected_title}', Actual: '{actual_title}'"

    logger.info("Dashboard verification successful - page title: %s", actual_title)


@then('User sees error message')
def step_verify_error_message(context):
    """
    Verify error message alert is displayed for invalid login credentials.

    This step confirms authentication failure by checking that error message alert
    element becomes visible after submitting invalid username/password combination.

    Java equivalent:
        @Then("User sees error message")
        public void user_sees_error_message() {
            Assert.assertTrue(loginP.alertErrorMessage.isDisplayed());
        }

    Implementation Details:
        - Uses LoginPage.alert_error_message property with wait_for_visibility
        - BasePage wait ensures element appears before assertion
        - Replaces JUnit Assert.assertTrue with Python assert statement
        - Error message indicates authentication rejected by server

    Args:
        context: Behave context object containing WebDriver instance

    Raises:
        TimeoutException: If error alert element not visible within default timeout
                         Indicates unexpected success (should have failed with invalid credentials)
        AssertionError: If alert element exists but not displayed
                       Indicates DOM presence without visibility

    Expected State:
        - User submitted invalid credentials (wrong username, wrong password, or both)
        - Server rejected authentication attempt
        - Error alert element with class="alert" visible on page
        - Typical error message: "Wrong login/password" or similar

    Example:
        Then User sees error message
        # Error alert visible with "Wrong login/password" message

    Test Scenario Context:
        Scenario Outline: Users log in with invalid credentials (UPGN-287)
            When User enters "salesmanager6@info.com" username
            And User enters "saLesManager" password  # Wrong case
            And User clicks the login button
            Then User sees error message  # This step
    """
    logger.info("Verifying error message visibility for invalid credentials")

    # Instantiate LoginPage with current WebDriver
    login_page = LoginPage(context.driver)

    # Wait for error alert element to be visible
    # Replaces: Assert.assertTrue(loginP.alertErrorMessage.isDisplayed())
    error_alert = login_page.alert_error_message

    # Verify error alert is displayed
    assert error_alert.is_displayed(), \
        "Error message alert not displayed after invalid login attempt"

    # Optional: Log error message text for debugging
    error_text = error_alert.text
    logger.info("Error message displayed: %s", error_text)


@then('User sees "{alert_message}" message')
def step_verify_validation_message(context, alert_message):
    """
    Verify field validation message matches expected text for empty input fields.

    This step validates browser's native HTML5 field validation messages when required
    fields are left empty. Parameterized alert_message allows testing different
    validation messages (e.g., different browser locales).

    Java equivalent:
        @Then("User sees {string} message")
        public void user_sees_please_fill_out_this_field_message(String alertMessage) {
            String expectedMessage = Driver.getDriver()
                .findElement(By.name("login"))
                .getAttribute("validationMessage");
            Assert.assertEquals(expectedMessage, alertMessage);
        }

    Implementation Details:
        - Accesses email input field directly via driver.find_element
        - Retrieves HTML5 validationMessage attribute (browser-native message)
        - Compares retrieved message with parameterized expected message
        - Supports locale-specific validation messages (e.g., French "Veuillez renseigner ce champ.")

    Critical Note:
        Java implementation has assertion order swapped - it asserts:
        Assert.assertEquals(expectedMessage, alertMessage) where expectedMessage is
        from browser and alertMessage is from test data. Python maintains same
        functional equivalence by swapping comparison order to match semantics.

    Args:
        context: Behave context object containing WebDriver instance
        alert_message: Expected validation message from Examples table
                      Example: "Veuillez renseigner ce champ." (French for "Please fill out this field")

    Raises:
        NoSuchElementException: If email input field not found (element lookup by name="login")
        AssertionError: If validation message doesn't match expected value
                       Indicates different browser locale or validation behavior

    Expected State:
        - User clicked login button with empty email field
        - Browser triggered HTML5 field validation
        - ValidationMessage attribute populated on email input element
        - Form submission blocked by browser validation

    Example:
        Then User sees "Veuillez renseigner ce champ." message
        # Browser validation message matches French locale message

    Test Scenario Context:
        Scenario Outline: Empty field validation (UPGN-288)
            When User enters "salesmanager" username  # Only username, no password
            And User clicks the login button
            Then User sees "Veuillez renseigner ce champ." message  # This step
    """
    logger.info("Verifying field validation message: %s", alert_message)

    # Find email input field by name attribute
    # Java line 56: Driver.getDriver().findElement(By.name("login"))
    email_input = context.driver.find_element(By.NAME, "login")

    # Retrieve HTML5 validationMessage attribute
    # Java line 56: .getAttribute("validationMessage")
    actual_message = email_input.get_attribute("validationMessage")

    logger.debug("Retrieved validation message: %s", actual_message)

    # Verify validation message matches expected value
    # Java line 57: Assert.assertEquals(expectedMessage, alertMessage)
    # Note: Java asserts retrieved=expected, we assert expected=retrieved (same outcome)
    assert actual_message == alert_message, \
        f"Validation message mismatch! Expected: '{alert_message}', Actual: '{actual_message}'"

    logger.info("Validation message verification successful")


@then('User should see the password in bullet signs')
def step_verify_password_masking(context):
    """
    Verify password input field masks characters with bullet signs (type="password").

    This step validates password input field security by confirming the HTML input
    element has type="password" attribute, which causes browsers to display entered
    characters as bullet signs (•••) or asterisks (***) instead of plain text.

    Java equivalent:
        @Then("User should see the password in bullet signs")
        public void user_should_see_the_password_in_bullet_signs() {
            Assert.assertTrue(loginP.bulletPass.getAttribute("type").equals("password"));
        }

    Deduplication Note:
        **LOCATOR CONSOLIDATION**: Java implementation used bulletPass field (line 31)
        which was duplicate of inputPassword field (line 16) - both with
        @FindBy(name="password"). Python implementation uses consolidated
        LoginPage.input_password property eliminating duplication.

    Implementation Details:
        - Accesses password field via LoginPage.input_password property
        - Retrieves "type" HTML attribute from input element
        - Verifies type equals "password" (not "text")
        - Password masking is browser-rendered, not application-controlled

    Args:
        context: Behave context object containing WebDriver instance

    Raises:
        TimeoutException: If password input element not found within default timeout
        AssertionError: If type attribute doesn't equal "password"
                       Indicates security issue - password displayed as plain text

    Expected State:
        - Password input field present on login page
        - Input element HTML: <input type="password" name="password">
        - Browser renders input as masked bullets/asterisks
        - User cannot see actual password characters typed

    Security Implication:
        This test validates important security control - passwords must never be
        displayed in plain text in input fields. Failure indicates security vulnerability.

    Example:
        When User enters "salesmanager" password
        Then User should see the password in bullet signs
        # Password field type="password", characters masked as •••••••••••••

    Test Scenario Context:
        Scenario Outline: Password masking verification (UPGN-289)
            When User enters "saLesManager" password
            Then User should see the password in bullet signs  # This step
    """
    logger.info("Verifying password input masking (type='password' attribute)")

    # Instantiate LoginPage with current WebDriver
    login_page = LoginPage(context.driver)

    # Access password input field (consolidated from Java's duplicate bulletPass)
    # Java line 62: loginP.bulletPass.getAttribute("type")
    password_input = login_page.input_password

    # Retrieve type attribute
    input_type = password_input.get_attribute("type")

    logger.debug("Password input type attribute: %s", input_type)

    # Verify type attribute is "password" (not "text")
    # Java line 62: Assert.assertTrue(...getAttribute("type").equals("password"))
    assert input_type == "password", \
        f"Password input type mismatch! Expected: 'password', Actual: '{input_type}' " \
        f"(SECURITY ISSUE: password displayed as plain text)"

    logger.info("Password masking verification successful - input type is 'password'")
