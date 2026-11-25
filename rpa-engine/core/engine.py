from dataclasses import dataclass
from .config import RPAConfig

@dataclass
class RPAEngine:
    config: RPAConfig

    def status(self) -> dict:
        return {
            "engine": "rpa",
            "status": "healthy",
            "max_concurrency": self.config.max_concurrency,
        }
