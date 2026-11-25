"""Evaluate extraction paths on frozen, single-reviewer public protocol annotations."""

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import re
from statistics import median
from time import perf_counter
from urllib.request import urlopen

from patient_outreach.trial_intelligence import (
    LOCAL_MODEL, MAX_TEXT, REGISTRY, extract_fact, local_proposal, registry_facts, verify_candidate,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/manifests/document_holdout.json"
PDF_URL = "https://cdn.clinicaltrials.gov/large-docs/"
MODEL_ID = "65ec06548149"
TAG_URL = "http://127.0.0.1:11434/api/tags"
WINDOW = re.compile(r"(?:(?:up to|within) )?(\d+ (?:days?|weeks?|months?|years?))(?: (?:after|of|from) .+)?",
                    re.IGNORECASE)


def source_bytes(path: Path, url: str, cap: int, digest: str, fetch: bool) -> bytes:
    if path.is_file():
        content = path.read_bytes()
    elif fetch:
        with urlopen(url, timeout=35) as source:
            content = source.read(cap + 1)
    else:
        raise ValueError(f"Source missing from cache: {path.name}")
    if not 0 < len(content) <= cap or sha256(content).hexdigest() != digest:
        raise ValueError(f"Frozen source differs: {path.name}")
    if fetch and not path.exists():
        path.write_bytes(content)
    return content


def registry_window(record: dict) -> str | None:
    paths = registry_facts(record["protocolSection"]["identificationModule"]["nctId"], record)
    facts = paths["primary_outcomes"]
    if not facts or not isinstance(facts.value, list) or len(facts.value) != 1:
        return None
    time_frame = facts.value[0].get("timeFrame", "")
    window = WINDOW.fullmatch(time_frame.strip())
    if not window:
        return None
    value = window.group(1).lower()
    return str(int(value.split()[0]) * 12) + " months" if value.endswith(("year", "years")) else value


def evaluate(manifest: dict, cache: Path, fetch: bool, use_model: bool) -> dict:
    from io import BytesIO
    from pypdf import PdfReader, __version__ as pdf_version

    if use_model:
        with urlopen(TAG_URL, timeout=5) as response:
            local_models = json.load(response)["models"]
        if not any(m["name"] == LOCAL_MODEL and m["digest"].startswith(MODEL_ID) for m in local_models):
            raise ValueError("Pinned local model digest is not available.")
    cache.mkdir(parents=True, exist_ok=True)
    results = []
    for trial in manifest["trials"]:
        identifier, filename = trial["id"], trial["filename"]
        if not re.fullmatch(r"NCT\d{8}", identifier) or not re.fullmatch(r"Prot[A-Z_]*_\d{3}\.pdf", filename):
            raise ValueError("Invalid frozen source locator.")
        record = json.loads(source_bytes(cache / (identifier + ".json"), REGISTRY + identifier,
                                         3_000_000, trial["registry_sha256"], fetch))
        pdf = source_bytes(cache / (identifier + ".pdf"), f"{PDF_URL}{identifier[-2:]}/{identifier}/{filename}",
                           30_000_000, trial["pdf_sha256"], fetch)
        reader = PdfReader(BytesIO(pdf))
        for check in trial["checks"]:
            field = check["field"]
            sections = {f"page {i}": " ".join((reader.pages[i - 1].extract_text() or "").split())
                        for i in check["pages"]}
            if len(json.dumps(sections, ensure_ascii=False)) > MAX_TEXT:
                raise ValueError(f"Frozen document pages exceed the context budget: {identifier}")
            started = perf_counter()
            structured = registry_window(record) if field == "primary_window" else None
            registry_seconds = perf_counter() - started
            started = perf_counter()
            regex = extract_fact(field, sections)
            local = {
                "registry": {"value": structured, "evidence": structured is not None, "schema": True,
                             "seconds": registry_seconds},
                "deterministic": {"value": regex.value if regex else None, "evidence": regex is not None,
                                  "schema": True, "seconds": perf_counter() - started},
            }
            if use_model:
                candidate, elapsed = local_proposal(field, sections, keep_alive="10m")
                value = candidate["value"] if candidate else None
                exact_span = bool(candidate and candidate["source"] in sections
                                  and candidate["quote"] in sections[candidate["source"]])
                verified = verify_candidate(field, sections, candidate)
                local["local_model"] = {"value": value, "evidence": exact_span, "schema": candidate is not None,
                                        "seconds": elapsed}
                local["verified_model"] = {
                    "value": verified.value if verified else None, "evidence": verified is not None,
                    "schema": candidate is not None, "seconds": elapsed,
                }
            results.append({"id": identifier, "field": field, "expected": check["expected"], "methods": local})
    scores = defaultdict(Counter)
    timings = defaultdict(list)
    for case in results:
        expected = case["expected"]
        for method, output in case["methods"].items():
            value = output["value"]
            tally = scores[method]
            tally["cases"] += 1
            tally["schema_valid"] += output["schema"]
            tally["scorable"] += expected is not None
            tally["exact_on_scorable"] += expected is not None and value == expected
            tally["abstention_cases"] += expected is None
            tally["correct_abstentions"] += expected is None and value is None and output["schema"]
            tally["value_on_abstention_case"] += expected is None and value is not None
            tally["incorrect_populated"] += value is not None and value != expected
            tally["missing_evidence"] += value is not None and not output["evidence"]
            timings[method].append(output["seconds"])
            output["seconds"] = round(output["seconds"], 4)
    for method, summary in scores.items():
        summary["median_seconds"] = round(median(timings[method]), 4)
        summary["max_seconds"] = round(max(timings[method]), 4)
    return {"manifest_version": manifest["version"], "trials": len(manifest["trials"]), "pypdf": pdf_version,
            "model": {"tag": LOCAL_MODEL, "digest_prefix": MODEL_ID} if use_model else None,
            "scores": dict(scores), "results": results}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=ROOT / ".cache/benchmark")
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--model", action="store_true")
    args = parser.parse_args()
    manifest = MANIFEST.read_bytes()
    report = evaluate(json.loads(manifest), args.cache, args.fetch, args.model)
    report["manifest_sha256"] = sha256(manifest).hexdigest()
    runtime = {name: round(values["median_seconds"], 4) for name, values in report["scores"].items()}
    print(json.dumps({**report, "median_seconds": runtime}, indent=2))


if __name__ == "__main__":
    main()
