# CYCLE01 UAT Plan

## Test Scenarios

| ID | Priority | Scenario Description |
|---|---|---|
| UAT_01_01 | High | Add a new TODO item with title and priority. |
| UAT_01_02 | High | List all TODO items. |
| UAT_01_03 | High | Mark a pending TODO item as completed. |
| UAT_01_04 | High | Delete an existing TODO item. |

## Behavior Definitions

### UAT_01_01: Add a new TODO item
```gherkin
Feature: Add TODO
  As a user
  I want to add a new task
  So that I can track what needs to be done

  Scenario: Adding a basic task
    Given the TODO storage is empty
    When I run the CLI command to add a task with title "Buy groceries" and priority "high"
    Then the task "Buy groceries" should be saved in the system
    And its status should be "pending"
    And its priority should be "high"
```

### UAT_01_02: List all TODO items
```gherkin
Feature: List TODOs
  As a user
  I want to see all my tasks
  So that I know my overall workload

  Scenario: Listing existing tasks
    Given there are tasks "Task A" and "Task B" in the system
    When I run the CLI command to list tasks
    Then I should see both "Task A" and "Task B" in the output
```

### UAT_01_03: Mark TODO as complete
```gherkin
Feature: Complete TODO
  As a user
  I want to mark a task as done
  So that I can track my progress

  Scenario: Completing a pending task
    Given there is a pending task with ID 1
    When I run the CLI command to complete task 1
    Then the status of task 1 should be changed to "completed"
```

### UAT_01_04: Delete a TODO item
```gherkin
Feature: Delete TODO
  As a user
  I want to remove a task
  So that my list only contains relevant items

  Scenario: Deleting an existing task
    Given there is a task with ID 1
    When I run the CLI command to delete task 1
    Then task 1 should no longer exist in the system
```
