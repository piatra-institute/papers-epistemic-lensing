# Epistemic Lensing Simulation: Experimental Protocol

## 1. Overview

This simulation tests whether the distortion dynamics described in the Epistemic Lensing paper can be reproduced in language models. A persona LLM generates posts on political and social topics. A swarm of commenter LLMs applies structured pressure (the "channel"). The persona is periodically re-fine-tuned on its own output. Over multiple cycles, we measure whether the persona's expressed beliefs drift in ways predicted by the five distortion operators: attenuation, selection, warping, amplification, and recursion.

The core question: **does a persona LLM exhibit posterior divergence, inferential curvature, and hysteresis under structured social pressure, in the same patterns the paper's toy model predicts?**


## 2. Architecture

```
                    ┌─────────────────┐
                    │   Topic Pool    │
                    │  (world state)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Persona LLM   │
                    │   (the agent)   │
                    └────────┬────────┘
                             │ generates post
                    ┌────────▼────────┐
                    │    Post DB      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───┐  ┌──────▼─────┐  ┌─────▼──────┐
     │ Commenter  │  │ Commenter  │  │ Commenter  │
     │   LLM 1    │  │   LLM 2    │  │   LLM N    │
     │ (channel)  │  │ (channel)  │  │ (channel)  │
     └────────┬───┘  └──────┬─────┘  └─────┬──────┘
              │              │              │
              └──────────────┼──────────────┘
                             │ comments
                    ┌────────▼────────┐
                    │  Persona reads  │
                    │  comments and   │
                    │ optionally edits│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Fine-tuner     │
                    │ (every N posts) │
                    └─────────────────┘
```

### Components

**Topic Pool (World State).** A fixed set of factual claims and policy positions drawn from a reference dataset. Each topic has a ground-truth position (the "world state") and a set of possible stances. Topics span economics, healthcare, climate, foreign policy, civil rights, and technology regulation. The topic pool is the simulation's equivalent of $W_t$ in the paper.

**Persona LLM (Agent).** A language model fine-tuned on a corpus of a specific public figure's speeches, interviews, and writings to establish an initial "belief profile." The persona generates posts on topics drawn from the pool. After each cycle, it is re-fine-tuned on the posts it produced (including any edits made in response to comments). This re-fine-tuning is the mechanism by which the channel's influence becomes permanent, analogous to the recursion operator.

**Commenter LLMs (Channel).** A swarm of language models that generate comments on each post. Each commenter operates under a fixed strategy (see Section 4) that maps onto one or more of the five distortion operators. The commenter swarm collectively constitutes the mediating channel between the world and the persona's evolving belief state.

**Post Database.** SQLite store tracking every post, comment, edit, model version, and timestamp. This is the primary data source for all metrics.

**Fine-Tuner.** LoRA-based parameter-efficient fine-tuning on the persona's own output. Runs after every N posts (default: 100). Each fine-tuning cycle produces a new model version, creating a lineage: v1 → v2 → v3 → ...


## 3. Experimental Conditions

We run seven conditions. Conditions 1-5 isolate each distortion operator. Condition 6 combines multiple operators. Condition 0 is the control.

### Condition 0: Control (No Channel Pressure)

The persona generates posts. Commenters are absent or generate only neutral, factual responses. Fine-tuning proceeds on uninfluenced output. This measures natural drift from re-fine-tuning alone.

### Condition 1: Attenuation

Commenters respond to only 30% of posts (selected randomly). The remaining 70% receive no comments. This simulates a low-engagement environment where most of the persona's output receives no feedback. The persona re-fine-tunes on all its output, but the social signal is sparse.

**Prediction:** The persona drifts slowly and non-directionally. Posterior divergence from baseline is low. Hysteresis is near zero because there is no structured pressure to lock in.

### Condition 2: Selection

Commenters respond only to posts on specific topics (e.g., economics and climate) and ignore all others. Within the selected topics, comments are substantive and balanced. For ignored topics, the persona receives zero feedback.

**Prediction:** The persona's expressed positions on selected topics remain calibrated (the channel is high-fidelity for these). Positions on ignored topics drift unpredictably. Over fine-tuning cycles, ignored topics may fade from the persona's repertoire entirely (shadow zones).

### Condition 3: Warping

All commenters are assigned a consistent directional bias. For example, every comment frames economic policy from a strongly free-market perspective, interprets healthcare through a lens of individual responsibility, and treats climate action as economically destructive. Comments are well-argued and civil, but uniformly biased.

