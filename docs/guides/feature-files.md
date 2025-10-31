# Writing Gherkin Feature Files

## Overview

This guide covers how to write effective Gherkin feature files for behavior-driven development (BDD) in the Testinium QA Python test automation framework. Gherkin provides a business-readable, domain-specific language that describes software behavior without detailing implementation.

**What You'll Learn:**
- Gherkin syntax fundamentals (Given/When/Then)
- Feature file structure and organization
- Scenario vs Scenario Outline usage
- Examples tables for data-driven testing
- Tags for test organization and filtering
- Background sections for common preconditions
- Best practices for maintainable feature files

**Prerequisites:**
- Framework installed and configured (see [Getting Started](../getting-started/installation.md))
- Basic understanding of behavior-driven development concepts
- Familiarity with the application under test

## Gherkin Syntax Fundamentals

Gherkin uses a set of special keywords to define test behavior in a structured way. The language is designed to be readable by both technical and non-technical stakeholders.

### Core Keywords

**Given** - Describes the initial context or preconditions
```gherkin
Given User is on the upgenix login page
```

**When** - Describes an event or action
```gherkin
When User enters "salesmanager7@info.com" username
And User enters "salesmanager" password
And User clicks the login button
```

**Then** - Describes an expected outcome
```gherkin
Then User should see the dashboard
```

**And** / **But** - Connects multiple steps of the same type
```gherkin
When User enters "test@example.com" username
And User enters "password123" password
But User does not check remember me
```

**Source:** `features/Login.feature:10-18`

## Feature File Structure

### Feature Keyword

Every feature file starts with the `Feature` keyword followed by a brief description of the functionality being tested.

```gherkin
@Login
Feature: Testinium app login feature

  User Story:
  As a user, I should be able to login with correct credentials to different accounts.

  Accounts are: PosManager, SalesManager
```

**Components:**
- **Tag (@Login):** Identifies the feature for filtering and organization
- **Feature Title:** Clear, concise description of the feature
- **User Story:** Optional but recommended - describes the business value
- **Additional Context:** Supporting details about the feature

**Source:** `features/Login.feature:1-7`

### Background Section

The `Background` keyword defines steps that run before each scenario in the feature file. Use it for common preconditions shared across multiple scenarios.

```gherkin
Background: For the scenarios in the feature file, user is expected to be on login page
  Given User is on the upgenix login page
```

**When to Use Background:**
- Common setup steps needed by all scenarios
- Authentication or navigation to starting point
- Data setup shared across scenarios

**Important:** Background steps execute before EVERY scenario in the file. Keep them minimal to avoid unnecessary overhead.

**Source:** `features/Login.feature:9-10`

### Complete Feature Structure Example

```gherkin
@Calendar
Feature: Testinium app Calendar Module

  Account is: PosManager
  Background: As a Posmanager, I should be able to create and to see my meetings and events on my calendar from "Calendar" module
              For this ERP application, the calendar function is very crucial.
              Anyone in the team can contribute and plan their agenda using the calendar.
              To prevent any conflict, events should be created, edited and displayed by all team members.
  Given User login to test other features

  Scenario: Verify that all buttons work as expected at the Calendar stage
    When User click on the calendar dashboard
    And User click on day button
    And User click on week button
    And User click on month button
    Then User should see the last stage of calendar view
```

**Source:** `features/Calendar.feature:1-16`

## Scenarios: Single Test Cases

A `Scenario` defines a single test case with concrete steps. Each scenario should test one specific behavior.

### Basic Scenario Structure

```gherkin
Scenario: Verify that all buttons work as expected at the Calendar stage
  When User click on the calendar dashboard
  And User click on day button
  And User click on week button
  And User click on month button
  Then User should see the last stage of calendar view
```

**Best Practices for Scenarios:**
- One scenario = one test case
- Use descriptive scenario names that explain the behavior
- Keep scenarios focused and concise
- Include only relevant steps
- Start with the expected outcome in mind

**Source:** `features/Calendar.feature:11-16`

### When to Use Scenario

Use regular `Scenario` when:
- Testing a single, specific case
- Steps don't need parameterization
- Test data is hardcoded and doesn't vary
- Example: Testing that a specific button exists

