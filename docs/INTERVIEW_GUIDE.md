# Portfolio walkthrough

## One-minute demo

Start on Overview and identify the published-evidence boundary. In Patient Targeting, switch between the fictional risk-effect patterns and explain why equal reach can still generate different yield. In Outreach Planner, reduce the budget and show the binding contact constraint. In Pilot Designer, reduce ranking quality and explain the change in the sample size. End on the linked Study 4 primary population and explain why descriptive cross-trial comparisons are insufficient.

## Technical questions

- Why use an RCT? Known assignment probabilities support estimation of arm contrasts under the randomized design. Trial population, estimand and post-assignment missingness still matter.
- Why freeze policy thresholds? Selecting an apparently superior rule using the same outcomes that evaluate it distorts reported intervals.
- Why can the pilot require many participants? A targeted policy can improve individual outreach yield while shifting the all-eligible outcome rate by only a fraction of a percentage point.
- Why is the local extractor experimental? Its smoke run checks exact support and abstention. The held-out multitrial evaluation is open.

## Portfolio description

Built a decision workspace for comparing preventive outreach at matched capacity and designing prospective randomized pilots. It pairs simulated causal-policy validation with a transparent evidence trail to published vaccination studies.

## Resume bullets

- Built a TypeScript workspace for matched-capacity targeting, channel costing and randomized pilot sizing, with a separate evidence trail to four published study designs.
- Implemented known-propensity AIPW and a reproducible fictional holdout and assessed coverage in six known-truth scenarios with 1,500 replications each.

## Continuation talking points

- Reproduced a published community immunization contrast across 902 villages, checked variance independently, and compared frozen outreach policies on 19 held-out primary health centers. The sensitivity analysis explains why the apparent precision depends on analysis choices.
- Built a frozen assessment on 30 public trial protocols with registry, deterministic, local model and verified extraction paths. Evidence verification avoided unsupported fills on designated abstention cases and its coverage did not justify deployment.

In a demo, open Evidence & Methods and show how the Haryana interval changes when clustering is widened. Walk through the matched village comparison and its interference assumptions. Then select Patient Targeting and change the fictional effect pattern to show how capacity and ranking interact. Close by showing the prospective sample-size result and its assumed design.
