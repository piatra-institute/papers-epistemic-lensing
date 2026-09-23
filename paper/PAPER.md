---
title: |
  Epistemic Lensing:\
  A Markov-Blanket Account of\
  Mediated Belief Distortion
author: PIATRA . INSTITUTE
date: April 2026
---

## Abstract

Public epistemic failure is usually described by volume of information or by discrete false claims. We describe it by the shape of the channel between world and belief. *Epistemic lensing* is defined, within a Markov-blanket framing, as systematic divergence between the posterior an agent forms from a mediated stream and the benchmark posterior a higher-fidelity channel would support. Five distortion operators (attenuation, selection, warping, amplification, recursion) and four metric families (information loss, posterior divergence, inferential curvature, hysteresis) make the concept measurable. A seeded toy model, in which a one-dimensional Kalman agent that cannot observe its channel tracks a random-walk world over 400 repetitions, gives each operator a distinct signature. Attenuation loses information (0.37) at near-zero curvature. Selection with warping loses the most (0.88) with negative curvature ($-0.27$). Amplification produces the largest posterior divergence (0.36 bits) and strong positive curvature ($+1.06$). Recursion loses least (0.16) and blunts updating ($-0.43$). In three of the four channels the mediated posterior is displaced while its width is unchanged, so the agent is confidently wrong. After a world reversal, residual divergence tracks each channel's steady-state distortion and does not isolate a memory-specific residue. Extended to populations, the framework defines posterior shear, focal capture, shadow zones, and narrative gravity wells. Ignorance and distortion have different signatures and call for different remedies: more signal in the first case, differently structured channels in the second.


## 1. Introduction

The standard vocabulary for epistemic failure in public life is thin. Citizens are called "low information" or "high information," as though the relevant variable were volume. "Misinformation" and "disinformation" treat the problem as discrete false propositions injected into an otherwise clean signal. "Media bias" treats distortion as a scalar that can be placed on a left-right axis and corrected by balance.

None of these framings captures the structure of the problem. Two agents exposed to the same underlying reality through differently structured channels disagree about more than facts. They disagree about what counts as evidence, how strongly evidence bears on conclusions, and which aspects of reality are salient at all. The relevant variable is the shape of the transformation between world and belief, of which the amount of information is one component.

Ignorance is one form of the pathology. Guided misperception under structured mediation is another, and the second is the subject here. Its central concept, *epistemic lensing*, is the systematic deformation of belief-updating induced by the channel between world and agent. The optical term names a specific property: a lens transmits light and changes its path. A mediating channel can likewise preserve most of the information it receives and still reshape the inferential path from evidence to posterior. Some reshaping is corrective, since journalism, expertise, and synthesis often *increase* fidelity relative to raw sensory exposure. Distortion begins where the channel moves posterior beliefs away from what a higher-fidelity channel would support.

The framework has three components: a *three-layer architecture* (world, channel, posterior) formalized through Markov blankets; a *taxonomy of distortion operators* describing the elementary ways a channel can reshape inference; and a *family of metrics* that make distortion measurable. A toy Bayesian simulation computes the metrics for each operator, and a population extension describes collective phenomena (polarization, epistemic fragmentation, persistent miscalibration) that no account of individual cognitive failure explains on its own.


## 2. Theoretical Framework

### 2.1 The Three-Layer Architecture

Agents encounter the world through channels. Mediation is the basic architecture of bounded cognition and is not in itself pathological. An organism's sensory apparatus is a channel that compresses, selects, and transforms environmental signals into a format the organism can process. The relevant questions are what *kind* of mediation occurs and what it does to inference.

The architecture has three layers:

- **World** $W_t$: the state of affairs at time $t$, including events, causal structure, and distributions over observables.
- **Evidence stream** $X_t$: a relatively high-fidelity signal from $W_t$, the best evidence reasonably available, which need not be "raw reality" (often inaccessible).
- **Mediated stream** $M_t$: the signal that reaches the agent after processing by a mediating channel $\mathcal{C}$.

The agent forms a posterior belief $q(W_t \mid \cdot)$ from whichever stream it receives. Two posteriors are distinguished:

- $q^*(W_t \mid X_t)$: the *benchmark posterior*, what a well-calibrated agent would believe given high-fidelity evidence.
- $q_i(W_t \mid M_t)$: agent $i$'s *mediated posterior*, what the agent comes to believe given the channel output.

