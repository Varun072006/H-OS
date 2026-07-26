"""Training callbacks for checkpointing, early stopping, and metric logging."""

from pathlib import Path
import torch
import torch.nn as nn


class ModelCheckpoint:
    """Callback saving model weights based on validation metric improvement."""

    def __init__(
        self,
        checkpoint_dir: str | Path,
        monitor: str = "val_acc",
        mode: str = "max",
        save_best_only: bool = True,
    ) -> None:
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.monitor = monitor
        self.mode = mode
        self.save_best_only = save_best_only

        self.best_score = float("-inf") if mode == "max" else float("inf")

    def __call__(self, epoch: int, model: nn.Module, metrics: dict[str, float]) -> bool:
        score = metrics.get(self.monitor, 0.0)
        improved = (score > self.best_score) if self.mode == "max" else (score < self.best_score)

        if improved or not self.save_best_only:
            self.best_score = score
            save_path = self.checkpoint_dir / f"checkpoint_epoch_{epoch:03d}_{self.monitor}_{score:.4f}.pt"
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "metrics": metrics,
                },
                save_path,
            )
            return True
        return False


class EarlyStopping:
    """Callback stopping training if monitored validation metric fails to improve."""

    def __init__(self, patience: int = 10, mode: str = "max", min_delta: float = 1e-4) -> None:
        self.patience = patience
        self.mode = mode
        self.min_delta = min_delta
        self.best_score = float("-inf") if mode == "max" else float("inf")
        self.counter = 0
        self.should_stop = False

    def __call__(self, score: float) -> bool:
        improved = (
            (score - self.best_score > self.min_delta)
            if self.mode == "max"
            else (self.best_score - score > self.min_delta)
        )
        if improved:
            self.best_score = score
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True

        return self.should_stop
