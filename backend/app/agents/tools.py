"""
Executable Agent Tools for Admissions Advisory
Preserves the 4 core tools:
 1. tool_query_campuses
 2. tool_calculate_roi
 3. tool_compare_curriculum
 4. tool_generate_dossier
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from backend.app.services.campus_service import search_campuses
from backend.app.services.roi_calculator import calculate_roi_model
from backend.app.services.dossier_service import generate_dossier
from backend.app.models.campus import PartnerCampus, NIAT_PARTNER_CAMPUSES
from backend.app.models.curriculum import CURRICULUM_COMPARISON
from backend.app.schemas.roi import RoiSimulationInput
from backend.app.schemas.agent import ToolExecutionRecord


def tool_query_campuses(
    state: Optional[str] = None,
    budget_max: Optional[int] = None,
    min_nat_score: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Tool 1: Queries and ranks NIAT partner campuses based on student academic profile and budget.
    """
    matched = search_campuses(
        state=state if state != "All" else None,
        max_budget=(budget_max + 50000) if budget_max else None,
        min_nat_score=min_nat_score,
    )
    primary = matched[0] if matched else NIAT_PARTNER_CAMPUSES[0]

    record = ToolExecutionRecord(
        toolName="tool_query_campuses",
        input={"state": state, "budgetMax": budget_max, "minNatScore": min_nat_score},
        outputSummary=f"Matched {len(matched)} partner campuses. Primary recommendation: {primary.name} in {primary.city} ({primary.accreditation}).",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    return {
        "matched_campuses": matched,
        "primary_campus": primary,
        "record": record,
    }


def tool_calculate_roi(
    niat_fee: int,
    tier3_fee: int = 400000,
    starting_salary: int = 850000,
) -> Dict[str, Any]:
    """
    Tool 2: Computes 5-year career net wealth gain, loan monthly EMI, and break-even timeline in months.
    """
    roi_input = RoiSimulationInput(
        niatTotalFee=niat_fee,
        tier3TotalFee=tier3_fee,
        niatExpectedStartingSalary=starting_salary,
        tier3ExpectedStartingSalary=360000,
        loanSharePercentage=60.0,
        loanInterestRate=8.5,
    )
    model = calculate_roi_model(roi_input)
    break_even = model["metrics"]["breakEvenMonths"]
    break_even_yrs = model["metrics"]["breakEvenYears"]
    wealth_lakhs = f"{(model['metrics']['fiveYearNetWealthAdvantage'] / 100000):.1f}"

    record = ToolExecutionRecord(
        toolName="tool_calculate_roi",
        input={"niatTotalFee": niat_fee, "tier3TotalFee": tier3_fee, "expectedStartingSalary": starting_salary},
        outputSummary=f"Break-even period: {break_even} months ({break_even_yrs} yrs). 5-year net wealth advantage: ₹{wealth_lakhs} Lakhs over traditional tier-3 colleges.",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    return {
        "roi_model": model,
        "record": record,
    }


def tool_compare_curriculum(focus_areas: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Tool 3: Analyzes 8-semester curriculum contrast between legacy tier-3 theory vs NIAT applied AI & Lab 5.0.
    """
    record = ToolExecutionRecord(
        toolName="tool_compare_curriculum",
        input={"focusAreas": focus_areas or ["AI_Threat", "Coding_Hours", "Accreditation"]},
        outputSummary="NIAT offers 18-28 coding hrs/week with hands-on GenAI, LLMs, and Microservices vs Tier-3's 2-4 hrs/week of obsolete C/workshop theory.",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    return {
        "curriculum": CURRICULUM_COMPARISON,
        "record": record,
    }


def tool_generate_dossier(
    student_name: str,
    parent_name: str,
    primary_campus: PartnerCampus,
    roi_model: Dict[str, Any],
    language: str = "en",
) -> Dict[str, Any]:
    """
    Tool 4: Assembles the official personalized Family Admissions Dossier with verifiable proof of accreditation.
    """
    dossier = generate_dossier(
        student_name=student_name,
        parent_name=parent_name,
        primary_campus=primary_campus,
        roi_model=roi_model,
        language=language,
    )

    record = ToolExecutionRecord(
        toolName="tool_generate_dossier",
        input={"dossierId": dossier["dossierId"], "studentName": student_name, "matchedCampus": primary_campus.name},
        outputSummary=f"Compiled official NIAT Family Admissions Dossier ({dossier['dossierId']}) with full accreditation proof, financial plan, and provisional seat window.",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    return {
        "dossier": dossier,
        "record": record,
    }
