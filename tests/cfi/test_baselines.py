"""Tests for the CFI-005 belief-dynamics baselines and their recovery study."""

from __future__ import annotations

import math

import pytest
from drl_cfi.baselines import (
    MAX_REPRESENTABLE_LOG_ODDS,
    SaturatedBeliefError,
    fit_asymmetric_bayesian,
    fit_bayesian,
    fit_diffusion,
    fit_jump_diffusion,
    fit_ornstein_uhlenbeck,
    recovery_study,
    simulate_asymmetric_bayesian,
    simulate_bayesian,
    simulate_diffusion,
    simulate_jump_diffusion,
    simulate_ornstein_uhlenbeck,
)
from drl_cfi.beliefs import Maturity, SubjectKind

ALTERNATING = [0.6, -0.5, 0.7, -0.4, 0.55, -0.65, 0.45, -0.35] * 8


class TestSimulatorsProduceSchemaRecords:
    def test_paths_are_synthetic_and_labelled(self) -> None:
        path = simulate_diffusion(drift=0.2, volatility=0.5, steps=20, dt=0.1, seed=1)
        assert path.is_synthetic
        assert path.maturity is Maturity.SYNTHETIC
        assert path.subject_kind is SubjectKind.SIMULATOR
        assert len(path) == 21

    def test_same_seed_same_path(self) -> None:
        kwargs = dict(drift=0.2, volatility=0.5, steps=50, dt=0.1)
        a = simulate_diffusion(seed=99, **kwargs)  # type: ignore[arg-type]
        b = simulate_diffusion(seed=99, **kwargs)  # type: ignore[arg-type]
        assert a.log_odds_path() == b.log_odds_path()

    def test_different_seed_different_path(self) -> None:
        kwargs = dict(drift=0.2, volatility=0.5, steps=50, dt=0.1)
        a = simulate_diffusion(seed=1, **kwargs)  # type: ignore[arg-type]
        b = simulate_diffusion(seed=2, **kwargs)  # type: ignore[arg-type]
        assert a.log_odds_path() != b.log_odds_path()


class TestSaturationIsLoud:
    def test_runaway_belief_raises(self) -> None:
        # A strong one-directional drift leaves the representable range. Before
        # this raised, the report pinned at the boundary and every later
        # increment was exactly zero — which the estimators read as data.
        with pytest.raises(SaturatedBeliefError, match="representable"):
            simulate_diffusion(drift=50.0, volatility=0.1, steps=200, dt=0.1, seed=3)

    def test_error_names_the_bound(self) -> None:
        with pytest.raises(SaturatedBeliefError) as excinfo:
            simulate_diffusion(drift=50.0, volatility=0.1, steps=200, dt=0.1, seed=3)
        assert f"{MAX_REPRESENTABLE_LOG_ODDS:.3f}" in str(excinfo.value)

    def test_in_range_paths_are_unaffected(self) -> None:
        path = simulate_diffusion(drift=0.1, volatility=0.4, steps=100, dt=0.05, seed=4)
        assert max(abs(v) for v in path.log_odds_path()) < MAX_REPRESENTABLE_LOG_ODDS


class TestExactBayesian:
    def test_recovers_per_evidence_llr(self) -> None:
        # In log-odds Bayes is addition, so a noiseless path recovers exactly.
        llrs = [0.8, -0.3, 0.8, -0.3, 0.8, -0.3]
        ids = ["strong", "weak", "strong", "weak", "strong", "weak"]
        path = simulate_bayesian(llrs, seed=11, evidence_ids=ids)
        fit = fit_bayesian(path)
        assert fit.llr_by_evidence["strong"] == pytest.approx(0.8, abs=1e-9)
        assert fit.llr_by_evidence["weak"] == pytest.approx(-0.3, abs=1e-9)
        assert fit.residual_scale == pytest.approx(0.0, abs=1e-9)

    def test_reporting_noise_shows_up_as_residual_not_bias(self) -> None:
        llrs = [0.5, -0.5] * 60
        ids = ["up", "down"] * 60
        path = simulate_bayesian(llrs, seed=12, report_noise=0.05, evidence_ids=ids)
        fit = fit_bayesian(path)
        assert fit.llr_by_evidence["up"] == pytest.approx(0.5, abs=0.05)
        assert fit.residual_scale > 0.0

    def test_unlabelled_path_refuses_attribution(self) -> None:
        path = simulate_diffusion(drift=0.1, volatility=0.3, steps=20, dt=1.0, seed=13)
        with pytest.raises(ValueError, match="no evidence-labelled"):
            fit_bayesian(path)


