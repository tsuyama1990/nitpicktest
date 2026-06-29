# CYCLE02 UAT Plan

## Test Scenarios

| ID | Priority | Scenario Description |
|---|---|---|
| UAT_02_01 | High | Filter TODO items by status. |
| UAT_02_02 | High | Filter TODO items by priority. |
| UAT_02_03 | High | Search for TODO items by keyword. |
| UAT_02_04 | Medium | Sort TODO items by priority. |
| UAT_02_05 | High | Edit an existing TODO item's details. |

## Behavior Definitions

### UAT_02_01: Filter TODO items by status
```gherkin
Feature: Filter TODOs
  As a user
  I want to filter tasks by status
  So that I can see only what is pending or completed

  Scenario: Filtering by completed status
    Given there is a pending task "Task A" and a completed task "Task B"
    When I run the CLI command to list tasks with status "completed"
    Then I should only see "Task B" in the output
```

### UAT_02_02: Filter TODO items by priority
```gherkin
Feature: Filter TODOs
  As a user
  I want to filter tasks by priority
  So that I can focus on high priority tasks

  Scenario: Filtering by high priority
    Given there is a low priority task "Task A" and a high priority task "Task B"
    When I run the CLI command to list tasks with priority "high"
    Then I should only see "Task B" in the output
```

### UAT_02_03: Search TODO items
```gherkin
Feature: Search TODOs
  As a user
  I want to search for tasks by keyword
  So that I can quickly find specific items

  Scenario: Searching by keyword
    Given there is a task with title "Buy milk" and a task with title "Walk the dog"
    When I run the CLI command to search for "milk"
    Then I should only see "Buy milk" in the output
```

### UAT_02_04: Sort TODO items
```gherkin
Feature: Sort TODOs
  As a user
  I want to sort tasks
  So that they are ordered in a meaningful way

  Scenario: Sorting by priority
    Given there is a low priority task "Task A" and a high priority task "Task B"
    When I run the CLI command to list tasks sorted by priority
    Then I should see "Task B" before "Task A" in the output
```

### UAT_02_05: Edit a TODO item
```gherkin
Feature: Edit TODO
  As a user
  I want to edit an existing task
  So that I can update its details without recreating it

  Scenario: Editing task title and priority
    Given there is a task with ID 1, title "Old Title", and priority "low"
    When I run the CLI command to edit task 1 with title "New Title" and priority "high"
    Then the task with ID 1 should have title "New Title" and priority "high"
```
