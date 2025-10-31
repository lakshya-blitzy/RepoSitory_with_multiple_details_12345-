# Gherkin Syntax Reference

## Overview

Gherkin is a Business Readable, Domain Specific Language (DSL) used to describe application behavior in a way that is understandable to both technical and non-technical stakeholders. It serves as the language for writing BDD (Behavior Driven Development) feature files in the Testinium QA Python framework.

**Purpose:**
- Bridge communication between developers, testers, and business stakeholders
- Create executable specifications that serve as both documentation and automated tests
- Express application behavior in plain, human-readable language
- Enable data-driven testing through parameterization

**Key Characteristics:**
- Uses natural language constructs
- Focuses on business value and user behavior
- Supports multiple spoken languages (English is standard)
- Structured format that can be parsed by automation tools (Behave)
- Living documentation that evolves with the application

**File Format:**
- File extension: `.feature`
- Location: `features/` directory
- Encoding: UTF-8
- Line-based structure with keywords at the start of lines

## Gherkin Keywords

Gherkin uses a set of special keywords to structure feature files. Each keyword has a specific purpose in describing application behavior.

### Core Keywords

| Keyword | Purpose | Required | Occurrence |
|---------|---------|----------|------------|
| `Feature` | Describes the feature being tested | Yes | Once per file |
| `Scenario` | Describes a single test case | Yes | One or more per feature |
| `Scenario Outline` | Describes a parameterized test case | No | Zero or more per feature |
| `Background` | Common setup steps for all scenarios | No | Zero or one per feature |
| `Given` | Preconditions or initial state | Yes (in scenarios) | One or more per scenario |
| `When` | Actions or events | Yes (in scenarios) | One or more per scenario |
| `Then` | Expected outcomes or assertions | Yes (in scenarios) | One or more per scenario |
| `And` | Additional steps (continues previous keyword) | No | Zero or more |
| `But` | Additional steps with negative connotation | No | Zero or more |
| `Examples` | Data tables for Scenario Outline | Yes (with Scenario Outline) | One or more per outline |

### Secondary Keywords

| Keyword | Purpose | Usage |
|---------|---------|-------|
| `*` (asterisk) | Step keyword wildcard (treated as any step type) | Alternative to Given/When/Then |
| `"""` (doc strings) | Multi-line string arguments | Embedded in steps |
| `\|` (pipe) | Table delimiters | Data tables in steps |
| `@` | Tags for organizing and filtering tests | Before Feature or Scenario |
| `#` | Comments (ignored by parser) | Anywhere in file |

**Source:** `features/Login.feature`, `features/Crm.feature`, `features/EmployeeFc.feature`

## Feature Keyword

The `Feature` keyword is the top-level structure of a Gherkin file. It provides high-level documentation about the feature being tested and groups related scenarios together.

### Syntax

```gherkin
@FeatureTags
Feature: Short description of the feature

  Optional longer description
  that can span multiple lines
  
  Scenarios go here...
```

### Components

1. **Feature Tags** (optional): One or more tags preceding the Feature keyword
2. **Feature Name**: Short, descriptive title on the same line as the keyword
3. **Feature Description** (optional): Multi-line description providing context
4. **Scenarios**: One or more Scenario or Scenario Outline blocks

### Example from Login Feature

```gherkin
@Login
Feature: Testinium app login feature

  User Story:
  As a user, I should be able to login with correct credentials to different accounts.

  Accounts are: PosManager, SalesManager
```

**Source:** `features/Login.feature:1-7`

### User Story Format

The feature description often includes a user story following the standard format:

```
As a [role]
I want [feature]
So that [benefit]
```

This format clearly communicates:
- **Who** is using the feature (role/persona)
- **What** they want to accomplish (feature)
- **Why** they need it (business value)

### Example from CRM Feature

```gherkin
@Smoke
Feature: Testinium app CRM Module

  Account is: PosManager
```

**Source:** `features/Crm.feature:1-4`

### Example from Employees Feature

```gherkin
@UPGN-344
Feature: Testinium app Employees module

  Account is: PosManager
```

**Source:** `features/EmployeeFc.feature:1-4`

### Best Practices for Feature

- **Concise Title**: Keep the feature name short and descriptive (under 100 characters)
- **Clear Description**: Provide enough context for anyone to understand the feature's purpose
- **Business Language**: Use business terminology, not technical implementation details
- **User-Centric**: Focus on user value and business outcomes
- **Consistent Format**: Maintain consistent feature description format across all feature files

