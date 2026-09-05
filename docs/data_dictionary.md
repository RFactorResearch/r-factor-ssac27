# Data Dictionary

## data/frozen_public_forecast_calls.csv

- `forecast_id`, `note_id`, `canonical_note_url`: public forecast identifiers and note URL.
- `published_at_utc`, `official_tipoff_utc`, `actual_start_utc`: recorded timing fields.
- `lead_time_minutes`: minutes from publication to scheduled tipoff; this can be negative when a game started late.
- `lead_time_to_actual_start_minutes`: minutes from publication to recorded actual start.
- `prospective_timing_basis`: `PUBLISHED_BEFORE_RECORDED_ACTUAL_START` or `NOT_PROSPECTIVE_BY_RECORDED_ACTUAL_START`.
- `predicted_control_team`: frozen control-call team label, or `NO_CONTROL_CALL`.
- `predicted_outcome_team`: frozen outcome-team label recorded in the structured ledger.
- `analysis_outcome_call_correct`: whether the frozen outcome-team label matched the recorded winner.
- `strict_prospective_sample`: inclusion flag for the 68-game prospective sample.

## data/h1_downstream_window_dataset.csv

The table contains the H1 downstream model sample only. The duplicate inclusive view and unused non-model rows are omitted. The primary and inclusive views coincided for this dataset.

- `h1_window_id`: opaque sequential row identifier for the public H1 downstream dataset.
- `nba_game_id`: NBA game identifier for the game containing the indexed window.
- `series_id`: playoff series identifier used as the H1 clustering unit.
- `period`: game period number for the indexed window.
- `index_end_clock_seconds`: game-clock seconds remaining in the period at the end of the indexed window.
- `home_score_differential_after_index`: home-team score differential after the indexed window.
- `lag5_signed_net_points`: home-team signed net points over the preceding five-possession lag window.
- `home_control_indicator`: frozen downstream CAP output identifying the applicable home-control state for the indexed window; this field does not describe or reproduce how that state was generated.
- `away_control_indicator`: frozen downstream CAP output identifying the applicable away-control state for the indexed window; this field does not describe or reproduce how that state was generated.
- `future5_signed_net_points`: home-team signed net points over the following five-possession outcome window.
- `h1_y10_model_eligible`: indicator that the row is eligible for the H1 Y10 analysis.
- `future10_signed_net_points`: home-team signed net points over the following ten-possession outcome window when `h1_y10_model_eligible` is true.
- `future5_structural_failure_differential`: home-team signed structural-failure differential over the following five-possession outcome window.

A row with both CAP control indicators equal to false is a baseline control-state row for the H1 model. The file does not describe how CAP labels were produced.

`future10_signed_net_points` is intentionally blank for the 1,010 retained rows that are not eligible for the Y10 analysis. `h1_y10_model_eligible` identifies the eligible rows; blank Y10 values avoid exposing or implying an outcome for ineligible rows. This treatment does not affect the Y5 or structural-failure analyses, and the Y10 model uses only eligible rows.

## data/h2_downstream_master_ledger.csv

Game-level downstream variables for H2 categorical, continuous, and benchmark evaluations. `NO_CONTROL_CALL` means the structured forecast ledger contains no frozen control-call team for that game. H2 categorical excludes indeterminate CAP rows and the no-control-call row; H2 continuous excludes only the no-control-call row.

## data/cap_frozen_evaluation_input.csv

Frozen CAP outputs and paired official game-context variables used for downstream association tests. CAP status labels and shares are frozen outputs. CAP classification-generation details are not included.

## data/posthoc_cap_game_level_profile.csv

Corrected game-level profile variables for downstream posthoc summaries. `NO_CONTROL_CALL` is used for the game without a frozen control-call team. The 67-game winner comparison is stored separately.

## data/posthoc_winner_forecast_comparison.csv

Winner-comparison rows for the 67 games used in the posthoc winner benchmark analysis.
