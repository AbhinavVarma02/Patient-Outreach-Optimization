"""Reproducible known-truth validation on generated, independent trial records."""
import argparse
import hashlib
import json
from math import sqrt
from pathlib import Path
from random import Random
from statistics import mean, stdev

from .estimators import contrast_scores, summarize

SCENARIOS = {
    "null": (0.0, 0.0, 0.0),
    "homogeneous": (0.03, 0.03, 0.03),
    "monotonic": (0.01, 0.04, 0.08),
    "inverted_u": (0.01, 0.09, 0.02),
    "weak": (0.024, 0.033, 0.029),
    "strong": (-0.04, 0.15, 0.025),
}
SHARES = (0.3, 0.5, 0.2)
BASELINE = (0.40, 0.32, 0.20)
CAPACITY = 0.2
ASSIGNMENT = 0.75
POLICY = (0.0, 0.0, 1.0)


def wilson(hits: int, n: int) -> list[float]:
    p, z = hits / n, 1.95996398454
    center = (p + z*z / (2*n)) / (1 + z*z/n)
    width = z*sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return [center-width, center+width]


def simulate(reps: int, n: int, seed: int) -> dict[str, object]:
    if reps < 1000 or n < 100:
        raise ValueError("Use at least 1,000 replicates of at least 100 independent records.")
    rng = Random(seed)
    results: dict[str, object] = {}
    for name, effects in SCENARIOS.items():
        weights = [prob - CAPACITY for prob in POLICY]
        truth = sum(s*w*t for s, w, t in zip(SHARES, weights, effects, strict=True))
        regret = CAPACITY * (max(effects) - effects[-1])
        covered = 0
        estimates = []
        for _ in range(reps):
            group = rng.choices(range(3), weights=SHARES, k=n)
            t = [int(rng.random() < ASSIGNMENT) for _ in group]
            p0 = [BASELINE[g] for g in group]
            p1 = [BASELINE[g] + effects[g] for g in group]
            y = [int(rng.random() < (b if a else c)) for a, b, c in zip(t, p1, p0, strict=True)]
            effect = summarize(contrast_scores(t, y, [ASSIGNMENT]*n, [weights[g] for g in group], p0, p1))
            covered += effect.lower <= truth <= effect.upper
            estimates.append(effect.value)
        bias = mean(estimates) - truth
        sampling_sd = stdev(estimates)
        results[name] = {
            "truth": truth, "bias": bias, "sampling_sd": sampling_sd,
            "bias_mcse": sampling_sd/sqrt(reps), "coverage": covered/reps,
            "coverage_mc_interval": wilson(covered, reps),
            "null_rejection": (reps-covered)/reps if name in ("null", "homogeneous") else None,
            "policy_regret": regret,
        }
    return {"kind": "fictional_known_truth", "seed": seed, "replicates": reps, "n": n,
            "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "estimator_sha256": hashlib.sha256(Path(__file__).with_name("estimators.py").read_bytes()).hexdigest(),
            "results": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reps", type=int, default=1000)
    parser.add_argument("--n", type=int, default=700)
    parser.add_argument("--seed", type=int, default=20261124)
    args = parser.parse_args()
    print(json.dumps(simulate(args.reps, args.n, args.seed), indent=2))