### 2.2 Markov-Blanket Framing

The architecture corresponds to the Markov-blanket formalism [@pearl1988; @friston2013]. In active inference, an agent is separated from its environment by a Markov blanket: sensory and active states that mediate all interaction between internal and external states [@friston2017]. The agent's internal model of the world is updated only through blanket-facing inputs.

A mediating channel $\mathcal{C}$ sits between the environment and the blanket and transforms the evidence stream before it reaches the agent's sensory surface:

$$M_t = \mathcal{C}(X_t, \theta_{\mathcal{C}})$$

where $\theta_{\mathcal{C}}$ parameterizes the channel's structure: noise level, selection function, amplification profile, and so on. The agent observes $M_t$ and never $\mathcal{C}$ itself, and updates accordingly. From the agent's side, $M_t$ *is* the evidence.

### 2.3 Definition

\begin{definition}[Epistemic Lensing]
Epistemic lensing occurs when the mapping $W_t \to M_t \to q_i$ systematically deforms belief relative to the benchmark mapping $W_t \to X_t \to q^*$. Formally, a channel $\mathcal{C}$ induces epistemic lensing with respect to benchmark $q^*$ if, for a non-negligible set of world states and time periods:
$$D\big(q_i(W_t \mid M_t),\; q^*(W_t \mid X_t)\big) > \epsilon$$
where $D$ is a divergence measure on probability distributions and $\epsilon > 0$ is a calibration tolerance.
\end{definition}

The benchmark $q^*$ is the posterior a well-calibrated agent would form from a *higher-fidelity* channel. It makes no claim to omniscience or to direct access to $W_t$; the framework measures *relative* fidelity.

Mediation can improve calibration. A channel that compresses redundant signals, filters noise, or synthesizes scattered evidence may leave the agent better calibrated than raw exposure would. Epistemic lensing refers to the *deformative* component: the residual divergence after any corrective value of the channel is accounted for.

The distortion must also be *systematic*. Random errors wash out under repeated observation. Epistemic lensing describes *structured* deformation: consistent directional bias, systematic salience warping, or persistent occlusion of specific domains.


## 3. Distortion Operators

Five elementary operations describe how a channel $\mathcal{C}$ can reshape inference. Real mediating systems are treated as compositions of these operators.

### 3.1 Attenuation $\mathcal{A}$

Attenuation removes signal. The channel transmits less information than it receives:

$$I(W_t; M_t) < I(W_t; X_t)$$

where $I(\cdot;\cdot)$ is mutual information [@shannon1948]. Attenuation increases uncertainty without biasing inference in a particular direction. The posterior becomes wider and less confident; in the limit, total attenuation leaves the agent at maximum entropy.

*Examples*: news deserts (geographic attenuation of local information), paywalls (economic attenuation), language barriers, algorithmic deprioritization of low-engagement content.

### 3.2 Selection $\mathcal{S}$

Selection passes some signals and blocks others. Attenuation reduces signal uniformly; selection acts on *content*:

$$M_t = \mathcal{S}(X_t) = X_t \cdot \mathbf{s}$$

where $\mathbf{s} \in \{0,1\}^n$ is a selection mask over $n$ dimensions of the evidence space. The agent receives a *partial* world-model, accurate in the domains the channel transmits and empty in the domains it blocks.

Selection is hazardous because the agent cannot detect it. It cannot distinguish "nothing is happening in domain $d$" from "the channel does not transmit domain $d$." This asymmetry between absence of evidence and evidence of absence is the epistemic core of selection bias.

*Examples*: editorial selection of stories, algorithmic content curation, geographic isolation from certain populations or events, institutional specialization.

### 3.3 Warping $\mathcal{W}$

Warping reframes content. The channel transforms the *meaning* of the signals it passes relative to the agent's inferential framework:

$$M_t = \mathcal{W}(X_t) = f_{\mathcal{W}}(X_t)$$

where $f_{\mathcal{W}}$ is a nonlinear transformation that preserves some structural features of $X_t$ and distorts others. Warping produces directional bias: the posterior is *shifted* toward specific regions of belief-space, in addition to any broadening or narrowing.

