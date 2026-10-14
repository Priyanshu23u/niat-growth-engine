/**
 * NIAT ParentTrust AI — Main Frontend Application
 * Technology: Vanilla JavaScript ES6+
 * No React, No frameworks, No build tools required.
 *
 * Architecture:
 *  - AppState: single source of truth (reactive-lite pattern)
 *  - init(): bootstraps all event listeners and initial renders
 *  - Each module has its own render/update function
 */

// ══════════════════════════════════════════════════════════════
// APP STATE
// ══════════════════════════════════════════════════════════════
const AppState = {
  currentLanguage: "te",          // default: Telugu (NxtWave heartland)
  activeTab: "console",
  isSpeaking: false,
  isLoadingAgent: false,
  agentResult: null,
  activeDossierData: null,
  selectedCampus: null,           // currently selected campus for seat modal
  studentProfile: {
    studentName: "Sai Teja Reddy",
    parentName: "K. Venkatesh",
    parentPhone: "+91 98480 23456",
    boardPercentage: 88,
    natScore: 82,
    state: "Telangana",
    budgetAnnual: 300000,
  },
  activeObjectionCategory: "accreditation",
};

// Shorthand helpers
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);
const setText = (sel, txt) => { const el = $(sel); if (el) el.textContent = txt; };
const setHTML = (sel, html) => { const el = $(sel); if (el) el.innerHTML = html; };
const show = (el) => { if (typeof el === "string") el = $(el); if (el) el.style.display = ""; };
const hide = (el) => { if (typeof el === "string") el = $(el); if (el) el.style.display = "none"; };

// ══════════════════════════════════════════════════════════════
// INIT — Entry point
// ══════════════════════════════════════════════════════════════
document.addEventListener("DOMContentLoaded", () => {
  AppState.selectedCampus = window.NIAT_DATA.CAMPUSES[0];
  bindNavTabs();
  bindLanguageSelector();
  bindProfileModal();
  bindSeatModal();
  bindDossierModal();
  bindVoiceButton();
  renderObjectionList();
  bindCustomQuestionForm();
  renderCampusGrid(window.NIAT_DATA.CAMPUSES);
  bindCampusFilters();
  initRoiSimulator();
  loadDashboard();
  updateNavStudentPill();
  updateHeroSection();
  // Auto-trigger first objection on load
  setTimeout(() => triggerObjection(window.NIAT_DATA.PARENT_OBJECTIONS[AppState.currentLanguage][0]), 300);
});

// ══════════════════════════════════════════════════════════════
// TAB NAVIGATION
// ══════════════════════════════════════════════════════════════
function bindNavTabs() {
  $$(".nav-tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tab = btn.dataset.tab;
      switchTab(tab);
    });
  });
}

function switchTab(tab) {
  AppState.activeTab = tab;
  // Update nav tab active state
  $$(".nav-tab").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.tab === tab);
  });
  // Show correct section
  $$(".tab-content").forEach((section) => {
    section.classList.toggle("active", section.id === `tab-content-${tab}`);
  });
}

// ══════════════════════════════════════════════════════════════
// LANGUAGE SELECTOR
// ══════════════════════════════════════════════════════════════
function bindLanguageSelector() {
  const sel = $("#lang-select");
  if (!sel) return;
  sel.addEventListener("change", (e) => {
    AppState.currentLanguage = e.target.value;
    renderObjectionList();
    updateHeroSection();
    updateConsoleUIStrings();
    // Re-trigger first objection for new language
    const objs = window.NIAT_DATA.PARENT_OBJECTIONS[AppState.currentLanguage];
    if (objs && objs.length) triggerObjection(objs[0]);
  });
}

function updateHeroSection() {
  const t = getUIStrings();
  const p = AppState.studentProfile;
  setText("#hero-title", t.heroTitle);
  setText("#hero-sub", t.heroSubtitle);
  setText("#hero-student-name", p.studentName);
  setText("#hero-board", `(12th Board: ${p.boardPercentage}%)`);
  setText("#hero-nat", `NAT Percentile: ${p.natScore}%`);
  setText("#hero-state", `State: ${p.state}`);
}

function updateConsoleUIStrings() {
  const t = getUIStrings();
  const langSel = $("#lang-select");
  const langCode = langSel ? langSel.value.toUpperCase() : "EN";

  setText("#custom-q-label", `Ask Any Custom Question in ${langCode}`);
  const placeholder = t.askQuestionPlaceholder;
  const ta = $("#custom-question");
  if (ta) ta.placeholder = placeholder;
  setText("#dossier-btn-text", t.downloadDossier);
  setText("#seat-btn-text", t.lockSeat);
  setText("#trace-label", t.agentReasoning);
  setText("#consult-btn-text", t.consultBtnText);
  setText("#metric-label-campuses", t.campusesFound);
  setText("#metric-label-breakeven", t.roiBreakEven);
  setText("#metric-label-wealth", t.wealthDelta);
}

