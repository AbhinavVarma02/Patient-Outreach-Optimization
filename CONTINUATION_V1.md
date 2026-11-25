# Patient Outreach Optimization — Continuation to v1.0.0

Resume development of Patient Outreach Optimization from the existing v0.1.0-demo release.

GitHub: https://github.com/AbhinavVarma02/Patient-Outreach-Optimization

Production: https://patient-outreach-optimization.pages.dev/

## 1. Recover project context

Before making changes, read:

- AGENTS.md and CLAUDE.md
- MASTER_PROMPT.md
- progress.md
- PROJECT_STATE.json
- PLANS.md
- DECISIONS.md
- docs/RELEASE_AUDIT.md
- docs/LICENSING.md
- docs/RESEARCH_PROTOCOL.md
- docs/EXPERIMENT_REPORT.md
- docs/AI_EVALUATION.md

Inspect the actual repository, Git history, existing implementation, outstanding milestones and production deployment.

Do not restart the project or duplicate completed work. Preserve the existing release, design system, working functionality and research safeguards.

Persist this continuation prompt in CONTINUATION_V1.md and reference it from AGENTS.md and CLAUDE.md.

## 2. Current status and objective

The current release is a verified software demonstration, not a completed causal ML research product.

Outstanding limitations:

- OSF metadata matches all 20 pinned files, but participant-level payload and schema validation remain incomplete.
- Dataset reuse, linkage and publication rights remain unresolved.
- Independent replication of randomized trial results has not been performed.
- Causal policy evaluation currently uses fictional data.
- Real-data temporal backtesting remains incomplete.
- AI document extraction has only five smoke cases and has not outperformed its deterministic baseline.

The objective is to resolve these limitations and deliver a scientifically credible, production-quality v1.0.0 release.

## 3. Resolve the data blocker first

Conduct an independent investigation of the OSF dataset's reuse conditions, the original publication's data availability statement, supplementary materials, applicable licenses and author-provided code.

Determine separately whether the available terms permit:

1. Download and private research.
2. Independent statistical analysis.
3. Publication of disclosure-reviewed aggregate findings.
4. Cross-study patient linkage.
5. Publication of trained model artifacts.

Do not assume that public accessibility grants unrestricted rights. Equally, do not assume that the absence of an explicit license automatically prohibits every form of analysis. Investigate the applicable terms carefully and document the evidence.

Identify the corresponding authors and verify their professional contact information. Prepare a ready-to-send permission request. Do not send correspondence without authorization.

In parallel, independently search for alternative real-world randomized healthcare outreach datasets with clearer reuse terms.

Prioritize datasets containing:

- Randomized intervention assignments.
- Pretreatment patient characteristics.
- Preventive-care or patient-engagement outcomes.
- Known assignment probabilities.
- Multiple outreach strategies or channels.
- Adequate sample sizes.
- Explicit research and publication permissions.

Inspect actual files, documentation and licensing wherever possible.

Do not merely provide another list of possible datasets. Produce a verified feasibility comparison and recommend the strongest usable option.

If the original dataset remains blocked, pursue a scientifically defensible alternative without changing the project's fundamental business objective.

## 4. Complete the real-data research

Once appropriate permissions and data integrity are established:

- Download and verify the actual trial payloads against pinned hashes.
- Inspect schemas, randomization, eligibility and outcome definitions.
- Reproduce published treatment-effect estimates.
- Investigate post-randomization exclusions and missing outcomes.
- Finalize and lock the pre-analysis protocol.
- Estimate average and heterogeneous treatment effects.
- Compare risk-based, uniform and benefit-based targeting.
- Implement and validate appropriate causal ML methods.
- Evaluate policies at matched outreach capacities.
- Perform temporal backtesting where study comparability permits.
- Investigate randomized outreach-channel effectiveness.
- Develop transparent cost-effectiveness scenarios.
- Perform subgroup, uncertainty and sensitivity analyses.

Use strong statistical baselines, known randomization probabilities, cross-fitting, appropriate confidence intervals, multiplicity corrections and leakage prevention.

Validate estimators against established reference implementations where feasible.

Do not force advanced models to outperform simpler rules. Negative, mixed and inconclusive results are valid research outcomes.

## 5. Strengthen AI Engineering

Expand the trial document intelligence subsystem into a properly evaluated AI engineering component.

Build a frozen benchmark covering approximately 25–30 diverse public clinical trials, subject to document availability.

