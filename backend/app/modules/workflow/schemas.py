from pydantic import BaseModel, Field


class WorkflowNode(BaseModel):
    id: str
    type: str
    name: str
    properties: dict = Field(default_factory=dict)


class WorkflowCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str = ""
    nodes: list[WorkflowNode] = Field(default_factory=list)


class WorkflowResponse(BaseModel):
    workflow_id: str
    name: str
    description: str
    version: str = "1.0"
    status: str = "draft"
    nodes: list[WorkflowNode]
