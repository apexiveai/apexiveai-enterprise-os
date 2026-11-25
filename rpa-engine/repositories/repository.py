class JobRepository:
    def __init__(self):
        self.jobs: dict[str, dict] = {}

    def save(self, job_id: str, job: dict) -> dict:
        self.jobs[job_id] = job
        return job
