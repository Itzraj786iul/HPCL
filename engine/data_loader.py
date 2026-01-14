import pandas as pd

def load_base_oils(path="data/base_oils.csv"):
    return pd.read_csv(path)

def load_additives(path="data/additives.csv"):
    return pd.read_csv(path)

def load_regulations(path="data/regulations.csv"):
    return pd.read_csv(path)

def load_environmental_factors(path="data/environmental_factors.csv"):
    return pd.read_csv(path)
