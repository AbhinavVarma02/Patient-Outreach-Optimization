# Evidence sources and access log

Checked 2026-11-24 (America/New_York). Links identify the original materials.

| Source | What it supports | Access notes |
| --- | --- | --- |
| [Rosenbaum et al., Nature Human Behaviour](https://pubmed.ncbi.nlm.nih.gov/42834081/) | Three content trials on influenza risk communication | PubMed record opens. Nature landing page encountered an identity redirect. |
| [Authors’ supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41562-026-02603-4/MediaObjects/41562_2026_2603_MOESM1_ESM.pdf) | Study 4 registration, six arms, 29-day endpoint, primary population and published contrasts. Section 6.2 reports trial overlap. | Reviewed relevant sections. Send-year discrepancy within section 7 requires registry reconciliation. |
| [OSF API node](https://api.osf.io/v2/nodes/mqbux/) | Public status and null license metadata | Verified by local HTTPS request. Neither establishes reuse authorization. |
| [OSF file API](https://api.osf.io/v2/files/6a06485c3e3084a367783491/) | Pinned remote filename, byte length and checksum metadata | All 20 match the historical manifest. This check read metadata only. |
| [Study 1 protocol](https://cdn.clinicaltrials.gov/large-docs/37/NCT04323137/Prot_001.pdf) | Four assignments, passive control with usual outreach, season-long vaccination outcome | Protocol. |
| [Study 2 SAP](https://cdn.clinicaltrials.gov/large-docs/51/NCT05009251/SAP_000.pdf) | Five assignments, 8 weeks + 1 day, multiple eligible delivery modalities | SAP. |
| [Study 3](https://clinicaltrials.gov/study/NCT05509283) | Registration for outreach in the lower-risk enrollment band | Use alongside the authors’ results. |
| [Study 4](https://clinicaltrials.gov/study/NCT05509270) | Modality study registration | Distinct from prospective personalization. |
| [NCT06566534 SAP](https://cdn.clinicaltrials.gov/large-docs/34/NCT06566534/SAP_000.pdf) | Later prospective personalization design | Official registry API reports no posted results as of the check. Published outcomes elsewhere remain unverified. |
| [Imai and Li](https://arxiv.org/abs/1905.05389) | Formal experimental evaluation of individualized treatment rules | Do not attribute this repository's fixed-policy SE to their learned-rule evaluation method. |
| [Yadlowsky et al.](https://arxiv.org/abs/2111.07966) | Rank-weighted treatment effect metrics | Candidate for later implementation and reference validation. |
| [Medicaid targeting cohort](https://pubmed.ncbi.nlm.nih.gov/42498943/) | Real-world use case comparing two targeting approaches | Retrospective design. No inference for vaccination from this source. |
| [Cotiviti Engagement Hub](https://www.cotiviti.com/solutions/engagement/engagement-hub) | Commercial member outreach, targeting and quality workflows | Product descriptions do not validate a causal targeting method. |
| [Banerjee et al., Econometrica](https://onlinelibrary.wiley.com/doi/10.3982/ECTA19739) and [replication archive](https://zenodo.org/records/11392582) | Multilevel outreach assignments, camp-recorded outcome, Figure 4 and documented cost modeling | Verified and ran an independent aggregate pipeline. |
| [Chernozhukov et al., Econometrica](https://onlinelibrary.wiley.com/doi/10.3982/ECTA19303) and [replication archive](https://zenodo.org/records/10871241) | Published Haryana village heterogeneity and baseline extensions | Replication payload matches the deposit. Shares the Haryana trial. |
| [Meriggi et al., Nature](https://www.nature.com/articles/s41586-024-07158-w) and [Dataverse archive](https://doi.org/10.7910/DVN/PRXF5Z) | Matched triplets and nested structure assignment with a mobile vaccination rollout | Verified CC0 original files, reproduced five published contrasts and audited the structure lottery. [Replication](../docs/SIERRA_LEONE_RESEARCH.md) |
| [ClinicalTrials.gov](https://clinicaltrials.gov/) | Protocol PDFs, design context and structured endpoints for 30 trials | [Pinned archive locators](manifests/document_holdout.json) include case-level hashes and page references. |

The 2026-11-25 US continuation verified the [2027 CMS tables and technical notes](https://www.cms.gov/medicare/health-drug-plans/part-c-d-performance-data), [UCLA influenza registry results](https://clinicaltrials.gov/study/NCT05525494?tab=results) and [SCORE Table 2](https://doi.org/10.1001/jamanetworkopen.2024.46693). The [US data card](../docs/US_PAYER_EVIDENCE.md) records how the sources were transformed, what can be reported, and which datasets remain gated.
