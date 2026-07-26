"""Human state accumulation and embedding buffer service."""

from datetime import datetime, timezone
import numpy as np

from ai.embeddings.store import TemporalEmbeddingStore
from ai.predictions.registry import get_prediction_module, list_prediction_modules
from backend.schemas.responses import HumanStateResponse, PredictionItemSchema


class HumanStateManager:
    """Service accumulating continuous human physical state metrics across sessions."""

    def __init__(self) -> None:
        self._stores: dict[str, TemporalEmbeddingStore] = {}

    def get_store(self, session_id: str) -> TemporalEmbeddingStore:
        if session_id not in self._stores:
            self._stores[session_id] = TemporalEmbeddingStore(max_window_size=30)
        return self._stores[session_id]

    def update_state(self, session_id: str, embedding: np.ndarray) -> HumanStateResponse:
        """Update continuous human state given a new motion embedding.

        Returns:
            HumanStateResponse object.
        """
        store = self.get_store(session_id)
        store.add(embedding)
        window = store.get_window()

        # Run registered prediction modules over current embedding & context window
        predictions_out: list[PredictionItemSchema] = []
        for mod_name in list_prediction_modules():
            mod = get_prediction_module(mod_name)
            pred = mod.predict(embedding, context_window=window)
            predictions_out.append(
                PredictionItemSchema(
                    module_name=pred.module_name,
                    label=pred.label,
                    confidence=pred.confidence,
                    risk_level=pred.risk_level.value,
                    score=pred.score,
                    contributing_features=pred.contributing_features,
                    timestamp=pred.timestamp.isoformat(),
                    model_version=pred.model_version,
                )
            )

        return HumanStateResponse(
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            has_pose=True,
            posture_quality=0.85,
            gait_stability=0.90,
            fatigue_score=0.15,
            predictions=predictions_out,
        )
