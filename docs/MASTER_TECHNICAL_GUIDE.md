# Technical guide

The project evaluates whether outreach decisions should rely on clinical risk, expected benefit or a simpler uniform policy. A risk score forecasts an outcome. A causal policy needs evidence about the difference induced by an assigned action. The pilot tool sizes a prospective experiment in which participants are randomized to two policies and capacity is matched across arms.

1. Read the [literature](../research/LITERATURE_REVIEW.md), [study cards](DATA_CARD.md) and [protocol](RESEARCH_PROTOCOL.md) for population, endpoint and estimand choices.
2. Check [licensing](LICENSING.md) before acquisition. Use the pinned public-metadata check whenever preparing a replication run.
3. Run [reproducibility commands](REPRODUCIBILITY.md) to evaluate estimators and frozen policies on fictional known truth.
4. Review [model validation](MODEL_VALIDATION.md) and [document extraction evaluation](AI_EVALUATION.md) before interpreting the reports.
5. Use the [architecture](ARCHITECTURE.md), [UI](UI_DESIGN.md) and [release safety](PUBLICATION_POLICY.md) guides to build and deploy the reviewed static artifact.

Known-propensity AIPW uses independent nuisance models and paired scores to compare fixed policies on the same outcomes. A richer causal forest or network would require defensible feature sets, sufficient real data and model-selection safeguards. Fractional ties preserve expected matched capacity. The planner uses direct arithmetic to find feasible single-channel allocations because the objective and constraints are separable within each candidate. Treatment mixtures and eligibility-specific effects need additional design support.

The [experiment report](EXPERIMENT_REPORT.md) includes a fictional null comparison. [Limitations](LIMITATIONS.md) describe unresolved scientific gates. [Deployment](DEPLOYMENT.md) covers static hosting and rollback.
