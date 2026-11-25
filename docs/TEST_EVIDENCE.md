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

The continuation checkpoint reran all 13 Python tests and all nine Playwright tests on the local and production builds. The exact opt-in Chromium comparison passed all nine captures on Windows. The local build reproduced all five build-ledger hashes and the live check again verified the four public assets and headers. An initial sandboxed attempt could not resolve production DNS and a local preview held the test port. The read-only HTTPS check and the restarted loopback test then passed. [Approved design and capture workflow](UI_DESIGN.md)
