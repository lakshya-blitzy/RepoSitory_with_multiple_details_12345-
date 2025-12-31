package com.testinium.utilities;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

/**
 * Static configuration loading utility for the test automation framework.
 * 
 * <p>This class implements a singleton-like pattern via a static initializer block,
 * ensuring that configuration properties are loaded exactly once when the class is
 * first loaded by the JVM. All configuration values are cached at the JVM level,
 * providing a snapshot of the configuration file at class-load time.</p>
 * 
 * <p><strong>Configuration File Location:</strong> The configuration is read from
 * {@code configuration.properties} located in the process working directory (typically
 * the project root when running tests via Maven or an IDE).</p>
 * 
 * <p><strong>JVM-Level Caching:</strong> Configuration properties are loaded once
 * during class initialization and remain static throughout the JVM lifetime. No
 * automatic reloading occurs during runtime. Changes to the {@code configuration.properties}
 * file require a JVM restart (i.e., re-running the tests) to take effect.</p>
 * 
 * <p><strong>Common Configuration Keys:</strong></p>
 * <ul>
 *   <li>{@code browser} - Browser type for WebDriver initialization (e.g., "chrome", "firefox")</li>
 *   <li>{@code url} - Base URL of the application under test</li>
 *   <li>{@code username} - Test user credentials</li>
 *   <li>{@code password} - Test user password</li>
 * </ul>
 * 
 * <p><strong>Usage Example:</strong></p>
 * <pre>{@code
 * String browser = ConfigurationReader.getProperty("browser");
 * String url = ConfigurationReader.getProperty("url");
 * }</pre>
 * 
 * @see Driver Driver class that uses this for browser configuration via getProperty("browser")
 */
public class ConfigurationReader {
    
    /**
     * Static storage for loaded configuration key-value pairs.
     * 
     * <p>This {@link java.util.Properties} field holds the parsed contents from
     * the {@code configuration.properties} file. The private static scope ensures
     * a single shared instance across all callers, providing consistent configuration
     * access throughout the test framework.</p>
     * 
     * <p>The field is initialized as an empty Properties object and populated
     * during the static initializer block execution. If the configuration file
     * cannot be loaded, this field remains as an empty Properties object.</p>
     */
    private static Properties properties = new Properties();

    /*
     * Static initializer block for one-time configuration loading.
     * 
     * This block executes automatically when the ConfigurationReader class is first
     * loaded by the JVM. It performs the following operations:
     * 
     * 1. Creates a FileInputStream using the relative path "configuration.properties",
     *    resolved from the current process working directory.
     * 
     * 2. Loads the properties from the FileInputStream by calling properties.load(file),
     *    which parses the file content as key=value pairs according to the standard
     *    Java Properties file format.
     * 
     * 3. Closes the FileInputStream to release system resources and file handles.
     * 
     * Exception Handling:
     * - If the configuration file is not found or cannot be read, an IOException
     *   is caught and logged to System.out with a stack trace.
     * - The exception is NOT rethrown, allowing the class to remain usable even
     *   if configuration loading fails. In this case, getProperty() will return
     *   null for all keys since the properties object remains empty.
     * - This fail-soft behavior prevents test framework initialization failures
     *   but may lead to NullPointerExceptions if callers don't handle null returns.
     */
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
     * Retrieves a configuration property value by its key.
     * 
     * <p>This method provides simple key-based lookup of configuration values
     * with no additional caching or transformation. It delegates directly to
     * {@link Properties#getProperty(String)} for the actual lookup operation.</p>
     * 
     * <p><strong>Return Value Behavior:</strong></p>
     * <ul>
     *   <li>Returns the property value as a String if the key exists in the
     *       loaded configuration</li>
     *   <li>Returns {@code null} if the key is not found in the properties file</li>
     *   <li>Returns {@code null} for all keys if the configuration file failed
     *       to load during class initialization (IOException was caught and logged
     *       but not rethrown)</li>
     * </ul>
     * 
     * <p><strong>Usage Example:</strong></p>
     * <pre>{@code
     * // Retrieve browser type for WebDriver initialization
     * String browser = ConfigurationReader.getProperty("browser");
     * 
     * // Retrieve application URL
     * String url = ConfigurationReader.getProperty("url");
     * }</pre>
     * 
     * @param keyword the configuration property key to look up (e.g., "browser",
     *                "url", "username", "password")
     * @return the property value as a String, or {@code null} if the key is not
     *         found in the properties file or if the configuration file was not
     *         loaded successfully
     * @see Driver Driver class uses getProperty("browser") for browser configuration
     * @see Properties#getProperty(String)
     */
    public static String getProperty(String keyword){
        return properties.getProperty(keyword);
    }
}
