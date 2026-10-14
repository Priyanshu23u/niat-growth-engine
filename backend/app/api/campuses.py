"""
API Router: Partner Campuses Query & Explorer
"""

from typing import Optional
from fastapi import APIRouter, Query
from backend.app.services.campus_service import search_campuses, get_all_states
from backend.app.models.campus import NIAT_PARTNER_CAMPUSES

router = APIRouter(prefix="/api/campuses", tags=["Partner Campuses"])


@router.get("")
def get_campuses(
    state: Optional[str] = Query(None, description="State name (e.g. Telangana, Tamil Nadu)"),
    maxBudget: Optional[int] = Query(None, description="Max annual budget in INR"),
    minNatScore: Optional[int] = Query(None, description="Minimum NAT Percentile"),
    keyword: Optional[str] = Query(None, description="Search keyword"),
):
    """
    Retrieves filtered list of NIAT's 35+ partner university campuses.
    """
    matched = search_campuses(
        state=state,
        max_budget=maxBudget,
        min_nat_score=minNatScore,
        keyword=keyword,
    )
    states = get_all_states()

    return {
        "success": True,
        "totalCount": len(NIAT_PARTNER_CAMPUSES),
        "matchedCount": len(matched),
        "states": states,
        "campuses": [c.model_dump() for c in matched],
        "total": len(matched),
    }
