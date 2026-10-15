"""
Admissions Agent — Autonomous Multilingual Admissions Advisory & Closer
Orchestrates genuine tool-calling via Groq (Llama 3.3 / Llama 3.1) with
an authentic multilingual deterministic fallback engine when API credentials are absent.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from backend.app.schemas.agent import AgentRequestBody, AgentResponseBody, ToolExecutionRecord
from backend.app.agents.tools import (
    tool_query_campuses,
    tool_calculate_roi,
    tool_compare_curriculum,
    tool_generate_dossier,
)
from backend.app.services.groq_service import call_groq_chat, is_groq_configured, get_groq_model

logger = logging.getLogger("admissions_agent")

# OpenAI-compatible tool specifications for Groq function calling
GROQ_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "tool_query_campuses",
            "description": "Query and rank NIAT partner university campuses based on state, annual budget, and student NAT percentile.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "description": "Indian state preference (e.g. Telangana, Andhra Pradesh, Maharashtra, Karnataka, Tamil Nadu, Uttar Pradesh, Kerala)",
                    },
                    "budget_max": {
                        "type": "integer",
                        "description": "Maximum annual tuition budget in INR (e.g. 300000)",
                    },
                    "min_nat_score": {
                        "type": "integer",
                        "description": "Minimum NAT exam percentile (0-100)",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_calculate_roi",
            "description": "Compute 5-year post-tax financial ROI, monthly loan EMI, and break-even payback period comparing NIAT against traditional tier-3 colleges.",
            "parameters": {
                "type": "object",
                "properties": {
                    "niat_fee": {
                        "type": "integer",
                        "description": "Total 4-year NIAT program fee in INR (e.g. 1200000)",
                    },
                    "tier3_fee": {
                        "type": "integer",
                        "description": "Total 4-year tier-3 college fee in INR (default 400000)",
                    },
                    "starting_salary": {
                        "type": "integer",
                        "description": "Expected NIAT starting salary in INR (default 850000)",
                    },
                },
                "required": ["niat_fee"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_compare_curriculum",
            "description": "Compare 8-semester curriculum of NIAT (applied GenAI, autonomous agents, Lab 5.0) against traditional tier-3 university theory syllabus.",
            "parameters": {
                "type": "object",
                "properties": {
                    "focus_areas": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Focus areas to compare, e.g. ['AI_Threat', 'Coding_Hours', 'Accreditation']",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tool_generate_dossier",
            "description": "Generate the verified personalized NIAT Family Admissions Dossier with accreditation, fee schedule, and provisional seat token.",
            "parameters": {
                "type": "object",
                "properties": {
                    "student_name": {"type": "string", "description": "Student full name"},
                    "parent_name": {"type": "string", "description": "Parent full name"},
                    "language": {"type": "string", "description": "Language code (en, te, ta, hi, kn, ml)"},
                },
            },
        },
    },
]

ALLOWED_TOOL_NAMES = {
    "tool_query_campuses",
    "tool_calculate_roi",
    "tool_compare_curriculum",
    "tool_generate_dossier",
}


async def process_admissions_question(body: AgentRequestBody) -> AgentResponseBody:
    """
    Executes the autonomous admissions advisory workflow:
    1. If Groq API key is present: sends prompt + profile to Groq with native tool-calling.
       Validates and executes requested tools on the server, feeds back tool results,
       and lets Groq synthesize the final authoritative multilingual advice.
    2. If Groq API key is absent or API fails: executes only the relevant tools based on
       the objection category and synthesizes authentic vernacular responses.
    """
    profile = body.studentProfile
    student_name = (profile.studentName or profile.name or "Student Aspirant") if profile else "Student Aspirant"
    parent_name = profile.parentName if profile and profile.parentName else "Respected Parent"
    nat_score = profile.natScore if profile and profile.natScore else 75
    board_percentage = profile.boardPercentage if profile and profile.boardPercentage else 82
    state = profile.state if profile and profile.state else "Telangana"
    budget = profile.budgetAnnual if profile and profile.budgetAnnual else 320000

    language = body.language or "en"
    objection_category = body.objectionCategory or "custom"
    prompt = body.prompt

    # Baseline primary campus and ROI data to ensure UI integrity
    campuses_result = tool_query_campuses(state=state, budget_max=budget, min_nat_score=nat_score)
    primary_campus = campuses_result["primary_campus"]
    matched_campuses = campuses_result["matched_campuses"]

    roi_result = tool_calculate_roi(niat_fee=primary_campus.total_four_year_fee)
    roi_model = roi_result["roi_model"]

    executed_tools: List[ToolExecutionRecord] = []
    agent_response_text: str = ""
    ai_model_used: str = "Deterministic Multi-Tool Engine (Standby Mode)"
    provider: str = "fallback"
    execution_mode: str = "deterministic_fallback"

    # ─────────────────────────────────────────────────────────────
    # PATH A: LIVE GROQ MODEL INFERENCE (Native Tool-Calling)
    # ─────────────────────────────────────────────────────────────
    if is_groq_configured():
        model_name = get_groq_model()
        system_prompt = f"""You are the Senior NIAT Admissions & Parent Trust Advisory Agent.