---

## Background Keyword

The `Background` keyword allows you to define common setup steps that run before each scenario in the feature file. It reduces repetition by extracting shared preconditions.

### Syntax

```gherkin
Background: Optional description of the background
  Given [precondition step]
  And [additional precondition step]
```

### Purpose

- **DRY Principle**: Don't Repeat Yourself - avoid duplicating setup steps across scenarios
- **Test Context**: Establish the initial state required for all scenarios in the feature
- **Readability**: Make scenarios more concise by moving common setup to Background

### When to Use Background

**Use Background when:**
- Multiple scenarios in the feature share the same preconditions
- Setup steps are required for all or most scenarios
- The shared steps represent a common starting point

**Don't use Background when:**
- Only one or two scenarios need the setup
- Different scenarios require significantly different setup
- Background would make the feature file harder to understand

### Example from Login Feature

```gherkin
Background: For the scenarios in the feature file, user is expected to be on login page
  Given User is on the upgenix login page
```

**Source:** `features/Login.feature:9-10`

This Background ensures all login test scenarios start from the login page, eliminating the need to repeat this step in each scenario.

### Example from CRM Feature

```gherkin
Background: As a Posmanager, I should be able to create and to see my pipeline and custommers on my customers from "CRM" module.
  Given User login to test other features
```

**Source:** `features/Crm.feature:6-7`

This Background handles authentication once, so all CRM scenarios can focus on testing CRM functionality.

### Example from Employees Feature

```gherkin
Background: As a Posmanager, I should be able to create and edit a new employee from "Employees" module
```

**Source:** `features/EmployeeFc.feature:5`

### Background Execution Flow

1. Before each scenario, Behave runs all Background steps
2. If Background fails, the scenario is skipped
3. Background runs before each data row in Scenario Outline
4. Background steps appear in test reports for each scenario

### Best Practices for Background

- **Keep It Short**: Limit to essential setup steps (typically 1-5 steps)
- **Universal Setup**: Only include steps needed by all scenarios
- **Fast Execution**: Avoid slow operations that run repeatedly
- **Clear Context**: Use descriptive Background description
- **Consider Hooks**: For complex setup, use Behave hooks (`before_scenario`) instead

---

## Scenario Keyword

The `Scenario` keyword defines a single test case that describes specific behavior of the application. Each scenario represents one concrete example of how the feature should work.

### Syntax

```gherkin
@ScenarioTags
Scenario: Description of the test case
  Given [precondition]
  When [action]
  Then [expected outcome]
```

### Structure

A scenario consists of:
1. **Tags** (optional): Organize and filter scenarios
2. **Scenario Title**: Clear description of what is being tested
3. **Steps**: Series of Given/When/Then statements

### Step Keywords

#### Given - Preconditions

**Purpose**: Establish the initial state before the test action

**Usage**: Describe the context and preconditions

**Examples:**
```gherkin
Given User is on the upgenix login page
Given User login to test other features
Given User is on the dashboard
```

**When to use Given:**
- Setting up test data
- Navigating to a starting page
- Logging in as a user
- Configuring system state

#### When - Actions

**Purpose**: Describe the action or event that triggers the behavior being tested

**Usage**: User interactions, system events, or time passing

**Examples:**
```gherkin
When User enters "salesmanager7@info.com" username
When User clicks the login button
When User click on the crm dashboard
When User creates new employees "Cristiano Ronaldo" in the Employees stage
```

**When to use When:**
- User clicking buttons or links
- User entering data in forms
- User selecting options
- System processing events
- API calls or background jobs

#### Then - Expected Outcomes

**Purpose**: Verify the expected result of the action

**Usage**: Assertions and validations

**Examples:**
```gherkin
Then User should see the dashboard
Then User sees error message
Then User should see the Employee created message under full profile
Then User can print the profile
```

**When to use Then:**
- Verifying UI elements are visible
- Checking values are correct
- Validating system state
- Confirming expected outcomes

#### And / But - Continuing Steps

**Purpose**: Add additional steps without repeating Given/When/Then

**Usage**: Continue the previous step type

**Examples:**
```gherkin
Given User is on the upgenix login page
When User enters "salesmanager7@info.com" username
And User enters "salesmanager" password
And User clicks the login button
Then User should see the dashboard
```

