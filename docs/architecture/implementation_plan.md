# HumanOS — Complete Build Plan

> **Version**: 1.0
> **Based on**: SRS v1.0 + Technology Stack Specification
> **Strategy**: Bottom-up, layer-by-layer — each step produces a working, testable increment.

---

## Build Philosophy

```
Step 1  ✅ Repository Architecture & Documentation    (COMPLETED)
Step 2  ✅ Python project foundation & dev tooling     (COMPLETED)
Step 3  → Pose extraction pipeline (FR-003)
Step 4  → Motion graph construction (FR-004, FR-005)
Step 5  → ST-GCN model implementation (FR-006)
Step 6  → Training infrastructure (FR-016, FR-017, FR-018)
Step 7  → Motion embeddings & prediction modules (FR-007, FR-008, FR-009)
Step 8  → Privacy enforcement pipeline (NFR-Privacy)
Step 9  → Backend API server (FR-011, FR-014, FR-015)
Step 10 → Python SDK (FR-012)
Step 11 → Database layer
Step 12 → Streaming pipeline (FR-001, FR-002, FR-014)
Step 13 → Explainability & reasoning (FR-010)
Step 14 → Frontend dashboard (FR-019)
Step 15 → JavaScript SDK (FR-013)
Step 16 → Monitoring & telemetry
Step 17 → Docker deployment
Step 18 → Testing & quality gates
Step 19 → Edge deployment
Step 20 → Cloud deployment
Step 21 → End-to-end integration & MVP validation
```

---

## Traceability Matrix

Every SRS requirement maps to a build step:

| Requirement | Description | Build Step |
|-------------|-------------|------------|
| FR-001 | Live video capture | Step 12 |
| FR-002 | Offline video analysis | Step 12 |
| FR-003 | Pose extraction | Step 3 |
| FR-004 | Landmark → graph | Step 4 |
| FR-005 | Temporal motion graphs | Step 4 |
| FR-006 | ST-GCN processing | Step 5 |
| FR-007 | Motion embeddings | Step 7 |
| FR-008 | Prediction modules | Step 7 |
| FR-009 | Confidence scores | Step 7 |
| FR-010 | Explainable predictions | Step 13 |
| FR-011 | REST API | Step 9 |
| FR-012 | Python SDK | Step 10 |
| FR-013 | JavaScript SDK | Step 15 |
| FR-014 | Real-time streaming | Step 12 |
| FR-015 | Batch processing | Step 9 |
| FR-016 | Configurable models | Step 6 |
| FR-017 | Experiment management | Step 6 |
| FR-018 | Model versioning | Step 6 |
| FR-019 | Visualization dashboard | Step 14 |
| FR-020 | Inference logs without raw video | Step 8 |

---

## Phase 1 — Foundation

### Step 2: Python Project Foundation & Dev Tooling

**Goal**: Establish the Python package structure, dependency management, linting, type-checking, and CI so every subsequent step has a solid foundation.

**Tech**: Python 3.12+, PyTorch, ruff, mypy, pytest, GitHub Actions

#### Files to Create/Modify

```
ai/
├── __init__.py
├── graph/
│   └── __init__.py
├── models/
│   ├── __init__.py
│   └── stgcn/
│       └── __init__.py
├── datasets/
│   └── __init__.py
├── training/
│   └── __init__.py
└── evaluation/
    └── __init__.py

backend/
├── __init__.py
└── api/
    └── __init__.py

privacy/
└── __init__.py

streaming/
└── __init__.py

tests/
├── __init__.py
├── conftest.py                    # Shared fixtures
└── unit/
    └── __init__.py
```

#### Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Update with full dependency list (PyTorch, FastAPI, etc.) |
| `requirements/base.txt` | Core runtime dependencies |
| `requirements/dev.txt` | Development tools (pytest, ruff, mypy) |
| `requirements/ai.txt` | AI-specific (torch, torch-geometric, mediapipe) |
| `.github/workflows/ci.yml` | CI pipeline: lint, type-check, test |
| `Makefile` | Developer shortcuts (`make lint`, `make test`, `make format`) |

#### Acceptance Criteria

- [ ] `pip install -e ".[dev]"` installs successfully
- [ ] `ruff check .` passes with zero errors
- [ ] `mypy .` passes with zero errors
- [ ] `pytest` runs and reports 0 tests collected (no tests yet, but infra works)
- [ ] GitHub Actions CI runs on push

#### Estimated Effort: ~2 hours

---

## Phase 2 — Sensor & Pose Extraction

### Step 3: Pose Extraction Pipeline (FR-003)

**Goal**: Build the pose extraction layer that converts raw video frames into normalized skeletal joint coordinates using MediaPipe.

**Tech**: MediaPipe, OpenCV, NumPy

#### Files to Create

```
ai/
├── pose/
│   ├── __init__.py
│   ├── base.py                    # Abstract PoseExtractor interface
│   ├── mediapipe_extractor.py     # MediaPipe implementation
│   ├── types.py                   # PoseResult, Joint, Skeleton dataclasses
│   └── utils.py                   # Coordinate normalization, filtering
│
streaming/
├── __init__.py
├── ingest/
│   ├── __init__.py
│   ├── base.py                    # Abstract FrameSource interface
│   ├── webcam.py                  # USB/webcam capture (cv2.VideoCapture)
│   └── file.py                    # Video file source (for offline/testing)

tests/
├── unit/
│   ├── test_pose_extractor.py
│   ├── test_frame_source.py
│   └── fixtures/
│       └── sample_skeleton.json   # Known-good skeleton data
```

