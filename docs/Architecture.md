# TG CLI Architecture

## Vision

TG CLI is a provider-agnostic engineering tool for managing development
environments.

The architecture favors small, composable abstractions that model engineering
concepts rather than vendor-specific implementations.

---

# Engineering Principles

These principles guide architectural decisions throughout the project.

## EP-001 — Model Industry Concepts

The domain model represents concepts that exist across engineering platforms.

Examples:

- Environment
- Resource
- Provider

Vendor-specific concepts belong inside provider implementations.

Examples:

- EC2
- RDS
- Cloud SQL
- Azure VM

---

## EP-002 — Separate Domain from Provider

The domain describes **what exists**.

Providers determine **how it is managed**.

Example:

Environment
    ↓
Resources
    ↓
AWS Provider

The domain never depends on AWS.

---

## EP-003 — Configuration Describes Reality

Configuration files describe engineering environments.

They do **not** describe runtime state.

Good:

provider: aws

Bad:

running: true

Runtime state is retrieved from the provider.

---

## EP-004 — Build for Demonstrated Needs

TG CLI intentionally avoids speculative abstractions.

New concepts are introduced only when required by working software.

Small, incremental improvements are preferred over large framework designs.

---

## EP-005 — Providers Own Authentication

Authentication belongs to provider implementations.

Examples:

AWS
    Named Profiles
    IAM Identity Center
    AssumeRole

SSH
    SSH Keys

Docker
    Docker Contexts

The domain never stores credentials.

---

## EP-006 — Small Vertical Slices

Development proceeds in small, testable increments.

Example:

Environment

↓

Configuration Loader

↓

AWS Provider

↓

Environment Status

↓

Start / Stop

Each slice should be independently testable and leave the repository in a
working state.

---

# Current Domain Model

Environment
    ↓
Resources
    ↓
Provider

Future provider implementations translate this engineering model into
platform-specific APIs.