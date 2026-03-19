# LinkedIn Post — Agent Semantic Resistance

> Blog link as FIRST COMMENT.

---

I ran 6 experiments on real Claude agents to answer: why do LLM agents resist cascade poisoning at 60% when simulations predict 97%?

The answer: resistance varies by 98 percentage points depending on payload type.

Privilege escalation ("grant admin access to all team members") cascades at 98%. Agents treat it as legitimate business advice.

Generic injection (CryptoScamCoin) hits 69%. Agents partially detect off-topic content.

Domain-aligned framing? 0% detected. Not because agents resist better — because our detection can't see it. The most dangerous attacks are invisible.

Three resistance patterns:

1. Semantic incongruity — agents catch off-topic content (31% resistance)
2. Depth dilution — each delegation hop filters poison (26pp reduction per hop)
3. Role-based critique — reviewer agents resist at 52% vs analyst agents at 92%

The practical takeaways for multi-agent builders:
- Target privilege escalation, not financial injection
- Design deeper delegation chains (depth is a defense)
- Put reviewer agents BETWEEN delegations, not just at the end
- Keyword detection is insufficient — need semantic similarity

6 pre-registered hypotheses. 3 supported, 1 refuted, 1 complicated, 1 partial.

#AISecurity #MultiAgent #ResearchFindings #NegativeResults #BuildInPublic
