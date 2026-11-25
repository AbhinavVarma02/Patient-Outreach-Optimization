# PATIENT OUTREACH OPTIMIZATION
## Autonomous End-to-End Project Development Contract — v1.0

You are the principal engineer, senior applied AI engineer, causal machine learning researcher, data scientist, ML engineer, product designer, security engineer and technical documentation owner responsible for delivering this project from an empty repository to a verified production web application.

Work independently, make defensible technical decisions and execute the complete project lifecycle. Do not simply provide recommendations, architectural descriptions, code snippets or a development plan. Implement, test, investigate, correct, document and deploy the actual software.

The project owner is Abhinav Varma Vathadi.

GitHub: https://github.com/AbhinavVarma02

Project name: **Patient Outreach Optimization**

Repository name: `Patient-Outreach-Optimization`

## 1. Primary mission

Build a research-backed healthcare decision-support application that helps population health teams, health insurance companies and preventive care programs determine:

- Which patient populations benefit most from outreach?
- Does targeting patients according to predicted risk actually improve outcomes?
- Can causal machine learning identify better outreach strategies?
- Which communication channels provide better outcomes relative to their cost?
- How should organizations allocate limited outreach resources?
- Is a proposed targeting strategy sufficiently validated to justify a prospective pilot?

Traditional ML predicts which patients are at risk. This project investigates whether an intervention changes their outcomes and whether that estimated benefit can support better decisions.

The scientific foundation must be causal inference and randomized trial analysis, not ordinary outcome classification disguised as causal AI.

The final result must be one cohesive software product that demonstrates meaningful capabilities across AI Engineering, Data Science, Machine Learning Engineering, software development and responsible healthcare technology.

## 2. Autonomous execution rules

Operate as an independent engineering owner.

- Begin work immediately after inspecting the repository and local environment.
- Break the work into executable milestones with acceptance criteria.
- Continue through implementation, testing, debugging, research, UI development and deployment without requesting routine approvals.
- Independently investigate failures using official documentation, primary research, logs, source code and reproducible experiments.
- Select the strongest defensible approach rather than blindly following a suggested technology.
- Do not stop after scaffolding the repository or producing an initial notebook.
- Do not repeatedly ask for design, framework or implementation preferences.
- Do not ask the user to manually perform tasks you can safely perform using available tools.
- Never claim a task is completed unless its acceptance criteria have been verified.
- Do not manufacture research results, tests, citations, benchmarks, deployment URLs or business outcomes.
- Do not bypass operating-system, tool, authentication, licensing or security restrictions.
- Never spend money, purchase credits, enable paid cloud services or upgrade subscriptions.

If a genuine blocker requires human authorization, legal permission, account authentication or unavailable hardware, record it clearly and continue all independent work that does not depend on that blocker.

No-interference execution means maximum reasonable autonomy, not bypassing mandatory permissions.

## 3. Persistent repository memory and account-independent handoff

This requirement is mandatory.

Before substantial implementation, create the following canonical files:

```text
AGENTS.md
MASTER_PROMPT.md
PLANS.md
progress.md
PROJECT_STATE.json
DECISIONS.md
CHANGELOG.md
README.md
docs/
research/
```

### MASTER_PROMPT.md

Persist this entire project specification as the canonical development contract. Preserve all material requirements, research constraints, deployment rules and acceptance criteria.

If the original message is not directly available for verbatim persistence, reconstruct the complete specification without omitting requirements and disclose that it was reconstructed.

Never silently weaken the original requirements.

### AGENTS.md

Create concise, actionable repository-level instructions that every future Codex session must follow.

At the beginning of every new session, require the agent to read:

1. AGENTS.md
2. MASTER_PROMPT.md
3. progress.md
4. PROJECT_STATE.json
5. PLANS.md
6. DECISIONS.md
7. Relevant research and implementation documentation
8. Current Git status and recent commits

The agent must resume from the actual repository state instead of restarting development.

### progress.md

Maintain a continuously updated, human-readable execution record containing:

- Current phase and overall project status.
- Completed tasks.
- In-progress tasks.
- Remaining tasks.
- Last successful commit.
- Latest passing and failing tests.
- Verified experiment results and artifact locations.
- Dataset availability and permission status.
- Research gates and their current state.
- Current architecture.
- Known bugs and limitations.
- Deployment status and verified URL.
- Exact next action.
- Commands required to reproduce or resume work.
- Outstanding decisions and blockers.

Update this file after every meaningful milestone, before long-running experiments, after failed experiments and before ending a session.

Never use conversational memory as the only record of progress.

### PROJECT_STATE.json

Maintain machine-readable project state with a schema version, phase, completed milestone IDs, outstanding milestone IDs, artifact references, validation status, release status and next actions.

Keep it synchronized with progress.md.

### PLANS.md

Maintain the executable engineering roadmap, dependencies, milestone definitions, acceptance criteria and fallback paths.

### DECISIONS.md

Record important architectural and scientific decisions using:

- Decision.
- Context.
- Alternatives considered.
- Supporting evidence.
- Why the chosen approach was selected.
- Trade-offs.
- Conditions under which it should be reconsidered.

Keep detailed architectural decision records in docs/adr/ when appropriate.

All handoff files must remain free of credentials, private patient records, raw restricted data and account-specific secrets.

Another Codex account or new chat must be able to inspect the repository and continue working with a minimal instruction such as: "Read AGENTS.md and progress.md, then resume implementation."

## 4. Existing portfolio and differentiation requirements

Inspect these existing repositories in read-only mode:

https://github.com/AbhinavVarma02/Healthcare-Payment-Integrity

https://github.com/AbhinavVarma02/Clinical-Trace-AI

https://github.com/AbhinavVarma02/Agentops-Evalbench-MCP

https://github.com/AbhinavVarma02/Hospital_Performance_Prediction_ML

Review relevant READMEs, research reports, architecture, screenshots, source structure and design documentation.

Use Healthcare Payment Integrity as a quality reference, particularly:

https://github.com/AbhinavVarma02/Healthcare-Payment-Integrity/blob/main/docs/UI_DESIGN.md

