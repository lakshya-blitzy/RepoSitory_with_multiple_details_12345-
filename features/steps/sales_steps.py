"""
Sales Step Definitions Module

Behave step definitions for sales and customer management operations.
This module implements BDD steps for:
- Sales dashboard navigation
- Customer creation workflows with address, state, and country fields
- Customer save and list operations
- Customer search functionality with keyboard interactions
- Validation error handling for incomplete customer data
- Title verification for Customers module

Migration Context:
    Converted from Sales.java Cucumber step definitions (Java) to Python Behave decorators.
    Original implementation used @When/@Then/@And annotations from io.cucumber.java.en package
    with hardcoded 4-second WebDriverWait and InterruptedException declarations. This Python
    version uses @when/@then/@step decorators from behave package with context-based driver
    management and logging framework instead of System.out.println debug statements.

Key Changes from Java Implementation:
    1. Replaced Cucumber @When/@Then/@And with Behave @when/@then/@step decorators
    2. Converted SalesP salesp instance to sales_page = SalesPage(context.driver) pattern
    3. Replaced WebDriverWait(Driver.getDriver(), 4) with context-based utilities from BasePage
    4. Replaced Assert.assertEquals() with Python assert statements with descriptive messages
    5. Removed System.out.println debug logging (Java lines 34-35, 74-75, 93-94)
    6. Added logging.debug() and logging.info() for structured test execution logging
    7. Added missing assertions where Java code only printed values without asserting
    8. Implemented Keys.ENTER keyboard interaction for search functionality (line 68)
    9. Removed InterruptedException declarations (not needed in Python)
    10. Maintained exact Gherkin step text for behavioral preservation

Technical Debt from Java Source:
    - Hardcoded customer data in Java (line 44: "Lucas", line 45: "1 boulevard auguste rodin 75000",
      line 48: "Albania", line 49: "78") - maintained for behavioral equivalence but recommend
      Faker integration or parameterized data in future enhancement
    - Java code printed values without assertions in lines 74-75 (actualName/expectedName) and
      lines 93-94 (actualWarning/expectedWarning) - added proper assertions in Python version

Security Note:
    No hardcoded credentials present in this module. All test data is non-sensitive customer
    information which is appropriate for test scenarios.

Example Usage:
    Feature file (Sales.feature) scenario:
        When User click on the sales dashboard
        And User click customers button
        When User can create the customer
        And User can save the customer
        Then User can find his name "Lucas" from search bar

    This module provides the Python implementations for these Gherkin steps.

Design Pattern:
    - Context pattern: Uses behave's Context object for sharing driver and state
    - Page Object Model: Delegates element interactions to SalesPage class
    - Property-based locators: SalesPage provides fresh element references via @property
    - Explicit waits: All waits handled by BasePage utilities (inherited by SalesPage)
    - Structured logging: Python logging module for test diagnostics and debugging
"""

import logging
from behave import when, then, step
from selenium.webdriver.common.keys import Keys
from pages.sales_page import SalesPage

# Configure module-level logger for step execution tracking
logger = logging.getLogger(__name__)


@when('User click on the sales dashboard')
def user_click_on_sales_dashboard(context):
    """
    Navigate to sales dashboard by clicking the sales partial link.

    Corresponds to Java method: user_click_on_the_sales_dashboard() (line 19)
    Original Java: salesp.salesPartial.click(); wait.until(visibilityOf(salesp.salesPartial))

    Args:
        context: Behave context object containing driver instance

    Behavior:
        1. Instantiate SalesPage with context.driver
        2. Click on sales partial link text navigation element
        3. Wait for sales element visibility (implicit in property-based locator)

    Migration Notes:
        - Removed InterruptedException declaration (not needed in Python)
        - Removed explicit WebDriverWait - handled by SalesPage.sales_partial property
        - Added debug logging for test execution tracking
    """
    logger.info("Step: User clicks on the sales dashboard")
    sales_page = SalesPage(context.driver)
    sales_page.sales_partial.click()
    logger.debug("Sales dashboard link clicked, waiting for page load")


