package com.testinium.utilities;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

import java.util.concurrent.TimeUnit;

/**
 * Central WebDriver lifecycle management utility class providing thread-safe browser instance management.
 * 
 * <p>This utility implements the <strong>thread-local pattern</strong> using {@link InheritableThreadLocal}
 * to ensure each thread maintains its own isolated WebDriver instance. This design is critical for
 * supporting parallel test execution where multiple tests run simultaneously in separate threads,
 * each requiring an independent browser session.</p>
 * 
 * <h2>Design Pattern</h2>
 * <p>This class follows the <strong>Singleton-per-Thread</strong> pattern with lazy initialization:</p>
 * <ul>
 *   <li>A single WebDriver instance is created per thread on first access</li>
 *   <li>Subsequent calls from the same thread return the existing instance</li>
 *   <li>Child threads inherit their parent's WebDriver reference via {@link InheritableThreadLocal}</li>
 * </ul>
 * 
 * <h2>Non-Instantiability</h2>
 * <p>This class cannot be instantiated. The private constructor enforces static-only access
 * through the provided utility methods. All interaction must occur via
 * {@link #getDriver()} and {@link #closeDriver()}.</p>
 * 
 * <h2>Usage Pattern</h2>
 * <pre>{@code
 * // Obtain WebDriver for current thread (creates new instance if none exists)
 * WebDriver driver = Driver.getDriver();
 * 
 * // Use driver for browser automation
 * driver.get("https://example.com");
 * 
 * // Clean up when test completes (typically in @After hook)
 * Driver.closeDriver();
 * }</pre>
 * 
 * <h2>Browser Configuration</h2>
 * <p>Browser type is determined by reading the "browser" property from configuration.properties
 * via {@link ConfigurationReader#getProperty(String)}. Supported values:</p>
 * <ul>
 *   <li>{@code "chrome"} - Creates a ChromeDriver instance</li>
 *   <li>{@code "firefox"} - Creates a FirefoxDriver instance</li>
 * </ul>
 * 
 * @see ConfigurationReader
 * @see WebDriverManager
 * @see WebDriver
 * @see InheritableThreadLocal
 * @see com.testinium.step_definitions.Hooks
 */
public class Driver {

    /**
     * Private constructor preventing instantiation of this utility class.
     * 
     * <p>This constructor enforces the static-only usage pattern. All WebDriver
     * management must be performed through the static methods {@link #getDriver()}
     * and {@link #closeDriver()}. Attempting to instantiate this class will result
     * in a compilation error from external code.</p>
     */
    private Driver(){

    }

    /**
     * Thread-local storage for WebDriver instances providing per-thread driver isolation.
     * 
     * <p>Uses {@link InheritableThreadLocal} instead of regular {@link ThreadLocal} to allow
     * child threads to inherit the parent thread's WebDriver reference. This behavior is
     * important in scenarios where test code spawns child threads that need access to the
     * same browser session.</p>
     * 
     * <h3>Key Behaviors</h3>
     * <ul>
     *   <li><strong>Per-thread isolation:</strong> Each thread has its own WebDriver slot,
     *       preventing cross-thread interference during parallel test execution</li>
     *   <li><strong>Lazy initialization:</strong> The actual WebDriver instance is created
     *       on first {@link #getDriver()} call per thread (when slot is null)</li>
     *   <li><strong>Thread inheritance:</strong> Child threads automatically inherit parent's
     *       driver reference, enabling shared browser access when needed</li>
     *   <li><strong>Explicit cleanup:</strong> Must call {@link #closeDriver()} to remove
     *       the thread-local reference and quit the browser</li>
     * </ul>
     * 
     * @see #getDriver()
     * @see #closeDriver()
     */
    private static InheritableThreadLocal<WebDriver> driverPool = new InheritableThreadLocal<>();