*Examples*: partisan framing, euphemism and dysphemism, context-stripping, misleading juxtaposition, emotive imagery selection.

### 3.4 Amplification $\mathcal{G}$

Amplification overweights certain cues relative to their evidential strength:

$$M_t^{(j)} = g_j \cdot X_t^{(j)}, \quad g_j > 1 \text{ for some } j$$

where $g_j$ is a gain factor on dimension $j$ of the evidence. Amplification produces *salience inflation*: the agent treats certain signals as more informative than they are. If the amplified cues are diagnostic, performance improves. If they are not, calibration degrades because posterior mass concentrates on a narrow subset of the evidence.

*Examples*: sensationalist coverage of rare events, trending algorithms that promote high-engagement content regardless of base rate, exploitation of the availability heuristic [@tversky1974].

### 3.5 Recursion $\mathcal{R}$

Recursion occurs when the channel's output feeds back into itself:

$$M_{t+1} = \mathcal{C}(X_{t+1}, M_t)$$

The channel at time $t+1$ depends on new evidence and on its own prior output. The result is *path dependence*: beliefs at $t$ shape the channel at $t+1$, which shapes beliefs at $t+2$. Recursion is the operator responsible for *hysteresis*, the persistence of distorted beliefs after corrective evidence arrives, and for *lock-in*, in which initial channel biases compound over time.

*Examples*: recommendation algorithms that personalize content by prior engagement [@pariser2011], echo chambers, confirmation-seeking information behavior, viral amplification of early framings.

### 3.6 Composition

Real mediating systems compose these operators. A social media feed may *select* (algorithmic curation), *amplify* (engagement-weighted ranking), *warp* (framing by content creators), and *recurse* (personalization by prior behavior) at once. The distortion of the composite channel arises from the interaction of the individual distortions, which can be nonlinear, and need not equal their sum. A mildly selective channel with strong recursion may distort more than a heavily warped channel without feedback.


## 4. Distortion Metrics

Four families of metrics measure distortion, each capturing a different aspect of how the channel deforms inference.

### 4.1 Information Loss

Information loss measures how much world-relevant information survives mediation:

$$\mathcal{L} = 1 - \frac{I(W_t; M_t)}{I(W_t; X_t)}$$

$\mathcal{L} = 0$ means the channel preserves all world-relevant information, even if it warps or amplifies; $\mathcal{L} = 1$ means total attenuation. The metric records the *quantity* of evidential signal destroyed, without regard to direction.

Low information loss does not imply low distortion, because a channel can preserve mutual information while systematically warping the *structure* of the signal. Information loss is therefore a necessary and insufficient indicator.

### 4.2 Posterior Divergence

Posterior divergence measures how far the mediated posterior departs from the benchmark:

$$\mathcal{D} = D_{JS}\big(q_i(W_t \mid M_t),\; q^*(W_t \mid X_t)\big)$$

where $D_{JS}$ is the Jensen-Shannon divergence, which is symmetric, bounded, and defined even when the distributions do not share support. Posterior divergence is the most direct measure of epistemic lensing: it compares what the agent believes with what it would believe under a better channel.

Posterior divergence decomposes into *location shift* (the posterior mean moves), *dispersion change* (the posterior width changes), and *shape distortion* (changes in geometry not captured by location and scale). The decomposition separates, for instance, an agent who is confidently wrong (small dispersion change, large location shift) from one who is confused (large dispersion change, small location shift).

### 4.3 Inferential Curvature

The third metric compares the *sensitivity* of belief-updating to evidence under the two channels, where posterior divergence compares the *level* of belief.

Let $e$ denote an increment of evidence and define the *update function*

$$u(e) = \frac{\partial q(W_t)}{\partial e}.$$

Inferential curvature is the difference in update sensitivity between mediated and benchmark channels:

$$\kappa = u_\text{mediated}(e) - u_\text{benchmark}(e)$$

Three regimes follow:

- $\kappa > 0$: **magnification**. The agent updates too much from evidence of a given strength, treating weak signals as strong.
- $\kappa < 0$: **occlusion**. The agent updates too little, and strong signals fail to move belief.
- $\text{sign}(\kappa) \neq \text{sign}(u_\text{benchmark})$: **deflection**. The agent updates in the wrong direction: evidence that should increase $q$ decreases it, or the reverse.

