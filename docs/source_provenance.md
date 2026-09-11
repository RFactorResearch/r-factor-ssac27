# Source Provenance

Forecast-call provenance is represented by forecast IDs, Substack note IDs, publication timestamps, NBA game IDs, and recorded source URLs. URLs are provenance fields; the reproduction script does not access them.

Cleaning the Glass was among the third-party sources consulted during development of the frozen forecasts. The reproduction boundary begins with frozen forecast calls and CAP outputs. No Cleaning the Glass fields, values, exports, PDFs, screenshots, copied tables, exact field lists, or correspondence are included. Its upstream role does not imply that forecast generation can be reproduced from this repository, or that third-party materials are licensed for reuse.

Prospective status follows publication before the recorded actual game start. Forecast `RF2026-013` was recorded after scheduled tipoff but before the recorded actual start, so the historical scheduled-tipoff lead remains negative while the actual-start lead is positive.

Game `0042500214` has no frozen control call in the structured forecast ledger. The same structured ledger records an outcome-team value, but the winner-comparison table uses the 67 games with a control-call row and does not include this game. Any interpretation beyond the structured ledger belongs outside this repository.

Official leadership-duration values for game `0042500122` were corrected before the analytical freeze. The downstream data files contain the corrected values used in the analyses.

Raw NBA files and proprietary generation methods are not included.

## CAP name and freeze timing

CAP is the Control Adjudication Protocol. Forecast publication is assessed against recorded actual game starts, as described above. CAP v1.0.2 was frozen on August 24, 2026, after the games and before its historical evaluation run; the resulting CAP dataset was frozen and replicated before the August 25 analysis-plan lock. The exact locked plan already recorded 21 indeterminate games, zero not-adjudicable games, and a maximum determinate H2 denominator of 47 before forecast exclusions. It also recorded that forecasts and winners had not been merged for analysis and H1/H2/H3 had not been calculated. Those aggregate determinacy counts are distinct from forecast agreement, scoring associations, and winner alignment. The plan lock and subsequent analysis authorization are separate from pregame forecast publication. This chronology documents prior knowledge of aggregate determinacy; it does not establish whole-study preregistration before the games or what every participant knew about game outcomes or analytical results.

The operative H1/H2 results are the corrected Phase A v2.7 package, designated by the September 2 final verified handoff. The accepted exploratory CAP association reproduction is distinct from repeated execution of the frozen CAP classifier; see the [reproduction guide](reproduction_guide.md). Historical pending labels and earlier development examples do not supersede those closure records.

The following package hashes identify the frozen sources; they are provenance identifiers, not additional repository files or grants of access or reuse rights.

| Frozen source | SHA-256 |
|---|---|
| Final locked analysis-plan package | bde3dc0169c2b339c435b802c800926ea6348784a2e51eaf3ca49c00772bbc2b |
| Corrected Phase A v2.7 results package | 136491e2d34f95625f180de53d6c203b0dffda95184a8e21c6dbe1de39ae717e |
| CAP v1.0.2 release | 39af48829c9e462e58d4f5991de98a7ce0f2a890bb2aa78d140babde724db224 |
| Replicated CAP dataset | bf0b3ea97b6df6f0072b6e1d8597fa477278c3076fd3acb6f015a142d2b1e326 |
| CAP association package | c72920256565de84044ab2e41363e0232b2b3a60f754c7ac657d423fe11bb687 |
