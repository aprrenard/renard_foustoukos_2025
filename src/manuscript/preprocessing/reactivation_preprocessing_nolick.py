"""
Reactivation preprocessing pipeline — no-lick (correct rejection) variant.

Reuses all core functions from reactivation_preprocessing.py, only changing
the trial selection to no_stim & lick_flag==0 trials restricted to a ±2s
window around no_stim onset, and running detection at three surrogate
percentiles (99, 99.5, 99.9) computed from a single surrogate pass.

Outputs are written to a separate 'nolick' subdirectory so the original
all-no_stim outputs (data_processed/reactivation/) stay untouched and
reproducible.
"""

import os
import sys

sys.path.append('/home/aprenard/repos/fast-learning')
import src.manuscript.preprocessing.reactivation_preprocessing as rp

# ============================================================================
# Parameters
# ============================================================================

NO_LICK_ONLY = True
TIME_WINDOW = (-2, 2)
PERCENTILES = [99, 99.5, 99.9]

OUTPUT_DIR = os.path.join(rp.OUTPUT_DIR, 'nolick')


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("REACTIVATION PREPROCESSING PIPELINE — NO-LICK VARIANT")
    print("=" * 60)
    print(f"  Output directory: {OUTPUT_DIR}")
    print(f"  Trial selection: no_stim & lick_flag==0, time_window={TIME_WINDOW}")
    print(f"  Percentiles: {PERCENTILES}")

    all_mice_to_process = rp.r_plus_mice + rp.r_minus_mice

    # ------------------------------------------------------------------
    # Part 1b: Per-mouse surrogate thresholds (one pass, all percentiles)
    # ------------------------------------------------------------------
    rp.run_surrogates_per_mouse(
        all_mice_to_process,
        output_dir=OUTPUT_DIR,
        percentiles=PERCENTILES,
        no_lick_only=NO_LICK_ONLY,
        time_window=TIME_WINDOW,
    )

    # ------------------------------------------------------------------
    # Part 2: Reactivation event detection, one run per percentile
    # ------------------------------------------------------------------
    for percentile in PERCENTILES:
        rp.run_reactivation_detection(
            rp.r_plus_mice,
            rp.r_minus_mice,
            output_dir=OUTPUT_DIR,
            percentile=percentile,
            no_lick_only=NO_LICK_ONLY,
            time_window=TIME_WINDOW,
        )
