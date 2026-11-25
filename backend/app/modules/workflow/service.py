from uuid import uuid4


class WorkflowService:
    def __init__(self):
        self.workflows: dict[str, dict] = {}
        self.executions: dict[str, dict] = {}
        self.human_tasks: dict[str, dict] = {}

    def create(self, name: str, description: str, nodes: list[dict]) -> dict:
        workflow_id = str(uuid4())
        workflow = {
            "workflow_id": workflow_id,
            "name": name,
            "description": description,
            "version": "1.0",
            "status": "draft",
            "nodes": nodes,
        }
        self.workflows[workflow_id] = workflow
        return workflow

    def list_workflows(self) -> list[dict]:
        return list(self.workflows.values())

    def deploy(self, workflow_id: str) -> dict:
        workflow = self.workflows[workflow_id]
        workflow["status"] = "deployed"
        workflow["version"] = str(float(workflow["version"]) + 0.1)[:3]
        return workflow

    def start(self, workflow_id: str, variables: dict | None = None) -> dict:
        if workflow_id not in self.workflows:
            raise KeyError(workflow_id)
        execution_id = str(uuid4())
        execution = {
            "execution_id": execution_id,
            "workflow_id": workflow_id,
            "status": "running",
            "variables": variables or {},
            "history": [{"step": "Start", "status": "completed"}],
        }
        self.executions[execution_id] = execution
        return execution

    def list_executions(self) -> list[dict]:
        return list(self.executions.values())

    def create_human_task(self, execution_id: str, name: str, assignee: str) -> dict:
        task_id = str(uuid4())
        task = {
            "task_id": task_id,
            "execution_id": execution_id,
            "name": name,
            "assignee": assignee,
            "status": "pending",
        }
        self.human_tasks[task_id] = task
        return task

    def list_human_tasks(self) -> list[dict]:
        return list(self.human_tasks.values())

    def complete_human_task(self, task_id: str, decision: str) -> dict:
        task = self.human_tasks[task_id]
        task["status"] = "completed"
        task["decision"] = decision
        return task
