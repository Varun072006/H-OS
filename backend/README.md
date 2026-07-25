# Backend

API servers, core services, and background workers for HumanOS.

## Modules

### `api/`
REST and gRPC API server exposing human state, predictions, and system management endpoints. Built with FastAPI for automatic OpenAPI documentation generation.

### `services/`
Core business logic layer implementing human state management, session tracking, and coordination between AI inference and API responses.

### `workers/`
Background task workers for asynchronous processing: batch analysis, model warm-up, data pipeline orchestration, and scheduled maintenance tasks.

## Architecture

```
Client Request
    │
    ▼
┌─────────┐    ┌──────────┐    ┌──────────┐
│   API   │───▶│ Services │───▶│ AI Engine│
│  Server │    │  Layer   │    │          │
└─────────┘    └──────────┘    └──────────┘
                    │
                    ▼
              ┌──────────┐
              │ Workers  │
              │ (async)  │
              └──────────┘
```

## Technology

- **API Framework**: FastAPI (async, OpenAPI auto-generation)
- **Task Queue**: Celery with Redis broker
- **Database**: PostgreSQL (via SQLAlchemy)
- **Serialization**: Pydantic models