function getUIStrings() {
  const lang = AppState.currentLanguage;
  return window.NIAT_DATA.UI_STRINGS[lang] || window.NIAT_DATA.UI_STRINGS.en;
}

// ══════════════════════════════════════════════════════════════
// OBJECTION LIST
// ══════════════════════════════════════════════════════════════
function renderObjectionList() {
  const container = $("#objection-list");
  if (!container) return;
  const objs = window.NIAT_DATA.PARENT_OBJECTIONS[AppState.currentLanguage] || window.NIAT_DATA.PARENT_OBJECTIONS.en;
  container.innerHTML = "";
  objs.forEach((obj) => {
    const btn = document.createElement("button");
    btn.className = "objection-btn" + (obj.category === AppState.activeObjectionCategory ? " active" : "");
    btn.setAttribute("data-category", obj.category);
    btn.innerHTML = `
      <div>
        <div class="obj-label">${escapeHTML(obj.label)}</div>
        <div class="obj-question">${escapeHTML(obj.question)}</div>
      </div>
      <svg class="obj-chevron" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="${obj.category === AppState.activeObjectionCategory ? "#60a5fa" : "#64748b"}" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
    `;
    btn.addEventListener("click", () => triggerObjection(obj));
    container.appendChild(btn);
  });
}

async function triggerObjection(obj) {
  AppState.activeObjectionCategory = obj.category;
  // Update active state on buttons
  $$(".objection-btn").forEach((btn) => {
    const isActive = btn.dataset.category === obj.category;
    btn.classList.toggle("active", isActive);
    const svg = btn.querySelector("svg");
    if (svg) svg.setAttribute("stroke", isActive ? "#60a5fa" : "#64748b");
  });
  // Update textarea
  const ta = $("#custom-question");
  if (ta) ta.value = obj.question;
  // Call agent
  await callAgent(obj.question, obj.category);
}

// ══════════════════════════════════════════════════════════════
// CUSTOM QUESTION FORM
// ══════════════════════════════════════════════════════════════
function bindCustomQuestionForm() {
  const consultBtn = $("#btn-consult-agent");
  if (consultBtn) {
    consultBtn.addEventListener("click", async () => {
      const q = $("#custom-question")?.value?.trim();
      if (!q || AppState.isLoadingAgent) return;
      await callAgent(q, "custom");
    });
  }
  // Allow Enter+Shift for new line, Enter alone = submit
  const ta = $("#custom-question");
  if (ta) {
    ta.addEventListener("keydown", async (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        const q = ta.value.trim();
        if (q && !AppState.isLoadingAgent) await callAgent(q, "custom");
      }
    });
  }
}

// ══════════════════════════════════════════════════════════════
// AGENT API CALL
// ══════════════════════════════════════════════════════════════
async function callAgent(prompt, objectionCategory = "custom") {
  if (AppState.isLoadingAgent) return;
  AppState.isLoadingAgent = true;

  const t = getUIStrings();
  const consultBtn = $("#btn-consult-agent");
  if (consultBtn) { consultBtn.disabled = true; setText("#consult-btn-text", t.consultingText || "Consulting..."); }

  // Show loading state in response card
  show("#response-loading");
  hide("#response-text");
  hide("#roi-metrics-bar");
  hide("#tool-trace");

  try {
    const res = await fetch("/api/agent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        language: AppState.currentLanguage,
        studentProfile: {
          name: AppState.studentProfile.studentName,
          parentName: AppState.studentProfile.parentName,
          boardPercentage: AppState.studentProfile.boardPercentage,
          natScore: AppState.studentProfile.natScore,
          state: AppState.studentProfile.state,
          budgetAnnual: AppState.studentProfile.budgetAnnual,
        },
        objectionCategory,
      }),
    });

    const data = await res.json();
    if (data.success) {
      AppState.agentResult = data;
      if (data.primaryCampus) AppState.selectedCampus = data.primaryCampus;
      renderAgentResponse(data);
    }
  } catch (err) {
    console.error("Agent API Error:", err);
    show("#response-text");
    setText("#response-text", "⚠️ Network error. Please check the server is running and try again.");
  } finally {
    AppState.isLoadingAgent = false;
    hide("#response-loading");
    show("#response-text");
    if (consultBtn) { consultBtn.disabled = false; setText("#consult-btn-text", t.consultBtnText || "Consult Agent"); }
  }
}

