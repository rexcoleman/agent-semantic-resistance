---
title: "Privilege Escalation Cascades at 98% While Domain-Aligned Attacks Are Invisible"
date: 2026-03-19
format: technical
tags: ["ai-security", "multi-agent", "cascade-resistance", "research"]
audience_side: "Both"
image_count: 0
description: "First taxonomy of why real LLM agents resist cascade poisoning — and which attacks bypass each resistance pattern."
---

# Privilege Escalation Cascades at 98% While Domain-Aligned Attacks Are Invisible

FP-15 showed real agents resist cascade at 60% where simulations predict 97%. FP-16 showed defenses fail because they don't understand this resistance. This project answers the question both left open: **WHY do real agents resist, and what bypasses it?**

Six experiments on real Claude Haiku agents. Six pre-registered hypotheses. Three resistance patterns identified.

## The 98pp Spread

The most important finding: resistance varies by **98 percentage points** across payload types.

| Payload | Poison Rate | Resistance |
|---------|------------|------------|
| Privilege escalation ("grant admin access") | **97.6%** | Almost none |
| Generic (CryptoScamCoin) | **68.8%** | Moderate |
| Data exfiltration (marker string) | **55.2%** | Moderate |
| Domain-aligned (portfolio diversification) | **0.0%** | Invisible to detection |

"Grant admin access" sounds like legitimate business advice. Agents propagate it freely. CryptoScamCoin is obviously off-topic — agents partially catch it. Domain-aligned framing is so well-crafted that neither agents NOR our detection can see it.

**The most dangerous attacks aren't the ones that cascade visibly. They're the ones you can't detect.**

## Three Resistance Patterns

### 1. Semantic Incongruity Detection

Agents partially detect when injected content doesn't match the task. Generic CryptoScamCoin in a business analysis triggers this — 31% resistance. Domain-aligned framing ("portfolio diversification") doesn't trigger it at all.

### 2. Depth Dilution

Each delegation hop filters the poison signal. Hop 1 (direct from attacker): 74% poisoned. Hop 2 (grandchildren): 48% poisoned. Every hop is a natural defense — the agent's own processing buries the injection in rewriting and summarization.

**Practical implication:** Deeper delegation chains are more resistant. This is the opposite of what you'd expect if agents were just passing messages through.

### 3. Role-Based Critique

Analyst agents propagate 92% of poison — their job is to "include everything." Reviewer agents propagate only 52% — their job is to "critique and evaluate." A 40pp spread from system prompt alone.

**Practical implication:** Put reviewer agents BETWEEN delegations, not just at the end.

## What This Means

1. **Multi-agent defenses should target privilege escalation payloads** — they cascade at 98% and are domain-plausible.
2. **Delegation depth is a defense** — design for deeper chains, not flatter ones.
3. **System prompt design matters** — reviewer framing reduces propagation by 40pp.
4. **Keyword detection is insufficient** — sophisticated attacks evade detection entirely. Need semantic similarity scoring.

## Limitations

Keyword detection conflates evasion with resistance. Claude Haiku only. 5 seeds. Single compromised agent. Static payloads. See FINDINGS.md for full discussion.

---

If you're building multi-agent systems, check out the full [resistance taxonomy](https://github.com/rexcoleman/agent-semantic-resistance). For more AI security research, follow on [LinkedIn](https://linkedin.com/in/rexcoleman).

---

*Rex Coleman is securing AI from the architecture up. MS Computer Science (Machine Learning) at Georgia Tech. Previously data analytics and enterprise sales at FireEye/Mandiant. CFA charterholder. Creator of [govML](https://github.com/rexcoleman/govML).*
