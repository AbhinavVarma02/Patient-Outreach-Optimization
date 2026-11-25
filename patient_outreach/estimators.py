"""Independent randomized evaluation with known assignment probabilities."""
from collections.abc import Sequence
from dataclasses import dataclass
from math import isfinite, sqrt
from statistics import NormalDist, mean, variance


@dataclass(frozen=True)
class Estimate:
    value: float
    se: float
    lower: float
    upper: float
    n: int


def summarize(scores: Sequence[float], alpha: float = 0.05) -> Estimate:
    if len(scores) < 2 or not all(isfinite(x) for x in scores) or not 0 < alpha < 1:
        raise ValueError("Inference requires finite scores, at least two independent rows and valid alpha.")
    value = mean(scores)
    se = sqrt(variance(scores, xbar=value) / len(scores))
    radius = NormalDist().inv_cdf(1 - alpha / 2) * se
    return Estimate(value, se, value - radius, value + radius, len(scores))


def contrast_scores(
    treatment: Sequence[int], outcomes: Sequence[float], propensity: Sequence[float],
    weights: Sequence[float], m0: Sequence[float], m1: Sequence[float],
) -> list[float]:
    """Paired AIPW contrast for fixed stochastic policy probabilities, q1 minus q0.

    All model predictions and policy probabilities must come from a design fixed
    independently of these outcomes. Zero nuisance predictions give IPW.
    The sampling unit must be independent for summarize's standard error.
    """
    result = []
    for a, y, e, weight, p0, p1 in zip(treatment, outcomes, propensity, weights, m0, m1, strict=True):
        if (a not in (0, 1) or y not in (0, 1) or not 0 < e < 1 or not -1 <= weight <= 1
                or not 0 <= p0 <= 1 or not 0 <= p1 <= 1):
            raise ValueError("Invalid assignment, outcome, propensity, policy contrast or nuisance probability.")
        residual = (y - p1) / e if a else -(y - p0) / (1 - e)
        result.append(weight * (p1 - p0 + residual))
    return result


def difference_in_means(treatment: Sequence[int], outcomes: Sequence[float]) -> Estimate:
    arms: tuple[list[float], list[float]] = ([], [])
    for assigned, outcome in zip(treatment, outcomes, strict=True):
        if assigned not in (0, 1) or outcome not in (0, 1):
            raise ValueError("Assignment and outcome must be binary.")
        arms[assigned].append(outcome)
    control, treated = arms
    if min(len(control), len(treated)) < 2:
        raise ValueError("Both treatment arms need at least two observations.")
    value = mean(treated) - mean(control)
    se = sqrt(variance(treated) / len(treated) + variance(control) / len(control))
    radius = NormalDist().inv_cdf(0.975) * se
    return Estimate(value, se, value - radius, value + radius, len(treatment))


def holm(p_values: Sequence[float]) -> list[float]:
    if not all(0 <= value <= 1 for value in p_values):
        raise ValueError("P values must be in [0, 1].")
    adjusted = [0.0] * len(p_values)
    bound = 0.0
    for rank, index in enumerate(sorted(range(len(p_values)), key=p_values.__getitem__)):
        bound = min(1.0, max(bound, (len(p_values) - rank) * p_values[index]))
        adjusted[index] = bound
    return adjusted
