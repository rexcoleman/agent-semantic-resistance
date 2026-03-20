# Conference Abstract — AISec Workshop (ACM CCS 2026)

> **Title:** Privilege Escalation Cascades at 98% While Domain-Aligned Attacks Are Invisible: A Taxonomy of Agent Semantic Resistance
> **Speaker:** Rex Coleman

## Abstract

Real LLM agents resist cascade poisoning at 60%, not the 97% simulations predict. We present the first mechanistic taxonomy of this resistance through 6 experiments on real Claude Haiku agents with 5-seed validation.

Key findings: (1) Resistance varies by 98pp across payload types — privilege escalation cascades at 97.6% while domain-aligned attacks produce 0% detectable poison. (2) Delegation depth dilutes poison at 26pp per hop, making deeper chains naturally more resistant. (3) Agent role determines resistance: analysts propagate 92% of poison while reviewers propagate only 52% (40pp spread from system prompt alone). (4) Sophisticated attacks evade keyword detection rather than overcoming resistance, revealing a fundamental methodological challenge: binary poison detection conflates evasion with resistance.

These findings explain the 37pp simulation-to-real gap documented in our cascade simulation and why semantic verification defenses fail as shown in our delegation protocol. We propose three resistance patterns (semantic incongruity, depth dilution, role-based critique) with quantified bypass conditions for each.

## Bio (100 words)

Rex Coleman is building at the intersection of AI security and ML systems engineering. He spent over a decade at FireEye and Mandiant in data analytics and enterprise sales, working with security teams across Fortune 500 organizations. He is completing his MS in Computer Science at Georgia Tech (Machine Learning specialization), where he researches AI security — adversarial evaluation of ML systems, agent exploitation, and ML governance tooling. He is the creator of govML, an open-source governance framework for ML research projects. CFA charterholder.
