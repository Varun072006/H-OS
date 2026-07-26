"""Multi-camera temporal frame synchronizer."""

import numpy as np


def synchronize_multi_stream(packets_by_source: dict[str, list[dict]], time_tolerance_sec: float = 0.05) -> list[dict[str, dict]]:
    """Synchronize frame packets across multiple sensor sources based on closest timestamps.

    Args:
        packets_by_source: Dict mapping source_id -> list of packet dicts with 'timestamp'.
        time_tolerance_sec: Maximum allowable timestamp difference in seconds.

    Returns:
        List of synchronized frame packet dicts keyed by source_id.
    """
    if not packets_by_source:
        return []

    sources = list(packets_by_source.keys())
    primary_source = sources[0]
    primary_packets = packets_by_source[primary_source]

    synced_frames: list[dict[str, dict]] = []

    for p in primary_packets:
        t_ref = p["timestamp"]
        frame_set = {primary_source: p}
        valid_match = True

        for other_src in sources[1:]:
            other_packets = packets_by_source[other_src]
            # Find closest packet in timestamp
            best_pkt = min(other_packets, key=lambda x: abs(x["timestamp"] - t_ref))
            if abs(best_pkt["timestamp"] - t_ref) <= time_tolerance_sec:
                frame_set[other_src] = best_pkt
            else:
                valid_match = False
                break

        if valid_match:
            synced_frames.append(frame_set)

    return synced_frames
