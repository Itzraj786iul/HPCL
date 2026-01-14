import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/evaluate-formulation"

st.set_page_config(
    page_title="HPCL Sustainable Formulation Engine",
    layout="wide"
)

st.title("Next-Gen Sustainable Lubricant Formulation Engine")

st.markdown("""
This interface demonstrates an **explainable, regulation-aware formulation engine**
designed for **HPCL-scale decision making**.
""")

st.sidebar.header("Formulation Inputs")

# --- Regulatory inputs ---
phosphorus = st.sidebar.slider("Phosphorus (%)", 0.0, 0.1, 0.05, step=0.005)
sulfur = st.sidebar.slider("Sulfur (%)", 0.0, 0.5, 0.18, step=0.01)
ash = st.sidebar.slider("Sulphated Ash (%)", 0.0, 2.0, 0.6, step=0.05)

# --- Sustainability inputs ---
avg_toxicity = st.sidebar.slider("Average Toxicity (0–1)", 0.0, 1.0, 0.32, step=0.01)
carbon_index = st.sidebar.slider("Carbon Index (0–1)", 0.0, 1.0, 0.45, step=0.01)
biodegradability = st.sidebar.slider("Biodegradability (0–1)", 0.0, 1.0, 0.7, step=0.05)

# --- Cost inputs ---
baseline_cost = st.sidebar.number_input("Baseline Cost", value=100.0)
formulation_cost = st.sidebar.number_input("Formulation Cost", value=104.0)

payload = {
    "formulation_metrics": {
        "phosphorus_pct": phosphorus,
        "sulfur_pct": sulfur,
        "ash_contribution": ash
    },
    "sustainability_metrics": {
        "avg_toxicity": avg_toxicity,
        "carbon_index": carbon_index,
        "biodegradability": biodegradability
    },
    "baseline_cost": baseline_cost,
    "formulation_cost": formulation_cost
}

if st.button("Evaluate Formulation"):
    with st.spinner("Evaluating formulation..."):
        response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()

        st.subheader("Regulatory Headroom")
        st.json(result["regulatory_headroom"])

        st.subheader("Sustainability Score")
        st.json(result["sustainability"])

        st.subheader("Cost Elasticity Assessment")
        st.json(result["cost_assessment"])

        st.subheader("Future Regulation Scenario")
        st.json(result["scenario_simulation"])

        st.subheader("Decision Trace (Explainability)")
        st.json(result["decision_trace"])
    else:
        st.error("API error. Is FastAPI running?")
