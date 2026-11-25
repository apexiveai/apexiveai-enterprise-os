from core.engine import AIEngine
from core.config import AIEngineConfig

class AIService:
    def __init__(self):
        self.engine = AIEngine(AIEngineConfig())

    def health(self) -> dict:
        return self.engine.status()

    def run(self, prompt: str, agent: str, context: dict) -> dict:
        return {
            "agent": agent,
            "result": f"Processed by {agent}: {prompt[:200]}",
            "status": "completed",
        }
