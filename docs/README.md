# Documentation

Comprehensive project documentation for HumanOS.

## Structure

| Directory | Purpose |
|-----------|---------|
| `architecture/` | Architecture Decision Records (ADRs) and system design documents |
| `api/` | API reference documentation (OpenAPI, gRPC, WebSocket) |
| `research/` | Research notes, literature reviews, and technical deep-dives |
| `model_cards/` | Per-model documentation: architecture, training, biases, limitations |
| `dataset_docs/` | Datasheets for datasets: source, demographics, biases |
| `deployment_guides/` | Step-by-step deployment guides for each target environment |
| `onboarding/` | Developer onboarding: setup, architecture walkthrough, first-PR guide |
| `experiments/` | Structured experiment reports with reproducibility information |
| `rfcs/` | Requests for Comments — design proposals for significant changes |

## Documentation Standards

### Architecture Decision Records (ADRs)

Use the ADR format for significant architectural decisions:
```markdown
# ADR-NNNN: Title

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or harder as a result of this decision?
```

### Model Cards

Every AI model must have a model card (see `model_cards/TEMPLATE.md`).

### Experiment Reports

Every experiment must have a report (see `experiments/TEMPLATE.md`).

## Building Documentation

Documentation is written in Markdown and can be rendered with any Markdown viewer or static site generator. Future plans include MkDocs integration.
