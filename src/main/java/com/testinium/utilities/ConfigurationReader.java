package com.testinium.utilities;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

/**
 * Utility-layer accessor for the framework's externalized test configuration.
 *
 * <p>A static initializer loads {@code configuration.properties} exactly once, when the class is
 * first initialized (normally by the first {@link #getProperty(String)} call), into an in-memory
 * {@link java.util.Properties} snapshot; edits made after that initialization are not reloaded. The
 * file is opened with {@code new FileInputStream("configuration.properties")}, relative to the JVM working
 * directory, which must be the project root: set it in the IDE run configuration or start {@code JUnitCore} there.
 *
 * <p>{@code configuration.properties} is not committed to the repository. Create it at the
 * project root before running the suite.
 *
 * <p>Error handling: the initializer catches any {@link java.io.IOException}, prints a message and a
 * stack trace, and does not rethrow it. If the file cannot be opened, every {@link #getProperty(String)}
 * call returns {@code null}; if reading fails partway, pairs parsed earlier are kept. Any other exception,
 * such as the one from a malformed <code>&#92;uXXXX</code> escape, propagates and class initialization fails.
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
     * <p>The lookup reads the in-memory snapshot captured when the class was initialized, normally by the
     * first call to this method, and performs no file I/O; edits to {@code configuration.properties}
     * made after that initialization are not reloaded.
     *
     * @param keyword the property key to look up, for example {@code "browser"}
     * @return the property value, or {@code null} if the key is not in the loaded snapshot; see the
     *         class comment for how a load failure empties or truncates it
     */
    public static String getProperty(String keyword){
        return properties.getProperty(keyword);
    }
}