function renderAgentResponse(data) {
  // Update parent name in header
  setText("#response-for", `Targeted for ${AppState.studentProfile.parentName}`);

  // Set response text
  const responseText = $("#response-text");
  if (responseText) responseText.textContent = data.agentResponse || "No response available.";

  // Tool trace
  if (data.executedTools && data.executedTools.length) {
    setText("#model-tag", data.aiModelUsed || "NIAT Agent");
    const stepsEl = $("#tool-steps");
    if (stepsEl) {
      stepsEl.innerHTML = "";
      data.executedTools.forEach((tool) => {
        const step = document.createElement("div");
        step.className = "tool-step";
        step.innerHTML = `
          <div class="tool-step-name">
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
            ${escapeHTML(tool.toolName)}
          </div>
          <div class="tool-step-summary">${escapeHTML(tool.outputSummary)}</div>
        `;
        stepsEl.appendChild(step);
      });
    }
    show("#tool-trace");
  }

  // ROI Metrics Bar
  if (data.roiMetrics) {
    setText("#metric-campuses", `${data.matchedCampusesCount} Partner Campuses`);
    setText("#metric-breakeven", `${data.roiMetrics.breakEvenMonths} Months`);
    setText("#metric-wealth", `+₹${(data.roiMetrics.fiveYearNetWealthAdvantage / 100000).toFixed(1)} Lakhs`);
    show("#roi-metrics-bar");
  }
}

// ══════════════════════════════════════════════════════════════
// VOICE / TTS
// ══════════════════════════════════════════════════════════════
function bindVoiceButton() {
  const btn = $("#btn-voice");
  if (!btn) return;
  btn.addEventListener("click", toggleSpeech);
}

function toggleSpeech() {
  if (!("speechSynthesis" in window)) return;
  const btn = $("#btn-voice");
  if (AppState.isSpeaking) {
    window.speechSynthesis.cancel();
    AppState.isSpeaking = false;
    updateVoiceBtn(false);
  } else if (AppState.agentResult?.agentResponse) {
    const utterance = new SpeechSynthesisUtterance(AppState.agentResult.agentResponse);
    const langCodes = { en: "en-IN", te: "te-IN", ta: "ta-IN", hi: "hi-IN", kn: "kn-IN", ml: "ml-IN" };
    utterance.lang = langCodes[AppState.currentLanguage] || "en-IN";
    utterance.rate = 0.92;
    utterance.onend = () => { AppState.isSpeaking = false; updateVoiceBtn(false); };
    utterance.onerror = () => { AppState.isSpeaking = false; updateVoiceBtn(false); };
    window.speechSynthesis.speak(utterance);
    AppState.isSpeaking = true;
    updateVoiceBtn(true);
  }
}

function updateVoiceBtn(speaking) {
  const btn = $("#btn-voice");
  const textEl = $("#voice-btn-text");
  const iconOn = $("#voice-icon-on");
  const iconOff = $("#voice-icon-off");
  if (!btn) return;
  btn.classList.toggle("speaking", speaking);
  if (textEl) textEl.textContent = speaking ? "Mute Voice" : "Voice Read";
  if (iconOn) iconOn.style.display = speaking ? "none" : "";
  if (iconOff) iconOff.style.display = speaking ? "" : "none";
}

// ══════════════════════════════════════════════════════════════
// DOSSIER MODAL
// ══════════════════════════════════════════════════════════════
function bindDossierModal() {
  // Open buttons
  $("#btn-open-dossier")?.addEventListener("click", openDossierModal);
  // Close
  document.querySelectorAll("[data-modal='dossier']").forEach((btn) =>
    btn.addEventListener("click", () => hide("#modal-dossier"))
  );
  // Print
  $("#btn-print-dossier")?.addEventListener("click", () => window.print());
  // Dossier → Seat
  $("#btn-dossier-to-seat")?.addEventListener("click", () => {
    hide("#modal-dossier");
    openSeatModal();
  });
  // Close on overlay click
  $("#modal-dossier")?.addEventListener("click", (e) => {
    if (e.target === e.currentTarget) hide("#modal-dossier");
  });
}

function openDossierModal() {
  const data = AppState.agentResult?.dossierData;
  if (!data) return;
  AppState.activeDossierData = data;
  renderDossierContent(data);
  show("#modal-dossier");
}

