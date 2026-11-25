from dataclasses import dataclass
from .config import AIEngineConfig

@dataclass
class AIEngine:
    config: AIEngineConfig

    def status(self) -> dict:
        return {
            "engine": "ai",
            "status": "healthy",
            "model": self.config.default_model,
        }