    /**
     * Retrieves or creates a WebDriver instance for the current thread using lazy initialization.
     * 
     * <p>This method implements the lazy initialization pattern: if no WebDriver exists for the
     * current thread (i.e., {@code driverPool.get()} returns {@code null}), a new browser
     * instance is created and configured. Subsequent calls from the same thread return the
     * existing instance without creating a new browser.</p>
     * 
     * <p><strong>Initialization Process:</strong>
     * When creating a new WebDriver instance:</p>
     * <ol>
     *   <li>Browser type is read from configuration via {@code ConfigurationReader.getProperty("browser")}</li>
     *   <li>{@link WebDriverManager} automatically downloads and configures the browser driver executable</li>
     *   <li>A new browser instance is created (ChromeDriver or FirefoxDriver)</li>
     *   <li>Browser window is maximized for consistent element visibility</li>
     *   <li>Implicit wait of 10 seconds is configured using {@link java.util.concurrent.TimeUnit#SECONDS}</li>
     * </ol>
     * 
     * <p><strong>Supported Browser Types:</strong></p>
     * <table border="1">
     *   <caption>Browser Configuration Options</caption>
     *   <tr><th>Config Value</th><th>Driver Class</th><th>WebDriverManager Setup</th></tr>
     *   <tr><td>{@code "chrome"}</td><td>{@link ChromeDriver}</td><td>{@code WebDriverManager.chromedriver().setup()}</td></tr>
     *   <tr><td>{@code "firefox"}</td><td>{@link FirefoxDriver}</td><td>Note: Currently calls chromedriver setup (potential bug)</td></tr>
     * </table>
     * 
     * <p><strong>Important Notes:</strong></p>
     * <ul>
     *   <li><strong>Firefox configuration issue:</strong> The firefox branch currently calls
     *       {@code WebDriverManager.chromedriver().setup()} instead of
     *       {@code WebDriverManager.firefoxdriver().setup()}. This may cause issues if
     *       chromedriver is not available on the system.</li>
     *   <li><strong>Null return possibility:</strong> If the browser type from configuration
     *       does not match "chrome" or "firefox", no driver is created and {@code null}
     *       is returned. Callers should handle this case.</li>
     *   <li><strong>Thread safety:</strong> Each thread gets its own independent WebDriver
     *       instance, enabling safe parallel test execution.</li>
     * </ul>
     * 
     * @return the WebDriver instance for the current thread; may return {@code null} if the
     *         browser type specified in configuration.properties is not "chrome" or "firefox"
     * 
     * @see ConfigurationReader#getProperty(String)
     * @see WebDriverManager
     * @see #closeDriver()
     */
    public static WebDriver getDriver(){
        if(driverPool.get() == null){
            /*
            We read our browserType from configuration.properties.
            This way, we can control which browser is opened from outside our code, from configuration.properties.
            */
            String browserType = ConfigurationReader.getProperty("browser");

            switch(browserType){
                case "chrome":
                    WebDriverManager.chromedriver().setup();
                    driverPool.set(new ChromeDriver());
                    driverPool.get().manage().window().maximize();
                    driverPool.get().manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
                    break;
                case "firefox":
                    WebDriverManager.chromedriver().setup();
                    driverPool.set(new FirefoxDriver());
                    driverPool.get().manage().window().maximize();
                    driverPool.get().manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
                    break;
            }
        }
        return driverPool.get();
    }

    /**
     * Closes the WebDriver instance for the current thread and cleans up thread-local storage.
     * 
     * <p>This method performs complete cleanup of the browser session:</p>
     * <ol>
     *   <li>Checks if a WebDriver exists for the current thread</li>
     *   <li>Calls {@link WebDriver#quit()} to close all browser windows and terminate the
     *       WebDriver session, releasing system resources</li>
     *   <li>Removes the WebDriver reference from {@link #driverPool} via
     *       {@link InheritableThreadLocal#remove()}, ensuring the thread-local slot is cleared</li>
     * </ol>
     * 
     * <p><strong>Importance of Proper Cleanup:</strong>
     * Calling this method is essential for:</p>
     * <ul>
     *   <li><strong>Resource management:</strong> Releases browser processes and associated
     *       system resources (memory, file handles, network connections)</li>
     *   <li><strong>Session leak prevention:</strong> In parallel execution, failing to clean up
     *       thread-local storage can cause memory leaks as threads may be reused by the
     *       thread pool with stale references</li>
     *   <li><strong>Test isolation:</strong> Ensures each test starts with a fresh browser
     *       state when combined with {@link #getDriver()}</li>
     * </ul>
     * 
     * <p><strong>Typical Usage:</strong>
     * This method is typically invoked in Cucumber's {@code @After} hook to ensure browser
     * cleanup occurs after each scenario, regardless of test success or failure:</p>
     * <pre>{@code
     * @After
     * public void tearDown() {
     *     Driver.closeDriver();
     * }
     * }</pre>
     * 
     * <p><strong>Null-Safety:</strong>
     * This method is null-safe and performs no action if no WebDriver exists for the
     * current thread (i.e., if {@link #getDriver()} was never called or the driver was
     * already closed).</p>
     * 
     * @see WebDriver#quit()
     * @see com.testinium.step_definitions.Hooks
     * @see #getDriver()
     */
    public static void closeDriver(){
        if (driverPool.get() != null){
            driverPool.get().quit();
            driverPool.remove();
        }
    }

}
