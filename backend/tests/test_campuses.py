"""
Unit Tests: Partner Campuses Dataset & Search Service
"""

import sys
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.app.models.campus import NIAT_PARTNER_CAMPUSES
from backend.app.services.campus_service import search_campuses, get_campus_by_id, get_all_states


def test_campus_dataset_integrity():
    assert len(NIAT_PARTNER_CAMPUSES) >= 8, f"Expected >= 8 campuses, got {len(NIAT_PARTNER_CAMPUSES)}"

    chaitanya = next((c for c in NIAT_PARTNER_CAMPUSES if c.id == "campus-chaitanya-hyd"), None)
    assert chaitanya is not None, "Chaitanya University must be present"
    assert chaitanya.ugc_approved is True, "Chaitanya must have UGC approval"
    assert chaitanya.total_four_year_fee == 1200000, "Chaitanya fee must be ₹12,00,000"

    dypatil = next((c for c in NIAT_PARTNER_CAMPUSES if c.id == "campus-dypatil-pune"), None)
    assert dypatil is not None, "D.Y. Patil University must be present"

    yenepoya = next((c for c in NIAT_PARTNER_CAMPUSES if c.id == "campus-yenepoya-mng"), None)
    assert yenepoya is not None, "Yenepoya University must be present"

    niu = next((c for c in NIAT_PARTNER_CAMPUSES if c.id == "campus-niu-delhi"), None)
    assert niu is not None, "Noida International University must be present"

    has_lab = any("Lab 5.0" in c.lab_type for c in NIAT_PARTNER_CAMPUSES)
    assert has_lab, "Must specify Lab 5.0 compute pods"


def test_campus_search_by_state():
    telangana = search_campuses(state="Telangana")
    assert len(telangana) >= 2, f"Expected >= 2 Telangana campuses, got {len(telangana)}"
    for c in telangana:
        assert c.state == "Telangana"


def test_campus_search_by_budget():
    budget_campuses = search_campuses(max_budget=320000)
    assert len(budget_campuses) > 0
    for c in budget_campuses:
        assert c.total_annual_fee <= 320000


def test_campus_search_by_keyword():
    ai_campuses = search_campuses(keyword="AI")
    assert len(ai_campuses) > 0


def test_get_campus_by_id():
    campus = get_campus_by_id("campus-chaitanya-hyd")
    assert campus is not None
    assert campus.city.startswith("Hyderabad")

    unknown = get_campus_by_id("non-existent-id")
    assert unknown is None


def test_get_all_states():
    states = get_all_states()
    assert "Telangana" in states
    assert "Karnataka" in states
    assert "Tamil Nadu" in states
    assert "Maharashtra" in states
