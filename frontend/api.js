/**
 * NIAT ParentTrust AI — Frontend API Client Module
 * Technology: Vanilla JavaScript ES6+ fetch()
 *
 * This file centralizes all HTTP communication with the Python FastAPI backend.
 * Every function uses standard async/await and returns clean JSON data.
 */

const API_BASE = "";

/**
 * Consult the Autonomous Admissions Agent
 * Calls POST /api/agent with question prompt, language, profile, and objection category.
 */
async function apiConsultAgent(prompt, language, studentProfile, objectionCategory) {
  const response = await fetch(`${API_BASE}/api/agent`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      prompt,
      language: language || "en",
      studentProfile: studentProfile || {},
      objectionCategory: objectionCategory || "custom",
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || `Agent consultation failed (${response.status})`);
  }

  return await response.json();
}

/**
 * Query partner campuses with optional state, budget, natScore, or keyword filters
 * Calls GET /api/campuses
 */
async function apiGetCampuses(filters = {}) {
  const query = new URLSearchParams();
  if (filters.state && filters.state !== "All") query.append("state", filters.state);
  if (filters.maxBudget) query.append("maxBudget", filters.maxBudget);
  if (filters.minNatScore) query.append("minNatScore", filters.minNatScore);
  if (filters.keyword) query.append("keyword", filters.keyword);

  const url = `${API_BASE}/api/campuses${query.toString() ? "?" + query.toString() : ""}`;
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to load campuses (${response.status})`);
  }

  return await response.json();
}

/**
 * Calculate Financial ROI and loan EMI model
 * Calls POST /api/roi
 */
async function apiCalculateRoi(modelInputs) {
  const response = await fetch(`${API_BASE}/api/roi`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(modelInputs || {}),
  });

  if (!response.ok) {
    throw new Error(`ROI calculation failed (${response.status})`);
  }

  return await response.json();
}

/**
 * Retrieve Growth Dashboard telemetry & leads pipeline
 * Calls GET /api/leads
 */
async function apiGetLeadsTelemetry() {
  const response = await fetch(`${API_BASE}/api/leads`);
  if (!response.ok) {
    throw new Error(`Failed to load leads telemetry (${response.status})`);
  }
  return await response.json();
}

/**
 * Record a new lead session
 * Calls POST /api/leads
 */
async function apiRecordLead(leadData) {
  const response = await fetch(`${API_BASE}/api/leads`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(leadData),
  });

  if (!response.ok) {
    throw new Error(`Failed to record lead (${response.status})`);
  }

  return await response.json();
}

/**
 * Reserve a provisional seat with refundable token
 * Calls POST /api/reserve-seat
 */
async function apiReserveSeat(reservationData) {
  const response = await fetch(`${API_BASE}/api/reserve-seat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(reservationData),
  });

  if (!response.ok) {
    throw new Error(`Seat reservation failed (${response.status})`);
  }

  return await response.json();
}

/**
 * Trigger WhatsApp nurture webhook simulation
 * Calls POST /api/webhook
 */
async function apiTriggerWebhook(webhookPayload) {
  const response = await fetch(`${API_BASE}/api/webhook`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(webhookPayload),
  });

  if (!response.ok) {
    throw new Error(`Webhook dispatch failed (${response.status})`);
  }

  return await response.json();
}

/**
 * Check backend health & Groq AI status
 * Calls GET /api/health
 */
async function apiCheckHealth() {
  const response = await fetch(`${API_BASE}/api/health`);
  if (!response.ok) {
    throw new Error(`Health check failed (${response.status})`);
  }
  return await response.json();
}

// Export functions to window for vanilla global access
window.NIAT_API = {
  consultAgent: apiConsultAgent,
  getCampuses: apiGetCampuses,
  calculateRoi: apiCalculateRoi,
  getLeadsTelemetry: apiGetLeadsTelemetry,
  recordLead: apiRecordLead,
  reserveSeat: apiReserveSeat,
  triggerWebhook: apiTriggerWebhook,
  checkHealth: apiCheckHealth,
};
