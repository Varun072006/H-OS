# APIs

Public API definitions, contracts, and specifications for HumanOS.

This directory contains the **API specifications** (not the server implementation — that lives in `backend/`).

## Modules

### `rest/`
OpenAPI 3.1 specifications for the REST API. These specs are the source of truth for:
- Endpoint definitions
- Request/response schemas
- Authentication requirements
- Error response formats

### `grpc/`
Protocol Buffer (`.proto`) definitions for the gRPC API. Used for:
- High-throughput, low-latency inter-service communication
- Edge-to-cloud streaming
- SDK code generation

### `websocket/`
WebSocket event schemas for real-time streaming. Defines:
- Event types (human state updates, risk alerts, system events)
- Message formats
- Connection lifecycle

## API Design Principles

1. **Spec-First**: API specifications are written before implementation.
2. **Versioned**: All APIs are versioned (e.g., `/v1/`, `/v2/`).
3. **Consistent**: Follow consistent naming conventions and error formats.
4. **Documented**: Every endpoint has descriptions, examples, and error documentation.
