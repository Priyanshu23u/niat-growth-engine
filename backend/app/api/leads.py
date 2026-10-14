"""
API Router: Leads Pipeline & Provisional Seat Reservations
"""

import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from fastapi import APIRouter
from backend.app.schemas.lead import (
    LeadCreateRequest,
    SeatReservationRequest,
    SeatReservationResponse,
)
from backend.app.database import db

router = APIRouter(prefix="/api", tags=["Leads & Seat Reservations"])


@router.get("/leads")
def get_leads_telemetry():
    """
    Returns the real-time consultation lead pipeline and Growth Manager A/B telemetry.
    """
    leads = db.get_all_leads()
    analytics = db.get_analytics()
    return {
        "success": True,
        "leads": leads,
        "analytics": analytics,
    }


@router.post("/leads")
def record_lead(body: LeadCreateRequest):
    """
    Records a new parent/student consultation lead session.
    """
    new_lead = {
        "id": f"lead-{str(int(time.time() * 1000))[-4:]}",
        "studentName": body.studentName or "Student Aspirant",
        "parentName": body.parentName or "Parent",
        "parentPhone": body.parentPhone or "+91 98765 43210",
        "language": body.language or "en",
        "boardPercentage": body.boardPercentage or 85,
        "natScore": body.natScore or 75,
        "state": body.state or "Telangana",
        "budgetAnnual": body.budgetAnnual or 300000,
        "objectionsAsked": body.objectionsAsked or ["accreditation"],
        "matchedCampusId": body.matchedCampusId,
        "matchedCampusName": body.matchedCampusName,
        "dossierGenerated": bool(body.dossierGenerated),
        "seatReserved": bool(body.seatReserved),
        "tokenAmount": body.tokenAmount or (10000 if body.seatReserved else 0),
        "status": "converted" if body.seatReserved else "in_consultation",
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "source": "ParentTrust Web Console",
    }

    saved_lead = db.add_lead(new_lead)
    return {
        "success": True,
        "message": "Lead session recorded successfully",
        "lead": saved_lead,
    }


@router.post("/reserve-seat", response_model=Dict[str, Any])
def reserve_provisional_seat(body: SeatReservationRequest):
    """
    Locks a provisional seat with a 100% refundable token (14-day window, 48h lock).
    """
    now = datetime.now(timezone.utc)
    reservation_id = f"SEAT-{str(int(time.time() * 1000))[-8:]}"

    reservation = {
        "reservationId": reservation_id,
        "studentName": body.studentName,
        "parentName": body.parentName,
        "parentPhone": body.parentPhone,
        "campusId": body.campusId or "campus-chaitanya-hyd",
        "campusName": body.campusName or "NIAT Partner University",
        "status": "PROVISIONAL_CONFIRMED",
        "tokenAmount": 10000,
        "refundableWindowDays": 14,
        "expiresAt": (now + timedelta(hours=48)).isoformat(),
        "confirmedAt": now.isoformat(),
        "message": "Your provisional seat has been reserved. A counselor will contact you within 2 hours.",
    }

    # Record to persistent leads ledger
    db.add_lead({
        "id": f"lead-{str(int(time.time() * 1000))[-4:]}",
        "studentName": body.studentName,
        "parentName": body.parentName,
        "parentPhone": body.parentPhone,
        "language": "te",
        "boardPercentage": 88,
        "natScore": 82,
        "state": "Telangana",
        "budgetAnnual": 300000,
        "objectionsAsked": ["accreditation", "roi_financial"],
        "matchedCampusId": reservation["campusId"],
        "matchedCampusName": reservation["campusName"],
        "dossierGenerated": True,
        "seatReserved": True,
        "tokenAmount": 10000,
        "status": "converted",
        "createdAt": now.isoformat(),
        "source": "1-Click Seat Reservation Modal",
    })

    return {
        "success": True,
        "reservation": reservation,
    }
