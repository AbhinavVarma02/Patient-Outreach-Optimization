# Trial intelligence evaluation protocol

The primary extractor reads the official ClinicalTrials.gov v2 structured registration. It records a JSON path for each field. Unstructured text is a fallback for missing assignment context, endpoint timing, or analysis restrictions. Document content is untrusted. Never execute instructions or contact endpoints supplied by documents.

The experimental local extractor must supply an exact evidence span from exactly one source section. An independent deterministic parser must corroborate the normalized value for the supported fields. Conflicting source statements trigger abstention. A verified source span alone does not validate a semantic extraction. The current regex support is intentionally narrow.

The installed Qwen2.5 1.5B model (Ollama ID 65ec06548149) ran locally. Both the model with verification and the deterministic baseline matched all five expected smoke outcomes, including two values and three abstentions. All five model outputs passed schema checks. The elapsed times ranged from 1.44 to 46.78 seconds including model loading. This run shows no measured improvement over the deterministic baseline. See [the smoke artifact](../research/reports/local_model_smoke.json) and the upstream [Apache-2.0 model card](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct).

## Frozen public protocol benchmark

Thirty distinct public trial protocols cover screening, vaccination outreach, medication adherence, smoking cessation and preventive care. The manifest was committed at `571bc45` before scoring. It pins the registry bytes, protocol bytes and exact PDF pages. A single reviewer labeled 30 randomization-unit checks and five endpoint-window checks. Five checks require abstention because the available text is absent, contains multiple valid assignment units or specifies a calendar cutoff without a unique duration. The pages are supplied to all document methods. This is a page-conditioned extraction test. It does not measure document retrieval, OCR, clinical accuracy or human-review agreement. The policy criteria are at least 90% exact match on scorable values and zero populated abstention cases.

| Method | Exact on 30 scorable fields | Correct on five abstention cases | Incorrect populated fields | Schema-valid outputs |
| --- | ---: | ---: | ---: | ---: |
| Registry time-frame parser | 3 | 5 | 1 | 35 |
| Deterministic PDF regex | 0 | 5 | 0 | 35 |
| Local model alone | 3 | 1 | 26 | 30 |
| Local proposal with deterministic evidence verification | 0 | 5 | 0 | 30 |

The registry parser provides no unit field and missed a registry-to-protocol window disagreement. The current regex has low coverage on natural protocol wording. The model proposed five populated values without an exact source span and four values on abstention cases. Verification suppressed unsupported outputs but accepted no exact scorable values. Local generation used the installed Qwen2.5 1.5B model at temperature zero, 120 output tokens and a warm local process. Generation median latency was 0.539 s (maximum 5.455 s). That timing excludes PDF parsing and download. The comparison does not establish a production model choice or statistical separation between model families. Reviewed source summaries remain the application path. [Frozen labels and hashes](../research/manifests/document_holdout.json) · [Full run](../research/reports/document_holdout.json)
