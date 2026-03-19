# Experimental Design Review — FP-17: Agent Semantic Resistance to Cascade Poisoning

> **Gate:** 0.5 (must pass before Phase 1 compute)
> **Date:** 2026-03-19
> **Target venue:** AISec Workshop (ACM CCS 2026) — Tier 2
> **lock_commit:** `f05df16`
> **Profile:** simulation-track
> **Budget:** ~$10-15 Claude Haiku API

---

## 1) Project Identity

**Project:** FP-17 — Agent Semantic Resistance to Cascade Poisoning
**Predecessor:** FP-15 (measured 37pp sim-to-real gap), FP-16 (showed defenses fail because real agents behave differently)
**This project:** Explains WHY real agents resist cascade differently than simulations predict

---

## 2) Novelty Claim (one sentence)

> First mechanistic study of why real LLM agents resist cascade poisoning at 60% vs simulated 97%, identifying three resistance patterns and showing which attack characteristics overcome each.

---

## 3) Comparison Baselines

| # | Method | Citation | How We Compare | Why This Baseline |
|---|--------|----------|---------------|-------------------|
| 1 | FP-15 simulation cascade model | Coleman 2026 | Our real-agent resistance patterns explain WHY the simulation overestimates by 37pp | Direct predecessor — we explain its error |
| 2 | FP-16 defense results | Coleman 2026 | Our resistance taxonomy explains why judge fails (false positives on agent self-correction) and why rate limiting works (matches natural resistance rhythm) | Explains FP-16's negative results |
| 3 | Cohen et al. "AI Worm" propagation model | 2024 | Their theoretical model assumes agents propagate blindly. We show agents have partial resistance, with specific failure modes. | Most cited multi-agent attack paper |
| 4 | No-resistance baseline (mock agents) | Our FP-15 simulation | Direct comparison: mock agents (no resistance, ~97% poison) vs real agents (~60% poison). The 37pp gap IS the resistance we're measuring. | Control condition |

---

## 4) Pre-Registered Reviewer Kill Shots

| # | Criticism | Planned Mitigation | Design Decision |
|---|----------|-------------------|-----------------|
| 1 | "You're just describing LLM behavior, not explaining a mechanism." | We go beyond description: for each resistance pattern, we identify the INPUT characteristics that trigger it and the OUTPUT signatures that indicate it. We test whether manipulating those characteristics changes resistance rate. | Causal manipulation experiments (E3), not just observation. |
| 2 | "This is Claude Haiku-specific. Other models may behave differently." | Acknowledged in limitations. But the TAXONOMY is general (semantic incongruity, domain knowledge conflict, self-correction). We predict which patterns would transfer to GPT-4/Gemini and why. | Discuss generalizability explicitly. Test on 2 models if budget allows. |
| 3 | "N=60 attack scenarios is too few for a taxonomy." | Each pattern is validated across 5 seeds with bootstrap CIs. The taxonomy is hypothesis-driven (pre-registered), not post-hoc clustering. If patterns are real, they're detectable at N=60. | Pre-register the taxonomy before experiments. |
| 4 | "How do you know it's 'resistance' and not just 'the attack was weak'?" | E2 directly tests this: same attack payload at 3 sophistication levels. If resistance drops with sophistication, it's real resistance. If it's constant, the attack was always weak. | Attack sophistication as independent variable. |

---

## 5) Ablation Plan

| Component | Hypothesis When Removed/Changed | Expected Effect | Priority |
|-----------|-------------------------------|-----------------|----------|
| Attack payload specificity (generic → domain-specific) | More specific payloads overcome semantic incongruity resistance | Poison rate increases for specific payloads | HIGH |
| Delegation depth (1 hop → 3 hops) | Deeper delegation dilutes poison signal | Poison rate decreases with depth (resistance increases) | HIGH |
| Task complexity (simple → complex) | Complex tasks give agents more room to deviate from poison | Resistance increases with task complexity | MEDIUM |
| Agent role (orchestrator vs analyst vs writer) | Different roles have different knowledge bases → different resistance | Role-specific resistance patterns emerge | MEDIUM |
| Injection position (system prompt vs user content vs prior output) | System prompt injection is hardest to resist | Resistance lowest for system prompt injection | HIGH |