Two agents can hold the *same* posterior at time $t$ with *different* curvatures and will then respond differently to future evidence. Curvature is a second-order property of the inferential surface, and posterior divergence, a first-order property, does not register it.

### 4.4 Hysteresis

Hysteresis measures how much distortion persists after corrective evidence arrives. Let $E_\text{correct}$ be a corrective evidence event that, under the benchmark channel, would bring the posterior to within $\epsilon$ of $q^*$. Hysteresis is the residual divergence after correction:

$$\mathcal{H} = D_{JS}\big(q_i(W_t \mid M_{1:t}, E_\text{correct}),\; q^*(W_t \mid X_{1:t}, E_\text{correct})\big)$$

$\mathcal{H} = 0$ means complete correction, with the agent returning to the benchmark. $\mathcal{H} > 0$ means *epistemic residue*: the history of distortion leaves a trace that survives corrective evidence. The empirical counterpart is the continued influence of misinformation after retraction [@lewandowsky2012] and the limited and variable effect of fact-checking [@walter2020].

Hysteresis is the metric most directly relevant to democratic epistemology. A society can tolerate temporary distortion if correction works. When hysteresis is high, even accurate corrective information fails to undo accumulated distortion, which has settled into the agent's posterior and conditions every later update.


## 5. Toy Simulation

### 5.1 Setup

A minimal simulation tests whether the framework yields quantitatively distinct patterns of distortion. It has one world state, one agent, and one channel, observed over time.

**World.** A continuous latent state $W_t \in \mathbb{R}$ evolves as a random walk:

$$W_{t+1} = W_t + \eta_t, \quad \eta_t \sim \mathcal{N}(0, \sigma_W^2)$$

**Evidence stream.** The high-fidelity evidence is the world state plus observation noise:

$$X_t = W_t + \xi_t, \quad \xi_t \sim \mathcal{N}(0, \sigma_X^2)$$

**Mediated stream.** The channel applies a parameterized transformation:

$$M_t = (1-\gamma)\big(\mathcal{S}(X_t) + \beta \cdot b\big) + \gamma \cdot M_{t-1} + \nu_t$$

where:

- $\mathcal{S}$ is a selection function that drops the signal with probability $p_\text{omit}$ (on a dropped step the agent receives channel noise carrying no information about $W_t$ and runs no update),
- $\beta$ controls warping (injection of directional bias $b$),
- $\gamma \in [0,1)$ controls recursion (dependence on prior channel output),
- $\nu_t \sim \mathcal{N}(0, \sigma_\nu^2)$ is channel noise.

Attenuation is modeled as reduced signal-to-noise: a parameter $\alpha \in (0,1]$ adds $(1/\alpha - 1)\,\sigma_X^2$ of variance, so the channel still tracks $X_t$ without directional bias and transmits less information. Multiplicative shrinkage of the mean was avoided because it injects the directional bias the framework assigns to warping. Amplification scales the surprising part of the signal, the innovation $X_t - X_{t-1}$, by a gain $g > 1$ whenever that jump exceeds a threshold $\tau$, so the operator inflates rare events and leaves the level of the signal alone.

**Agent.** A Bayesian updater (a one-dimensional Kalman filter on the random-walk prior) maintains a Gaussian posterior $q_t = \mathcal{N}(\mu_t, \sigma_t^2)$ with Kalman gain $k_t = \sigma_t^2 / (\sigma_t^2 + \sigma_\text{obs}^2)$:

$$\mu_t = k_t \cdot M_t + (1 - k_t) \cdot \mu_{t-1}$$

In keeping with Section 2.2, the agent does not observe the channel $\mathcal{C}$. It uses a fixed assumed observation noise $\sigma_\text{obs}$, treats $M_t$ as direct evidence, and therefore cannot widen its posterior to account for a degraded channel. The same agent run on the high-fidelity stream $X_t$ supplies the benchmark posterior $q^*$; run on $M_t$ it supplies the mediated posterior $q_i$. All distortion is measured as $q_i$ relative to $q^*$ on the same world and evidence draw.

**Estimators.** Information loss uses the Gaussian mutual information computed from the sample correlation. Posterior divergence is the Jensen-Shannon divergence between $q_i$ and $q^*$, averaged over time steps; its location component is the mean absolute difference of posterior means and its dispersion component the mean difference of posterior standard deviations, both in units of the world state. Curvature is estimated as the least-squares slope of the per-step belief change on the true world change, mediated minus benchmark. Hysteresis is described in Section 5.3.

