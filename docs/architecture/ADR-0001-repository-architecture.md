# ADR-0001: Repository Architecture and Module Boundaries

## Status

**Accepted** — 2025

## Context

HumanOS requires a repository architecture that supports:
- Long-term development by a growing contributor base
- Clear separation between AI research, backend services, privacy enforcement, and deployment
- Independent evolution of each architectural layer
- Research experimentation without disrupting production code

## Decision

We adopt a **monorepo** structure with clearly separated top-level directories for each concern:

| Directory | Responsibility |
|-----------|----------------|
| `ai/` | All AI/ML code: models, graph construction, datasets, training, evaluation |
| `backend/` | API servers, services, and business logic |
| `frontend/` | Web-based UIs and dashboards |
| `privacy/` | Privacy enforcement (frame deletion, anonymization, audit) |
| `security/` | Security policies, encryption, authentication |
| `streaming/` | Real-time stream processing |
| `apis/` | API specifications and contracts (not implementations) |
| `sdk/` | Client SDKs |
| `deployment/` | Infrastructure-as-code for all deployment targets |
| `monitoring/` | Observability, telemetry, and alerting |

Each directory is a self-contained module with its own README and clear boundaries.

## Consequences

### Positive
- Clear ownership boundaries for each module
- Independent testing and development
- Easy onboarding — contributors can focus on their area
- Monorepo enables atomic cross-module changes when needed

### Negative
- Monorepo can become large over time (mitigated by `.gitignore` for data/models)
- CI/CD must be smart about which tests to run (mitigated by path-based triggers)
- Need to enforce boundary discipline through code review and linting
