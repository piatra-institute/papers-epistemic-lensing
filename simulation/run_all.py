"""Run every epistemic-lensing scenario and write output/results.json.

One command, fully seeded, reproducible:

    python run_all.py          # or: uv run run_all.py
"""

from __future__ import annotations

import json
from pathlib import Path

import lensing_toy as toy

SEED = 20260417   # paper date 2026-04, fixed for reproducibility


def main() -> None:
    out_dir = Path(__file__).parent / "output"
    out_dir.mkdir(exist_ok=True)

    scenarios = {}
    for i, (name, channel) in enumerate(toy.SCENARIOS.items()):
        scenarios[name] = toy.run_scenario(channel, SEED + i)

    # The paper reports metrics to 2 decimals. Emit those rounded display values
    # (including unsigned magnitudes, since prose writes "kappa = -0.27" and the
    # claims gate reads the bare decimal) so every number in Section 5 traces here.
    metric_keys = [
        "information_loss", "posterior_divergence", "divergence_location_shift",
        "divergence_dispersion_change", "inferential_curvature", "hysteresis",
    ]
    reported = {}
    for name, s in scenarios.items():
        for k in metric_keys:
            v = round(s[k], 2)
            reported[f"{name}.{k}"] = v
            reported[f"{name}.{k}.abs"] = abs(v)

    results = {
        "seed": SEED,
        "config": {
            "time_steps": toy.T,
            "t_correct": toy.T_CORRECT,
            "t_measure": toy.T_MEASURE,
            "h_window": toy.H_WINDOW,
            "reps": toy.N_REPS,
            "sigma_W": toy.SIGMA_W,
            "sigma_X": toy.SIGMA_X,
            "sigma_nu": toy.SIGMA_NU,
            "sigma_obs": toy.SIGMA_OBS,
            "tau": toy.TAU,
            "bias_b": toy.BIAS_B,
            "gain_g": toy.GAIN_G,
        },
        "metrics_note": (
            "information_loss = 1 - I(W;M)/I(W;X), Gaussian mutual information; "
            "posterior_divergence = mean over t of JS(q_i, q*); "
            "inferential_curvature = slope(d mu_mediated / d W) - slope(d mu_benchmark / d W); "
            "hysteresis = mean JS(q_i, q*) over the h_window steps after a world "
            "reversal at t_correct (recovery lag). JS divergence in bits (base 2), "
            "bounded in [0,1]."
        ),
        "scenarios": scenarios,
        "reported_2dp": reported,
    }

    out_path = out_dir / "results.json"
    out_path.write_text(json.dumps(results, indent=2) + "\n")
    print(f"wrote {out_path}")
    for name, s in scenarios.items():
        print(f"  {name:22s} L={s['information_loss']:.2f} "
              f"D={s['posterior_divergence']:.2f} "
              f"kappa={s['inferential_curvature']:+.2f} "
              f"H={s['hysteresis']:.2f}")


if __name__ == "__main__":
    main()
