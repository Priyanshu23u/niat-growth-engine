"""
Pydantic Schemas for AI Admissions Agent
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class StudentProfile(BaseModel):
    name: Optional[str] = "Student Aspirant"
    studentName: Optional[str] = None
    parentName: Optional[str] = "Respected Parent"
    parentPhone: Optional[str] = "+91 98480 23456"
    boardPercentage: Optional[int] = 82
    natScore: Optional[int] = 75
    state: Optional[str] = "Telangana"
    budgetAnnual: Optional[int] = 320000


class AgentRequestBody(BaseModel):
    prompt: str = Field(..., description="Parent question or objection prompt")
    language: Optional[str] = Field("en", description="Target language code: en, te, ta, hi, kn, ml")
    studentProfile: Optional[StudentProfile] = None
    objectionCategory: Optional[str] = Field("custom", description="Category: accreditation, ai_threat, roi_financial, campus_matching, custom")


class ToolExecutionRecord(BaseModel):
    toolName: str
    input: Dict[str, Any]
    outputSummary: str
    timestamp: str


class AgentResponseBody(BaseModel):
    success: bool
    agentResponse: str
    aiModelUsed: str
    provider: Optional[str] = "fallback"
    executionMode: Optional[str] = "deterministic_fallback"
    language: str
    executedTools: List[ToolExecutionRecord]
    primaryCampus: Dict[str, Any]
    matchedCampusesCount: int
    roiMetrics: Dict[str, Any]
    dossierData: Dict[str, Any]
