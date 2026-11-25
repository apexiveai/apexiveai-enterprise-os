from fastapi import APIRouter


router = APIRouter(prefix="/enterprise-suites", tags=["Enterprise Automation Suites"])

SUITES = [
    {"name": "AI Bot Studio", "status": "active", "capabilities": ["bot-builder", "knowledge", "channels", "testing"]},
    {"name": "Agentic Process Automation", "status": "active", "capabilities": ["agents", "rpa", "workflow", "human-loop"]},
    {"name": "Process & Task Mining", "status": "active", "capabilities": ["process-mining", "task-mining", "conformance"]},
    {"name": "Intelligent Documents", "status": "active", "capabilities": ["ocr", "classification", "extraction", "validation"]},
    {"name": "Integration Studio", "status": "active", "capabilities": ["api", "connectors", "webhooks", "mapping"]},
    {"name": "Decision & Rules", "status": "active", "capabilities": ["rules", "decision-trees", "simulation"]},
    {"name": "Workforce & Collaboration", "status": "active", "capabilities": ["tasks", "approvals", "teams", "capacity"]},
    {"name": "Automation Quality", "status": "active", "capabilities": ["unit-tests", "visual-tests", "quality-gates"]},
    {"name": "Automation Center", "status": "active", "capabilities": ["operations", "incidents", "capacity", "queues"]},
    {"name": "Low-Code Builder", "status": "active", "capabilities": ["forms", "pages", "data", "logic", "publish"]},
    {"name": "Enterprise Data", "status": "active", "capabilities": ["catalog", "lineage", "quality", "pipelines"]},
    {"name": "Digital Twin", "status": "active", "capabilities": ["assets", "iot", "gis", "simulation"]},
    {"name": "Security & Governance", "status": "active", "capabilities": ["identity", "policy", "audit", "compliance"]},
    {"name": "Enterprise Marketplace", "status": "active", "capabilities": ["templates", "bots", "agents", "connectors"]},
    {"name": "Advanced Automation", "status": "active", "capabilities": ["vision", "llm", "speech", "self-healing", "edge"]},
]


@router.get("")
def list_suites():
    return {"total": len(SUITES), "items": SUITES}


@router.get("/{suite_name}")
def get_suite(suite_name: str):
    normalized = suite_name.lower().replace("-", " ")
    suite = next((item for item in SUITES if item["name"].lower() == normalized), None)
    if suite is None:
        return {"error": "Suite not found"}
    return suite
