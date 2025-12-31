package com.testinium.step_definitions;

import com.testinium.pages.CalendarP;
import com.testinium.utilities.Driver;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.junit.Assert;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * Cucumber step definitions class for the Calendar/Meetings module tests in the Odoo application.
 * 
 * <p>This class provides Gherkin step implementations for testing the Calendar functionality,
 * including date navigation, view switching (day/week/month), event creation, editing, and verification.
 * It serves as the glue code that binds Cucumber feature file steps to executable Java methods.</p>
 * 
 * <p>The class implements steps using the following Cucumber annotations:</p>
 * <ul>
 *   <li>{@code @When} - Actions the user performs on the calendar interface</li>
 *   <li>{@code @Then} - Verifications and assertions of expected outcomes</li>
 *   <li>{@code @And} - Additional actions within a scenario sequence</li>
 * </ul>
 * 
 * <p>This class utilizes explicit waits via {@link WebDriverWait} with a 2-second timeout
 * to handle dynamic element loading. Note that this short timeout may cause flaky tests
 * on slower environments or when network latency is high.</p>
 * 
 * <p>Example Gherkin step binding:</p>
 * <pre>{@code
 * When User click on the calendar dashboard
 * Then User should see the last stage of calendar view
 * }</pre>
 * 
 * @see com.testinium.pages.CalendarP
 * @see com.testinium.utilities.Driver
 * @see org.openqa.selenium.support.ui.WebDriverWait
 */
public class Calendar {

    /**
     * CalendarP page object instance providing WebElement locators for Calendar module UI interactions.
     * 
     * <p>This page object encapsulates all WebElement locators for the Calendar/Meetings module,
     * including navigation buttons, view toggles, date cells, and event creation elements.
     * The instance is initialized eagerly at field declaration time, which triggers the
     * PageFactory initialization with the current WebDriver instance.</p>
     * 
     * @see CalendarP
     */
    CalendarP calendarP = new CalendarP();
    
