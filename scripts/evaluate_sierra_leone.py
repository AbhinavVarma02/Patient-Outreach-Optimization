"""Train, freeze and evaluate village-level policies in the Sierra Leone trial."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform
from subprocess import check_output

import numpy as np
import pandas as pd
import scipy
from scipy.stats import t

from bounded_inference import hoeffding_radius
from evaluate_haryana import write_json
from replicate_sierra_leone import DEFAULT_CACHE, MANIFEST, ROOT, adults, load, replicate

SEED = 20261124
PROPENSITY = 2 / 3
CAPACITY = 0.5
PENALTY = 10
PROTOCOL = ROOT / "research/SIERRA_LEONE_PROTOCOL.md"
FEATURES = {
    "perc_immun": (0, 1), "perc_literacy": (0, 1), "avg_age": (0, 120),
    "health_fivemiles_above": (0, 1), "vaccinated_baseline_18": (0, 1),
}
POLICIES = ("low_baseline_uptake", "low_predicted_control", "ridge_t_learner", "ridge_dr_learner")


def score(y: np.ndarray, a: np.ndarray, mu: np.ndarray) -> np.ndarray:
    p = PROPENSITY
    return mu[:, 1] - mu[:, 0] + a * (y - mu[:, 1]) / p - (1 - a) * (y - mu[:, 0]) / (1 - p)


def fit_ridge(x: np.ndarray, y: np.ndarray) -> dict:
    mean = x.mean(axis=0)
    scale = x.std(axis=0)
    scale[scale == 0] = 1
    design = (x - mean) / scale
    beta = np.linalg.solve(design.T @ design + PENALTY * np.eye(x.shape[1]), design.T @ (y - y.mean()))
    return {"mean": mean.tolist(), "scale": scale.tolist(), "beta": beta.tolist(), "intercept": float(y.mean())}


def predict(x: np.ndarray, fit: dict) -> np.ndarray:
    return (x - np.array(fit["mean"])) / np.array(fit["scale"]) @ np.array(fit["beta"]) + fit["intercept"]


def fit_arms(x: np.ndarray, y: np.ndarray, a: np.ndarray) -> list[dict]:
    return [fit_ridge(x[a == arm], y[a == arm]) for arm in (0, 1)]


def predict_arms(x: np.ndarray, fits: list[dict]) -> np.ndarray:
    return np.clip(np.column_stack([predict(x, fit) for fit in fits]), 0, 1)


def fit_models(x: np.ndarray, y: np.ndarray, a: np.ndarray, fold: np.ndarray) -> dict:
    training_score = np.empty(len(y))
    for k in range(5):
        other = fold != k
        fit = fit_arms(x[other], y[other], a[other])
        rows = fold == k
        training_score[rows] = score(y[rows], a[rows], predict_arms(x[rows], fit))
    return {"arms": fit_arms(x, y, a), "dr": fit_ridge(x, training_score)}


def quota(ranking: np.ndarray) -> np.ndarray:
    if not np.isfinite(ranking).all() or len(ranking) == 0:
        raise ValueError("Quota requires nonempty, finite rankings")
    ordered = np.sort(ranking)[::-1]
    budget = len(ordered) * CAPACITY
    boundary = ordered[int(np.ceil(budget)) - 1]
    selected = ranking > boundary
    ties = ranking == boundary
    return selected.astype(float) + ties * (budget - selected.sum()) / ties.sum()


def block_ranges(weight: np.ndarray, nuisance: np.ndarray) -> np.ndarray:
    """Range of each triplet's mean score over legal assignments and bounded potential outcomes."""
    lower, upper = [], []
    for assignment in 1 - np.eye(3):
        at_zero = (weight.ravel() * score(np.zeros(weight.size), np.tile(assignment, len(weight)), nuisance))
        at_one = (weight.ravel() * score(np.ones(weight.size), np.tile(assignment, len(weight)), nuisance))
        lower.append(np.minimum(at_zero, at_one).reshape(-1, 3).mean(axis=1))
        upper.append(np.maximum(at_zero, at_one).reshape(-1, 3).mean(axis=1))
    return np.max(upper, axis=0) - np.min(lower, axis=0)


def inference(weight: np.ndarray, nuisance: np.ndarray, observed: np.ndarray, alpha: float) -> dict:
    block_weights = weight.reshape(-1, 3)
    values = (block_weights * observed.reshape(-1, 3)).mean(axis=1)
    point = float(values.mean())
    radius_t = float(t.ppf(0.975, len(values) - 1) * values.std(ddof=1) / np.sqrt(len(values)))
    radius = hoeffding_radius(block_ranges(block_weights, nuisance), alpha)
    return {"estimate": point, "nominal_t_95": [point - radius_t, point + radius_t],
            "simultaneous_bounded_95": [point - radius, point + radius]}


