"""HumanOS datasets module."""

from ai.datasets.registry import get_dataset_class, register_dataset
import ai.datasets.loaders.ntu_rgbd
import ai.datasets.loaders.skeleton_folder

__all__ = ["get_dataset_class", "register_dataset"]
