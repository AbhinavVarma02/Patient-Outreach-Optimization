# Technical guide

The project evaluates whether outreach decisions should rely on clinical risk, expected benefit or a simpler uniform policy. A risk score forecasts an outcome. A causal policy needs evidence about the difference induced by an assigned action. The pilot tool sizes a prospective experiment in which participants are randomized to two policies and capacity is matched across arms.

1. Read the [literature](../research/LITERATURE_REVIEW.md), [study cards](DATA_CARD.md) and [protocol](RESEARCH_PROTOCOL.md) for population, endpoint and estimand choices.
2. Check [licensing](LICENSING.md) before acquisition. Use the pinned public-metadata check whenever preparing a replication run.
3. Run [reproducibility commands](REPRODUCIBILITY.md) to evaluate estimators and frozen policies on fictional known truth.
4. Review [model validation](MODEL_VALIDATION.md) and [document extraction evaluation](AI_EVALUATION.md) before interpreting the reports.
5. Use the [architecture](ARCHITECTURE.md), [UI](UI_DESIGN.md) and [release safety](PUBLICATION_POLICY.md) guides to build and deploy the reviewed static artifact.

Known-propensity AIPW uses independent nuisance models and paired scores to compare fixed policies on the same outcomes. A richer causal forest or network would require defensible feature sets, sufficient real data and model-selection safeguards. Fractional ties preserve expected matched capacity. The planner uses direct arithmetic to find feasible single-channel allocations because the objective and constraints are separable within each candidate. Treatment mixtures and eligibility-specific effects need additional design support.

## Empirical pipeline

The [Haryana track](HARYANA_RESEARCH.md) starts with a verifiable deposit and a pretreatment feature contract. It validates a one-hot assignment within each intervention domain, nests village assignments in health sub-centers and PHCs, and gates downstream analysis on two published reference numbers. The policy experiment fits ridge per treatment on 14 whole training PHCs, freezes the fit and ranks a disjoint roster. Paired augmented scores reuse the documented conditional block lottery. Cluster sensitivity, a fixed-roster calibration and a conditional sharp-null test expose limitations of the small test sample. A separate export script reduces the experiment to selected rounded aggregates. [Architecture](ARCHITECTURE.md) · [Protocol](../research/HARYANA_PROTOCOL.md)

The [document benchmark](AI_EVALUATION.md) compares exact scorable labels and abstention across registry metadata, deterministic PDF text parsing, installed local inference and an evidence verifier on the same pinned inputs. Local generation only improves a feature when the returned data are demonstrably supported and useful. The benchmark did not meet this standard.

The [experiment report](EXPERIMENT_REPORT.md) includes a fictional null comparison. [Limitations](LIMITATIONS.md) describe unresolved scientific gates. [Deployment](DEPLOYMENT.md) covers static hosting and rollback.