@when('User click customers button')
def user_click_customers_button(context):
    """
    Navigate to customers page and verify page title.

    Corresponds to Java method: user_click_customers_button() (line 25)
    Original Java: salesp.customersButton.click(); wait; title assertion with System.out.println

    Args:
        context: Behave context object containing driver instance

    Behavior:
        1. Click customers button to navigate to Customers page
        2. Wait for customers button visibility
        3. Verify page title matches "Customers - Odoo"

    Assertions:
        - Page title must equal "Customers - Odoo" (case-sensitive)

    Migration Notes:
        - Removed InterruptedException declaration
        - Replaced System.out.println (lines 34-35) with logger.debug()
        - Replaced Assert.assertEquals() with Python assert statement
        - Fixed Java title comparison logic (was comparing "Customers - Odoo" with
          "Customers - {actualTitle}" which would always fail)
        - Corrected to verify driver.title equals "Customers - Odoo"
    """
    logger.info("Step: User clicks customers button")
    sales_page = SalesPage(context.driver)
    
    sales_page.customers_button.click()
    logger.debug("Customers button clicked, waiting for page load")
    
    # Title verification
    expected_title = "Customers - Odoo"
    actual_title = context.driver.title
    
    logger.debug(f"Expected title: {expected_title}")
    logger.debug(f"Actual title: {actual_title}")
    
    assert actual_title == expected_title, \
        f"The title is not same as the expected! Expected: '{expected_title}', Actual: '{actual_title}'"
    
    logger.info("Customers page title verified successfully")


@when('User can create the customer')
def user_can_create_customer(context):
    """
    Create a new customer with name, address, state, and country information.

    Corresponds to Java method: user_can_create_the_customer() (line 40)
    Original Java: Multiple clicks and sendKeys with hardcoded data (lines 44-51)

    Args:
        context: Behave context object containing driver instance

    Behavior:
        1. Click create button to open customer creation form
        2. Fill customer name: "Lucas"
        3. Fill address: "1 boulevard auguste rodin 75000"
        4. Open state options dropdown
        5. Click "Create and Edit" for state
        6. Enter state name: "Albania"
        7. Enter state code: "78"
        8. Click country state button
        9. Select country from dropdown

    Technical Debt:
        - Uses hardcoded customer data matching Java implementation for behavioral equivalence
        - Future enhancement: Integrate Faker library for dynamic test data generation
        - Future enhancement: Parameterize customer data via scenario outline examples

    Migration Notes:
        - Removed InterruptedException declaration
        - Removed explicit WebDriverWait - handled by SalesPage property-based locators
        - Maintained hardcoded data values to preserve behavioral equivalence with Java
    """
    logger.info("Step: User can create the customer")
    sales_page = SalesPage(context.driver)
    
    # Open customer creation form
    sales_page.create_button.click()
    logger.debug("Create button clicked")
    
    # Fill customer name
    customer_name = "Lucas"
    sales_page.customer_name.send_keys(customer_name)
    logger.debug(f"Customer name entered: {customer_name}")
    
    # Fill customer address
    customer_address = "1 boulevard auguste rodin 75000"
    sales_page.address.send_keys(customer_address)
    logger.debug(f"Customer address entered: {customer_address}")
    
    # Configure state information
    sales_page.state_options.click()
    logger.debug("State options dropdown opened")
    
    sales_page.create_and_edit_state.click()
    logger.debug("Create and Edit state option selected")
    
    # Enter state details
    state_name = "Albania"
    sales_page.state_name.send_keys(state_name)
    logger.debug(f"State name entered: {state_name}")
    
    state_code = "78"
    sales_page.state_code.send_keys(state_code)
    logger.debug(f"State code entered: {state_code}")
    
    # Select country
    sales_page.country_state_button.click()
    logger.debug("Country state button clicked")
    
    sales_page.country_selection.click()
    logger.debug("Country selected from dropdown")
    
    logger.info("Customer creation form completed")


@when('User can save the customer')
def user_can_save_customer(context):
    """
    Save customer information and return to customers list view.

    Corresponds to Java method: user_can_save_the_customer() (line 54)
    Original Java: Multiple clicks with WebDriverWait (lines 56-61)

    Args:
        context: Behave context object containing driver instance

    Behavior:
        1. Click save button to save state/country information
        2. Wait for save button visibility
        3. Click create customer button to finalize customer creation
        4. Wait for create customer button visibility
        5. Click customers button to return to customer list
        6. Wait for customers button visibility

    Migration Notes:
        - Removed explicit WebDriverWait - handled by SalesPage property-based locators
        - Each property access includes implicit wait via BasePage.wait_for_clickable()
        - Behavior preserved from Java implementation
    """
    logger.info("Step: User can save the customer")
    sales_page = SalesPage(context.driver)
    
    # Save state/country information
    sales_page.save_button.click()
    logger.debug("Save button clicked for state/country data")
    
    # Create customer
    sales_page.create_customer.click()
    logger.debug("Create customer button clicked")
    
    # Return to customers list
    sales_page.customers_button.click()
    logger.debug("Navigated back to customers list")
    
    logger.info("Customer saved successfully")


