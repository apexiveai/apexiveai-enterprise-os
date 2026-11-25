from app.modules.workflow.service import WorkflowService


def test_workflow_data_persists_between_service_instances(tmp_path):
    storage_path = tmp_path / "workflows.json"
    first_service = WorkflowService(storage_path)
    workflow = first_service.create(
        "Purchase Approval",
        "Approve purchases",
        [{"id": "start", "type": "Start", "name": "Request"}],
    )
    first_service.deploy(workflow["workflow_id"])
    execution = first_service.start(workflow["workflow_id"], {"amount": 500})
    task = first_service.create_human_task(
        execution["execution_id"],
        "Finance Approval",
        "Finance Manager",
    )

    restarted_service = WorkflowService(storage_path)

    assert restarted_service.list_workflows()[0]["status"] == "deployed"
    assert restarted_service.list_executions()[0]["execution_id"] == execution["execution_id"]
    assert restarted_service.complete_human_task(task["task_id"], "approved")["status"] == "completed"


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
