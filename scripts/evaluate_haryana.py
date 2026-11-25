"""Audit the Haryana design, replicate Figure 4 uncertainty, and evaluate frozen policies."""

import argparse
from collections import Counter, defaultdict
import csv
from hashlib import file_digest, sha256
from io import BytesIO, TextIOWrapper
import json
from math import ceil, sqrt
from pathlib import Path
import platform
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

import numpy as np
from scipy.stats import t

from replicate_haryana import (
    ARCHIVE_SHA256, CONTROL, FILTER, MEMBER, MEMBER_SHA256, MISSING, OUTCOME, TIME_EFFECT, VARIANTS, WEIGHT,
)

BASELINE = "replication package/Data/Input Data/Baseline_Village.csv"
BASELINE_SHA = "b4ec3c94f8800e9b1434ff298597c805566fe8adafa9e1f6eead315c325e6c32"
GEO = ("id_district", "id_phc", "id_sc", "id_village_grp")
ARMS = (
    (CONTROL[0], "highflat", "lowflat", "highslope", "lowslope"),
    (CONTROL[1], "trfrac33_first", "trfrac66_first"),
    (CONTROL[2], "random", "gossip", "trusted", "trustgossip"),
)
FEATURES = ("d7_ab1_receive_card", "measles_ever", "a1_5_literate")
SEED = 20261124
PENALTY = 10
CAPACITY = 0.5
MIN_CELL = 11
COMMON_MONTHS = range(4, 11)
FISHER_DRAWS = 19_999


def read_member(archive: ZipFile, member: str, digest: str) -> list[dict[str, str]]:
    content = archive.read(member)
    if sha256(content).hexdigest() != digest:
        raise ValueError("Archive member checksum does not match.")
    with TextIOWrapper(BytesIO(content), encoding="utf-8-sig", errors="replace", newline="") as source:
        return list(csv.DictReader(source))


def load(path: Path) -> tuple[list[dict[str, str]], dict[str, tuple[float, ...]]]:
    with path.open("rb") as source:
        if file_digest(source, "sha256").hexdigest() != ARCHIVE_SHA256:
            raise ValueError("Archive checksum does not match the approved deposit.")
        with ZipFile(source) as archive:
            rows = read_member(archive, MEMBER, MEMBER_SHA256)
            baseline = read_member(archive, BASELINE, BASELINE_SHA)
    sample = [row for row in rows if all(row[key] == "1" for key in FILTER)]
    if not sample:
        raise ValueError("Empty ambassador analysis sample.")
    features = {
        row[GEO[3]]: tuple(float("nan") if row[field] in MISSING else float(row[field]) for field in FEATURES)
        for row in baseline
    }
    if len(features) != len(baseline):
        raise ValueError("Duplicate baseline village key.")
    return sample, features


def assignment(row: dict[str, str], flags: tuple[str, ...]) -> str:
    selected = [flag for flag in flags if row[flag] == "1"]
    if len(selected) != 1 or any(row[flag] not in {"0", "1"} for flag in flags):
        raise ValueError("Assignment must be one-hot in each intervention domain.")
    return selected[0]


def validate(
    rows: list[dict[str, str]], features: dict[str, tuple[float, ...]],
) -> dict[str, list[dict[str, str]]]:
    village_rows: dict[str, list[dict[str, str]]] = defaultdict(list)
    sc_context: dict[str, tuple[str, ...]] = {}
    phc_district: dict[str, str] = {}
    visit_keys: set[tuple[str, ...]] = set()
    for row in rows:
        district, phc, sc, village = (row[col] for col in GEO)
        date = (row["created_year"], row["created_month"])
        arms = tuple(assignment(row, flags) for flags in ARMS)
        context = (phc, district, *arms[:2])
        if sc_context.setdefault(sc, context) != context or phc_district.setdefault(phc, district) != district:
            raise ValueError("Unexpected geography or sub-center assignment variation.")
        if village_rows[village]:
            first = village_rows[village][0]
            constant_fields = (*GEO, WEIGHT, *(flag for flags in ARMS for flag in flags))
            if any(row[field] != first[field] for field in constant_fields):
                raise ValueError("Village geography, weight, or first-window assignment changes.")
        if (village, *date) in visit_keys:
            raise ValueError("Duplicate village-month.")
        visit_keys.add((village, *date))
        count, weight = float(row[OUTCOME]), float(row[WEIGHT])
        if not count.is_integer() or count < 0 or not np.isfinite(weight) or weight <= 0:
            raise ValueError("Invalid observed count or population weight.")
        if village not in features or not all(0 <= value <= 1 for value in features[village]):
            raise ValueError("Baseline feature is missing or invalid.")
        village_rows[village].append(row)
    return dict(village_rows)


