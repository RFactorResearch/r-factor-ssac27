# Reproduction Guide

Run from the repository root:

```bash
python3 code/reproduce_downstream.py
```

The script requires Python 3.9 or newer and NumPy 1.26 or newer. It was validated with Python 3.9.6 and NumPy 2.0.2. Typical runtime is under two seconds on a laptop-class CPU. Output is written to `generated_results/reproduction_summary.json`.

The Webb wild-cluster seed string and integer seeds are fixed downstream reproducibility constants. They make the reported randomization draws deterministic without exposing forecast-generation or CAP-classification logic.

The H1 point estimates and standard errors are checked with a 2e-6 tolerance because the public H1 derivative contains rounded saved downstream fields rather than the full internal construction state. H1 Webb confidence interval grid bounds and p-values reproduce exactly against the expected tables.

The reproduction script recomputes the statistics identified as `RECOMPUTED` in `docs/reproducibility_matrix.md`. Other expected values are either recomputable from the public inputs but not scripted, or reported only from the frozen expected result tables.
