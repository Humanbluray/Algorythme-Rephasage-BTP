class Environment:
    def __init__(self, period, shock, political, constraint):
        self.period = period
        self.external_shock = shock
        self.political_pressure = political
        self.constraint = constraint