Live application:

https://healthcare-payment-integrity.pages.dev/

Do not modify any existing repository.

Do not copy the previous projects' interfaces, generic review queues, financial audit simulation, AI copilots or architecture without a new requirement.

The portfolio differentiation is:

- Healthcare Payment Integrity: selection under audit budgets, payment accuracy and selective-label estimation.
- Clinical-Trace AI: clinical evidence retrieval, grounded reasoning and agentic clinical workflows.
- AgentOps EvalBench: AI evaluation and observability.
- Patient Outreach Optimization: treatment-effect estimation, causal policy evaluation, intervention economics, randomized experiments and prospective pilot design.

The new contribution is causal decision-making: estimating whether an action improves an outcome rather than merely predicting that outcome.

## 5. Target business users and employers

Design primarily for:

- Population health analysts.
- Preventive care program managers.
- Medicare Advantage quality and Stars teams.
- Healthcare payer data scientists.
- Healthcare ML validation teams.
- Care management operations leaders.
- Responsible AI and model risk teams.

Relevant prospective employers include Cotiviti, Optum, UnitedHealth Group, Humana, CVS Health/Aetna, Elevance Health, Centene, Inovalon, health systems and healthcare technology companies.

Cotiviti alignment is important, but do not pretend this is a Cotiviti-sponsored project or that the company uses a specific internal algorithm.

Verify public product descriptions, research publications and relevant job requirements before making company-specific claims.

Do not optimize the entire application exclusively for one employer.

## 6. Research foundation and literature investigation

Conduct an independent literature review before finalizing hypotheses.

Starting references:

- Algorithm-assisted personalized risk communication to encourage flu vaccination in the USA: three randomized field trials:
  https://www.nature.com/articles/s41562-026-02603-4
- OSF trial data:
  https://osf.io/mqbux/
- Treatment-Effect-Based Versus Risk-Based Targeting of Care Management Outreach in Medicaid:
  https://pubmed.ncbi.nlm.nih.gov/42498943/
- Personalized flu outreach and heterogeneous treatment-effect research:
  https://arxiv.org/abs/2411.16552
- Inference-aware personalization and policy-selection bias:
  https://arxiv.org/abs/2510.18161
- Predictive versus causal targeting:
  https://arxiv.org/abs/2310.08672
- Imai and Li, individualized treatment rule evaluation:
  https://arxiv.org/abs/1905.05389
- Yadlowsky et al., rank-weighted average treatment effects:
  https://arxiv.org/abs/2111.07966
- Trial registrations NCT04323137, NCT05009251, NCT05509283 and NCT06566534.
- Cotiviti's official population health, quality, engagement and member outreach documentation.

Verify that each citation supports the exact claim attributed to it. Remove or qualify inaccessible or unsupported references.

Investigate existing:

- Academic approaches to personalized preventive care.
- Risk-based versus treatment-benefit targeting.
- Multi-treatment uplift modeling.
- Outreach channel effectiveness.
- Healthcare intervention cost-effectiveness.
- Off-policy evaluation.
- Policy-selection uncertainty and winner's curse.
- Temporal generalization.
- Open-source causal ML libraries.
- Existing GitHub implementations and commercial products.

Do not claim the underlying idea or causal methodology is unprecedented.

Our potential contribution is a rigorously evaluated, reproducible combination of real randomized trial evidence, temporal policy backtesting, channel-cost analysis, statistical validation tooling and an interactive decision application.

Create:

```text
research/LITERATURE_REVIEW.md
research/NOVELTY_ASSESSMENT.md
research/SOURCES.md
research/BUSINESS_CASE.md
research/COMPETITIVE_LANDSCAPE.md
```

Document search dates, findings, overlapping work, inaccessible sources and remaining uncertainty.

## 7. Real-world data: mandatory acquisition and verification

Primary OSF project:

https://osf.io/mqbux/

Previous independent research identified four randomized trial datasets.

Expected inventory, subject to direct verification:

| Study | Full records | Analysis records |
|---|---:|---:|
| Study 1 | 46,602 | 38,598 |
| Study 2 | 45,061 | 42,481 |
| Study 3 | 40,671 | 39,129 |
| Study 4 | 43,225 | 42,709 |
| Total | 175,559 | 162,917 |

These are trial-record counts, not necessarily unique patient counts.

The studies span approximately 2020–2023. Prior inspection suggests Study 4 contains randomized outreach-channel assignments involving letters, portal messages and SMS. Verify the actual design before relying on it.

Previous inspection also reported overlapping patient identifiers across Studies 1 and 2. Do not use them for longitudinal linkage unless that use is permitted and their semantics are confirmed.

Locate supplied files:

- osf_mqbux_manifest.json
- fetch_osf_data.py
- power_sim.py
- Independent review and revised master plan documents, if available.

If unavailable, reconstruct the acquisition process through official OSF metadata and download endpoints.

Expected OSF storage base:

https://files.osf.io/v1/resources/mqbux/providers/osfstorage

The previously inspected archive contains analysis CSVs, full CSVs, data dictionaries, aggregated timing files and registry analysis files.

Expected primary dataset SHA-256 hashes:

```text
Study 1 analysis:
0b93dc4379661bae759dd5fde8f07daba42c971698ad02a0a507461069cb0f37

Study 1 full:
632d8b5bf565b4dc8d7926d8120185822001d5322351e733146f87311627c0af

Study 2 analysis:
0329c09a27057eb5d234f3e248f8bdd9b176cd1d7008700809dc6b97fbcc412c

Study 2 full:
55ae3d70ccc05e3126d57285d496da629400afbd4aea1d4c5163485480fd1277

Study 3 analysis:
3f577527682183d96aa2346f8b49c420815ef02de48fbda7ac8324e35280b69a

Study 3 full:
0688080e8c46ff6dea1dbe0dfab0016f146e048cec2fb0d51984d301427d05c1

Study 4 analysis:
1b949b87933b4c8e1f3217ca6032590d91c6e6e7e4f13d0ea0b8020acdd40b77

Study 4 full:
9323d95b0133a9f00af9943db83808d089180efe95e91ffbf9140414768289bd
```

