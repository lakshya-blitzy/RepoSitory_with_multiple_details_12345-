"""
Employee Step Definitions Module

Behave step definitions for employee and HR management test scenarios.
Converted from Java Cucumber step definitions (EmployeeStage.java).

Key Features:
- Employee module navigation (Employees, Departments, Challenges, Badges, Goals History stages)
- Employee CRUD operations (create and edit workflows)
- Employee name input and validation
- Saved/created message validation
- Page title verification for different HR module stages
- ConfigurationReader integration for URL and title expectations
- Environment variable-based authentication (SECURITY REMEDIATION)

Critical Security Remediation:
    This module addresses the hardcoded credentials vulnerability from EmployeeP.java
    by using environment variables (POS_MANAGER_USERNAME, POS_MANAGER_PASSWORD) via
    the employee_page.enter_pos_manager_credentials() method.

Critical Improvements from Java Version:
    - Eliminated ALL Thread.sleep() calls (8 instances: 7000ms, 3000ms repeated)
    - Replaced with explicit WebDriverWait conditions using expected_conditions
    - Context pattern for WebDriver and page object instances
    - Comprehensive logging for test execution diagnostics
    - Proper exception handling with descriptive error messages
    - Type hints for better code maintainability

Migration Context:
    Source: src/main/java/com/testinium/step_definitions/EmployeeStage.java
    Target: features/steps/employee_steps.py
    Framework: Cucumber (@When/@Then) → Behave (@when/@then)
    Wait Strategy: Thread.sleep() → WebDriverWait with expected_conditions

Thread.sleep() Elimination Summary:
    Line 48: sleep(7000) → wait.until(title_is("Departments - Odoo"))
    Line 62: sleep(3000) → wait.until(element_to_be_clickable(empl_stage))
    Line 68: sleep(3000) → wait.until(element_to_be_clickable(create_btn))
    Line 70: sleep(3000) → wait.until(title_is("New - Odoo"))
    Line 95: sleep(3000) → wait.until(element_to_be_clickable(empl_stage))
    Line 97: sleep(3000) → wait.until(title_is("Employees - Odoo"))
    Line 100: sleep(3000) → wait.until(element_to_be_clickable(edit_employee))
    Line 103: sleep(3000) → wait.until(element_to_be_clickable(saved_message))

Example Usage:
    Feature: EmployeeFc.feature
    Scenario: Navigate to Employees stage
        When User is on the dashboard
        And User clicks Employees stage
        Then User should see the page title "Employees - Odoo"
"""

import os
import logging
from behave import when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Internal imports from dependency whitelist
from pages.employee_page import EmployeePage
from utilities.config_reader import ConfigReader


# Module logger configuration
logger = logging.getLogger(__name__)


@when("User is on upgenix login page")
def user_is_on_upgenix_login_page(context):
    """
    Navigate to the Upgenix login page URL from configuration.

    Converted from Java:
        @When("User is on upgenix login page")
        public void user_is_on_upgenix_login_page() {
            String url = ConfigurationReader.getProperty("web.table.url");
            Driver.getDriver().get(url);
        }

    Args:
        context: Behave context object containing driver and shared state

    Configuration Required:
        web.table.url: Base URL for the Upgenix login page

    Example:
        Given User is on upgenix login page

    Technical Details:
        - Retrieves 'web.table.url' from config/config.yaml
        - Navigates browser to login page URL
        - Uses context.driver instead of static Driver.getDriver()
    """
    logger.info("Step: User is on upgenix login page")
    
    try:
        # Retrieve login URL from configuration
        config = ConfigReader()
        login_url = config.get_property("web.table.url")
        
        logger.debug(f"Retrieved login URL from config: {login_url}")
        
        # Navigate to login page
        context.driver.get(login_url)
        logger.info(f"Successfully navigated to login page: {login_url}")
        
    except Exception as exc:
        logger.exception(f"Failed to navigate to upgenix login page: {exc}")
        raise


