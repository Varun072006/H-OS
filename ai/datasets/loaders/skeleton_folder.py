"""Generic folder dataset loader reading skeleton sequence arrays from disk."""

from pathlib import Path
from typing import Any
import numpy as np
import torch
from torch.utils.data import Dataset

from ai.datasets.registry import register_dataset


@register_dataset("skeleton_folder")
class SkeletonFolderDataset(Dataset):
    """PyTorch Dataset reading skeleton array files (.npy/.npz) from structured directory folders.

    Directory structure:
        root_dir/
            action_001/
                sample_001.npy   # Array of shape (C, T, V)
                sample_002.npy
            action_002/
                sample_003.npy
    """

    def __init__(
        self,
        data_dir: str | Path,
        transform: Any | None = None,
        target_frames: int = 30,
    ) -> None:
        self.data_dir = Path(data_dir)
        self.transform = transform
        self.target_frames = target_frames

        self.samples: list[tuple[Path, int]] = []
        self.classes: list[str] = []

        self._scan_directory()

    def _scan_directory(self) -> None:
        """Scan directory and index sample files and label indices."""
        if not self.data_dir.exists():
            return

        class_dirs = sorted([d for d in self.data_dir.iterdir() if d.is_dir()])
        self.classes = [d.name for d in class_dirs]
        class_to_idx = {name: i for i, name in enumerate(self.classes)}

        for class_dir in class_dirs:
            label = class_to_idx[class_dir.name]
            for file_path in sorted(class_dir.glob("*.npy")):
                self.samples.append((file_path, label))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:
        file_path, label = self.samples[idx]
        data = np.load(file_path).astype(np.float32)  # Shape (C, T, V)

        if self.transform is not None:
            data = self.transform(data)

        tensor = torch.from_numpy(data).float()
        return tensor, label