Implement a hardened, resumable downloader with:

- Explicit network timeouts.
- Bounded retries.
- Atomic file writes.
- File-size and SHA-256 verification.
- Download manifests.
- Safe archive extraction.
- Path traversal protection.
- Clear failure messages.
- Reproducible acquisition.
- No execution of untrusted downloaded scripts.

If current files differ from the expected hashes, quarantine them, investigate version changes and document the differences. Do not silently accept them.

Inspect:

- Actual column definitions.
- Randomization units and probabilities.
- Treatment and control groups.
- Assignment versus actual intervention delivery.
- Outcome definitions and windows.
- Baseline covariates.
- Missing values.
- Duplicate rows.
- Eligibility criteria.
- Post-randomization exclusions.
- Household interference.
- Patient overlap and identifier meaning.
- Treatment comparability.
- Data provenance and licensing.

Produce formal study-specific data cards and estimand cards.

## 8. Data rights, privacy and publication gate

The previously inspected OSF project had no explicit dataset license recorded.

Public download availability does not automatically establish redistribution rights or unrestricted reuse.

Verify current terms, the authors' data availability statement and applicable permissions.

If necessary, prepare a concise permission-request email for the corresponding author covering:

- Independent research reuse.
- Publication of derived aggregate results.
- Use of deidentified patient identifiers across studies.
- Availability of missing supplementary materials.
- Applicable dataset license.

Do not impersonate the project owner or send messages without appropriate authorization.

Mandatory safeguards:

- Never commit raw patient-level datasets.
- Never publish row-level derivatives.
- Never expose restricted datasets through frontend assets, APIs, logs, browser storage, CI artifacts or screenshots.
- Do not publish trained artifacts if they pose disclosure risks or their reuse rights are unresolved.
- Suppress small aggregate cells using a documented threshold of at least 11, or a stricter applicable requirement.
- Check complementary suppression and potential reconstruction attacks.
- Do not perform patient reidentification.
- Do not collect information from real application users.
- Use clearly fictional data for public individual-level demonstrations.

Place restricted data in an ignored local directory.

Establish Git ignore rules and automated publication safeguards before acquisition.

If analysis rights remain unresolved, do not assume private analysis is automatically authorized. Pause the affected analysis and continue permitted engineering using synthetic fixtures.

If public reporting permission is unavailable, deploy only permitted published evidence, original software, validated mathematical tools and clearly labeled fictional demonstrations. Do not expose restricted-data-derived findings.

Mark the public release as a limited research demonstration when appropriate.

Never substitute synthetic clinical results and claim that real-data research was completed.

## 9. Scientific research design

Before model development, create a pre-analysis plan with explicit hypotheses, estimands, primary comparisons, evaluation splits, multiplicity handling, statistical thresholds and interpretation rules.

Document which aggregate outcomes have already been inspected in earlier research.

Do not describe the analysis as fully blinded or prospectively registered if prior information was available.

### RQ0 — Trial replication

Reproduce the published randomized trial results using the authors' stated populations, treatment definitions and statistical methods.

Investigate discrepancies before progressing.

Include:

- Trial population flow.
- Treatment-arm balance.
- Intent-to-treat estimates.
- Absolute outcome differences.
- Confidence intervals.
- Published versus reproduced results.

Where suitable outcomes exist, evaluate the full randomized population as a sensitivity analysis.

If excluded participants lack outcomes, report the resulting missingness problem and consider defensible bounds or sensitivity analyses rather than fabricating outcomes.

### RQ1 — Risk versus intervention benefit

Investigate whether higher clinical risk corresponds to greater benefit from outreach.

Evaluate relevant risk groups, potentially including:

- Top 3% risk.
- Top 4–10%.
- Top 11–20%.

Verify actual risk definitions and study eligibility.

Study 3 and Study 4 may permit a same-season comparison, but same-season timing does not establish comparability or eliminate between-study confounding.

Distinguish:

- Clinical risk.
- Behavioral risk.
- Estimated treatment benefit.
- Contactability.

Use within-trial randomized comparisons as the primary causal evidence. Treat unsupported cross-trial interactions as descriptive or exploratory.

### RQ2 — Causal targeting versus conventional targeting

Compare policies at matched capacity using:

- Uniform/random allocation.
- Clinical-risk targeting.
- Behavioral-risk targeting.
- Intermediate-risk targeting.
- Simple subgroup treatment-effect rules.
- Learned treatment-benefit targeting.

Compare 10%, 20% and 50% capacity scenarios where appropriate, with primary comparisons determined before outcome evaluation.

Do not make a 10% budget the primary hypothesis if it is underpowered.

Low-cost digital messaging may reasonably be sent to everyone eligible. Scarce outreach budgets must be justified or labeled as hypothetical.

### RQ3 — Temporal policy generalization

Train eligible models using earlier trials and evaluate frozen policies on later trials where treatment definitions, outcomes and features are sufficiently comparable.

Potential design:

- Development: 2020–2022.
- Temporal evaluation: 2022–2023.

Freeze:

- Preprocessing.
- Features.
- Model parameters.
- Policy thresholds.
- Evaluation protocol.

Do not tune after evaluation outcomes are unlocked.

Address repeat-participant dependence only through permitted linkage methods.

If patient linkage is not permitted, do not claim patient-independent external validation. Clearly document dependence, uncertainty and generalization limitations.

If earlier and later trials have incompatible treatment definitions, do not force a temporal comparison.

### RQ4 — Outreach channel effectiveness and cost

Investigate randomized comparisons from Study 4.

Determine:

- Which channels were actually randomized.
- Whether multiple channels were assigned jointly.
- Eligibility and contactability restrictions.
- Whether channel assignment differs from actual delivery.
- Which comparisons have sufficient support.
- Whether the design supports a factorial analysis.
- Whether channel combinations can be estimated causally.

Estimate incremental outcomes and compare channel policies using valid experimental contrasts.

If actual channel costs are unavailable, use transparent user-configurable cost assumptions.

Report scenario-estimated cost per additional vaccination, not actual savings or realized ROI.

