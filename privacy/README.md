# Privacy

Privacy enforcement and audit modules for HumanOS.

Privacy is not a feature — it is a **foundational architectural constraint** of the platform.

## Modules

### `frame_deletion.py`
Guaranteed raw frame cleanup after pose extraction. Ensures that raw video frames are immediately and verifiably deleted after skeleton extraction, with no possibility of persistence.

### `anonymization.py`
Skeleton anonymization utilities. Transforms joint coordinates to prevent any correlation with physical identity (height normalization, body proportion randomization).

### `audit_log.py`
Immutable privacy action audit trail. Logs every privacy-relevant action (frame deletion, data access, consent changes) with timestamps and cryptographic verification.

### `compliance/`
Regulatory compliance checking modules:
- **GDPR**: EU General Data Protection Regulation
- **HIPAA**: US Health Insurance Portability and Accountability Act
- **CCPA**: California Consumer Privacy Act

## Privacy Architecture

```
IDENTIFIABLE ZONE          PRIVACY BOUNDARY          ANONYMOUS ZONE
─────────────────    ──────────────────────    ─────────────────────
 Raw Camera Frame  →  Pose Extraction  →  ✗   Skeleton Joints
                      [Frame Deleted]         Motion Graph
                                              Embedding Vector
                                              Human State
                                              API Response
```

## Testing

Privacy modules have a **95% minimum code coverage requirement**. All privacy tests live in `tests/privacy/`.