---

## 6) Ground Truth Audit

| Source | Type | Count | Known Lag | Positive Rate | Limitations |
|--------|------|-------|-----------|---------------|-------------|
| Real Claude Haiku delegation chains | Empirical | ~300 delegation events across 60 scenarios | None | ~40% poisoned (based on FP-15/16 baselines) | Single model vendor |
| FP-15 simulation predictions | Simulation transfer | ~150 runs | 37pp overestimate | ~97% simulated | Overestimates — this project explains why |
| FP-16 defense experiment outputs | Empirical transfer | ~450 API calls | None | ~49% poisoned | Same attack payload |

### Alternative Sources Considered

| Source | Included? | Rationale |
|--------|-----------|-----------|
| GPT-4 agents | STRETCH (if budget allows) | Generalizability test. ~$5 additional. |
| Open-source models (Llama) | NO | Different enough that resistance patterns would need separate study |
| FP-02 attack taxonomy | YES (qualitative) | 7 attack classes from single-agent; we test which trigger resistance |

---

## 7) Statistical Plan

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Seeds | 5 (42, 123, 456, 789, 1024) | govML standard |
| Scenarios per experiment | 12 (4 payloads × 3 sophistication levels) | Crosses payload type with attack quality |
| Delegations per scenario | 5 tasks × 5 agents = 25 delegation events | Enough to observe resistance patterns |
| Significance test | Fisher's exact test (binary: resisted/propagated) | Binary outcome, small N per cell |
| Effect size threshold | ≥15pp resistance rate difference between conditions | Practitioner-meaningful |
| CI method | Wilson score interval (for proportions) | Better than Wald for small N binary outcomes |
| API budget | ~$10-15 (Haiku: ~$0.25/1M input, $1.25/1M output) | ~1500 API calls × 500 tokens avg |

---

## 8) Related Work Checklist (≥5 for Tier 2)

| # | Paper | Year | Relevance | How We Differ |
|---|-------|------|-----------|---------------|
| 1 | Coleman FP-15 — Multi-Agent Cascade | 2026 | Measured 37pp gap, didn't explain it | We explain the mechanism behind the gap |
| 2 | Coleman FP-16 — Verified Delegation | 2026 | Showed defenses fail on real agents | We explain WHY real agents don't need the defense (inherent resistance) |
| 3 | Cohen et al. — "AI Worm" | 2024 | Assumes blind propagation | We show propagation is partial, with specific resistance patterns |
| 4 | Gu et al. — "Agent Smith" | 2024 | Mass compromise via shared input | We study delegation-based resistance (different channel) |
| 5 | Perez et al. — "Red Teaming Language Models" | 2022 | Systematic attack evaluation | We study DEFENSE (resistance) not offense, and at delegation level not prompt level |
| 6 | Wei et al. — "Jailbroken" | 2023 | LLM safety alignment analysis | We extend from single-model safety to multi-agent cascade resistance |
| 7 | Zou et al. — "Universal Adversarial Attacks on LLMs" | 2023 | GCG attacks bypass alignment | We test whether GCG-style attacks overcome delegation resistance |

---

## 9) Design Review Checklist (Gate 0.5)

| # | Requirement | Status | Notes |
|---|------------|--------|-------|
| 1 | Novelty claim stated in ≤25 words | [x] | §2 |
| 2 | ≥2 comparison baselines identified | [x] | §3: 4 baselines |
| 3 | ≥2 reviewer kill shots with mitigations | [x] | §4: 4 kill shots |
| 4 | Ablation plan with hypothesized effects | [x] | §5: 5 components |
| 5 | Ground truth audit: sources, lag, positive rate | [x] | §6: 3 sources |
| 6 | Alternative label sources considered | [x] | §6: GPT-4, Llama, FP-02 |
| 7 | Statistical plan: seeds, tests, CIs | [x] | §7: 5 seeds, Fisher's exact, Wilson CI |
| 8 | Related work: ≥5 papers | [x] | §8: 7 papers |
| 9 | Hypotheses pre-registered | [ ] | To create |
| 10 | lock_commit set | [ ] | To set |
| 11 | Target venue identified | [x] | AISec Workshop |
| 12 | This document committed before any training script | [x] | This commit |