#### Key Interfaces

```python
# ai/pose/base.py
class PoseExtractor(ABC):
    @abstractmethod
    def extract(self, frame: np.ndarray) -> PoseResult: ...
    
# PoseResult contains:
#   - joints: list[Joint]  (x, y, z, visibility, confidence)
#   - timestamp: float
#   - frame_index: int
```

#### Acceptance Criteria

- [ ] `MediaPipePoseExtractor` extracts 33 body landmarks from a video frame
- [ ] Joints are normalized to body-centered coordinates
- [ ] Confidence scores are returned per-joint
- [ ] Works with both webcam and video file inputs
- [ ] Unit tests pass with sample fixture data
- [ ] Interface is abstract — other extractors can be swapped in

#### Estimated Effort: ~4 hours

---

## Phase 3 — Motion Graph & ST-GCN

### Step 4: Motion Graph Construction (FR-004, FR-005)

**Goal**: Convert sequences of skeleton poses into spatiotemporal graph tensors suitable for graph neural networks.

**Tech**: PyTorch, PyTorch Geometric, NumPy

#### Files to Create

```
ai/graph/
├── __init__.py
├── skeleton_config.py             # Joint indices, bone connections, adjacency
├── builder.py                     # SkeletonSequence → PyG Data object
├── normalization.py               # Center-of-mass normalization, scale invariance
├── augmentation.py                # Jittering, rotation, temporal crop, bone noise
└── types.py                       # MotionGraph dataclass

configs/
├── graph/
│   └── mediapipe_33.yaml          # MediaPipe 33-joint topology
│   └── ntu_25.yaml                # NTU RGB+D 25-joint topology

tests/unit/
├── test_graph_builder.py
├── test_normalization.py
└── test_augmentation.py
```

#### Key Design

```
Input:  Skeleton sequence [T frames × V joints × C channels (x,y,z)]
Output: PyG Data(x, edge_index, edge_attr)
  - Spatial edges: bone connections within each frame
  - Temporal edges: same joint across consecutive frames
  - Node features: normalized (x, y, z, confidence)
```

#### Acceptance Criteria

- [ ] Builds valid PyTorch Geometric `Data` objects from skeleton sequences
- [ ] Supports configurable joint topologies (MediaPipe 33, NTU 25)
- [ ] Normalization produces translation/scale invariant representations
- [ ] Augmentations are stochastic and configurable
- [ ] All graph tensors have correct shapes and valid edge indices
- [ ] Unit tests cover shape validation, edge correctness, and augmentation bounds

#### Estimated Effort: ~5 hours

---

### Step 5: ST-GCN Model Implementation (FR-006)

**Goal**: Implement the Spatial Temporal Graph Convolutional Network as the initial motion encoder.

**Tech**: PyTorch, PyTorch Geometric

#### Files to Create

```
ai/models/stgcn/
├── __init__.py
├── model.py                       # STGCN main model class
├── layers.py                      # ST-GCN block, spatial/temporal convolutions
├── attention.py                   # Optional attention mechanisms
└── config.py                      # Model hyperparameter dataclass

configs/model/
└── stgcn_default.yaml             # Default ST-GCN hyperparameters

tests/unit/
└── test_stgcn.py                  # Shape tests, forward pass, gradient flow
```

#### Architecture

```
Input: [N, C_in, T, V]  (batch, channels, temporal, vertices)
  │
  ├─ ST-GCN Block 1 (64 channels)
  ├─ ST-GCN Block 2 (64 channels)
  ├─ ST-GCN Block 3 (64 channels)
  ├─ ST-GCN Block 4 (128 channels)
  ├─ ST-GCN Block 5 (128 channels)
  ├─ ST-GCN Block 6 (128 channels)
  ├─ ST-GCN Block 7 (256 channels)
  ├─ ST-GCN Block 8 (256 channels)
  ├─ ST-GCN Block 9 (256 channels)
  │
  ├─ Global Average Pooling
  │
  └─ Output: [N, 256] motion embedding
             or [N, num_classes] classification logits
```

#### Acceptance Criteria

- [ ] Forward pass produces correct output shapes
- [ ] Gradients flow through all layers (no dead layers)
- [ ] Supports both embedding mode and classification mode
- [ ] Model is configurable via YAML (layers, channels, dropout)
- [ ] Parameter count matches expected values
- [ ] Can load/save checkpoints

#### Estimated Effort: ~6 hours

---

### Step 6: Training Infrastructure (FR-016, FR-017, FR-018)

**Goal**: Build config-driven training loops with experiment tracking, model versioning, and dataset loading.

**Tech**: PyTorch, MLflow, PyTorch Geometric, NumPy, scikit-learn

#### Files to Create

```
ai/
├── datasets/
│   ├── __init__.py
│   ├── registry.py                # Dataset registry (name → loader)
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── ntu_rgbd.py            # NTU RGB+D 60/120 loader
│   │   └── skeleton_folder.py     # Generic folder-of-skeletons loader
│   └── preprocessing/
│       ├── __init__.py
│       ├── interpolation.py       # Missing joint interpolation
│       └── filtering.py           # Outlier joint filtering
│
├── training/
│   ├── __init__.py
│   ├── trainer.py                 # Unified training loop
│   ├── losses.py                  # CrossEntropy, contrastive, forecasting losses
│   ├── schedulers.py              # CosineAnnealing, WarmupCosine
│   ├── callbacks.py               # Checkpointing, early stopping, logging
│   └── experiment.py              # MLflow experiment tracking wrapper
│
├── evaluation/
│   ├── __init__.py
│   ├── metrics.py                 # Top-k accuracy, F1, confusion matrix
│   └── evaluator.py              # Evaluation runner

configs/training/
├── stgcn_ntu60_xsub.yaml         # NTU60 cross-subject training config
└── stgcn_ntu60_xview.yaml         # NTU60 cross-view training config

scripts/training/
└── train.py                       # CLI training launcher
```