function renderDossierContent(d) {
  setText("#dossier-id-text", `ID: ${d.dossierId} · Generated: ${d.generatedAt}`);
  const body = $("#dossier-body");
  if (!body) return;
  body.innerHTML = `
    <div class="dossier-section">
      <div class="dossier-section-title">Student & Campus Match</div>
      <div class="dossier-campus-box">
        <div class="dossier-campus-name">${escapeHTML(d.matchedCampus.name)}</div>
        <div class="dossier-meta">${escapeHTML(d.matchedCampus.city)}, ${escapeHTML(d.matchedCampus.state)}</div>
        <div class="dossier-meta" style="color:#34d399;margin-top:4px;">${escapeHTML(d.matchedCampus.accreditation)}</div>
        <div class="dossier-meta" style="margin-top:4px;">${escapeHTML(d.matchedCampus.degreeAwarded)}</div>
        <div class="dossier-meta" style="margin-top:4px;">Lab Pod: ${escapeHTML(d.matchedCampus.labPod)}</div>
        <div class="dossier-meta" style="margin-top:4px;">Annual Fee: ₹${(d.matchedCampus.annualFee / 100000).toFixed(1)} Lakhs · Total 4-Year: ₹${(d.matchedCampus.totalFeeFourYears / 100000).toFixed(1)} Lakhs</div>
      </div>
    </div>

    <div class="dossier-section">
      <div class="dossier-section-title">5-Year Financial ROI Snapshot (Estimated)</div>
      <div class="dossier-roi-grid">
        <div class="dossier-roi-item">
          <div class="dossier-roi-label">Estimated Starting Salary Target</div>
          <div class="dossier-roi-value green">${escapeHTML(d.roiHighlights.startingSalaryTarget)}</div>
        </div>
        <div class="dossier-roi-item">
          <div class="dossier-roi-label">Estimated Tier-3 Average Salary</div>
          <div class="dossier-roi-value" style="color:#94a3b8;">${escapeHTML(d.roiHighlights.tier3AverageSalary)}</div>
        </div>
        <div class="dossier-roi-item">
          <div class="dossier-roi-label">Estimated Monthly Loan EMI</div>
          <div class="dossier-roi-value amber">${escapeHTML(d.roiHighlights.monthlyEmiEstimate)}/mo</div>
        </div>
        <div class="dossier-roi-item">
          <div class="dossier-roi-label">Estimated Payback Period</div>
          <div class="dossier-roi-value blue">${escapeHTML(d.roiHighlights.paybackPeriodMonths)}</div>
        </div>
        <div class="dossier-roi-item" style="grid-column:1/-1;">
          <div class="dossier-roi-label">Estimated 5-Year Net Wealth Advantage</div>
          <div class="dossier-roi-value green" style="font-size:1.1rem;">+${escapeHTML(d.roiHighlights.fiveYearNetWealthAdvantage)}</div>
        </div>
      </div>
    </div>

    <div class="dossier-section">
      <div class="dossier-section-title">Dual Credential Guarantee</div>
      <div class="dossier-cred-list">
        ${d.dualCredentials.map((c) => `
          <div class="dossier-cred-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
            ${escapeHTML(c)}
          </div>`).join("")}
      </div>
    </div>

    <div class="dossier-section">
      <div class="dossier-next">
        <div class="dossier-next-title">⚡ Next Step: Lock Your Provisional Seat</div>
        <div class="dossier-next-meta">Reserve with ₹${d.nextStep.tokenAmount.toLocaleString("en-IN")} refundable token · Valid for ${d.nextStep.validityHours} hours · 100% refundable within ${d.nextStep.refundableWindowDays} days</div>
      </div>
    </div>

    <div class="dossier-section" style="padding-top:4px;">
      <div style="font-size:0.73rem; color:#94a3b8; line-height:1.45; border-top:1px solid rgba(255,255,255,0.08); padding-top:8px;">
        ℹ️ <strong>Disclaimer:</strong> ${escapeHTML(d.disclaimer || "Official Admissions Information Dossier generated by the NIAT ParentTrust AI Advisory Tool for planning purposes; not an admission offer issued directly by NIAT or host universities. Individual salary outcomes and career trajectories depend on academic performance and industry hiring.")}
      </div>
    </div>
  `;
}

// ══════════════════════════════════════════════════════════════
// SEAT RESERVATION MODAL
// ══════════════════════════════════════════════════════════════
function bindSeatModal() {
  $("#btn-open-seat")?.addEventListener("click", openSeatModal);
  document.querySelectorAll("[data-modal='seat']").forEach((btn) =>
    btn.addEventListener("click", () => {
      hide("#modal-seat");
      hide("#seat-success");
      show("#seat-form");
    })
  );
  $("#modal-seat")?.addEventListener("click", (e) => {
    if (e.target === e.currentTarget) hide("#modal-seat");
  });
  $("#seat-form")?.addEventListener("submit", handleSeatReservation);
}

