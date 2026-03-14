class ProjectParameters:
    def __init__(self, name: str, budget: float, lambda_finance, horizon, governance):
        self.name = name
        self.budget = budget
        self.lambda_finance = lambda_finance
        self.horizon = horizon
        self.governance = governance