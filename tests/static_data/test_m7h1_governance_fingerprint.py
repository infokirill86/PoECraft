from pathlib import Path

from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_M7H1_SEMANTIC_FINGERPRINT = (
    "cc39128cef59e699a1c530c7a9aab7169b2a19f8c5d8656af072cfc32c2dea69"
)


def test_m7h1_foundation_semantic_fingerprint_is_pinned():
    static = build_static_game_data(ROOT)

    assert static.semantic_fingerprint == EXPECTED_M7H1_SEMANTIC_FINGERPRINT
