"""
API Router: WhatsApp Cloud API Nurture Webhook Simulation
"""

import time
import random
from datetime import datetime, timezone
from fastapi import APIRouter
from backend.app.schemas.webhook import WebhookRequest, WebhookResponse, WebhookDispatch

router = APIRouter(prefix="/api/webhook", tags=["Nurture Webhook"])


@router.post("", response_model=WebhookResponse)
def dispatch_webhook(body: WebhookRequest):
    """
    Simulates or dispatches automated WhatsApp Cloud API nurture message.
    Includes personalized dossier link and 48-hour provisional seat token alert.
    """
    lead_data = body.leadData or {}
    language = body.language or "en"
    dossier_url = body.dossierUrl or "https://niatindia.com/dossier"

    parent_name = lead_data.get("parentName", "Parent")
    student_name = lead_data.get("studentName", "Student")
    phone = lead_data.get("parentPhone", "+91 98480 23456")

    whatsapp_templates = {
        "te": f"నమస్కారం {parent_name} గారికి! {student_name} కోసం ఎన్ఐఏటీ (NIAT) ధృవీకరించబడిన అడ్మిషన్ల రిపోర్ట్ మరియు పార్టనర్ యూనివర్సిటీ ఎంపికలు సిద్ధంగా ఉన్నాయి: {dossier_url}. సీట్ రిజర్వేషన్ కోసం 48 గంటల సమయం కలదు.",
        "ta": f"வணக்கம் {parent_name} அவர்களே! {student_name} மாணவருக்கான NIAT சேர்க்கை அறிக்கை மற்றும் பல்கலைக்கழக விவரங்கள் தயாராக உள்ளன: {dossier_url}. தற்காலிக சேர்க்கை முன்பதிவு செல்லுபடியாகும் காலம்: 48 மணிநேரம்.",
        "hi": f"नमस्ते {parent_name} जी! {student_name} का NIAT सत्यापित एडमिशन डोजियर एवं पार्टनर यूनिवर्सिटी रिपोर्ट तैयार है: {dossier_url}। अर्ली-बर्ड सीट रिजर्वेशन अगले 48 घंटे के लिए खुला है।",
        "kn": f"ನಮಸ್ಕಾರ {parent_name} ಅವರಿಗೆ! {student_name} ಅವರ NIAT ಪ್ರವೇಶ ವರದಿ ಮತ್ತು ಕಾಲೇಜು ವಿವರಗಳು ಸಿದ್ಧವಾಗಿವೆ: {dossier_url}. 48 ಗಂಟೆಗಳ ಕಾಲ ಸೀಟ್ ಬುಕಿಂಗ್ ಲಭ್ಯವಿದೆ.",
        "ml": f"നമസ്കാരം {parent_name}! {student_name} ഉള്ള NIAT പ്രവേശന റിപ്പോർട്ട് തയ്യാറാണ്: {dossier_url}. 48 മണിക്കൂർ നേരത്തേക്ക് സീറ്റ് റിസർവേഷൻ ലഭ്യമാണ്.",
        "en": f"Dear {parent_name}, your verified NIAT Family Admissions & Career ROI Dossier for {student_name} is ready: {dossier_url}. Early-bird seat reservation token is active for 48 hours.",
    }

    message_content = whatsapp_templates.get(language, whatsapp_templates["en"])

    dispatch = WebhookDispatch(
        id=f"WH-{str(int(time.time() * 1000))[-8:]}",
        action=body.action or "DISPATCH_WHATSAPP_DOSSIER",
        status="SIMULATED_SUCCESS",
        channel="Meta WhatsApp Cloud API (Simulated Sandbox)",
        recipient=phone,
        languageDispatched=language,
        dispatchedText=message_content,
        crmSyncStatus="LEADSQUARED_OPPORTUNITY_UPDATED",
        eventTimestamp=datetime.now(timezone.utc).isoformat(),
        deliveryEstimateSeconds=random.randint(2, 5),
    )

    return WebhookResponse(
        success=True,
        message="Automated nurture webhook dispatched successfully (Simulated Sandbox Mode)",
        dispatch=dispatch,
    )
