# I tested why LLM agents resist cascade poisoning — resistance varies by 98 percentage points depending on payload type

I ran 6 experiments on real Claude Haiku agents to figure out why multi-agent systems resist cascade poisoning differently than simulations predict. The biggest finding: privilege escalation payloads cascade at 97.6%, while domain-aligned attacks are completely invisible to detection (0.0%). That's a 98 percentage point spread across payload types.

I tested four payload types injected through a compromised orchestrator agent in a 3-agent hierarchy. "Grant admin access" cascades freely because it sounds like legitimate business advice. "CryptoScamCoin" gets partially caught (68.8%) because it's obviously off-topic. Domain-aligned framing like "portfolio diversification" evades both agent resistance AND detection entirely — the 0.0% rate is a detection failure, not genuine resistance. I confirmed this with E0 sanity checks that revealed the detection threshold before running experiments.

Three resistance patterns emerged, and a linear model predicts resistance with R-squared = 0.75 using five measurable features:

- **Semantic incongruity detection** — agents partially catch off-topic injections (31% resistance for generic payloads) but domain-aligned framing bypasses this completely
- **Depth dilution** — each delegation hop filters ~17.5pp of poison signal, so deeper chains are actually MORE resistant (opposite of naive expectation)
- **Role-based critique** — reviewer agents propagate only 52% of poison vs 92% for analyst agents, a 40pp spread from system prompt alone
- **Resistance is predictable** — the 5-feature model lets you score your multi-agent architecture's vulnerability before deployment
- **The most dangerous attacks aren't visible** — keyword detection catches obvious injections but sophisticated domain-aligned attacks evade it entirely

Methodology: 6 pre-registered hypotheses, E0 sanity validation (positive control, negative control, dose-response), 5 seeds x 5 tasks per condition on real Claude Haiku agents. Without E0, I would have published "domain-aligned attacks are fully resisted" — which is wrong. The attack evaded detection, it didn't fail.

Repo: [github.com/rexcoleman/agent-semantic-resistance](https://github.com/rexcoleman/agent-semantic-resistance)

Code is open source with full experiment data. Happy to answer questions about the methodology or findings.