@when("User is on the dashboard")
def user_is_on_the_dashboard(context):
    """
    Navigate to dashboard and authenticate with POS Manager credentials.

    Converted from Java:
        @When("User is on the dashboard")
        public void user_is_on_the_dashboard() {
            Driver.getDriver().get(ConfigurationReader.getProperty("url"));
            employeePage.login();
        }

    SECURITY REMEDIATION:
        Replaces employeePage.login() which used hardcoded credentials with
        employee_page.enter_pos_manager_credentials() which retrieves credentials
        from environment variables (POS_MANAGER_USERNAME, POS_MANAGER_PASSWORD).

    Args:
        context: Behave context object containing driver and shared state

    Configuration Required:
        url: Dashboard URL after successful authentication

    Environment Variables Required:
        POS_MANAGER_USERNAME: POS Manager username (e.g., posmanager50@info.com)
        POS_MANAGER_PASSWORD: POS Manager password

    Raises:
        ValueError: If required environment variables are not set

    Example:
        Given User is on the dashboard

    Technical Details:
        - Retrieves 'url' from config/config.yaml
        - Navigates to dashboard URL
        - Instantiates EmployeePage with context.driver
        - Calls enter_pos_manager_credentials() for secure authentication
    """
    logger.info("Step: User is on the dashboard")
    
    try:
        # Retrieve dashboard URL from configuration
        config = ConfigReader()
        dashboard_url = config.get_property("url")
        
        logger.debug(f"Retrieved dashboard URL from config: {dashboard_url}")
        
        # Navigate to dashboard
        context.driver.get(dashboard_url)
        logger.debug(f"Navigated to dashboard: {dashboard_url}")
        
        # Initialize employee page object
        employee_page = EmployeePage(context.driver)
        
        # Authenticate using environment variables (SECURITY REMEDIATION)
        logger.info("Authenticating with POS Manager credentials from environment variables")
        employee_page.enter_pos_manager_credentials()
        
        logger.info("Successfully authenticated and on the dashboard")
        
    except ValueError as val_err:
        logger.error(f"Credential configuration error: {val_err}")
        raise
    except Exception as exc:
        logger.exception(f"Failed to navigate to dashboard and login: {exc}")
        raise


@when("User clicks Employees stage")
def user_clicks_employees_stage(context):
    """
    Click Employees navigation link and verify page title.

    Converted from Java:
        @When("User clicks Employees stage")
        public void user_clicks_employees_stage() {
            employeePage.emplStage.click();
            wait.until(ExpectedConditions.titleIs(ConfigurationReader.getProperty("EmplTitle")));
            Assert.assertTrue(Driver.getDriver().getTitle().equals("Employees - Odoo"));
        }

    Args:
        context: Behave context object containing driver and shared state

    Configuration Required:
        EmplTitle: Expected page title for Employees stage (default: "Employees - Odoo")

    Raises:
        AssertionError: If page title does not match expected "Employees - Odoo"
        TimeoutException: If title does not update within timeout period

    Example:
        When User clicks Employees stage

    Technical Details:
        - Instantiates EmployeePage with context.driver
        - Clicks empl_stage navigation link
        - Waits for page title to match expected value using explicit wait
        - Validates final page title equals "Employees - Odoo"
        - Configurable timeout (10 seconds default from WebDriverWait)
    """
    logger.info("Step: User clicks Employees stage")
    
    try:
        # Initialize employee page object
        employee_page = EmployeePage(context.driver)
        
        # Retrieve expected title from configuration
        config = ConfigReader()
        expected_title = config.get_property("EmplTitle", default="Employees - Odoo")
        
        logger.debug(f"Expected page title: {expected_title}")
        
        # Click Employees stage navigation link
        logger.debug("Clicking Employees stage link")
        employee_page.empl_stage.click()
        
        # Wait for page title to update (replaces Thread.sleep)
        wait = WebDriverWait(context.driver, 10)
        logger.debug(f"Waiting for page title to be: {expected_title}")
        wait.until(EC.title_is(expected_title))
        
        # Validate page title
        actual_title = context.driver.title
        logger.debug(f"Actual page title: {actual_title}")
        
        assert actual_title == "Employees - Odoo", (
            f"Expected page title 'Employees - Odoo', but got '{actual_title}'"
        )
        
        logger.info("Successfully navigated to Employees stage")
        
    except AssertionError as assert_err:
        logger.error(f"Page title validation failed: {assert_err}")
        raise
    except Exception as exc:
        logger.exception(f"Failed to click Employees stage: {exc}")
        raise


