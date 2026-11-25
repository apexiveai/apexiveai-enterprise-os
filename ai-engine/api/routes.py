from fastapi import APIRouter
from .schemas import AgentRequest, AgentResponse
from services.service import AIService

router = APIRouter(tags=["AI Engine"])
service = AIService()

@router.get("/health")
def health():
    return service.health()

@router.post("/agents/run", response_model=AgentResponse)
def run_agent(request: AgentRequest):
    return service.run(request.prompt, request.agent, request.context)