You are conversing with {parent_name}, parent of prospective student {student_name}.
Student Academic Profile: Class 12: {board_percentage}%, NAT Percentile: {nat_score}%, State: {state}, Budget: ₹{budget}/year.
Primary Recommended Campus: {primary_campus.name} ({primary_campus.city}, {primary_campus.state}).
Accreditation: {primary_campus.accreditation}, Degree: {primary_campus.degree_awarded}.

You have access to 4 approved server tools:
- tool_query_campuses: search partner universities
- tool_calculate_roi: compute 5-year wealth advantage and loan EMI
- tool_compare_curriculum: analyze curriculum differences vs legacy engineering
- tool_generate_dossier: generate official admissions dossier

INSTRUCTIONS:
1. Call ONLY the tools that are genuinely required to answer the parent's specific question.
2. Respond strictly in the parent's requested language code: "{language}" (te=Telugu, ta=Tamil, hi=Hindi, kn=Kannada, ml=Malayalam, en=English).
3. Be reassuring, factual, respectful, and transparent. Do not invent unapproved degrees or partner institutions."""

        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f'Parent Question / Objection: "{prompt}" (Category: {objection_category})'},
        ]

        initial_res = await call_groq_chat(
            messages=messages,
            tools=GROQ_TOOLS,
            tool_choice="auto",
            model=model_name,
        )

        if initial_res:
            tool_calls = initial_res.get("tool_calls", [])

            if tool_calls:
                # Groq requested one or more tool executions
                messages.append(initial_res["raw_message"])

                for tc in tool_calls:
                    fn_name = tc.get("function", {}).get("name", "")
                    if fn_name not in ALLOWED_TOOL_NAMES:
                        logger.warning(f"Rejected unapproved tool call from model: {fn_name}")
                        continue

                    raw_args = tc.get("function", {}).get("arguments", "{}")
                    try:
                        args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                    except Exception:
                        args = {}

                    tool_output_summary = ""

                    if fn_name == "tool_query_campuses":
                        q_state = str(args.get("state", state))[:50]
                        q_budget = min(max(int(args.get("budget_max", budget)), 100000), 2000000)
                        q_nat = min(max(int(args.get("min_nat_score", nat_score)), 0), 100)
                        res = tool_query_campuses(state=q_state, budget_max=q_budget, min_nat_score=q_nat)
                        primary_campus = res["primary_campus"]
                        matched_campuses = res["matched_campuses"]
                        executed_tools.append(res["record"])
                        tool_output_summary = res["record"].outputSummary

                    elif fn_name == "tool_calculate_roi":
                        n_fee = min(max(int(args.get("niat_fee", primary_campus.total_four_year_fee)), 200000), 3000000)
                        res = tool_calculate_roi(niat_fee=n_fee)
                        roi_model = res["roi_model"]
                        executed_tools.append(res["record"])
                        tool_output_summary = res["record"].outputSummary

                    elif fn_name == "tool_compare_curriculum":
                        res = tool_compare_curriculum()
                        executed_tools.append(res["record"])
                        tool_output_summary = res["record"].outputSummary

                    elif fn_name == "tool_generate_dossier":
                        res = tool_generate_dossier(
                            student_name=student_name,
                            parent_name=parent_name,
                            primary_campus=primary_campus,
                            roi_model=roi_model,
                            language=language,
                        )
                        executed_tools.append(res["record"])
                        tool_output_summary = res["record"].outputSummary

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.get("id", f"call_{fn_name}"),
                        "name": fn_name,
                        "content": json.dumps({"status": "success", "summary": tool_output_summary}),
                    })

                # Second turn: Groq synthesizes final response based on tool results
                final_res = await call_groq_chat(
                    messages=messages,
                    model=model_name,
                )

                if final_res and final_res.get("text"):
                    agent_response_text = final_res["text"]
                    ai_model_used = f"Groq {final_res.get('model', model_name)} (Autonomous Tool-Calling)"
                    provider = "groq"
                    execution_mode = "live_ai"
                else:
                    # Groq returned empty synthesis — fall through to deterministic fallback
                    logger.warning("[Agent] Groq second-turn returned empty text; using deterministic fallback.")

            elif initial_res.get("text"):
                # Model directly answered without calling tools
                agent_response_text = initial_res["text"]
                ai_model_used = f"Groq {initial_res.get('model', model_name)} (Direct Reasoning)"
                provider = "groq"
                execution_mode = "live_ai"
            else:
                # Groq returned neither tool calls nor text — fall through to deterministic fallback
                logger.warning("[Agent] Groq initial response was empty (no text, no tool_calls); using deterministic fallback.")

    # ─────────────────────────────────────────────────────────────
    # PATH B: AUTHENTIC DETERMINISTIC MULTI-TOOL FALLBACK
    # ─────────────────────────────────────────────────────────────
    if not agent_response_text:
        # Deliberately select and execute only the tools relevant to the objection category
        if objection_category == "campus_matching":
            executed_tools = [campuses_result["record"], roi_result["record"]]
        elif objection_category == "roi_financial":
            executed_tools = [roi_result["record"], campuses_result["record"]]
        elif objection_category in ("accreditation", "ai_threat"):
            curr_res = tool_compare_curriculum()
            executed_tools = [campuses_result["record"], curr_res["record"]]
        else:
            # Multi-tool comprehensive consultation
            curr_res = tool_compare_curriculum()
            executed_tools = [campuses_result["record"], roi_result["record"], curr_res["record"]]

        agent_response_text = generate_multilingual_fallback(
            language=language,
            objection_category=objection_category,
            parent_name=parent_name,
            student_name=student_name,
            primary_campus=primary_campus,
            roi_model=roi_model,
        )
        ai_model_used = "Deterministic Multi-Tool Engine (Standby Mode)"
        provider = "fallback"
        execution_mode = "deterministic_fallback"

    # Always ensure the official Admissions Dossier tool is executed for complete client modal rendering
    dossier_res = tool_generate_dossier(
        student_name=student_name,
        parent_name=parent_name,
        primary_campus=primary_campus,
        roi_model=roi_model,
        language=language,
    )
    dossier_data = dossier_res["dossier"]
    if not any(t.toolName == "tool_generate_dossier" for t in executed_tools):
        executed_tools.append(dossier_res["record"])

    return AgentResponseBody(
        success=True,
        agentResponse=agent_response_text,
        aiModelUsed=ai_model_used,
        provider=provider,
        executionMode=execution_mode,
        language=language,
        executedTools=executed_tools,
        primaryCampus=primary_campus.model_dump(),
        matchedCampusesCount=len(matched_campuses),
        roiMetrics=roi_model["metrics"],
        dossierData=dossier_data,
    )


def generate_multilingual_fallback(
    language: str,
    objection_category: str,
    parent_name: str,
    student_name: str,
    primary_campus: Any,
    roi_model: Dict[str, Any],
) -> str:
    """Provides culturally authentic, empathetic native responses for reliable fallback."""
    wealth_lakhs = f"{(roi_model['metrics']['fiveYearNetWealthAdvantage'] / 100000):.1f}"
    annual_fee_lakhs = f"{(primary_campus.total_annual_fee / 100000):.2f}"
    four_year_fee_lakhs = f"{(primary_campus.total_four_year_fee / 100000):.1f}"
    break_even = roi_model['metrics']['breakEvenMonths']

    if language == "te":
        if objection_category == "accreditation":
            return f"""గౌరవనీయులైన {parent_name} గారికి నమస్కారం,