#### Key Features

- Config-driven: entire training run defined by a YAML file
- MLflow integration for experiment tracking
- Automatic model checkpointing with versioning
- Mixed-precision training (AMP) support
- Multi-GPU via PyTorch DDP
- Reproducible: seed control, env logging, git hash capture

#### Acceptance Criteria

- [ ] `python scripts/training/train.py --config configs/training/stgcn_ntu60_xsub.yaml` launches training
- [ ] MLflow logs metrics, params, and artifacts per run
- [ ] Checkpoints are saved with version metadata
- [ ] Training can resume from checkpoint
- [ ] Evaluation produces accuracy, F1, and confusion matrix
- [ ] Dataset loaders handle NTU RGB+D format correctly

#### Estimated Effort: ~8 hours

---

## Phase 4 — Intelligence & Prediction

### Step 7: Motion Embeddings & Prediction Modules (FR-007, FR-008, FR-009)

**Goal**: Extract reusable motion embeddings from ST-GCN and build pluggable prediction modules for fall risk, posture analysis, activity recognition, and rehabilitation tracking.

**Tech**: PyTorch, scikit-learn, NumPy

#### Files to Create

```
ai/
├── embeddings/
│   ├── __init__.py
│   ├── extractor.py               # MotionEmbeddingExtractor (model → embedding)
│   ├── store.py                   # In-memory embedding buffer with temporal context
│   └── analysis.py                # Embedding similarity, clustering, drift detection
│
├── predictions/
│   ├── __init__.py
│   ├── base.py                    # Abstract PredictionModule interface
│   ├── registry.py                # Plugin registry for prediction modules
│   ├── fall_risk.py               # Fall risk estimation (FR-008a)
│   ├── posture.py                 # Unsafe posture detection (FR-008b)
│   ├── activity.py                # Activity recognition (FR-008c)
│   ├── rehabilitation.py          # Rehabilitation progress (FR-008d)
│   ├── ergonomics.py              # Ergonomic analysis (FR-008e)
│   └── types.py                   # Prediction, Confidence, RiskLevel dataclasses

configs/
├── predictions/
│   ├── fall_risk.yaml
│   ├── posture.yaml
│   └── activity.yaml
```

#### Plugin Architecture

```python
# ai/predictions/base.py
class PredictionModule(ABC):
    @abstractmethod
    def predict(self, embedding: MotionEmbedding, context: TemporalContext) -> Prediction:
        ...

# Every prediction returns:
# Prediction(
#     label: str,
#     confidence: float,          # FR-009
#     risk_level: RiskLevel,
#     contributing_features: list, # For explainability (Step 13)
#     timestamp: datetime,
#     model_version: str
# )
```

#### Acceptance Criteria

- [ ] Embeddings are extractable from trained ST-GCN model
- [ ] At least one prediction module (activity recognition) produces validated results
- [ ] All predictions include confidence scores (FR-009)
- [ ] New prediction modules can be added without modifying core code
- [ ] Prediction registry auto-discovers modules
- [ ] Unit tests for each prediction module

#### Estimated Effort: ~8 hours

---

## Phase 5 — Privacy & Security

### Step 8: Privacy Enforcement Pipeline (NFR-Privacy, FR-020)

**Goal**: Implement the privacy-first pipeline: guaranteed frame deletion, skeleton anonymization, audit logging, and consent management.

**Tech**: Python, cryptography

#### Files to Create

```
privacy/
├── __init__.py
├── frame_deletion.py              # Secure frame zeroing + deletion verification
├── anonymization.py               # Skeleton de-identification (height norm, proportion noise)
├── audit_log.py                   # Immutable audit trail with cryptographic hashing
├── consent.py                     # Consent management framework
├── retention.py                   # Configurable data retention policies
└── compliance/
    ├── __init__.py
    ├── gdpr.py                    # GDPR compliance checks
    └── hipaa.py                   # HIPAA compliance checks

security/
├── __init__.py
├── encryption/
│   ├── __init__.py
│   └── aes.py                    # AES-256 encryption for data at rest
├── auth/
│   ├── __init__.py
│   ├── jwt_handler.py            # JWT token generation/validation
│   ├── oauth2.py                 # OAuth2 flow implementation
│   └── rbac.py                   # Role-based access control
└── policies/
    ├── __init__.py
    └── api_keys.py               # API key management

tests/privacy/
├── test_frame_deletion.py
├── test_anonymization.py
├── test_audit_log.py
└── test_consent.py
```

#### Key Guarantee

```python
# The pipeline enforces:
# 1. Frame enters memory
# 2. Pose extraction runs
# 3. Frame buffer is ZEROED (not just freed)
# 4. Audit log records deletion with SHA-256 hash
# 5. Only skeleton data proceeds downstream
#
# This is enforced via context manager:
async with PrivacyBoundary(audit_log) as boundary:
    skeleton = boundary.extract_and_delete(frame, extractor)
    # frame is guaranteed deleted here
```

#### Acceptance Criteria

