# Audit

Dated log of editorial passes and verification runs. Newest first.

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
