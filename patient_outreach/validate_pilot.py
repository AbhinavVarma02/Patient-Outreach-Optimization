"""Monte Carlo check of the prospective two-policy power calculation."""
import json
from math import sqrt
from random import Random
from statistics import NormalDist

from .power import Pilot
from .validate import wilson


def evaluate() -> dict:
    rng = Random(20261124)
    scenarios = [
        Pilot(.315, .026, .20, 2, .7, .50, .05),
        Pilot(.315, .026, .20, 2, .7, .75, .05),
        Pilot(.315, .026, .20, 2, 0, .50, .05),
    ]
    reps = 5000
    results = []
    for pilot in scenarios:
        control, treated = pilot.rates()
        n = pilot.enrollment(.8) or 10000
        n1 = round(n * pilot.allocation)
        n0 = n - n1
        z = NormalDist().inv_cdf(1-pilot.alpha/2)
        rejects = 0
        for _ in range(reps):
            rate0 = rng.binomialvariate(n0, control) / n0
            rate1 = rng.binomialvariate(n1, treated) / n1
            se = sqrt(rate0*(1-rate0)/n0 + rate1*(1-rate1)/n1)
            rejects += abs(rate1-rate0) > z*se
        interval = wilson(rejects, reps)
        power = pilot.power(n)
        results.append({"n": n, "allocation": pilot.allocation, "gain": treated-control, "analytic": power,
                        "empirical": rejects/reps, "wilson_interval": interval,
                        "analytic_inside_interval": interval[0] <= power <= interval[1]})
    return {"seed": 20261124, "replicates": reps, "kind": "independent_binary_policy_trial", "results": results}


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
