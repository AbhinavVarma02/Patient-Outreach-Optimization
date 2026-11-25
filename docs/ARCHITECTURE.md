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
  Haryana["Pinned CC BY 4.0 archive"] --> Contract["Validate village panel and feature join"]
  Contract --> Figure["Replicate Figure 4 and stress-test variance"]
  Contract --> Geo["Split matched sub-centers by PHC"]
  Geo --> Frozen["Fit ridge on training PHCs and freeze"]
  Frozen --> Score["Evaluate fixed policies in held-out PHCs"]
  Score --> Aggregate["Review and project aggregate summaries"]
  Figure --> Aggregate
  Aggregate --> Workspace
  Workspace --> Build["Vite build"]
  Build --> Gate["Allowlist and browser verification"]
  Gate --> Pages["Cloudflare Pages static assets"]
```

Python implements known-propensity estimators, prospective sample size, deterministic metadata extraction, a frozen local model benchmark and acquisition. Browser TypeScript computes planner, targeting and pilot results without a network service. The checked Haryana JSON projection is the only empirical pipeline input to the web build. Complete experiment artifacts and fitted parameters remain outside that build. Production requires the artifact allowlist, claim review and live tests.

```mermaid
sequenceDiagram
  participant R as Frozen source manifest
  participant P as Local PDF and registry parser
  participant L as Local Ollama runtime
  participant V as Evidence verifier
  participant E as Benchmark evaluator
  R->>P: Hashes, locators and permitted fields
  P->>E: Structured and deterministic baseline outputs
  P->>L: Selected public PDF pages
  L->>V: Proposed field and exact excerpt
  V->>E: Corroborated value or abstention
  E->>E: Score against held-out annotations
```
