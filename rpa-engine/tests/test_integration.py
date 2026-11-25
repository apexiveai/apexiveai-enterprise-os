from services.service import RPAService

def test_submit_job():
    job = RPAService().submit("invoice-sync", {}, None)
    assert job["status"] == "queued"


def test_bot_lifecycle():
    service = RPAService()
    bot = service.create_bot(
        "DAILY_FINANCE_REPORT",
        "Daily report",
        "17:00",
        3,
    )
    assert bot["status"] == "draft"
    execution = service.test_bot(bot["bot_id"])
    assert execution["status"] == "completed"
    deployed = service.deploy_bot(bot["bot_id"])
    assert deployed["status"] == "deployed"


def test_orchestrator_control():
    service = RPAService()
    assert len(service.list_robots()) == 4
    stopped = service.control_robot("ROB-FIN-01", "stop")
    assert stopped["status"] == "stopped"
    emergency = service.emergency_stop()
    assert emergency["dispatching"] == "paused"
