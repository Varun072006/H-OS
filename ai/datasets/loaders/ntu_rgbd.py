"""NTU RGB+D 60/120 skeleton dataset loader implementation."""

from pathlib import Path
import numpy as np
import torch
from torch.utils.data import Dataset

from ai.datasets.registry import register_dataset


@register_dataset("ntu_rgbd")
class NTURGBDDataset(Dataset):
    """PyTorch Dataset loader for NTU RGB+D 60 / 120 skeleton action recognition benchmark dataset."""

    def __init__(
        self,
        data_path: str | Path,
        split: str = "train",
        benchmark: str = "xsub",
        target_frames: int = 30,
    ) -> None:
        self.data_path = Path(data_path)
        self.split = split
        self.benchmark = benchmark
        self.target_frames = target_frames

        self.samples: list[dict] = []
        self._load_metadata()

    def _load_metadata(self) -> None:
        """Load dataset split file lists."""
        if not self.data_path.exists():
            return
        # If npy file pre-extracted exist
        npy_files = list(self.data_path.glob("*.npy"))
        for f in npy_files:
            # NTU filename format: S001C001P001R001A001.skeleton.npy
            try:
                action_idx = int(f.name.split("A")[1].split(".")[0]) - 1
                self.samples.append({"path": f, "label": action_idx})
            except (IndexError, ValueError):
                continue

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, int]:
        sample_info = self.samples[idx]
        data = np.load(sample_info["path"]).astype(np.float32)  # Shape (C, T, V)
        tensor = torch.from_numpy(data).float()
        return tensor, sample_info["label"]
