# Architecture

```mermaid
flowchart LR
  Analyst --> Workspace["Static React workspace"]
  Sources["Trial article / registry"] --> Reviewed["Reviewed evidence summaries"]
  Reviewed --> Workspace
  CMS["CMS contract table + technical notes"] --> US["Pinned aggregate exporter"]
  Registry["UCLA posted results + SCORE Table 2"] --> US
  US --> Workspace
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
  SL["CC0 Sierra Leone originals"] --> Match["Whole matched triplets"]
  Match --> Fit["Train ridge T and DR learners and freeze"]
  Fit --> Holdout["Evaluate disjoint triplets and check inference"]
  Holdout --> Aggregate
  Aggregate --> Workspace
  Workspace --> Build["Vite build"]
  Build --> Gate["Allowlist and browser verification"]
  Gate --> Pages["Cloudflare Pages static assets"]
```

Python implements known-propensity estimators, prospective sample size, deterministic metadata extraction, a frozen local model benchmark and acquisition. Browser TypeScript computes targeting, campaign cost, CMS benchmark gap and pilot results without a network service. The build reads the checked Haryana, Sierra Leone and US JSON projections and reviewed trial summaries. The CMS benchmark is an arithmetic reference. Randomized trial values are a separate evidence path. [US data lineage](US_PAYER_EVIDENCE.md) · [Model artifacts](MODEL_CARD.md)

```mermaid
sequenceDiagram
  participant R as Frozen source manifest
  participant P as Local PDF and registry parser
  participant L as Local Ollama runtime
  participant V as Evidence verifier
  participant E as Benchmark evaluator
  R->>P: Hashes, locators and permitted fields
  P->>E: Structured and deterministic baseline outputs
  P->>L: Bounded numbered excerpts from supplied PDF pages
  L->>V: Enumerated value and excerpt index
  V->>E: Corroborated value or abstention
  E->>E: Score against held-out annotations
```

## Static release boundary

```mermaid
flowchart LR
  subgraph Local["Local research workspace"]
    Inputs["Verified inputs in ignored storage"] --> Research["Analysis and local evaluation"]
    Research --> Private["Private fitted parameters and row-level data"]
    Research --> Review["Rights, methods and disclosure review"]
  end
  Review --> Aggregate["Versioned aggregate projections"]
  Aggregate --> Git["Intended GitHub repository"]
  Git --> CI["Synthetic and static CI checks"]
  Aggregate --> Dist["Five-file static Vite build"]
  Dist --> Allowlist["File and outbound URL allowlist"]
  CI --> Release["Verified release commit"]
  Allowlist --> Release
  Release --> Pages["Existing Cloudflare Pages Direct Upload"]
  Pages --> Stable["Stable URL and immutable deployment"]
  Stable --> Check["HTTPS hashes, headers, browser matrix"]
```