- [ ] Raw frames are provably zeroed after pose extraction
- [ ] Audit log records every frame deletion with timestamp and hash
- [ ] Skeleton anonymization prevents height/proportion-based identification
- [ ] Consent manager supports opt-in/opt-out workflows
- [ ] Data retention policies are configurable and enforced
- [ ] 95%+ test coverage on privacy module
- [ ] Security: JWT auth works, RBAC restricts endpoints, AES-256 encrypts stored data

#### Estimated Effort: ~6 hours

---

## Phase 6 — Backend & API

### Step 9: Backend API Server (FR-011, FR-014, FR-015)

**Goal**: Build the FastAPI server exposing human state, predictions, and system management via REST and WebSocket.

**Tech**: FastAPI, Uvicorn, Pydantic, Redis, PostgreSQL (SQLAlchemy)

#### Files to Create

```
backend/
├── __init__.py
├── main.py                        # FastAPI app factory
├── config.py                      # Settings (Pydantic BaseSettings)
├── dependencies.py                # Dependency injection
│
├── api/
│   ├── __init__.py
│   ├── router.py                  # Main API router
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── health.py              # Health check endpoints
│   │   ├── sessions.py            # Camera session management
│   │   ├── state.py               # Human state queries
│   │   ├── predictions.py         # Prediction endpoints
│   │   ├── models.py              # Model management endpoints
│   │   └── batch.py               # Batch processing endpoints (FR-015)
│   └── ws/
│       ├── __init__.py
│       └── stream.py              # WebSocket streaming (FR-014)
│
├── services/
│   ├── __init__.py
│   ├── inference.py               # Inference orchestration service
│   ├── session_manager.py         # Camera session lifecycle
│   ├── model_manager.py           # Model loading, versioning, hot-swap
│   └── state_manager.py           # Human state accumulation
│
├── workers/
│   ├── __init__.py
│   ├── batch_worker.py            # Celery batch processing worker
│   └── inference_worker.py        # Background inference tasks
│
├── schemas/
│   ├── __init__.py
│   ├── requests.py                # API request models
│   ├── responses.py               # API response models
│   └── events.py                  # WebSocket event models

apis/rest/
└── openapi.yaml                   # Generated OpenAPI 3.1 specification

tests/
├── unit/test_api_endpoints.py
└── integration/test_inference_pipeline.py
```

#### Key Endpoints

| Method | Endpoint | Description | FR |
|--------|----------|-------------|-----|
| `GET` | `/v1/health` | System health check | — |
| `POST` | `/v1/sessions` | Create camera session | FR-001 |
| `GET` | `/v1/sessions/{id}/state` | Get current human state | FR-011 |
| `GET` | `/v1/sessions/{id}/predictions` | Get predictions | FR-008 |
| `POST` | `/v1/batch/analyze` | Submit batch analysis | FR-015 |
| `GET` | `/v1/models` | List available models | FR-016 |
| `WS` | `/v1/ws/stream/{session_id}` | Real-time streaming | FR-014 |

#### Acceptance Criteria

- [ ] FastAPI server starts and serves OpenAPI docs at `/docs`
- [ ] All endpoints return correct response schemas (Pydantic validated)
- [ ] WebSocket streams real-time predictions
- [ ] Batch processing accepts video files and returns results
- [ ] JWT authentication protects all endpoints
- [ ] RBAC restricts model management to admins
- [ ] Rate limiting prevents abuse
- [ ] Integration test: camera → pose → graph → model → API response

#### Estimated Effort: ~10 hours

---

### Step 10: Python SDK (FR-012)

**Goal**: Build the Python client SDK so developers can interact with HumanOS without touching HTTP directly.

**Tech**: Python, httpx, Pydantic, WebSocket

#### Files to Create

```
sdk/python/
├── humanos/
│   ├── __init__.py
│   ├── client.py                  # HumanOSClient main class
│   ├── session.py                 # Session management
│   ├── models.py                  # SDK data models
│   ├── streaming.py               # WebSocket streaming client
│   ├── batch.py                   # Batch processing client
│   ├── exceptions.py              # SDK-specific exceptions
│   └── auth.py                    # Authentication handling
├── pyproject.toml                 # SDK package config
├── README.md                      # SDK documentation
└── examples/
    ├── basic_usage.py
    ├── streaming_example.py
    └── batch_example.py

tests/unit/
└── test_python_sdk.py
```

#### Usage Example

```python
from humanos import HumanOSClient

client = HumanOSClient(
    endpoint="http://localhost:8000",
    api_key="your-api-key"
)

# Create session
session = client.create_session(source="webcam:0")

# Get current state
state = session.get_state()
print(f"Posture quality: {state.posture.quality}")
print(f"Fall risk: {state.predictions.fall_risk}")

# Stream real-time updates
for update in session.stream():
    print(f"[{update.timestamp}] {update.predictions}")
```

#### Acceptance Criteria

- [ ] SDK installable via `pip install humanos`
- [ ] All API endpoints are wrapped with typed methods
- [ ] Streaming client handles reconnection gracefully
- [ ] Comprehensive docstrings and type hints
- [ ] Example scripts work end-to-end

#### Estimated Effort: ~5 hours

---

## Phase 7 — Data & Streaming

### Step 11: Database Layer

**Goal**: Set up persistent storage for sessions, predictions, metrics, audit logs, and embeddings.

**Tech**: PostgreSQL, Redis, InfluxDB, Qdrant, SQLAlchemy, Alembic

#### Files to Create

