# Chapter 2 – Development Environment
# 2.1 Overview

A consistent development environment is essential for ensuring reliable software delivery across engineering teams. Differences in operating systems, tool versions, dependency management, or local infrastructure often result in inconsistent behavior, difficult debugging, and deployment failures.

To eliminate these issues, AAOP defines a standardized development environment that provides every engineer and AI coding agent with an identical foundation for building, testing, debugging, and running platform services.

The development environment is designed around the following principles:

Reproducibility
Automation
Containerization
Minimal manual configuration
Platform independence
Fast onboarding
Local-first development
Production parity

By standardizing the local development ecosystem, AAOP minimizes "works on my machine" problems and ensures that code behaves consistently across development, testing, staging, and production environments.

# 2.2 Development Environment Architecture

The AAOP development environment mirrors the production architecture while remaining lightweight enough for local development.

                Developer Workstation
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
      VS Code          Git           Docker Desktop
        │               │                │
        └───────────────┼────────────────┘
                        ▼
              Local Kubernetes Cluster
                        │
        ┌───────────────┼────────────────────────┐
        ▼               ▼                        ▼
 Backend Services   Frontend App        Infrastructure Services
        │               │                        │
        ▼               ▼                        ▼
 PostgreSQL         Next.js              Redis
 Kafka              React                Qdrant
 Elasticsearch      TypeScript           MinIO
 Temporal                               Prometheus
 Celery                                 Grafana

This environment enables engineers to develop and test the complete platform locally before deployment.

# 2.3 Supported Operating Systems

AAOP officially supports the following operating systems for development.

Operating System :	Support Level
Ubuntu 24.04 LTS :Primary
macOS (Latest Stable) :Primary
Windows 11 (WSL2 Recommended) :Primary
Other Linux Distributions :Community Support
Recommendation

Windows developers should perform backend development using Windows Subsystem for Linux (WSL2) to provide a Linux-compatible development environment consistent with production deployments.

# 2.4 Required Software

Every engineering workstation should include the following software.

Software : Purpose
Git : Version control
Python 3.13 : Backend development
uv : Python package and environment management
Node.js (LTS) : Frontend tooling
pnpm : Frontend package management
Docker Desktop : Container execution
Kubernetes (Kind or Minikube) : Local orchestration
kubectl : Kubernetes management
Helm : Kubernetes package management
Terraform : Infrastructure provisioning
VS Code : Primary IDE
GitHub CLI : Repository management
Postman / Bruno : API testing
DBeaver : Database administration

Every contributor should use the officially approved versions documented in the repository's compatibility matrix.

# 2.5 IDE Standards

Visual Studio Code is the recommended integrated development environment.

Recommended Extensions
Category : Extension
Python : Python
Python Linting : Ruff
Python Formatting : Ruff Formatter
Docker : Docker
Kubernetes : Kubernetes
Git : GitLens
REST : Thunder Client or REST Client
YAML : YAML
Markdown : Markdown All in One
Terraform : Terraform
SQL : SQLTools
Tailwind CSS : Tailwind CSS IntelliSense
TypeScript : TypeScript Hero
ESLint : ESLint
Prettier : Prettier

These extensions provide consistent formatting, linting, debugging, and productivity across the engineering team.

# 2.6 Repository Initialization

After cloning the repository, engineers should perform a standardized initialization process.

Clone Repository
        │
        ▼
Install Dependencies
        │
        ▼
Create Environment Files
        │
        ▼
Start Infrastructure
        │
        ▼
Run Database Migrations
        │
        ▼
Seed Development Data
        │
        ▼
Launch Services

This sequence ensures that all required dependencies and infrastructure are available before development begins.

# 2.7 Environment Variables

Environment-specific configuration should be externalized through environment variables.

Environment Categories
Environment : Purpose
Local : Developer workstation
Development : Shared engineering environment
Testing : Automated test execution
Staging : Pre-production validation
Production : Live platform
Configuration Rules
Never hardcode secrets.
Keep .env.example under version control.
Store production secrets in HashiCorp Vault.
Validate configuration during application startup.
Document every required environment variable.
# 2.8 Local Infrastructure

AAOP services depend on several supporting infrastructure components during development.

Service : Purpose
PostgreSQL : Relational database
Redis : Cache
Kafka : Event streaming
Elasticsearch : Search
Qdrant : Vector database
MinIO : Object storage
Temporal : Workflow orchestration
Prometheus : Metrics
Grafana : Dashboards
Loki : Logging
Tempo : Distributed tracing

