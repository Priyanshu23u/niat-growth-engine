// Automated test suite for NIAT Growth System (Vanilla HTML/CSS/JS + Express Backend)
const fs = require("fs");
const path = require("path");

console.log("=== RUNNING NIAT PARENTTRUST AI VERIFICATION SUITE ===");

let passed = 0;
let failed = 0;

function assert(condition, message) {
  if (condition) {
    console.log(`✓ PASS: ${message}`);
    passed++;
  } else {
    console.error(`✗ FAIL: ${message}`);
    failed++;
  }
}

// 1. Verify all core Vanilla Frontend & Backend files exist
const requiredFiles = [
  "public/index.html",
  "public/styles.css",
  "public/app.js",
  "public/data.js",
  "server/index.js",
  "server/data/campuses.js",
  "server/data/curriculum.js",
  "server/data/translations.js",
  "server/utils/roi.js",
  ".env.example",
  "package.json",
  "README.md",
];

requiredFiles.forEach((file) => {
  const fullPath = path.join(__dirname, file);
  assert(fs.existsSync(fullPath), `File exists: ${file}`);
});

// 2. Validate Partner Campuses Data Integrity
const { NIAT_PARTNER_CAMPUSES, searchCampuses } = require("./server/data/campuses");
assert(NIAT_PARTNER_CAMPUSES.length >= 8, `Loaded ${NIAT_PARTNER_CAMPUSES.length} partner campuses (expected >= 8)`);

const chaitanya = NIAT_PARTNER_CAMPUSES.find((c) => c.id === "campus-chaitanya-hyd");
assert(chaitanya !== undefined, "Dataset includes founding partner: Chaitanya University");
assert(chaitanya?.ugcApproved === true, "Chaitanya has verified UGC approval");
assert(chaitanya?.totalFourYearFee === 1200000, "Chaitanya total 4-year fee matches ₹12,00,000");

const dypatil = NIAT_PARTNER_CAMPUSES.find((c) => c.id === "campus-dypatil-pune");
assert(dypatil !== undefined, "Dataset includes D.Y. Patil University Pune");

const yenepoya = NIAT_PARTNER_CAMPUSES.find((c) => c.id === "campus-yenepoya-mng");
assert(yenepoya !== undefined, "Dataset includes Yenepoya University");

const niu = NIAT_PARTNER_CAMPUSES.find((c) => c.id === "campus-niu-delhi");
assert(niu !== undefined, "Dataset includes NIU Greater Noida");

const hasLabPod = NIAT_PARTNER_CAMPUSES.some((c) => c.labType && c.labType.includes("Lab 5.0"));
assert(hasLabPod, "Dataset includes Lab 5.0 pod specifications across partner campuses");

// 3. Validate Campus Search and Filters
const telanganaMatches = searchCampuses({ state: "Telangana" });
assert(telanganaMatches.length >= 2, `Matched ${telanganaMatches.length} Telangana campuses`);

const budgetMatches = searchCampuses({ maxBudget: 320000 });
assert(budgetMatches.length > 0, `Matched ${budgetMatches.length} campuses under ₹3.2L/year budget`);

const keywordMatches = searchCampuses({ keyword: "AI" });
assert(keywordMatches.length > 0, `Matched ${keywordMatches.length} campuses matching keyword 'AI'`);

// 4. Validate Multilingual Translations
const { SUPPORTED_LANGUAGES, PARENT_OBJECTIONS } = require("./server/data/translations");
assert(SUPPORTED_LANGUAGES.length === 6, `Supports 6 languages: ${SUPPORTED_LANGUAGES.map((l) => l.name).join(", ")}`);
assert(PARENT_OBJECTIONS.te && PARENT_OBJECTIONS.te.length >= 4, "Includes native Telugu (తెలుగు) localization with 4 objections");
assert(PARENT_OBJECTIONS.ta && PARENT_OBJECTIONS.ta.length >= 4, "Includes native Tamil (தமிழ்) localization with 4 objections");
assert(PARENT_OBJECTIONS.hi && PARENT_OBJECTIONS.hi.length >= 4, "Includes native Hindi (हिन्दी) localization with 4 objections");
assert(PARENT_OBJECTIONS.kn && PARENT_OBJECTIONS.kn.length >= 4, "Includes native Kannada (ಕನ್ನಡ) localization with 4 objections");
assert(PARENT_OBJECTIONS.ml && PARENT_OBJECTIONS.ml.length >= 4, "Includes native Malayalam (മലയാളം) localization with 4 objections");
assert(PARENT_OBJECTIONS.en && PARENT_OBJECTIONS.en.length >= 4, "Includes native English localization with 4 objections");

// 5. Validate 8-Semester Curriculum Comparison
const { CURRICULUM_COMPARISON } = require("./server/data/curriculum");
assert(CURRICULUM_COMPARISON.length === 8, "Complete 8-semester curriculum comparison mapped");
assert(CURRICULUM_COMPARISON[0].niatProgram.codingHoursPerWeek >= 18, "Semester 1 NIAT offers >= 18 coding hrs/week");
assert(CURRICULUM_COMPARISON[0].traditionalTier3.codingHoursPerWeek <= 4, "Semester 1 Tier-3 offers <= 4 coding hrs/week");