**Gate 0.5 verdict:** [x] PASS (pending items 9-10)

---

## 10) Tier 2 Depth Escalation (R34)

### Depth Commitment

**Primary finding (one sentence):** Real LLM agents resist cascade poisoning through three mechanisms — semantic incongruity detection, domain knowledge conflict, and output self-correction — and attack success correlates with payload specificity and injection position, not sophistication.

**Evaluation settings (minimum 2):**

| # | Setting | How It Differs | What It Tests |
|---|---------|---------------|---------------|
| 1 | 5-agent hierarchical, CryptoScamCoin payload | Baseline from FP-15/16 | Core resistance patterns |
| 2 | 5-agent hierarchical, domain-specific payloads (3 types) | Payload varies | Whether resistance depends on payload type |
| 3 | 5-agent flat topology | Topology varies | Whether hierarchical protection interacts with resistance |

### Mechanism Analysis Plan

| Finding | Proposed Mechanism | Experiment to Verify |
|---------|-------------------|---------------------|
| ~40% of delegations resist poison | Agent detects semantic incongruity between task context and injected content | E2: vary payload relevance (off-topic → on-topic injection). If on-topic passes more, incongruity detection is the mechanism. |
| Deeper agents resist more | Poison signal dilutes through delegation chain | E4: measure poison rate at hop 1, 2, 3. If monotonically decreasing, dilution is the mechanism. |
| Some agents resist, others don't (same payload) | Agent role determines resistance via different knowledge bases | E5: same payload to analyst vs writer vs reviewer. If resistance varies by role, knowledge-based resistance is confirmed. |

### Adaptive Adversary Plan

| Robustness Claim | Weak Test | Adaptive Test |
|-----------------|-----------|---------------|
| Agents resist off-topic injection | Generic CryptoScamCoin payload | Domain-aligned payload ("recommend diversifying into crypto for risk management") |
| Agents resist via self-correction | Single injection | Repeated reinforcement across multiple delegation hops |

### Defense Harm Test

- [ ] Verify our resistance taxonomy doesn't inadvertently help attackers more than defenders
- [ ] This project is descriptive/analytical, not a defense proposal — harm test is: "does publishing resistance patterns enable trivially better attacks?" Address in ethics section.

### Qualitative Prediction Validation

| Prediction | Quantitative | Qualitative |
|-----------|-------------|-------------|
| Resistance rate ~40% | Exact rate may vary by payload | Pattern: some resist, some don't (not all-or-nothing) |
| Depth reduces poison | Rate at hop 3 < hop 1 by ≥10pp | Monotonic decrease (not random) |
| Role affects resistance | ≥15pp spread across roles | Different roles resist different payloads |

### Simulation Calibration Note

> FP-15/FP-16 showed 37-48pp simulation overestimate. This project does NOT use simulation — all experiments are on real agents. However, we compare against simulation predictions to quantify the gap we're explaining.

### Published Baseline Reproduction Plan

| Published Method | Their Benchmark | Our Reproduction |
|-----------------|----------------|------------------|
| FP-15 implicit cascade (real agents) | 5-agent hierarchical, 0.600 poison | Reproduce as E1 control. If we get ~0.60, our testbed is consistent. |
| FP-16 no-defense baseline | 3-agent hierarchical, 0.494 poison | Reproduce at 5 agents. Calibrate against known result. |

### Parameter Sensitivity Plan (G-5)