మీ ఆందోళన చాలా సమంజసమైనది. NIAT (ఎన్ఐఏటీ) కేవలం ప్రైవేట్ కోచింగ్ ఇన్స్టిట్యూట్ కాదు. {student_name} కు లభించే బి.టెక్ (B.Tech) డిగ్రీ యూజీసీ (UGC) గుర్తింపు పొందిన మా భాగస్వామ్య విశ్వవిద్యాలయం ({primary_campus.university_name}) ద్వారా నేరుగా జారీ చేయబడుతుంది. దీనితో పాటు కేంద్ర ప్రభుత్వ నైపుణ్యాభివృద్ధి సంస్థ (NSDC) మరియు NxtWave సంయుక్త పరిశ్రమ ధృవీకరణ పత్రం కూడా లభిస్తుంది. కాబట్టి ప్రభుత్వ ఉద్యోగాలకు, ఉన్నత విద్యకు (M.Tech/MS) మరియు ఎంఎన్సీ ఉద్యోగాలకు ఈ డిగ్రీ 100% పూర్తిగా చెల్లుబాటు అవుతుంది."""
        if objection_category == "ai_threat":
            return f"""గౌరవనీయులైన {parent_name} గారు,
ఆర్టిఫిషియల్ ఇంటెలిజెన్స్ (AI) కేవలం పాతకాలపు బట్టీ పట్టే కోడింగ్ ఉద్యోగాలనే తీసివేస్తుంది, కానీ ఆధునిక AI ఇంజనీర్లకు డిమాండ్ 300% పెరిగింది. సాధారణ కాలేజీలు ఇంకా 25 ఏళ్ల నాటి సిలబస్ బోధిస్తుండగా, ఎన్ఐఏటీ మొదటి సంవత్సరం నుండే అత్యాధునిక AI ఏజెంట్లు, LLM సిస్టమ్స్ మరియు పూర్తి స్థాయి సాఫ్ట్‌వేర్ బిల్డింగ్ నేర్పిస్తుంది. {student_name} AI ని సమర్థవంతంగా నియంత్రించే ఒక ఇంజనీర్‌గా ఎదుగుతారు, కాబట్టి 2028 నాటికి వీరి కెరీర్ అత్యున్నత భద్రతతో ఉంటుంది."""
        return f"""గౌరవనీయులైన {parent_name} గారు,
