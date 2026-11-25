def publish_job_submitted(job_id: str, robot: str) -> dict:
    return {"event": "rpa.job.submitted", "job_id": job_id, "robot": robot}
