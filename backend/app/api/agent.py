"""
API Router: AI Admissions Advisory Agent
"""

from fastapi import APIRouter, HTTPException
from backend.app.schemas.agent import AgentRequestBody, AgentResponseBody
from backend.app.agents.admissions_agent import process_admissions_question

router = APIRouter(prefix="/api/agent", tags=["AI Admissions Agent"])


@router.post("", response_model=AgentResponseBody)
async def consult_agent(body: AgentRequestBody):
    """
    Executes the multi-tool autonomous AI admissions advisor.
    Queries partner campuses, computes ROI, reviews curriculum,
    and runs Gemini LLM reasoning to address parent objections.
    """
    try:
        response = await process_admissions_question(body)
        return response
    except Exception as e:
        print(f"[Agent Endpoint Error]: {e}")
        raise HTTPException(status_code=500, detail="Internal Agent Execution Failed")
