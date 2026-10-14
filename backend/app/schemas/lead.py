"""
Pydantic Schemas for Leads & Seat Reservations
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class LeadSession(BaseModel):
    id: str
    studentName: str
    parentName: str
    parentPhone: str
    language: str = "en"
    boardPercentage: int = 85
    natScore: int = 75
    state: str = "Telangana"
    budgetAnnual: int = 300000
    objectionsAsked: List[str] = Field(default_factory=list)
    matchedCampusId: Optional[str] = None
    matchedCampusName: Optional[str] = None
    dossierGenerated: bool = False
    seatReserved: bool = False
    tokenAmount: int = 0
    status: str = "in_consultation"
    createdAt: str
    source: str = "ParentTrust Web Console"


class LeadCreateRequest(BaseModel):
    studentName: Optional[str] = "Student Aspirant"
    parentName: Optional[str] = "Parent"
    parentPhone: Optional[str] = "+91 98765 43210"
    language: Optional[str] = "en"
    boardPercentage: Optional[int] = 85
    natScore: Optional[int] = 75
    state: Optional[str] = "Telangana"
    budgetAnnual: Optional[int] = 300000
    objectionsAsked: Optional[List[str]] = Field(default_factory=lambda: ["accreditation"])
    matchedCampusId: Optional[str] = None
    matchedCampusName: Optional[str] = None
    dossierGenerated: Optional[bool] = False
    seatReserved: Optional[bool] = False
    tokenAmount: Optional[int] = 0


class SeatReservationRequest(BaseModel):
    studentName: str
    parentName: str
    parentPhone: str
    campusId: Optional[str] = "campus-chaitanya-hyd"
    campusName: Optional[str] = "NIAT Partner University"


class SeatReservationResponse(BaseModel):
    reservationId: str
    studentName: str
    parentName: str
    parentPhone: str
    campusId: str
    campusName: str
    status: str = "PROVISIONAL_CONFIRMED"
    tokenAmount: int = 10000
    refundableWindowDays: int = 14
    expiresAt: str
    confirmedAt: str
    message: str
