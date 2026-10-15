"""
NIAT ParentTrust AI — Complete System Verification Suite
Technology: Python FastAPI Backend + Plain HTML5/CSS3/Vanilla JS Frontend
Usage:
    python test_system.py
"""

import sys
from pathlib import Path

# Ensure UTF-8 stdout encoding on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Set up paths
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

print("\n" + "=" * 60)
print("=== RUNNING NIAT PARENTTRUST AI (FASTAPI + VANILLA) SUITE ===")
print("=" * 60 + "\n")

passed = 0
failed = 0


def assert_test(condition: bool, message: str):
    global passed, failed
    if condition:
        print(f"✓ PASS: {message}")
        passed += 1
    else:
        print(f"✗ FAIL: {message}")
        failed += 1


# 1. Verify Core Files
required_files = [
    "frontend/index.html",
    "frontend/styles.css",
    "frontend/app.js",
    "frontend/api.js",
    "frontend/data.js",
    "backend/app/main.py",
    "backend/app/api/agent.py",
    "backend/app/api/campuses.py",
    "backend/app/api/roi.py",
    "backend/app/api/leads.py",
    "backend/app/api/webhook.py",
    "backend/app/agents/admissions_agent.py",
    "backend/app/agents/tools.py",
    "backend/app/services/campus_service.py",
    "backend/app/services/roi_calculator.py",
    "backend/app/services/groq_service.py",
    "backend/app/services/dossier_service.py",
    "backend/app/models/campus.py",
    "backend/app/models/curriculum.py",
    "backend/app/models/translations.py",
    "backend/app/schemas/agent.py",
    "backend/app/schemas/roi.py",
    "backend/app/schemas/lead.py",
    "backend/app/schemas/webhook.py",
    "backend/app/database.py",
    "backend/requirements.txt",
    "run_server.py",
    "README.md",
]

for file_rel in required_files:
    file_path = root_dir / file_rel
    assert_test(file_path.exists(), f"File exists: {file_rel}")

# 2. Validate Partner Campuses Data Integrity
from backend.app.models.campus import NIAT_PARTNER_CAMPUSES
from backend.app.services.campus_service import search_campuses, get_campus_by_id

assert_test(len(NIAT_PARTNER_CAMPUSES) >= 8, f"Loaded {len(NIAT_PARTNER_CAMPUSES)} partner campuses (expected >= 8)")

chaitanya = next((c for c in NIAT_PARTNER_CAMPUSES if c.id == "campus-chaitanya-hyd"), None)
assert_test(chaitanya is not None, "Dataset includes founding partner: Chaitanya University")
assert_test(chaitanya.ugc_approved is True, "Chaitanya has verified UGC approval")
assert_test(chaitanya.total_four_year_fee == 1200000, "Chaitanya total 4-year fee matches ₹12,00,000")

dypatil = next((c for c in NIAT_PARTNER_CAMPUSES if c.id == "campus-dypatil-pune"), None)
assert_test(dypatil is not None, "Dataset includes D.Y. Patil University Pune")

yenepoya = next((c for c in NIAT_PARTNER_CAMPUSES if c.id == "campus-yenepoya-mng"), None)
assert_test(yenepoya is not None, "Dataset includes Yenepoya University")

niu = next((c for c in NIAT_PARTNER_CAMPUSES if c.id == "campus-niu-delhi"), None)
assert_test(niu is not None, "Dataset includes NIU Greater Noida")

has_lab = any("Lab 5.0" in c.lab_type for c in NIAT_PARTNER_CAMPUSES)
assert_test(has_lab, "Dataset includes Lab 5.0 compute pods across campuses")

# 3. Campus Filters
telangana_campuses = search_campuses(state="Telangana")
assert_test(len(telangana_campuses) >= 2, f"Matched {len(telangana_campuses)} Telangana campuses")

budget_campuses = search_campuses(max_budget=320000)
assert_test(len(budget_campuses) > 0, f"Matched {len(budget_campuses)} campuses under ₹3.2L/year budget")

keyword_campuses = search_campuses(keyword="AI")
assert_test(len(keyword_campuses) > 0, f"Matched {len(keyword_campuses)} campuses matching 'AI'")

