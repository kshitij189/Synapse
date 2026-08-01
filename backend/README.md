# Synapse Backend

Backend service for the **Autonomous Adaptive Organization Platform (AAOP)**.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12+ |
| Framework | FastAPI |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2.x (setup only) |
| Cache | Redis (setup only) |
| Package Manager | uv |

## Quick Start

```bash
# 1. Install uv (if not already installed)
pip install uv

# 2. Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"

# 3. Copy environment template
cp .env.example .env

# 4. Start the server
uvicorn app.main:app --reload

# 5. Run tests
pytest tests/ -v
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service identification |
| GET | `/health` | Health check |
| GET | `/version` | Version information |

## Project Structure

```
backend/
├── app/
│   ├── api/          # API Layer — routers and endpoints
│   ├── core/         # Core — exceptions, logging, handlers
│   ├── common/       # Common — shared response models
│   ├── shared/       # Shared — constants, cross-cutting
│   ├── config/       # Configuration — settings
│   ├── dependencies/ # FastAPI dependency injection
│   ├── middleware/    # Middleware — request ID
│   ├── models/       # Database models (future)
│   ├── schemas/      # Pydantic schemas (future)
│   ├── services/     # Application services (future)
│   ├── utils/        # Utility functions
│   └── main.py       # Application entry point
├── tests/            # Test suite
├── pyproject.toml    # Dependencies and tooling
├── Dockerfile        # Container image
└── .env.example      # Environment variable template
```

## Docker

```bash
docker build -t synapse-backend .
docker run -p 8000:8000 synapse-backend
```

## Documentation

Refer to the project-level documentation for architecture details:

- `AI_GUIDE.md` — AI implementation guide
- `CONTEXT.md` — Project context
- `DOC_INDEX.md` — Documentation catalogue
