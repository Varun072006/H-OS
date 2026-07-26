"""Working Fall Detection Application Demo built on HumanOS."""

import time
import numpy as np

from ai.embeddings.extractor import MotionEmbeddingExtractor
from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN
from ai.pose.mediapipe_extractor import MediaPipePoseExtractor
from ai.predictions.fall_risk import FallRiskPredictionModule
from privacy.frame_deletion import PrivacyBoundary


def main() -> None:
    print("=== HumanOS Fall Detection Application ===")

    # 1. Initialize models & privacy boundary
    extractor = MediaPipePoseExtractor()
    boundary = PrivacyBoundary()
    stgcn = STGCN(STGCNConfig())
    embedding_extractor = MotionEmbeddingExtractor(stgcn)
    fall_module = FallRiskPredictionModule()

    # 2. Simulate camera stream processing
    dummy_frame = np.ones((480, 640, 3), dtype=np.uint8) * 180

    print("\n[Step 1] Ingesting video frame...")
    pose_result = boundary.extract_and_delete(dummy_frame, extractor=extractor, frame_index=1)
    print(f"[Step 2] Frame zero-filled & privacy audit logged. Landmarks Extracted: {pose_result.has_pose}")

    print("\n[Step 3] Extracting 256-D Motion Embedding vector...")
    dummy_motion = np.random.randn(4, 10, 33).astype(np.float32)
    embedding = embedding_extractor.extract(dummy_motion)
    print(f"[Step 4] Motion Embedding extracted! Shape: {embedding.shape}")

    print("\n[Step 5] Running Fall Risk Prediction Module...")
    prediction = fall_module.predict(embedding)
    print(f"\n>>> PREDICTION RESULT >>>")
    print(f"Module: {prediction.module_name}")
    print(f"Label: {prediction.label}")
    print(f"Confidence: {prediction.confidence*100:.1f}%")
    print(f"Risk Level: {prediction.risk_level.value}")
    print(f"Contributing Features: {prediction.contributing_features}")


if __name__ == "__main__":
    main()
