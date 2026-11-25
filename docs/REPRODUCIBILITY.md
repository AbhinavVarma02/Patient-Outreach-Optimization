# Reproducibility

Use Python 3.12+ and Node 24+. Python research tools use only the standard library. Build dependencies are locked in web/package-lock.json.

```sh
python -m unittest discover -s tests -v
python -m patient_outreach
python -m patient_outreach.acquisition
python -m patient_outreach.validate --reps 1500 --n 700 --seed 20261124
python -m patient_outreach.fictional --seed 20261124 --train 10000 --test 40000
cd web
npm ci --ignore-scripts
npm test
npm run build
npm run release:check
npx playwright install
npm run test:browser
```

The acquisition command without flags verifies public metadata only. No permission record is supplied. The publication build and CI read no participant records. Browser and Python calculations use a normal approximation. Their source implementations can be checked independently with a known fixture.