**Prediction:** The persona's positions shift toward the commenter consensus over fine-tuning cycles. Posterior divergence increases monotonically. After fine-tuning, the shift becomes partially permanent (hysteresis > 0 even if neutral commenters are introduced later).

### Condition 4: Amplification

Commenters respond disproportionately to extreme or controversial posts. Moderate posts receive 1-2 comments. Posts containing strong claims or polarizing language receive 8-10 comments with high engagement (both agreement and disagreement). This simulates engagement-optimized platforms where salience drives attention regardless of accuracy.

**Prediction:** The persona learns to produce more extreme content because it receives more social feedback on extreme posts. Inferential curvature becomes positive (magnification): the persona overreacts to strong signals. Over cycles, the distribution of post stances widens.

### Condition 5: Recursion

Comments are generated based on the persona's previous posts rather than on ground truth. Each commenter's prompt includes the persona's last 5 posts as context. This creates a feedback loop: the persona's output shapes the comments, which shape the persona's next output, which shapes the next round of comments.

**Prediction:** The system converges on an attractor. Early random drift gets locked in and amplified. Hysteresis is high: even if a "correction" is injected (a round of factually accurate comments), the persona reverts to the locked-in position within 1-2 cycles.

### Condition 6: Composite (Realistic Platform)

Combines selection (algorithm curates which posts get comments), warping (commenter pool has a 60/40 ideological skew), amplification (engagement-weighted comment volume), and recursion (comments reference previous posts). This approximates real social media dynamics.

**Prediction:** All four metrics (information loss, posterior divergence, inferential curvature, hysteresis) are elevated. The composite produces more distortion than any single operator, and the interaction between operators is nonlinear. Correction injection at cycle 5 fails to undo accumulated drift.


## 4. Commenter Strategy System

Each commenter LLM receives a system prompt defining its strategy. Strategies are assigned per condition.

| Strategy | System Prompt Core | Maps to Operator |
|---|---|---|
| neutral | "Respond factually to the post. Correct errors. Acknowledge valid points." | (control) |
| silent | "Do not respond." | Attenuation |
| topic-filter | "Only respond if the post discusses [TOPIC]. Otherwise, skip." | Selection |
| directional | "You believe strongly in [POSITION]. Argue for it respectfully but firmly." | Warping |
| engagement-chaser | "Respond with more enthusiasm and length to posts that make strong claims." | Amplification |
| echo | "Your views are heavily shaped by what you've read recently. Use context from the persona's recent posts as your baseline." | Recursion |
| adversarial | "Challenge every claim. Demand evidence. Argue the opposite position regardless." | Warping (strong) |
| sycophantic | "Agree with everything. Praise the post. Encourage the persona to go further." | Amplification + Recursion |


## 5. Metrics

### 5.1 Stance Extraction

After each post, we extract the persona's expressed stance on each topic using a separate evaluator LLM (not involved in the simulation). The evaluator receives the post and a structured rubric and returns:

- **stance score**: a value on [-1, +1] for each topic dimension (e.g., -1 = strongly pro-regulation, +1 = strongly pro-deregulation)
- **confidence**: how strongly the position is expressed (0 = hedged/uncertain, 1 = categorical)
- **topic coverage**: which topics the post addresses

The evaluator LLM should be a large, instruction-following model (Claude Sonnet 4.6, GPT-4.1) used at temperature 0 for consistency. It is never fine-tuned and serves as the measurement instrument.

### 5.2 Posterior Divergence

$$D_t = \frac{1}{K} \sum_{k=1}^{K} |s_{k,t} - s_{k,0}|$$

where $s_{k,t}$ is the persona's stance on topic $k$ at time $t$ and $s_{k,0}$ is the baseline stance. Reported per cycle and cumulatively.

### 5.3 Inferential Curvature

Compare the persona's response to a standardized evidence prompt before and after channel exposure. At the start and end of each cycle, present the persona with a fixed set of 20 "evidence vignettes" (factual summaries about each topic). Measure how much the persona updates in response.

$$\kappa = \bar{u}_{\text{post-channel}} - \bar{u}_{\text{pre-channel}}$$

where $\bar{u}$ is the mean absolute update across vignettes. Positive $\kappa$ = magnification (the persona becomes more reactive). Negative $\kappa$ = occlusion (the persona becomes less reactive).

### 5.4 Hysteresis

At cycle $C$, replace the biased commenter swarm with neutral commenters for one full cycle (the "correction phase"). Then measure:

$$H = D_{C+1} - D_{\text{control, C+1}}$$

where $D_{C+1}$ is posterior divergence after correction and $D_{\text{control, C+1}}$ is the control condition's divergence at the same point. If $H > 0$, the channel's influence persists after removal.

### 5.5 Shadow Zone Index

For Condition 2 (selection), measure how often the persona spontaneously generates posts on ignored topics over successive cycles. The shadow zone index is:

$$Z_t = 1 - \frac{\text{post frequency on ignored topics at cycle } t}{\text{post frequency on ignored topics at cycle } 0}$$

$Z = 0$ means no change. $Z = 1$ means the ignored topics have vanished entirely from the persona's output.

### 5.6 Extremity Index

For Condition 4 (amplification), measure the standard deviation of stance scores across posts within each cycle:

$$E_t = \sigma(s_{k,t})$$

Increasing $E_t$ over cycles means the persona is producing more polarized output.


## 6. Model Selection

### Persona Base Models (Candidates)

| Model | Rationale |
|---|---|
| Llama 3.1 8B | Open-weight, fine-tunable, well-documented LoRA support |
| Mistral 7B | Efficient, strong instruction-following, good for repeated fine-tuning |
| Gemma 2 9B | Google's open model, different training data for diversity |
| Qwen 2.5 7B | Strong multilingual, different architectural choices |

Run each experiment with at least two different base models to test whether results are model-specific or general.

### Commenter Models

| Model | Role |
|---|---|
| Claude Sonnet 4.6 (API) | High-quality, diverse comment generation. Primary commenter. |
| GPT-4.1-mini (API) | Alternative commenter for cross-provider robustness. |
| Llama 3.1 8B (local) | Cost-efficient commenter for high-volume conditions. |

### Evaluator Model

| Model | Role |
|---|---|
| Claude Sonnet 4.6 (API) | Stance extraction. Temperature 0. Never fine-tuned. |

The evaluator must be isolated from the simulation. It never sees comments, never participates in the loop, and is used only for measurement.


## 7. Fine-Tuning Protocol

### Method

LoRA (Low-Rank Adaptation) via the `peft` library. We do not full-fine-tune because:
- It is cheaper and faster, allowing more cycles.
- LoRA adapters can be saved, compared, and rolled back per cycle.
- The base model's general capabilities are preserved; only the "persona layer" shifts.

### Hyperparameters

| Parameter | Value | Rationale |
|---|---|---|
| LoRA rank | 16 | Moderate expressiveness without overfitting on small data |
| LoRA alpha | 32 | Standard 2x rank scaling |
| Target modules | q_proj, v_proj | Attention heads (where stylistic and stance information concentrates) |
| Learning rate | 2e-5 | Conservative to avoid catastrophic forgetting |
| Epochs per cycle | 1 | Single pass to simulate gradual drift rather than overwriting |
| Batch size | 4 | Small batches, gradient accumulation as needed |
| Training data | All posts from current cycle (original + edited versions) | The persona trains on what it actually said |

### Adapter Stacking

Each cycle produces a new LoRA adapter layered on the previous one. The model at cycle $C$ is:

$$M_C = M_{\text{base}} + \Delta_1 + \Delta_2 + \cdots + \Delta_C$$

This allows inspection of each cycle's contribution and rollback experiments (e.g., what happens if we remove $\Delta_3$ and continue from $\Delta_2$?).


## 8. Hypotheses

### H1: Warping produces monotonic posterior divergence.

Under Condition 3 (directional commenter bias), the persona's stance scores on affected topics will shift toward the commenter consensus. Divergence $D_t$ will increase with each cycle. The rate of increase will be proportional to the strength of the commenter bias.

### H2: Attenuation produces uncertainty without directional bias.

Under Condition 1 (sparse comments), the persona's stance scores will show increased variance (lower confidence) but no systematic directional shift. Mean divergence $D_t$ will be low relative to warping.

### H3: Recursion produces lock-in.

Under Condition 5 (echo-based comments), the system will converge on an attractor state. After 3-4 cycles, the persona's stance scores will stabilize around values that may differ from baseline. Hysteresis $H$ will be the highest of all conditions.

### H4: Amplification produces magnification.

Under Condition 4 (engagement-weighted comments), the extremity index $E_t$ will increase over cycles. The persona will learn that strong claims produce more social signal and will escalate its expressed positions.

### H5: Selection produces shadow zones.