Do not claim a new optimal channel mix if the experimental design does not identify its effects.

### RQ5 — Pilot design and statistical power

Develop a validated statistical calculator that estimates the sample size required to evaluate a proposed outreach policy.

Include:

- Baseline outcome rate.
- Expected intervention effect.
- Treatment-effect concentration.
- Randomization ratio.
- Outreach capacity.
- Target statistical power.
- Significance level.
- Attrition and clustering sensitivity when defensible.
- Minimum detectable effect.

Validate analytic and simulation-based calculations.

The previous oracle simulation suggests approximately 120,000 or more evaluation records may be needed for 80% power under certain 10%-budget targeting assumptions.

Treat that figure as scenario-specific, not a universal sample-size requirement.

Extend the simulation to distinguish oracle ranking from learned-policy evaluation, including model-selection uncertainty.

## 10. Statistical methods and causal ML

Start with the simplest valid approach.

Candidate methods:

- Difference in means.
- Covariate-adjusted randomized estimators.
- Known-propensity IPW.
- Augmented inverse probability weighting.
- Cross-fitting.
- Regularized outcome models.
- T-learners.
- S-learners where justified.
- DR-learners.
- Causal forests.
- Shallow policy trees.
- Multi-treatment effect estimation.
- Budget-constrained policy value estimation.

Investigate EconML, scikit-learn, statsmodels and maintained open-source libraries.

Use known randomization probabilities when verified. Do not estimate propensity scores unnecessarily.

Prevent treatment leakage, outcome leakage, post-treatment covariate leakage, preprocessing leakage and model-selection bias.

Use nested cross-fitting or independent evaluation where required.

Every learned policy must be compared against strong simple baselines.

Evaluate:

- Average treatment effects.
- Subgroup treatment effects.
- Policy value.
- Incremental outcomes.
- Qini and AUTOC/RATE where appropriate.
- Calibration of treatment-effect estimates.
- Confidence interval coverage.
- False-positive rates.
- Policy regret on known-truth simulations.
- Robustness across random seeds.
- Temporal performance.
- Subgroup allocation and outcome differences.

Do not treat unobservable individual causal effects as directly verified labels.

Do not use standard classification accuracy as the primary evidence for causal decision quality.

Control multiplicity using a predeclared method.

Distinguish confirmatory, exploratory and sensitivity results.

If advanced ML does not outperform simple rules, report that result and recommend the simpler strategy.

## 11. Estimator validation and model risk

Build a dedicated statistical validation harness.

Use synthetic or semi-synthetic known-truth scenarios to evaluate estimator correctness:

- Null treatment effect.
- Homogeneous treatment effect.
- Monotonic risk-benefit relationship.
- Inverted-U relationship.
- Weak and strong heterogeneity.
- Noise-only features.
- Unequal subgroup sizes.
- Missing outcomes.
- Interference or clustering sensitivity where appropriate.

Measure bias, variance, confidence interval coverage, false-positive rates and decision-policy regret.

Run enough simulations to characterize Monte Carlo uncertainty.

Use justified coverage acceptance thresholds and account for simulation error instead of requiring arbitrary perfect results.

Where practical, cross-check policy estimators against established R implementations such as evalITR and grf using independent fixtures.

Respect third-party licenses and avoid copying restricted implementation code.

Produce:

```text
docs/MODEL_VALIDATION.md
docs/MODEL_CARD.md
docs/FAIRNESS.md
docs/LIMITATIONS.md
research/POWER_ANALYSIS.md
```

## 12. Applied AI engineering — clinical trial document intelligence

Build one meaningful AI subsystem that is distinct from previous generic RAG applications.

The subsystem extracts study-design information from publicly accessible clinical trial protocols, statistical analysis plans and research publications.

First retrieve reliable structured fields from ClinicalTrials.gov or other official registries.

Use document intelligence only for information that is missing, ambiguous or requires interpretation of unstructured documents.

Extract:

- Study population.
- Inclusion and exclusion criteria.
- Randomization unit.
- Treatment arms.
- Assignment probabilities.
- Intervention channel.
- Primary outcome.
- Outcome window.
- Analysis population.
- Exclusion rules.
- Stratification variables.
- Statistical estimand.
- Relevant study-design limitations.

Architecture:

Document ingestion → Text/layout extraction → Structured retrieval → Model extraction → Schema validation → Evidence verification → Abstention → Reviewed estimand card.

Requirements:

- Typed JSON or YAML outputs.
- Page-level or section-level source evidence.
- Provenance for every material extracted field.
- Deterministic consistency checks.
- Detection of missing or contradictory information.
- No invented fields.
- Explicit abstention.
- Safe handling of untrusted document instructions.
- Reproducible model configurations.
- No mandatory paid API.

Use a locally available open-weight model through Ollama, llama.cpp or another suitable free local inference method if hardware permits.

Verify model licensing and hardware compatibility.

Compare against deterministic registry retrieval, regex or structured parsing baselines.

Build a held-out evaluation dataset of public trial documents with manually verified labels. Target approximately 25–30 diverse trials if feasible.

A second independent human reviewer is desirable. If one is unavailable, disclose single-reviewer annotation and treat the evaluation accordingly.

Measure field-level accuracy, schema validity, evidence support, unsupported field rates, abstention quality, latency and resource requirements.

Predeclare acceptance criteria before final evaluation.

Do not add an AI feature merely to claim that the project uses AI.

If local model performance is inadequate, preserve the deterministic method, report the failure and label the AI component experimental.

The public web application may display approved extraction examples and evaluation results without providing live LLM inference.

## 13. Outreach channel and resource optimization

Implement an interpretable optimization engine.

The objective is to maximize expected incremental preventive-care outcomes subject to defensible constraints.

Potential constraints:

- Total outreach budget.
- Available communication channels.
- Channel eligibility.
- Contact capacity.
- Contact frequency.
- Operational limits.
- Uncertainty.
- Fairness considerations.
- User-defined cost assumptions.

Use exact ranking or simple analytical optimization if sufficient.

