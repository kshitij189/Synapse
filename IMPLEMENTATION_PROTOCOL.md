# Implementation Protocol

## Purpose

This document defines the standard implementation workflow for the Synapse platform.

Every implementation task must follow this protocol to ensure architectural consistency, maintainability, security, and production-quality engineering.

This document is the operational playbook for AI coding assistants and human developers.

---

# Core Principle

The project is documentation-driven.

Code exists to implement the documented architecture.

Documentation is never reverse-engineered from code.

When documentation and implementation disagree, documentation takes precedence until explicitly updated.

---

# Source of Truth

Implementation must follow the following priority.

1. Project Documentation (Documents 01–25)
2. Architecture Decision Records (ADRs)
3. Technology Stack & Engineering Decisions
4. Engineering Handbook
5. AI_GUIDE.md
6. CONTEXT.md
7. DOC_INDEX.md
8. IMPLEMENTATION_PROGRESS.md
9. Existing Source Code

Implementation must never contradict a higher-priority artifact.

---

# Standard Implementation Workflow

Every implementation task follows the same workflow.

```
Receive Task

↓

Read Documentation

↓

Understand Requirements

↓

Prepare Implementation Plan

↓

Approval (if required)

↓

Implement

↓

Test

↓

Verify

↓

Update Documentation

↓

Mark Task Complete
```

---

# Mandatory Reading

Before implementing any feature, always read:

- AI_GUIDE.md
- CONTEXT.md
- DOC_INDEX.md
- IMPLEMENTATION_PROGRESS.md

Then identify the current milestone and read only the relevant architecture documents.

Never read unnecessary documents.

---

# Task Execution

Every implementation begins with a completed implementation task.

Use:

IMPLEMENTATION_TASK_TEMPLATE.md

The task defines:

- Objective
- Scope
- References
- Deliverables
- Constraints
- Acceptance Criteria

Implementation should never begin without a defined task.

---

# Planning Phase

Before writing code:

1. Understand the task.
2. Review the required documentation.
3. Identify affected services.
4. Identify affected APIs.
5. Identify affected databases.
6. Identify dependencies.
7. Determine implementation order.

If documentation is ambiguous:

Stop.

Request clarification.

Do not guess.

---

# Implementation Rules

Always:

- Preserve architecture.
- Follow Clean Architecture.
- Follow Domain-Driven Design.
- Follow repository conventions.
- Write production-ready code.
- Use dependency injection.
- Validate inputs.
- Handle errors gracefully.
- Use structured logging.
- Write modular code.
- Use meaningful names.
- Keep functions focused.

Never:

- Change service boundaries.
- Invent APIs.
- Invent database schema.
- Introduce undocumented libraries.
- Skip validation.
- Skip testing.
- Leave TODOs.
- Leave placeholder implementations.
- Commit incomplete functionality.

---

# Testing Requirements

Every implementation must include:

- Unit Tests
- Integration Tests
- API Tests (if applicable)

Verify:

- Success cases
- Failure cases
- Unauthorized requests
- Validation errors
- Edge cases

Implementation is incomplete without tests.

---

# Documentation Updates

After implementation:

Update:

- IMPLEMENTATION_PROGRESS.md
- CHANGELOG.md

Update project documentation only if implementation changes the documented design.

Never silently diverge from documentation.

---

# Completion Checklist

Before marking a task complete verify:

- Relevant documentation reviewed
- Architecture preserved
- Engineering standards followed
- Security implemented
- Validation implemented
- Logging implemented
- Tests written
- Documentation updated
- Build succeeds
- Lint passes
- Type checking passes

---

# Definition of Done

A task is complete only if:

- All requirements implemented
- Production-ready code
- Tests passing
- No build errors
- No lint errors
- No type errors
- Documentation updated
- Architecture unchanged
- Acceptance criteria satisfied

---

# AI Coding Session

Every coding session should follow this sequence.

1. Read mandatory documentation.
2. Read the implementation task.
3. Explain task understanding.
4. Review documentation.
5. Produce implementation plan.
6. Wait for approval if required.
7. Implement.
8. Generate tests.
9. Verify implementation.
10. Update documentation.

---

# Change Management

If implementation requires changes to:

- Architecture
- APIs
- Database schema
- Technology stack
- Repository structure

Stop implementation.

Explain:

- Why the change is needed.
- Impact on the project.
- Affected documentation.

Wait for approval.

---

# Engineering Principles

Every implementation should prioritize:

- Correctness
- Maintainability
- Security
- Scalability
- Readability
- Simplicity
- Observability
- Testability
- Consistency

Implementation quality is more important than implementation speed.

---

# Continuous Progress

Implementation should always continue from the next pending task recorded in:

IMPLEMENTATION_PROGRESS.md

Never skip milestones unless explicitly instructed.

---

# Final Principle

The objective is not merely to generate working software.

The objective is to build a production-grade AI platform whose implementation remains faithful to the documented architecture throughout its entire lifecycle.

When in doubt:

Read the documentation.

Follow the architecture.

Ask for clarification instead of making assumptions.