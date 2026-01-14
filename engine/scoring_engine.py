def normalize(series):
    """
    Min-max normalization (0–1)
    """
    return (series - series.min()) / (series.max() - series.min())


def score_additives(additives_df, weights):
    """
    Score additives using weighted multi-objective framework
    """

    df = additives_df.copy()

    # Normalize relevant columns
    df["toxicity_norm"] = normalize(df["toxicity_score"])
    df["cost_norm"] = normalize(df["cost_index"])
    df["co2_norm"] = normalize(df["co2_kg_per_kg"])
    df["bio_norm"] = normalize(df["biodegradability_score"])

    # Higher score = better
    df["final_score"] = (
        weights["toxicity"] * (1 - df["toxicity_norm"]) +
        weights["cost"] * (1 - df["cost_norm"]) +
        weights["co2"] * (1 - df["co2_norm"]) +
        weights["biodegradability"] * df["bio_norm"]
    )

    return df.sort_values("final_score", ascending=False)
