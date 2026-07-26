"""Learning rate schedulers with linear warmup and cosine annealing."""

import math
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler


class CosineAnnealingWithWarmup(_LRScheduler):
    """Cosine Annealing learning rate scheduler with linear warmup steps."""

    def __init__(
        self,
        optimizer: Optimizer,
        warmup_epochs: int,
        max_epochs: int,
        min_lr: float = 1e-6,
        last_epoch: int = -1,
    ) -> None:
        self.warmup_epochs = warmup_epochs
        self.max_epochs = max_epochs
        self.min_lr = min_lr
        super().__init__(optimizer, last_epoch)

    def get_lr(self) -> list[float]:
        if self.last_epoch < self.warmup_epochs:
            # Linear warmup
            alpha = float(self.last_epoch) / float(max(1, self.warmup_epochs))
            return [base_lr * alpha for base_lr in self.base_lrs]
        else:
            # Cosine decay
            progress = float(self.last_epoch - self.warmup_epochs) / float(
                max(1, self.max_epochs - self.warmup_epochs)
            )
            return [
                self.min_lr + (base_lr - self.min_lr) * 0.5 * (1.0 + math.cos(math.pi * progress))
                for base_lr in self.base_lrs
            ]
