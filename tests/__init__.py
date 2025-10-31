"""
Test Suite for Testinium QA Python Test Automation Framework.

This package contains pytest-based unit tests for the test automation framework
itself, validating utilities, configuration, and driver management components.

Purpose:
    - Validate framework reliability through automated testing
    - Ensure driver manager thread safety and singleton pattern correctness
    - Verify configuration reader handles YAML, environment variables, and errors
    - Test critical bug fixes from Java-to-Python migration (Firefox driver setup)
    - Enable pytest discovery of test modules (test_*.py)
    - Support continuous integration and quality assurance

Test Modules:
    - test_driver_manager.py: Unit tests for WebDriver lifecycle management,
      thread-local isolation, and browser driver initialization
    - test_config.py: Unit tests for YAML configuration parsing, environment
      variable overrides, and error handling

Test Execution:
    Run all tests:
        $ pytest tests/ -v
    
    Run specific test module:
        $ pytest tests/test_driver_manager.py -v
    
    Run with coverage:
        $ pytest tests/ --cov=utilities --cov-report=html
    
    Run specific test:
        $ pytest tests/test_driver_manager.py::TestDriverManager::test_get_driver_firefox -v

Standards:
    - All test functions must start with 'test_' for pytest discovery
    - Use pytest fixtures for setup and teardown
    - Use unittest.mock for isolating external dependencies
    - Validate proper exception handling (no swallowed errors)
    - Test thread safety for parallel execution scenarios

Migration Context:
    This test suite validates the Python implementation against the original
    Java Selenium + Cucumber framework, ensuring behavioral equivalence and
    fixing critical bugs identified in the Java source code:
    - Driver.java line 37: Firefox case incorrectly called chromedriver setup
    - ConfigurationReader.java: IOException swallowed with printStackTrace
    - Security: Hardcoded credentials removed (use environment variables)

References:
    - Agent Action Plan Section 0.4.1: Target Python Project Structure
    - Agent Action Plan Section 0.8.1: Cross-Cutting Concerns Analysis
    - Agent Action Plan Section 0.8.2: Bug Fixes and Security Remediations
"""

__version__ = "1.0.0"
__author__ = "Testinium QA Team"
__package_name__ = "testinium-qa-python-tests"
