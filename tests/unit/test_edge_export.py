"""Unit tests for ONNX model export and edge validation."""

from pathlib import Path
from ai.models.export.onnx_export import export_stgcn_to_onnx
from ai.models.export.validate_export import validate_onnx_export


def test_onnx_model_export(tmp_path: Path) -> None:
    """Test exporting STGCN PyTorch model to ONNX format."""
    out_file = tmp_path / "stgcn_test.onnx"
    exported_path = export_stgcn_to_onnx(output_path=out_file)

    assert exported_path.exists()
    assert validate_onnx_export(exported_path)
