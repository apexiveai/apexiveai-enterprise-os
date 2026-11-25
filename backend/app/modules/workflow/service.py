
import json
import os
import tempfile

from pathlib import Path
from threading import RLock
from uuid import uuid4


class WorkflowService:
    def __init__(self, storage_path: Path | None = None):
        self.storage_path = Path(storage_path) if storage_path else None
        self._lock = RLock()

        self.workflows: dict[str, dict] = {}
        self.executions: dict[str, dict] = {}
        self.human_tasks: dict[str, dict] = {}

        if self.storage_path:
            self._load()

    def _load(self) -> None:
        if not self.storage_path or not self.storage_path.exists():
            return

        try:
            saved = json.loads(
                self.storage_path.read_text(encoding="utf-8")
            )

            self.workflows = saved.get("workflows", {})
            self.executions = saved.get("executions", {})
            self.human_tasks = saved.get("human_tasks", {})

        except (OSError, json.JSONDecodeError, AttributeError) as error:
            raise RuntimeError(
                f"Workflow storage could not be loaded: {self.storage_path}"
            ) from error

    def _persist(self) -> None:
        if self.storage_path is None:
            return

        self.storage_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {
            "workflows": self.workflows,
            "executions": self.executions,
            "human_tasks": self.human_tasks,
        }

        temporary_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.storage_path.parent,
                prefix=".workflows-",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:

                temporary_path = Path(temporary_file.name)

                json.dump(
                    payload,
                    temporary_file,
                    ensure_ascii=False,
                    indent=2,
                )

                temporary_file.flush()
                os.fsync(temporary_file.fileno())

            os.replace(
                temporary_path,
                self.storage_path,
            )

        finally:
            if temporary_path and temporary_path.exists():
                temporary_path.unlink()

    def create(self, name: str, description: str, nodes: list[dict]) -> dict:
        with self._lock:
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
            self._persist()

            return workflow

    def update(
        self,
        workflow_id: str,
        name: str,
        description: str,
        nodes: list[dict],
    ) -> dict:
        with self._lock:
            workflow = self.workflows[workflow_id]

            workflow.update(
                name=name,
                description=description,
                nodes=nodes,
                status="draft",
            )

            self._persist()
            return workflow

    def list_workflows(self) -> list[dict]:
        with self._lock:
            return list(self.workflows.values())

    def deploy(self, workflow_id: str) -> dict:
        with self._lock:
            workflow = self.workflows[workflow_id]

            workflow["status"] = "deployed"
            workflow["version"] = str(
                round(float(workflow["version"]) + 0.1, 1)
            )

            self._persist()
            return workflow

    def start(
        self,
        workflow_id: str,
        variables: dict | None = None,
    ) -> dict:
        with self._lock:
            if workflow_id not in self.workflows:
                raise KeyError(workflow_id)

            execution_id = str(uuid4())

            execution = {
                "execution_id": execution_id,
                "workflow_id": workflow_id,
                "status": "running",
                "variables": variables or {},
                "history": [
                    {"step": "Start", "status": "completed"}
                ],
            }

            self.executions[execution_id] = execution
            self._persist()

            return execution

    def list_executions(self) -> list[dict]:
        with self._lock:
            return list(self.executions.values())

    def create_human_task(
        self,
        execution_id: str,
        name: str,
        assignee: str,
    ) -> dict:
        with self._lock:
            task_id = str(uuid4())

            task = {
                "task_id": task_id,
                "execution_id": execution_id,
                "name": name,
                "assignee": assignee,
                "status": "pending",
            }

            self.human_tasks[task_id] = task
            self._persist()

            return task

    def list_human_tasks(self) -> list[dict]:
        with self._lock:
            return list(self.human_tasks.values())

    def complete_human_task(
        self,
        task_id: str,
        decision: str,
    ) -> dict:
        with self._lock:
            task = self.human_tasks[task_id]

            task["status"] = "completed"
            task["decision"] = decision

            self._persist()
            return task
