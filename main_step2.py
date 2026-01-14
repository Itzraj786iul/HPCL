from engine.data_loader import (
    load_base_oils,
    load_additives,
    load_regulations,
    load_environmental_factors
)
from engine.compliance_filters import apply_all_filters

# Load data
base_oils = load_base_oils()
additives = load_additives()
regulations = load_regulations()
env = load_environmental_factors()

# Select ACEA C6 (most restrictive)
acea_c6 = regulations[regulations["spec"] == "ACEA_C6"].iloc[0]

# Toxicity threshold
toxicity_threshold = env[env["parameter"] == "toxicity_threshold"]["value"].values[0]

# Apply filters
filtered_additives = apply_all_filters(
    additives,
    acea_c6,
    toxicity_threshold
)

print("Initial additives count:", len(additives))
print("Filtered additives count:", len(filtered_additives))
print("\nRemaining additives:\n")
print(filtered_additives[[
    "additive_id",
    "additive_class",
    "toxicity_score",
    "phosphorus_pct",
    "sulfur_pct",
    "ash_contribution"
]])
from explainability.decision_trace import DecisionTrace

trace = DecisionTrace()

trace.log_reject(
    formulation_id="F-001",
    reason="Phosphorus = 0.09% exceeds API SP limit (0.08%)"
)

trace.log_accept(
    formulation_id="F-002",
    reason="Bio-ester base oil reduced CO₂ score by 18% while meeting SAPS limits"
)

for entry in trace.export():
    print(entry)
from engine.regulatory_headroom import RegulatoryHeadroom
from explainability.decision_trace import DecisionTrace

trace = DecisionTrace()
headroom_engine = RegulatoryHeadroom()

# Example formulation aggregate values
formulation_metrics = {
    "phosphorus_pct": 0.05,
    "sulfur_pct": 0.18,
    "ash_contribution": 0.6
}

headroom = headroom_engine.calculate(formulation_metrics)

trace.log_accept(
    formulation_id="F-HEADROOM-01",
    reason=f"Regulatory headroom achieved: {headroom}"
)

print(headroom)

from engine.sustainability_scorer import SustainabilityScorer

scorer = SustainabilityScorer()

# Example aggregated formulation sustainability metrics
sustainability_metrics = {
    "avg_toxicity": 0.32,
    "carbon_index": 0.45,
    "biodegradability": 0.7
}

sustainability_score = scorer.score(sustainability_metrics)

trace.log_accept(
    formulation_id="F-SUSTAIN-01",
    reason=f"Sustainability score computed: {sustainability_score}"
)

print(sustainability_score)
from engine.cost_elasticity import CostElasticityEngine

cost_engine = CostElasticityEngine(max_cost_increase_pct=5)

baseline_cost = 100.0          # hypothetical baseline cost
formulation_cost = 104.0       # new formulation cost
sustainability_total = sustainability_score["total_sustainability_score"]

cost_result = cost_engine.evaluate(
    baseline_cost=baseline_cost,
    formulation_cost=formulation_cost,
    sustainability_score=sustainability_total
)

trace.log_accept(
    formulation_id="F-COST-01",
    reason=f"Cost elasticity assessment: {cost_result}"
)

print(cost_result)

from simulations.scenario_runner import ScenarioRunner

scenario = ScenarioRunner()

scenario_result = scenario.tighten_phosphorus_limit(
    formulation_metrics={
        "phosphorus_pct": 0.05
    },
    reduction_pct=20
)

trace.log_accept(
    formulation_id="F-SCENARIO-01",
    reason=f"Scenario test (20% tighter phosphorus): {scenario_result}"
)

print(scenario_result)
