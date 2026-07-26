"""Model evaluation runner computing evaluation metrics over test datasets."""

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from ai.evaluation.metrics import compute_confusion_matrix, topk_accuracy


class ModelEvaluator:
    """Evaluator executing validation/test dataset runs over trained model checkpoints."""

    def __init__(self, model: nn.Module, device: str = "cpu") -> None:
        self.model = model.to(device)
        self.device = torch.device(device)

    def evaluate(self, data_loader: DataLoader, num_classes: int = 60) -> dict[str, float]:
        """Run model evaluation loop over DataLoader.

        Args:
            data_loader: PyTorch DataLoader for evaluation.
            num_classes: Total class count.

        Returns:
            Dictionary containing 'top1_acc', 'top5_acc', 'loss', and confusion matrix metrics.
        """
        self.model.eval()
        total_loss = 0.0
        top1_accs = []
        top5_accs = []

        all_preds: list[int] = []
        all_targets: list[int] = []

        criterion = nn.CrossEntropyLoss()

        with torch.no_grad():
            for data, target in data_loader:
                data = data.to(self.device)
                target = target.to(self.device)

                logits = self.model(data)
                loss = criterion(logits, target)
                total_loss += loss.item() * data.size(0)

                top1, top5 = topk_accuracy(logits, target, topk=(1, 5))
                top1_accs.append(top1)
                top5_accs.append(top5)

                preds = torch.argmax(logits, dim=1).cpu().numpy()
                all_preds.extend(preds)
                all_targets.extend(target.cpu().numpy())

        total_samples = max(1, len(data_loader.dataset))  # type: ignore
        avg_loss = total_loss / total_samples
        avg_top1 = float(np.mean(top1_accs)) if top1_accs else 0.0
        avg_top5 = float(np.mean(top5_accs)) if top5_accs else 0.0

        cm = compute_confusion_matrix(np.array(all_targets), np.array(all_preds), num_classes)

        return {
            "val_loss": avg_loss,
            "top1_acc": avg_top1,
            "top5_acc": avg_top5,
            "confusion_matrix": cm.tolist(),  # type: ignore
        }
