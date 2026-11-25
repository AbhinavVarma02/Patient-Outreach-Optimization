"""Train, freeze and independently evaluate policies on a fictional RCT."""
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
from random import Random

from .estimators import contrast_scores, summarize

SHARES = (0.25, 0.35, 0.40)
BASELINE = (0.25, 0.30, 0.35)
EFFECT = (0.012, 0.041, 0.022)
CAPACITY = 0.20
PROPENSITY = 0.5


def sample(seed: int, size: int) -> list[tuple[int, int, int]]:
    rng = Random(seed)
    groups = rng.choices(range(len(SHARES)), weights=SHARES, k=size)
    rows = []
    for group in groups:
        action = int(rng.random() < PROPENSITY)
        outcome = int(rng.random() < BASELINE[group] + action * EFFECT[group])
        rows.append((group, action, outcome))
    return rows


def allocate(score: tuple[float, ...], capacity: float) -> tuple[float, ...]:
    if not 0 <= capacity <= 1 or len(score) != len(SHARES):
        raise ValueError("Requires a valid budget and one score per group.")
    policy = [0.0] * len(SHARES)
    remaining = capacity
    for value in sorted(set(score), reverse=True):
        tied = [g for g, s in enumerate(score) if s == value]
        total_share = sum(SHARES[g] for g in tied)
        fraction = min(1.0, remaining / total_share)
        for group in tied:
            policy[group] = fraction
        remaining = max(0.0, remaining - total_share)
    return tuple(policy)


def train(rows: list[tuple[int, int, int]]) -> tuple[tuple[float, ...], tuple[float, ...]]:
    sums = [[1, 1] for _ in SHARES]
    counts = [[2, 2] for _ in SHARES]
    for group, treatment, outcome in rows:
        sums[group][treatment] += outcome
        counts[group][treatment] += 1
    return tuple(s[0]/n[0] for s,n in zip(sums,counts,strict=True)), tuple(
        s[1]/n[1] for s,n in zip(sums,counts,strict=True))


def run(seed: int, training_n: int, evaluation_n: int) -> dict:
    if min(training_n, evaluation_n) < 100:
        raise ValueError("Training and evaluation require at least 100 fictional records each.")
    m0, m1 = train(sample(seed, training_n))
    uplift = tuple(b-a for a,b in zip(m0,m1,strict=True))
    policies = {
        "uniform": (CAPACITY,) * len(SHARES),
        "clinical_risk": allocate((3,2,1), CAPACITY),
        "behavioral_risk": allocate(tuple(-value for value in m0), CAPACITY),
        "intermediate_behavioral_risk": allocate(tuple(-abs(value-0.30) for value in m0), CAPACITY),
        "subgroup_cell_means": allocate(uplift, CAPACITY),
    }
    frozen = json.dumps({"m0":m0,"m1":m1,"policies":policies}, sort_keys=True)
    # Draw the independent evaluation outcomes after all candidate rules are fixed.
    g, a, y = zip(*sample(seed+1, evaluation_n), strict=True)
    results = {}
    for policy, probabilities in policies.items():
        weights = [probabilities[group]-CAPACITY for group in g]
        estimate = summarize(contrast_scores(a,y,[PROPENSITY]*evaluation_n,weights,[m0[group] for group in g],
                                             [m1[group] for group in g]))
        truth = sum(share*(q-CAPACITY)*tau for share,q,tau in zip(SHARES,probabilities,EFFECT,strict=True))
        results[policy] = {"frozen_probabilities":probabilities,"truth_gain":truth,"estimate":asdict(estimate)}
    return {"kind":"fictional_independent_holdout","training_seed":seed,"evaluation_seed":seed+1,
            "training_rows":training_n,"evaluation_rows":evaluation_n,"capacity":CAPACITY,
            "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "frozen_policy_sha256":hashlib.sha256(frozen.encode()).hexdigest(),"frozen":json.loads(frozen),
            "results":results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20261124)
    parser.add_argument("--train", type=int, default=10000)
    parser.add_argument("--test", type=int, default=40000)
    args = parser.parse_args()
    print(json.dumps(run(args.seed,args.train,args.test),indent=2))