function openSeatModal() {
  const campus = AppState.selectedCampus || window.NIAT_DATA.CAMPUSES[0];
  setText("#seat-campus-name", campus.name);
  // Pre-fill form
  const nameEl = $("#seat-student-name");
  const parentEl = $("#seat-parent-name");
  const phoneEl = $("#seat-parent-phone");
  if (nameEl) nameEl.value = AppState.studentProfile.studentName;
  if (parentEl) parentEl.value = AppState.studentProfile.parentName;
  if (phoneEl) phoneEl.value = AppState.studentProfile.parentPhone;
  hide("#seat-success");
  show("#seat-form");
  show("#modal-seat");
}

async function handleSeatReservation(e) {
  e.preventDefault();
  const campus = AppState.selectedCampus || window.NIAT_DATA.CAMPUSES[0];
  const submitText = $("#seat-submit-text");
  if (submitText) submitText.textContent = "Reserving...";

  try {
    const res = await fetch("/api/reserve-seat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        studentName: $("#seat-student-name")?.value,
        parentName: $("#seat-parent-name")?.value,
        parentPhone: $("#seat-parent-phone")?.value,
        campusId: campus.id,
      }),
    });
    const data = await res.json();
    if (data.success) {
      hide("#seat-form");
      const detail = $("#seat-success-detail");
      if (detail) detail.textContent = `Reservation ID: ${data.reservation.reservationId} · ${data.reservation.message}`;
      show("#seat-success");
    }
  } catch (err) {
    console.error("Seat reservation error:", err);
  } finally {
    if (submitText) submitText.textContent = "Reserve Provisional Seat";
  }
}

// ══════════════════════════════════════════════════════════════
// STUDENT PROFILE MODAL
// ══════════════════════════════════════════════════════════════
function bindProfileModal() {
  $("#btn-open-profile")?.addEventListener("click", openProfileModal);
  document.querySelectorAll("[data-modal='profile']").forEach((btn) =>
    btn.addEventListener("click", () => hide("#modal-profile"))
  );
  $("#modal-profile")?.addEventListener("click", (e) => {
    if (e.target === e.currentTarget) hide("#modal-profile");
  });
  // Range input live labels
  $("#prof-board")?.addEventListener("input", (e) => setText("#prof-board-lbl", `${e.target.value}%`));
  $("#prof-nat")?.addEventListener("input", (e) => setText("#prof-nat-lbl", `${e.target.value}%`));
  $("#prof-budget")?.addEventListener("input", (e) =>
    setText("#prof-budget-lbl", `₹${parseInt(e.target.value).toLocaleString("en-IN")}`)
  );
  // Save
  $("#btn-save-profile")?.addEventListener("click", saveProfile);
}

function openProfileModal() {
  const p = AppState.studentProfile;
  const nameEl = $("#prof-student-name");
  const parentEl = $("#prof-parent-name");
  const phoneEl = $("#prof-parent-phone");
  const boardEl = $("#prof-board");
  const natEl = $("#prof-nat");
  const stateEl = $("#prof-state");
  const budgetEl = $("#prof-budget");
  if (nameEl) nameEl.value = p.studentName;
  if (parentEl) parentEl.value = p.parentName;
  if (phoneEl) phoneEl.value = p.parentPhone;
  if (boardEl) { boardEl.value = p.boardPercentage; setText("#prof-board-lbl", `${p.boardPercentage}%`); }
  if (natEl) { natEl.value = p.natScore; setText("#prof-nat-lbl", `${p.natScore}%`); }
  if (stateEl) stateEl.value = p.state;
  if (budgetEl) { budgetEl.value = p.budgetAnnual; setText("#prof-budget-lbl", `₹${p.budgetAnnual.toLocaleString("en-IN")}`); }
  show("#modal-profile");
}

function saveProfile() {
  AppState.studentProfile = {
    studentName: $("#prof-student-name")?.value || AppState.studentProfile.studentName,
    parentName:  $("#prof-parent-name")?.value  || AppState.studentProfile.parentName,
    parentPhone: $("#prof-parent-phone")?.value || AppState.studentProfile.parentPhone,
    boardPercentage: parseInt($("#prof-board")?.value) || AppState.studentProfile.boardPercentage,
    natScore:    parseInt($("#prof-nat")?.value)       || AppState.studentProfile.natScore,
    state:       $("#prof-state")?.value               || AppState.studentProfile.state,
    budgetAnnual: parseInt($("#prof-budget")?.value)   || AppState.studentProfile.budgetAnnual,
  };
  hide("#modal-profile");
  updateNavStudentPill();
  updateHeroSection();
  // Re-trigger consultation with new profile
  const objs = window.NIAT_DATA.PARENT_OBJECTIONS[AppState.currentLanguage];
  if (objs?.length) triggerObjection(objs[0]);
}

function updateNavStudentPill() {
  const p = AppState.studentProfile;
  setText("#nav-student-name", p.studentName);
  setText("#nav-student-meta", `NAT: ${p.natScore}% · ${p.state}`);
}

