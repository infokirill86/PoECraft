from dataclasses import replace

import pytest

from p2c_engine.decisions import (
    ExactBranchingDecisionSource,
    RecordingDecisionSource,
    ReplayDecisionSource,
    SeededDecisionSource,
)
from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.defects import (
    DuplicateDecisionIdDefect,
    ReplayDigestMismatch,
    SamplingContractDefect,
    SelectedKeyMismatch,
)

POOL = (Candidate("alpha", 1), Candidate("beta", 2), Candidate("gamma", 3))


def test_duplicate_decision_id_fails_loudly():
    source = SeededDecisionSource(1)
    source.choose_one("fixture.add", POOL)
    with pytest.raises(DuplicateDecisionIdDefect):
        source.choose_one("fixture.add", POOL)


def test_choose_sequence_is_ppswor_and_uses_semantic_sub_ids():
    decisions = SeededDecisionSource(11).choose_sequence("fixture.offer", POOL, 3)
    assert len({decision.selected.key for decision in decisions}) == 3
    assert [decision.record.decision_id for decision in decisions] == [
        "fixture.offer.0",
        "fixture.offer.1",
        "fixture.offer.2",
    ]


def test_sequence_sub_id_collision_fails():
    source = SeededDecisionSource(11)
    source.choose_sequence("fixture.offer", POOL, 1)
    with pytest.raises(DuplicateDecisionIdDefect):
        source.choose_one("fixture.offer.0", POOL)


@pytest.mark.parametrize("k", [True, -1, 4])
def test_invalid_sequence_k_fails(k):
    with pytest.raises(SamplingContractDefect):
        SeededDecisionSource(1).choose_sequence("fixture.offer", POOL, k)


def test_recording_is_transparent_and_replay_preserves_record():
    recording = RecordingDecisionSource(SeededDecisionSource(77))
    sampled = recording.choose_one("fixture.add", POOL)
    replayed = ReplayDecisionSource(recording.records).choose_one("fixture.add", tuple(reversed(POOL)))
    assert replayed == sampled
    assert replayed.record.raw_draw == sampled.record.raw_draw


def test_replay_pool_mismatch_is_loud():
    sampled = SeededDecisionSource(77).choose_one("fixture.add", POOL)
    with pytest.raises(ReplayDigestMismatch):
        ReplayDecisionSource((sampled.record,)).choose_one(
            "fixture.add", (Candidate("alpha", 9), Candidate("beta", 2), Candidate("gamma", 3))
        )


def test_replay_selected_key_mismatch_is_loud():
    sampled = SeededDecisionSource(77).choose_one("fixture.add", POOL)
    damaged = replace(sampled.record, selected_key="not_the_selected_key")
    with pytest.raises(SelectedKeyMismatch):
        ReplayDecisionSource((damaged,)).choose_one("fixture.add", POOL)



@pytest.mark.parametrize("raw_draw", [True, -1, 999])
def test_replay_rejects_invalid_raw_draw(raw_draw):
    sampled = SeededDecisionSource(77).choose_one("fixture.add", POOL)
    damaged = replace(sampled.record, raw_draw=raw_draw)
    with pytest.raises(ReplayDigestMismatch):
        ReplayDecisionSource((damaged,)).choose_one("fixture.add", POOL)


def test_replay_rejects_raw_draw_for_different_candidate_interval():
    sampled = SeededDecisionSource(77).choose_one("fixture.add", POOL)
    wrong_interval_draw = 0 if sampled.record.selected_rank != 0 else POOL[0].weight
    damaged = replace(sampled.record, raw_draw=wrong_interval_draw)
    with pytest.raises(ReplayDigestMismatch):
        ReplayDecisionSource((damaged,)).choose_one("fixture.add", POOL)

def test_exact_source_uses_pin_and_has_no_raw_draw():
    decision = ExactBranchingDecisionSource({"fixture.add": 1}).choose_one("fixture.add", POOL)
    assert decision.selected.key == "beta"
    assert decision.record.raw_draw is None


def test_exact_source_rejects_bool_and_out_of_range_pins():
    with pytest.raises(SamplingContractDefect):
        ExactBranchingDecisionSource({"fixture.add": True}).choose_one("fixture.add", POOL)
    with pytest.raises(SamplingContractDefect):
        ExactBranchingDecisionSource({"fixture.add": 99}).choose_one("fixture.add", POOL)