```gherkin
Scenario: User can change display between Day-Week-Month
  When User click on the calendar dashboard
  And User click day on the calendar and display day
  Then User click month on the calendar and display month
```

**Source:** `features/Calendar.feature:18-21`

## Scenario Outline: Data-Driven Testing

`Scenario Outline` enables data-driven testing by parameterizing scenario steps with values from an `Examples` table.

### Scenario Outline Structure

```gherkin
@UPGN-286
Scenario Outline: Users log in with valid credentials
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  Then User should see the dashboard

  @SalesManager
  Examples: SalesManager's username and password
    |username               |password    |
    |salesmanager7@info.com |salesmanager|
    |salesmanager8@info.com |salesmanager|
    |salesmanager9@info.com |salesmanager|
```

**Key Elements:**
- **Placeholders:** Use `<parameter_name>` syntax in steps
- **Examples Keyword:** Introduces the data table
- **Table Header:** Defines parameter names (must match placeholders)
- **Table Rows:** Each row executes the scenario once with those values

**Source:** `features/Login.feature:13-35`

### When to Use Scenario Outline

Use `Scenario Outline` when:
- Testing the same behavior with different data sets
- Verifying boundary conditions (min, max, edge cases)
- Testing multiple user roles or permissions
- Executing the same workflow with various inputs

**Example Use Cases:**
- Login with multiple valid credentials
- Form validation with different invalid inputs
- API testing with various payloads
- Cross-browser or cross-device testing

### Multiple Examples Tables

A single Scenario Outline can have multiple `Examples` tables, each with its own tag for selective execution.

```gherkin
@UPGN-286
Scenario Outline: Users log in with valid credentials
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  Then User should see the dashboard

  @SalesManager
  Examples: SalesManager's username and password
    |username               |password    |
    |salesmanager7@info.com |salesmanager|
    |salesmanager8@info.com |salesmanager|
    |salesmanager9@info.com |salesmanager|
    |salesmanager10@info.com|salesmanager|

  @PosManager
  Examples: PosManager's username and password
    |username              |password  |
    |posmanager5@info.com  |posmanager|
    |posmanager6@info.com  |posmanager|
    |posmanager7@info.com  |posmanager|
```

**Benefits:**
- Organize test data by category (user role, data type, etc.)
- Enable selective execution with tags (`behave --tags=@SalesManager`)
- Improve readability by grouping related data
- Facilitate maintenance when data changes

**Source:** `features/Login.feature:20-54`

## Examples Tables

Examples tables provide test data for Scenario Outlines. Each row represents one test execution.

### Table Syntax

```gherkin
Examples: Test name
  |test       |
  |Test test  |
```

**Syntax Rules:**
- Use pipe `|` characters to separate columns
- First row is the header (parameter names)
- Subsequent rows are data values
- Column alignment is optional but improves readability
- Whitespace inside cells is preserved

**Source:** `features/Calendar.feature:29-31`

### Multi-Column Examples

```gherkin
Examples:
  | name   |  street name |   phone number | email        |
  | &Dustin|  Haussman    |   +99999999999 | abcd@info.com|
```

**Best Practices:**
- Align columns for readability
- Use descriptive header names
- Include only necessary columns
- Consider edge cases in data (special characters, boundaries, null values)
- Add descriptive examples table names

**Source:** `features/Contact.feature:15-17`

### Complex Data Scenarios

```gherkin
Scenario Outline: Users log in with invalid email or invalid password credentials
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  Then User sees error message

  @SalesManager
  Examples: SalesManager's username and password
    |username               |password    |
    |salesmanager6@info.com |saLesManager|
    |salesm27aners@info.com |salesmanager|
    |salesmanager8@info.com |sale@g@0fz8r|
    |salesmanage28@info.com |saleSM2na2er|
    |salesmanager10@info.com|SaLeSMaNaGeR|
```

**Note:** This example tests various invalid credential combinations including:
- Valid username with wrong password case
- Invalid username with valid password
- Special characters in passwords
- Typos in usernames

**Source:** `features/Login.feature:59-72`

## Tags: Test Organization and Filtering

Tags are labels prefixed with `@` that enable test organization, filtering, and metadata association.

