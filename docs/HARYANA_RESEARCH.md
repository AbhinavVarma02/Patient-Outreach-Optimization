# Haryana immunization research

## Design and data card

Banerjee et al. evaluated childhood immunization in seven low-coverage districts with 140 primary health centers (PHCs) and 755 sub-centers. The paper reports 2,360 villages in the starting frame and 915 villages eligible for the ambassador experiment. Figure 4's implemented analysis contains 902 villages, 617 sub-centers and 7,370 village-months in 140 PHCs. The archive does not establish why every village in the paper's eligible frame is absent or present in the model sample. Calendar coverage ranges from December 2016 through October 2017, with 1–11 observed months across villages. Duplicate village-months, changing treatment flags, invalid counts and missing values in the three selected baseline features all fail the pipeline. A missing village-month remains missing. [Article, §§4.2–4.5](https://onlinelibrary.wiley.com/doi/10.3982/ECTA19739) · [Pinned deposit](https://zenodo.org/records/11392582)

| Domain | Assignment unit and arms | Implication |
| --- | --- | --- |
| Phone-credit incentive | PHCs were randomized within districts to eligibility or no incentive. Within eligible PHCs, sub-centers were assigned high or low flat or increasing rewards for eligible vaccinations. | PHC-level dependence matters. The overall 70/140 allocation does not establish all district-conditional probabilities or probabilities of variants. |
| Targeted reminders | Sub-centers assigned no reminders, 33% saturation or 66% saturation. Caregivers were subsequently randomized with the assigned probability after the first visit. Text and automated voice conveyed the same content. | Saturation effects are community-level. Individual receipt, direct effects and distinct voice or text effects are outside this release. Recorded delivery and eligibility are unsuitable training features. |
| Ambassadors | Eligible villages randomized within sub-centers to none, randomly selected people, information hubs, trusted people or trusted information hubs. Ambassadors were asked to relay messages. | Treat within-village diffusion as part of assignment. Between-village diffusion and shared camps threaten transport to different allocation patterns. |

The assay is the monthly count of children recorded receiving measles-1 at program camps. The records exclude children never seen and may miss vaccines received elsewhere. An increase could partly reflect substitution toward camps. The count is a proxy for schedule completion and has no consistent all-eligible-child denominator. The authors' revised analysis plan describes a November 2017 reminder interruption and the archive's first-implementation flag bounds the analysis. Later months and endline surveys cannot serve as an independent policy test. [Article, §4.4](https://onlinelibrary.wiley.com/doi/10.3982/ECTA19739) · [Authors’ revised plan in the archive](https://zenodo.org/records/11392582)

The 2016 pretreatment village survey covers household structure, education, literacy, vaccination history, caste, religion and marital status. Three inputs passed the feature contract: the village shares with a vaccination card, ever receiving measles vaccination and literacy. Exclude sensitive demographic shares, identifiers and all follow-up, cost, delivery and administrative uptake fields. Geography is used for splitting and uncertainty only. All 75 factorial bundles are represented in the retained sample, and 47 have fewer than 11 villages. Publish no sparse bundle table. The release contains no village, sub-center, PHC or individual records.

## Estimands and results

The Figure 4 coefficient is an additive, population-weighted contrast for assignment to information-hub ambassadors against assignment to no ambassador, averaging over the other randomized domains in the fitted sample. The separate pure-control mean is **7.32**. This baseline comes from villages assigned control in all three domains. Adding the coefficient to it does not identify a stand-alone ambassador policy effect. The authors' R plotting code reads the `lm_robust` CR0 confidence bounds after scaling the stored covariance without recalculating those bounds. We reproduced the coefficient and independently cross-checked the weighted coefficients and sandwich variances in statsmodels. The rounded plotted p-value is 0.04. [Figure 4 and authors’ code](https://zenodo.org/records/11392582) · [Estimatr variance conventions](https://declaredesign.org/r/estimatr/reference/lm_robust.html)

| Information-hub specification | Count difference per village-month | Nominal 95% CI |
| --- | ---: | ---: |
| Published population weighting and sub-center CR0 | +1.89 | 0.13 to 3.66 |
| Same weights with PHC CR1 | +1.89 | −0.07 to 3.86 |
| Equal village-month weights, PHC CR1 | +0.68 | −0.39 to 1.75 |
| April–October, population weights and PHC CR1 | +2.09 | −0.04 to 4.21 |

The PHC interval includes zero. With ten arm tests in the primary PHC model, the information-hub Holm-adjusted p-value is 0.53. Restricting calendar months leaves the PHC interval crossing zero. Changing weights changes the target population as well as the estimate.

The policy comparison asks how many recorded vaccinations per observed month a fixed rule would add over uniform ambassador assignment at 50% expected village capacity. It uses 73 villages in 33 sub-centers with both hub and no-ambassador observations. The training split is 31 villages in 14 PHCs. The holdout is 42 villages in 19 other PHCs, with 20 hub and 22 no-ambassador assignments. Under exchangeability within observed two-arm blocks, the retained marginal probabilities range from 1/3 to 1/2. This calculation conditions on the observed roster and arm counts. Observation by assignment, between-village spillovers or additional allocation constraints could break the identifying conditions.

| Policy vs uniform | Augmented estimate | Nominal simultaneous 95% CI | Unaugmented estimate | April–October estimate |
| --- | ---: | ---: | ---: | ---: |
| Low baseline measles take-up | +0.62 | −1.99 to 3.22 | +0.59 | +0.62 |
| Low predicted control count | +1.61 | −0.83 to 4.04 | +1.86 | +1.68 |
| Ridge T-learner ranking | +1.13 | −1.33 to 3.59 | +0.80 | +1.18 |

All three nominal intervals include zero. The 3,000-draw synthetic calibration produced 92.2% coverage under zero effects and 99.9% under the sampled heterogeneous effects. Simulated between-village spillover shifted the estimate from a no-spillover target of 0.49 to about zero. These finite-sample and interference results constrain use of the intervals. A post-run conditional Fisher test of **no assignment effect anywhere** gave adjusted p=0.044 for the low-predicted-count statistic, p=1.00 for low baseline take-up and p=0.32 for ridge. That diagnostic assumes the conditional lotteries and tests a sharp null. It does not establish a policy improvement over uniform. The comparison provides no basis for preferring the learned policy.

The follow-up bounded sensitivity capped each village's average monthly count at 25 and reused the frozen assignments, feature rules and fitted rankings. Under independent PHCs, conditional block exchangeability and no between-village interference, the Bonferroni simultaneous Hoeffding intervals were −12.58 to 13.65 for low baseline take-up, −12.10 to 15.16 for low predicted count and −12.21 to 14.32 for ridge. These intervals concern the capped count estimand. The 10,000-draw calibration showed 100% bounded coverage in the null and heterogeneous fixtures, versus 93.46% and 99.94% nominal t coverage. The wide intervals support no comparative performance claim. Simulated spillover biased the score by −0.49 counts relative to the no-spillover target. [Sensitivity specification](../research/HARYANA_PROTOCOL.md#bounded-outcome-sensitivity) · [Bounded sensitivity and simulation](../research/reports/community_inference.json)

## Supported research and deployment scope

- The observed-year, village-level assignment contrasts support replication, modest prespecified effect modification and evaluations restricted to observed overlap. The original authors published vintage-specific bundled cost and aggregate policy analyses. A current implementation would need delivery costs, scale, interference assumptions and a prospective experiment.
- The experiment provides too little matched support to justify a flexible causal forest or a 75-action optimizer here. The companion HTE publication is prior evidence on the same trial. It does not provide an external test set. No cross-period rollout performance, cost savings, household direct effect or patient benefit estimate is available from this pipeline.
- Capacity here is a share of villages offered the same ambassador intervention. If village cost varies, a fixed village quota is not a matched monetary budget. Cost-per-effect is particularly unstable when uncertainty includes zero. The USD and patient-level tools remain fictional.
- For externally verified inputs, see [alternative dataset feasibility](../research/DATASET_FEASIBILITY.md#companion-and-alternative-datasets). For the deterministic grouped split and frozen fits, see the [protocol](../research/HARYANA_PROTOCOL.md) and [reproduction commands](REPRODUCIBILITY.md).

Data from Banerjee et al., *Selecting the Most Effective Nudge: Evidence From a Large-Scale Experiment on Immunization*, Econometrica (2025), CC BY 4.0 replication deposit v2. This project independently filters, joins, models and summarizes the deposit. [Data and author attribution](https://zenodo.org/records/11392582) · [License](https://creativecommons.org/licenses/by/4.0/) · [Aggregate experiment](../research/reports/haryana_empirical.json) · [Fictional calibration](../research/reports/haryana_simulation.json)