**Note**: `And` continues the logic of the previous step. After `When`, `And` means another action. After `Then`, `And` means another assertion.

### Example: Simple Scenario from CRM Feature

```gherkin
Scenario: User can create pipeline in the displayed dashboard
  When User click on the crm dashboard
  And User click on the pipeline button
  And User can create the new pipeline
  And User can see the total price
  Then User can see new pipeline
```

**Source:** `features/Crm.feature:9-14`

This scenario tests pipeline creation with a sequence of actions followed by verification.

### Example: Multi-Step Scenario from Employees Feature

```gherkin
@UPGN-340
Scenario: Verify that all buttons work as expected at the employees stage
  When User is on the dashboard
  And User clicks Employees stage
  And User clicks Challenges stage
  And User clicks Departments stage
  Then User should see the last stage title
```

**Source:** `features/EmployeeFc.feature:8-13`

### Best Practices for Scenarios

- **Descriptive Titles**: Clearly state what is being tested
- **Single Focus**: Each scenario should test one specific behavior
- **Present Tense**: Use present tense for steps ("User clicks" not "User clicked")
- **Declarative over Imperative**: Focus on what, not how (avoid UI implementation details)
- **Atomic Steps**: Each step should be a single, clear action or assertion
- **Logical Flow**: Follow Given-When-Then order for clarity
- **Realistic Data**: Use meaningful test data that represents real usage

---

## Scenario Outline Keyword

The `Scenario Outline` keyword enables data-driven testing by allowing you to run the same scenario multiple times with different input values. This is essential for testing the same behavior with various data combinations.

### Syntax

```gherkin
@OutlineTags
Scenario Outline: Description of the parameterized test
  Given [step with <parameter>]
  When [step with <parameter>]
  Then [expected outcome]

  @ExampleTags
  Examples: Description of the data set
    | parameter1 | parameter2 |
    | value1     | value2     |
    | value3     | value4     |
```

### Components

1. **Scenario Outline**: The template scenario with parameters in `<angle_brackets>`
2. **Parameters**: Placeholders that will be replaced with actual values
3. **Examples**: One or more data tables providing values for each parameter
4. **Tags**: Can be applied to the outline, individual examples, or both

### Parameter Substitution

Parameters are defined using angle brackets: `<parameter_name>`

**In steps:**
```gherkin
When User enters "<username>" username
And User enters "<password>" password
```

**In Examples table:**
```gherkin
Examples: Test data
  | username                | password     |
  | salesmanager7@info.com  | salesmanager |
```

Each row in the Examples table generates one scenario execution with those values.

### Example: Login with Valid Credentials

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
    |username               |password  |
    |posmanager5@info.com   |posmanager|
    |posmanager6@info.com   |posmanager|
    |posmanager7@info.com   |posmanager|
```

**Source:** `features/Login.feature:14-50`

This Scenario Outline generates **7 scenarios** total:
- 4 scenarios for SalesManager data (lines 23-26)
- 3 scenarios for PosManager data (lines 40-42)

### Example: Multiple Parameters with CRM Data

```gherkin
Scenario Outline: User can change information in dashboard
  When User click on the crm dashboard
  And User can change any user's information like "<opportunity>" , "<revenue>" and "<probability>"
  And User can save information
  Then User can verify the information

  Examples: Expected name
    | opportunity | revenue | probability |
    | Test2       | 30      | 2           |
```

**Source:** `features/Crm.feature:16-24`

This demonstrates using three different parameters in a single scenario.

### Example: Employee Creation with Names

```gherkin
@UPGN-341
Scenario Outline: Verify that the "Employee created" message appears under full profile
  When User is on the employees dashboard
  And User creates new employees "<name>" in the Employees stage
  Then User should see the Employee created message under full profile

  Examples: Employee's name
    |name               |
    |Cristiano Ronaldo  |
```

**Source:** `features/EmployeeFc.feature:16-23`

### Multiple Examples Groups

A Scenario Outline can have multiple Examples blocks, each with its own tag and description:

```gherkin
@UPGN-287
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

  @PosManager
  Examples: PosManager's username and password
    |username               |password   |
    |posmanager5@info.com   |posmanager1|
    |posmanagerr6@info.com  |posmanager |
    |posmanger8@info.com    |posmager   |