```
backend/
├── database/
│   ├── __init__.py
│   ├── engine.py                  # SQLAlchemy async engine setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── session.py             # Session ORM model
│   │   ├── prediction.py          # Prediction log ORM model
│   │   ├── audit.py               # Audit log ORM model
│   │   └── model_registry.py      # Model version ORM model
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── session_repo.py
│   │   ├── prediction_repo.py
│   │   └── audit_repo.py
│   └── migrations/
│       └── alembic.ini            # Database migration config

configs/deployment/
├── database.yaml                  # Database connection configs
```

#### Database Mapping

| Database | Purpose | Data |
|----------|---------|------|
| **PostgreSQL** | Primary relational | Sessions, users, model registry, configs |
| **Redis** | Cache + message queue | Active session state, inference queue, pub/sub |
| **InfluxDB** | Time-series metrics | Inference latency, prediction history, system metrics |
| **Qdrant** | Vector search | Motion embeddings for similarity search |

#### Acceptance Criteria

- [ ] Database migrations run cleanly (Alembic)
- [ ] CRUD operations work for all models
- [ ] Redis caching reduces repeat query latency
- [ ] InfluxDB stores time-series prediction data
- [ ] Qdrant stores and queries motion embeddings by similarity

#### Estimated Effort: ~6 hours

---

### Step 12: Streaming Pipeline (FR-001, FR-002, FR-014)

**Goal**: Build the real-time video/sensor stream processing pipeline from camera to predictions.

**Tech**: OpenCV, Redis Streams, asyncio, WebRTC

#### Files to Create

```
streaming/
├── __init__.py
├── ingest/
│   ├── __init__.py
│   ├── base.py                    # Abstract FrameSource
│   ├── webcam.py                  # USB camera (FR-001)
│   ├── rtsp.py                    # IP camera via RTSP (FR-001)
│   ├── file.py                    # Video file (FR-002)
│   └── webrtc.py                  # Browser camera via WebRTC
│
├── pipeline/
│   ├── __init__.py
│   ├── pipeline.py                # Main processing pipeline orchestrator
│   ├── stages.py                  # Pipeline stages (pose → graph → inference → output)
│   └── config.py                  # Pipeline configuration
│
├── buffer/
│   ├── __init__.py
│   ├── ring_buffer.py             # Fixed-memory ring buffer for frames
│   └── sync.py                    # Multi-stream temporal synchronization

tests/integration/
└── test_streaming_pipeline.py
```

#### Pipeline Architecture

```
FrameSource → RingBuffer → PoseExtraction → PrivacyBoundary → GraphBuilder
                                                                    │
                                                                    ▼
                              WebSocket ← API ← StateManager ← STGCNInference
```

#### Acceptance Criteria

- [ ] Webcam stream processes at ≥25 FPS on recommended hardware
- [ ] RTSP ingestion handles network interruptions gracefully
- [ ] Video file processing works for offline batch analysis (FR-002)
- [ ] Ring buffer enforces bounded memory usage
- [ ] Privacy boundary is enforced within the pipeline (no frame leaks)
- [ ] End-to-end pipeline: camera → prediction in <100ms (GPU)

#### Estimated Effort: ~8 hours

---

## Phase 8 — Explainability & Frontend

### Step 13: Explainability & Reasoning (FR-010)

**Goal**: Add human-readable explanations for predictions with contributing features, confidence breakdown, and causal reasoning.

**Tech**: Captum (PyTorch explainability), custom reasoning engine

#### Files to Create

```
ai/
├── explainability/
│   ├── __init__.py
│   ├── feature_attribution.py     # Which joints/movements drove the prediction
│   ├── confidence_breakdown.py    # Confidence score decomposition
│   └── explanation_generator.py   # Natural language explanation generation
│
├── reasoning/
│   ├── __init__.py
│   ├── engine.py                  # Rule-based + learned reasoning engine
│   ├── rules.py                   # Configurable risk rules
│   └── causal.py                  # Causal inference chains

configs/reasoning/
└── rules_default.yaml             # Default reasoning rules
```

#### Explanation Format

```json
{
  "prediction": "fall_risk_elevated",
  "confidence": 0.78,
  "explanation": "Fall risk is elevated due to increasing gait instability over the past 3 minutes.",
  "contributing_features": [
    {"feature": "left_knee_flexion_angle", "importance": 0.34, "trend": "decreasing"},
    {"feature": "center_of_mass_sway", "importance": 0.28, "trend": "increasing"},
    {"feature": "step_length_variance", "importance": 0.16, "trend": "increasing"}
  ],
  "timestamp": "2025-07-25T18:30:00Z",
  "model_version": "stgcn-v0.3.1"
}
```

#### Acceptance Criteria

- [ ] Every prediction includes a human-readable explanation (FR-010)
- [ ] Feature attributions identify which joints contributed most
- [ ] Explanations include timestamp and model version (per SRS Explainability NFR)
- [ ] Reasoning engine produces causal chains for risk predictions
- [ ] Explanations are honest — they don't overstate model confidence

#### Estimated Effort: ~6 hours

---

### Step 14: Frontend Dashboard (FR-019)

**Goal**: Build the real-time monitoring dashboard with live camera feed, prediction panels, performance monitoring, and configuration.

**Tech**: Next.js 15, React 19, TypeScript, Tailwind CSS, shadcn/ui, Zustand, TanStack Query, Recharts, Framer Motion

#### Files to Create

