# Model card

The experimental Python subgroup learner estimates each fictional band's treated and control response rate with add-one smoothing. It ranks the band effects and freezes fractional outreach probabilities at 20% expected capacity using declared population shares. The independent holdout estimates the effect of each fixed policy versus uniform through paired AIPW with known assignment probability.

## Haryana community model

The ridge T-learner uses three pretreatment village features with a penalty of 10 and train-only standardization. It fits separate models for no ambassador and information-hub assignment, then ranks the prediction difference. The reference policies include uniform allocation, low baseline take-up and low predicted control count. The eligible study subset, uncertainty and alternatives are in the [Haryana model and data report](HARYANA_RESEARCH.md).

## Sierra Leone village models

The T- and DR-learners rank villages for assignment to the pooled mobile vaccination package. Fit uses five pretreatment features, ridge penalty 10 and whole triplets. The DR learner uses five training-only triplet folds to construct its regression target. Twenty distinct triplets evaluate the frozen policies at 50% expected village capacity. Both models have inconclusive gains over uniform. Low baseline uptake and low predicted uptake under control provide simpler comparators. Model parameters and village rankings remain private. The internal analysis provides no evidence of temporal performance or patient-specific benefit. [Feature contract and model report](SIERRA_LEONE_RESEARCH.md)

The policy evaluation uses a PHC holdout with 42 villages. Validation did not establish a gain over uniform or calibrate the intervals for all plausible sample-generating processes. The model artifact stays local and the application serves reviewed numerical summaries. This model’s outcome is camp-recorded village vaccination volume. The patient-facing calculators remain fictional and provide no patient-level inference.
