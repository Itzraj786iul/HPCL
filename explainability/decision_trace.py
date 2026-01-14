# explainability/decision_trace.py

class DecisionTrace:
    def __init__(self):
        self.logs = []

    def log_accept(self, formulation_id, reason):
        self.logs.append({
            "formulation_id": formulation_id,
            "decision": "ACCEPTED",
            "reason": reason
        })

    def log_reject(self, formulation_id, reason):
        self.logs.append({
            "formulation_id": formulation_id,
            "decision": "REJECTED",
            "reason": reason
        })

    def log_penalty(self, formulation_id, reason):
        self.logs.append({
            "formulation_id": formulation_id,
            "decision": "PENALIZED",
            "reason": reason
        })

    def export(self):
        return self.logs
