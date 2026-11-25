from app.modules.workflow.service import WorkflowService


def test_workflow_deployment_and_execution():
    service = WorkflowService()
    workflow = service.create(
        "Purchase Approval",
        "Approve purchases",
        [{"id": "start", "type": "Start", "name": "Request"}],
    )
    deployed = service.deploy(workflow["workflow_id"])
    execution = service.start(workflow["workflow_id"], {"amount": 500})
    assert deployed["status"] == "deployed"
    assert execution["status"] == "running"


def test_human_task_completion():
    service = WorkflowService()
    task = service.create_human_task("execution-1", "Finance Approval", "Finance Manager")
    completed = service.complete_human_task(task["task_id"], "approved")
    assert completed["status"] == "completed"
    assert completed["decision"] == "approved"