మీ విద్యార్థి {student_name} కోసం మేము {primary_campus.name} ({primary_campus.city}) క్యాంపస్‌ను సూచిస్తున్నాము. ఇక్కడ వార్షిక ఫీజు సుమారు ₹{annual_fee_lakhs} లక్షలు. సాధారణ కాలేజీలతో పోలిస్తే 5 ఏళ్లలో అదనంగా ₹{wealth_lakhs} లక్షల నికర ఆర్థిక లాభం లభిస్తుంది. కేవలం {break_even} నెలల్లో మీ మొత్తం విద్యా వ్యయం తిరిగి వస్తుంది."""

    if language == "ta":
        if objection_category == "accreditation":
            return f"""மதிப்பிற்குரிய {parent_name} அவர்களுக்கு வணக்கம்,
உங்கள் சந்தேகம் முற்றிலும் நியாயமானது. NIAT என்பது வெறும் பயிற்சி மையம் அல்ல. {student_name} பெறவிருக்கும் B.Tech பட்டம் UGC மற்றும் AICTE ஆல் அங்கீகரிக்கப்பட்ட எங்கள் கூட்டாண்மை பல்கலைக்கழகத்தால் ({primary_campus.university_name}) அதிகாரப்பூர்வமாக வழங்கப்படும். இதனுடன் NSDC மற்றும் NxtWave இணைந்து வழங்கும் தொழில்முறை சான்றிதழும் கிடைக்கும். இது அரசுப் பணிகள், உயர்கல்வி (MS/M.Tech) மற்றும் உலகளாவிய நிறுவனங்களின் வேலைவாய்ப்புகளுக்கு 100% செல்லுபடியாகும்."""
        return f"""மதிப்பிற்குரிய {parent_name} அவர்களுக்கு,
{student_name} க்காக நாங்கள் {primary_campus.name} வளாகத்தை பரிந்துரைக்கிறோம். இங்கு ஆண்டுக்கு நடைமுறை பொறியியல் கட்டணம் ₹{annual_fee_lakhs} லட்சம். சாதாரண கல்லூரிகளை விட 5 ஆண்டுகளில் ₹{wealth_lakhs} லட்சம் கூடுதல் வருவாய் ஈட்ட முடியும். முதலீட்டை வெறும் {break_even} மாதங்களில் திரும்பப் பெற முடியும்."""

    if language == "hi":
        if objection_category == "accreditation":
            return f"""आदरणीय {parent_name} जी,
