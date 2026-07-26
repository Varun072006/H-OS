"""Evaluation metrics calculation for model predictions."""

import numpy as np
import torch


def topk_accuracy(output: torch.Tensor, target: torch.Tensor, topk: tuple[int, ...] = (1, 5)) -> list[float]:
    """Calculate Top-k classification accuracy percentages.

    Args:
        output: Logits or probabilities tensor (N, num_classes).
        target: Target label indices (N).
        topk: Tuple of k values (e.g. (1, 5)).

    Returns:
        List of accuracy percentages corresponding to each k.
    """
    with torch.no_grad():
        num_classes = output.size(1)
        valid_topk = tuple(min(k, num_classes) for k in topk)
        maxk = min(max(topk), num_classes)
        batch_size = target.size(0)

        if batch_size == 0 or maxk == 0:
            return [0.0 for _ in topk]

        _, pred = output.topk(maxk, dim=1, largest=True, sorted=True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in valid_topk:
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(float(correct_k.mul_(100.0 / batch_size).item()))
        return res


def compute_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, num_classes: int) -> np.ndarray:
    """Compute NxN confusion matrix.

    Args:
        y_true: Ground truth target labels (N,).
        y_pred: Predicted target labels (N,).
        num_classes: Total class count C.

    Returns:
        (C, C) confusion matrix array.
    """
    cm = np.zeros((num_classes, num_classes), dtype=np.int64)
    for t, p in zip(y_true, y_pred):
        if 0 <= t < num_classes and 0 <= p < num_classes:
            cm[t, p] += 1
    return cm
