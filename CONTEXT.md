# AAOP - Project Context

## Purpose

This document provides the high-level project context required to understand the AAOP platform before reading the detailed design documents or beginning implementation.

It serves as the bridge between the repository overview (`README.md`) and the detailed documentation catalogue (`DOC_INDEX.md`).

---

# Project Overview

**Project Name:** Autonomous Adaptive Organization Platform (AAOP)

**Project Type:** Enterprise AI Platform

**Development Model:** AI-Assisted Software Engineering

**Implementation Status:** Active Development

**Documentation Status:** Architecture Complete (Documents 1–25)

---

# Project at a Glance

| Category | Value |
|----------|-------|
| Project | Autonomous Adaptive Organization Platform (AAOP) |
| Type | Enterprise AI Platform |
| Development Model | AI-Assisted Software Engineering |
| Architecture | Microservices + Event-Driven |
| Design Principles | Clean Architecture + Domain-Driven Design |
| Backend | Python + FastAPI |
| Frontend | Next.js + React + TypeScript |
| Database | PostgreSQL |
| Cache | Redis |
| Vector Database | ChromaDB |
| Search Engine | Elasticsearch |
| AI Framework | LangGraph + LangChain |
| Authentication | JWT + OAuth2 |
| Containerization | Docker |
| Orchestration | Kubernetes |
| CI/CD | GitHub Actions |
| Monitoring | OpenTelemetry + Prometheus + Grafana |
| Documentation | Documents 1–25 |
| Current Phase | Implementation |
| Source of Truth | Project Documentation |

---

# Documentation Navigation

This repository follows a documentation-first workflow.

Documentation should generally be read in the following order:

```text
README.md
      ↓
CONTEXT.md
      ↓
DOC_INDEX.md
      ↓
Relevant Design Documents
      ↓
AI_GUIDE.md (during implementation)
```

---

# Project Description

AAOP (Autonomous Adaptive Organization Platform) is an enterprise-grade AI-native platform designed to model, automate, and optimize organizational operations through intelligent agents, workflow automation, knowledge management, memory systems, and organizational digital twins.

The platform emphasizes scalability, maintainability, security, observability, and long-term extensibility.

All implementation follows a documentation-first approach where architectural and engineering decisions originate from the project documentation.

---

# High-Level Architecture

AAOP follows:

- Microservices Architecture
- Event-Driven Architecture
- Clean Architecture
- Domain-Driven Design (DDD)
- Repository Pattern
- Service Layer Pattern

Each microservice owns its own domain boundaries, data model, and business logic while communicating through documented REST APIs and asynchronous events.

---

# Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis

---

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

---

## AI Layer

- LangGraph
- LangChain
- ChromaDB
- Elasticsearch
- OpenAI / Gemini (Configurable)

---

## Infrastructure

- Docker
- Kubernetes
- Nginx

---

## CI/CD

- GitHub Actions

---

## Monitoring & Observability

- OpenTelemetry
- Prometheus
- Grafana

---

# Core Platform Modules

The platform is organized into the following major business domains.

## Identity

Responsible for:

- Authentication
- Authorization
- Role-Based Access Control (RBAC)
- User Management

---

## Organization

Responsible for:

- Organizations
- Departments
- Teams
- Employees
- Organizational Digital Twin

---

## Memory

Responsible for:

- Short-Term Memory
- Long-Term Memory
- Semantic Memory
- Conversation History
- Memory Retrieval

---

## Knowledge

Responsible for:

- Knowledge Base
- RAG Pipeline
- Document Processing
- Embeddings
- Vector Search

---

## Planner

Responsible for:

- Task Planning
- Decision Making
- Goal Decomposition
- Execution Planning

---

## Workers

Responsible for:

- Task Execution
- Tool Invocation
- Background Jobs
- Agent Execution

---

## Workflow Engine

Responsible for:

- Workflow Automation
- Event Orchestration
- Business Processes

---

## Analytics

Responsible for:

- Dashboards
- Metrics
- Reporting
- Business Intelligence

---

# Repository Layout

```text
AAOP/
├── docs/
├── backend/
├── frontend/
├── infra/
├── scripts/
│
├── README.md
├── AI_GUIDE.md
├── CONTEXT.md
├── DOC_INDEX.md
├── IMPLEMENTATION_PROGRESS.md
└── CHANGELOG.md
```

---

# Documentation Structure

## Architecture Documents (Documents 01–22)

These documents define the platform architecture and design, including:

- Product Vision
- Software Requirements Specification (SRS)
- Functional Design
- High-Level Design
- Low-Level Design
- Database Design
- REST API Specifications
- Event Contracts
- Worker SDK
- Tool SDK
- Memory Architecture
- Infrastructure
- CI/CD
- Security
- Repository Structure
- Coding Standards
- Testing Strategy
- Product Roadmap
- Architecture Decision Records (ADRs)

---

## Engineering Documents

### Document 23

**Technology Stack & Engineering Decisions**

Defines the approved technology stack and explains every technology selection.

---

### Document 24

**Engineering Playbook**

Defines engineering standards, coding practices, architectural patterns, folder structure, naming conventions, testing strategy, and implementation guidelines.

---

### Document 25

**Implementation Roadmap**

Defines the complete milestone-by-milestone implementation sequence for the platform.

---

# Development Philosophy

Implementation follows these core principles:

- Documentation First
- Architecture Before Code
- Security by Default
- Scalability by Design
- Maintainability over Shortcuts
- Production-Ready Engineering
- Test-Driven Validation
- AI-Assisted Development

---

# Current Project Status

**Development Stage:** Active Implementation

Development proceeds according to the milestones defined in the **Implementation Roadmap (Document 25).**

The current high-level implementation milestones are:

1. Repository Bootstrap
2. Identity & Authentication
3. Organization Management
4. Memory Layer
5. Knowledge Layer
6. Planner
7. Worker Framework
8. Workflow Engine
9. Frontend
10. Analytics & Reporting

---

# Important Repository Files

| File | Purpose |
|------|---------|
| README.md | General project overview |
| CONTEXT.md | High-level project context |
| AI_GUIDE.md | AI implementation operating manual |
| DOC_INDEX.md | Documentation catalogue and navigation guide |
| IMPLEMENTATION_PROGRESS.md | Tracks completed and pending milestones |
| CHANGELOG.md | Records significant implementation changes |

---

# Source of Truth Hierarchy

If multiple documents appear to conflict, resolve them using the following precedence:

1. Product Vision
2. Software Requirements Specification (SRS)
3. Functional Design
4. High-Level Design (HLD)
5. Low-Level Design (LLD)
6. Architecture Decision Records (ADRs)
7. Engineering Playbook
8. Implementation Roadmap
9. Source Code

If any conflict exists between implementation and documentation, implementation must stop until the conflict is resolved.

---

# Quick Start for AI

For every implementation request, follow the workflow below:

1. Read `AI_GUIDE.md`.
2. Read `DOC_INDEX.md`.
3. Identify the current implementation milestone.
4. Read only the relevant documents and chapters.
5. Prepare an implementation plan.
6. Implement production-ready code.
7. Generate comprehensive tests.
8. Verify compliance with engineering standards.

---

# Final Notes

AAOP is a documentation-driven enterprise software project.

Every implementation decision must be traceable to the project documentation.

Never invent undocumented functionality.

Never bypass documented architectural decisions.

Never introduce undocumented technologies.

When documentation is ambiguous or conflicting, stop implementation and request clarification before proceeding.