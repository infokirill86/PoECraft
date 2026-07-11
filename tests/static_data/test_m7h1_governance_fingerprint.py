from pathlib import Path

from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_ACCEPTED_SEMANTIC_FINGERPRINT = (
    "3b20a622bbd4406ce991a4b941390f19bd4ece50afe0aa2afd6b3cc3bac21d25"
)


def test_m7h1_foundation_semantic_fingerprint_is_pinned():
    static = build_static_game_data(ROOT)

    assert static.semantic_fingerprint == EXPECTED_ACCEPTED_SEMANTIC_FINGERPRINT
