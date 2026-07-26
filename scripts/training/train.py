"""CLI entrypoint training launcher for HumanOS motion models."""

import argparse
from pathlib import Path
import yaml

import torch
from torch.utils.data import DataLoader

from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN
from ai.training.trainer import Trainer
from ai.datasets.loaders.skeleton_folder import SkeletonFolderDataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train HumanOS ST-GCN Motion Model")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/training/stgcn_ntu60_xsub.yaml",
        help="Path to YAML training configuration file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = Path(args.config)

    if not config_path.exists():
        raise FileNotFoundError(f"Training config not found at: {config_path}")

    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Initialize model
    model_cfg = cfg.get("model", {})
    stgcn_config = STGCNConfig(
        in_channels=model_cfg.get("in_channels", 4),
        num_classes=model_cfg.get("num_classes", 60),
        graph_layout=model_cfg.get("graph_layout", "mediapipe_33"),
        num_joints=model_cfg.get("num_joints", 33),
        embedding_dim=model_cfg.get("embedding_dim", 256),
    )
    model = STGCN(stgcn_config)

    # Initialize dataset & dataloader
    data_cfg = cfg.get("dataset", {})
    dataset = SkeletonFolderDataset(data_dir=data_cfg.get("data_dir", "data/ntu60"))

    train_cfg = cfg.get("training", {})
    batch_size = train_cfg.get("batch_size", 16)

    # If dataset is empty (e.g. initial run without data), generate dummy dataloader
    if len(dataset) == 0:
        print("[Notice] No data found in data_dir. Generating synthetic dataset for verification run.")
        dummy_x = torch.randn(32, stgcn_config.in_channels, 30, stgcn_config.num_joints)
        dummy_y = torch.randint(0, stgcn_config.num_classes, (32,))
        train_dataset = torch.utils.data.TensorDataset(dummy_x, dummy_y)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    else:
        train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        max_epochs=train_cfg.get("max_epochs", 2),
        learning_rate=train_cfg.get("learning_rate", 0.001),
        device=train_cfg.get("device", "cpu"),
        experiment_name=cfg.get("experiment_name", "stgcn_training"),
    )

    print("Starting HumanOS Model Training...")
    best_metrics = trainer.fit()
    print(f"Training Complete! Metrics: {best_metrics}")


if __name__ == "__main__":
    main()
