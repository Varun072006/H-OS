"""Spatial Temporal Graph Convolutional Network (ST-GCN) main model architecture."""

import torch
import torch.nn as nn
import torch.nn.functional as F

from ai.graph.skeleton_config import get_topology
from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.layers import STGCNBlock


class STGCN(nn.Module):
    """Spatial Temporal Graph Convolutional Network (ST-GCN) for human motion encoding and action recognition.

    Paper: Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition (AAAI 2018).
    """

    def __init__(self, config: STGCNConfig | None = None) -> None:
        super().__init__()
        self.config = config or STGCNConfig()

        # Load graph adjacency matrix
        topology = get_topology(self.config.graph_layout)
        adj = torch.from_numpy(topology.get_adjacency_matrix()).float()
        # Shape (1, V, V) for single partition or (3, V, V) for spatial partitioning
        A = adj.unsqueeze(0)  # Shape (1, V, V)

        self.register_buffer("A", A)
        self.data_bn = nn.BatchNorm1d(self.config.in_channels * self.config.num_joints)

        # ST-GCN block cascade
        channels = [self.config.in_channels] + self.config.channel_list
        self.stgcn_blocks = nn.ModuleList()

        for idx in range(len(channels) - 1):
            in_c = channels[idx]
            out_c = channels[idx + 1]
            # Downsample stride = 2 at layer 3 and layer 6
            stride = 2 if idx in [3, 6] else 1

            block = STGCNBlock(
                in_channels=in_c,
                out_channels=out_c,
                A=A,
                stride=stride,
                dropout=self.config.dropout,
            )
            self.stgcn_blocks.append(block)

        # Global average pooling & dense heads
        last_channel = channels[-1]
        self.fc_embedding = nn.Linear(last_channel, self.config.embedding_dim)
        self.fc_classifier = nn.Linear(self.config.embedding_dim, self.config.num_classes)

    def extract_embedding(self, x: torch.Tensor) -> torch.Tensor:
        """Extract 256-dimensional motion embedding vector from skeleton sequence.

        Args:
            x: Input feature tensor of shape (N, C, T, V).

        Returns:
            Normalized motion embedding tensor of shape (N, embedding_dim).
        """
        N, C, T, V = x.size()

        # Batch normalization across joint features
        x_bn = x.permute(0, 1, 3, 2).contiguous().view(N, C * V, T)
        x_bn = self.data_bn(x_bn)
        x_bn = x_bn.view(N, C, V, T).permute(0, 1, 3, 2).contiguous()

        # Pass through ST-GCN blocks
        curr = x_bn
        for block in self.stgcn_blocks:
            curr = block(curr)

        # Global spatial & temporal average pooling: (N, C_out, T', V) -> (N, C_out)
        feat = F.avg_pool2d(curr, curr.size()[2:])
        feat = feat.view(N, -1)

        # Dense projection to motion embedding space
        embedding = self.fc_embedding(feat)
        embedding = F.normalize(embedding, p=2, dim=1)
        return embedding

    def forward(
        self, x: torch.Tensor, return_embedding: bool = False
    ) -> torch.Tensor | tuple[torch.Tensor, torch.Tensor]:
        """Forward pass.

        Args:
            x: Input tensor of shape (N, C, T, V).
            return_embedding: If True, returns tuple (logits, embedding).

        Returns:
            logits (N, num_classes) or tuple (logits, embedding).
        """
        embedding = self.extract_embedding(x)
        logits = self.fc_classifier(embedding)

        if return_embedding:
            return logits, embedding
        return logits
