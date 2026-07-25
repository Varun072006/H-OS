# ADR-0002: Privacy-First Architecture — Frame Deletion at Pose Extraction Boundary

## Status

**Accepted** — 2025

## Context

HumanOS processes camera feeds to understand human motion. Raw video frames contain personally identifiable information (faces, clothing, environment). The platform must be able to analyze movement without retaining identifiable data.

## Decision

We establish a **hard privacy boundary** between the Pose Extraction Layer and all downstream processing:

1. Raw frames are **ephemeral** — they exist only in memory during pose extraction.
2. After skeleton joints are extracted, the raw frame buffer is **zeroed and deallocated**.
3. No module below the privacy boundary can request, access, or reconstruct raw frames.
4. Frame deletion is **verified and audited** — every deletion is logged with a cryptographic proof.
5. The privacy module enforces this constraint independently of the streaming pipeline.

### Data Flow

```
Camera → Frame Buffer (ring buffer, bounded) → Pose Extractor → Skeleton Joints
                                                      │
                                                [Frame Buffer Zeroed]
                                                      │
                                                [Audit Log Entry]
```

## Consequences

### Positive
- Privacy compliance is structural, not behavioral — it cannot be accidentally bypassed
- GDPR/HIPAA compliance is simpler because identifiable data is never stored
- User trust is higher with demonstrable privacy guarantees

### Negative
- Debugging pose extraction issues is harder without raw frame access (mitigated by opt-in debug mode with explicit consent)
- Some future features (e.g., appearance-based re-identification) are architecturally impossible (this is intentional)
- Performance overhead of secure frame zeroing (negligible in practice)