```

**Source:** `features/Login.feature:58-81`

### Best Practices for Scenario Outline

- **Meaningful Parameters**: Use descriptive parameter names (not param1, param2)
- **Consistent Format**: Align table columns for readability
- **Descriptive Examples**: Provide clear descriptions for each Examples block
- **Appropriate Tags**: Tag examples groups for filtering (e.g., @SalesManager, @PosManager)
- **Coverage**: Include edge cases and boundary values in examples
- **Maintainable**: Keep examples tables manageable (typically under 20 rows)
- **Grouped Data**: Use multiple Examples blocks to group related test data

---

## Examples Tables

The `Examples` keyword defines data tables for Scenario Outline. Each row (except the header) creates one scenario execution with those parameter values.

### Syntax

```gherkin
Examples: Description of the data set
  | parameter1 | parameter2 | parameter3 |
  | value1a    | value2a    | value3a    |
  | value1b    | value2b    | value3b    |
```

### Table Structure

1. **Header Row**: Column names matching parameters in the Scenario Outline (must use exact same names)
2. **Data Rows**: Each row represents one set of test data
3. **Delimiters**: Pipe characters (`|`) separate columns
4. **Spacing**: Spaces around values improve readability (optional)

### Parameter Matching

**Parameters must match exactly** (case-sensitive):

```gherkin
Scenario Outline: Example
  When User enters "<username>" username
  # Parameter name is "username"

Examples: Data
  | username              |  # Column must be exactly "username"
  | test@example.com      |
```

### Single Column Examples

```gherkin
@UPGN-288
Scenario Outline:Users log in with invalid email or invalid password credentials
  When User enters "<password>" username
  And User clicks the login button
  Then User sees "Veuillez renseigner ce champ." message

  @SalesManager
  Examples: SalesManager's username and password
    |password    |
    |salesmanager|

  @PosManager
  Examples: PosManager's username and password
    |password    |
    |posmanager  |
```

**Source:** `features/Login.feature:85-99`

### Multi-Column Examples

```gherkin
Examples: Expected name
  | opportunity | revenue | probability |
  | Test2       | 30      | 2           |
```

**Source:** `features/Crm.feature:22-24`

### Large Data Sets

For comprehensive testing, Examples tables can contain many rows:

```gherkin
@SalesManager
Examples: SalesManager's username and password
  |username               |password    |
  |salesmanager7@info.com |salesmanager|
  |salesmanager8@info.com |salesmanager|
  |salesmanager9@info.com |salesmanager|
  |salesmanager10@info.com|salesmanager|
  |salesmanager11@info.com|salesmanager|
  |salesmanager12@info.com|salesmanager|
  |salesmanager13@info.com|salesmanager|
  |salesmanager14@info.com|salesmanager|
  |salesmanager15@info.com|salesmanager|
  |salesmanager16@info.com|salesmanager|
  |salesmanager17@info.com|salesmanager|
  |salesmanager18@info.com|salesmanager|
  |salesmanager19@info.com|salesmanager|
```

**Source:** `features/Login.feature:21-35`

This generates **13 separate scenario executions**, one for each data row.

### Best Practices for Examples Tables

- **Header Clarity**: Use descriptive column names that match parameter names exactly
- **Alignment**: Align columns for visual clarity (Behave ignores extra whitespace)
- **Data Quality**: Use realistic, meaningful test data
- **Coverage**: Include positive cases, negative cases, edge cases, and boundary values
- **Organization**: Group related data in separate Examples blocks with descriptive names
- **Maintainability**: Keep tables manageable; consider external data files for very large datasets
- **Comments**: Add comments above Examples to explain test data rationale

---

## Tags

Tags are annotations prefixed with `@` that allow you to organize, categorize, and filter scenarios. They are essential for test management and selective execution.

### Syntax

```gherkin
@TagName
@AnotherTag @MultipleTagsOnOneLine
Feature: Feature name
```

Tags can be placed:
- Before `Feature` - applies to all scenarios in the feature
- Before `Scenario` or `Scenario Outline` - applies to that specific scenario
- Before `Examples` - applies to only those example rows

### Tag Types and Usage

#### Feature-Level Tags

Tags applied to the entire feature:

```gherkin
@Login
Feature: Testinium app login feature
```

**Source:** `features/Login.feature:1-2`

```gherkin
@Smoke
Feature: Testinium app CRM Module
```

**Source:** `features/Crm.feature:1-2`

**Usage**: Categorize features by functional area, test priority, or module.

#### Scenario-Level Tags

Tags applied to individual scenarios:

```gherkin
@UPGN-286
Scenario Outline: Users log in with valid credentials
```

**Source:** `features/Login.feature:13-14`

```gherkin
@UPGN-340
Scenario: Verify that all buttons work as expected at the employees stage
```

**Source:** `features/EmployeeFc.feature:8`

#### Examples-Level Tags

Tags applied to specific data sets:

```gherkin
@SalesManager
Examples: SalesManager's username and password
  |username               |password    |
  |salesmanager7@info.com |salesmanager|
