# Model validation

The validated target is a paired fixed-policy difference with known randomization and independent evaluation records. The standard error is the empirical standard deviation of the independent contrast scores divided by the square root of sample size.

The six fictional scenarios use null, homogeneous, monotonic, inverted-U, weak and strong treatment effects, unequal groups and asymmetric assignment. Empirical coverage lies within the operating band recorded in the protocol. The 5.8% simulated null rejection rate comes with Monte Carlo variation. Missing outcomes fail closed. Cluster and interference-aware inference are unverified. Oracle nuisance inputs in the repeated simulation assess the scoring and variance implementation. They do not estimate trained-model performance. The separate held-out fictional experiment uses fitted nuisance predictions.

Run evidence includes seeds, scenario counts, bias, Monte Carlo uncertainty and code checksums. [Simulation artifact](../research/reports/fictional_validation.json)

## Haryana policy and variance

The numerical check agrees with statsmodels WLS and cluster variance for both sub-center CR0 and PHC CR1. Known-answer tests verify the conditional two-arm augmented score, clustered mean variance and fractional quota ties. The 19-PHC known-truth calibration produces 92.2% null and 99.9% heterogeneous coverage under a nominal 95% cluster t procedure. In the spillover scenario the no-spillover target receives biased estimates. These checks support exploratory reporting with caveats and provide no calibrated confidence claim for deployment. [Community experiment](HARYANA_RESEARCH.md) · [Calibration artifact](../research/reports/haryana_simulation.json)

## Matched trial blocks and bounded outcomes

Exact enumeration of all three assignments and all outcome-box vertices verified the Sierra Leone weighted score and conservative triplet range. The 10,000-draw simulations include null, heterogeneous and spillover designs for Sierra Leone and Haryana. The finite-sample bounds attain 100% simulated coverage for both no-interference fixtures per design with wide intervals. Nominal t coverage varies, including 93.46% and 99.94% in the Haryana fixtures. The bounded estimator fails the no-interference target under simulated spillover. Coverage from the conservative interval alone cannot identify a target under interference. CI runs the exact check and bias and coverage gates on generated data. [Sierra Leone inference](SIERRA_LEONE_RESEARCH.md) · [Calibration and Haryana sensitivity](../research/reports/community_inference.json)
