"""
Pydantic Schemas for WhatsApp Webhook Simulation
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class WebhookRequest(BaseModel):
    action: Optional[str] = "DISPATCH_WHATSAPP_DOSSIER"
    leadData: Optional[Dict[str, Any]] = None
    language: Optional[str] = "en"
    dossierUrl: Optional[str] = "https://niatindia.com/dossier"


class WebhookDispatch(BaseModel):
    id: str
    action: str
    status: str
    channel: str
    recipient: str
    languageDispatched: str
    dispatchedText: str
    crmSyncStatus: str
    eventTimestamp: str
    deliveryEstimateSeconds: int


class WebhookResponse(BaseModel):
    success: bool
    message: str
    dispatch: WebhookDispatch