### Tag Levels

Tags can be applied at multiple levels:

```gherkin
@Login                           # Feature-level tag
Feature: Testinium app login feature

  @UPGN-286                      # Scenario-level tag
  Scenario Outline: Users log in with valid credentials
    # ... scenario steps ...

    @SalesManager                # Examples-level tag
    Examples: SalesManager's username and password
      |username               |password    |
      |salesmanager7@info.com |salesmanager|
```

**Inheritance:** Tags inherit down the hierarchy:
- Feature-level tags apply to all scenarios in the file
- Scenario-level tags apply to all examples tables in that scenario
- Examples-level tags apply only to that specific examples table

**Source:** `features/Login.feature:1,13,20`

### Common Tag Patterns

**Feature Organization:**
```gherkin
@Login          # Feature area
@Calendar       # Feature module
@Contact        # Feature category
```

**Test Priorities:**
```gherkin
@Smoke          # Critical tests for every build
@Regression     # Full regression suite
@Sanity         # Quick validation tests
```

**Jira Integration:**
```gherkin
@UPGN-286       # Links to Jira ticket UPGN-286
@UPGN-287       # Links to Jira ticket UPGN-287
@UPGN-288       # Links to Jira ticket UPGN-288
```

**User Roles:**
```gherkin
@SalesManager   # Tests specific to SalesManager role
@PosManager     # Tests specific to PosManager role
```

**Source:** `features/Login.feature:1,13,20,37,58,85`

### Filtering Tests with Tags

Execute specific tests using the `--tags` option:

```bash
# Run all Login feature tests
behave --tags=@Login

# Run only SalesManager tests
behave --tags=@SalesManager

# Run specific Jira ticket tests
behave --tags=@UPGN-286

# Combine tags (AND logic)
behave --tags=@Login --tags=@SalesManager

# Exclude tags (NOT logic)
behave --tags=~@PosManager

# Complex expressions
behave --tags=@Login,@Calendar  # OR: Run Login OR Calendar
behave --tags=@Smoke --tags=~@WIP  # AND NOT: Run Smoke but not Work In Progress
```

**See Also:** [Behave Configuration Reference](../reference/behave-configuration.md)

### Tag Best Practices

1. **Use Consistent Naming Conventions**
   - PascalCase for feature areas: `@Login`, `@Calendar`
   - Uppercase for priorities: `@SMOKE`, `@REGRESSION`
   - Ticket format for Jira: `@UPGN-286`

2. **Create a Tag Hierarchy**
   - Feature → Module → Scenario → Examples
   - Broad → Specific

3. **Document Tag Meanings**
   - Maintain a tag glossary in your project documentation
   - Include tag purposes in team guidelines

4. **Avoid Tag Proliferation**
   - Too many tags reduce their value
   - Focus on meaningful categories
   - Review and prune unused tags regularly

## Comments in Feature Files

Use the `#` character to add comments. Comments are ignored during execution.

```gherkin
# This is a comment explaining the following scenarios

#1-Users can log in with valid credentials (We have 5 types of users but will test only 2 user: PosManager, SalesManager)
@UPGN-286
Scenario Outline: Users log in with valid credentials
  # Step comments can go here too
  When User enters "<username>" username
  And User enters "<password>" password
  And User clicks the login button
  Then User should see the dashboard
```

**Source:** `features/Login.feature:12-18`

**Comment Use Cases:**
- Explain complex scenarios or business rules
- Note test limitations or assumptions
- Provide context for test data
- Document known issues or workarounds
- Temporarily disable scenarios (prefix with `#`)

**Example - Commented Out Scenarios:**
```gherkin
Scenario: Verify that the user can delete a contact from 2 different side
  When User clicks list section and choose the profile
  And User clicks Action to choose delete button
#    And User clicks and goes directly to the profile
#    And User clicks Action to choose delete button
  Then User sees deleted profile
```

**Source:** `features/Contact.feature:19-24`

**Note:** Commented-out steps often indicate work in progress or disabled functionality. Consider using `@WIP` or `@Skip` tags instead for better visibility.

## Best Practices for Writing Readable Scenarios

### 1. Use Declarative Style (Not Imperative)

