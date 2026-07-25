# Contributing to HumanOS

Thank you for your interest in contributing to HumanOS! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/H-OS.git
   cd H-OS
   ```
3. **Create a branch** from `develop`:
   ```bash
   git checkout develop
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 20+ (for frontend)
- Docker & Docker Compose
- Git

### Python Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=humanos --cov-report=html

# Specific test category
pytest tests/unit/
pytest tests/integration/
pytest tests/privacy/
```

### Code Quality

```bash
# Linting
ruff check .

# Formatting
ruff format .

# Type checking
mypy .
```

---

## Making Changes

### Branch Naming

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New features | `feature/motion-graph-builder` |
| `fix/` | Bug fixes | `fix/normalization-nan-handling` |
| `docs/` | Documentation | `docs/api-reference-v1` |
| `research/` | Experiments | `research/transformer-encoder` |
| `refactor/` | Code refactoring | `refactor/pipeline-abstraction` |

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

<optional body>

<optional footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

Examples:
```
feat(graph): add spatial edge weighting to motion graph builder
fix(privacy): ensure frame deletion on pipeline error
docs(api): add WebSocket event schema documentation
test(stgcn): add unit tests for temporal convolution layer
```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows the project coding standards
- [ ] All tests pass (`pytest`)
- [ ] Linting passes (`ruff check .`)
- [ ] Type checking passes (`mypy .`)
- [ ] New code includes appropriate tests
- [ ] Documentation is updated for any public API changes
- [ ] Privacy impact assessment completed (if touching data handling)
- [ ] Model card updated (if modifying AI models)

### PR Description Template

```markdown
## Summary
Brief description of changes.

## Motivation
Why is this change needed?

## Changes
- List of specific changes

## Testing
How were these changes tested?

## Privacy Impact
Does this change affect data handling? If yes, describe impact.

## Breaking Changes
List any breaking changes (or "None").
```

### Review Process

- All PRs require **at least 1 maintainer approval**.
- PRs touching `privacy/` or `security/` require **2 maintainer approvals**.
- CI must pass before merge.
- Squash-merge is preferred for feature branches.

---

## Reporting Issues

### Bug Reports

Include:
1. Clear description of the bug
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python version, hardware)
6. Relevant logs or screenshots

### Feature Requests

Include:
1. Clear description of the feature
2. Use case and motivation
3. Proposed approach (if any)
4. Privacy implications (if any)

---

## Recognition

All contributors are recognized in our changelog and release notes. Significant contributions may be acknowledged in research publications.

Thank you for helping build the future of human motion intelligence! 🎯
