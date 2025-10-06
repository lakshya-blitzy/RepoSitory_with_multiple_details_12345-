"""
Screenshot capture utility module for test failure diagnostics.

This module extracts screenshot capture logic from the original Java Hooks.java
@After annotation into a dedicated Python helper, providing reusable functions
for screenshot capture, browser log collection, and filename sanitization.

Key Features:
- Automatic timestamp generation for unique filenames
- Cross-platform filename sanitization
- File system storage to reports/screenshots/ directory
- Optional Allure report integration
- Browser console log capture for comprehensive diagnostics
- Comprehensive error handling and logging

Original Java Source: src/main/java/com/testinium/step_definitions/Hooks.java
Migration: Java Selenium + Cucumber → Python Selenium + Behave
"""

import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

# Selenium WebDriver type import for type hints
try:
    from selenium.webdriver.remote.webdriver import WebDriver
except ImportError:
    # Fallback for type hints if selenium not installed
    WebDriver = None

# Allure integration (optional dependency)
try:
    from allure_commons.types import AttachmentType
    import allure
    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False
    AttachmentType = None

# Configure module logger
logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing or replacing invalid filesystem characters.

    Removes characters that are invalid in filenames across Windows, Linux, and macOS:
    - Forward slashes (/)
    - Backslashes (\\)
    - Colons (:)
    - Asterisks (*)
    - Question marks (?)
    - Double quotes (")
    - Less than (<)
    - Greater than (>)
    - Pipe (|)

    Also replaces spaces with underscores for better compatibility.

    Args:
        filename: Original filename string to sanitize

    Returns:
        Sanitized filename safe for cross-platform filesystem operations

    Example:
        >>> sanitize_filename("User login: admin@example.com")
        'User_login_admin_example_com'
    """
    # Pattern to match invalid filesystem characters
    invalid_chars_pattern = re.compile(r'[<>:"/\\|?*]')

    # Remove invalid characters
    sanitized = invalid_chars_pattern.sub('_', filename)

    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')

    # Remove leading/trailing underscores and dots
    sanitized = sanitized.strip('_.')

    # Ensure filename is not empty after sanitization
    if not sanitized:
        sanitized = 'screenshot'

    # Limit filename length to 200 characters (leaving room for timestamp and extension)
    if len(sanitized) > 200:
        sanitized = sanitized[:200]

    logger.debug("Sanitized filename: '%s' -> '%s'", filename, sanitized)
    return sanitized


def capture_screenshot(driver: WebDriver, scenario_name: str,
                      attach_to_allure: bool = True) -> Optional[str]:
    """
    Capture screenshot from WebDriver instance and save to filesystem.

    This function extracts the screenshot capture logic from the original Java
    Hooks.java @After method, providing a reusable implementation with enhanced
    features including timestamp generation, filename sanitization, and optional
    Allure report integration.

    Original Java Implementation (Hooks.java lines 14-15):
    Original Java Implementation (Hooks.java lines 14-15):
        byte[] screenshot = ((TakesScreenshot) Driver.getDriver())
                           .getScreenshotAs(OutputType.BYTES);
        scenario.attach(screenshot, "image/png", scenario.getName());

    Python Enhancement:
    - File system storage in addition to report attachment
    - Automatic timestamp generation for unique filenames
    - Cross-platform filename sanitization
    - Comprehensive error handling and logging
    - Optional Allure report integration

    Args:
        driver: Selenium WebDriver instance for screenshot capture
        scenario_name: Name of the test scenario (used in filename)
        attach_to_allure: Whether to attach screenshot to Allure report (default: True)

    Returns:
        Absolute path to saved screenshot file on success, None on failure

    Raises:
        Does not raise exceptions - logs errors and returns None on failure

    Example:
        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> screenshot_path = capture_screenshot(driver, "Login Test Failed")
        >>> print(screenshot_path)
        '/path/to/reports/screenshots/Login_Test_Failed_20240115_143022.png'
    """
    if driver is None:
        logger.error("Cannot capture screenshot: WebDriver instance is None")
        return None

    try:
        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Sanitize scenario name for filesystem compatibility
        sanitized_name = sanitize_filename(scenario_name)

        # Construct filename with format: scenario_name_YYYYMMDD_HHMMSS.png
        screenshot_filename = f"{sanitized_name}_{timestamp}.png"

        # Define screenshot directory path
        screenshot_dir = Path("reports") / "screenshots"

        # Ensure screenshot directory exists (create if necessary)
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("Screenshot directory ensured: %s", screenshot_dir.resolve())

        # Construct full screenshot file path
        screenshot_path = screenshot_dir / screenshot_filename

        # Capture and save screenshot using WebDriver
        driver.save_screenshot(str(screenshot_path))

        # Log successful screenshot capture
        logger.info("Screenshot captured successfully: %s", screenshot_path.resolve())

        # Optional: Attach screenshot to Allure report
        if attach_to_allure and ALLURE_AVAILABLE:
            try:
                screenshot_bytes = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot_bytes,
                    name=sanitized_name,
                    attachment_type=AttachmentType.PNG
                )
                logger.debug("Screenshot attached to Allure report: %s", sanitized_name)
            except Exception as allure_error:
                logger.warning(
                    "Failed to attach screenshot to Allure report: %s",
                    allure_error, exc_info=True
                )
        elif attach_to_allure and not ALLURE_AVAILABLE:
            logger.debug("Allure integration requested but allure-behave not installed")

        # Return absolute path to screenshot file
        return str(screenshot_path.resolve())

    except Exception as e:
        logger.exception("Failed to capture screenshot for scenario '%s': %s", scenario_name, e)
        return None


def capture_browser_logs(driver: WebDriver, scenario_name: str,
                        log_types: Optional[List[str]] = None) -> Optional[Dict[str, List[str]]]:
    """
    Capture browser console logs for comprehensive failure diagnostics.

    This function provides enhanced debugging capabilities beyond the original Java
    implementation by capturing browser console logs (JavaScript errors, warnings,
    network issues) that can help diagnose test failures.

    Enhancement over Java Implementation:
    - Captures multiple log types (browser, driver, performance)
    - Saves logs to filesystem for persistent analysis
    - Provides structured log data for programmatic processing
    - Integrates with Allure reporting for log visualization

    Args:
        driver: Selenium WebDriver instance for log retrieval
        scenario_name: Name of the test scenario (used in log filename)
        log_types: List of log types to capture (default: ['browser'])
                  Valid types: 'browser', 'driver', 'client', 'server', 'performance'

    Returns:
        Dictionary mapping log type to list of log entry strings on success,
        None on failure

    Example:
        >>> logs = capture_browser_logs(driver, "Login Test Failed")
        >>> if logs:
        ...     print(logs['browser'])
        ['SEVERE: Uncaught TypeError: Cannot read property...']
    """
    if driver is None:
        logger.error("Cannot capture browser logs: WebDriver instance is None")
        return None

    # Default to capturing browser console logs
    if log_types is None:
        log_types = ['browser']

    captured_logs = {}

    try:
        # Get available log types from driver
        try:
            available_log_types = driver.log_types
            logger.debug("Available log types: %s", available_log_types)
        except Exception as log_types_error:
            logger.warning("Could not retrieve available log types: %s", log_types_error)
            available_log_types = ['browser']  # Fallback to browser logs

        # Capture each requested log type
        for log_type in log_types:
            if log_type not in available_log_types:
                logger.warning("Log type '%s' not available, skipping", log_type)
                continue

            try:
                logs = driver.get_log(log_type)
                log_messages = [
                    f"[{log_entry.get('level', 'INFO')}] {log_entry.get('message', '')}"
                    for log_entry in logs
                ]
                captured_logs[log_type] = log_messages
                logger.debug("Captured %d log entries for type '%s'", len(log_messages), log_type)
            except Exception as log_capture_error:
                logger.warning(
                    "Failed to capture '%s' logs: %s",
                    log_type, log_capture_error, exc_info=True
                )

        # If logs were captured, save to filesystem
        if captured_logs:
            # Generate timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Sanitize scenario name
            sanitized_name = sanitize_filename(scenario_name)

            # Define logs directory
            logs_dir = Path("reports") / "screenshots"  # Store with screenshots for consistency
            logs_dir.mkdir(parents=True, exist_ok=True)

            # Construct log filename
            log_filename = f"{sanitized_name}_{timestamp}_logs.txt"
            log_path = logs_dir / log_filename

            # Write logs to file
            try:
                with open(log_path, 'w', encoding='utf-8') as log_file:
                    log_file.write(f"Browser Logs for Scenario: {scenario_name}\n")
                    log_file.write(f"Captured at: {datetime.now().isoformat()}\n")
                    log_file.write("=" * 80 + "\n\n")

                    for log_type, messages in captured_logs.items():
                        log_file.write(f"[{log_type.upper()} LOGS]\n")
                        log_file.write("-" * 80 + "\n")
                        for message in messages:
                            log_file.write(f"{message}\n")
                        log_file.write("\n")

                logger.info("Browser logs saved to: %s", log_path.resolve())

                # Optional: Attach logs to Allure report
                if ALLURE_AVAILABLE:
                    try:
                        with open(log_path, 'r', encoding='utf-8') as log_file:
                            log_content = log_file.read()
                        allure.attach(
                            log_content,
                            name=f"{sanitized_name}_browser_logs",
                            attachment_type=AttachmentType.TEXT
                        )
                        logger.debug("Browser logs attached to Allure report")
                    except Exception as allure_error:
                        logger.warning(
                            "Failed to attach logs to Allure: %s",
                            allure_error, exc_info=True
                        )

            except Exception as file_error:
                logger.error("Failed to save browser logs to file: %s", file_error, exc_info=True)

        return captured_logs if captured_logs else None

    except Exception as e:
        logger.exception("Failed to capture browser logs for scenario '%s': %s", scenario_name, e)
        return None


# Module-level convenience function for quick screenshot capture
def take_screenshot(driver: WebDriver, name: str = "screenshot") -> Optional[str]:
    """
    Convenience wrapper for capture_screenshot with simpler interface.

    Args:
        driver: Selenium WebDriver instance
        name: Simple name for the screenshot (default: "screenshot")

    Returns:
        Path to saved screenshot or None on failure
    """
    return capture_screenshot(driver, name, attach_to_allure=False)


# Module initialization logging
logger.debug("Screenshot helper module initialized (Allure available: %s)", ALLURE_AVAILABLE)