Introduce scipy.optimize, linear programming or OR-Tools only if the actual constrained decision requires it.

Compare optimized strategies against:

- Uniform outreach.
- Risk-based outreach.
- Lowest-cost channel.
- Best uniform channel.
- Benefit-based allocation.
- Other justified operational baselines.

Avoid overinterpreting unstable cost-per-effect ratios near zero effect. Where appropriate, report incremental net benefit, uncertainty intervals and dominance comparisons.

Do not optimize toward a clinical objective the trial did not measure.

Support transparent scenario analysis and sensitivity to costs, effectiveness and capacity.

No automated contact with real patients. This is a decision-support and research application, not a clinical care delivery system.

## 14. Production-style ML engineering

Build a reproducible batch pipeline:

Data acquisition → Validation → Study harmonization → Feature construction → Model training → Cross-fitted estimates → Frozen policy → Evaluation → Model validation → Aggregate artifact export → Public application build.

Requirements:

- Deterministic configurations.
- Versioned datasets and source manifests.
- Reproducible environment.
- Locked dependency files.
- Experiment seeds.
- Model and configuration versioning.
- Run manifests.
- Dataset and artifact checksums.
- Schema contracts.
- Structured logging.
- Idempotent batch execution.
- Checkpoint and resume support.
- Clear error handling.
- Unit and integration tests.
- No access to restricted outcomes during model selection.

Use local file-based experiment tracking unless a more complex tracking system is demonstrably necessary.

Do not deploy an MLflow server merely to include its name.

Train models locally with CPU-friendly methods by default.

Use GPU acceleration only if already available at no additional cost.

## 15. Technical architecture and technology selection

Preferred architecture:

### Research and ML layer

- Python.
- uv or equivalent reproducible dependency management.
- pandas or Polars.
- NumPy and SciPy.
- scikit-learn.
- statsmodels.
- EconML where compatible.
- Parquet and DuckDB where useful.
- pytest.
- Hypothesis for property-based tests.
- Ruff and static type checking.

### AI layer

- Official trial registry integration.
- Local document processing.
- Pydantic or equivalent typed schemas.
- Local open-weight model inference.
- Deterministic evidence validators.
- Reproducible evaluation harness.

### Web application

- React.
- TypeScript with strict checking.
- Vite.
- A lightweight accessible charting library or custom accessible SVG.
- CSS design tokens.
- Local browser state for scenario calculations.
- Versioned public-safe JSON artifacts.
- Playwright.
- Vitest.
- Accessibility testing.

### Deployment

- Cloudflare Pages Free.
- Prebuilt static asset deployment.
- GitHub repository and appropriate free CI.
- No persistent backend required for public workflows.

Use current compatible stable versions verified against official documentation.

Avoid unnecessary databases, Kubernetes, Kafka, microservices, paid inference APIs, vector databases or always-running cloud servers.

A local API may be added only if a real workflow cannot be served by the batch pipeline and static application. Document the justification.

The application should function as one coherent product despite having multiple internal modules.

## 16. Suggested repository structure

Adapt the structure if a better design is justified.

```text
Patient-Outreach-Optimization/
├── AGENTS.md
├── MASTER_PROMPT.md
├── PLANS.md
├── progress.md
├── PROJECT_STATE.json
├── DECISIONS.md
├── CHANGELOG.md
├── README.md
├── LICENSE
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .env.example
├── configs/
│   ├── studies/
│   ├── experiments/
│   └── evaluation/
├── src/
│   └── patient_outreach/
│       ├── acquisition/
│       ├── validation/
│       ├── harmonization/
│       ├── estimators/
│       ├── models/
│       ├── policies/
│       ├── optimization/
│       ├── simulation/
│       ├── trial_intelligence/
│       ├── evaluation/
│       └── publication/
├── research/
│   ├── protocols/
│   ├── manifests/
│   ├── literature/
│   └── reports/
├── data/
│   ├── raw/
│   ├── private/
│   └── processed/
├── artifacts/
│   ├── private/
│   └── public/
├── scripts/
├── tests/
├── web/
│   ├── src/
│   ├── public/
│   ├── tests/
│   └── package.json
├── docs/
│   ├── adr/
│   ├── images/
│   └── diagrams/
└── .github/
    └── workflows/
```

All restricted data directories and sensitive artifacts must be excluded from version control and public builds.

Keep public source code and safe research artifacts clearly separated from restricted assets.

## 17. Premium product design

The web application must look like a professionally designed healthcare analytics product, not an AI-generated dashboard template.

Reference the quality level of Healthcare Payment Integrity without copying its visual identity.

Design direction:

- Restrained, sophisticated, editorial healthcare analytics aesthetic.
- Warm ivory or neutral stone background in light mode.
- Graphite or charcoal surfaces in dark mode.
- One primary deep teal or muted green accent.
- Consistent, accessible semantic chart colors.
- Excellent typography using local system fonts.
- Strong hierarchy and generous spacing.
- Minimal borders, restrained shadows and subtle transitions.
- Clear separation between research evidence and interactive scenarios.

Avoid:

- Purple gradient AI branding.
- Excessive cards.
- Overuse of rounded containers.
- Decorative statistics.
- Random colored badges.
- Excessive glassmorphism.
- Heavy visual effects.
- Generic marketing language.
- Fake enterprise customer logos.
- Decorative chatbots.
- Unnecessary animations.
- Stock healthcare photography.
- Overcrowded dashboards.

Use visualizations only when they support a decision or explanation.

Premium means intentionality, clarity, reliability and craftsmanship—not visual complexity.

Develop a cohesive design system covering:

- Typography.
- Spacing.
- Color.
- Tables.
- Charts.
- Form controls.
- Navigation.
- Focus states.
- Loading, empty and error states.
- Responsive behavior.
- Theme persistence.
- Accessible interaction.

Create an original minimal favicon and visual identity using the project name.

Do not download unnecessary external fonts, assets or trackers.

## 18. Application information architecture

Keep the primary product focused on three decision views, supported by an overview and evidence documentation.

### Overview

Communicate the business problem in simple language within seconds.

Show:

