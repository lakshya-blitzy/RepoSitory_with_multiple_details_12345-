package com.testinium.runners;


import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;

/**
 * Runner: re-runs only the scenarios that failed in the previous {@link CukesRunner} execution.
 *
 * <p>{@code @CucumberOptions} configures the rerun:
 * <ul>
 *   <li>{@code features = "@target/rerun.txt"}: the leading {@code @} character makes Cucumber read
 *       scenario locations (feature-file paths with line numbers) from the rerun file written by the
 *       {@code "rerun:target/rerun.txt"} plugin of {@link CukesRunner}, instead of scanning a feature
 *       directory. The rerun file path and the feature-file paths it lists resolve against the working
 *       directory, so run both runners from the project root.</li>
 *   <li>{@code glue = "com/testinium/step_definitions"}: the same glue package as {@link CukesRunner},
 *       so step definitions and hooks bind the same way.</li>
 * </ul>
 * This runner sets no {@code tags} and no report {@code plugin}s.
 *
 * <p>Usage: run {@link CukesRunner} first so that {@code target/rerun.txt} exists, then run this class
 * explicitly as a JUnit test from the IDE, or from the project root with
 * {@code java -cp "target/classes:<dependency classpath>" org.junit.runner.JUnitCore
 * com.testinium.runners.FailedTestRunner}, where {@code mvn dependency:build-classpath} prints the
 * dependency classpath. Do not run {@code mvn clean} between the two runs, because {@code clean}
 * deletes {@code target/} and the rerun file with it.
 *
 * <p>Maven Surefire does not run this class. It does not match the Surefire include
 * <code>**&#47;CukesRunner*.java</code> in {@code pom.xml}, and Surefire scans only compiled test classes
 * ({@code target/test-classes}), while this class is compiled from {@code src/main/java}. As a result
 * {@code mvn test -Dtest=FailedTestRunner} stops with "No tests were executed!".
 */
@RunWith(Cucumber.class)
@CucumberOptions(
        glue = "com/testinium/step_definitions",
        features = "@target/rerun.txt"
)
public class FailedTestRunner {

}
