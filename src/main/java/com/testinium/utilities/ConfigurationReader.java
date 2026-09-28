package com.testinium.utilities;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

/**
 * Utility-layer accessor for the framework's externalized test configuration.
 *
 * <p>A static initializer loads {@code configuration.properties} exactly once, when this
 * class is first loaded, into an in-memory {@link java.util.Properties} snapshot. The file
 * is opened with {@code new FileInputStream("configuration.properties")}, a path resolved
 * against the JVM working directory, which is normally the project root when Maven runs
 * the tests.
 *
 * <p>{@code configuration.properties} is not committed to the repository. Create it at the
 * project root before running the suite.
 *
 * <p>Error handling: if the file cannot be opened or read, the initializer catches the
 * {@link java.io.IOException}, prints a message and the stack trace to standard output and
 * standard error, and does not rethrow it. The class still loads, the snapshot stays empty,
 * and every later {@link #getProperty(String)} call returns {@code null}.
 *
 * <p>Keys read by the codebase (names only):
 * <ul>
 *   <li>{@code browser}: read by {@link Driver#getDriver()}; expected {@code chrome} or
 *       {@code firefox}.</li>
 *   <li>{@code web.table.url}: read by the {@code LoginSD}, {@code EmployeeStage} and
 *       {@code Session} step definitions.</li>
 *   <li>{@code username}, {@code password}: read by the {@code Session} step definitions.</li>
 *   <li>{@code url}: read by the {@code EmployeeStage} step definitions.</li>
 *   <li>{@code EmplTitle}: read by the {@code EmployeeStage} step definitions as the expected
 *       Employees page title.</li>
 * </ul>
 *
 * @see Driver#getDriver()
 */
public class ConfigurationReader {
    //1- Create the object of Properties
    /** In-memory snapshot of the key/value pairs loaded from {@code configuration.properties}. */
    private static Properties properties = new Properties();

    static {
        try {
            //2 - We need to open the file in java memory: FileInputStream
            FileInputStream file = new FileInputStream("configuration.properties");

            //3- Load the properties object using FileInputStream object
            properties.load(file);

            //close the file
            file.close();
        } catch (IOException e) {
            System.out.println("File is not found in the ConfigurationReader class");
            e.printStackTrace();
        }
    }

    /**
     * Returns the configured value for the given key.
     *
     * <p>The lookup reads the in-memory snapshot captured at class-load time and performs no
     * file I/O or reload, so edits to {@code configuration.properties} during a run take
     * effect only on the next JVM start.
     *
     * @param keyword the property key to look up, for example {@code "browser"}
     * @return the property value, or {@code null} if the key is absent or the file failed
     *         to load
     */
    public static String getProperty(String keyword){
        return properties.getProperty(keyword);
    }
}