**Good - Declarative (What):**
```gherkin
Given User is logged in as Sales Manager
When User creates a new contact
Then User should see the contact in the dashboard
```

**Avoid - Imperative (How):**
```gherkin
Given User navigates to login page
And User enters username in the username field
And User enters password in the password field
And User clicks the login button
And User waits for dashboard to load
When User clicks on the Contacts menu
And User clicks on the Create button
# ... too many implementation details
```

**Why:** Declarative style focuses on behavior, not implementation. It's more maintainable and readable.

### 2. Use Business Language, Not Technical Details

**Good:**
```gherkin
When User creates an event for "Project Meeting"
Then User should see the event on the calendar
```

**Avoid:**
```gherkin
When User clicks element with ID "event-create-btn"
And User types "Project Meeting" in input field "event-title"
And User clicks CSS selector ".save-button"
Then Element with xpath "//div[@class='calendar-event']" should be visible
```

**Why:** Feature files are documentation for stakeholders. Use domain language, not technical locators.

### 3. One Scenario = One Test Case

**Good:**
```gherkin
Scenario: User can create a new contact
  When User creates a contact with name "John Doe"
  Then User should see "John Doe" in the contact list

Scenario: User can delete a contact
  Given User has a contact "John Doe"
  When User deletes the contact "John Doe"
  Then User should not see "John Doe" in the contact list
```

**Avoid:**
```gherkin
Scenario: User can create, edit, and delete a contact
  When User creates a contact with name "John Doe"
  Then User should see "John Doe" in the contact list
  When User edits the contact to "Jane Doe"
  Then User should see "Jane Doe" in the contact list
  When User deletes the contact "Jane Doe"
  Then User should not see "Jane Doe" in the contact list
```

**Why:** Each scenario should test one behavior. Multiple behaviors in one scenario make debugging harder and reduce test independence.

### 4. Use Meaningful Examples

**Good:**
```gherkin
Examples: Valid email formats
  | email                    |
  | user@example.com         |
  | user.name@example.co.uk  |
  | user+tag@example.com     |
```

**Avoid:**
```gherkin
Examples:
  | email           |
  | test1@test.com  |
  | test2@test.com  |
  | test3@test.com  |
```

**Why:** Meaningful data reveals test intent. Each example should demonstrate a specific case or edge condition.

### 5. Keep Scenarios Independent

**Good:**
```gherkin
Scenario: User can edit a contact
  Given User has a contact "John Doe"  # Scenario creates its own precondition
  When User edits the contact to "Jane Doe"
  Then User should see "Jane Doe" in the contact list
```

**Avoid:**
```gherkin
Scenario: User can create a contact
  When User creates a contact "John Doe"
  Then User should see "John Doe"

Scenario: User can edit a contact  # Depends on previous scenario
  When User edits the contact to "Jane Doe"
  Then User should see "Jane Doe"
```

**Why:** Scenarios should not depend on execution order. Each should be runnable independently.

### 6. Use Background for Common Preconditions

**Good:**
```gherkin
Background:
  Given User is logged in as PosManager

Scenario: User can create event
  When User creates a calendar event
  Then User should see the event

Scenario: User can edit event
  When User edits a calendar event
  Then User should see the changes
```

**Avoid - Repeated Steps:**
```gherkin
Scenario: User can create event
  Given User is logged in as PosManager
  When User creates a calendar event
  Then User should see the event

Scenario: User can edit event
  Given User is logged in as PosManager
  When User edits a calendar event
  Then User should see the changes
```

**Why:** Background eliminates repetition and highlights what's common vs. what's specific to each scenario.

## Feature File Organization Strategies

### One Feature Per File

Each `.feature` file should focus on a single feature or module:

```
features/
├── Login.feature          # Authentication functionality
├── Calendar.feature       # Calendar management
├── Contact.feature        # Contact operations
├── Inventory.feature      # Inventory management
├── Sales.feature          # Sales workflows
└── ...
```

**Benefits:**
- Easier to locate tests
- Clearer test organization
- Better parallel execution
- Simpler maintenance

### Grouping Related Scenarios

Within a feature file, group related scenarios logically:

