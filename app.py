import streamlit as st
import pandas as pd

from engine.data_loader import load_base_oils, load_additives, load_regulations
from engine.compliance_filters import apply_all_filters
from engine.scoring_engine import score_additives
from engine.formulation_engine import generate_formulations, score_formulation

st.set_page_config(page_title="HPCL Sustainable Formulation Engine", layout="wide")

st.title("Next-Gen Sustainable Lubricant Formulation Engine")

st.markdown("""
This prototype screens **public datasets** to recommend  
**API SP / ACEA C6-compliant, low-toxicity, low-CO₂ lubricant formulations**.
""")

# Sidebar controls
st.sidebar.header("Scoring Weights")

w_toxicity = st.sidebar.slider("Toxicity Weight", 0.0, 1.0, 0.35)
w_cost = st.sidebar.slider("Cost Weight", 0.0, 1.0, 0.25)
w_co2 = st.sidebar.slider("CO₂ Weight", 0.0, 1.0, 0.25)
w_bio = st.sidebar.slider("Biodegradability Weight", 0.0, 1.0, 0.15)

weights = {
    "toxicity": w_toxicity,
    "cost": w_cost,
    "co2": w_co2,
    "biodegradability": w_bio
}

# Load data
base_oils = load_base_oils()
additives = load_additives()
regulations = load_regulations()

acea_c6 = regulations[regulations["spec"] == "ACEA_C6"].iloc[0]
toxicity_threshold = 0.7

filtered_additives = apply_all_filters(additives, acea_c6, toxicity_threshold)
scored_additives = score_additives(filtered_additives, weights)

st.subheader("Top Sustainable Additives")
st.dataframe(
    scored_additives[[
        "additive_id",
        "additive_class",
        "final_score",
        "toxicity_score",
        "cost_index",
        "co2_kg_per_kg"
    ]].head(5)
)

if st.button("Generate Top Formulations"):
    formulations = generate_formulations(base_oils, scored_additives)

    valid_forms = []
    for f in formulations:
        metrics = score_formulation(f, base_oils, additives)

        if (
            metrics["total_phosphorus"] <= acea_c6["max_phosphorus"] and
            metrics["total_sulfur"] <= acea_c6["max_sulfur"] and
            metrics["total_ash"] <= acea_c6["max_sulphated_ash"]
        ):
            valid_forms.append({**f, **metrics})

    ranked = sorted(
        valid_forms,
        key=lambda x: (x["total_co2"], x["total_cost_index"])
    )

    st.subheader("Top 3 Sustainable Formulations")
    st.json(ranked[:3])
