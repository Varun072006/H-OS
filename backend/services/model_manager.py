"""Active model loading, versioning, and management service."""

from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN


class ModelManager:
    """Service managing active motion encoder models and version checkpoints."""

    def __init__(self) -> None:
        self._models: dict[str, dict] = {}

        # Default model registration
        stgcn_default = STGCN(STGCNConfig())
        stgcn_default.eval()
        self._models["stgcn_default"] = {
            "name": "ST-GCN Default",
            "version": "v1.0.0",
            "topology": "mediapipe_33",
            "status": "active",
            "instance": stgcn_default,
        }

    def list_models(self) -> list[dict]:
        """List registered model information."""
        return [
            {
                "id": k,
                "name": v["name"],
                "version": v["version"],
                "topology": v["topology"],
                "status": v["status"],
            }
            for k, v in self._models.items()
        ]

    def get_model(self, model_id: str = "stgcn_default") -> STGCN | None:
        """Get active model instance by ID."""
        info = self._models.get(model_id)
        if info:
            return info["instance"]
        return None
