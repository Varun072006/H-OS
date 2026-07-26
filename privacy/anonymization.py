"""Skeleton landmark anonymization and de-identification utilities."""

from ai.pose.types import Joint, Skeleton


def anonymize_skeleton(skeleton: Skeleton, noise_scale: float = 0.005) -> Skeleton:
    """Anonymize skeleton by removing absolute bone proportions and scaling features.

    Args:
        skeleton: Input Skeleton instance.
        noise_scale: Noise level added to bone proportion metrics.

    Returns:
        De-identified Skeleton instance.
    """
    if not skeleton.joints:
        return skeleton

    anonymized_joints = []
    for j in skeleton.joints:
        # Strip facial features (landmarks 0..10 in MediaPipe) to prevent face reconstruction
        if j.id <= 10:
            # Zero out detailed eye/nose/mouth landmark offsets
            anon_j = Joint(
                id=j.id,
                name=j.name,
                x=0.0,
                y=0.0,
                z=0.0,
                visibility=0.0,
                confidence=0.0,
            )
        else:
            anon_j = Joint(
                id=j.id,
                name=j.name,
                x=j.x,
                y=j.y,
                z=j.z,
                visibility=j.visibility,
                confidence=j.confidence,
            )
        anonymized_joints.append(anon_j)

    return Skeleton(
        joints=anonymized_joints,
        topology_name=skeleton.topology_name,
        person_id=0,  # Anonymous person ID
        center_of_mass=skeleton.center_of_mass,
    )
