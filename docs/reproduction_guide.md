# Reproduction Guide

Run from the repository root:

```bash
python3 code/reproduce_downstream.py
```

The script requires Python 3.9 or newer and NumPy 1.26 or newer. It was validated with Python 3.9.6 and NumPy 2.0.2. Typical runtime is under two seconds on a laptop-class CPU. Output is written to `generated_results/reproduction_summary.json`.

The Webb wild-cluster seed string and integer seeds are fixed downstream reproducibility constants. They make the reported randomization draws deterministic without exposing forecast-generation or CAP-classification logic.

The H1 point estimates and standard errors are checked with a 2e-6 tolerance because the public H1 derivative contains saved downstream fields rather than the full internal construction state: the exported clock covariate is floored to integer seconds, while the internal fit used decimal seconds. The script checks H1 Webb confidence interval grid bounds and p-values against the expected tables with a 1e-12 absolute tolerance.

The reproduction script recomputes the statistics identified as `RECOMPUTED` in `docs/reproducibility_matrix.md`. Other expected values are either recomputable from the public inputs but not scripted, or reported only from the frozen expected result tables.

## Scope of reproduction evidence

CAP means Control Adjudication Protocol. Three different forms of reproduction must be distinguished:

| Evidence | Supported scope | Limit |
|---|---|---|
| Historical CAP dataset repetition | A separate run reproduced outputs using the frozen classifier code and historical inputs | This is repetition of the same classifier implementation, not a separately coded classifier |
| Historical blinded second statistical implementation | Exploratory CAP association results were independently implemented, sealed before unblinding, and accepted with zero substantive mismatches | This claim concerns that statistical result family; it does not establish independent forecast generation or independently coded CAP classification |
| This repository's downstream command | The selected checks marked RECOMPUTED in the matrix, starting with frozen forecast calls and CAP outputs | Some expected statistics and sensitivities are reported only; the command starts from frozen downstream inputs |

Some expected statistics and sensitivities are reported only. The command does not regenerate forecasts, CAP classifications, or raw source data. High-level methodological explanations are included; upstream implementation code and detailed proprietary generation rules are excluded.

The previously completed independent post-upload verification reported 121 checks passed for the current code/data/result payload. The September 10 focused review checked payload and frozen-evidence agreement without rerunning the study. Documentation revisions do not create a new independent implementation or a new numerical reproduction result.

In particular, the command does not run the next-owner, remove-L5, or nonoverlapping H1 sensitivities. Remove-L5 could be computed from the existing primary inputs but is not scripted. Next-owner and nonoverlap reconstruction need omitted fields. Consult the [limitations](limitations_scope.md) alongside the expected sensitivity table; a successful command does not establish that every stored result was recalculated.
