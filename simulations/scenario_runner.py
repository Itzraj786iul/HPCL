# simulations/scenario_runner.py

from engine.regulatory_headroom import RegulatoryHeadroom

class ScenarioRunner:
    def __init__(self):
        self.base_engine = RegulatoryHeadroom()

    def tighten_phosphorus_limit(self, formulation_metrics, reduction_pct):
        """
        Simulate tighter phosphorus regulation
        reduction_pct = 20 means 20% tighter limit
        """

        original_limit = self.base_engine.API_SP_LIMITS["phosphorus_pct"]
        tightened_limit = original_limit * (1 - reduction_pct / 100)

        actual_phosphorus = formulation_metrics["phosphorus_pct"]

        if actual_phosphorus > tightened_limit:
            status = "FAIL"
        else:
            status = "PASS"

        return {
            "original_limit": original_limit,
            "tightened_limit": round(tightened_limit, 4),
            "actual_phosphorus": actual_phosphorus,
            "status": status
        }
