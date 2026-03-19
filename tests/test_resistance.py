"""Tests for FP-17 experiment infrastructure."""
import json
from pathlib import Path

RESULTS_DIR = Path("outputs/experiments")


def test_results_exist():
    assert RESULTS_DIR.exists(), "outputs/experiments/ must exist"


def test_all_experiments_summary():
    summary = RESULTS_DIR / "all_experiments_summary.json"
    assert summary.exists(), "all_experiments_summary.json must exist"
    with open(summary) as f:
        data = json.load(f)
    assert "results" in data


def test_e1_baseline():
    with open(RESULTS_DIR / "e1_results.json") as f:
        e1 = json.load(f)
    baseline = e1["results"]["baseline"]
    mean = baseline["poison_rate_mean"]
    assert 0.3 < mean < 0.9, f"E1 baseline {mean} outside expected range"


def test_e2_payload_types():
    with open(RESULTS_DIR / "e2_results.json") as f:
        e2 = json.load(f)
    results = e2["results"]
    assert "generic" in results
    assert "domain_aligned" in results
    assert "priv_escalation" in results
    # Priv escalation should be highest
    assert results["priv_escalation"]["poison_rate_mean"] > results["generic"]["poison_rate_mean"]


def test_e4_depth_dilution():
    with open(RESULTS_DIR / "e4_results.json") as f:
        e4 = json.load(f)
    # Aggregate per-hop data
    hop_totals = {}
    for seed_data in e4["results"]["depth_tracking"]["seeds"]:
        for hop, counts in seed_data.get("per_hop", {}).items():
            if hop not in hop_totals:
                hop_totals[hop] = {"t": 0, "p": 0}
            hop_totals[hop]["t"] += counts["total"]
            hop_totals[hop]["p"] += counts["poisoned"]
    # Hop 2 should have lower poison rate than hop 1
    if "1" in hop_totals and "2" in hop_totals:
        rate1 = hop_totals["1"]["p"] / hop_totals["1"]["t"]
        rate2 = hop_totals["2"]["p"] / hop_totals["2"]["t"]
        assert rate2 < rate1, f"Depth dilution failed: hop1={rate1:.2f}, hop2={rate2:.2f}"


def test_e5_role_variance():
    with open(RESULTS_DIR / "e5_results.json") as f:
        e5 = json.load(f)
    role_agg = {}
    for sd in e5["results"]["role_tracking"]["seeds"]:
        for role, c in sd.get("per_role", {}).items():
            if role not in role_agg:
                role_agg[role] = {"t": 0, "p": 0}
            role_agg[role]["t"] += c["total"]
            role_agg[role]["p"] += c["poisoned"]
    # At least 2 roles should exist
    assert len(role_agg) >= 2, f"Only {len(role_agg)} roles found"


def test_reproducibility_info():
    assert Path("EXPERIMENTAL_DESIGN.md").exists()
    assert Path("HYPOTHESIS_REGISTRY.md").exists()
    assert Path("reproduce.sh").exists()
