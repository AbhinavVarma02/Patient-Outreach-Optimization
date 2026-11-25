"""Verify the CC0 Sierra Leone deposit and reproduce its randomized contrasts."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import t

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/manifests/sierra_leone_v1.json"
DEFAULT_CACHE = ROOT / ".cache/benchmark"


def load(cache: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    files = json.loads(MANIFEST.read_text(encoding="utf-8"))["files"]
    for name, pin in files.items():
        payload = (cache / name).read_bytes()
        if len(payload) != pin["bytes"] or sha256(payload).hexdigest() != pin["sha256"]:
            raise ValueError(f"Deposit file differs from pinned original: {name}")
    villages = pd.read_stata(cache / "community_data.tab", convert_categoricals=False)
    people = pd.read_stata(cache / "individual_level.tab", convert_categoricals=False)
    if villages.shape != (150, 37) or people.shape != (31913, 64):
        raise ValueError("Unexpected Sierra Leone source schema or row count")
    keys = ["community_code", "grpID", "treatment"]
    if villages[keys].isna().any().any() or villages.community_code.duplicated().any():
        raise ValueError("Incomplete or duplicate village key")
    triplets = villages.groupby("grpID").treatment.agg(lambda arm: sorted(arm) == [0, 1, 2])
    if len(triplets) != 50 or not triplets.all():
        raise ValueError("Expected 50 complete randomized triplets")
    if people.master_person_id.isna().any() or people.master_person_id.duplicated().any():
        raise ValueError("Incomplete or duplicate person key")
    joined = people[keys].merge(villages[keys], on=keys, how="left", indicator=True, validate="many_to_one")
    if not joined["_merge"].eq("both").all():
        raise ValueError("Person-to-village membership or assignment does not match")
    if not people.any_treat.eq(people.treatment.ne(0)).all():
        raise ValueError("Pooled assignment differs from the trial arms")
    return villages, people


def adults(people: pd.DataFrame) -> pd.DataFrame:
    records = people.loc[people.above18.eq(1) & people.in_census.eq(1)].copy()
    if len(records) != 12096 or not records.vaccinated_endline.isin([0, 1]).all():
        raise ValueError("Unexpected adult trial roster or missing endpoint")
    return records


def fit(data: pd.DataFrame, terms: list[str], block: str, cluster: str | None, reference: bool) -> tuple:
    outcome = data.vaccinated_endline.to_numpy(dtype=float)
    fixed = pd.get_dummies(data[block], dtype=float).to_numpy()
    design = np.column_stack((data[terms].to_numpy(dtype=float), fixed))
    n, k = design.shape
    if np.linalg.matrix_rank(design) != k:
        raise ValueError("Trial regression has collinear terms")
    coefficient = np.linalg.lstsq(design, outcome, rcond=None)[0]
    residual = outcome - design @ coefficient
    bread = np.linalg.inv(design.T @ design)
    if cluster is None:
        covariance = bread * (residual @ residual) / (n - k)
        degrees = n - k
    else:
        if data[cluster].isna().any():
            raise ValueError("Missing cluster key")
        groups, codes = np.unique(data[cluster], return_inverse=True)
        influence = np.zeros((len(groups), k))
        np.add.at(influence, codes, design * residual[:, None])
        uncorrected = bread @ influence.T @ influence @ bread
        # reghdfe treats an absorbed effect nested in the clusters as redundant.
        nested = data.groupby(cluster)[block].nunique().eq(1).all()
        correction = len(groups) / (len(groups) - 1) * (n - 1) / (n - k + (fixed.shape[1] - 1 if nested else 0))
        covariance = uncorrected * correction
        degrees = len(groups) - 1
    if reference:
        from statsmodels.api import OLS

        comparison = OLS(outcome, design).fit()
        np.testing.assert_allclose(coefficient, comparison.params, rtol=0, atol=1e-10)
        check = comparison.cov_params() if cluster is None else comparison.get_robustcov_results(
            cov_type="cluster", groups=data[cluster], use_correction=False,
        ).cov_params()
        np.testing.assert_allclose(covariance if cluster is None else uncorrected, check, rtol=0, atol=1e-10)
    return coefficient[:len(terms)], covariance[:len(terms), :len(terms)], degrees


def contrast(fit_result: tuple, weights: list[int], target: tuple[float, float] | None = None) -> dict:
    coefficients, covariance, degrees = fit_result
    effect = float(weights @ coefficients)
    se = float(np.sqrt(weights @ covariance @ weights))
    critical = float(t.ppf(0.975, degrees))
    result = {"estimate": effect, "standard_error": se, "lower": effect - critical * se,
              "upper": effect + critical * se, "p_value_t": float(2 * t.sf(abs(effect / se), degrees))}
    if target:
        result.update(published_estimate=target[0], published_standard_error=target[1],
                      rounded_match=(round(effect, 3), round(se, 3)) == target)
    return result


def structure_audit(people: pd.DataFrame, home: pd.DataFrame) -> dict:
    door_roster = people.loc[people.treatment.eq(1) & people.in_census.eq(1)]
    structures = door_roster.loc[door_roster.periphery.eq(0)]
    if structures.structure_id.isna().any() or not structures.dtd_treatment.isin([0, 1]).all():
        raise ValueError("Incomplete visit assignment for the retained census roster")
    if structures.groupby("structure_id").community_code.nunique().gt(1).any():
        raise ValueError("Structure key used across villages")
    units = structures.groupby(["community_code", "structure_id"]).agg(
        assigned=("dtd_treatment", "first"), flags=("dtd_treatment", "nunique"), households=("hh_id", "nunique"),
    )
    if units["flags"].ne(1).any():
        raise ValueError("Assignment varies within a randomized structure")
    counts = units.groupby("community_code").assigned.agg(["size", "sum"])
    overlap = counts["sum"].gt(0) & counts["sum"].lt(counts["size"])
    shares = counts.loc[overlap, "sum"] / counts.loc[overlap, "size"]
    return {
        "adult_rows": len(home), "adult_structures": home.structure_id.nunique(),
        "assigned_adults": int(home.dtd_treatment.sum()), "eligible_census_structures": len(units),
        "structures_with_multiple_households": int(units.households.gt(1).sum()),
        "villages_with_both_arms_in_released_roster": int(overlap.sum()),
        "villages_with_all_structures_assigned_in_released_roster": int(counts["sum"].eq(counts["size"]).sum()),
        "observed_assignment_share_range_in_overlap": [float(shares.min()), float(shares.max())],
        "villages_matching_the_up_to_20_rule": int(counts["sum"].eq(counts["size"].clip(upper=20)).sum()),
        "has_unknown_census_periphery": bool(door_roster.periphery.isna().any()),
        "has_household_keys_crossing_structure": bool(structures.groupby("hh_id").structure_id.nunique().gt(1).any()),
    }


def replicate(cache: Path, reference: bool) -> dict:
    _, people = load(cache)
    cohort = adults(people)
    village = cohort.groupby(["community_code", "grpID", "any_treat"], as_index=False).vaccinated_endline.mean()
    cohort["door"] = cohort.treatment.eq(1)
    cohort["group"] = cohort.treatment.eq(2)
    home = cohort.loc[cohort.door & cohort.periphery.eq(0)]
    pool = fit(cohort, ["any_treat"], "grpID", "community_code", reference)
    equal = fit(village, ["any_treat"], "grpID", None, reference)
    arms = fit(cohort, ["door", "group"], "grpID", "community_code", reference)
    visit = fit(home, ["dtd_treatment"], "community_code", "structure_id", reference)
    effects = {
        "mobile_package_adult_weighted": contrast(pool, [1], (0.261, 0.018)),
        "mobile_package_equal_village": contrast(equal, [1], (0.283, 0.025)),
        "mobile_plus_door_to_door_vs_control": contrast(arms, [1, 0], (0.293, 0.023)),
        "mobile_plus_small_group_vs_control": contrast(arms, [0, 1], (0.231, 0.021)),
        "mobile_door_to_door_vs_small_group": contrast(arms, [1, -1]),
        "extra_visit_within_door_to_door_villages": contrast(visit, [1], (-0.011, 0.019)),
    }
    diagnostics = structure_audit(people, home)
    passed = len(home) == 3760 and diagnostics["adult_structures"] == 1120 and all(
        effect.get("rounded_match", True) for effect in effects.values()
    )
    return {"schema_version": 1, "passed": passed, "statsmodels_reference_checked": reference,
            "adult_rows": len(cohort), "villages": len(village), "triplets": village.grpID.nunique(),
            "structure_audit": diagnostics, "effects": effects}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--check-reference", action="store_true")
    args = parser.parse_args()
    result = replicate(args.cache, args.check_reference)
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit("Published replication gate failed")


if __name__ == "__main__":
    main()
