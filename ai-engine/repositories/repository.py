class AgentRepository:
    def __init__(self):
        self.executions: list[dict] = []

    def save(self, execution: dict) -> dict:
        self.executions.append(execution)
        return execution