// ══════════════════════════════════════════════════════════════
// CAMPUS EXPLORER
// ══════════════════════════════════════════════════════════════
function renderCampusGrid(campuses) {
  const grid = $("#campus-grid");
  if (!grid) return;
  if (!campuses || campuses.length === 0) {
    grid.innerHTML = `<div style="grid-column:1/-1;text-align:center;padding:40px;color:var(--text-muted);">No campuses match your filters. Try broadening your search.</div>`;
    return;
  }
  grid.innerHTML = "";
  campuses.forEach((campus) => {
    const card = document.createElement("div");
    card.className = "glass-panel campus-card fade-in";
    const annualLakhs = (campus.totalAnnualFee / 100000).toFixed(1);
    const totalLakhs = (campus.totalFourYearFee / 100000).toFixed(1);
    card.innerHTML = `
      <div class="campus-card-header">
        <div>
          <div class="campus-name">${escapeHTML(campus.name)}</div>
          <div class="campus-region">${escapeHTML(campus.city)} · ${escapeHTML(campus.state)} · Est. ${campus.establishedYear}</div>
        </div>
        <span class="badge ${campus.region === 'South' ? 'badge-teal' : campus.region === 'West' ? 'badge-amber' : 'badge-blue'}">${escapeHTML(campus.region)}</span>
      </div>

      <div class="campus-accreditation">
        ${campus.ugcApproved ? '<span class="badge badge-teal">UGC ✓</span>' : ''}
        ${campus.aicteApproved ? '<span class="badge badge-blue">AICTE ✓</span>' : ''}
      </div>

      <div class="campus-degree">${escapeHTML(campus.degreeAwarded)}</div>

      <div class="campus-specs">
        <div class="campus-spec">
          <div class="spec-label">Annual Fee</div>
          <div class="spec-value blue">₹${annualLakhs}L / yr</div>
        </div>
        <div class="campus-spec">
          <div class="spec-label">4-Year Total</div>
          <div class="spec-value">₹${totalLakhs}L</div>
        </div>
        <div class="campus-spec">
          <div class="spec-label">Min NAT Score</div>
          <div class="spec-value amber">${campus.minNatPercentile}+ Percentile</div>
        </div>
        <div class="campus-spec">
          <div class="spec-label">Min Board %</div>
          <div class="spec-value">${campus.minBoardPercentage}%+</div>
        </div>
      </div>

      <div class="campus-highlight">${escapeHTML(campus.featuredHighlight)}</div>

      <div class="campus-card-footer">
        <button class="btn-secondary" onclick="selectCampusForConsultation('${campus.id}')">Consult on This Campus</button>
        <button class="btn-primary"   onclick="lockSeatForCampus('${campus.id}')">Reserve Seat</button>
      </div>
    `;
    grid.appendChild(card);
  });
}

// Called from campus card buttons (global scope)
window.selectCampusForConsultation = function(campusId) {
  const campus = window.NIAT_DATA.CAMPUSES.find((c) => c.id === campusId);
  if (campus) {
    AppState.selectedCampus = campus;
    switchTab("console");
    // Trigger ROI or campus matching objection
    const objs = window.NIAT_DATA.PARENT_OBJECTIONS[AppState.currentLanguage];
    const campusObj = objs?.find((o) => o.category === "campus_matching");
    if (campusObj) triggerObjection(campusObj);
  }
};

window.lockSeatForCampus = function(campusId) {
  const campus = window.NIAT_DATA.CAMPUSES.find((c) => c.id === campusId);
  if (campus) {
    AppState.selectedCampus = campus;
    openSeatModal();
  }
};

function bindCampusFilters() {
  const btn = $("#btn-filter-campuses");
  if (btn) btn.addEventListener("click", filterCampuses);
  // Live filter on Enter
  $("#filter-keyword")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") filterCampuses();
  });
}

async function filterCampuses() {
  const state = $("#filter-state")?.value;
  const budget = $("#filter-budget")?.value;
  const keyword = $("#filter-keyword")?.value?.trim();

  try {
    const params = new URLSearchParams();
    if (state && state !== "All") params.set("state", state);
    if (budget) params.set("maxBudget", budget);
    if (keyword) params.set("keyword", keyword);

    const res = await fetch(`/api/campuses?${params.toString()}`);
    const data = await res.json();
    if (data.success) renderCampusGrid(data.campuses);
  } catch (err) {
    // Fallback to client-side filter
    const campuses = window.NIAT_DATA.CAMPUSES.filter((c) => {
      if (state && state !== "All" && c.state !== state) return false;
      if (budget && c.totalAnnualFee > parseInt(budget)) return false;
      if (keyword) {
        const kw = keyword.toLowerCase();
        return c.name.toLowerCase().includes(kw) || c.city.toLowerCase().includes(kw) || c.state.toLowerCase().includes(kw);
      }
      return true;
    });
    renderCampusGrid(campuses);
  }
}

