# Tests

All test suites for HumanOS.

## Structure

### `unit/`
Unit tests organized per-module. Each source module has a corresponding test directory:
```
tests/unit/
├── ai/
│   ├── test_graph_builder.py
│   ├── test_normalization.py
│   └── test_stgcn.py
├── privacy/
│   ├── test_frame_deletion.py
│   └── test_anonymization.py
└── backend/
    └── test_api.py
```

### `integration/`
Cross-module integration tests verifying that components work together correctly.

### `e2e/`
End-to-end tests covering the full pipeline from sensor input to API response.

### `performance/`
Performance and latency benchmarks used as regression tests.

### `privacy/`
Privacy compliance tests verifying that:
- Raw frames are never persisted
- Skeleton data is properly anonymized
- Audit logs are correctly generated
- Consent mechanisms function correctly

### `fixtures/`
Shared test data: sample skeleton sequences, mock camera feeds, expected outputs.

## Running Tests

```bash
pytest                          # All tests
pytest tests/unit/              # Unit tests only
pytest tests/privacy/           # Privacy tests only
pytest -m "not slow"            # Skip slow tests
pytest --cov=humanos            # With coverage report
```