### 5.2 Scenarios

Four channel configurations each isolate one distortion operator, with all other parameters at baseline. Each metric is averaged over 400 seeded repetitions of a 200-step run; a single command reproduces the run and writes `simulation/output/results.json`.

**Scenario A: attenuation.** $\alpha = 0.3$, all other distortion parameters zero. The agent receives a low signal-to-noise signal. *Hypothesis*: degraded tracking with no systematic directional pull.

**Scenario B: selection and warping.** $p_\text{omit} = 0.5$, $\beta = 0.4$ (positive bias). The agent misses half the evidence and receives a directionally biased remainder. *Hypothesis*: posterior shifted toward $b$, with intermittent tracking when transmitted signals arrive.

**Scenario C: amplification.** $g = 3$ on innovations with $|X_t - X_{t-1}| > \tau$ (rare jumps amplified). *Hypothesis*: salience inflation, with the agent overreacting to surprising signals and its posterior oscillating more than $q^*$.

**Scenario D: recursion.** $\gamma = 0.7$ (strong autoregressive feedback). *Hypothesis*: the channel mixes old and new signal, so the posterior tracks $W_t$ with a lag.

### 5.3 Results

All values are read from `results.json`. Divergences are Jensen-Shannon in bits, bounded in $[0,1]$.

**Information loss** ($\mathcal{L}$). Loss is highest under selection with warping (B, $\mathcal{L} = 0.88$), where dropping half the steps destroys the most mutual information. Amplification is also high (C, $\mathcal{L} = 0.68$), because scaling rare innovations decorrelates $M_t$ from $W_t$. Attenuation is moderate (A, $\mathcal{L} = 0.37$). Recursion is lowest (D, $\mathcal{L} = 0.16$): the channel preserves the signal and delays it.

**Posterior divergence** ($\mathcal{D}$). Divergence is highest under amplification (C, $\mathcal{D} = 0.36$). The other three cluster (A $= 0.22$, B $= 0.24$, D $= 0.24$), so the scalar alone understates how differently the channels fail. The decomposition of Section 4.2 separates them. All four channels displace the posterior mean, by a mean absolute shift of 0.86 (A), 1.07 (B), 1.39 (C), and 0.92 (D) in units of the world state. Only selection with warping also widens the posterior (dispersion change $= 0.44$), because dropped steps leave the agent less certain. The other three have a dispersion change of $0.00$, identically zero by construction: the agent updates on every step with a fixed assumed noise, so its posterior variance follows the same recursion as the benchmark's. The agent is displaced while remaining as confident as the benchmark agent, which is the formal content of *confidently wrong*.

**Inferential curvature** ($\kappa$). Curvature is near zero under attenuation (A, $\kappa = -0.00$): the agent responds with the benchmark sensitivity and more noise. It is strongly positive under amplification (C, $\kappa = +1.06$), a magnification in which the agent updates far more than the evidence warrants. It is negative under selection with warping (B, $\kappa = -0.27$) and recursion (D, $\kappa = -0.43$), an occlusion in which dropped steps and stale channel memory blunt the response to new evidence. Of the four metrics, curvature separates the operators most cleanly, including where posterior divergence does not.

**Hysteresis** ($\mathcal{H}$). At $t = 150$ the world reverses direction. The corrective evidence then arrives through each channel, with no external oracle, and hysteresis is the mean Jensen-Shannon divergence over the following 10 steps. Amplification leaves the largest residue (C, $\mathcal{H} = 0.35$), because the reversal is itself a large innovation that the channel over-amplifies. Selection with warping (B, $\mathcal{H} = 0.25$) and recursion (D, $\mathcal{H} = 0.24$) follow, and attenuation is lowest (A, $\mathcal{H} = 0.22$). In this single-agent model the post-reversal residual tracks each channel's steady-state distortion and does not isolate a memory-specific residue. Recursion lags, but a single reversal does not make it uniquely hard to correct; lock-in requires sustained recursion across a population, which a one-shot correction does not test (Section 6.5).

### 5.4 Ignorance and Distortion in the Simulation

