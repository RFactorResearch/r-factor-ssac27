# Limitations and Scope

The repository reproduces downstream evaluation from frozen forecast calls and frozen CAP outputs. It does not reproduce the production of R-Factor forecasts, the creation of R-Factor scores, or the generation of CAP classifications.

Some expected result tables include frozen values that are reported but not recomputed by the script, especially resampling intervals, permutation p-values, and H1 sensitivity rows that require omitted analysis-specific fields. The reproducibility matrix identifies each category.

Cleaning the Glass source data and raw NBA source files are not part of the repository. Source URLs and NBA game IDs are retained only to document provenance.
