"""
Pages Package - Page Object Model Implementation.

This package contains all Page Object Model (POM) classes for the Testinium
test automation framework migrated from Java/Selenium/Cucumber to Python/Selenium/Behave.

The package provides convenient access to all page objects through package-level imports,
enabling clean import statements throughout the test framework:

    from pages import LoginPage, CalendarPage
    from pages.login_page import LoginPage  # Also supported

Package Structure:
    - BasePage: Abstract base class providing common WebDriver utilities, wait helpers,
                and element interaction methods for all page objects
    - LoginPage: User authentication page object
    - LogoutPage: User session termination page object
    - CalendarPage: Calendar and meeting management page object
    - ContactsPage: Contacts management page object
    - CrmPage: CRM pipeline and opportunity management page object
    - EmployeePage: Employee and HR management page object
    - InventoryPage: Inventory and product management page object
    - NotesPage: Notes management page object
    - SalesPage: Sales and customer management page object
    - SessionPage: Session login management page object

Usage Examples:
    # Convenient package-level import
    from pages import LoginPage, CalendarPage
    
    # Explicit module import
    from pages.login_page import LoginPage
    
    # Import multiple classes
    from pages import (
        BasePage,
        LoginPage,
        LogoutPage,
        CalendarPage,
    )
    
    # Wildcard import (imports all classes in __all__)
    from pages import *

Migration Notes:
    This package replaces the Java com.testinium.pages package structure.
    Java's PageFactory pattern has been replaced with Python property-based
    element locators using explicit waits for improved reliability and
    maintainability.

Author: Blitzy Platform - Test Automation Migration
Version: 1.0.0
"""

# Import BasePage - foundation for all page objects
from pages.base_page import BasePage

# Import all page object classes
from pages.login_page import LoginPage
from pages.logout_page import LogoutPage
from pages.calendar_page import CalendarPage
from pages.contacts_page import ContactsPage
from pages.crm_page import CrmPage
from pages.employee_page import EmployeePage
from pages.inventory_page import InventoryPage
from pages.notes_page import NotesPage
from pages.sales_page import SalesPage
from pages.session_page import SessionPage

# Define public API - controls what's exported with "from pages import *"
__all__ = [
    # Base class
    'BasePage',
    
    # Authentication pages
    'LoginPage',
    'LogoutPage',
    'SessionPage',
    
    # Application module pages
    'CalendarPage',
    'ContactsPage',
    'CrmPage',
    'EmployeePage',
    'InventoryPage',
    'NotesPage',
    'SalesPage',
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'Blitzy Platform - Test Automation Team'
__description__ = 'Page Object Model implementation for Testinium test automation framework'

# Migration tracking
__migration_source__ = 'com.testinium.pages (Java)'
__migration_date__ = '2024'
__framework_stack__ = 'Python 3.9+ | Selenium 4.x | Behave BDD'
