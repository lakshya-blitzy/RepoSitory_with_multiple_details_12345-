"""
Behave Environment Configuration Module

This module implements Behave lifecycle hooks for test environment setup and teardown.
Converted from Java Cucumber Hooks.java (@After annotation) to Python Behave pattern
with enhanced features including comprehensive null safety, Allure integration, and
proper lifecycle management.

Original Java Source: src/main/java/com/testinium/step_definitions/Hooks.java
Migration: Java Selenium + Cucumber → Python Selenium + Behave

Lifecycle Hooks Implemented:
- before_all: Global configuration initialization (runs once before all features)
- after_all: Global cleanup (runs once after all features)
- before_scenario: Per-scenario WebDriver initialization (runs before each scenario)
- after_scenario: Per-scenario cleanup with screenshot capture (runs after each scenario)

Critical Enhancements from Java Version:
1. NULL SAFETY: Added defensive checks before driver operations (fixes unguarded
   Driver.getDriver() calls in original Java implementation lines 14, 17)
2. THREAD SAFETY: WebDriver managed via threading.local() through DriverManager
3. ALLURE INTEGRATION: Optional Allure reporting support for enhanced observability
4. COMPREHENSIVE LOGGING: Detailed lifecycle event logging for debugging
5. ERROR HANDLING: Graceful degradation and proper exception handling
6. PARALLEL EXECUTION: Compatible with behave-parallel and pytest-xdist

Example Test Execution Flow:
    1. before_all: Initialize ConfigReader → context.config_reader
    2. before_scenario: Initialize WebDriver → context.driver
    3. [Test scenario steps execute]
    4. after_scenario: Capture screenshot (if failed), quit driver
    5. [Repeat steps 2-4 for each scenario]
    6. after_all: Final cleanup

Usage:
    Behave automatically discovers and executes hooks in features/environment.py.
    No explicit imports needed in step definitions - just use context.driver.

    Example in step definition:
        >>> from behave import given
        >>> @given('User is on the login page')
        >>> def navigate_to_login(context):
        >>>     context.driver.get("https://example.com/login")
"""

import os
import logging
from typing import Optional

# Behave framework imports
from behave import fixture, use_fixture
from behave.runner import Context

# Internal utility imports (from depends_on_files)
from utilities.driver_manager import DriverManager
from utilities.config_reader import ConfigReader
from utilities.screenshot_helper import capture_screenshot

# Optional Allure integration for enhanced reporting
try:
    from allure_commons.types import AttachmentType
    import allure
    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False
    AttachmentType = None
    allure = None


# Configure module logger
logger = logging.getLogger(__name__)


# ============================================================================
# GLOBAL LIFECYCLE HOOKS (before_all / after_all)
# ============================================================================

def before_all(context: Context) -> None:
    """
    Global setup hook executed once before all test features.

    This hook runs before any feature file execution and performs one-time
    initialization of shared resources. Replaces suite-level setup that
    would be in Java @BeforeClass or test runner configuration.

    Responsibilities:
    1. Initialize ConfigReader singleton for configuration access
    2. Ensure reports/screenshots/ directory exists
    3. Configure logging for test execution
    4. Store configuration in context for scenario access

    Context Attributes Set:
    - context.config_reader: ConfigReader singleton instance
        Used to access configuration throughout test execution:
        >>> browser_type = context.config_reader.get_property('browser.type')

    Args:
        context: Behave context object shared across all scenarios

    Thread Safety:
        This hook runs in the main thread before any parallel execution begins.
        ConfigReader singleton initialization is safe here.

    Example:
        Behave automatically calls this hook before test execution:
        $ behave features/
        [before_all executes]
        [Feature 1 executes]
        [Feature 2 executes]
        [after_all executes]
    """
    logger.info("=" * 80)
    logger.info("BEHAVE TEST SUITE INITIALIZATION - before_all hook")
    logger.info("=" * 80)

    try:
        # Initialize ConfigReader singleton
        # This loads config/config.yaml and .env file for configuration access
        logger.info("Initializing ConfigReader singleton...")
        context.config_reader = ConfigReader()
        logger.info("ConfigReader initialized successfully: %s", context.config_reader)

        # Ensure reports directory structure exists
        # Creates reports/screenshots/ for screenshot storage
        reports_dir = os.path.join("reports", "screenshots")
        os.makedirs(reports_dir, exist_ok=True)
        logger.info("Reports directory ensured: %s", os.path.abspath(reports_dir))

        # Log configuration for debugging
        all_config = context.config_reader.get_all_properties()
        logger.info("Loaded configuration with %d top-level keys: %s",
                   len(all_config), list(all_config.keys()))

        # Optional: Log Allure integration status
        if ALLURE_AVAILABLE:
            logger.info("Allure reporting integration: ENABLED")
        else:
            logger.debug("Allure reporting integration: DISABLED (allure-behave not installed)")

        logger.info("Test suite initialization complete")
        logger.info("=" * 80)

    except Exception as e:
        logger.exception("CRITICAL: Failed to initialize test suite in before_all: %s", e)
        raise RuntimeError(f"Test suite initialization failed: {e}") from e


