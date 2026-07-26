"""Unified Trainer executing PyTorch model training loops with callbacks and evaluation."""

import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.utils.data import DataLoader

from ai.evaluation.evaluator import ModelEvaluator
from ai.training.callbacks import EarlyStopping, ModelCheckpoint
from ai.training.experiment import ExperimentTracker
from ai.training.schedulers import CosineAnnealingWithWarmup


class Trainer:
    """Unified Config-Driven Trainer for HumanOS motion models."""

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader | None = None,
        max_epochs: int = 10,
        learning_rate: float = 1e-3,
        weight_decay: float = 1e-4,
        device: str = "cpu",
        checkpoint_dir: str = "checkpoints",
        experiment_name: str = "stgcn_run",
    ) -> None:
        self.device = torch.device(device)
        self.model = model.to(self.device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.max_epochs = max_epochs

        self.optimizer = AdamW(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)
        self.scheduler = CosineAnnealingWithWarmup(self.optimizer, warmup_epochs=2, max_epochs=max_epochs)
        self.criterion = nn.CrossEntropyLoss()

        self.evaluator = ModelEvaluator(self.model, device=device)
        self.checkpoint_cb = ModelCheckpoint(checkpoint_dir=checkpoint_dir, monitor="top1_acc", mode="max")
        self.early_stopping_cb = EarlyStopping(patience=5, mode="max")
        self.tracker = ExperimentTracker(experiment_name=experiment_name)

        self.tracker.log_params(
            {
                "max_epochs": max_epochs,
                "learning_rate": learning_rate,
                "weight_decay": weight_decay,
                "device": device,
            }
        )

    def train_epoch(self, epoch: int) -> float:
        """Run single training epoch."""
        self.model.train()
        running_loss = 0.0
        total_samples = 0

        for data, target in self.train_loader:
            data = data.to(self.device)
            target = target.to(self.device)

            self.optimizer.zero_grad()
            logits = self.model(data)
            loss = self.criterion(logits, target)
            loss.backward()
            self.optimizer.step()

            batch_size = data.size(0)
            running_loss += loss.item() * batch_size
            total_samples += batch_size

        self.scheduler.step()
        avg_loss = running_loss / max(1, total_samples)
        return avg_loss

    def fit(self) -> dict[str, float]:
        """Execute full training loop across max_epochs."""
        best_metrics: dict[str, float] = {}

        for epoch in range(1, self.max_epochs + 1):
            train_loss = self.train_epoch(epoch)
            self.tracker.log_metric("train_loss", train_loss, step=epoch)

            metrics = {"train_loss": train_loss, "epoch": float(epoch)}

            if self.val_loader is not None:
                val_results = self.evaluator.evaluate(self.val_loader)
                metrics.update({"val_loss": val_results["val_loss"], "top1_acc": val_results["top1_acc"]})
                self.tracker.log_metric("val_loss", val_results["val_loss"], step=epoch)
                self.tracker.log_metric("top1_acc", val_results["top1_acc"], step=epoch)

                self.checkpoint_cb(epoch, self.model, metrics)
                if self.early_stopping_cb(val_results["top1_acc"]):
                    break

            best_metrics = metrics

        self.tracker.save_run()
        return best_metrics