```gherkin
Feature: Login functionality

  # Positive test cases
  Scenario Outline: Valid login credentials
    # ...

  # Negative test cases - Invalid credentials
  Scenario Outline: Invalid username or password
    # ...

  # Negative test cases - Empty fields
  Scenario Outline: Empty username or password
    # ...

  # UI validation
  Scenario: Password displayed in bullet signs
    # ...
```

**Organization Patterns:**
- Positive cases first, then negative cases
- Happy path before edge cases
- Group by test type (functional, UI, security)
- Order by user journey flow

**Source:** `features/Login.feature` (scenarios organized by test type)

### Logical Tag Hierarchy

Create a consistent tag structure:

```
@Login                          # Level 1: Feature
  @UPGN-286                     # Level 2: Jira ticket
    @SalesManager               # Level 3: User role
    @PosManager                 # Level 3: User role
  @UPGN-287                     # Level 2: Jira ticket
    @SalesManager
    @PosManager
```

**Benefits:**
- Flexible test selection
- Clear test categorization
- Easy reporting by category
- Better CI/CD integration

## Complete Feature File Examples

### Example 1: Login Feature with Multiple Test Types

```gherkin
@Login
Feature: Testinium app login feature

  User Story:
  As a user, I should be able to login with correct credentials to different accounts.

  Accounts are: PosManager, SalesManager

  Background: For the scenarios in the feature file, user is expected to be on login page
    Given User is on the upgenix login page

  # Positive test case - Valid login
  @UPGN-286
  Scenario Outline: Users log in with valid credentials
    When User enters "<username>" username
    And User enters "<password>" password
    And User clicks the login button
    Then User should see the dashboard

    @SalesManager
    Examples: SalesManager's username and password
      |username               |password    |
      |salesmanager7@info.com |salesmanager|
      |salesmanager8@info.com |salesmanager|

    @PosManager
    Examples: PosManager's username and password
      |username             |password  |
      |posmanager5@info.com |posmanager|
      |posmanager6@info.com |posmanager|

  # Negative test case - Invalid credentials
  @UPGN-287
  Scenario Outline: Users log in with invalid credentials
    When User enters "<username>" username
    And User enters "<password>" password
    And User clicks the login button
    Then User sees error message

    @SalesManager
    Examples: Invalid SalesManager credentials
      |username               |password    |
      |salesmanager6@info.com |wrongpass   |
      |wronguser@info.com     |salesmanager|

  # UI validation test
  @UPGN-289
  Scenario Outline: User should see the password in bullet signs by default
    When User enters "<password>" password
    Then User should see the password in bullet signs

    @SalesManager
    Examples: Test password masking
      |password    |
      |saLesManager|
```

**Source:** `features/Login.feature:1-119` (condensed for example)

### Example 2: Calendar Feature with Simple Scenarios

```gherkin
@Calendar
Feature: Testinium app Calendar Module

  Account is: PosManager
  Background: As a Posmanager, I should be able to create and to see my meetings and events on my calendar from "Calendar" module
              For this ERP application, the calendar function is very crucial.
              Anyone in the team can contribute and plan their agenda using the calendar.
              To prevent any conflict, events should be created, edited and displayed by all team members.
  Given User login to test other features

  Scenario: Verify that all buttons work as expected at the Calendar stage
    When User click on the calendar dashboard
    And User click on day button
    And User click on week button
    And User click on month button
    Then User should see the last stage of calendar view

  Scenario: User can change display between Day-Week-Month
    When User click on the calendar dashboard
    And User click day on the calendar and display day
    Then User click month on the calendar and display month

  Scenario Outline: User can create event by clicking on daily time box
    When User click on the calendar dashboard
    And User click day on the calendar and display day
    And User click on desired date time
    Then User enters "<test>" in the box and clicks the create button

    Examples: Test name
      |test       |
      |Test test  |
```

**Source:** `features/Calendar.feature:1-31`

### Example 3: Contact Feature with CRUD Operations

