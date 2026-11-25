# Patient Outreach Optimization

An independent research workspace for preventive-care teams evaluating which outreach strategies merit a randomized pilot. Clinical risk predicts an outcome. The outreach decision also depends on whether the intervention changes it.

[Open the live workspace](https://patient-outreach-optimization.pages.dev/)

**Limited research demonstration.** The app presents published evidence and fictional scenarios. It offers matched-capacity targeting, channel cost and eligibility planning, and statistical power for a randomized comparison of frozen policies. The source inventory covers four Geisinger trials. OSF's public checksum metadata matches the 20 pinned files. Independent participant-level replication remains on hold pending verified reuse rights.

![Production overview of the Patient Outreach Optimization workspace](docs/images/overview.png)

```sh
python -m unittest discover -s tests
python -m patient_outreach
cd web
npm ci --ignore-scripts
npm run dev
```

Read the [technical guide](docs/MASTER_TECHNICAL_GUIDE.md), [study cards](docs/DATA_CARD.md), [fictional experiments](docs/EXPERIMENT_REPORT.md), [limitations](docs/LIMITATIONS.md) and [test evidence](docs/TEST_EVIDENCE.md). [Progress](progress.md) records the latest verification and blockers. [Input reconciliation](research/INPUT_RECONCILIATION.md) records the archive and the v1.0 governing scope.
