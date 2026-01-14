def generate_formulations(base_oils_df, additives_df, top_n_per_class=2):
    """
    Generate candidate formulations using top additives per class
    """

    # Select top additives per class
    selected_additives = {}
    for cls in additives_df["additive_class"].unique():
        selected_additives[cls] = (
            additives_df[additives_df["additive_class"] == cls]
            .sort_values("final_score", ascending=False)
            .head(top_n_per_class)
        )

    formulations = []

    for _, base_oil in base_oils_df.iterrows():
        for disp in selected_additives.get("Dispersant", []).itertuples():
            for det in selected_additives.get("Detergent", []).itertuples():
                for aw in selected_additives.get("Anti-wear", []).itertuples():
                    for fm in selected_additives.get("Friction Modifier", []).itertuples():
                        for ao in selected_additives.get("Antioxidant", []).itertuples():
                            for vm in selected_additives.get("Viscosity Modifier", []).itertuples():

                                formulation = {
                                    "base_oil": base_oil["base_oil_id"],
                                    "Dispersant": disp.additive_id,
                                    "Detergent": det.additive_id,
                                    "Anti-wear": aw.additive_id,
                                    "Friction Modifier": fm.additive_id,
                                    "Antioxidant": ao.additive_id,
                                    "Viscosity Modifier": vm.additive_id
                                }

                                formulations.append(formulation)

    return formulations


def score_formulation(formulation, base_oils_df, additives_df):
    """
    Compute formulation-level cost, CO2, SAPS
    """

    treat_rates = {
        "base_oil": 0.92,
        "Dispersant": 0.03,
        "Detergent": 0.02,
        "Anti-wear": 0.01,
        "Friction Modifier": 0.005,
        "Antioxidant": 0.005,
        "Viscosity Modifier": 0.01
    }

    total_cost = 0
    total_co2 = 0
    total_p = 0
    total_s = 0
    total_ash = 0

    # Base oil contribution
    base = base_oils_df[base_oils_df["base_oil_id"] == formulation["base_oil"]].iloc[0]
    total_cost += treat_rates["base_oil"] * base["cost_index"]
    total_co2 += treat_rates["base_oil"] * base["co2_kg_per_kg"]

    # Additives contribution
    for cls, rate in treat_rates.items():
        if cls == "base_oil":
            continue

        add = additives_df[additives_df["additive_id"] == formulation[cls]].iloc[0]

        total_cost += rate * add["cost_index"]
        total_co2 += rate * add["co2_kg_per_kg"]
        total_p += rate * add["phosphorus_pct"]
        total_s += rate * add["sulfur_pct"]
        total_ash += rate * add["ash_contribution"]

    return {
        "total_cost_index": round(total_cost, 3),
        "total_co2": round(total_co2, 3),
        "total_phosphorus": round(total_p, 4),
        "total_sulfur": round(total_s, 4),
        "total_ash": round(total_ash, 4)
    }
