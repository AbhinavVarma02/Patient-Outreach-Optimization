# Project progress

2026-11-24 · Limited research demonstration published

- The authoritative v1.0 contract was copied byte for byte. Reviewed all four source inputs and archived their unchanged originals locally. The independent review identifies itself as v0.2.
- Git main holds the bootstrap and the 16cc9ed pre-analysis protocol, tagged research-protocol-v1. The production build is from d988063bb75e2870ad8e26e2edf316919d81c6d6. Use git log for the latest handoff checkpoint.
- All 20 metadata entries match the pinned names, lengths and SHA-256 values. No trial payload download or participant-level work. Analysis, linkage and aggregate-publication rights remain unresolved.
- Fictional holdout, fixed-policy coverage, prospective pilot and local extraction smoke artifacts are under research/reports. The supplied oracle simulation was reproduced.
- Thirteen Python tests, three Node tests, strict TypeScript, Ruff and mypy passed. Nine Playwright tests passed locally and nine passed on production. The staged source and the five-file application passed publication scans. See docs/TEST_EVIDENCE.md.
- The repository is public on [GitHub](https://github.com/AbhinavVarma02/Patient-Outreach-Optimization). [Cloudflare Pages production](https://patient-outreach-optimization.pages.dev/) deployment ID is 9112bbb3-551f-4d76-b7a4-df4e99b1b976. Additional external service expenditure is $0. Production screenshots are under docs/images.
- The release uses a Vite static build, React and browser-local TypeScript calculations. Python handles data provenance, estimators, fictional experiments and trial metadata extraction. No patient-level material or model weights are served.
- Open real-data work includes approved payload acquisition, study-specific schema and design reconciliation, RQ0 replication, adjusted and cross-fit estimation, temporal evaluation, subgroup fairness and disclosure review, and aggregate publication rights. The local extractor remains experimental pending a multi-trial held-out benchmark.

## v1.0.0 continuation checkpoint

- Preserved the owner’s [continuation brief](CONTINUATION_V1.md) and recorded the approved design in [docs/UI_DESIGN.md](docs/UI_DESIGN.md). Nine production references match the local build byte for byte. All nine browser tests passed locally and live with exact comparison enabled for Chromium. The five-file local build matched the release ledger and the four served assets and security headers were verified again over HTTPS.
- Rechecked all 20 Geisinger OSF metadata entries and located the authors’ scripts and message supplement. The reuse basis is still open. See the [unsent permission request](docs/LICENSING.md) with the verified corresponding-author contact.
- Verified the openly licensed Haryana immunization package against the deposit checksum and inspected its CSV headers and counts. The prepared analysis file has 28,903 village-month records. The [feasibility review](research/DATASET_FEASIBILITY.md) records the separate cluster-level scope and locks the first independent check against published Figure 4.
- The independent Haryana check passed both published rounding targets, 1.89 additional measles vaccinations per village-month for information-hub ambassador assignment and a pure-control mean of 7.32. The sample covers 7,370 village-months. Statsmodels agreed with the coefficient and CR0 standard error to `1e-10`. See the [experiment report](docs/EXPERIMENT_REPORT.md#haryana-figure-4-replication) and [run artifact](research/reports/haryana_figure4_replication.json). Design-based uncertainty remains open. The production app serves the limited demo.

## Resume

Reconcile Haryana assignment probabilities, cluster levels, the published interval and eligible intervention combinations before freezing a policy analysis. For Geisinger, use the [unsent permission draft](docs/LICENSING.md) and follow the [protocol](docs/RESEARCH_PROTOCOL.md) after documenting the reuse basis. Run `python -m patient_outreach.acquisition` for metadata verification, `python -m unittest discover -s tests -v` for Python tests and `npm run build`, `npm run release:check` and `npm run test:browser` under web. Use `node scripts/verify-live.mjs` under web for the production checksums and headers. See the [release audit](docs/RELEASE_AUDIT.md).
