# Patient Outreach Optimization

An independent research workspace for preventive-care teams evaluating which outreach strategies merit a randomized pilot. Clinical risk predicts an outcome. The outreach decision also depends on whether the intervention changes it.

[Open the live workspace](https://patient-outreach-optimization.pages.dev/)

**Limited research demonstration.** In Sierra Leone, mobile vaccination plus community mobilization increased recorded adult uptake by 26.1 percentage points. The extra visit estimate was −1.1 points and its interval crossed zero. Two trained causal models showed no reliable lift over uniform village allocation in a held-out comparison. Haryana's separate replication reproduced 1.89 additional recorded measles vaccinations per village-month with published weighting. The interval with primary-health-center clustering crossed zero. The patient targeting, channel cost and power tools use fictional inputs. [Sierra Leone study card](docs/SIERRA_LEONE_RESEARCH.md) · [Haryana findings](docs/HARYANA_RESEARCH.md)

All 20 Geisinger metadata entries match. Independent participant-level analysis awaits documented reuse rights. On 30 new public trial documents, the deterministic parser matched 14 of 30 scorable fields and the verified local model matched 3. Both fell short of the release gate. The app uses reviewed summaries. [Data rights](docs/LICENSING.md) · [AI evaluation](docs/AI_EVALUATION.md)

![Production overview of the Patient Outreach Optimization workspace](docs/images/overview.png)

```sh
python -m unittest discover -s tests
python -m patient_outreach
cd web
npm ci --ignore-scripts
npm run dev
```

Read the [technical guide](docs/MASTER_TECHNICAL_GUIDE.md), [study cards](docs/DATA_CARD.md), [experiment reports](docs/EXPERIMENT_REPORT.md), [limitations](docs/LIMITATIONS.md) and [test evidence](docs/TEST_EVIDENCE.md). [Progress](progress.md) records the latest verification and blockers. [Input reconciliation](research/INPUT_RECONCILIATION.md) records the archive and the v1.0 governing scope.