These services should be started automatically using Docker Compose or Kubernetes manifests.

# 2.9 Dependency Management

AAOP standardizes dependency management to ensure reproducible builds.

Backend
Python 3.13
uv
Locked dependency versions
Virtual environments
Frontend
Node.js LTS
pnpm
Lock files
Workspace support
Rules
Do not install packages globally unless required.
Commit lock files.
Update dependencies through approved workflows.
Remove unused dependencies regularly.
# 2.10 Local Development Workflow

The recommended daily development workflow is illustrated below.

Pull Latest Code
        │
        ▼
Update Dependencies
        │
        ▼
Start Infrastructure
        │
        ▼
Run Services
        │
        ▼
Develop Features
        │
        ▼
Run Tests
        │
        ▼
Commit Changes

Following a consistent workflow minimizes integration issues and improves productivity.

# 2.11 Build Automation

The repository should expose standardized automation commands for common development tasks.

Typical operations include:

Environment setup
Dependency installation
Infrastructure startup
Database migration
Service startup
Test execution
Linting
Formatting
Documentation generation
Cleanup

These commands should be available through a consistent interface (for example, a Makefile, task runner, or repository scripts) so contributors do not need to memorize complex command sequences.

# 2.12 Debugging Environment

Every engineer should have access to a standardized debugging environment.

Backend
VS Code debugger
Python breakpoints
FastAPI debugging
SQL query inspection
API request tracing
Frontend
Browser developer tools
React Developer Tools
Network inspection
State inspection
Performance profiling
Infrastructure
Kubernetes logs
Docker logs
Prometheus metrics
Grafana dashboards
Distributed traces

Consistent debugging tools reduce troubleshooting time across the team.

# 2.13 Development Data

Development environments require representative but non-sensitive data.

Guidelines
Never use production data directly.
Generate realistic sample datasets.
Seed databases automatically.
Reset development environments easily.
Maintain deterministic test data where practical.

This approach supports effective testing while protecting sensitive information.

# 2.14 Local Testing

Before code is committed, engineers should execute local validation.

Validation : Required
Formatting : ✓
Linting : ✓
Static Analysis : ✓
Unit Tests : ✓
API Tests : When Applicable
Integration Tests : When Applicable
Frontend Tests : When Applicable

Early validation reduces CI failures and shortens feedback cycles.

# 2.15 Development Best Practices

The following practices apply to every development workstation.

Keep tool versions up to date within the approved compatibility range.
Pull repository updates regularly.
Rebuild containers after dependency changes.
Restart infrastructure when configuration changes occur.
Use isolated feature branches.
Avoid committing temporary debugging changes.
Validate changes locally before opening a pull request.
Document local environment issues to improve onboarding documentation.

These practices promote consistency and reduce avoidable development friction.

# 2.16 Troubleshooting Guidelines

Common development issues should be addressed systematically.

Problem : Recommended Action
Dependency conflicts : Reinstall dependencies using the approved package manager.
Container failures : Rebuild and restart affected containers.
Database migration errors : Verify migration order and schema version.
API connection failures : Confirm that required infrastructure services are running.
Authentication issues : Validate environment variables and local credentials.
Build failures : Review logs, clear caches if appropriate, and rebuild.

Persistent issues should be documented in the repository's troubleshooting guide to improve future developer experience.

# 2.17 Development Environment Checklist

Before beginning feature development, every engineer should verify the following.

Checklist Item : Status
Repository cloned : □
Dependencies installed : □
Environment variables configured : □
Infrastructure services running : □
Database migrations applied : □
Development data seeded : □
Backend starts successfully : □
Frontend starts successfully : □
Tests execute successfully : □
Linting and formatting tools configured : □
Debugging tools operational : □

This checklist ensures that the local development environment is fully prepared before implementation begins.

# 2.18 Chapter Summary

This chapter established the official Development Environment standards for AAOP. It defined the supported operating systems, required software, IDE configuration, repository initialization process, environment variable management, local infrastructure, dependency management strategy, debugging tools, testing workflow, and troubleshooting practices required to create a consistent engineering experience.

By standardizing the development environment, AAOP ensures that all contributors work within a reproducible and production-aligned ecosystem, reducing configuration drift, simplifying onboarding, and improving collaboration between human engineers and AI coding agents.