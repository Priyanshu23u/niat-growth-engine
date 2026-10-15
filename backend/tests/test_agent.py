"""
Unit Tests: AI Admissions Agent Tools & Pipeline
"""

import sys
import json
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
    assert len(response.executedTools) >= 2
    assert response.provider in ("fallback", "groq")
    assert "గౌరవనీయులైన" in response.agentResponse or "UGC" in response.agentResponse
    assert response.dossierData["dossierId"].startswith("NIAT-DOSSIER-")


def test_groq_service_unconfigured():
    from backend.app.services.groq_service import is_groq_configured, call_groq_chat
    import asyncio
    import os

    # Temporarily ensure GROQ_API_KEY is not set
    old_key = os.environ.pop("GROQ_API_KEY", None)
    try:
        assert is_groq_configured() is False
        res = asyncio.run(call_groq_chat([{"role": "user", "content": "Hello"}]))
        assert res is None
    finally:
        if old_key:
            os.environ["GROQ_API_KEY"] = old_key


def test_groq_service_mocked_tool_calling(monkeypatch):
    import asyncio
    from unittest.mock import AsyncMock
    from backend.app.agents import admissions_agent

    # Mock call_groq_chat to simulate Groq tool calling
    mock_groq = AsyncMock()
    # Turn 1: model requests tool_query_campuses
    turn1 = {
        "text": "",
        "tool_calls": [
            {
                "id": "call_123",
                "function": {
                    "name": "tool_query_campuses",
                    "arguments": json.dumps({"state": "Telangana", "budget_max": 350000}),
                },
            }
        ],
        "model": "llama-3.3-70b-versatile",
        "finish_reason": "tool_calls",
        "raw_message": {"role": "assistant", "tool_calls": []},
    }
    # Turn 2: model synthesizes final answer grounded in tool output
    turn2 = {
        "text": "Based on verified university data, NIAT @ Chaitanya University offers UGC-recognized degrees.",
        "tool_calls": [],
        "model": "llama-3.3-70b-versatile",
        "finish_reason": "stop",
    }
    mock_groq.side_effect = [turn1, turn2]

    monkeypatch.setattr(admissions_agent, "call_groq_chat", mock_groq)
    monkeypatch.setattr(admissions_agent, "is_groq_configured", lambda: True)

    body = AgentRequestBody(
        prompt="Which campus is best in Telangana?",
        language="en",
        objectionCategory="campus_matching",
        studentProfile=StudentProfile(studentName="Rahul", state="Telangana"),
    )
    res = asyncio.run(admissions_agent.process_admissions_question(body))

    assert res.success is True
    assert res.provider == "groq"
    assert res.executionMode == "live_ai"
    assert "Chaitanya University" in res.agentResponse
    assert any(t.toolName == "tool_query_campuses" for t in res.executedTools)
    assert any(t.toolName == "tool_generate_dossier" for t in res.executedTools)


def test_groq_service_direct_reasoning(monkeypatch):
    import asyncio
    from unittest.mock import AsyncMock
    from backend.app.agents import admissions_agent

    mock_groq = AsyncMock()
    mock_groq.return_value = {
        "text": "Every NIAT student receives a formal UGC-recognized degree from our host university.",
        "tool_calls": [],
        "model": "llama-3.3-70b-versatile",
        "finish_reason": "stop",
    }

    monkeypatch.setattr(admissions_agent, "call_groq_chat", mock_groq)
    monkeypatch.setattr(admissions_agent, "is_groq_configured", lambda: True)

    body = AgentRequestBody(
        prompt="Is the degree genuine?",
        language="en",
        objectionCategory="accreditation",
    )
    res = asyncio.run(admissions_agent.process_admissions_question(body))

    assert res.success is True
    assert res.provider == "groq"
    assert "UGC-recognized" in res.agentResponse