@when("User clicks Challenges stage")
def user_clicks_challenges_stage(context):
    """
    Navigate through Badges → Challenges → Goals History stages with visibility waits.

    Converted from Java:
        @When("User clicks Challenges stage")
        public void user_clicks_challenges_stage() {
            employeePage.badgesBtn.click();
            wait.until(ExpectedConditions.visibilityOf(employeePage.badgesBtn));
            employeePage.challengesBtn.click();
            wait.until(ExpectedConditions.visibilityOf(employeePage.challengesBtn));
            employeePage.goalsHistoryBtn.click();
            wait.until(ExpectedConditions.visibilityOf(employeePage.goalsHistoryBtn));
        }

    Args:
        context: Behave context object containing driver and shared state

    Raises:
        TimeoutException: If any navigation button is not visible within timeout

    Example:
        When User clicks Challenges stage

    Technical Details:
        - Multi-stage navigation through HR module stages
        - Clicks Badges button and waits for visibility
        - Clicks Challenges button and waits for visibility
        - Clicks Goals History button and waits for visibility
        - Each click followed by explicit visibility wait (10 seconds timeout)
        - Ensures page transitions complete before next interaction
    """
    logger.info("Step: User clicks Challenges stage")
    
    try:
        # Initialize employee page object and wait
        employee_page = EmployeePage(context.driver)
        wait = WebDriverWait(context.driver, 10)
        
        # Stage 1: Click Badges button
        logger.debug("Clicking Badges button")
        employee_page.badges_btn.click()
        logger.debug("Waiting for Badges button visibility")
        wait.until(EC.visibility_of(employee_page.badges_btn))
        logger.info("Badges stage visible")
        
        # Stage 2: Click Challenges button
        logger.debug("Clicking Challenges button")
        employee_page.challenges_btn.click()
        logger.debug("Waiting for Challenges button visibility")
        wait.until(EC.visibility_of(employee_page.challenges_btn))
        logger.info("Challenges stage visible")
        
        # Stage 3: Click Goals History button
        logger.debug("Clicking Goals History button")
        employee_page.goals_history_btn.click()
        logger.debug("Waiting for Goals History button visibility")
        wait.until(EC.visibility_of(employee_page.goals_history_btn))
        logger.info("Goals History stage visible - Challenges stage navigation complete")
        
    except Exception as exc:
        logger.exception(f"Failed to navigate through Challenges stages: {exc}")
        raise


@when("User clicks Departments stage")
def user_clicks_departments_stage(context):
    """
    Click Departments navigation link and wait for page load.

    Converted from Java:
        @When("User clicks Departments stage")
        public void user_clicks_departments_stage() throws InterruptedException {
            employeePage.departmentsBtn.click();
            Thread.sleep(7000);  // ELIMINATED
        }

    CRITICAL IMPROVEMENT:
        Eliminated Thread.sleep(7000) anti-pattern from line 48 of Java version.
        Replaced with explicit wait for page title to ensure proper page load.

    Args:
        context: Behave context object containing driver and shared state

    Raises:
        TimeoutException: If Departments page title is not displayed within timeout

    Example:
        When User clicks Departments stage

    Technical Details:
        - Clicks departments_btn navigation link
        - Waits explicitly for "Departments - Odoo" page title (10 seconds timeout)
        - Replaces 7-second sleep with condition-based wait
        - More reliable and faster than arbitrary sleep duration
    """
    logger.info("Step: User clicks Departments stage")
    
    try:
        # Initialize employee page object and wait
        employee_page = EmployeePage(context.driver)
        wait = WebDriverWait(context.driver, 10)
        
        # Click Departments button
        logger.debug("Clicking Departments button")
        employee_page.departments_btn.click()
        
        # Wait for page title to update (replaces Thread.sleep(7000))
        expected_title = "Departments - Odoo"
        logger.debug(f"Waiting for page title: {expected_title}")
        wait.until(EC.title_is(expected_title))
        
        logger.info("Successfully navigated to Departments stage")
        
    except Exception as exc:
        logger.exception(f"Failed to click Departments stage: {exc}")
        raise


