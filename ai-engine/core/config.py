from pydantic import BaseModel

class AIEngineConfig(BaseModel):
    environment: str = "development"
    default_model: str = "apexive-default"
    max_context_tokens: int = 128000
