# Research

Research experiments, prototypes, and literature references.

## Modules

### `papers/`
Literature references and summaries. Organized by topic:
- Pose estimation
- Graph neural networks for skeleton data
- Motion forecasting
- Human activity understanding
- Privacy-preserving computer vision

### `experiments/`
Experiment scripts and notebooks for research exploration. Each experiment should follow the experiment tracking standards in `docs/experiments/`.

### `prototypes/`
Early-stage prototypes and proof-of-concept implementations. Code here is exploratory and may not meet production coding standards.

## Research Guidelines

1. **Reproducibility**: Every experiment must log its git commit, configuration, and environment.
2. **Documentation**: Write findings in `docs/experiments/` using the experiment report template.
3. **Branch Policy**: Use `research/*` branches for experimental work.
4. **Graduation**: Successful prototypes are refactored into production modules via standard PRs.

## Key Research Areas

| Area | Status | Priority |
|------|--------|----------|
| ST-GCN motion encoding | Active | High |
| Motion forecasting architectures | Planned | High |
| Learned risk reasoning | Planned | Medium |
| Transformer-based motion encoders | Planned | Medium |
| Federated learning for privacy | Future | Low |
| Diffusion-based motion prediction | Future | Low |
