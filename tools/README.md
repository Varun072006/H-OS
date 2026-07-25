# Tools

Internal developer tools for linting, visualization, and performance profiling.

## Modules

### `linting/`
Custom linting rules and configurations:
- Privacy-specific lint rules (detecting raw frame persistence)
- Security lint rules (detecting hardcoded secrets, insecure patterns)
- Architecture lint rules (enforcing layer boundaries)

### `visualization/`
Debug visualization utilities:
- Skeleton rendering overlays
- Motion graph visualization
- Embedding space visualization (t-SNE, UMAP)
- Prediction trajectory plotting

### `profiling/`
Performance profiling tools:
- Per-layer inference time profiling
- Memory usage analysis
- GPU utilization monitoring
- Pipeline bottleneck identification

## Usage

Tools are importable utilities, not standalone applications:

```python
from tools.visualization import skeleton_renderer
from tools.profiling import inference_profiler
```