// ══════════════════════════════════════════════════════════════
// ROI SIMULATOR
// ══════════════════════════════════════════════════════════════
function initRoiSimulator() {
  const sliders = ["niat-fee","tier3-fee","niat-salary","tier3-salary","loan-pct"];
  sliders.forEach((id) => {
    const el = $(`#slider-${id}`);
    if (el) el.addEventListener("input", () => updateRoiDisplay());
  });
  updateRoiDisplay();
}

async function updateRoiDisplay() {
  const niatFee    = parseInt($("#slider-niat-fee")?.value   || 1200000);
  const tier3Fee   = parseInt($("#slider-tier3-fee")?.value  || 400000);
  const niatSal    = parseInt($("#slider-niat-salary")?.value || 850000);
  const tier3Sal   = parseInt($("#slider-tier3-salary")?.value|| 360000);
  const loanPct    = parseInt($("#slider-loan-pct")?.value   || 60);

  // Update slider labels
  setText("#lbl-niat-fee",   `₹${(niatFee / 100000).toFixed(1)} Lakhs`);
  setText("#lbl-tier3-fee",  `₹${(tier3Fee / 100000).toFixed(1)} Lakhs`);
  setText("#lbl-niat-salary",`Estimated ₹${(niatSal / 100000).toFixed(1)} LPA`);
  setText("#lbl-tier3-salary",`Estimated ₹${(tier3Sal / 100000).toFixed(1)} LPA`);
  setText("#lbl-loan-pct-label", `Education Loan Share: ${loanPct}%`);

  try {
    const res = await fetch("/api/roi", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        niatTotalFee: niatFee,
        tier3TotalFee: tier3Fee,
        niatExpectedStartingSalary: niatSal,
        tier3ExpectedStartingSalary: tier3Sal,
        loanSharePercentage: loanPct,
        loanInterestRate: 8.5,
        loanTenureYears: 5,
      }),
    });
    const data = await res.json();
    if (data.success !== false) renderRoiResults(data, niatSal, tier3Sal);
  } catch (err) {
    // Fallback: compute client-side
    const roi = clientCalcRoi(niatFee, tier3Fee, niatSal, tier3Sal, loanPct);
    renderRoiResults(roi, niatSal, tier3Sal);
  }
}

function renderRoiResults(data, niatSal, tier3Sal) {
  setText("#lbl-emi", `EMI: ₹${data.inputs.monthlyEmi.toLocaleString("en-IN")}/mo`);
  setText("#roi-breakeven", `${data.metrics.breakEvenMonths} Months`);
  setText("#roi-breakeven-yrs", `(${data.metrics.breakEvenYears} Years post-grad)`);
  setText("#roi-wealth", `+₹${(data.metrics.fiveYearNetWealthAdvantage / 100000).toFixed(1)} Lakhs`);
  setText("#roi-year1-delta", `+₹${((niatSal - tier3Sal) / 100000).toFixed(1)} LPA`);
  setText("#roi-monthly-delta", `+₹${Math.round((niatSal - tier3Sal) / 12).toLocaleString("en-IN")}/month`);

  // Bar chart
  const chartEl = $("#roi-chart-bars");
  if (!chartEl || !data.yearlyProjections) return;
  chartEl.innerHTML = "";
  data.yearlyProjections.forEach((proj) => {
    const maxVal = Math.max(Math.abs(proj.niatNetCumulativeWealth), Math.abs(proj.tier3NetCumulativeWealth), 3500000);
    const niatW = Math.max(5, Math.min(100, (Math.max(0, proj.niatNetCumulativeWealth) / maxVal) * 100));
    const tier3W = Math.max(5, Math.min(100, (Math.max(0, proj.tier3NetCumulativeWealth) / maxVal) * 100));
    const advantage = proj.netWealthAdvantage;
    const row = document.createElement("div");
    row.className = "year-projection";
    row.innerHTML = `
      <div class="year-header">
        <strong>Year ${proj.year} Post-Graduation</strong>
        <span class="year-advantage">Advantage: +₹${(advantage / 100000).toFixed(1)}L</span>
      </div>
      <div class="bar-row">
        <span class="bar-label bar-niat-lbl">NIAT</span>
        <div class="bar-track"><div class="bar-fill bar-fill-niat" style="width:${niatW}%;"></div></div>
        <span class="bar-val">₹${(proj.niatNetCumulativeWealth / 100000).toFixed(1)}L</span>
      </div>
      <div class="bar-row">
        <span class="bar-label bar-tier3-lbl">Tier-3</span>
        <div class="bar-track"><div class="bar-fill bar-fill-tier3" style="width:${tier3W}%;"></div></div>
        <span class="bar-val">₹${(proj.tier3NetCumulativeWealth / 100000).toFixed(1)}L</span>
      </div>
    `;
    chartEl.appendChild(row);
  });
}