The model gives the distinction between ignorance and distortion distinct numerical signatures. Attenuation is ignorance: moderate information loss (0.37), curvature near zero, and divergence carried by unbiased location error; the agent is wrong only through noise. Amplification and selection with warping are distortion. Amplification combines the highest divergence (0.36) with strong positive curvature ($+1.06$); selection with warping combines the highest information loss (0.88) with negative curvature ($-0.27$). The decomposition carries the strongest evidence: three of the four channels displace the posterior without widening it, so the agent is confident and wrong at once. The blanket assumption, that the agent cannot see its channel, makes confident error the default response to a degraded signal, where honest uncertainty would require knowledge of the channel.


## 6. Population Extension

### 6.1 From Individual to Field

The framework extends from a single agent to a population. Suppose $N$ agents each receive $W_t$ through a potentially different channel $\mathcal{C}_{i}$ with parameters $\theta_{{\mathcal{C}}_i}$. The population's belief state is the *posterior field*, the distribution of posteriors $\{q_1, q_2, \ldots, q_N\}$ across agents.

At the population level, public distortion appears as a deformed inferential field across many agents, in addition to the false beliefs visible in individuals.

### 6.2 Posterior Shear

When subpopulations are exposed to differently structured channels, their posteriors diverge systematically. *Posterior shear* is defined as

$$\Sigma = D_{JS}\big(\bar{q}_A,\; \bar{q}_B\big)$$

where $\bar{q}_A$ and $\bar{q}_B$ are the average posteriors of groups $A$ and $B$. High shear means the groups hold systematically different pictures of the same world. The cause is structural: the channels deliver differently shaped evidence whether or not the groups share values or priors.

Posterior shear differs from polarization in the usual sense. Two groups can be polarized because they weight evidence differently, a cognitive phenomenon. Posterior shear describes groups polarized *because the evidence that reaches them is differently structured*, a channel phenomenon. The distinction matters for intervention: cognitive depolarization strategies such as perspective-taking and deliberation will fail if the underlying channel structure stays divergent.

### 6.3 Focal Capture

When a channel amplifies a narrow set of signals, collective attention collapses onto them. *Focal capture* occurs when

$$H\big(\text{Attention}(t)\big) < H_\text{benchmark}$$

where $H$ is the entropy of the attention distribution over topics. The population attends to fewer topics than the world's complexity warrants. The captured topics may be important; the cost is that other important topics fall below the threshold of collective visibility.

### 6.4 Shadow Zones

The dual of focal capture is the *shadow zone*, a region of the world that becomes effectively invisible because the channel rarely transmits it. A shadow zone is a topic the channel *could* transmit and *does not*, either because it fails selection criteria (judged unnewsworthy or low-engagement) or because it is actively suppressed.

Shadow zones are hazardous because they are invisible. An agent in a shadow zone does not know that information is missing, since the channel provides no signal of the absence.

### 6.5 Narrative Gravity Wells

A *narrative gravity well* is a dominant explanatory frame that draws heterogeneous evidence into a single attractor basin. Once established, the narrative reinterprets incoming evidence to fit itself:

- Confirming evidence is assimilated directly.
- Disconfirming evidence is reframed ("that's exactly what they would say").
- Ambiguous evidence is recruited ("this proves it's even deeper than we thought").

Narrative gravity wells combine warping (evidence is reframed), amplification (confirming cues are overweighted), and recursion (the narrative feeds back into itself). They are stable because they are self-reinforcing, and they produce high hysteresis because corrective evidence is absorbed into the frame instead of updating it.


## 7. Empirical Program

The framework suggests an empirical research program at three levels.

### 7.1 Individual Level

At the individual level, epistemic lensing predicts measurable differences in belief calibration, update sensitivity, and response to correction as a function of channel structure. The relevant variables are:

- **Calibration error**: the gap between an agent's confidence and accuracy, measured across domains.
- **Update sensitivity**: how far an agent's posterior shifts in response to standardized evidence, compared with a Bayesian benchmark.
- **Correction persistence**: whether belief revision from corrective information endures, or whether prior distortion reasserts itself.

Experimental designs would expose participants to identical world-state information through differently structured channels and measure downstream belief, confidence, and updating.

### 7.2 Channel Level

