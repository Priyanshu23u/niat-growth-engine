"""
Unit Tests: AI Admissions Agent Tools & Pipeline
"""

import sys
import pytest
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.app.schemas.agent import AgentRequestBody, StudentProfile
from backend.app.agents.tools import (
    tool_query_campuses,
    tool_calculate_roi,
    tool_compare_curriculum,
    tool_generate_dossier,
)
from backend.app.agents.admissions_agent import process_admissions_question, generate_multilingual_fallback


def test_tool_query_campuses():
    res = tool_query_campuses(state="Telangana", budget_max=320000, min_nat_score=75)
    assert len(res["matched_campuses"]) > 0
    assert res["primary_campus"] is not None
    assert res["record"].toolName == "tool_query_campuses"


def test_tool_calculate_roi():
    res = tool_calculate_roi(niat_fee=1200000)
    assert res["roi_model"]["metrics"]["breakEvenMonths"] > 0
    assert res["record"].toolName == "tool_calculate_roi"


def test_tool_compare_curriculum():
    res = tool_compare_curriculum()
    assert len(res["curriculum"]) == 8
    assert res["record"].toolName == "tool_compare_curriculum"


def test_tool_generate_dossier():
    campus_res = tool_query_campuses(state="Telangana")
    roi_res = tool_calculate_roi(niat_fee=1200000)

    dossier_res = tool_generate_dossier(
        student_name="Sai Teja",
        parent_name="Venkatesh",
        primary_campus=campus_res["primary_campus"],
        roi_model=roi_res["roi_model"],
        language="te",
    )
    dossier = dossier_res["dossier"]
    assert dossier["dossierId"].startswith("NIAT-DOSSIER-")
    assert dossier["studentName"] == "Sai Teja"
    assert dossier_res["record"].toolName == "tool_generate_dossier"


def test_multilingual_fallback_synthesis():
    campus_res = tool_query_campuses(state="Telangana")
    roi_res = tool_calculate_roi(niat_fee=1200000)

    # Telugu accreditation response
    te_resp = generate_multilingual_fallback(
        language="te",
        objection_category="accreditation",
        parent_name="వెంకటేష్",
        student_name="సాయి తేజ",
        primary_campus=campus_res["primary_campus"],
        roi_model=roi_res["roi_model"],
    )
    assert "గౌరవనీయులైన" in te_resp
    assert "యూజీసీ" in te_resp

    # Tamil accreditation response
    ta_resp = generate_multilingual_fallback(
        language="ta",
        objection_category="accreditation",
        parent_name="முருகன்",
        student_name="கார்த்திக்",
        primary_campus=campus_res["primary_campus"],
        roi_model=roi_res["roi_model"],
    )
    assert "மதிப்பிற்குரிய" in ta_resp

    # Hindi accreditation response
    hi_resp = generate_multilingual_fallback(
        language="hi",
        objection_category="accreditation",
        parent_name="राजेश शर्मा",
        student_name="अनन्या",
        primary_campus=campus_res["primary_campus"],
        roi_model=roi_res["roi_model"],
    )
    assert "आदरणीय" in hi_resp


def test_agent_pipeline_execution():
    import asyncio
    body = AgentRequestBody(
        prompt="ఈ డిగ్రీ యూజీసీ గుర్తింపు పొందినదేనా?",
        language="te",
        objectionCategory="accreditation",
        studentProfile=StudentProfile(
            studentName="Sai Teja Reddy",
            parentName="K. Venkatesh",
            boardPercentage=88,
            natScore=82,
            state="Telangana",
            budgetAnnual=300000,
        ),
    )
    response = asyncio.run(process_admissions_question(body))
    assert response.success is True
    assert len(response.executedTools) == 4
    assert "గౌరవనీయులైన" in response.agentResponse or "UGC" in response.agentResponse
    assert response.dossierData["dossierId"].startswith("NIAT-DOSSIER-")
