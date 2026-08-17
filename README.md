# TechnoGOAT TG CLI

`tg` is a lightweight command-line tool for managing engineering environments.

The goal of TG CLI is to provide a simple, provider-agnostic interface for common
environment management tasks while allowing each provider (AWS, local, Docker,
Kubernetes, etc.) to implement the details.

The project is intentionally being built in small, well-tested increments.

---

## Current Status

Current implementation includes:

- ✅ Project foundation
- ✅ Domain model
- ✅ Configuration model
- ✅ Configuration loader
- ✅ CLI framework
- ✅ Unit test infrastructure

Currently in progress:

- 🚧 AWS provider
- 🚧 Environment status
- 🚧 Environment start / stop

---

## Development Setup

Clone the repository.

Create and activate a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode.

```bash
python -m pip install -e ".[dev]"
```

Run the test suite.

```bash
pytest
```

---

## Configuration

TG CLI uses a local YAML configuration file to describe engineering environments.

Example:

```yaml
environments:
  uts:
    provider: aws
    profile: uts-validation
    region: us-east-1

    resources:
      - name: uts-moodle-web-01
        type: compute
```

The configuration describes **what exists**.

Providers determine **how those resources are managed**.

---

## Project Philosophy

TG CLI models engineering concepts rather than vendor-specific implementations.

Examples:

- Environment
- Resource
- Provider

Provider implementations translate those concepts into platform-specific APIs.

For example:

- AWS → EC2, RDS
- Local → Processes, Docker, Virtual Machines
- Kubernetes → Pods, Services

---

## Roadmap

Near-term goals:

- AWS provider implementation
- Environment status
- Start and stop environments
- Resource health reporting

Long-term goals:

- Additional providers
- Local development support
- Home lab support
- Automation workflows
- TechnoGOAT ecosystem integration

---

## License

See the LICENSE file.