@then("User should see the last stage title")
def user_should_see_the_last_stage_title(context):
    """
    Verify the page title is "Departments - Odoo".

    Converted from Java:
        @Then("User should see the last stage title")
        public void user_should_see_the_last_stage_title() {
            Assert.assertTrue(Driver.getDriver().getTitle().equals("Departments - Odoo"));
            //String act = Driver.getDriver().getTitle();
            //String exp = "Departments - Odoo";
            //Assert.assertEquals(exp,act);
        }

    Args:
        context: Behave context object containing driver and shared state

    Raises:
        AssertionError: If page title does not equal "Departments - Odoo"

    Example:
        Then User should see the last stage title

    Technical Details:
        - Retrieves current page title from context.driver
        - Validates title equals "Departments - Odoo"
        - Descriptive assertion error message for debugging
    """
    logger.info("Step: User should see the last stage title")
    
    try:
        # Get current page title
        actual_title = context.driver.title
        expected_title = "Departments - Odoo"
        
        logger.debug(f"Expected title: {expected_title}")
        logger.debug(f"Actual title: {actual_title}")
        
        # Validate page title
        assert actual_title == expected_title, (
            f"Expected page title '{expected_title}', but got '{actual_title}'"
        )
        
        logger.info("Successfully verified Departments stage title")
        
    except AssertionError as assert_err:
        logger.error(f"Page title validation failed: {assert_err}")
        raise


@when("User is on the employees dashboard")
def user_is_on_the_employees_dashboard(context):
    """
    Navigate to dashboard, authenticate, and navigate to Employees stage.

    Converted from Java:
        @When("User is on the employees dashboard")
        public void user_is_on_the_employees_dashboard() throws InterruptedException {
            Driver.getDriver().get(ConfigurationReader.getProperty("url"));
            employeePage.login();
            Thread.sleep(3000);  // ELIMINATED
            employeePage.emplStage.click();
        }

    CRITICAL IMPROVEMENTS:
        - Replaced employeePage.login() with environment variable-based authentication
        - Eliminated Thread.sleep(3000) from line 62
        - Added explicit wait for empl_stage button to be clickable

    Args:
        context: Behave context object containing driver and shared state

    Configuration Required:
        url: Dashboard URL

    Environment Variables Required:
        POS_MANAGER_USERNAME: POS Manager username
        POS_MANAGER_PASSWORD: POS Manager password

    Raises:
        ValueError: If required environment variables are not set
        TimeoutException: If Employees stage button is not clickable within timeout

    Example:
        Given User is on the employees dashboard

    Technical Details:
        - Navigates to dashboard URL from configuration
        - Authenticates with POS Manager credentials from environment variables
        - Waits for empl_stage button to be clickable (replaces sleep)
        - Clicks Employees stage navigation link
    """
    logger.info("Step: User is on the employees dashboard")
    
    try:
        # Retrieve dashboard URL from configuration
        config = ConfigReader()
        dashboard_url = config.get_property("url")
        
        logger.debug(f"Retrieved dashboard URL: {dashboard_url}")
        
        # Navigate to dashboard
        context.driver.get(dashboard_url)
        logger.debug(f"Navigated to dashboard: {dashboard_url}")
        
        # Initialize employee page object
        employee_page = EmployeePage(context.driver)
        
        # Authenticate using environment variables (SECURITY REMEDIATION)
        logger.info("Authenticating with POS Manager credentials")
        employee_page.enter_pos_manager_credentials()
        logger.debug("Authentication successful")
        
        # Wait for Employees stage button to be clickable (replaces Thread.sleep(3000))
        wait = WebDriverWait(context.driver, 10)
        logger.debug("Waiting for Employees stage button to be clickable")
        wait.until(EC.element_to_be_clickable(employee_page._EMPL_STAGE))
        
        # Click Employees stage
        logger.debug("Clicking Employees stage link")
        employee_page.empl_stage.click()
        
        logger.info("Successfully navigated to employees dashboard")
        
    except ValueError as val_err:
        logger.error(f"Credential configuration error: {val_err}")
        raise
    except Exception as exc:
        logger.exception(f"Failed to navigate to employees dashboard: {exc}")
        raise


