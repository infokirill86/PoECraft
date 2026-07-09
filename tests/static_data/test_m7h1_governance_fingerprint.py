from pathlib import Path

from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_M7H1_SEMANTIC_FINGERPRINT = (
    "18339351096e3e925907f2901763f36d69325e4e76bc47ab5db8fbe75c719203"
)


def test_m7h1_foundation_semantic_fingerprint_is_pinned():
    static = build_static_game_data(ROOT)

    assert static.semantic_fingerprint == EXPECTED_M7H1_SEMANTIC_FINGERPRINT
