"""Verify public US sources and export only selected contract and trial aggregates."""

import argparse
import csv
from hashlib import sha256
from io import BytesIO, StringIO
import json
from pathlib import Path
import re
from statistics import median, quantiles
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/manifests/us_evidence_v1.json"
OUTPUT = ROOT / "web/src/us-evidence.json"


def verified(data: bytes, pin: dict) -> bytes:
    if len(data) != pin["bytes"] or sha256(data).hexdigest() != pin["sha256"]:
        raise ValueError("Unexpected US source size or hash")
    return data


def contract_measures(archive: bytes, manifest: dict) -> dict:
    with ZipFile(BytesIO(archive)) as release:
        pin = manifest["measure_table"]
        if release.getinfo(pin["name"]).file_size != pin["bytes"]:
            raise ValueError("Unexpected measure table size")
        raw = verified(release.read(pin["name"]), pin)
    rows = list(csv.reader(StringIO(raw.decode("cp1252", errors="replace"))))
    if rows[1][:2] != ["CONTRACT_ID", "Organization Type"]:
        raise ValueError("Unexpected CMS table schema")
    selected = [row for row in rows[4:] if row[1].strip() in {"Local CCP", "Regional CCP"}]
    ids = {row[0].strip() for row in selected}
    if len(ids) != len(selected) or not all(re.fullmatch(r"[HR]\d{4}", key) for key in ids):
        raise ValueError("Unexpected Medicare Advantage contract keys")
    measures = []
    for spec in manifest["measures"]:
        index = rows[2].index(f"{spec['id']}: {spec['name']}")
        pattern = r"\d{1,3}%" if spec["unit"] == "%" else r"\d{1,3}"
        valid = [int(value.rstrip("%")) for row in selected
                 if re.fullmatch(pattern, value := row[index].strip())]
        if len(valid) < 11 or any(value > 100 for value in valid):
            raise ValueError("Unsupported or disclosure-sensitive CMS measure")
        lower, _, upper = quantiles(valid, method="inclusive")
        measures.append({**spec, "reported": len(valid), "median": median(valid), "iqr": [lower, upper]})
    return {"ratingsYear": manifest["ratings_year"], "contracts": len(selected), "measures": measures}


def vaccination_trial(record: dict) -> dict:
    protocol = record["protocolSection"]
    study = protocol["identificationModule"]["nctId"]
    outcome = record["resultsSection"]["outcomeMeasuresModule"]["outcomeMeasures"][0]
    if (study, outcome["type"], outcome["timeFrame"], outcome["title"]) != (
        "NCT05525494", "PRIMARY", "6 months", "Number of Participants With Annual Influenza Vaccine Among Index Patients",
    ):
        raise ValueError("Unexpected outcome definition")
    counts = {row["groupId"]: int(row["value"]) for row in outcome["classes"][0]["categories"][0]["measurements"]}
    totals = {row["groupId"]: int(row["value"]) for row in outcome["denoms"][0]["counts"]}
    arms = {"Text": ("OG000", "OG001"), "Portal": ("OG002", "OG003", "OG004", "OG005"), "Control": ("OG006",)}
    if set(counts) != {key for keys in arms.values() for key in keys} or set(counts) != set(totals):
        raise ValueError("Unexpected trial arm coverage")
    if any(not 11 <= counts[key] <= totals[key] - 11 for key in counts):
        raise ValueError("Unexpected or disclosure-sensitive trial counts")
    summary: dict[str, dict[str, int | float | list[float]]] = {}
    for arm, keys in arms.items():
        complete = sum(counts[key] for key in keys)
        total = sum(totals[key] for key in keys)
        summary[arm] = {"n": total, "vaccinated": complete, "rate": round(100 * complete / total, 2)}
    for arm in ("Text", "Portal"):
        ids = set(arms[arm] + arms["Control"])
        comparison, = (item for item in outcome["analyses"] if set(item["groupIds"]) == ids)
        summary[arm]["adjustedRR"] = float(comparison["paramValue"])
        summary[arm]["ci"] = [float(comparison["ciLowerLimit"]), float(comparison["ciUpperLimit"])]
    return {"id": study, "registryPosted": protocol["statusModule"]["lastUpdatePostDateStruct"]["date"],
            "window": outcome["timeFrame"], "arms": summary}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=ROOT / ".cache/us-evidence")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_bytes())
    if args.check and not (args.cache / "cms.zip").exists():
        # CI needs no external payloads. Verify the reviewed projection against its independent pin.
        verified(OUTPUT.read_bytes(), manifest["projection"])
        return
    cms = verified((args.cache / "cms.zip").read_bytes(), manifest["cms_zip"])
    registry = verified((args.cache / "NCT05525494.json").read_bytes(), manifest["registry"])
    data = contract_measures(cms, manifest)
    data["influenzaTrial"] = vaccination_trial(json.loads(registry))
    data["screeningTrial"] = manifest["score_table_2"]
    encoded = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode()
    if args.check:
        verified(encoded, manifest["projection"])
        if OUTPUT.read_bytes() != encoded:
            raise ValueError("US public projection differs from its verified source data")
    else:
        OUTPUT.write_bytes(encoded)


if __name__ == "__main__":
    main()
