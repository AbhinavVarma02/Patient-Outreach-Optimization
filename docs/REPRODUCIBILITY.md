# Reproducibility

Use Python 3.12+ and Node 24+. The core fictional suite uses the standard library. Use Python 3.13 with the pinned numerical requirements for Haryana and pypdf 7.1.1 to rerun the document benchmark. Build dependencies are locked in web/package-lock.json.

```sh
python -m unittest discover -s tests -v
python -m patient_outreach
python -m patient_outreach.acquisition
python -m patient_outreach.validate --reps 1500 --n 700 --seed 20261124
python -m patient_outreach.fictional --seed 20261124 --train 10000 --test 40000
cd web
npm ci --ignore-scripts
npm test
npm run build
npm run release:check
npx playwright install
npm run test:browser
```

The acquisition command without flags verifies public metadata only. No permission record is supplied. The publication build and CI read no participant records. Browser and Python calculations use a normal approximation. Their source implementations can be checked independently with a known fixture.

## Community evidence

Extract no files from the [pinned deposit](https://zenodo.org/records/11392582). Save the archive to ignored local storage. The script checks the archive and both required members before parsing. It writes an atomic versioned report and a separate private ridge artifact whose digest is listed in the report. Re-running the command from the root restores the public aggregate and the private model without serializing any row output.

```powershell
python -m pip install -r research/haryana-requirements.txt
$env:OPENBLAS_NUM_THREADS = '1'
python scripts/evaluate_haryana.py data/private/zenodo-11392582/replication-package.zip --check-reference --report research/reports/haryana_empirical.json
python scripts/validate_haryana.py
python scripts/export_haryana.py --check
```

Use `python scripts/export_haryana.py` after reviewing an intentional update to the aggregate. The export schema contains only the selected Figure 4 and holdout summaries. Use explicit version updates for changes to the estimand or feature contract. Compare full-precision numerics within tolerance when toolchain or CPUs differ.

## Document benchmark

Install `pypdf==7.1.1` in the local research environment. A cache holds only public protocols and registry metadata. Exact registry bytes can change when trials are updated. The evaluator fails on changed bytes and reports the source to recover. Use stored verified snapshots to reproduce the original comparison. The committed manifest records original registry dates and digests, along with official document filenames and page locators.

```powershell
python -m patient_outreach.benchmark --fetch
python -m patient_outreach.benchmark --model
```

The second command requires a running local Ollama installation with the pinned existing Qwen2.5 1.5B digest. It evaluates the frozen cases without uploading trial materials. See [AI evaluation](AI_EVALUATION.md).

## Sierra Leone replication and frozen policies

Use the original bytes for the four files in the [versioned manifest](../research/manifests/sierra_leone_v1.json). In Dataverse request `https://dataverse.harvard.edu/api/access/datafile/{file_id}?format=original` and use the manifest's local names. The legacy `.tab` names identify Stata binaries when downloaded in original format. Keep the files in `.cache/benchmark`, or pass a separate ignored `--cache` directory. The project independently checks the pinned size and SHA-256 of every input before accessing rows. The author script is documentation. Use Python 3.13 and the pinned numerical dependencies.

```powershell
python -m pip install -r research/sierra-leone-requirements.txt
$env:OPENBLAS_NUM_THREADS = '1'
python scripts/replicate_sierra_leone.py --check-reference
python scripts/evaluate_sierra_leone.py --report research/reports/sierra_leone_policy.json
python scripts/validate_community_inference.py --haryana-archive data/private/zenodo-11392582/replication-package.zip --report research/reports/community_inference.json
python scripts/export_sierra_leone.py --check
```

The policy command writes hashed models and policies to ignored `artifacts/private/sierra-leone-v1`. Repeat runs verify the stored freeze and reproduce the aggregate output on the same toolchain. Use an explicit new ignored `--private` run directory if the same freeze cannot be reused. CI runs the synthetic inference gates without trial records. Inspect the public projection and repeat the disclosure audit after intentional aggregate updates.

## Extraction repair reproduction

Cache the 30 pinned registry snapshots and protocol PDFs under `.cache/document-holdout-v2`, named by their NCT IDs with `.json` and `.pdf` extensions. The original development cache remains `.cache/benchmark`. The new manifest identifies official PDF file names and source dates. Use `pypdf==7.1.1` and the matching installed local Ollama models. Omit `--model` for the deterministic-only paths.

```powershell
python -m patient_outreach.document_evaluation --model qwen2.5:latest
python -m patient_outreach.document_evaluation --model llama3.2:latest
python -m patient_outreach.document_evaluation --manifest research/manifests/document_holdout_v2.json --cache .cache/document-holdout-v2 --holdout --model qwen2.5:latest
```

The evaluator emits exact, evidence and timing metrics plus model and manifest digests. Local inference can vary across runs and hardware. The committed report is the evaluated snapshot. [Benchmark protocol and evidence](AI_EVALUATION.md)
