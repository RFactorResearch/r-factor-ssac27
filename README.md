# R-Factor Sloan Downstream Reproduction Package

This repository reproduces downstream statistical evaluation for the R-Factor Sloan analysis. The evaluation begins with frozen R-Factor forecast calls and frozen CAP outputs. It does not generate forecasts, derive R-Factor scores, or classify CAP states.

The repository includes game identifiers, recorded forecast timestamps, source URLs, downstream analysis inputs, expected result tables, and a reproduction script. Cleaning the Glass source data and raw NBA source files are not included. NBA game identifiers and source URLs are provided for provenance only.

Run `python3 code/reproduce_downstream.py` from the repository root. The script writes `generated_results/reproduction_summary.json` and uses only files in this repository.

No license is granted. The absence of a license means no reuse, redistribution, sublicensing, upload, or publication rights are provided by this repository.