```
frontend/
├── package.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── postcss.config.js
│
├── app/
│   ├── layout.tsx                 # Root layout with providers
│   ├── page.tsx                   # Landing / dashboard home
│   ├── dashboard/
│   │   └── page.tsx               # Main monitoring dashboard
│   ├── analytics/
│   │   └── page.tsx               # Analytics & history
│   ├── models/
│   │   └── page.tsx               # Model management
│   └── settings/
│       └── page.tsx               # Configuration panel
│
├── components/
│   ├── ui/                        # shadcn/ui components
│   ├── layout/
│   │   ├── sidebar.tsx
│   │   ├── header.tsx
│   │   └── footer.tsx
│   ├── dashboard/
│   │   ├── camera-feed.tsx        # Live camera view with skeleton overlay
│   │   ├── prediction-panel.tsx   # Real-time prediction cards
│   │   ├── risk-gauge.tsx         # Risk level gauge
│   │   ├── state-timeline.tsx     # Human state over time
│   │   └── performance-chart.tsx  # Inference latency, FPS charts
│   ├── analytics/
│   │   ├── history-table.tsx      # Prediction history
│   │   └── trend-chart.tsx        # Trend analysis
│   └── models/
│       ├── model-card.tsx         # Model info display
│       └── model-selector.tsx     # Active model selection
│
├── lib/
│   ├── api.ts                     # API client (TanStack Query)
│   ├── websocket.ts               # WebSocket connection manager
│   └── store.ts                   # Zustand global state
│
├── hooks/
│   ├── use-stream.ts              # Real-time stream hook
│   ├── use-predictions.ts         # Prediction data hook
│   └── use-performance.ts         # Performance metrics hook
│
└── styles/
    └── globals.css                # Tailwind base + custom styles
```

#### Dashboard Features

| Feature | SRS Ref | Component |
|---------|---------|-----------|
| Live camera feed | FR-019 | `camera-feed.tsx` |
| Prediction panels | FR-019 | `prediction-panel.tsx` |
| Performance monitoring | FR-019 | `performance-chart.tsx` |
| Model selection | FR-019 | `model-selector.tsx` |
| Configuration panel | FR-019 | `settings/page.tsx` |
| History viewer | FR-019 | `history-table.tsx` |
| Analytics dashboard | FR-019 | `analytics/page.tsx` |

#### Acceptance Criteria

- [ ] Dashboard renders with skeleton overlay on live camera feed
- [ ] Predictions update in real-time via WebSocket
- [ ] Risk gauge shows current fall risk with color coding
- [ ] Performance charts show inference latency and FPS
- [ ] Model selector allows switching active models
- [ ] Responsive layout works on desktop and tablet
- [ ] Dark mode by default with premium aesthetics
- [ ] Framer Motion animations on state transitions

#### Estimated Effort: ~12 hours

---

### Step 15: JavaScript SDK (FR-013)

**Goal**: TypeScript/JavaScript client SDK for web integration.

**Tech**: TypeScript, fetch API, WebSocket

#### Files to Create

```
sdk/javascript/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts                   # Main exports
│   ├── client.ts                  # HumanOSClient class
│   ├── session.ts                 # Session management
│   ├── streaming.ts               # WebSocket streaming
│   ├── types.ts                   # TypeScript interfaces
│   └── errors.ts                  # Error types
├── README.md
└── examples/
    └── browser-example.html

tests/
└── unit/test_js_sdk.ts
```

#### Acceptance Criteria

- [ ] SDK publishable via npm
- [ ] Full TypeScript type definitions
- [ ] WebSocket streaming with auto-reconnect
- [ ] Works in both Node.js and browser environments
- [ ] Example demonstrates browser integration

#### Estimated Effort: ~5 hours

---

## Phase 9 — Infrastructure

### Step 16: Monitoring & Telemetry

**Goal**: System health, GPU/CPU/memory metrics, inference latency, and error tracking.

**Tech**: Prometheus, Grafana, Loki, Jaeger, Sentry, Uptime Kuma

#### Files to Create

```
monitoring/
├── telemetry/
│   ├── __init__.py
│   ├── metrics.py                 # Custom Prometheus metrics
│   ├── middleware.py              # FastAPI middleware for request metrics
│   └── exporters/
│       ├── __init__.py
│       └── prometheus.py          # Prometheus exporter
│
├── dashboards/
│   ├── system_health.json         # Grafana dashboard: CPU, GPU, memory
│   ├── inference.json             # Grafana dashboard: latency, throughput
│   └── privacy.json               # Grafana dashboard: frame deletions, audits
│
├── alerts/
│   └── alert_rules.yaml           # Prometheus alert rules

deployment/docker/
├── docker-compose.monitoring.yml  # Prometheus + Grafana + Loki + Jaeger stack
```

#### Key Metrics (per SRS §13)

| Metric | Type | Threshold |
|--------|------|-----------|
| `humanos_system_cpu_usage` | Gauge | Alert > 90% |
| `humanos_system_gpu_usage` | Gauge | Alert > 95% |
| `humanos_system_memory_bytes` | Gauge | Alert > 85% |
| `humanos_inference_latency_ms` | Histogram | Alert p99 > 200ms |
| `humanos_api_latency_ms` | Histogram | Alert p99 > 500ms |
| `humanos_prediction_accuracy` | Gauge | Monitor trend |
| `humanos_errors_total` | Counter | Alert rate > 10/min |

#### Acceptance Criteria

- [ ] Prometheus scrapes metrics from FastAPI server
- [ ] Grafana dashboards show all SRS §13 metrics
- [ ] Alerts fire on threshold violations
- [ ] Jaeger traces show end-to-end request flow
- [ ] Sentry captures and reports errors
- [ ] Loki aggregates structured logs

