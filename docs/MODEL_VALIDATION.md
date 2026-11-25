# Model validation

The validated target is a paired fixed-policy difference with known randomization and independent evaluation records. The standard error is the empirical standard deviation of the independent contrast scores divided by the square root of sample size.

The six fictional scenarios use null, homogeneous, monotonic, inverted-U, weak and strong treatment effects, unequal groups and asymmetric assignment. Empirical coverage lies within the operating band recorded in the protocol. The 5.8% simulated null rejection rate comes with Monte Carlo variation. Missing outcomes fail closed. Cluster and interference-aware inference are unverified. Oracle nuisance inputs in the repeated simulation assess the scoring and variance implementation. They do not estimate trained-model performance. The separate held-out fictional experiment uses fitted nuisance predictions.

Run evidence includes seeds, scenario counts, bias, Monte Carlo uncertainty and code checksums. [Simulation artifact](../research/reports/fictional_validation.json)
