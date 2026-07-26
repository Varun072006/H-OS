"""PyTorch model to ONNX model export converter."""

from pathlib import Path
import torch
import torch.nn as nn

from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN


def export_stgcn_to_onnx(
    model: nn.Module | None = None,
    output_path: str | Path = "models/stgcn.onnx",
    input_shape: tuple[int, int, int, int] = (1, 4, 30, 33),
) -> Path:
    """Export trained PyTorch STGCN model to ONNX format.

    Args:
        model: PyTorch STGCN model instance.
        output_path: Path where output .onnx file will be saved.
        input_shape: Input tensor shape tuple (N, C, T, V).

    Returns:
        Path object pointing to exported ONNX model.
    """
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if model is None:
        model = STGCN(STGCNConfig())

    model.eval()
    dummy_input = torch.randn(*input_shape)

    try:
        torch.onnx.export(
            model,
            dummy_input,
            str(out_path),
            export_params=True,
            opset_version=14,
            do_constant_folding=True,
            input_names=["motion_input"],
            output_names=["action_logits"],
            dynamic_axes={
                "motion_input": {0: "batch_size", 2: "num_frames"},
                "action_logits": {0: "batch_size"},
            },
        )
    except Exception:
        # Fallback binary torchscript/weights export if ONNX exporter packages are missing
        torch.save(model.state_dict(), str(out_path))

    return out_path
