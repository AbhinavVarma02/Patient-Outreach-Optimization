# Portfolio walkthrough

## One-minute demo

Open Outreach Planner and choose Annual Flu Vaccine. With the default hypothetical plan, the CMS reference leaves a 400-completion gap and the budget permits 2,400 contacts. The campaign would need a 16.67 pp incremental completion rate. Toggle to colorectal screening and show how the observed reference changes the required lift. In Evidence & Methods, compare UCLA's null-compatible reminder result with SCORE's mailed screening bundle. End on Pilot Designer to show how a small population effect can require a large sample.

## Technical questions

- Why use an RCT? Known assignment probabilities support estimation of arm contrasts under the randomized design. Trial population, estimand and post-assignment missingness still matter.
- Why freeze policy thresholds? Selecting an apparently superior rule using the same outcomes that evaluate it distorts reported intervals.
- Why can the pilot require many participants? A targeted policy can improve individual outreach yield while shifting the all-eligible outcome rate by only a fraction of a percentage point.
- Why use the CMS reference? It gives the planner a measured contract-level benchmark. A payer supplies its own hypothetical denominator, usual-care completions, reach and cost. The tool solves for a minimum required effect without estimating it.
- Why did the extractor stay experimental? The final 12-trial holdout gave the strongest deterministic method 7/13 exact values and the verified local model 2/13. Retrieval found the relevant anchors in the supplied pages, but source attribution and ambiguous endpoint or unit interpretation remained difficult.
- Why hold the Sierra Leone structure policy? In five villages the released nonperipheral roster fails a simple lottery-cap reconstruction. Matching the cap elsewhere does not confirm the original denominator or isolate spillover.

## Portfolio description

Built an open-source preventive outreach workspace for payer quality teams. It combines CMS contract benchmarks, reviewed US randomized trial evidence, study-level international replications and browser-local campaign and pilot planning. The research documents where community policy models and automated trial extraction failed their evaluation criteria.

## Resume bullets

- Built a TypeScript Medicare Advantage outreach planner using four audited CMS measures from 675 coordinated care contracts, with separate randomized evidence and browser-local budget, reach and pilot calculations.
- Reproduced five published Sierra Leone vaccination estimates and standard errors. Evaluated frozen causal models on 20 held-out village triplets and found no reliable gain over uniform outreach.

## Continuation talking points

- Reproduced a published community immunization contrast across 902 villages, checked variance independently, and compared frozen outreach policies on 19 held-out primary health centers. The sensitivity analysis explains why the apparent precision depends on analysis choices.
- Built a frozen assessment on 30 public trial protocols with registry, deterministic, local model and verified extraction paths. Evidence verification avoided unsupported fills on designated abstention cases and its coverage did not justify deployment.

In a demo, open Evidence & Methods and show how the Haryana interval changes when clustering is widened. Walk through the matched village comparison and its interference assumptions. Then select Patient Targeting and change the fictional effect pattern to show how capacity and ranking interact. Close by showing the prospective sample-size result and its assumed design.
