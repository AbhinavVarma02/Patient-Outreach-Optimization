# Test evidence

- Python 3.13.2 ran 13 known-answer, failure-handling, acquisition, model-freeze and evidence validation checks. Python source compilation passed.
- Node 24 ran three calculator tests. Strict TypeScript checking and Vite build passed. The standard pilot fixture agrees with the independent Python implementation.
- npm audit reported zero known vulnerabilities for the locked dependency graph at the time of the check.
- OSF API provided matching name, size and SHA-256 metadata for all 20 pinned entries.
- Fictional experiment outputs, analytic pilot simulations and the local extraction trial are tracked under research/reports.

Initial browser runs encountered a port collision, absent pinned engines, and workflow failures in label lookup and WebKit keyboard behavior. The dedicated loopback port, pinned engine installation, field names and browser key handling were adjusted.

The final local production build passed nine Playwright tests across Chromium, Firefox and WebKit. The matrix exercised five views at 1440×900, 1280×800, 768×1024 and 390×844 in both themes. It checked layout and requests, keyboard activation, theme persistence, scenario recomputation and axe WCAG A/AA rules. Automated accessibility checks are scoped to the selected rules.
