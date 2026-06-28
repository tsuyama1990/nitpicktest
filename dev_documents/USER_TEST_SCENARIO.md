# User Test Scenario & Tutorial Plan

## Tutorial Strategy
The goal of this tutorial is to walk users through the entire lifecycle of managing tasks using the TODO application CLI. We will use a single executable Marimo notebook to allow users to interactively experience the core operations (CYCLE01) and the advanced filtering/searching capabilities (CYCLE02).

By running the CLI commands via `subprocess` within the Marimo notebook, users can see the exact output and state changes.

## Tutorial Plan
The tutorial will be consolidated into a SINGLE Marimo file located at `tutorials/UAT_AND_TUTORIAL.py`.

It will cover the following flow:
1. **Introduction:** Overview of the TODO App.
2. **Basic Operations (CYCLE01):**
   - Adding a new task (e.g., "Buy Groceries", high priority).
   - Listing tasks to confirm creation.
   - Completing the task.
   - Deleting a task.
3. **Advanced Operations (CYCLE02):**
   - Populating the system with multiple tasks of varying priorities and statuses.
   - Searching for tasks by a specific keyword.
   - Filtering the task list by "high" priority or "completed" status.
   - Sorting tasks to see what needs attention first.
   - Editing an existing task to change its title or priority.
4. **Cleanup:** Resetting the environment to leave it clean after the tutorial.

## Tutorial Validation
During the final verification phase, the `tutorials/UAT_AND_TUTORIAL.py` Marimo file must be executed to ensure all CLI commands behave as documented and that no exceptions occur.
