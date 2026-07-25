# Developer Onboarding Guide

Welcome to HumanOS! This guide will get you set up and contributing.

## Prerequisites

- **Python 3.11+** — [Download](https://www.python.org/downloads/)
- **Git** — [Download](https://git-scm.com/downloads)
- **Docker** — [Download](https://www.docker.com/get-started) (optional, for containerized development)
- **NVIDIA GPU + CUDA** — Recommended for AI model training (not required for API/frontend work)

## Quick Setup

### 1. Clone the Repository

```bash
git clone https://github.com/humanos/H-OS.git
cd H-OS
```

### 2. Set Up Python Environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

pip install -e ".[dev]"
```

### 3. Verify Setup

```bash
# Run linting
ruff check .

# Run type checking
mypy .

# Run tests
pytest tests/unit/ -v
```

### 4. Explore the Codebase

Start by reading:
1. [README.md](../../README.md) — Project overview and architecture
2. [docs/architecture/ADR-0001](../architecture/ADR-0001-repository-architecture.md) — Repository structure rationale
3. [docs/architecture/ADR-0002](../architecture/ADR-0002-privacy-first-frame-deletion.md) — Privacy architecture
4. The README of the module you'll be working on

## Contribution Areas

| Interest | Start Here |
|----------|------------|
| AI / ML | `ai/README.md` |
| Backend / API | `backend/README.md` |
| Frontend | `frontend/README.md` |
| Privacy | `privacy/README.md` |
| Documentation | `docs/README.md` |
| DevOps | `deployment/README.md` |

## Your First PR

1. Pick an issue labeled `good first issue`
2. Create a feature branch: `git checkout -b feature/your-change`
3. Make your changes with tests
4. Run the full check suite: `ruff check . && mypy . && pytest`
5. Submit a PR against `develop`

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for full guidelines.
