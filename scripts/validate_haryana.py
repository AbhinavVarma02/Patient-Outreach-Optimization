"""Known-truth calibration for the held-out community policy score."""

import json

import numpy as np
from scipy.stats import t

from evaluate_haryana import CAPACITY, SEED, capacity_rule, score_difference

REPETITIONS = 3000
PHCS = 19


def simulate(shaped: bool, spillover: bool = False) -> dict:
    rng = np.random.default_rng(SEED)
    x = rng.uniform(0, 1, (PHCS, 2))
    baseline = 2 + 8 * x + rng.uniform(0, 4, (PHCS, 1))
    effect = 1 + 4 * x if shaped else np.zeros_like(x)
    weights = (capacity_rule(x.ravel()) - CAPACITY).reshape(PHCS, 2)
    true_value = float(np.mean(weights * effect))
    model = np.stack((baseline - 0.8, baseline + 2)).reshape(2, -1).T
    estimates, covered = [], []
    critical = float(t.ppf(0.975, PHCS - 1))
    for _ in range(REPETITIONS):
        chosen = rng.integers(0, 2, size=(PHCS, 1))
        assignment = (np.arange(2) == chosen).astype(float)
        outcome = baseline + assignment * effect
        if spillover:
            # Each selected village also changes outcomes in the other village.
            outcome = outcome + (1 - assignment) * (1 + 4 * x)
        score = score_difference(outcome.ravel(), assignment.ravel(), np.full(2 * PHCS, 0.5), model)
        block_means = (weights * score.reshape(PHCS, 2)).mean(axis=1)
        value = float(block_means.mean())
        radius = critical * float(block_means.std(ddof=1)) / np.sqrt(PHCS)
        estimates.append(value)
        covered.append(abs(value - true_value) <= radius)
    coverage = float(np.mean(covered))
    return {"contrast_under_no_spillover": true_value, "mean_estimate": float(np.mean(estimates)),
            "bias_vs_no_spillover_target": float(np.mean(estimates)) - true_value,
            "coverage_of_no_spillover_target": coverage,
            "coverage_monte_carlo_se": float(np.sqrt(coverage * (1 - coverage) / REPETITIONS))}


if __name__ == "__main__":
    print(json.dumps({
        "scope": "fictional matched village pairs with one lottery per PHC",
        "replicates_per_scenario": REPETITIONS, "phcs": PHCS, "seed": SEED,
        "null": simulate(False), "heterogeneous": simulate(True), "between_village_spillover": simulate(True, True),
    }, indent=2))
