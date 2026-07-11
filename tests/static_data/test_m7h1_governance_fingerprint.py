from pathlib import Path

from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_ACCEPTED_SEMANTIC_FINGERPRINT = (
    "230dc88b9e8c5cd90857fc06cb2ccec66ca58498878579cd47258766948c8979"
)


def test_m7h1_foundation_semantic_fingerprint_is_pinned():
    static = build_static_game_data(ROOT)

    assert static.semantic_fingerprint == EXPECTED_ACCEPTED_SEMANTIC_FINGERPRINT
