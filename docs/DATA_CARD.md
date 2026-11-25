# Data and estimand cards

The pinned historical inventory reports expected archive records: 46,602 full / 38,598 analysis for Study 1, 45,061 / 42,481 for Study 2, 40,671 / 39,129 for Study 3, and 43,225 / 42,709 for Study 4. SHA-256 values and file sizes are stored in research/manifests/osf_mqbux_manifest.json. Records are not unique people. No participant outcomes were downloaded for analysis in this workspace.

| Study | Published design | Target primary contrast for replication | Checks still required |
| --- | --- | --- | --- |
| 1 · NCT04323137 | Top clinical-risk decile, passive control and three disclosure arms. Eligible modalities delivered the assigned content. | Assigned risk disclosure versus no study outreach and original author arm contrasts. Season-long vaccination outcome, with authors' analysis criteria. | Confirm randomization strata and probabilities, risk-band semantics, exclusions and endpoint fields. |
| 2 · NCT05009251 | Top clinical-risk decile, passive control, general reminder and three disclosure arms. | Assigned disclosure versus passive control and versus reminder. Primary outcome at 8 weeks + 1 day from study start. | Verify dates, consent modalities, post-randomization exclusions and shared-address flags. |
| 3 · NCT05509283 | Clinical-risk percentiles 11–20, five content arms, six-week primary endpoint. | Assigned disclosure versus passive control and versus active reminder where stipulated. | Establish treatment version, eligibility timing, assignment design and comparability before any temporal evaluation. |
| 4 · NCT05509270 | Modality trial. The fully channel-eligible primary analysis includes 29,186 people, across letter, portal, SMS, portal + SMS, all three and passive control. | Within the primary eligibility stratum, assigned bundle versus passive control for 29-day vaccination. Reproduce authors' model and document secondary comparisons. | Validate assignment probabilities by eligibility, date discrepancy, exclusions and reasons the 42,709 file rows differ from the primary sample. |

No inferred household ID. The supplement reports repeated trial participation. Linkage needs explicit authorization and verified identifier semantics. Full-population sensitivities require outcome-availability and attrition analysis.

Sources are documented in [research/SOURCES.md](../research/SOURCES.md).