@when('User creates new employees "{name}" in the Employees stage')
def user_creates_new_employees_in_the_employees_stage(context, name):
    """
    Create a new employee with the specified name.

    Converted from Java:
        @When("User creates new employees {string} in the Employees stage")
        public void user_creates_new_employees_in_the_employees_stage(String name) 
            throws InterruptedException {
            Thread.sleep(3000);  // ELIMINATED
            employeePage.createBtn.click();
            Thread.sleep(3000);  // ELIMINATED
            wait.until(ExpectedConditions.titleIs("New - Odoo"));
            employeePage.employeesName.sendKeys(name);
            employeePage.savedMessage.click();
        }

    CRITICAL IMPROVEMENTS:
        - Eliminated Thread.sleep(3000) from line 68
        - Eliminated Thread.sleep(3000) from line 70
        - Added explicit waits for create_btn clickability and title change
        - Added explicit wait for saved_message button clickability

    Args:
        context: Behave context object containing driver and shared state
        name: Name of the employee to create (from Gherkin step parameter)

    Raises:
        TimeoutException: If expected elements or page title do not appear within timeout

    Example:
        When User creates new employees "John Doe" in the Employees stage

    Technical Details:
        - Waits for create_btn to be clickable (replaces first sleep)
        - Clicks Create button
        - Waits for page title to change to "New - Odoo" (replaces second sleep)
        - Enters employee name into employees_name input field
        - Waits for saved_message button to be clickable
        - Clicks Save button to create employee
    """
    logger.info(f'Step: User creates new employees "{name}" in the Employees stage')
    
    try:
        # Initialize employee page object and wait
        employee_page = EmployeePage(context.driver)
        wait = WebDriverWait(context.driver, 10)
        
        # Wait for Create button to be clickable (replaces Thread.sleep(3000))
        logger.debug("Waiting for Create button to be clickable")
        wait.until(EC.element_to_be_clickable(employee_page._CREATE_BTN))
        
        # Click Create button
        logger.debug("Clicking Create button")
        employee_page.create_btn.click()
        
        # Wait for page title to change to "New - Odoo" (replaces Thread.sleep(3000))
        expected_title = "New - Odoo"
        logger.debug(f"Waiting for page title: {expected_title}")
        wait.until(EC.title_is(expected_title))
        logger.debug(f"Page title changed to: {expected_title}")
        
        # Enter employee name
        logger.debug(f"Entering employee name: {name}")
        employee_page.employees_name.send_keys(name)
        
        # Wait for Save button to be clickable
        logger.debug("Waiting for Save button to be clickable")
        wait.until(EC.element_to_be_clickable(employee_page._SAVED_MESSAGE))
        
        # Click Save button
        logger.debug("Clicking Save button")
        employee_page.saved_message.click()
        
        logger.info(f"Successfully created employee: {name}")
        
    except Exception as exc:
        logger.exception(f"Failed to create employee '{name}': {exc}")
        raise


