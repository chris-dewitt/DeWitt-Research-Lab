"""Dense linear algebra for the CFI estimators, in pure Python.

The repository has no NumPy or SciPy dependency and this package does not add
one. The problems here are small — a handful of claims over a modest state grid
— and a pure-Python implementation keeps results bit-reproducible across
platforms, which matters more for this program than speed. Every routine is
deterministic and allocation-explicit; none of them mutate their arguments.
"""

from __future__ import annotations

from math import sqrt

Matrix = list[list[float]]
Vector = list[float]

# Below this, a Householder pivot is treated as a rank deficiency rather than a
# usable pivot. Chosen well above double-precision noise for the problem sizes
# this package handles.
PIVOT_TOLERANCE = 1e-12


class LinearAlgebraError(ValueError):
    """A matrix argument was malformed or a solve could not be completed."""


def shape(matrix: Matrix) -> tuple[int, int]:
    """Return ``(rows, columns)``, rejecting ragged input."""
    rows = len(matrix)
    if rows == 0:
        return 0, 0
    columns = len(matrix[0])
    if any(len(row) != columns for row in matrix):
        raise LinearAlgebraError("matrix rows have inconsistent lengths")
    return rows, columns


def mat_vec(matrix: Matrix, vector: Vector) -> Vector:
    """Compute ``matrix @ vector``."""
    rows, columns = shape(matrix)
    if len(vector) != columns:
        raise LinearAlgebraError(
            f"cannot multiply {rows}x{columns} matrix by length-{len(vector)} vector"
        )
    return [sum(matrix[i][j] * vector[j] for j in range(columns)) for i in range(rows)]


def mat_t_vec(matrix: Matrix, vector: Vector) -> Vector:
    """Compute ``matrix.T @ vector`` without forming the transpose."""
    rows, columns = shape(matrix)
    if len(vector) != rows:
        raise LinearAlgebraError(
            f"cannot multiply transposed {rows}x{columns} matrix by length-{len(vector)} vector"
        )
    return [sum(matrix[i][j] * vector[i] for i in range(rows)) for j in range(columns)]


def columns_of(matrix: Matrix, indices: list[int]) -> Matrix:
    """Return the submatrix holding only ``indices``, in the order given."""
    return [[row[j] for j in indices] for row in matrix]


def norm(vector: Vector) -> float:
    """Euclidean norm."""
    return sqrt(sum(value * value for value in vector))


def _householder_qr(matrix: Matrix, rhs: Vector) -> tuple[Matrix, Vector]:
    """Reduce ``matrix`` to upper-triangular form, applying the same reflections to ``rhs``.

    Returns the reduced matrix and transformed right-hand side. Both inputs are
    copied first, so neither argument is modified.
    """
    rows, columns = shape(matrix)
    reduced: Matrix = [row[:] for row in matrix]
    transformed: Vector = rhs[:]

    for k in range(min(rows - 1, columns)):
        column_norm = sqrt(sum(reduced[i][k] ** 2 for i in range(k, rows)))
        if column_norm <= PIVOT_TOLERANCE:
            continue
        # Choose the sign that avoids cancellation when forming the reflector.
        alpha = -column_norm if reduced[k][k] > 0.0 else column_norm
        reflector: Vector = [0.0] * rows
        reflector[k] = reduced[k][k] - alpha
        for i in range(k + 1, rows):
            reflector[i] = reduced[i][k]
        reflector_norm_squared = sum(reflector[i] ** 2 for i in range(k, rows))
        if reflector_norm_squared <= PIVOT_TOLERANCE:
            continue

        for j in range(k, columns):
            projection = sum(reflector[i] * reduced[i][j] for i in range(k, rows))
            scale = 2.0 * projection / reflector_norm_squared
            for i in range(k, rows):
                reduced[i][j] -= scale * reflector[i]
        projection = sum(reflector[i] * transformed[i] for i in range(k, rows))
        scale = 2.0 * projection / reflector_norm_squared
        for i in range(k, rows):
            transformed[i] -= scale * reflector[i]

    return reduced, transformed


def solve_least_squares(matrix: Matrix, rhs: Vector) -> Vector:
    """Return a least-squares solution of ``matrix @ x = rhs`` via Householder QR.

    Columns whose pivot falls below :data:`PIVOT_TOLERANCE` are rank-deficient;
    their coefficients are returned as zero rather than raising, which is what
    the NNLS driver needs when a passive set goes degenerate.
    """
    rows, columns = shape(matrix)
    if len(rhs) != rows:
        raise LinearAlgebraError(
            f"cannot solve {rows}x{columns} system against length-{len(rhs)} target"
        )
    if columns == 0:
        return []

    reduced, transformed = _householder_qr(matrix, rhs)
    solution: Vector = [0.0] * columns
    for i in range(min(rows, columns) - 1, -1, -1):
        pivot = reduced[i][i]
        if abs(pivot) <= PIVOT_TOLERANCE:
            solution[i] = 0.0
            continue
        accumulated = transformed[i]
        for j in range(i + 1, columns):
            accumulated -= reduced[i][j] * solution[j]
        solution[i] = accumulated / pivot
    return solution


def nnls(
    matrix: Matrix, target: Vector, *, tolerance: float = 1e-10, max_iterations: int = 0
) -> Vector:
    """Solve ``min ||matrix @ x - target||`` subject to ``x >= 0``.

    This is the Lawson-Hanson active-set algorithm. It terminates finitely: each
    outer step strictly decreases the residual, and there are finitely many
    active sets, so no set is visited twice. ``max_iterations`` defaults to the
    conventional ``3 * columns`` guard against pathological cycling under
    floating-point ties.
    """
    rows, columns = shape(matrix)
    if len(target) != rows:
        raise LinearAlgebraError(
            f"cannot fit {rows}x{columns} matrix to length-{len(target)} target"
        )
    if columns == 0:
        return []
    iteration_budget = max_iterations if max_iterations > 0 else 3 * columns

    solution: Vector = [0.0] * columns
    passive: list[int] = []
    active: list[int] = list(range(columns))

    for _ in range(iteration_budget):
        residual = [target[i] - value for i, value in enumerate(mat_vec(matrix, solution))]
        gradient = mat_t_vec(matrix, residual)
        candidates = [j for j in active if gradient[j] > tolerance]
        if not candidates:
            break
        entering = max(candidates, key=lambda j: gradient[j])
        active.remove(entering)
        passive.append(entering)
        passive.sort()

        for _ in range(iteration_budget):
            trial = solve_least_squares(columns_of(matrix, passive), target)
            if all(value > tolerance for value in trial):
                for position, index in enumerate(passive):
                    solution[index] = trial[position]
                break
            # Step only as far as the first passive coefficient that would go
            # negative, then release every coefficient that reached zero.
            step = min(
                (
                    solution[index] / (solution[index] - trial[position])
                    for position, index in enumerate(passive)
                    if trial[position] <= tolerance and solution[index] != trial[position]
                ),
                default=0.0,
            )
            for position, index in enumerate(passive):
                solution[index] += step * (trial[position] - solution[index])
            released = [index for index in passive if abs(solution[index]) <= tolerance]
            if not released:
                # Numerically stuck: accept the clipped trial and stop refining.
                for position, index in enumerate(passive):
                    solution[index] = max(trial[position], 0.0)
                break
            for index in released:
                solution[index] = 0.0
                passive.remove(index)
                active.append(index)
            active.sort()
            if not passive:
                break

    return solution
