# Architecture

```mermaid
flowchart LR
  Analyst --> Workspace["Static React workspace"]
  Sources["Trial article / registry"] --> Reviewed["Reviewed evidence summaries"]
  Reviewed --> Workspace
  Fiction["Seeded fictional RCT"] --> Train["Train and freeze policy"]
  Train --> Eval["Independent fictional holdout"]
  Eval --> Reports["Research run artifacts"]
  OSF["OSF metadata"] --> Verify["Compare pinned file size and SHA-256"]
  Verify -. "Rights required for payloads" .-> Restricted["Ignored local storage"]
  Workspace --> Build["Vite build"]
  Build --> Gate["Allowlist and browser verification"]
  Gate --> Pages["Cloudflare Pages static assets"]
```

Python implements known-propensity estimators, prospective sample size, deterministic metadata extraction, a local model smoke runner and acquisition. Browser TypeScript computes planner, targeting and pilot results without a network service. Public study evidence is reviewed source material. Experiment artifacts remain outside the web build. Production requires the artifact allowlist, claim review and live tests.
