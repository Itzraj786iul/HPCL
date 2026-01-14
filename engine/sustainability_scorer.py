# engine/sustainability_scorer.py

class SustainabilityScorer:
    WEIGHTS = {
        "toxicity": 0.4,
        "carbon": 0.35,
        "biodegradability": 0.25
    }

    def score(self, formulation_metrics):
        """
        formulation_metrics example:
        {
            "avg_toxicity": 0.32,      # 0 (best) → 1 (worst)
            "carbon_index": 0.45,      # lower is better
            "biodegradability": 0.7    # 0 → 1 (higher is better)
        }
        """

        toxicity_score = (1 - formulation_metrics["avg_toxicity"]) * 100
        carbon_score = (1 - formulation_metrics["carbon_index"]) * 100
        bio_score = formulation_metrics["biodegradability"] * 100

        total = (
            toxicity_score * self.WEIGHTS["toxicity"]
            + carbon_score * self.WEIGHTS["carbon"]
            + bio_score * self.WEIGHTS["biodegradability"]
        )

        return {
            "toxicity_score": round(toxicity_score, 2),
            "carbon_score": round(carbon_score, 2),
            "biodegradability_score": round(bio_score, 2),
            "total_sustainability_score": round(total, 2)
        }