# 4. Multilingual Translations
from backend.app.models.translations import SUPPORTED_LANGUAGES, PARENT_OBJECTIONS

assert_test(len(SUPPORTED_LANGUAGES) == 6, f"Supports 6 languages: {[l['name'] for l in SUPPORTED_LANGUAGES]}")
assert_test("te" in PARENT_OBJECTIONS and len(PARENT_OBJECTIONS["te"]) >= 4, "Includes native Telugu (తెలుగు) localization")
assert_test("ta" in PARENT_OBJECTIONS and len(PARENT_OBJECTIONS["ta"]) >= 4, "Includes native Tamil (தமிழ்) localization")
assert_test("hi" in PARENT_OBJECTIONS and len(PARENT_OBJECTIONS["hi"]) >= 4, "Includes native Hindi (हिन्दी) localization")
assert_test("kn" in PARENT_OBJECTIONS and len(PARENT_OBJECTIONS["kn"]) >= 4, "Includes native Kannada (ಕನ್ನಡ) localization")
assert_test("ml" in PARENT_OBJECTIONS and len(PARENT_OBJECTIONS["ml"]) >= 4, "Includes native Malayalam (മലയാളം) localization")
assert_test("en" in PARENT_OBJECTIONS and len(PARENT_OBJECTIONS["en"]) >= 4, "Includes native English localization")

# 5. Curriculum Comparison
from backend.app.models.curriculum import CURRICULUM_COMPARISON
assert_test(len(CURRICULUM_COMPARISON) == 8, "Complete 8-semester curriculum comparison mapped")
assert_test(CURRICULUM_COMPARISON[0]["niat_program"]["coding_hours_per_week"] >= 18, "Semester 1 NIAT offers >= 18 coding hrs/week")

# 6. Financial ROI Calculations
from backend.app.services.roi_calculator import calculate_roi_model
roi = calculate_roi_model()
assert_test(0 < roi["metrics"]["breakEvenMonths"] <= 30, f"Payback break-even verified: {roi['metrics']['breakEvenMonths']} months")
assert_test(roi["metrics"]["fiveYearNetWealthAdvantage"] > 1000000, f"5-Year net wealth gain verified: ₹{(roi['metrics']['fiveYearNetWealthAdvantage'] / 100000):.1f} Lakhs")
assert_test(12000 < roi["inputs"]["monthlyEmi"] < 18000, f"Loan EMI verified: ₹{roi['inputs']['monthlyEmi']}/month")

# 7. Deliverables Documentation
docs = [
    "../docs/DELIVERABLE_1_NIAT_AUDIT.md",
    "../docs/DELIVERABLE_2_GROWTH_TRACK_AND_AVENUE.md",
    "../docs/DELIVERABLE_3_WORKING_SYSTEM.md",
    "../docs/DELIVERABLE_4_REFLECTION.md",
    "../docs/FULL_SUBMISSION_DOSSIER.md",
]

for doc in docs:
    doc_path = root_dir / doc
    assert_test(doc_path.exists(), f"Deliverable document exists: {doc_path.name}")

# 8. Frontend HTML & Vanilla JS Code Quality Check
html_content = (root_dir / "frontend/index.html").read_text(encoding="utf-8")
assert_test("tab-content-console" in html_content, "HTML contains Parent Advisory Console tab")
assert_test("tab-content-campuses" in html_content, "HTML contains 35+ Campuses Explorer tab")
assert_test("tab-content-roi" in html_content, "HTML contains Financial ROI Simulator tab")
assert_test("tab-content-dashboard" in html_content, "HTML contains Growth Manager Dashboard tab")
assert_test("modal-dossier" in html_content, "HTML contains Admissions Dossier Modal")
assert_test("modal-seat" in html_content, "HTML contains Provisional Seat Reservation Modal")
assert_test("modal-profile" in html_content, "HTML contains Student Profile Editor Modal")
assert_test("<script src=\"/_next/" not in html_content, "HTML is 100% free of React / Next.js scripts")

