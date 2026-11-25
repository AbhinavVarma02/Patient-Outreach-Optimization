# Threat model

The main risks are accidental inclusion of participant records, substitution or corruption of an input dataset, creating unsupported causal claims, and executing instructions contained in source documents. Public input assumptions are numeric and in memory. React escapes display text. There is no inference endpoint, data upload, tracking, server-side workflow, session identifier or runtime third-party request. The browser policy denies outbound connections and limits scripts and styles to same-origin assets.

Pinned acquisition validates input paths and IDs, verifies sizes and hashes, and accepts only exact named archive members through bounded streaming. Mismatches are quarantined under ignored storage. Rights checks and filesystem permissions are operational barriers. A supplied rights record must cite an actual verified permission basis.

The experimental document tool accepts bounded sections, sends them only to local inference, and requires exact evidence and deterministic corroboration. The static application contains reviewed summaries. Local research collaborators are responsible for access to restricted storage and independent release review. There is no claim of regulated clinical use or HIPAA certification.