def interval(estimate: float, se: float, clusters: int, alpha: float = 0.05) -> dict:
    radius = float(t.ppf(1 - alpha / 2, clusters - 1)) * se
    p_value = float(2 * t.sf(abs(estimate / se), clusters - 1)) if se else float(estimate == 0)
    return {"estimate": estimate, "standard_error": se, "ci": [estimate - radius, estimate + radius],
            "p_value": p_value, "clusters": clusters}


def regression(rows: list[dict[str, str]], cluster: str, weighted: bool, cr1: bool, reference: bool) -> dict:
    months = ["/".join(row[key] for key in TIME_EFFECT) for row in rows]
    _, month_index = np.unique(months, return_inverse=True)
    _, cluster_index = np.unique([row[cluster] for row in rows], return_inverse=True)
    groups = int(cluster_index.max()) + 1
    design = np.column_stack((
        [[float(row[field]) for field in VARIANTS] for row in rows],
        np.eye(int(month_index.max()) + 1)[month_index],
    ))
    weight = np.array([float(row[WEIGHT]) if weighted else 1.0 for row in rows])
    outcome = np.array([float(row[OUTCOME]) for row in rows])
    root = np.sqrt(weight)
    x = design * root[:, None]
    y = outcome * root
    beta, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    if rank != x.shape[1] or groups < MIN_CELL:
        raise ValueError("Regression does not have adequate rank or cluster support.")
    correction = groups / (groups - 1) * (len(rows) - 1) / (len(rows) - rank) if cr1 else 1.0
    scores = np.zeros((groups, rank))
    np.add.at(scores, cluster_index, x * (y - x @ beta)[:, None])
    influence = np.linalg.solve(x.T @ x, scores.T)
    variance = np.sum(influence**2, axis=1) * correction
    if reference:
        from statsmodels.regression.linear_model import WLS
        from statsmodels.stats.sandwich_covariance import cov_cluster

        fit = WLS(outcome, design, weights=weight).fit()
        np.testing.assert_allclose(fit.params, beta, atol=1e-9, rtol=0)
        np.testing.assert_allclose(np.diag(cov_cluster(fit, cluster_index, use_correction=cr1)),
                                   variance, atol=1e-9, rtol=0)
    estimates = {name: interval(float(beta[i]), sqrt(variance[i]), groups) for i, name in enumerate(VARIANTS)}
    previous = 0.0
    for i, name in enumerate(sorted(estimates, key=lambda key: estimates[key]["p_value"])):
        previous = min(1.0, max(previous, (len(estimates) - i) * estimates[name]["p_value"]))
        estimates[name]["holm_p_value"] = previous
    return {"village_months": len(rows), "estimates": estimates}


def split_phcs(phcs: set[str]) -> set[str]:
    ordered = sorted(phcs, key=lambda key: sha256(f"{SEED}:{key}".encode()).digest())
    return set(ordered[:ceil(0.4 * len(ordered))])


def fit_ridge(x: np.ndarray, y: np.ndarray, a: np.ndarray) -> dict:
    center = x.mean(axis=0)
    scale = x.std(axis=0)
    scale[scale == 0] = 1
    z = np.column_stack((np.ones(len(x)), (x - center) / scale))
    penalty = np.eye(z.shape[1]) * PENALTY
    penalty[0, 0] = 0
    coefficients = []
    for arm in (0, 1):
        arm_x = z[a == arm]
        coefficients.append(np.linalg.solve(arm_x.T @ arm_x + penalty, arm_x.T @ y[a == arm]).tolist())
    return {"features": list(FEATURES), "center": center.tolist(), "scale": scale.tolist(),
            "coefficients": coefficients, "penalty": PENALTY}


def capacity_rule(score: np.ndarray) -> np.ndarray:
    threshold = np.sort(score)[::-1][ceil(CAPACITY * len(score)) - 1]
    above, tied = score > threshold, score == threshold
    return above + tied * ((CAPACITY * len(score) - above.sum()) / tied.sum())


def score_difference(y: np.ndarray, a: np.ndarray, p: np.ndarray, m: np.ndarray) -> np.ndarray:
    if np.any((p <= 0) | (p >= 1)):
        raise ValueError("Policy effect requires support for both actions.")
    return m[:, 1] - m[:, 0] + a * (y - m[:, 1]) / p - (1 - a) * (y - m[:, 0]) / (1 - p)


