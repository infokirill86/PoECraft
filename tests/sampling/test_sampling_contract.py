from fractions import Fraction

import pytest

from p2c_engine.decisions.seeded import SeededDecisionSource
from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.sampling import branch_options, pool_digest
from p2c_engine.sampling.weighted import draw_uniform

POOL = (
    Candidate("alpha", 1),
    Candidate("beta", 3),
    Candidate("gamma", 6),
)


def test_seeded_choice_is_deterministic_and_order_independent():
    left = SeededDecisionSource(12345).choose_one("fixture.add", POOL)
    right = SeededDecisionSource(12345).choose_one("fixture.add", tuple(reversed(POOL)))
    assert left == right
    assert left.record.candidate_digest == pool_digest(POOL)


def test_known_vector_is_stable():
    decision = SeededDecisionSource(7).choose_one("fixture.add", POOL)
    assert (decision.selected.key, decision.record.raw_draw, decision.record.total_weight) == (
        "gamma",
        6,
        10,
    )


def test_pool_digest_changes_on_key_or_weight_and_not_order():
    assert pool_digest(POOL) == pool_digest(tuple(reversed(POOL)))
    assert pool_digest(POOL) != pool_digest((Candidate("alpha", 2), *POOL[1:]))
    assert pool_digest(POOL) != pool_digest((Candidate("delta", 1), *POOL[1:]))


@pytest.mark.parametrize(
    "candidates",
    [
        (),
        (Candidate("alpha", 0),),
        (Candidate("alpha", -1),),
        (Candidate("alpha", True),),
        (Candidate("alpha", 1), Candidate("alpha", 2)),
        (Candidate("Bad Key", 1),),
    ],
)
def test_bad_candidate_pools_raise_contract_defect(candidates):
    with pytest.raises(SamplingContractDefect):
        pool_digest(candidates)


@pytest.mark.parametrize("seed", [True, -1, 1.5])
def test_invalid_seed_is_rejected(seed):
    with pytest.raises(SamplingContractDefect):
        SeededDecisionSource(seed)


def test_draw_uniform_handles_total_larger_than_sha256_block():
    total = (1 << 300) + 123
    draw = draw_uniform(master_seed=9, decision_id="fixture.large", total=total)
    assert 0 <= draw < total


def test_exact_branch_options_sum_to_one_and_share_digest():
    options = branch_options("fixture.add", POOL)
    assert sum(
        (Fraction(option.probability_numerator, option.probability_denominator) for option in options),
        Fraction(0, 1),
    ) == Fraction(1, 1)
    assert {option.candidate_digest for option in options} == {pool_digest(POOL)}
    assert [option.selected_key for option in options] == ["alpha", "beta", "gamma"]
