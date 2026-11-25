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

## Repair and independent evaluation

The previous verified path was a failed release gate. Its narrow regex required near-literal field-label wording and recognized four assignment units. Combined with the model's free-text reconstruction of exact quotes, verification had two independent ways to discard a correct proposal. Long preselected pages also contain distractors such as eligibility, sampling, blocking and unrelated trial discussion. We compared plain and layout-preserving PDF reading, added bounded field-specific context retrieval, expanded deterministic patterns and used an output schema with enumerated values and numbered source spans. The hybrid still requires full-context and local-span agreement with the deterministic parser. This improves precision at the cost of coverage. The design does not resolve text-free PDF pages or all mixed trial designs.

On the original 30 scorable development fields, both improved PDF parsers matched 23, the 7B Qwen2.5 matched 15 and the 3B Llama 3.2 matched 11. Their verified paths matched 10 and 8 respectively. An earlier Qwen development run produced 16 exact raw values and 11 verified, so reruns can differ despite fixed sampling settings. Plain reading matched layout mode on accuracy with lower median preprocessing-plus-parser latency. Qwen and Llama added no coverage to the parser. Llama's quantized weights occupy 2.02 GB on disk. [Development runs](../research/reports/document_development_v2.json) · [Qwen Apache-2.0 model card](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) · [Llama community-license model card](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)

Freeze `9b9f637` locked 30 disjoint source trials, 39 checks, page locators, short supporting anchors and the extractor before final scoring. One annotator reviewed the pages. The original gate remains at least 90% exact match and zero populated abstention cases. The evaluation covers two design fields under a page-conditioned task. It does not measure full-document retrieval, OCR or independent reviewer agreement.

| Method | Exact / 30 | Evidence correct | Populated / 39 | Correct abstention / 9 | Unsupported populated | Schema valid / 39 | Median / maximum seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Registry | 2 | 2 | 4 | 7 | 2 | 39 | <0.001 / <0.001 |
| PDF plain parser | 14 | 9 | 14 | 9 | 5 | 39 | 0.043 / 0.102 |
| PDF layout parser | 14 | 9 | 14 | 9 | 5 | 39 | 0.085 / 1.215 |
| Qwen2.5 7B | 7 | 7 | 12 | 7 | 5 | 37 | 0.481 / 5.315 |
| Qwen2.5 7B with corroboration | 3 | 3 | 3 | 9 | 0 | 37 | 0.481 / 5.315 |

The deterministic parser correctly abstained on all designated cases but left many scorable fields blank. Examples include dyads and counties, which were outside the development vocabulary, and cues separated by modifiers or written-out durations. Five exact parser values did not meet the separate span-anchor scoring criterion. That conservative criterion can also miss another supporting phrase. The constrained 7B model returned two schema-invalid outputs and populated two designated abstention cases. Agreement checks removed unsupported values while reducing exact recovery. Model timings include the loopback API and occasional model loading. Qwen's quantized weights occupied 4.68 GB on disk and the Ollama runner reported 4.8 GB allocated on a local GPU with 4,096 context tokens. Runtime depends on comparable hardware. All methods failed the accuracy threshold. Reviewed summaries remain the production path and the evidence page displays the measured outcome. [Protocol](../research/DOCUMENT_EVALUATION_PROTOCOL.md) · [Frozen holdout](../research/manifests/document_holdout_v2.json) · [Full evaluation](../research/reports/document_holdout_v2.json)
