# Test evidence

- Python 3.13.2 ran 13 known-answer, failure-handling, acquisition, model-freeze and evidence validation checks. Python source compilation passed.
- Node 24 ran three calculator tests. Strict TypeScript checking and Vite build passed. The standard pilot fixture agrees with the independent Python implementation.
- npm audit reported zero known vulnerabilities for the locked dependency graph at the time of the check.
- OSF API provided matching name, size and SHA-256 metadata for all 20 pinned entries.
- Fictional experiment outputs, analytic pilot simulations and the local extraction trial are tracked under research/reports.

Initial browser runs encountered a port collision, absent pinned engines, and workflow failures in label lookup and WebKit keyboard behavior. The dedicated loopback port, pinned engine installation, field names and browser key handling were adjusted.

The final local production build passed nine Playwright tests across Chromium, Firefox and WebKit. The matrix exercised five views at 1440×900, 1280×800, 768×1024 and 390×844 in both themes. It checked layout and requests, keyboard activation, theme persistence, scenario recomputation and axe WCAG A/AA rules. Automated accessibility checks are scoped to the selected rules.

The same nine tests passed on the public production domain. The production overview, mobile dark theme, planner and pilot screenshots are in [docs/images](images/). The compiled JavaScript is 77.53 kB gzip and the compiled CSS is 3.18 kB gzip. These are build sizes, not measured page-load latencies. [Verified initial GitHub Actions run](https://github.com/AbhinavVarma02/Patient-Outreach-Optimization/actions/runs/45539352114)

Ruff 0.15.0 passed for the Python source and tests. Mypy 1.19.0 reported no issues in 10 checked source files. Chromium compared the four public assets byte for byte with the [build ledger](../research/reports/public_build_sha256.json) and verified response security headers. The Pages control file is hashed locally and validated through those response headers.

The continuation checkpoint reran all 13 Python tests, three Node calculator tests and all nine Playwright tests on the local and production builds. The exact opt-in Chromium comparison passed all nine captures on Windows. The local build reproduced all five build-ledger hashes and the live check again verified the four public assets and headers. An initial sandboxed attempt could not resolve production DNS and a local preview held the test port. The read-only HTTPS check and the restarted loopback test then passed. [Approved design and capture workflow](UI_DESIGN.md)

The Haryana reproduction command passed both locked publication-rounding checks. The coefficient and CR0 standard error agreed with statsmodels to an absolute tolerance of `1e-10`. A run with an unrelated file failed at the archive checksum gate. Ruff 0.15.0 passed on the Python sources, tests and scripts. [Experiment report](EXPERIMENT_REPORT.md#haryana-figure-4-replication)

## v0.2.0-demo local verification

- Seventeen Python tests, Ruff, mypy and Python compile checks passed. Three Node calculator tests and strict TypeScript passed.
- The pinned archive yielded the same independent WLS point results and statsmodels covariance checks. The community policy validation includes observed non-nominal finite-sample coverage and interference bias. See [Haryana results](HARYANA_RESEARCH.md).
- Thirty public trials and 35 document checks completed with the pinned local model. The prespecified release criteria for model assistance failed. See [AI evaluation](AI_EVALUATION.md).
- Twelve browser tests passed across Chromium, Firefox and WebKit on Windows with one worker. The suite exercises all five views in four viewports and two themes, keyboard workflows, accessibility and source/claim presentation. An earlier unpinned run lacked browser executables, and an initial parallel run hit one Chromium screenshot capture failure. Pinned engines and serial execution recovered.
- npm audit and OSV batch queries for the ten pinned Python research and PDF dependencies returned zero advisories at verification time. Static asset content and the five-file deployment allowlist passed.

## v0.2.0-demo production verification

- The release source passed the 108-path staged publication scan. GitHub ran its Python, Node, static build and Chromium gates successfully on the deployed commit. [CI run](https://github.com/AbhinavVarma02/Patient-Outreach-Optimization/actions/runs/45544473794)
- All 12 public browser tests passed on Chromium, Firefox and WebKit. The four served assets matched the release ledger and carried the checked CSP, HSTS and nosniff headers. The site initiated no external requests across the tested views. [Production](https://patient-outreach-optimization.pages.dev/) · [Build digests](../research/reports/public_build_sha256.json)
- Eleven captured views matched byte for byte locally and live. Five prior workflow screenshots remain byte-identical. Overview and Evidence & Methods reflect the new research and the narrow-screen table fix. The new build size is 78.56 kB JavaScript and 3.19 kB CSS gzip. [Screenshot references](UI_DESIGN.md#screenshot-references)
- After promotion, the original deployment served all four original public assets with the original hashes. [Previous deployment](https://9112bbb3.patient-outreach-optimization.pages.dev/)

## v0.3.0-demo verification · 2026-11-25

- Seventeen Python tests, Ruff, mypy on 21 source files, bytecode compilation and both public projection checks passed. Sierra Leone reproduced all five locked point estimates and standard errors. Statsmodels reference, exact enumeration and 10,000-draw community inference checks passed. The extractor's accuracy gate failed on the frozen holdout. [Study and artifacts](SIERRA_LEONE_RESEARCH.md) · [Extraction evaluation](AI_EVALUATION.md)
- Three Node tests, strict TypeScript, Vite build and all 12 Playwright tests passed locally and in production. Chromium, Firefox and WebKit exercised four viewports in both themes, interactive workflows, axe WCAG A/AA checks, trial evidence labels and no unexpected requests. All 11 production captures matched the local build. Five workflow captures also matched v0.2.0-demo. The compiled JavaScript is 79.61 kB and CSS is 3.19 kB gzip. [Screenshot references](UI_DESIGN.md)
- The 128-path staged source scan, five-file build allowlist and disclosure review passed. npm audit and scoped OSV queries for 13 pinned research and PDF dependency versions reported zero advisories. The four HTTPS-served assets matched the ledger and security header checks on the stable and immutable v0.3.0 URLs. Both previous production deployments also matched their release-specific asset hashes and remained eligible rollback targets. [CI run for the deployed commit](https://github.com/AbhinavVarma02/Patient-Outreach-Optimization/actions/runs/45631462871) · [Artifact ledger](../research/reports/public_build_sha256.json) · [Deployment and rollback evidence](DEPLOYMENT.md)

## v0.4.0-demo release candidate · 2026-11-25

- Seventeen Python tests, Ruff, mypy across 23 source files, compilation, known-answer inference, and all three public projection checks passed. The pinned Sierra Leone replication reproduced the previous report. The frozen village policy replay differed only in runtime metadata. Haryana estimates reproduced within numerical tolerance using a newer numerical stack. Its historical source and protocol pins remain tied to the earlier checkpoint. The full community-inference report reproduced exactly. [Reproducibility](REPRODUCIBILITY.md)
- Four Node tests, TypeScript and 15 local Playwright tests passed. Chromium, Firefox and WebKit exercised four viewports in both themes, keyboard and focus behavior, the payer workflow, and the configured automated axe WCAG A/AA rules. No test reported page errors or unexpected network requests. The static output size was 82.00 kB JavaScript and 3.22 kB CSS gzip.
- npm audit and OSV checks for 19 pinned Python package versions reported zero advisories. The five-file static build allowlist passed. Production v0.3.0-demo matched its committed HTTPS ledger before promotion. [Build ledger](../research/reports/public_build_sha256.json)
- The final AI extraction gate failed as recorded on the independent holdout. Statistical and application tests passing does not change that research outcome. [Final extraction results](AI_EVALUATION.md)
