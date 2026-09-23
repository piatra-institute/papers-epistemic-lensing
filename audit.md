# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-09-23 — prose revision

Prose rewritten against the house standards. Headings: Abstract; 1 Introduction; 2 Theoretical Framework; 3 Distortion Operators; 4 Distortion Metrics (was "Metrics of the Bend"); 5 Toy Simulation (5.4 Ignorance and Distortion in the Simulation, was "Key Finding"); 6 Population Extension; 7 Empirical Program; 8 Limitations (was "What a comparative benchmark can and cannot fix"); 9 Conclusion (was "Ignorance and distortion are different problems"); Reproducibility (new).
Tic counts before -> after: "rather than" 18 -> 0; "this paper" 3 -> 0; "not X but Y" 1 -> 0; sentence-initial "This is" 1 -> 0; merely/simply 3 -> 0.
Corrections and clarifications:
  - Section 5.4 called attenuation's information loss (0.37) "high" while 5.3 called it "moderate"; now "moderate" in both places.
  - The location-shift figures (0.86, 1.07, 1.39, 0.92) and dispersion change (0.44) were placed in a paragraph whose units were declared as Jensen-Shannon bits; they are mean absolute posterior-mean differences and mean posterior-sd differences in world-state units, and the text now says so. An Estimators paragraph states how each metric is computed (from the metrics_note in results.json).
  - The dispersion change of 0.00 for channels A, C, D is now stated as identically zero by construction (the agent updates every step with a fixed assumed noise, so its variance recursion equals the benchmark's).
  - Previously uncited bibliography entries now cited where they support existing statements: Shannon 1948 (mutual information), Friston et al. 2017 (active inference), Tversky & Kahneman 1974 (availability heuristic), Pariser 2011 (personalization), Lewandowsky et al. 2012 and Walter et al. 2020 (continued influence, fact-checking) in 4.4. Kahneman & Tversky 1979 remains uncited.
Grid/number audit: the model has no thresholds, optima or grid-derived values; every metric is a 400-repetition mean at a single parameter setting. All prose numbers match results.json reported_2dp. No simulation code changed; results.json untouched.

## 2026-06-19 — wire the toy model to real computed results

A referee found, and we confirmed, that Section 5 reported specific metric numbers in the present tense as computed Results while no code produced them (the repo's NarrativeNavigator.py is unrelated, there was no results.json, claims_target was none, and an earlier audit entry admitted the values were "illustrative ≈"). Reporting invented numbers as results is disqualifying, so Section 5 is now backed by a real seeded simulation.

Simulation: new `simulation/lensing_toy.py` + `run_all.py` (+ pyproject, numpy only). A one-dimensional Kalman agent updates a Gaussian posterior over a random-walk world. The five operators are implemented faithfully to Section 3: attenuation as reduced signal-to-noise (added variance, no mean shift), selection as per-step signal drops the agent cannot distinguish from absence, warping as an additive directional bias, amplification as gain on extreme innovations, recursion as autoregressive mixing of prior channel output. The four metrics are computed: information loss from Gaussian mutual information, posterior divergence as mean Jensen-Shannon between mediated and benchmark posteriors (with a location/dispersion decomposition), inferential curvature as the difference in the slope of belief-change on true world-change, hysteresis as residual divergence over a recovery window after a world reversal. 400 seeded reps; one command writes `simulation/output/results.json`.

Section 5 rewritten to report the computed numbers (L: A 0.37, B 0.88, C 0.68, D 0.16; D: A 0.22, B 0.24, C 0.36, D 0.24; kappa: A -0.00, B -0.27, C +1.06, D -0.43; H: A 0.22, B 0.25, C 0.35, D 0.24). The new numbers differ from the old illustrative ones; honesty over matching. Two honest departures from the old narrative are reported rather than hidden: amplification, not selection, now shows the highest posterior divergence, and the single-agent post-reversal residual tracks each channel's steady-state distortion rather than isolating a recursion-specific memory residue. The "confidently wrong" claim is carried by the location/dispersion decomposition (three of four channels shift location with zero dispersion change), which is the sharper evidence. Model choices left open by the paper are documented inline in the code (tagged CHOICE) and noted in §5.

Metadata: has_simulation already true; claims_target set to results.json.

Verification: voice 0 errors / 0 warns; claims 0 decimals without a results.json match; refs advisory unchanged (citation set untouched); build clean; check => PASS (web WARN only, deployed PDF differs from the local rebuild; sync writes outside the paper dir and was left to the publish step).

## 2026-06-13 — voice reform

Editorial pass to remove AI-writing tells per tooling/docs/voice.md.

Syntax: rewrote the negate-pivot and inline-contrastive constructions flagged by the gate as positive declaratives, using "rather than" for ", not" (mediation as architecture §2.1; the benchmark $q^*$ passage §2.3, where a double inline-contrastive plus negate-pivot was recast positively; composition "interaction not sum" §3.6; population field §6.1; shadow-zone selection criteria §6.4; "processing that worsens calibration" §7.3; the benchmark and toy-model caveats §8). Also softened the bare "the problem is not X, the problem is Y" opener of the closing into a positive contrast.

Pet-vocabulary: the one gate-flagged tell, "the bend has become load-bearing" (§4.4 hysteresis), rewritten to "the bend has set into the agent's posterior and structures every later update".

Structure: the gate flagged the formulaic skeleton (numbered sections + generic "Conclusion" + a "Limits" bolt-on). The §8 "Limits" section is substantive (five framework-wide caveats that do not belong to any single earlier section), so it was retitled rather than folded: "Limits" -> "What a comparative benchmark can and cannot fix". §9 "Conclusion" -> "Ignorance and distortion are different problems". No renumbering, so no cross-references changed.

Density: no filler "exactly"/"precisely" in the abstract, intro, or conclusion; the two uses elsewhere are genuine (a quoted phrase and "precisely because" in §6.4). The abstract's lists are substantive enumerations of the framework's named operators, metrics, and population phenomena, left intact.

Verification: voice 0 errors / 0 warns (structure advisory cleared); build succeeds, 0 missing-character warnings; claims_target none; check => PASS. Refs: citation set unchanged from baseline (Pearl 1988, Friston 2013, Benkler/Faris/Roberts 2018 all still resolve; 0 missing). The refs gate remains in its pre-existing advisory state (3 detected in-text, 12 bib, 9 unused) because most bib entries were already uncited and its author-year detection is unreliable on this paper; no citation was added, dropped, or altered. No numbers, equations, or figure values changed.

## 2026-05-29 — upgrade pass (Group D)

Baseline: 3 voice errors (the §1 roadmap paragraph), refs advisory, 14 pages.

Scope contract:
1. Remove the §1 roadmap paragraph ("The paper is organized as follows…") — the
   3 voice errors; section headings already do this work.
2. Voice tells: §2.2 "maps naturally onto" hedge; §2.3 "Three clarifications
   follow" counting lead; §5.4 italic takeaway-lead; §8 throat-clear opener.
3. Research (named gap): engage asymmetric-misinformation literature where §8
   claims the framework "applies symmetrically" — add Benkler, Faris & Roberts
   (2018) and frame symmetry as an empirical question the metrics can settle.

Next-pass candidates (logged): wire the §5 toy model to a committed results.json
(currently illustrative ≈ values, claims_target=none); de-circularize the §2.3
definition vs §3 operators ordering; network-polarization literature.

Verification: voice 0 errors; refs advisory; build clean; check => PASS.

## 2026-05-29 — workspace import

Scope: brought into the piatra-papers workspace as a worked example; no prose
changes to the paper itself.

Changes:
- Added metadata.yaml, brief.md, research.md, sources.md (this pipeline scaffold).
- Rebuilt PAPER.pdf with the canonical recipe (header "Epistemic Lensing").

Verification:
- build: 14 pages, zero missing-character warnings.
- voice: 0 errors (inline-contrastive warns to review).
- refs: advisory — detached narrative citations not reliably auto-resolved;
  reconcile sources.md against prose by hand on the next refresh.

## 2026-07-02 — Corpus reform, Phase 0 (integrity)
Removed a fabricated bibliography entry: Sunstein, C. R. (2001), *Echo Chambers:
Bush v. Gore, Impeachment, and Beyond* — no such book exists (the 2001 Sunstein
title is *Republic.com*). It was orphaned (cited nowhere in text) and appeared
identically in this paper and one other, evidence of a shared uncurated
bibliography. Also removed the orphan signSGD (Bernstein et al. 2018) entry
where present. Rebuilt + synced. Remaining uncited refs to be reconciled in the
Phase 2 rewrite of this paper.