class TestAsymmetricBayesian:
    def test_recovers_both_weights(self) -> None:
        path = simulate_asymmetric_bayesian(
            ALTERNATING, confirming_weight=1.4, disconfirming_weight=0.6, seed=21
        )
        fit = fit_asymmetric_bayesian(path, ALTERNATING)
        assert fit.confirming_weight == pytest.approx(1.4, abs=1e-6)
        assert fit.disconfirming_weight == pytest.approx(0.6, abs=1e-6)
        assert fit.asymmetry == pytest.approx(0.8, abs=1e-6)

    def test_exact_bayes_is_nested_at_unit_weights(self) -> None:
        path = simulate_asymmetric_bayesian(
            ALTERNATING, confirming_weight=1.0, disconfirming_weight=1.0, seed=22
        )
        fit = fit_asymmetric_bayesian(path, ALTERNATING)
        assert fit.asymmetry == pytest.approx(0.0, abs=1e-6)

    def test_one_sided_evidence_cannot_separate_the_weights(self) -> None:
        one_sided = [0.5] * 20
        path = simulate_asymmetric_bayesian(
            one_sided, confirming_weight=1.2, disconfirming_weight=0.7, seed=23
        )
        with pytest.raises(ValueError, match="both confirming and disconfirming"):
            fit_asymmetric_bayesian(path, one_sided)

    def test_length_mismatch_rejected(self) -> None:
        path = simulate_asymmetric_bayesian(
            ALTERNATING, confirming_weight=1.0, disconfirming_weight=1.0, seed=24
        )
        with pytest.raises(ValueError, match="one nominal LLR per increment"):
            fit_asymmetric_bayesian(path, ALTERNATING[:-1])


class TestDiffusion:
    def test_recovers_drift_and_volatility(self) -> None:
        path = simulate_diffusion(drift=0.4, volatility=0.8, steps=4000, dt=0.01, seed=31)
        fit = fit_diffusion(path)
        assert fit.drift == pytest.approx(0.4, abs=0.2)
        assert fit.volatility == pytest.approx(0.8, abs=0.05)

    def test_volatility_is_scaled_by_the_gap_not_the_step(self) -> None:
        # Halving dt must not halve the estimated volatility.
        fine = fit_diffusion(
            simulate_diffusion(drift=0.0, volatility=0.6, steps=4000, dt=0.01, seed=32)
        )
        coarse = fit_diffusion(
            simulate_diffusion(drift=0.0, volatility=0.6, steps=2000, dt=0.02, seed=32)
        )
        assert fine.volatility == pytest.approx(coarse.volatility, abs=0.05)


class TestOrnsteinUhlenbeck:
    def test_recovers_level_and_volatility(self) -> None:
        path = simulate_ornstein_uhlenbeck(
            reversion_rate=1.5, level=0.7, volatility=0.6, steps=4000, dt=0.02, seed=41
        )
        fit = fit_ornstein_uhlenbeck(path)
        assert fit.level == pytest.approx(0.7, abs=0.15)
        assert fit.volatility == pytest.approx(0.6, abs=0.05)
        assert fit.reversion_rate == pytest.approx(1.5, rel=0.35)

    def test_half_life_matches_the_reversion_rate(self) -> None:
        path = simulate_ornstein_uhlenbeck(
            reversion_rate=2.0, level=0.0, volatility=0.5, steps=4000, dt=0.02, seed=42
        )
        fit = fit_ornstein_uhlenbeck(path)
        assert fit.half_life == pytest.approx(math.log(2.0) / fit.reversion_rate)

    def test_driftless_walk_reports_no_reversion(self) -> None:
        # The random walk is nested at theta = 0; the fit should sit near it
        # rather than inventing a pull.
        path = simulate_diffusion(drift=0.0, volatility=0.5, steps=4000, dt=0.02, seed=43)
        fit = fit_ornstein_uhlenbeck(path)
        assert abs(fit.reversion_rate) < 0.5


