# engine/regulatory_headroom.py

class RegulatoryHeadroom:
    API_SP_LIMITS = {
        "phosphorus_pct": 0.08,
        "sulfur_pct": 0.30,
        "ash_contribution": 1.0
    }

    def calculate(self, formulation_metrics):
        headroom = {}

        for param, limit in self.API_SP_LIMITS.items():
            actual = formulation_metrics.get(param, 0)

            if actual > limit:
                headroom[param] = 0.0
            else:
                headroom[param] = round(((limit - actual) / limit) * 100, 2)

        headroom["overall_headroom"] = round(
            sum(headroom.values()) / len(self.API_SP_LIMITS), 2
        )

        return headroom
