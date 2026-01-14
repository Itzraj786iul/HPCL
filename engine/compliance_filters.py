def filter_pfas(additives_df):
    """
    Remove 'forever chemicals'
    """
    return additives_df[additives_df["is_pfas"] == False]


def filter_toxicity(additives_df, toxicity_threshold):
    """
    Remove additives above toxicity threshold
    """
    return additives_df[additives_df["toxicity_score"] <= toxicity_threshold]


def filter_saps(additives_df, max_phosphorus, max_sulfur, max_ash):
    """
    Enforce SAPS limits (per additive contribution)
    """
    return additives_df[
        (additives_df["phosphorus_pct"] <= max_phosphorus) &
        (additives_df["sulfur_pct"] <= max_sulfur) &
        (additives_df["ash_contribution"] <= max_ash)
    ]


def apply_all_filters(additives_df, regulation_row, toxicity_threshold):
    """
    Apply all hard filters together
    """
    df = filter_pfas(additives_df)
    df = filter_toxicity(df, toxicity_threshold)
    df = filter_saps(
        df,
        regulation_row["max_phosphorus"],
        regulation_row["max_sulfur"],
        regulation_row["max_sulphated_ash"]
    )
    return df