@then("User should see the Employee created message under full profile")
def user_should_see_the_employee_created_message_under_full_profile(context):
    """
    Verify that the "Employee created" confirmation message is displayed.

    Converted from Java:
        @Then("User should see the Employee created message under full profile")
        public void user_should_see_the_message_under_full_profile() {
            Assert.assertTrue(employeePage.createdMessage.isDisplayed());
            //String expected = "Employee created";
            //String actual = employeePage.createdMessage.getText();
            //Assert.assertEquals(expected,actual);
        }

    Args:
        context: Behave context object containing driver and shared state

    Raises:
        AssertionError: If created_message element is not displayed

    Example:
        Then User should see the Employee created message under full profile

    Technical Details:
        - Instantiates EmployeePage with context.driver
        - Accesses created_message property (includes visibility wait)
        - Validates element is displayed
        - Property accessor handles explicit wait for visibility
    """
    logger.info("Step: User should see the Employee created message under full profile")
    
    try:
        # Initialize employee page object
        employee_page = EmployeePage(context.driver)
        
        # Verify created message is displayed
        # Note: created_message property uses wait_for_visibility() internally
        logger.debug("Checking if Employee created message is displayed")
        created_msg_element = employee_page.created_message
        
        assert created_msg_element.is_displayed(), (
            "Expected 'Employee created' message to be displayed, but it was not visible"
        )
        
        actual_text = created_msg_element.text
        logger.debug(f"Created message text: {actual_text}")
        
        logger.info("Successfully verified Employee created message is displayed")
        
    except AssertionError as assert_err:
        logger.error(f"Employee created message validation failed: {assert_err}")
        raise
    except Exception as exc:
        logger.exception(f"Failed to verify Employee created message: {exc}")
        raise


@then("User should see listed employees in the Employees stage")
def user_should_see_listed_employees_in_the_employees_stage(context):
    """
    Navigate to Employees stage and verify page title.

    Converted from Java:
        @Then("User should see listed employees in the Employees stage")
        public void user_should_see_listed_employees_in_the_employees_stage() 
            throws InterruptedException {
            employeePage.emplStage.click();
            wait.until(ExpectedConditions.titleIs("Employees - Odoo"));
            Assert.assertTrue(Driver.getDriver().getTitle().equals("Employees - Odoo"));
        }

    Args:
        context: Behave context object containing driver and shared state

    Raises:
        AssertionError: If page title does not equal "Employees - Odoo"
        TimeoutException: If page title does not update within timeout

    Example:
        Then User should see listed employees in the Employees stage

    Technical Details:
        - Clicks empl_stage navigation link
        - Waits for page title to be "Employees - Odoo"
        - Validates final page title equals "Employees - Odoo"
        - 10 second timeout for title change
    """
    logger.info("Step: User should see listed employees in the Employees stage")
    
    try:
        # Initialize employee page object and wait
        employee_page = EmployeePage(context.driver)
        wait = WebDriverWait(context.driver, 10)
        
        # Click Employees stage link
        logger.debug("Clicking Employees stage link")
        employee_page.empl_stage.click()
        
        # Wait for page title to update
        expected_title = "Employees - Odoo"
        logger.debug(f"Waiting for page title: {expected_title}")
        wait.until(EC.title_is(expected_title))
        
        # Validate page title
        actual_title = context.driver.title
        logger.debug(f"Actual page title: {actual_title}")
        
        assert actual_title == expected_title, (
            f"Expected page title '{expected_title}', but got '{actual_title}'"
        )
        
        logger.info("Successfully verified Employees stage with listed employees")
        
    except AssertionError as assert_err:
        logger.error(f"Employees stage title validation failed: {assert_err}")
        raise
    except Exception as exc:
        logger.exception(f"Failed to verify listed employees in Employees stage: {exc}")
        raise