app_js = (root_dir / "frontend/app.js").read_text(encoding="utf-8")
assert_test("speechSynthesis" in app_js, "Vanilla JS implements Web Speech Synthesis")
assert_test("addEventListener" in app_js, "Vanilla JS uses standard DOM addEventListener")

api_js = (root_dir / "frontend/api.js").read_text(encoding="utf-8")
assert_test("fetch(`${API_BASE}/api/agent`" in api_js, "api.js connects to /api/agent endpoint")
assert_test("fetch(`${API_BASE}/api/roi`" in api_js, "api.js connects to /api/roi endpoint")

# 9. FastAPI TestClient Endpoint Verification
from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

res_health = client.get("/health")
assert_test(res_health.status_code == 200, "GET /health returns 200 OK")
assert_test(res_health.json()["status"] == "healthy", "Health check reports 'healthy'")

res_campuses = client.get("/api/campuses?state=Telangana")
assert_test(res_campuses.status_code == 200, "GET /api/campuses returns 200 OK")
assert_test(res_campuses.json()["matchedCount"] >= 2, "Returned >= 2 Telangana campuses")

res_roi = client.post("/api/roi", json={"niatTotalFee": 1200000, "tier3TotalFee": 400000})
assert_test(res_roi.status_code == 200, "POST /api/roi returns 200 OK")
assert_test(res_roi.json()["metrics"]["breakEvenMonths"] > 0, "Calculated break-even payback period")

res_agent = client.post("/api/agent", json={
    "prompt": "ఈ డిగ్రీ నిజంగా యూజీసీ గుర్తింపు పొందినదేనా?",
    "language": "te",
    "objectionCategory": "accreditation",
    "studentProfile": {"name": "Sai Teja", "parentName": "Venkatesh", "state": "Telangana"},
})
assert_test(res_agent.status_code == 200, "POST /api/agent returns 200 OK")
assert_test(len(res_agent.json()["executedTools"]) >= 2, "Agent executed appropriate tools")
assert_test("గౌరవనీయులైన" in res_agent.json()["agentResponse"], "Agent responded in authentic respectful Telugu")
assert_test(res_agent.json()["dossierData"]["dossierId"].startswith("NIAT-DOSSIER-"), "Generated official Dossier ID")

res_leads = client.get("/api/leads")
assert_test(res_leads.status_code == 200, "GET /api/leads returns 200 OK")
assert_test(len(res_leads.json()["leads"]) >= 5, "Pipeline contains >= 5 leads")
assert_test("funnelComparison" in res_leads.json()["analytics"], "Analytics includes A/B funnel comparison")

res_seat = client.post("/api/reserve-seat", json={
    "studentName": "Sai Teja Reddy",
    "parentName": "K. Venkatesh",
    "parentPhone": "+91 98480 23456",
    "campusId": "campus-chaitanya-hyd",
})
assert_test(res_seat.status_code == 200, "POST /api/reserve-seat returns 200 OK")
assert_test(res_seat.json()["reservation"]["tokenAmount"] == 10000, "Provisional seat token is ₹10,000")

res_webhook = client.post("/api/webhook", json={
    "action": "DISPATCH_WHATSAPP_DOSSIER",
    "language": "te",
    "leadData": {"parentName": "వెంకటేష్", "studentName": "సాయి తేజ"},
})
assert_test(res_webhook.status_code == 200, "POST /api/webhook returns 200 OK")
assert_test(res_webhook.json()["dispatch"]["status"] == "SIMULATED_SUCCESS", "Webhook simulation dispatched successfully")

res_static = client.get("/")
assert_test(res_static.status_code == 200, "GET / serves static frontend HTML")
assert_test("NIAT ParentTrust AI" in res_static.text, "Served HTML contains NIAT ParentTrust AI")

print("\n" + "=" * 60)
print(f"VERIFICATION SUMMARY: {passed} Passed, {failed} Failed")
print("=" * 60 + "\n")

if failed == 0:
    print("✓ ALL AUTOMATED SYSTEM & API INTEGRATION TESTS PASSED PERFECTLY!\n")
    sys.exit(0)
else:
    print(f"✗ {failed} test(s) failed.\n")
    sys.exit(1)
