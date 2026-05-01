package com.testinium.step_definitions;

import com.testinium.utilities.Driver;
import io.cucumber.java.Scenario;
import org.junit.After;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

/**
 * Cucumber lifecycle hooks class providing test setup and teardown functionality for the test automation framework.
 * 
 * <p>This class implements the {@code @After} hook for post-scenario cleanup operations, ensuring that
 * WebDriver sessions are properly terminated and screenshots are captured on test failures. It is a
 * critical infrastructure class that prevents session leaks, which is especially important in parallel
 * test execution environments where each thread maintains its own WebDriver instance.</p>
 * 
 * <h2>Screenshot Capture Mechanism</h2>
 * <p>When a test scenario fails, this class captures a screenshot using the Selenium 
 * {@link TakesScreenshot} interface. The screenshot is captured as PNG bytes using 
 * {@link OutputType#BYTES} and attached directly to the Cucumber Scenario report. This provides
 * visual evidence of the application state at the point of failure, which is invaluable for
 * debugging and defect analysis.</p>
 * 
 * <h2>WebDriver Lifecycle Management</h2>
 * <p>The hook ensures that {@link Driver#closeDriver()} is called after every scenario, regardless
 * of whether the test passed or failed. This unconditional cleanup is essential for:</p>
 * <ul>
 *   <li>Releasing browser resources and system memory</li>
 *   <li>Preventing zombie browser processes</li>
 *   <li>Removing thread-local WebDriver references to avoid session leaks</li>
 *   <li>Ensuring test isolation in parallel execution scenarios</li>
 * </ul>
 * 
 * <h2>Usage</h2>
 * <p>This class is automatically discovered and executed by Cucumber through the glue path
 * configuration in the test runner. No explicit instantiation is required.</p>
 * 
 * <pre>
 * // Example CukesRunner configuration that includes this hooks class:
 * &#64;CucumberOptions(
 *     glue = "com/testinium/step_definitions",
 *     // ... other options
 * )
 * public class CukesRunner {}
 * </pre>
 * 
 * @see com.testinium.utilities.Driver
 * @see io.cucumber.java.Scenario
 * @see org.openqa.selenium.TakesScreenshot
 * @see org.openqa.selenium.OutputType
 */
public class Hooks {

    /**
     * Cucumber {@code @After} hook executed after each Cucumber scenario completes, regardless of outcome.
     * 
     * <p>This method performs two critical operations:</p>
     * 
     * <p><strong>1. Conditional Screenshot Capture (on failure):</strong>
     * When a scenario fails ({@code scenario.isFailed()} returns {@code true}), this method:</p>
     * <ol>
     *   <li>Retrieves the current WebDriver instance via {@link Driver#getDriver()}</li>
     *   <li>Casts the WebDriver to the {@link TakesScreenshot} interface</li>
     *   <li>Captures a screenshot as PNG bytes using {@link TakesScreenshot#getScreenshotAs(OutputType)}
     *       with {@link OutputType#BYTES}</li>
     *   <li>Attaches the screenshot byte array to the Cucumber Scenario report using
     *       {@link Scenario#attach(byte[], String, String)} with "image/png" MIME type and
     *       the scenario name as the attachment identifier</li>
     * </ol>
     * 
     * <p><strong>2. Unconditional Driver Cleanup:</strong>
     * After processing any screenshot capture, this method always calls {@link Driver#closeDriver()}
     * to clean up the WebDriver session. This cleanup:</p>
     * <ul>
     *   <li>Calls {@code WebDriver.quit()} to close the browser and end the WebDriver session</li>
     *   <li>Removes the thread-local WebDriver reference to prevent memory leaks</li>
     *   <li>Ensures that subsequent scenarios start with a fresh WebDriver instance</li>
     * </ul>
     * 
     * <p>This unconditional cleanup is critical for parallel test execution, where each thread
     * has its own WebDriver instance managed via {@code InheritableThreadLocal}. Without proper
     * cleanup, threads could accumulate stale browser sessions, leading to resource exhaustion
     * and test instability.</p>
     * 
     * <p><strong>Implementation Details:</strong></p>
     * <pre>{@code
     * // Pseudo-code flow:
     * if (scenario.isFailed()) {
     *     TakesScreenshot ts = (TakesScreenshot) Driver.getDriver();
     *     byte[] screenshot = ts.getScreenshotAs(OutputType.BYTES);
     *     scenario.attach(screenshot, "image/png", scenario.getName());
     * }
     * Driver.closeDriver(); // Always executed
     * }</pre>
     * 
     * <p><strong>Note:</strong> This class imports {@code @After} from the {@code org.junit}
     * package (see import statement). Cucumber 7.x also provides {@code io.cucumber.java.After}
     * for Cucumber-native hook semantics; ensure the import in use matches the desired hook
     * behavior for your test framework setup.</p>
     * 
     * @param scenario the Cucumber {@link Scenario} object providing scenario context including:
     *                 <ul>
     *                   <li>Pass/fail status via {@link Scenario#isFailed()}</li>
     *                   <li>Scenario name via {@link Scenario#getName()}</li>
     *                   <li>Attachment capabilities via {@link Scenario#attach(byte[], String, String)}</li>
     *                   <li>Scenario tags, ID, and other metadata</li>
     *                 </ul>
     *                 This parameter is automatically injected by Cucumber at runtime.
     * 
     * @see Driver#closeDriver()
     * @see TakesScreenshot#getScreenshotAs(OutputType)
     * @see Scenario#isFailed()
     * @see Scenario#attach(byte[], String, String)
     */
    @After
    public void teardownScenario(Scenario scenario){
        if(scenario.isFailed()){
            byte [] screenshot = ((TakesScreenshot) Driver.getDriver()).getScreenshotAs(OutputType.BYTES);
            scenario.attach(screenshot, "image/png", scenario.getName());
        }
        Driver.closeDriver();
    }

}