@when("User edits created employees in the Employees module")
def user_edits_created_employees_in_the_employees_module(context):
    """
    Navigate to dashboard, authenticate, select employee, and edit employee name to "Sterling".

    Converted from Java:
        @When("User edits created employees in the Employees module")
        public void user_edits_created_employees_in_the_employees_module() 
            throws InterruptedException {
            Driver.getDriver().get(ConfigurationReader.getProperty("url"));
            employeePage.login();
            Thread.sleep(3000);  // ELIMINATED
            employeePage.emplStage.click();
            Thread.sleep(3000);  // ELIMINATED
            employeePage.chooseEmployee.click();
            employeePage.editEmployee.click();
            Thread.sleep(3000);  // ELIMINATED
            employeePage.nameEdit.clear();
            employeePage.nameEdit.sendKeys("Sterling");
            Thread.sleep(3000);  // ELIMINATED
            employeePage.savedMessage.click();
        }

    CRITICAL IMPROVEMENTS:
        - Eliminated Thread.sleep(3000) from line 95
        - Eliminated Thread.sleep(3000) from line 97
        - Eliminated Thread.sleep(3000) from line 100
        - Eliminated Thread.sleep(3000) from line 103
        - Replaced with explicit waits for element clickability
        - Environment variable-based authentication

    Args:
        context: Behave context object containing driver and shared state

    Configuration Required:
        url: Dashboard URL

    Environment Variables Required:
        POS_MANAGER_USERNAME: POS Manager username
        POS_MANAGER_PASSWORD: POS Manager password

    Raises:
        ValueError: If required environment variables are not set
        TimeoutException: If expected elements do not become clickable within timeout

    Example:
        When User edits created employees in the Employees module

    Technical Details:
        - Navigates to dashboard and authenticates
        - Waits for empl_stage button clickability (replaces sleep)
        - Clicks Employees stage
        - Waits for page title to confirm navigation (replaces sleep)
        - Clicks to select employee from list
        - Waits for edit_employee button clickability (replaces sleep)
        - Clicks Edit button
        - Clears and enters new name "Sterling"
        - Waits for saved_message button clickability (replaces sleep)
        - Clicks Save button
    """
    logger.info("Step: User edits created employees in the Employees module")
    
    try:
        # Retrieve dashboard URL from configuration
        config = ConfigReader()
        dashboard_url = config.get_property("url")
        
        logger.debug(f"Retrieved dashboard URL: {dashboard_url}")
        
        # Navigate to dashboard
        context.driver.get(dashboard_url)
        logger.debug(f"Navigated to dashboard: {dashboard_url}")
        
        # Initialize employee page object
        employee_page = EmployeePage(context.driver)
        wait = WebDriverWait(context.driver, 10)
        
        # Authenticate using environment variables (SECURITY REMEDIATION)
        logger.info("Authenticating with POS Manager credentials")
        employee_page.enter_pos_manager_credentials()
        logger.debug("Authentication successful")
        
        # Wait for Employees stage button to be clickable (replaces Thread.sleep(3000))
        logger.debug("Waiting for Employees stage button to be clickable")
        wait.until(EC.element_to_be_clickable(employee_page._EMPL_STAGE))
        
        # Click Employees stage
        logger.debug("Clicking Employees stage link")
        employee_page.empl_stage.click()
        
        # Wait for Employees page title (replaces Thread.sleep(3000))
        expected_title = "Employees - Odoo"
        logger.debug(f"Waiting for page title: {expected_title}")
        wait.until(EC.title_is(expected_title))
        logger.debug(f"Page title confirmed: {expected_title}")
        
        # Select employee from list
        logger.debug("Clicking to select employee from list")
        employee_page.choose_employee.click()
        
        # Wait for Edit button to be clickable (replaces Thread.sleep(3000))
        logger.debug("Waiting for Edit button to be clickable")
        wait.until(EC.element_to_be_clickable(employee_page._EDIT_EMPLOYEE))
        
        # Click Edit button
        logger.debug("Clicking Edit button")
        employee_page.edit_employee.click()
        
        # Clear existing name and enter new name
        logger.debug("Clearing existing employee name")
        employee_page.name_edit.clear()
        
        new_name = "Sterling"
        logger.debug(f"Entering new employee name: {new_name}")
        employee_page.name_edit.send_keys(new_name)
        
        # Wait for Save button to be clickable (replaces Thread.sleep(3000))
        logger.debug("Waiting for Save button to be clickable")
        wait.until(EC.element_to_be_clickable(employee_page._SAVED_MESSAGE))
        
        # Click Save button
        logger.debug("Clicking Save button")
        employee_page.saved_message.click()
        
        logger.info("Successfully edited employee name to Sterling")
        
    except ValueError as val_err:
        logger.error(f"Credential configuration error: {val_err}")
        raise
    except Exception as exc:
        logger.exception(f"Failed to edit employee: {exc}")
        raise


