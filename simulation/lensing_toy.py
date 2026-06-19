"""Epistemic lensing toy model.

Faithful, minimal implementation of the model defined in Section 5 of the paper:
one latent world state, one evidence stream, one mediating channel built from the
five distortion operators, and one Gaussian Bayesian agent. We compute the four
metric families (information loss, posterior divergence, inferential curvature,
hysteresis) for four channel configurations, each isolating one operator.

The benchmark posterior q* is the agent run on the high-fidelity evidence stream
X_t. The mediated posterior q_i is the same agent run on the channel output M_t.
All distortion is measured as q_i relative to q*, exactly as Definition 2.3 states.

Design choices where the paper leaves a quantity to the implementer are flagged
with the tag CHOICE and explained inline. Everything is seeded and deterministic.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

# ---------------------------------------------------------------------------
# Fixed model constants (these match the numerals stated in Section 5 prose).
# ---------------------------------------------------------------------------
T = 200                 # number of time steps
T_CORRECT = 150         # corrective evidence injected here (true W revealed)
T_MEASURE = 200         # hysteresis residual read off at the final step
H_WINDOW = 10           # steps after correction over which recovery is averaged
SIGMA_W = 1.0           # world random-walk innovation sd  (sigma_W)
SIGMA_X = 1.0           # high-fidelity observation noise sd (sigma_X)
SIGMA_NU = 0.5          # channel noise sd (nu_t)
SIGMA_OBS = 1.0         # agent's assumed observation-noise sd (sigma_obs)
N_REPS = 400            # independent random-seed repetitions, averaged
TAU = 1.5               # amplification threshold |X_t| > tau for extreme events
BIAS_B = 2.0            # warping bias direction/magnitude b
GAIN_G = 3.0            # amplification gain on extreme signals


@dataclass
class Channel:
    """Parameterisation theta_C of the mediating channel.

    Each field switches one distortion operator on or off. With all fields at
    their identity value (alpha=1, p_omit=0, beta=0, gamma=0, gain=1) the channel
    is M_t = X_t + nu_t, a near-transparent reference channel. Operators are
    modelled to match the qualitative behaviour each is defined to produce in
    Sections 3 and 5.1.
    """
    alpha: float = 1.0      # attenuation  : signal strength in [0,1]
    p_omit: float = 0.0     # selection    : per-step probability the signal is dropped
    beta: float = 0.0       # warping      : weight on the directional bias b
    gamma: float = 0.0      # recursion    : autoregressive dependence on M_{t-1}
    gain: float = 1.0       # amplification: multiplier on extreme (|X|>tau) signals


def _run_channel(X: np.ndarray, ch: Channel, rng: np.random.Generator):
    """Apply the channel and return (M, observed) where `observed` is a boolean
    mask: False on steps the selection operator drops (no signal reaches the
    agent at all, the absence-of-evidence case of Section 3.2).

    Operator models (each faithful to its Section 3 definition):

      Attenuation A: the channel still tracks X without directional bias but
      transmits less information. CHOICE: we lower the signal-to-noise ratio by
      adding (1/alpha - 1) units of variance, so the posterior widens with no
      systematic shift, the behaviour Section 3.1/5.1 ascribe to attenuation.
      (Multiplicatively shrinking the mean would instead inject a downward bias,
      which the paper assigns to warping, not attenuation.)

      Selection S: with probability p_omit the step is dropped (observed=False),
      so the agent simply does not update. This is the absence-of-evidence the
      agent cannot distinguish from evidence-of-absence (Section 3.2).

      Warping W: a directional bias beta*b is added to transmitted signals,
      shifting the posterior toward b (Section 3.3).

      Amplification G: extreme *innovations* (a step-to-step jump larger than
      tau) are multiplied by `gain`, inflating their salience while mundane steps
      pass unchanged (Section 3.4). CHOICE: the operator scales the surprising
      change X_t - X_{t-1}, not the absolute level, so it models overreaction to
      rare events ("sensationalist coverage") rather than a global rescaling.

      Recursion R: M_t mixes gamma*M_{t-1} with the current signal, giving the
      channel memory and path dependence (Section 3.5).
    """
    n = len(X)
    nu = rng.normal(0.0, SIGMA_NU, n)
    observed = rng.random(n) >= ch.p_omit
    # attenuation as added noise: SNR drops as alpha -> 0, mean stays unbiased.
    atten_sd = math.sqrt(max(1.0 / ch.alpha - 1.0, 0.0)) * SIGMA_X
    atten = rng.normal(0.0, atten_sd, n) if atten_sd > 0 else np.zeros(n)
    M = np.zeros(n)
    prev = 0.0
    x_prev = X[0]
    for t in range(n):
        if not observed[t]:
            # dropped step carries no information about W (pure channel noise),
            # so it lowers I(W;M); the agent treats it as a no-update (see _kalman).
            M[t] = nu[t]
            prev = ch.gamma * prev + nu[t]
            x_prev = X[t]
            continue
        innov = X[t] - x_prev                              # step-to-step surprise
        if ch.gain != 1.0 and abs(innov) > TAU:
            signal_x = x_prev + ch.gain * innov            # amplify rare jumps
        else:
            signal_x = X[t]
        signal = signal_x + atten[t] + ch.beta * BIAS_B
        M[t] = (1.0 - ch.gamma) * signal + ch.gamma * prev + nu[t]
        prev = M[t]
        x_prev = X[t]
    return M, observed


def _kalman(obs: np.ndarray, observed, correct_idx: int | None, W_true: np.ndarray):
    """Gaussian Bayesian agent (a 1-D Kalman filter on a random-walk prior).

    Returns posterior means, posterior variances, and per-step Kalman gains.
    The gain k_t = sigma_t^2 / (sigma_t^2 + sigma_obs^2) is the local update
    sensitivity d mu_t / d obs_t (Section 4.3). On dropped steps (observed=False)
    the agent only runs the predict step and does not update.

    At `correct_idx` (if given) the agent receives the true world state directly
    with near-zero noise, the corrective evidence event E_correct of Section 4.4.
    """
    n = len(obs)
    mu = np.zeros(n)
    var = np.zeros(n)
    gain = np.zeros(n)
    m = 0.0                       # running posterior mean (prior mean 0)
    v = 10.0                      # diffuse prior variance
    for t in range(n):
        v = v + SIGMA_W ** 2      # predict step: random-walk inflates variance
        if correct_idx is not None and t == correct_idx:
            z, r, upd = W_true[t], 1e-4, True   # E_correct: truth revealed
        elif observed is not None and not observed[t]:
            z, r, upd = m, SIGMA_OBS ** 2, False  # dropped: no evidence, no update
        else:
            z, r, upd = obs[t], SIGMA_OBS ** 2, True
        if upd:
            k = v / (v + r)       # Kalman gain = update sensitivity
            m = m + k * (z - m)   # = (1-k)*m + k*z, the Section 5.1 mean update
            v = (1.0 - k) * v
        else:
            k = 0.0
        mu[t], var[t], gain[t] = m, v, k
    return mu, var, gain


# ---------------------------------------------------------------------------
# Metrics.
# ---------------------------------------------------------------------------
def _mutual_information(a: np.ndarray, b: np.ndarray) -> float:
    """Gaussian mutual information I(a;b) = -0.5 log(1 - rho^2) from the sample
    correlation. CHOICE: the model is linear-Gaussian, so the closed-form
    Gaussian MI is exact in expectation and needs no histogram binning."""
    rho = np.corrcoef(a, b)[0, 1]
    rho = float(np.clip(rho, -0.999999, 0.999999))
    return -0.5 * math.log(1.0 - rho ** 2)


def _gauss_pdf(x: np.ndarray, mu: float, var: float) -> np.ndarray:
    var = max(var, 1e-9)
    return np.exp(-0.5 * (x - mu) ** 2 / var) / math.sqrt(2 * math.pi * var)


def _js_gaussian(mu1: float, v1: float, mu2: float, v2: float) -> float:
    """Jensen-Shannon divergence (base 2, in [0,1]) between two 1-D Gaussians,
    evaluated on a dense grid. Symmetric, bounded, defined on disjoint support,
    matching the D_JS used in Sections 4.2 and 4.4."""
    lo = min(mu1 - 5 * math.sqrt(v1), mu2 - 5 * math.sqrt(v2))
    hi = max(mu1 + 5 * math.sqrt(v1), mu2 + 5 * math.sqrt(v2))
    xs = np.linspace(lo, hi, 4000)
    p = _gauss_pdf(xs, mu1, v1)
    q = _gauss_pdf(xs, mu2, v2)
    p /= np.trapezoid(p, xs)
    q /= np.trapezoid(q, xs)
    m = 0.5 * (p + q)

    def _kl(a, b):
        mask = a > 1e-12
        return np.trapezoid(a[mask] * np.log2(a[mask] / b[mask]), xs[mask])

    return float(0.5 * _kl(p, m) + 0.5 * _kl(q, m))


def _update_slope(mu: np.ndarray, W: np.ndarray) -> float:
    """Update sensitivity u: ordinary-least-squares slope of the per-step belief
    change d mu_t on the true world change d W_t. A well-calibrated tracker has
    slope near 1; a channel that magnifies pushes it above the benchmark, one
    that occludes pushes it below."""
    dmu = np.diff(mu)
    dw = np.diff(W)
    denom = float(np.dot(dw, dw))
    if denom < 1e-12:
        return 0.0
    return float(np.dot(dw, dmu) / denom)


@dataclass
class ScenarioResult:
    information_loss: float = 0.0
    posterior_divergence: float = 0.0
    inferential_curvature: float = 0.0
    hysteresis: float = 0.0
    samples: list = field(default_factory=list)


def run_scenario(ch: Channel, seed: int) -> dict:
    """Run one channel configuration over N_REPS seeded repetitions and average
    the four metrics. Every metric compares the mediated run to the benchmark run
    on the same world and evidence draw, so distortion is isolated from world
    noise."""
    L, D, K, H = [], [], [], []
    LOC, DISP = [], []   # divergence decomposition: location shift vs dispersion
    for rep in range(N_REPS):
        rng = np.random.default_rng(seed * 100003 + rep)
        # world random walk and high-fidelity evidence
        W = np.cumsum(rng.normal(0.0, SIGMA_W, T))
        X = W + rng.normal(0.0, SIGMA_X, T)
        M, observed = _run_channel(X, ch, rng)

        # hysteresis world: identical until a sharp reversal at T_CORRECT, the
        # corrective event the channel must transmit (Section 4.4 / 5.2-D).
        Wr = W.copy()
        Wr[T_CORRECT:] = W[T_CORRECT] - (W[T_CORRECT:] - W[T_CORRECT])
        Xr = Wr + rng.normal(0.0, SIGMA_X, T)
        Mr, observed_r = _run_channel(Xr, ch, rng)

        # benchmark posterior q* (agent on X) and mediated posterior q_i (on M)
        mu_b, var_b, gain_b = _kalman(X, None, None, W)
        mu_m, var_m, gain_m = _kalman(M, observed, None, W)

        # 1. information loss: 1 - I(W;M)/I(W;X)
        i_x = _mutual_information(W, X)
        i_m = _mutual_information(W, M)
        L.append(1.0 - i_m / i_x)

        # 2. posterior divergence: mean over t of JS(q_i, q*)
        js = [_js_gaussian(mu_m[t], var_m[t], mu_b[t], var_b[t]) for t in range(T)]
        D.append(float(np.mean(js)))
        # decomposition (Section 4.2): mean |location shift| and mean change in
        # posterior sd. Location shift = confidently wrong; dispersion = uncertain.
        LOC.append(float(np.mean(np.abs(mu_m - mu_b))))
        DISP.append(float(np.mean(np.sqrt(var_m) - np.sqrt(var_b))))

        # 3. inferential curvature: kappa = u_mediated - u_benchmark, where u(e) is
        #    the sensitivity of the belief update to a unit of real evidence
        #    (Section 4.3). CHOICE: estimate u as the slope of d mu_t regressed on
        #    the true world increment d W_t; kappa is the mediated-minus-benchmark
        #    slope. kappa>0 is magnification (overreaction), kappa<0 occlusion.
        K.append(_update_slope(mu_m, W) - _update_slope(mu_b, W))

        # 4. hysteresis: at T_CORRECT the world sharply reverses direction. The
        #    corrective evidence then arrives through each channel (it is not
        #    magically revealed); we measure how far the mediated posterior lags
        #    the benchmark over the recovery window [T_CORRECT+1, +H_WINDOW]. This
        #    is the residue of Section 4.4: a memoryless channel re-tracks fast,
        #    while recursion's stale memory re-distorts the post-reversal signal.
        #    CHOICE: a world reversal (rather than a one-shot truth injection)
        #    operationalises "corrective evidence" so the channel's own dynamics,
        #    not an external oracle, govern recovery.
        mu_br, var_br, _ = _kalman(Xr, None, None, Wr)
        mu_mr, var_mr, _ = _kalman(Mr, observed_r, None, Wr)
        win = range(T_CORRECT + 1, min(T_CORRECT + 1 + H_WINDOW, T))
        H.append(float(np.mean([
            _js_gaussian(mu_mr[t], var_mr[t], mu_br[t], var_br[t]) for t in win])))

    return {
        "channel": {
            "alpha": ch.alpha, "p_omit": ch.p_omit, "beta": ch.beta,
            "gamma": ch.gamma, "gain": ch.gain,
        },
        "information_loss": round(float(np.mean(L)), 4),
        "posterior_divergence": round(float(np.mean(D)), 4),
        "divergence_location_shift": round(float(np.mean(LOC)), 4),
        "divergence_dispersion_change": round(float(np.mean(DISP)), 4),
        "inferential_curvature": round(float(np.mean(K)), 4),
        "hysteresis": round(float(np.mean(H)), 4),
    }


# Scenario definitions, each isolating one operator (Section 5.2).
SCENARIOS = {
    "A_attenuation": Channel(alpha=0.3),
    "B_selection_warping": Channel(p_omit=0.5, beta=0.4),
    "C_amplification": Channel(gain=GAIN_G),
    "D_recursion": Channel(gamma=0.7),
}
