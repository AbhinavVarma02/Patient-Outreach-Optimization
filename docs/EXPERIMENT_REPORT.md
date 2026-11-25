# Experiment report

## Frozen fictional policy comparison

In the seeded fictional holdout, 10,000 generated records were used for training and an independently seeded 40,000 for evaluation. All rules offered an expected 20% capacity in the generating population. Clinical and behavioral risk selected the same band in this run. Their gain estimate over uniform was +0.084 percentage points (95% CI −0.219 to +0.387). The subgroup cell-means rule had an estimated −0.049 points (95% CI −0.274 to +0.177). None of the non-uniform comparisons excluded zero. These results belong only to the generated scenario. Different ranking, sampling variation and unobserved individual counterfactuals affect the interpretation. [Run artifact](../research/reports/fictional_policy_holdout.json)

## Known-truth estimator validation

Across six generating scenarios and 1,500 replications each, empirical coverage ranged from 93.9% to 95.4%. The null rejection point estimate was 5.8%. A Wilson Monte Carlo interval includes 5%, so the observed estimate does not demonstrate a departure from nominal size, and it exceeds the review's older 5% point cutoff. See [Model validation](MODEL_VALIDATION.md).
