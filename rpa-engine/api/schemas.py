from pydantic import BaseModel, Field

class JobRequest(BaseModel):
    robot: str = Field(min_length=1, max_length=200)
    parameters: dict = Field(default_factory=dict)
    schedule: str | None = None

class JobResponse(BaseModel):
    job_id: str
    robot: str
    status: str = "queued"

class BotCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str = ""
    trigger: str = "17:00"
    retry_count: int = Field(default=3, ge=0, le=10)

class BotResponse(BaseModel):
    bot_id: str
    name: str
    description: str
    trigger: str
    retry_count: int
    status: str
    steps: list[str] = Field(default_factory=list)

class ExecutionResponse(BaseModel):
    execution_id: str
    bot_id: str
    status: str
    evidence: dict

class RobotResponse(BaseModel):
    robot_id: str
    name: str
    mode: str
    host: str
    status: str
    version: str

class FleetAction(BaseModel):
    action: str = Field(pattern="^(start|stop|restart|kill)$")
