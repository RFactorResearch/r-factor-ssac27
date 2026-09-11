# Limitations and Scope

The repository reproduces downstream evaluation from frozen forecast calls and frozen Control Adjudication Protocol (CAP) outputs. It does not reproduce the production of R-Factor forecasts, the creation of R-Factor scores, or the generation of CAP classifications.

Some expected result tables include frozen values that are reported but not recomputed by the script, especially resampling intervals, permutation p-values, and H1 sensitivity rows that require omitted analysis-specific fields. The reproducibility matrix identifies each category.

Cleaning the Glass source data and raw NBA source files are not part of the repository. Source URLs and NBA game IDs are retained only to document provenance.

## H1 interpretation and specification sensitivity

H2 categorical agreement is the study's sole primary hypothesis. H1 is secondary validation, and Y5 is the primary outcome within H1. Y5 is home-minus-away scoring over the next five combined eligible possessions after an eligible regulation possession endpoint. The reported contrast compares home-control with away-control endpoints, conditional on the model covariates; neutral is the reference state for the two indicators. It does not estimate the frequency of control transitions.

The following are rounded presentations of saved results, not new fits. All five rows cover 68 games and use 13 series clusters with 9,999 Webb wild-cluster draws. Exact saved values remain in [H1 model results](../results/h1_model_results_expected.csv) and [H1 sensitivity results](../results/h1_sensitivity_results_expected.csv).

| Specification | Observations | Estimate | 95% CI | Two-sided p | Change from primary |
|---|---:|---:|---|---:|---|
| Primary Y5 | 7,092 | -0.6244 | [-0.920, -0.365] | .0003 | Game and period fixed effects, current score, clock, and L5 scoring |
| Add next-possession owner | 7,092 | +0.0171 | [-0.275, +0.280] | .8938 | Add home ownership of the first subsequent eligible possession |
| Remove L5 | 7,092 | +0.4830 | [+0.220, +0.705] | .0036 | Drop only the recent-scoring covariate; retain L5 completeness as a sample requirement |
| Y10 | 6,082 | -0.0604 | [-0.465, +0.305] | .7490 | Ten-possession horizon and its complete, non-garbage sample |
| Nonoverlapping Y5 | 1,451 | -0.5497 | [-0.935, -0.160] | .0121 | Subset selected within game/quarter so each next index starts after the previous selected Y5 ends |

The first three specifications use exactly the same observations. Y10 changes the horizon, sample, and endpoint-specific randomization seed (2026082402 rather than 2026082401). Nonoverlap retains Y5 and the primary covariates while changing endpoint selection. Its negative estimate does not support attributing the primary finding entirely to overlap. Y10's interval includes positive and negative associations and does not establish disappearance of an effect.

These are observational, specification-sensitive associations. The negative primary contrast is neither a typical-reversal rate nor a causal effect. The owner-adjusted interval does not establish no effect, equivalence, or persistence of control. Changes between coefficients have not themselves been tested as differences between models. Scoring outcomes and CAP control transitions are different quantities.

Next ownership is derived from the first subsequent eligible possession, which also contributes to Y5. In ordinary play its owner can often be known when the preceding play resolves, but the frozen construction does not certify live availability at every index. Five combined possessions may give one team an extra offensive opportunity. That is a plausible interpretation of sensitivity, not proof of a mechanism: ownership and recent scoring can also reflect shared context or parts of the process through which control manifests. The records do not separate confounding from mediation or conditioning effects.

The saved confirmation-onset and natural-spline sensitivity rows have status `NOT_ESTIMABLE`. Their numeric zeros are placeholders, not estimates, zero-width intervals, or p=0 evidence; their omission-reason fields are blank. An `OMITTED` row is likewise not an estimated result. Preserve these statuses when using the tables. H3 remains [not estimable](../results/h3_publication_limitation.md); no replacement endpoint was constructed.

## Generation and historical clock scope

Downstream reproduction evaluates the calls actually issued. It does not establish that all historical development rules, rosters, or examples were applied consistently during forecast generation, or that one standardized generation model was applied retrospectively to every call. Possible upstream influence of conflicting development records remains unverified.

The September 10 focused review found neither the permissive-parser defect's triggering malformed clock/period values in the 68 frozen historical play-by-play files nor invalid formatted clocks among 25,956 exported start/end fields. That supports no result-changing correction for those two findings within the tested historical inputs and exports. It does not certify every internal branch or future feed. Exported clocks feed internal H1 construction and are not merely cosmetic. Future parser/formatter hardening belongs in a separate CAP release.
