from pathlib import Path

from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_ACCEPTED_SEMANTIC_FINGERPRINT = (
    "2e5e4454f941d01d1b31da143db5a34480a9865fa4e1dd9cd6302de16b0eccdf"
)


def test_m7h1_foundation_semantic_fingerprint_is_pinned():
    static = build_static_game_data(ROOT)

    assert static.semantic_fingerprint == EXPECTED_ACCEPTED_SEMANTIC_FINGERPRINT