```gherkin
Feature: Testinium app Contact feature

  User Story:
  Background: As a Posmanager, should be able to create, delete, edit a contact and change the colour of the new contact
  Given User login to test other features
  Given User is at Contact dashboard

  Scenario Outline: Verify that the user can create a new contact
    When User clicks the create button
    And User enters name "<name>"
    And User enters "<street name>"
    And User enters "<phone number>" and "<email>"
    And User clicks save button
    Then User sees the created new contact details at dashboard
    Examples:
      | name   |  street name |   phone number | email        |
      | &Dustin|  Haussman    |   +99999999999 | abcd@info.com|

  Scenario: Verify that the user can delete a contact
    When User clicks list section and choose the profile
    And User clicks Action to choose delete button
    Then User sees deleted profile

  Scenario Outline: Verify that the user can edit the contact
    When User selects the profile
    And User clicks for editing button
    And User enters name "<name>"
    And User enters "<street name>"
    And User enters "<phone number>" and "<email>"
    And User clicks save button
    Then User sees the updated contact details at dashboard
    Examples:
      | name   |  street name |   phone number | email        |
      | &Dustin|  Haussman    |   +99999999999 | abcd@info.com|
```

**Source:** `features/Contact.feature:1-36`

## Troubleshooting Common Gherkin Issues

### Issue 1: Step Definition Not Found

**Symptoms:**
```
Step does not have a matching step definition:
  When User enters "test@example.com" username
```

**Causes:**
- Step definition doesn't exist
- Step text doesn't match the regex pattern
- Step definition file not in `features/steps/` directory
- Typo in step text

**Solutions:**

1. **Check step definition exists:**
```bash
grep -r "User enters.*username" features/steps/
```

2. **Verify step pattern matches:**
```python
# In features/steps/login_steps.py
@when('User enters "{username}" username')
def step_enter_username(context, username):
    # Implementation
```

3. **Check for typos:**
   - Compare feature file step with step definition exactly
   - Watch for extra spaces, punctuation differences
   - Parameter placeholders must match

4. **Verify step file is discovered:**
```bash
# All .py files in features/steps/ are auto-discovered
ls features/steps/*.py
```

**See Also:** [Writing Step Definitions Guide](step-definitions.md)

### Issue 2: Examples Table Parsing Errors

**Symptoms:**
```
ParserError: Failed to parse Examples table
```

**Causes:**
- Missing pipe `|` characters
- Misaligned columns
- Missing header row
- Empty cells without placeholders

**Solutions:**

1. **Verify table syntax:**
```gherkin
# Correct format
Examples:
  | username         | password  |
  | user1@email.com  | pass123   |
  | user2@email.com  | pass456   |

# Incorrect - missing closing pipes
Examples:
  | username         | password
  | user1@email.com  | pass123
```

2. **Check header matches placeholders:**
```gherkin
Scenario Outline: Login test
  When User enters "<username>" username
  # Header MUST have "username" column
  
  Examples:
    | username         |  # Column name matches <username>
    | user@example.com |
```

3. **Handle special characters:**
```gherkin
# Special characters in data are fine
Examples:
  | name    | email           |
  | &Dustin | abcd@info.com   |  # & character is OK
```

### Issue 3: Tag Filtering Not Working

**Symptoms:**
- Tests run when they shouldn't with `--tags` option
- Expected tests don't execute

**Causes:**
- Tag syntax error (missing `@`)
- Tag inheritance not understood
- Incorrect tag expression

**Solutions:**

1. **Verify tag syntax:**
```gherkin
# Correct
@Login
Feature: Login tests

# Incorrect - missing @
Login
Feature: Login tests
```

2. **Understand tag inheritance:**
```gherkin
@Login                    # All scenarios inherit this
Feature: Login

  @UPGN-286              # This scenario has: @Login, @UPGN-286
  Scenario Outline: Test
    
    @SalesManager        # This example has: @Login, @UPGN-286, @SalesManager
    Examples:
```

3. **Use correct tag expressions:**
```bash
# OR logic (comma)
behave --tags=@Login,@Calendar    # Runs Login OR Calendar

# AND logic (multiple --tags)
behave --tags=@Login --tags=@Smoke  # Runs Login AND Smoke

# NOT logic (tilde)
behave --tags=~@WIP               # Runs everything EXCEPT @WIP

# Complex
behave --tags=@Login --tags=@Smoke,@Regression
# Runs: (@Login) AND (@Smoke OR @Regression)
```