आपकी चिंता पूरी तरह स्वाभाविक है। NIAT कोई अनधिकृत प्राइवेट कोचिंग नहीं है। {student_name} को 4 साल की औपचारिक B.Tech डिग्री UGC और AICTE से मान्यता प्राप्त विश्वविद्यालय ({primary_campus.university_name}) द्वारा ही प्रदान की जाएगी। इसके साथ भारत सरकार के NSDC और NxtWave का इंडस्ट्री-रेडी सर्टिफिकेट भी मिलेगा। यह डिग्री सरकारी नौकरियों, गेट (GATE), विदेश में MS और शीर्ष टेक कंपनियों में 100% मान्य है।"""
        if objection_category == "ai_threat":
            return f"""आदरणीय {parent_name} जी,
AI पुरानी और रट्टामार कोडिंग वाली नौकरियों को प्रभावित कर रहा है, लेकिन AI-नेटिव डेवलपर्स की मांग कई गुना बढ़ गई है। पारंपरिक कॉलेज 1990 का पाठ्यक्रम पढ़ाते हैं, जबकि NIAT में छात्र Day 1 से आधुनिक AI टूल्स, LLMs और क्लाउड आर्किटेक्चर सीखते हैं। 2028 में जब {student_name} पास होंगे, वे AI से विस्थापित होने वाले नहीं, बल्कि AI सिस्टम्स को लीड करने वाले टॉप 5% इंजीनियर्स में होंगे।"""
        return f"""आदरणीय {parent_name} जी,
{student_name} के प्रोफाइल के आधार पर हमने {primary_campus.name} ({primary_campus.city}) को शॉर्टलिस्ट किया है। 5 वर्षों में टियर-3 कॉलेज की तुलना में लगभग ₹{wealth_lakhs} लाख का शुद्ध अतिरिक्त वित्तीय लाभ होगा, और मात्र {break_even} महीनों में शिक्षा की पूरी लागत वसूल हो जाएगी।"""

    if language == "kn":
        if objection_category == "accreditation":
            return f"""ಗೌರವಾನ್ವಿತ {parent_name} ಅವರಿಗೆ ನಮಸ್ಕಾರ,