@then("User should see the edited name in the Employees module")
def user_should_see_the_edited_name_in_the_employees_module(context):
    """
    Navigate back to Employees stage to view the edited employee.

    Converted from Java:
        @Then("User should see the edited name in the Employees module")
        public void user_should_see_the_edited_name_in_the_employees_module() {
            employeePage.emplStage.click();
        }

    Args:
        context: Behave context object containing driver and shared state

    Example:
        Then User should see the edited name in the Employees module

    Technical Details:
        - Clicks empl_stage navigation link to return to employees list
        - This allows verification that the edited employee name is displayed
        - No explicit validation in this step (validation happens in visual inspection
          or could be enhanced with explicit name verification)
    """
    logger.info("Step: User should see the edited name in the Employees module")
    
    try:
        # Initialize employee page object
        employee_page = EmployeePage(context.driver)
        
        # Click Employees stage to view the edited employee
        logger.debug("Clicking Employees stage link to view edited employee")
        employee_page.empl_stage.click()
        
        logger.info("Successfully navigated to Employees stage to view edited employee")
        
    except Exception as exc:
        logger.exception(f"Failed to navigate to Employees stage: {exc}")
        raise


# Module self-test and documentation
if __name__ == "__main__":
    """
    Employee steps module loaded successfully.
    
    This module provides Behave step definitions for employee management test scenarios.
    All steps follow the Page Object Model pattern with explicit waits and environment
    variable-based credential management.
    
    Step Definitions Implemented:
        1. @when("User is on upgenix login page")
        2. @when("User is on the dashboard")
        3. @when("User clicks Employees stage")
        4. @when("User clicks Challenges stage")
        5. @when("User clicks Departments stage")
        6. @then("User should see the last stage title")
        7. @when("User is on the employees dashboard")
        8. @when('User creates new employees "{name}" in the Employees stage')
        9. @then("User should see the Employee created message under full profile")
        10. @then("User should see listed employees in the Employees stage")
        11. @when("User edits created employees in the Employees module")
        12. @then("User should see the edited name in the Employees module")
    
    Environment Variables Required:
        POS_MANAGER_USERNAME: Username for POS Manager authentication
        POS_MANAGER_PASSWORD: Password for POS Manager authentication
    
    Configuration Requirements:
        config/config.yaml must contain:
            - url: Dashboard URL
            - web.table.url: Login page URL
            - EmplTitle: Expected Employees page title
    """
    print("Employee steps module loaded successfully")
    print("\nImplemented 12 step definitions for employee management scenarios")
    print("\nSecurity Notice:")
    print("  - Requires POS_MANAGER_USERNAME environment variable")
    print("  - Requires POS_MANAGER_PASSWORD environment variable")
    print("\nCritical Improvements:")
    print("  - Eliminated 8 Thread.sleep() calls (total: 29000ms saved)")
    print("  - Replaced with explicit WebDriverWait conditions")
    print("  - Environment variable-based credential management")
    print("  - Comprehensive logging for test diagnostics")
