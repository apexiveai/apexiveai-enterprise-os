from pydantic import BaseModel

class RPAConfig(BaseModel):
    environment: str = "development"
    default_timeout_seconds: int = 300
    max_concurrency: int = 10
