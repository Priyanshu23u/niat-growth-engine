"""
Campus Service — Query and Filtering logic for NIAT's 35+ Partner Campuses (8 representative campuses in demo dataset)
"""

from typing import List, Optional, Dict, Any
from backend.app.models.campus import NIAT_PARTNER_CAMPUSES, PartnerCampus


def search_campuses(
    state: Optional[str] = None,
    max_budget: Optional[int] = None,
    min_nat_score: Optional[int] = None,
    keyword: Optional[str] = None,
) -> List[PartnerCampus]:
    """
    Filters partner campuses based on criteria.
    """
    results: List[PartnerCampus] = []
    kw_lower = keyword.lower().strip() if keyword else None

    for campus in NIAT_PARTNER_CAMPUSES:
        # State filter
        if state and state != "All" and campus.state != state:
            continue

        # Budget filter
        if max_budget and campus.total_annual_fee > max_budget:
            continue

        # NAT Percentile filter
        if min_nat_score and campus.min_nat_percentile > min_nat_score:
            continue

        # Keyword filter (campus name, city, state, or specializations)
        if kw_lower:
            name_match = kw_lower in campus.name.lower()
            city_match = kw_lower in campus.city.lower()
            state_match = kw_lower in campus.state.lower()
            spec_match = any(kw_lower in s.lower() for s in campus.specializations)
            if not (name_match or city_match or state_match or spec_match):
                continue

        results.append(campus)

    return results


def get_campus_by_id(campus_id: str) -> Optional[PartnerCampus]:
    """Retrieve a single campus by its unique ID."""
    for campus in NIAT_PARTNER_CAMPUSES:
        if campus.id == campus_id:
            return campus
    return None


def get_all_states() -> List[str]:
    """Retrieve sorted list of unique states where partner campuses exist."""
    return sorted(list(set(c.state for c in NIAT_PARTNER_CAMPUSES)))
