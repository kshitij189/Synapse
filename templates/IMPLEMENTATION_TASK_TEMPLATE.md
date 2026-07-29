# Implementation Task Template

> Copy this template for every implementation task assigned to the coding agent.

---

# Purpose

This template standardizes implementation tasks across the project.

Every implementation request should be documented using this template to ensure sufficient context, architectural consistency, traceability, and compliance with the project's engineering standards.

---

# Required Reading Order

Before completing this task, review the project documentation in the following order:

1. `README.md`
2. `CONTEXT.md`
3. `AI_GUIDE.md`
4. `DOC_INDEX.md`
5. Relevant implementation milestone documents
6. Relevant feature-specific documents

---

# Task Information

## Task ID

```
TASK-XXX
```

---

## Title

```
<Short descriptive title>
```

---

## Milestone

Reference the implementation milestone from **Document 25 – Implementation Roadmap**.

---

## Priority

- Critical
- High
- Medium
- Low

---

## Status

- Planned
- In Progress
- Review
- Completed
- Blocked

---

# Objective

Clearly describe the business objective of this task.

---

# Scope

Everything that must be implemented.

-

-

-

---

# Out of Scope

Everything that must **NOT** be implemented.

-

-

-

---

# Implementation References

List every project artifact relevant to this implementation.

## Documentation

-

-

-

## Existing APIs

-

-

-

## Existing Services

-

-

-

## Database Tables

-

-

-

## Related Tasks

-

-

-

---

# Required Documentation

The implementation agent must review these documents before writing any code.

## Mandatory

- `README.md`
- `CONTEXT.md`
- `AI_GUIDE.md`
- `DOC_INDEX.md`

## Project Documents

-

-

-

---

# Dependencies

List prerequisite modules or services.

-

-

-

---

# Implementation Requirements

Frameworks, libraries, architectural patterns, engineering constraints, and implementation requirements.

-

-

-

---

# Expected Files

## Create

-

-

-

---

## Modify

-

-

-

---

# Database Changes

Complete only if applicable.

### Tables

-

-

-

### Columns

-

-

-

### Relationships

-

-

-

### Indexes

-

-

-

### Constraints

-

-

-

### Migration Required

Yes / No

### Migration File

-

---

# API Changes

Complete only if applicable.

## New Endpoints

-

-

-

## Modified Endpoints

-

-

-

## Deprecated Endpoints

-

-

-

## Version Changes

-

---

# Security Requirements

Examples:

- Authentication
- Authorization
- RBAC
- Input Validation
- Output Validation
- Secure Error Handling

---

# Performance Considerations

Examples:

- Indexing
- Query Optimization
- Pagination
- Connection Pooling
- Caching

---

# Error Handling

Describe expected errors.

-

-

-

---

# Deliverables

Implementation must include:

- Production-ready code
- Unit Tests
- Integration Tests
- API Documentation
- Database Migration (if required)
- Configuration Updates
- Logging & Metrics
- Documentation Updates

---

# Testing Requirements

Generate all applicable tests:

- Unit Tests
- Integration Tests
- API Tests
- End-to-End Tests (where applicable)

Verify:

- Successful Requests
- Invalid Requests
- Unauthorized Requests
- Edge Cases

---

# Acceptance Criteria

The task is complete only if:

- All requirements are implemented.
- All tests pass.
- Build succeeds.
- No linting errors.
- No type-checking errors.
- Architecture remains unchanged.
- Existing functionality remains unaffected.
- Engineering standards are followed.
- Documentation is updated.

---

# Constraints

Do **NOT**:

- Invent APIs.
- Invent database schema.
- Introduce unapproved libraries.
- Change project architecture.
- Skip testing.
- Skip documentation.
- Ignore engineering standards.

---

# AI Response Workflow

The implementation agent should respond using the following structure.

## 1. Task Understanding

Summarize the task.

---

## 2. Documentation Reviewed

List every document reviewed.

---

## 3. Implementation Plan

Explain:

- Components
- Services
- APIs
- Database
- Files
- Dependencies

---

## 4. Risks / Questions

If documentation is ambiguous:

- Stop implementation.
- Ask for clarification.
- Do not guess.

---

## 5. Approval Check

If approval is required:

- Stop after presenting the implementation plan.

Otherwise, continue with implementation.

---

## 6. Implementation

Generate production-ready code.

---

## 7. Testing

Generate all required tests.

---

## 8. Verification

Verify:

- Documentation followed
- Architecture preserved
- Security implemented
- Tests added
- Existing functionality remains unaffected
- Engineering standards followed

---

## 9. Completion Report

### Summary

Brief overview of the completed implementation.

### Files Created

-

-

-

### Files Modified

-

-

-

### APIs Added

-

-

-

### Database Changes

-

-

-

### Breaking Changes

None / Describe

### Documentation Updated

-

-

-

### Known Limitations

-

-

-

### Risks / Follow-up Work

-

-

-

### Recommended Next Task

Suggest the next logical implementation task.

---

# Definition of Done

A task is complete only when:

- Production-ready implementation completed.
- Build succeeds.
- All tests pass.
- Linting passes.
- Type checking passes.
- Documentation updated.
- Architecture preserved.
- No blockers remain.

---

# Task Completion Checklist

Before marking the task as complete, verify:

- Relevant documentation reviewed
- Architecture followed
- Coding standards followed
- Required files created
- Existing files updated correctly
- APIs validated
- Database validated
- Security validated
- Existing functionality verified
- Tests added
- Documentation updated
- `IMPLEMENTATION_PROGRESS.md` updated
- `CHANGELOG.md` updated

---

# Traceability

Every completed task should be traceable to:

- An implementation milestone
- One or more design documents
- The affected source code
- Associated tests
- Documentation updates (if applicable)

Implementation should never exist without documented traceability.

---

# Notes

- Complete only the sections relevant to the task.
- Mark non-applicable sections as **Not Applicable**.
- If any section is intentionally omitted, explicitly mark it as **Not Applicable** rather than leaving it blank.
- Never assume undocumented requirements.
- If documentation is unclear, stop and request clarification.
- Prioritize correctness, maintainability, security, and architectural consistency over implementation speed.