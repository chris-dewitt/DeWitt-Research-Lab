"""Numerical core: least squares and non-negative least squares."""

from __future__ import annotations

import pytest
from drl_cfi.linalg import (
    LinearAlgebraError,
    mat_t_vec,
    mat_vec,
    nnls,
    norm,
    solve_least_squares,
)


def test_least_squares_recovers_an_exact_solution() -> None:
    matrix = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    target = mat_vec(matrix, [2.0, -3.0])
    solution = solve_least_squares(matrix, target)
    assert solution == pytest.approx([2.0, -3.0], abs=1e-9)


def test_least_squares_residual_is_orthogonal_to_the_column_space() -> None:
    """The defining property of a least-squares fit: A^T (b - A x) = 0."""
    matrix = [[1.0, 1.0], [1.0, 2.0], [1.0, 3.0], [1.0, 4.0]]
    target = [1.0, 3.0, 2.0, 5.0]
    solution = solve_least_squares(matrix, target)
    residual = [t - f for t, f in zip(target, mat_vec(matrix, solution), strict=True)]
    assert mat_t_vec(matrix, residual) == pytest.approx([0.0, 0.0], abs=1e-9)


def test_least_squares_rejects_a_mismatched_target() -> None:
    with pytest.raises(LinearAlgebraError):
        solve_least_squares([[1.0], [1.0]], [1.0])


def test_nnls_matches_least_squares_when_the_solution_is_already_positive() -> None:
    matrix = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    target = mat_vec(matrix, [2.0, 3.0])
    assert nnls(matrix, target) == pytest.approx([2.0, 3.0], abs=1e-8)


def test_nnls_clamps_a_negative_coefficient_to_zero() -> None:
    """Unconstrained the second weight is negative, so NNLS must pin it at zero."""
    matrix = [[1.0, 0.0], [0.0, 1.0]]
    target = [2.0, -5.0]
    solution = nnls(matrix, target)
    assert solution[1] == pytest.approx(0.0, abs=1e-9)
    assert solution[0] == pytest.approx(2.0, abs=1e-9)


def test_nnls_never_returns_a_negative_weight() -> None:
    matrix = [[1.0, 2.0, 3.0], [2.0, 1.0, 0.0], [0.5, 1.5, 1.0], [1.0, 1.0, 1.0]]
    target = [-3.0, 4.0, -1.0, 2.0]
    assert all(value >= -1e-12 for value in nnls(matrix, target))


def test_nnls_residual_does_not_exceed_the_zero_solution() -> None:
    """A fit can never be worse than the all-zero feasible point."""
    matrix = [[1.0, 2.0], [3.0, 1.0], [0.0, 1.0]]
    target = [1.0, -2.0, 4.0]
    solution = nnls(matrix, target)
    fitted = mat_vec(matrix, solution)
    residual = norm([t - f for t, f in zip(target, fitted, strict=True)])
    assert residual <= norm(target) + 1e-9
