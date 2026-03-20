# For: OpenClaw Discord

domain-aligned payloads are invisible to detection in multi-agent setups. if your OpenClaw agents pass context between each other, this is the attack class that should worry you most.

```
privilege escalation ("grant admin")  → 97.6% poison rate
generic (CryptoScamCoin)              → 68.8%
data exfiltration                     → 55.2%
domain-aligned (portfolio advice)     →  0.0% ← undetectable

reviewer agents: 52% propagation
analyst agents:  92% propagation
(40pp gap from system prompt alone)
```

the 0.0% detection rate on domain-aligned payloads is the finding. if an attacker crafts a payload that looks like legitimate output for your agent's domain — financial advice for a finance agent, code review for a dev agent — no detection layer catches it. not SOUL.md rules, not tool policies, not an LLM-as-judge.

the 40pp gap between reviewer and analyst agents is basically free defense. if you put a reviewer-role agent between delegation hops in your OpenClaw config, propagation drops by nearly half. that's just a system prompt change — "you are a security reviewer, validate this before passing it on."

for multi-agent OpenClaw setups: every handoff between agents is an injection point. the heartbeat cycle processes whatever context it receives. if agent A passes "poisoned but domain-appropriate" context to agent B, agent B has no signal that it's compromised.

is anyone running reviewer agents between skill outputs and agent consumption? what does your inter-agent validation look like?