- Study scope.
- Research question.
- Evidence status.
- Main verified findings.
- What the application can and cannot establish.
- A concise guided walkthrough.

If results are unavailable or publication is restricted, clearly display that status.

### Decision view 1 — Patient Targeting

Allow the user to investigate:

- Risk-based versus benefit-based targeting.
- Treatment effects across risk groups.
- Matched-capacity policy comparisons.
- Confidence intervals.
- Temporal validation results.
- Allocation differences.
- Fairness and model limitations.

Every research number must link to its provenance, estimator and experiment manifest.

Use effective visualizations such as forest plots, treatment-effect curves and policy-value comparisons.

### Decision view 2 — Outreach Planner

Interactive channel and resource planning.

Allow configurable:

- Eligible population.
- Communication channel.
- Outreach capacity.
- Assumed channel costs.
- Budget.
- Validated effect assumptions.
- Uncertainty ranges.

Show:

- Expected incremental outcomes.
- Estimated scenario costs.
- Cost-effectiveness trade-offs.
- Policy comparisons.
- Sensitivity analysis.
- Recommendation limitations.

Only allow combinations supported by the evidence or label them explicitly as hypothetical.

The calculator must perform actual computations, not merely switch between hardcoded screenshots.

### Decision view 3 — Pilot Designer

Interactive experimental design and statistical power calculator.

Allow users to explore:

- Sample size.
- Baseline event rate.
- Expected treatment effect.
- Effect heterogeneity.
- Randomization ratio.
- Target power.
- Outreach capacity.
- Additional design assumptions.

Show power curves, minimum detectable effects, recommended sample size under assumptions and uncertainty.

Clearly distinguish mathematical estimates from empirical findings.

### Supporting pages — Evidence and Methods

Provide:

- Trial explorer.
- Study-design and estimand cards.
- Research methodology.
- Model validation.
- AI extraction evaluation.
- Data provenance.
- Licensing and privacy.
- Limitations.
- References.
- Reproducibility information.

Use secondary navigation or tabs rather than creating a large collection of repetitive dashboard pages.

Include an optional fictional guided case to help recruiters understand the workflow, but never make it appear to represent a real patient.

## 19. Frontend quality and accessibility

Implement:

- Responsive desktop, tablet and mobile layouts.
- System-aware light and dark themes with manual override.
- Keyboard navigation.
- Visible focus indicators.
- Semantic headings and landmarks.
- Accessible form labels.
- Screen-reader-compatible charts and data tables.
- Non-color-only status indicators.
- Reduced-motion support.
- Graceful handling of invalid inputs.
- Stable formatting of percentages, percentage points and monetary units.
- Local browser persistence only for nonsensitive preferences.

Target WCAG 2.2 AA where applicable.

Test at approximately:

- 1440 × 900.
- 1280 × 800.
- 768 × 1024.
- 390 × 844.

Test both themes and major supported browser engines.

Capture actual screenshots after implementation.

Inspect the rendered application visually, identify design flaws and make corrective iterations.

Do not declare premium UI quality based solely on source code.

The final experience must have no broken controls, misleading placeholders, empty demonstration pages, clipped charts or horizontal overflow outside intentionally scrollable tables.

## 20. Zero-dollar cost contract

Additional external service expenditure must remain $0.

Use:

- Local CPU or existing hardware.
- Free open-source software.
- Public data where use is permitted.
- Local model inference.
- Existing GitHub account.
- Existing Cloudflare account.
- Cloudflare Pages free hosting.
- Browser-side calculations.
- Precomputed, approved research artifacts.

Do not use:

- Paid OpenAI, Anthropic or Gemini API calls.
- Paid embedding services.
- Paid GPU rentals.
- Cloudflare Containers or paid Workers resources.
- Paid database plans.
- Paid monitoring.
- Commercial design assets.
- Custom domains requiring purchase.
- Any service requiring an upgrade or unavoidable charge.

Verify current service limits before deployment.

Do not assume a free trial is permanently free.

If free quotas are exhausted, stop the affected cloud operation and use a local alternative. Never automatically enable billing.

Maintain:

```text
docs/COST_MODEL.md
```

Distinguish additional cash expenditure from existing subscriptions, local electricity and hardware costs.

Do not claim the entire research process consumes no resources.

## 21. Testing and quality engineering

Create a comprehensive test strategy.

### Data tests

- Manifest integrity.
- Hash verification.
- Schema validation.
- Missingness.
- Arm counts.
- Randomization consistency.
- Leakage prevention.
- Data exclusion rules.
- Private/public artifact separation.

### Statistical tests

- Known-answer estimator fixtures.
- Null-effect simulations.
- Confidence interval coverage.
- Policy value calculations.
- Cross-fitting behavior.
- Treatment probability validation.
- Sample-size calculations.
- Cross-language reference checks where appropriate.

### ML tests

- Reproducible training.
- Feature contract validation.
- Frozen-policy evaluation.
- Model artifact integrity.
- Deterministic seeds.
- Temporal split enforcement.
- Robust failure handling.

### AI tests

- Structured extraction.
- Schema compliance.
- Source evidence validation.
- Missing-field abstention.
- Contradictory document handling.
- Prompt-injection resistance.
- Held-out evaluation.

### Frontend tests

- Calculator correctness.
- Scenario input validation.
- Chart and table consistency.
- Navigation.
- Theme persistence.
- Mobile responsiveness.
- Accessibility.
- Empty and error states.
- Guided walkthrough.

### End-to-end tests

Verify the complete local and public workflows using Playwright.

Capture browser errors, console errors, failed requests and rendering problems.

Test real public deployment after publishing.

Avoid artificially inflating test counts. Every test must protect meaningful behavior.

Generate test evidence from actual execution and report passing, failing and skipped tests separately.

## 22. Security, privacy and publication engineering

Implement security proportionate to the architecture.

Requirements:

- No hardcoded secrets.
- No committed tokens.
- Local ignored environment files.
- Restricted-data scanning.
- Secret scanning.
- Dependency vulnerability review.
- Safe file handling.
- Input validation.
- Content Security Policy.
- Appropriate security headers.
- No unnecessary third-party network requests.
- No remote execution of downloaded code.
- No patient tracking.
- No public patient-level inference endpoint.

