from pathlib import Path

from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_ACCEPTED_SEMANTIC_FINGERPRINT = (
    "251bf97728e97c1907f6d59229120544852053dd20eba728a98aabd9ac453158"
)


def test_m7h1_foundation_semantic_fingerprint_is_pinned():
    static = build_static_game_data(ROOT)

    assert static.semantic_fingerprint == EXPECTED_ACCEPTED_SEMANTIC_FINGERPRINT
