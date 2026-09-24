# Implement Polymorphic Task Types

## Task Brief
Refactor Task hierarchy to use polymorphism; override methods in UrgentTask and RecurringTask subclasses for specialized behavior.

## Scenario
Your team needs polymorphic task types for the CLI. Override display and priority methods in subclasses.

## Deliverables
- task_types.py with polymorphic methods
- Updated main.py calling polymorphic methods

## Success Criteria
- Each task type overrides display() and priority()
- Polymorphic calls work correctly in CLI