"""Unit tests for training infrastructure: dataset loaders, losses, schedulers, callbacks, metrics, and trainer."""

import pytest
import torch
from torch.utils.data import DataLoader, TensorDataset

from ai.datasets.registry import get_dataset_class
from ai.datasets.preprocessing.interpolation import interpolate_missing_joints
from ai.datasets.preprocessing.filtering import moving_average_smooth
from ai.training.losses import MotionContrastiveLoss, TrajectoryForecastingLoss
from ai.training.callbacks import EarlyStopping, ModelCheckpoint
from ai.training.experiment import ExperimentTracker
from ai.evaluation.metrics import topk_accuracy, compute_confusion_matrix
from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN
from ai.training.trainer import Trainer


def test_dataset_registry() -> None:
    """Test retrieving dataset classes from registry."""
    cls = get_dataset_class("skeleton_folder")
    assert cls is not None

    with pytest.raises(ValueError):
        get_dataset_class("nonexistent_dataset")


def test_missing_joint_interpolation() -> None:
    """Test interpolating zero joint coordinates."""
    x = torch.zeros(4, 10, 33).numpy()
    x[:3, 0, 0] = 1.0
    x[:3, 9, 0] = 10.0

    interp_x = interpolate_missing_joints(x)
    assert interp_x.shape == (4, 10, 33)
    # Midpoint t=4 joint 0 should be non-zero interpolated value
    assert interp_x[0, 4, 0] > 0.0


def test_moving_average_smooth() -> None:
    """Test smoothing noisy joint trajectories."""
    x = torch.randn(4, 10, 33).numpy()
    smoothed = moving_average_smooth(x, window_size=3)
    assert smoothed.shape == x.shape


def test_motion_contrastive_loss() -> None:
    """Test InfoNCE contrastive loss forward pass."""
    loss_fn = MotionContrastiveLoss(temperature=0.1)
    emb_a = torch.randn(4, 128)
    emb_b = torch.randn(4, 128)

    loss = loss_fn(emb_a, emb_b)
    assert loss.dim() == 0
    assert loss.item() > 0.0


def test_trajectory_forecasting_loss() -> None:
    """Test trajectory forecasting MPJPE loss."""
    loss_fn = TrajectoryForecastingLoss()
    pred = torch.randn(2, 3, 10, 33)
    target = torch.randn(2, 3, 10, 33)

    loss = loss_fn(pred, target)
    assert loss.dim() == 0
    assert loss.item() >= 0.0


def test_callbacks_early_stopping_and_checkpoint(tmp_path) -> None:
    """Test ModelCheckpoint and EarlyStopping callbacks."""
    checkpoint_cb = ModelCheckpoint(checkpoint_dir=tmp_path, monitor="top1_acc", mode="max")
    model = torch.nn.Linear(10, 2)

    improved = checkpoint_cb(epoch=1, model=model, metrics={"top1_acc": 85.0})
    assert improved

    early_stop = EarlyStopping(patience=2, mode="max")
    assert not early_stop(80.0)
    assert not early_stop(80.0)
    assert early_stop(80.0)  # Patience exhausted


def test_metrics_topk_and_confusion_matrix() -> None:
    """Test accuracy and confusion matrix computation."""
    logits = torch.tensor([[10.0, 0.0], [0.0, 10.0]])
    targets = torch.tensor([0, 1])

    top1, top5 = topk_accuracy(logits, targets, topk=(1, 2))
    assert top1 == 100.0

    cm = compute_confusion_matrix(targets.numpy(), targets.numpy(), num_classes=2)
    assert cm[0, 0] == 1
    assert cm[1, 1] == 1


def test_trainer_synthetic_fit(tmp_path) -> None:
    """Test full Trainer synthetic dataset fit loop."""
    config = STGCNConfig(in_channels=4, num_classes=3, graph_layout="mediapipe_33", num_joints=33)
    model = STGCN(config)

    x = torch.randn(8, 4, 10, 33)
    y = torch.tensor([0, 1, 2, 0, 1, 2, 0, 1])
    dataset = TensorDataset(x, y)
    loader = DataLoader(dataset, batch_size=4)

    trainer = Trainer(
        model=model,
        train_loader=loader,
        val_loader=loader,
        max_epochs=2,
        checkpoint_dir=str(tmp_path),
        experiment_name="test_exp",
    )

    metrics = trainer.fit()
    assert "train_loss" in metrics
    assert "top1_acc" in metrics