def cluster_mean(values: np.ndarray, groups: list[str], alpha: float = 0.05) -> dict:
    count = len(set(groups))
    if count < MIN_CELL:
        raise ValueError("Too few PHCs for aggregate evaluation.")
    mean = float(values.mean())
    sums: dict[str, float] = defaultdict(float)
    for group, value in zip(groups, values, strict=True):
        sums[group] += float(value - mean)
    se = sqrt(count / (count - 1) * sum(value**2 for value in sums.values())) / len(values)
    return interval(mean, se, count, alpha)


def mean_count(rows: list[dict[str, str]], common: bool = False) -> float:
    counts = [float(row[OUTCOME]) for row in rows if not common or int(row["created_month"]) in COMMON_MONTHS]
    if not counts:
        raise ValueError("No observation in the restricted window.")
    return sum(counts) / len(counts)


def sharp_null_scores(y: np.ndarray, a: np.ndarray, p: np.ndarray, m: np.ndarray,
                      blocks: list[str]) -> np.ndarray:
    """Resample within the retained blocks under the full sharp null."""
    rng = np.random.default_rng(SEED)
    assignments = np.zeros((FISHER_DRAWS, len(a)), dtype=int)
    by_block: dict[str, list[int]] = defaultdict(list)
    for i, block in enumerate(blocks):
        by_block[block].append(i)
    for indices in by_block.values():
        total = int(a[indices].sum())
        order = np.argsort(rng.random((FISHER_DRAWS, len(indices))), axis=1)[:, :total]
        assignments[np.arange(FISHER_DRAWS)[:, None], np.asarray(indices)[order]] = 1
    return score_difference(y, assignments, p, m)


def policy_experiment(villages: dict[str, list[dict[str, str]]],
                      features: dict[str, tuple[float, ...]]) -> tuple[dict, dict]:
    blocks: dict[str, list[str]] = defaultdict(list)
    for village, rows in villages.items():
        if assignment(rows[0], ARMS[2]) in {"gossip", CONTROL[2]}:
            blocks[rows[0][GEO[2]]].append(village)
    treated = {v: int(rows[0]["gossip"]) for v, rows in villages.items()}
    eligible = [v for block in blocks.values() if len({treated[v] for v in block}) == 2 for v in block]
    propensity = {v: sum(treated[u] for u in block) / len(block)
                  for block in blocks.values() for v in block}
    phc = {v: rows[0][GEO[1]] for v, rows in villages.items()}
    train_groups = split_phcs({phc[v] for v in eligible})
    train = [v for v in eligible if phc[v] in train_groups]
    test = [v for v in eligible if phc[v] not in train_groups]
    if len(train_groups) < MIN_CELL or min(Counter(treated[v] for v in test).values(), default=0) < MIN_CELL:
        raise ValueError("Held-out intervention arm or training PHC count below release threshold.")
    if len({treated[v] for v in test}) != 2:
        raise ValueError("One held-out arm is absent.")

    # Freeze all parameters before reading held-out outcomes for scoring.
    model = fit_ridge(np.array([features[v] for v in train]),
                      np.array([mean_count(villages[v]) for v in train]),
                      np.array([treated[v] for v in train]))
    test_x = np.array([features[v] for v in test])
    z = np.column_stack((np.ones(len(test)), (test_x - model["center"]) / model["scale"]))
    m = z @ np.array(model["coefficients"]).T
    rules = {"low_baseline_measles": capacity_rule(-test_x[:, FEATURES.index("measles_ever")]),
             "low_predicted_control_count": capacity_rule(-m[:, 0]),
             "ridge_t_learner": capacity_rule(m[:, 1] - m[:, 0])}
    y = np.array([mean_count(villages[v]) for v in test])
    common_y = np.array([mean_count(villages[v], common=True) for v in test])
    a = np.array([treated[v] for v in test])
    p = np.array([propensity[v] for v in test])
    groups = [phc[v] for v in test]
    scores = score_difference(y, a, p, m)
    unaugmented = score_difference(y, a, p, np.zeros_like(m))
    common = score_difference(common_y, a, p, m)
    null_scores = sharp_null_scores(y, a, p, m, [villages[v][0][GEO[2]] for v in test])
    results = {}
    for name, rule in rules.items():
        contrast = rule - CAPACITY
        null_statistics = np.mean(null_scores * contrast, axis=1)
        observed = abs(float(np.mean(contrast * scores)))
        fisher_p = (1 + np.count_nonzero(np.abs(null_statistics) >= observed - 1e-12)) / (FISHER_DRAWS + 1)
        results[name] = {
            "expected_capacity": float(rule.mean()),
            "delta_vs_uniform": cluster_mean(contrast * scores, groups),
            "simultaneous_ci": cluster_mean(contrast * scores, groups, 0.05 / len(rules))["ci"],
            "ipw_sensitivity": cluster_mean(contrast * unaugmented, groups),
            "common_calendar_sensitivity": cluster_mean(contrast * common, groups),
            "sharp_null_p": fisher_p,
            "sharp_null_bonferroni_p": min(1.0, fisher_p * len(rules)),
        }
    report = {
        "unit": "recorded measles-1 vaccinations per eligible village per observed month",
        "village_capacity": CAPACITY, "villages": len(eligible), "sub_centers": len({villages[v][0][GEO[2]]
                                                                                     for v in eligible}),
        "train_villages": len(train), "heldout_villages": len(test), "train_phcs": len(train_groups),
        "heldout_phcs": len(set(groups)), "heldout_arm_villages": {"hub": int(a.sum()), "control": int(len(a)-a.sum())},
        "heldout_propensity_range": [float(p.min()), float(p.max())],
        "uniform_gain_vs_no_ambassador": cluster_mean(CAPACITY * scores, groups),
        "sharp_null_draws": FISHER_DRAWS,
        "comparisons": results,
        "limits": "Exploratory matched-block analysis conditional on exchangeability, roster observation and no between-village interference.",
    }
    return report, model