def after_all(context: Context) -> None:
    """
    Global teardown hook executed once after all test features.

    This hook runs after all feature file execution completes and performs
    final cleanup of shared resources. Replaces suite-level teardown that
    would be in Java @AfterClass or test runner configuration.

    Responsibilities:
    1. Log test execution summary
    2. Perform any final cleanup operations
    3. Ensure all resources are properly released

    Args:
        context: Behave context object shared across all scenarios

    Thread Safety:
        This hook runs in the main thread after all parallel execution completes.
        All scenario-level WebDriver instances should already be quit by after_scenario.

    Example:
        Behave automatically calls this hook after test execution:
        $ behave features/
        [before_all executes]
        [All features execute]
        [after_all executes]
    """
    logger.info("=" * 80)
    logger.info("BEHAVE TEST SUITE TEARDOWN - after_all hook")
    logger.info("=" * 80)

    try:
        # Log test execution summary
        logger.info("Test suite execution completed")

        # Defensive cleanup: Ensure no lingering WebDriver instances
        # This should not be necessary if after_scenario works correctly,
        # but provides safety net for edge cases
        try:
            logger.debug("Performing final WebDriver cleanup check...")
            DriverManager.quit_driver()
            logger.debug("Final WebDriver cleanup complete")
        except Exception as cleanup_error:
            logger.warning("Non-critical error during final cleanup: %s", cleanup_error)

        logger.info("Test suite teardown complete")
        logger.info("=" * 80)

    except Exception as e:
        logger.error("Error during test suite teardown in after_all: %s", e, exc_info=True)
        # Don't raise exception in teardown to allow test results to be reported


# ============================================================================
# SCENARIO LIFECYCLE HOOKS (before_scenario / after_scenario)
# ============================================================================

def before_scenario(context: Context, scenario) -> None:
    """
    Per-scenario setup hook executed before each test scenario.

    This hook runs before every test scenario (including scenario outlines)
    and initializes a fresh WebDriver instance for test isolation. Ensures
    each test starts with a clean browser state.

    Responsibilities:
    1. Initialize thread-local WebDriver via DriverManager.get_driver()
    2. Store WebDriver reference in context.driver for scenario access
    3. Log scenario start with name and tags
    4. Provide clean browser state for each test

    Context Attributes Set:
    - context.driver: Selenium WebDriver instance (thread-safe)
        Used in step definitions to interact with browser:
        >>> context.driver.get("https://example.com")
        >>> element = context.driver.find_element(By.ID, "login")

    Args:
        context: Behave context object for this scenario
        scenario: Behave Scenario object with name, tags, status

    Thread Safety:
        DriverManager uses threading.local() to provide isolated WebDriver
        instances per thread, supporting parallel test execution via
        behave-parallel or pytest-xdist.

    Critical Enhancement from Java:
        Original Java Hooks.java had no @Before hook - driver initialization
        was implicit on first Driver.getDriver() call. This explicit hook
        provides better control and logging of driver lifecycle.

    Example:
        Given a scenario in Login.feature:
        ```gherkin
        @Login @Smoke
        Scenario: Valid login
            Given User is on the login page
            [before_scenario initializes context.driver]
            [Step definitions use context.driver]
        ```
    """
    logger.info("-" * 80)
    logger.info("SCENARIO START: %s", scenario.name)
    logger.info("Tags: %s", scenario.tags if scenario.tags else "No tags")
    logger.info("-" * 80)

    try:
        # Initialize WebDriver for this scenario via DriverManager
        # Uses threading.local() for thread safety in parallel execution
        logger.debug("Initializing WebDriver for scenario: %s", scenario.name)

        # CRITICAL: Use DriverManager.get_driver() for lazy initialization
        # This replaces Java's Driver.getDriver() with thread-safe implementation
        context.driver = DriverManager.get_driver()

        logger.info("WebDriver initialized successfully for scenario: %s", scenario.name)

        # Log driver details for debugging
        try:
            browser_name = context.driver.capabilities.get('browserName', 'unknown')
            browser_version = context.driver.capabilities.get('browserVersion', 'unknown')
            session_id = context.driver.session_id
            logger.debug("Browser: %s %s, Session: %s",
                        browser_name, browser_version, session_id)
        except Exception as details_error:
            logger.debug("Could not retrieve driver details: %s", details_error)

    except Exception as e:
        logger.exception("CRITICAL: Failed to initialize WebDriver in before_scenario: %s", e)
        raise RuntimeError(f"WebDriver initialization failed for scenario '{scenario.name}': {e}") from e


