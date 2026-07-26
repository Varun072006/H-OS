"""Working Workplace Ergonomics & Posture Monitoring Demo."""

import numpy as np

from ai.embeddings.extractor import MotionEmbeddingExtractor
from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN
from ai.predictions.ergonomics import ErgonomicAnalysisPredictionModule
from ai.predictions.posture import UnsafePosturePredictionModule


def main() -> None:
    print("=== HumanOS Workplace Safety & Ergonomics Monitor ===")

    stgcn = STGCN(STGCNConfig())
    embedding_extractor = MotionEmbeddingExtractor(stgcn)
    posture_mod = UnsafePosturePredictionModule()
    ergo_mod = ErgonomicAnalysisPredictionModule()

    dummy_motion = np.random.randn(4, 15, 33).astype(np.float32)
    embedding = embedding_extractor.extract(dummy_motion)

    posture_pred = posture_mod.predict(embedding)
    ergo_pred = ergo_mod.predict(embedding)

    print(f"\n[Posture Analysis] {posture_pred.label} (Risk: {posture_pred.risk_level.value})")
    print(f"[REBA Ergonomics]  {ergo_pred.label} (Risk: {ergo_pred.risk_level.value})")


if __name__ == "__main__":
    main()
