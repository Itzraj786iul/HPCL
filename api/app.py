from fastapi import FastAPI
from engine.regulatory_headroom import RegulatoryHeadroom
from engine.sustainability_scorer import SustainabilityScorer
from engine.cost_elasticity import CostElasticityEngine
from simulations.scenario_runner import ScenarioRunner
from explainability.decision_trace import DecisionTrace

app = FastAPI(
    title="HPCL Sustainable Lubricant Formulation Engine",
    description="Explainable, regulation-aware formulation intelligence system",
    version="1.0"
)

@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/evaluate-formulation")
def evaluate_formulation(payload: dict):
    """
    Expected payload:
    {
      "formulation_metrics": {
        "phosphorus_pct": 0.05,
        "sulfur_pct": 0.18,
        "ash_contribution": 0.6
      },
      "sustainability_metrics": {
        "avg_toxicity": 0.32,
        "carbon_index": 0.45,
        "biodegradability": 0.7
      },
      "baseline_cost": 100,
      "formulation_cost": 104
    }
    """

    trace = DecisionTrace()

    # Regulatory headroom
    headroom_engine = RegulatoryHeadroom()
    headroom = headroom_engine.calculate(payload["formulation_metrics"])
    trace.log_accept("FORMULATION", f"Regulatory headroom computed: {headroom}")

    # Sustainability score
    sustainability_engine = SustainabilityScorer()
    sustainability = sustainability_engine.score(payload["sustainability_metrics"])
    trace.log_accept("FORMULATION", f"Sustainability score: {sustainability}")

    # Cost elasticity
    cost_engine = CostElasticityEngine()
    cost_result = cost_engine.evaluate(
        baseline_cost=payload["baseline_cost"],
        formulation_cost=payload["formulation_cost"],
        sustainability_score=sustainability["total_sustainability_score"]
    )
    trace.log_accept("FORMULATION", f"Cost elasticity result: {cost_result}")

    # Scenario simulation (20% tighter phosphorus)
    scenario_engine = ScenarioRunner()
    scenario = scenario_engine.tighten_phosphorus_limit(
        formulation_metrics=payload["formulation_metrics"],
        reduction_pct=20
    )
    trace.log_accept("FORMULATION", f"Future regulation scenario: {scenario}")

    return {
        "regulatory_headroom": headroom,
        "sustainability": sustainability,
        "cost_assessment": cost_result,
        "scenario_simulation": scenario,
        "decision_trace": trace.export()
    }
