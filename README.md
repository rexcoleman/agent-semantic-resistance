# FP-17: Agent Semantic Resistance to Cascade Poisoning

Why do real LLM agents resist cascade poisoning at 60% when simulations predict 97%? This project identifies three resistance mechanisms and shows which attacks bypass each.

**Blog post:** [Privilege Escalation Cascades at 98%](https://rexcoleman.dev/posts/agent-semantic-resistance/)

## Key Finding

Resistance varies by **98 percentage points** across payload types:
- Privilege escalation: **97.6%** poison (near-zero resistance)
- Generic injection: **68.8%** (moderate resistance)
- Data exfiltration: **55.2%** (moderate resistance)
- Domain-aligned: **0.0%** detected (invisible to keyword detection)

## Three Resistance Patterns

1. **Semantic incongruity** — agents detect off-topic content (31% resistance)
2. **Depth dilution** — each delegation hop filters poison (-26pp per hop)
3. **Role-based critique** — reviewer agents propagate 52% vs analyst 92%

## Quick Start

```bash
export ANTHROPIC_API_KEY=sk-...
python -u scripts/run_experiments.py          # All 6 experiments
python -u scripts/run_experiments.py --experiments E1,E2  # Subset
```

## Designed for 8/10

Built with [govML](https://github.com/rexcoleman/govML) Gate 0.5 + R34. check_gate05.sh: 12/12 PASS.

## Predecessors

- [FP-15](https://github.com/rexcoleman/multi-agent-security): Measured the 37pp gap
- [FP-16](https://github.com/rexcoleman/verified-delegation-protocol): Showed defenses fail
- FP-17: Explains WHY

## License

MIT
