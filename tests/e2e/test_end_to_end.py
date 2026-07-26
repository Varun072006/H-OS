"""Full end-to-end regression test verifying full pipeline execution."""

import numpy as np
from ai.pose.mediapipe_extractor import MediaPipePoseExtractor
from ai.graph.builder import MotionGraphBuilder
from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN
from privacy.frame_deletion import PrivacyBoundary
from backend.services.state_manager import HumanStateManager


def test_full_pipeline_e2e_flow() -> None:
    """Full End-to-End Test Flow:

    1. Ingest raw frame (H, W, C).
    2. Run MediaPipe Pose Extraction through Privacy Boundary.
    3. Verify raw frame zero-filling.
    4. Build spatiotemporal motion graph from skeleton joints.
    5. Pass graph through ST-GCN model -> extract motion embedding.
    6. Update continuous human state manager -> generate predictions & confidence scores.
    """
    # 1. Raw frame
    raw_frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
    extractor = MediaPipePoseExtractor()

    # 2 & 3. Privacy boundary extraction & zero-fill
    boundary = PrivacyBoundary()
    pose_result = boundary.extract_and_delete(raw_frame, extractor=extractor, frame_index=1)
    assert np.max(raw_frame) == 0  # Zero fill verified

    # 4. Motion graph
    builder = MotionGraphBuilder("mediapipe_33")
    if pose_result.has_pose:
        skels = [pose_result.skeletons[0]]
    else:
        # Create fallback skeleton for testing complete tensor pipeline
        from ai.pose.types import Joint, Skeleton
        skels = [Skeleton(joints=[Joint(id=i, name=f"j_{i}", x=0.5, y=0.5, z=0.0) for i in range(33)])]

    graph = builder.build_from_skeletons(skels)
    assert graph.x.shape == (4, 1, 33)

    # 5. ST-GCN inference
    import torch
    model = STGCN(STGCNConfig())
    model.eval()
    with torch.no_grad():
        emb = model.extract_embedding(torch.from_numpy(graph.x).float()).numpy()

    # 6. State & prediction engine
    state_mgr = HumanStateManager()
    state = state_mgr.update_state("e2e_sess", emb[0])

    assert state.session_id == "e2e_sess"
    assert len(state.predictions) >= 5
    assert state.predictions[0].confidence > 0.0
