ai_requests_total = 0

def record_request() -> int:
    global ai_requests_total
    ai_requests_total += 1
    return ai_requests_total