#### Estimated Effort: ~5 hours

---

### Step 17: Docker Deployment (SRS §12)

**Goal**: Full containerized deployment with Docker and Docker Compose.

**Tech**: Docker, Docker Compose, NVIDIA Container Toolkit

#### Files to Create

```
deployment/docker/
├── Dockerfile.backend             # FastAPI backend
├── Dockerfile.frontend            # Next.js frontend
├── Dockerfile.ai                  # AI inference worker (GPU-enabled)
├── Dockerfile.streaming           # Streaming pipeline worker
├── docker-compose.yml             # Full stack (dev)
├── docker-compose.prod.yml        # Production overrides
├── docker-compose.monitoring.yml  # Monitoring stack
├── .dockerignore
└── entrypoint.sh                  # Container entrypoint with health checks

deployment/ci/
├── .github/workflows/ci.yml       # CI: lint, test, build
├── .github/workflows/release.yml  # CD: build images, push, deploy
└── .github/workflows/security.yml # Security: dependency scan, SAST
```

#### Docker Compose Services

| Service | Image | Ports | GPU |
|---------|-------|-------|-----|
| `backend` | `humanos/backend` | 8000 | ❌ |
| `frontend` | `humanos/frontend` | 3000 | ❌ |
| `ai-worker` | `humanos/ai` | — | ✅ |
| `streaming` | `humanos/streaming` | — | ✅ |
| `postgres` | `postgres:16` | 5432 | ❌ |
| `redis` | `redis:7` | 6379 | ❌ |
| `influxdb` | `influxdb:2` | 8086 | ❌ |
| `qdrant` | `qdrant/qdrant` | 6333 | ❌ |
| `prometheus` | `prom/prometheus` | 9090 | ❌ |
| `grafana` | `grafana/grafana` | 3001 | ❌ |

#### Acceptance Criteria

- [ ] `docker compose up` brings up the entire stack
- [ ] GPU inference works via NVIDIA Container Toolkit
- [ ] Health checks on all services
- [ ] Volumes persist data across restarts
- [ ] CI pipeline builds and tests on every PR
- [ ] Multi-stage builds produce minimal production images

#### Estimated Effort: ~6 hours

---

### Step 18: Testing & Quality Gates (SRS §14)

**Goal**: Comprehensive test suites covering all SRS §14 requirements.

**Tech**: pytest, Vitest, Playwright, Locust, OWASP ZAP

#### Test Suites

| Suite | Location | Tool | SRS Ref |
|-------|----------|------|---------|
| Unit tests | `tests/unit/` | pytest | §14 |
| Integration tests | `tests/integration/` | pytest | §14 |
| API tests | `tests/integration/test_api.py` | pytest + httpx | §14 |
| Model validation | `tests/unit/test_model_validation.py` | pytest | §14 |
| Performance tests | `tests/performance/` | pytest-benchmark + Locust | §14 |
| Stress tests | `tests/performance/test_stress.py` | Locust | §14 |
| Security tests | `tests/security/` | OWASP ZAP | §14 |
| Regression tests | CI automated suite | pytest | §14 |
| Frontend tests | `frontend/__tests__/` | Vitest | §14 |
| E2E tests | `tests/e2e/` | Playwright | §14 |
| Privacy tests | `tests/privacy/` | pytest | §14 |

#### Coverage Requirements

| Module | Minimum | Rationale |
|--------|---------|-----------|
| `privacy/` | 95% | Safety-critical |
| `security/` | 95% | Safety-critical |
| `ai/graph/` | 90% | Data integrity |
| `backend/api/` | 90% | User-facing |
| `ai/models/` | 80% | Research code |
| Overall | 80% | Quality baseline |

#### Acceptance Criteria

- [ ] All SRS §14 test types have at least one test
- [ ] Coverage meets minimums per module
- [ ] CI enforces coverage thresholds (fail if below)
- [ ] Performance tests baseline inference latency
- [ ] Locust stress test handles 100 concurrent API users
- [ ] Playwright E2E covers dashboard critical paths
- [ ] OWASP ZAP finds no critical/high vulnerabilities

#### Estimated Effort: ~8 hours

---

## Phase 10 — Production Deployment

### Step 19: Edge Deployment (SRS §12)

**Goal**: Package HumanOS for edge devices (Jetson, Coral, Raspberry Pi).

**Tech**: ONNX Runtime, TensorRT, TFLite, Docker

#### Files to Create

```
ai/models/export/
├── __init__.py
├── onnx_export.py                 # PyTorch → ONNX conversion
├── tensorrt_export.py             # ONNX → TensorRT (Jetson)
├── tflite_export.py               # ONNX → TFLite (Coral)
└── validate_export.py             # Accuracy validation post-export

deployment/edge/
├── jetson/
│   ├── Dockerfile                 # JetPack-based container
│   ├── deploy.sh                  # Deployment script
│   └── config.yaml                # Jetson-specific config
├── coral/
│   ├── Dockerfile
│   └── config.yaml
└── raspberry_pi/
    ├── Dockerfile
    └── config.yaml

benchmarks/latency/
├── edge_benchmark.py              # Edge device latency profiling
```

#### Acceptance Criteria

- [ ] ONNX export produces valid model with matching accuracy (±0.5%)
- [ ] TensorRT model runs on Jetson with <200ms end-to-end latency
- [ ] Edge containers are minimal size (<500MB)
- [ ] Edge deployment works fully offline (no cloud dependency)

#### Estimated Effort: ~8 hours

---

### Step 20: Cloud Deployment (SRS §12)

