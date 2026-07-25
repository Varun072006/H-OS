# Scripts

Developer utility scripts for setup, data management, training, and releases.

## Modules

### `setup/`
Environment setup scripts:
- Development environment setup
- GPU driver and CUDA toolkit installation verification
- Dependency installation and validation

### `data/`
Data download and preparation:
- Dataset download scripts (NTU RGB+D, Kinetics)
- Data preprocessing pipelines
- Data validation and integrity checks

### `training/`
Training launch scripts:
- Single-GPU training launcher
- Multi-GPU / distributed training launcher
- Hyperparameter sweep launcher
- Experiment configuration generators

### `release/`
Release and packaging scripts:
- Version bumping
- Changelog generation
- Package building (PyPI, Docker)
- Release artifact publishing

## Usage

All scripts are designed to be run from the repository root:

```bash
# Setup development environment
python scripts/setup/dev_setup.py

# Download NTU RGB+D dataset
python scripts/data/download_ntu.py --output-dir data/ntu_rgbd/

# Launch training
python scripts/training/train.py --config configs/training/stgcn_ntu_xsub.yaml
```
