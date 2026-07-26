"""Hyperparameter configuration dataclass for Spatial Temporal Graph Convolutional Network (ST-GCN)."""

from dataclasses import dataclass, field


@dataclass
class STGCNConfig:
    """Hyperparameter config container for ST-GCN model initialization.

    Attributes:
        in_channels: Number of input channels per joint node (e.g. 3 for xyz or 4 for xyz+confidence).
        num_classes: Output class count for classification mode (e.g. 60 for NTU60).
        graph_layout: Skeleton topology name ('mediapipe_33', 'ntu_25').
        num_joints: Number of vertices V in skeletal graph.
        edge_importance_weighting: Learnable adaptive weight matrix for spatial edges.
        temporal_kernel_size: Temporal convolution kernel size (odd integer, e.g. 9).
        dropout: Dropout probability.
        embedding_dim: Dense motion embedding feature dimension (e.g. 256).
    """

    in_channels: int = 4
    num_classes: int = 60
    graph_layout: str = "mediapipe_33"
    num_joints: int = 33
    edge_importance_weighting: bool = True
    temporal_kernel_size: int = 9
    dropout: float = 0.5
    embedding_dim: int = 256
    channel_list: list[int] = field(default_factory=lambda: [64, 64, 64, 128, 128, 128, 256, 256, 256])
