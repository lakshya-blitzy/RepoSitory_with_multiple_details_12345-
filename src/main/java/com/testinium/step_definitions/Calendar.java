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
 * Step Definition for the Calendar (Meetings) module of the Odoo/Upgenix ERP, binding every step of
 * {@code Calendar.feature} except its Background login step, bound in {@link com.testinium.step_definitions.Session}.
 *
 * <p>The steps open the Calendar module, switch between the day, week and month views, check the
 * date shown in the control-panel header, and create, select and edit a calendar event.
 *
 * <p>Page Object: {@link com.testinium.pages.CalendarP}, held in the {@code calendarP} field.
 * Both {@code calendarP} and the 2-second {@code WebDriverWait} are created in field initializers
 * that call {@link com.testinium.utilities.Driver#getDriver()}. Creating an instance reuses the thread's
 * browser session or, if it has none, opens one when the {@code browser} key is {@code chrome} or
 * {@code firefox}. Otherwise creation fails with {@code NullPointerException}: from {@code getDriver()}
 * if the key or configuration file is missing, or from the {@code WebDriverWait} for any other value.
 */
public class Calendar {

    /** Page Object for the Calendar module, whose elements the steps click, read and check. */
    CalendarP calendarP = new CalendarP();
    /** Explicit wait of 2 seconds on the thread's driver. */
    WebDriverWait wait = new WebDriverWait(Driver.getDriver(),2);

    /**
     * Opens the Calendar module by clicking {@code calendarP.calendarButton}, then waits for that button to be visible
     * with a two-second configured explicit timeout; the 10-second implicit wait can extend the elapsed time.
     * <p>
     * Gherkin: {@code User click on the calendar dashboard}
     *
     * @throws InterruptedException never in practice: the signature declares it, but the body does
     *         not call {@code Thread.sleep}, and neither {@code WebElement.click()} nor
     *         {@code WebDriverWait.until} declares it
     */
    @When("User click on the calendar dashboard")
    public void user_clicks_on_the_calendar_dashboard() throws InterruptedException {
        calendarP.calendarButton.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.calendarButton));
    }

    /**
     * Switches the calendar to the day view by clicking {@code calendarP.day}, then waits for that button to be
     * visible with a two-second configured explicit timeout; the 10-second implicit wait can extend the elapsed time.
     * <p>
     * Gherkin: {@code User click on day button}
     */
    @When("User click on day button")
    public void user_clicks_on_day_button() {
        calendarP.day.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.day));
    }

    /**
     * Switches the calendar to the week view by clicking {@code calendarP.week}, then waits for that button to be
     * visible with a two-second configured explicit timeout; the 10-second implicit wait can extend the elapsed time.
     * <p>
     * Gherkin: {@code User click on week button}
     */
    @When("User click on week button")
    public void user_clicks_on_week_button() {
        calendarP.week.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.week));
    }

    /**
     * Switches the calendar to the month view by clicking {@code calendarP.month}, then waits for that button to be
     * visible with a two-second configured explicit timeout; the 10-second implicit wait can extend the elapsed time.
     * <p>
     * Gherkin: {@code User click on month button}
     */
    @When("User click on month button")
    public void user_clicks_on_month_button() {
        calendarP.month.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.month));
    }

    /**
     * Verifies that the Calendar module has loaded: waits for {@code calendarP.calendarModule} to be visible with a
     * two-second configured explicit timeout (the 10-second implicit wait can extend the elapsed time), then asserts
     * that the browser page title, read from {@link com.testinium.utilities.Driver#getDriver()}, equals the Meetings
     * page title hard-coded in this method.
     * <p>
     * Gherkin: {@code User should see the last stage of calendar view}
     */
    @Then("User should see the last stage of calendar view")
    public void user_should_see_the_last_stage_of_calendar_view() {
        wait.until(ExpectedConditions.visibilityOf(calendarP.calendarModule));
        String expectedDashboard = "Meetings - Odoo";
        String actualDashboard = Driver.getDriver().getTitle();
        Assert.assertEquals("The title is not same as the expected!", expectedDashboard, actualDashboard);
    }

    /**
     * Switches to the day view and verifies that the control-panel header shows today's date.
     *
     * <p>The step clicks {@code calendarP.day} and waits for it to be visible with a two-second configured explicit
     * timeout; the 10-second implicit wait can extend the elapsed time. It builds the expected header text from
     * three values: the day of month, read as the text of {@code calendarP.dayCalendar}; the month, read from the
     * zero-based {@code data-month} attribute of {@code calendarP.monthAndYearCalendar}, incremented by 1 and mapped
     * by a {@code switch} to its English name; and the year, read from the {@code data-year} attribute of the same
     * element. The expected text is the module name followed, in parentheses, by the month name, day and year.
     * After a fixed 3-second {@code Thread.sleep}, it asserts that the text of {@code calendarP.dateActual} equals
     * the expected text.
     *
     * <p>The {@code switch} has no {@code default} branch, so a month number outside 1 to 12 leaves
     * the month name empty in the expected text; the assertion then fails unless the header shows that same text.
     * <p>
     * Gherkin: {@code User click day on the calendar and display day}
     *
     * @throws InterruptedException if the thread is interrupted during the 3-second
     *         {@code Thread.sleep}
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
     * Switches to the month view and verifies that the control-panel header shows the current
     * month and year.
     *
     * <p>The step clicks {@code calendarP.month} and waits for it to be visible with a two-second configured
     * explicit timeout; the 10-second implicit wait can extend the elapsed time. It reads
     * the zero-based {@code data-month} attribute of {@code calendarP.monthAndYearCalendar}, increments it by 1 and
     * maps it by a {@code switch} to its English name, and reads the year from the {@code data-year} attribute of
     * the same element. The expected text is the module name followed, in parentheses, by the month name and
     * year. After a fixed 3-second {@code Thread.sleep}, it asserts that the text of {@code calendarP.dateActual}
     * equals the expected text.
     *
     * <p>Although bound with {@code @Then}, this step performs an action (the view switch) as well
     * as the assertion. As in the day-view step, a month number outside 1 to 12 leaves the month
     * name empty in the expected text; the assertion then fails unless the header shows that same text.
     * <p>
     * Gherkin: {@code User click month on the calendar and display month}
     *
     * @throws InterruptedException if the thread is interrupted during the 3-second
     *         {@code Thread.sleep}
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
     * Clicks the grid cell {@code calendarP.dateBox} to start creating an event, then asserts that the
     * first {@code modal-header} on the page ({@code calendarP.createNote}) is displayed, whichever modal it belongs to.
     * <p>
     * Gherkin: {@code User click on desired date time}
     */
    @And("User click on desired date time")
    public void userClickOnDesiredDateTime() {
        calendarP.dateBox.click();
        Assert.assertTrue(calendarP.createNote.isDisplayed());
    }

    /**
     * Creates a calendar event: types {@code note} into {@code calendarP.summaryBox}, clicks
     * {@code calendarP.createButton}, and asserts that the text of {@code calendarP.getNote} equals
     * {@code note}.
     *
     * <p>The assertion passes the actual value first and the expected value second, so a failure
     * message labels the two values in reverse.
     * <p>
     * Gherkin: {@code User enters {string} in the box and clicks the create button}
     *
     * @param note the event summary bound to the {@code {string}} parameter of the step
     */
    @Then("User enters {string} in the box and clicks the create button")
    public void userEntersInTheBoxAndClicksTheCreateButton(String note) {

        String eventName = note;

        calendarP.summaryBox.sendKeys(note);
        calendarP.createButton.click();

        Assert.assertEquals(calendarP.getNote.getText(),eventName);
    }

    /**
     * Asserts that the name field of the created event, {@code calendarP.createdNote}, is displayed.
     * <p>
     * Gherkin: {@code User can see all the note}
     */
    @When("User can see all the note")
    public void user_can_see_all_the_note() {
        Assert.assertTrue(calendarP.createdNote.isDisplayed());
    }
    /**
     * Opens the created event by clicking {@code calendarP.selectNote}, waits for it to be visible with a two-second
     * configured explicit timeout (the 10-second implicit wait can extend the elapsed time), and asserts that the first
     * {@code modal-content} on the page ({@code calendarP.createdModele}) is displayed, whichever modal it belongs to.
     * <p>
     * Gherkin: {@code User can select the note}
     */
    @When("User can select the note")
    public void user_can_select_the_note() {
        calendarP.selectNote.click();
        wait.until(ExpectedConditions.visibilityOf(calendarP.selectNote));
        Assert.assertTrue(calendarP.createdModele.isDisplayed());
    }
    /**
     * Edits the opened event: clicks {@code calendarP.editButton} and waits for it to be visible, clears
     * {@code calendarP.editText}, types hard-coded replacement text, and waits for that field to be visible. Each
     * wait has a two-second configured explicit timeout; the 10-second implicit wait can extend the elapsed time.
     *
     * <p>Known discrepancy: the step calls {@code calendarP.tagsCheckbox.isSelected()} but
     * discards the result, so the checkbox state is read but not asserted, and the step makes
     * no assertion.
     * <p>
     * Gherkin: {@code User can edit the information}
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
     * Saves the edited event by clicking {@code calendarP.saveButton}. The step performs no
     * verification that the save succeeded.
     * <p>
     * Gherkin: {@code User can save all edit}
     */
    @Then("User can save all edit")
    public void user_can_save_all_edit() {
        calendarP.saveButton.click();
    }


}
