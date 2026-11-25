# Trial intelligence evaluation protocol

The primary extractor reads the official ClinicalTrials.gov v2 structured registration. It records a JSON path for each field. Unstructured text is a fallback for missing assignment context, endpoint timing, or analysis restrictions. Document content is untrusted. Never execute instructions or contact endpoints supplied by documents.

The experimental local extractor must supply an exact evidence span from exactly one source section. An independent deterministic parser must corroborate the normalized value for the supported fields. Conflicting source statements trigger abstention. A verified source span alone does not validate a semantic extraction. The current regex support is intentionally narrow.

The installed Qwen2.5 1.5B model (Ollama ID 65ec06548149) ran locally. Both the model with verification and the deterministic baseline matched all five expected smoke outcomes, including two values and three abstentions. All five model outputs passed schema checks. The elapsed times ranged from 1.44 to 46.78 seconds including model loading. This run shows no measured improvement over the deterministic baseline. See [the smoke artifact](../research/reports/local_model_smoke.json) and the upstream [Apache-2.0 model card](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct).

Before evaluating an LLM, define two pass criteria on a held-out set of about 25–30 distinct trials: at least 90% exact match on scorable field values and no unsupported fields on missing-value cases. Track schema validity, supported-field accuracy, correct abstentions and elapsed time. The included finite smoke corpus is single-reviewer and insufficient for either release criterion. The website uses reviewed published summaries.
