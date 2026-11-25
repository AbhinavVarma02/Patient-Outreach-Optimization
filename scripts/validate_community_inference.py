"""Check fixed-rule inference in known-truth triplet and PHC lottery fixtures."""

import argparse
from itertools import product
import json
from pathlib import Path

import numpy as np
from scipy.stats import t

from bounded_inference import hoeffding_radius
from evaluate_haryana import bounded_policy, load, policy_experiment, validate, write_json
from evaluate_sierra_leone import PROPENSITY, SEED, block_ranges, quota, score

REPETITIONS = 10000


def known_answer() -> dict:
    assignments = 1 - np.eye(3)
    control = np.array([0.1, 0.4, 0.3])
    treated = np.array([0.6, 0.5, 0.8])
    mu = np.array([[0.2, 0.9], [0.5, 0.4], [0.2, 0.3]])
    weight = quota(np.array([0.0, 0.5, 0.5])) - 0.5
    truth = float(weight @ (treated - control) / 3)
    means = [float(weight @ score(control + a * (treated - control), a, mu) / 3) for a in assignments]
    vertices = [float(weight @ score(np.array(y), a, mu) / 3)
                for y in product([0.0, 1.0], repeat=3) for a in assignments]
    width = block_ranges(weight.reshape(1, 3), mu)[0]
    assert abs(float(np.mean(means)) - truth) < 1e-12
    assert abs(width - (max(vertices) - min(vertices))) < 1e-12
    assert abs(float(weight.sum())) < 1e-12
    return {"enumerated_estimate": float(np.mean(means)), "true_contrast": truth, "exact_range_width": float(width)}


def metrics(draws: np.ndarray, truth: float, radius_t: np.ndarray, radius_bounded: float) -> dict:
    error = np.abs(draws - truth)
    return {"target": truth, "bias": float(draws.mean() - truth), "simulation_se_of_mean": float(
            draws.std(ddof=1) / np.sqrt(REPETITIONS)), "nominal_t_coverage": float((error <= radius_t).mean()),
            "bounded_coverage": float((error <= radius_bounded).mean()), "bounded_radius": radius_bounded}


def triplets(shaped: bool, interference: bool = False) -> dict:
    rng = np.random.default_rng(SEED)
    n = 20
    x = rng.uniform(0, 1, (n, 3))
    baseline = 0.15 + 0.35 * x
    tau = 0.1 + 0.3 * x if shaped else np.zeros_like(x)
    fired = rng.integers(0, 3, (REPETITIONS, n, 1))
    a = (np.arange(3) != fired).astype(float)
    y = baseline + a * tau
    if interference:
        y = y + (1 - a) * 0.3 * x
    weight = quota(x.ravel()) - 0.5
    mu = np.column_stack(((baseline - 0.05).ravel(), (baseline + 0.2).ravel()))
    p = PROPENSITY
    m0, m1 = mu.T.reshape(2, n, 3)
    pseudo = m1 - m0 + a * (y - m1) / p - (1 - a) * (y - m0) / (1 - p)
    blocks = (pseudo * weight.reshape(n, 3)).mean(axis=2)
    return metrics(blocks.mean(axis=1), float(weight @ tau.ravel() / (3 * n)),
                   t.ppf(0.975, n - 1) * blocks.std(axis=1, ddof=1) / np.sqrt(n),
                   hoeffding_radius(block_ranges(weight.reshape(n, 3), mu), 0.05))


def matched_phcs(shaped: bool, interference: bool = False) -> dict:
    rng = np.random.default_rng(SEED)
    n = 19
    x = rng.uniform(0, 1, (n, 2))
    baseline = 2 + 8 * x + rng.uniform(0, 4, (n, 1))
    tau = 1 + 4 * x if shaped else np.zeros_like(x)
    weight = (quota(x.ravel()) - 0.5).reshape(n, 2)
    a = (np.arange(2) == rng.integers(0, 2, (REPETITIONS, n, 1))).astype(float)
    y = baseline + a * tau
    if interference:
        y = y + (1 - a) * (1 + 4 * x)
    m0, m1 = baseline - 0.8, baseline + 2
    pseudo = m1 - m0 + 2 * a * (y - m1) - 2 * (1 - a) * (y - m0)
    blocks = (weight * pseudo).mean(axis=2)
    ids = [str(i) for i in range(n) for _ in range(2)]
    first_draw = bounded_policy(weight.ravel(), y[0].ravel(), a[0].ravel(), np.full(2 * n, 0.5),
                                np.column_stack((m0.ravel(), m1.ravel())), ids, ids, 25, 0.05)
    assert abs(first_draw["estimate"] - float(blocks[0].mean())) < 1e-12
    return metrics(blocks.mean(axis=1), float(np.mean(weight * tau)),
                   t.ppf(0.975, n - 1) * blocks.std(axis=1, ddof=1) / np.sqrt(n),
                   first_draw["simultaneous_bounded_95"][1] - first_draw["estimate"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--haryana-archive", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    output = {"known_answer": known_answer(), "draws_per_scenario": REPETITIONS, "seed": SEED}
    for name, generate in (("triplet_lottery", triplets), ("matched_phc_lottery", matched_phcs)):
        simulations = {"null": generate(False), "heterogeneous": generate(True), "spillover": generate(True, True)}
        for scenario in ("null", "heterogeneous"):
            run = simulations[scenario]
            if abs(run["bias"]) > 4 * run["simulation_se_of_mean"] or run["bounded_coverage"] < 0.93:
                raise SystemExit(f"Statistical validation gate failed for {name}/{scenario}")
        output[name] = simulations
    if args.haryana_archive:
        records, features = load(args.haryana_archive)
        report, _ = policy_experiment(validate(records, features), features, bounded=True)
        output["haryana_capped_empirical"] = {name: effect["capped_at_25_sensitivity"]
                                               for name, effect in report["comparisons"].items()}
    if args.report:
        write_json(args.report, output)
    else:
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
