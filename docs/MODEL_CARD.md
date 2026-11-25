# Model card

The experimental Python subgroup learner estimates each fictional band's treated and control response rate with add-one smoothing. It ranks the band effects and freezes fractional outreach probabilities at 20% expected capacity using declared population shares. The independent holdout estimates the effect of each fixed policy versus uniform through paired AIPW with known assignment probability.

## Haryana community model

The ridge T-learner uses three pretreatment village features with a penalty of 10 and train-only standardization. It fits separate models for no ambassador and information-hub assignment, then ranks the prediction difference. The reference policies include uniform allocation, low baseline take-up and low predicted control count. The eligible study subset, uncertainty and alternatives are in the [Haryana model and data report](HARYANA_RESEARCH.md).

The PHC holdout has 42 villages. Validation did not establish a gain over uniform or calibrate the intervals for every tested sample-generating process. The outcome is camp-recorded village vaccination volume. The model stays local and the application serves reviewed aggregates.

## Sierra Leone village models

The T- and DR-learners rank villages for assignment to the pooled mobile vaccination package. Fit uses five pretreatment features, ridge penalty 10 and whole triplets. The DR learner uses five training-only triplet folds to construct its regression target. Twenty distinct triplets evaluate the frozen policies at 50% expected village capacity. Both models have inconclusive gains over uniform. Low baseline uptake and low predicted uptake under control provide simpler comparators. Model parameters and village rankings remain private. The internal analysis provides no evidence of temporal performance or patient-specific benefit. [Feature contract and model report](SIERRA_LEONE_RESEARCH.md)

## Trial extraction and US planning

The extraction experiment compares structured registry fields, deterministic PDF text parsing and local Qwen2.5 7B with evidence corroboration. Inputs are public protocol pages pinned by hash and outputs are an enumerated field value, a source locator or an abstention. Single-reviewer labels and page-conditioned retrieval limit the reported error rates. The application uses reviewed evidence summaries. [Evaluation and source pins](AI_EVALUATION.md)

US gap planning uses fixed-denominator arithmetic with rounded CMS contract averages as references and hypothetical member counts and contact costs. No US patient model has been trained or validated. When available, a compatible prospectively randomized study could support patient policy performance and fairness evaluation. [US payer evidence](US_PAYER_EVIDENCE.md) · [Fairness considerations](FAIRNESS.md)