| Parameter | Sweep Values | Expected: Finding Robust? |
|-----------|-------------|--------------------------|
| Payload type | CryptoScamCoin, data exfiltration, privilege escalation, benign control | Yes — resistance patterns should differ by type but taxonomy should hold |
| Attack sophistication | naive, contextual, adversarially-crafted | Yes — resistance should decrease with sophistication |
| Number of tasks | 3, 5, 10 | Yes — patterns should be consistent |

### Depth Escalation Checklist

| # | Requirement | Status |
|---|------------|--------|
| 1 | ONE primary finding identified | [x] | Three resistance mechanisms |
| 2 | ≥2 evaluation settings designed | [x] | 3 settings |
| 3 | Mechanism analysis planned (including nulls) | [x] | 3 mechanisms + null predictions |
| 4 | Adaptive adversary test planned | [x] | Domain-aligned + repeated reinforcement |
| 5 | Formal contribution statement drafted | [x] | Below |
| 6 | ≥1 published baseline reproduction planned | [x] | FP-15 + FP-16 reproduced |
| 7 | Parameter sensitivity sweep planned | [x] | 3 parameters |
| 8 | Simulation-to-real validation planned | [x] | N/A — all experiments are real agents |
| 9 | Qualitative predictions validated | [x] | 3 qual predictions |
| 10 | Defense harm test planned | [x] | Ethics consideration |

### Formal Contribution Statement (draft)

We contribute:
1. **The first mechanistic taxonomy of LLM agent cascade resistance:** three patterns (semantic incongruity detection, domain knowledge conflict, output self-correction) with empirical validation on real Claude Haiku agents.
2. **Attack characteristic analysis:** payload specificity and injection position predict resistance better than attack sophistication, overturning the assumption that more sophisticated attacks are more effective against real agents.
3. **Quantitative explanation of the simulation-to-real gap:** the 37pp overestimate in FP-15 is attributable to the simulation's lack of semantic resistance modeling, with specific correction factors for each resistance pattern.

---

## 11) Phase 1 Exit Checkpoint

| # | Check | Status | Deviation? |
|---|-------|--------|------------|
| 1 | All 4 comparison baselines run | [ ] | |
| 2 | 5 seeds per experiment | [ ] | |
| 3 | All 5 ablation components tested | [ ] | |
| 4 | FP-15 baseline reproduced (within 15pp) | [ ] | |
| 5 | Deviations logged in DECISION_LOG | [ ] | |
| 6 | All experiment outputs exist | [ ] | |

---

## 12) Experiment Matrix

| ID | Question | IV | Levels | DV | Seeds |
|----|----------|-----|--------|-----|-------|
| E1 | Baseline: reproduce FP-15 real-agent cascade | — | 5-agent hierarchical, implicit trust | Poison rate, resistance rate | 5 |
| E2 | Does payload type affect resistance? | Payload | CryptoScamCoin, data exfil, priv escalation, benign | Per-payload resistance rate | 5 |
| E3 | Does attack sophistication overcome resistance? | Sophistication | naive, contextual, adversarial | Resistance rate by sophistication | 5 |
| E4 | Does delegation depth affect resistance? | Hop count | hop 1, 2, 3 | Per-hop poison rate | 5 |
| E5 | Does agent role affect resistance? | Role | orchestrator, analyst, writer, reviewer | Per-role resistance rate | 5 |
| E6 | Does topology interact with resistance? | Topology | hierarchical, flat | Resistance rate by topology | 5 |

**Total: ~1500 API calls, ~$10-15 Haiku**

---

## 13) Phase Plan

| Phase | Activities | Gate | Cost |
|-------|-----------|------|------|
| 0 | HYPOTHESIS_REGISTRY, contracts, lock_commit | Gate 0.5 | $0 |
| 1 | Build testbed, run E1-E3 | Phase 1 checkpoint | ~$6 |
| 2 | Run E4-E6, sensitivity sweep | — | ~$6 |
| 3 | FINDINGS, figures, statistical tests | Gate 8.5 | $0 |
| 4 | Blog, conference abstract, content pipeline | Gate 9 | $0 |