// Simple client-side ROI fallback (no server call)
function clientCalcRoi(niatFee, tier3Fee, niatSal, tier3Sal, loanPct) {
  const principal = niatFee * (loanPct / 100);
  const rate = 0.085 / 12;
  const n = 60;
  const emi = rate === 0 ? Math.round(principal / n) : Math.round(principal * rate * Math.pow(1+rate,n) / (Math.pow(1+rate,n)-1));
  const projections = [];
  let nc = -niatFee, tc = -tier3Fee;
  let ns = niatSal, ts = tier3Sal;
  for (let y = 1; y <= 5; y++) {
    const emiD = y <= 5 ? emi * 12 : 0;
    nc += ns * 0.88 - emiD;
    tc += ts * 0.94;
    projections.push({ year:y, niatNetCumulativeWealth:Math.round(nc), tier3NetCumulativeWealth:Math.round(tc), netWealthAdvantage:Math.round(nc-tc) });
    ns *= 1.15; ts *= 1.07;
  }
  const breakEven = Math.max(12, Math.round((niatFee - tier3Fee + emi*n - principal) / ((niatSal - tier3Sal) / 12)));
  return {
    success: true,
    inputs: { monthlyEmi: emi },
    metrics: { breakEvenMonths: breakEven, breakEvenYears: (breakEven/12).toFixed(1), fiveYearNetWealthAdvantage: projections[4].netWealthAdvantage },
    yearlyProjections: projections,
  };
}

// ══════════════════════════════════════════════════════════════
// GROWTH DASHBOARD
// ══════════════════════════════════════════════════════════════
async function loadDashboard() {
  try {
    const res = await fetch("/api/leads");
    const data = await res.json();
    if (data.success) {
      renderLeadsTable(data.leads);
      setText("#leads-count-badge", `${data.leads.length} Live Leads`);
    }
  } catch (err) {
    console.error("Dashboard load error:", err);
    setText("#leads-count-badge", "Server Offline");
  }
  bindWebhookTest();
}

function renderLeadsTable(leads) {
  const tbody = $("#leads-table-body");
  if (!tbody) return;
  tbody.innerHTML = "";
  leads.forEach((lead) => {
    const statusClass = {
      converted: "status-converted",
      dossier_sent: "status-dossier",
      seat_reserved: "status-seat",
      in_consultation: "status-consult",
      cold: "status-cold",
    }[lead.status] || "status-cold";

    const statusLabel = {
      converted: "✅ Converted",
      dossier_sent: "📄 Dossier Sent",
      seat_reserved: "🔒 Seat Reserved",
      in_consultation: "💬 Consulting",
      cold: "❄️ Cold",
    }[lead.status] || lead.status;

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${escapeHTML(lead.studentName)}</td>
      <td>${escapeHTML(lead.parentName)}</td>
      <td><span class="badge badge-blue" style="font-size:0.65rem;">${lead.language.toUpperCase()}</span></td>
      <td>${escapeHTML(lead.state)}</td>
      <td>${lead.natScore}%</td>
      <td><span class="status-pill ${statusClass}">${statusLabel}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

function bindWebhookTest() {
  const btn = $("#btn-trigger-webhook");
  if (!btn) return;
  btn.addEventListener("click", async () => {
    setText("#webhook-btn-text", "Sending...");
    btn.disabled = true;
    try {
      const res = await fetch("/api/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "TEST_GROWTH_EXPERIMENT_DISPATCH",
          leadData: { parentName: "S. Rama Rao", studentName: "Tarun Kumar", parentPhone: "+91 98490 99887" },
          language: AppState.currentLanguage,
          dossierUrl: "https://niatindia.com/dossier/NIAT-DOSSIER-DEMO",
        }),
      });
      const data = await res.json();
      const logEl = $("#webhook-log");
      if (logEl) {
        logEl.textContent = JSON.stringify(data.dispatch, null, 2);
        show(logEl);
      }
    } catch (err) {
      const logEl = $("#webhook-log");
      if (logEl) { logEl.textContent = "Error: " + err.message; show(logEl); }
    } finally {
      setText("#webhook-btn-text", "Send Test Dispatch");
      btn.disabled = false;
    }
  });
}

// ══════════════════════════════════════════════════════════════
// UTILITIES
// ══════════════════════════════════════════════════════════════
function escapeHTML(str) {
  if (str == null) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
