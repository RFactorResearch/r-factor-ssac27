# Source Provenance

Forecast-call provenance is represented by forecast IDs, Substack note IDs, publication timestamps, NBA game IDs, and recorded source URLs. URLs are provenance fields; the reproduction script does not access them.

Cleaning the Glass was among the third-party sources consulted during development of the frozen forecasts. Cleaning the Glass data and source materials are not included in this repository and are not required to reproduce the downstream evaluation.

Prospective status follows publication before the recorded actual game start. Forecast `RF2026-013` was recorded after scheduled tipoff but before the recorded actual start, so the historical scheduled-tipoff lead remains negative while the actual-start lead is positive.

Game `0042500214` has no frozen control call in the structured forecast ledger. The same structured ledger records an outcome-team value, but the winner-comparison table uses the 67 games with a control-call row and does not include this game. Any interpretation beyond the structured ledger belongs outside this repository.

Official leadership-duration values for game `0042500122` were corrected before the analytical freeze. The downstream data files contain the corrected values used in the analyses.

Raw NBA files and proprietary generation methods are not included.