Compare:

- Structured registry extraction.
- Deterministic document parsing.
- Local open-weight LLM extraction.
- Hybrid extraction with evidence verification.

Evaluate field-level accuracy, evidence support, schema validity, abstention, hallucinations, latency and computational requirements.

Use local inference at zero additional service cost. Select the model based on measured performance and available hardware, not popularity.

Retain AI assistance only where it demonstrates meaningful value. If deterministic extraction remains superior, document that outcome.

Do not add a generic chatbot or unnecessary multi-agent orchestration.

## 6. Strengthen ML Engineering

Complete the reproducible batch training and evaluation pipeline.

Include:

- Versioned data and feature contracts.
- Frozen training and evaluation configurations.
- Model artifacts and experiment manifests.
- Model-selection controls.
- Temporal validation.
- Statistical correctness tests.
- Reproducible environments.
- Automated quality gates.
- Safe public artifact generation.

Maintain separation between restricted research data and public application assets.

The project must demonstrate actual ML training, validation and engineering rather than only statistical calculators.

## 7. Upgrade the existing production application

Preserve the current premium UI and overall visual identity.

Once validated research artifacts are available, integrate them into:

- Patient Targeting.
- Outreach Planner.
- Pilot Designer.
- Trial Evidence Explorer.
- Model Validation and Research Results.

Replace fictional research comparisons with verified empirical results wherever permitted. Retain clearly labeled fictional scenarios for interactive demonstrations.

Improve visual hierarchy, usability, accessibility and performance where genuinely necessary.

Follow a less-is-more design philosophy. Avoid excessive cards, gradients, decorative charts, unnecessary navigation and generic AI aesthetics.

Use Healthcare Payment Integrity as a quality reference, not a template to copy.

Do not prioritize additional cosmetic features over unresolved scientific work.

## 8. Autonomous execution and persistent progress

Work independently through all feasible milestones without requesting routine approvals.

Whenever a dependency is blocked, continue other legitimate work instead of stopping the entire project.

Maintain and synchronize:

- progress.md
- PROJECT_STATE.json
- PLANS.md
- DECISIONS.md
- CHANGELOG.md
- Research logs.
- Experiment manifests.
- Architecture decision records.

Record every meaningful change, verified result, failed experiment, unresolved blocker and exact next action.

Ensure both Claude Code and Codex can resume from the same repository without relying on conversation history.

Commit verified milestones incrementally. Preserve existing Git history and the previous production release.

## 9. Cost, security and deployment

Maintain $0 additional external service expenditure.

Use local computation, open-source software, existing GitHub and Cloudflare accounts, and Cloudflare Pages Free.

Do not enable paid APIs, cloud GPUs, paid hosting or additional subscriptions.

Never publish restricted patient data, unauthorized derived artifacts, credentials or private research files.

Run comprehensive scientific, Python, frontend, accessibility, security and browser tests.

Perform an independent release audit before deployment.

Deploy the approved production build to the existing Cloudflare Pages project and verify the actual live application.

Do not create a redundant production website.

## 10. Final deliverables

Complete:

- Real-data research report, where permitted.
- Causal ML model evaluation.
- Temporal validation and channel analysis.
- Statistical power and pilot-design tools.
- AI extraction benchmark.
- Reproducible ML pipeline.
- Premium production application.
- Comprehensive technical master guide.
- Architectural diagrams.
- Model cards and limitations.
- Test evidence and production screenshots.
- Release audit.
- Updated README and portfolio presentation.
- Verified resume bullet points.
- Technical interview preparation guide.
- Complete cross-agent handoff documentation.

Release v1.0.0 only when the mandatory scientific, engineering, privacy and publication gates pass.

If permissions or other genuine external blockers prevent completion, publish only the permitted scope under an appropriate demo or prerelease version. Never represent incomplete empirical research as completed.

## Begin execution

Recover the existing project state and immediately prioritize dataset feasibility and permissions.

Continue all independent statistical validation, AI evaluation and ML engineering tasks while resolving external dependencies.

Do not return another conceptual plan instead of implementing the project.

The goal is to transform Patient Outreach Optimization from a polished software demonstration into a rigorous, differentiated healthcare AI and causal ML flagship project suitable for AI Engineer, Data Scientist and Machine Learning Engineer applications, particularly at Cotiviti and major healthcare organizations.

Proceed independently, maintain scientific honesty, and complete the maximum feasible scope without additional service costs.