def after_scenario(context: Context, scenario) -> None:
    """
    Per-scenario teardown hook executed after each test scenario.

    This hook runs after every test scenario (including scenario outlines)
    and performs cleanup operations including screenshot capture for failed
    tests and WebDriver termination. Converted from Java Hooks.java @After
    annotation with enhanced null safety and error handling.

    Original Java Implementation (Hooks.java lines 11-18):
    ```java
    @After
    public void teardownScenario(Scenario scenario){
        if(scenario.isFailed()){
            byte [] screenshot = ((TakesScreenshot) Driver.getDriver())
                                .getScreenshotAs(OutputType.BYTES);
            scenario.attach(screenshot, "image/png", scenario.getName());
        }
        Driver.closeDriver();
    }
    ```

    Critical Enhancements from Java Version:
    1. NULL SAFETY: Defensive check for context.driver before operations
       (Java code had unguarded Driver.getDriver() calls on lines 14, 17)
    2. THREAD SAFETY: Uses DriverManager.quit_driver() with threading.local()
    3. ALLURE INTEGRATION: Optional attachment of screenshots to Allure reports
    4. FILE SYSTEM STORAGE: Screenshots saved to reports/screenshots/ directory
    5. COMPREHENSIVE LOGGING: Detailed scenario execution logging
    6. ERROR HANDLING: Graceful degradation on screenshot capture failures

    Responsibilities:
    1. Check scenario.status for failure detection
    2. Capture screenshot if scenario failed (with null safety)
    3. Quit WebDriver and cleanup browser process
    4. Log scenario execution results
    5. Optional: Attach screenshot to Allure report

    Args:
        context: Behave context object for this scenario
        scenario: Behave Scenario object with name, tags, status

    Thread Safety:
        DriverManager.quit_driver() safely removes thread-local WebDriver
        reference without affecting other threads in parallel execution.

    Idempotent:
        Safe to call even if driver initialization failed in before_scenario.
        Null checks ensure no errors from missing driver.

    Example:
        After a scenario completes:
        ```gherkin
        Scenario: Invalid login
            When User enters invalid credentials
            Then Error message should be displayed
            [Scenario fails - status = 'failed']
            [after_scenario captures screenshot]
            [after_scenario quits driver]
        ```
    """
    logger.info("-" * 80)
    logger.info("SCENARIO END: %s", scenario.name)
    logger.info("Status: %s", scenario.status)
    logger.info("-" * 80)

    # ========================================================================
    # SCREENSHOT CAPTURE ON FAILURE
    # ========================================================================

    # Check if scenario failed and WebDriver exists
    # CRITICAL NULL SAFETY: Check context.driver is not None before operations
    # This fixes unguarded Driver.getDriver() in original Java Hooks.java
    if scenario.status == 'failed':
        logger.warning("Scenario FAILED: %s", scenario.name)

        # Defensive check: Ensure driver exists before screenshot capture
        # Original Java code on line 14 did not check if driver was null
        if hasattr(context, 'driver') and context.driver is not None:
            logger.info("Capturing failure screenshot for scenario: %s", scenario.name)

            try:
                # Use screenshot_helper for comprehensive screenshot capture
                # This replaces Java's inline screenshot code with reusable function
                screenshot_path = capture_screenshot(
                    driver=context.driver,
                    scenario_name=scenario.name,
                    attach_to_allure=ALLURE_AVAILABLE
                )

                if screenshot_path:
                    logger.info("Screenshot saved successfully: %s", screenshot_path)

                    # Additional Behave-specific screenshot attachment
                    # This mimics Java's scenario.attach() from line 15
                    try:
                        screenshot_bytes = context.driver.get_screenshot_as_png()
                        scenario.attach(
                            data=screenshot_bytes,
                            mime_type='image/png',
                            name=scenario.name
                        )
                        logger.debug("Screenshot attached to Behave scenario report")
                    except Exception as attach_error:
                        logger.warning(
                            "Failed to attach screenshot to Behave report: %s",
                            attach_error
                        )

                else:
                    logger.error("Screenshot capture returned None for scenario: %s", scenario.name)

            except Exception as screenshot_error:
                # Log error but don't fail teardown due to screenshot issues
                logger.error(
                    "Failed to capture screenshot for failed scenario '%s': %s",
                    scenario.name,
                    screenshot_error,
                    exc_info=True
                )
        else:
            # Scenario failed but no driver available
            logger.warning(
                "Cannot capture screenshot for failed scenario '%s': "
                "WebDriver not initialized (driver is None or missing)",
                scenario.name
            )
            logger.warning(
                "This may indicate driver initialization failed in before_scenario"
            )

    else:
        # Scenario passed or skipped
        logger.info("Scenario completed with status: %s", scenario.status)

    # ========================================================================
    # WEBDRIVER CLEANUP
    # ========================================================================

    # Quit WebDriver and cleanup browser process
    # CRITICAL NULL SAFETY: Check driver exists before quit operation
    # Original Java code on line 17 did not check if driver was null
    if hasattr(context, 'driver') and context.driver is not None:
        logger.debug("Quitting WebDriver for scenario: %s", scenario.name)

        try:
            # Use DriverManager.quit_driver() for proper cleanup
            # This replaces Java's Driver.closeDriver() with thread-safe implementation
            # Handles both driver.quit() and thread-local reference removal
            DriverManager.quit_driver()
            logger.info("WebDriver quit successfully for scenario: %s", scenario.name)

        except Exception as quit_error:
            # Log error but don't raise exception in teardown
            # Ensures cleanup continues even if quit fails
            logger.error(
                "Error quitting WebDriver for scenario '%s': %s",
                scenario.name,
                quit_error,
                exc_info=True
            )

        finally:
            # Ensure context.driver reference is cleared
            # Prevents stale driver reference on next scenario
            context.driver = None
            logger.debug("Cleared context.driver reference")

    else:
        # No driver to quit (may have failed to initialize)
        logger.debug(
            "No WebDriver to quit for scenario '%s' "
            "(driver is None or not initialized)",
            scenario.name
        )

    logger.info("Scenario teardown complete: %s", scenario.name)
    logger.info("=" * 80 + "\n")


