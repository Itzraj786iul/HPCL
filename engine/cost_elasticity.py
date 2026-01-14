# engine/cost_elasticity.py

class CostElasticityEngine:
    def __init__(self, max_cost_increase_pct=5):
        self.max_cost_increase_pct = max_cost_increase_pct

    def evaluate(self, baseline_cost, formulation_cost, sustainability_score):
        """
        Returns cost impact assessment
        """

        cost_delta_pct = ((formulation_cost - baseline_cost) / baseline_cost) * 100

        result = {
            "cost_delta_pct": round(cost_delta_pct, 2),
            "status": "ACCEPTABLE",
            "penalty": 0
        }

        if cost_delta_pct > self.max_cost_increase_pct:
            result["status"] = "PENALIZED"
            result["penalty"] = round(cost_delta_pct - self.max_cost_increase_pct, 2)

        elif cost_delta_pct <= 0 and sustainability_score >= 60:
            result["status"] = "BONUS"
            result["bonus_reason"] = "Cost-neutral sustainability improvement"

        return result