At the channel level, the framework predicts that measurable properties of mediating systems (concentration, diversity, repetition, ranking logic, cue distribution) predict population-level distortion metrics. The relevant variables are:

- **Source concentration**: the Herfindahl index of information sources within a population.
- **Signal diversity**: the entropy of topic coverage relative to a benchmark of world-state dimensionality.
- **Recursion depth**: the degree to which a channel's output at $t$ depends on its output at $t-1$, measurable in recommendation systems by autoregressive analysis of content feeds.
- **Correction latency**: the delay between a world-state change and the channel's transmission of the corrective signal.

### 7.3 Place Level

At the geographic level, epistemic lensing predicts that local media ecology predicts local belief distortion. The relevant variables are:

- **Broadband access and platform penetration**: which channels are available.
- **Network homophily**: how structurally similar an agent's information network is.
- **Institutional trust**: baseline trust in mediating institutions (journalism, government, science), which conditions how agents weight channel outputs.
- **Channel plurality**: the number of structurally independent information sources available in a locale.

Across all three levels, part of mediation is corrective, since journalism, expertise, and synthesis often increase fidelity. The object of study is the subset of processing that worsens calibration.


## 8. Limitations

**The benchmark is approximate.** Distortion is defined relative to a higher-fidelity channel, and unmediated reality plays no role in the definition. Deciding which channel is higher-fidelity requires judgment and carries its own epistemic assumptions. The framework uses relative fidelity as a tractable proxy and cannot escape this circularity.

**Direct access to reality is often unavailable.** For many questions of public concern (the state of the economy, the course of a pandemic, the effects of a policy), no agent has direct access to $W_t$ and every channel is mediated to some degree. The framework is comparative: it asks which mediation structures produce better-calibrated posteriors and makes no claim that any structure achieves perfect calibration.

**Reliance on mediation is unavoidable.** Most knowledge is second-hand, and a prescription that citizens bypass all channels would be impractical and incoherent. The task is to recognize when a channel's structure deforms inference and when it supports it.

**The framework is silent on normative content.** Epistemic lensing describes *how* beliefs are deformed and says nothing about *which beliefs are correct*. It applies symmetrically: any channel, whatever its ideological orientation, can be assessed for information loss, posterior divergence, inferential curvature, and hysteresis. Whether channels are in fact symmetrically distortive is then an empirical question for the metrics. Work on asymmetric misinformation ecosystems argues that they are not [@benkler2018], and the metrics offer a way to quantify that asymmetry.

**The toy model demonstrates logic and does not model human cognition.** The numbers in Section 5 are computed and reproducible, but the Bayesian agent is a normative benchmark. Real agents show motivated reasoning, identity-protective cognition, and bounded rationality that interact with channel structure in complex ways. The operator parameters are single illustrative settings, the model is one-dimensional, and the single-agent hysteresis test cannot represent population-level lock-in. Empirical validation requires the program of Section 7.


## 9. Conclusion

The familiar diagnosis of public epistemic failure concerns the distance between citizens and reality. A second problem is that the route from reality to belief may be curved in systematic ways. Epistemic lensing describes, measures, and analyzes that curvature through five elementary distortion operators (attenuation, selection, warping, amplification, recursion) and four metric families (information loss, posterior divergence, inferential curvature, hysteresis). Extended from individual agents to populations, it names four collective phenomena induced by channel structure: posterior shear, focal capture, shadow zones, and narrative gravity wells.

The framework's main result is the distinction between *ignorance* and *distortion*. Ignorance is a deficit of signal; distortion is a reshaping of the inferential path. The two have different causes, dynamics, metrics, and remedies, and in the toy model they have different signatures: attenuation loses information at near-zero curvature, while amplification and selection with warping displace the posterior with nonzero curvature and no loss of confidence. A society suffering from ignorance needs more information. A society suffering from distortion needs *differently structured* channels and the institutional capacity to recognize when its channels deform inference. The open political question concerns both who knows what and the structure of the channels through which evidence reaches belief.


## Reproducibility

The toy model is implemented in `simulation/lensing_toy.py` (numpy only) and run by `simulation/run_all.py` with the fixed seed 20260417. The run writes every configuration value and every metric reported in Section 5, at full precision and rounded to two decimals, to `simulation/output/results.json`. Modeling choices left open by the definitions are documented inline in the code.


## References