```

**Source:** `features/Login.feature:20-23`

```gherkin
@PosManager
Examples: PosManager's username and password
  |username               |password  |
  |posmanager5@info.com   |posmanager|
```

**Source:** `features/Login.feature:37-40`

### Tag Categories

#### 1. Jira Integration Tags

Tags that reference issue tracking system tickets:

```gherkin
@UPGN-286
@UPGN-287
@UPGN-288
@UPGN-289
@UPGN-290
@UPGN-340
@UPGN-341
@UPGN-342
@UPGN-343
@UPGN-344
```

**Purpose**: Link scenarios to Jira tickets for traceability

**Usage**: `behave --tags=@UPGN-286` runs scenarios for that ticket

#### 2. Feature Area Tags

Tags categorizing by application module or feature:

```gherkin
@Login
@Smoke
@CRM
@Employees
@Inventory
@Sales
```

**Purpose**: Organize tests by functional area

**Usage**: `behave --tags=@Login` runs all login-related tests

#### 3. User Role Tags

Tags identifying which user type the test covers:

```gherkin
@SalesManager
@PosManager
```

**Purpose**: Filter tests by user role or persona

**Usage**: `behave --tags=@SalesManager` runs tests for Sales Manager role

#### 4. Test Priority Tags

Tags indicating test importance or execution frequency:

```gherkin
@Smoke
@Regression
@Critical
@P0
@P1
```

**Purpose**: Prioritize test execution

**Usage**: `behave --tags=@Smoke` runs smoke test suite

#### 5. Test Status Tags

Tags indicating test state:

```gherkin
@WIP          # Work In Progress
@Skip         # Temporarily skip
@Bug          # Known bug
@Manual       # Manual test only
```

**Purpose**: Mark tests for special handling

**Usage**: `behave --tags=~@Skip` runs all tests except skipped ones

### Tag Expressions

Behave supports boolean logic for tag filtering:

#### AND Logic (multiple tags required)

```bash
# Run scenarios that have BOTH @Login AND @SalesManager tags
behave --tags=@Login --tags=@SalesManager
```

#### OR Logic (any tag matches)

```bash
# Run scenarios that have EITHER @SalesManager OR @PosManager
behave --tags=@SalesManager,@PosManager
```

#### NOT Logic (exclude tags)

```bash
# Run all scenarios EXCEPT those tagged @Skip
behave --tags=~@Skip
```

#### Complex Expressions

```bash
# Run Login tests for SalesManager, but not WIP
behave --tags=@Login --tags=@SalesManager --tags=~@WIP
```

### Tag Inheritance

Tags inherit down the hierarchy:

```gherkin
@Login                          # Applies to entire feature
Feature: Login feature

  @UPGN-286                     # Applies to this scenario + inherits @Login
  Scenario Outline: Valid login
    
    @SalesManager               # Applies to these examples + inherits @Login and @UPGN-286
    Examples: SalesManager data
```

**Result**: The SalesManager examples have tags: `@Login`, `@UPGN-286`, `@SalesManager`

### Best Practices for Tags

- **Meaningful Names**: Use descriptive tag names that clearly indicate purpose
- **Consistent Convention**: Establish and follow team tagging conventions
- **Hierarchical**: Use feature-level tags for broad categorization, scenario-level for specifics
- **Jira Integration**: Include ticket numbers for traceability
- **Selective Execution**: Design tag structure to support flexible test execution
- **Avoid Over-Tagging**: Don't add too many tags; keep it manageable
- **Document Tags**: Maintain a tag glossary for team reference

---

## Comments

Comments in Gherkin start with the `#` symbol and are ignored by the parser. They provide additional context and documentation for human readers.

### Syntax

