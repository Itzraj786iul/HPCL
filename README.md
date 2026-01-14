# Sustainable Lubricant Formulation Intelligence Engine

A modular, explainable engine designed to help HPCL formulate
future-ready lubricants by balancing:

- Regulatory compliance (API SP / ACEA C6)
- Sustainability (carbon, toxicity, biodegradability)
- India-specific cost sensitivity
- Future regulatory uncertainty

## Key Capabilities

- Compliance filtering with explainable decisions
- Regulatory headroom computation
- Lifecycle sustainability scoring
- Cost elasticity evaluation for Indian markets
- Scenario simulation for future regulation tightening

## Architecture Overview

data → compliance → headroom → sustainability → cost → scenario → explainability
## How to Run

```bash
pip install -r requirements.txt
python main_step2.py
Output

The engine prints:

Filtered additive sets

Regulatory headroom scores

Sustainability scores

Cost elasticity decisions

Scenario simulation results

Human-readable decision traces
---

## 4️⃣ Add `.gitignore`

### Create file
```powershell
New-Item .gitignore -ItemType File
Paste this
__pycache__/
*.pyc
.env
.vscode/