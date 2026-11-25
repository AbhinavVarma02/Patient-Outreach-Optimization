# Model card

The experimental Python subgroup learner estimates each fictional band's treated and control response rate with add-one smoothing. It ranks the band effects and freezes fractional outreach probabilities at 20% expected capacity using declared population shares. The independent holdout estimates the effect of each fixed policy versus uniform through paired AIPW with known assignment probability.

The current model operates only on generated trials. It has no real-patient inference endpoint, no persisted patient records and no approval for operational use. The website's known-effect examples are mathematically specified scenarios.