    /**
     * WebDriverWait instance for explicit waits with a 2-second timeout.
     * 
     * <p>This wait object is used throughout the class to wait for element visibility
     * before performing actions. The 2-second timeout is relatively short and may
     * cause flaky tests on slower environments or when dealing with complex page loads.</p>
     * 
     * <p><strong>Note:</strong> This field is initialized at declaration time using
     * {@link Driver#getDriver()}, which couples object instantiation to driver availability.
     * The driver must be initialized before this class is instantiated.</p>
     * 
     * @see WebDriverWait
     * @see Driver#getDriver()
     */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),2);

    /**
     * Clicks on the calendar navigation button to access the Calendar dashboard.
     * 
     * <p>This method implements the Gherkin step: <em>"User click on the calendar dashboard"</em></p>
     * 
     * <p>The method clicks the calendar navigation button in the Odoo sidebar and then
     * waits for the button element to remain visible, confirming the navigation action
     * was initiated successfully.</p>
     * 
     * @throws InterruptedException if thread sleep is interrupted during execution
     * @see CalendarP#calendarButton
     */
    @When("User click on the calendar dashboard")
    public void user_clicks_on_the_calendar_dashboard() throws InterruptedException {
        calendarP.calendarButton.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.calendarButton));
    }

    /**
     * Clicks the Day view toggle button to switch the calendar display to single-day view.
     * 
     * <p>This method implements the Gherkin step: <em>"User click on day button"</em></p>
     * 
     * <p>Switches the calendar display mode to show a single day's events and schedules.
     * After clicking, the method waits for the day button to remain visible to ensure
     * the view toggle action completed.</p>
     * 
     * @see CalendarP#day
     */
    @When("User click on day button")
    public void user_clicks_on_day_button() {
        calendarP.day.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.day));
    }

    /**
     * Clicks the Week view toggle button to switch the calendar display to week view.
     * 
     * <p>This method implements the Gherkin step: <em>"User click on week button"</em></p>
     * 
     * <p>Switches the calendar display mode to show a week's worth of events and schedules.
     * After clicking, the method waits for the week button to remain visible to ensure
     * the view toggle action completed.</p>
     * 
     * @see CalendarP#week
     */
    @When("User click on week button")
    public void user_clicks_on_week_button() {
        calendarP.week.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.week));
    }

    /**
     * Clicks the Month view toggle button to switch the calendar display to month view.
     * 
     * <p>This method implements the Gherkin step: <em>"User click on month button"</em></p>
     * 
     * <p>Switches the calendar display mode to show a full month's events and schedules.
     * After clicking, the method waits for the month button to remain visible to ensure
     * the view toggle action completed.</p>
     * 
     * @see CalendarP#month
     */
    @When("User click on month button")
    public void user_clicks_on_month_button() {
        calendarP.month.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.month));
    }

    /**
     * Verifies that the calendar module has loaded by asserting the page title.
     * 
     * <p>This method implements the Gherkin step: <em>"User should see the last stage of calendar view"</em></p>
     * 
     * <p>The verification is performed by comparing the actual browser page title against
     * the expected value "Meetings - Odoo". The method first waits for the calendar module
     * container to become visible before performing the title assertion.</p>
     * 
     * <p>If the title does not match, the assertion will fail with the message:
     * "The title is not same as the expected!"</p>
     * 
     * @see CalendarP#calendarModule
     * @see Driver#getDriver()
     */
    @Then("User should see the last stage of calendar view")
    public void user_should_see_the_last_stage_of_calendar_view() {
        wait.until(ExpectedConditions.visibilityOf(calendarP.calendarModule));
        String expectedDashboard = "Meetings - Odoo";
        String actualDashboard = Driver.getDriver().getTitle();
        Assert.assertEquals("The title is not same as the expected!", expectedDashboard, actualDashboard);
    }

    /**
     * Clicks the day view and verifies that the displayed date matches the expected format.
     * 
     * <p>This method implements the Gherkin step: <em>"User click day on the calendar and display day"</em></p>
     * 
     * <p>This method performs a complex verification sequence:</p>
     * <ol>
     *   <li>Clicks the day view toggle button</li>
     *   <li>Extracts the day number from the highlighted calendar cell</li>
     *   <li>Extracts the month (0-indexed) and year from the calendar element's data attributes</li>
     *   <li>Converts the numeric month to a full month name string via switch statement</li>
     *   <li>Builds the expected breadcrumb format: "Meetings (Month Day, Year)"</li>
     *   <li>Waits 3 seconds for UI stabilization</li>
     *   <li>Asserts the actual date display text matches the expected format</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> The 3-second Thread.sleep is used for UI stabilization,
     * which is generally not recommended. Consider replacing with explicit waits for
     * better reliability and faster test execution.</p>
     * 
     * @throws InterruptedException if the thread sleep is interrupted during execution
     * @see CalendarP#dayCalendar
     * @see CalendarP#monthAndYearCalendar
     * @see CalendarP#dateActual
     */
    @When("User click day on the calendar and display day")
    public void user_clicks_day_on_the_calendar_and_display_day() throws InterruptedException {
        calendarP.day.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.day));
        String dayCalendar = calendarP.dayCalendar.getText();
        int monthCalendar = Integer.parseInt(calendarP.monthAndYearCalendar.getAttribute("data-month")) + 1;
        int yearCalendar = Integer.parseInt(calendarP.monthAndYearCalendar.getAttribute("data-year"));

        String month = "";

        switch (monthCalendar) {
            case 1:
                month = "January";
                break;
            case 2:
                month = "February";
                break;
            case 3:
                month = "March";
                break;
            case 4:
                month = "April";
                break;
            case 5:
                month = "May";
                break;
            case 6:
                month = "June";
                break;
            case 7:
                month = "July";
                break;
            case 8:
                month = "August";
                break;
            case 9:
                month = "September";
                break;
            case 10:
                month = "October";
                break;
            case 11:
                month = "November";
                break;
            case 12:
                month = "December";
                break;
        }

        String expectedResult = "Meetings (" + month + " " + dayCalendar + ", " + yearCalendar + ")";
        Thread.sleep(3000);
        String actualResult = calendarP.dateActual.getText();
        Assert.assertEquals(expectedResult,actualResult);


    }

    /**
     * Clicks the month view and verifies that the displayed month/year matches the expected format.
     * 
     * <p>This method implements the Gherkin step: <em>"User click month on the calendar and display month"</em></p>
     * 
     * <p>Similar to the day verification method, but for month view. This method:</p>
     * <ol>
     *   <li>Clicks the month view toggle button</li>
     *   <li>Extracts the month (0-indexed) and year from calendar element's data attributes</li>
     *   <li>Converts the numeric month to a full month name string via switch statement</li>
     *   <li>Builds the expected breadcrumb format: "Meetings (Month Year)" without day</li>
     *   <li>Waits 3 seconds for UI stabilization</li>
     *   <li>Asserts the actual date display text matches the expected format</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> The 3-second Thread.sleep is used for UI stabilization,
     * which is generally not recommended. Consider replacing with explicit waits for
     * better reliability and faster test execution.</p>
     * 
     * @throws InterruptedException if the thread sleep is interrupted during execution
     * @see CalendarP#month
     * @see CalendarP#monthAndYearCalendar
     * @see CalendarP#dateActual
     */
    @Then("User click month on the calendar and display month")
    public void user_click_month_on_the_calendar_and_display_month() throws InterruptedException {
        calendarP.month.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.month));
        int monthCalendar = Integer.parseInt(calendarP.monthAndYearCalendar.getAttribute("data-month")) + 1;
        int yearCalendar = Integer.parseInt(calendarP.monthAndYearCalendar.getAttribute("data-year"));

        String month = "";

        switch (monthCalendar) {
            case 1:
                month = "January";
                break;
            case 2:
                month = "February";
                break;
            case 3:
                month = "March";
                break;
            case 4:
                month = "April";
                break;
            case 5:
                month = "May";
                break;
            case 6:
                month = "June";
                break;
            case 7:
                month = "July";
                break;
            case 8:
                month = "August";
                break;
            case 9:
                month = "September";
                break;
            case 10:
                month = "October";
                break;
            case 11:
                month = "November";
                break;
            case 12:
                month = "December";
                break;
        }

        String expectedResult = "Meetings (" + month+ " "+ yearCalendar + ")";
        Thread.sleep(3000);
        String actualResult = calendarP.dateActual.getText();
        Assert.assertEquals(expectedResult,actualResult);
    }

    /**
     * Clicks on a specific calendar grid cell to open the event creation modal.
     * 
     * <p>This method implements the Gherkin step: <em>"User click on desired date time"</em></p>
     * 
     * <p>Clicks on a predefined date/time cell in the calendar grid (dateBox) to trigger
     * the event creation modal. After clicking, the method asserts that the createNote
     * modal element is displayed, confirming the modal opened successfully.</p>
     * 
     * @see CalendarP#dateBox
     * @see CalendarP#createNote
     */
    @And("User click on desired date time")
    public void userClickOnDesiredDateTime() {
        calendarP.dateBox.click();
        Assert.assertTrue(calendarP.createNote.isDisplayed());
    }

    /**
     * Enters an event/meeting summary and creates the calendar event.
     * 
     * <p>This method implements the Gherkin step: <em>"User enters {string} in the box and clicks the create button"</em></p>
     * 
     * <p>This is a parameterized Cucumber step that accepts the event name from the Gherkin
     * feature file. The method performs the following actions:</p>
     * <ol>
     *   <li>Enters the provided note/event summary into the summary input field</li>
     *   <li>Clicks the create button to save the event</li>
     *   <li>Verifies that the created note displays the expected event name</li>
     * </ol>
     * 
     * @param note the event/meeting summary text to enter, provided from the Cucumber step parameter
     * @see CalendarP#summaryBox
     * @see CalendarP#createButton
     * @see CalendarP#getNote
     */
    @Then("User enters {string} in the box and clicks the create button")
    public void userEntersInTheBoxAndClicksTheCreateButton(String note) {

        String eventName = note;

        calendarP.summaryBox.sendKeys(note);
        calendarP.createButton.click();

        Assert.assertEquals(calendarP.getNote.getText(),eventName);
    }

    /**
     * Verifies that the created note/event is visible on the calendar.
     * 
     * <p>This method implements the Gherkin step: <em>"User can see all the note"</em></p>
     * 
     * <p>Asserts that the createdNote element is displayed on the page, confirming
     * that the event was successfully created and is visible in the calendar view.</p>
     * 
     * @see CalendarP#createdNote
     */
    @When("User can see all the note")
    public void user_can_see_all_the_note() {
        Assert.assertTrue(calendarP.createdNote.isDisplayed());
    }
    
    /**
     * Clicks on an existing note/event to select it and open the event details modal.
     * 
     * <p>This method implements the Gherkin step: <em>"User can select the note"</em></p>
     * 
     * <p>Clicks on an existing note element to select it, waits for the element visibility,
     * and then asserts that the event details modal (createdModele) is displayed.</p>
     * 
     * @see CalendarP#selectNote
     * @see CalendarP#createdModele
     */
    @When("User can select the note")
    public void user_can_select_the_note() {
        calendarP.selectNote.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.selectNote));
        Assert.assertTrue(calendarP.createdModele.isDisplayed());
    }
    
    /**
     * Edits the selected event information by modifying the event text.
     * 
     * <p>This method implements the Gherkin step: <em>"User can edit the information"</em></p>
     * 
     * <p>This method performs the following editing sequence:</p>
     * <ol>
     *   <li>Clicks the edit button to enter edit mode</li>
     *   <li>Waits for the edit button visibility confirmation</li>
     *   <li>Clears the existing text in the edit text field</li>
     *   <li>Enters the new text "Hello My Friends"</li>
     *   <li>Waits for the edit text field visibility</li>
     *   <li>Checks if the tags checkbox is selected (note: result is not asserted)</li>
     * </ol>
     * 
     * <p><strong>Note:</strong> The tagsCheckbox.isSelected() call result is not captured
     * or asserted, which may indicate incomplete implementation or a verification that
     * was added for debugging purposes.</p>
     * 
     * @see CalendarP#editButton
     * @see CalendarP#editText
     * @see CalendarP#tagsCheckbox
     */
    @When("User can edit the information")
    public void user_can_edit_the_information() {
        calendarP.editButton.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.editButton));
        calendarP.editText.clear();
        calendarP.editText.sendKeys("Hello My Friends");
        wait.until(ExpectedConditions.visibilityOf(calendarP.editText));
        calendarP.tagsCheckbox.isSelected();


    }
    
    /**
     * Saves all edited event information by clicking the save button.
     * 
     * <p>This method implements the Gherkin step: <em>"User can save all edit"</em></p>
     * 
     * <p>Clicks the save button to persist the edited event information.
     * This completes the event editing workflow initiated by {@link #user_can_edit_the_information()}.</p>
     * 
     * @see CalendarP#saveButton
     */
    @Then("User can save all edit")
    public void user_can_save_all_edit() {
        calendarP.saveButton.click();
    }


}
