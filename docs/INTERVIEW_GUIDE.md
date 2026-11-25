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

## Resume bullets by role

### AI Engineer

- Built and evaluated a local trial-document pipeline that combined ClinicalTrials.gov fields, plain and layout PDF parsing, structured extraction and evidence-backed abstention.
- Benchmarked rules and a local 7B model on 12 disjoint trial protocols. The best rules matched 7 of 13 scorable fields and the verified model matched 2 of 13, so the public app retained reviewed summaries.

### Data Scientist

- Reproduced five published Sierra Leone vaccination estimates and standard errors against an independent regression implementation. The bundled mobile clinics and outreach intervention increased adult uptake by 26.1 percentage points.
- Compared fixed ridge T- and DR-learners with uniform allocation on 20 held-out village triplets at equal expected capacity. Neither learner showed a reliable gain.

### ML Engineer

- Built a CPU replay for pinned sources, grouped training, frozen policies, statistical gates and reviewed outputs. Reproduced 14 stages in 25.85 seconds with a sampled worker peak of 265 MiB RSS on Windows.
- Shipped a TypeScript payer and pilot workspace backed by four CMS measures across 675 coordinated care contracts. Verified the static release using three browser engines, an asset allowlist and HTTPS digest checks.

## Continuation talking points

- Reproduced a published community immunization contrast across 902 villages, checked variance independently, and compared frozen outreach policies on 19 held-out primary health centers. The sensitivity analysis explains why the apparent precision depends on analysis choices.
- Built a frozen assessment on 30 public trial protocols with registry, deterministic, local model and verified extraction paths. Evidence verification avoided unsupported fills on designated abstention cases and its coverage did not justify deployment.

In a demo, open Evidence & Methods and show how the Haryana interval changes when clustering is widened. Walk through the matched village comparison and its interference assumptions. Then select Patient Targeting and change the fictional effect pattern to show how capacity and ranking interact. Close by showing the prospective sample-size result and its assumed design.

## Technical walkthrough

1. Open the payer scenario. Walk through the fixed denominator, remaining gap, cost and contact limit. Separate the required gain from an estimated effect.
2. Open Sierra Leone. Explain matched triplets, the bundled treatment, the extra randomized structure visit and the incompatible roster cap. Compare the point estimates and bounded intervals at 50% capacity.
3. Show the pinned manifest, training split, frozen policy hash and offline replay. Explain why the public projection omits fitted weights and row-level allocations.
4. Compare the benchmark's rules, layout, model and corroboration rows. Explain what evidence alignment measures and why source accuracy blocked deployment.
5. Trace the public build through type checks, cross-engine browser tests and the release ledger. Explain the use of direct upload, static hosting and a verified rollback target.

## Interview prompts

| Role | Question | Answer to defend |
| --- | --- | --- |
| Healthcare business | Would the 16.67 pp target justify funding the flu campaign? | It quantifies the gain to test under the assumed reach and costs. Local evidence, realistic delivery and downstream capacity determine feasibility. |
| Healthcare business | Could CMS averages imply a Star or revenue change? | Measure thresholds, contract-level scoring and financial terms are separate inputs, and the flu measure is survey-based. |
| Causal inference | Why use known propensities and whole triplets? | Design probabilities identify assignment contrasts under the stated observation and interference assumptions. Grouped splitting keeps dependent assignments in one partition. |
| Causal inference | Why do the conservative intervals remain wide? | They allow the full bounded outcome range under a small number of independent blocks and protect multiple comparisons. Repeated rows cannot create more independent experiments. |
| ML engineering | How do you resume a stopped run? | Keep the verified source snapshots and stage reports, run the affected CLI group and match the stored policy freeze. Protect the source and audit digests independently. |
| ML engineering | Why use ridge and local files? | Small cluster counts constrain flexible models. Explicit manifests and static exports meet the current replay and publication requirements without a service. |
| AI engineering | What failed after relevant text was retrieved? | The extractor confused allocation, recruitment and endpoint scope. Hard corroboration removed correct values and reduced unsupported fills without passing the gate. |
| AI engineering | What evidence would justify reopening extraction? | Development improvement on justified candidates, alternate valid span labels, independent review and a frozen new holdout using the original 90% and abstention criteria. |
