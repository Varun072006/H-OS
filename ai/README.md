# AI

All AI/ML code for HumanOS: model architectures, graph construction, dataset handling, training, and evaluation.

## Modules

### `models/`
Neural network architectures for motion encoding, forecasting, and reasoning.

- **`stgcn/`** — Spatial Temporal Graph Convolutional Network. The initial motion encoder that transforms spatiotemporal skeleton graphs into dense motion embeddings. Designed to be replaceable with future architectures (MS-G3D, CTR-GCN, transformers).

- **`forecaster/`** — Motion forecasting models that predict future joint positions and body configurations from current and historical motion embeddings.

- **`reasoner/`** — Risk reasoning and causal inference models that translate motion features and predictions into structured risk assessments and recommendations.

### `graph/`
Motion graph construction and manipulation utilities.

- **`builder.py`** — Converts raw skeleton joint sequences into spatiotemporal graph tensors (PyTorch Geometric format).
- **`normalization.py`** — Joint coordinate normalization to body-centered reference frames, scale-invariant representations.
- **`augmentation.py`** — Graph-level data augmentation: joint jittering, temporal cropping, spatial rotation, bone-length perturbation.

### `datasets/`
Dataset loaders, preprocessors, and a dataset registry.

- **`loaders/`** — Per-dataset loading logic (NTU RGB+D, Kinetics-Skeleton, custom datasets).
- **`preprocessing/`** — Shared preprocessing pipelines: missing joint interpolation, outlier filtering, temporal resampling.

### `training/`
Training infrastructure.

- **`trainer.py`** — Unified, config-driven training loop supporting multi-GPU, mixed precision, and checkpoint management.
- **`losses.py`** — Custom loss functions: contrastive motion loss, forecasting loss, hierarchical classification loss.
- **`schedulers.py`** — Learning rate schedulers: cosine annealing, warm restarts, linear warmup.

### `evaluation/`
Evaluation and benchmarking.

- **`metrics.py`** — Standard and custom metrics: top-k accuracy, F1 (macro/micro), AUC-ROC, mean per-joint position error (MPJPE).
- **`benchmark_runner.py`** — Automated benchmark execution against standard datasets with result logging.

## Design Principles

1. **Replaceability**: Every model is behind an interface. ST-GCN is the first encoder, not the last.
2. **Reproducibility**: All experiments are config-driven with seed control and environment logging.
3. **Separation**: Model code never touches data loading, serving, or deployment concerns.
