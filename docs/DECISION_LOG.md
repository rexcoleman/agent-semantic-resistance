# DECISION LOG — FP-17 Agent Semantic Resistance

## ADR-0001: Real agents only — no simulation mode
- **Date:** 2026-03-19 | **Phase:** 0
- **Context:** FP-15 showed simulation overestimates by 37pp. FP-16 showed defenses that work in simulation fail on real agents. R34.7 requires real-agent validation for Tier 2+.
- **Decision:** FP-17 uses real Claude Haiku agents exclusively. No simulation mode. No mock mode. Every data point comes from actual LLM API calls.
- **Consequences:** Higher cost (~$10-15) but results are directly credible. No simulation-to-real gap to explain.

## ADR-0002: CryptoScamCoin as standard + 3 additional payloads
- **Date:** 2026-03-19 | **Phase:** 0
- **Context:** FP-15 and FP-16 both used CryptoScamCoin exclusively. FP-17's H-2 tests whether payload type affects resistance.
- **Decision:** Use 4 payload types: generic (CryptoScamCoin), domain-aligned (portfolio diversification), data exfiltration (marker string), privilege escalation (admin access).
- **Consequences:** 4x the conditions but answers whether resistance is payload-general or payload-specific.

## ADR-0003: Per-hop and per-role tracking from E1
- **Date:** 2026-03-19 | **Phase:** 0
- **Context:** FP-15 measured aggregate poison rate only. FP-17 needs per-hop (H-4) and per-role (H-5) granularity.
- **Decision:** Track poison rate at each delegation hop and for each agent role separately, starting from E1.
- **Consequences:** Richer data from same API calls. E4 and E5 reuse E1 data with different analysis views.
