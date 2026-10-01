package com.testinium.step_definitions;

import com.testinium.utilities.Driver;
import io.cucumber.java.Scenario;
import org.junit.After;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;

/**
 * Cucumber Hook written to tear down each scenario of the Odoo/Upgenix UI suite.
 *
 * <p>When a scenario has failed, {@link #teardownScenario(Scenario)} captures a PNG screenshot
 * from {@link com.testinium.utilities.Driver#getDriver()} and attaches it to the scenario report.
 * Unless that screenshot step throws, it then calls {@link com.testinium.utilities.Driver#closeDriver()} to
 * attempt to release the thread's WebDriver; only if {@code quit()} returns is the pool entry cleared, so the
 * next scenario on that thread can start a fresh session. The method comment describes the exception paths.
 *
 * <p>Known discrepancy: the hook annotation is imported from JUnit ({@code org.junit.After}),
 * not from Cucumber ({@code io.cucumber.java.After}). Cucumber 7 registers hooks only from
 * {@code io.cucumber.java} annotations, so as written Cucumber does not register
 * {@link #teardownScenario(Scenario)} as an after-hook, and no failure screenshot is attached
 * and no driver is closed from this class. The import is left unchanged by design, because this
 * change adds documentation only.
 *
 * <p>The class declares no fields and uses no Page Objects.
 */
public class Hooks {

    /**
     * Attaches a screenshot to a failed scenario, then closes the thread's WebDriver if nothing throws first.
     *
     * <p>When {@code scenario.isFailed()} is true, the method casts
     * {@link com.testinium.utilities.Driver#getDriver()} to {@code TakesScreenshot}, captures the
     * browser screenshot as bytes with {@code getScreenshotAs(OutputType.BYTES)}, and attaches it to
     * the scenario with media type {@code image/png}, named after {@code scenario.getName()}.
     * If nothing throws, it then calls {@link com.testinium.utilities.Driver#closeDriver()}, which
     * quits the thread's driver and clears it. The call has no {@code finally}: an exception in the
     * screenshot or attach step skips it, leaving open any browser the thread holds; if {@code quit()} throws,
     * {@code closeDriver()} leaves the thread's pool entry set. The method is annotated with JUnit's
     * {@code @After}, not Cucumber's; see the class comment for why Cucumber does not register it.
     *
     * @param scenario the current Cucumber scenario; its status and name are read, and the
     *                 screenshot is attached to it
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
