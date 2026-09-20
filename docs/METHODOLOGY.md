# Methodology and limitations

## Prediction target and timing

The target is the complete finishing order. The prediction is made from information available before the race and locked before the start. Outcomes and later observations must not enter the feature set for that race.

## Time-aware validation

The recorded study evaluates races in chronological order. For target race *t*, training rows come only from races completed before *t*. After scoring *t*, it becomes available for the next training step. This mirrors deployment more closely than a random split, which can put later races in the training set for earlier predictions.

The 2024–2025 races were used to choose numerical model settings. The first 13 rounds of 2026 form a later evaluation period. Development continued while 2026 results were visible, including changes to the modelling approach. This means the 2026 aggregate is exploratory and should not be presented as a fully untouched test set, even if individual settings were selected on earlier seasons. Its small sample adds further uncertainty.

## Leakage checks

The private implementation contains four checks:

1. A static check that post-race fields are absent from the model feature list.
2. A debut check that history-based features are unavailable before a driver's first recorded race.
3. A truncation check that the features for a chosen race are identical after all later races are removed from the input.
4. A label-permutation check that predictive skill collapses when historical finishing positions are shuffled within races.

The example in this repository demonstrates the strict temporal cutoff; it is not the full leakage audit.

## Baseline and metrics

The baseline is starting-grid order. The headline metric is Spearman rank correlation, computed over classified finishers for each race and then summarized across races. Other recorded metrics include top-10 overlap and winner identification. A retirement should not automatically teach a pace ranker that a fast car was slow; the private system models that distinction separately.

## Limits of the public evidence

The table in the README is transcribed from the project's private evaluation report. Because the race-level predictions and third-party data are not published here, an outside reader cannot independently recompute the reported season scores from this repository. The code example demonstrates the evaluation principle on invented data only.

The 2026 comparison spans 13 races and was monitored during development. Weather, incidents, regulation changes, and team changes can alter how well the model transfers to future races. The 2024–2025 results are model-selection results and should not be read as independent test performance. A stronger prospective study would freeze the model, feature pipeline, metrics, and exclusion rules before a future season begins, timestamp each prediction, and report every scheduled race whether the prediction succeeds or fails.
