# Approved production UI

The project owner approved the visual design of `v0.1.0-demo`, deployed from `d988063bb75e2870ad8e26e2edf316919d81c6d6`. The interface is a restrained healthcare research workspace. Keep its visual identity and existing workflow as the application gains validated research and functionality. Make visible changes only when they serve functionality, accessibility or usability. [Production application](https://patient-outreach-optimization.pages.dev/) · [Approved deployment](https://9112bbb3.patient-outreach-optimization.pages.dev/)

## Design system

| Element | Approved design |
| --- | --- |
| Typography | Georgia with Times New Roman fallback for the main headings and key figures. Segoe UI with system sans-serif fallback for labels, copy, controls and tables. Use the existing fluid heading sizes, quiet uppercase labels and tabular numerals in tables. Fonts are local. |
| Surfaces | Warm ivory canvas and paper in light mode. Deep graphite-green canvas and paper in dark mode. Shaded assumption panels, thin rules and restrained corner radii separate content. |
| Color | Deep green and lime anchor the brand and Overview hero in both themes. Use the theme accent for active navigation, links, focus rings and the principal data series. Use text, values or accessible labels alongside color. |
| Spacing | The masthead, navigation, main and footer align to the shared 1,240 px maximum content width. Page sections start 34 px apart at desktop sizes. Use the existing 15–17 px grid gaps and component padding. At 960 px and 720 px the total side inset reduces from 80 px to 48 px and then 32 px. |
| Navigation | Keep the masthead wordmark and System, Light and Dark selector. Below it, keep Overview, Patient Targeting, Outreach Planner, Pilot Designer and Evidence & Methods in order. Keep the active underline and the existing linked workflow from targeting to planning to pilot design. |
| Layouts | Overview pairs the headline and actions with a fictional risk-band chart, then presents the evidence-status strip, three workflow links and trial summaries. Decision views use an assumption rail beside results, with controls first in the mobile stack. Evidence & Methods uses the trial grid, cited comparisons and expandable methods. |
| Data and inputs | Use the existing tables, restrained SVG charts, metrics, callouts, labels and reset buttons where applicable. Give a decision chart an accessible name and a readable numeric counterpart. Keep `%`, `pp`, counts and USD distinct. Label published evidence, fictional inputs and analytic projections at the point of use. |
| Accessible interaction | Preserve the skip link, focus on the main landmark after route changes, visible focus rings, labeled inputs, keyboard-operable table regions and status messages. Navigation wraps at narrow widths, workbenches and the hero stack at 720 px, and wide tables scroll within their own region. Persist only the theme preference. |

The CSS values and component structure are defined in [web/src/style.css](../web/src/style.css) and [web/src/main.tsx](../web/src/main.tsx).

| Theme tokens | Light | Dark |
| --- | --- | --- |
| `--canvas`, `--paper` | `#f7f6f1`, `#fffefa` | `#161e1b`, `#202a26` |
| `--ink`, `--muted` | `#172a24`, `#4c6258` | `#eff4ec`, `#afc0b7` |
| `--rule`, `--shade` | `#d8dfd5`, `#eaf0e7` | `#3a4c42`, `#26362e` |
| `--accent` | `#21584a` | `#bde593` |
| `--deep`, `--lime` | `#133c32`, `#d0e9a2` | `#133c32`, `#d0e9a2` |

When adding approved research, use the existing Evidence & Methods hierarchy for provenance and methods. Put a result in a decision view only when it answers that workflow’s question. Keep assumptions alongside outputs and use the existing evidence strip, table or callout for limitations and source links.

## Screenshot references

Full-page captures use the pinned Playwright Chromium on Windows, default workflow inputs, 1× device scale, and explicit theme selection. The viewport size is the browser viewport before the full page is captured. All eleven v0.2.0-demo PNGs matched the local production build and the public application byte for byte on 2026-11-24.

The Overview copy now points readers to the Haryana evidence. Evidence & Methods presents the independent community study above the existing Geisinger trial explorer. The new tables wrap row labels on narrow screens to keep numeric columns visible. The five prior screenshots for Targeting, Planner and Pilot match exactly. Navigation, typography, surfaces and workflow structure follow the approved release. The original captures remain in Git history and the prior deployment is available for comparison. [Prior deployment](https://9112bbb3.patient-outreach-optimization.pages.dev/)

| View | Desktop (1440 × 900), light | Mobile (390 × 844), light | Mobile (390 × 844), dark |
| --- | --- | --- | --- |
| Overview | [Reference](images/overview.png) | [Reference](images/overview-mobile-light.png) | [Reference](images/overview-mobile-dark.png) |
| Patient Targeting | [Reference](images/patient-targeting.png) | — | — |
| Outreach Planner | [Reference](images/outreach-planner.png) | — | — |
| Pilot Designer | [Reference](images/pilot-designer.png) | [Reference](images/pilot-designer-mobile-light.png) | [Reference](images/pilot-designer-mobile-dark.png) |
| Evidence & Methods | [Reference](images/evidence-and-methods.png) | [Reference](images/evidence-and-methods-mobile-light.png) | [Reference](images/evidence-and-methods-mobile-dark.png) |

## Reviewing changes

1. Build and run `npm run test:browser -- --workers=1` from `web`. The browser matrix covers all five views in both themes at 1440 × 900, 1280 × 800, 768 × 1024 and 390 × 844. Chromium writes the reference views to `web/qa-output`.
2. On Windows with the pinned Chromium, enable the exact comparison with `$env:OUTREACH_UI_REFERENCE = '1'` in PowerShell and run `npm run test:browser -- --project=chromium`. Set `OUTREACH_LIVE_URL` to run against production. The test reports which comparison failed and retains the new capture for inspection. On other rendering environments, compare the captures visually.
3. Review any difference at the affected viewport and theme. Record the intended functionality, accessibility or usability change and its visual effect during review. Update the affected references from the verified production release when that change ships. Keep captures in `docs/images` and out of the deployable web directory. [Browser checks](../web/tests/workspace.spec.ts) · [Test evidence](TEST_EVIDENCE.md)