class TestJumpDiffusion:
    def test_separates_jumps_from_diffusion(self) -> None:
        path = simulate_jump_diffusion(
            drift=0.0,
            volatility=0.4,
            jump_intensity=0.5,
            jump_mean=0.0,
            jump_scale=2.0,
            steps=3000,
            dt=0.02,
            seed=51,
        )
        fit = fit_jump_diffusion(path)
        # Large jumps relative to the diffusion are the case thresholding is
        # good at, so volatility should be clean here.
        assert fit.volatility == pytest.approx(0.4, abs=0.05)
        assert fit.jump_count > 0

    def test_no_jumps_reduces_to_the_diffusion_fit(self) -> None:
        path = simulate_diffusion(drift=0.2, volatility=0.5, steps=2000, dt=0.02, seed=52)
        jump = fit_jump_diffusion(path)
        plain = fit_diffusion(path)
        assert jump.jump_intensity == pytest.approx(0.0, abs=0.2)
        assert jump.volatility == pytest.approx(plain.volatility, rel=0.1)

    def test_small_jumps_are_undetectable_by_construction(self) -> None:
        # Jumps below the detection threshold are indistinguishable from
        # diffusion. This is a property of thresholding, not a defect, and the
        # estimator must under-report rather than pretend otherwise.
        path = simulate_jump_diffusion(
            drift=0.0,
            volatility=0.5,
            jump_intensity=0.8,
            jump_mean=0.0,
            jump_scale=1.2,
            steps=400,
            dt=0.05,
            seed=53,
        )
        fit = fit_jump_diffusion(path)
        assert fit.jump_intensity < 0.8


class TestRecoveryStudy:
    def test_diffusion_recovers_volatility_tightly(self) -> None:
        report = recovery_study(
            "diffusion", replications=40, steps=400, dt=0.05, drift=0.4, volatility=0.8
        )
        assert abs(report.by_name("volatility").relative_bias) < 0.05

    def test_drift_error_matches_the_information_limit(self) -> None:
        # Drift over a finite horizon has standard error sigma/sqrt(T); no
        # estimator does better. Recording that here keeps a future reader from
        # reading the wide drift interval as a bug in the estimator.
        steps, dt, volatility = 400, 0.05, 0.8
        report = recovery_study(
            "diffusion",
            replications=60,
            steps=steps,
            dt=dt,
            drift=0.4,
            volatility=volatility,
        )
        horizon = steps * dt
        limit = volatility / math.sqrt(horizon)
        assert report.by_name("drift").root_mean_square_error == pytest.approx(limit, rel=0.4)

    def test_ornstein_uhlenbeck_reversion_is_biased_upward(self) -> None:
        # The least-squares OU estimator inherits the classic downward bias of
        # the AR(1) coefficient, which appears as an upward bias in theta.
        report = recovery_study(
            "ornstein_uhlenbeck",
            replications=40,
            steps=400,
            dt=0.05,
            reversion_rate=1.5,
            level=0.7,
            volatility=0.6,
        )
        assert report.by_name("reversion_rate").bias > 0.0
        assert abs(report.by_name("level").relative_bias) < 0.15

    def test_report_renders_without_a_verdict(self) -> None:
        report = recovery_study(
            "diffusion", replications=5, steps=100, dt=0.05, drift=0.2, volatility=0.5
        )
        text = report.render()
        assert "truth" in text and "bias" in text
        # No pass/fail language: thresholds belong to a protocol, and G3 has
        # not been passed.
        assert "pass" not in text.lower() and "fail" not in text.lower()

    def test_unknown_model_rejected(self) -> None:
        with pytest.raises(ValueError, match="unknown model"):
            recovery_study("neural_sde", replications=1, steps=10, dt=0.1)

    def test_zero_replications_rejected(self) -> None:
        with pytest.raises(ValueError, match="at least one replication"):
            recovery_study("diffusion", replications=0, drift=0.1, volatility=0.5)

    def test_study_is_reproducible_from_its_seed(self) -> None:
        kwargs = dict(replications=10, steps=200, dt=0.05, drift=0.3, volatility=0.6)
        a = recovery_study("diffusion", seed=777, **kwargs)  # type: ignore[arg-type]
        b = recovery_study("diffusion", seed=777, **kwargs)  # type: ignore[arg-type]
        assert a.by_name("drift").estimates == b.by_name("drift").estimates
