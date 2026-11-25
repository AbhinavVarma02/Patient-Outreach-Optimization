# Licensing and permission status

Reviewed 2026-11-24. The OSF API reports `mqbux` as public with a null license relationship. All 20 pinned names, sizes and SHA-256 metadata matched. The authors describe the deposited records and scripts as materials for reproducing the paper. Vaccination timing is shared by experimental condition because exact dates were withheld. The OSF catalog lists one analysis notebook for each study, including `Study_4_2026-04-17.Rmd`. Its Study 4 filters still require review. The authors’ supplement includes the nudge text in §11.1, Supplementary Table 41. [Publisher statements](https://www.nature.com/articles/s41562-026-02603-4?error=cookies_not_supported#data-availability) · [OSF metadata](https://api.osf.io/v2/nodes/mqbux/) · [Author supplement](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41562-026-02603-4/MediaObjects/41562_2026_2603_MOESM1_ESM.pdf)

OSF’s terms distinguish public access and limited use under its terms from extra permissions a depositor can grant through a license. Public deposition and the authors’ reproduction statement support access for the stated purpose. The terms also treat unlicensed deposits as copyrighted by default. The project will obtain a written basis for the intended participant-level work before payload acquisition. [OSF terms, §8](https://osf.io/terms-of-use/) · [OSF licensing guidance](https://help.osf.io/article/148-licensing)

| Proposed use | Evidence and project decision |
| --- | --- |
| Download and private research | Public access and the stated reproduction purpose are documented. Obtain confirmation that private local storage and the proposed follow-on research are permitted. |
| Independent statistical analysis | The statement supports reproducing the publication. Authorization for the project’s planned independent targeting and policy analyses remains unresolved. |
| Publish disclosure-reviewed aggregates | The application can cite the authors’ published findings. Obtain authorization for new data-derived tables and results and complete the disclosure review. |
| Link records across studies | Confirm whether IDs recur, what they represent, and whether the data steward permits linkage for dependence assessment. |
| Publish trained artifacts | Establish explicit permission and assess disclosure risk before considering release. Keep weights and row-level outputs private. |

The software license excludes third-party data, code and source materials. For the separately licensed Haryana replication archive, see the [dataset feasibility review](../research/DATASET_FEASIBILITY.md).

## Geisinger correspondence

On 2026-11-25 the project owner reported sending the permission request and receiving an out-of-office response. There is no substantive authorization on record. No duplicate request was sent and no Geisinger participant payload was acquired. The text below is the repository's preparation copy. No private email or reply is stored here.

**To** Christopher F. Chabris, `cfchabris@geisinger.edu`. The article identifies Dr. Chabris as the corresponding author and Geisinger lists this institutional address. [Publisher correspondence](https://www.nature.com/articles/s41562-026-02603-4?error=cookies_not_supported#author-information) · [Geisinger faculty directory](https://www.geisinger.org/-/media/onegeisinger/pdfs/ghs/education-gcsom/faculty-affairs/faculty-directory-040826.pdf?sc_lang=en)

**Subject** Reuse of Geisinger influenza outreach trial data from OSF mqbux

Dear Dr. Chabris,

I’m writing about the deidentified influenza outreach trial data you deposited at OSF mqbux for your Nature Human Behaviour article (DOI 10.1038/s41562-026-02603-4). Patient Outreach Optimization is an independent, open-source research project studying whether randomized outreach evidence can inform targeting and pilot design.

Could you confirm the applicable license or data-use agreement, and whether it allows local downloading and storage, replication of the published estimates, new independent analyses of outreach targeting and channel assignment, and publication of disclosure-reviewed aggregate findings with source code? Participant records and row-level derivatives would be kept private.

If deidentified IDs recur across studies, could you clarify what they represent and whether linkage solely to assess sample dependence is allowed? Is release of trained model parameters ever permitted after disclosure review, or should those remain private? Could you also identify the Study 4 script and data files corresponding to the primary fully channel-eligible 29-day analysis?

Thank you for clarifying the permitted uses and preferred citation. If Geisinger handles these requests through a data steward or review process, a referral would be appreciated.

## Continuation verification

The OSF API again returned a public project with `attributes.node_license` equal to null, and all 20 pinned metadata entries matched. The requested rights to new secondary analyses, derived aggregate publication, linkage and model export remain unresolved. The deposited participant files were left untouched. The study article's research-reproduction statement and the absence of a reuse license are separate pieces of evidence. [OSF node](https://api.osf.io/v2/nodes/mqbux/) · [Publisher data availability](https://www.nature.com/articles/s41562-026-02603-4#data-availability) · [OSF licensing guidance](https://help.osf.io/article/148-licensing)

The public OSF storage catalog contained no filename matching a license, terms document or README. Read the authors' Study 4 notebook as text. Its primary Figure 5 code subsets the analysis payload to all-channel-eligible participants, contrasts six assigned modalities and uses the precomputed `vaccinated` flag. The notebook references author-local RDS files while the deposit pins CSVs. The 29-day window is documented by the supplement. Audit the correspondence between definitions and deposited bytes after authorization. [OSF manuscript catalog](https://api.osf.io/v2/nodes/mqbux/files/osfstorage/6a064485ed0692607d7831a1/)

Haryana and its companion replication archive are CC BY 4.0. Published project results attribute the authors, identify the pinned data deposit and describe the transformations. The Sierra Leone feasibility deposit is CC0 1.0. Study materials and data are licensed separately from this repository's original software. [Haryana data card and attribution](HARYANA_RESEARCH.md) · [Feasibility sign-off](../research/DATASET_FEASIBILITY.md#companion-and-alternative-datasets)

On 2026-11-25, the metadata-only verification again matched all 20 Geisinger entries. Reuse remains unresolved after the owner's request and the out-of-office reply. The continuation used the independently licensed Sierra Leone files. [Sierra Leone source and scope](SIERRA_LEONE_RESEARCH.md)
