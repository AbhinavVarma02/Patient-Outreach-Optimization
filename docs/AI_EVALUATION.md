# Trial intelligence evaluation protocol

## Final bounded cycle

The final experiment extended assignment-unit vocabulary, added more bounded assignment phrases and recognized written-out durations. The established plain PDF parser scored 23/30 on the original development cases. The revision scored 20/30 with four of five designated abstentions. Raw Qwen2.5 7B scored 15/30 and verified Qwen scored 11/30. Broader vocabulary did not overcome grammatical and source-scope ambiguity. [Development artifact](../research/reports/document_development_v3.json)

The extractor was frozen at `99ddcdc` and the new label manifest at `fecd677` before final scoring. The 12 source trials are disjoint from both earlier benchmarks. The registry-query sample includes a wider set of designs than US preventive care alone. One reviewer labeled 12 assignment-unit and six endpoint-window checks. There were 13 scorable values and five designated abstentions. The top 12 snippets included all 13 labeled anchors within the supplied pages. This measurement does not establish quality on full documents or scanned pages. [Frozen queries, source pins and labels](../research/manifests/document_holdout_v3.json)

| Method | Exact / 13 | Anchor-aligned exact | Correct abstention / 5 | Unsupported populated | Schema valid / 18 | Median seconds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Registry | 1 | 1 | 3 | 2 | 18 | <0.001 |
| Baseline PDF plain | 7 | 1 | 4 | 7 | 18 | 0.045 |
| Baseline PDF layout | 7 | 0 | 4 | 8 | 18 | 0.085 |
| Revised PDF plain | 6 | 4 | 4 | 3 | 18 | 0.045 |
| Qwen2.5 7B | 8 | 3 | 3 | 6 | 17 | 0.526 |
| Qwen2.5 7B plus corroboration | 2 | 1 | 4 | 1 | 17 | 0.526 |

“Unsupported” includes values whose excerpt misses the single labeled anchor. An alternative valid span can therefore fail this metric. The local model recovered some individual values missed by the parser, including a long assignment clause and a duration, but overall source alignment and structured output failed to support its use. The verified model lost coverage when agreement was required. The revised parser abstained on one protocol that used both “families” and “caregivers.” It incorrectly returned six months for another protocol where that duration covered one part of a composite feasibility endpoint. Retrieval finding the right passage leaves these interpretation questions open. [Holdout outputs and runtime details](../research/reports/document_holdout_v3.json)

The original gate stays at 90% exact on scorable fields and zero populated abstention cases. The local model did not demonstrate a dependable evidence-grounded improvement and the revised parser regressed on exact recovery. This was the final model-selection cycle for the release. The app uses reviewed source summaries. Both prior frozen benchmarks and results remain available below.

## Final architecture review

The deterministic replay recovered the committed exact counts, evidence alignment, fill rates, abstentions and schema counts from the pinned final protocol pages. It used the same labels and skipped model generation. The frozen report retains the measured model outputs. The replay introduced no new extractor or accuracy claim. [Replay command](REPRODUCIBILITY.md#final-offline-replay) · [Pinned final report](../research/reports/document_holdout_v3.json)

The postmortem examined the stored paired proposals. The corroboration stage withheld six of the eight exact raw model values. The raw model aligned three exact values with a labeled anchor, while the verified path aligned one. A lexical match can prove the snippet was present. Interpreting whether it answers the requested field still requires identifying the unit, scope and endpoint. An oracle that keeps only outputs matching the benchmark anchor uses information unavailable during deployment. Even that restriction would leave the raw model at three exact supported values. Lowering corroboration would recover some exact values and reintroduce unsupported or ambiguous fills.

Descriptive 95% Wilson intervals on the 13 scorable checks are 29.1% to 76.8% for the best rules-based exact rate, 35.5% to 82.3% for the raw 7B model and 4.3% to 42.2% for the verified model. Checks share protocols and were deliberately selected. These intervals describe the size of the measured sample and provide no population-wide accuracy guarantee. The original zero-fill rule for designated abstentions remains unchanged.

Layout reading, bounded retrieval, constrained local generation, deterministic candidates and hybrid corroboration were evaluated over the existing cycles. The review considered span question answering and compact entailment classification. Both would need field- and scope-specific development labels, examples of valid alternative spans and an independently reviewed final holdout. OCR and tables require a separate annotated stratum. Those unexecuted alternatives have no measured quality claim. The current evidence supports closing automated extraction for the release and keeping reviewed source summaries.

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