### Issue 4: Background Steps Failing

**Symptoms:**
- All scenarios in a feature fail
- Failure occurs before scenario steps execute

**Causes:**
- Background step has error
- Precondition not met
- Background too complex

**Solutions:**

1. **Debug background steps:**
```gherkin
Background:
  Given User is on the upgenix login page  # If this fails, all scenarios fail
```

2. **Keep background minimal:**
```gherkin
# Good - simple precondition
Background:
  Given User login to test other features

# Avoid - complex background
Background:
  Given User is on the login page
  And User enters username
  And User enters password
  And User clicks login
  And User navigates to dashboard
  And User waits 5 seconds
  # Too many steps - consider making this a reusable step definition
```

3. **Verify background runs before each scenario:**
   - Background is NOT run once per feature
   - It runs before EVERY scenario
   - Keep it fast to avoid slowing down tests

### Issue 5: Scenario Outline Not Parameterizing

**Symptoms:**
- Literal `<parameter>` text appears instead of values
- Steps fail with "element not found" using literal placeholder text

**Causes:**
- Placeholder name doesn't match Examples header
- Missing Examples table
- Typo in placeholder or header

**Solutions:**

1. **Match placeholders to headers exactly:**
```gherkin
Scenario Outline: Test
  When User enters "<username>" username  # Placeholder name
  
  Examples:
    | username         |  # Header MUST match exactly
    | user@example.com |
```

2. **Check for typos:**
```gherkin
# Incorrect - placeholder vs header mismatch
Scenario Outline: Test
  When User enters "<user_name>" username  # underscore
  
  Examples:
    | username  |  # no underscore - MISMATCH
```

3. **Verify Examples table exists:**
```gherkin
# Incomplete - missing Examples
Scenario Outline: Test
  When User enters "<username>" username
  # ERROR: No Examples table provided
```

**See Also:** 
- [Behave Configuration Reference](../reference/behave-configuration.md)
- [Gherkin Syntax Reference](../reference/gherkin-syntax.md)
- [Common Errors Troubleshooting](../troubleshooting/common-errors.md)

## Implementing Step Definitions

Once you've written your feature file, you need to implement the step definitions that execute the test logic.

### Step Definition Basics

Each Gherkin step must have a corresponding step definition in Python:

```gherkin
# In features/Login.feature
Given User is on the upgenix login page
When User enters "test@example.com" username
Then User should see the dashboard
```

```python
# In features/steps/login_steps.py
from behave import given, when, then

@given('User is on the upgenix login page')
def step_navigate_to_login(context):
    context.driver.get(context.config.base_url + "/login")

@when('User enters "{username}" username')
def step_enter_username(context, username):
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)

@then('User should see the dashboard')
def step_verify_dashboard(context):
    dashboard_page = DashboardPage(context.driver)
    assert dashboard_page.is_displayed()
```

**Key Points:**
- Step definitions go in `features/steps/` directory
- Use decorators: `@given`, `@when`, `@then`, `@step`
- Parameter placeholders `"<param>"` become function arguments
- Access shared state via `context` object

**Complete Guide:** [Writing Step Definitions](step-definitions.md)

### Connecting Features to Step Definitions

**Discovery Process:**
1. Behave scans `features/steps/` directory for `*.py` files
2. Collects all functions decorated with `@given`, `@when`, `@then`, `@step`
3. Matches feature file steps to step definition patterns
4. Executes matched step definition when step runs

**Matching Rules:**
- Exact text match (case-sensitive)
- Regex patterns for flexibility
- Parameter capture with quotes or regex groups

**Example Matching:**
```gherkin
# Feature file step
When User enters "salesmanager7@info.com" username

# Matches this step definition
@when('User enters "{username}" username')
def step_impl(context, username):
    # username = "salesmanager7@info.com"
```

### Page Object Integration

Step definitions should use Page Objects for UI interactions:

```python
from pages.login_page import LoginPage

@when('User enters "{username}" username')
def step_enter_username(context, username):
    # Use Page Object instead of direct WebDriver calls
    login_page = LoginPage(context.driver)
    login_page.input_email.send_keys(username)
```

**Benefits:**
- Separates test logic from UI locators
- Improves maintainability
- Enables code reuse
- Makes step definitions readable