# ============================================================================
# OPTIONAL: FIXTURE PATTERN FOR ADVANCED SCENARIOS
# ============================================================================

@fixture
def browser_fixture(context: Context):
    """
    Optional fixture for advanced WebDriver lifecycle management.

    This fixture provides an alternative pattern to before_scenario/after_scenario
    hooks using Behave's fixture system. Useful for feature-level or step-level
    driver scoping instead of scenario-level.

    Not used by default in this migration (scenario-level hooks are primary pattern),
    but provided as reference for advanced use cases.

    Usage:
        In environment.py before_feature:
        >>> def before_feature(context, feature):
        >>>     use_fixture(browser_fixture, context)

    Yields:
        WebDriver: Initialized WebDriver instance

    Cleanup:
        Automatically quits driver after fixture scope ends
    """
    logger.debug("Browser fixture: Initializing WebDriver")

    try:
        # Initialize driver
        context.driver = DriverManager.get_driver()
        logger.debug("Browser fixture: WebDriver initialized")

        # Yield control back to test execution
        yield context.driver

    finally:
        # Cleanup after fixture scope ends
        logger.debug("Browser fixture: Cleaning up WebDriver")
        if hasattr(context, 'driver') and context.driver is not None:
            DriverManager.quit_driver()
            context.driver = None
        logger.debug("Browser fixture: Cleanup complete")


# ============================================================================
# MODULE INITIALIZATION LOGGING
# ============================================================================

logger.debug(
    "Behave environment.py loaded successfully "
    "(Allure integration: %s)",
    "ENABLED" if ALLURE_AVAILABLE else "DISABLED"
)