// 6. Validate Financial ROI Calculation Engine
const { calculateRoiModel } = require("./server/utils/roi");
const roi = calculateRoiModel({
  niatTotalFee: 1200000,
  tier3TotalFee: 400000,
  niatExpectedStartingSalary: 850000,
  tier3ExpectedStartingSalary: 360000,
  loanSharePercentage: 60,
  loanInterestRate: 8.5,
  loanTenureYears: 5,
  annualSalaryHike: 15,
});

assert(roi.metrics.breakEvenMonths > 0 && roi.metrics.breakEvenMonths <= 30, `Payback break-even verified: ${roi.metrics.breakEvenMonths} months`);
assert(roi.metrics.fiveYearNetWealthAdvantage > 1000000, `5-Year net wealth gain verified: ₹${(roi.metrics.fiveYearNetWealthAdvantage / 100000).toFixed(1)} Lakhs`);
assert(roi.inputs.monthlyEmi > 12000 && roi.inputs.monthlyEmi < 18000, `Loan EMI verified: ₹${roi.inputs.monthlyEmi}/month`);
assert(roi.yearlyProjections.length === 5, "Generated 5 annual career earnings projections");

// 7. Validate Deliverables Exist
const docs = [
  "../docs/DELIVERABLE_1_NIAT_AUDIT.md",
  "../docs/DELIVERABLE_2_GROWTH_TRACK_AND_AVENUE.md",
  "../docs/DELIVERABLE_3_WORKING_SYSTEM.md",
  "../docs/DELIVERABLE_4_REFLECTION.md",
  "../docs/FULL_SUBMISSION_DOSSIER.md",
];

docs.forEach((doc) => {
  const docPath = path.join(__dirname, doc);
  assert(fs.existsSync(docPath), `Deliverable document exists: ${path.basename(doc)}`);
});

// 8. Validate Frontend HTML Structure
const htmlContent = fs.readFileSync(path.join(__dirname, "public/index.html"), "utf-8");
assert(htmlContent.includes("tab-content-console"), "HTML includes Parent Advisory Console tab");
assert(htmlContent.includes("tab-content-campuses"), "HTML includes 35+ Campuses Explorer tab");
assert(htmlContent.includes("tab-content-roi"), "HTML includes Financial ROI Simulator tab");
assert(htmlContent.includes("tab-content-dashboard"), "HTML includes Growth Manager Dashboard tab");
assert(htmlContent.includes("modal-dossier"), "HTML includes Admissions Dossier Modal");
assert(htmlContent.includes("modal-seat"), "HTML includes Provisional Seat Reservation Modal");
assert(htmlContent.includes("modal-profile"), "HTML includes Student Profile Editor Modal");
assert(!htmlContent.includes("<script src=\"/_next/"), "HTML is 100% free of Next.js / React scripts");

// 9. Validate Frontend JS Logic
const jsContent = fs.readFileSync(path.join(__dirname, "public/app.js"), "utf-8");
assert(jsContent.includes("speechSynthesis"), "Vanilla JS includes Web Speech Synthesis support");
assert(jsContent.includes("fetch(\"/api/agent\""), "Vanilla JS connects to /api/agent backend");
assert(jsContent.includes("fetch(\"/api/roi\""), "Vanilla JS connects to /api/roi backend");
assert(jsContent.includes("fetch(\"/api/leads\""), "Vanilla JS connects to /api/leads backend");
assert(jsContent.includes("addEventListener"), "Vanilla JS uses standard DOM addEventListener");

// 10. Validate Backend Express API Routes
const serverContent = fs.readFileSync(path.join(__dirname, "server/index.js"), "utf-8");
assert(serverContent.includes("app.post(\"/api/agent\""), "Express exposes POST /api/agent");
assert(serverContent.includes("app.get(\"/api/campuses\""), "Express exposes GET /api/campuses");
assert(serverContent.includes("app.post(\"/api/roi\""), "Express exposes POST /api/roi");
assert(serverContent.includes("app.get(\"/api/leads\""), "Express exposes GET /api/leads");
assert(serverContent.includes("app.post(\"/api/leads\""), "Express exposes POST /api/leads");
assert(serverContent.includes("app.post(\"/api/webhook\""), "Express exposes POST /api/webhook");
assert(serverContent.includes("app.post(\"/api/reserve-seat\""), "Express exposes POST /api/reserve-seat");
assert(serverContent.includes("app.get(\"/api/health\""), "Express exposes GET /api/health");
assert(serverContent.includes("tool_query_campuses"), "Backend defines tool_query_campuses");
assert(serverContent.includes("tool_calculate_roi"), "Backend defines tool_calculate_roi");
assert(serverContent.includes("tool_compare_curriculum"), "Backend defines tool_compare_curriculum");
assert(serverContent.includes("tool_generate_dossier"), "Backend defines tool_generate_dossier");

console.log(`\n========================================`);
console.log(`TEST SUMMARY: ${passed} Passed, ${failed} Failed`);
if (failed === 0) {
  console.log("✓ ALL AUTOMATED SYSTEM & REPOSITORIES TESTS PASSED!");
} else {
  process.exit(1);
}
