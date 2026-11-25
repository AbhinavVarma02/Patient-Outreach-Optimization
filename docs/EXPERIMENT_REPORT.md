# Experiment report

## Frozen fictional policy comparison

In the seeded fictional holdout, 10,000 generated records were used for training and an independently seeded 40,000 for evaluation. All rules offered an expected 20% capacity in the generating population. Clinical and behavioral risk selected the same band in this run. Their gain estimate over uniform was +0.084 percentage points (95% CI −0.219 to +0.387). The subgroup cell-means rule had an estimated −0.049 points (95% CI −0.274 to +0.177). None of the non-uniform comparisons excluded zero. These results belong only to the generated scenario. Different ranking, sampling variation and unobserved individual counterfactuals affect the interpretation. [Run artifact](../research/reports/fictional_policy_holdout.json)

## Known-truth estimator validation

Across six generating scenarios and 1,500 replications each, empirical coverage ranged from 93.9% to 95.4%. The null rejection point estimate was 5.8%. A Wilson Monte Carlo interval includes 5%, so the observed estimate does not demonstrate a departure from nominal size, and it exceeds the review's older 5% point cutoff. See [Model validation](MODEL_VALIDATION.md).

## Haryana Figure 4 replication

The independent population-weighted regression reproduced the published information-hub estimate of 1.89 additional measles vaccinations per village-month and the pure-control mean of 7.32. The unrounded results were 1.89233 and 7.31977. All 7,370 eligible village-month records entered the regression, spanning 617 health sub-centers. The pure-control mean used 566 village-months. The estimates are counts in this trial setting. [Banerjee et al., Figure 4](https://onlinelibrary.wiley.com/doi/10.3982/ECTA19739) · [Locked specification](../research/DATASET_FEASIBILITY.md#first-replication-check)

Statsmodels WLS and its uncorrected cluster covariance agreed with the coefficient and sub-center CR0 standard error to an absolute tolerance of `1e-10`. This checks numerical implementation. Design-based uncertainty, the authors’ interval and the assignment hierarchy still require reconciliation before policy analysis. [Statsmodels reference](https://www.statsmodels.org/stable/generated/statsmodels.stats.sandwich_covariance.cov_cluster.html) · [Run artifact](../research/reports/haryana_figure4_replication.json)

Reproduce from the project root with Python 3.13, NumPy 2.4.2 and the licensed archive and checksums in the feasibility review. The optional reference check uses statsmodels 0.14.6. The command emits aggregate JSON to standard output and rejects a different archive before parsing data.

```powershell
python scripts/replicate_haryana.py data/private/zenodo-11392582/replication-package.zip --check-reference
```