```gherkin
# This is a comment
Feature: Feature name
  # Comments can appear anywhere in the file
  Scenario: Scenario name
    # Even between steps
    Given a precondition
    # Another comment
    When an action occurs
    Then expected outcome
```

### Comment Examples from Feature Files

#### Documenting Test Requirements

```gherkin
#1-Users can log in with valid credentials (We have 5 types of users but will test only 2 user: PosManager, SalesManager)
@UPGN-286
Scenario Outline: Users log in with valid credentials
```

**Source:** `features/Login.feature:12-14`

#### Explaining Test Scenarios

```gherkin
#2-"Wrong login/password" should be displayed for invalid (valid username-invalid password and invalid username-valid password) credentials
@UPGN-287
Scenario Outline: Users log in with invalid email or invalid password credentials
```

**Source:** `features/Login.feature:57-59`

#### Noting Disabled Tests

```gherkin
#4- User land on the 'reset password' page after clicking on the "Reset password" link
```

**Source:** `features/Login.feature:102`

This comment documents a test case that is defined but not yet implemented.

#### Describing Expected Behavior

```gherkin
#5-User should see the password in bullet signs by default
@UPGN-289
Scenario Outline: User should see the password in bullet signs by default
```

**Source:** `features/Login.feature:104-106`

#### Test Case Verification Notes

```gherkin
#6- Verify if the 'Enter' key of the keyboard is working correctly on the login page.
@UPGN-290
Scenario Outline: User tries whether enter button works on the login page.
```

**Source:** `features/Login.feature:121-123`

### Best Practices for Comments

- **Document Intent**: Explain why a test exists, not what it does (Gherkin is self-documenting)
- **Test Requirements**: Reference requirement IDs or acceptance criteria
- **Temporary States**: Mark disabled tests or work-in-progress with comments
- **Complex Logic**: Explain non-obvious test design decisions
- **Minimal Use**: Let Gherkin's readability speak for itself; don't over-comment
- **Keep Updated**: Remove obsolete comments as tests evolve
- **Team Communication**: Use comments to share context with other team members

---

## Step Arguments

Gherkin steps can include additional data through arguments. There are two types: data tables and doc strings.

### Data Tables

Data tables provide structured data to step definitions using pipe-delimited rows.

#### Syntax

```gherkin
When User provides the following data:
  | Field     | Value          |
  | Name      | John Doe       |
  | Email     | john@test.com  |
  | Role      | Admin          |
```

**Note**: This is different from Examples tables. Data tables are arguments passed to a single step, while Examples tables define multiple scenario executions.

#### Usage in Test Framework

While not extensively used in the provided feature files, data tables are useful for:
- Complex form data entry
- Multiple entity creation
- Verification of tabular data
- Configuration of test scenarios

### Doc Strings (Multi-line Text)

Doc strings allow passing multi-line text to steps using triple quotes `"""`.

#### Syntax

```gherkin
When User enters the following message:
  """
  This is a multi-line message
  that spans several lines
  and preserves formatting.
  """
```

#### Usage Scenarios

- Long text input
- JSON or XML payloads
- Multi-paragraph content
- Formatted text with line breaks

---

## Complete Example

Here is a complete, well-structured feature file combining all Gherkin elements:

```gherkin
@Login
Feature: Testinium app login feature

  User Story:
  As a user, I should be able to login with correct credentials to different accounts.

  Accounts are: PosManager, SalesManager

  Background: For the scenarios in the feature file, user is expected to be on login page
    Given User is on the upgenix login page

  #1-Users can log in with valid credentials (We have 5 types of users but will test only 2 user: PosManager, SalesManager)
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

    @PosManager
    Examples: PosManager's username and password
      |username               |password  |
      |posmanager5@info.com   |posmanager|
      |posmanager6@info.com   |posmanager|
      |posmanager7@info.com   |posmanager|

  #2-"Wrong login/password" should be displayed for invalid credentials
  @UPGN-287
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

    @PosManager
    Examples: PosManager's username and password
      |username               |password   |
      |posmanager5@info.com   |posmanager1|
      |posmanagerr6@info.com  |posmanager |

  #5-User should see the password in bullet signs by default
  @UPGN-289
  Scenario Outline: User should see the password in bullet signs by default
    When User enters "<password>" password
    Then User should see the password in bullet signs

    @SalesManager
    Examples: SalesManager's username and password
      |password    |
      |saLesManager|

    @PosManager
    Examples: PosManager's username and password
      |password   |
      |posmanager|
```

