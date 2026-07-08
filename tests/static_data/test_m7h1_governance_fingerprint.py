from pathlib import Path

from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_M7H1_SEMANTIC_FINGERPRINT = (
    "acc50b83bd6b94835fe9544266ebf7863c67938957a4aa0408d4262765ee7c25"
)


def test_m7h1_foundation_semantic_fingerprint_is_pinned():
    static = build_static_game_data(ROOT)

    assert static.semantic_fingerprint == EXPECTED_M7H1_SEMANTIC_FINGERPRINT
