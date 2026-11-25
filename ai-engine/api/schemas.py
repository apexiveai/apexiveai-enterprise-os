from pydantic import BaseModel, Field

class AgentRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10000)
    agent: str = "general"
    context: dict = Field(default_factory=dict)

class AgentResponse(BaseModel):
    agent: str
    result: str
    status: str = "completed"