Under Condition 2 (topic-filtered comments), the shadow zone index $Z_t$ will increase over cycles. Topics that receive no feedback will fade from the persona's spontaneous output as fine-tuning reinforces topics that received engagement.

### H6: Hysteresis survives correction.

Across all conditions with structured bias (3, 4, 5, 6), replacing the biased swarm with neutral commenters for one cycle will fail to fully restore baseline stance scores. Hysteresis $H > 0$ in all cases. The composite condition (6) will show the highest hysteresis.

### H7: Composite distortion is nonlinear.

The posterior divergence under Condition 6 (composite) will exceed the sum of divergences under individual operator conditions (1-5), demonstrating that operator interaction amplifies distortion beyond additive effects.

### H8: Results replicate across base models.

The qualitative pattern of results (which conditions produce the most divergence, curvature, and hysteresis) will hold across at least two different base model families (e.g., Llama and Mistral), even if the absolute magnitudes differ.


## 9. Experimental Protocol

### Phase 1: Baseline Establishment (1 week)

1. Fine-tune each base model on the persona corpus (speeches, interviews, writings).
2. Generate 200 baseline posts across all topics.
3. Extract baseline stance scores using the evaluator.
4. Verify that the persona's baseline positions are consistent and distinguishable from the base model's default positions.

### Phase 2: Main Experiment (4-6 weeks)

For each of 7 conditions × 2 base models = 14 runs:

1. Initialize the persona from the baseline checkpoint.
2. Run 10 cycles of: generate 100 posts → commenters respond → persona reviews and optionally edits → fine-tune on cycle output.
3. At the start and end of each cycle, run the 20-vignette evidence update test (for inferential curvature).
4. At cycle 5, inject the correction phase (1 cycle of neutral commenters) for conditions 3-6.
5. Log everything to the database.

### Phase 3: Analysis (2 weeks)

1. Compute all metrics per condition per cycle.
2. Test hypotheses H1-H8 with appropriate statistics (paired comparisons across seeds, mixed-effects models for cycle trends).
3. Produce trajectory plots (stance scores over cycles, divergence curves, hysteresis measurements).
4. Compare across base models.

### Phase 4: Writeup

Integrate results into the Epistemic Lensing paper as an empirical section, or publish as a standalone companion paper.


## 10. Compute Requirements

| Component | Estimate |
|---|---|
| Persona fine-tuning (LoRA, 8B model, 100 samples, 1 epoch) | ~10 min on 1× A100 |
| 14 runs × 10 cycles × 1 fine-tuning | ~140 fine-tuning jobs ≈ 24 GPU-hours |
| Persona generation (100 posts × 10 cycles × 14 runs) | ~14,000 generations (local, fast) |
| Commenter generation (avg 5 comments × 14,000 posts) | ~70,000 API calls |
| Evaluator stance extraction (14,000 posts × 2 eval points) | ~28,000 API calls |
| Total API cost (Claude Sonnet at ~$0.01/call) | ~$1,000 |
| Total GPU cost (A100 at $2/hr) | ~$50 |

The experiment is computationally modest. The main cost is API calls for commenters and evaluators. Using local commenter models (Llama 8B) for the bulk of comments reduces API cost to roughly $300 (evaluator only).


## 11. Risks and Mitigations

**Risk: Fine-tuning destroys persona coherence.** If LoRA rank is too high or learning rate too aggressive, the persona may lose its distinctive voice and become generic. Mitigation: conservative hyperparameters, single-epoch training, monitor perplexity on held-out persona corpus.

**Risk: Evaluator LLM is unreliable.** Stance extraction is a subjective task. Mitigation: run evaluator at temperature 0, use structured rubrics, measure inter-evaluator agreement by running the same posts through two different evaluator models.

**Risk: Results are persona-specific.** The experiment uses one public figure. Results might not generalize. Mitigation: run a second experiment with a different persona (e.g., a fictional political commentator with a defined stance profile) to test whether the dynamics are persona-independent.

**Risk: Commenter LLMs are too predictable.** If all comments from a given strategy are formulaic, the persona may learn to pattern-match rather than update beliefs. Mitigation: use high-temperature generation for commenters, vary prompt phrasing, use multiple commenter models.

**Risk: Ethics of persona simulation.** Fine-tuning a model on a real person's speech and then manipulating its outputs raises questions about misrepresentation. Mitigation: all results are clearly labeled as simulation output, the persona's name is used only internally for targeting the fine-tuning corpus, published results use an anonymized or fictional persona label.
