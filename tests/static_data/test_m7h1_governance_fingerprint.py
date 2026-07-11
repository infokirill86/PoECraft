from pathlib import Path

from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]

EXPECTED_ACCEPTED_SEMANTIC_FINGERPRINT = (
    "fcc793113cb803c3cec71bd8582489edc0efe037fcbce169485427da0d7927b4"
)


def test_m7h1_foundation_semantic_fingerprint_is_pinned():
    static = build_static_game_data(ROOT)

    assert static.semantic_fingerprint == EXPECTED_ACCEPTED_SEMANTIC_FINGERPRINT