def write_json(path: Path, value: dict) -> str:
    if path.exists() and path.is_symlink():
        raise ValueError("Output must not be a symlink.")
    path.parent.mkdir(parents=True, exist_ok=True)
    content = (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    with NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
        temporary.write(content)
        pending = Path(temporary.name)
    try:
        pending.replace(path)
    finally:
        pending.unlink(missing_ok=True)
    return sha256(content).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--check-reference", action="store_true")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    rows, features = load(args.archive)
    villages = validate(rows, features)
    primary = regression(rows, GEO[2], True, False, args.check_reference)
    control = [row for row in rows if all(row[key] == "1" for key in CONTROL)]
    control_mean = float(np.average([float(row[OUTCOME]) for row in control],
                                    weights=[float(row[WEIGHT]) for row in control]))
    if round(primary["estimates"]["gossip"]["estimate"], 2) != 1.89 or round(control_mean, 2) != 7.32:
        raise ValueError("Published replication targets do not match.")
    policies, model = policy_experiment(villages, features)
    model_path = Path("artifacts/private/haryana/ridge.json")
    model_sha = write_json(model_path, model)
    bundle_sizes = Counter(tuple(assignment(series[0], flags) for flags in ARMS) for series in villages.values())
    report = {
        "version": 1, "study": "Haryana immunization experiment", "source": "https://zenodo.org/records/11392582",
        "license": "CC-BY-4.0", "archive_sha256": ARCHIVE_SHA256, "baseline_sha256": BASELINE_SHA,
        "prepared_member_sha256": MEMBER_SHA256,
        "protocol_sha256": sha256(Path("research/HARYANA_PROTOCOL.md").read_bytes()).hexdigest(),
        "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "ridge_model_sha256": model_sha, "holdout_seed": SEED,
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "schema_audit": {
            "villages": len(villages), "village_months": len(rows), "districts": len({r[GEO[0]] for r in rows}),
            "phcs": len({r[GEO[1]] for r in rows}), "sub_centers": len({r[GEO[2]] for r in rows}),
            "months_per_village": [min(map(len, villages.values())), max(map(len, villages.values()))],
            "observed_bundles": len(bundle_sizes), "bundles_below_11_villages": sum(n < MIN_CELL for n in bundle_sizes.values()),
        },
        "figure_4": {
            "pure_control_mean": control_mean, "sub_center_cr0": primary,
            "phc_cr1": regression(rows, GEO[1], True, True, args.check_reference),
            "equal_weights_phc_cr1": regression(rows, GEO[1], False, True, False),
            "april_october_phc_cr1": regression([r for r in rows if int(r["created_month"]) in COMMON_MONTHS],
                                               GEO[1], True, True, False),
            "statsmodels_cross_check": args.check_reference,
        },
        "policy_experiment": policies,
    }
    digest = write_json(args.report, report)
    print(json.dumps({"report": str(args.report), "sha256": digest}, sort_keys=True))


if __name__ == "__main__":
    main()