**Goal**: Production Kubernetes deployment with auto-scaling, secrets management, and infrastructure as code.

**Tech**: Kubernetes, Helm, Terraform, HashiCorp Vault, NGINX

#### Files to Create

```
deployment/cloud/
├── kubernetes/
│   ├── namespace.yaml
│   ├── backend-deployment.yaml
│   ├── ai-worker-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── services.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml                   # Horizontal Pod Autoscaler
│   └── network-policies.yaml
│
├── helm/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values.production.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       └── configmap.yaml
│
├── terraform/
│   ├── main.tf                    # AWS infrastructure
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules/
│   │   ├── vpc/
│   │   ├── eks/
│   │   ├── rds/
│   │   └── ecr/
│   └── environments/
│       ├── staging/
│       └── production/
```

#### Acceptance Criteria

- [ ] Helm chart deploys the full stack to Kubernetes
- [ ] Terraform provisions cloud infrastructure (AWS)
- [ ] HPA auto-scales AI workers based on queue depth
- [ ] Network policies restrict pod-to-pod communication
- [ ] Secrets managed via Vault (no plaintext secrets)
- [ ] 99.9% availability target with health checks and rolling updates

#### Estimated Effort: ~10 hours

---

### Step 21: End-to-End Integration & MVP Validation

**Goal**: Validate all SRS success criteria and ship MVP.

**SRS §17 Success Criteria**:

| Criterion | Validation Method |
|-----------|-------------------|
| Process live skeletal motion | Demo: webcam → skeleton → API |
| Generate motion embeddings | Test: embedding shape and similarity |
| Perform at least one validated prediction | Demo: fall risk or activity recognition |
| Return predictions through API | Test: API returns valid Prediction response |
| Operate without storing identifiable video | Audit: privacy test suite passes, audit log verified |
| Demonstrate modularity | Test: add new prediction module without core changes |

#### Final Deliverables

```
examples/
├── fall_detection/
│   ├── README.md
│   └── main.py                    # Working fall detection demo
├── workplace_safety/
│   ├── README.md
│   └── main.py                    # Posture monitoring demo
├── basic_tracking/
│   ├── README.md
│   └── main.py                    # Minimal skeleton tracking

docs/
├── deployment_guides/
│   ├── local_development.md
│   ├── docker_deployment.md
│   ├── edge_deployment.md
│   └── cloud_deployment.md
```

#### Acceptance Criteria

- [ ] All 6 SRS success criteria validated
- [ ] End-to-end demo: webcam → prediction → dashboard
- [ ] All tests pass (unit, integration, e2e, privacy, security, performance)
- [ ] Documentation complete for all SRS §15 requirements
- [ ] Docker deployment works out of the box
- [ ] Version tagged as v0.1.0

#### Estimated Effort: ~6 hours

---

## Summary

### Build Timeline

| Phase | Steps | Description | Total Effort |
|-------|-------|-------------|--------------|
| **Phase 1** | 2 | Foundation & tooling | ~2 hours |
| **Phase 2** | 3 | Pose extraction | ~4 hours |
| **Phase 3** | 4–6 | Motion graph, ST-GCN, training | ~19 hours |
| **Phase 4** | 7 | Embeddings & predictions | ~8 hours |
| **Phase 5** | 8 | Privacy & security | ~6 hours |
| **Phase 6** | 9–10 | Backend API & Python SDK | ~15 hours |
| **Phase 7** | 11–12 | Database & streaming | ~14 hours |
| **Phase 8** | 13–15 | Explainability, dashboard, JS SDK | ~23 hours |
| **Phase 9** | 16–18 | Monitoring, Docker, testing | ~19 hours |
| **Phase 10** | 19–21 | Edge, cloud, MVP validation | ~24 hours |
| | | **Total** | **~134 hours** |

### Technology Stack Alignment

> [!IMPORTANT]
> The tech stack in this plan matches your specification exactly:
> - **Frontend**: Next.js 15 + React 19 + Tailwind CSS + shadcn/ui + Zustand + TanStack Query + Recharts + Framer Motion
> - **Backend**: FastAPI + Celery + Redis + APScheduler + OAuth2/JWT
> - **AI**: PyTorch + PyTorch Geometric + ST-GCN + MediaPipe + OpenCV + MLflow + ONNX + TensorRT + Captum
> - **Database**: PostgreSQL + Redis + InfluxDB + Qdrant + MinIO
> - **Monitoring**: Prometheus + Grafana + Loki + Jaeger + Sentry
> - **Deployment**: Docker + Kubernetes + Helm + Terraform + Vault
> - **Testing**: pytest + Vitest + Playwright + Locust + OWASP ZAP

### Milestone Markers

| Milestone | After Step | What Works |
|-----------|-----------|------------|
| 🏗️ **Infrastructure Ready** | Step 2 | Project builds, lints, tests |
| 👁️ **Pose Extraction** | Step 3 | Camera → skeleton joints |
| 🧠 **AI Pipeline** | Step 6 | Graph → ST-GCN → trained model |
| 🔮 **Predictions** | Step 7 | Embeddings → fall risk / activity |
| 🔒 **Privacy Enforced** | Step 8 | Frame deletion + audit trail |
| 🌐 **API Live** | Step 9 | REST + WebSocket serving predictions |
| 📊 **Dashboard** | Step 14 | Real-time monitoring UI |
| 🐳 **Containerized** | Step 17 | Full stack in Docker |
| ✅ **MVP** | Step 21 | All SRS success criteria met |