def split(villages: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    blocks = sorted(villages.grpID.unique(), key=lambda key: sha256(f"{SEED}:{int(key)}".encode()).digest())
    indexed = villages.assign(split_order=villages.grpID.map({key: i for i, key in enumerate(blocks)}))
    indexed = indexed.sort_values(["split_order", "community_code"])
    return indexed.loc[indexed.split_order.lt(30)], indexed.loc[indexed.split_order.ge(30)]


def features(villages: pd.DataFrame) -> np.ndarray:
    x = villages[list(FEATURES)].to_numpy(dtype=float)
    bounds = np.array(list(FEATURES.values()))
    if not np.isfinite(x).all() or np.any(x < bounds[:, 0]) or np.any(x > bounds[:, 1]):
        raise ValueError("Village features violate the pretreatment data contract")
    return x


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def freeze(path: Path, value: dict) -> str:
    if path.is_file():
        if json.loads(path.read_text(encoding="utf-8")) != value:
            raise ValueError(f"Frozen private artifact differs: {path.name}; use a new explicit run directory")
        return digest(path)
    return write_json(path, value)


def evaluate(cache: Path, private: Path) -> dict:
    replication = replicate(cache, True)
    if not replication["passed"]:
        raise ValueError("Policy evaluation requires the published replication gate")
    villages, people = load(cache)
    train, test = split(villages)
    train_keys = train.community_code.tolist()
    test_keys = test.community_code.tolist()
    if not private.resolve().is_relative_to((ROOT / "artifacts/private").resolve()):
        raise ValueError("Write the model only under artifacts/private")
    train_counts = train.treatment.value_counts().sort_index().to_list()
    test_counts = test.treatment.value_counts().sort_index().to_list()
    if train_counts != [30, 30, 30] or test_counts != [20, 20, 20]:
        raise ValueError("Split must retain whole matched triplets with arm overlap")
    x, x_test = features(train), features(test)
    training_rows = people.loc[
        people.community_code.isin(train_keys) & people.above18.eq(1) & people.in_census.eq(1)
    ]
    y = training_rows.groupby("community_code").vaccinated_endline.mean().loc[train_keys].to_numpy()
    a = train.treatment.ne(0).to_numpy(dtype=float)
    fits = fit_models(x, y, a, train.split_order.to_numpy() % 5)
    nuisance = predict_arms(x_test, fits["arms"])
    low_baseline = quota(-x_test[:, list(FEATURES).index("vaccinated_baseline_18")])
    rankings = (low_baseline, quota(-nuisance[:, 0]), quota(nuisance[:, 1] - nuisance[:, 0]),
                quota(predict(x_test, fits["dr"])))
    weights = dict(zip(POLICIES, rankings, strict=True))
    if any(not np.isclose(policy.mean(), CAPACITY) for policy in weights.values()):
        raise ValueError("Policy quota differs from the uniform comparator")
    model_path = private / "models.json"
    model_hash = freeze(model_path, {"feature_contract_version": 1, "feature_order": list(FEATURES),
                                     "fits": fits, "train_triplets": train.grpID.unique().tolist()})
    policy_path = private / "policies.json"
    policy_hash = freeze(policy_path, {"version": 1, "model_sha256": model_hash, "holdout_villages": test_keys,
                                       "rules": {name: value.tolist() for name, value in weights.items()}})
    if digest(model_path) != model_hash or digest(policy_path) != policy_hash:
        raise ValueError("Frozen artifacts changed before evaluation")
    cohort = adults(people)
    outcome = cohort.groupby("community_code").vaccinated_endline.mean().loc[test_keys].to_numpy()
    assignment = test.treatment.ne(0).to_numpy(dtype=float)
    observed = score(outcome, assignment, nuisance)
    unadjusted = score(outcome, assignment, np.zeros_like(nuisance))
    alpha = 0.05 / (len(weights) + 1)
    results = {}
    for name, policy in weights.items():
        contrast = policy - CAPACITY
        results[name] = {**inference(contrast, nuisance, observed, alpha),
                         "unaugmented_estimate": float(np.mean(contrast * unadjusted))}
    interaction = inference(4 * (low_baseline - CAPACITY), nuisance, observed, alpha)
    interaction["lower_baseline_half_itt"] = float(np.average(observed, weights=low_baseline))
    interaction["higher_baseline_half_itt"] = float(np.average(observed, weights=1 - low_baseline))
    protocol_commit = check_output(
        ["git", "log", "-1", "--format=%H", "--", str(PROTOCOL)], cwd=ROOT, text=True,
    ).strip()
    return {
        "schema_version": 1, "scope": "internal geographic village holdout; exploratory",
        "protocol_commit": protocol_commit,
        "digests": {"protocol": digest(PROTOCOL), "source_manifest": digest(MANIFEST),
                    "training_code": digest(Path(__file__)), "private_models": model_hash, "private_policies": policy_hash},
        "runtime": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
                    "scipy": scipy.__version__},
        "feature_contract": {"version": 1, "ranges": FEATURES, "features": list(FEATURES)},
        "workflow_gates": {"replication": True, "whole_triplets": True, "frozen_artifacts": True, "matched_quota": True},
        "seed": SEED, "ridge_penalty": PENALTY, "training_triplets": 30, "holdout_triplets": 20,
        "propensity": PROPENSITY, "family_size": len(weights) + 1, "matched_capacity": CAPACITY,
        "policies_vs_uniform": results, "low_vs_high_baseline_uptake": interaction,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--private", type=Path, default=ROOT / "artifacts/private/sierra-leone-v1")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    print(write_json(args.report, evaluate(args.cache, args.private)))


if __name__ == "__main__":
    main()