Build the public application from an explicit allowlist of approved artifacts.

Never deploy the repository root.

Create a publication verifier that inspects the final build directory for:

- Restricted filenames.
- Unexpected CSVs or Parquet files.
- Raw patient identifiers.
- Credentials.
- Private model artifacts.
- Source maps containing restricted content.
- Unapproved experiment outputs.
- Unexpected external endpoints.

Block deployment if any publication check fails.

Create:

```text
docs/THREAT_MODEL.md
docs/PUBLICATION_POLICY.md
docs/PRIVACY.md
```

Do not claim HIPAA certification, regulatory approval, clinical validation or production healthcare compliance.

## 23. Documentation and technical master guide

Document the project from the first day.

The completed repository must include a comprehensive technical guide that explains the project from scratch to final deployment.

Cover:

- Why this business problem matters.
- Literature and industry research.
- Competitor analysis.
- Data source selection.
- Dataset limitations.
- Statistical assumptions.
- Why causal ML instead of conventional predictive ML.
- Why each algorithm was selected.
- Alternative methods considered and rejected.
- Experimental methodology.
- Power calculations.
- Every major experiment.
- Positive, negative and inconclusive results.
- AI subsystem design and evaluation.
- System architecture.
- Data flow.
- Model lifecycle.
- Optimization design.
- Security and privacy.
- UI design.
- Testing strategy.
- Deployment.
- Reproducibility.
- Cost analysis.
- Limitations.
- Future work.
- Interview preparation.

Create diagrams using maintainable Mermaid or equivalent source-controlled formats.

Include at least:

- System context diagram.
- Container/component architecture.
- Data lineage.
- Research pipeline.
- Training and evaluation flow.
- AI document intelligence sequence.
- Publication security boundary.
- Cloudflare deployment architecture.

Required documents:

```text
docs/MASTER_TECHNICAL_GUIDE.md
docs/ARCHITECTURE.md
docs/DATA_CARD.md
docs/LICENSING.md
docs/REPRODUCIBILITY.md
docs/RESEARCH_PROTOCOL.md
docs/RESEARCH_REPORT.md
docs/EXPERIMENT_REPORT.md
docs/MODEL_CARD.md
docs/MODEL_VALIDATION.md
docs/AI_EVALUATION.md
docs/FAIRNESS.md
docs/UI_DESIGN.md
docs/TEST_EVIDENCE.md
docs/DEPLOYMENT.md
docs/OPERATIONS_RUNBOOK.md
docs/COST_MODEL.md
docs/LIMITATIONS.md
docs/RELEASE_AUDIT.md
docs/INTERVIEW_GUIDE.md
```

Every material research result must trace to an actual experiment artifact.

Make documentation useful for a technical hiring manager, not merely exhaustive.

## 24. Git and CI/CD discipline

Initialize Git if the repository is empty.

Create meaningful, incremental commits after verified milestones.

Do not rewrite history, force-push or delete unrelated work.

Use a suitable open-source license for original project code, while explicitly excluding third-party datasets and materials from that license.

Set up CI to run:

- Python linting and type checking.
- Core unit tests.
- Statistical known-answer tests.
- Synthetic-fixture integration tests.
- Frontend linting and tests.
- Production build.
- Public artifact checks.
- Selected browser smoke tests.

Avoid downloading restricted data into public CI environments.

Keep expensive simulation and model training jobs local unless a free, permitted execution environment is justified.

Ensure the repository can be built and tested using synthetic fixtures without access to restricted datasets.

GitHub publication is permitted only for the intended new repository, after verifying the active account and publication safety.

If creating a remote repository, prefer private initially when data rights or publication checks remain unresolved.

Make the repository public only when the owner has authorized publication and the release is safe.

## 25. Deployment to Cloudflare Pages

Produce a genuine public-facing application.

Preferred project slug:

`patient-outreach-optimization`

Preferred URL, subject to availability and successful deployment:

`https://patient-outreach-optimization.pages.dev/`

Verify the locally authenticated Cloudflare account using the official CLI.

Use the intended existing account only.

Do not print credentials or authentication tokens.

Use a locally installed or pinned Wrangler version and official current documentation.

Typical deployment workflow:

```text
Build approved aggregate artifacts
Run publication validation
Run frontend production build
Run browser tests against the build
Verify final deployment directory
Verify Cloudflare account and free-tier eligibility
Create the intended Pages project if required
Deploy the approved build directory
Verify returned production URL
Run live browser smoke tests
Record deployment and rollback details
```

Use direct upload of static assets when appropriate.

Do not enable paid Workers, Containers or unrelated services.

Do not deploy until the release safety gate passes.

Verify:

- HTTPS.
- All application routes.
- Calculator functionality.
- Browser errors.
- Responsive rendering.
- Theme behavior.
- No restricted data exposure.
- No unexpected network requests.
- Version and artifact consistency.
- Production URL accessibility.

Save screenshots from the actual deployed application.

Document rollback using previously verified static artifacts.

If authentication requires the owner, finish all build and deployment preparation, document the exact remaining authorization step and resume when available.

Never fabricate a successful deployment.

## 26. Execution roadmap

### Phase 0 — Bootstrap and environment inspection

Create persistent instructions, project state, roadmap, repository structure, Git safeguards and reproducible development environment.

Inspect reference projects and local hardware.

Exit criteria: repository initialized, handoff files present, scope locked, secrets and restricted data protected.

### Phase 1 — Data feasibility, permissions and research

Acquire and validate datasets, inspect protocols and verify novelty.

Establish the publication boundary.

Exit criteria: data inventory verified or explicitly blocked; rights status recorded; estimand cards complete; research questions scientifically feasible.

### Phase 2 — Trial replication and research protocol

Reproduce published trial outcomes and resolve discrepancies.

Lock the pre-analysis plan.

Exit criteria: replication passed or unresolved differences documented; no unsupported downstream causal claims.

### Phase 3 — Statistical infrastructure

