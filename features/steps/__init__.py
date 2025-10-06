"""
Step Definitions Package for Testinium QA Behave Test Framework.

This package contains all step definition modules that implement the Gherkin
scenarios defined in the feature files. Step definitions map Given/When/Then
statements to Python code that interacts with the application under test.

Package Structure:
-----------------
- calendar_steps.py    : Step definitions for Calendar feature scenarios
- contacts_steps.py    : Step definitions for Contacts feature scenarios
- crm_steps.py         : Step definitions for CRM feature scenarios
- employee_steps.py    : Step definitions for Employee feature scenarios
- inventory_steps.py   : Step definitions for Inventory feature scenarios
- login_steps.py       : Step definitions for Login feature scenarios
- logout_steps.py      : Step definitions for Logout feature scenarios
- notes_steps.py       : Step definitions for Notes feature scenarios
- sales_steps.py       : Step definitions for Sales feature scenarios
- session_steps.py     : Step definitions for Session feature scenarios

Behave Framework Auto-Discovery:
--------------------------------
This __init__.py file marks the directory as a Python package, enabling the
Behave framework to automatically discover and load all step definition
functions decorated with @given, @when, and @then from modules in this package.

No explicit imports are required in this file - Behave scans all Python files
in the steps/ directory and registers decorated functions as step definitions.

Migration Notes:
---------------
This file replaces the Java package declaration 'package com.testinium.step_definitions;'
used in the original Cucumber Java framework. Python uses file-based package structure
instead of explicit package declarations.

Converted from: src/main/java/com/testinium/step_definitions/
Framework: Cucumber Java 7.2.3 → Behave Python 1.2.6+
"""
