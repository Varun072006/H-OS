"""Spatial-Temporal Graph Convolutional layers implementation in PyTorch."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvSpatial(nn.Module):
    """Spatial Graph Convolution Layer for skeletal graphs.

    Computes X' = sum_k (A_k * X * W_k) where A_k is partition matrix of graph.
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int = 1,
        stride: int = 1,
        residual: bool = True,
    ) -> None:
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size

        self.conv = nn.Conv2d(
            in_channels,
            out_channels * kernel_size,
            kernel_size=(1, 1),
            stride=(stride, 1),
            padding=(0, 0),
        )

    def forward(self, x: torch.Tensor, A: torch.Tensor) -> torch.Tensor:
        """Forward pass.

        Args:
            x: Input tensor of shape (N, C, T, V).
            A: Adjacency matrix of shape (K, V, V) or (V, V).

        Returns:
            Spatial graph convolution output tensor (N, C_out, T, V).
        """
        N, C, T, V = x.size()

        # Ensure A is 3D (K, V, V)
        if A.dim() == 2:
            A = A.unsqueeze(0)

        K = A.size(0)

        # 1. Linear transformation: (N, K*C_out, T, V)
        x_conv = self.conv(x)
        x_conv = x_conv.view(N, K, self.out_channels, T, V)

        # 2. Spatial Graph Aggregation via Einstein summation: N, K, C_out, T, V and K, V, W -> N, C_out, T, W
        out = torch.einsum("nkctv,kvw->nctw", x_conv, A)
        return out


class ConvTemporal(nn.Module):
    """Temporal Convolution Layer over sequence frames T."""

    def __init__(
        self,
        channels: int,
        kernel_size: int = 9,
        stride: int = 1,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        padding = (kernel_size - 1) // 2
        self.conv = nn.Sequential(
            nn.BatchNorm2d(channels),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Conv2d(
                channels,
                channels,
                kernel_size=(kernel_size, 1),
                stride=(stride, 1),
                padding=(padding, 0),
            ),
            nn.BatchNorm2d(channels),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(x)


class STGCNBlock(nn.Module):
    """Spatial Temporal Graph Convolutional Block (ST-GCN Block).

    Combines Spatial Graph Convolution with Temporal Convolution and Residual connections.
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        A: torch.Tensor,
        stride: int = 1,
        dropout: float = 0.0,
        residual: bool = True,
    ) -> None:
        super().__init__()
        self.register_buffer("A", A)

        # Spatial Graph Conv
        self.gcn = ConvSpatial(in_channels, out_channels, kernel_size=A.size(0) if A.dim() == 3 else 1)

        # Temporal Conv
        self.tcn = ConvTemporal(out_channels, kernel_size=9, stride=stride, dropout=dropout)

        # Residual projection
        if not residual:
            self.residual = lambda x: 0
        elif (in_channels == out_channels) and (stride == 1):
            self.residual = lambda x: x
        else:
            self.residual = nn.Sequential(
                nn.Conv2d(
                    in_channels,
                    out_channels,
                    kernel_size=1,
                    stride=(stride, 1),
                ),
                nn.BatchNorm2d(out_channels),
            )

        self.relu = nn.ReLU(inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass for ST-GCN block.

        Args:
            x: Input tensor of shape (N, C_in, T, V).

        Returns:
            Output tensor of shape (N, C_out, T', V).
        """
        res = self.residual(x)
        x_gcn = self.gcn(x, self.A)
        x_out = self.tcn(x_gcn) + res
        return self.relu(x_out)
