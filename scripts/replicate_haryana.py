"""Reproduce the two published Haryana Figure 4 point values with aggregate output."""

import argparse
import csv
from hashlib import file_digest, sha256
from io import BytesIO, TextIOWrapper
import json
from math import isclose
from pathlib import Path
import platform
from zipfile import ZipFile

import numpy as np

ARCHIVE_SHA256 = "052d7705d50d87ffa22992532e76776ea2c48fa4988635b08a4abece5fc2fe7e"
MEMBER = "replication package/Data/Prepared Data/Tablet_VillageXMonth_Costs.csv"
MEMBER_SHA256 = "6a09609b0a4cfd3c6ba8c4141a08c154d27f6b02d0c2252b1fa37274d85968d6"
VARIANTS = (
    "trfrac33_first", "trfrac66_first", "highflat", "lowflat", "highslope",
    "lowslope", "random", "gossip", "trusted", "trustgossip",
)
CONTROL = ("incentive_control", "reminder_control_first", "communication_control")
TIME_EFFECT = ("id_district", "created_year", "created_month")
OUTCOME = "shot_Measles1"
WEIGHT = "village_population"
CLUSTER = "id_sc"
FILTER = ("first_implementation", "seedsrisk")
MISSING = {"", "NA", "NaN"}
REFERENCE = {"information_hub_shots_per_village_month": 1.89, "pure_control_shots_per_village_month": 7.32}


def analyze(archive_path: Path, check_reference: bool = False) -> dict:
    with archive_path.open("rb") as source:
        if file_digest(source, "sha256").hexdigest() != ARCHIVE_SHA256:
            raise ValueError("Archive differs from the verified Zenodo v2 deposit.")
        source.seek(0)
        with ZipFile(source) as archive:
            member = archive.read(MEMBER)
    if sha256(member).hexdigest() != MEMBER_SHA256:
        raise ValueError("Prepared village-month CSV differs from the pinned member.")

    fields = (*VARIANTS, *TIME_EFFECT, OUTCOME, WEIGHT, CLUSTER)
    with TextIOWrapper(BytesIO(member), encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not set((*fields, *CONTROL, *FILTER)).issubset(reader.fieldnames or []):
            raise ValueError("Missing fields in prepared village-month CSV.")
        sample = [row for row in reader if all(row[key] == "1" for key in FILTER)]

    complete = [row for row in sample if all(row[key] not in MISSING for key in fields)]
    pure_control = [row for row in sample if all(row[key] == "1" for key in CONTROL)
                    and row[OUTCOME] not in MISSING and row[WEIGHT] not in MISSING]
    values = np.array([[float(row[key]) for key in VARIANTS] for row in complete])
    outcome = np.array([float(row[OUTCOME]) for row in complete])
    weight = np.array([float(row[WEIGHT]) for row in complete])
    time_labels = ["/".join(row[key] for key in TIME_EFFECT) for row in complete]
    _, groups = np.unique(time_labels, return_inverse=True)
    _, clusters = np.unique([row[CLUSTER] for row in complete], return_inverse=True)
    if not np.isin(values, (0, 1)).all() or not np.isfinite(outcome).all() or not np.all(outcome >= 0):
        raise ValueError("Expected binary variant indicators and nonnegative finite counts.")
    if not np.isfinite(weight).all() or not np.all(weight > 0):
        raise ValueError("Expected finite, positive population weights.")

    # Fit the weighted regression with an explicit dummy for every district-month and no intercept.
    fixed_effects = np.eye(int(groups.max()) + 1)[groups]
    design = np.column_stack((values, fixed_effects))
    root_weight = np.sqrt(weight)
    weighted_design = design * root_weight[:, None]
    weighted_outcome = outcome * root_weight
    beta, _, rank, _ = np.linalg.lstsq(weighted_design, weighted_outcome, rcond=None)
    if rank != design.shape[1]:
        raise ValueError("Figure 4 design is rank deficient.")

    # Use the sub-center CR0 variance for the targeted coefficient only.
    hub_index = VARIANTS.index("gossip")
    unit = np.eye(design.shape[1])[hub_index]
    bread_column = np.linalg.solve(weighted_design.T @ weighted_design, unit)
    residual = weighted_outcome - weighted_design @ beta
    cluster_score = np.bincount(clusters, weights=(weighted_design @ bread_column) * residual)
    cluster_se = float(np.linalg.norm(cluster_score))
    control_mean = np.average([float(row[OUTCOME]) for row in pure_control],
                              weights=[float(row[WEIGHT]) for row in pure_control])

    reproduced = dict(zip(REFERENCE, (float(beta[hub_index]), float(control_mean)), strict=True))
    report = {
        "study": "Banerjee et al. (2025), Haryana immunization, Figure 4",
        "specification_commit": "285addd4a5cc91001ceba34ba070316b34d4799b",
        "source": "https://zenodo.org/records/11392582",
        "data_license": "CC-BY-4.0",
        "archive_sha256": ARCHIVE_SHA256,
        "prepared_member_sha256": MEMBER_SHA256,
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "eligible_village_months": len(sample),
        "analyzed_village_months": len(complete),
        "pure_control_village_months": len(pure_control),
        "sub_center_clusters": len(cluster_score),
        "published": REFERENCE,
        "reproduced": reproduced,
        "matches_published_rounding": {name: round(reproduced[name], 2) == target
                                       for name, target in REFERENCE.items()},
        "information_hub_cr0_se_diagnostic": cluster_se,
    }
    if check_reference:
        from statsmodels import __version__ as reference_version  # type: ignore[import-untyped]
        from statsmodels.regression.linear_model import WLS  # type: ignore[import-untyped]
        from statsmodels.stats.sandwich_covariance import cov_cluster  # type: ignore[import-untyped]

        reference_fit = WLS(outcome, design, weights=weight).fit()
        reference_vcov = cov_cluster(reference_fit, clusters, use_correction=False)
        reference_beta = float(reference_fit.params[hub_index])
        reference_se = float(np.sqrt(reference_vcov[hub_index, hub_index]))
        tolerance = 1e-10
        if not (isclose(reference_beta, beta[hub_index], rel_tol=0.0, abs_tol=tolerance)
                and isclose(reference_se, cluster_se, rel_tol=0.0, abs_tol=tolerance)):
            raise ValueError("The coefficient or CR0 standard error disagrees with statsmodels.")
        report["statsmodels_reference"] = {
            "version": reference_version,
            "absolute_tolerance": tolerance,
            "coefficient": reference_beta,
            "cr0_standard_error": reference_se,
        }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--check-reference", action="store_true", help="Cross-check WLS and CR0 with statsmodels.")
    args = parser.parse_args()
    try:
        report = analyze(args.archive, args.check_reference)
    except (ImportError, OSError, ValueError) as error:
        parser.exit(1, f"Haryana replication failed. {error}\n")
    print(json.dumps(report, indent=2))
    if not all(report["matches_published_rounding"].values()):
        raise SystemExit("A reproduced value differs from the published rounding.")


if __name__ == "__main__":
    main()
