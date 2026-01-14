from engine.data_loader import load_additives, load_environmental_factors
from engine.compliance_filters import apply_all_filters
from engine.scoring_engine import score_additives
import pandas as pd

# Load data
additives = load_additives()
env = load_environmental_factors()

# Regulations (ACEA C6)
regulations = pd.read_csv("data/regulations.csv")
acea_c6 = regulations[regulations["spec"] == "ACEA_C6"].iloc[0]

toxicity_threshold = env[env["parameter"] == "toxicity_threshold"]["value"].values[0]

# Filter additives
filtered_additives = apply_all_filters(additives, acea_c6, toxicity_threshold)

# Define weights (can be tuned live later)
weights = {
    "toxicity": 0.35,
    "cost": 0.25,
    "co2": 0.25,
    "biodegradability": 0.15
}

# Score additives
scored_additives = score_additives(filtered_additives, weights)

print("\nTop Recommended Sustainable Additives:\n")
print(scored_additives[[
    "additive_id",
    "additive_class",
    "final_score",
    "toxicity_score",
    "cost_index",
    "co2_kg_per_kg",
    "biodegradability_score"
]].head(5))
