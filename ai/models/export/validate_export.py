"""Validation helper checking exported ONNX model integrity."""

from pathlib import Path
import numpy as np


def validate_onnx_export(onnx_file_path: str | Path) -> bool:
    """Validate that exported ONNX file exists and has non-zero size."""
    file_path = Path(onnx_file_path)
    if not file_path.exists():
        return False
    return file_path.stat().st_size > 0
