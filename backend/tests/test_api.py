"""
Integration Tests: FastAPI REST Endpoints & Web Workflows
"""

import sys
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoints():
    res1 = client.get("/health")
    assert res1.status_code == 200
    assert res1.json()["status"] == "healthy"
    assert "FastAPI" in res1.json()["framework"]

    res2 = client.get("/api/health")
    assert res2.status_code == 200
    assert res2.json()["status"] == "healthy"


def test_get_campuses_api():
    res = client.get("/api/campuses?state=Telangana")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["matchedCount"] >= 2
    assert "Telangana" in data["states"]


def test_roi_api_endpoints():
    # POST
    post_res = client.post("/api/roi", json={
        "niatTotalFee": 1200000,
        "tier3TotalFee": 400000,
        "niatExpectedStartingSalary": 850000,
        "tier3ExpectedStartingSalary": 360000,
    })
    assert post_res.status_code == 200
    post_data = post_res.json()
    assert post_data["success"] is True
    assert post_data["metrics"]["breakEvenMonths"] > 0

    # GET default
    get_res = client.get("/api/roi")
    assert get_res.status_code == 200
    assert get_res.json()["metrics"]["breakEvenMonths"] > 0


def test_agent_api_endpoint():
    res = client.post("/api/agent", json={
        "prompt": "Will AI kill software coding jobs by 2028?",
        "language": "en",
        "objectionCategory": "ai_threat",
        "studentProfile": {
            "name": "Sai Teja",
            "parentName": "Venkatesh",
            "boardPercentage": 88,
            "natScore": 82,
            "state": "Telangana",
            "budgetAnnual": 300000,
        },
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert len(data["executedTools"]) == 4
    assert data["dossierData"]["dossierId"].startswith("NIAT-DOSSIER-")


def test_leads_telemetry_and_creation():
    # GET leads
    get_res = client.get("/api/leads")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["success"] is True
    assert len(data["leads"]) >= 5
    assert "funnelComparison" in data["analytics"]

    # POST lead
    post_res = client.post("/api/leads", json={
        "studentName": "Divya Reddy",
        "parentName": "Ramesh Reddy",
        "parentPhone": "+91 98480 99887",
        "language": "te",
        "state": "Telangana",
        "budgetAnnual": 320000,
        "seatReserved": False,
    })
    assert post_res.status_code == 200
    assert post_res.json()["lead"]["studentName"] == "Divya Reddy"


def test_seat_reservation_endpoint():
    res = client.post("/api/reserve-seat", json={
        "studentName": "Sai Teja Reddy",
        "parentName": "K. Venkatesh",
        "parentPhone": "+91 98480 23456",
        "campusId": "campus-chaitanya-hyd",
        "campusName": "NIAT @ Chaitanya University",
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["reservation"]["status"] == "PROVISIONAL_CONFIRMED"
    assert data["reservation"]["tokenAmount"] == 10000


def test_webhook_simulation_endpoint():
    res = client.post("/api/webhook", json={
        "action": "DISPATCH_WHATSAPP_DOSSIER",
        "language": "te",
        "leadData": {
            "parentName": "వెంకటేష్",
            "studentName": "సాయి తేజ",
            "parentPhone": "+91 98480 23456",
        },
    })
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["dispatch"]["status"] == "SIMULATED_SUCCESS"
    assert "నమస్కారం" in data["dispatch"]["dispatchedText"]


def test_static_frontend_serving():
    res = client.get("/")
    assert res.status_code == 200
    assert "NIAT ParentTrust AI" in res.text
    assert "text/html" in res.headers.get("content-type", "")
