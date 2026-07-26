"""MotionEmbeddingExtractor extracting reusable 256-D motion embeddings from ST-GCN."""

import numpy as np
import torch
import torch.nn as nn


class MotionEmbeddingExtractor:
    """Extractor wrapper translating skeleton motion tensors into dense motion embedding vectors."""

    def __init__(self, model: nn.Module, device: str = "cpu") -> None:
        self.model = model.to(device)
        self.device = torch.device(device)
        self.model.eval()

    def extract(self, tensor: np.ndarray | torch.Tensor) -> np.ndarray:
        """Extract L2-normalized 256-D motion embedding vector from motion tensor.

        Args:
            tensor: Motion feature array or tensor of shape (C, T, V) or (N, C, T, V).

        Returns:
            Embedding vector NumPy array of shape (N, D) or (D,).
        """
        if isinstance(tensor, np.ndarray):
            tensor = torch.from_numpy(tensor).float()

        is_3d = tensor.dim() == 3
        if is_3d:
            tensor = tensor.unsqueeze(0)  # Add batch dim N=1

        tensor = tensor.to(self.device)

        with torch.no_grad():
            if hasattr(self.model, "extract_embedding"):
                embedding = self.model.extract_embedding(tensor)
            else:
                embedding = self.model(tensor)

        emb_np = embedding.cpu().numpy()
        if is_3d:
            return emb_np[0]
        return emb_np
