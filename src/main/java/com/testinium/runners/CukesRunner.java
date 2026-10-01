package com.testinium.runners;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;

/**
 * Runner: the primary JUnit 4 and Cucumber entry point for the Odoo/Upgenix ERP UI test suite.
 *
 * <p>{@code @RunWith(Cucumber.class)} hands the JUnit lifecycle to Cucumber, and
 * {@code @CucumberOptions} configures the run:
 * <ul>
 *   <li>{@code plugin} writes the report artifacts:
 *     <ul>
 *       <li>{@code "html:target/cucumber-reports.html"}: the HTML report.</li>
 *       <li>{@code "json:target/cucumber.json"}: the JSON report. The Jenkins "Generate report" stage
 *           is configured to publish it, when present, through the {@code cucumber} step
 *           ({@code fileIncludePattern} <code>'**&#47;*.json'</code>); see Execution below.</li>
 *       <li>{@code "rerun:target/rerun.txt"}: the failed-scenario locations consumed by
 *           {@link FailedTestRunner}.</li>
 *       <li>{@code "me.jvt.cucumber.report.PrettyReports:target/cucumber"}: the PrettyReports HTML
 *           report bundle.</li>
 *     </ul>
 *   </li>
 *   <li>{@code features = "src/main/resources/features"}: the directory scanned for {@code .feature} files.</li>
 *   <li>{@code glue = "com/testinium/step_definitions"}: the package holding step definitions and hooks.</li>
 *   <li>{@code dryRun = false}: steps are executed, not only checked for matching bindings.</li>
 *   <li>{@code tags = "@Smoke"}: only scenarios tagged {@code @Smoke} run.</li>
 * </ul>
 *
 * <p>Execution: Surefire in {@code pom.xml} includes <code>**&#47;CukesRunner*.java</code> with
 * {@code parallel=methods} and {@code testFailureIgnore=true}, but it scans only compiled test classes and this
 * class compiles from {@code src/main/java}, so the Jenkins {@code mvn clean test} runs no scenario.
 *
 * @see FailedTestRunner
 */
@RunWith(Cucumber.class)
@CucumberOptions(
    plugin = {
        "html:target/cucumber-reports.html",
        "json:target/cucumber.json",
        "rerun:target/rerun.txt",
        "me.jvt.cucumber.report.PrettyReports:target/cucumber"
    },
    features = "src/main/resources/features",
    glue = "com/testinium/step_definitions",
    dryRun = false,
    tags = "@Smoke"

)
public class CukesRunner {



}
