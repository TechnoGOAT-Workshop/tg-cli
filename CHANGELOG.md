# Changelog

## Unreleased

### Added

- Add `tg env plan stop <environment>` for non-mutating stop previews.
- Add `OperationPlan` and `ResourceAction` domain models for describing intended
  resource state transitions.
- Add `OperationResult` and `ResourceResult` domain models for reporting
  verified execution outcomes.
- Add resource-level status modeling.
- Add Rich-based renderers for operation plans and operation results.
- Add planner tests for running and already-stopped resources.
- Add CLI coverage verifying that plan-only operations do not call `apply()`.
- Add shared pytest AWS service fixtures.

### Changed

- Stop operations now discover current state and build an operation plan before
  performing any mutation.
- Stop operations display the plan and require user confirmation before
  applying changes.
- Stop operations with no required changes now exit without confirmation or
  provider mutation.
- AWS stop execution now waits for EC2 instances to reach the stopped state
  before reporting completion.
- Applied operations now verify provider state and return an `OperationResult`
  instead of treating an accepted API request as successful completion.
- Environment service execution now returns verified operation results.
- Separate domain, provider, presentation, and CLI responsibilities for the
  stop-operation lifecycle.

## 0.1.0 - 2026-08-17

- Initial project skeleton.
- Add `tg env list`, `status`, `start`, and `stop` commands.
- Add EC2 and RDS support behind an AWS service boundary.