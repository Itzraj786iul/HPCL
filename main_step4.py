from engine.data_loader import load_base_oils, load_additives, load_regulations
from engine.compliance_filters import apply_all_filters
from engine.scoring_engine import score_additives
from engine.formulation_engine import generate_formulations, score_formulation
import pandas as pd

# Load data
base_oils = load_base_oils()
additives = load_additives()
regulations = load_regulations()

# Select ACEA C6
acea_c6 = regulations[regulations["spec"] == "ACEA_C6"].iloc[0]

# Toxicity threshold
toxicity_threshold = 0.7

# Filter & score additives
filtered_additives = apply_all_filters(additives, acea_c6, toxicity_threshold)

weights = {
    "toxicity": 0.35,
    "cost": 0.25,
    "co2": 0.25,
    "biodegradability": 0.15
}

scored_additives = score_additives(filtered_additives, weights)

# Generate formulations
formulations = generate_formulations(base_oils, scored_additives)

scored_formulations = []

for f in formulations:
    metrics = score_formulation(f, base_oils, additives)

    # Compliance check
    if (
        metrics["total_phosphorus"] <= acea_c6["max_phosphorus"] and
        metrics["total_sulfur"] <= acea_c6["max_sulfur"] and
        metrics["total_ash"] <= acea_c6["max_sulphated_ash"]
    ):
        scored_formulations.append({**f, **metrics})

# Rank by CO2 then cost
ranked = sorted(
    scored_formulations,
    key=lambda x: (x["total_co2"], x["total_cost_index"])
)

print("\nTop 3 Sustainable Lubricant Formulations:\n")
for i, f in enumerate(ranked[:3], 1):
    print(f"Formulation {i}:")
    print(f)
    print("-" * 50)
