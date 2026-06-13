# Audit

Dated log of editorial passes and verification runs. Newest first.

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
