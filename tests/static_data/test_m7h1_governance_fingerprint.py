from pathlib import Path

from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_M7H1_SEMANTIC_FINGERPRINT = (
    "90e4b017325f6949490377358fff6538d36c1c845ad7c52fdb85a2d363b64678"
)


def test_m7h1_foundation_semantic_fingerprint_is_pinned():
    static = build_static_game_data(ROOT)

    assert static.semantic_fingerprint == EXPECTED_M7H1_SEMANTIC_FINGERPRINT