**Complete Guide:** [Page Object Model Guide](page-object-model.md)

## Advanced Gherkin Patterns

### Reusable Step Definitions

Write generic step definitions that work across multiple features:

```python
# Generic step usable in any feature
@when('User enters "{text}" in the "{field_name}" field')
def step_enter_text_in_field(context, text, field_name):
    # Dynamic field lookup
    element = context.current_page.get_field(field_name)
    element.send_keys(text)
```

### Data Tables in Steps

Pass structured data to steps using tables:

```gherkin
Scenario: Create contact with complete information
  When User creates a contact with details:
    | Field        | Value              |
    | Name         | John Doe           |
    | Email        | john@example.com   |
    | Phone        | +1234567890        |
    | Street       | 123 Main St        |
  Then User should see the contact
```

```python
@when('User creates a contact with details')
def step_create_contact_with_table(context):
    # Access table data
    for row in context.table:
        field = row['Field']
        value = row['Value']
        # Use field and value
```

### Doc Strings for Large Text

Pass multi-line text to steps:

```gherkin
Scenario: Add note with formatted text
  When User adds a note with content:
    """
    This is a multi-line note.
    
    It can contain multiple paragraphs.
    And special characters: @#$%
    """
  Then User should see the note
```

```python
@when('User adds a note with content')
def step_add_note_with_text(context):
    # Access doc string
    note_text = context.text
    # Use note_text
```

## Feature File Checklist

Before committing your feature file, verify:

- [ ] **Feature keyword** with clear, concise title
- [ ] **User story** or description explaining business value
- [ ] **Feature-level tag** for categorization (e.g., `@Login`)
- [ ] **Background** section if common preconditions exist
- [ ] **Scenarios** with descriptive names
- [ ] **Scenario Outlines** for data-driven tests
- [ ] **Examples tables** with meaningful data
- [ ] **Tags** for organization (Jira tickets, priorities, roles)
- [ ] **Declarative steps** using business language
- [ ] **Independent scenarios** that can run in any order
- [ ] **Comments** explaining complex scenarios or business rules
- [ ] **Corresponding step definitions** implemented
- [ ] **Tests pass** when run with behave

## Summary

Gherkin feature files provide a bridge between business requirements and automated tests. Key takeaways:

**Structure:**
- Feature → Background → Scenarios → Steps
- Use Scenario for single cases, Scenario Outline for data-driven tests
- Examples tables parameterize scenario outlines

**Organization:**
- One feature per file
- Group related scenarios logically
- Use tags for filtering and categorization
- Apply consistent naming conventions

**Best Practices:**
- Write in declarative style (what, not how)
- Use business language, not technical details
- Keep scenarios independent and focused
- Make examples meaningful and representative
- Keep background minimal and fast

**Implementation:**
- Connect to step definitions in `features/steps/`
- Use Page Objects in step definitions
- Leverage behave's context for shared state
- Test features thoroughly before committing

## See Also

**Related Guides:**
- [Writing Step Definitions](step-definitions.md) - Implementing Gherkin steps in Python
- [Page Object Model Guide](page-object-model.md) - Creating maintainable page objects
- [Parallel Execution Guide](parallel-execution.md) - Running features in parallel
- [Authentication Testing Guide](authentication-testing.md) - Login feature example

**API Reference:**
- [Step Definitions API](../api-reference/steps/index.md) - All available step definitions
- [Behave Environment Hooks](../api-reference/features/environment.md) - Before/after hooks

**Configuration:**
- [Behave Configuration Reference](../reference/behave-configuration.md) - behave.ini options
- [Command Reference](../reference/command-reference.md) - behave CLI commands
- [Gherkin Syntax Reference](../reference/gherkin-syntax.md) - Complete Gherkin keywords

**Troubleshooting:**
- [Common Errors](../troubleshooting/common-errors.md) - Frequent issues and solutions
- [Configuration Issues](../troubleshooting/configuration-issues.md) - Config problems

**Source Files Referenced:**
- `features/Login.feature` - Comprehensive login testing examples
- `features/Calendar.feature` - Calendar module scenarios
- `features/Contact.feature` - Contact management examples

