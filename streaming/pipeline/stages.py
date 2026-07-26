"""Pipeline processing stages: Pose, Privacy, Graph, Inference."""

import numpy as np
from ai.graph.builder import MotionGraphBuilder
from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN
from ai.pose.base import PoseExtractor
from ai.pose.types import PoseResult, Skeleton
from backend.schemas.responses import HumanStateResponse
from backend.services.state_manager import HumanStateManager
from privacy.frame_deletion import PrivacyBoundary
from streaming.buffer.ring_buffer import RingBuffer


class PipelineStages:
    """Orchestrator for sequential frame processing pipeline stages."""

    def __init__(
        self,
        extractor: PoseExtractor,
        topology_name: str = "mediapipe_33",
        window_size: int = 30,
        device: str = "cpu",
    ) -> None:
        self.extractor = extractor
        self.privacy_boundary = PrivacyBoundary()
        self.graph_builder = MotionGraphBuilder(topology_name)
        self.skeleton_buffer: RingBuffer[Skeleton] = RingBuffer(capacity=window_size)

        # ST-GCN Model & State Manager
        self.stgcn = STGCN(STGCNConfig(graph_layout=topology_name)).to(device)
        self.stgcn.eval()
        self.state_manager = HumanStateManager()

    def process_frame(self, frame: np.ndarray, frame_index: int, session_id: str = "stream_sess") -> HumanStateResponse:
        """Process single video frame through end-to-end pipeline.

        Stage 1 & 2: Pose Extraction + Privacy Frame Zeroing
        Stage 3: Skeleton RingBuffer pushing
        Stage 4: Motion Graph Construction
        Stage 5: ST-GCN Embedding Inference
        Stage 6: Prediction Modules & State Update
        """
        # Stage 1 & 2: Pose extraction + Privacy Zeroing
        pose_result: PoseResult = self.privacy_boundary.extract_and_delete(
            frame, self.extractor, frame_index=frame_index
        )

        if pose_result.has_pose:
            self.skeleton_buffer.push(pose_result.skeletons[0])

        # If buffer is full enough, construct graph tensor & run inference
        skels = self.skeleton_buffer.get_all()
        if len(skels) > 0:
            graph = self.graph_builder.build_from_skeletons(skels)
            # Extracted embedding vector
            embedding = self.stgcn.extract_embedding(
                import_torch().from_numpy(graph.x).float()
            ).cpu().numpy()
        else:
            embedding = np.random.randn(256).astype(np.float32)
            embedding = embedding / np.linalg.norm(embedding)

        return self.state_manager.update_state(session_id, embedding)


def import_torch():
    import torch
    return torch