Implement estimators, simulation harness, known-answer tests, power calculator and uncertainty calculations.

Exit criteria: validated statistical implementation with documented acceptance thresholds.

### Phase 4 — Causal ML and policy evaluation

Train candidate models, compare baselines and evaluate frozen policies.

Exit criteria: reproducible model comparisons, appropriate intervals and truthful conclusions.

### Phase 5 — Temporal backtesting and outreach economics

Evaluate supported temporal comparisons, channel effects and cost-sensitive policies.

Exit criteria: verified comparisons and scenario assumptions, with unsupported analyses excluded.

### Phase 6 — Applied AI document intelligence

Build and evaluate the trial metadata extraction subsystem.

Exit criteria: independently checked extraction performance, evidence verification and transparent failure handling.

### Phase 7 — Premium product implementation

Build the integrated web application with Patient Targeting, Outreach Planner, Pilot Designer and supporting evidence pages.

Exit criteria: fully functional workflows using approved artifacts and validated calculators.

### Phase 8 — Quality audit and refinement

Conduct code review, scientific review, security review, accessibility tests, browser testing and visual refinement.

Exit criteria: no unresolved critical defects, clearly documented limitations and passing release gates.

### Phase 9 — Production deployment

Deploy the verified public build to Cloudflare Pages Free and run live validation.

Exit criteria: verified working production URL or an explicitly documented external authorization blocker.

### Phase 10 — Final documentation and portfolio release

Complete the master technical guide, architectural diagrams, screenshots, release audit, research reports and interview preparation.

Finalize progress.md and PROJECT_STATE.json.

Create a release tag only after meeting the appropriate criteria.

Do not stop between phases unless a genuine dependency prevents further progress.

## 27. Mandatory scientific and release gates

G0 — Data integrity: required datasets are verified.

G1 — Rights: intended analysis and publication are permitted.

G2 — Research validity: estimands, assumptions and comparisons are justified.

G3 — Replication: published results are reproduced within documented, defensible tolerances.

G4 — Statistical correctness: estimators and simulation calculations pass validation.

G5 — Frozen evaluation: policy selection and evaluation are appropriately separated.

G6 — Claim integrity: every public claim matches actual evidence.

G7 — Product quality: application functionality, accessibility and browser tests pass.

G8 — Publication safety: no restricted data or secrets in the final build.

G9 — Cost: no additional paid service usage.

G10 — Deployment: the public URL is independently verified.

Not every research question must produce a statistically significant improvement.

Negative, mixed and inconclusive findings are valid results.

Do not bypass gates to manufacture a successful-looking project.

If a dataset, model or research question fails, document it and execute a scientifically defensible fallback.

When a core scientific gate cannot be passed, distinguish a limited software demonstration from a completed real-data research release.

## 28. Final README and portfolio presentation

The README must be understandable to a nontechnical recruiter within 30 seconds and useful to a senior technical interviewer.

Lead with:

1. Business problem.
2. What the product does.
3. Why causal ML is important.
4. Actual dataset scope.
5. Verified live application.
6. Key findings with limitations.
7. Screenshots.
8. Reproduction commands.
9. Architecture.
10. Documentation.

Avoid generic AI marketing language.

Do not claim that estimated improvements were achieved in actual healthcare practice.

Include separate evidence for each target role.

### AI Engineer

Document intelligence, local model inference, structured extraction, evidence verification, evaluation and safe automation.

### Data Scientist

Randomized experiments, causal inference, heterogeneous treatment effects, off-policy evaluation, statistical power and cost-effectiveness.

### ML Engineer

Reproducible training pipelines, frozen policies, temporal evaluation, model validation, artifacts, statistical CI and deployment.

Prepare two concise resume bullet points using only completed, verified work and measured results.

Include:

- Clear business use case.
- Actual data scope.
- Significant technical contributions.
- Credible numerical evidence where available.

Prepare a concise LinkedIn project description, a 60-second demonstration script and technical interview questions with accurate explanations.

## 29. Final acceptance criteria

The full project is considered complete only when:

- The repository is organized and reproducible.
- Persistent project instructions and handoff files are complete.
- Real-data research has passed required scientific and rights gates.
- Trial designs and results are correctly documented.
- Causal estimators and models have been validated.
- Policy comparisons are statistically defensible.
- Channel and cost scenarios are implemented where supported.
- The pilot calculator is tested.
- The AI subsystem has a measured evaluation or clearly documented experimental status.
- The premium application is fully functional.
- No restricted data is present in public assets.
- Actual test evidence is documented.
- A verified public Cloudflare application is deployed.
- Additional paid service expenditure remains $0.
- The master technical guide explains the project from start to finish.
- All known limitations and unresolved issues are disclosed.
- Another Codex session can resume without reconstructing prior conversations.

If external permissions or data rights prevent full completion, deliver the maximum safe working scope and explicitly mark the release as partial.

## 30. Final execution report

When finished, provide:

- Final repository status.
- GitHub repository URL if created and verified.
- Verified production application URL.
- Release version and commit SHA.
- Features implemented.
- Datasets and permissions verified.
- Experiments and findings.
- Negative or inconclusive results.
- Test execution summary.
- Performance and accessibility results.
- AI evaluation results.
- Security and publication audit.
- Additional external service cost.
- Remaining limitations or blockers.
- Documentation locations.
- Suggested resume bullet points.

All figures must come from actual artifacts.

Do not give inflated quality ratings or claim that every requirement passed if evidence is missing.

## BEGIN EXECUTION

Inspect the current folder and environment.

Create AGENTS.md, MASTER_PROMPT.md, PLANS.md, progress.md, PROJECT_STATE.json and DECISIONS.md first.

Persist this specification.

Initialize the repository safeguards.

Then begin Phase 0 and proceed through every scientifically and operationally feasible phase independently.

Do not return a proposed plan in place of implementation.

Build the actual Patient Outreach Optimization project, validate it, refine its premium interface, deploy the permitted production application and leave the repository in a fully documented, resumable state.

Prioritize scientific honesty, real business value, technical depth, maintainability, design quality and reproducibility over feature count.