# R-Factor Sloan Downstream Reproduction Package

This repository reproduces downstream statistical evaluation for the R-Factor Sloan analysis. The evaluation begins with frozen R-Factor forecast calls and frozen Control Adjudication Protocol (CAP) outputs. It does not generate forecasts, derive R-Factor scores, or classify CAP states.

The repository includes game identifiers, recorded forecast timestamps, source URLs, downstream analysis inputs, expected result tables, and a reproduction script. Cleaning the Glass source data and raw NBA source files are not included. NBA game identifiers and source URLs are provided for provenance only.

Run `python3 code/reproduce_downstream.py` from the repository root. The script writes `generated_results/reproduction_summary.json` and uses only files in this repository.

H2 categorical agreement is the study's sole primary hypothesis. H1 is secondary validation, with Y5 as its primary outcome: subsequent home-minus-away points over five combined eligible possessions. Its association is sensitive to next-possession ownership and recent-scoring adjustment; see the [data dictionary](docs/data_dictionary.md) and [limitations](docs/limitations_scope.md).

The historical blinded second statistical implementation concerned exploratory CAP association results. This repository supports the more limited downstream checks listed in the [reproducibility matrix](docs/reproducibility_matrix.md); see the [reproduction guide](docs/reproduction_guide.md) for the distinctions.

## Licensing and data scope

Mark Barnekow/RFactorResearch retains ownership of the original materials in this repository. Original software and code, including `code/reproduce_downstream.py`, are licensed under the [MIT License](LICENSE). Original documentation and original or derived research-data materials in `data/` and `results/` are licensed under the [Creative Commons Attribution 4.0 International License](LICENSE-DATA-DOCS). These express grants supersede the general no-license statement in `NOTICE.md` only for those scoped original materials; the third-party exclusions in that notice remain in effect.

Third-party NBA and Cleaning the Glass materials are not relicensed or redistributed. NBA game IDs and source links identify official source material but do not grant rights in that material. Trademarks, project names, and logos are not licensed merely by publication of this repository. Intellectual property not actually contained in this repository, including proprietary forecast-generation and CAP classification-generation methods, is not released.
