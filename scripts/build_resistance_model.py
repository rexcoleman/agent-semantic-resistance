#!/usr/bin/env python3
"""Build a predictive model of agent cascade resistance.

Uses FP-17 experiment results to train a model that predicts resistance
rate from payload characteristics. Tests whether resistance is predictable
from measurable input features.

This is the 8→9 upgrade: moving from taxonomy (description) to prediction.

Usage:
    python scripts/build_resistance_model.py
"""
import json
import sys
from pathlib import Path

import numpy as np

OUTPUT_DIR = Path("outputs/experiments")
MODEL_DIR = Path("outputs/models")


def load_all_results():
    """Load all experiment results and build feature matrix."""
    features = []
    labels = []

    # E2: Payload type → resistance
    with open(OUTPUT_DIR / "e2_results.json") as f:
        e2 = json.load(f)

    payload_features = {
        "generic": {"semantic_distance": 0.8, "domain_plausibility": 0.2, "keyword_detectability": 0.9},
        "domain_aligned": {"semantic_distance": 0.2, "domain_plausibility": 0.9, "keyword_detectability": 0.1},
        "data_exfil": {"semantic_distance": 0.6, "domain_plausibility": 0.1, "keyword_detectability": 0.7},
        "priv_escalation": {"semantic_distance": 0.3, "domain_plausibility": 0.8, "keyword_detectability": 0.8},
    }

    for payload_type, feat in payload_features.items():
        if payload_type in e2["results"]:
            for seed_data in e2["results"][payload_type]["seeds"]:
                features.append([
                    feat["semantic_distance"],
                    feat["domain_plausibility"],
                    feat["keyword_detectability"],
                    0,    # hop (aggregate)
                    0.5,  # role_critique_level (aggregate)
                ])
                labels.append(seed_data["poison_rate"])

    # E4: Depth → resistance (from per-hop data)
    with open(OUTPUT_DIR / "e4_results.json") as f:
        e4 = json.load(f)
    for seed_data in e4["results"]["depth_tracking"]["seeds"]:
        for hop_str, counts in seed_data.get("per_hop", {}).items():
            hop = int(hop_str)
            rate = counts["poisoned"] / max(counts["total"], 1)
            features.append([
                0.8,  # semantic_distance (generic payload)
                0.2,  # domain_plausibility
                0.9,  # keyword_detectability
                hop,
                0.5,  # role_critique_level (aggregate)
            ])
            labels.append(rate)

    # E5: Role → resistance (from per-role data)
    role_critique = {
        "orchestrator": 0.1,  # Compromised, not relevant
        "analyst": 0.2,       # "Analyze everything" = low critique
        "writer": 0.5,        # Reframing = moderate
        "reviewer": 0.8,      # Critique = high
        "publisher": 0.7,     # Quality check = moderate-high
    }
    with open(OUTPUT_DIR / "e5_results.json") as f:
        e5 = json.load(f)
    for seed_data in e5["results"]["role_tracking"]["seeds"]:
        for role, counts in seed_data.get("per_role", {}).items():
            rate = counts["poisoned"] / max(counts["total"], 1)
            features.append([
                0.8,
                0.2,
                0.9,
                1,  # average hop
                role_critique.get(role, 0.5),
            ])
            labels.append(rate)

    return np.array(features), np.array(labels)


def fit_linear_model(X, y):
    """Fit a simple linear model: y = Xw + b."""
    # Add bias term
    X_bias = np.column_stack([X, np.ones(len(X))])
    # Least squares
    w, residuals, rank, sv = np.linalg.lstsq(X_bias, y, rcond=None)
    y_pred = X_bias @ w
    # Metrics
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / max(ss_tot, 1e-10)
    rmse = np.sqrt(np.mean((y - y_pred) ** 2))
    return w, r2, rmse, y_pred


def leave_one_out_cv(X, y):
    """Leave-one-out cross-validation."""
    errors = []
    for i in range(len(X)):
        X_train = np.delete(X, i, axis=0)
        y_train = np.delete(y, i)
        X_test = X[i:i+1]
        y_test = y[i]

        X_bias = np.column_stack([X_train, np.ones(len(X_train))])
        w, _, _, _ = np.linalg.lstsq(X_bias, y_train, rcond=None)
        y_pred = np.column_stack([X_test, np.ones(1)]) @ w
        errors.append((y_test - y_pred[0]) ** 2)

    return np.sqrt(np.mean(errors))


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("FP-17 Resistance Prediction Model")
    print("=" * 60)

    X, y = load_all_results()
    feature_names = ["semantic_distance", "domain_plausibility",
                     "keyword_detectability", "hop_depth", "role_critique_level"]

    print(f"\nDataset: {len(X)} observations, {X.shape[1]} features")
    print(f"Target: poison_rate (mean={y.mean():.3f}, std={y.std():.3f})")

    # Fit model
    w, r2, rmse, y_pred = fit_linear_model(X, y)

    print(f"\n--- Linear Model ---")
    print(f"R² = {r2:.4f}")
    print(f"RMSE = {rmse:.4f}")
    print(f"\nFeature weights:")
    for name, weight in zip(feature_names, w[:-1]):
        direction = "↑ poison" if weight > 0 else "↓ poison (protective)"
        print(f"  {name:<25} {weight:+.4f}  {direction}")
    print(f"  {'bias':<25} {w[-1]:+.4f}")

    # Cross-validation
    cv_rmse = leave_one_out_cv(X, y)
    print(f"\nLeave-one-out CV RMSE = {cv_rmse:.4f}")

    # Predictions for key scenarios
    print(f"\n--- Scenario Predictions ---")
    scenarios = {
        "Worst case (priv_escalation, analyst, hop0)":
            [0.3, 0.8, 0.8, 0, 0.2],
        "Best case (generic, reviewer, hop2)":
            [0.8, 0.2, 0.9, 2, 0.8],
        "Stealth attack (domain_aligned, analyst, hop0)":
            [0.2, 0.9, 0.1, 0, 0.2],
        "Protected chain (generic, reviewer, hop2)":
            [0.8, 0.2, 0.9, 2, 0.8],
    }
    X_bias_model = np.column_stack([np.ones(1)])  # dummy
    for name, feat in scenarios.items():
        pred = np.array(feat + [1.0]) @ w
        pred = np.clip(pred, 0, 1)
        print(f"  {name}: predicted poison = {pred:.3f}")

    # Save model
    model_data = {
        "feature_names": feature_names,
        "weights": w.tolist(),
        "r2": float(r2),
        "rmse": float(rmse),
        "cv_rmse": float(cv_rmse),
        "n_observations": len(X),
        "predictions": {k: float(np.clip(np.array(v + [1.0]) @ w, 0, 1))
                       for k, v in scenarios.items()},
    }
    out_file = MODEL_DIR / "resistance_model.json"
    with open(out_file, "w") as f:
        json.dump(model_data, f, indent=2)
    print(f"\nSaved: {out_file}")

    # Assessment
    print(f"\n--- Model Assessment ---")
    if r2 > 0.6:
        print(f"R² = {r2:.3f} — resistance IS predictable from these features.")
        print("This supports formalizing the taxonomy into a predictive model.")
    elif r2 > 0.3:
        print(f"R² = {r2:.3f} — partial predictability. Features explain some variance but not all.")
        print("Additional features needed (e.g., task complexity, agent temperature).")
    else:
        print(f"R² = {r2:.3f} — resistance is NOT well-predicted by these features.")
        print("The taxonomy is descriptive, not predictive. Honest negative result.")


if __name__ == "__main__":
    main()
