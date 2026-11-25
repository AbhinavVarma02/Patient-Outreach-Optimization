# Patient Outreach Optimization

An independent research workspace for preventive-care teams evaluating which outreach strategies merit a randomized pilot. Clinical risk predicts an outcome. The outreach decision also depends on whether the intervention changes it.

[Open the live workspace](https://patient-outreach-optimization.pages.dev/)

**Limited research demonstration.** The app includes published Geisinger evidence and an independent replication on the CC BY 4.0 Haryana immunization trial. In 902 villages, assigning information-hub ambassadors was associated with 1.89 additional recorded measles vaccinations per village-month under the published weighting. The primary-health-center interval spans zero. An exploratory 42-village holdout did not establish a gain over uniform allocation. The patient targeting, channel cost and power tools use fictional inputs. [Haryana findings and limits](docs/HARYANA_RESEARCH.md)

The Geisinger inventory covers four trials and all 20 public file metadata entries match. Independent participant-level analysis awaits verified reuse rights. A 30-trial held-out benchmark found no benefit from enabling the tested local model with evidence verification. [Data rights](docs/LICENSING.md) · [AI evaluation](docs/AI_EVALUATION.md)

![Production overview of the Patient Outreach Optimization workspace](docs/images/overview.png)

```sh
python -m unittest discover -s tests
python -m patient_outreach
cd web
npm ci --ignore-scripts
npm run dev
```

Read the [technical guide](docs/MASTER_TECHNICAL_GUIDE.md), [study cards](docs/DATA_CARD.md), [experiment reports](docs/EXPERIMENT_REPORT.md), [limitations](docs/LIMITATIONS.md) and [test evidence](docs/TEST_EVIDENCE.md). [Progress](progress.md) records the latest verification and blockers. [Input reconciliation](research/INPUT_RECONCILIATION.md) records the archive and the v1.0 governing scope.
