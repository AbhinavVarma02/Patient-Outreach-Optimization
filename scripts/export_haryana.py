"""Project the reviewed community-level results into the static application."""

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reports/haryana_empirical.json"
OUTPUT = ROOT / "web/src/haryana.json"
POLICIES = ("low_baseline_measles", "low_predicted_control_count", "ridge_t_learner")


def project(report: dict) -> dict:
    if report["version"] != 1 or report["license"] != "CC-BY-4.0":
        raise ValueError("Unexpected report schema or license.")
    figure = report["figure_4"]
    policy = report["policy_experiment"]
    if not figure["statsmodels_cross_check"] or min(policy["heldout_arm_villages"].values()) < 11:
        raise ValueError("Replication verification or disclosure threshold failed.")

    def rounded(value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("Expected a finite publication value.")
        return round(value, 2)

    def estimate(row: dict, bounds: list[float]) -> dict:
        if len(bounds) != 2 or not bounds[0] <= row["estimate"] <= bounds[1]:
            raise ValueError("Invalid interval.")
        return {"estimate": rounded(row["estimate"]), "ci": list(map(rounded, bounds))}

    def figure_result(name: str) -> dict:
        row = figure[name]["estimates"]["gossip"]
        return estimate(row, row["ci"])

    return {
        "controlMean": rounded(figure["pure_control_mean"]),
        "villageMonths": report["schema_audit"]["village_months"],
        "villages": report["schema_audit"]["villages"],
        "subCenterInterval": figure_result("sub_center_cr0"),
        "phcInterval": figure_result("phc_cr1"),
        "equalVillageMonthWeights": figure_result("equal_weights_phc_cr1"),
        "holdoutVillages": policy["heldout_villages"],
        "holdoutPhcs": policy["heldout_phcs"],
        "capacityPct": round(policy["village_capacity"] * 100),
        "comparisons": {
            name: estimate(policy["comparisons"][name]["delta_vs_uniform"],
                           policy["comparisons"][name]["simultaneous_ci"])
            for name in POLICIES
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    options = parser.parse_args()
    expected = json.dumps(project(json.loads(REPORT.read_bytes())), indent=2, allow_nan=False) + "\n"
    if options.check:
        if OUTPUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("The Haryana public data differ from the aggregate projection.")
    else:
        OUTPUT.write_text(expected, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
