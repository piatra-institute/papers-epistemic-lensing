# Brief

Reconstructed retroactively from the finished paper and the 611-line design seed
in `paper/project.md`, as the second worked example for the pipeline.

## Question

How do mediated information channels deform belief formation, and can the
deformation be measured?

## Claim

Epistemic lensing is a formal account of mediated belief distortion. Using a
Markov-blanket framing, distinguish direct environmental evidence from processed
informational inputs; define distortion as the divergence between the posterior a
higher-fidelity channel supports and the posterior a mediated channel induces.
Five distortion operators (attenuation, selection, warping, amplification,
recursion) and four metric families (information loss, posterior divergence,
inferential curvature, hysteresis). Extends to populations: posterior shear,
focal capture, shadow zones, narrative gravity wells.

## Kind

Formal-model. Ships a simulation (`has_simulation: true`). The toy simulation
demonstrates the operators; `claims_target: none` because the headline claims are
qualitative phenomena rather than reconciled numeric outputs — revisit if the
simulation gains a `results.json`.

## Cornerstone literature

Active inference / free energy (Friston), Markov blankets, information theory
(Shannon), judgment under uncertainty (Kahneman & Tversky), filter bubbles /
echo chambers (Pariser, Sunstein), misinformation (Lewandowsky).
