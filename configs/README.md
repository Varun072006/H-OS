# Configs

Configuration files for models, training, deployment, and pipelines.

## Structure

### `model/`
Model hyperparameter configurations:
- Architecture definitions (layer sizes, graph structure, attention heads)
- Pretrained model paths
- Inference settings

### `training/`
Training run configurations:
- Learning rate, batch size, epochs
- Data augmentation settings
- Loss function weights
- Distributed training settings

### `deployment/`
Deployment environment configurations:
- `base.yaml` — Default configuration
- `development.yaml` — Local development overrides
- `staging.yaml` — Staging environment overrides
- `production.yaml` — Production environment overrides
- `edge/` — Per-device edge configurations

### `pipeline/`
Processing pipeline configurations:
- Pose estimation backend selection
- Graph construction parameters
- Stream processing settings
- Privacy pipeline settings

## Configuration Precedence

```
base.yaml → environment.yaml → environment variables → CLI arguments
```

Later sources override earlier ones. Environment variables use the `HUMANOS_` prefix.

## Format

All configurations use YAML format with JSON Schema validation. Schemas are defined alongside each config directory.
