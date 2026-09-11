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

The table contains 7,092 H1 primary model rows from 68 games and 13 playoff series. The duplicate inclusive view and unused non-model rows are omitted. The primary and inclusive views coincided for this dataset.

Each row indexes the endpoint of one primary-CAP-eligible regulation possession. Possessions are ordered by their start-action identifier within the same quarter. The included current states are confirmed home control, confirmed away control, and neutral; contested and provisional states are excluded. Team-control confirmation must occur in the same episode and quarter at or before the index. These are H1 sample-selection conditions applied to frozen CAP labels; they do not describe how the labels or confirmation events were generated. There is no requirement for five earlier possessions controlled by the current controller.

L5 uses the five eligible possessions strictly before the indexed possession. Y5 uses the next five eligible possessions strictly after it; Y10 uses the next ten. These are combined possessions across both teams, not five or ten per team. All are within the same regulation quarter, and the index's points are excluded. The primary point sums use non-administrative points and skip ineligible intervening possessions. The index cannot be in garbage time, and the chronological span through the future horizon cannot enter garbage time. Both the lag window and required future horizon must be complete.

Strictly after means later in possession order. Adjacent frozen possession records can share an action/clock boundary, so later in possession order does not require a distinct clock time or raw action identifier. The published opaque row identifier does not expose the internal endpoint identifiers needed to reconstruct the original possession boundaries.

- `h1_window_id`: opaque sequential row identifier for the public H1 downstream dataset.
- `nba_game_id`: NBA game identifier for the game containing the indexed window.
- `series_id`: playoff series identifier used as the H1 clustering unit.
- `period`: game period number for the indexed window.
- `index_end_clock_seconds`: game-clock seconds remaining at the indexed possession endpoint, floored to integer seconds in this saved table. The internal H1 design used decimal seconds from the CAP export; see the precision note in the [reproduction guide](reproduction_guide.md).
- `home_score_differential_after_index`: home-minus-away cumulative score differential after the indexed possession.
- `lag5_signed_net_points`: non-administrative home-minus-away net points over the five preceding combined eligible possessions, excluding the index (L5).
- `home_control_indicator`: frozen downstream CAP output identifying the applicable home-control state at the indexed possession endpoint; this field does not describe or reproduce how that state was generated.
- `away_control_indicator`: frozen downstream CAP output identifying the applicable away-control state at the indexed possession endpoint; this field does not describe or reproduce how that state was generated.
- `future5_signed_net_points`: non-administrative home-minus-away net points over the next five combined eligible possessions, excluding the index (Y5).
- `h1_y10_model_eligible`: indicator that the row is eligible for the H1 Y10 analysis.
- `future10_signed_net_points`: non-administrative home-minus-away net points over the next ten combined eligible possessions, excluding the index (Y10), when `h1_y10_model_eligible` is true.
- `future5_structural_failure_differential`: away-offense structural failures minus home-offense structural failures over the following five combined eligible possessions, excluding the index. Positive values mean more failures by the away offense; the underlying failure flags are frozen CAP outputs.

A row with both CAP control indicators equal to false is neutral, the model reference state. The reported contrast is the home-control coefficient minus the away-control coefficient, not either coefficient versus neutral. Positive signed net-point values favor home scoring. The primary model includes game and period fixed effects, both control indicators, score differential after the index, endpoint clock seconds, and L5 signed net points. See [limitations](limitations_scope.md) for specification sensitivity. The file does not reproduce how CAP labels were produced.

`future10_signed_net_points` is intentionally blank for the 1,010 retained rows that are not eligible for the Y10 analysis. `h1_y10_model_eligible` identifies the eligible rows; blank Y10 values avoid exposing or implying an outcome for ineligible rows. This treatment does not affect the Y5 or structural-failure analyses, and the Y10 model uses only eligible rows.

## data/h2_downstream_master_ledger.csv

Game-level downstream variables for H2 categorical, continuous, and benchmark evaluations. `NO_CONTROL_CALL` means the structured forecast ledger contains no frozen control-call team for that game. H2 categorical excludes indeterminate CAP rows and the no-control-call row; H2 continuous excludes only the no-control-call row.

## data/cap_frozen_evaluation_input.csv

Frozen Control Adjudication Protocol (CAP) outputs and paired official game-context variables used for downstream association tests. CAP status labels and shares are frozen outputs. CAP classification-generation details are not included.

## data/posthoc_cap_game_level_profile.csv

Corrected game-level profile variables for downstream posthoc summaries. `NO_CONTROL_CALL` is used for the game without a frozen control-call team. The 67-game winner comparison is stored separately.

## data/posthoc_winner_forecast_comparison.csv

Winner-comparison rows for the 67 games used in the posthoc winner benchmark analysis.
