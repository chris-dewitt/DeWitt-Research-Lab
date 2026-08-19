"""Frame pairs, and the structural guarantee that wording cannot move the payoff."""

from __future__ import annotations

import pytest
from drl_cfi.frames import (
    Frame,
    FrameEquivalenceError,
    FrameFamily,
    FramePair,
    PairedValuation,
    vanilla_option,
)
from drl_cfi.payoffs import Claim, Leg, LegKind

STRIKE = 100.0

PROTECTIVE_PUT = Claim(
    "protective-put",
    (Leg(kind=LegKind.UNDERLYING), Leg(kind=LegKind.PUT, strike=STRIKE)),
)
CALL_PLUS_CASH = Claim(
    "call-plus-cash",
    (Leg(kind=LegKind.CALL, strike=STRIKE), Leg(kind=LegKind.CASH, quantity=STRIKE)),
)
BARE_CALL = Claim("bare-call", (Leg(kind=LegKind.CALL, strike=STRIKE),))


def insurance_frame() -> Frame:
    return Frame(
        frame_id="insurance",
        family=FrameFamily.INSURANCE_GAMBLE,
        text="You hold the asset and buy protection against it falling below 100.",
        claim=PROTECTIVE_PUT,
    )


def upside_frame() -> Frame:
    return Frame(
        frame_id="upside",
        family=FrameFamily.NARRATIVE_TECHNICAL,
        text="You hold 100 in cash plus the right to buy the asset at 100.",
        claim=CALL_PLUS_CASH,
    )


def test_equivalent_claims_make_a_valid_pair() -> None:
    pair = FramePair("insurance-vs-upside", insurance_frame(), upside_frame())
    assert pair.families() == (FrameFamily.INSURANCE_GAMBLE, FrameFamily.NARRATIVE_TECHNICAL)


def test_pair_construction_refuses_a_payoff_difference() -> None:
    """The failure mode this class exists to prevent: two claims that are not the same bet."""
    mismatched = Frame(
        frame_id="bare-call",
        family=FrameFamily.GAIN_LOSS,
        text="You hold the right to buy the asset at 100.",
        claim=BARE_CALL,
    )
    with pytest.raises(FrameEquivalenceError, match="does not hold payoff fixed"):
        FramePair("invalid", insurance_frame(), mismatched)


def test_pair_construction_reports_why_the_payoffs_differ() -> None:
    mismatched = Frame(
        frame_id="bare-call",
        family=FrameFamily.GAIN_LOSS,
        text="You hold the right to buy the asset at 100.",
        claim=BARE_CALL,
    )
    with pytest.raises(FrameEquivalenceError) as caught:
        FramePair("invalid", insurance_frame(), mismatched)
    assert "payoffs differ" in str(caught.value) or "terminal slopes differ" in str(caught.value)


def test_pair_rejects_identical_wording() -> None:
    left = insurance_frame()
    right = Frame(
        frame_id="insurance-copy",
        family=FrameFamily.GAIN_LOSS,
        text=left.text,
        claim=PROTECTIVE_PUT,
    )
    with pytest.raises(ValueError, match="varies nothing"):
        FramePair("no-contrast", left, right)


def test_frame_rejects_empty_text() -> None:
    with pytest.raises(ValueError, match="empty text"):
        Frame(frame_id="blank", family=FrameFamily.GAIN_LOSS, text="   ", claim=BARE_CALL)


def test_vanilla_option_identifies_a_single_option() -> None:
    assert vanilla_option(BARE_CALL) == (True, STRIKE)


def test_vanilla_option_rejects_a_multi_leg_claim() -> None:
    """Implied volatility is undefined for a portfolio, so the caller must be told."""
    assert vanilla_option(PROTECTIVE_PUT) is None


def test_vanilla_option_rejects_a_non_unit_quantity() -> None:
    doubled = Claim("two-calls", (Leg(kind=LegKind.CALL, quantity=2.0, strike=STRIKE),))
    assert vanilla_option(doubled) is None


def test_paired_valuation_reports_raw_difference_and_distortion() -> None:
    valuation = PairedValuation(
        pair_id="insurance-vs-upside",
        subject_id="model-a",
        left_value=12.0,
        right_value=9.5,
        oracle_price=10.0,
    )
    assert valuation.framing_difference == pytest.approx(2.5)
    assert valuation.distortion() == pytest.approx((2.0, -0.5))
