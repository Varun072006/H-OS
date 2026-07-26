"""Example demonstrating Python SDK usage for monitoring human state."""

import time
from sdk.python.humanos.client import HumanOSClient


def main() -> None:
    # Initialize client connecting to backend server
    client = HumanOSClient(endpoint="http://localhost:8000")

    # Check system health
    health = client.health()
    print(f"HumanOS API Health: {health}")

    # Create session
    session = client.create_session(camera_id="webcam:0")
    print(f"Created Session: {session.session_id}")

    # Fetch continuous human state
    state = session.get_state()
    print(f"\n--- Human Physical State [{state.timestamp}] ---")
    print(f"Posture Quality: {state.posture_quality * 100:.1f}%")
    print(f"Gait Stability: {state.gait_stability * 100:.1f}%")
    print(f"Active Predictions:")

    for pred in state.predictions:
        print(f" - [{pred.module_name.upper()}] {pred.label} (Conf: {pred.confidence*100:.1f}%, Risk: {pred.risk_level})")

    # Close session
    session.close()
    print(f"\nClosed Session {session.session_id}")


if __name__ == "__main__":
    main()
