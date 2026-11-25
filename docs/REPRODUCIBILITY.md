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

## US evidence and the final research checks

Save the CMS Star Ratings ZIP and the UCLA registry JSON to ignored `.cache/us-evidence` as `cms.zip` and `NCT05525494.json`. Exact URLs, byte sizes and SHA-256 hashes are in the [US source manifest](../research/manifests/us_evidence_v1.json). The exporter reads one named CSV from the ZIP and the posted primary summary from the registry. It does not extract the archive. Compare the SCORE Table 2 transcription and the CMS technical-note averages with the sources before a future release. CI checks the approved projection hash without downloading external datasets.

```powershell
python scripts/export_us_evidence.py --check
python scripts/audit_sierra_leone_lottery.py
python -m patient_outreach.document_evaluation --final-cycle --model qwen2.5:latest
python -m patient_outreach.document_evaluation --final-cycle --holdout --manifest research/manifests/document_holdout_v3.json --cache .cache/document-holdout-v3 --model qwen2.5:latest
```

Run the lottery audit with the Sierra Leone requirements and four original cached files listed above. For the final extraction holdout, save official PDFs and study API snapshots under the manifest's NCT identifiers in the ignored cache. Reuse the identical prior model, pypdf and local runtime. A later registry update can change bytes, so preserve or recover the dated verified snapshot. The original v2 extraction code and its run environment are identified by the earlier freeze commit, with labels preserved in the prior manifest.

## Final offline replay

Install the Sierra Leone numerical pins and `pypdf==7.1.1`, or use the equivalent `uv` environment. Prepare the approved local inputs listed above. Full Git history is needed for the original Haryana provenance pins. The runner does no network acquisition and does not invoke model generation.

```sh
uv run --no-project --with-requirements research/sierra-leone-requirements.txt --with pypdf==7.1.1 python scripts/reproduce.py
python scripts/reproduce.py fictional
python scripts/reproduce.py --help
```

The command supports `fictional`, `haryana`, `sierra-leone`, `community`, `us` and `documents` as independently runnable groups. The fixture group uses the standard library. Each run writes a new ignored directory with stage digests, byte sizes and wall times. Failure stops the run at the first mismatch and leaves the last completed stage ledger. Rerun the affected group after resolving the cause. The artifact exporters run in check mode. Model artifacts remain under the existing ignored private locations. The Sierra Leone run checks stored freezes before evaluation. The Haryana replay checks the original source and protocol digests from `dad2575`, then compares the current result to the archived numerical outputs. Historical runtime and private model metadata can vary. Finite numerical comparisons use absolute tolerance `1e-10` or relative tolerance `1e-9`, like-for-like methods and identical inputs. Document replay checks deterministic score counts and source pins, excluding timings and the historical local model path.

The measured full run used Python 3.12.12 and one OpenBLAS thread on the existing Windows host. It completed all 14 stages in 25.85 s. At 50 ms sampling, the largest worker peaked at about 265 MiB RSS for community-inference validation. This is observed resident memory for a single worker and sampled peak, with no inference model, downloads or installation included. [Replay timings and artifact hashes](../research/reports/final_reproduction.json)
