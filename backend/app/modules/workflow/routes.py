
import os
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.modules.workflow.schemas import WorkflowCreate, WorkflowResponse
from app.modules.workflow.service import WorkflowService


router = APIRouter(prefix="/workflow", tags=["Workflow Studio"])

data_directory = Path(
    os.environ.get(
        "APEXIVE_DATA_DIR",
        str(Path(__file__).resolve().parents[3] / "data"),
    )
).expanduser()

storage_path = data_directory / "workflows.json"
service = WorkflowService(storage_path)


@router.get("/definitions", response_model=list[WorkflowResponse])
def list_definitions():
    return service.list_workflows()


@router.post("/definitions", response_model=WorkflowResponse)
def create_definition(request: WorkflowCreate):
    return service.create(
        request.name,
        request.description,
        [node.model_dump() for node in request.nodes],
    )


@router.put("/definitions/{workflow_id}", response_model=WorkflowResponse)
def update_definition(workflow_id: str, request: WorkflowCreate):
    try:
        return service.update(
            workflow_id,
            request.name,
            request.description,
            [node.model_dump() for node in request.nodes],
        )
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )


@router.post("/definitions/{workflow_id}/deploy", response_model=WorkflowResponse)
def deploy_workflow(workflow_id: str):
    try:
        return service.deploy(workflow_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )


@router.post("/executions")
def start_execution(workflow_id: str, variables: dict | None = None):
    try:
        return service.start(workflow_id, variables)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )


@router.get("/executions")
def list_executions():
    return service.list_executions()


@router.get("/tasks")
def list_tasks():
    return service.list_human_tasks()


@router.post("/tasks/{task_id}/complete")
def complete_task(task_id: str, decision: str = "approved"):
    try:
        return service.complete_human_task(task_id, decision)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Human task not found",
        )