ನಿಮ್ಮ ಚಿಂತೆ ಸಂಪೂರ್ಣ ಸರಿಯಾಗಿದೆ. NIAT ಕೇವಲ ಖಾಸಗಿ ತರಬೇತಿ ಸಂಸ್ಥೆ ಅಲ್ಲ. {student_name} ಪಡೆಯಲಿರುವ B.Tech ಪದವಿ UGC ಮತ್ತು AICTE ಮಾನ್ಯತೆ ಪಡೆದ ನಮ್ಮ ಸಹಭಾಗಿತ್ವದ ವಿಶ್ವವಿದ್ಯಾಲಯ ({primary_campus.university_name}) ನೇರವಾಗಿ ನೀಡುತ್ತದೆ."""
        return f"""ಗೌರವಾನ್ವಿತ {parent_name} ಅವರಿಗೆ,
{student_name} ಗಾಗಿ ನಾವು {primary_campus.name} ({primary_campus.city}) ಶಿಫಾರಸು ಮಾಡುತ್ತೇವೆ. ಇಲ್ಲಿ ವಾರ್ಷಿಕ ಶುಲ್ಕ ₹{annual_fee_lakhs} ಲಕ್ಷ. 5 ವರ್ಷಗಳಲ್ಲಿ ₹{wealth_lakhs} ಲಕ್ಷ ಹೆಚ್ಚುವರಿ ಆರ್ಥಿಕ ಲಾಭ ಮತ್ತು ಕೇವಲ {break_even} ತಿಂಗಳಲ್ಲಿ ಸಂಪೂರ್ಣ ಶಿಕ್ಷಣ ವೆಚ್ಚ ಮರುಪಾವತಿ."""

    if language == "ml":
        if objection_category == "accreditation":
            return f"""ബഹുമാനപ്പെട്ട {parent_name},
NIAT ഒരു സ്വകാര്യ കോച്ചിംഗ് മാത്രമല്ല. {student_name} ക്ക് ലഭിക്കുന്ന B.Tech ബിരുദം UGC, AICTE അംഗീകൃത ഞങ്ങളുടെ പങ്കാളിത്ത സർവകലാശാലയായ {primary_campus.university_name} നൽകുന്നു. NSDC-NxtWave ഇൻഡസ്ട്രി സർട്ടിഫിക്കറ്റും ലഭിക്കും."""
        return f"""ബഹുമാനപ്പെട്ട {parent_name},
{student_name} ന് {primary_campus.name} ({primary_campus.city}) ശുപാർശ ചെയ്യുന്നു. 5 വർഷത്തിൽ ₹{wealth_lakhs} ലക്ഷം അധിക വരുമാനം, {break_even} മാസത്തിൽ മൊത്തം ഫീസ് തിരിച്ചു കിട്ടും."""

    # Default English response
    return f"""Dear {parent_name},

Thank you for raising this critical question regarding {student_name}'s career and undergraduate education.

1. **UGC & AICTE Accreditation:** The 4-year B.Tech degree in Computer Science & Engineering is awarded directly by our UGC-recognized host university ({primary_campus.university_name}, {primary_campus.accreditation}). Alongside the official degree, {student_name} earns an NSDC-recognized Industry-Ready Certificate from NxtWave. This degree carries full legal validity for UPSC, government exams, GATE, higher studies abroad (MS), and top multinational companies.

2. **The AI Disruption Reality:** AI is eliminating obsolete syntax typists, but demand for engineers who build and deploy AI systems has surged. While typical engineering colleges still teach legacy theory, NIAT provides 18–30 hours/week of hands-on coding in modern GenAI, microservices, and autonomous agents inside our on-campus "Lab 5.0" pods.

3. **Financial Return on Investment:** At {primary_campus.name}, total 4-year investment is ₹{four_year_fee_lakhs} Lakhs. Compared to a low-cost college offering ₹3.6 LPA mass-recruiter placements, NIAT graduates target starting packages of ₹8.5 to ₹14 LPA. Our financial model projects a 5-year net wealth advantage of ₹{wealth_lakhs} Lakhs, with the entire fee delta recovered in just {break_even} months.

Your personalized Family Admissions Dossier has been compiled and is ready for download below."""
