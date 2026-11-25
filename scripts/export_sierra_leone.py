"""Project verified Sierra Leone studies to the explicitly reviewed web schema."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "research/reports"
TARGET = ROOT / "web/src/sierra-leone.json"


def project() -> dict:
    replication = json.loads((REPORTS / "sierra_leone_replication.json").read_bytes())
    policies = json.loads((REPORTS / "sierra_leone_policy.json").read_bytes())
    if (replication["schema_version"] != 1 or policies["schema_version"] != 1 or not replication["passed"]
            or not replication["statsmodels_reference_checked"] or not all(policies["workflow_gates"].values())
            or min(policies["training_triplets"], policies["holdout_triplets"]) < 11):
        raise ValueError("Sierra Leone public projection requires verified schemas, replication and frozen policy gates")
    effects = {}
    for key in ("mobile_package_adult_weighted", "mobile_package_equal_village", "mobile_door_to_door_vs_small_group",
                "extra_visit_within_door_to_door_villages"):
        result = replication["effects"][key]
        effects[key] = {"pp": round(100 * result["estimate"], 1),
                        "ci": [round(100 * result[bound], 1) for bound in ("lower", "upper")]}
    comparisons = {}
    for key in ("low_baseline_uptake", "low_predicted_control", "ridge_t_learner", "ridge_dr_learner"):
        rule = policies["policies_vs_uniform"][key]
        comparisons[key] = {"pp": round(100 * rule["estimate"], 1),
                            "ci": [round(100 * x, 1) for x in rule["simultaneous_bounded_95"]]}
    if any(not effect["ci"][0] <= 0 <= effect["ci"][1] for effect in comparisons.values()):
        raise ValueError("Policy claim change requires a fresh review before export")
    return {"schemaVersion": 1, "villages": replication["villages"], "adults": replication["adult_rows"],
            "structureTrialAdults": replication["structure_audit"]["adult_rows"],
            "structureTrialUnits": replication["structure_audit"]["adult_structures"], "effects": effects,
            "holdoutTriplets": policies["holdout_triplets"], "capacityPct": round(policies["matched_capacity"] * 100),
            "policiesVsUniform": comparisons}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    content = json.dumps(project(), indent=2, allow_nan=False) + "\n"
    if parser.parse_args().check:
        if TARGET.read_text(encoding="utf-8") != content:
            raise SystemExit("Sierra Leone projection is stale")
    else:
        TARGET.write_text(content, encoding="utf-8", newline="\n")
