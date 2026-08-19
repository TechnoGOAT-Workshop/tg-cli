# TechnoGOAT TG CLI

`tg` is a lightweight command-line tool for managing engineering environments
safely and predictably.

The current implementation supports AWS-backed environments and discovers live
provider state before planning or applying changes.

## Installation

TG requires Python 3.11 or later.

From the project root:

```bash
python -m pip install -e ".[dev]"
```

## Configuration

TG reads environment definitions from `tg.yaml` by default.

A configuration can define the provider, authentication profile, region, and
resources that belong to an environment.

Example:

```yaml
environments:
  uts:
    provider: aws
    profile: uts-admin
    region: us-east-1
    resources:
      - name: uts-moodle-web-01
        type: compute
```

Use another configuration file with `--config`:

```bash
tg --config ./examples/tg.yaml env status uts
```

## AWS Authentication

TG uses the AWS authentication configured for the environment's named profile.

For AWS IAM Identity Center / SSO profiles, authenticate with the AWS CLI before
running TG:

```bash
aws sso login --profile uts-admin
```

TG does not manage AWS credentials itself.

Planning operations still require valid provider authentication because TG
discovers live resource state before deciding what changes would be required.

## Commands

### Environment Status

```bash
tg --config ./examples/tg.yaml env status uts
```

Displays the current state of the environment.

### Preview a Stop Operation

```bash
tg --config ./examples/tg.yaml env plan stop uts
```

Builds and displays a stop plan without applying any changes.

This command may query AWS to discover current state, but it does not mutate
resources.

For example:

```text
Environment: uts
Operation: stop

Resource             Current   Target    Action
uts-moodle-web-01    running   stopped   stop
```

### Stop an Environment

```bash
tg --config ./examples/tg.yaml env stop uts
```

A stop operation follows a deliberate lifecycle:

```text
discover
   ↓
plan
   ↓
render
   ↓
confirm
   ↓
apply
   ↓
wait
   ↓
verify
   ↓
report result
```

TG always builds the operation plan before performing a mutation.

If no changes are required, TG displays the plan and exits without asking for
confirmation or calling the provider mutation API.

If changes are required, TG displays the plan and asks for confirmation before
applying it.

After execution, TG waits for the requested resource transition to complete,
discovers the resulting state, and reports the verified operation result.

Example:

```text
Operation complete: stop

Resource             Before    After      Result
uts-moodle-web-01    running   stopped    success
```

## Planning and Results

TG separates intended changes from observed outcomes.

### Operation Plan

An `OperationPlan` describes what TG intends to do.

Each resource is represented by a `ResourceAction`, including:

- resource identifier;
- observed current state;
- requested target state;
- action to perform;
- optional reason when no action is required.

Resources already in the requested state remain visible in the plan but are not
mutated.

### Operation Result

An `OperationResult` describes what TG observed after execution.

Each affected resource produces a `ResourceResult` containing its previous
state, verified current state, and whether the requested transition succeeded.

This means TG does not treat acceptance of a provider API request as proof that
the requested state has been reached.

## Development

Run the test suite:

```bash
pytest
```

Run static analysis and lint checks:

```bash
ruff check .
```

Tests use mocked provider services and do not require live AWS credentials.

## Design Principles

TG is being built around a few core ideas:

- discover reality before changing it;
- model engineering concepts separately from provider-specific APIs;
- require a plan before mutation;
- make changes explicit and previewable;
- treat operations as validated state transitions;
- verify resulting state rather than assuming success;
- keep provider authentication owned by the provider;
- build small, demonstrated capabilities before adding broader abstractions.

## Scope

TG is intentionally small.

The current work focuses on establishing a reliable environment-management
lifecycle and proving the architecture against real AWS environments.

Broader capabilities should be added only when real engineering work
demonstrates the need for them.