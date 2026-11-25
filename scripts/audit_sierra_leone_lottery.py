"""Check whether released structure rosters reconstruct the published visit lottery."""

import argparse
import json
from pathlib import Path

import pandas as pd

from replicate_sierra_leone import DEFAULT_CACHE, load


def summarize(frame: pd.DataFrame) -> dict:
    keys = ["community_code", "structure_id"]
    units = frame.dropna(subset=keys).groupby(keys).dtd_treatment.agg(["nunique", "first"])
    if units["nunique"].ne(1).any() or not units["first"].isin([0, 1]).all():
        raise ValueError("Unresolved assignment within a released structure")
    counts = pd.crosstab(units.index.get_level_values("community_code"), units["first"])
    if len(counts) != 50 or not {0, 1} <= set(counts.columns):
        raise ValueError("Unexpected door-to-door village or assignment coverage")
    size = counts[0] + counts[1]
    return {"structures": int(size.sum()), "matches_minimum_of_cap_and_roster": int(counts[1].eq(size.clip(upper=20)).sum()),
            "villages_with_both_arms": int((counts[0].gt(0) & counts[1].gt(0)).sum()),
            "observed_assignments_exceed_cap": bool(counts[1].gt(20).any())}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    args = parser.parse_args()
    _, people = load(args.cache)
    census = people.loc[people.treatment.eq(1) & people.in_census.eq(1)]
    retained = census.loc[census.periphery.eq(0)]
    remote = census.loc[census.periphery.eq(1)]
    result = {
        "release": "Harvard Dataverse V1",
        "unit": "residential structure nested in village",
        "roster_checks": {
            "all_census_structures": summarize(census),
            "nonperipheral_census_structures": summarize(retained),
            "add_unknown_periphery": summarize(census.loc[~census.periphery.eq(1)]),
            "adult_analysis_structures": summarize(retained.loc[retained.above18.eq(1)]),
        },
        "remote_exclusion_reference_reproduced": bool(
            remote.loc[remote.age.ge(12) & ~remote.dtd.eq(1)].structure_id.nunique() == 10
            and len(remote.loc[remote.age.ge(12) & ~remote.dtd.eq(1)]) == 40
        ),
        "documented_preassignment_roster_in_deposit": False,
        "decision": "Lottery denominators and propensities remain unresolved. No new structure policy estimates.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
