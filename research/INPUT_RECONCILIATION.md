# Research input reconciliation

The cover of the Word review reads “v0.2 (supersedes v0.1 of 24 Nov 2026).” The OOXML package revision is 24, a Word metadata field. The full review text, tables, and embedded figures were inspected from the unchanged package. The oral or written history of earlier sessions is unnecessary.

| Original under local research/source-inputs/ | SHA-256 |
| --- | --- |
| Patient Outreach Optimization Independent Review and Revised Master Plan.docx | 720bb43d063455f37882a182244e46d29d98c34165f75928babb9c4d17498a18 |
| osf_mqbux_manifest.json | 522126286b9a97b0a5f9b411feb91a27977e0d3f43478580485c97aa26de19 |
| power_sim.py | adf4e84de9f3528eecd355b4d2bdc725382e30457359083090a62d07a224990c |
| fetch_osf_data.py | 2414cec1e01503e3b90275247f213824fefb09690fc0abdfbe8378c757d33f22 |

The copied master prompt SHA-256 is `66fb8c1b5c1de5b4ca149c83bfcf5d4b220e96b2696a350e5b5e87ec734192c6`. The tracked manifest is a byte-identical copy. The source archive stays local to keep third-party content out of releases. Its hashes allow handoff and verification if supplied separately.

- The review narrowed v0.1 to three content trials, an estimator toolkit and a static report. The v1.0 contract adds Study 4 channel design, the decision workspace and trial document intelligence. The master prompt controls product scope and rights.
- Retain within-study ITT, known randomization probabilities from protocol, predeclared comparisons, sensitivity to post-randomization exclusions, temporally frozen policies where compatible, and strong simple baselines. Never infer a cluster ID from shared-address flags.
- The review's Study 2-only access assessment was secondhand. The supplied manifest pins 20 files covering all four studies, dictionaries, timing aggregates, and registry derivatives. It asserts 175,559 full and 162,917 analysis records. These are expected archive rows, potentially overlapping people. Its null license is a historical input. The UTC timestamp of November 25 corresponds to November 24 in New York. Live file verification remains outstanding.
- The original fetcher uses a 120-second per-request timeout, skips matching hashes and never executes payloads. It buffers a whole response, writes directly to the target, checks no expected size, has no retry bound or effective quarantine, and trusts the manifest-controlled paths.
- The original oracle simulation uses 3,000 replicates and seed 20261124, baseline 31.5%, mean effect 2.6 pp and allocation 3:1. It constructs two subgroups at fixed share, estimates (b) times top-group minus pooled effect, and uses the Monte Carlo standard deviation for rejection. The approximate sample size scales the SE by the square root of N. It assumes independent people and perfect score ordering. It cannot validate learned-rule selection or account for repeated participation and household interference. Its Study 2 power results are scenario-specific.
- Study 4 was the modality trial NCT05509270. NCT06566534 is a later personalization trial. The paper supplement reports 29,186 people in the three-channel-eligible analysis, distinct from the manifest's 42,709 analyzed file rows. It reports a 29-day window, six assigned arms and a date inconsistency between methods prose and the analysis/timing sections. Verify the registry and authors' data before a replication claim. The study was not a complete factorial.
