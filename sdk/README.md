# SDK

Client SDKs for application developers to interact with HumanOS.

## Modules

### `python/`
Python client SDK — the primary SDK for data scientists, researchers, and backend developers.

```python
# Example usage (conceptual)
from humanos import HumanOSClient

client = HumanOSClient(endpoint="http://localhost:8000")
session = client.create_session(camera_id="front-lobby")

for state in session.stream():
    print(f"Posture: {state.posture.quality}")
    print(f"Fall Risk: {state.predict.fall_risk(horizon='30s')}")
```

### `javascript/`
JavaScript/TypeScript SDK for web dashboard and frontend integration.

### `examples/`
Working examples demonstrating SDK usage across common use cases.

## SDK Design Principles

1. **Minimal Dependencies**: SDKs should have minimal external dependencies.
2. **Type Safety**: Full type annotations (Python type hints, TypeScript types).
3. **Async-First**: Support both synchronous and asynchronous usage patterns.
4. **Versioned**: SDK versions track API versions.
