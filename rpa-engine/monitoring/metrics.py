rpa_jobs_submitted = 0

def record_job() -> int:
    global rpa_jobs_submitted
    rpa_jobs_submitted += 1
    return rpa_jobs_submitted
