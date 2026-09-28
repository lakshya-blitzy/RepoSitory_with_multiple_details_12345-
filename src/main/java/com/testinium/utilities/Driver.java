package com.testinium.utilities;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

import java.util.concurrent.TimeUnit;


/**
 * Utility-layer factory and lifecycle manager for the Selenium {@link org.openqa.selenium.WebDriver}
 * shared by all Page Objects and Step Definitions that drive the Odoo/Upgenix ERP UI.
 *
 * <p>The class keeps one {@code WebDriver} per thread in an {@link InheritableThreadLocal} pool.
 * The pool exists because Maven Surefire is configured to run tests in parallel
 * ({@code parallel=methods} in the {@code pom.xml} Surefire configuration), so each test thread
 * holds its own browser session. Because the pool is inheritable, a child thread started after
 * its parent thread obtained a driver inherits the parent's driver reference.
 *
 * <p>Consumers:
 * <ul>
 *   <li>Page Objects bind their {@code @FindBy} fields in their constructors with
 *       {@code PageFactory.initElements(Driver.getDriver(), this)}.</li>
 *   <li>Step Definitions call {@link #getDriver()} for browser-level actions such as navigation,
 *       title checks and explicit waits.</li>
 *   <li>{@code Hooks.teardownScenario(Scenario)} calls {@link #closeDriver()} to end the session.</li>
 * </ul>
 *
 * <p>All members are static and the class cannot be instantiated.
 *
 * @see ConfigurationReader#getProperty(String)
 */
public class Driver {

    /** Prevents instantiation; all members of this utility class are static. */
    private Driver(){

    }

    /** Per-thread holder of the current {@code WebDriver} session; empty until {@link #getDriver()} creates one. */
    private static InheritableThreadLocal<WebDriver> driverPool = new InheritableThreadLocal<>();
    /*
    Create a re-usable utility method which will return same driver instance when we call it
    */
    /**
     * Returns the {@code WebDriver} bound to the current thread, creating it lazily on first use.
     *
     * <p>Only when the current thread has no driver yet, the browser type is read with
     * {@code ConfigurationReader.getProperty("browser")} and a new session is created:
     * <ul>
     *   <li>{@code chrome}: provisions the driver binary with
     *       {@code WebDriverManager.chromedriver().setup()} and creates a {@code ChromeDriver}.</li>
     *   <li>{@code firefox}: creates a {@code FirefoxDriver}.</li>
     * </ul>
     * In both cases the browser window is maximized and a 10-second implicit wait is set.
     * Later calls from the same thread return the same instance until {@link #closeDriver()} runs.
     *
     * <p>Usage:
     * <pre>{@code
     * WebDriver driver = Driver.getDriver();
     * }</pre>
     * Page Objects pass the driver to Selenium's page factory in their constructors with
     * {@code PageFactory.initElements(Driver.getDriver(), this)}.
     *
     * <p>Behavior to be aware of:
     * <ul>
     *   <li>The {@code firefox} branch calls {@code WebDriverManager.chromedriver().setup()}
     *       rather than a geckodriver setup, so it provisions chromedriver, not geckodriver,
     *       before creating the {@code FirefoxDriver}.</li>
     *   <li>The {@code switch} has no {@code default} branch: any other {@code browser} value
     *       leaves the pool empty and this method returns {@code null}.</li>
     *   <li>A missing {@code browser} key, or a missing {@code configuration.properties} file,
     *       yields a {@code null} value, which causes a {@code NullPointerException} at the
     *       {@code switch}.</li>
     * </ul>
     *
     * @return the {@code WebDriver} bound to the current thread, or {@code null} if the configured
     *         browser is unsupported
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

    /*
       This method will make sure our driver value is always null after using quit() method
    */
    /**
     * Ends the browser session bound to the current thread and clears the thread's pool entry.
     *
     * <p>If the current thread holds a driver, this method calls {@code quit()} on it to close the
     * browser session and then {@code driverPool.remove()}, so the next {@link #getDriver()} call
     * on this thread creates a fresh session. If the thread holds no driver, it does nothing.
     *
     * <p>{@code Hooks.teardownScenario(Scenario)} invokes this method after it attaches a
     * screenshot for a failed scenario.
     */
    public static void closeDriver(){
        if (driverPool.get() != null){
            driverPool.get().quit();
            driverPool.remove();
        }
    }

}
