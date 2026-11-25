# Limitations

- OSF published matching hash and size metadata for all 20 files. Payload bytes and participant-level data remains unverified. The repository has no evidence of permission for the intended analysis.
- Replication, clinical effect modification, clinical policy performance, temporal transport and fairness remain unassessed. Published trial comparisons apply to their original populations, assigned modalities and timeframes.
- Synthetic inference uses i.i.d. records and independently frozen rules. The toolkit has partial coverage of the requested statistical methods. Independent R-reference validation, adjusted ITT, RATE and learned-rule cross-fit variance remain pending.
- Power assumes a binary outcome, normal approximation and independent fixed strategies. The variance inflation for clustering is an approximation. Attrition is treated as a design loss.
- The planner compares single-channel strategies. It does not infer effects for untested channel bundles or treat scenario unit costs as observed cost.
- Local model accuracy was measured on five smoke cases. Held-out multitrial evaluation is pending.