**Source:** Adapted from `features/Login.feature`

This example demonstrates:
- ✅ Feature-level tag (@Login)
- ✅ User story in feature description
- ✅ Background for shared setup
- ✅ Comments documenting requirements (#1, #2, #5)
- ✅ Scenario Outline with parameters
- ✅ Multiple Examples groups with tags
- ✅ Jira integration tags (@UPGN-286, @UPGN-287, @UPGN-289)
- ✅ Role-based tags (@SalesManager, @PosManager)
- ✅ Clear Given-When-Then structure
- ✅ Parameterized steps with angle brackets

---

## Gherkin Best Practices

### 1. Use Present Tense

**Do:**
```gherkin
When User clicks the login button
Then User should see the dashboard
```

**Don't:**
```gherkin
When User clicked the login button
Then User should have seen the dashboard
```

**Rationale**: Present tense describes behavior as it happens, making scenarios more immediate and readable.

### 2. Keep Steps Atomic

**Do:**
```gherkin
When User enters "test@example.com" username
And User enters "password123" password
And User clicks the login button
```

**Don't:**
```gherkin
When User logs in with "test@example.com" and "password123"
```

**Rationale**: Atomic steps are reusable, easier to maintain, and provide better failure diagnostics.

### 3. Avoid Technical Implementation Details

**Do:**
```gherkin
When User selects "Premium" subscription plan
Then User should see subscription confirmation
```

**Don't:**
```gherkin
When User clicks the button with ID "btn-premium-subscription"
And User waits for 3 seconds
Then User should see element with class "confirmation-message"
```

**Rationale**: Gherkin should describe business behavior, not UI implementation. Keep scenarios resilient to UI changes.

### 4. Use Background for Repeated Setup

**Do:**
```gherkin
Background:
  Given User is logged in as Sales Manager

Scenario: Create opportunity
  When User creates new opportunity
  
Scenario: View opportunities
  When User navigates to opportunities list
```

**Don't:**
```gherkin
Scenario: Create opportunity
  Given User is logged in as Sales Manager
  When User creates new opportunity
  
Scenario: View opportunities
  Given User is logged in as Sales Manager
  When User navigates to opportunities list
```

**Rationale**: DRY principle - don't repeat setup across scenarios.

### 5. Use Scenario Outline for Similar Scenarios with Different Data

**Do:**
```gherkin
Scenario Outline: User logs in with valid credentials
  When User enters "<username>" username
  And User enters "<password>" password
  Then User should see the dashboard
  
  Examples:
    | username              | password     |
    | admin@test.com        | admin123     |
    | manager@test.com      | manager123   |
```

**Don't:**
```gherkin
Scenario: Admin logs in
  When User enters "admin@test.com" username
  And User enters "admin123" password
  Then User should see the dashboard
  
Scenario: Manager logs in
  When User enters "manager@test.com" username
  And User enters "manager123" password
  Then User should see the dashboard
```

**Rationale**: Scenario Outline reduces duplication and makes data-driven testing explicit.

### 6. Use Meaningful Tag Names

**Do:**
```gherkin
@Smoke @Login @Critical @UPGN-286
Scenario: Successful login
```

**Don't:**
```gherkin
@test1 @quick @a
Scenario: Successful login
```

**Rationale**: Descriptive tags enable effective test organization and filtering.

### 7. Write Declarative Scenarios (What), Not Imperative (How)

**Declarative (Better):**
```gherkin
When User creates a new employee "John Doe"
Then Employee "John Doe" should be visible in the employee list
```

**Imperative (Avoid):**
```gherkin
When User clicks the "New Employee" button
And User enters "John" in the first name field
And User enters "Doe" in the last name field
And User clicks the "Save" button
Then User should see "John Doe" in the employee table
```

**Rationale**: Declarative scenarios focus on business intent and are more maintainable when UI changes.

**Exception**: Sometimes imperative steps are necessary for UI-specific tests (e.g., testing button functionality).

### 8. One Scenario = One Behavior

**Do:**
```gherkin
Scenario: User creates new employee
  When User creates new employee "Jane Smith"
  Then Employee "Jane Smith" should appear in the list

Scenario: User edits existing employee
  When User edits employee name to "Jane Doe"
  Then Employee "Jane Doe" should appear in the list
```

**Don't:**
```gherkin
Scenario: User manages employees
  When User creates new employee "Jane Smith"
  Then Employee "Jane Smith" should appear in the list
  When User edits employee name to "Jane Doe"
  Then Employee "Jane Doe" should appear in the list
  When User deletes employee "Jane Doe"
  Then Employee "Jane Doe" should not appear in the list
```

**Rationale**: Testing one behavior per scenario makes failures easier to diagnose and scenarios easier to maintain.

### 9. Use Consistent Language and Terminology

**Do:**
```gherkin
Given User is on the login page
When User enters credentials
Then User should see the dashboard

Given User is on the profile page
When User updates personal information
Then User should see the updated profile
```

**Don't:**
```gherkin
Given User navigates to login
When User types in credentials
Then User views the dashboard

Given User goes to their profile
When User changes their info
Then User can see the profile updated
```

**Rationale**: Consistent terminology improves readability and makes step definitions more reusable.

### 10. Keep Scenarios Independent

**Do:**
```gherkin
Scenario: User creates employee
  Given Database is in clean state
  When User creates employee "Alice"
  Then Employee "Alice" exists

Scenario: User deletes employee
  Given Employee "Bob" exists
  When User deletes employee "Bob"
  Then Employee "Bob" does not exist
```

**Don't:**
```gherkin
Scenario: User creates employee
  When User creates employee "Alice"
  Then Employee "Alice" exists

Scenario: User deletes employee (depends on previous scenario)
  When User deletes employee "Alice"
  Then Employee "Alice" does not exist
```

**Rationale**: Independent scenarios can run in any order and in parallel, improving test reliability and execution speed.

---

## Gherkin Anti-Patterns to Avoid

### 1. Overly Technical Steps

**Avoid:**
```gherkin
When User sends POST request to "/api/login" with payload {"user": "admin", "pass": "123"}
And Response status code should be 200
```

**Better:**
```gherkin
When User logs in as administrator
Then User should be authenticated successfully
```

### 2. Too Many And Steps

**Avoid:**
```gherkin
When User clicks button A
And User waits 2 seconds
And User clicks button B
And User enters text in field C
And User clicks button D
And User waits for element E
And User verifies text F
```

**Better:** Consolidate related actions or reconsider scenario granularity.

### 3. Scenario Becoming Integration Tests

**Avoid:**
```gherkin
Scenario: Complete user workflow
  Given User registers new account
  When User logs in
  And User updates profile
  And User creates 10 employees
  And User generates report
  And User exports to PDF
  And User logs out
  Then All operations should complete successfully
```

**Better:** Split into multiple focused scenarios.

### 4. Hard-Coded Test Data in Multiple Places

**Avoid:** Repeating the same test data across many scenarios

**Better:** Use Scenario Outline with Examples or externalize test data.

---

## Summary

Gherkin provides a structured, readable format for defining application behavior that bridges communication between business stakeholders and technical teams. 

**Key Takeaways:**

- **Feature** describes the feature being tested
- **Background** defines common setup for all scenarios
- **Scenario** defines a single test case
- **Scenario Outline** enables data-driven testing
- **Given/When/Then** structure creates clear, logical test flows
- **Examples** tables provide test data for parameterized scenarios
- **Tags** organize and filter tests effectively
- **Comments** add context and documentation

**Next Steps:**

- **Write Feature Files**: Start creating `.feature` files in the `features/` directory
- **Step Definitions**: Implement step definitions in `features/steps/` to connect Gherkin to code
- **Page Objects**: Use page objects to interact with the application
- **Execute Tests**: Run tests with Behave using tags for selective execution

**Related Documentation:**

- [Feature Files Guide](../guides/feature-files.md) - Detailed guide on writing feature files
- [Step Definitions Guide](../guides/step-definitions.md) - How to implement step definitions
- [Authentication Testing Guide](../guides/authentication-testing.md) - Login feature testing examples
- [Command Reference](./command-reference.md) - Behave commands and options
- [Behave Configuration](./behave-configuration.md) - Behave framework configuration

**Source Citations:**
- `features/Login.feature` - Comprehensive login testing examples with multiple scenario outlines
- `features/Crm.feature` - CRM module testing with Background and simple scenarios
- `features/EmployeeFc.feature` - Employee management testing examples

---

*This reference documentation is part of the Testinium QA Python test automation framework. For questions or contributions, see the [Contributing Guide](../contributing/index.md).*