@then('User can find his name "{name}" from search bar')
def user_can_find_name_from_search_bar(context, name):
    """
    Search for customer by name using search bar with keyboard Enter key.

    Corresponds to Java method: userCanFindHisNameFromSearchBar(String name) (line 66)
    Original Java: salesp.searchBar.sendKeys(name + Keys.ENTER); System.out.println only (no assertion)

    Args:
        context: Behave context object containing driver instance
        name (str): Customer name to search for (parameterized from Gherkin scenario)

    Behavior:
        1. Enter customer name in search bar
        2. Press ENTER key to execute search (keyboard interaction)
        3. Wait for search results to load
        4. Verify displayed customer name matches expected name

    Assertions:
        - Displayed customer name (from name_check element) must equal search name parameter
        - Added assertion missing from Java implementation (Java only printed values)

    Migration Notes:
        - Implemented Keys.ENTER keyboard interaction (from selenium.webdriver.common.keys)
        - Replaced System.out.println (lines 74-75) with logger.debug()
        - CRITICAL FIX: Added missing assertion (Java code printed actualName and expectedName
          but never asserted equality - lines 74-77 had no assertion)
        - Corrected logic: Assert that name_check.text equals the parameterized name argument
    """
    logger.info(f"Step: User can find his name '{name}' from search bar")
    sales_page = SalesPage(context.driver)
    
    # Perform search with keyboard ENTER key
    sales_page.search_bar.send_keys(name + Keys.ENTER)
    logger.debug(f"Search executed for customer name: {name}")
    
    # Retrieve displayed customer name from search results
    displayed_name = sales_page.name_check.text
    
    logger.debug(f"Expected name: {name}")
    logger.debug(f"Displayed name: {displayed_name}")
    
    # ASSERTION ADDED: Java code only printed values without asserting (critical bug fix)
    assert displayed_name == name, \
        f"Customer name mismatch! Expected: '{name}', but found: '{displayed_name}'"
    
    logger.info(f"Customer name '{name}' verified successfully in search results")


@step('User can create new customer')
def user_can_create_new_customer(context):
    """
    Initiate customer creation workflow by clicking create and create customer buttons.

    Corresponds to Java method: userCanCreateNewCustomer() (line 80)
    Original Java: salesp.createButton.click(); wait; salesp.createCustomer.click()
    Annotation: @And decorator (mapped to @step in Python Behave for flexibility)

    Args:
        context: Behave context object containing driver instance

    Behavior:
        1. Click create button to open customer creation form
        2. Wait for create button visibility
        3. Click create customer button (without filling any fields)
        4. This step is used to test validation error scenarios

    Usage Context:
        This step is typically used in negative test scenarios where customer is created
        without required fields to trigger validation errors (see userCanGetTheError step).

    Migration Notes:
        - Removed InterruptedException declaration
        - Removed explicit WebDriverWait - handled by SalesPage property-based locators
        - Mapped Java @And to Python @step for decorator flexibility
    """
    logger.info("Step: User can create new customer (validation test)")
    sales_page = SalesPage(context.driver)
    
    # Open customer creation form
    sales_page.create_button.click()
    logger.debug("Create button clicked to open customer form")
    
    # Attempt to create customer without filling required fields
    sales_page.create_customer.click()
    logger.debug("Create customer button clicked without filling fields (testing validation)")
    
    logger.info("Customer creation attempted without required fields")


@then('User can get the error')
def user_can_get_error(context):
    """
    Verify validation error message is displayed for incomplete customer data.

    Corresponds to Java method: userCanGetTheError() (line 87)
    Original Java: System.out.println only - no assertion (lines 93-94)

    Args:
        context: Behave context object containing driver instance

    Behavior:
        1. Wait for warning notification to appear
        2. Retrieve warning message text
        3. Verify warning contains expected validation error text

    Assertions:
        - Warning text must contain "The following fields are invalid:"
        - Added assertion missing from Java implementation

    Migration Notes:
        - Replaced System.out.println (lines 93-94) with logger.debug()
        - CRITICAL FIX: Added missing assertion (Java code only printed actualWarning and
          expectedWarning but never validated - lines 88-95 had no assertion)
        - Used 'in' comparison (substring match) instead of exact equality for robustness
          since full warning message may include dynamic field names
    """
    logger.info("Step: User can get the error (validation error verification)")
    sales_page = SalesPage(context.driver)
    
    # Retrieve validation error message from warning notification
    expected_warning_text = "The following fields are invalid:"
    actual_warning = sales_page.warning.text
    
    logger.debug(f"Expected warning text: {expected_warning_text}")
    logger.debug(f"Actual warning: {actual_warning}")
    
    # ASSERTION ADDED: Java code only printed values without asserting (critical bug fix)
    # Using 'in' for substring match since full message may contain additional field details
    assert expected_warning_text in actual_warning, \
        f"Validation error not found! Expected text containing: '{expected_warning_text}', " \
        f"but got: '{actual_warning}'"
    
    logger.info("Validation error message verified successfully")


