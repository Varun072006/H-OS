"""Custom loss functions for classification, motion embedding contrastive learning, and forecasting."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class MotionContrastiveLoss(nn.Module):
    """InfoNCE Contrastive Loss for self-supervised motion embedding learning."""

    def __init__(self, temperature: float = 0.07) -> None:
        super().__init__()
        self.temperature = temperature

    def forward(self, emb_a: torch.Tensor, emb_b: torch.Tensor) -> torch.Tensor:
        """Compute contrastive loss between augmented motion embeddings emb_a and emb_b.

        Args:
            emb_a: L2-normalized embeddings of shape (N, D).
            emb_b: L2-normalized embeddings of shape (N, D).

        Returns:
            Scalar contrastive loss tensor.
        """
        N = emb_a.size(0)
        # Normalize
        emb_a = F.normalize(emb_a, dim=1)
        emb_b = F.normalize(emb_b, dim=1)

        # Cosine similarity matrix: (N, N)
        sim_matrix = torch.matmul(emb_a, emb_b.T) / self.temperature

        # Positive pair targets along diagonal
        labels = torch.arange(N, device=emb_a.device)
        loss = F.cross_entropy(sim_matrix, labels)
        return loss


class TrajectoryForecastingLoss(nn.Module):
    """Mean Per-Joint Position Error (MPJPE) loss for joint trajectory forecasting."""

    def __init__(self) -> None:
        super().__init__()

    def forward(self, pred_traj: torch.Tensor, target_traj: torch.Tensor) -> torch.Tensor:
        """Compute MPJPE loss between predicted and ground-truth joint trajectories.

        Args:
            pred_traj: Predicted joint coordinates (N, C, T, V).
            target_traj: Ground truth joint coordinates (N, C, T, V).

        Returns:
            Mean squared error loss across joints.
        """
        diff = pred_traj - target_traj
        return torch.mean(torch.sum(diff**2, dim=1))
