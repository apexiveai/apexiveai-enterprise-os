from fastapi import APIRouter, HTTPException
from .schemas import BotCreate, BotResponse, ExecutionResponse, FleetAction, JobRequest, JobResponse, RobotResponse
from services.service import RPAService

router = APIRouter(tags=["RPA Engine"])
service = RPAService()

@router.get("/health")
def health():
    return service.health()

@router.post("/jobs", response_model=JobResponse)
def submit_job(request: JobRequest):
    return service.submit(request.robot, request.parameters, request.schedule)

@router.get("/bots", response_model=list[BotResponse])
def list_bots():
    return service.list_bots()

@router.post("/bots", response_model=BotResponse)
def create_bot(request: BotCreate):
    return service.create_bot(
        request.name,
        request.description,
        request.trigger,
        request.retry_count,
    )

@router.post("/bots/{bot_id}/test", response_model=ExecutionResponse)
def test_bot(bot_id: str):
    try:
        return service.test_bot(bot_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Bot not found")

@router.post("/bots/{bot_id}/deploy", response_model=BotResponse)
def deploy_bot(bot_id: str):
    try:
        return service.deploy_bot(bot_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Bot not found")

@router.get("/executions", response_model=list[ExecutionResponse])
def list_executions(bot_id: str | None = None):
    return service.list_executions(bot_id)

@router.get("/robots", response_model=list[RobotResponse])
def list_robots():
    return service.list_robots()

@router.post("/robots/{robot_id}/control")
def control_robot(robot_id: str, request: FleetAction):
    return service.control_robot(robot_id, request.action)

@router.post("/emergency-stop")
def emergency_stop():
    return service.emergency_stop()
