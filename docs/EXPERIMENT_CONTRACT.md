# EXPERIMENT CONTRACT — FP-17 Agent Semantic Resistance

## 0) Gate 0.5 Cross-Reference

**EXPERIMENTAL_DESIGN.md status:** PASS (lock_commit: `f05df16`)

### Comparison Baselines

| # | Method | Implementation |
|---|--------|---------------|
| 1 | FP-15 simulation cascade model | Compare our real-agent results to FP-15 predictions |
| 2 | FP-16 defense experiment outputs | Compare our resistance patterns to FP-16 baseline |
| 3 | Cohen et al. "AI Worm" propagation | Compare to their blind-propagation assumption |
| 4 | No-resistance mock baseline | FP-15 simulation (~97%) as control |

### Ablation Plan

| Component | Hypothesis | Status |
|-----------|-----------|--------|
| Payload specificity | Domain-aligned > generic | E2 |
| Delegation depth | Deeper = less poison | E4 |
| Task complexity | Complex = more resistance | Implicit in E1 |
| Agent role | Reviewer resists most | E5 |
| Injection position | System prompt hardest to resist | Implicit in design |

## 1) Experiment Matrix

| ID | IV | Levels | DV | Seeds |
|----|-----|--------|-----|-------|
| E1 | — (baseline) | 5-agent hierarchical, generic payload | Poison rate + per-hop + per-role | 5 |
| E2 | Payload type | generic, domain_aligned, data_exfil, priv_escalation | Poison rate | 5 |
| E3 | Sophistication | naive, contextual, adversarial | Poison rate | 5 |
| E4 | Hop depth | hop 0, 1, 2 (from E1 data) | Per-hop poison rate | 5 |
| E5 | Role | orchestrator, analyst, writer, reviewer, publisher | Per-role poison rate | 5 |
| E6 | Topology | hierarchical, flat | Poison rate | 5 |
