# Examples

End-to-end usage examples demonstrating HumanOS capabilities.

## Available Examples

### `fall_detection/`
**Fall Risk Monitoring** — Demonstrates real-time fall risk prediction using a webcam feed. Shows how to:
- Connect to a camera
- Stream human state updates
- Monitor fall risk predictions
- Trigger alerts when risk exceeds thresholds

### `workplace_safety/`
**Industrial Safety Monitoring** — Demonstrates posture analysis for workplace ergonomics. Shows how to:
- Detect unsafe lifting postures
- Monitor fatigue accumulation over a shift
- Generate safety compliance reports

### `rehabilitation/`
**Rehabilitation Progress Tracking** — Demonstrates mobility assessment for rehabilitation patients. Shows how to:
- Track range of motion over time
- Compare movement patterns against baselines
- Generate progress reports

### `basic_tracking/`
**Minimal Skeleton Tracking** — The simplest possible HumanOS integration. Shows how to:
- Extract poses from a webcam
- Visualize the skeleton overlay
- Access raw joint coordinates

## Running Examples

```bash
# Install HumanOS and example dependencies
pip install -e ".[examples]"

# Run an example
python examples/basic_tracking/main.py
```

Each example includes its own README with detailed setup and usage instructions.
