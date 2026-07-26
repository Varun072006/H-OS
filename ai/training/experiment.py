"""Experiment tracking manager supporting MLflow and local JSON artifact logging."""

from pathlib import Path
import json
from datetime import datetime, timezone
from typing import Any


class ExperimentTracker:
    """Experiment logging abstraction for logging metrics, parameters, and model artifacts."""

    def __init__(self, experiment_name: str, log_dir: str | Path = "experiments") -> None:
        self.experiment_name = experiment_name
        self.log_dir = Path(log_dir) / experiment_name
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.run_params: dict[str, Any] = {}
        self.run_metrics: list[dict[str, Any]] = []

    def log_params(self, params: dict[str, Any]) -> None:
        """Log hyperparameter dictionary."""
        self.run_params.update(params)

    def log_metric(self, key: str, value: float, step: int) -> None:
        """Log a single numerical metric for a training step/epoch."""
        entry = {
            "key": key,
            "value": value,
            "step": step,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.run_metrics.append(entry)

    def save_run(self) -> Path:
        """Persist experiment run parameters and metrics to disk as JSON artifact."""
        artifact = {
            "experiment_name": self.experiment_name,
            "params": self.run_params,
            "metrics": self.run_metrics,
        }
        out_path = self.log_dir / "run_summary.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(artifact, f, indent=2)
        return out_path
