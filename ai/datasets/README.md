# Datasets

Dataset loaders, preprocessors, and registry for HumanOS training and evaluation.

## Supported Datasets

| Dataset | Joints | Classes | Subjects | Status |
|---------|--------|---------|----------|--------|
| NTU RGB+D 60 | 25 (3D) | 60 | 40 | 🔲 Planned |
| NTU RGB+D 120 | 25 (3D) | 120 | 106 | 🔲 Planned |
| Kinetics-Skeleton | 18 (2D) | 400 | — | 🔲 Planned |
| Custom (HumanOS) | Configurable | — | — | 🔲 Planned |

## Structure

```
datasets/
├── README.md
├── loaders/           # Per-dataset loading logic
│   ├── ntu_rgbd.py
│   ├── kinetics.py
│   └── custom.py
├── preprocessing/     # Shared preprocessing
│   ├── interpolation.py
│   ├── filtering.py
│   └── resampling.py
└── registry.py        # Dataset registry for config-driven loading
```

## Dataset Documentation

Every dataset used in HumanOS must have a corresponding datasheet in `docs/dataset_docs/` documenting:
- Source and license
- Collection methodology
- Demographic distribution
- Known biases and limitations
- Preprocessing applied
